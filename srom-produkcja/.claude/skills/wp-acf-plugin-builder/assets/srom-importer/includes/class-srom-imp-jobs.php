<?php
/**
 * Job storage: each import is a "job" persisted in a wp_options row,
 * with the uploaded file kept in a protected uploads subfolder.
 * Everything is plain arrays (no object serialization).
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Jobs {

	const OPT_PREFIX = 'srom_imp_job_';
	const MAX_AGE    = 172800; // 48 h, then jobs + files are garbage-collected.
	const MAX_LOG    = 3000;   // stored log entries per job (counts stay exact).

	/**
	 * Protected directory for uploaded spreadsheets.
	 *
	 * @return string|WP_Error absolute path
	 */
	public static function ensure_upload_dir() {
		$up = wp_upload_dir();
		if ( ! empty( $up['error'] ) ) {
			return new WP_Error( 'srom_imp_updir', 'Uploads directory is not writable: ' . $up['error'] );
		}
		$dir = trailingslashit( $up['basedir'] ) . 'srom-importer';
		if ( ! is_dir( $dir ) && ! wp_mkdir_p( $dir ) ) {
			return new WP_Error( 'srom_imp_updir', 'Could not create ' . $dir );
		}
		// Best-effort hardening; filenames are random either way.
		if ( ! file_exists( $dir . '/.htaccess' ) ) {
			@file_put_contents( $dir . '/.htaccess', "Require all denied\nDeny from all\n" );
		}
		if ( ! file_exists( $dir . '/index.html' ) ) {
			@file_put_contents( $dir . '/index.html', '' );
		}
		return $dir;
	}

	/**
	 * @return string 20-char lowercase alphanumeric token.
	 */
	public static function new_token() {
		$token = strtolower( wp_generate_password( 24, false, false ) );
		$token = preg_replace( '/[^a-z0-9]/', '', $token );
		if ( strlen( $token ) < 12 ) { // extremely defensive fallback
			$token = md5( uniqid( (string) wp_rand(), true ) );
		}
		return substr( $token, 0, 20 );
	}

	/**
	 * @param string $raw user-supplied token.
	 * @return string sanitized token or ''.
	 */
	public static function clean_token( $raw ) {
		$raw = is_string( $raw ) ? $raw : '';
		return preg_match( '/^[a-z0-9]{12,32}$/', $raw ) ? $raw : '';
	}

	public static function create( array $job ) {
		$token          = self::new_token();
		$job['token']   = $token;
		$job['created'] = time();
		$job['user_id'] = get_current_user_id();
		self::save( $token, $job );
		return $token;
	}

	/**
	 * @return array|null
	 */
	public static function get( $token ) {
		$token = self::clean_token( $token );
		if ( '' === $token ) {
			return null;
		}
		$job = get_option( self::OPT_PREFIX . $token, null );
		return is_array( $job ) ? $job : null;
	}

	public static function save( $token, array $job ) {
		// Cap the stored log so the option row cannot grow without bound.
		if ( isset( $job['log'] ) && is_array( $job['log'] ) && count( $job['log'] ) > self::MAX_LOG ) {
			$job['log']           = array_slice( $job['log'], 0, self::MAX_LOG );
			$job['log_truncated'] = 1;
		}
		update_option( self::OPT_PREFIX . $token, $job, false );
	}

	public static function delete( $token ) {
		$job = self::get( $token );
		if ( $job && ! empty( $job['file'] ) && self::is_our_file( $job['file'] ) && file_exists( $job['file'] ) ) {
			@unlink( $job['file'] );
		}
		delete_option( self::OPT_PREFIX . self::clean_token( $token ) );
	}

	/**
	 * Only ever unlink files inside our own protected folder.
	 */
	public static function is_our_file( $path ) {
		$dir = self::ensure_upload_dir();
		if ( is_wp_error( $dir ) ) {
			return false;
		}
		$real_dir  = realpath( $dir );
		$real_file = realpath( $path );
		return $real_dir && $real_file && 0 === strpos( $real_file, $real_dir . DIRECTORY_SEPARATOR );
	}

	/**
	 * Remove jobs (and their files) older than MAX_AGE. Called on page load.
	 */
	public static function cleanup() {
		global $wpdb;
		$like  = $wpdb->esc_like( self::OPT_PREFIX ) . '%';
		$names = $wpdb->get_col( $wpdb->prepare( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s", $like ) );
		foreach ( (array) $names as $name ) {
			$job = get_option( $name );
			if ( ! is_array( $job ) || empty( $job['created'] ) || ( time() - (int) $job['created'] ) > self::MAX_AGE ) {
				if ( is_array( $job ) && ! empty( $job['file'] ) && self::is_our_file( $job['file'] ) && file_exists( $job['file'] ) ) {
					@unlink( $job['file'] );
				}
				delete_option( $name );
			}
		}
		// Orphaned files (job option gone) older than MAX_AGE.
		$dir = self::ensure_upload_dir();
		if ( ! is_wp_error( $dir ) ) {
			foreach ( (array) glob( $dir . '/job-*.*' ) as $f ) {
				if ( is_file( $f ) && ( time() - (int) @filemtime( $f ) ) > self::MAX_AGE ) {
					@unlink( $f );
				}
			}
		}
	}
}
