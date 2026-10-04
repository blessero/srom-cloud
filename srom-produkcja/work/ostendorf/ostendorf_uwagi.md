# Ostendorf, "Familiar Outsiders Abroad" (The Romani Atlantic, CUP 2026, ch. 3) — stage-1 test 4: open points

Stage 1 done 28.09.2026 (srom-produkcja). Source: `work/11.3_pp_86_108_Familiar_Outsiders_Abroad.pdf` (Cambridge Core
download, 23 pp. = printed pp. 86–108; p. 23 is the download stamp only). Chapter in M. Fotta, A. Ostendorf (eds.),
*The Romani Atlantic*, Cambridge University Press 2026, DOI 10.1017/9781009706032.005 (book data from Crossref: the PDF
carries only the DOI).
Files: `ostendorf_src.md` (frozen source: 5 sections, 62 notes, 54 keyed — 2 of them partly literal —, 8 literal),
`refs.json` (83 works, from `refs.py`, typed from the notes: the chapter has no bibliography), `ostendorf_src_front.md`,
`ostendorf_src_robocza.docx` (Word working copy), `build/ostendorf_src_korekta.docx` (source proof: the Polish apparatus
as it will print), `build/ostendorf_src_pytania.md` (query sheet), `key_log.md` (every keying change), `doi_check.txt`
(17 DOIs against Crossref). Pipeline: `pdf_extract.py` → `key.py` → `check.py --keyed` → `build.py --source` →
`export_work.py`; `refs.py` → refs.json. `wordcheck.py`: every word and number of the PDF in the extraction.

What this PDF broke, fixed in the toolchain with tests (commits aaecba0, ea04d6a and the next): the text layer has no
digits and no small capitals (Sabon LT Std old-style figures and small caps as private-use code points — the first run
said "EXTRACT OK" with 0 notes); "=" as "¼"; "Savi´c"; word spaces set as gaps; notes running over a page with no
separator rule (read as block quotations); a chapter numeral above the title; compounds split at a line end. The digit
table is confirmed independently: all 17 DOIs/URLs in the text equal the PDF's own link targets. `check.py --keyed` now
reads the pages of Chicago full citations (before: a lost page passed as a warning). CSL: editors of authored books and
anonymous chapters were dropped from print (A3).

## A. MB (state after MB's answers of 28.09.2026)

**GEN-3 · A1. Rights — corrected: open access, CC BY-NC 4.0.** My first reading (PDF stamp and Crossref point only to the Cambridge
Core terms) was wrong. The chapter page on Cambridge Core: "This content is Open Access and distributed under the terms of the
Creative Commons Attribution licence CC-BY-NC 4.0"; the book's copyright page: "© Cambridge University Press & Assessment
2026", CC BY-NC 4.0 for the online version; OA funder: Institute of Ethnology, Czech Academy of Sciences. So the question
is Pahulich's (D17 A1): SROM's distribution non-commercial? consent of author/publisher anyway? The translation note
(§ 12.2.3) then gives the licence, "przekład stanowi zmianę utworu", and the copyright notice. Does not block the translation.

