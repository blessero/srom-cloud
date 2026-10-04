# Build report — ostendorf_pl

**RESULT: PASS — ready for InDesign**

- footnotes: 62 · citation keys used: 85 · bibliography sections: {'VI': 85}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.16)
- Ibidem notes to check after layout: 2 (run ostendorf_pl_ibidem.jsx)
- DOI links (online PDF, not printed): 19 citations in notes, 17 bibliography entries, 17 works with a DOI (run ostendorf_pl_doi.jsx last, before the PDF export)

## Errors
- none

## Warnings (review)
- 4 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA (pytania D1): przypis 25 cytuje „De Cadiz a V | DO SPRAWDZENIA (pytania D2): przypis 35 cytuje list Penna z  | DO SPRAWDZENIA: S1 – strona i brzmienie wydania polskiego (W | DO SPRAWDZENIA: S2 – strona i brzmienie wydania polskiego (M
- corrections of the author's data (approved; refs.json srom-as-written): matache2026: title “The Permanence of Anti-Roma Racism:(Un)uttered Sentences” (as written) → corrected; savic2022: note “Conference Paper presented at” (as written) → corrected; mangas2024: note “PhD diss.” (as written) → corrected; berquinduvallon1803: title “Vue de la colonie Espagnole du Mississipi, ou des provinces de Louisiane et Floride Occidentale,en l’année 1802” (as written) → corrected; cunniffe2023: note “PhD diss.” (as written) → corrected; jamaicalady1720: author “Anonymous” (as written) → corrected; wollon1952: title “Notes and Documents: Sir Augustus J. Foster and ‘the Wild Natives of the Woods,’ 1805–1807” (as written) → corrected
- missing data placeholders ['[BRAK MIEJSCA]', '[BRAK WYDAWCY]'] in notes [1, 2, 11, 12, 15, 17, 18, 34, 36, 47, 48] — ask the author (kanon §0; see ostendorf_pl_pytania.md)
- query sheet ostendorf_pl_pytania.md: 14× odwołanie do całości dzieła (bez strony), 2× cytat bez numeru strony, 13× brak danych bibliograficznych, 1× tekst bez autora w tomie zbiorowym, 1× strona wydania polskiego (S1) – cytat do podmiany, 1× strona wydania polskiego (S2) – cytat do podmiany, 5× niejednoznaczność oryginału, 1× błąd w oryginale, 7× informacja, 1× termin do rozstrzygnięcia, 1× nazwa grupy do rozstrzygnięcia (§ 12.2.6), 1× pierwsze wystąpienie „Cyganie” (§ 12.2.6), 1× formuła przy cytacie (§ 12.2.4 c) – do decyzji
- asterisk series (kanon § 7.1): title note + 1 translator/editorial note(s) are paragraphs in 'Przypis GWIAZDKOWY' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run ostendorf_pl_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł': 6, 'Tekst BEZ WCIĘCIA': 5, 'Tekst': 33, 'Cytat': 1, 'Bibliografia': 85, 'Przypis GWIAZDKOWY': 2}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 307, 'Gwiazdka': 1, 'Kapitaliki': 76}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 62 / source 62
- [x] footnote paragraphs use footnote style only: {'Przypis': 62}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 1 / notes 1
- [x] asterisk notes at the end = notes + title note: 'Przypis GWIAZDKOWY' notes 2 / expected 1 + 1
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
- 18: *Ibidem*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993.  ⇒  Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993.
- 22: *Ibidem*; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.  ⇒  Herzog, *Defining Nations…*, s. 133; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/ostendorf_pl.txt
============================================================
No mechanical issues found.

--- counts (interpret by zone; RULES.md §J) ---
  apparatus_year_forms (1943 r.): 2
  prose_year_forms (1943 roku): 36
  apparatus_century_forms (XX w.): 1
  prose_century_forms (XX wieku): 7
  i_in: 0
  ibidem: 2
  ascii_apostrophe_inside_word (soft sign?): 0

Not checkable here:
  · Ibidem legality (same page) — proofs.
  · Short-title consistency; note↔bibliography coverage.
  · Metryczki anonymisation — editor's call.
  · Initials in notes / full names in bibliography.
  · Surnames must NOT be capitalised in the CSV.
  · Missing source data: flag it, never reconstruct.
```
