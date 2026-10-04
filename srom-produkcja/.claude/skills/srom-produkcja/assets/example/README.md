# Example: INJECT build (stage 3) of a translated passage

Input: three paragraphs of the vol. 19 Ostendorf translation (`srom-produkcja/work/ostendorf/pl/ostendorf_pl.md`, the take-back of the delivered draft: paragraphs "Aby to pokazać…", "Rasa nie wyłoniła się…", "Choć transatlantyckie…"), with its translator front matter and title note, and the refs.json entries those paragraphs cite (16 works).

Expected: `build.py` prints `PASS`; the DOCX carries only named styles, real footnotes with first citations and short forms from the CSL, the title note as an asterisk note at the end, a Polish bibliography; the report (`_report.md`), the query sheet (`_pytania.md/.csv`), the bibliography for Crossref (`_citations.json`) and the InDesign scripts. `.txt` is the DOCX's text, the readable view of what InDesign will receive.

Command (run in this folder, `python3` with `srom-produkcja/requirements.txt` installed):

`python3 ../../scripts/build.py input/ostendorf_pl_wycinek.md --refs input/refs.json --out expected`

Produced by the command: expected/ostendorf_pl_wycinek.txt, expected/ostendorf_pl_wycinek_report.md, expected/ostendorf_pl_wycinek_pytania.md, expected/ostendorf_pl_wycinek_pytania.csv, expected/ostendorf_pl_wycinek_citations.json, expected/ostendorf_pl_wycinek_postimport.jsx, expected/ostendorf_pl_wycinek_ibidem.jsx, expected/ostendorf_pl_wycinek_gwiazdki.jsx, expected/ostendorf_pl_wycinek_doi.jsx, expected/ostendorf_pl_wycinek.docx