**OST-1 · A2. Missing imprint data — sourced: 43 values; 14 for you by hand.** Sourcing from the Library of Congress catalogue
(`source_imprints.py`: SRU/MARC; a record counts only if title, year and — where we have them — publisher and place match;
place = the imprint's first city; evidence per value in `imprints.tsv` and in refs.json `srom-sourced`), plus the vol. 67
title page for Thwaites. Imprint formulas reduced to the name ("Printed for C. Cradock and W. Joy" → "C. Cradock and W. Joy";
"De l'Imprimerie expéditive" → "Imprimerie expéditive"); Harvard's "Cambridge, Mass." kept to tell it from Cambridge UK.
**By hand (no reliable record; candidates are hints, not evidence):**
- places: Matache 2026 (Routledge), Bogdal 2023 (Penguin/Allen Lane?), Monteiro 2018 (Cambridge University Press — its
  2018 imprint: Cambridge? New York?), Gómez Alfaro et al. 1999 (Centre de recherches tsiganes: Paris?), Gómez Alfaro
  1993 (the English edition was co-published: Hatfield, University of Hertfordshire Press / Paris, CRT / Madrid, Presencia
  Gitana — which the author means), *Actas da Camara da Villa de S. Paulo* 1915 (São Paulo?), Mangas 2024 and Cunniffe 2023
  (dissertations: the university's city — Porto, London — if you accept it), Savić 2022 (conference paper: Södertörn
  University, Huddinge), Beretario 1617 (**two editions that year: Cologne, Kinchius — LoC — and Lyon**), *A Relation or
  Journall* 1622 (London, printed for John Bellamie — no record found);
- publishers: Scott 1815 (joint imprint: Edinburgh, printed by Ballantyne for Longman, Hurst, Rees, Orme, and Brown,
  London, and A. Constable, Edinburgh — how much to give), Hofland 1830 (New York: W.B. Gilley? Open Library only).

**A3. Decided (MB):** `tłum. i red.`, edition of a source `red.` after the title; an unsigned text in a collection: the
editors establish the author (build query row), else title first. In Kanon § 7.2/§ 9.4 (commit ea50df6). Here: note 26 is
listed (the author is du Poisson — B3, for the translation stage).

**A4. Decided (MB: "whatever the custom is") — Kanon § 9.3/§ 9.5:** the heading form of the name's language, as in the
LC name authority file and Chicago: "Fuente, Alejandro de la" (sorted under F; checked: LC NAF), "Hippel, Wolfgang von"
(D18 A5), "Heusch, Luc de" (the Kanon example changed), Portuguese under the last element ("Costa, Elisa Maria Lopes da"),
Icelandic under the forename ("Guðmundur Hálfdanarson"). First note in full ("A. de la Fuente"), short form "Fuente".

**A5. Withdrawn.** The curator's record does not assume a journal article (`original_source` is a free citation string,
`original_doi` gives Crossref `isTranslationOf`, which works for a chapter DOI). And the original **has** a summary and ten
keywords (Cambridge Core chapter page, not the PDF) — now in `ostendorf_src_front.md`: the translator translates them
(Keywords "jak w oryginale"), nothing to draft.

## OST-3 · B. Slips in the author's data — for the translation stage (MB: flag to the translator, decide then; kept as written)

- **B1** notes 4, 24 — Galletti's title "Hispanoaméria" → "Hispanoamérica" (Crossref; the journal).
- **B2** note 15 — Fotta, IRSH 65/2 "(2019): 8–10": 2019 is the online FirstView date (08.11.2019) and 8–10 its own
  pagination; the issue is 65/2 (2020), pp. 315–341. *Proposal:* year 2020, range 315–341; the cited pages → D3.
- **B3** note 26 — "Lettre au P.re Paul du Poisson; aux Akensas, October 3, 1727": the author copied the volume's table
  of contents, where Paul du Poisson is the **writer**, not the addressee. Verified in Thwaites vol. 67 (1900; archive.org
  scan): doc. CCI, "Lettre du Père du Poisson, Missionnaire aux Akensas, au Père \*\*\*. Aux Akensas, 3 octobre 1727"; the
  quoted passage ("comme des singes… si c'est une troupe de Bohémiens…") on pp. 314–315, running head "Letter by Poisson";
  the text itself says "He notes". *Proposal:* author Paul du Poisson, title "Lettre au Père \*\*\*", chapter in vol. 67.
- **B4** note 51 — editor "William Cambell" → **William W. Campbell** (catalogue records, archive.org); publisher Baker
  and Scribner, New York 1849 (the publisher is now in refs.json, A2).
- **B5** note 60 — "New Granada" → **New Grenada**, as on the 1831 title page (London: Longman; the full title goes on
  "…, and in the Pacific Ocean; from 1817 to 1830"); the book was published anonymously (Vowell attributed).
- **B6** note 23 — publisher "Wilhelm Braumuller University": garbled; probably "Wilhelm Braumüller,
  Universitäts-Verlagsbuchhandlung" (Wien). LoC (LCCN 66083415) confirms Wien, W. Braumüller; the edition's title there is
  "Hin und her. Hin süsse und vergnügt, her bitter und betrübt…" (Zwettler Codex 420). Place Wien now in refs.json.
