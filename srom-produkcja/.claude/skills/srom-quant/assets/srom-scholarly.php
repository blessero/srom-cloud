<?php
/**
 * Plugin Name: SROM Scholarly Infrastructure
 * Description: Full-DOI permalinks, Highwire citation_* meta tags, ScholarlyArticle JSON-LD, display shortcodes. Content model (CPTs, taxonomies, ACF groups) is owned by the SROM Importer plugin — this file registers NO post types.
 * Version: 2.3
 * Install: drop into wp-content/mu-plugins/ (create the dir if absent) — loads always, cannot be deactivated by accident.
 *
 * v2.3 changes (fixes the "grid shows nothing / shortcode renders nothing" class of bug):
 *  - ROOT CAUSE: every display shortcode and query filter gated on is_singular().
 *    Inside an Elementor Loop Grid, the editor preview, or an admin-ajax widget
 *    re-render, the global query is NOT the main query, so is_singular() is false
 *    and the fail-closed branch fired: [srom_cite] returned '', the "W tym tomie"
 *    rail set post__in=[0]. Replaced with srom_ctx_id(), which latches the real
 *    main-query object at `wp` and falls back to the set-up post.
 *  - Every elementor/query/* callback is wrapped in srom_safe_query_cb(): an
 *    exception now logs and leaves the query alone instead of white-screening
 *    the page ("There has been a critical error on this website").
 *  - get_terms() for the dzial resolver is cached per request (was once per grid).
 *  - New [srom_diag] admin-only diagnostic shortcode.
 *
 * v2.2 changes (adversarial audit pass, verified against the real ACF export + importer source):
 *  - PHP 7.4 compatibility (str_starts_with removed — it is PHP 8.0+).
 *  - [srom_cite]: page range and DOI segments are omitted cleanly when empty
 *    (was rendering a dangling "s. –." for unpaginated articles).
 *  - language normalised to an ISO code for citation_language / inLanguage
 *    ("polski" typed by an editor no longer leaks into machine metadata).
 *  - dzial resolver returns ALL matching terms (generic czesc-i AND legacy
 *    czesc-i-… can coexist during the rename without emptying the TOC).
 *  - New query filter srom_other_volumes for the "Inne roczniki" loop grids
 *    (they had no filter: listed every volume including the one being viewed).
 *  - [srom_volume_field] gains format="F Y" for pub_date (→ "grudzień 2025").
 *  - Legacy rewrite for the old /artykul/{slug}/ base → 301s to canonical after
 *    the CPT slug moves to /articles/ (locked decision).
 *  - Comment fix: pdf_file is a plain TEXT URL field (per ACF export), not a File field.
 *
 * v2.1 changes:
 *  - Author name now renders "Given Surname" everywhere (parse bug: only the given
 *    name was emitted in [srom_authors], [srom_cite], citation_author, JSON-LD, and
 *    the autor-archive link lookup silently failed because "Ann" != term "Ann Ostendorf").
 *  - Page range: no PHP shortcode for this — swap the templates' broken
 *    [acf field="pages_from"] tag for Elementor Pro's native post-custom-field
 *    dynamic tag on the same two fields. No shortcode needed; see HANDOVER.md.
 *  - [srom_flipbook]: serve the DearFlip reader dynamically (from pdf_file, or the
 *    flipbook_shortcode override) so no per-article DearFlip book has to be built by hand.
 *  - Loop query filters: scope the volume "Spis treści" and article "W tym tomie" grids
 *    to the current Tom (+ section) — they were listing every article of every volume.
 * Requires: SROM Importer plugin active (registers srom_article / srom_volume / dzial / slowa_kluczowe as ACF-native records).
 */

if (!defined('ABSPATH')) exit;

/** Crossref prefix — update ONCE after membership, then Settings -> Permalinks -> Save. */
define('SROM_DOI_PREFIX', '10.68100');

/* ---------------------------------------------------------------
 * 1. URL MACHINERY ONLY. CPTs are registered by the SROM Importer
 *    plugin (ACF-native, editable in Custom Fields UI). Registering
 *    them here too would double-register and silently fight over
 *    rewrite args — removed in v2.0.
 * --------------------------------------------------------------- */
/* ---------------------------------------------------------------
 * 0. FATAL CATCHER + KILL SWITCH — TEMPORARY (v2.3), remove once diagnosed.
 *
 * Why: try/catch cannot see a memory exhaustion or a stack overflow (they are
 * E_ERROR, not exceptions), and the host log we could get hold of is the
 * ModSecurity/access log, which never contains PHP errors. A shutdown handler
 * sees every fatal, whatever its kind, so we capture it ourselves into a file
 * we know the path of: wp-content/srom-fatal.log.
 *
 * Kill switch: append ?srom_off=1 to any URL to disable every SROM query
 * filter for that one request — so a broken grid can never lock you out of a
 * page while we debug.
 * --------------------------------------------------------------- */
