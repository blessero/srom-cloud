# Build report — tittel_src

**RESULT: PROOF — reading copy with the full apparatus; not for InDesign**

- footnotes: 100 · citation keys used: 63 · bibliography sections: {'IV': 5, 'V': 2, 'VI': 56}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/srom-typeset/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.7)
- Ibidem notes to check after layout: 18 (run tittel_src_ibidem.jsx)

## Errors
- none

## Source language: Polish typography not applied (handoff.md; normalize.py runs on the translation)
- no ASCII ellipsis: 1
- no English quotes “: 170
- linter [ELLIPSIS-DOTS]: 1
- linter [NOTE-AFTERDOT]: 55

## Warnings (review)
- 1 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA (pytania A4): skrót MEW 23 nie jest używany w
- corrections of the author's data (approved; refs.json srom-as-written): decker2018: author “Decker” (as written) → corrected; vanbaar2019: title “The Securitization of the Roma in Europe. Human rights interventions” (as written) → corrected; ruch1986: note “unpublished dissertation” (as written) → corrected; breger2003: editor “Engbring-Romang; Strauss” (as written) → corrected; tomlins1811: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected; raithby1811a: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected; raithby1811b: publisher “Printed by G. Eyre and A. Strahan, printers to the King” (as written) → corrected
- missing data placeholders ['[BRAK WYDAWCY]'] in notes [20] — ask the author (kanon §0; see tittel_src_pytania.md)
- query sheet tittel_src_pytania.md: 27× odwołanie do całości dzieła (bez strony), 1× cytat bez numeru strony, 1× brak danych bibliograficznych, 1× tekst w sieci bez pełnej daty publikacji
- asterisk series (kanon § 7.1): title note + 0 translator/editorial note(s) are paragraphs in 'Przypis gwiazdkowy' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run tittel_src_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł 1': 5, 'Tekst bez wcięcia': 5, 'Tekst': 35, 'Cytat blokowy': 6, 'Bibliografia – tytuł': 1, 'Bibliografia – dział': 3, 'Bibliografia': 63, 'Przypis gwiazdkowy': 1}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 324, 'Kapitaliki': 75}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 100 / source 100
- [x] footnote paragraphs use footnote style only: {'Przypis': 100}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 0 / notes 0
- [x] asterisk notes at the end = notes + title note: 'Przypis gwiazdkowy' notes 1 / expected 0 + 1
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [x] no em dash: 0
- [x] no double spaces: 0
- [ ] no ASCII ellipsis: 1
- [ ] no English quotes “: 170

## Ibidem replaced by the short form at build time (§7.3)
- 26: Eberl claims that one can see a change in Kant’s attitude towards the travel reports: “Where Kant first uncritically trusted and accepted the description of and judgements on foreign peoples in those travel reports (1764), he ultimately became […] critical of them (1785)” (Eberl, *Kant on Race*, s. 390). He further describes how Kant, in his late writings, rather relied on biological explanations of ‘race’ than on travel reports (Eberl, *Kant on Race*, s. 408).  — Ibidem inside a sentence
- 50: Marx, *Das Kapital…*, s. 746.  — previous note also cites another (literal) source
- 83: Original: “Verordnung wegen Austreibung der Zigeuner,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 489.  — Ibidem inside a sentence
- 84: Original: “dises Landschädliche Gesind außrotten helffen,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 490.  — Ibidem inside a sentence
- 85: Original: “gänzlicher Ausrottung,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 822.  — Ibidem inside a sentence
- 86: Original: “Zigeiner, Garttbrüder, Jauner und andern herrenlosen Gesindes,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 822.  — Ibidem inside a sentence
- 87: Original: “dieses verdammliche Zigeiner-Gesind innerhalb Vierzehn Tag von Publication dieses offenen Patents den Creyß und gantz Schwaben raumen, dafern Sie aber nach Verfliessung solcher Zeit in demselben noch betretten würden, Sie Vogelfrey und Männiglich erlaubt seyn solle, dieselbe ohne Frevel und Verantwortung [...] zu erlegen, zu spoliren, und nach Belieben zu hantieren,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 88: Original: “todt geschossen,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 89: Original: “nidergelegt,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 90: Original: “ohne den wenigsten Anstandt todtschiessen,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 824.  — Ibidem inside a sentence
- 91: Original: “in die härtiste Gefängnüssen geworffen,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 92: Original: “wie Sie dann von dergleichen niemalhs rein seyn können,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 823.  — Ibidem inside a sentence
- 93: Original: “biß die gantze Race von diesem Gesind in allen Theilen des Creyses extirpiert und auff den Grund außgerottet worden,” Zeller, Reyscher, *Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…*, s. 824.  — Ibidem inside a sentence

