# SROM — Studia Romologica journal site

Polish Romani-studies journal (studiaromologica.pl). WordPress + **ACF Free** (no repeater — hence flat textarea conventions). Working folder: MB's website project folder on his Mac (not part of the SROM plugin).

> **Canonical contract lives in the `srom-quant` skill (formerly `srom-scholarly-curator`).** That skill's `SKILL.md` + `references/master_schema.md` are the single source of truth for the data contract and the locked decisions. This file is the *importer's* view of it — enough to build against without re-deriving. If the two ever disagree, the curator wins. Keep them in sync; last reconciled 2026-07-24.

> **Before debugging live behaviour, enumerate what is actually deployed.** The project folder is NOT the whole site. Real incidents came from a **second, legacy `wp-content/mu-plugins/srom-loops.php`** (not in the repo) that hooked the same Elementor query IDs as `srom-scholarly.php` and recursed into a stack-overflow fatal, and from Elementor **Custom Code** snippets. List `wp-content/mu-plugins/`, `wp-content/plugins/`, and Elementor → Custom Code on the server and read anything unfamiliar before concluding a bug is in our code.

## Three components, strict ownership (do not cross the lines)

| Concern | Owner |
|---|---|
| CPTs, taxonomies, ACF field groups (as ACF-native DB records); CSV import | **srom-importer** plugin — this skill's `assets/srom-importer/` |
| Full-DOI permalinks, canonical 301, Highwire `citation_*` tags, JSON-LD, display shortcodes | **srom-scholarly.php** (mu-plugin) |
| Elementor Theme Builder templates, dynamic tags | Elementor templates (use **wp-elementor-builder** skill) |

The mu-plugin **registers no post types** — double registration would fight over rewrite args. If asked to add a shortcode, citation tag, or permalink rule, that's the mu-plugin's job, not the importer's.

## Content model (importer v2.3.0)

**Post types**
- `srom_article` — "Artykuł", **`/articles/…`** (English base — DOI landing URLs are `/articles/{full-doi}/`, so the CPT must share it), archive `/artykuly/`. ⚠️ On the **live** site the base is a DB-native ACF record: the plugin default only applies to fresh installs — change it once by hand in **ACF → Post Types → Artykuł → URL slug → `articles`**, then Permalinks → Save.
- `srom_volume` — "Tom", `/tom/…`, archive `/tomy/`. Auto-created volumes get slug `{volume}-{year}` → `/tom/18-2025/` and title **`Tom: {volume}·{year}`** (e.g. "Tom: 18·2025", U+00B7), built from the volume+year columns (falls back to the signature).

**Taxonomies on `srom_article`** (key ≠ URL slug in one case)

| Key | Hierarchical | URL | Filled from |
|---|---|---|---|
| `dzial` | yes | `/dzial/` | `section_label` — **generic** `Część I`…`Część IV` (slugs `czesc-i`…`czesc-iv`), NOT theme-suffixed. The mu-plugin's TOC filter matches by slug prefix `czesc-i`, so it tolerates a legacy `czesc-i-…` during an in-place rename. |
| `slowa_kluczowe` | no | `/slowa-kluczowe/` ← note hyphen | `keywords_pl` |
| `autor` | no | `/autor/` | `authors_display` (comma-split, one term per author) |
| `rocznik` | no | `/rocznik/` | `year` |

**Article ACF fields (the complete list of persisted meta keys):**
`article_id`, `doi`, `title_en`, `authors_raw`, `authors_display`, `abstract_pl`, `abstract_en`, `keywords_pl`, `keywords_en`, `bio_note`, `pages_from`, `pages_to`, `language`, `license_url`, `pdf_file`, `flipbook_shortcode` (optional per-article DearFlip override; empty = mu-plugin builds the reader from `pdf_file`), `is_translation`, `original_title`, `original_source`, `original_doi`, `volume`.

**Volume (Tom) fields:** `volume`(number), `year`, `signature`, `theme`, `pub_date`(Y-m-d), `full_pdf`(file, `return_format: url`), `description`.