define('SROM_FILTERS_OFF', isset($_GET['srom_off']));

register_shutdown_function(function () {
    $e = error_get_last();
    if (!$e) return;
    $fatal = [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR, E_USER_ERROR];
    if (!in_array($e['type'], $fatal, true)) return;
    $mem = function_exists('size_format') ? size_format(memory_get_peak_usage(true)) : memory_get_peak_usage(true);
    $log = sprintf(
        "[%s] FATAL: %s\n    in %s:%d\n    url: %s\n    peak memory: %s (limit %s)\n\n",
        date('c'), $e['message'], $e['file'], (int) $e['line'],
        isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : 'cli',
        $mem, ini_get('memory_limit')
    );
    if (defined('WP_CONTENT_DIR')) @file_put_contents(WP_CONTENT_DIR . '/srom-fatal.log', $log, FILE_APPEND);
    error_log('[SROM] ' . str_replace("\n", ' ', $log));
});

add_action('init', function () {
    // Full-DOI URLs: /articles/{prefix}/{suffix}/ resolves to the article whose slug == suffix.
    // Targets post_type+name (not the CPT query var) so it works regardless of how
    // the importer plugin configures query_var.
    add_rewrite_rule(
        'articles/10\.[0-9]+/([a-z0-9-]+)/?$',
        'index.php?post_type=srom_article&name=$matches[1]',
        'top'
    );
    // Legacy base: the CPT slug was /artykul/ before the /articles/ decision.
    // Route old URLs to the post so template_redirect can 301 them to canonical
    // (without this they would 404 the moment the CPT slug changes).
    add_rewrite_rule(
        'artykul/([a-z0-9-]+)/?$',
        'index.php?post_type=srom_article&name=$matches[1]',
        'top'
    );
}, 20); // after the importer's registrations
// After first activation: Settings -> Permalinks -> Save (flush rewrite rules).

/* Permalinks carry the full DOI (per-post `doi` meta, so a future prefix change
 * cannot orphan old articles). Fallback /articles/{slug}/ until DOI assigned. */
add_filter('post_type_link', function ($link, $post) {
    if ($post->post_type !== 'srom_article') return $link;
    $doi = get_post_meta($post->ID, 'doi', true);
    if ($doi && strpos($doi, 'XXXXX') === false && strpos($doi, '/') !== false) {
        return home_url(user_trailingslashit('articles/' . $doi));
    }
    return $link;
}, 10, 2);

/* 301 short form -> canonical full-DOI form (and any other variant). */
add_action('template_redirect', function () {
    if (!is_singular('srom_article') || is_preview()) return;
    $canon = get_permalink();
    $req   = home_url(strtok($_SERVER['REQUEST_URI'], '?'));
    if (untrailingslashit($req) !== untrailingslashit($canon)) {
        wp_safe_redirect($canon, 301);
        exit;
    }
});

/* ---------------------------------------------------------------
 * 2. HELPERS
 * --------------------------------------------------------------- */

/* CONTEXT RESOLVER — why this exists (v2.3, replaces bare is_singular() gates).
 *
 * Elementor renders widgets in contexts where the global query is NOT the main
 * one: inside a Loop Grid item, in the editor preview, and over admin-ajax when
 * a widget is re-rendered. In those contexts is_singular('srom_article') is
 * FALSE even though we are logically "on" an article. Gating on it made
 * [srom_cite]/[srom_flipbook] return '' and made the fail-closed query filters
 * blank their grids — the exact symptoms reported.
 *
 * So: latch the real main-query object once, at `wp` (after the main query is
 * parsed, before any template or widget renders), and resolve against that
 * first, falling back to whatever post is currently set up. */
$GLOBALS['SROM_CTX'] = ['id' => 0, 'type' => ''];
add_action('wp', function () {
    $o = get_queried_object();
    if ($o instanceof WP_Post) $GLOBALS['SROM_CTX'] = ['id' => (int) $o->ID, 'type' => $o->post_type];
}, 1);

/**
 * The post this widget is logically rendering for.
 * @param string $post_type Require this type ('' = any).
 * @return int Post ID, or 0 when we are genuinely off-context.
 */
