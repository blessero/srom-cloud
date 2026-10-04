# Build report — ostendorf_pl

**RESULT: PASS — ready for InDesign**

- footnotes: 62 · citation keys used: 85 · bibliography sections: {'VI': 85}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/srom-produkcja/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.14)
- Ibidem notes to check after layout: 2 (run ostendorf_pl_ibidem.jsx)

## Errors
- none

## Warnings (review)
- 4 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA (pytania D1): przypis 25 cytuje „De Cadiz a V | DO SPRAWDZENIA (pytania D2): przypis 35 cytuje list Penna z  | DO SPRAWDZENIA: S1 – strona i brzmienie wydania polskiego (W | DO SPRAWDZENIA: S2 – strona i brzmienie wydania polskiego (M
- corrections of the author's data (approved; refs.json srom-as-written): matache2026: title “The Permanence of Anti-Roma Racism:(Un)uttered Sentences” (as written) → corrected; savic2022: note “Conference Paper presented at” (as written) → corrected; mangas2024: note “PhD diss.” (as written) → corrected; berquinduvallon1803: title “Vue de la colonie Espagnole du Mississipi, ou des provinces de Louisiane et Floride Occidentale,en l’année 1802” (as written) → corrected; cunniffe2023: note “PhD diss.” (as written) → corrected; jamaicalady1720: author “Anonymous” (as written) → corrected; wollon1952: title “Notes and Documents: Sir Augustus J. Foster and ‘the Wild Natives of the Woods,’ 1805–1807” (as written) → corrected
- heading number removed (kanon §2): 1. WSTĘP
- heading number removed (kanon §2): 2. ATLANTYK IBERYJSKI
- heading number removed (kanon §2): 3. ATLANTYK FRANCUSKI
- heading number removed (kanon §2): 4. ATLANTYK ANGLOSASKI
- heading number removed (kanon §2): 5. ZAKOŃCZENIE
- missing data placeholders ['[BRAK MIEJSCA]', '[BRAK WYDAWCY]'] in notes [1, 2, 11, 12, 15, 17, 18, 34, 36, 47, 48] — ask the author (kanon §0; see ostendorf_pl_pytania.md)
- query sheet ostendorf_pl_pytania.md: 14× odwołanie do całości dzieła (bez strony), 2× cytat bez numeru strony, 13× brak danych bibliograficznych, 1× tekst bez autora w tomie zbiorowym
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
- 18: *Ibidem*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993. [tłum. z przekładu angielskiego – przyp. tłum.]  ⇒  Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993. [tłum. z przekładu angielskiego – przyp. tłum.]
- 22: *Ibidem*; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.  ⇒  Herzog, *Defining Nations…*, s. 133; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build_inject/ostendorf_pl.txt
============================================================

--- WARN ---
285:374  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … ty, London 1893, s. 235–238. [tłum. z przekładu angielskiego – przyp. tłum.] Zapewne niepr …
287:121  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … [BRAK MIEJSCA] 1617, s. 39. [tłum. z przekładu angielskiego autorki – przyp. tłum.] Podob …
287:464  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … Society, DeLand 1932, s. 118 [tłum. z przekładu angielskiego – przyp. tłum.] …
295:166  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … 003, s. 129, 249, przyp. 36. [tłum. z przekładu angielskiego – przyp. tłum.] …
297:143  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … [BRAK MIEJSCA] 1999, s. 19. [tłum. z przekładu angielskiego autorki – przyp. tłum.] …
299:176  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … Press, [BRAK MIEJSCA] 1993. [tłum. z przekładu angielskiego – przyp. tłum.] …
305:42  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … , Defining Nations…, s. 133. [tłum. z przekładu angielskiego – przyp. tłum.] …
309:142  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … 83, 239, 303 i t. 2, s. 452. [tłum. z przekładu angielskiego autorki – przyp. tłum.] …
313:303  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … 1996, t. 101, nr 5, s. 1415. [tłum. z przekładu angielskiego – przyp. tłum.] …
321:164  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … , Archivo General de Indias. [tłum. z przekładu angielskiego autorki – przyp. tłum.] …
327:116  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … 02.1744, Huntington Library. [tłum. z przekładu angielskiego autorki – przyp. tłum.] …
329:175  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … hneuzeit-Info”, 2020, t. 31. [tłum. z przekładu angielskiego autorki – przyp. tłum.] …
347:138  [TLUM-ADNOTACJA] Annotation withdrawn: a quotation translated from the author's English needs none (§12.2.4 c) — remove it.
        … adelphia 1945, t. 2, s. 638. [tłum. z przekładu angielskiego – przyp. tłum.] …

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
