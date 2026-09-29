---
name: srom-typeset
description: Tested toolchain that turns an article for Studia Romologica (SROM) — a Polish Word file with footnotes, an author-date/Harvard manuscript, or a foreign-language PDF/DOCX — into a kanon-compliant Polish DOCX that imports into the SROM InDesign template with named paragraph/character styles and real footnotes (first citation / short form / Ibidem generated from CSL-JSON). For translated articles it prepares the frozen source and takes the translation back; the translating itself is srom-tlumacz's (separate chat). Use whenever an SROM article is imported from DOCX/PDF, converted from author-date to footnotes, keyed into refs.json, exported as a Word working copy or proof, checked for note/marker integrity or translation handoff, built, or placed in InDesign; also for "SROM-MD", "refs.json", "build.py", "Ibidem check", "import do InDesign", "skład SROM". Complements srom-kanon (rules), srom-tlumacz (translation) and srom-scholarly-curator (metadata).
---

# srom-typeset — from manuscript to InDesign

Priority order: **correct apparatus > nothing silently changed > speed.** Every step is a script with a
verdict line; nothing goes to InDesign unless `build.py` prints `PASS`. The house rules live in the
**srom-kanon** skill — `references/kanon-redakcyjny.md` (normative, Polish) and `RULES.md` (English digest), same
§ numbers; this skill implements them and cites them by §, never restates them. srom-kanon is **required**: the build
runs its linter and fails, saying so, if the skill is missing (looked up next to this skill, in `~/.claude/skills`, or
`$SROM_KANON`).

Scripts live in `scripts/` next to this file (`S=<skill dir>/scripts`). Requirements: pandoc ≥ 3.1,
Python ≥ 3.12 with python-docx, lxml, PyMuPDF. Where you run decides the rest:
- **Claude Code on the editor's Mac** — Python is the venv `~/.venvs/srom/bin/python` (the system
  `python3` is too old; wherever this file says `python3`, use the venv). Work in the article's own folder
  in the editor's project, never inside the skill directory. InDesign is installed locally.
- **claude.ai sandbox** — `python3`; work in `/home/claude/<article>/` and hand every intermediate file to
  the user (`present_files`) — the sandbox resets between sessions.

**Preflight, once per session (≈ 30 s):** `python3 <skill dir>/tests/run_all.py` → `SUITE ALL PASS 19/19`
(on the Mac it switches itself to the venv). A different pandoc version can change citeproc behaviour and
the DOCX reader; the tests are what proves the toolchain still does what this file says.

## The pipeline

| step | command | verdict | judgment needed (Claude / editor) |
|---|---|---|---|
| 1a DOCX in | `python3 $S/docx_in.py art.docx -o art.md` | `IMPORT OK/CHECK n` | `_import.md`: pending track changes, fake superscript notes, manual headings. The author's reference list goes to `art_bib.txt`; Zotero/Mendeley fields are harvested into `art_cited.md` + `art_refs.json`. Notes typed as text (superscript digits + numbered note paragraphs page by page, a PDF rip): add `--typed-notes` → real notes labelled with the source numbers; read every REPAIRED / GAP / LOST TEXT line against the PDF |
| 1b PDF in | `python3 $S/pdf_extract.py art.pdf -o src.md [--pages a-b]` | `EXTRACT OK/CHECK n` | `_extract.md`: hyphen joins, headings, verse, captions, retyped small caps, dropped lines; reference list → `src_bib.txt`; title/author/abstract → `src_front.md` (for the CSV) |
| 2 normalise | `python3 $S/normalize.py art.md -o art.md --log art_norm.md` | change log + flags | resolve every flag |
| 3 refs | Claude writes `refs.json` from `_bib.txt` (or completes `_refs.json`) per `references/srom-md.md` | `cite_map.py audit --refs refs.json --bib art_bib.txt` → `CITEMAP OK`; web texts: `lookup.py webdates refs.json --csv art_q.csv` | every PROBLEM line; publication dates found on the pages (fill in, § 8.6), undated pages → `"srom-undated": true` |
| 4a author-date | `python3 $S/cite_map.py scan art.md --refs refs.json --apply art_fn.md` | `CITEMAP OK/FAIL` | INFLECTED, TRIMMED, YEAR-ONLY, YEAR-UNIQUE, IN-NOTE, NOT-CITED?, YEAR-ONLY?, PAGE-ONLY rows; a citation of a work missing from the author's list: `lookup.py missing "Names" year --csv art_q.csv` (query to the author, never into refs.json until confirmed); `art_q.csv` goes to `build.py --queries` |
| 4b footnoted | Claude keys literal notes → `[@key, s. N]` (archival, fieldwork, laws stay literal) | `check.py --keyed art.md art_keyed.md --refs refs.json` → `CHECK OK` | — |
| 5 Word | `python3 $S/export_work.py art.md -o art_robocza.docx` → you edit in Word → `docx_in.py art_robocza.docx -o art.md` (lossless) | `IMPORT OK` | the Word file is the master once exported; proof: `build.py --proof` |
| 6 build | `python3 $S/build.py art.md --refs refs.json --out build/` | `PASS` / `FAIL` + `_report.md` | warnings; **`_pytania.md/.csv`** = the query sheet for author and editor |
| 7 InDesign | place DOCX with preset "SROM – pandoc", run `_postimport.jsx`, after layout `_ibidem.jsx` (and `_gwiazdki.jsx` if written) | `RESULT: OK` | per `references/indesign.md` |