function srom_ctx_id($post_type = '') {
    $ctx = isset($GLOBALS['SROM_CTX']) ? $GLOBALS['SROM_CTX'] : ['id' => 0, 'type' => ''];
    if ($ctx['id'] && ($post_type === '' || $ctx['type'] === $post_type)) return $ctx['id'];
    // Editor preview / ajax render / nested loop: trust the set-up post instead.
    $id = (int) get_the_ID();
    if ($id && ($post_type === '' || get_post_type($id) === $post_type)) return $id;
    return 0;
}

function srom_parse_authors($raw) {
    // one author per line: Given | Surname | Affiliation | ORCID-URL
    // (fields 2-4 optional). Matches ACF textarea `authors_raw`, which the importer
    // builds from authors_struct (Given|Surname|Affiliation|ORCID ;; ...).
    // `name` = the FULL display name ("Given Surname") — that is what every consumer
    // wants (Highwire citation_author, JSON-LD, [srom_cite], [srom_authors]) and what
    // the `autor` taxonomy terms are keyed on, so the archive link resolves.
    $out = [];
    foreach (preg_split('/\r\n|\r|\n/', (string)$raw) as $line) {
        $line = trim($line);
        if ($line === '') continue;
        $p = array_map('trim', explode('|', $line));
        $given   = $p[0] ?? '';
        $surname = $p[1] ?? '';
        $out[] = [
            'given'   => $given,
            'surname' => $surname,
            'name'    => trim($given . ' ' . $surname), // full display name
            'aff'     => $p[2] ?? '',
            'orcid'   => $p[3] ?? '',
        ];
    }
    return $out;
}

function srom_article_meta($post_id) {
    // article -> Tom relation: post_object field `volume` (returns the Tom's post ID).
    // NB the linked Tom post has its OWN `volume` field holding the volume NUMBER.
    $vol_id = get_field('volume', $post_id);
    $vol_id = is_object($vol_id) ? $vol_id->ID : $vol_id;
    $pdf = get_field('pdf_file', $post_id); // plain TEXT field holding the direct PDF URL
    $dzial = get_the_terms($post_id, 'dzial');
    $section = (!is_wp_error($dzial) && $dzial) ? $dzial[0]->name : '';
    // citation_language / inLanguage want an ISO code; editors sometimes type the
    // language name. Normalise the common cases, pass anything else through.
    $lang = strtolower(trim((string) get_field('language', $post_id))) ?: 'pl';
    $lang_map = ['polski' => 'pl', 'polish' => 'pl', 'angielski' => 'en', 'english' => 'en'];
    if (isset($lang_map[$lang])) $lang = $lang_map[$lang];
    return [
        'section'    => $section,
        'title_pl'   => get_the_title($post_id),
        'title_en'   => get_field('title_en', $post_id),
        'authors'    => srom_parse_authors(get_field('authors_raw', $post_id)),
        'abstract_pl'=> get_field('abstract_pl', $post_id),
        'abstract_en'=> get_field('abstract_en', $post_id),
        'kw_pl'      => get_field('keywords_pl', $post_id),
        'kw_en'      => get_field('keywords_en', $post_id),
        'doi'        => get_field('doi', $post_id),
        'fp'         => get_field('pages_from', $post_id),
        'lp'         => get_field('pages_to', $post_id),
        'pdf'        => is_array($pdf) ? ($pdf['url'] ?? '') : (string)$pdf,
        'lang'       => $lang,
        'license'    => get_field('license_url', $post_id),
        'volume'     => $vol_id ? get_field('volume', $vol_id) : '',
        'year'       => $vol_id ? get_field('year', $vol_id) : '',
        'pub_date'   => $vol_id ? get_field('pub_date', $vol_id) : '', // Y-m-d or Y/m/d
    ];
}

/* ---------------------------------------------------------------
 * 3. HIGHWIRE citation_* TAGS + JSON-LD (single article pages only)
 *    Priority 1: as early in <head> as possible.
 * --------------------------------------------------------------- */
