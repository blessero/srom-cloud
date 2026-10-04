# WordPress gotchas that cost real hours

Each of these produced a real bug or a false test failure. They share a shape: **the code looks correct and fails quietly.**

## `wp_nonce_url()` HTML-escapes the URL — never redirect with it

`wp_nonce_url()` is built for printing into HTML, so it escapes `&` to `&#038;`. Put that in a `Location:` header and the query string is corrupt.

```php
// WRONG — silently broken redirect
wp_safe_redirect( wp_nonce_url( $url, 'action' ) );

// RIGHT — build redirect targets with add_query_arg()
wp_safe_redirect( add_query_arg( array( 'page' => $slug, 'job' => $token ), admin_url('admin.php') ) );
```
Only caught by following an actual HTTP redirect in a test. Unit-level inspection shows a plausible string.

## Admin menu icons only exist on top-level items

`add_management_page()` (Tools submenu), `add_options_page()`, etc. have **no icon slot at all**. If the user wants a branded icon like ACF's, the page must become top-level via `add_menu_page( $title, $label, $cap, $slug, $cb, $icon, $position )`.

Custom SVG icon → base64 data URI (keeps your colors; dashicons get recolored by WP):
```php
'data:image/svg+xml;base64,' . base64_encode( $svg_markup )
```

Moving from submenu to top-level **changes the parent file**: URLs go from `tools.php?page=…` to `admin.php?page=…`. Update every URL builder or every link 404s.

## `sanitize_title()` percent-encodes non-ASCII punctuation

A title of `SROM·18·2025` (middle dot, U+00B7) becomes the slug:
```
srom%c2%b718%c2%b72025      → /tom/srom%c2%b718%c2%b72025/
```
It doesn't strip the character; it encodes it. Any auto-created post whose title contains typographic punctuation gets a garbage URL.

**Fix:** set `post_name` explicitly from clean components (`"18-2025"`), or pre-replace non-alphanumerics before sanitizing:
```php
$slug = sanitize_title( preg_replace( '/[^a-z0-9]+/i', '-', $raw ) );
```

## WordPress search never indexes ACF meta

Native search covers `post_title`, `post_content`, `post_excerpt` — and nothing else. An abstract living only in an ACF field is **unfindable by site search**.

Mirror searchable text into `post_content`/`post_excerpt` at import time, regenerated from the same source cell on every run so the copies can't drift. The ACF field stays canonical for structured/metadata use.

## `wp_count_terms()` can return a string

`0 === wp_count_terms(...)` fails when it returns `"0"`. Cast: `0 === (int) wp_count_terms(...)`. (A general hazard with older WP APIs — prefer `(int)` casts in assertions.)

## Rewrite rules

- `flush_rewrite_rules()` is expensive — call it **once** after registering new post types/taxonomies (on install/upgrade), never on every load.
- Rewrite slugs only take effect with **pretty permalinks enabled**. With plain permalinks, `get_term_link()` returns `?taxonomy=slug` and any slug assertion "fails" misleadingly.
- ACF omits `rewrite['slug']` when it equals the object's key. Assert on `get_permalink()` / `get_term_link()` output, never on the config array.

## Taxonomy key ≠ URL slug

`slowa_kluczowe` (the key you pass to `get_the_terms()`, `wp_set_object_terms()`, `tax_query`) vs `slowa-kluczowe` (the pretty URL). Mixing them up produces empty results with no error. Document both columns in any handover table.

## `wp_insert_post()` / `wp_update_post()`

- Pass `wp_slash()`ed data — WP unslashes internally.
- Pass `true` as the second arg to get a `WP_Error` back instead of a silent `0`.
- Changing `post_date` on an existing draft requires `'edit_date' => true`, otherwise WP ignores it.

## Meta vs core vs taxonomy (the phantom-key problem)

Other developers will assume every column is a meta key. It isn't, and reading a non-existent meta key returns `''` — a blank template, not an error. Publish the persisted-vs-derived table (see SKILL.md). Recurring examples:

| Assumed meta key | Actually |
|---|---|
| `seq` | `menu_order` core field → order by `menu_order` |
| `section` | a taxonomy → `get_the_terms($id,'dzial')` |
| `landing_url` | derived → `get_permalink()`; storing it guarantees drift |
| `doi_suffix` | the post slug → `get_post_field('post_name',$id)` |
