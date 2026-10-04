# Build report — ndiaye_src

**RESULT: PROOF — reading copy with the full apparatus; not for InDesign**

- footnotes: 133 · citation keys used: 79 · bibliography sections: {'V': 1, 'VI': 83}
- pandoc 3.8.3 · CSL srom.csl · config styles.json · linter /Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/srom-typeset/.claude/skills/srom-kanon/scripts/lint_srom.py (Kanon v1.6)
- Ibidem notes to check after layout: 30 (run ndiaye_src_ibidem.jsx)

## Errors
- none

## Source language: Polish typography not applied (handoff.md; normalize.py runs on the translation)
- no em dash: 63
- no English quotes “: 173
- linter [EMDASH]: 63
- linter [NOTE-AFTERDOT]: 71
- linter [SPACE-BEFOREPUNCT]: 5

## Warnings (review)
- corrections of the author's data (approved; refs.json srom-as-written): admant2015: publisher-place “Droit” (as written) → corrected; vanlennep1965: editor “Van Lannep” (as written) → corrected
- printed though not cited in the notes (the author's bibliography, Kanon § 9.2): ['cervantes1617', 'crooks1931', 'galland2017', 'netzloff2003', 'ravenscroft1678']
- nested italics set roman, verify: The Spanish Gypsie
- nested italics set roman, verify: The Spanish Gypsie
- nested italics set roman, verify: Les Fourberies de Scapin
- nested italics set roman, verify: Paios
- nested italics set roman, verify: Paios
- nested italics set roman, verify: Antony and Cleopatra
- nested italics set roman, verify: Les Fourberies de Scapin
- nested italics set roman, verify: The Spanish Gypsie
- query sheet ndiaye_src_pytania.md: 13× odwołanie do całości dzieła (bez strony), 2× cytat bez numeru strony, 24× długi tytuł bez formy skróconej (title-short)
- asterisk series (kanon § 7.1): title note + 0 translator/editorial note(s) are paragraphs in 'Przypis gwiazdkowy' at the end of the DOCX, marked * in the text — set them by hand above the numbered notes; after layout run ndiaye_src_gwiazdki.jsx for the asterisks per page

## DOCX verification
- [x] paragraph styles ⊆ config: used {'Śródtytuł 1': 7, 'Tekst bez wcięcia': 7, 'Cytat blokowy': 4, 'Tekst': 44, 'Cytat – wiersz': 5, 'Podpis': 3, 'Bibliografia – tytuł': 1, 'Bibliografia – dział': 2, 'Bibliografia': 84, 'Przypis gwiazdkowy': 1}; foreign {}; unstyled 0
- [x] character styles ⊆ config: used {'Kursywa': 403, 'Kapitaliki': 89}; foreign {}
- [x] no direct italic/bold/caps runs: 0 direct-formatted runs
- [x] footnote count: docx 133 / source 133
- [x] footnote paragraphs use footnote style only: {'Przypis': 133}
- [x] no leading space in notes: 0 notes start with a space
- [x] footnote number not in an empty paragraph: 0
- [x] no translator/editorial note among the numbered footnotes (§7.1): footnotes []
- [x] asterisk markers in the text = translator/editorial notes: markers 0 / notes 0
- [x] asterisk notes at the end = notes + title note: 'Przypis gwiazdkowy' notes 1 / expected 0 + 1
- [x] no hyperlinks: 0
- [x] no straight double quotes: 0
- [ ] no em dash: 63
- [x] no double spaces: 0
- [x] no ASCII ellipsis: 0
- [ ] no English quotes “: 173

## Ibidem replaced by the short form at build time (§7.3)
- 42: “I prefer the term ‘natal alienation,’ because it goes directly to the heart of what is critical in the slave’s forced alienation, the loss of ties of birth in both ascending and descending generations. It also has the important nuance of a loss of native status, of deracination. It was this alienation of the slave from all formal, legally enforceable ties of ‘blood,’ and from any attachment to groups or localities other than those chosen for him by the master, that gave the relation of slavery its peculiar value to the master”: O. Patterson, *Slavery and Social Death: A Comparative Study*, Harvard University Press, Cambridge, MA 1982, s. 7. “Social death” is “the outward conception” of this natal alienation: Patterson, *Slavery and Social Death: A Comparative Study*, s. 8.  — Ibidem inside a sentence
- 50: “Un petit démêlé avec la justice . . . elle en usa fort mal avec moi”: Molière, *Les fourberies de Scapin*, s. 7.  — Ibidem inside a sentence
- 51: “Trois ans de galère de plus, ou de moins, ne sont pas pour arrêter un noble cœur”: Molière, *Les fourberies de Scapin*, s. 34.  — Ibidem inside a sentence
- 52: For Scapin’s diatribe against the French justice system, zob. Molière, *Les fourberies de Scapin*, s. 61–62. Scapin’s resentment seems to echo a widespread perception at the time that the justice system was entirely corrupt and failed to implement the law. Louis XIV’s Grande Ordonnance of 1670 was meant to address those issues. The Ordonnance aimed in particular at shortening the length and diminishing the expenses involved in trials. M. Boulanger, *Justice et absolutisme: La grande ordonnance criminelle d’août 1670*, „Revue d’histoire moderne et contemporaine”, 2000, t. 47, nr 1, s. 31.  — this note also cites another (literal) source before it
- 64: K. Dauge-Roth, *Signing the Body: Marks on Skin in Early Modern France*, Routledge, New York 2019, s. 224. Dauge-Roth underlines the similarities between the branding of galley men and the branding of enslaved Afro-diasporic people in the French colonies: in both cases, branding marked the racialized body as property of the king or a white master. Dauge-Roth, *Signing the Body: Marks on Skin in Early Modern France*, s. 220–225.  — Ibidem inside a sentence
- 69: “You do not resemble him in the least. Don’t you know everybody says he is only your father on paper?”: Molière, *Les fourberies de Scapin*, s. 53.  — Ibidem inside a sentence
- 78: Hitchcock, *Vagrancy in English Culture and Society, 1650–1750*, s. 5.  — previous note also cites another (literal) source
- 82: G. Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles . . . and translated into English by R. C. . . .*, Printed for W. Gilbertson, London 1662, k. S2r. While Theodorus, the “master,” regularly calls Bannacar his “servant” in the English version of Ruggle’s play, he is contrasted with Bannacar’s previous master, Alfonso, a slave master who manumitted him at the time of his death. Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles . . . and translated into English by R. C. . . .*, k. S4r.  — Ibidem inside a sentence
- 83: Ravenscroft also decided to cut a raunchy scene from Ruggle’s play featuring sex workers of many ethnicities, including a black-skinned Moorish woman: Ruggle, *Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles . . . and translated into English by R. C. . . .*, k. D4r. This play has received no attention from early modern critical race scholars yet.  — Ibidem inside a sentence
- 107: “Peace, or I’le teach your Gipsie-ship some manners”: M. W., M. A., *A comedy called The marriage broaker: or, The pander*, s. 60.  — Ibidem inside a sentence

## Ibidem map (note → form to use if it lands on a different column)
- 7: *Ibidem*, s. 23–24. Zob. też Y. Matras, *I Met Lucky People: The Story of the Romany Gypsies*, Penguin Books, London 2014, s. 131.  ⇒  Chang, Rucker-Chang, *Roma Rights and Civil Rights: A Transatlantic Comparison*, s. 23–24. Zob. też Y. Matras, *I Met Lucky People: The Story of the Romany Gypsies*, Penguin Books, London 2014, s. 131.
- 18: *Ibidem*, s. 393. Although “Little Egypt,” the phrase used in various other early modern sources, is often understood as referencing some part of Egypt, some Romani studies scholars, like Yaron Matras, take it as a reference to the port of Modon in the Peloponnese, Greece, which was “an important station on the sea route from Venice to Jaffa and was used as a stop by pilgrims on their way to the Holy Land”: Matras, *I Met Lucky People: The Story of the Romany Gypsies*, s. 136–137.  ⇒  Pasquier, *Les recherches de la France d’Estienne Pasquier*, s. 393. Although “Little Egypt,” the phrase used in various other early modern sources, is often understood as referencing some part of Egypt, some Romani studies scholars, like Yaron Matras, take it as a reference to the port of Modon in the Peloponnese, Greece, which was “an important station on the sea route from Venice to Jaffa and was used as a stop by pilgrims on their way to the Holy Land”: Matras, *I Met Lucky People: The Story of the Romany Gypsies*, s. 136–137.
- 21: *Ibidem*, s. 64: “Lydias: Florinde, au compte de ces garçons, tu passeras pour une bourgeoise du Nil ou d’Arger. Florinde: Et toi, Lydias, pour un pèlerin de la Mecque.”  ⇒  Montluc, *La comédie des proverbes*, s. 64: “Lydias: Florinde, au compte de ces garçons, tu passeras pour une bourgeoise du Nil ou d’Arger. Florinde: Et toi, Lydias, pour un pèlerin de la Mecque.”
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
SROM canon check — build/ndiaye_src.txt
============================================================

--- ERROR ---
3:290  [EMDASH] Em dash is not used — en dash.
        … everal recent plays by Molière—chief among them, Les fourberi …
3:664  [EMDASH] Em dash is not used — en dash.
        … dell’arte typology): Plautino—who, as his name indicates, is …