**Article→Tom link:** ACF `volume` post_object, `return_format: id` → returns the Tom's post ID. Note `volume` exists on *both* post types with different meanings (relation vs number) — this is deliberate and was the source of a real auto-mapping bug (see `plugin-architecture.md`).

**Import keys (upsert):** `article_id` for articles, `signature` for volumes (`SROM·18·2025`).

## NOT meta keys — the phantom-key table

Other devs will assume field-name→meta-key. These fail silently (blank, not error):

| Assumed | Actually | Read via |
|---|---|---|
| `seq` | core `menu_order` | order by `menu_order` |
| `section_nr` / `section` | `dzial` taxonomy (from `section_label`; `section_nr` itself ignored) | `get_the_terms($id,'dzial')` |
| `landing_url` | ignored column; URL is DOI-derived | `get_permalink()` — never store it, it drifts |
| `doi_suffix` | the post slug | `get_post_field('post_name',$id)` |
| `year` (on article) | `rocznik` taxonomy + the Tom's `year` | traverse `volume`→Tom |

Only `volume` resolves the way a naive assumption expects.

`abstract_pl` is additionally mirrored into `post_content` + `post_excerpt` — WP search never indexes ACF meta, so without it articles aren't findable by abstract. Regenerated from the same CSV cell each import, so it can't drift.

## Master CSV (`srom_master_v3.csv`)

One article per row, ~38 columns, all-English headers. Extra non-ACF columns (`journal_title`, `issn`, `landing_url`, `publisher`) are ignored unless mapped.

- **Authors:** `authors_struct` = `Given|Surname|Affiliation|ORCID-URL`, multiple authors separated by ` ;; `. Imported into `authors_raw` as one author per line. No `|` or `;;` inside affiliation text.
- `pdf_url` (full URL) → the ACF `pdf_file` field. **Not** the `pdf_file` *column* (a bare filename) — a classic mis-map.
- `title_pl` → post title; `doi_suffix` → post slug; `seq` → menu_order.
- **Volume columns keep their old names**: `issue_signature`, `issue_theme` (from before the Numer→Tom rename). Do not "fix" them — the CSV is the contract with InDesign and the Crossref generator.
- Placeholder junk is expected in unfinished cells: `TODO`, `2025-12-TODO`, `10.XXXXX/…`, `todo0001`. The importer skips the bad field with a note and imports the rest of the row.

## Rename history (settled — do not re-litigate)

- v2.0: plain `register_post_type()` → **ACF-native DB records** (client must manage the model in ACF's UI).
- v2.0: flat `section` select → hierarchical `dzial` taxonomy.
- v2.1: `doi_suffix` ACF field **removed** (the suffix *is* the slug); added `autor` + `rocznik` taxonomies; `abstract_pl` mirrored to post_content/excerpt.
- v2.2: `srom_issue`/"Numer" → **`srom_volume`/"Tom"** (a volume is the correct term for an annual journal, and it matched the front-end dev's naming). Article link field `issue` → `volume`. In-place upgrades retire the old `post_type_srom_issue` / `group_srom_issue` records.
- v2.2.2: `full_pdf` `return_format` id → `url` (so a download button can bind directly; storage unchanged).
- v2.3.0: article CPT default rewrite slug `artykul` → **`articles`** (DOI landing base); auto-created volume title → **`Tom: {vol}·{year}`** (was the signature, which leaked a "SROM·" prefix); added optional **`flipbook_shortcode`** article field. ⚠️ The slug + existing volume titles/slugs must be changed **by hand on the live site** — DB-native ACF records ignore plugin defaults; only fresh installs get them automatically.

## Working style for this project

The user coordinates three parallel dev chats and relays messages between them. Consequences:

- **The `HANDOVER.md` in the working folder is the cross-team contract.** Update it whenever the model changes — especially the persisted-vs-derived table. It is what stops the other two devs building against phantom keys.
- Don't unilaterally change the shared content model when another component may read it. Flag it, recommend, let the coordinator get a nod. (Exception: read-time-only changes with provably no storage impact, which you can ship with an FYI.)
- The user is happy to wipe and re-import from the master CSV — the importer is idempotent, so a clean slate is always available. Prefer "do it right" over migration hacks when they say the data is disposable.
