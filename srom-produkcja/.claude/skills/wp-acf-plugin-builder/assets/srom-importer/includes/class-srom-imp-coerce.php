<?php
/**
 * Field-type-aware value validation and conversion.
 *
 * Contract: coerce() never throws and never returns a value that would
 * corrupt an ACF field. A cell either converts cleanly ('ok'), or the field
 * is skipped for that row with an explanatory message ('skip') while the
 * rest of the row still imports.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Coerce {

	/**
	 * @param array  $field ACF field array (needs at least type; choices etc. as applicable).
	 * @param string $raw   trimmed cell value (non-empty; empty cells are policy-handled by the runner).
	 * @param array  $ctx   ['runner'=>SROM_Imp_Runner|null, 'dry'=>bool, 'options'=>array, 'row_assoc'=>array]
	 * @return array ['status'=>'ok'|'skip', 'value'=>mixed, 'msgs'=>string[]]
	 */
	public static function coerce( array $field, $raw, array $ctx ) {
		try {
			return self::do_coerce( $field, (string) $raw, $ctx );
		} catch ( Throwable $e ) {
			return self::skip( 'unexpected error while converting the value (' . $e->getMessage() . ')' );
		}
	}

	private static function ok( $value, array $msgs = array() ) {
		return array( 'status' => 'ok', 'value' => $value, 'msgs' => $msgs );
	}

	private static function skip( $msg ) {
		return array( 'status' => 'skip', 'value' => null, 'msgs' => array( $msg ) );
	}

	private static function do_coerce( array $field, $raw, array $ctx ) {
		$type   = isset( $field['type'] ) ? $field['type'] : 'text';
		$runner = isset( $ctx['runner'] ) ? $ctx['runner'] : null;

		switch ( $type ) {

			case 'text':
			case 'password':
				return self::ok( $raw );

			case 'textarea':
				return self::ok( str_replace( "\r\n", "\n", $raw ) );

			case 'wysiwyg':
				return self::ok( wp_kses_post( str_replace( "\r\n", "\n", $raw ) ) );

			case 'email':
				if ( ! is_email( $raw ) ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a valid e-mail address — field skipped' );
				}
				return self::ok( $raw );

			case 'url':
			case 'oembed':
				$url = esc_url_raw( $raw );
				if ( '' === $url ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a valid URL — field skipped' );
				}
				return self::ok( $url );

			case 'number':
			case 'range':
				$num = self::parse_number( $raw );
				if ( null === $num ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a number — field skipped' );
				}
				$msgs = array();
				if ( isset( $field['min'] ) && '' !== (string) $field['min'] && $num < (float) $field['min'] ) {
					$msgs[] = 'value ' . $num . ' is below the field minimum (' . $field['min'] . ') — imported anyway';
				}
				if ( isset( $field['max'] ) && '' !== (string) $field['max'] && $num > (float) $field['max'] ) {
					$msgs[] = 'value ' . $num . ' is above the field maximum (' . $field['max'] . ') — imported anyway';
				}
				return self::ok( $num, $msgs );

			case 'true_false':
				$b = self::parse_bool( $raw );
				if ( null === $b ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a recognized yes/no value — field skipped' );
				}
				return self::ok( $b ? 1 : 0 );

			case 'select':
			case 'radio':
			case 'button_group':
				$choices = (array) ( isset( $field['choices'] ) ? $field['choices'] : array() );
				if ( ! empty( $field['multiple'] ) && 'select' === $type ) {
					return self::match_choices_multi( $raw, $choices, $field );
				}
				$hit = self::match_choice( $raw, $choices );
				if ( null === $hit ) {
					if ( ! empty( $field['allow_custom'] ) ) {
						return self::ok( $raw, array( '"' . self::shorten( $raw ) . '" is not a predefined choice — imported as a custom value' ) );
					}
					return self::skip( '"' . self::shorten( $raw ) . '" does not match any choice of "' . $field['label'] . '" — field skipped' );
				}
				return self::ok( $hit );

			case 'checkbox':
				return self::match_choices_multi( $raw, (array) ( isset( $field['choices'] ) ? $field['choices'] : array() ), $field );

			case 'date_picker':
				$dt = self::parse_date( $raw );
				if ( ! $dt ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a recognizable date — field skipped' );
				}
				return self::ok( $dt->format( 'Ymd' ) );

			case 'date_time_picker':
				$dt = self::parse_date( $raw, true );
				if ( ! $dt ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a recognizable date/time — field skipped' );
				}
				return self::ok( $dt->format( 'Y-m-d H:i:s' ) );

			case 'time_picker':
				foreach ( array( 'H:i:s', 'H:i', 'g:i a', 'g:ia' ) as $fmt ) {
					$dt = DateTime::createFromFormat( '!' . $fmt, $raw );
					if ( $dt && self::clean_parse() ) {
						return self::ok( $dt->format( 'H:i:s' ) );
					}
				}
				return self::skip( '"' . self::shorten( $raw ) . '" is not a recognizable time — field skipped' );

			case 'color_picker':
				$c = ltrim( $raw, '#' );
				if ( ! preg_match( '/^[0-9a-f]{3}([0-9a-f]{3})?([0-9a-f]{2})?$/i', $c ) ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a hex color — field skipped' );
				}
				return self::ok( '#' . strtolower( $c ) );

			case 'post_object':
			case 'relationship':
			case 'page_link':
				if ( ! $runner ) {
					return self::skip( 'related posts cannot be resolved in this context' );
				}
				$multiple = ( 'relationship' === $type ) || ! empty( $field['multiple'] );
				$tokens   = $multiple ? self::split_multi( $raw, false ) : array( $raw );
				$ids      = array();
				$msgs     = array();
				foreach ( $tokens as $tok ) {
					$res = $runner->resolve_post( $field, $tok );
					if ( null !== $res['id'] ) {
						$ids[] = $res['id'];
					}
					foreach ( $res['msgs'] as $m ) {
						$msgs[] = $m;
					}
					if ( null === $res['id'] && ! $res['deferred'] ) {
						// unresolved token -> whole field is skipped for safety
						return array( 'status' => 'skip', 'value' => null, 'msgs' => $msgs );
					}
				}
				if ( $multiple ) {
					return self::ok( $ids, $msgs );
				}
				return empty( $ids )
					? array( 'status' => 'skip', 'value' => null, 'msgs' => $msgs ) // dry-run "would create"
					: self::ok( $ids[0], $msgs );

			case 'taxonomy':
				if ( ! $runner ) {
					return self::skip( 'terms cannot be resolved in this context' );
				}
				return $runner->resolve_terms( $field, self::split_multi( $raw, true ) );

			case 'user':
				$multiple = ! empty( $field['multiple'] );
				$tokens   = $multiple ? self::split_multi( $raw, true ) : array( $raw );
				$ids      = array();
				foreach ( $tokens as $tok ) {
					$u = null;
					if ( preg_match( '/^\d+$/', $tok ) ) {
						$u = get_user_by( 'id', (int) $tok );
					}
					if ( ! $u && is_email( $tok ) ) {
						$u = get_user_by( 'email', $tok );
					}
					if ( ! $u ) {
						$u = get_user_by( 'login', $tok );
					}
					if ( ! $u ) {
						return self::skip( 'user "' . self::shorten( $tok ) . '" not found — field skipped' );
					}
					$ids[] = $u->ID;
				}
				return self::ok( $multiple ? $ids : $ids[0] );

			case 'file':
			case 'image':
				if ( ! $runner ) {
					return self::skip( 'attachments cannot be resolved in this context' );
				}
				$res = $runner->resolve_attachment( $raw, ( 'image' === $type ) );
				if ( null === $res['id'] ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => $res['msgs'] );
				}
				return self::ok( $res['id'], $res['msgs'] );

			case 'gallery':
				if ( ! $runner ) {
					return self::skip( 'attachments cannot be resolved in this context' );
				}
				$ids  = array();
				$msgs = array();
				foreach ( self::split_multi( $raw, false ) as $tok ) {
					$res = $runner->resolve_attachment( $tok, false );
					foreach ( $res['msgs'] as $m ) {
						$msgs[] = $m;
					}
					if ( null === $res['id'] ) {
						return array( 'status' => 'skip', 'value' => null, 'msgs' => $msgs );
					}
					$ids[] = $res['id'];
				}
				return self::ok( $ids, $msgs );

			case 'google_map':
				$json = json_decode( $raw, true );
				if ( is_array( $json ) && isset( $json['lat'], $json['lng'] ) ) {
					return self::ok(
						array(
							'address' => isset( $json['address'] ) ? (string) $json['address'] : '',
							'lat'     => (float) $json['lat'],
							'lng'     => (float) $json['lng'],
						)
					);
				}
				if ( preg_match( '/^(-?\d+(?:[.,]\d+)?)\s*,\s*(-?\d+(?:[.,]\d+)?)$/', $raw, $m ) ) {
					return self::ok(
						array(
							'address' => '',
							'lat'     => (float) str_replace( ',', '.', $m[1] ),
							'lng'     => (float) str_replace( ',', '.', $m[2] ),
						)
					);
				}
				return self::skip( '"' . self::shorten( $raw ) . '" is not "lat, lng" or JSON with lat/lng — field skipped' );

			case 'link':
				$json = json_decode( $raw, true );
				if ( is_array( $json ) && ! empty( $json['url'] ) ) {
					return self::ok(
						array(
							'url'    => esc_url_raw( (string) $json['url'] ),
							'title'  => isset( $json['title'] ) ? (string) $json['title'] : '',
							'target' => isset( $json['target'] ) ? (string) $json['target'] : '',
						)
					);
				}
				$url = esc_url_raw( $raw );
				if ( '' === $url ) {
					return self::skip( '"' . self::shorten( $raw ) . '" is not a valid URL — field skipped' );
				}
				return self::ok( array( 'url' => $url, 'title' => '', 'target' => '' ) );

			default:
				// Unknown / future field type: store the raw string rather than lose data.
				return self::ok( $raw, array( 'field type "' . $type . '" is not specifically supported — imported as plain text' ) );
		}
	}

	/* ------------------------------------------------------------ helpers */

	public static function shorten( $v, $len = 60 ) {
		$v = (string) $v;
		if ( function_exists( 'mb_strlen' ) && mb_strlen( $v ) > $len ) {
			return mb_substr( $v, 0, $len ) . '…';
		}
		if ( strlen( $v ) > $len ) {
			return substr( $v, 0, $len ) . '…';
		}
		return $v;
	}

	/**
	 * "11", "11,5", "1 234,5" (NBSP thousands) -> float|int. null when not numeric.
	 */
	public static function parse_number( $raw ) {
		$v = str_replace( array( "\xC2\xA0", ' ' ), '', (string) $raw );
		if ( substr_count( $v, ',' ) === 1 && false === strpos( $v, '.' ) ) {
			$v = str_replace( ',', '.', $v );
		}
		if ( ! is_numeric( $v ) ) {
			return null;
		}
		return ( false === strpos( $v, '.' ) && false === stripos( $v, 'e' ) ) ? (int) $v : (float) $v;
	}

	/**
	 * @return bool|null
	 */
	public static function parse_bool( $raw ) {
		$v = function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( (string) $raw ) ) : strtolower( trim( (string) $raw ) );
		if ( in_array( $v, array( '1', 'true', 'yes', 'y', 'tak', 'prawda', 'on', 'x' ), true ) ) {
			return true;
		}
		if ( in_array( $v, array( '0', 'false', 'no', 'n', 'nie', 'fałsz', 'falsz', 'off', '-' ), true ) ) {
			return false;
		}
		return null;
	}

	/**
	 * Tolerant date parsing: explicit formats only (no free-form guessing),
	 * plus Excel serial numbers (10000–80000 ≈ years 1927–2119, so a bare
	 * "2025" is never mistaken for a serial).
	 *
	 * @return DateTime|null
	 */
	public static function parse_date( $raw, $with_time = false ) {
		$raw = trim( (string) $raw );

		if ( preg_match( '/^\d{5}(\.\d+)?$/', $raw ) || ( preg_match( '/^\d{4,5}(\.\d+)?$/', $raw ) && (float) $raw >= 10000 && (float) $raw <= 80000 ) ) {
			$serial = (float) $raw;
			if ( $serial >= 10000 && $serial <= 80000 ) {
				$days = (int) floor( $serial );
				$secs = (int) round( ( $serial - $days ) * 86400 );
				$dt   = DateTime::createFromFormat( '!Y-m-d', '1899-12-30' );
				if ( $dt ) {
					$dt->modify( '+' . $days . ' days' );
					if ( $secs > 0 ) {
						$dt->modify( '+' . $secs . ' seconds' );
					}
					return $dt;
				}
			}
		}

		$formats = $with_time
			? array( 'Y-m-d H:i:s', 'Y-m-d H:i', 'Y-m-d\TH:i:s', 'Y-m-d\TH:i', 'd.m.Y H:i:s', 'd.m.Y H:i', 'd/m/Y H:i', 'Y-m-d', 'Ymd', 'd.m.Y', 'd/m/Y', 'Y/m/d', 'd-m-Y' )
			: array( 'Y-m-d', 'Ymd', 'd.m.Y', 'd/m/Y', 'Y/m/d', 'd-m-Y', 'Y-m-d H:i:s', 'Y-m-d\TH:i:s' );

		foreach ( $formats as $fmt ) {
			$dt = DateTime::createFromFormat( '!' . $fmt, $raw );
			if ( $dt && self::clean_parse() ) {
				return $dt;
			}
		}
		return null;
	}

	/**
	 * True when the last createFromFormat had no errors or warnings
	 * (rejects things like 2025-13-45 that PHP would otherwise roll over).
	 */
	private static function clean_parse() {
		$err = DateTime::getLastErrors();
		if ( ! is_array( $err ) ) {
			return true; // PHP 8.2+: returns false when there are none.
		}
		return empty( $err['warning_count'] ) && empty( $err['error_count'] );
	}

	/**
	 * Split a multi-value cell. New lines win, then ";", then "," (only if
	 * commas are allowed for this context — post titles may contain commas).
	 */
	public static function split_multi( $raw, $allow_comma = true ) {
		$raw = (string) $raw;
		if ( false !== strpos( $raw, "\n" ) ) {
			$parts = preg_split( '/\r?\n/', $raw );
		} elseif ( false !== strpos( $raw, ';' ) ) {
			$parts = explode( ';', $raw );
		} elseif ( $allow_comma && false !== strpos( $raw, ',' ) ) {
			$parts = explode( ',', $raw );
		} else {
			$parts = array( $raw );
		}
		$out = array();
		foreach ( (array) $parts as $p ) {
			$p = SROM_Imp_Spreadsheet::clean_cell( $p );
			if ( '' !== $p ) {
				$out[] = $p;
			}
		}
		return $out;
	}

	private static function match_choice( $raw, array $choices ) {
		foreach ( $choices as $val => $label ) {
			if ( (string) $val === $raw ) {
				return (string) $val;
			}
		}
		$raw_l = function_exists( 'mb_strtolower' ) ? mb_strtolower( $raw ) : strtolower( $raw );
		foreach ( $choices as $val => $label ) {
			$v_l = function_exists( 'mb_strtolower' ) ? mb_strtolower( (string) $val ) : strtolower( (string) $val );
			if ( $v_l === $raw_l ) {
				return (string) $val;
			}
		}
		foreach ( $choices as $val => $label ) {
			if ( (string) $label === $raw ) {
				return (string) $val;
			}
		}
		foreach ( $choices as $val => $label ) {
			$l_l = function_exists( 'mb_strtolower' ) ? mb_strtolower( (string) $label ) : strtolower( (string) $label );
			if ( $l_l === $raw_l ) {
				return (string) $val;
			}
		}
		return null;
	}

	private static function match_choices_multi( $raw, array $choices, array $field ) {
		$vals = array();
		$msgs = array();
		foreach ( self::split_multi( $raw, true ) as $tok ) {
			$hit = self::match_choice( $tok, $choices );
			if ( null === $hit ) {
				if ( ! empty( $field['allow_custom'] ) ) {
					$vals[] = $tok;
					$msgs[] = '"' . self::shorten( $tok ) . '" imported as a custom choice';
					continue;
				}
				return self::skip( '"' . self::shorten( $tok ) . '" does not match any choice of "' . $field['label'] . '" — field skipped' );
			}
			$vals[] = $hit;
		}
		return self::ok( array_values( array_unique( $vals ) ), $msgs );
	}
}