3:715  [EMDASH] Em dash is not used — en dash.
        … icates, is “a man of intrigue”—and Harlequin, whose black mas …
3:1009  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … an face to a white-passing Rom.[2] The second moment is March 20 …
5:606  [EMDASH] Em dash is not used — en dash.
        … ellectual and social community—my people—was always, from the …
5:616  [EMDASH] Em dash is not used — en dash.
        … and social community—my people—was always, from the beginning …
5:1438  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … bout liberation and solidarity.[4] …
9:321  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … brownface in the movie ROMing).[6] In this essay, however, I mov …
11:310  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … rough a robust legal apparatus.[7] Thus, in Romanian, the word R …
11:489  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … avo in sixteenth-century Spain.[9] As Felix Chang and Sunnie Ruc …
13:127  [EMDASH] Em dash is not used — en dash.
        … their own labor at the galleys—both of which forms of persecu …
13:1707  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … the age of nascent capitalism.[15] …
15:454  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … e Gypsies Metamorphos’d (1621).[16] Without denying the importanc …
15:1075  [EMDASH] Em dash is not used — en dash.
        … r-canonical playwright Molière—by placing them on equal evide …
15:1120  [EMDASH] Em dash is not used — en dash.
        … m on equal evidentiary footing—I resist the centripetal force …
