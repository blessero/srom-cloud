# Rules → implementation (srom-produkcja)

The rules are in the **srom-kanon** skill: `references/kanon-redakcyjny.md` (normative, Polish) and `RULES.md` (English
digest), same § numbers. This file does not restate them. It maps each rule the toolchain enforces to the code and the
test that prove it, lists conventions that belong to the toolchain only, and keeps the open items.

Decisions 1–19 of the earlier register (26.09.2026) were confirmed by the editor and moved into the Kanon (§ 17, row 1.6); their
old numbers are given in brackets for the record.

## Kanon rules → code → test

| Kanon § | rule (short) | implemented in | tested in |
|---|---|---|---|
| § 0 | `[BRAK MIEJSCA/ROKU/WYDAWCY]` printed, blocks the build unless `--draft` [16] | srom.csl, build.py | test_csl, test_e2e, test_check |
| § 2 | two heading levels; numbered lists `1.` + tab, own style [10] | srom_post.lua | test_e2e, test_docx_in |
| § 3.1–3.2, 3.5 | quotes, dashes, ranges, ellipsis | normalize.py | test_normalize |
| § 3.3 | no non-breaking spaces stored; stray nbsp → space [13]; GREP styles in the template | normalize.py, style_spec.json | test_normalize, test_jsx |
| § 3.4 | no bold/underline; reverse italics (title in an italic title set roman) [11] | srom_post.lua | test_e2e |
| § 4.1 | verse quotation keeps its line breaks [17] | srom_post.lua | test_e2e |
| § 5.3 | interlinear example: three styled lines, real tabs [17] | srom_post.lua | test_e2e, test_normalize |
| § 7.1 | marker before `. , ; :`, after an abbreviation's period [1] | normalize.py | test_normalize |
| § 7.1 | non-author notes (`– przyp. tłum./red.`, title note) = asterisk series, not numbered (E8) | srom_post.lua, build.py, check.py, JSX | test_e8, test_check |
| § 7.1 | author-date → footnote conversion [9] | cite_map.py | test_citemap |
| § 7.2 | first citation forms; physical-form note at the end | srom.csl | test_csl |
| § 7.2 | page-less citation never blocks; listed in the query sheet (quotation → author, whole work → editor) [7] | srom_post.lua, build.py | test_e2e |
| § 7.3 | short form; `title-short` with `…` [3]; multi-author short forms [2] | srom.csl | test_csl |
| § 7.3 | Ibidem only where unambiguous; short form otherwise [8]; same-column check after layout | build.py, `_ibidem.jsx` | test_e2e, test_jsx |
| § 7.3 | forbidden back-references (op. cit., tamże…) fail the build | srom-kanon linter via build.py | test_lint, test_docx_in |
| § 7.4 | multi-paragraph footnote kept, flagged [14] | srom_post.lua | test_e2e |
| § 8.6 | hyperlinks → plain text [12] | srom_post.lua, build.py (verification) | test_e2e |
| § 9.2 | only sections used, unnumbered, single section without heading [5] | build.py | test_e2e, test_csl |
| § 9.3 | small caps as character style; particles and institutional authors outside small caps [6] | srom_post.lua, build.py | test_e2e |
| § 9.5 | Polish collation | build.py | test_csl |
| § 9.7 | `ISBN 978-…` without colon [4]; missing ISBN listed | srom.csl, build.py | test_csl, test_e2e |
| § 10.1 | table title above, source below; cell/title/source styles [17] | srom_post.lua | test_e2e |
| § 12.2 | translation handoff (`handoff.md`), translator notes, added citations | check.py, cite_map.py | test_check, test_e2e |
| § 12.2.3 | translator = header data: front matter `tlumaczenie`, reported for the CSV, kept through Word (E10) | check.py, build.py, export_work.py, docx_in.py | test_e10 |
| § 3.4, § 6.3 | kartoteka: foreign exonyms italic (`italic_house`); structure | srom-kanon `references/kartoteka.tsv` | test_kanon |
| § 12.3 | spelling of 2026: -owski adjectives from personal names lowercase, nie + participle joined — WARN only (surnames, pronoun *nie*, quotations left to the editor) | srom-kanon linter (`ORTH-OWSKI`, `ORTH-NIE-IMIESLOW`, `PUNCT-SPOJNIK` — compound conjunctions, 30.09.2026) | test_lint |
| all | the srom-kanon linter runs on the rendered text; ERROR fails the build | build.py, kanon_path.py | test_lint, test_kanon |

