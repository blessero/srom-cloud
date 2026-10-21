<?php
// WordPress stubs that execute srom-scholarly.php (mu-plugin v2.5, review 20.10.2026; v2.6–2.7 redirects). Run by test_muplugin.py:
// php muplugin_harness.php <plugin.php>; one "ok"/"FAIL" line per case, last line HARNESS ALL PASS / HARNESS FAILED n.
define('ABSPATH', '/');
$H = ['action' => [], 'filter' => [], 'sc' => []];
class WP_Post { public $ID; public $post_type; function __construct($id, $t) { $this->ID = $id; $this->post_type = $t; } }
class WP_Query { public $vars = []; public $found_posts = 0; public $posts = []; function __construct($a = []) {} function set($k, $v) { $this->vars[$k] = $v; } }
class WP_Term { public $term_id, $slug, $name, $count = 1; function __construct($i, $s) { $this->term_id = $i; $this->slug = $s; $this->name = $s; } }
function add_action($h, $cb, $p = 10, $n = 1) { global $H; $H['action'][$h][] = $cb; }
function add_filter($h, $cb, $p = 10, $n = 1) { global $H; $H['filter'][$h][] = $cb; }
function do_action($h, ...$a) { global $H; foreach ($H['action'][$h] ?? [] as $cb) $cb(...$a); }
function apply_filters($h, $v, ...$a) { global $H; foreach ($H['filter'][$h] ?? [] as $cb) $v = $cb($v, ...$a); return $v; }
function has_action($h) { global $H; return !empty($H['action'][$h]); }
function add_shortcode($t, $cb) { global $H; $H['sc'][$t] = $cb; }
function do_shortcode($s) { global $H; return preg_replace_callback('/\[(\w+)([^\]]*)\](?:\[\/\1\])?/', function ($m) use ($H) {
    if (!isset($H['sc'][$m[1]])) return '{' . $m[1] . '}'; return $H['sc'][$m[1]]([]); }, $s); }
function shortcode_atts($d, $a) { return array_merge($d, (array) $a); }
function add_rewrite_rule() {}
$OPT = []; $FLUSHES = 0;
function get_option($k, $d = false) { global $OPT; return $OPT[$k] ?? $d; }
function flush_rewrite_rules($hard = true) { global $OPT, $FLUSHES; $FLUSHES++; $OPT['rewrite_rules'] = apply_filters('rewrite_rules_array', ['articles/([^/]+)/?$' => 'index.php?srom_article=$matches[1]']); }
function esc_attr($s) { return htmlspecialchars((string) $s, ENT_QUOTES); }
function esc_html($s) { return htmlspecialchars((string) $s, ENT_QUOTES); }
function esc_url($s) { return (string) $s; }
function wp_json_encode($v, $f = 0) { return json_encode($v, $f); }
function home_url($p = '') { return 'https://x.test/' . ltrim($p, '/'); }
function user_trailingslashit($p) { return rtrim($p, '/') . '/'; }
function untrailingslashit($p) { return rtrim($p, '/'); }
function is_preview() { return false; }
function is_404() { global $IS404; return !empty($IS404); }
class Redir extends Exception {}
function wp_safe_redirect($to, $code = 302) { throw new Redir($code . ' ' . $to); }
function current_user_can() { return false; }
function taxonomy_exists() { return true; }
function post_type_exists() { return true; }
function is_wp_error($x) { return false; }
function get_term_by() { return false; }
function get_term_link() { return ''; }
function get_terms() { return [new WP_Term(1, 'czesc-i')]; }
function date_i18n($f, $t) { return date($f, $t); }
// --- data
$DB = []; $MAIN = null; $CUR = 0; $QUERIES = 0;
function get_field($k, $id = 0) { global $DB, $CUR; if (!$id) $id = $CUR; return $DB[$id][$k] ?? ''; }
function get_post_meta($id, $k, $s = false) { global $DB; return $DB[$id][$k] ?? ''; }
function get_post_type($id) { global $DB; return $DB[$id]['_type'] ?? ''; }
function get_the_ID() { global $CUR; return $CUR; }
function get_the_title($id) { global $DB; return $DB[$id]['_title'] ?? ''; }
function get_permalink($id = 0) { global $CUR; return 'https://x.test/p/' . ($id ?: $CUR) . '/'; }
function get_the_terms($id, $t) { return false; }
function get_queried_object() { global $MAIN; return $MAIN; }
function is_singular($t = '') { global $MAIN; return $MAIN instanceof WP_Post && (!$t || $MAIN->post_type === $t); }
function get_posts($a) { global $DB, $QUERIES; $QUERIES++; $out = [];
    foreach ($DB as $id => $r) if (($r['_type'] ?? '') === $a['post_type'] && (string) ($r['volume'] ?? '') === $a['meta_query'][0]['value'] && ($r['_status'] ?? 'publish') === 'publish') $out[] = $id;
    return $out; }

