<?php
/**
 * Uninstall: remove the plugin's own options and temporary files.
 * Imported posts, issues and field data are of course left untouched.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

global $wpdb;
$like = $wpdb->esc_like( 'srom_imp_' ) . '%';
$names = $wpdb->get_col( $wpdb->prepare( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s", $like ) );
foreach ( (array) $names as $name ) {
	delete_option( $name );
}

$up = wp_upload_dir();
if ( empty( $up['error'] ) ) {
	$dir = trailingslashit( $up['basedir'] ) . 'srom-importer';
	if ( is_dir( $dir ) ) {
		foreach ( (array) glob( $dir . '/*' ) as $f ) {
			if ( is_file( $f ) ) {
				@unlink( $f );
			}
		}
		@unlink( $dir . '/.htaccess' );
		@rmdir( $dir );
	}
}
