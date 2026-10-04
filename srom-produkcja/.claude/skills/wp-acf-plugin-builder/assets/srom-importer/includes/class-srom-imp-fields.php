<?php
/**
 * Target discovery (core post fields + ACF fields of the chosen post type)
 * and automatic column -> field mapping, including the SROM preset that
 * knows the master-spreadsheet column names.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Fields {

	/**
	 * ACF field types this importer cannot fill (layout / ACF-Pro structures).
	 */
	const UNSUPPORTED_TYPES = array( 'repeater', 'flexible_content', 'group', 'clone', 'message', 'tab', 'accordion' );

	public static function acf_active() {
		return function_exists( 'acf_get_field_groups' ) && function_exists( 'acf_get_fields' ) && function_exists( 'update_field' );
	}

	/**
	 * Post types offered in the importer.
	 *
	 * @return array slug => label
	 */
	public static function post_types() {
		$exclude = array(
			'attachment', 'revision', 'nav_menu_item', 'custom_css', 'customize_changeset',
			'oembed_cache', 'user_request', 'wp_block', 'wp_template', 'wp_template_part',
			'wp_global_styles', 'wp_navigation', 'wp_font_family', 'wp_font_face',
			'acf-field', 'acf-field-group', 'acf-post-type', 'acf-taxonomy', 'acf-ui-options-page',
		);
		$out     = array();
		foreach ( get_post_types( array( 'show_ui' => true ), 'objects' ) as $pt ) {
			if ( in_array( $pt->name, $exclude, true ) ) {
				continue;
			}
			$out[ $pt->name ] = $pt->labels->singular_name . ' (' . $pt->name . ')';
		}
		// SROM post types first, then alphabetical.
		uksort(
			$out,
			function ( $a, $b ) {
				$a_srom = ( 0 === strpos( $a, 'srom_' ) ) ? 0 : 1;
				$b_srom = ( 0 === strpos( $b, 'srom_' ) ) ? 0 : 1;
				if ( $a_srom !== $b_srom ) {
					return $a_srom - $b_srom;
				}
				return strcmp( $a, $b );
			}
		);
		return $out;
	}

	/**
	 * All import targets for a post type.
	 *
	 * @return array ['targets'=>array[], 'unsupported'=>string[]]
	 */
	public static function get_targets( $post_type ) {
		$targets = array();

		$core = array(
			'post_title'   => array( 'Title', 'The post title. If left unmapped, new posts use the key value as their title.' ),
			'post_name'    => array( 'Slug', 'URL slug; sanitized automatically.' ),
			'post_date'    => array( 'Publish date', 'Accepted: 2025-12-31, 31.12.2025, Excel dates. Invalid dates are skipped with a warning.' ),
			'post_content' => array( 'Content', 'Main editor content.' ),
			'post_excerpt' => array( 'Excerpt', '' ),
			'menu_order'   => array( 'Menu order', 'Whole number used for manual ordering.' ),
		);
		foreach ( $core as $name => $info ) {
			$targets[] = array(
				'id'    => 'core:' . $name,
				'kind'  => 'core',
				'name'  => $name,
				'label' => $info[0],
				'type'  => 'core',
				'group' => 'Post fields',
				'note'  => $info[1],
			);
		}

		$unsupported = array();
		if ( self::acf_active() ) {
			$groups = acf_get_field_groups( array( 'post_type' => $post_type ) );
			foreach ( (array) $groups as $group ) {
				$fields = acf_get_fields( $group );
				foreach ( (array) $fields as $field ) {
					if ( empty( $field['key'] ) || empty( $field['name'] ) ) {
						continue;
					}
					if ( in_array( $field['type'], self::UNSUPPORTED_TYPES, true ) ) {
						if ( ! in_array( $field['type'], array( 'message', 'tab', 'accordion' ), true ) ) {
							$unsupported[] = $field['label'] . ' (' . $field['type'] . ')';
						}
						continue;
					}
					$targets[] = array(
						'id'    => 'acf:' . $field['key'],
						'kind'  => 'acf',
						'name'  => $field['name'],
						'label' => $field['label'] ? $field['label'] : $field['name'],
						'type'  => $field['type'],
						'group' => $group['title'] ? $group['title'] : 'ACF',
						'note'  => self::type_note( $field ),
						'field' => $field,
					);
				}
			}
		}

		// Taxonomies attached to this post type become import targets too, so a
		// column can be mapped straight into a taxonomy (e.g. keywords_pl -> tags).
		// A single column may feed both a field and a taxonomy — both targets can
		// point at the same column.
		foreach ( self::taxonomies_for( $post_type ) as $tax ) {
			$targets[] = array(
				'id'           => 'tax:' . $tax->name,
				'kind'         => 'taxonomy',
				'name'         => $tax->name,
				'label'        => $tax->labels->singular_name ? $tax->labels->singular_name : $tax->name,
				'type'         => 'taxonomy',
				'group'        => 'Taxonomies',
				'note'         => 'Term names or slugs; separate several with new lines, ";" or ",".'
					. ( $tax->hierarchical ? ' Use "Parent > Child" for nesting.' : '' )
					. ' Missing terms can be created (see options).',
				'taxonomy'     => $tax->name,
				'hierarchical' => (bool) $tax->hierarchical,
			);
		}

		return array( 'targets' => $targets, 'unsupported' => $unsupported );
	}

	/**
	 * Public, UI-visible taxonomies registered for a post type.
	 *
	 * @return WP_Taxonomy[]
	 */
	public static function taxonomies_for( $post_type ) {
		$out = array();
		foreach ( get_object_taxonomies( $post_type, 'objects' ) as $tax ) {
			if ( in_array( $tax->name, array( 'post_format' ), true ) ) {
				continue;
			}
			if ( empty( $tax->show_ui ) && empty( $tax->public ) ) {
				continue;
			}
			$out[] = $tax;
		}
		return $out;
	}

	/**
	 * Human hint shown next to each field in the mapping table.
	 */
	private static function type_note( array $field ) {
		switch ( $field['type'] ) {
			case 'select':
			case 'radio':
			case 'button_group':
			case 'checkbox':
				$choices = array();
				foreach ( (array) ( isset( $field['choices'] ) ? $field['choices'] : array() ) as $v => $l ) {
					$choices[] = ( (string) $v === (string) $l ) ? (string) $v : $v . ' = ' . $l;
					if ( count( $choices ) >= 8 ) {
						$choices[] = '…';
						break;
					}
				}
				$multi = ( 'checkbox' === $field['type'] || ! empty( $field['multiple'] ) )
					? ' Multiple values: separate with new lines, ";" or ",".' : '';
				return 'Choices: ' . implode( ' | ', $choices ) . '. Values or labels are both accepted.' . $multi;
			case 'true_false':
				return 'Accepted: 1/0, tak/nie, yes/no, true/false. Empty = not changed.';
			case 'number':
			case 'range':
				return 'Plain number. Comma decimals ("11,5") are accepted.';
			case 'date_picker':
				return 'Accepted: 2025-12-31, 31.12.2025, 31/12/2025, Excel dates. Stored in ACF format.';
			case 'date_time_picker':
				return 'Accepted: 2025-12-31 14:30, 31.12.2025 14:30, Excel dates.';
			case 'time_picker':
				return 'Accepted: 14:30 or 14:30:59.';
			case 'post_object':
			case 'relationship':
				$types = ! empty( $field['post_type'] ) ? implode( ', ', (array) $field['post_type'] ) : 'any post type';
				$extra = ( is_array( $field['post_type'] ) && in_array( 'srom_volume', (array) $field['post_type'], true ) )
					? ' For volumes, the volume signature (e.g. SROM·18·2025) also works and missing volumes can be created automatically.' : '';
				$multi = ( 'relationship' === $field['type'] || ! empty( $field['multiple'] ) )
					? ' Multiple values: separate with new lines or ";".' : '';
				return 'Match by post ID, exact title or slug (' . $types . ').' . $extra . $multi;
			case 'page_link':
				return 'Match by post ID, exact title or slug.';
			case 'file':
			case 'image':
				return 'Attachment ID, a file name already in the media library, or a URL. Downloads only happen if enabled in the options.';
			case 'gallery':
				return 'Multiple attachments: IDs, file names or URLs separated by new lines or ";".';
			case 'taxonomy':
				return 'Term names or slugs, separated by new lines, ";" or ",".';
			case 'user':
				return 'User ID, login or e-mail address.';
			case 'google_map':
				return 'Either "lat, lng" (e.g. 50.01, 20.98) or a JSON object with lat/lng.';
			case 'email':
				return 'Must be a valid e-mail address.';
			case 'url':
			case 'oembed':
				return 'Must be a valid URL.';
			case 'link':
				return 'A URL (link text stays empty) or JSON {"url":..,"title":..}.';
			case 'wysiwyg':
				return 'HTML allowed (filtered to safe tags).';
			default:
				return '';
		}
	}

	/**
	 * The SROM preset: master-spreadsheet column -> field name, with optional
	 * value transform. Applied after plain name matching; a preset entry wins
	 * over a name match only where noted (pdf_file), because the master sheet
	 * has both pdf_file (bare file name) and pdf_url (the real URL the ACF
	 * field expects).
	 *
	 * @return array target-name => [source column, transform|null, override-name-match]
	 */
	public static function preset() {
		return array(
			// srom_article — fields
			'authors_raw'    => array( 'authors_struct', 'authors_lines', false ),
			'pdf_file'       => array( 'pdf_url', null, true ),
			'volume'         => array( 'issue_signature', null, false ),
			// keywords_en: store as semicolon-separated discrete terms (override the
			// plain name match to apply the transform), ready for a future EN taxonomy.
			'keywords_en'    => array( 'keywords_en', 'to_semicolons', true ),
			// srom_article — taxonomies (target name = taxonomy slug)
			'dzial'          => array( 'section_label', null, false ),
			'slowa_kluczowe' => array( 'keywords_pl', null, false ),
			// authors_display is "Given Surname, Given Surname" — split_multi's comma
			// handling turns that into one term per author.
			'autor'          => array( 'authors_display', null, false ),
			'rocznik'        => array( 'year', null, false ),
			// srom_volume (also used when auto-creating volumes from article rows)
			'signature'      => array( 'issue_signature', null, false ),
			'theme'          => array( 'issue_theme', null, false ),
			'pub_date'       => array( 'pub_date_online', null, false ),
		);
	}

	/**
	 * Core-field preset for the master sheet.
	 */
	public static function core_preset() {
		return array(
			'post_title' => array( 'title_pl', null, false ),
			'post_name'  => array( 'doi_suffix', null, false ),
			'menu_order' => array( 'seq', null, false ),
			// WordPress' native search indexes post_title/post_content/post_excerpt but
			// never ACF meta, so the abstract is mirrored into the core fields to make
			// articles findable by their abstract. The ACF `abstract_pl` field stays the
			// canonical source for citation metadata; both are rewritten from the same
			// CSV cell on every import, so the copies cannot drift apart.
			'post_content' => array( 'abstract_pl', null, false ),
			'post_excerpt' => array( 'abstract_pl', null, false ),
		);
	}

	/**
	 * Column-name aliases for core fields (plain name matching).
	 */
	private static function core_aliases() {
		return array(
			'post_title'   => array( 'post_title', 'title', 'tytul', 'tytuł' ),
			'post_name'    => array( 'post_name', 'slug' ),
			'post_date'    => array( 'post_date', 'date', 'data' ),
			'post_content' => array( 'post_content', 'content', 'tresc', 'treść' ),
			'post_excerpt' => array( 'post_excerpt', 'excerpt' ),
			'menu_order'   => array( 'menu_order', 'order', 'kolejnosc', 'kolejność' ),
		);
	}

	private static function norm( $name ) {
		$name = function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( (string) $name ) ) : strtolower( trim( (string) $name ) );
		return preg_replace( '/[\s\-]+/u', '_', $name );
	}

	/**
	 * Build the automatic mapping.
	 *
	 * @param array $targets from get_targets()['targets'].
	 * @param array $header  column names.
	 * @return array target_id => ['col'=>int, 'transform'=>string|null, 'auto'=>'name'|'preset']
	 */
	public static function auto_map( array $targets, array $header ) {
		$cols = array();
		foreach ( $header as $i => $name ) {
			$key = self::norm( $name );
			if ( '' !== $key && ! isset( $cols[ $key ] ) ) {
				$cols[ $key ] = $i;
			}
		}

		$mapping = array();
		$aliases = self::core_aliases();

		// Pass 1: plain name matching.
		foreach ( $targets as $t ) {
			$names = ( 'core' === $t['kind'] && isset( $aliases[ $t['name'] ] ) ) ? $aliases[ $t['name'] ] : array( $t['name'] );
			foreach ( $names as $n ) {
				$key = self::norm( $n );
				if ( isset( $cols[ $key ] ) ) {
					$mapping[ $t['id'] ] = array( 'col' => $cols[ $key ], 'transform' => null, 'auto' => 'name' );
					break;
				}
			}
		}

		// Pass 2: SROM preset (only when the source column actually exists).
		$preset = self::preset() + self::core_preset();
		foreach ( $targets as $t ) {
			if ( ! isset( $preset[ $t['name'] ] ) ) {
				continue;
			}
			list( $src, $transform, $override ) = $preset[ $t['name'] ];
			// A relationship/post_object link field must take its preset source.
			// Its field name can collide with an unrelated scalar column of the
			// same name (e.g. the article's `volume` link vs the numeric `volume`
			// column); a name-match to that column is never meaningful, so the
			// preset always wins for these fields.
			if ( in_array( $t['type'], array( 'post_object', 'relationship' ), true ) ) {
				$override = true;
			}
			$key = self::norm( $src );
			if ( ! isset( $cols[ $key ] ) ) {
				continue;
			}
			if ( isset( $mapping[ $t['id'] ] ) && ! $override ) {
				continue;
			}
			$mapping[ $t['id'] ] = array( 'col' => $cols[ $key ], 'transform' => $transform, 'auto' => 'preset' );
		}

		return $mapping;
	}

	/**
	 * Targets that may serve as the unique key for upserts.
	 */
	public static function key_eligible( array $target ) {
		if ( 'core' === $target['kind'] ) {
			return in_array( $target['name'], array( 'post_name', 'post_title' ), true );
		}
		return in_array( $target['type'], array( 'text', 'number', 'email', 'url' ), true );
	}

	/**
	 * Preferred default key, in order of preference.
	 */
	public static function default_key( array $targets, array $mapping ) {
		$prefer = array( 'article_id', 'signature', 'post_name', 'post_title' );
		foreach ( $prefer as $name ) {
			foreach ( $targets as $t ) {
				if ( $t['name'] === $name && isset( $mapping[ $t['id'] ] ) && self::key_eligible( $t ) ) {
					return $t['id'];
				}
			}
		}
		foreach ( $targets as $t ) {
			if ( isset( $mapping[ $t['id'] ] ) && self::key_eligible( $t ) && 'acf' === $t['kind'] ) {
				return $t['id'];
			}
		}
		foreach ( $targets as $t ) {
			if ( isset( $mapping[ $t['id'] ] ) && self::key_eligible( $t ) ) {
				return $t['id'];
			}
		}
		return '';
	}

	/**
	 * Available value transforms (kept deliberately tiny).
	 */
	public static function apply_transform( $transform, $value ) {
		if ( 'authors_lines' === $transform ) {
			// Master sheet separates multiple authors with ";;".
			// The authors_raw field wants one author per line.
			$parts = preg_split( '/\s*;;\s*/u', (string) $value );
			$parts = array_filter( array_map( 'trim', (array) $parts ), 'strlen' );
			return implode( "\n", $parts );
		}
		if ( 'to_semicolons' === $transform ) {
			// Normalize a comma/semicolon/newline list into "a; b; c" discrete terms.
			$parts = preg_split( '/[;,\r\n]+/u', (string) $value );
			$parts = array_filter( array_map( 'trim', (array) $parts ), 'strlen' );
			return implode( '; ', $parts );
		}
		return $value;
	}

	/**
	 * Transforms offered as a checkbox in the mapping UI, by target name.
	 *
	 * @return array target-name => [transform-slug, checkbox-label]
	 */
	public static function optional_transforms() {
		return array(
			'authors_raw' => array( 'authors_lines', 'split authors on ";;" into one per line' ),
			'keywords_en' => array( 'to_semicolons', 'store as semicolon-separated discrete terms' ),
		);
	}

	/**
	 * Does this post type have a post_object/relationship field pointing at srom_volume?
	 *
	 * @return array|null the ACF field array of the volume link field.
	 */
	public static function volume_link_field( array $targets ) {
		foreach ( $targets as $t ) {
			if ( 'acf' !== $t['kind'] || empty( $t['field'] ) ) {
				continue;
			}
			if ( ! in_array( $t['type'], array( 'post_object', 'relationship' ), true ) ) {
				continue;
			}
			$types = (array) ( isset( $t['field']['post_type'] ) ? $t['field']['post_type'] : array() );
			if ( in_array( 'srom_volume', $types, true ) ) {
				return $t['field'];
			}
		}
		return null;
	}
}