require $argv[1];
$fails = 0;
function t($name, $ok, $detail = '') { global $fails; if (!$ok) $fails++; echo ($ok ? 'ok   ' : 'FAIL ') . $name . ($ok ? '' : " — $detail") . "\n"; }
function page($main, $cur) { global $MAIN, $CUR, $GLOBALS; $MAIN = $main; $CUR = $cur; $GLOBALS['SROM_CTX'] = ['id' => 0, 'type' => '']; do_action('wp'); }
function head() { ob_start(); do_action('wp_head'); return ob_get_clean(); }
function sc($t) { global $H; return $H['sc'][$t]([]); }

$CC = 'https://creativecommons.org/licenses/by-nc/4.0/';
$DB = [
    10 => ['_type' => 'srom_volume', 'volume' => '17', 'year' => '2024'],
    11 => ['_type' => 'srom_article', '_title' => 'Z DOI', 'volume' => '10', 'doi' => '10.68100/abcdefgh', 'license_url' => $CC, 'pdf_file' => 'https://x.test/a.pdf', 'abstract_pl' => 'A', 'authors_raw' => "Jan|Kowalski||"],
    12 => ['_type' => 'srom_article', '_title' => 'Bez DOI', 'volume' => '10', 'doi' => '', 'license_url' => '', 'pdf_file' => 'https://x.test/b.pdf', 'authors_raw' => "Anna|Nowak||", 'flipbook_shortcode' => '[srom_flipbook]'],
    20 => ['_type' => 'srom_volume', 'volume' => '18', 'year' => '2025'],
    21 => ['_type' => 'srom_article', '_title' => 'CC only', 'volume' => '20', 'doi' => '10.68100/zzzzzzzz', 'license_url' => $CC],
    30 => ['_type' => 'srom_volume', 'volume' => '16'],
    31 => ['_type' => 'srom_article', 'volume' => '30', 'license_url' => ''],
];
// 1. article without DOI: no stub identifiers
page(new WP_Post(12, 'srom_article'), 12);
$h = head();
t('no-DOI: no dc.identifier stub', strpos($h, 'dc.identifier') === false, $h);
t('no-DOI: no bare doi.org in JSON-LD', strpos($h, 'https://doi.org/"') === false && strpos($h, 'https:\/\/doi.org\/"') === false, $h);
t('no-DOI: body classes', apply_filters('body_class', []) === ['srom-no-doi', 'srom-no-license', 'srom-no-abstract'], json_encode(apply_filters('body_class', [])));
t('no-DOI: CSS emitted', strpos($h, 'srom-backcat') !== false);
t('license fallback text', sc('srom_license') === 'Wszelkie prawa zastrzeżone; dostęp bezpłatny', sc('srom_license'));
t('flipbook self-reference does not recurse', is_string(sc('srom_flipbook')), '');
// 2. article with DOI
page(new WP_Post(11, 'srom_article'), 11);
$h = head();
t('DOI: dc.identifier present', strpos($h, 'content="doi:10.68100/abcdefgh"') !== false, $h);
t('DOI: JSON-LD identifier', strpos($h, '"identifier":"https://doi.org/10.68100/abcdefgh"') !== false, $h);
t('DOI: no body classes', apply_filters('body_class', []) === [], json_encode(apply_filters('body_class', [])));
t('license by name', strpos(sc('srom_license'), 'CC BY-NC 4.0') !== false, sc('srom_license'));
// 3. archive page (main query object = term), current post = first article without DOI
page(new WP_Term(5, 'autor-x'), 12);
t('archive: no body classes leak', apply_filters('body_class', []) === [], json_encode(apply_filters('body_class', [])));
t('archive: no CSS', strpos(head(), 'srom-backcat') === false);
t('archive: authors shortcode still works in loop item', strpos(sc('srom_authors'), 'Anna Nowak') !== false);
// 4. off-context: authors returns ''
page(new WP_Term(5, 'x'), 0);
t('off-context authors empty', sc('srom_authors') === '', sc('srom_authors'));
// 5. volume licences
page(new WP_Post(10, 'srom_volume'), 10);
t('mixed volume: według artykułu', sc('srom_volume_license') === esc_html('według artykułu (CC BY-NC 4.0, wszelkie prawa zastrzeżone)'), sc('srom_volume_license'));
t('mixed volume: licence row shown', apply_filters('body_class', []) === []);
page(new WP_Post(20, 'srom_volume'), 20);
t('single-CC volume: linked name', strpos(sc('srom_volume_license'), '>CC BY-NC 4.0</a>') !== false, sc('srom_volume_license'));
page(new WP_Post(30, 'srom_volume'), 30);
t('no-CC volume: empty + hidden', sc('srom_volume_license') === '' && apply_filters('body_class', []) === ['srom-no-license'], sc('srom_volume_license') . json_encode(apply_filters('body_class', [])));
// 6. query filters: guard + fail closed + no kill switch
$_GET['srom_off'] = '1';
page(new WP_Post(10, 'srom_volume'), 10);
$q = new WP_Query(); do_action('elementor/query/srom_contents_part1', $q);
t('?srom_off ignored: TOC still scoped', ($q->vars['post_type'] ?? '') === 'srom_article' && isset($q->vars['tax_query']), json_encode($q->vars));
page(new WP_Term(1, 'x'), 0);
$q = new WP_Query(); do_action('elementor/query/srom_other_articles', $q);
t('W tym tomie fails closed off-context', ($q->vars['post__in'] ?? null) === [0], json_encode($q->vars));
// 7. retired bases 301 to /volumes/ and /articles/ (v2.6)
function redir($uri) { $_SERVER['REQUEST_URI'] = $uri; page(new WP_Term(1, 'x'), 0);
    try { do_action('template_redirect'); return ''; } catch (Redir $e) { return $e->getMessage(); } }