add_action('wp_head', function () {
    if (!is_singular('srom_article')) return;
    $m = srom_article_meta(get_the_ID());
    $esc = fn($s) => esc_attr(trim((string)$s));
    $tag = function ($name, $content) use ($esc) {
        if (trim((string)$content) === '') return;
        echo '<meta name="' . $name . '" content="' . $esc($content) . '">' . "\n";
    };

    echo "\n<!-- SROM scholarly metadata -->\n";
    $tag('citation_journal_title', 'Studia Romologica');
    $tag('citation_issn', '1689-4758');
    $tag('citation_title', $m['title_pl']);
    foreach ($m['authors'] as $a) {
        $tag('citation_author', $a['name']);
        $tag('citation_author_institution', $a['aff']);
        if ($a['orcid']) $tag('citation_author_orcid', $a['orcid']);
    }
    // Scholar wants YYYY/MM/DD
    $pd = $m['pub_date'] ? str_replace('-', '/', $m['pub_date']) : $m['year'];
    $tag('citation_publication_date', $pd);
    $tag('citation_online_date', $pd);
    $tag('citation_volume', $m['volume']);
    $tag('citation_firstpage', $m['fp']);
    $tag('citation_lastpage', $m['lp']);
    $tag('citation_doi', $m['doi']);
    $tag('citation_language', $m['lang']);
    $tag('citation_pdf_url', $m['pdf']);        // MUST resolve directly to the PDF, no redirects
    $tag('citation_abstract_html_url', get_permalink());
    if ($m['kw_pl']) $tag('citation_keywords', $m['kw_pl'] . ($m['kw_en'] ? '; ' . $m['kw_en'] : ''));
    $tag('dc.identifier', 'doi:' . $m['doi']);

    // ScholarlyArticle JSON-LD
    $authors_ld = array_map(function ($a) {
        $p = ['@type' => 'Person', 'name' => $a['name']];
        if ($a['orcid']) $p['sameAs'] = $a['orcid'];
        if ($a['aff'])   $p['affiliation'] = ['@type' => 'Organization', 'name' => $a['aff']];
        return $p;
    }, $m['authors']);
    $ld = [
        '@context' => 'https://schema.org',
        '@type' => 'ScholarlyArticle',
        'headline' => $m['title_pl'],
        'name' => $m['title_pl'],
        'alternativeHeadline' => $m['title_en'],
        'author' => $authors_ld,
        'inLanguage' => $m['lang'],
        'articleSection' => $m['section'],
        'abstract' => $m['abstract_pl'],
        'identifier' => 'https://doi.org/' . $m['doi'],
        'sameAs' => 'https://doi.org/' . $m['doi'],
        'pageStart' => $m['fp'], 'pageEnd' => $m['lp'],
        'datePublished' => $m['pub_date'] ?: $m['year'],
        'license' => $m['license'],
        'url' => get_permalink(),
        'isPartOf' => [
            '@type' => 'PublicationVolume',
            'volumeNumber' => $m['volume'],
            'isPartOf' => ['@type' => 'Periodical', 'name' => 'Studia Romologica', 'issn' => '1689-4758'],
        ],
    ];
    echo '<script type="application/ld+json">' . wp_json_encode(array_filter($ld), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "</script>\n";
}, 1);

/* ---------------------------------------------------------------
 * 4. "JAK CYTOWAĆ" — computed, never stored (single source of truth).
 *    In Elementor: shortcode widget -> [srom_cite]
 *    House style: Imię Nazwisko, Tytuł kursywą, „Studia Romologica", Rok, t. X, s. A–B.
 * --------------------------------------------------------------- */
add_shortcode('srom_cite', function () {
    $id = srom_ctx_id('srom_article');
    if (!$id) return '';
    $m = srom_article_meta($id);
    $names = implode(', ', array_map(fn($a) => esc_html($a['name']), $m['authors']));
    // Assemble segments conditionally — an unpaginated / pre-linking article must
    // not render dangling "t. , s. –." fragments.
    $cite = $names . ', <em>' . esc_html($m['title_pl']) . '</em>, „Studia Romologica”';
    if ($m['year'] !== '' && $m['year'] !== null)     $cite .= ', ' . esc_html($m['year']);
    if ($m['volume'] !== '' && $m['volume'] !== null) $cite .= ', t. ' . esc_html($m['volume']);
    if ($m['fp'] !== '' && $m['fp'] !== null) {
        $cite .= ', s. ' . esc_html($m['fp']);
        if ($m['lp'] !== '' && $m['lp'] !== null) $cite .= '–' . esc_html($m['lp']);
    }
    $cite .= '.';
    if ($m['doi']) $cite .= sprintf(' DOI: <a href="https://doi.org/%1$s">https://doi.org/%1$s</a>', esc_attr($m['doi']));
    return '<p class="srom-cite">' . $cite . '</p>';
});

/* Shortcode for displaying the DOI as a full clickable URL (Crossref display guideline) */
add_shortcode('srom_doi', function () {
    $id = srom_ctx_id('srom_article');
    if (!$id) return '';
    $doi = get_field('doi', $id);
    return $doi ? sprintf('<a href="https://doi.org/%1$s">https://doi.org/%1$s</a>', esc_attr($doi)) : '';
});

/* ---------------------------------------------------------------
 * 5. DISPLAY SHORTCODES for Elementor templates.
 *    Why: ACF dynamic tags read fields of the CURRENT post only —
 *    they cannot traverse the article->Tom (volume) post_object relation,
 *    and they render nothing on plain Pages (field groups are
 *    located on srom_article/srom_volume). These shortcodes fill
 *    both gaps. Use an Elementor Shortcode/Text widget.
 * --------------------------------------------------------------- */

/* [srom_volume_field name="volume"] — Tom (volume) metadata ON THE ARTICLE template,
 * traversing the article->Tom relation. Allowed: volume, year, signature, theme, pub_date.
 * (Alias [srom_issue_field] kept for any pre-v2.2 template references.) */
$srom_volume_field = function ($atts) {
    $atts = shortcode_atts(['name' => '', 'format' => ''], $atts);
    $allowed = ['volume', 'year', 'signature', 'theme', 'pub_date'];
    if (!in_array($atts['name'], $allowed, true)) return '';
    // Article template first (traverse the relation), then the Tom template itself.
    $post_id = srom_ctx_id('srom_article');
    if ($post_id) {
        $vol_id = get_field('volume', $post_id);    // article->Tom relation field
        $vol_id = is_object($vol_id) ? $vol_id->ID : $vol_id;
    } else {
        $vol_id = srom_ctx_id('srom_volume');       // also usable on the Tom template
    }
    if (!$vol_id) return '';
    $val = (string) get_field($atts['name'], $vol_id);
    // pub_date is a date_picker returning Y-m-d; format="F Y" renders the
    // localised house style ("grudzień 2025"). Default: raw value, no surprises.
    if ($atts['name'] === 'pub_date' && $atts['format'] !== '' && $val !== '') {
        $ts = strtotime($val);
        if ($ts) $val = date_i18n($atts['format'], $ts);
    }
    return esc_html($val);
};
add_shortcode('srom_volume_field', $srom_volume_field);
add_shortcode('srom_issue_field', $srom_volume_field); // back-compat alias

/* [srom_flipbook] — on-screen PDF reader (DearFlip), served dynamically.
 * Order of preference:
 *   1. the article's `flipbook_shortcode` field, if set (e.g. [dflip id="1198"]);
 *   2. otherwise a URL embed built straight from `pdf_file` — same file as the
 *      download, so nothing is re-uploaded, there is no separate DearFlip "book" to
 *      maintain per article, and the reader is byte-identical to the PDF (the metadata
 *      worry disappears: DearFlip only *displays* the file, it never rewrites it).
 * The nested [dflip] is run through do_shortcode() here in PHP, so it works placed
 * literally in a Shortcode widget — no fragile acf-text dynamic tag needed.
 * DearFlip Lite honours source= for same-site PDFs (SROM's /uploads/ are same-origin,
 * so no CORS issue); the id= keeps share links working. NB: height= is a DearFlip PRO
 * attribute — in Lite the book sizes responsively to its container, so we don't emit a
 * dead attribute (only pass height="…" if you're on PRO). The 0-width collapse on the
 * current build is a LAYOUT issue, not this shortcode: set the Shortcode widget's
 * Align Self = Stretch (or the wrapping container's Align Items = Stretch). */
add_shortcode('srom_flipbook', function ($atts) {
    $id = srom_ctx_id('srom_article');
    if (!$id) return '';
    $atts = shortcode_atts(['height' => ''], $atts); // empty for Lite; set only on PRO
    $sc  = trim((string) get_field('flipbook_shortcode', $id));
    if ($sc === '') {
        $pdf = get_field('pdf_file', $id);
        $pdf = is_array($pdf) ? ($pdf['url'] ?? '') : (string) $pdf;
        if ($pdf === '') return '';
        $h  = $atts['height'] !== '' ? sprintf(' height="%s"', esc_attr($atts['height'])) : '';
        $sc = sprintf('[dflip source="%s" id="srom_df_%d"%s][/dflip]', esc_url($pdf), $id, $h);
    }
    return '<div class="srom-flipbook" style="width:100%;max-width:100%">' . do_shortcode($sc) . '</div>';
});

/* [srom_authors] — full author block from authors_raw: one .srom-author per
 * contributor; name links to the `autor` taxonomy archive when the term exists
 * (interlinking: click an author -> all their articles); ORCID link appended.
 * Attributes: links="0" to disable archive links, orcid="0" to hide ORCID. */
add_shortcode('srom_authors', function ($atts) {
    $atts = shortcode_atts(['links' => '1', 'orcid' => '1'], $atts);
    $authors = srom_parse_authors(get_field('authors_raw', srom_ctx_id('srom_article')));
    if (!$authors) return '';
    $out = '<div class="srom-authors">';
    foreach ($authors as $a) {
        $name_html = esc_html($a['name']);
        if ($atts['links'] === '1' && taxonomy_exists('autor')) {
            $term = get_term_by('name', $a['name'], 'autor');
            if ($term && !is_wp_error($term)) {
                $name_html = '<a href="' . esc_url(get_term_link($term)) . '">' . $name_html . '</a>';
            }
        }
        $out .= '<div class="srom-author"><span class="srom-author-name">' . $name_html . '</span>';
        if ($a['aff'])
            $out .= ' <span class="srom-author-aff">— ' . esc_html($a['aff']) . '</span>';
        if ($atts['orcid'] === '1' && strpos($a['orcid'], 'https://orcid.org/') === 0) // strpos: PHP 7.4-safe
            $out .= ' <a class="srom-author-orcid" href="' . esc_url($a['orcid']) . '" rel="noopener">ORCID</a>';
        $out .= '</div>';
    }
    return $out . '</div>';
});

/* ---------------------------------------------------------------
 * 6. LOOP QUERY FILTERS (Elementor Pro Loop Grids)
 *    A Loop Grid has no idea which post it sits on, so with no filter it
 *    lists EVERY srom_article of EVERY volume — the "Spis treści loads all
 *    posts regardless of section" and "W tym tomie shows everything" bugs.
 *    These filters supply what Elementor's query UI cannot: the article->Tom
 *    relation. They FAIL CLOSED (post__in=[0]) off-context — showing nothing
 *    beats dumping the whole archive at a reader.
 *
 *    Set these Query IDs on the grids (Content -> Query -> Query ID):
 *      Volume "Spis treści" — one grid per part, Query ID:
 *          srom_contents_part1 / _part2 / _part3 / _part4
 *      Article "W tym tomie" rail — Query ID: srom_other_articles
 *    (Articles relate to their Tom via the ACF post_object field `volume`,
 *    stored as the Tom's post ID in postmeta `volume`.)
 * --------------------------------------------------------------- */

// Which dzial section each TOC grid shows. The base slug matches a term whose
// slug is exactly it OR begins "{base}-…", so this works whether the terms are
// the generic "czesc-i" (recommended) or today's "czesc-i-romski-atlantyk".
$GLOBALS['SROM_TOC_SECTIONS'] = [
    'srom_contents_part1' => 'czesc-i',
    'srom_contents_part2' => 'czesc-ii',
    'srom_contents_part3' => 'czesc-iii',
    'srom_contents_part4' => 'czesc-iv',
];

function srom_resolve_dzial_terms($base) {
    // Returns ALL matching term ids: while renaming "czesc-i-romski-atlantyk" to the
    // generic "czesc-i", both may exist for a moment — matching only the first would
    // silently empty the TOC for articles still tagged with the other.
    static $cache = null; // one get_terms() per request, not one per grid
    if ($cache === null) {
        $cache = [];
        if (taxonomy_exists('dzial')) {
            $terms = get_terms(['taxonomy' => 'dzial', 'hide_empty' => false]);
            if (!is_wp_error($terms) && $terms) $cache = $terms;
        }
    }
    $ids = [];
    foreach ($cache as $t) {
        if ($t->slug === $base || strpos($t->slug, $base . '-') === 0) $ids[] = (int) $t->term_id;
    }
    return $ids;
}

/* Never let a query filter take the site down. An exception inside an
 * elementor/query/* callback bubbles up through WP_Query and white-screens the
 * whole page ("There has been a critical error"). Wrap every callback: on
 * failure log it and leave the query untouched. */
function srom_safe_query_cb(callable $fn) {
    return function ($query) use ($fn) {
        if (SROM_FILTERS_OFF) return;              // ?srom_off=1 escape hatch
        if (!$query instanceof WP_Query) {         // never assume Elementor's arg type
            error_log('[SROM] query filter got ' . (is_object($query) ? get_class($query) : gettype($query)) . ', expected WP_Query');
            return;
        }
        /* RE-ENTRANCY GUARD. Elementor fires elementor/query/{id} from inside
         * pre_get_posts. Any callback that then runs its own query re-enters
         * pre_get_posts -> Elementor -> this callback -> ... without bound, and
         * PHP dies with "Maximum call stack size reached" — not a catchable
         * exception, so try/catch below cannot save it. That is precisely how the
         * legacy mu-plugin srom-loops.php white-screened the volume pages
         * (get_posts() at srom-loops.php:54 inside its own query filter).
         * Nothing here queries today; this guard keeps it that way. */
        if (!empty($GLOBALS['SROM_IN_QUERY_FILTER'])) return;
        $GLOBALS['SROM_IN_QUERY_FILTER'] = true;
        try {
            $fn($query);
        } catch (\Throwable $e) {
            error_log('[SROM] query filter failed: ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
        } finally {
            $GLOBALS['SROM_IN_QUERY_FILTER'] = false;
        }
    };
}

// Scope a query to the articles of one Tom, ordered by menu_order (the `seq`).
function srom_scope_to_volume($query, $vol_id) {
    $query->set('post_type', 'srom_article');
    $query->set('meta_query', [['key' => 'volume', 'value' => (string) $vol_id, 'compare' => '=']]);
    $query->set('orderby', 'menu_order');
    $query->set('order', 'ASC');
    $query->set('posts_per_page', 50);
    $query->set('ignore_sticky_posts', true);
}

foreach ($GLOBALS['SROM_TOC_SECTIONS'] as $qid => $base_slug) {
    add_action("elementor/query/$qid", srom_safe_query_cb(function ($query) use ($base_slug) {
        $vol_id   = srom_ctx_id('srom_volume');
        $term_ids = $vol_id ? srom_resolve_dzial_terms($base_slug) : [];
        if (!$vol_id || !$term_ids) { $query->set('post__in', [0]); return; } // fail closed
        srom_scope_to_volume($query, $vol_id);
        $query->set('tax_query', [[
            'taxonomy' => 'dzial', 'field' => 'term_id', 'terms' => $term_ids,
        ]]);
    }));
}

// Article "W tym tomie" rail: sibling articles in the same Tom, current one excluded.
add_action('elementor/query/srom_other_articles', srom_safe_query_cb(function ($query) {
    $cur = srom_ctx_id('srom_article');
    if (!$cur) { $query->set('post__in', [0]); return; } // fail closed
    $vol_id = get_post_meta($cur, 'volume', true);
    if (!$vol_id) { $query->set('post__in', [0]); return; }
    srom_scope_to_volume($query, $vol_id);
    $query->set('post__not_in', [$cur]);
}));

// "Inne roczniki" sidebar (volume templates "Tom" + "Tomy >17"): other volumes,
// newest first by the `year` number field, current one excluded. Without a
// Query ID those grids list every volume INCLUDING the one being viewed.
// Set Query ID: srom_other_volumes on both grids.
add_action('elementor/query/srom_other_volumes', srom_safe_query_cb(function ($query) {
    $query->set('post_type', 'srom_volume');
    $query->set('meta_key', 'year');
    $query->set('orderby', 'meta_value_num');
    $query->set('order', 'DESC');
    $query->set('ignore_sticky_posts', true);
    $cur = srom_ctx_id('srom_volume');
    if ($cur) $query->set('post__not_in', [$cur]);
    // No fail-closed here: on any other context "all volumes, newest first"
    // is the correct, harmless result (it's a navigation list, not content).
}));

/* Volumes ARCHIVE grid (/tomy/) — every volume, newest first, 24 per page.
 * INHERITED from the legacy mu-plugin srom-loops.php v3.0, which owned this
 * Query ID and nothing else here replaced. Ordered by the numeric `volume`
 * meta DESC (not post date) so back-issues digitised out of order still sort
 * 18 -> 1. Kept byte-for-byte in behaviour so retiring srom-loops.php is a
 * no-op for this page.
 * NB: `meta_key` + meta_value_num ordering INNER JOINs postmeta, so a volume
 * with no `volume` value silently drops out of this grid — [srom_diag] counts
 * that for you; the fix is to fill the field, not to change the query. */
add_action('elementor/query/srom_archive', srom_safe_query_cb(function ($query) {
    $query->set('post_type', 'srom_volume');
    $query->set('meta_key', 'volume');
    $query->set('orderby', 'meta_value_num');
    $query->set('order', 'DESC');
    $query->set('posts_per_page', 24);
    $query->set('ignore_sticky_posts', true);
}));

/* ---------------------------------------------------------------
 * 7. [srom_diag] — TEMPORARY DIAGNOSTIC. Put it in a Shortcode widget
 *    (or any page) and view the page as an ADMIN; it prints nothing for
 *    everyone else. Answers, in one shot: is this file even loaded, what
 *    context do the shortcodes see, what does `volume` actually contain,
 *    and which dzial slugs exist. Delete the widget when done.
 * --------------------------------------------------------------- */
add_shortcode('srom_diag', function () {
    if (!current_user_can('manage_options')) return '';
    $ctx  = isset($GLOBALS['SROM_CTX']) ? $GLOBALS['SROM_CTX'] : ['id' => 0, 'type' => ''];
    $art  = srom_ctx_id('srom_article');
    $vol  = srom_ctx_id('srom_volume');
    $rows = [
        'mu-plugin version'      => '2.3',
        'PHP'                    => PHP_VERSION,
        'main query object'      => $ctx['id'] . ' (' . ($ctx['type'] ?: '—') . ')',
        'get_the_ID()'           => (string) get_the_ID(),
        'ctx article / volume'   => $art . ' / ' . $vol,
        'ACF get_field()'        => function_exists('get_field') ? 'available' : 'MISSING (ACF inactive?)',
        'post types registered'  => (post_type_exists('srom_article') ? 'srom_article ' : '!srom_article ')
                                  . (post_type_exists('srom_volume') ? 'srom_volume' : '!srom_volume'),
    ];
    if ($art) {
        $rows['article meta `volume`'] = var_export(get_post_meta($art, 'volume', true), true);
        $t = get_the_terms($art, 'dzial');
        $rows['article dzial terms'] = (!is_wp_error($t) && $t)
            ? implode(', ', wp_list_pluck($t, 'slug')) : '(none)';
    }
    if ($vol) {
        $n = get_posts(['post_type' => 'srom_article', 'posts_per_page' => -1, 'fields' => 'ids',
            'meta_query' => [['key' => 'volume', 'value' => (string) $vol, 'compare' => '=']]]);
        $rows['articles matching this Tom'] = count($n) . ' (meta volume = ' . $vol . ')';
    }
    // Volumes missing the meta used for ordering vanish from the archive /
    // "Inne roczniki" grids (meta_key ordering INNER JOINs postmeta).
    $all_vols = get_posts(['post_type' => 'srom_volume', 'posts_per_page' => -1, 'fields' => 'ids', 'post_status' => 'any']);
    $miss_vol = $miss_year = [];
    foreach ($all_vols as $v) {
        if (get_post_meta($v, 'volume', true) === '') $miss_vol[]  = $v;
        if (get_post_meta($v, 'year', true)   === '') $miss_year[] = $v;
    }
    $rows['volumes total'] = count($all_vols);
    $rows['volumes missing `volume`'] = $miss_vol  ? 'DROPS OUT of /tomy/: ' . implode(',', $miss_vol)   : 'none ✓';
    $rows['volumes missing `year`']   = $miss_year ? 'DROPS OUT of Inne roczniki: ' . implode(',', $miss_year) : 'none ✓';
    foreach (['srom_other_articles', 'srom_other_volumes', 'srom_archive'] as $qid) {
        $rows['hook ' . $qid] = has_action("elementor/query/$qid") ? 'registered' : 'NOT registered';
    }
    $terms = taxonomy_exists('dzial') ? get_terms(['taxonomy' => 'dzial', 'hide_empty' => false]) : [];
    $rows['dzial terms'] = (!is_wp_error($terms) && $terms)
        ? implode(' | ', array_map(fn($t) => $t->slug . ' (#' . $t->term_id . ', ' . $t->count . ')', $terms))
        : '(none / taxonomy missing)';
    foreach ($GLOBALS['SROM_TOC_SECTIONS'] as $qid => $base) {
        $rows['hook ' . $qid] = has_action("elementor/query/$qid") ? 'registered' : 'NOT registered';
        $ids = srom_resolve_dzial_terms($base);
        $rows['  ' . $base . ' -> terms'] = $ids ? implode(',', $ids) : '(no term matches!)';
        // SELF-TEST: run the exact query the filter builds, outside Elementor.
        // If the volume page fatals but this row prints, the query is innocent
        // and the fault is in Elementor's rendering of the grid.
        if ($vol && $ids) {
            $q = new WP_Query([
                'post_type' => 'srom_article', 'posts_per_page' => 50,
                'orderby' => 'menu_order', 'order' => 'ASC', 'fields' => 'ids',
                'meta_query' => [['key' => 'volume', 'value' => (string) $vol, 'compare' => '=']],
                'tax_query' => [['taxonomy' => 'dzial', 'field' => 'term_id', 'terms' => $ids]],
            ]);
            $rows['  ' . $base . ' -> self-test'] = $q->found_posts . ' posts: ' . implode(',', $q->posts);
        }
    }
    $out = '<table style="font:12px/1.5 monospace;border-collapse:collapse" border="1" cellpadding="4">';
    foreach ($rows as $k => $v) $out .= '<tr><th align="left">' . esc_html($k) . '</th><td>' . esc_html((string) $v) . '</td></tr>';
    return $out . '</table>';
});
