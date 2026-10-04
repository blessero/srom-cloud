# Build report — tittel_pl

**RESULT: PASS — ready for InDesign**

- footnotes: 100 · citation keys used: 63 · bibliography sections: {'IV': 19, 'VI': 42, 'V': 2}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.16)
- Ibidem notes to check after layout: 17 (run tittel_pl_ibidem.jsx)
- DOI links (online PDF, not printed): 13 citations in notes, 4 bibliography entries, 4 works with a DOI (run tittel_pl_doi.jsx last, before the PDF export)

## Errors
- none

## Warnings (review)
- 13 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA: S1 – licencja CC BY 4.0 do potwierdzenia na  | DO SPRAWDZENIA: S2 – brzmienie pozycji kwestionariusza wedłu | DO SPRAWDZENIA: S3 – Röttgers, „Kant-Studien” 1997, s. 63: o | DO SPRAWDZENIA: S4 – Geulen, wykład (nagranie): „more racist | DO SPRAWDZENIA: S5 – przekład roboczy z niemieckiego (AA VII | DO SPRAWDZENIA: S6 – przekład roboczy z niemieckiego (AA II  | DO SPRAWDZENIA: S7 – „Hindusi”, „pariasi”: formy wydania pol | DO SPRAWDZENIA: S8 – przekład roboczy z niemieckiego (AA VII
- corrections of the author's data (approved; refs.json srom-as-written): decker2018: author “Decker” (as written) → corrected; vanbaar2019: title “The Securitization of the Roma in Europe. Human rights interventions” (as written) → corrected; ruch1986: note “unpublished dissertation” (as written) → corrected; breger2003: editor “Engbring-Romang; Strauss” (as written) → corrected; tomlins1811: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected; raithby1811a: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected; raithby1811b: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected
- missing data placeholders ['[BRAK WYDAWCY]'] in notes [20] — ask the author (kanon §0; see tittel_pl_pytania.md)
- query sheet tittel_pl_pytania.md: 25× odwołanie do całości dzieła (bez strony), 3× cytat bez numeru strony, 1× brak danych bibliograficznych, 1× tekst w sieci bez pełnej daty publikacji, 1× nota o przekładzie (S1), 11× cytat, 2× błąd w oryginale, 2× niejednoznaczność oryginału, 7× termin do rozstrzygnięcia, 2× pominięcie w przekładzie (§ 12.2.8) – do decyzji, 1× informacja
- asterisk series (kanon § 7.1): title note + 2 translator/editorial note(s) are paragraphs in 'Przypis GWIAZDKOWY' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run tittel_pl_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł': 6, 'Tekst BEZ WCIĘCIA': 5, 'Tekst': 35, 'Cytat': 6, 'Śródtytuł MAŁE': 3, 'Bibliografia': 63, 'Przypis GWIAZDKOWY': 4}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Gwiazdka': 2, 'Kursywa': 347, 'Kapitaliki': 72}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 100 / source 100
- [x] footnote paragraphs use footnote style only: {'Przypis': 100}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 2 / notes 2
- [x] asterisk notes at the end = notes + title note: 'Przypis GWIAZDKOWY' notes 3 / expected 2 + 1
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [x] no em dash: 0
- [x] no double spaces: 0
- [x] no ASCII ellipsis: 0
- [x] no English quotes “: 0

## Header data (not printed — set in InDesign; copy to the master CSV)
- translator(s), Kanon § 12.2.3: Michał Bartosz → `translators_struct`: `Michał|Bartosz||` (given name | surname split at the last space — check)

## Ibidem replaced by the short form at build time (§7.3)
- 26: Eberl twierdzi, że można dostrzec zmianę w stosunku Kanta do relacji z podróży: „Choć początkowo Kant bezkrytycznie ufał opisom obcych ludów i sądom o nich zawartym w tych relacjach z podróży i je przyjmował (1764), ostatecznie stał się […] wobec nich krytyczny (1785)” (Eberl, *Kant on Race*, s. 390). Opisuje on dalej, jak Kant w późnych pismach opierał się raczej na biologicznych wyjaśnieniach „rasy” niż na relacjach z podróży (Eberl, *Kant on Race*, s. 408).  — Ibidem inside a sentence
- 50: Marx, *Das Kapital…*, s. 746.  — previous note also cites another (literal) source
- 83: Oryginał: „Verordnung wegen Austreibung der Zigeuner”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 489.  — Ibidem inside a sentence
- 84: Oryginał: „dises Landschädliche Gesind außrotten helffen”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 490.  — Ibidem inside a sentence
- 85: Oryginał: „gänzlicher Ausrottung”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 822.  — Ibidem inside a sentence
- 86: Oryginał: „Zigeiner, Garttbrüder, Jauner und andern herrenlosen Gesindes”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 822.  — Ibidem inside a sentence
- 87: Oryginał: „dieses verdammliche Zigeiner-Gesind innerhalb Vierzehn Tag von Publication dieses offenen Patents den Creyß und gantz Schwaben raumen, dafern Sie aber nach Verfliessung solcher Zeit in demselben noch betretten würden, Sie Vogelfrey und Männiglich erlaubt seyn solle, dieselbe ohne Frevel und Verantwortung […] zu erlegen, zu spoliren, und nach Belieben zu hantieren”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 88: Oryginał: „todt geschossen”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 89: Oryginał: „nidergelegt”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 90: Oryginał: „ohne den wenigsten Anstandt todtschiessen”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 824.  — Ibidem inside a sentence
- 91: Oryginał: „in die härtiste Gefängnüssen geworffen”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 92: Oryginał: „wie Sie dann von dergleichen niemalhs rein seyn können”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 93: Oryginał: „biß die gantze Race von diesem Gesind in allen Theilen des Creyses extirpiert und auff den Grund außgerottet worden”, Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 824.  — Ibidem inside a sentence

## Ibidem map (note → form to use if it lands on a different column)
- 15: *Ibidem*, s. 73–75.  ⇒  Röttgers, *Kants Zigeuner*, s. 73–75.
- 16: *Ibidem*, s. 64.  ⇒  Röttgers, *Kants Zigeuner*, s. 64.
- 17: *Ibidem*. Choć Kraus nigdy sam nie opublikował wyników, Röttgers przedstawia jasne dowody, że pracował nad tym tematem (*Ibidem*, s. 64–75). Więcej o badaniu Krausa zob. K. Röttgers, *Kants Kollege und seine ungeschriebene Schrift über die Zigeuner*, Manutius, Heidelberg 1993.  ⇒  Röttgers, *Kants Zigeuner*, s. 64. Choć Kraus nigdy sam nie opublikował wyników, Röttgers przedstawia jasne dowody, że pracował nad tym tematem (Röttgers, *Kants Zigeuner*, s. 64–75). Więcej o badaniu Krausa zob. K. Röttgers, *Kants Kollege und seine ungeschriebene Schrift über die Zigeuner*, Manutius, Heidelberg 1993.
- 28: *Ibidem*, s. 84–85.  ⇒  Hund, *„It Must Come from Europe”*, s. 84–85.
- 30: Wśród nich znajdziemy filozofów Woltera i Hume’a. Zob. *Ibidem*, s. 101.  ⇒  Wśród nich znajdziemy filozofów Woltera i Hume’a. Zob. Larrimore, *Sublime Waste*, s. 101.
- 44: *Ibidem*, s. 209 / AA VIII 174.  ⇒  Kant, *Teleological Principles*, s. 209 / AA VIII 174.
- 51: *Ibidem*, s. 748–749.  ⇒  Marx, *Das Kapital…*, s. 748–749.
- 54: *Ibidem*, s. 762.  ⇒  Marx, *Das Kapital…*, s. 762.
- 66: Zob. *Ibidem*, s. 762–770.  ⇒  Zob. Marx, *Das Kapital…*, s. 762–770.
- 67: *Ibidem*, s. 764, przyp.  ⇒  Marx, *Das Kapital…*, s. 764, przyp.
- 68: *Ibidem*, s. 746.  ⇒  Marx, *Das Kapital…*, s. 746.
- 71: *Ibidem*, s. 724.  ⇒  Marx, *Das Kapital…*, s. 724.
- 73: *Ibidem*, s. 722.  ⇒  Marx, *Das Kapital…*, s. 722.
- 74: *Ibidem*, s. 723.  ⇒  Marx, *Das Kapital…*, s. 723.
- 75: *Ibidem*, s. 724.  ⇒  Marx, *Das Kapital…*, s. 724.
- 76: *Ibidem*.  ⇒  Marx, *Das Kapital…*, s. 724.
- 77: *Ibidem*, s. 724–725.  ⇒  Marx, *Das Kapital…*, s. 724–725.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/tittel_pl.txt
============================================================

--- WARN ---
133:195  [RANGE-SHORT] Elided range — write both numbers in full: s. 115–128, 1939–1945.
        … t. 3: From 1 Hen. VIII. A.D. 1509–10. – To 7 Edw. VI. A.D. 1553, G …
359:198  [RANGE-SHORT] Elided range — write both numbers in full: s. 115–128, 1939–1945.
        … t. 3: From 1 Hen. VIII. A.D. 1509–10. – To 7 Edw. VI. A.D. 1553, G …

--- counts (interpret by zone; RULES.md §J) ---
  apparatus_year_forms (1943 r.): 7
  prose_year_forms (1943 roku): 26
  apparatus_century_forms (XX w.): 3
  prose_century_forms (XX wieku): 19
  i_in: 1
  ibidem: 16
  ascii_apostrophe_inside_word (soft sign?): 0

Not checkable here:
  · Ibidem legality (same page) — proofs.
  · Short-title consistency; note↔bibliography coverage.
  · Metryczki anonymisation — editor's call.
  · Initials in notes / full names in bibliography.
  · Surnames must NOT be capitalised in the CSV.
  · Missing source data: flag it, never reconstruct.
```