Re-run step 2 after 4a/5 (normalize is idempotent). `check.py art.md --refs refs.json` can be run
at any time; `build.py` runs it itself.

## Scenarios

**A. Polish Word file, footnotes** — 1a → 2 → 3 → 4b → 6 → 7. If the author used Zotero/Mendeley, 1a has
already keyed the citations (`_cited.md`): complete `_refs.json`, run `--keyed art.md art_cited.md`, go on
from the `_cited` file. Keying by hand is the only non-deterministic step; `--keyed` proves no page,
note or work was lost. *Lite variant* for an article whose notes are already kanon-clean: skip 3–4,
keep notes literal, put the whole bibliography as literal sections in the `::: {#bibliografia}` block.
Styles, markers and linter are still enforced, but first/short/Ibidem sequence is then the author's
and nothing verifies it.

**B. Author-date manuscript** — 1a → 2 → 3 → 4a → 2 → 6 → 7 (Zotero/Mendeley: 1a already converted it).
`cite_map` never guesses a work: AMBIGUOUS/UNKNOWN/UNPARSED/PAGE-ONLY? block `--apply` until resolved or
explicitly released (`--allow-unknown`, `--allow-unparsed`); a page-only "(s. 21)" becomes a citation of the
work cited just before it and is listed.

**C. Translated article** — the translating is srom-tlumacz's, in its own chat; the contract is
`references/handoff.md`. Here: 1a/1b → 3 → 4a/4b **in the source language** (4a with `--apply <id>_src.md --renumber`:
note labels = printed numbers) → `check.py` → hand over
`<id>_src.md` + refs.json + `<id>_src_front.md` (+ working copy and `build.py --source` proof for you). Back:
`<id>_pl.md`, `<id>_refs_tlum.json` (the translation's added citations), `<id>_front_pl.md` (Polish title, abstract,
keywords: header data for the CSV, not built) → working copy → your edits in Word → `docx_in.py` →
`check.py --pair <id>_src.md <id>_pl.md --refs refs.json --refs <id>_refs_tlum.json` → 2 → 6 with both `--refs`,
`--pair-src <id>_src.md` and `--queries` (merges the translator's query rows) → 7. The translator's name is front matter `tlumaczenie:` (not printed; the build report
gives the `translators_struct` value for the master CSV). Never MarkItDown: it loses italics and note markers.

## What the build guarantees (tests: `tests/`)

- every paragraph and every italic/small-caps run carries a **named style** from `config/styles.json`
  (body, headings, quotes, verse, lists, tables, interlinear examples, bibliography, captions); no
  direct formatting, no Word footnote-reference style, no `w:lang`, no hyperlinks, tabs as real tabs
- first citation / short form / *Ibidem* computed by `csl/srom.csl` (kanon §7.2–7.3). *Ibidem* is
  replaced by the short form at build time wherever it would be ambiguous or ungrammatical (inside a
  sentence; next to a literal archival reference in the same or the preceding note); the rest are
  checked for "same column" by `_ibidem.jsx` after layout
- forbidden forms (op. cit., tamże, idem…) cannot come out of CSL, and the srom-kanon linter fails the
  build on any in literal notes
- bibliography sections I–VI assembled, empty ones omitted, renumbered, Polish collation, surnames
  (not particles, not institutions) in the small-caps character style
- the build **fails** on: unknown key, marker without note or orphan note, `@key` / `[-@key]`
  citations, missing bibliographic data `[BRAK MIEJSCA/ROKU/WYDAWCY]` (kanon §0; `--draft` for proofs
  only), heading level 3, numbered
  list, image in text, code block outside `::: przyklad`, literal and CSL entries in one bibliography
  section, an unconverted author-date reference to a work in refs.json, any kanon-linter ERROR, any
  DOCX verification failure
- editor comments `<!-- … -->` (PRZYWRÓCIĆ, DO SPRAWDZENIA …) **never** block (`handoff.md`): removed before
  building and listed as a warning in `_report.md`; in the Word working copy they are Word comments, dropped on
  import and listed in `_import.md`. Open items are tracked by whoever wrote them, not by the build
- non-author notes (kanon §7.1: title note, `– przyp. tłum.`, `– przyp. red.`) are **not** Word footnotes:
  a `*` in its character style at the marker, the notes (opening `* `, title note first) in their own style at
  the end of the DOCX, for the typesetter to set above the numbered notes; `_gwiazdki.jsx` gives the
  asterisks per page. They take no footnote number and no Ibidem; verified in the DOCX and after import
- a citation without a page **never** blocks: it is printed without placeholder and listed in the
  query sheet — "cytat bez numeru strony" (to the author) when it is the source of a quotation,
  "odwołanie do całości dzieła" (to the editor) otherwise. The sheet also lists missing ISBNs, long
  titles without a short form, and every `[BRAK …]` with its work.

## Hard rules

- Never invent bibliographic data. A missing field stays missing and produces `[BRAK …]`.
- Never hand-edit the DOCX. Fix the SROM-MD or refs.json and rebuild.
- Style names in `config/styles.json` must equal the template's names exactly; they are defined in
  `indesign/style_spec.json` (house style v3) and set up in InDesign by `srom_style_setup.jsx`.
- *Ibidem* legality depends on layout (same column): always run `_ibidem.jsx` on final pages.

## Tests

`python3 tests/run_all.py` after any change to the CSL, the Lua filter, config or scripts (and as the
session preflight). `test_pdf.py` needs LibreOffice to generate its PDF; `test_jsx.py` parses as strict
ES3 with acorn if installed (sandbox: `npm i acorn` in `/home/claude/es3`; Mac: `~/.venvs/srom/node`), otherwise with a weaker parser.

## House style in InDesign

`indesign/style_spec.json` (v3, 29.09.2026) is the one definition of the SROM styles: 29 paragraph styles
(15 at the root, most used first; folders "Rzadkie" and "Numer") and 8 character styles, with vol. 18's own
values (read from the templates in `dump/`), the document settings (baseline grid 13.2945 pt, Footnote Options)
and the map old style → new style. `python3 scripts/make_style_setup.py` renders `indesign/srom_style_setup.jsx`
(run on a blank document or a copy of an old one: purges every style, builds the house set, maps text in old
styles to the new ones, reads every value back) and `references/style-sheet.md`, and checks the config against
the spec. `tests/test_jsx.py` checks the spec against the vol. 18 IDMLs; `tools/indesign_check/indesign_check.py`
runs the script in InDesign itself and proves line for line that body and notes do not move. Several pipeline
roles share one style (config maps roles → names). v2 (the renaming script): `indesign/legacy/v2/`.

## References

- `references/srom-md.md` — SROM-MD format, citation syntax, refs.json field conventions, roles
- `references/handoff.md` — what goes to srom-tlumacz and what comes back; the handoff check
- `references/style-sheet.md` — the house style: every paragraph/character style, hierarchy and values
- `references/indesign.md` — Word-import preset, template requirements, post-import and Ibidem scripts, first-article verification
- `references/decisions.md` — Kanon rule → implementing file → test; toolchain-only conventions; open items
