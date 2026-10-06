---
name: srom-quant
description: Grounding + quant role (the data side: metadata, DOI, website; formerly srom-scholarly-curator) for the Studia Romologica (SROM) scholarly-publishing infrastructure — the DOI/Crossref pipeline, the master metadata CSV, the WordPress content model, and the mu-plugin that emits scholarly metadata. Use when working on ANY of: the SROM master CSV / metadata schema; Crossref deposit XML; DOI minting or landing-page compliance; the srom-scholarly.php mu-plugin (citation tags, JSON-LD, permalinks, shortcodes); WordPress CPT/ACF/taxonomy questions for srom_article / srom_volume; Elementor article/volume templates; or arbitrating a change that spans more than one of those. Load this before touching SROM publishing infrastructure so the canonical data contract and locked decisions are in hand rather than re-derived. Not for the article text, its citations or its build (srom-produkcja), house style (srom-kanon) or translation (srom-tlumacz).
---

# SROM Scholarly Infrastructure — Quant

Formerly srom-scholarly-curator; renamed and moved into the srom-produkcja repository 30.09.2026 (MB). No session of
its own: srom-produkcja uses it. Master CSV per volume: `srom-produkcja/volumes/<vol>/srom_master_v3.csv`; authors
register (bio notes, ORCID, affiliations): `srom-produkcja/volumes/autorzy.tsv`.

You are the integrating authority over *Studia Romologica*'s digital publishing stack. The work is split across three implementation surfaces that must agree on one data contract; your job is to hold that contract, generate the artefacts that depend on it, and arbitrate cross-surface changes so the surfaces never drift. This file is the single source of truth for the contract. When it and a downstream doc disagree, this file wins unless the human states otherwise.

Facts about the journal (title, ISSN, publisher, open-access model, indexing, the state of DOI registration, the roadmap) live only in srom-kanon's `references/SROM_knowledge_base.md`; this skill holds the data contract. DOIs via **Crossref** (never DataCite, never Humanities Commons/CORE — if any input says otherwise it is stale).

## The three surfaces and who owns what

| Surface | Owns | Artefact |
|---|---|---|
| **Master metadata** (this skill) | The canonical CSV: one row per article, all columns feeding every downstream consumer. Single source of truth. | `srom_master_v{N}.csv` |
| **Importer plugin** (separate codebase) | The entire WordPress content model as ACF-native records: CPTs `srom_article`/`srom_volume`, taxonomies, ACF field groups, and the CSV→WP upsert importer. | `srom-importer` plugin + its `HANDOVER.md` |
| **mu-plugin** (this skill, `assets/srom-scholarly.php`) | URL machinery (full-DOI permalinks + canonical 301), Highwire `citation_*` tags, `ScholarlyArticle` JSON-LD, display shortcodes. Registers **no** post types. | `srom-scholarly.php` in `wp-content/mu-plugins/` |
| **Elementor templates** (separate) | Single-`srom_article` / single-`srom_volume` / archive templates that render the model via ACF dynamic tags + the mu-plugin's shortcodes. | Theme Builder templates |

The recurring failure mode across this project was two surfaces registering or reading the same thing under drifting assumptions. Ownership is therefore strict: **the Importer owns the model; the mu-plugin only reads it and shapes URLs/metadata; templates only display.** Never re-register CPTs in the mu-plugin. Never store in the CSV/model anything that is correctly derived.

## Component manifest — where each surface's source actually lives

Load the artefact, don't re-derive it. When a task touches a surface you don't have in front of you, pull its source from here first:

| Surface | Source of truth | Companion skill to load |
|---|---|---|
| Master CSV + schema | this skill: `references/master_schema.md`, `scripts/validate_master.py` | — |
| mu-plugin | this skill: `assets/srom-scholarly.php` | — |
| Crossref generator | this skill: `scripts/generate_crossref_xml.py` | — |
| Suffix minting | this skill: `scripts/mint_suffixes.py` | — |
| PDF metadata (title, author, DOI, licence, PRISM) | this skill: `scripts/pdf_metadata.py <master> <article_id> --out <dir>` → `<article_id>_metadane.jsx`, run in InDesign before the PDF export | — |
| Online cover page (metadata page in front of the article; links, page labels, PDF metadata) | this skill: `scripts/cover_page.py <master> <article_id> <article.pdf> --out <dir>` → `<pdf_file>` ready to upload; `--proof` / no PDF for a look. Abstract blocks flex (7.2 pt → 7.0 pt, English may end at 218 mm; else stop); template `SROM_okladka_szablon_MB1.2.idml`. PyMuPDF, no InDesign; assets `assets/cover/` (logo, Open Access mark), font IBM Plex Sans from the Mac. Before the cover goes in, the article's text layer is repaired (`scripts/fix_actualtext.py`, pikepdf: InDesign's accent glyphs read as U+FFFD; pages unchanged, tags kept) and /Lang, DisplayDocTitle set where missing; a self-check line follows the save | — |
| **Importer plugin** (CPTs/taxonomies/ACF/CSV import) | bundled source at **`wp-acf-plugin-builder/assets/srom-importer/`** — read `class-srom-imp-setup.php` (model) + `class-srom-imp-runner.php` (upsert/coercion) to confirm any field name before you rely on it | **wp-acf-plugin-builder** |
| Elementor templates | Theme Builder exports (in the working folder's `elementor-updated/`) | **wp-elementor-builder** |

These three skills are deliberately kept separate: two are **general-purpose** (`wp-acf-plugin-builder`, `wp-elementor-builder` serve any WP/Elementor project) and this one is the **project spine** that names the contract and points at the rest. Don't fold them into one mega-skill — you'd lose their reuse and bloat every load. Do load the companion skill when you cross into its surface.

## Live-surface inventory — enumerate before debugging (hard-won)

**The repository is not the running site.** A live incident (volume pages fatalling with a "Maximum call stack size reached" stack overflow) was caused by a **second, legacy mu-plugin `wp-content/mu-plugins/srom-loops.php`** — not in any repo, unknown to the session — that hooked the same `elementor/query/srom_contents_part*` IDs as `srom-scholarly.php` and recursed. Two implementations competing for one hook made the bug look like ours; several hypotheses about our own code were wrong.

Before concluding any live bug is in our code, enumerate what is actually deployed:

- `wp-content/mu-plugins/` — **every** `*.php` loads automatically and cannot be deactivated from wp-admin. Read anything you didn't write.
- `wp-content/plugins/` — active plugins (esp. anything also touching Elementor queries, ACF, or rewrites).
- Elementor → **Custom Code** snippets, and the theme's `functions.php`.
- Drop-ins (`object-cache.php`, `advanced-cache.php`).

And instrument rather than guess: the mu-plugin ships a shutdown-handler fatal logger (`wp-content/srom-fatal.log`, catches the non-catchable E_ERROR class), a `?srom_off=1` kill switch for its query filters, and `[srom_diag]`. The host's "error log" is often the ModSecurity/access log and contains **no** PHP errors — get `wp-content/debug.log` or the fatal logger instead.

## The canonical data contract (the coupling point — get this exactly right)

Templates and the mu-plugin bind by exact key. Three kinds of "field" exist and they are NOT interchangeable. The trap that bit every downstream builder: assuming a CSV column name is an article meta key. Most are not.

**Persisted ACF meta on `srom_article` — the ONLY real `get_field()` keys:**
`article_id`, `doi`, `title_en`, `authors_raw`, `authors_display`, `abstract_pl`, `abstract_en`, `keywords_pl`, `keywords_en`, `bio_note`, `pages_from`, `pages_to`, `language`, `license_url`, `pdf_file`, `flipbook_shortcode`, `is_translation`, `original_title`, `original_source`, `original_doi`, `volume`.

`flipbook_shortcode` is an optional per-article override: empty (the norm) → `[srom_flipbook]` builds the reader straight from `pdf_file`; set (e.g. `[dflip id="1198"]`) → that runs instead. `pages_from`/`pages_to` are plain text fields — Elementor's native `post-custom-field` tag reads them directly, so **there is no `[srom_pages]` shortcode** (it was removed; don't reintroduce it).

