# Build report — ndiaye_pl

**RESULT: PASS — ready for InDesign**

- footnotes: 133 · citation keys used: 81 · bibliography sections: {'VI': 85, 'V': 1}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.16)
- Ibidem notes to check after layout: 30 (run ndiaye_pl_ibidem.jsx)
- DOI links (online PDF, not printed): 1 citations in notes, 1 bibliography entries, 1 works with a DOI (run ndiaye_pl_doi.jsx last, before the PDF export)

## Errors
- none

## Warnings (review)
- 7 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA: S1 – cytat z Chorego z urojenia w przekładzi | DO SPRAWDZENIA: S2 – strona wydania polskiego (Szelmostwa Sk | DO SPRAWDZENIA: S3 – strona wydania polskiego (akt I: „małe  | DO SPRAWDZENIA: S4 – strona wydania polskiego (akt I: „trzy  | DO SPRAWDZENIA: S5 – strona wydania polskiego (akt III, scen | DO SPRAWDZENIA: S6 – strona wydania polskiego (akt II, Skape | DO SPRAWDZENIA: S7 – cytat z Cathy Park Hong według wydania 
- integrity: parenthesis with a name and a year — a citation? (name not in refs): (Antony and Cleopatra, 1607)
- integrity: parenthesis with a name and a year — a citation? (name not in refs): (L’étourdi, 1655)
- corrections of the author's data (approved; refs.json srom-as-written): admant2015: publisher-place “Droit” (as written) → corrected; vanlennep1965: editor “Van Lannep” (as written) → corrected
- printed though not cited in the notes (the author's bibliography, Kanon § 9.2): ['cervantes1617', 'crooks1931', 'galland2017', 'netzloff2003', 'ravenscroft1678']
- query sheet ndiaye_pl_pytania.md: 17× odwołanie do całości dzieła (bez strony), 4× cytat bez numeru strony, 24× długi tytuł bez formy skróconej (title-short), 1× tekst w sieci bez pełnej daty publikacji, 1× strona wydania polskiego (S1) – cytat do podmiany, 1× strona wydania polskiego (S2), 1× strona wydania polskiego (S3), 1× strona wydania polskiego (S4), 1× strona wydania polskiego (S5), 1× strona wydania polskiego (S6), 1× strona i brzmienie wydania polskiego (S7), 1× wybór wydania Boya, 1× dane pierwodruku – brak numeru zeszytu, 2× rozbieżność daty, 2× informacja, 1× słowa kluczowe do zatwierdzenia
- asterisk series (kanon § 7.1): title note + 2 translator/editorial note(s) are paragraphs in 'Przypis GWIAZDKOWY' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run ndiaye_pl_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł': 8, 'Tekst BEZ WCIĘCIA': 7, 'Cytat': 4, 'Tekst': 44, 'Cytat WIERSZ': 5, 'Podpis': 3, 'Śródtytuł MAŁE': 2, 'Bibliografia': 86, 'Przypis GWIAZDKOWY': 4}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 458, 'Gwiazdka': 2, 'Kapitaliki': 87}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 133 / source 133
- [x] footnote paragraphs use footnote style only: {'Przypis': 133}
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
- 42: „Wolę termin »alienacja natalna«, ponieważ trafia on wprost w sedno tego, co w wymuszonej alienacji niewolnika najistotniejsze: w utratę więzów urodzenia zarówno w pokoleniach wstępnych, jak i zstępnych. Niesie on też ważny odcień utraty statusu rodzimego, wykorzenienia. To właśnie ta alienacja niewolnika od wszelkich formalnych, prawnie egzekwowalnych więzów »krwi« i od wszelkiej przynależności do grup czy miejsc innych niż te, które wybrał dla niego pan, nadawała relacji niewolnictwa jej szczególną wartość dla pana”: O. Patterson, *Slavery and Social Death: A Comparative Study*, Harvard University Press, Cambridge, MA 1982, s. 7. „Śmierć społeczna” jest „zewnętrzną koncepcją” tej alienacji natalnej: Patterson, *Slavery and Social Death: A Comparative Study*, s. 8.  — Ibidem inside a sentence
- 64: K. Dauge-Roth, *Signing the Body: Marks on Skin in Early Modern France*, Routledge, New York 2019, s. 224. Dauge-Roth podkreśla podobieństwa między piętnowaniem galerników a piętnowaniem zniewolonych ludzi afrodiasporycznych we francuskich koloniach: w obu przypadkach piętno oznaczało urasowione ciało jako własność króla lub białego pana. Dauge-Roth, *Signing the Body: Marks on Skin in Early Modern France*, s. 220–225.  — Ibidem inside a sentence
- 78: Hitchcock, *Vagrancy in English Culture and Society, 1650–1750*, s. 5.  — previous note also cites another (literal) source
- 82: G. Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles […] and translated into English by R. C. […]*, Printed for W. Gilbertson, London 1662, k. S2r. Choć Theodorus, „pan”, regularnie nazywa Bannacara w angielskiej wersji sztuki Ruggle’a swoim „sługą”, zostaje on przeciwstawiony poprzedniemu panu Bannacara, Alfonsowi, właścicielowi niewolników, który wyzwolił go w chwili swojej śmierci. Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles […] and translated into English by R. C. […]*, k. S4r.  — Ibidem inside a sentence
- 83: Ravenscroft postanowił także wyciąć ze sztuki Ruggle’a sprośną scenę z udziałem kobiet świadczących usługi seksualne różnych narodowości, w tym czarnoskórej Maurki: Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles […] and translated into English by R. C. […]*, k. D4r. Sztuka ta nie zwróciła dotąd uwagi badaczy rasy we wczesnej nowożytności.  — Ibidem inside a sentence
- 107: „Cicho, bo nauczę waszą cygańskość trochę manier”: M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 60.  — Ibidem inside a sentence

## Ibidem map (note → form to use if it lands on a different column)
- 7: *Ibidem*, s. 23–24. Zob. też Y. Matras, *I Met Lucky People: The Story of the Romany Gypsies*, Penguin Books, London 2014, s. 131.  ⇒  Chang, Rucker-Chang, *Roma Rights and Civil Rights: A Transatlantic Comparison*, s. 23–24. Zob. też Y. Matras, *I Met Lucky People: The Story of the Romany Gypsies*, Penguin Books, London 2014, s. 131.
- 18: *Ibidem*, s. 393. Choć wyrażenie „Mały Egipt”, używane w wielu innych źródłach wczesnonowożytnych, rozumie się często jako odnoszące się do jakiejś części Egiptu, niektórzy romolodzy, jak Yaron Matras, uznają je za nazwę portu Modon na Peloponezie w Grecji, który był „ważną stacją na szlaku morskim z Wenecji do Jafy, a pielgrzymi zmierzający do Ziemi Świętej zatrzymywali się w nim po drodze”: Matras, *I Met Lucky People: The Story of the Romany Gypsies*, s. 136–137.  ⇒  Pasquier, *Les recherches de la France d’Estienne Pasquier*, s. 393. Choć wyrażenie „Mały Egipt”, używane w wielu innych źródłach wczesnonowożytnych, rozumie się często jako odnoszące się do jakiejś części Egiptu, niektórzy romolodzy, jak Yaron Matras, uznają je za nazwę portu Modon na Peloponezie w Grecji, który był „ważną stacją na szlaku morskim z Wenecji do Jafy, a pielgrzymi zmierzający do Ziemi Świętej zatrzymywali się w nim po drodze”: Matras, *I Met Lucky People: The Story of the Romany Gypsies*, s. 136–137.
- 21: *Ibidem*, s. 64: „Lydias: Florinde, au compte de ces garçons, tu passeras pour une bourgeoise du Nil ou d’Arger. Florinde: Et toi, Lydias, pour un pèlerin de la Mecque”.  ⇒  Montluc, *La comédie des proverbes*, s. 64: „Lydias: Florinde, au compte de ces garçons, tu passeras pour une bourgeoise du Nil ou d’Arger. Florinde: Et toi, Lydias, pour un pèlerin de la Mecque”.
- 34: *Ibidem*, s. 376.  ⇒  Browne, *Pseudodoxia epidemica, or Enquiries into the very many received tenents and commonly presumed truths*, s. 376.
- 46: *Ibidem*, s. 206–214.  ⇒  Ndiaye, *Scripts of Blackness: Early Modern Performance Culture and the Making of Race*, s. 206–214.
- 65: *Ibidem*, s. 223; Zysberg, *Les galériens: Vies et destins de 60,000 forçats sur les galères de France, 1680–1748*, s. 376.  ⇒  Dauge-Roth, *Signing the Body: Marks on Skin in Early Modern France*, s. 223; Zysberg, *Les galériens: Vies et destins de 60,000 forçats sur les galères de France, 1680–1748*, s. 376.
- 86: *Ibidem*, s. 81, 80.  ⇒  Ravenscroft, *Scaramouch a philosopher, Harlequin a school-boy, bravo, merchant, and magician. A comedy after the Italian manner: Acted at the Theatre-Royal*, s. 81, 80.
- 87: *Ibidem*, s. 80–81.  ⇒  Ravenscroft, *Scaramouch a philosopher, Harlequin a school-boy, bravo, merchant, and magician. A comedy after the Italian manner: Acted at the Theatre-Royal*, s. 80–81.
- 88: *Ibidem*, s. 9.  ⇒  Ravenscroft, *Scaramouch a philosopher, Harlequin a school-boy, bravo, merchant, and magician. A comedy after the Italian manner: Acted at the Theatre-Royal*, s. 9.
- 91: *Ibidem*, akt 4, sc. 1, w. 782–806.  ⇒  Brome, *The English Moor, or the Mock-Marriage*, akt 4, sc. 1, w. 782–806.
- 93: *Ibidem*, s. 65.  ⇒  Carlell, *The fool would be a favourit, or, The discreet lover: A trage-comedy*, s. 65.
- 98: *Ibidem*, s. 34–36.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 34–36.
- 99: *Ibidem*, s. 34.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 34.
- 100: *Ibidem*, s. 45.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 45.
- 101: *Ibidem*, s. 44.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 44.
- 102: *Ibidem*, s. 45.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 45.
- 103: *Ibidem*, s. 47.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 47.
- 104: *Ibidem*, s. 36.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 36.
- 105: *Ibidem*, s. 34.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 34.
- 106: *Ibidem*, s. 45.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 45.
- 108: *Ibidem*, s. 76.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 76.
- 109: *Ibidem*, s. 77.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 77.
- 110: *Ibidem*, s. 78.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 78.
- 111: *Ibidem*, s. 79.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 79.
- 115: *Ibidem*, s. 79.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 79.
- 116: *Ibidem*, s. 7.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 7.
- 117: *Ibidem*, s. 20.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 20.
- 118: *Ibidem*.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 20.
- 119: *Ibidem*.  ⇒  M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 20.
- 133: *Ibidem*, s. 3.  ⇒  King, *The Black Shoals: Offshore Formations of Black and Native Studies*, s. 3.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/ndiaye_pl.txt
============================================================

--- WARN ---
192:77  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … nde ordonnance criminelle d’août 1670, „Revue d’histoire mode …
228:56  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … ique de l’identité dans le théâtre français, 1550–1680: Le dé …
236:180  [ABBR-VIDE] vide / cf. / etc. are not used — zob., por.
        … , Titles, Dramatic Companies, Etc., University of Pennsylvania P …
278:84  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … dernes selon les règles du théâtre, René Guignard, Paris 1682 …
292:70  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … aire, comédie en trois actes mêlez de danses et de musique, D …
336:35  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … aurens Jean, Séville et le théâtre: De la fin du Moyen Age à …
362:89  [ORTH-OWSKI] Since 2026 -owski adjectives from personal names are lowercase (przekład molierowski, ujęcie kantowskie). Ignore if it is a surname or part of a proper name.
        … ane są tu Szelmostwa Skapena, Molierowscy Égyptiens są konsekwentnie „C …
412:402  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … Un Amour affricain, qui s’apprête à voller”. …
418:183  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … dernes selon les règles du théâtre, René Guignard, Paris 1682 …
438:38  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … Sentaurens, Séville et le théâtre: De la fin du Moyen Age à …
446:56  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … ique de l’identité dans le théâtre français, 1550–1680: Le dé …
446:237  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … lle d’un héros qui s’est lui-même persuadé qu’il est mort en …
452:314  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … aire, comédie en trois actes mêlez de danses et de musique, D …
462:230  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … de province en province, se mêlent de dire la bonne fortune, …
464:45  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … zieła; oryginał: „Un petit démêlé avec la justice […] elle en …
466:95  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … de moins, ne sont pas pour arrêter un noble cœur”: Molière, L …
468:512  [ISO9-VOWELS] â/û/ê: ISO 9 if this is transliterated Cyrillic (ALA-LC: ia/iu/ie). Legitimate in French or Romanian.
        … nde ordonnance criminelle d’août 1670, „Revue d’histoire mode …
552:181  [ABBR-VIDE] vide / cf. / etc. are not used — zob., por.
        … , Titles, Dramatic Companies, Etc., University of Pennsylvania P …

--- counts (interpret by zone; RULES.md §J) ---
  apparatus_year_forms (1943 r.): 0
  prose_year_forms (1943 roku): 42
  apparatus_century_forms (XX w.): 0
  prose_century_forms (XX wieku): 27
  i_in: 0
  ibidem: 30
  ascii_apostrophe_inside_word (soft sign?): 0

Not checkable here:
  · Ibidem legality (same page) — proofs.
  · Short-title consistency; note↔bibliography coverage.
  · Metryczki anonymisation — editor's call.
  · Initials in notes / full names in bibliography.
  · Surnames must NOT be capitalised in the CSV.
  · Missing source data: flag it, never reconstruct.
```