17:1299  [EMDASH] Em dash is not used — en dash.
        … on, and bodily commodification—in tune with the times. Finall …
21:90  [EMDASH] Em dash is not used — en dash.
        … fifteenth century onward, Roma—who originally hail from the I …
21:139  [EMDASH] Em dash is not used — en dash.
        … l from the Indian subcontinent—were erroneously construed as …
21:232  [EMDASH] Em dash is not used — en dash.
        … er wrote that Romani companies—“whom some call Egyptians and …
21:283  [EMDASH] Em dash is not used — en dash.
        … tians and other Bohemians”[17]—claimed to hail from “basse Eg …
21:538  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … istian nations for seven years.[18] This popular myth, which init …
21:682  [EMDASH] Em dash is not used — en dash.
        … retained the Egyptian demonym—shortened as “Gypsy”—across th …
21:703  [EMDASH] Em dash is not used — en dash.
        … n demonym—shortened as “Gypsy”—across the early modern period …
32:288  [EMDASH] Em dash is not used — en dash.
        … in La belle Egyptienne (1642)—to which I will shortly return …
32:319  [EMDASH] Em dash is not used — en dash.
        … to which I will shortly return—the Gadjo (non-Roma) Don Jean …
32:716  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ian Claude-François Ménestrier.[27] Similarly, visual culture art …
36:149  [EMDASH] Em dash is not used — en dash.
        … rceptions of the Roma as white—as Gadje counterfeits delibera …
36:215  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … espousing a marginal lifestyle.[28] The suspected whiteness of Ro …
36:772  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … teenth-century popular culture.[29] In 1617, John Minsheu defined …
40:422  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … too heavie for their carriage.[30] …
42:444  [EMDASH] Em dash is not used — en dash.
        … in herb which darkens our skin—we have a secret recipe to lif …
46:336  [EMDASH] Em dash is not used — en dash.
        … ment that is of interest to me—namely, the growing associatio …
46:453  [EMDASH] Em dash is not used — en dash.
        … n the logic of white supremacy—deploys itself. The use of cos …
50:414  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … m it in one important instance.[35] When, at the beginning of the …
50:1376  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ties in early modern Andalusia.[38] …
52:250  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … Jacobean and Caroline theater.[39] Sallebray’s vignette thus dra …
52:745  [EMDASH] Em dash is not used — en dash.
        … he shared craving for mobility—real and symbolic—that comes w …
52:763  [EMDASH] Em dash is not used — en dash.
        … for mobility—real and symbolic—that comes with enslavement. …
54:1178  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ally, the Black Fortune-Teller.[40] As Georges Forestier notes, t …
54:1902  [EMDASH] Em dash is not used — en dash.
        … prince, remains oddly attached—as the play’s title suggests—t …
54:1931  [EMDASH] Em dash is not used — en dash.
        … d—as the play’s title suggests—to the idea of his own enslave …
54:2281  [EMDASH] Em dash is not used — en dash.
        … nt can inflict on the enslaved—unambiguously figured, here, a …
56:708  [EMDASH] Em dash is not used — en dash.
        … ast in the role of the “Mores”—who, I have argued elsewhere, …
56:817  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … y modern French ballet culture.[45] Here again, the association b …
56:1373  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … luded them in the animal realm.[46] The trope of animalization br …
60:567  [NOTE-AFTERDOT] Note marker goes before the closing period.
        … ing that he shall 
```