`volume` is a post_object field (`return_format: id`) — the article→Tom relation, returns the volume post's ID. Note the linked volume post ALSO has its own `volume` field holding the volume *number*; same name, different post type, do not conflate.

**Everything else a builder might reach for is NOT article meta:**

| Looks like a meta key | Actually | Read via |
|---|---|---|
| `seq` | core `menu_order` | `WP_Query orderby=menu_order` |
| `section_nr` / `section` | `dzial` taxonomy term — generic `Część I`…`Część IV`, slugs `czesc-i`…`czesc-iv` | `get_the_terms($id,'dzial')` / `tax_query` |
| `landing_url` | not stored — DOI-derived | `get_permalink($id)` — never store it; storing drifts from canonical |
| `doi_suffix` | the post slug | `get_post_field('post_name',$id)` |
| `year` (on the article) | `rocznik` taxonomy + linked Tom's `year` | `get_the_terms($id,'rocznik')` or traverse `volume`→Tom |

**Taxonomies on `srom_article`** (keys underscored; only `slowa_kluczowe` differs from its `slowa-kluczowe` URL slug): `dzial` (hierarchical, section), `slowa_kluczowe` (keywords), `autor` (authors), `rocznik` (year). `autor` terms come from comma-splitting `authors_display`.

**Volume post (`srom_volume`, label "Tom") meta:** `volume`, `year`, `signature`, `theme`, `pub_date`, `full_pdf`, `description`.

**Core WP fields that carry article data:** `post_title` ← `title_pl`; `post_name` ← `doi_suffix` (slug); `post_content` AND `post_excerpt` ← `abstract_pl` (mirrored so WP native search, which never indexes ACF meta, can find articles by abstract); `menu_order` ← `seq`.

## Master CSV schema (v3, 38 columns + optional `translators_struct`)

One row per article. Feeds three consumers from one cell each: `cover_page.py` (online cover pages; formerly planned as InDesign Data Merge) · Importer (WP posts) · Crossref generator (deposit XML). Full field reference: `references/master_schema.md`. Validate any master CSV before deposit with `scripts/validate_master.py`.

Column groups: identity (`article_id`, `doi_suffix`, `doi`, `landing_url`, `pdf_url`) · volume constants repeated per row (`journal_title`, `issn`, `volume`, `year`, `issue_signature`, `issue_theme`, `publisher`, `pub_date_online`) · ordering (`section_nr`, `section_label`, `seq`) · bibliographic (`title_pl`, `title_en`, `authors_display`, `authors_struct`, `affiliation_display`, `orcid_display`, `abstract_pl`, `abstract_en`, `keywords_pl`, `keywords_en`, `bio_note`, `pages`, `pages_from`, `pages_to`, `pdf_file`) · rights/provenance (`language`, `license`, `license_url`, `is_translation`, `original_title`, `original_source`, `original_doi`).

`authors_struct` is the structured author encoding, `Given|Surname|Affiliation|ORCID ;; Given|Surname|...` — this is what carries multi-author + per-author ORCID cleanly (e.g. Marushiakova + Popov). It is the source for the Crossref XML's per-contributor `<person_name>`/`<ORCID>` and, via the Importer, the mu-plugin's `authors_raw` (one author per line, pipe-delimited). Never flatten multiple authors into one field; ORCID is a per-contributor element, never a list. Constraint: no `|` or `;;` inside affiliation text.

`translators_struct` (optional, added 27.09.2026, last column): translators of a translated article (`is_translation` = `TAK`), same encoding as `authors_struct`. Kanon § 12.2.3 credits the translator in the article header. Crossref gets them as `<person_name contributor_role="translator">` after the authors. CSVs without the column stay valid. The Importer ignores it (no ACF field yet), and so does Data Merge (no header renamed).

CSV headers are all-English by decision. `cover_page.py` and the other scripts read columns by header name, so a header rename means changing them (and their tests) — flag this whenever proposing a schema change.

## Locked decisions (do not re-litigate; each was settled with rationale)