## Toolchain conventions (not house rules)

| # | convention | where |
|---|---|---|
| [15] | Comments `<!-- … -->` never print and never block; in the Word working copy they are Word comments, dropped and listed on import. | build.py, export_work.py, docx_in.py |
| [18] | `@key` (author in text) and `[-@key]` (author suppressed) are forbidden: pandoc would print the first citation without its author. | srom_post.lua, check.py |
| [19] | The author's own reference list is taken out on import (`_bib.txt`); SROM prints only the bibliography generated from refs.json plus literal sections. | docx_in.py, pdf_extract.py |
| 20 | ✔ 27.09.2026 (MB-decisions D1): translation handoff (`handoff.md`): translator (`[^t<n>]`) and editorial (`[^r<n>]`) notes and the title note are outside the handoff check; an added citation passes only when declared; after translation the editor's Word working copy is the master. | check.py, export_work.py, docx_in.py |
| 22 | ✔ 27.09.2026 (MB-decisions D2): additions by the translation are declared by `"srom-added"` in `<id>_refs_tlum.json` (survives Word); `DODANO` comments still accepted. | check.py, cite_map.py |
| E8 | Asterisk notes leave the Word footnotes: in the text a placeholder `*` in character style *Gwiazdka* (v2: *Odsyłacz gwiazdkowy*); the notes as paragraphs in *Przypis GWIAZDKOWY* (v2: *Przypis gwiazdkowy*) at the end of the DOCX (title note first), each beginning `* `. The typesetter sets them above the numbered notes and the right number of asterisks per page (`_gwiazdki.jsx` lists them). | srom_post.lua, build.py |

## Open (○ = taken, not yet confirmed by the editor)

| # | item | where |
|---|---|---|
| 21 | ✔ 29.09.2026 (MB, style discussion; D3 closed): house style v3 — vol. 18's own values (body and notes must not move), new short names, 15 styles at the root by frequency, folders Rzadkie / Numer, the script purges and rebuilds (for a blank document). Cytat 9 pt on Tekst's H&J; two captions (with / without rule); long notes may split. Kanon § 3.4 vs italic speaker/affiliation: closed 29.09.2026 (MB, D21) — the no-italics rule governs the text, not display elements (Kanon § 3.4, § 17 row 1.8). | style_spec.json, srom_style_setup.jsx, test_jsx.py, tools/indesign_check |
| 23 | ✔ 28.09.2026 (MB, D19 A3): Kanon § 7.2/§ 9.4 — an edition of a source prints its editor after the title (`red.`); editor and translator the same people once (`tłum. i red.`); an unsigned text in a collection: the editors establish the author, else title first, the volume's editor after the volume title, and a query row. § 9.3/§ 9.5 — particles and compound surnames by the name's language (LC NAF): preposition particles as `dropping-particle`. | srom.csl, build.py (query row); test_csl.py, test_e2e.py |
| 24 | ✔ 02.10.2026 (MB, Ostendorf test in InDesign, Kanon v1.11): headings unnumbered (the build drops "1.", "1.2.", "IV." with a warning); one grid line before a heading and around a block quotation (styles, none between a quotation's own paragraphs); note number without a full stop (Footnote Options separator = en space); bibliography without a comma after the surname (CSL sort-separator); a range never broken at its dash (GREP rule in Tekst); the editor stands first only for an edited volume — an anonymous source edition (`type: classic`) and an edited article print it after the title; the DOCX styles carry the template's alignment (InDesign kept a missing one as a left-align override: every justified paragraph arrived ragged); every style the DOCX uses sits at the root of the panel ("Rzadkie" dissolved: the Word import does not look into folders and made its own Przypis GWIAZDKOWY) | srom.csl, srom_post.lua, build.py, style_spec.json, srom_postimport.jsx.tpl |