- **B7** note 14 — "Universidad Nacional de Litoral" → "Universidad Nacional **del** Litoral" (the university's name).
- **B8** note 57 — "Notes and Documents:" is the journal's section heading, not part of the title (Crossref: "Sir
  Augustus J. Foster and 'The Wild Natives of the Woods,' 1805–1807"). *Proposal:* drop it.
- **B9** note 1 — Matache, Routledge 2026: Crossref has the book online on 15.11.2025. Keep 2026 if the printed imprint
  says so (usual for books out in November). No LoC record yet.
- **B10** typography only, applied (listed in the build report as `srom-as-written` where a field changed): "Racism:(Un)
  uttered" → "Racism: (Un)uttered" (Matache); "Occidentale,en" → "Occidentale, en" (Berquin-Duvallon); "1590s– 1900s" →
  "1590s–1900s" (Fotta); the comma after the closing quotation mark in B8's title (§ 3.1); abbreviated ranges in full
  (§ 3.2); "PhD diss." → `praca doktorska`; "Anonymous" → title first (*The Jamaica Lady*).
- **B11** found while sourcing: Matthews 2018 — the record's publisher is I.B. Tauris (a Bloomsbury imprint; the author
  gives Bloomsbury); Block — LoC has the book as 2018 (the author's 2021 is probably the paperback); Muhlenberg — the record
  gives "Philadelphia: Evangelical Lutheran Ministerium of Pennsylvania…, 1942–58" (the author: Muhlenberg Press 1945);
  O'Reilly's volume: "PLUS, Università di Pisa" (the author: Edizioni Plus); the volume editor is **Guðmundur Hálfdanarson**
  (LC NAF; the author: "Gudmundur Hálfdánarson"). (02.10.2026 18:58) The second editor: the author has "Anne Katherine Isaacs"; she publishes as **Ann Katherine Isaacs** (to confirm in LC NAF). Since v1.13 the bibliography prints editors' full names, so both spellings now show; refs.json keeps the author's forms until MB decides (OST-3).
- **B12** (29.09.2026 17:47, srom-tlumacz E18 [Ostendorf], verified by srom-produkcja) note 41 — Urlsperger: the author's title
  "*Der ausführlichen nachrichten … in America erster*" (Halle, 1751) is volume 1's; her locator "3:979" is right.
  Bolzius's answers are in the **18th Continuation** (Halle 1752, pp. 777–1004), which is part of **volume 3** (collective
  title page 1752, Continuations 13–18, continuous pagination; John Carter Brown Library record on archive.org,
  `derachtzehenteco00urls`); the passage runs pp. 979–980. Proposal: the record describes the whole work — "*Der
  ausführlichen Nachrichten von der königlich-groß-britannischen Colonie saltzburgischer Emigranten in America*", ed.
  S. Urlsperger, Halle 1741–1752 — cited as t. 3, s. 979 (the token as it stands). **Key `urlsperger1751` and the token
  stay either way**: no change to `ostendorf_src.md` or the translation, only refs.json fields. Answers D4.
- **B13** (29.09.2026 17:49, srom-produkcja, found answering E17) text before note 60 — Vowell 1831 (*Campaigns and Cruises*, Notes,
  p. 324, note 14; archive.org `campaignsandcru07vowegoog`, page image read): "resemble **those of the *Zinganées***, or Eastern
  gypsies"; the author quotes "resemble the *Zingances*, or Eastern Gypsies" (a misreading, and "those of" dropped).
  *Chinganéros* is Vowell's spelling. Proposal: the quotation as Vowell prints it (the translation follows the original,
  § 12.2.4). Kartoteka row *Zinganées* (variant *Zingances*).
- **B14** (29.09.2026 17:49, srom-tlumacz E17) text, New Orleans 1802 — the author writes "*Bohemes*"; Berquin-Duvallon's 1803 print
  has *Bohèmes* (srom-tlumacz; not re-checked here). Proposal: *Bohèmes*, as printed. Kartoteka row *Bohèmes*.
- For information, kept: CRS 2/2 (Ostendorf) dated 2019 as the issue (Crossref: published 2.12.2020); "Louisiana
  Bohémiens" (Crossref drops the accent); "Cadiz" without accent in Moreno Alonso's title (not verified).

## C. For the translator and for you (no decision needed)