- **DOI suffix = opaque random `[a-z0-9]{8}`** (e.g. `ab3k9x2q`), generated separately. NOT human-readable. The readable `SROM-18-2025-001` string is `article_id`, an internal key only — different column, different job. Lowercase-only forever: DOIs are case-insensitive, URLs are not.
- **`article_id` format:** `SROM-{vol}-{year}-{NNN}`. Upsert key for the Importer; never appears in a URL or DOI.
- **Article URL:** `/articles/{full-doi}/` → `/articles/10.xxxxx/ab3k9x2q/`. The mu-plugin builds the permalink from each post's own `doi` field (so a future prefix change can't orphan old articles) and 301-redirects any non-canonical form. Slug = the 8-char suffix, frozen at import.
- **Volume URL:** `/tom/{vol}-{year}/` (`/tom/18-2025/`). Importer sets the slug explicitly to `{vol}-{year}` so the signature's middle dot (`·`, U+00B7) never percent-encodes into the URL. `/tom/` is deliberately kept distinct from the `rocznik` taxonomy archive at `/rocznik/` — one-letter-apart bases would be a routing footgun.
- **PDF path:** `/wp-content/uploads/archive/{vol}-{year}/SROM_{vol}_{year}_{Author_Shorttitle}.pdf`. (`/archive/`, not `/srom/` — "srom" is meaningless as a folder when the whole site is SROM.)
- **DOIs are article-level only.** The Crossref deposit carries the volume *number* in `<journal_issue><journal_volume>` for citation structure but registers no volume/issue-level DOI. No `volume_doi` field anywhere. (Adding issue-level DOIs later = one plugin field + one generator block; not on the roadmap.)
- **`section` and `doi_suffix` are not ACF fields.** Section is the `dzial` taxonomy; suffix is the slug. Both were removed after v1/v2.1.
- **Section terms are generic `Część I–IV`** (slugs `czesc-i`…`czesc-iv`), never theme-suffixed — the theme lives in the volume `theme` field / `issue_theme` column. So the CSV `section_label` is the bare `Część I`, one shared term per section across all volumes, which the mu-plugin's TOC filter can match by slug prefix. A theme-suffixed label would mint a per-volume term and break cross-volume matching (and re-break it on any re-import).
- **Article CPT rewrite slug = `articles`** (matches the `/articles/{full-doi}/` DOI landing base). On the live site this is a DB-native ACF record — change it by hand in ACF; plugin defaults only reach fresh installs.
- **`pdf_file` on the article is a plain-text URL**, not an attachment/file field — it is emitted verbatim as `citation_pdf_url`. Do not assume `wp_get_attachment_url()`.
- **`landing_url` is never persisted.** Always `get_permalink()`.
- **Crossref, not DataCite/HCommons.** Deposit schema **5.4.0** (5.3.1 also accepted).

## mu-plugin (`assets/srom-scholarly.php`)

Drop into `wp-content/mu-plugins/` (create the dir if absent) — always-on, cannot be accidentally deactivated. Requires the Importer plugin active (it registers the model). Registers no post types. Contents:

