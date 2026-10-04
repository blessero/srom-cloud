# SROM Importer — handover brief for cross-plugin work

**Yes, drop in `srom-importer.zip` as-is** — that's the real source, needed if any tweak touches PHP. This document is the map: what the plugin owns, exact names/slugs, and how data correlates, so the other plugin can read/write the same content model without guessing.

## 1. What this plugin owns

It registers the entire *Studia Romologica* content model as **native ACF database records** (not `register_post_type()` calls) — so everything below is editable under **Custom Fields → Post Types / Taxonomies / Field Groups** in wp-admin, exactly like anything built by hand in ACF. It also runs a spreadsheet importer that fills this content model from the master CSV.

Requires ACF (free tier is enough). Auto-installs on activation, no button to press. Fixed ACF keys (so re-runs are detectable): `post_type_srom_article`, `post_type_srom_volume`, `taxonomy_srom_dzial`, `taxonomy_srom_slowa_kluczowe`, `taxonomy_srom_autor`, `taxonomy_srom_rocznik`, `group_srom_article`, `group_srom_volume`.

> **v2.2 rename:** the second post type is `srom_volume` (label **Tom**). It was called `srom_issue` / **Numer** up to v2.1 — that slug is gone. In-place upgrades auto-retire the old `srom_issue` records.

## 2. Post types

| Post type slug | Label | Slug/archive | Notes |
|---|---|---|---|
| `srom_article` | Artykuł | `/artykul/...`, archive `/artykuly/` | `public`, `show_in_rest`, `has_archive`, supports title/editor/thumbnail/custom-fields/revisions/excerpt |
| `srom_volume` | Tom | `/tom/...`, archive `/tomy/` | same visibility flags. Auto-created volumes get a clean slug `{volume}-{year}` (e.g. `/tom/18-2025/`) — set explicitly so the signature's middle dot isn't percent-encoded into the URL (v2.2.1). |

Both are `show_in_rest => true` — Gutenberg, REST API, and Elementor dynamic tags all work normally.

## 3. Taxonomies attached to `srom_article`

| Taxonomy key | Label | Hierarchical? | Rewrite slug (URL) | Filled from (import) |
|---|---|---|---|---|
| `dzial` | Dział | **yes** | `/dzial/` | column `section_label` |
| `slowa_kluczowe` | Słowa kluczowe | no (flat tags) | `/slowa-kluczowe/` | column `keywords_pl` |
| `autor` | Autor | no (flat tags) | `/autor/` | column `authors_display` |
| `rocznik` | Rocznik | no (flat tags) | `/rocznik/` | column `year` |

**Taxonomy key ≠ rewrite slug.** Use the *key* (underscored) in `get_the_terms()`, `wp_get_object_terms()`, `wp_set_object_terms()`, `register_taxonomy` lookups, `tax_query`. The rewrite slug only shapes URLs. The only place they differ is `slowa_kluczowe` (key) vs `slowa-kluczowe` (URL). For `autor`, `rocznik` and `dzial` the two coincide.

All four are `public`, `show_in_rest`, `show_admin_column`; `dzial` also has `show_in_quick_edit`. Term archive URLs verified live: `/autor/<term>/`, `/rocznik/<term>/`, `/dzial/<term>/`, `/slowa-kluczowe/<term>/`.

These four are the **only** taxonomies attached to `srom_article`. No categories/post_tags, nothing else.

`autor` terms are produced by comma-splitting `authors_display`, so `"Elena Marushiakova, Vesselin Popov"` becomes two separate terms.

## 4. ACF field groups (full field list)

### Group "Artykuł" → post type `srom_article`