- Literal notes (Kanon § 8): archival 29, 32 and the first half of 30; press 49, 50, 52, 53, 54, 59 (19th-century US
  newspapers, date form § 8.3 is the translator's); note 14 keeps the URL of the digitised Schmidl manuscript (the PDF's
  link target has `%26` for `&`: the text is right, the link broken).
- Author's prose inside notes (11, 12, 14, 38; lead-ins in 5, 11, 52) stays for translation.
- The author's short form "Gómez Alfaro, et al." prints as the Kanon's three-author short form (§ 7.3); "Cressy,
  *Gypsies*" as "Cressy, *Gypsies…*".
- Loewald, Starika, Taylor "trans. and eds." of two journal articles (note 41) print as "(red.)": the article form has no
  translator slot. Acceptable; say if not.
- Group names: the author italicises *Bohémiens* and *Zigeuner* but not Gitanos/Ciganos (italic in the kartoteka, T6).
  Not in the kartoteka yet: *cingani*, *Zingaros*/*Zingari*, *Zingances*, *Chinganéros*, *Bohemes*, "Gipsies" (spelling
  variant), "Anglo-Romani". Early-modern "Egyptians" → „Egipcjanie” (D13).
- 14 whole-work references (no page) for you to confirm: query sheet, "odwołanie do całości dzieła".
- Side finding (Pahulich, not changed): the improved hyphen rule reads Pahulich's "religio-|political" (Wynter quote) as
  "religio-political"; the frozen `pahulich_src.md` has "religiopolitical". Wynter's own spelling decides; worth checking
  when D17 is applied.

## OST-4 · D. Questions to the author — for the translation stage (with B)

- **D1** Text, Iberian section: "Manuel Moreno Alonso described a Puerto Rican stopover during his 1747 journey between
  Cadiz and Veracruz" — note 25 cites Moreno Alonso, "De Cadiz a Veracruz en **1745**" (1983). Which year? And Moreno
  Alonso is the article's (modern) author: whose journey is it? (comment in the text)
- **D2** Text, Anglo section: Penn "noted in a **1686** promotional tract" — note 35 cites his letter of **1683**. (comment in the text)
- **D3** Note 15 (with B2): Fotta's pages 8–10 in the print pagination (315–341).
- **D4** Note 41: Urlsperger's title ends "erster [Theil]" but the locator is 3:979 (vol. 3). Which part/volume?
  29.09.2026: answered by the originals (B12): vol. 3 is right, the title is volume 1's; nothing to ask the author.
- **D5** Note 44: Tucker's *Blackstone's Commentaries* (1803) has five volumes; pp. 33, 165–66 of which?

## OST-9 · Who stands first in three edited texts (02.10.2026 01:48, srom-produkcja)

MB's test layout (02.10.2026) printed editors in the author's place: n. 34 „H. Dexter (red.), *Mourt's Relation…*”,
n. 41 „K.G. Loewald, B. Starika, P.S. Taylor (red.), *Johann Martin Bolzius Answers…*” (twice), n. 51 „W. Cambell (red.),
*The Life and Writings…*”. Cause: refs.json keyed them as edited volumes (editor, no author), and the style printed any
editor-only item with the editor first. The author's own notes open with the title in nn. 34 and 51 ("*Mourt's
Relation…*, ed. Henry Dexter"; "*The Life and Writings…*, ed. William Cambell"); in n. 41 she puts the editors first
("Klaus G. Loewald, Beverly Starika and Paul S. Taylor, trans. and eds.").
Fixed (Kanon v1.11): `mourt1865`, `clinton1849` → `type: classic` (an edition of a source: title first, „red.” after it);
`loewald1957`/`1958` stay articles, now printed title first with „tłum. i red.” (translator and editors as the author
gives them). Keys and tokens unchanged; the translation is not affected.
Open (MB-decisions OST-9): who stands first. Checked 02.10.2026: Crossref 10.2307/1922111 (Part I) lists Loewald,
Starika, Taylor as authors; 10.2307/1919443 (Part II) the same three plus Johann Martin Bolzius. archive.org's copies of
Clinton 1849 (`lifewritingsofde00clin`, `lifeandwritings00campgoog`) give Clinton, DeWitt and Campbell, William W.
Proposed: title first in all three (as now); Campbell's spelling per B4.
