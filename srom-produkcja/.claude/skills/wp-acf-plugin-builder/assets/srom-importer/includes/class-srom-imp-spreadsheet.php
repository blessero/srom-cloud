<?php
/**
 * Spreadsheet reading: CSV / TSV / TXT / XLSX -> header + rows of strings.
 *
 * Design goals: never fatal, never guess silently. Everything unusual is
 * surfaced as a warning; anything unreadable returns WP_Error with a
 * human-readable reason and a suggested fix.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Spreadsheet {

	/**
	 * @param string $path absolute file path.
	 * @param string $ext  lowercase extension without dot (csv|tsv|txt|xlsx).
	 * @param bool   $collect_warnings whether to build warning strings (first parse) or skip (batch re-parse).
	 * @return array|WP_Error ['header'=>string[], 'rows'=>string[][], 'warnings'=>string[], 'skipped_empty'=>int]
	 */
	public static function parse( $path, $ext, $collect_warnings = true ) {
		try {
			if ( ! is_string( $path ) || ! file_exists( $path ) || ! is_readable( $path ) ) {
				return new WP_Error( 'srom_imp_file', 'The uploaded file is no longer available. Please upload it again.' );
			}
			$size = (int) filesize( $path );
			if ( $size <= 0 ) {
				return new WP_Error( 'srom_imp_file', 'The uploaded file is empty.' );
			}
			if ( $size > SROM_IMP_MAX_FILE_BYTES ) {
				return new WP_Error( 'srom_imp_file', 'The file is larger than the ' . size_format( SROM_IMP_MAX_FILE_BYTES ) . ' limit.' );
			}

			if ( 'xlsx' === $ext ) {
				$matrix = self::read_xlsx( $path );
			} else {
				$matrix = self::read_csv( $path, $ext );
			}
			if ( is_wp_error( $matrix ) ) {
				return $matrix;
			}

			return self::finalize( $matrix['data'], $matrix['notes'], $collect_warnings );
		} catch ( Throwable $e ) {
			return new WP_Error(
				'srom_imp_parse',
				'Could not read the file (' . esc_html( $e->getMessage() ) . '). If this is an Excel file, try exporting it as CSV (UTF-8) and uploading that.'
			);
		}
	}

	/* ---------------------------------------------------------------- CSV */

	/**
	 * @return array|WP_Error ['data'=>string[][], 'notes'=>string[]]
	 */
	private static function read_csv( $path, $ext ) {
		$raw = file_get_contents( $path );
		if ( false === $raw ) {
			return new WP_Error( 'srom_imp_file', 'Could not read the uploaded file from disk.' );
		}
		$notes = array();

		// --- Encoding: BOM detection first, then UTF-8 validation. ---
		if ( "\xEF\xBB\xBF" === substr( $raw, 0, 3 ) ) {
			$raw = substr( $raw, 3 );
		} elseif ( "\xFF\xFE" === substr( $raw, 0, 2 ) ) {
			$raw     = self::convert( substr( $raw, 2 ), 'UTF-16LE' );
			$notes[] = 'File was UTF-16 (LE) encoded — converted to UTF-8.';
		} elseif ( "\xFE\xFF" === substr( $raw, 0, 2 ) ) {
			$raw     = self::convert( substr( $raw, 2 ), 'UTF-16BE' );
			$notes[] = 'File was UTF-16 (BE) encoded — converted to UTF-8.';
		} elseif ( function_exists( 'mb_check_encoding' ) && ! mb_check_encoding( $raw, 'UTF-8' ) ) {
			// Excel on Windows commonly saves Polish CSV as Windows-1250.
			$raw     = self::convert( $raw, 'Windows-1250' );
			$notes[] = 'File was not valid UTF-8 — converted from Windows-1250 (Central European). Check Polish characters in the preview; if they look wrong, re-export the file as "CSV UTF-8".';
		}
		if ( false === $raw || null === $raw ) {
			return new WP_Error( 'srom_imp_enc', 'The file encoding could not be converted to UTF-8. Please re-export as "CSV UTF-8".' );
		}

		// Old-Mac line endings (\r only, no \n anywhere).
		if ( false !== strpos( $raw, "\r" ) && false === strpos( $raw, "\n" ) ) {
			$raw = str_replace( "\r", "\n", $raw );
		}

		// --- Delimiter sniffing on the first line (quote-aware). ---
		if ( 'tsv' === $ext ) {
			$delim = "\t";
		} else {
			$delim = self::sniff_delimiter( $raw );
		}
		if ( "," !== $delim ) {
			$notes[] = ( "\t" === $delim ) ? 'Detected tab-separated values.' : 'Detected "' . $delim . '" as the column separator.';
		}

		// --- Parse with fgetcsv (handles quoted cells + embedded newlines). ---
		$fh = fopen( 'php://temp', 'r+' );
		fwrite( $fh, $raw );
		rewind( $fh );
		unset( $raw );

		$data = array();
		// escape '' => plain RFC 4180 (quotes doubled), no backslash magic.
		while ( ( $row = fgetcsv( $fh, 0, $delim, '"', '' ) ) !== false ) {
			if ( null === $row ) {
				continue;
			}
			$cells = array();
			foreach ( $row as $cell ) {
				$cells[] = is_string( $cell ) ? $cell : (string) $cell;
			}
			$data[] = $cells;
			if ( count( $data ) > SROM_IMP_MAX_ROWS + 5 ) {
				fclose( $fh );
				return new WP_Error( 'srom_imp_rows', 'The file has more than ' . number_format_i18n( SROM_IMP_MAX_ROWS ) . ' rows. Please split it into smaller files.' );
			}
		}
		fclose( $fh );

		return array( 'data' => $data, 'notes' => $notes );
	}

	private static function convert( $raw, $from ) {
		// iconv first: it reliably knows the single-byte Windows codepages
		// (some mbstring builds do not, and PHP 8 throws on unknown names).
		if ( function_exists( 'iconv' ) ) {
			$out = @iconv( $from, 'UTF-8//TRANSLIT', $raw );
			if ( is_string( $out ) && '' !== $out ) {
				return $out;
			}
		}
		if ( function_exists( 'mb_convert_encoding' ) ) {
			try {
				$out = @mb_convert_encoding( $raw, 'UTF-8', $from );
				if ( is_string( $out ) && '' !== $out ) {
					return $out;
				}
			} catch ( Throwable $e ) {
				// fall through
			}
		}
		return false;
	}

	/**
	 * Count candidate delimiters outside quoted sections of the first line.
	 */
	private static function sniff_delimiter( $raw ) {
		$eol   = strpos( $raw, "\n" );
		$line  = ( false === $eol ) ? $raw : substr( $raw, 0, $eol );
		$line  = substr( $line, 0, 20000 );
		$count = array( ',' => 0, ';' => 0, "\t" => 0 );
		$in_q  = false;
		$len   = strlen( $line );
		for ( $i = 0; $i < $len; $i++ ) {
			$ch = $line[ $i ];
			if ( '"' === $ch ) {
				$in_q = ! $in_q;
			} elseif ( ! $in_q && isset( $count[ $ch ] ) ) {
				$count[ $ch ]++;
			}
		}
		arsort( $count );
		$best = key( $count );
		return ( $count[ $best ] > 0 ) ? $best : ',';
	}

	/* --------------------------------------------------------------- XLSX */

	/**
	 * Minimal, defensive XLSX reader (first worksheet only).
	 * Handles shared strings (incl. rich text), inline strings, booleans,
	 * numbers and formula result caches. Date cells arrive as Excel serial
	 * numbers; the field coercion layer converts those for date fields.
	 *
	 * @return array|WP_Error ['data'=>string[][], 'notes'=>string[]]
	 */
	private static function read_xlsx( $path ) {
		if ( ! class_exists( 'ZipArchive' ) ) {
			return new WP_Error( 'srom_imp_zip', 'This server\'s PHP is missing the "zip" extension, so .xlsx files cannot be read. Please export the sheet as CSV (UTF-8) and upload that instead.' );
		}
		$zip = new ZipArchive();
		if ( true !== $zip->open( $path ) ) {
			return new WP_Error( 'srom_imp_xlsx', 'The .xlsx file could not be opened — it may be corrupted. Try re-saving it, or export as CSV (UTF-8).' );
		}

		$notes = array();
		try {
			// Zip-bomb guard: refuse absurd uncompressed sizes.
			$total = 0;
			for ( $i = 0; $i < $zip->numFiles; $i++ ) {
				$st = $zip->statIndex( $i );
				if ( $st ) {
					$total += (int) $st['size'];
				}
			}
			if ( $total > 200 * 1024 * 1024 ) {
				return new WP_Error( 'srom_imp_xlsx', 'The .xlsx file expands to over 200 MB and was rejected. Please export as CSV.' );
			}

			$workbook = self::xml( $zip, 'xl/workbook.xml' );
			if ( ! $workbook || ! isset( $workbook->sheets->sheet[0] ) ) {
				return new WP_Error( 'srom_imp_xlsx', 'No worksheet found in the .xlsx file. Please export as CSV (UTF-8).' );
			}
			$first = $workbook->sheets->sheet[0];
			$rid   = '';
			foreach ( $first->attributes( 'http://schemas.openxmlformats.org/officeDocument/2006/relationships' ) as $k => $v ) {
				if ( 'id' === $k ) {
					$rid = (string) $v;
				}
			}
			if ( count( $workbook->sheets->sheet ) > 1 ) {
				$notes[] = 'The workbook has ' . count( $workbook->sheets->sheet ) . ' sheets — only the first sheet ("' . (string) $first['name'] . '") is imported.';
			}

			// Resolve the sheet path via the relationships part.
			$sheet_path = 'xl/worksheets/sheet1.xml';
			$rels       = self::xml( $zip, 'xl/_rels/workbook.xml.rels' );
			if ( $rels && $rid ) {
				foreach ( $rels->Relationship as $rel ) {
					if ( (string) $rel['Id'] === $rid ) {
						$target = (string) $rel['Target'];
						$target = ltrim( $target, '/' );
						if ( 0 !== strpos( $target, 'xl/' ) ) {
							$target = 'xl/' . $target;
						}
						$sheet_path = $target;
						break;
					}
				}
			}

			// Shared strings (may be absent).
			$shared = array();
			$ss_xml = self::xml( $zip, 'xl/sharedStrings.xml' );
			if ( $ss_xml ) {
				foreach ( $ss_xml->si as $si ) {
					$parts = $si->xpath( './/*[local-name()="t"]' );
					$txt   = '';
					foreach ( (array) $parts as $t ) {
						$txt .= (string) $t;
					}
					$shared[] = $txt;
				}
			}

			$sheet = self::xml( $zip, $sheet_path );
			if ( ! $sheet || ! isset( $sheet->sheetData ) ) {
				return new WP_Error( 'srom_imp_xlsx', 'The worksheet data could not be read. Please export as CSV (UTF-8).' );
			}

			$data    = array();
			$max_col = 0;
			$r_index = 0;
			foreach ( $sheet->sheetData->row as $row ) {
				// Respect the sheet's own row numbering so blank rows stay blank.
				$declared = (int) $row['r'];
				$r_index  = ( $declared > 0 ) ? $declared - 1 : $r_index;
				if ( $r_index > SROM_IMP_MAX_ROWS + 5 ) {
					return new WP_Error( 'srom_imp_rows', 'The sheet has more than ' . number_format_i18n( SROM_IMP_MAX_ROWS ) . ' rows. Please split it into smaller files.' );
				}
				$cells   = array();
				$c_guess = 0;
				foreach ( $row->c as $c ) {
					$ref = (string) $c['r'];
					$col = self::col_from_ref( $ref );
					if ( null === $col ) {
						$col = $c_guess;
					}
					$c_guess = $col + 1;
					if ( $col > SROM_IMP_MAX_COLS + 5 ) {
						continue;
					}
					$type = (string) $c['t'];
					$val  = '';
					if ( 's' === $type ) {
						$idx = (int) $c->v;
						$val = isset( $shared[ $idx ] ) ? $shared[ $idx ] : '';
					} elseif ( 'inlineStr' === $type ) {
						$parts = $c->is ? $c->is->xpath( './/*[local-name()="t"]' ) : array();
						foreach ( (array) $parts as $t ) {
							$val .= (string) $t;
						}
					} elseif ( 'b' === $type ) {
						$val = ( '1' === (string) $c->v ) ? '1' : '0';
					} else { // n, str, e, or untyped: use the cached value.
						$val = isset( $c->v ) ? (string) $c->v : '';
					}
					$cells[ $col ] = $val;
					if ( $col + 1 > $max_col ) {
						$max_col = $col + 1;
					}
				}
				$data[ $r_index ] = $cells;
				$r_index++;
			}

			// Densify into a rectangular string matrix.
			$out    = array();
			$last_r = empty( $data ) ? -1 : max( array_keys( $data ) );
			for ( $r = 0; $r <= $last_r; $r++ ) {
				$row_cells = isset( $data[ $r ] ) ? $data[ $r ] : array();
				$line      = array();
				for ( $cix = 0; $cix < $max_col; $cix++ ) {
					$line[] = isset( $row_cells[ $cix ] ) ? $row_cells[ $cix ] : '';
				}
				$out[] = $line;
			}

			return array( 'data' => $out, 'notes' => $notes );
		} finally {
			$zip->close();
		}
	}

	/**
	 * Load an XML part safely (no network, no DOCTYPE).
	 *
	 * @return SimpleXMLElement|null
	 */
	private static function xml( ZipArchive $zip, $name ) {
		$raw = $zip->getFromName( $name );
		if ( false === $raw || '' === $raw ) {
			return null;
		}
		if ( preg_match( '/<!DOCTYPE/i', substr( $raw, 0, 1000 ) ) ) {
			return null; // never present in real xlsx parts; refuse if it is.
		}
		$prev = libxml_use_internal_errors( true );
		$sx   = simplexml_load_string( $raw, 'SimpleXMLElement', LIBXML_NONET | LIBXML_NOCDATA );
		libxml_clear_errors();
		libxml_use_internal_errors( $prev );
		return ( $sx instanceof SimpleXMLElement ) ? $sx : null;
	}

	/**
	 * "C5" -> 2. Returns null when the ref has no letters.
	 */
	private static function col_from_ref( $ref ) {
		if ( ! preg_match( '/^([A-Z]+)\d+$/i', $ref, $m ) ) {
			return null;
		}
		$letters = strtoupper( $m[1] );
		$n       = 0;
		$len     = strlen( $letters );
		for ( $i = 0; $i < $len; $i++ ) {
			$n = $n * 26 + ( ord( $letters[ $i ] ) - 64 );
		}
		return $n - 1;
	}

	/* ------------------------------------------------------------ common */

	/**
	 * Turn a raw matrix into header + data rows with all the tolerant
	 * clean-up: skip leading blank rows, trim headers, drop ghost trailing
	 * columns, pad/trim rows, skip empty and repeated-header rows.
	 */
	private static function finalize( array $data, array $notes, $collect_warnings ) {
		$warnings = $collect_warnings ? $notes : array();

		// Find the header: first row with at least one non-empty cell.
		$header     = null;
		$header_pos = 0;
		foreach ( $data as $i => $row ) {
			foreach ( $row as $cell ) {
				if ( '' !== trim( (string) $cell ) ) {
					$header     = $row;
					$header_pos = $i;
					break 2;
				}
			}
		}
		if ( null === $header ) {
			return new WP_Error( 'srom_imp_empty', 'The file contains no data (all rows are empty).' );
		}
		if ( $header_pos > 0 && $collect_warnings ) {
			$warnings[] = 'Skipped ' . $header_pos . ' empty row(s) before the header row.';
		}

		// Normalize header names.
		$names = array();
		foreach ( $header as $cell ) {
			$name    = self::clean_cell( (string) $cell );
			$name    = preg_replace( '/\s+/u', ' ', $name );
			$names[] = $name;
		}
		// Drop trailing "ghost" columns with empty headers (common Excel artifact).
		while ( ! empty( $names ) && '' === end( $names ) ) {
			array_pop( $names );
		}
		if ( empty( $names ) ) {
			return new WP_Error( 'srom_imp_header', 'The header row is empty.' );
		}
		if ( count( $names ) > SROM_IMP_MAX_COLS ) {
			return new WP_Error( 'srom_imp_cols', 'The file has more than ' . SROM_IMP_MAX_COLS . ' columns.' );
		}
		// Name interior empty/duplicate headers so every column stays addressable.
		$seen = array();
		foreach ( $names as $i => $name ) {
			if ( '' === $name ) {
				$names[ $i ] = '(column ' . ( $i + 1 ) . ')';
			}
			$lower = function_exists( 'mb_strtolower' ) ? mb_strtolower( $names[ $i ] ) : strtolower( $names[ $i ] );
			if ( isset( $seen[ $lower ] ) ) {
				$seen[ $lower ]++;
				if ( $collect_warnings ) {
					$warnings[] = 'Duplicate column name "' . $names[ $i ] . '" — the later one is shown as "' . $names[ $i ] . ' (' . $seen[ $lower ] . ')".';
				}
				$names[ $i ] .= ' (' . $seen[ $lower ] . ')';
			} else {
				$seen[ $lower ] = 1;
			}
		}
		$ncols = count( $names );

		// Data rows.
		$rows          = array();
		$skipped_empty = 0;
		$total         = count( $data );
		for ( $i = $header_pos + 1; $i < $total; $i++ ) {
			$row      = $data[ $i ];
			$line_no  = $i + 1; // 1-based line number as seen in a spreadsheet app.
			$is_empty = true;
			foreach ( $row as $cell ) {
				if ( '' !== trim( (string) $cell ) ) {
					$is_empty = false;
					break;
				}
			}
			if ( $is_empty ) {
				$skipped_empty++;
				continue;
			}

			$cells = array();
			for ( $c = 0; $c < $ncols; $c++ ) {
				$cells[] = isset( $row[ $c ] ) ? self::clean_cell( (string) $row[ $c ] ) : '';
			}
			// Extra non-empty cells beyond the header width?
			if ( count( $row ) > $ncols && $collect_warnings ) {
				for ( $c = $ncols; $c < count( $row ); $c++ ) {
					if ( '' !== trim( (string) $row[ $c ] ) ) {
						$warnings[] = 'Row ' . $line_no . ' has data beyond the last named column — those extra cells are ignored.';
						break;
					}
				}
			}
			// A pasted copy of the header row is data noise, not data.
			if ( self::row_equals_header( $cells, $names ) ) {
				if ( $collect_warnings ) {
					$warnings[] = 'Row ' . $line_no . ' repeats the header row — skipped.';
				}
				continue;
			}

			$rows[] = array( 'line' => $line_no, 'cells' => $cells );
			if ( count( $rows ) > SROM_IMP_MAX_ROWS ) {
				return new WP_Error( 'srom_imp_rows', 'The file has more than ' . number_format_i18n( SROM_IMP_MAX_ROWS ) . ' data rows. Please split it into smaller files.' );
			}
		}

		if ( empty( $rows ) ) {
			return new WP_Error( 'srom_imp_empty', 'The file has a header row but no data rows.' );
		}

		return array(
			'header'        => $names,
			'rows'          => $rows,
			'warnings'      => $warnings,
			'skipped_empty' => $skipped_empty,
		);
	}

	/**
	 * Trim whitespace incl. non-breaking spaces and stray BOMs; keep inner content intact.
	 */
	public static function clean_cell( $v ) {
		$v = str_replace( "\xEF\xBB\xBF", '', $v );
		$v = preg_replace( '/^[\s\x{00A0}\x{FEFF}]+|[\s\x{00A0}\x{FEFF}]+$/u', '', $v );
		return ( null === $v ) ? '' : $v;
	}

	private static function row_equals_header( array $cells, array $names ) {
		foreach ( $cells as $i => $cell ) {
			$a = function_exists( 'mb_strtolower' ) ? mb_strtolower( $cell ) : strtolower( $cell );
			$b = function_exists( 'mb_strtolower' ) ? mb_strtolower( $names[ $i ] ) : strtolower( $names[ $i ] );
			if ( $a !== $b ) {
				return false;
			}
		}
		return true;
	}
}