| ACF field name | Type | Notes |
|---|---|---|
| `article_id` | text | **import key** (upsert match), e.g. `SROM-18-2025-001` |
| `doi` | text | e.g. `10.xxxxx/srom-18-2025-001` |
| `title_en` | text | |
| `authors_raw` | textarea | one author per line: `Given\|Surname\|Affiliation\|ORCID-URL` |
| `authors_display` | text | authors exactly as printed |
| `abstract_pl` | textarea | |
| `abstract_en` | textarea | |
| `keywords_pl` | text | comma-separated; **also feeds** the `slowa_kluczowe` taxonomy |
| `keywords_en` | text | semicolon-separated discrete terms (`a; b; c`) — forward-compatible with a future EN taxonomy |
| `bio_note` | textarea | |
| `pages_from` | number | |
| `pages_to` | number | |
| `language` | text | default `pl` |
| `license_url` | text | full CC URL |
| `pdf_file` | text | **direct PDF URL**, not a file/attachment field — used as `citation_pdf_url` |
| `is_translation` | text | |
| `original_title` | text | |
| `original_source` | text | |
| `original_doi` | text | |
| `volume` | post_object → `srom_volume` | `return_format: id`, single, nullable — this is the article→Tom link (the field name is `volume`) |

Plus the four taxonomies above via standard WP term boxes — not ACF fields.

Deliberately **absent** fields (don't read these meta keys, they're stale):
- **`section`** — was a flat select in v1, replaced by the `dzial` taxonomy.
- **`doi_suffix`** — removed in v2.1. The suffix *is* the post slug (`post_name`); the full DOI is in `doi`. The CSV column `doi_suffix` is still read, but only to set the slug.
- **`issue`** — the article→volume link field was renamed `issue` → **`volume`** in v2.2 (and now targets `srom_volume`). Reference `get_field('volume', $article_id)`.

`abstract_pl` is additionally mirrored into **`post_content`** and **`post_excerpt`** on every import — WP's native search indexes those but never ACF meta. `abstract_pl` stays the canonical source for citation metadata; the mirror is regenerated from the same CSV cell each run, so it can't drift.

### Group "Tom" → post type `srom_volume`

| ACF field name | Type | Notes |
|---|---|---|
| `volume` | number | |
| `year` | number | |
| `signature` | text | **import key** (upsert match), e.g. `SROM·18·2025` |
| `theme` | text | |
| `pub_date` | date_picker | stored/returned as `Y-m-d` |
| `full_pdf` | file | `return_format: url` (v2.2.2; stores the attachment ID, `get_field` returns the URL — bind directly to a download button) |
| `description` | wysiwyg | full toolbar |

## 5. Correlation cheat-sheet (spreadsheet column → WP data)

This is the importer's built-in auto-mapping preset — useful if another tool needs to replicate or anticipate the same transforms:

| Spreadsheet column | Goes to | Transform |
|---|---|---|
| `title_pl` | post title | — |
| `doi_suffix` | post slug | — |
| `seq` | menu_order | — |
| `authors_struct` | ACF `authors_raw` | split on `;;` → one author per line |
| `pdf_url` | ACF `pdf_file` | verbatim (note: NOT the `pdf_file` column, which is a bare filename and is ignored) |
| `issue_signature` | ACF `volume` (post_object) | resolved to the matching `srom_volume` (Tom) post by its `signature` field; note the CSV column keeps its old name `issue_signature` |
| `keywords_pl` | ACF `keywords_pl` **and** taxonomy `slowa_kluczowe` | one column feeds both |
| `section_label` | taxonomy `dzial` | term name(s), `;`/comma/newline separated, `Parent > Child` for hierarchy |
| `authors_display` | taxonomy `autor` | comma-split → one term per author |
| `year` | taxonomy `rocznik` | one term per year |
| `abstract_pl` | ACF `abstract_pl` **and** `post_content` **and** `post_excerpt` | one column feeds all three (search indexing) |
| `keywords_en` | ACF `keywords_en` | normalized to `; `-separated |
| `signature`, `theme`, `pub_date_online` | volume fields `signature`/`theme`/`pub_date` | when importing a separate volume (Tom) sheet |
| everything else (e.g. `journal_title`, `issn`, `landing_url`) | ignored | not mapped unless user maps manually |

Import keys (upsert match, never duplicates on re-run): `article_id` for articles, `signature` for volumes.

### NOT stored as post meta (do not build templates against these as meta keys)

