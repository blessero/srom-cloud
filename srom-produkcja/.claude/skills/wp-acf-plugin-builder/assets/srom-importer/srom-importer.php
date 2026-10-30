<?php
/**
 * Plugin Name:       SROM Importer
 * Description:       Reliable spreadsheet importer (CSV / TSV / XLSX) for ACF-powered custom post types. Registers the Studia Romologica post types, taxonomies and field groups as native, editable ACF records; works with any ACF field group. Dry-run preview, upsert by key, taxonomy mapping, batched processing.
 * Version:           2.3.2
 * Author:            Studia Romologica
 * Requires PHP:      7.4
 * Requires at least: 5.8
 * Requires Plugins:  advanced-custom-fields
 * Text Domain:       srom-importer
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'SROM_IMP_VERSION', '2.3.2' );
/*
 * 2.3.2 (2026-10-30, C31 [general]):
 *  - Core preset post_date <- pub_date_online: re-importing drafts no longer resets their post date to the
 *    import time. Rows without a valid date skip the field (post keeps its date).
 *
 * 2.3.1 (2026-10-21, review 21.10.2026):
 *  - A volume's pub_date (the print date: citation_publication_date, „grudzień 2025”) comes from
 *    pub_date_print, no longer from pub_date_online: an auto-created Tom 19 would have dated its
 *    articles by the day they went online. A year-only print date (back volumes) is skipped as not
 *    a date, so the mu-plugin falls back to the year.
 *  - Defaults for fresh installs: article archive /articles/, volume slug and archive /volumes/
 *    (on the live site the post types are DB-native ACF records, edited in the ACF UI; mu-plugin
 *    v2.6 301s the old bases).
 *
 * 2.3.0 (2026-07-23):
 *  - Article CPT default rewrite slug: artykul -> articles (locked decision; DOI
 *    landing URLs are /articles/{full-doi}/). NB: on an install where the post
 *    type already exists as an ACF record, this default does NOT apply — change
 *    it once in ACF UI -> Post Types -> Artykul -> URL slug, then save Permalinks.
 *  - Auto-created volumes are titled "Tom: {volume}·{year}" (falls back to the
 *    signature when the volume/year columns are missing).
 *  - Article field group gains flipbook_shortcode (optional per-article override
 *    for the [srom_flipbook] reader). Existing installs: the field already exists
 *    (added manually in ACF UI); create-missing-only install will not duplicate it.
 */
define( 'SROM_IMP_DIR', plugin_dir_path( __FILE__ ) );
define( 'SROM_IMP_FILE', __FILE__ );

// Hard limits that keep the importer predictable.
define( 'SROM_IMP_MAX_FILE_BYTES', 25 * 1024 * 1024 ); // 25 MB upload
define( 'SROM_IMP_MAX_ROWS', 20000 );
define( 'SROM_IMP_MAX_COLS', 200 );
define( 'SROM_IMP_BATCH_SIZE', 10 );

require_once SROM_IMP_DIR . 'includes/class-srom-imp-jobs.php';
require_once SROM_IMP_DIR . 'includes/class-srom-imp-spreadsheet.php';
require_once SROM_IMP_DIR . 'includes/class-srom-imp-fields.php';
require_once SROM_IMP_DIR . 'includes/class-srom-imp-coerce.php';
require_once SROM_IMP_DIR . 'includes/class-srom-imp-runner.php';
require_once SROM_IMP_DIR . 'includes/class-srom-imp-setup.php';

if ( is_admin() ) {
	require_once SROM_IMP_DIR . 'includes/class-srom-imp-admin.php';
	SROM_Imp_Admin::init();
}

SROM_Imp_Setup::init();

register_activation_hook( __FILE__, 'srom_imp_activate' );

/**
 * On activation, schedule a one-time creation of the ACF-native content
 * model (post types, taxonomies and field groups as editable ACF records).
 * The actual import runs on the next `acf/init` once ACF is fully loaded
 * (see SROM_Imp_Setup::maybe_autoinstall). Guarded so that deliberately
 * removing the definitions later is respected and not silently reinstalled.
 */
function srom_imp_activate() {
	// Clean up the option used by the pre-ACF-native versions of this plugin.
	delete_option( 'srom_imp_register' );
	SROM_Imp_Setup::schedule_autoinstall();
	SROM_Imp_Jobs::ensure_upload_dir();
}