- **`SROM_DOI_PREFIX`** constant — set once to the real Crossref prefix after membership.
- **Rewrite rule** `articles/10\.[0-9]+/([a-z0-9-]+)/?$` → `post_type=srom_article&name=$1`, priority 20 (after the Importer). Targets post_type+name, not the CPT query var, so it is independent of the Importer's query-var config.
- **`post_type_link` filter** — builds the full-DOI permalink from the post's `doi`; falls back to `/articles/{slug}/` until a DOI is assigned.
- **`template_redirect`** — 301s any non-canonical article URL to the canonical.
- **`wp_head` @ priority 1** — Highwire `citation_*` tags + `ScholarlyArticle` JSON-LD, single-article pages only. Section sourced from the `dzial` taxonomy and surfaced as `articleSection`. `citation_pdf_url` MUST resolve directly to the PDF (HTTP 200, no redirect).
- **Shortcodes** (for Elementor Shortcode/Text widgets, because ACF dynamic tags read only the current post and can't traverse the article→volume relation or render on non-CPT contexts):
  - `[srom_doi]` — DOI as full clickable `https://doi.org/…` (Crossref display rule).
  - `[srom_cite]` — house-style citation, computed from fields (never stored → single source of truth). Style: `Imię Nazwisko, Tytuł [kursywa], „Studia Romologica", Rok, t. X, s. A–B. DOI: …`. Segments assemble conditionally (no dangling `t. , s. –.` for an unpaginated article).
  - `[srom_volume_field name="…" format="…"]` — volume metadata on the article template via the relation. Attribute is `name`; allowed: `volume`, `year`, `signature`, `theme`, `pub_date`. `format="F Y"` localises `pub_date` (→ "grudzień 2025"). Also works placed on the Tom template directly. Alias `[srom_issue_field]` kept for pre-v2.2 references.
  - `[srom_flipbook]` — on-screen PDF reader (DearFlip), served dynamically: uses `flipbook_shortcode` if set, else builds `[dflip source="…"]` from `pdf_file`. DearFlip **Lite** honours `source=` for same-origin PDFs; `height=` is PRO-only. The 0-width-collapse bug is a *layout* issue → set the widget's Align Self = Stretch.
  - `[srom_authors links="1" orcid="1"]` — full author block from `authors_raw`: per author a `.srom-author` with `.srom-author-name` (linked to the `autor` archive when the term exists), `.srom-author-aff`, `.srom-author-orcid`. Returns ONE composed block, not three addressable widgets — this is required for multi-author articles. Per-line styling = style the three CSS classes; do NOT split into per-value Elementor widgets (breaks on multi-author).
  - `[srom_diag]` — **temporary** admin-only diagnostic (context, volume-meta, dzial slugs, hook registration, missing-meta warnings, per-section self-test). Strip once an investigation is closed.

**Context resolution (v2.3):** every shortcode and query filter resolves the "current" post via `srom_ctx_id()`, which latches the real main-query object at `wp` and falls back to the set-up post — NOT bare `is_singular()`. Inside a Loop Grid item, the editor preview, or an admin-ajax widget re-render the global query is not the main query, so an `is_singular()` gate is false and the feature silently renders nothing. Any new reader must use `srom_ctx_id()`.

**Elementor Loop-Grid query filters** (the mu-plugin supplies what Elementor's query UI can't — the article→Tom relation and section scoping). Set the grid's **Query ID** via the current UI (Elementor Pro ≥4.2 stores it under `post_query_query_id`; a grid carrying only the legacy `query_query_id` is silently ignored). All callbacks are wrapped so an exception logs instead of white-screening, and guarded against re-entrancy (a filter that runs its own query re-enters `pre_get_posts` → stack-overflow fatal — the exact `srom-loops.php` incident):

| Query ID | Grid | Scopes to |
|---|---|---|
| `srom_contents_part1`…`_part4` | Volume › Spis treści, one per section | current Tom's articles in `dzial` `czesc-i`…`czesc-iv`, ordered by `menu_order` |
| `srom_other_articles` | Article › "W tym tomie" rail | sibling articles in the same Tom, current excluded |
| `srom_other_volumes` | Volume › "Inne roczniki" | other volumes, newest-first by `year`, current excluded |
| `srom_archive` | Volumes archive `/tomy/` | all volumes, newest-first by numeric `volume` meta, 24/page |

A grid ordered by a `meta_key` INNER-JOINs postmeta, so a volume missing that meta (`volume` for the archive, `year` for "Inne roczniki") silently drops out — fix the data, not the query; `[srom_diag]` counts them.

**Building/updating the mu-plugin:** edit `assets/srom-scholarly.php` directly; it is a standalone file with no build step. `php -l` to lint. After any change to CPT slug, taxonomy key, or ACF field name in the Importer, re-check the mu-plugin's `srom_article_meta()` and shortcodes for matching names. After deploying, always Settings → Permalinks → Save to flush rewrites.

## Crossref deposit (`scripts/generate_crossref_xml.py`)

CSV → deposit XML, schema 5.4.0, one file per volume. Fill the CONFIG block (depositor name/email, registrant) once. Emits: per-article `<journal_article>` with bilingual `<titles>`/JATS `<abstract>`, per-contributor `<person_name>`+`<ORCID>` (authors, then translators from `translators_struct` with `contributor_role="translator"`, `sequence="additional"`), `<pages>`, AccessIndicators license (`free_to_read` + `license_ref`), `isTranslationOf` relation when `original_doi` is present, and `<doi_data>` with the landing `<resource>` + crawler PDF item. References: `<citation_list>` from `volumes/<vol>/citations/<article_id>.json` (srom-produkcja build's `_citations.json`, Kanon § 13.1; DOI + unstructured text per entry; articles without one are named on screen). Affiliations: one `<institution>` per institution ("A; B", "A / B"), ROR ID from `volumes/ror.tsv` (`--ror <csv>` adds new institutions with ROR's confident match; check the file before a deposit). XSD-valid (5.4.0, 30.09.2026). Hard-aborts on: placeholder prefix `10.XXXXX`, non-`YYYY-MM-DD` `pub_date_online`, or any `doi_suffix` not matching `[a-z0-9]{8}`. Validate output at test.crossref.org before production.

## Pre-deposit invariants (`scripts/validate_master.py`)

Run against any master CSV before minting. Checks: 38-column schema present · DOI prefix filled (not `10.XXXXX`) · every `doi_suffix` is final opaque `[a-z0-9]{8}` and unique · `pub_date_online` is `YYYY-MM-DD` · `license`/`license_url` filled (no `TODO`) · `pages_from ≤ pages_to` · `authors_struct` parses and every ORCID is well-formed · slugs lowercase · translators: `translators_struct` segments are 4 pipe-fields (error), with a warning when `is_translation=TAK` has no translator or a translator is given without `TAK`. Reports blocking errors vs warnings.

## Deployment sequence (fresh volume)

1. Crossref membership → prefix + credentials (smallest tier ≈ $275/yr + $1/current DOI). Parallelizable with everything below.
2. Generate opaque suffixes: `scripts/mint_suffixes.py <csv> --prefix 10.NNNNN` (`--dry-run` first; replaces `todoNNNN` placeholders, unique across all volumes, fills `doi`/`landing_url`, never touches a final suffix). Fill `pub_date_online`, licenses, any `original_doi`. Run `validate_master.py` until clean.
3. mu-plugin in `mu-plugins/`; set `SROM_DOI_PREFIX`. Settings → Permalinks → Save.
4. Online PDF per article: `scripts/cover_page.py <csv> <article_id> <InDesign export, 165 × 235 mm, no marks> --out <dir>` (stops on any placeholder; names the file per `pdf_file`); upload to `/uploads/archive/{vol}-{year}/`. Never move/rename again.
5. Importer: dry-run the CSV, confirm taxonomy mappings resolve, then import (drafts).
6. Build/verify templates in Theme Builder (single `srom_article`/`srom_volume`) with a real imported post as preview. Verify one article: view-source shows `citation_*` tags; DOI renders as full `https://doi.org/…`; `curl -I` the PDF → 200, no 301.
7. Publish articles.
8. `generate_crossref_xml.py` → test.crossref.org → production. Await deposit report; click 2–3 DOIs to confirm resolution.
9. OpenAlex (the open index most discovery tools read) picks the journal up from Crossref by itself. 2–4 weeks after the first deposit: `https://api.openalex.org/sources?filter=issn:<ISSN>` (ISSN: knowledge base) must return the journal, and a DOI must show its references and abstract; if the journal record is wrong or missing, OpenAlex's support form fixes it.
10. Wikidata: the journal item once (`scripts/wikidata_qs.py journal` → QuickStatements, MB's account); after each deposit `wikidata_qs.py articles <csv> --journal Q… --check` for the article items.

Order dependency: suffixes freeze at import (step 5); everything before is reversible, nothing after deposit is.

## Roadmap / not-yet-built

In srom-kanon's `references/SROM_knowledge_base.md` § Roadmap. None of it changes the data contract above; treat it as downstream.

## Working style for this project

The human is a fast developer with a solid DOI grasp and communicates tersely — lead with conclusions, keep rationale terse-but-present, don't over-explain settled decisions. When a change spans surfaces, state which surfaces move and which stay, and prefer the most WordPress-native source (taxonomy/`menu_order`/`get_permalink()`) over adding stored fields — every added stored field is a second source of truth that can drift. Flag InDesign re-map cost on any header change. Keep design/CMS work in separate contexts from metadata/plugin work.
