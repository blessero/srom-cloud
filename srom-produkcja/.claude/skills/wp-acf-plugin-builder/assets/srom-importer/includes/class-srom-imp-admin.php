<?php
/**
 * Admin UI: top-level "SROM Importer" menu (own icon, like ACF's).
 *
 * Flow: 1) upload file + choose post type  2) map columns to fields
 *       3) dry-run preview (nothing written)  4) import, in small batches.
 *
 * All state lives server-side in the job option; the browser only asks
 * "process the next batch", so a lost connection or closed tab can always
 * be resumed from where it stopped.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Admin {

	const CAP  = 'manage_options';
	const SLUG = 'srom-importer';

	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_post_srom_imp_upload', array( __CLASS__, 'handle_upload' ) );
		add_action( 'admin_post_srom_imp_map', array( __CLASS__, 'handle_map' ) );
		add_action( 'admin_post_srom_imp_setup', array( __CLASS__, 'handle_setup' ) );
		add_action( 'admin_post_srom_imp_discard', array( __CLASS__, 'handle_discard' ) );
		add_action( 'wp_ajax_srom_imp_start', array( __CLASS__, 'ajax_start' ) );
		add_action( 'wp_ajax_srom_imp_batch', array( __CLASS__, 'ajax_batch' ) );
	}

	public static function menu() {
		add_menu_page( 'SROM Importer', 'SROM Importer', self::CAP, self::SLUG, array( __CLASS__, 'render' ), self::icon(), 80 );
	}

	/**
	 * The SROM wheel as a base64 data URI, for the admin-menu icon slot.
	 */
	private static function icon() {
		return 'data:image/svg+xml;base64,' . base64_encode( '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44.19 44.19"><path fill="#df2d22" d="M44.19,22.09c0,12.21-9.9,22.1-22.1,22.1S0,34.3,0,22.09,9.89,0,22.09,0s22.1,9.89,22.1,22.09ZM16.18,20.11s-10.46-3.6-10.51-3.61c-.24-.09-.5-.14-.77-.14-1.29,0-2.34,1.05-2.34,2.34s.97,2.25,2.19,2.33c.04,0,11.16.68,11.2.68.45,0,.81-.37.81-.82,0-.38-.25-.68-.58-.78M28.14,24.11s10.46,3.6,10.51,3.61c.23.09.49.13.76.13,1.29,0,2.33-1.04,2.33-2.33s-.97-2.25-2.19-2.33c-.03,0-11.16-.68-11.19-.68-.45,0-.81.37-.81.82,0,.37.24.68.58.78M15.87,22.56s-11.04.68-11.08.68c-.25.02-.51.07-.76.18-1.2.49-1.76,1.86-1.27,3.04.47,1.15,1.76,1.71,2.92,1.31.04,0,10.57-3.64,10.6-3.65.41-.18.62-.66.45-1.07-.15-.34-.5-.54-.86-.49M28.44,21.67s11.05-.69,11.09-.69c.25-.02.51-.07.78-.18,1.18-.49,1.74-1.85,1.26-3.05-.48-1.15-1.77-1.71-2.92-1.31-.05.02-10.58,3.64-10.6,3.65-.43.17-.62.66-.45,1.07.14.35.49.54.84.5M16.51,24.92s-9.94,4.86-9.97,4.88c-.24.1-.45.26-.64.45-.92.91-.92,2.39,0,3.3.87.88,2.28.92,3.2.1.02-.02,8.37-7.41,8.39-7.42.32-.33.32-.84,0-1.17-.26-.25-.66-.3-.97-.14M27.8,19.3s9.94-4.86,9.98-4.87c.23-.12.45-.27.64-.46.91-.91.91-2.39,0-3.31-.88-.88-2.29-.9-3.19-.09-.03.02-8.37,7.41-8.41,7.42-.31.32-.31.84,0,1.16.27.26.68.31.98.14M18.02,26.87s-7.33,8.28-7.35,8.32c-.17.2-.31.42-.41.66-.5,1.2.07,2.57,1.25,3.05,1.16.48,2.46-.03,3-1.14,0-.03,4.91-10.04,4.91-10.07.17-.42-.02-.9-.44-1.08-.34-.14-.73-.02-.95.26M26.3,17.36s7.32-8.3,7.35-8.33c.18-.19.32-.41.43-.66.48-1.19-.08-2.56-1.28-3.05-1.14-.48-2.45.04-2.98,1.14-.02.04-4.9,10.05-4.92,10.08-.17.42.03.9.45,1.07.34.14.73.03.95-.24M20.16,28.09s-3.6,10.47-3.6,10.5c-.08.25-.14.51-.14.78,0,1.29,1.05,2.33,2.34,2.33s2.26-.96,2.33-2.2c0-.03.68-11.14.68-11.18,0-.46-.37-.82-.81-.82-.38,0-.69.25-.79.58M24.16,16.13s3.6-10.47,3.6-10.51c.1-.24.14-.5.14-.77,0-1.3-1.04-2.34-2.33-2.34s-2.25.97-2.33,2.2c0,.03-.68,11.15-.68,11.18,0,.46.37.82.82.82.37,0,.69-.25.78-.58M22.6,28.4s.69,11.05.69,11.09c0,.26.06.52.18.76.5,1.2,1.85,1.77,3.05,1.27,1.14-.48,1.71-1.76,1.31-2.92-.01-.03-3.64-10.57-3.65-10.6-.17-.42-.66-.62-1.07-.44-.35.14-.54.5-.5.84M21.72,15.82s-.69-11.04-.69-11.08c-.02-.26-.07-.52-.18-.77-.49-1.19-1.86-1.76-3.04-1.27-1.15.48-1.71,1.77-1.33,2.93.03.04,3.65,10.57,3.66,10.6.18.41.65.61,1.07.44.35-.15.54-.5.5-.85M24.98,27.76s4.86,9.94,4.87,9.97c.12.23.26.45.46.64.91.92,2.37.92,3.3,0,.88-.88.9-2.28.1-3.2-.02-.03-7.41-8.37-7.43-8.4-.31-.32-.84-.32-1.16,0-.26.26-.32.66-.13.98M19.35,16.47s-4.86-9.95-4.88-9.97c-.11-.24-.25-.46-.44-.65-.92-.91-2.39-.91-3.32,0-.87.88-.9,2.28-.09,3.19.03.03,7.41,8.38,7.42,8.4.33.32.85.32,1.16,0,.26-.26.31-.66.14-.96M26.92,26.25s8.29,7.33,8.32,7.35c.2.17.42.32.67.42,1.18.5,2.56-.06,3.04-1.25.48-1.15-.03-2.46-1.13-2.99-.03-.02-10.05-4.9-10.08-4.91-.42-.18-.89.02-1.06.44-.14.34-.04.72.24.95M17.4,17.98s-8.29-7.33-8.33-7.35c-.19-.18-.41-.33-.66-.43-1.19-.49-2.55.06-3.05,1.26-.48,1.15.04,2.45,1.14,2.99.02.01,10.05,4.9,10.07,4.91.42.17.9-.02,1.07-.44.15-.34.03-.73-.25-.95"/></svg>' );
	}

	/* ------------------------------------------------------------ helpers */

	private static function url( array $args = array() ) {
		return add_query_arg( array_merge( array( 'page' => self::SLUG ), $args ), admin_url( 'admin.php' ) );
	}

	private static function job_url( $token, array $args = array() ) {
		// Built raw with add_query_arg (NOT wp_nonce_url, which HTML-escapes
		// the URL for display and would corrupt Location: headers).
		$url = self::url( array_merge( array( 'job' => $token ), $args ) );
		return add_query_arg( '_wpnonce', wp_create_nonce( 'srom_imp_view_' . $token ), $url );
	}

	private static function notice( $msg, $type = 'error' ) {
		set_transient( 'srom_imp_notice_' . get_current_user_id(), array( 'msg' => $msg, 'type' => $type ), 120 );
	}

	private static function take_notice() {
		$key = 'srom_imp_notice_' . get_current_user_id();
		$n   = get_transient( $key );
		if ( $n ) {
			delete_transient( $key );
		}
		return is_array( $n ) ? $n : null;
	}

	/**
	 * Load a job and verify URL nonce + ownership. Returns array|null.
	 */
	private static function current_job() {
		if ( empty( $_GET['job'] ) ) {
			return null;
		}
		$token = SROM_Imp_Jobs::clean_token( wp_unslash( $_GET['job'] ) );
		if ( '' === $token ) {
			return null;
		}
		if ( empty( $_GET['_wpnonce'] ) || ! wp_verify_nonce( wp_unslash( $_GET['_wpnonce'] ), 'srom_imp_view_' . $token ) ) {
			return null;
		}
		$job = SROM_Imp_Jobs::get( $token );
		if ( ! $job || (int) $job['user_id'] !== get_current_user_id() ) {
			return null;
		}
		return $job;
	}

	private static function default_options() {
		return array(
			'update_existing' => 1,
			'new_status'      => 'draft',
			'empty_cells'     => 'keep',
			'link_volumes'    => 1,
			'sideload'        => 0,
			'create_terms'    => 1,
		);
	}

	private static function zero_counts() {
		return array( 'created' => 0, 'updated' => 0, 'skipped' => 0, 'errors' => 0, 'warnings' => 0 );
	}

	/* ------------------------------------------------------- POST handlers */

	public static function handle_upload() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_die( 'Insufficient permissions.' );
		}
		check_admin_referer( 'srom_imp_upload' );

		$back = self::url();

		$post_type = isset( $_POST['post_type'] ) ? sanitize_key( wp_unslash( $_POST['post_type'] ) ) : '';
		if ( ! isset( SROM_Imp_Fields::post_types()[ $post_type ] ) ) {
			self::notice( 'Please choose a valid post type.' );
			wp_safe_redirect( $back );
			exit;
		}

		if ( empty( $_FILES['srom_file'] ) || ! is_array( $_FILES['srom_file'] ) ) {
			self::notice( 'No file received. Please choose a spreadsheet file.' );
			wp_safe_redirect( $back );
			exit;
		}
		$file = $_FILES['srom_file'];
		if ( ! empty( $file['error'] ) || empty( $file['tmp_name'] ) ) {
			$errors = array(
				UPLOAD_ERR_INI_SIZE  => 'The file exceeds the server upload limit (upload_max_filesize).',
				UPLOAD_ERR_FORM_SIZE => 'The file exceeds the upload limit.',
				UPLOAD_ERR_PARTIAL   => 'The upload was interrupted — please try again.',
				UPLOAD_ERR_NO_FILE   => 'No file received. Please choose a spreadsheet file.',
			);
			$code   = isset( $file['error'] ) ? (int) $file['error'] : -1;
			self::notice( isset( $errors[ $code ] ) ? $errors[ $code ] : 'The upload failed (code ' . $code . '). Please try again.' );
			wp_safe_redirect( $back );
			exit;
		}
		if ( (int) $file['size'] > SROM_IMP_MAX_FILE_BYTES ) {
			self::notice( 'The file is larger than the ' . size_format( SROM_IMP_MAX_FILE_BYTES ) . ' limit.' );
			wp_safe_redirect( $back );
			exit;
		}
		$orig_name = sanitize_file_name( (string) $file['name'] );
		$ext       = strtolower( (string) pathinfo( $orig_name, PATHINFO_EXTENSION ) );
		if ( ! in_array( $ext, array( 'csv', 'tsv', 'txt', 'xlsx' ), true ) ) {
			self::notice( 'Unsupported file type ".' . esc_html( $ext ) . '". Please upload a .csv, .tsv, .txt or .xlsx file (from Excel/Google Sheets use “Download as CSV”).' );
			wp_safe_redirect( $back );
			exit;
		}
		if ( ! is_uploaded_file( $file['tmp_name'] ) ) {
			self::notice( 'The upload could not be verified. Please try again.' );
			wp_safe_redirect( $back );
			exit;
		}

		$dir = SROM_Imp_Jobs::ensure_upload_dir();
		if ( is_wp_error( $dir ) ) {
			self::notice( $dir->get_error_message() );
			wp_safe_redirect( $back );
			exit;
		}
		$token = SROM_Imp_Jobs::new_token();
		$dest  = $dir . '/job-' . $token . '.' . $ext;
		if ( ! @move_uploaded_file( $file['tmp_name'], $dest ) ) {
			self::notice( 'Could not store the uploaded file in ' . esc_html( $dir ) . '. Check that the uploads folder is writable.' );
			wp_safe_redirect( $back );
			exit;
		}
		@chmod( $dest, 0644 );

		$parsed = SROM_Imp_Spreadsheet::parse( $dest, $ext, true );
		if ( is_wp_error( $parsed ) ) {
			@unlink( $dest );
			self::notice( $parsed->get_error_message() );
			wp_safe_redirect( $back );
			exit;
		}

		$t_info  = SROM_Imp_Fields::get_targets( $post_type );
		$mapping = SROM_Imp_Fields::auto_map( $t_info['targets'], $parsed['header'] );

		$job = array(
			'file'           => $dest,
			'orig_name'      => $orig_name,
			'ext'            => $ext,
			'post_type'      => $post_type,
			'header'         => $parsed['header'],
			'total_rows'     => count( $parsed['rows'] ),
			'sample'         => isset( $parsed['rows'][0] ) ? $parsed['rows'][0]['cells'] : array(),
			'parse_warnings' => $parsed['warnings'],
			'skipped_empty'  => (int) $parsed['skipped_empty'],
			'mapping'        => $mapping,
			'key_target'     => SROM_Imp_Fields::default_key( $t_info['targets'], $mapping ),
			'options'        => self::default_options(),
			'state'          => 'new',
			'next_row'       => 0,
			'counts'         => self::zero_counts(),
			'log'            => array(),
			'seen_keys'      => array(),
			'volume_cache'   => array(),
		);
		$token = SROM_Imp_Jobs::create( $job );

		wp_safe_redirect( self::job_url( $token, array( 'step' => 'map' ) ) );
		exit;
	}

	public static function handle_map() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_die( 'Insufficient permissions.' );
		}
		$token = isset( $_POST['job'] ) ? SROM_Imp_Jobs::clean_token( wp_unslash( $_POST['job'] ) ) : '';
		check_admin_referer( 'srom_imp_map_' . $token );

		$job = SROM_Imp_Jobs::get( $token );
		if ( ! $job || (int) $job['user_id'] !== get_current_user_id() ) {
			self::notice( 'This import session has expired. Please upload the file again.' );
			wp_safe_redirect( self::url() );
			exit;
		}

		$t_info  = SROM_Imp_Fields::get_targets( $job['post_type'] );
		$by_id   = array();
		foreach ( $t_info['targets'] as $t ) {
			$by_id[ $t['id'] ] = $t;
		}
		$ncols = count( $job['header'] );

		$raw_map   = isset( $_POST['map'] ) && is_array( $_POST['map'] ) ? wp_unslash( $_POST['map'] ) : array();
		$raw_tr    = isset( $_POST['transform'] ) && is_array( $_POST['transform'] ) ? wp_unslash( $_POST['transform'] ) : array();
		$mapping   = array();
		foreach ( $raw_map as $target_id => $col ) {
			$target_id = (string) $target_id;
			if ( ! isset( $by_id[ $target_id ] ) || '' === (string) $col || ! is_numeric( $col ) ) {
				continue;
			}
			$col = (int) $col;
			if ( $col < 0 || $col >= $ncols ) {
				continue;
			}
			$transform = null;
			$allowed_tr = SROM_Imp_Fields::optional_transforms();
			if ( isset( $raw_tr[ $target_id ], $allowed_tr[ $by_id[ $target_id ]['name'] ] )
				&& (string) $raw_tr[ $target_id ] === $allowed_tr[ $by_id[ $target_id ]['name'] ][0] ) {
				$transform = $allowed_tr[ $by_id[ $target_id ]['name'] ][0];
			}
			$mapping[ $target_id ] = array( 'col' => $col, 'transform' => $transform, 'auto' => '' );
		}

		if ( empty( $mapping ) ) {
			self::notice( 'Nothing is mapped. Map at least the key column and one field.' );
			wp_safe_redirect( self::job_url( $token, array( 'step' => 'map' ) ) );
			exit;
		}

		$key_target = isset( $_POST['key_target'] ) ? (string) wp_unslash( $_POST['key_target'] ) : '';
		if ( ! isset( $by_id[ $key_target ] ) || ! SROM_Imp_Fields::key_eligible( $by_id[ $key_target ] ) ) {
			self::notice( 'Please choose a valid key field for matching existing posts.' );
			wp_safe_redirect( self::job_url( $token, array( 'step' => 'map' ) ) );
			exit;
		}
		if ( ! isset( $mapping[ $key_target ] ) ) {
			self::notice( 'The key field "' . esc_html( $by_id[ $key_target ]['label'] ) . '" must be mapped to a column.' );
			wp_safe_redirect( self::job_url( $token, array( 'step' => 'map' ) ) );
			exit;
		}

		$statuses = array( 'draft', 'publish', 'pending', 'private' );
		$empties  = array( 'keep', 'clear' );
		$options  = array(
			'update_existing' => empty( $_POST['opt_update_existing'] ) ? 0 : 1,
			'new_status'      => in_array( isset( $_POST['opt_new_status'] ) ? wp_unslash( $_POST['opt_new_status'] ) : 'draft', $statuses, true ) ? wp_unslash( $_POST['opt_new_status'] ) : 'draft',
			'empty_cells'     => in_array( isset( $_POST['opt_empty_cells'] ) ? wp_unslash( $_POST['opt_empty_cells'] ) : 'keep', $empties, true ) ? wp_unslash( $_POST['opt_empty_cells'] ) : 'keep',
			'link_volumes'    => empty( $_POST['opt_link_volumes'] ) ? 0 : 1,
			'sideload'        => empty( $_POST['opt_sideload'] ) ? 0 : 1,
			'create_terms'    => empty( $_POST['opt_create_terms'] ) ? 0 : 1,
		);

		$job['mapping']     = $mapping;
		$job['key_target']  = $key_target;
		$job['options']     = $options;
		$job['state']       = 'mapped';
		$job['next_row']    = 0;
		$job['counts']      = self::zero_counts();
		$job['log']         = array();
		$job['seen_keys']   = array();
		$job['volume_cache'] = array();
		unset( $job['log_truncated'] );
		SROM_Imp_Jobs::save( $token, $job );

		wp_safe_redirect( self::job_url( $token, array( 'step' => 'run' ) ) );
		exit;
	}

	public static function handle_setup() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_die( 'Insufficient permissions.' );
		}
		check_admin_referer( 'srom_imp_setup' );
		$do = isset( $_POST['srom_setup_action'] ) ? sanitize_key( wp_unslash( $_POST['srom_setup_action'] ) ) : '';

		if ( 'install' === $do || 'reinstall' === $do ) {
			$report = SROM_Imp_Setup::install( 'reinstall' === $do );
			update_option( 'srom_imp_setup_done', '1', false );
			update_option( 'srom_imp_setup_version', SROM_IMP_VERSION, false );
			delete_option( 'srom_imp_autoinstall_pending' );
			flush_rewrite_rules( false );
			if ( ! empty( $report['errors'] ) ) {
				self::notice( 'Setup finished with problems: ' . implode( ' ', $report['errors'] ) );
			} else {
				$made = count( $report['created'] );
				$upd  = count( $report['updated'] );
				$kept = count( $report['kept'] );
				self::notice(
					'ACF definitions ready — created ' . $made . ', updated ' . $upd . ', left untouched ' . $kept . '. They are now editable under Custom Fields → Post Types / Taxonomies / Field Groups.',
					'success'
				);
			}
		} elseif ( 'remove' === $do ) {
			$report = SROM_Imp_Setup::remove();
			update_option( 'srom_imp_setup_done', '1', false ); // don't auto-reinstall
			flush_rewrite_rules( false );
			self::notice(
				empty( $report['errors'] )
					? 'Removed ' . count( $report['removed'] ) . ' ACF definition(s). Your articles, volumes and their data were not touched.'
					: 'Removal finished with problems: ' . implode( ' ', $report['errors'] ),
				empty( $report['errors'] ) ? 'success' : 'error'
			);
		}

		wp_safe_redirect( self::url( array( 'tab' => 'setup' ) ) );
		exit;
	}

	public static function handle_discard() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_die( 'Insufficient permissions.' );
		}
		$token = isset( $_POST['job'] ) ? SROM_Imp_Jobs::clean_token( wp_unslash( $_POST['job'] ) ) : '';
		check_admin_referer( 'srom_imp_discard_' . $token );
		$job = SROM_Imp_Jobs::get( $token );
		if ( $job && (int) $job['user_id'] === get_current_user_id() ) {
			SROM_Imp_Jobs::delete( $token );
		}
		self::notice( 'Import session discarded. Nothing else was changed.', 'success' );
		wp_safe_redirect( self::url() );
		exit;
	}

	/* --------------------------------------------------------------- AJAX */

	private static function ajax_job() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_send_json_error( array( 'message' => 'Insufficient permissions.' ), 403 );
		}
		check_ajax_referer( 'srom_imp_ajax' );
		$token = isset( $_POST['job'] ) ? SROM_Imp_Jobs::clean_token( wp_unslash( $_POST['job'] ) ) : '';
		$job   = SROM_Imp_Jobs::get( $token );
		if ( ! $job || (int) $job['user_id'] !== get_current_user_id() ) {
			wp_send_json_error( array( 'message' => 'This import session has expired. Please upload the file again.' ), 410 );
		}
		return array( $token, $job );
	}

	public static function ajax_start() {
		list( $token, $job ) = self::ajax_job();
		$mode = isset( $_POST['mode'] ) && 'import' === $_POST['mode'] ? 'import' : 'preview';

		if ( 'preview' === $mode ) {
			$allowed = array( 'mapped', 'previewed', 'done', 'preview_running' );
			if ( ! in_array( $job['state'], $allowed, true ) ) {
				wp_send_json_error( array( 'message' => 'Preview cannot start from state "' . esc_html( $job['state'] ) . '".' ) );
			}
			if ( 'preview_running' !== $job['state'] ) {
				$job = self::reset_run( $job );
				$job['state'] = 'preview_running';
			}
		} else {
			$allowed = array( 'previewed', 'done', 'import_running' );
			if ( ! in_array( $job['state'], $allowed, true ) ) {
				wp_send_json_error( array( 'message' => 'Run the preview first — the import only starts after a completed preview.' ) );
			}
			if ( 'import_running' !== $job['state'] ) {
				$job = self::reset_run( $job );
				$job['state'] = 'import_running';
			}
		}
		SROM_Imp_Jobs::save( $token, $job );
		wp_send_json_success(
			array(
				'state'    => $job['state'],
				'next_row' => (int) $job['next_row'],
				'total'    => (int) $job['total_rows'],
				'counts'   => $job['counts'],
			)
		);
	}

	private static function reset_run( array $job ) {
		$job['next_row']    = 0;
		$job['counts']      = self::zero_counts();
		$job['log']         = array();
		$job['seen_keys']   = array();
		$job['volume_cache'] = array();
		unset( $job['log_truncated'] );
		return $job;
	}

	public static function ajax_batch() {
		list( $token, $job ) = self::ajax_job();
		$mode   = isset( $_POST['mode'] ) && 'import' === $_POST['mode'] ? 'import' : 'preview';
		$runner = new SROM_Imp_Runner( $token, $job );
		$result = $runner->process_batch( $mode );
		if ( is_wp_error( $result ) ) {
			wp_send_json_error( array( 'message' => $result->get_error_message() ) );
		}
		wp_send_json_success( $result );
	}

	/* ------------------------------------------------------------- render */

	public static function render() {
		if ( ! current_user_can( self::CAP ) ) {
			wp_die( 'Insufficient permissions.' );
		}
		SROM_Imp_Jobs::cleanup();

		$tab = isset( $_GET['tab'] ) ? sanitize_key( wp_unslash( $_GET['tab'] ) ) : 'import';
		if ( ! in_array( $tab, array( 'import', 'setup', 'help' ), true ) ) {
			$tab = 'import';
		}

		echo '<div class="wrap srom-imp">';
		echo '<h1>SROM Importer</h1>';
		self::styles();

		$notice = self::take_notice();
		if ( $notice ) {
			$class = ( 'success' === $notice['type'] ) ? 'notice-success' : 'notice-error';
			echo '<div class="notice ' . esc_attr( $class ) . ' is-dismissible"><p>' . esc_html( $notice['msg'] ) . '</p></div>';
		}
		if ( ! SROM_Imp_Fields::acf_active() ) {
			echo '<div class="notice notice-error"><p><strong>Advanced Custom Fields is not active.</strong> The importer needs the ACF plugin (the free version is enough) to read field definitions. Only core post fields can be imported until it is activated.</p></div>';
		}

		echo '<nav class="nav-tab-wrapper">';
		foreach ( array( 'import' => 'Import', 'setup' => 'Setup & status', 'help' => 'Help' ) as $slug => $label ) {
			$class = ( $tab === $slug ) ? ' nav-tab-active' : '';
			echo '<a class="nav-tab' . esc_attr( $class ) . '" href="' . esc_url( self::url( array( 'tab' => $slug ) ) ) . '">' . esc_html( $label ) . '</a>';
		}
		echo '</nav>';

		if ( 'setup' === $tab ) {
			self::render_setup();
		} elseif ( 'help' === $tab ) {
			self::render_help();
		} else {
			$job = self::current_job();
			if ( ! $job ) {
				self::render_upload();
			} else {
				$step = isset( $_GET['step'] ) ? sanitize_key( wp_unslash( $_GET['step'] ) ) : 'map';
				if ( 'run' === $step && 'new' !== $job['state'] ) {
					self::render_run( $job );
				} else {
					self::render_map( $job );
				}
			}
		}
		echo '</div>';
	}

	private static function styles() {
		?>
<style>
.srom-imp .srom-card{background:#fff;border:1px solid #c3c4c7;border-radius:4px;padding:16px 20px;margin:16px 0;max-width:1100px}
.srom-imp table.srom-map{border-collapse:collapse;width:100%;max-width:1100px}
.srom-imp table.srom-map th,.srom-imp table.srom-map td{border-bottom:1px solid #eee;padding:8px 10px;text-align:left;vertical-align:top}
.srom-imp table.srom-map tr.srom-group th{background:#f0f0f1;font-size:13px;padding:6px 10px}
.srom-imp .srom-fieldname{color:#646970;font-family:monospace;font-size:12px}
.srom-imp .srom-type{display:inline-block;background:#f0f0f1;border-radius:3px;padding:1px 6px;font-size:11px;color:#3c434a;margin-left:6px}
.srom-imp .srom-note{color:#646970;font-size:12px;max-width:340px}
.srom-imp .srom-sample{color:#2271b1;font-size:12px;font-family:monospace;word-break:break-all;max-width:260px;display:inline-block}
.srom-imp .srom-auto{font-size:11px;color:#008a20;margin-left:6px}
.srom-imp .srom-chips{margin:12px 0}
.srom-imp .srom-chip{display:inline-block;border-radius:14px;padding:3px 12px;margin-right:8px;background:#f0f0f1;font-size:13px}
.srom-imp .srom-chip b{font-size:14px}
.srom-imp .srom-chip.err{background:#fcf0f1;color:#8a1f11}
.srom-imp .srom-chip.warn{background:#fcf9e8;color:#674600}
.srom-imp .srom-chip.ok{background:#edfaef;color:#00450c}
.srom-imp .srom-progress{background:#f0f0f1;border-radius:4px;height:22px;max-width:1100px;overflow:hidden;margin:10px 0;display:none}
.srom-imp .srom-progress-bar{background:#2271b1;height:100%;width:0;color:#fff;font-size:12px;line-height:22px;text-align:center;transition:width .2s;white-space:nowrap}
.srom-imp table.srom-log{border-collapse:collapse;width:100%;max-width:1100px;background:#fff}
.srom-imp table.srom-log th,.srom-imp table.srom-log td{border-bottom:1px solid #eee;padding:5px 10px;text-align:left;font-size:13px;vertical-align:top}
.srom-imp table.srom-log td.act-error{color:#8a1f11;font-weight:600}
.srom-imp table.srom-log td.act-created,.srom-imp table.srom-log td.act-would-create{color:#00450c}
.srom-imp table.srom-log td.act-updated,.srom-imp table.srom-log td.act-would-update{color:#2271b1}
.srom-imp table.srom-log td.act-exists{color:#646970}
.srom-imp .srom-msgs{color:#674600;font-size:12px}
.srom-imp .srom-actions{margin:16px 0}
.srom-imp .srom-actions .button{margin-right:10px}
.srom-imp .srom-keyrow select{min-width:260px}
.srom-imp .srom-optlist label{display:block;margin:6px 0}
.srom-imp .srom-badfile{color:#8a1f11}
</style>
		<?php
	}

	private static function render_upload() {
		$types = SROM_Imp_Fields::post_types();
		?>
<div class="srom-card">
	<h2>1. Upload a spreadsheet</h2>
	<p>Accepted: <strong>.csv</strong>, <strong>.tsv</strong>, <strong>.xlsx</strong> (first sheet). Recommended: CSV (UTF-8).
	Extra columns are simply ignored, empty rows are skipped — nothing is written until you confirm after a preview.</p>
	<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" enctype="multipart/form-data">
		<?php wp_nonce_field( 'srom_imp_upload' ); ?>
		<input type="hidden" name="action" value="srom_imp_upload">
		<table class="form-table" role="presentation">
			<tr>
				<th scope="row"><label for="srom_file">Spreadsheet file</label></th>
				<td><input type="file" name="srom_file" id="srom_file" accept=".csv,.tsv,.txt,.xlsx" required></td>
			</tr>
			<tr>
				<th scope="row"><label for="srom_pt">Import into</label></th>
				<td>
					<select name="post_type" id="srom_pt">
						<?php foreach ( $types as $slug => $label ) : ?>
							<option value="<?php echo esc_attr( $slug ); ?>"><?php echo esc_html( $label ); ?></option>
						<?php endforeach; ?>
					</select>
					<p class="description">For the journal: articles → <code>srom_article</code>, volumes → <code>srom_volume</code>. When importing articles, missing volumes can be created and linked automatically.</p>
				</td>
			</tr>
		</table>
		<p><button type="submit" class="button button-primary">Continue to mapping →</button></p>
	</form>
</div>
		<?php
	}

	private static function render_map( array $job ) {
		$token  = $job['token'];
		$t_info = SROM_Imp_Fields::get_targets( $job['post_type'] );
		$header = $job['header'];
		$sample = isset( $job['sample'] ) ? $job['sample'] : array();

		// Column usage for the "ignored columns" summary.
		$used_cols = array();
		foreach ( $job['mapping'] as $m ) {
			$used_cols[ (int) $m['col'] ] = true;
		}

		echo '<div class="srom-card">';
		echo '<h2>2. Map columns to fields</h2>';
		echo '<p><strong>' . esc_html( $job['orig_name'] ) . '</strong> — ' . (int) $job['total_rows'] . ' data rows, ' . count( $header ) . ' columns → <strong>' . esc_html( $job['post_type'] ) . '</strong>. ';
		echo '<a href="' . esc_url( self::url() ) . '">Start over with a different file</a></p>';

		foreach ( (array) $job['parse_warnings'] as $w ) {
			echo '<div class="notice notice-warning inline"><p>' . esc_html( $w ) . '</p></div>';
		}
		if ( ! empty( $job['skipped_empty'] ) ) {
			echo '<p class="description">' . (int) $job['skipped_empty'] . ' empty row(s) in the file will be skipped automatically.</p>';
		}
		if ( ! empty( $t_info['unsupported'] ) ) {
			echo '<div class="notice notice-info inline"><p>These ACF fields exist but cannot be imported from a flat spreadsheet and are not listed: ' . esc_html( implode( ', ', $t_info['unsupported'] ) ) . '.</p></div>';
		}

		echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
		wp_nonce_field( 'srom_imp_map_' . $token );
		echo '<input type="hidden" name="action" value="srom_imp_map">';
		echo '<input type="hidden" name="job" value="' . esc_attr( $token ) . '">';

		echo '<table class="srom-map"><thead><tr><th style="width:30%">Field</th><th style="width:26%">Spreadsheet column</th><th style="width:22%">First-row value</th><th>Notes</th></tr></thead><tbody>';
		$current_group = null;
		foreach ( $t_info['targets'] as $t ) {
			if ( $t['group'] !== $current_group ) {
				$current_group = $t['group'];
				echo '<tr class="srom-group"><th colspan="4">' . esc_html( $current_group ) . '</th></tr>';
			}
			$m         = isset( $job['mapping'][ $t['id'] ] ) ? $job['mapping'][ $t['id'] ] : null;
			$selected  = $m ? (int) $m['col'] : -1;
			$auto_note = ( $m && ! empty( $m['auto'] ) ) ? ( 'preset' === $m['auto'] ? 'auto (SROM preset)' : 'auto (name match)' ) : '';

			echo '<tr>';
			echo '<td><strong>' . esc_html( $t['label'] ) . '</strong>';
			if ( $t['label'] !== $t['name'] ) {
				echo ' <span class="srom-fieldname">' . esc_html( $t['name'] ) . '</span>';
			}
			echo '<span class="srom-type">' . esc_html( $t['type'] ) . '</span>';
			if ( $auto_note ) {
				echo '<span class="srom-auto">' . esc_html( $auto_note ) . '</span>';
			}
			echo '</td>';

			echo '<td><select name="map[' . esc_attr( $t['id'] ) . ']" class="srom-col-select">';
			echo '<option value="">— not imported —</option>';
			foreach ( $header as $i => $col_name ) {
				echo '<option value="' . (int) $i . '"' . selected( $selected, (int) $i, false ) . '>' . esc_html( $col_name ) . '</option>';
			}
			echo '</select>';
			$opt_tr = SROM_Imp_Fields::optional_transforms();
			if ( isset( $opt_tr[ $t['name'] ] ) ) {
				list( $tr_slug, $tr_label ) = $opt_tr[ $t['name'] ];
				$checked = ( $m && $tr_slug === $m['transform'] ) ? ' checked' : '';
				echo '<br><label style="font-size:12px"><input type="checkbox" name="transform[' . esc_attr( $t['id'] ) . ']" value="' . esc_attr( $tr_slug ) . '"' . $checked . '> ' . esc_html( $tr_label ) . '</label>';
			}
			echo '</td>';

			echo '<td><span class="srom-sample" data-target="' . esc_attr( $t['id'] ) . '"></span></td>';
			echo '<td><span class="srom-note">' . esc_html( $t['note'] ) . '</span></td>';
			echo '</tr>';
		}
		echo '</tbody></table>';

		// Key + options.
		echo '<div class="srom-card">';
		echo '<h3>Matching & options</h3>';
		echo '<p class="srom-keyrow"><label><strong>Key field</strong> (identifies each row; re-importing the same file updates instead of duplicating):<br>';
		echo '<select name="key_target">';
		foreach ( $t_info['targets'] as $t ) {
			if ( ! SROM_Imp_Fields::key_eligible( $t ) ) {
				continue;
			}
			echo '<option value="' . esc_attr( $t['id'] ) . '"' . selected( $job['key_target'], $t['id'], false ) . '>' . esc_html( $t['group'] . ' → ' . $t['label'] ) . '</option>';
		}
		echo '</select></label></p>';

		$o = $job['options'];
		echo '<div class="srom-optlist">';
		echo '<label><input type="checkbox" name="opt_update_existing" value="1"' . checked( $o['update_existing'], 1, false ) . '> Update posts that already match the key (unchecked: skip them)</label>';
		echo '<label>Status for newly created posts: <select name="opt_new_status">';
		foreach ( array( 'draft' => 'Draft (recommended — review, then publish)', 'publish' => 'Published', 'pending' => 'Pending review', 'private' => 'Private' ) as $v => $l ) {
			echo '<option value="' . esc_attr( $v ) . '"' . selected( $o['new_status'], $v, false ) . '>' . esc_html( $l ) . '</option>';
		}
		echo '</select></label>';
		echo '<label>Empty cells: <select name="opt_empty_cells">';
		echo '<option value="keep"' . selected( $o['empty_cells'], 'keep', false ) . '>Leave the field as it is (recommended)</option>';
		echo '<option value="clear"' . selected( $o['empty_cells'], 'clear', false ) . '>Clear the field</option>';
		echo '</select></label>';
		echo '<label><input type="checkbox" name="opt_link_volumes" value="1"' . checked( $o['link_volumes'], 1, false ) . '> Create missing volumes (srom_volume) automatically from volume columns and link them</label>';
		echo '<label><input type="checkbox" name="opt_sideload" value="1"' . checked( $o['sideload'], 1, false ) . '> For file/image fields: download URLs that are not yet in the media library</label>';
		echo '<label><input type="checkbox" name="opt_create_terms" value="1"' . checked( $o['create_terms'], 1, false ) . '> For taxonomy fields: create terms that do not exist yet</label>';
		echo '</div>';
		echo '</div>';

		echo '<p><button type="submit" class="button button-primary">Save mapping & continue to preview →</button></p>';
		echo '</form>';
		echo '</div>';

		// Sample values + unmapped columns note, driven by a tiny script.
		$samples = array();
		foreach ( $header as $i => $name ) {
			$samples[ $i ] = isset( $sample[ $i ] ) ? SROM_Imp_Coerce::shorten( (string) $sample[ $i ], 90 ) : '';
		}
		?>
<script>
(function(){
	var samples = <?php echo wp_json_encode( $samples ); ?>;
	function refresh(sel){
		var span = sel.closest('tr').querySelector('.srom-sample');
		if(!span){return;}
		var v = sel.value;
		span.textContent = (v === '' || samples[v] === undefined || samples[v] === '') ? '' : samples[v];
	}
	document.querySelectorAll('.srom-col-select').forEach(function(sel){
		refresh(sel);
		sel.addEventListener('change', function(){ refresh(sel); });
	});
})();
</script>
		<?php
	}

	private static function render_run( array $job ) {
		$token   = $job['token'];
		$t_info  = SROM_Imp_Fields::get_targets( $job['post_type'] );
		$by_id   = array();
		foreach ( $t_info['targets'] as $t ) {
			$by_id[ $t['id'] ] = $t;
		}
		$key_label = isset( $by_id[ $job['key_target'] ] ) ? $by_id[ $job['key_target'] ]['label'] : '?';

		echo '<div class="srom-card">';
		echo '<h2>3. Preview, then import</h2>';
		echo '<p><strong>' . esc_html( $job['orig_name'] ) . '</strong> — ' . (int) $job['total_rows'] . ' rows → <strong>' . esc_html( $job['post_type'] ) . '</strong>, ';
		echo count( $job['mapping'] ) . ' fields mapped, key: <strong>' . esc_html( $key_label ) . '</strong>, new posts: <strong>' . esc_html( $job['options']['new_status'] ) . '</strong>. ';
		echo '<a href="' . esc_url( self::job_url( $token, array( 'step' => 'map' ) ) ) . '">← Edit mapping</a></p>';

		echo '<p>The preview reads every row and reports exactly what the import would do — <strong>nothing is written during the preview</strong>. The import button unlocks after a completed preview.</p>';

		echo '<div class="srom-actions">';
		echo '<button class="button button-primary" id="srom-preview-btn">Run preview (no changes)</button>';
		echo '<button class="button button-primary" id="srom-import-btn" disabled>Import now</button>';
		echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" style="display:inline">';
		wp_nonce_field( 'srom_imp_discard_' . $token );
		echo '<input type="hidden" name="action" value="srom_imp_discard"><input type="hidden" name="job" value="' . esc_attr( $token ) . '">';
		echo '<button type="submit" class="button">Discard this import session</button>';
		echo '</form>';
		echo '</div>';

		echo '<div class="srom-progress" id="srom-progress"><div class="srom-progress-bar" id="srom-progress-bar">0%</div></div>';
		echo '<div class="srom-chips" id="srom-chips" style="display:none"></div>';
		echo '<div id="srom-status" style="margin:8px 0;font-weight:600"></div>';
		echo '<table class="srom-log" id="srom-log" style="display:none"><thead><tr><th style="width:60px">Row</th><th style="width:120px">Action</th><th style="width:320px">Post</th><th>Notes</th></tr></thead><tbody></tbody></table>';
		echo '</div>';

		$cfg = array(
			'ajax'     => admin_url( 'admin-ajax.php' ),
			'nonce'    => wp_create_nonce( 'srom_imp_ajax' ),
			'token'    => $token,
			'total'    => (int) $job['total_rows'],
			'state'    => $job['state'],
			'nextRow'  => (int) $job['next_row'],
			'counts'   => $job['counts'],
			'log'      => array_slice( (array) $job['log'], 0, 800 ),
			'truncated'=> ! empty( $job['log_truncated'] ),
		);
		?>
<script>
(function(){
	var cfg = <?php echo wp_json_encode( $cfg ); ?>;
	var $ = function(id){ return document.getElementById(id); };
	var previewBtn = $('srom-preview-btn'), importBtn = $('srom-import-btn');
	var progress = $('srom-progress'), bar = $('srom-progress-bar');
	var chips = $('srom-chips'), status = $('srom-status');
	var logTable = $('srom-log'), logBody = logTable.querySelector('tbody');
	var logCount = 0, LOG_MAX = 2000;
	var running = false;

	function post(action, data){
		data = data || {};
		data.action = action;
		data._ajax_nonce = cfg.nonce;
		data.job = cfg.token;
		return fetch(cfg.ajax, {
			method:'POST', credentials:'same-origin',
			headers:{'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},
			body: new URLSearchParams(data).toString()
		}).then(function(r){
			if(!r.ok){ throw new Error('HTTP ' + r.status); }
			return r.json();
		}).then(function(j){
			if(!j || !j.success){ throw new Error((j && j.data && j.data.message) ? j.data.message : 'Unexpected server response'); }
			return j.data;
		});
	}

	function setProgress(next, total){
		progress.style.display = 'block';
		var pct = total ? Math.round(next * 100 / total) : 0;
		bar.style.width = pct + '%';
		bar.textContent = pct + '% (' + next + '/' + total + ')';
	}

	function chip(label, n, cls){
		return '<span class="srom-chip ' + cls + '"><b>' + n + '</b> ' + label + '</span>';
	}

	function setCounts(mode, c){
		chips.style.display = 'block';
		var created = (mode === 'import') ? 'created' : 'to create';
		var updated = (mode === 'import') ? 'updated' : 'to update';
		chips.innerHTML =
			chip(created, c.created, c.created ? 'ok' : '') +
			chip(updated, c.updated, c.updated ? 'ok' : '') +
			chip('skipped', c.skipped, '') +
			chip('rows with notes', c.warnings, c.warnings ? 'warn' : '') +
			chip('errors', c.errors, c.errors ? 'err' : '');
	}

	function addLog(entries){
		if(!entries || !entries.length){ return; }
		logTable.style.display = 'table';
		entries.forEach(function(e){
			if(logCount >= LOG_MAX){ return; }
			logCount++;
			var tr = document.createElement('tr');
			var td1 = document.createElement('td'); td1.textContent = e.row;
			var td2 = document.createElement('td'); td2.textContent = e.action.replace(/-/g,' '); td2.className = 'act-' + e.action;
			var td3 = document.createElement('td');
			if(e.edit){
				var a = document.createElement('a'); a.href = e.edit; a.target = '_blank'; a.textContent = (e.title || ('#' + e.post_id));
				td3.appendChild(a);
			} else {
				td3.textContent = e.title || '';
			}
			var td4 = document.createElement('td'); td4.className='srom-msgs'; td4.textContent = (e.msgs || []).join(' • ');
			tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3); tr.appendChild(td4);
			logBody.appendChild(tr);
		});
		if(logCount >= LOG_MAX){ status.textContent = 'Log display capped at ' + LOG_MAX + ' rows (processing continues; counts stay exact).'; }
	}

	function lock(on){
		running = on;
		previewBtn.disabled = on;
		importBtn.disabled = on || !canImport();
	}
	function canImport(){
		return cfg.state === 'previewed' || cfg.state === 'done' || cfg.state === 'import_running';
	}

	function clearLog(){
		logBody.innerHTML = '';
		logCount = 0;
		chips.style.display = 'none';
		logTable.style.display = 'none';
	}

	function runLoop(mode){
		lock(true);
		var failures = 0;
		function step(){
			post('srom_imp_batch', {mode: mode}).then(function(d){
				failures = 0;
				setProgress(d.next_row, d.total);
				setCounts(mode, d.counts);
				addLog(d.log);
				if(d.done){
					cfg.state = (mode === 'import') ? 'done' : 'previewed';
					lock(false);
					status.textContent = (mode === 'import')
						? 'Import finished. Newly created posts have the status you chose — review and publish them when ready. Re-running this import is safe: rows match by key and update instead of duplicating.'
						: 'Preview finished — nothing was written. Review the list above, then press “Import now”.';
					if(mode !== 'import'){ importBtn.disabled = false; }
					window.onbeforeunload = null;
					return;
				}
				step();
			}).catch(function(err){
				failures++;
				if(failures >= 4){
					lock(false);
					cfg.state = (mode === 'import') ? 'import_running' : 'preview_running';
					status.textContent = 'Stopped after a repeated connection/server error: ' + err.message + ' — nothing is lost. Press the button again to resume from row ' + (cfg.nextRow + 1) + '.';
					previewBtn.textContent = (mode === 'import') ? previewBtn.textContent : 'Resume preview';
					if(mode === 'import'){ importBtn.disabled = false; importBtn.textContent = 'Resume import'; }
					window.onbeforeunload = null;
					return;
				}
				status.textContent = 'Connection hiccup (' + err.message + ') — retrying…';
				setTimeout(step, 1500 * failures);
			});
		}
		step();
	}

	function start(mode){
		if(running){ return; }
		status.textContent = '';
		post('srom_imp_start', {mode: mode}).then(function(d){
			if(d.next_row === 0){ clearLog(); }
			setProgress(d.next_row, d.total);
			window.onbeforeunload = function(){ return 'Import in progress'; };
			runLoop(mode);
		}).catch(function(err){
			status.textContent = err.message;
		});
	}

	previewBtn.addEventListener('click', function(){ start('preview'); });
	importBtn.addEventListener('click', function(){
		if(cfg.state === 'import_running' || window.confirm('Write these changes to WordPress now? New posts will be created as ' + '<?php echo esc_js( $job['options']['new_status'] ); ?>' + '. Re-running later is safe (rows update by key).')){
			start('import');
		}
	});

	// Restore state on revisit.
	if(cfg.state === 'previewed' || cfg.state === 'done' || cfg.state === 'preview_running' || cfg.state === 'import_running'){
		setProgress(cfg.nextRow, cfg.total);
		setCounts(cfg.state === 'done' || cfg.state === 'import_running' ? 'import' : 'preview', cfg.counts);
		addLog(cfg.log);
		if(cfg.truncated){ status.textContent = 'The stored log was trimmed to the first entries; counts are exact.'; }
		if(cfg.state === 'previewed'){ importBtn.disabled = false; status.textContent = 'Preview finished — nothing was written. Press “Import now” to apply.'; }
		if(cfg.state === 'done'){ importBtn.disabled = false; status.textContent = 'This import already finished. Running it again is safe (rows update by key).'; }
		if(cfg.state === 'preview_running'){ previewBtn.textContent = 'Resume preview'; }
		if(cfg.state === 'import_running'){ importBtn.disabled = false; importBtn.textContent = 'Resume import'; status.textContent = 'An import was interrupted at row ' + cfg.nextRow + ' of ' + cfg.total + '. Press “Resume import” to continue safely.'; }
	}
})();
</script>
		<?php
	}

	private static function render_setup() {
		$available = SROM_Imp_Setup::available();
		$status    = SROM_Imp_Setup::status();
		$installed = $available ? SROM_Imp_Setup::is_installed() : false;
		?>
<div class="srom-card">
	<h2>ACF content model</h2>
	<p>This plugin creates the journal's post types, taxonomies and field groups as <strong>native ACF records</strong>. They appear — and are fully editable — under <em>Custom Fields → Post Types, Taxonomies and Field Groups</em>, exactly like items you build by hand in ACF. Editing or extending them there is safe; the importer reads whatever ACF reports.</p>
	<ul style="list-style:disc;padding-left:20px">
		<li><code>srom_article</code> (Artykuł) &amp; <code>srom_volume</code> (Tom) — post types with their field groups.</li>
		<li><code>dzial</code> (Dział) — hierarchical taxonomy on articles, for on-site filtering.</li>
		<li><code>slowa_kluczowe</code> (Słowa kluczowe) — flat tag taxonomy, filled from <code>keywords_pl</code> on import.</li>
		<li><code>autor</code> (Autor) — flat tag taxonomy, one term per author, filled from <code>authors_display</code>.</li>
		<li><code>rocznik</code> (Rocznik) — flat tag taxonomy, one term per year, filled from <code>year</code>.</li>
	</ul>
	<?php if ( ! $available ) : ?>
		<div class="notice notice-error inline"><p><strong>Advanced Custom Fields is not active.</strong> Activate ACF (free is enough), then return here.</p></div>
	<?php else : ?>
	<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" style="margin-top:8px">
		<?php wp_nonce_field( 'srom_imp_setup' ); ?>
		<input type="hidden" name="action" value="srom_imp_setup">
		<?php if ( ! $installed ) : ?>
			<button type="submit" name="srom_setup_action" value="install" class="button button-primary">Create / complete ACF definitions</button>
			<span class="description" style="margin-left:8px">Creates whatever is missing. Never overwrites items you've edited.</span>
		<?php else : ?>
			<button type="submit" name="srom_setup_action" value="install" class="button button-primary">Re-check / create missing</button>
			<button type="submit" name="srom_setup_action" value="reinstall" class="button" onclick="return confirm('Reset the plugin\'s post types, taxonomies and field groups to their defaults? Any changes you made to them in ACF will be overwritten. Your articles, volumes and their data are NOT affected.');">Reset to plugin defaults</button>
			<button type="submit" name="srom_setup_action" value="remove" class="button button-link-delete" onclick="return confirm('Remove the plugin\'s ACF post types, taxonomies and field groups? Your articles, volumes and their field data stay in the database (only the definitions are removed).');">Remove definitions</button>
		<?php endif; ?>
	</form>
	<?php endif; ?>
</div>
<div class="srom-card">
	<h2>Current status</h2>
	<table class="widefat striped" style="max-width:900px">
		<thead><tr><th>Definition</th><th>Type</th><th>In ACF (editable)?</th><th>Live in WordPress?</th><th></th></tr></thead>
		<tbody>
		<?php foreach ( $status as $s ) : ?>
			<tr>
				<td><strong><?php echo esc_html( $s['label'] ); ?></strong></td>
				<td><?php echo esc_html( str_replace( '_', ' ', $s['type'] ) ); ?></td>
				<td><?php echo $s['in_db'] ? '<span style="color:#00450c">yes — editable in ACF UI</span>' : '<span class="srom-badfile">no</span>'; ?></td>
				<td><?php echo $s['live'] ? 'yes' : '<span class="srom-badfile">no</span>'; ?></td>
				<td><?php if ( $s['edit_url'] ) { echo '<a href="' . esc_url( $s['edit_url'] ) . '">Edit in ACF →</a>'; } ?></td>
			</tr>
		<?php endforeach; ?>
		</tbody>
	</table>
	<p class="description">ACF plugin active: <?php echo SROM_Imp_Fields::acf_active() ? 'yes' : '<strong class="srom-badfile">no</strong>'; ?></p>
</div>
		<?php
	}

	private static function render_help() {
		?>
<div class="srom-card">
	<h2>Workflow for the journal</h2>
	<ol>
		<li><strong>Articles:</strong> upload the master spreadsheet, choose <code>srom_article</code>. The mapping is filled in automatically (including the special cases: <code>title_pl</code> → post title, <code>doi_suffix</code> → slug, <code>authors_struct</code> → <code>authors_raw</code> with one author per line, <code>pdf_url</code> → <code>pdf_file</code>, <code>seq</code> → menu order). Check it, run the preview, then import.</li>
		<li><strong>Taxonomies:</strong> <code>keywords_pl</code> also fills the <strong>Słowa kluczowe</strong> tag taxonomy (one term per comma-separated keyword), and <code>section_label</code> fills the hierarchical <strong>Dział</strong> taxonomy — both used for on-site filtering (author • year • dział • keyword). <code>keywords_en</code> stays a text field, normalised to semicolon-separated terms. Turn "create missing terms" on (default) so new terms are added as they appear.</li>
		<li><strong>Volumes (Tomy):</strong> you usually don't need a separate volume import — when article rows carry <code>issue_signature</code> / <code>volume</code> / <code>year</code> / <code>issue_theme</code>, the missing volume is created once and every article is linked to it. A separate volume spreadsheet (columns like <code>signature</code>, <code>volume</code>, <code>year</code>, <code>theme</code>, <code>pub_date</code>) also works, with <code>signature</code> as key.</li>
		<li><strong>Re-running is safe.</strong> Rows are matched by the key field (articles: <code>article_id</code>, volumes: <code>signature</code>). Re-importing the same or a corrected file updates the existing posts instead of duplicating them — that is also the recovery path if anything was interrupted.</li>
	</ol>
</div>
<div class="srom-card">
	<h2>What the importer tolerates</h2>
	<ul style="list-style:disc;padding-left:20px">
		<li>Extra columns (e.g. <code>journal_title</code>, <code>issn</code>, <code>landing_url</code>) — ignored unless you map them.</li>
		<li>Empty rows, repeated header rows, note/summary rows — skipped and reported, they never stop the run.</li>
		<li>Windows/Excel encodings (UTF-8 BOM, UTF-16, Windows-1250) and comma/semicolon/tab separators — detected automatically.</li>
		<li>Bad values in typed fields (e.g. an unfinished date like <code>2025-12-TODO</code>, a non-number in a number field, an unknown select choice) — that one field is skipped with a note; the rest of the row still imports. Fix the cell and re-import later to fill it.</li>
	</ul>
</div>
<div class="srom-card">
	<h2>Value formats per field type</h2>
	<table class="widefat striped" style="max-width:900px">
		<tbody>
		<tr><td>date</td><td><code>2025-12-31</code>, <code>31.12.2025</code>, <code>31/12/2025</code>, Excel date cells</td></tr>
		<tr><td>yes/no</td><td><code>1/0</code>, <code>tak/nie</code>, <code>yes/no</code>, <code>true/false</code></td></tr>
		<tr><td>select / radio</td><td>the stored value (<code>I</code>) or the visible label (<code>Część I – Romski Atlantyk</code>)</td></tr>
		<tr><td>taxonomy</td><td>term names or slugs; several separated by <code>;</code>, commas or new lines. Hierarchical: <code>Parent &gt; Child</code></td></tr>
		<tr><td>multiple values</td><td>separate with new lines or <code>;</code> (commas also work where titles can't contain them)</td></tr>
		<tr><td>post object / relationship</td><td>post ID, exact title, or slug — for volumes also the signature, e.g. <code>SROM·18·2025</code></td></tr>
		<tr><td>file / image</td><td>attachment ID, a file name that exists in the media library, or a URL (downloading is opt-in)</td></tr>
		<tr><td>number</td><td><code>11</code> or <code>11,5</code></td></tr>
		</tbody>
	</table>
</div>
		<?php
	}
}
