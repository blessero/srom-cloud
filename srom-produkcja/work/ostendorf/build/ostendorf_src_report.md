# Build report — ostendorf_src

**RESULT: PROOF — reading copy with the full apparatus; not for InDesign**

- footnotes: 62 · citation keys used: 83 · bibliography sections: {'VI': 83}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/srom-typeset/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.7)
- Ibidem notes to check after layout: 2 (run ostendorf_src_ibidem.jsx)

## Errors
- none

## Source language: Polish typography not applied (handoff.md; normalize.py runs on the translation)
- no English quotes “: 117
- linter [NOTE-AFTERDOT]: 31
- linter [SPACE-BEFOREPUNCT]: 8

## Warnings (review)
- 2 comment(s) removed from the text (never printed, never blocking): DO SPRAWDZENIA (pytania D1): przypis 25 cytuje „De Cadiz a V | DO SPRAWDZENIA (pytania D2): przypis 35 cytuje list Penna z 
- corrections of the author's data (approved; refs.json srom-as-written): matache2026: title “The Permanence of Anti-Roma Racism:(Un)uttered Sentences” (as written) → corrected; savic2022: note “Conference Paper presented at” (as written) → corrected; mangas2024: note “PhD diss.” (as written) → corrected; berquinduvallon1803: title “Vue de la colonie Espagnole du Mississipi, ou des provinces de Louisiane et Floride Occidentale,en l’année 1802” (as written) → corrected; cunniffe2023: note “PhD diss.” (as written) → corrected; jamaicalady1720: author “Anonymous” (as written) → corrected; wollon1952: title “Notes and Documents: Sir Augustus J. Foster and ‘the Wild Natives of the Woods,’ 1805–1807” (as written) → corrected
- nested italics set roman, verify: Cigano
- nested italics set roman, verify: Divide et impera
- nested italics set roman, verify: c.
- nested italics set roman, verify: c.
- nested italics set roman, verify: Cigano
- nested italics set roman, verify: Divide et impera
- missing data placeholders ['[BRAK MIEJSCA]', '[BRAK WYDAWCY]'] in notes [1, 2, 11, 12, 15, 17, 18, 34, 36, 47, 48] — ask the author (kanon §0; see ostendorf_src_pytania.md)
- query sheet ostendorf_src_pytania.md: 14× odwołanie do całości dzieła (bez strony), 13× brak danych bibliograficznych, 1× tekst bez autora w tomie zbiorowym

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł 1': 5, 'Tekst bez wcięcia': 5, 'Tekst': 33, 'Cytat blokowy': 1, 'Bibliografia – tytuł': 1, 'Bibliografia': 83}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 273, 'Kapitaliki': 86}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 62 / source 62
- [x] footnote paragraphs use footnote style only: {'Przypis': 62}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 0 / notes 0
- [x] asterisk notes at the end = notes + title note: 'Przypis gwiazdkowy' notes 0 / expected 0 + 0
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [x] no em dash: 0
- [x] no double spaces: 0
- [x] no ASCII ellipsis: 0
- [ ] no English quotes “: 117

## Ibidem replaced by the short form at build time (§7.3)
- none

## Ibidem map (note → form to use if it lands on a different column)
- 18: *Ibidem*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993.  ⇒  Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 27–33; A. Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the General Imprisonment of Gypsies in 1749*, University of Hertfordshire Press, [BRAK MIEJSCA] 1993.
- 22: *Ibidem*; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.  ⇒  Herzog, *Defining Nations…*, s. 133; Gómez Alfaro, Lopes da Costa, Floate, *Deportaciones de Gitanos*, s. 30; R. Pym, *The Gypsies of Early Modern Spain*, Palgrave Macmillan, Basingstoke 2007, s. 145–147.

