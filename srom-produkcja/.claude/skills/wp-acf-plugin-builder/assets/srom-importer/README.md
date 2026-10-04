# SROM Importer

Reliable spreadsheet importer (CSV / TSV / XLSX) for the *Studia Romologica* content model — and any other ACF-powered post type. It registers the journal's post types, taxonomies and field groups as **native, editable ACF records**, then imports the master spreadsheet into them. Nothing is written without a completed dry-run preview, every row is matched by a key so re-running updates instead of duplicating, and one bad cell never stops the run.

Requires **Advanced Custom Fields** (the free version is enough).

## What it sets up (ACF-native)

On activation the plugin creates — as real ACF records you can open and edit under **Custom Fields → Post Types / Taxonomies / Field Groups** — the following:

| Item | Type | Notes |
|---|---|---|
| **Artykuł** (`srom_article`) | Post type | Field group with all article fields |
| **Tom** (`srom_volume`) | Post type | Field group: volume, year, signature, theme, pub_date, full_pdf, description |
| **Dział** (`dzial`) | Taxonomy (hierarchical) | On-site filtering by department; filled from `section_label` |
| **Słowa kluczowe** (`slowa_kluczowe`) | Taxonomy (flat tags) | Filled from `keywords_pl` |
| **Autor** (`autor`) | Taxonomy (flat tags) | One term per author; filled from `authors_display` |
| **Rocznik** (`rocznik`) | Taxonomy (flat tags) | One term per year; filled from `year` |

Because these are ordinary ACF records, everything works exactly as if you had built them by hand in ACF: Elementor single/archive templates and dynamic tags, REST/Gutenberg, admin sort/filter columns, adding your own fields or taxonomies, etc. Edit or extend them freely — the importer reads whatever ACF reports.

`keywords_en` stays a plain text field but is stored as **semicolon-separated discrete terms**, so a future English keyword taxonomy is a clean split-and-import job. (The former flat `section` select is intentionally gone — its role is now the hierarchical **Dział** taxonomy. There is likewise no `doi_suffix` field: the suffix *is* the post slug, and the full DOI lives in `doi`.)

The Polish abstract is written to the ACF `abstract_pl` field **and** mirrored into `post_content` / `post_excerpt`. That duplication is deliberate: WordPress' native search indexes the title, content and excerpt but never ACF meta, so without the mirror the site's own search cannot find an article by its abstract. `abstract_pl` remains the canonical source for citation metadata, and both copies are rewritten from the same CSV cell on every import, so they cannot drift.

Upgrading the plugin creates any definitions a new version introduces (never overwriting records you've edited); if you deliberately removed the definitions, an upgrade leaves them removed.

### Setup & status tab

*Tools → SROM Importer → Setup & status* shows each definition's state (in ACF / editable / live) with a direct "Edit in ACF" link, plus:

- **Create / complete** — creates anything missing; never overwrites items you've edited.
- **Reset to plugin defaults** — overwrites the definitions back to the shipped defaults (your articles/volumes and their data are untouched).
- **Remove definitions** — deletes just the ACF definitions; your posts and field values remain in the database.

## Import workflow

*Tools → SROM Importer*:

1. **Upload** the spreadsheet, choose the post type (`srom_article` for the master sheet).
2. **Check the mapping.** Columns with the same name as a field map automatically; the SROM specials are pre-configured:
   - `title_pl` → post title, `doi_suffix` → slug, `seq` → menu order
   - `authors_struct` → `authors_raw` (multiple authors split on `;;`, one per line)
   - `pdf_url` → `pdf_file` (the field wants the URL, not the bare file name)
   - `issue_signature` → `volume` (post object → the linked Tom)
   - `keywords_pl` → the **Słowa kluczowe** taxonomy *and* the `keywords_pl` field
   - `section_label` → the **Dział** taxonomy
   - `authors_display` → the **Autor** taxonomy (one term per author, comma-split)
   - `year` → the **Rocznik** taxonomy
   - `abstract_pl` → the `abstract_pl` field *and* `post_content` + `post_excerpt`
   - `keywords_en` → `keywords_en` field, normalised to `a; b; c`
   - Unmapped columns (`journal_title`, `issn`, `landing_url`, …) are ignored.
3. **Run the preview.** Processes every row without writing anything, listing exactly what would happen (including notes like “`2025-12-TODO` is not a recognizable date — field skipped” and “will create N new terms”).
4. **Import.** New posts are created as drafts by default. Missing volumes (Tomy) are created once from the volume columns and every article is linked to them via its `volume` relationship field; new taxonomy terms are created (toggle in options).

## Safety properties

- **Dry run first** — the import button only unlocks after a completed preview.
- **Upsert by key** (`article_id` / `signature`): re-importing the same or a corrected file updates existing posts; nothing is duplicated. Taxonomy terms are matched/created idempotently, never doubled.
- **Row isolation** — a broken row is logged and skipped; the rest of the file imports.
- **Field isolation** — an invalid value (bad date, unknown choice, non-number) skips that one field with a note; the rest of the row imports.
- **Batched processing** — small server-side batches with progress; a timeout can't corrupt a run, and an interrupted run resumes from the exact row.
- **Tolerant parsing** — UTF-8/UTF-16/Windows-1250, BOMs, comma/semicolon/tab delimiters, quoted multi-line cells, Excel date serials, empty rows, repeated headers, ghost columns.
- Everything runs under `manage_options` with nonces; uploads live in a protected folder and are garbage-collected after 48 h.

## Field value formats

| Field type | Accepted values |
|---|---|
| date | `2025-12-31`, `31.12.2025`, `31/12/2025`, Excel date cells |
| yes/no | `1/0`, `tak/nie`, `yes/no`, `true/false` |
| select / radio / checkbox | stored value (`I`) or visible label |
| taxonomy | term names or slugs; several separated by `;`, commas or new lines; hierarchical `Parent > Child` |
| post object / relationship | post ID, exact title, slug — for volumes also the signature (`SROM·18·2025`) |
| file / image / gallery | attachment ID, media-library file name, or URL (downloading is opt-in) |
| number | `11` or `11,5` |

## Uninstalling

Deleting the plugin removes its own options and temporary upload files. It **does not** delete the ACF post types/taxonomies/field groups or any imported content — remove those first via the Setup tab if you really want them gone. Repeater / flexible-content / group fields (ACF Pro layouts) can't be imported from a flat spreadsheet and are listed as such in the mapping screen.