## Ibidem map (note → form to use if it lands on a different column)
- 15: *Ibidem*, s. 73–75.  ⇒  Röttgers, *Kants Zigeuner*, s. 73–75.
- 16: *Ibidem*, s. 64.  ⇒  Röttgers, *Kants Zigeuner*, s. 64.
- 17: *Ibidem*. Even though Kraus never published the results himself, Röttgers provides clear evidence that Kraus was working on this topic (*Ibidem*, s. 64–75). For more information on Kraus’s study, zob. K. Röttgers, *Kants Kollege und seine ungeschriebene Schrift über die Zigeuner*, Manutius, Heidelberg 1993.  ⇒  Röttgers, *Kants Zigeuner*, s. 64. Even though Kraus never published the results himself, Röttgers provides clear evidence that Kraus was working on this topic (Röttgers, *Kants Zigeuner*, s. 64–75). For more information on Kraus’s study, zob. K. Röttgers, *Kants Kollege und seine ungeschriebene Schrift über die Zigeuner*, Manutius, Heidelberg 1993.
- 28: *Ibidem*, s. 84–85.  ⇒  Hund, *„It Must Come from Europe”*, s. 84–85.
- 30: Among them, we can find the philosophers Voltaire and Hume. Zob. *Ibidem*, s. 101.  ⇒  Among them, we can find the philosophers Voltaire and Hume. Zob. Larrimore, *Sublime Waste*, s. 101.
- 44: *Ibidem*, s. 209 / AA VIII 174.  ⇒  Kant, *Teleological Principles*, s. 209 / AA VIII 174.
- 51: *Ibidem*, s. 748–749.  ⇒  Marx, *Das Kapital…*, s. 748–749.
- 54: *Ibidem*, s. 762.  ⇒  Marx, *Das Kapital…*, s. 762.
- 66: Zob. *Ibidem*, s. 762–770.  ⇒  Zob. Marx, *Das Kapital…*, s. 762–770.
- 67: *Ibidem*, s. 764, przyp.  ⇒  Marx, *Das Kapital…*, s. 764, przyp.
- 68: *Ibidem*, s. 746.  ⇒  Marx, *Das Kapital…*, s. 746.
- 71: *Ibidem*, s. 724.  ⇒  Marx, *Das Kapital…*, s. 724.
- 72: *Ibidem*, s. 711.  ⇒  Marx, *Das Kapital…*, s. 711.
- 73: *Ibidem*, s. 722.  ⇒  Marx, *Das Kapital…*, s. 722.
- 74: *Ibidem*, s. 723.  ⇒  Marx, *Das Kapital…*, s. 723.
- 75: *Ibidem*, s. 724.  ⇒  Marx, *Das Kapital…*, s. 724.
- 76: *Ibidem*.  ⇒  Marx, *Das Kapital…*, s. 724.
- 77: *Ibidem*, s. 724–725.  ⇒  Marx, *Das Kapital…*, s. 724–725.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/tittel_src.txt
============================================================

--- ERROR ---
3:997  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … victim of violence themselves.[2] The image of Sinti and Roma h …
3:1197  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … rgely based on this assumption.[3] …
7:263  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … hin the context of police work.[4] They highlight that until the …
7:449  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ntion of illegitimate mobility.[5] They suggest that the police …
7:612  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … egulate nomadism/sedentariness.[6] Only later did “gypsies” star …
15:117  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ast promoting racialized ideas.[8] The question debated here is …
15:461  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … he mid-1790s, were problematic.[10] Others yet find that his anth …
15:561  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … is moral or juridical writings.[11] All of these studies focus on …
15:693  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … t “gypsies” as a special group.[12] …
17:550  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … tion-based concept of progress.[15] This interpretation itself sh …
17:1124  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … em with the gallows as penalty.[16] Professor of practical philos …
17:1449  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … es” due to the edict from 1725.[17] Röttgers argues that Kant mus …
17:1629  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … famous Berliner Monatsschrift.[18] Kant and Kraus regularly talk …
17:1959  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ed among Kant’s contemporaries.[20] …
19:527  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … tial book on the topic in 1783.[22] It became highly popular soon …
19:721  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … turn of the eighteenth century.[23] The historians Martin Ruch an …
19:971  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … rch on “gypsies” for centuries.[24] Grellmann heavily relied on t …
19:1103  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … source for Kant’s race theory.[26] Even though Kant did not name …
21:248  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … rucial role in his race theory.[27] He maintains that Kant chose …
21:423  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … vilization-related development.[28] Within studies on Kant’s race …
21:854  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … environment and are immutable.[29] With both approaches Kant eng …
21:1550  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … der through controlling nature.[31] Exactly this explanation by K …
25:491  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … e of the crudity of his nature.[32] …
27:641  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ts with their own inner nature.[33] …
29:142  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ions” have reached this status.[34] Europeans, he thinks, have de …
29:745  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … sh term “gypsy” up until today.[35] In Kant’s view, the Asian nat …
31:856  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … s a result of Grellmann’s book.[41] While in Europe it was almost …
35:471  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … m the shape of their forebears.[42] …
41:557  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … mean to doubt nature’s imprint.[43] …
43:905  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … fferentiated, advanced society.[45] Kant’s argumentation thus off …
51:686  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … in Western European societies.[48] The first period of time were …
55:334  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … e end of the fifteenth century.[50] Moreover, he considers the re …
55:467  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … the second cause of the shift.[51] Both these processes led to t …
57:118  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ondage” in the German Ideology.[52] Arriving in the cities, he ex …
57:329  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … to adapt to the new situation.[53] Thus, the displaced “turned e …
59:548  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … sical punishment like whipping.[58] Marx analyzes the 1530 act as …
59:678  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … for those who refused to work.[59] In the same year, the “Egypti …
59:1094  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … re also made against vagabonds.[61] During the following decades, …
59:1213  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … abonds increased the penalties.[62] While the 1530 “Egyptian Act” …
63:434  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ditions that no longer existed.[65] …
65:272  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … lifelong enslavement and death.[66] According to Holinshed's Chro …
65:469  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … people were executed for theft.[67] This number should not be tak …
65:61
```
