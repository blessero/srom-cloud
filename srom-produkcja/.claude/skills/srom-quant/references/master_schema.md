# SROM master CSV — column reference (v3, 38 columns + 1 optional)

One row per article. All-English headers (the scripts read columns by header name — a rename means changing them). Encoding UTF-8 with BOM. Consumers: `cover_page.py` (online cover page) · Importer plugin · `generate_crossref_xml.py`.

Legend for **Consumed by**: **X**=Crossref XML · **W**=WordPress via Importer · **D**=online cover page (`cover_page.py`; was InDesign Data Merge) · **—**=reference/derivation only.

| # | Column | Consumed by | Goes to / meaning |
|---|---|---|---|
| 1 | `article_id` | W | Importer upsert key. `SROM-{vol}-{year}-{NNN}`. Internal only — never a URL/DOI. |
| 2 | `doi_suffix` | W, X | Opaque random `[a-z0-9]{8}`. Becomes the post slug. |
| 3 | `doi` | X | Full DOI `{prefix}/{suffix}`. mu-plugin builds the permalink from this. |
| 4 | `landing_url` | — | `/articles/{doi}/`. Reference only; WP derives via `get_permalink()`. Ignored by Importer. |
| 5 | `pdf_url` | X, W | Full public PDF URL → ACF `pdf_file` and Crossref crawler resource. |
| 6 | `journal_title` | X | Constant: `Studia Romologica`. |
| 7 | `issn` | X | Constant: `1689-4758`. |
| 8 | `volume` | X, W | Volume number. |
| 9 | `year` | X, W | Publication year → also `rocznik` taxonomy. |
| 10 | `issue_signature` | W | `SROM·18·2025`. Resolves the article→Tom link by the Tom's `signature`. CSV keeps the `issue_` name for back-compat. |
| 11 | `issue_theme` | D | Volume theme (cover pages). |
| 12 | `publisher` | X | Registrant/publisher string. |
| 13 | `pub_date_online` | X | `YYYY-MM-DD`. Online publication date for the deposit. |
| 14 | `section_nr` | — | `I`/`II`/`III`/`IV`. Ordering reference; NOT stored (section = `dzial` taxonomy from `section_label`). |
| 15 | `section_label` | W | **Generic** section name → `dzial` taxonomy term: `Część I`…`Część IV` (slugs `czesc-i`…`czesc-iv`). **NOT** theme-suffixed — the theme lives in `issue_theme` (#11), never here. This was locked (decision #4): a theme-suffixed label like "Część I – Romski Atlantyk" makes every volume mint its own term, so the mu-plugin's TOC filter can't match across volumes, and it re-creates the wrong term on re-import. `Parent > Child` still supported for genuine hierarchy. |
| 16 | `seq` | W | Order within volume → core `menu_order`. |
| 17 | `title_pl` | X, W, D | Polish title → post title + `citation_title`. |
| 18 | `title_en` | X, W, D | English title → ACF `title_en`; Crossref `original_language_title` for translations. |
| 19 | `authors_display` | W, D | Authors exactly as printed → ACF `authors_display` + `autor` taxonomy (comma-split). |
| 20 | `authors_struct` | X, W | Structured: `Given\|Surname\|Affiliation\|ORCID ;; …`. Source for per-contributor Crossref `<person_name>`/`<ORCID>` and mu-plugin `authors_raw`. No `\|`/`;;` inside affiliations. |
| 21 | `affiliation_display` | D | Flat affiliation string for cover pages. |
| 22 | `orcid_display` | D | Flat ORCID string for cover pages. |
| 23 | `abstract_pl` | X, W, D | Polish abstract → ACF `abstract_pl` + mirrored to `post_content`/`post_excerpt` (search). |
| 24 | `abstract_en` | X, W, D | English abstract → ACF + JATS `<abstract xml:lang="en">`. |
| 25 | `keywords_pl` | X, W | Comma-separated → ACF `keywords_pl` + `slowa_kluczowe` taxonomy. |
| 26 | `keywords_en` | W | `; `-separated discrete terms → ACF `keywords_en` (forward-compatible with a future EN taxonomy). |
| 27 | `bio_note` | W, D | Author bio note. |
| 28 | `pages` | D | Human range `11–50` for cover pages. |
| 29 | `pages_from` | X, W | First page (machine). |
| 30 | `pages_to` | X, W | Last page (machine). |
| 31 | `pdf_file` | D | Bare PDF filename (cover-page reference). NOTE: the Importer's `pdf_file` ACF field is fed from `pdf_url` (#5), not this column. |
| 32 | `language` | X, W | Primary language, default `pl`. |
| 33 | `license` | — | Short license code (`CC-BY`), drives `license_url`. |
| 34 | `license_url` | X, W | Full CC URL → ACF + Crossref AccessIndicators `license_ref`. |
| 35 | `is_translation` | X, W | `TAK`/`ADAPTACJA`/empty. Translations get `original_language_title`. |
| 36 | `original_title` | X, W | Original title of a translated work. |
| 37 | `original_source` | W | Original source citation. |
| 38 | `original_doi` | X, W | Original work's DOI → Crossref `isTranslationOf` relation when present. |
| 39 | `translators_struct` | X | **Optional** (added 27.09.2026). Translator(s) of a translated work, same encoding as `authors_struct`: `Given\|Surname\|Affiliation\|ORCID ;; …`. → Crossref `<person_name contributor_role="translator">`, after the authors. Not imported to WP (the Importer ignores unknown columns) and not bound in Data Merge. `validate_master.py` warns when `is_translation`=`TAK` and it is empty. |
| 40 | `pub_date_print` | — | Required (07.10.2026). `YYYY-MM-DD`, print publication date; cover page "Data publikacji". |
| 41 | `editorial_period` | — | Optional (MB 08.10.2026, vol. 18: left empty). Printed as written, e.g. `marzec 2026 – czerwiec 2026`; cover page "Okres redakcji"; when empty the cover page leaves the item out (validate_master warns). |

## Volume (Tom) sheet — if importing volumes separately

Columns map to the `srom_volume` group: `volume`, `year`, `signature` (upsert key), `theme`, `pub_date` (`Y-m-d`), plus `full_pdf` and `description` set in WP. In the article sheet the volume constants (#6–13) are repeated per row; the Importer resolves/creates the Tom by `signature`.

## Change protocol

Any header change → note which scripts read the column (`cover_page.py`, `pdf_metadata.py`, the Crossref generator) and change them with their tests. Any new column that should become article meta → confirm it belongs in ACF (persisted) vs a taxonomy vs derived, per the contract in SKILL.md; default away from adding stored fields that duplicate a taxonomy or core field.
