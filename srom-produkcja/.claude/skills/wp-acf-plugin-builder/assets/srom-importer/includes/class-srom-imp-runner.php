<?php
/**
 * The import engine.
 *
 * Both the dry-run preview and the real import walk the same code path;
 * $this->dry decides whether anything is written. Rows are processed in
 * small batches (one HTTP request each) so large files cannot hit PHP
 * time limits, and every row is isolated: an error in row N is logged
 * and row N+1 still runs.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Runner {

	/** @var string */
	private $token;

	/** @var array */
	private $job;

	/** @var bool */
	private $dry = true;

	/** @var array target definitions indexed by target id */
	private $targets = array();

	/** @var array|null ACF fields of srom_volume, name => field (lazy) */
	private $volume_fields = null;

	public function __construct( $token, array $job ) {
		$this->token = $token;
		$this->job   = $job;
	}

	/**
	 * Process the next batch. Returns data for the UI or WP_Error.
	 */
	public function process_batch( $mode, $batch_size = SROM_IMP_BATCH_SIZE ) {
		$expected_state = ( 'import' === $mode ) ? 'import_running' : 'preview_running';
		if ( ! isset( $this->job['state'] ) || $this->job['state'] !== $expected_state ) {
			return new WP_Error( 'srom_imp_state', 'This import is not currently running in ' . $mode . ' mode. Reload the page and start it again.' );
		}
		$this->dry = ( 'import' !== $mode );

		$parsed = SROM_Imp_Spreadsheet::parse( $this->job['file'], $this->job['ext'], false );
		if ( is_wp_error( $parsed ) ) {
			return $parsed;
		}
		$rows  = $parsed['rows'];
		$total = count( $rows );
		$from  = max( 0, (int) $this->job['next_row'] );

		// Row count changed between requests? (file replaced/corrupted) — bail clearly.
		if ( (int) $this->job['total_rows'] !== $total ) {
			return new WP_Error( 'srom_imp_changed', 'The stored file no longer matches this job. Please start over and upload the file again.' );
		}

		$t_info        = SROM_Imp_Fields::get_targets( $this->job['post_type'] );
		$this->targets = array();
		foreach ( $t_info['targets'] as $t ) {
			$this->targets[ $t['id'] ] = $t;
		}

		if ( function_exists( 'set_time_limit' ) ) {
			@set_time_limit( 120 );
		}
		if ( function_exists( 'wp_raise_memory_limit' ) ) {
			wp_raise_memory_limit( 'admin' );
		}
		if ( ! $this->dry ) {
			wp_defer_term_counting( true );
		}

		$delta = array();
		$to    = min( $total, $from + max( 1, (int) $batch_size ) );
		for ( $i = $from; $i < $to; $i++ ) {
			$entry = $this->process_row( $rows[ $i ]['line'], $rows[ $i ]['cells'] );
			$this->bump_counts( $entry );
			$delta[]                 = $entry;
			$this->job['log'][]      = $entry;
			$this->job['next_row']   = $i + 1;
		}

		if ( ! $this->dry ) {
			wp_defer_term_counting( false );
		}

		$done = ( $this->job['next_row'] >= $total );
		if ( $done ) {
			$this->job['state'] = $this->dry ? 'previewed' : 'done';
		}
		SROM_Imp_Jobs::save( $this->token, $this->job );

		return array(
			'done'     => $done,
			'next_row' => (int) $this->job['next_row'],
			'total'    => $total,
			'counts'   => $this->job['counts'],
			'log'      => $delta,
		);
	}

	private function bump_counts( array $entry ) {
		$c = &$this->job['counts'];
		switch ( $entry['action'] ) {
			case 'created':
			case 'would-create':
				$c['created']++;
				break;
			case 'updated':
			case 'would-update':
				$c['updated']++;
				break;
			case 'error':
				$c['errors']++;
				break;
			default:
				$c['skipped']++;
		}
		if ( 'error' !== $entry['action'] && ! empty( $entry['msgs'] ) ) {
			$c['warnings']++;
		}
	}

	/**
	 * @return array log entry.
	 */
	private function process_row( $line_no, array $cells ) {
		try {
			return $this->do_row( $line_no, $cells );
		} catch ( Throwable $e ) {
			return $this->entry( $line_no, 'error', 0, '', array( 'Unexpected error: ' . $e->getMessage() ) );
		}
	}

	private function entry( $line_no, $action, $post_id, $title, array $msgs ) {
		$e = array(
			'row'     => (int) $line_no,
			'action'  => $action,
			'post_id' => (int) $post_id,
			'title'   => SROM_Imp_Coerce::shorten( (string) $title, 80 ),
			'msgs'    => array_values( array_unique( array_map( 'strval', $msgs ) ) ),
		);
		if ( $post_id && ! $this->dry ) {
			$link = get_edit_post_link( $post_id, 'url' );
			if ( $link ) {
				$e['edit'] = esc_url_raw( $link );
			}
		}
		return $e;
	}

	private function do_row( $line_no, array $cells ) {
		$opts    = $this->job['options'];
		$mapping = $this->job['mapping'];
		$header  = $this->job['header'];

		// Full row keyed by column name (used for auto-creating volumes).
		$row_assoc = array();
		foreach ( $header as $i => $name ) {
			$row_assoc[ $name ] = isset( $cells[ $i ] ) ? $cells[ $i ] : '';
		}
		$this->row_assoc = $row_assoc;

		// --- 1. The unique key. ---
		$key_id = $this->job['key_target'];
		if ( ! isset( $mapping[ $key_id ], $this->targets[ $key_id ] ) ) {
			return $this->entry( $line_no, 'error', 0, '', array( 'The key field is no longer mapped — edit the mapping and run the preview again.' ) );
		}
		$key_target = $this->targets[ $key_id ];
		$key_raw    = $this->raw_for( $key_id, $cells );
		if ( '' === $key_raw ) {
			return $this->entry( $line_no, 'error', 0, '', array( 'The key column "' . $header[ $mapping[ $key_id ]['col'] ] . '" is empty in this row — row skipped. (Summary or note rows are skipped this way on purpose.)' ) );
		}
		if ( isset( $this->job['seen_keys'][ $key_raw ] ) ) {
			return $this->entry( $line_no, 'error', 0, $key_raw, array( 'Duplicate key "' . SROM_Imp_Coerce::shorten( $key_raw ) . '" — already used in row ' . $this->job['seen_keys'][ $key_raw ] . '. Row skipped.' ) );
		}
		$this->job['seen_keys'][ $key_raw ] = $line_no;

		// --- 2. Find an existing post by key. ---
		$existing = $this->find_existing( $key_target, $key_raw );
		if ( is_wp_error( $existing ) ) {
			return $this->entry( $line_no, 'error', 0, $key_raw, array( $existing->get_error_message() ) );
		}
		if ( $existing && empty( $opts['update_existing'] ) ) {
			return $this->entry( $line_no, 'exists', $existing, $key_raw, array( 'A post with this key already exists (#' . $existing . ') and "update existing" is off — row skipped.' ) );
		}

		// --- 3. Convert every mapped cell. ---
		$core_updates = array();
		$acf_updates  = array(); // field_key => value
		$tax_updates  = array(); // taxonomy => array of term_ids (real) — assigned after save
		$msgs         = array();
		$ctx          = array(
			'runner'    => $this,
			'dry'       => $this->dry,
			'options'   => $opts,
			'row_assoc' => $row_assoc,
		);

		$filled_beyond_key = 0;
		foreach ( $mapping as $target_id => $m ) {
			if ( ! isset( $this->targets[ $target_id ] ) ) {
				continue; // field was deleted since mapping was saved
			}
			$target = $this->targets[ $target_id ];
			$raw    = $this->raw_for( $target_id, $cells );
			if ( '' !== $raw && $target_id !== $key_id ) {
				$filled_beyond_key++;
			}

			if ( '' === $raw ) {
				if ( 'clear' === $opts['empty_cells'] ) {
					if ( 'acf' === $target['kind'] ) {
						$acf_updates[ $target['field']['key'] ] = $this->clear_value( $target['field'] );
					} elseif ( 'taxonomy' === $target['kind'] ) {
						$tax_updates[ $target['taxonomy'] ] = array(); // clear all terms
					}
				}
				continue; // 'keep' policy: never touch a field for an empty cell
			}

			if ( 'taxonomy' === $target['kind'] ) {
				$res = $this->resolve_wp_terms( $target, SROM_Imp_Coerce::split_multi( $raw, true ) );
				foreach ( $res['msgs'] as $m2 ) {
					$msgs[] = $target['label'] . ': ' . $m2;
				}
				if ( 'ok' === $res['status'] ) {
					$tax_updates[ $target['taxonomy'] ] = $res['ids'];
				}
				continue;
			}

			if ( 'core' === $target['kind'] ) {
				$res = $this->coerce_core( $target['name'], $raw );
			} else {
				$res = SROM_Imp_Coerce::coerce( $target['field'], $raw, $ctx );
			}
			foreach ( $res['msgs'] as $m2 ) {
				$msgs[] = $target['label'] . ': ' . $m2;
			}
			if ( 'ok' !== $res['status'] ) {
				continue;
			}
			if ( 'core' === $target['kind'] ) {
				$core_updates[ $target['name'] ] = $res['value'];
			} else {
				$acf_updates[ $target['field']['key'] ] = $res['value'];
			}
		}

		// --- 4. Write (or pretend to). ---
		$title_for_log = isset( $core_updates['post_title'] ) ? $core_updates['post_title'] : $key_raw;

		if ( ! $existing && 0 === $filled_beyond_key ) {
			$msgs[] = 'Only the key column has a value in this row — check whether it is a real record (summary or note rows can look like this).';
		}

		if ( $this->dry ) {
			$action = $existing ? 'would-update' : 'would-create';
			return $this->entry( $line_no, $action, (int) $existing, $title_for_log, $msgs );
		}

		if ( $existing ) {
			$post_id  = (int) $existing;
			$post_arr = $this->core_postarr( $core_updates, false );
			if ( ! empty( $post_arr ) ) {
				$post_arr['ID'] = $post_id;
				$result         = wp_update_post( wp_slash( $post_arr ), true );
				if ( is_wp_error( $result ) ) {
					return $this->entry( $line_no, 'error', $post_id, $title_for_log, array_merge( $msgs, array( 'Could not update the post: ' . $result->get_error_message() ) ) );
				}
			}
		} else {
			$post_arr               = $this->core_postarr( $core_updates, true );
			$post_arr['post_type']  = $this->job['post_type'];
			$post_arr['post_status'] = $opts['new_status'];
			if ( empty( $post_arr['post_title'] ) ) {
				$post_arr['post_title'] = $key_raw;
				$msgs[]                 = 'No title mapped — the key value was used as the title.';
			}
			$post_id = wp_insert_post( wp_slash( $post_arr ), true );
			if ( is_wp_error( $post_id ) ) {
				return $this->entry( $line_no, 'error', 0, $title_for_log, array_merge( $msgs, array( 'Could not create the post: ' . $post_id->get_error_message() ) ) );
			}
		}

		foreach ( $acf_updates as $field_key => $value ) {
			try {
				update_field( $field_key, $value, $post_id );
			} catch ( Throwable $e ) {
				$label  = isset( $this->targets[ 'acf:' . $field_key ]['label'] ) ? $this->targets[ 'acf:' . $field_key ]['label'] : $field_key;
				$msgs[] = $label . ': saving failed (' . $e->getMessage() . ')';
			}
		}

		foreach ( $tax_updates as $taxonomy => $term_ids ) {
			$result = wp_set_object_terms( $post_id, array_map( 'intval', $term_ids ), $taxonomy, false );
			if ( is_wp_error( $result ) ) {
				$msgs[] = 'Taxonomy ' . $taxonomy . ': could not assign terms (' . $result->get_error_message() . ')';
			}
		}

		return $this->entry( $line_no, $existing ? 'updated' : 'created', $post_id, $title_for_log, $msgs );
	}

	/**
	 * Resolve tokens to term IDs for a WP taxonomy target (create when allowed).
	 * Supports "Parent > Child" nesting for hierarchical taxonomies.
	 *
	 * @return array ['status'=>'ok'|'skip', 'ids'=>int[], 'msgs'=>string[]]
	 */
	public function resolve_wp_terms( array $target, array $tokens ) {
		$taxonomy = $target['taxonomy'];
		if ( ! taxonomy_exists( $taxonomy ) ) {
			return array( 'status' => 'skip', 'ids' => array(), 'msgs' => array( 'taxonomy "' . $taxonomy . '" is not registered — skipped' ) );
		}
		$hierarchical = ! empty( $target['hierarchical'] );
		$create       = ! empty( $this->job['options']['create_terms'] );
		$ids          = array();
		$msgs         = array();
		$new_count    = 0;

		foreach ( $tokens as $token ) {
			// Hierarchical "Parent > Child": resolve/attach step by step.
			$segments = $hierarchical ? array_map( 'trim', explode( '>', $token ) ) : array( $token );
			$segments = array_filter( $segments, 'strlen' );
			if ( empty( $segments ) ) {
				continue;
			}
			$parent   = 0;
			$term_id  = 0;
			$ok       = true;
			foreach ( $segments as $seg ) {
				$term = get_term_by( 'name', $seg, $taxonomy );
				if ( ! $term ) {
					$term = get_term_by( 'slug', sanitize_title( $seg ), $taxonomy );
				}
				// A matched term must sit under the resolved parent (hierarchical).
				if ( $term && $hierarchical && (int) $term->parent !== (int) $parent ) {
					$term = false;
				}
				if ( $term ) {
					$term_id = (int) $term->term_id;
					$parent  = $term_id;
					continue;
				}
				if ( ! $create ) {
					$msgs[] = 'term "' . SROM_Imp_Coerce::shorten( $seg ) . '" does not exist and term creation is off — skipped';
					$ok     = false;
					break;
				}
				if ( $this->dry ) {
					$new_count++;
					$term_id = -1; // placeholder in preview
					$parent  = 0;  // cannot know new parent id in preview
					continue;
				}
				$args = ( $hierarchical && $parent ) ? array( 'parent' => $parent ) : array();
				$new  = wp_insert_term( $seg, $taxonomy, $args );
				if ( is_wp_error( $new ) ) {
					// "term_exists" race: fall back to the existing id.
					$existing_id = $new->get_error_data();
					if ( is_array( $existing_id ) ) {
						$existing_id = reset( $existing_id );
					}
					if ( $existing_id ) {
						$term_id = (int) $existing_id;
						$parent  = $term_id;
						continue;
					}
					$msgs[] = 'could not create term "' . SROM_Imp_Coerce::shorten( $seg ) . '": ' . $new->get_error_message();
					$ok     = false;
					break;
				}
				$term_id   = (int) $new['term_id'];
				$parent    = $term_id;
				$new_count++;
			}
			if ( $ok && $term_id > 0 ) {
				$ids[] = $term_id;
			}
		}

		if ( $new_count > 0 ) {
			$msgs[] = ( $this->dry ? 'will create ' : 'created ' ) . $new_count . ' new term(s)';
		}
		$ids = array_values( array_unique( array_filter( $ids, function ( $id ) { return $id > 0; } ) ) );

		// In preview, terms that don't exist yet can't produce ids; still report as ok
		// so the row counts as a normal write with an informational note.
		if ( empty( $ids ) && empty( $msgs ) ) {
			return array( 'status' => 'skip', 'ids' => array(), 'msgs' => array() );
		}
		return array( 'status' => 'ok', 'ids' => $ids, 'msgs' => $msgs );
	}

	/** @var array current row, name-keyed (for volume auto-create) */
	private $row_assoc = array();

	private function raw_for( $target_id, array $cells ) {
		$m   = $this->job['mapping'][ $target_id ];
		$col = (int) $m['col'];
		$raw = isset( $cells[ $col ] ) ? $cells[ $col ] : '';
		if ( ! empty( $m['transform'] ) ) {
			$raw = SROM_Imp_Fields::apply_transform( $m['transform'], $raw );
		}
		return SROM_Imp_Spreadsheet::clean_cell( $raw );
	}

	private function clear_value( array $field ) {
		$array_types = array( 'checkbox', 'gallery', 'relationship', 'taxonomy' );
		if ( in_array( $field['type'], $array_types, true ) || ! empty( $field['multiple'] ) ) {
			return array();
		}
		return '';
	}

	private function coerce_core( $name, $raw ) {
		switch ( $name ) {
			case 'post_title':
			case 'post_excerpt':
				return array( 'status' => 'ok', 'value' => $raw, 'msgs' => array() );
			case 'post_content':
				return array( 'status' => 'ok', 'value' => str_replace( "\r\n", "\n", $raw ), 'msgs' => array() );
			case 'post_name':
				$slug = sanitize_title( $raw );
				if ( '' === $slug ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => array( '"' . SROM_Imp_Coerce::shorten( $raw ) . '" produces an empty slug — field skipped' ) );
				}
				return array( 'status' => 'ok', 'value' => $slug, 'msgs' => array() );
			case 'menu_order':
				$n = SROM_Imp_Coerce::parse_number( $raw );
				if ( null === $n ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => array( '"' . SROM_Imp_Coerce::shorten( $raw ) . '" is not a number — field skipped' ) );
				}
				return array( 'status' => 'ok', 'value' => (int) $n, 'msgs' => array() );
			case 'post_date':
				$dt = SROM_Imp_Coerce::parse_date( $raw, true );
				if ( ! $dt ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => array( '"' . SROM_Imp_Coerce::shorten( $raw ) . '" is not a recognizable date — publish date skipped' ) );
				}
				return array( 'status' => 'ok', 'value' => $dt->format( 'Y-m-d H:i:s' ), 'msgs' => array() );
		}
		return array( 'status' => 'skip', 'value' => null, 'msgs' => array( 'unknown core field' ) );
	}

	private function core_postarr( array $core_updates, $creating ) {
		$out = array();
		foreach ( $core_updates as $name => $value ) {
			if ( 'post_date' === $name ) {
				$out['post_date']     = $value;
				$out['post_date_gmt'] = get_gmt_from_date( $value );
				if ( ! $creating ) {
					$out['edit_date'] = true; // force the date change on drafts
				}
			} else {
				$out[ $name ] = $value;
			}
		}
		return $out;
	}

	/* --------------------------------------------------- lookups & upsert */

	/**
	 * @return int|false|WP_Error post ID, false when none, WP_Error when ambiguous.
	 */
	private function find_existing( array $key_target, $key_raw ) {
		$post_type = $this->job['post_type'];

		if ( 'core' === $key_target['kind'] ) {
			global $wpdb;
			$column = ( 'post_name' === $key_target['name'] ) ? 'post_name' : 'post_title';
			$value  = ( 'post_name' === $key_target['name'] ) ? sanitize_title( $key_raw ) : $key_raw;
			$ids    = $wpdb->get_col(
				$wpdb->prepare(
					"SELECT ID FROM {$wpdb->posts} WHERE {$column} = %s AND post_type = %s AND post_status NOT IN ('trash','auto-draft') ORDER BY ID ASC LIMIT 2",
					$value,
					$post_type
				)
			);
		} else {
			$ids = get_posts(
				array(
					'post_type'              => $post_type,
					'post_status'            => 'any',
					'meta_key'               => $key_target['name'],
					'meta_value'             => $key_raw,
					'numberposts'            => 2,
					'fields'                 => 'ids',
					'orderby'                => 'ID',
					'order'                  => 'ASC',
					'no_found_rows'          => true,
					'update_post_meta_cache' => false,
					'update_post_term_cache' => false,
				)
			);
		}

		if ( empty( $ids ) ) {
			return false;
		}
		if ( count( $ids ) > 1 ) {
			return new WP_Error(
				'srom_imp_ambiguous',
				'More than one existing post matches key "' . SROM_Imp_Coerce::shorten( $key_raw ) . '" (#' . (int) $ids[0] . ', #' . (int) $ids[1] . '…). Row skipped — resolve the duplicate in WordPress first.'
			);
		}
		return (int) $ids[0];
	}

	/**
	 * Resolve one token to a post ID for post_object / relationship / page_link.
	 *
	 * @return array ['id'=>int|null, 'deferred'=>bool, 'msgs'=>string[]]
	 */
	public function resolve_post( array $field, $token ) {
		$types = array_values( array_filter( (array) ( isset( $field['post_type'] ) ? $field['post_type'] : array() ) ) );
		$token = SROM_Imp_Spreadsheet::clean_cell( $token );

		if ( '' === $token ) {
			return array( 'id' => null, 'deferred' => false, 'msgs' => array() );
		}

		// 1. Numeric ID.
		if ( preg_match( '/^\d+$/', $token ) ) {
			$p = get_post( (int) $token );
			if ( $p && ( empty( $types ) || in_array( $p->post_type, $types, true ) ) && 'trash' !== $p->post_status ) {
				return array( 'id' => (int) $p->ID, 'deferred' => false, 'msgs' => array() );
			}
			return array( 'id' => null, 'deferred' => false, 'msgs' => array( 'no post with ID ' . (int) $token . ( $types ? ' of type ' . implode( '/', $types ) : '' ) . ' — field skipped' ) );
		}

		global $wpdb;
		$type_sql = '';
		$params   = array( $token );
		if ( ! empty( $types ) ) {
			$type_sql = ' AND post_type IN (' . implode( ',', array_fill( 0, count( $types ), '%s' ) ) . ')';
			$params   = array_merge( $params, $types );
		}

		// 2. Exact title.
		$ids = $wpdb->get_col(
			$wpdb->prepare(
				"SELECT ID FROM {$wpdb->posts} WHERE post_title = %s{$type_sql} AND post_status NOT IN ('trash','auto-draft','inherit') ORDER BY ID ASC LIMIT 2",
				$params
			)
		);
		if ( count( $ids ) === 1 ) {
			return array( 'id' => (int) $ids[0], 'deferred' => false, 'msgs' => array() );
		}
		if ( count( $ids ) > 1 ) {
			return array( 'id' => null, 'deferred' => false, 'msgs' => array( 'several posts share the title "' . SROM_Imp_Coerce::shorten( $token ) . '" — use the post ID instead. Field skipped.' ) );
		}

		// 3. Slug.
		$slug      = sanitize_title( $token );
		$params[0] = $slug;
		if ( '' !== $slug ) {
			$ids = $wpdb->get_col(
				$wpdb->prepare(
					"SELECT ID FROM {$wpdb->posts} WHERE post_name = %s{$type_sql} AND post_status NOT IN ('trash','auto-draft','inherit') ORDER BY ID ASC LIMIT 2",
					$params
				)
			);
			if ( count( $ids ) === 1 ) {
				return array( 'id' => (int) $ids[0], 'deferred' => false, 'msgs' => array() );
			}
		}

		// 4. SROM volumes: match by signature, optionally create.
		if ( in_array( 'srom_volume', $types, true ) || ( empty( $types ) && 'srom_volume' === $this->job['post_type'] ) ) {
			return $this->find_or_create_volume( $token );
		}

		return array( 'id' => null, 'deferred' => false, 'msgs' => array( 'no ' . ( $types ? implode( '/', $types ) : 'post' ) . ' found matching "' . SROM_Imp_Coerce::shorten( $token ) . '" (tried ID, title, slug) — field skipped' ) );
	}

	/**
	 * Look up an srom_volume by its ACF "signature"; create it (with as much
	 * volume data as the current row carries) when the option allows.
	 *
	 * @return array ['id'=>int|null, 'deferred'=>bool, 'msgs'=>string[]]
	 */
	public function find_or_create_volume( $signature ) {
		$signature = SROM_Imp_Spreadsheet::clean_cell( $signature );
		if ( '' === $signature ) {
			return array( 'id' => null, 'deferred' => false, 'msgs' => array() );
		}

		if ( isset( $this->job['volume_cache'][ $signature ] ) ) {
			$cached = $this->job['volume_cache'][ $signature ];
			if ( 'dry' === $cached ) {
				return array( 'id' => null, 'deferred' => true, 'msgs' => array( 'volume "' . $signature . '" will be created and linked during import' ) );
			}
			return array( 'id' => (int) $cached, 'deferred' => false, 'msgs' => array() );
		}

		$found = get_posts(
			array(
				'post_type'              => 'srom_volume',
				'post_status'            => 'any',
				'meta_key'               => 'signature',
				'meta_value'             => $signature,
				'numberposts'            => 1,
				'fields'                 => 'ids',
				'orderby'                => 'ID',
				'order'                  => 'ASC',
				'no_found_rows'          => true,
				'update_post_meta_cache' => false,
				'update_post_term_cache' => false,
			)
		);
		if ( ! empty( $found ) ) {
			$this->job['volume_cache'][ $signature ] = (int) $found[0];
			return array( 'id' => (int) $found[0], 'deferred' => false, 'msgs' => array() );
		}

		if ( empty( $this->job['options']['link_volumes'] ) ) {
			return array( 'id' => null, 'deferred' => false, 'msgs' => array( 'no volume (srom_volume) with signature "' . SROM_Imp_Coerce::shorten( $signature ) . '" exists and automatic creation is disabled — field skipped' ) );
		}

		if ( $this->dry ) {
			$this->job['volume_cache'][ $signature ] = 'dry';
			return array( 'id' => null, 'deferred' => true, 'msgs' => array( 'volume "' . $signature . '" does not exist yet — it will be created and linked during import' ) );
		}

		// Real creation. Give the volume a clean slug of "{volume}-{year}"
		// (e.g. 18-2025) from the row; otherwise WordPress would derive it from
		// the signature title and percent-encode its middle dot into the URL
		// (SROM·18·2025 -> srom%c2%b718%c2%b72025). Fall back to a de-punctuated
		// signature when the volume/year columns are absent.
		$vol_col  = isset( $this->row_assoc['volume'] ) ? SROM_Imp_Spreadsheet::clean_cell( $this->row_assoc['volume'] ) : '';
		$year_col = isset( $this->row_assoc['year'] ) ? SROM_Imp_Spreadsheet::clean_cell( $this->row_assoc['year'] ) : '';
		$slug     = trim( $vol_col . '-' . $year_col, '-' );
		if ( '' === $slug ) {
			$slug = preg_replace( '/[^a-z0-9]+/i', '-', $signature );
		}
		// Title format "Tom: 18·2025" (locked decision 2026-07): built from the
		// volume/year columns, NOT from the signature, so a stray "SROM·" prefix
		// can never leak into the visible title. Falls back to the signature when
		// the columns are absent. U+00B7 middle dot, matching the signature style.
		if ( '' !== $vol_col && '' !== $year_col ) {
			$title = 'Tom: ' . $vol_col . "\u{00B7}" . $year_col;
		} else {
			$title = $signature;
		}
		$volume_id = wp_insert_post(
			wp_slash(
				array(
					'post_type'   => 'srom_volume',
					'post_status' => $this->job['options']['new_status'],
					'post_title'  => $title,
					'post_name'   => sanitize_title( $slug ),
				)
			),
			true
		);
		if ( is_wp_error( $volume_id ) ) {
			return array( 'id' => null, 'deferred' => false, 'msgs' => array( 'could not create volume "' . $signature . '": ' . $volume_id->get_error_message() ) );
		}

		$msgs = array( 'created volume "' . $signature . '" (#' . $volume_id . ', ' . $this->job['options']['new_status'] . ')' );

		// Fill the new volume with whatever volume data this row carries.
		$fields  = $this->get_volume_fields();
		$sources = array(
			'signature' => array( 'issue_signature', 'signature' ),
			'volume'    => array( 'volume' ),
			'year'      => array( 'year' ),
			'theme'     => array( 'issue_theme', 'theme' ),
			'pub_date'  => array( 'pub_date_online', 'pub_date' ),
		);
		foreach ( $sources as $field_name => $columns ) {
			if ( ! isset( $fields[ $field_name ] ) ) {
				continue;
			}
			$raw = '';
			foreach ( $columns as $col ) {
				if ( isset( $this->row_assoc[ $col ] ) && '' !== $this->row_assoc[ $col ] ) {
					$raw = $this->row_assoc[ $col ];
					break;
				}
			}
			if ( 'signature' === $field_name && '' === $raw ) {
				$raw = $signature; // always store the key we matched on
			}
			if ( '' === $raw ) {
				continue;
			}
			$res = SROM_Imp_Coerce::coerce( $fields[ $field_name ], $raw, array( 'runner' => $this, 'dry' => false, 'options' => $this->job['options'], 'row_assoc' => $this->row_assoc ) );
			if ( 'ok' === $res['status'] ) {
				update_field( $fields[ $field_name ]['key'], $res['value'], $volume_id );
			} else {
				foreach ( $res['msgs'] as $m ) {
					$msgs[] = 'volume ' . $field_name . ': ' . $m;
				}
			}
		}

		$this->job['volume_cache'][ $signature ] = (int) $volume_id;
		return array( 'id' => (int) $volume_id, 'deferred' => false, 'msgs' => $msgs );
	}

	private function get_volume_fields() {
		if ( null !== $this->volume_fields ) {
			return $this->volume_fields;
		}
		$this->volume_fields = array();
		if ( SROM_Imp_Fields::acf_active() ) {
			$groups = acf_get_field_groups( array( 'post_type' => 'srom_volume' ) );
			foreach ( (array) $groups as $group ) {
				foreach ( (array) acf_get_fields( $group ) as $f ) {
					if ( ! empty( $f['name'] ) && ! isset( $this->volume_fields[ $f['name'] ] ) ) {
						$this->volume_fields[ $f['name'] ] = $f;
					}
				}
			}
		}
		return $this->volume_fields;
	}

	/**
	 * Resolve an attachment token (ID, media-library file name, or URL).
	 *
	 * @return array ['id'=>int|null, 'msgs'=>string[]]
	 */
	public function resolve_attachment( $token, $must_be_image ) {
		$token = SROM_Imp_Spreadsheet::clean_cell( $token );
		if ( '' === $token ) {
			return array( 'id' => null, 'msgs' => array() );
		}

		if ( preg_match( '/^\d+$/', $token ) ) {
			$p = get_post( (int) $token );
			if ( $p && 'attachment' === $p->post_type ) {
				return $this->check_image( (int) $p->ID, $must_be_image );
			}
			return array( 'id' => null, 'msgs' => array( 'no media item with ID ' . (int) $token . ' — field skipped' ) );
		}

		$is_url = (bool) preg_match( '#^https?://#i', $token );

		if ( $is_url ) {
			$id = attachment_url_to_postid( $token );
			if ( $id ) {
				return $this->check_image( (int) $id, $must_be_image );
			}
		}

		// Match by file name in the media library.
		$basename = wp_basename( $is_url ? (string) wp_parse_url( $token, PHP_URL_PATH ) : $token );
		if ( '' !== $basename ) {
			global $wpdb;
			$like = '%' . $wpdb->esc_like( '/' . $basename );
			$ids  = $wpdb->get_col(
				$wpdb->prepare(
					"SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND (meta_value LIKE %s OR meta_value = %s) ORDER BY post_id ASC LIMIT 2",
					$like,
					$basename
				)
			);
			if ( count( $ids ) === 1 ) {
				return $this->check_image( (int) $ids[0], $must_be_image );
			}
			if ( count( $ids ) > 1 ) {
				return array( 'id' => null, 'msgs' => array( 'several media items are named "' . SROM_Imp_Coerce::shorten( $basename ) . '" — use the attachment ID. Field skipped.' ) );
			}
		}

		// Optional download.
		if ( $is_url && ! empty( $this->job['options']['sideload'] ) ) {
			if ( $this->dry ) {
				return array( 'id' => null, 'msgs' => array( '"' . SROM_Imp_Coerce::shorten( $basename ? $basename : $token ) . '" is not in the media library — it will be downloaded during import' ) );
			}
			return $this->sideload( $token, $must_be_image );
		}

		return array( 'id' => null, 'msgs' => array( '"' . SROM_Imp_Coerce::shorten( $basename ? $basename : $token ) . '" was not found in the media library' . ( $is_url ? ' (enable "download files" in the options to fetch it)' : '' ) . ' — field skipped' ) );
	}

	private function check_image( $id, $must_be_image ) {
		if ( $must_be_image && ! wp_attachment_is_image( $id ) ) {
			return array( 'id' => null, 'msgs' => array( 'media item #' . $id . ' is not an image — field skipped' ) );
		}
		return array( 'id' => $id, 'msgs' => array() );
	}

	private function sideload( $url, $must_be_image ) {
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';

		$tmp = download_url( $url, 60 );
		if ( is_wp_error( $tmp ) ) {
			return array( 'id' => null, 'msgs' => array( 'download failed for "' . SROM_Imp_Coerce::shorten( $url ) . '": ' . $tmp->get_error_message() . ' — field skipped' ) );
		}
		$file_array = array(
			'name'     => wp_basename( (string) wp_parse_url( $url, PHP_URL_PATH ) ),
			'tmp_name' => $tmp,
		);
		if ( '' === $file_array['name'] ) {
			$file_array['name'] = 'srom-import-' . time();
		}
		$id = media_handle_sideload( $file_array, 0 );
		if ( is_wp_error( $id ) ) {
			@unlink( $tmp );
			return array( 'id' => null, 'msgs' => array( 'could not add "' . SROM_Imp_Coerce::shorten( $file_array['name'] ) . '" to the media library: ' . $id->get_error_message() . ' — field skipped' ) );
		}
		$res         = $this->check_image( (int) $id, $must_be_image );
		$res['msgs'] = array_merge( array( 'downloaded "' . SROM_Imp_Coerce::shorten( $file_array['name'] ) . '" into the media library (#' . $id . ')' ), $res['msgs'] );
		return $res;
	}

	/**
	 * Resolve taxonomy terms for an ACF taxonomy field.
	 *
	 * @return array coerce-style result.
	 */
	public function resolve_terms( array $field, array $tokens ) {
		$taxonomy = isset( $field['taxonomy'] ) ? $field['taxonomy'] : '';
		if ( ! $taxonomy || ! taxonomy_exists( $taxonomy ) ) {
			return array( 'status' => 'skip', 'value' => null, 'msgs' => array( 'the taxonomy "' . $taxonomy . '" does not exist — field skipped' ) );
		}
		$ids  = array();
		$msgs = array();
		foreach ( $tokens as $tok ) {
			$term = get_term_by( 'name', $tok, $taxonomy );
			if ( ! $term ) {
				$term = get_term_by( 'slug', sanitize_title( $tok ), $taxonomy );
			}
			if ( ! $term ) {
				if ( empty( $this->job['options']['create_terms'] ) ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => array( 'term "' . SROM_Imp_Coerce::shorten( $tok ) . '" does not exist in ' . $taxonomy . ' and term creation is disabled — field skipped' ) );
				}
				if ( $this->dry ) {
					$msgs[] = 'term "' . SROM_Imp_Coerce::shorten( $tok ) . '" will be created in ' . $taxonomy . ' during import';
					continue;
				}
				$new = wp_insert_term( $tok, $taxonomy );
				if ( is_wp_error( $new ) ) {
					return array( 'status' => 'skip', 'value' => null, 'msgs' => array( 'could not create term "' . SROM_Imp_Coerce::shorten( $tok ) . '": ' . $new->get_error_message() . ' — field skipped' ) );
				}
				$msgs[] = 'created term "' . SROM_Imp_Coerce::shorten( $tok ) . '" in ' . $taxonomy;
				$ids[]  = (int) $new['term_id'];
				continue;
			}
			$ids[] = (int) $term->term_id;
		}
		$single = in_array( ( isset( $field['field_type'] ) ? $field['field_type'] : 'checkbox' ), array( 'radio', 'select' ), true );
		if ( $this->dry && empty( $ids ) && ! empty( $msgs ) ) {
			return array( 'status' => 'skip', 'value' => null, 'msgs' => $msgs );
		}
		return array( 'status' => 'ok', 'value' => $single ? ( $ids ? $ids[0] : '' ) : $ids, 'msgs' => $msgs );
	}
}