t('/tom/18-2025/ -> /volumes/18-2025/', redir('/tom/18-2025/') === '301 https://x.test/volumes/18-2025/', redir('/tom/18-2025/'));
t('/tom/18-2025 (no slash) + query kept', redir('/tom/18-2025?a=1') === '301 https://x.test/volumes/18-2025/?a=1', redir('/tom/18-2025?a=1'));
t('/tomy/ -> /volumes/', redir('/tomy/') === '301 https://x.test/volumes/', redir('/tomy/'));
t('/tomy/page/2/ -> /volumes/page/2/', redir('/tomy/page/2/') === '301 https://x.test/volumes/page/2/', redir('/tomy/page/2/'));
t('/artykuly/ -> /articles/', redir('/artykuly') === '301 https://x.test/articles/', redir('/artykuly'));
t('/tomasz/, /volumes/18-2025/ untouched', redir('/tomasz/') === '' && redir('/volumes/18-2025/') === '' && redir('/articles/10.68100/abcdefgh/') === '', redir('/tomasz/'));
// 8. old PDF names 301 to Studia_Romologica_ once the file is gone (v2.7)
$IS404 = true;
$P = '/wp-content/uploads/archive/18-2025/';
t('404 SROM_ PDF -> Studia_Romologica_ PDF, same folder', redir($P . 'SROM_18_2025_Ostendorf_Historia.pdf') === '301 https://x.test' . $P . 'Studia_Romologica_18_2025_Ostendorf_Historia.pdf', redir($P . 'SROM_18_2025_Ostendorf_Historia.pdf'));
t('404 on another file, or a new-name PDF, untouched', redir($P . 'Studia_Romologica_18_2025_X.pdf') === '' && redir('/wp-content/uploads/2025/SROM_18_2025_X.pdf') === '' && redir($P . 'SROM_cover.pdf') === '', redir($P . 'Studia_Romologica_18_2025_X.pdf'));
$IS404 = false;
t('SROM_ PDF that still exists (no 404): untouched', redir($P . 'SROM_18_2025_Ostendorf_Historia.pdf') === '', redir($P . 'SROM_18_2025_Ostendorf_Historia.pdf'));
// 8. DOI rewrite rule survives any rebuild (v2.8)
$r = apply_filters('rewrite_rules_array', ['articles/([^/]+)/?$' => 'x', 'articles/[^/]+/([^/]+)/?$' => 'attachment']);
t('DOI rule first in rebuilt rules', array_key_first($r) === 'articles/10\\.[0-9]+/([a-z0-9-]+)/?$', array_key_first($r));
t('legacy /artykul/ rule present, CPT rules kept', isset($r['artykul/([a-z0-9-]+)/?$']) && isset($r['articles/([^/]+)/?$']) && count($r) === 4, json_encode(array_keys($r)));
$OPT['rewrite_rules'] = ['articles/([^/]+)/?$' => 'x']; $FLUSHES = 0; do_action('wp_loaded');
t('self-check rebuilds once when DOI rule missing', $FLUSHES === 1 && isset($OPT['rewrite_rules']['articles/10\\.[0-9]+/([a-z0-9-]+)/?$']), "flushes=$FLUSHES");
do_action('wp_loaded');
t('self-check idle when rules present', $FLUSHES === 1, "flushes=$FLUSHES");
$OPT['rewrite_rules'] = ''; do_action('wp_loaded');
t('self-check idle on plain permalinks / pending rebuild', $FLUSHES === 1, "flushes=$FLUSHES");
echo $fails ? "HARNESS FAILED $fails\n" : "HARNESS ALL PASS\n";
