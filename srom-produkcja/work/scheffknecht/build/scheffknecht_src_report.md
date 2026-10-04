# Build report — scheffknecht_src

**RESULT: PROOF — reading copy with the full apparatus; not for InDesign**

- footnotes: 120 · citation keys used: 35 · bibliography sections: {'VI': 35}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/srom-typeset/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.7)
- Ibidem notes to check after layout: 3 (run scheffknecht_src_ibidem.jsx)

## Errors
- none

## Source language: Polish typography not applied (handoff.md; normalize.py runs on the translation)
- no ASCII ellipsis: 1
- no English quotes “: 88
- linter [ELLIPSIS-DOTS]: 1
- linter [NOTE-AFTERDOT]: 2

## Warnings (review)
- 1 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA: w źródle tu odsyłacz 1 (numer przypisu do ty
- missing data placeholders ['[BRAK WYDAWCY]'] in notes [1, 5, 6, 7, 8, 9, 10, 12, 17, 19, 23, 24, 29, 30, 31, 34, 39, 68, 107, 108, 109, 120] — ask the author (kanon §0; see scheffknecht_src_pytania.md)
- query sheet scheffknecht_src_pytania.md: 7× odwołanie do całości dzieła (bez strony), 29× brak danych bibliograficznych
- asterisk series (kanon § 7.1): title note + 0 translator/editorial note(s) are paragraphs in 'Przypis GWIAZDKOWY' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run scheffknecht_src_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł': 9, 'Cytat': 21, 'Tekst': 56, 'Tekst BEZ WCIĘCIA': 7, 'Podpis': 2, 'Bibliografia': 35, 'Przypis GWIAZDKOWY': 1}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 288, 'Kapitaliki': 38}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 120 / source 120
- [x] footnote paragraphs use footnote style only: {'Przypis': 120}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 0 / notes 0
- [x] asterisk notes at the end = notes + title note: 'Przypis GWIAZDKOWY' notes 1 / expected 0 + 1
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [x] no em dash: 0
- [x] no double spaces: 0
- [ ] no ASCII ellipsis: 1
- [ ] no English quotes “: 88

## Ibidem replaced by the short form at build time (§7.3)
- 21: Cyt. za Landwehr, *Norm, Normalität, Anomale…*, s. 57.  — Ibidem inside a sentence

## Ibidem map (note → form to use if it lands on a different column)
- 22: *Ibidem*.  ⇒  Landwehr, *Norm, Normalität, Anomale…*, s. 57.
- 41: *Ibidem*, s. 100.  ⇒  Hippel, *Armut, Unterschichten, Randgruppen…*, s. 100.
- 111: *Ibidem*, s. 236.  ⇒  Schubert, *Arme Leute…*, s. 236.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/scheffknecht_src.txt
============================================================

--- ERROR ---
7:699  [ELLIPSIS-DOTS] Use the single character … ; omissions in quotes as […].
        … verschiedene Art zu getragen [...][4] suchen wir diese angeblic …
75:269  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … er nicht gespihlt als das mahl.[45] …
171:78  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … st ein Receptator, wie voriger.[115] …

--- WARN ---
5:326  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … ns withdrew, and settled in a “city of tents” where now stand …
7:945  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … faßte Heimatkunde von Lustenau“ veröffentlichte, hielt er es …
7:1134  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … Überschrift „Unsere Abstammung“ führte er aus: …
15:907  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … alekt weist Ähnlichkeiten auf.“[5] …
19:753  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … hlechtsnamen sind kerndeutsch.“[6] …
21:124  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … . Nach Leo Jutz wird „Zigeuner“ in Götzis als „Spottname für …
21:180  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … für die Bewohner von Lustenau“ verwendet[7]. …
23:233  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … ndete Lustenauer „Fasnat-Zunft“ trägt beispielsweise den Name …
23:279  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … sweise den Namen „Rhin-Zigünar“[8]. Herbert Riedmann wählte f …
23:375  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … band den Titel „Zigünar-dütsch“. Drei der darin enthaltenen M …
23:472  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … nten Klischee: „Zigünar-dütsch“, „Ziginar odr Zigünar?“ und „ …
23:496  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … dütsch“, „Ziginar odr Zigünar?“ und „Meyor siond Rhinzigünar“ …
23:526  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … “ und „Meyor siond Rhinzigünar“[9]. Auch mehrere Lustenauer B …
23:596  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … aben die Bezeichnung „Zigeuner“ zu einer Markenbezeichnung ge …
23:719  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … ten unter dem Namen „Zigünarli“, und die örtliche Senffabrik …
23:821  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … derem auch einen „Zigeunersenf“ an. Diese Aufzählung ließe si …
23:1188  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … rgern unterscheidet. „Zigeuner“ ist damit längst zu einer Chi …
23:1325  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … von einer Art „Erinnerungsort“ zu sprechen[10]. Im folgenden …
27:62  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … a tribe of gypsy horse traders“, im Zuge der römischen Erober …
29:79  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … vergleichsweise vorurteilsfrei“. Sie galten „als reuige chris …
29:213  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … gläubigen vertriebene Christen“[13]. Dies half ihnen, kaiserl …
29:416  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … ie wurden fortan als „Zigeuner“, „Tartaren“, „Spione der Türk …
29:428  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … rtan als „Zigeuner“, „Tartaren“, „Spione der Türken“[15], „He …
29:449  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … „Tartaren“, „Spione der Türken“[15], „Heiden“[16], „Kannibale …
29:463  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … pione der Türken“[15], „Heiden“[16], „Kannibalen“ oder „Kinde …
29:481  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … 15], „Heiden“[16], „Kannibalen“ oder „Kinderräuber“[17] verru …
29:501  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … Kannibalen“ oder „Kinderräuber“[17] verrufen. Seit etwa 1470 …
31:256  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … deutig ethnisch zu bestimmende“ Gruppe handelte. Vieles spric …
31:514  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … im Familienverband umherzogen“[20]. Bereits 1727 vertrat Joh …
31:917  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … amilial organisierte Mobilität“ ermöglichte es der normsetzen …
31:1055  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … ndeutig als solche zu erkennen“[22]. Dazu kam noch ihr angebl …
31:1298  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … und seßhaften Lebensweise war“, gleichsam „ein doppeltes Pro …
31:1333  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … eichsam „ein doppeltes Problem“. Ihre Nicht-Sesshaftigkeit se …
31:1449  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … und kriminelles Leben führten“. Überdies wurden sie als Heid …
31:1539  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … thnisch unterscheidbare Gruppe“ – oder besser als eine ethnis …
31:1652  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … sonders argwöhnisch betrachtet“, entsprechend diskriminiert u …
33:1294  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … oros
```
