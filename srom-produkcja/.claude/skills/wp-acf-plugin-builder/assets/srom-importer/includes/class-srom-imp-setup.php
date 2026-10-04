<?php
/**
 * ACF-native registration of the SROM content model.
 *
 * Instead of calling register_post_type() ourselves, we hand ACF real
 * definitions and let ACF own them — so the post types, taxonomies and
 * field groups appear in ACF's own admin screens (Custom Fields → Post
 * Types / Taxonomies / Field Groups) and are fully editable there, exactly
 * as if they had been created by hand in the UI.
 *
 * Mechanism (verified against ACF 6.8 source):
 *   acf_import_post_type() / acf_import_taxonomy() / acf_import_field_group()
 *   write real acf-post-type / acf-taxonomy / acf-field-group database
 *   records (post_name = our fixed key, post_content = serialized settings).
 *   ACF then registers the live WP post types/taxonomies on `acf/init`.
 *
 * Idempotency: ACF's import inserts a NEW record whenever the incoming
 * array has ID = 0 — it does NOT dedupe by key. So we guard by key
 * ourselves: if a record with our key already exists we skip it (never
 * clobber the user's edits), unless an explicit "reinstall/overwrite" is
 * requested, in which case we pass the existing ID so ACF updates in place.
 *
 * The content model:
 *   srom_article  (Artykuł)  + field group + taxonomies dzial, slowa_kluczowe, autor, rocznik
 *   srom_volume   (Tom)      + field group
 *   dzial            (Dział)          — hierarchical, filters articles
 *   slowa_kluczowe   (Słowa kluczowe) — flat tags, from keywords_pl
 *   autor            (Autor)          — flat tags, from authors_display
 *   rocznik          (Rocznik)        — flat tags, from year
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class SROM_Imp_Setup {

	// Fixed ACF keys — deterministic, so re-install is detectable by key.
	const PT_ARTICLE  = 'post_type_srom_article';
	const PT_VOLUME   = 'post_type_srom_volume';
	const TAX_DZIAL   = 'taxonomy_srom_dzial';
	const TAX_KEYWORD = 'taxonomy_srom_slowa_kluczowe';
	const TAX_AUTOR   = 'taxonomy_srom_autor';
	const TAX_ROCZNIK = 'taxonomy_srom_rocznik';
	const FG_ARTICLE  = 'group_srom_article';
	const FG_VOLUME   = 'group_srom_volume';

	public static function init() {
		// Run the one-time automatic install once ACF is fully ready.
		add_action( 'acf/init', array( __CLASS__, 'maybe_autoinstall' ), 20 );
		// After a plugin update, create definitions added by the new version.
		add_action( 'acf/init', array( __CLASS__, 'maybe_upgrade' ), 21 );
	}

	/**
	 * Whether ACF's native registration/import API is available.
	 */
	public static function available() {
		return function_exists( 'acf_import_post_type' )
			&& function_exists( 'acf_import_taxonomy' )
			&& function_exists( 'acf_import_field_group' )
			&& function_exists( 'acf_get_acf_post_types' )
			&& function_exists( 'acf_get_acf_taxonomies' );
	}

	/**
	 * Called on activation (bootstrap) — flags that a first-run install is due.
	 * Guarded by 'srom_imp_setup_done' so removing the definitions on purpose
	 * is respected and never silently reinstalled.
	 */
	public static function schedule_autoinstall() {
		if ( ! get_option( 'srom_imp_setup_done' ) ) {
			update_option( 'srom_imp_autoinstall_pending', '1', false );
		}
	}

	public static function maybe_autoinstall() {
		if ( '1' !== get_option( 'srom_imp_autoinstall_pending' ) ) {
			return;
		}
		if ( ! self::available() ) {
			return; // ACF not ready yet; try again next load.
		}
		self::install( false );
		update_option( 'srom_imp_setup_done', '1', false );
		update_option( 'srom_imp_setup_version', SROM_IMP_VERSION, false );
		delete_option( 'srom_imp_autoinstall_pending' );
		// Live post types were just added; refresh permalinks once.
		flush_rewrite_rules( false );
	}

	/**
	 * After the plugin is updated, add definitions that the new version
	 * introduced (e.g. a new taxonomy) without touching the ones already there.
	 *
	 * install( false ) only ever creates what is missing, so a user's own edits
	 * to existing records are never clobbered. If the user deliberately removed
	 * every definition, nothing is present to top up and we stay out of the way.
	 */
	public static function maybe_upgrade() {
		if ( ! self::available() ) {
			return;
		}
		if ( get_option( 'srom_imp_autoinstall_pending' ) ) {
			return; // First-run install handles it.
		}
		if ( ! get_option( 'srom_imp_setup_done' ) ) {
			return; // Never installed.
		}
		if ( SROM_IMP_VERSION === get_option( 'srom_imp_setup_version' ) ) {
			return; // Already up to date.
		}

		if ( self::any_installed() ) {
			$report = self::install( false );
			self::cleanup_legacy();
			if ( ! empty( $report['created'] ) ) {
				flush_rewrite_rules( false ); // New post types/taxonomies need permalinks.
			}
		}
		update_option( 'srom_imp_setup_version', SROM_IMP_VERSION, false );
	}

	/**
	 * Remove definitions that earlier versions of this plugin created and that
	 * later versions renamed away, so an in-place upgrade doesn't leave a stale
	 * record double-registering an old post type. Only ever touches our own
	 * legacy keys; imported posts and their data are untouched.
	 *
	 * v2.2.0: the "Numer" post type + field group (srom_issue) became "Tom"
	 * (srom_volume). Retire the old records if they are still present.
	 */
	public static function cleanup_legacy() {
		if ( ! self::available() ) {
			return;
		}
		$legacy = array(
			array( 'post_type', 'post_type_srom_issue' ),
			array( 'field_group', 'group_srom_issue' ),
		);
		foreach ( $legacy as $item ) {
			list( $type, $key ) = $item;
			$existing = self::find_existing( $type, $key );
			if ( ! $existing || empty( $existing['is_db'] ) ) {
				continue;
			}
			$fn = 'acf_delete_' . $type;
			if ( function_exists( $fn ) ) {
				$fn( $key );
			} elseif ( ! empty( $existing['ID'] ) ) {
				wp_delete_post( (int) $existing['ID'], true );
			}
		}
	}

	/**
	 * True when at least one of our definitions still exists as an ACF record.
	 */
	public static function any_installed() {
		foreach ( self::status() as $s ) {
			if ( $s['in_db'] ) {
				return true;
			}
		}
		return false;
	}

	/* --------------------------------------------------------- install/remove */

	/**
	 * Import all definitions as ACF database records.
	 *
	 * @param bool $overwrite When true, existing records are updated in place
	 *                        (their UI edits are replaced by plugin defaults).
	 *                        When false, existing records are left untouched.
	 * @return array report: created[], kept[], updated[], errors[]
	 */
	public static function install( $overwrite = false ) {
		$report = array( 'created' => array(), 'kept' => array(), 'updated' => array(), 'errors' => array() );
		if ( ! self::available() ) {
			$report['errors'][] = 'Advanced Custom Fields is not active, so the ACF-native definitions cannot be created. Activate ACF (the free version is enough) and try again.';
			return $report;
		}

		$defs = self::definitions();

		// Taxonomies first, then post types (which reference them), then field groups.
		foreach ( $defs['taxonomies'] as $def ) {
			self::import_one( 'taxonomy', $def, $overwrite, $report );
		}
		foreach ( $defs['post_types'] as $def ) {
			self::import_one( 'post_type', $def, $overwrite, $report );
		}
		foreach ( $defs['field_groups'] as $def ) {
			self::import_one( 'field_group', $def, $overwrite, $report );
		}

		return $report;
	}

	/**
	 * Import a single definition with key-based idempotency.
	 */
	private static function import_one( $type, array $def, $overwrite, array &$report ) {
		$key      = $def['key'];
		$existing = self::find_existing( $type, $key );

		try {
			if ( $existing && ! empty( $existing['is_db'] ) ) {
				if ( ! $overwrite ) {
					$report['kept'][] = $def['title'];
					return;
				}
				$def['ID'] = (int) $existing['ID']; // update in place
			}

			$fn = 'acf_import_' . $type;
			$result = $fn( $def );

			if ( is_array( $result ) && ! empty( $result['ID'] ) ) {
				if ( $existing && ! empty( $existing['is_db'] ) ) {
					$report['updated'][] = $def['title'];
				} else {
					$report['created'][] = $def['title'];
				}
			} else {
				$report['errors'][] = $def['title'] . ' could not be created (ACF returned no record).';
			}
		} catch ( Throwable $e ) {
			$report['errors'][] = $def['title'] . ': ' . $e->getMessage();
		}
	}

	/**
	 * Look up an existing ACF record by key.
	 *
	 * @return array|null ['ID'=>int, 'is_db'=>bool] or null when absent.
	 */
	private static function find_existing( $type, $key ) {
		if ( 'post_type' === $type ) {
			foreach ( (array) acf_get_acf_post_types() as $p ) {
				if ( isset( $p['key'] ) && $p['key'] === $key ) {
					return array( 'ID' => (int) ( $p['ID'] ?? 0 ), 'is_db' => empty( $p['local'] ) && ! empty( $p['ID'] ) );
				}
			}
		} elseif ( 'taxonomy' === $type ) {
			foreach ( (array) acf_get_acf_taxonomies() as $t ) {
				if ( isset( $t['key'] ) && $t['key'] === $key ) {
					return array( 'ID' => (int) ( $t['ID'] ?? 0 ), 'is_db' => empty( $t['local'] ) && ! empty( $t['ID'] ) );
				}
			}
		} else { // field_group
			$fg = function_exists( 'acf_get_field_group' ) ? acf_get_field_group( $key ) : false;
			if ( $fg ) {
				return array( 'ID' => (int) ( $fg['ID'] ?? 0 ), 'is_db' => empty( $fg['local'] ) && ! empty( $fg['ID'] ) );
			}
		}
		return null;
	}

	/**
	 * Delete the plugin's own ACF definitions (moves the records to trash).
	 * Imported articles/volumes and their data are NOT touched.
	 */
	public static function remove() {
		$report = array( 'removed' => array(), 'errors' => array() );
		if ( ! self::available() ) {
			$report['errors'][] = 'ACF is not active.';
			return $report;
		}

		$targets = array(
			array( 'field_group', self::FG_ARTICLE, 'Field group: Artykuł' ),
			array( 'field_group', self::FG_VOLUME, 'Field group: Tom' ),
			array( 'post_type', self::PT_ARTICLE, 'Post type: Artykuł' ),
			array( 'post_type', self::PT_VOLUME, 'Post type: Tom' ),
			array( 'taxonomy', self::TAX_DZIAL, 'Taxonomy: Dział' ),
			array( 'taxonomy', self::TAX_KEYWORD, 'Taxonomy: Słowa kluczowe' ),
			array( 'taxonomy', self::TAX_AUTOR, 'Taxonomy: Autor' ),
			array( 'taxonomy', self::TAX_ROCZNIK, 'Taxonomy: Rocznik' ),
		);
		foreach ( $targets as $t ) {
			list( $type, $key, $label ) = $t;
			$existing = self::find_existing( $type, $key );
			if ( ! $existing || empty( $existing['is_db'] ) ) {
				continue;
			}
			$fn = 'acf_delete_' . $type;
			if ( function_exists( $fn ) && $fn( $key ) ) {
				$report['removed'][] = $label;
			} elseif ( ! empty( $existing['ID'] ) && wp_delete_post( (int) $existing['ID'], true ) ) {
				$report['removed'][] = $label;
			} else {
				$report['errors'][] = 'Could not remove ' . $label . '.';
			}
		}
		flush_rewrite_rules( false );
		return $report;
	}

	/* ---------------------------------------------------------------- status */

	/**
	 * Per-item status for the Setup tab.
	 *
	 * @return array
	 */
	public static function status() {
		$items = array(
			array( 'post_type', self::PT_ARTICLE, 'srom_article', 'Artykuł (post type)' ),
			array( 'post_type', self::PT_VOLUME, 'srom_volume', 'Tom (post type)' ),
			array( 'taxonomy', self::TAX_DZIAL, 'dzial', 'Dział (taxonomy)' ),
			array( 'taxonomy', self::TAX_KEYWORD, 'slowa_kluczowe', 'Słowa kluczowe (taxonomy)' ),
			array( 'taxonomy', self::TAX_AUTOR, 'autor', 'Autor (taxonomy)' ),
			array( 'taxonomy', self::TAX_ROCZNIK, 'rocznik', 'Rocznik (taxonomy)' ),
			array( 'field_group', self::FG_ARTICLE, '', 'Artykuł (field group)' ),
			array( 'field_group', self::FG_VOLUME, '', 'Tom (field group)' ),
		);
		$out = array();
		foreach ( $items as $it ) {
			list( $type, $key, $object, $label ) = $it;
			$existing = self::available() ? self::find_existing( $type, $key ) : null;
			$live     = false;
			if ( 'post_type' === $type ) {
				$live = post_type_exists( $object );
			} elseif ( 'taxonomy' === $type ) {
				$live = taxonomy_exists( $object );
			} elseif ( 'field_group' === $type ) {
				$live = (bool) $existing;
			}
			$out[] = array(
				'label'    => $label,
				'type'     => $type,
				'in_db'    => (bool) ( $existing && ! empty( $existing['is_db'] ) ),
				'editable' => (bool) ( $existing && ! empty( $existing['is_db'] ) ),
				'live'     => $live,
				'edit_url' => ( $existing && ! empty( $existing['ID'] ) ) ? admin_url( 'post.php?post=' . (int) $existing['ID'] . '&action=edit' ) : '',
			);
		}
		return $out;
	}

	public static function is_installed() {
		foreach ( self::status() as $s ) {
			if ( ! $s['in_db'] ) {
				return false;
			}
		}
		return true;
	}

	/* ----------------------------------------------------------- definitions */

	/**
	 * All ACF definitions as plain arrays ready for acf_import_*().
	 */
	public static function definitions() {
		return array(
			'taxonomies'   => array( self::tax_dzial(), self::tax_keyword(), self::tax_autor(), self::tax_rocznik() ),
			'post_types'   => array( self::pt_article(), self::pt_volume() ),
			'field_groups' => array( self::fg_article(), self::fg_volume() ),
		);
	}

	private static function pt_article() {
		return array(
			'key'          => self::PT_ARTICLE,
			'title'        => 'Artykuł',
			'active'       => true,
			'post_type'    => 'srom_article',
			'labels'       => array(
				'name'          => 'Artykuły',
				'singular_name' => 'Artykuł',
				'menu_name'     => 'Artykuły',
				'all_items'     => 'Wszystkie artykuły',
				'add_new_item'  => 'Dodaj artykuł',
				'edit_item'     => 'Edytuj artykuł',
				'view_item'     => 'Zobacz artykuł',
				'search_items'  => 'Szukaj artykułów',
			),
			'public'       => true,
			'hierarchical' => false,
			'show_in_rest' => true, // Gutenberg + REST + many Elementor dynamic features.
			'supports'     => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'revisions', 'excerpt' ),
			'taxonomies'   => array( 'dzial', 'slowa_kluczowe', 'autor', 'rocznik' ),
			'menu_icon'    => 'dashicons-media-document',
			'menu_position'=> 26,
			'has_archive'  => true,
			'has_archive_slug' => 'artykuly',
			// 'articles' (English) — locked decision: the DOI landing URLs are
			// /articles/{full-doi}/, and the plain fallback permalink must share
			// that base. The srom-scholarly mu-plugin still routes the legacy
			// /artykul/{slug}/ form and 301s it to canonical.
			'rewrite'      => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'articles', 'with_front' => false ),
		);
	}

	private static function pt_volume() {
		return array(
			'key'          => self::PT_VOLUME,
			'title'        => 'Tom',
			'active'       => true,
			'post_type'    => 'srom_volume',
			'labels'       => array(
				'name'          => 'Tomy',
				'singular_name' => 'Tom',
				'menu_name'     => 'Tomy',
				'all_items'     => 'Wszystkie tomy',
				'add_new_item'  => 'Dodaj tom',
				'edit_item'     => 'Edytuj tom',
				'view_item'     => 'Zobacz tom',
				'search_items'  => 'Szukaj tomów',
			),
			'public'       => true,
			'hierarchical' => false,
			'show_in_rest' => true,
			'supports'     => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'revisions' ),
			'taxonomies'   => array(),
			'menu_icon'    => 'dashicons-book',
			'menu_position'=> 27,
			'has_archive'  => true,
			'has_archive_slug' => 'tomy',
			'rewrite'      => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'tom', 'with_front' => false ),
		);
	}

	private static function tax_dzial() {
		return array(
			'key'          => self::TAX_DZIAL,
			'title'        => 'Dział',
			'active'       => true,
			'taxonomy'     => 'dzial',
			'object_type'  => array( 'srom_article' ),
			'labels'       => array(
				'name'          => 'Działy',
				'singular_name' => 'Dział',
				'menu_name'     => 'Działy',
				'all_items'     => 'Wszystkie działy',
				'edit_item'     => 'Edytuj dział',
				'add_new_item'  => 'Dodaj dział',
				'search_items'  => 'Szukaj działów',
			),
			'hierarchical'      => true, // like categories — the point of using a taxonomy, not a select.
			'public'            => true,
			'show_in_rest'      => true,
			'show_admin_column' => true,
			'show_in_quick_edit'=> true,
			'rewrite'           => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'dzial', 'with_front' => false ),
		);
	}

	private static function tax_keyword() {
		return array(
			'key'          => self::TAX_KEYWORD,
			'title'        => 'Słowa kluczowe',
			'active'       => true,
			'taxonomy'     => 'slowa_kluczowe',
			'object_type'  => array( 'srom_article' ),
			'labels'       => array(
				'name'          => 'Słowa kluczowe',
				'singular_name' => 'Słowo kluczowe',
				'menu_name'     => 'Słowa kluczowe',
				'all_items'     => 'Wszystkie słowa kluczowe',
				'edit_item'     => 'Edytuj słowo kluczowe',
				'add_new_item'  => 'Dodaj słowo kluczowe',
				'search_items'  => 'Szukaj słów kluczowych',
			),
			'hierarchical'      => false, // flat tags.
			'public'            => true,
			'show_in_rest'      => true,
			'show_admin_column' => true,
			'show_tagcloud'     => true,
			'rewrite'           => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'slowa-kluczowe', 'with_front' => false ),
		);
	}

	/**
	 * Autor — flat tags, one term per author, filled from authors_display.
	 * Gives every author a browsable archive at /autor/<slug>/.
	 */
	private static function tax_autor() {
		return array(
			'key'          => self::TAX_AUTOR,
			'title'        => 'Autor',
			'active'       => true,
			'taxonomy'     => 'autor',
			'object_type'  => array( 'srom_article' ),
			'labels'       => array(
				'name'          => 'Autorzy',
				'singular_name' => 'Autor',
				'menu_name'     => 'Autorzy',
				'all_items'     => 'Wszyscy autorzy',
				'edit_item'     => 'Edytuj autora',
				'add_new_item'  => 'Dodaj autora',
				'search_items'  => 'Szukaj autorów',
			),
			'hierarchical'      => false, // flat tags.
			'public'            => true,
			'show_in_rest'      => true,
			'show_admin_column' => true,
			'rewrite'           => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'autor', 'with_front' => false ),
		);
	}

	/**
	 * Rocznik — flat tags, one term per publication year, filled from `year`.
	 */
	private static function tax_rocznik() {
		return array(
			'key'          => self::TAX_ROCZNIK,
			'title'        => 'Rocznik',
			'active'       => true,
			'taxonomy'     => 'rocznik',
			'object_type'  => array( 'srom_article' ),
			'labels'       => array(
				'name'          => 'Roczniki',
				'singular_name' => 'Rocznik',
				'menu_name'     => 'Roczniki',
				'all_items'     => 'Wszystkie roczniki',
				'edit_item'     => 'Edytuj rocznik',
				'add_new_item'  => 'Dodaj rocznik',
				'search_items'  => 'Szukaj roczników',
			),
			'hierarchical'      => false, // flat tags.
			'public'            => true,
			'show_in_rest'      => true,
			'show_admin_column' => true,
			'rewrite'           => array( 'permalink_rewrite' => 'custom_permalink', 'slug' => 'rocznik', 'with_front' => false ),
		);
	}

	private static function text( $key, $name, $label, array $extra = array() ) {
		return array_merge(
			array( 'key' => $key, 'name' => $name, 'label' => $label, 'type' => 'text' ),
			$extra
		);
	}

	private static function fg_article() {
		return array(
			'key'      => self::FG_ARTICLE,
			'title'    => 'Artykuł',
			'active'   => true,
			'location' => array(
				array(
					array( 'param' => 'post_type', 'operator' => '==', 'value' => 'srom_article' ),
				),
			),
			'menu_order'  => 0,
			'position'    => 'normal',
			'style'       => 'default',
			'label_placement' => 'top',
			'fields'   => array(
				self::text( 'field_srom_art_article_id', 'article_id', 'article_id', array( 'instructions' => 'Import key, e.g. SROM-18-2025-001.', 'required' => 1 ) ),
				self::text( 'field_srom_art_doi', 'doi', 'doi', array( 'instructions' => 'e.g. 10.xxxxx/srom-18-2025-001' ) ),
				// No doi_suffix field: the suffix IS the post slug (the CSV column still
				// maps to post_name), and the full DOI lives in `doi`.
				self::text( 'field_srom_art_title_en', 'title_en', 'title_en' ),
				array( 'key' => 'field_srom_art_authors_raw', 'name' => 'authors_raw', 'label' => 'authors_raw', 'type' => 'textarea', 'instructions' => 'One author per line: Given names | Surname | Affiliation | ORCID-URL', 'new_lines' => '' ),
				self::text( 'field_srom_art_authors_display', 'authors_display', 'authors_display', array( 'instructions' => 'Authors exactly as printed.' ) ),
				array( 'key' => 'field_srom_art_abstract_pl', 'name' => 'abstract_pl', 'label' => 'abstract_pl', 'type' => 'textarea', 'new_lines' => '' ),
				array( 'key' => 'field_srom_art_abstract_en', 'name' => 'abstract_en', 'label' => 'abstract_en', 'type' => 'textarea', 'new_lines' => '' ),
				self::text( 'field_srom_art_keywords_pl', 'keywords_pl', 'keywords_pl', array( 'instructions' => 'Comma-separated. Also feeds the "Słowa kluczowe" taxonomy on import.' ) ),
				self::text( 'field_srom_art_keywords_en', 'keywords_en', 'keywords_en', array( 'instructions' => 'Semicolon-separated discrete terms (feeds citation metadata; ready for a future EN taxonomy).' ) ),
				array( 'key' => 'field_srom_art_bio_note', 'name' => 'bio_note', 'label' => 'bio_note', 'type' => 'textarea', 'new_lines' => '' ),
				array( 'key' => 'field_srom_art_pages_from', 'name' => 'pages_from', 'label' => 'pages_from', 'type' => 'number' ),
				array( 'key' => 'field_srom_art_pages_to', 'name' => 'pages_to', 'label' => 'pages_to', 'type' => 'number' ),
				self::text( 'field_srom_art_language', 'language', 'language', array( 'default_value' => 'pl' ) ),
				self::text( 'field_srom_art_license_url', 'license_url', 'license_url', array( 'instructions' => 'Full CC URL.' ) ),
				self::text( 'field_srom_art_pdf_file', 'pdf_file', 'pdf_file', array( 'instructions' => 'Direct PDF URL (citation_pdf_url).' ) ),
				self::text( 'field_srom_art_is_translation', 'is_translation', 'is_translation' ),
				self::text( 'field_srom_art_original_title', 'original_title', 'original_title' ),
				self::text( 'field_srom_art_original_source', 'original_source', 'original_source' ),
				self::text( 'field_srom_art_original_doi', 'original_doi', 'original_doi' ),
				self::text( 'field_srom_art_flipbook_shortcode', 'flipbook_shortcode', 'flipbook_shortcode', array( 'instructions' => 'Optional override for the on-screen reader. Leave empty: [srom_flipbook] builds the DearFlip reader from pdf_file automatically. Fill only to force a specific [dflip …] shortcode for this article.' ) ),
				array( 'key' => 'field_srom_art_volume', 'name' => 'volume', 'label' => 'volume', 'instructions' => 'The Tom (volume) this article belongs to; linked by signature on import.', 'type' => 'post_object', 'post_type' => array( 'srom_volume' ), 'return_format' => 'id', 'allow_null' => 1, 'multiple' => 0, 'ui' => 1 ),
			),
		);
	}

	private static function fg_volume() {
		return array(
			'key'      => self::FG_VOLUME,
			'title'    => 'Tom',
			'active'   => true,
			'location' => array(
				array(
					array( 'param' => 'post_type', 'operator' => '==', 'value' => 'srom_volume' ),
				),
			),
			'menu_order'  => 0,
			'position'    => 'normal',
			'style'       => 'default',
			'label_placement' => 'top',
			'fields'   => array(
				array( 'key' => 'field_srom_iss_volume', 'name' => 'volume', 'label' => 'volume', 'type' => 'number' ),
				array( 'key' => 'field_srom_iss_year', 'name' => 'year', 'label' => 'year', 'type' => 'number' ),
				self::text( 'field_srom_iss_signature', 'signature', 'signature', array( 'instructions' => 'e.g. SROM·18·2025 (import key).' ) ),
				self::text( 'field_srom_iss_theme', 'theme', 'theme' ),
				array( 'key' => 'field_srom_iss_pub_date', 'name' => 'pub_date', 'label' => 'pub_date', 'type' => 'date_picker', 'display_format' => 'd.m.Y', 'return_format' => 'Y-m-d', 'first_day' => 1 ),
				array( 'key' => 'field_srom_iss_full_pdf', 'name' => 'full_pdf', 'label' => 'full_pdf', 'type' => 'file', 'return_format' => 'url', 'library' => 'all' ),
				array( 'key' => 'field_srom_iss_description', 'name' => 'description', 'label' => 'description', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 1 ),
			),
		);
	}
}