Several CSV columns drive core WP fields, taxonomies, or nothing — they are **not** ACF meta on the article. Common traps:

| You might expect a meta key… | …but it's actually | Read it via |
|---|---|---|
| `seq` | the core `menu_order` post field | order by `menu_order` (e.g. `WP_Query` `orderby => menu_order`) |
| `section_nr` / `section` | the `dzial` taxonomy (term I/II, from the `section_label` column; `section_nr` itself is ignored) | `get_the_terms($id, 'dzial')` / `tax_query` |
| `landing_url` | not stored — an ignored CSV column; the canonical URL is DOI-derived | `get_permalink($id)` (never a stored key — storing it would drift from the canonical URL) |
| `doi_suffix` | the post slug (`post_name`) | `get_post_field('post_name', $id)` |
| `year` (on the article) | the `rocznik` taxonomy + the linked Tom's `year` field | `get_the_terms($id,'rocznik')`, or traverse `volume`→Tom |

Only `volume` (the article→Tom relation, returns the parent post ID) is a real post_object meta key that resolves as a naïve field-name→meta-key mapping would assume. Everything else on the article that IS a meta key is in the §4 field table.

## 6. Programmatic surface for another plugin to hook into

- **Reading**: `get_field('article_id', $post_id)`, `get_the_terms($post_id, 'dzial')`, `get_the_terms($post_id, 'slowa_kluczowe')`, `get_field('volume', $post_id)` (returns the linked Tom's post ID).
- **Post type/taxonomy existence**: standard `post_type_exists('srom_article')`, `taxonomy_exists('dzial')` — both true as soon as this plugin is active (auto-installed).
- **Class entry points** (in `includes/`) if you need to call the setup logic directly: `SROM_Imp_Setup::is_installed()`, `SROM_Imp_Setup::status()`, `SROM_Imp_Setup::install($overwrite=false)`. Fields/targets introspection: `SROM_Imp_Fields::get_targets($post_type)`.
- No custom hooks/filters are exposed yet (fires no custom actions) — if the other plugin needs to react to imports (e.g. "after an article is upserted"), that would need to be added to `class-srom-imp-runner.php`'s `do_row()` method. Flag this if needed — not currently there.

## 7. Things likely to need alignment/tweaks

- If the other plugin was built against the **old v1 flat `section` select**, it needs to switch to reading the `dzial` taxonomy instead.
- Likewise `doi_suffix` is no longer an ACF field (v2.1) — read `get_post_field('post_name', $id)` or `doi`.
- If it expects `pdf_file` to be an attachment ID (ACF file field), note it's actually a **plain text URL field** here by design (citation metadata convention) — don't assume `wp_get_attachment_url()`.
- Taxonomy **keys** use underscores (`slowa_kluczowe`); only the pretty permalink uses a hyphen (`slowa-kluczowe`) — easy source of a silent mismatch. `autor`/`rocznik`/`dzial` are identical in both.
- The article→volume link is the `volume` post_object field returning a **plain ID** (`return_format: id`), not an array/object. (It was named `issue` before v2.2.)
- **v2.2 rename summary for both other devs:** post type `srom_issue`→`srom_volume`, label Numer→**Tom**, URL base `/numer/`→`/tom/` (archive `/numery/`→`/tomy/`), article link field `issue`→`volume`, ACF keys `post_type_srom_issue`/`group_srom_issue`→`..._srom_volume`. CSV column names are unchanged (still `issue_signature`, `issue_theme`).

## 8. Upgrade behaviour (relevant if the site already runs 2.0.0)

Bumping the plugin runs a version-triggered top-up on `acf/init`: it creates definitions the new version added (e.g. `autor`, `rocznik`) and **never overwrites** records the user has edited. If every definition was deliberately removed, the upgrade leaves them removed. Removing the `doi_suffix` field from the shipped field group only affects *fresh* installs and "Reset to plugin defaults" — an existing field group keeps the field until reset, and pre-existing `doi_suffix` postmeta is left in place (harmless, just orphaned).