## Lint (srom-kanon lint_srom.py on rendered text)
```
SROM canon check — build/ostendorf_src.txt
============================================================

--- ERROR ---
5:463  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … cializing practices in general.[1] By stretching the frame to in …
5:693  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … e inventing European modernity.[2] Turning Romani people into fo …
5:1608  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … s time, space and circumstance.[3] …
7:248  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … otherness in and of themselves.[4] I also move beyond Tamar Herz …
7:614  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … nging and estrangement surface.[5] This chapter also differs fro …
19:1176  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … l racialization from the start.[11] …
23:129  [SPACE-BEFOREPUNCT] Space before punctuation.
        … rom the dregs of the Egyptians . . . whom we call Zingaros in …
25:297  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … otivation and civic attachment.[12] Today a Catholic saint, Anchi …
29:970  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … rred alongside others and self.[15] …
33:1535  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … nto which they might disappear.[18] Though there was never any ex …
33:2143  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … he mechanisms of Habsburg rule.[19] …
35:663  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … o rather than “Indio” ancestry.[20] One’s reputation was often re …
35:1101  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … uals the appearance of Gitanos.[21] …
37:1159  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … as any reified notion of race.[22] …
39:483  [SPACE-BEFOREPUNCT] Space before punctuation.
        … ers with a Zigeuner complexion . . . [Others] have a white-yel …
41:471  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ,” noted Joseph Roldán in 1762.[24] Similarly, Manuel Moreno Alon …
41:731  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … men’s “Gitano-like” appearance.[25] Physiognomy and mobility, in …
47:564  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … t the end of the prior century.[28] These connections caught the …
47:1235  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … oncerns these choices provoked.[29] Colonial agents desirous of e …
49:1036  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … zation influencing their lives.[30] Romani men also married Indig …
49:1547  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … om the reality of their labors.[31] …
51:468  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … t meant to be French and white.[32] This example also reveals the …
55:1219  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … fference more tightly together.[33] …
59:1511  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … d through literature and drama.[36] When Penn noted seeing Native …
59:1989  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … o spread European civilization.[38] …
61:225  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … Atlantic world and even beyond.[39] And, like the confusion cause …
61:555  [SPACE-BEFOREPUNCT] Space before punctuation.
        … ly of a pale yellow Complexion . . . [spoke] . . . a sort of j …
65:569  [SPACE-BEFOREPUNCT] Space before punctuation.
        … n: “Ran away on Sunday evening . . . Joseph Smith, an old man, …
65:1108  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … hor scripted race relationally.[43] …
67:436  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … nd mulattoes” remained illegal.[44] Emphasizing Romani peoples’ d …
69:1819  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ni people as part of one whole.[48] …
73:255  [SPACE-BEFOREPUNCT] Space before punctuation.
        … nufacturing brooms and baskets . . . . These Indians are now t …
73:552  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … nted two people with one brush.[52] One author even supposed that …
73:862  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … g into their abandoned wigwams.[53] …
75:698  [SPACE-BEFOREPUNCT] Space before punctuation.
        … y have actually no alternative . . . . For such is the prejudi …
77:1135  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … in authors and audiences alike.[56] Of the dozens of examples, a …
79:494  [SPACE-BEFOREPUNCT] Space before punctuation.
        … ica’s “distinguishing features . . . in their natural colours. …
81:355  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … fortune tellers and sorcerers.[60] Similarly, in an account from …
331:233  [SPACE-BEFOREPUNCT] Space before punctuation.
        … people on the banks of rivers . . . are generally a loose set …

--- WARN ---
5:649  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … alogous comparisons, invented “Gypsies” while inventing Europ …
5:915  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … the accompanying invention of “Indians” in European thought. …
5:1011  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … g on Noémie Ndiaye’s ideas of “racial scripts” as trans-imper …
5:1046  [QUOTE-EN-IN-PL] English opening quote in a Polish article — use „ ”.
        … al scripts” as trans-imperial “metaphorical strains” that “we …
5:1074  [QUOTE-EN-IN-PL] English opening quote in a Polish articl
```
