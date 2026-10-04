# Build report — ostendorf_pl_wycinek

**RESULT: PASS — ready for InDesign**

- footnotes: 7 · citation keys used: 16 · bibliography sections: {'VI': 16}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter <skills>/srom-kanon/scripts/lint_srom.py (Kanon v1.16)
- Ibidem notes to check after layout: 0 (run ostendorf_pl_wycinek_ibidem.jsx)
- DOI links (online PDF, not printed): 4 citations in notes, 4 bibliography entries, 4 works with a DOI (run ostendorf_pl_wycinek_doi.jsx last, before the PDF export)

## Errors
- none

## Warnings (review)
- query sheet ostendorf_pl_wycinek_pytania.md: 5× odwołanie do całości dzieła (bez strony)
- asterisk series (kanon § 7.1): title note + 0 translator/editorial note(s) are paragraphs in 'Przypis GWIAZDKOWY' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run ostendorf_pl_wycinek_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Tekst BEZ WCIĘCIA': 1, 'Tekst': 2, 'Śródtytuł': 1, 'Bibliografia': 16, 'Przypis GWIAZDKOWY': 1}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 49, 'Kapitaliki': 17}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 7 / source 7
- [x] footnote paragraphs use footnote style only: {'Przypis': 7}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 0 / notes 0
- [x] asterisk notes at the end = notes + title note: 'Przypis GWIAZDKOWY' notes 1 / expected 0 + 1
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [x] no em dash: 0
- [x] no double spaces: 0
- [x] no ASCII ellipsis: 0
- [x] no English quotes “: 0

## Header data (not printed — set in InDesign; copy to the master CSV)
- translator(s), Kanon § 12.2.3: Michał Bartosz → `translators_struct`: `Michał|Bartosz||` (given name | surname split at the last space — check)

## Ibidem replaced by the short form at build time (§7.3)
- none

## Ibidem map (note → form to use if it lands on a different column)
- none

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — expected/ostendorf_pl_wycinek.txt
============================================================
No mechanical issues found.

--- counts (interpret by zone; RULES.md §J) ---
  apparatus_year_forms (1943 r.): 0
  prose_year_forms (1943 roku): 0
  apparatus_century_forms (XX w.): 0
  prose_century_forms (XX wieku): 1
  i_in: 0
  ibidem: 0
  ascii_apostrophe_inside_word (soft sign?): 0

Not checkable here:
  · Ibidem legality (same page) — proofs.
  · Short-title consistency; note↔bibliography coverage.
  · Metryczki anonymisation — editor's call.
  · Initials in notes / full names in bibliography.
  · Surnames must NOT be capitalised in the CSV.
  · Missing source data: flag it, never reconstruct.
```
