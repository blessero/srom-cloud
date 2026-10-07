# Stages of a text — the stage-gate spec

The one specification of the pipeline. The other skills point here and do not restate it; the commands and their
options are in `SKILL.md` (srom-produkcja) and srom-tlumacz's `SKILL.md`. Paths are relative to the workspace root.

| # | Stage (MB's name) | Who | For |
|---|---|---|---|
| 1 | **RIP** — preprocessing | srom-produkcja | every text |
| 2 | **TRANS** — translation | srom-tlumacz | translated articles only (scenario C) |
| 3 | **INJECT** — post-translation formatting and build | srom-produkcja | every text |
| 4 | **InDesign import** — layout and PDF | MB, on his Mac (InDesign) | every text |

A Polish original goes 1 → 3 → 4: its RIP ends with the Word working copy, MB edits it, INJECT imports it again and
builds. A stage starts only when the previous one has passed. Every check prints a verdict line; a stage passes when
every line in its **Pass** row is printed (and the manual reads are done), and fails on any other outcome.

## 1. RIP — preprocessing (srom-produkcja, SKILL.md steps 1–5; scenario C up to the hand-over)

- **Input:** the author's PDF or DOCX, saved in `srom-produkcja/work/` (and the author's reference list, if separate).
- **Output** in `srom-produkcja/work/<id>/`: `<id>_src.md` (frozen SROM-MD, every reference a citation token, note
  labels = printed numbers), `refs.json`, `<id>_src_front.md` (the original's title, abstract, keywords),
  `<id>_src_robocza.docx` (Word copy for MB), `build/<id>_src_korekta.docx` and `build/<id>_src_pytania.md/.csv`
  (`build.py --source`: the proof and the query sheet), `<id>_uwagi.md` (notes sheet for MB), MB's questions in
  `MB-decisions.md`.
- **Pass:** `EXTRACT OK` / `IMPORT OK` (or `CHECK n` with every listed line read against the source) ·
  `cite_map.py audit` → `CITEMAP OK` · footnoted source: `check.py --keyed` → `CHECK OK` and `mutate_keyed.py` →
  `MUTATIONS CAUGHT n/n`; author-date source: `cite_map.py scan --apply` → `CITEMAP OK` · `check.py <id>_src.md --refs
  refs.json` → `CHECK OK` · `build.py --source` proof written, its report read.
- **Gate out (translated article):** the three files `<id>_src.md`, `refs.json`, `<id>_src_front.md` copied into
  `srom-tlumacz/work/<id>/src/` with a `manifest.sha256`, and a line in the hand-off log of `STATUS.md` with their
  sha256 (`first8…last7`). A later change to `refs.json` = a new log line and a new copy.
- **Fail:** fix the extraction, the keying or refs.json and re-run the failing check; doubts in the source go to the
  notes sheet, never corrected silently.

## 2. TRANS — translation (srom-tlumacz, its SKILL.md § The procedure)

- **Input:** `srom-tlumacz/work/<id>/src/`, identical to the last hand-off log line (`shasum -a 256 -c manifest.sha256`).
- **Output** in `srom-tlumacz/work/<id>/`: `<id>_intake.md`, `<id>_pl.md`, `<id>_front_pl.md`, `<id>_refs_tlum.json`
  (only if the translation adds citations), `<id>_pytania_tlum.csv`, `<id>_quotes.tsv`, `<id>_uwagi.md`,
  `<id>_robocza.docx` → MB edits it in Word; from his first edit **the Word file is the master**.
- **Pass (draft and every editing round):** manifest `OK` · `check.py --pair` → `CHECK OK` · `tlumacz-front_check.py` →
  `FRONT OK` · `build.py … --draft` → `PASS`, report "Errors: none", translator listed · `tlumacz-draft_check.py <id>` →
  `leftover 0, marks a=a` · the re-read against the source (manual, with counts of HOUSE terms).
- **Gate out (delivery, after MB's edit):** the master renamed `<id>_robocza.docx` (older exports `_old<n>`), imported
  (`docx_in.py` → `<id>_pl.md`), the Pass row re-run on the import, and a delivery line in the `STATUS.md` hand-off
  log with the sha256 of `<id>_robocza.docx`, `<id>_pl.md`, `<id>_front_pl.md` (and `<id>_refs_tlum.json`,
  `<id>_pytania_tlum.csv` when they exist) and of the `refs.json` checked against. A new round = a new line.
- **Fail:** corrections go into the Word master and the import is repeated; the md is never edited by hand.

## 3. INJECT — post-translation formatting and build (srom-produkcja, SKILL.md steps 6–8)

- **Input:** translated: the delivery in `srom-tlumacz/work/<id>/` as logged; Polish original: MB's edited
  `<id>_robocza.docx`, imported with `docx_in.py`.
- **Output:** `srom-produkcja/work/<id>/pl/` (copies of the delivery + `SHA256SUMS`, never edited) and
  `srom-produkcja/work/<id>/build/`: `<id>_pl.md` + `_norm.md` (`normalize.py` of the copy, written here), `<stem>.docx`, `_report.md`, `_pytania.md/.csv`, `_postimport.jsx`, `_ibidem.jsx`
  (+ `_gwiazdki.jsx`, `_doi.jsx` when written), `_citations.json` → copied to
  `srom-produkcja/volumes/<vol>/citations/<article_id>.json`; the article's row of the master CSV filled (Polish title,
  abstract, keywords from `<id>_front_pl.md`; `translators_struct` from the build report).
- **Pass:** `take_back.py … --expect <file>=<sha256> …` (one per logged file) → `TAKE-BACK OK <id>` · `normalize.py` of
  the copy into `build/` with no flag left · `build.py` on that file without `--draft` → `PASS` (no `[BRAK …]`, linter 0 ERROR, DOCX verified) · the CSV row: `validate_master.py` without blocking
  errors before any deposit (srom-quant).
- **Fail:** the report (or a normaliser flag) lists every error; note it in the notes sheet and fix it in the Word
  master (or refs.json, with a new hand-off line), never in the md or the DOCX; deliver and take back again.

## 4. InDesign import — layout and PDF (MB, on his Mac; `references/indesign.md`)

- **Input:** `build/<stem>.docx` and its `.jsx` scripts, the template `indesign/SROM_szablon_v3.idml` (saved as .indt),
  the Word-import preset "SROM – pandoc". The scripts reach InDesign's Scripts Panel with
  `sh tools/install_scripts.sh <build dir>` (this repository, Mac only).
- **Output:** the laid-out article; the PDF with bookmarks and invisible DOI links; PDF metadata from srom-quant's
  `pdf_metadata.py` (`<article_id>_metadane.jsx`, run before the export).
- **Pass:** `_postimport.jsx` → `RESULT: OK — import is clean` · after layout `_ibidem.jsx` and `_gwiazdki.jsx` report
  and fix · `srom_final_pass.jsx` → `RESULT: OK` (Kanon § 3.6) · right before the export `srom_zakladki.jsx`, then
  `_doi.jsx` (export with Bookmarks and Hyperlinks ticked).
- **Fail:** a style or import problem goes back to stage 3 (template names, the build), never patched by hand in a way
  the next build would lose.

After stage 4 the volume goes to publication: srom-quant (suffixes, `validate_master.py`, the website importer, the
Crossref deposit).

## The hand-off log (`STATUS.md` at the workspace root)

One table, appended, never rewritten; times from `date '+%d.%m.%Y %H:%M'`:

| when | text | what | files and sha256 (`first8…last7`) | verdicts |
|---|---|---|---|---|
| dd.mm.yyyy HH:MM | [Author] | RIP → TRANS / TRANS → INJECT (delivery) / refs.json changed | … | CHECK OK, FRONT OK, PASS … |

`take_back.py --expect` takes its values from the last delivery line of the text.
