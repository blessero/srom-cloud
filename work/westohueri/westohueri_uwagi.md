# [West Ohueri] "Peripheral whiteness and racial belonging and non-belonging" (Off White, MUP 2024, ch. 6) — stage-1 test 6: open points

Stage 1 done 29.09.2026 04:11 (srom-produkcja); MB's answers of 29.09.2026 applied (see the end). Source: `work/Peripheral whiteness and racial belonging and non-belonging.pdf`
(manchesterhive download, 18 pp. = printed pp. 138–155; each page carries a download stamp). Chapter 6 in C. Baker,
B.C. Iacob, A. Imre, J. Mark (eds), *Off White: Central and Eastern Europe and the Global History of Race*, Manchester
University Press 2024, DOI 10.7765/9781526172211.00013 (book data from Crossref and the chapter page).
Files: `westohueri_src.md` (frozen source: 6 sections, 68 endnotes → footnotes, 66 keyed — 7 of them partly literal —, 2
literal), `refs.json` (52 works, from `refs.py`, typed from the notes: the chapter has no bibliography),
`westohueri_src_front.md` (title, author, book, licence, abstract, 10 keywords), `westohueri_src_robocza.docx` (Word
working copy; round trip identical), `build/westohueri_src_korekta.docx` (source proof: the Polish apparatus as it will
print), `build/westohueri_src_pytania.md` (query sheet: 13 quotations without a page, 48 whole-work citations),
`key_log.md` (every change), `doi_check.txt` (16 DOIs against Crossref). Pipeline: `pdf_extract.py` → `key.py` →
`check.py --keyed westohueri_pre.md westohueri_src.md` → `build.py --source` → `export_work.py`; `refs.py` → refs.json.
`wordcheck.py`: every word and number of the PDF is in the extraction (only the "Notes" heading dropped); the
publisher's HTML full text (found by MB) agrees paragraph for paragraph, word for word and in italics.
`mutate_keyed.py`: every mutant of the keying caught.

What this PDF broke, fixed in the toolchain with tests (commits 950f46e, 9163315, 4a088a2): a small-capitals font's text
layer ("1000 bce" for BCE); `check.py --keyed` read MUP's "40:3 (2021)", "2nd ed." and "26 May 2020" as lost pages, and —
found by a mutation test on this text — **did not notice a work dropped from a note citing several, or a key swapped for
another work named in the same note** (now both fail, also with the author's short forms "Galaty, *Memory*"); the query
sheet did not see quotations in ‘single quotes’ with the marker after the stop (2 → 13 rows); an Ibidem after "See" with
the sentence going on ("Zob. Ibidem, for more on …", n. 53) is now printed as the short form. Regression: the five earlier
PDFs extract identically, their keyed checks pass, their Ibidem handling is unchanged.

## A. MB

**WOH-1 · A1. Rights: CC BY-NC-ND 4.0 — the ND blocks a published translation without permission.** Crossref and the page stamp:
CC BY-NC-ND 4.0 from 28.05.2024. Under the licence a translation is "Adapted Material", and ND allows sharing the chapter
only unchanged; NC is Pahulich's question (D17 A1). So, unlike Pahulich, Ostendorf and Tittel, this one needs **written
permission** of the rights holder (the author and/or Manchester University Press — the copyright line is on the book's
copyright page, behind a bot check). Then the translation note (§ 12.2.3 (2)) gives the basis of consent, not the licence.
Recommendation: ask the author and MUP (its rights department) now; you decide whether srom-tlumacz
starts before permission. Blocks publication.

**WOH-2 · A2. Front matter.** Affiliation and copyright line are not in the chapter PDF; the book's "Notes on contributors" and
copyright page are behind a bot check — please copy both once in a browser. The abstract (online, 1,508 characters) is
longer than § 1 pkt 7 allows: the Polish is shortened by the editors, the English stays (§ 12.2.2). Ten keywords online.

**WOH-3 · A5. Names.** João Helion Costa Vargas (n. 68): Brazilian compound → § 9.5 sorts under Vargas (Crossref/LC form "Vargas,
João H. Costa"); not expressible in CSL-JSON (srom-md.md) — the bibliography sorts him under C. Set by hand at stage 3, or
accept.

**WOH-4 · A6. Two audiovisual works** typed per § 8.7 (film): Card 2020 (a film, "reż. K. Card", n. 9) and Hall & Jhally 2002 (a
recorded lecture, n. 66, the two names as the author gives them). The § 8.7 pattern prints no producer/distributor (BFD
Productions; Media Education Foundation are dropped). OK?

**GEN-9 · A8. Reprint years not printed (journal-wide gap).** Robinson "2000 [1983]" and Linné "1964 [1759]": the first-edition
year is in refs.json (`original-date`) but the CSL does not print it and the Kanon has no line. Proposal for § 7.2:
"Przedruk: rok wydania, po nim rok pierwodruku w nawiasie kwadratowym: … 2000 [1983]." (then one CSL change + test).

**GEN-10 · A9. DOIs.** 16 DOIs added from Crossref (§ 9.7: obligatory for every item that has one), each with volume, issue and
pages equal to the author's (`doi_check.txt`; `srom-sourced` in refs.json). More in C2. Same question as D20 C (Tittel).

## WOH-5 · B. Slips in the author's data and text, kept as written ("approve B" = all proposals)

- B1 n. 3: "Sevati Trubeta" → Sevasti (Crossref; the article's byline).
- B2 n. 5: "Nira Yural-Davis" → Yuval-Davis (Crossref).
- B3 n. 24: "J. Kramer" → J. Cramer (the Weinheim publisher of the 1964 facsimile); "[1759]": the 10th edition is dated 1758
  (vol. 1; vol. 2 1759) — author (D5).
- B4 n. 41: "East European Politics and Society" → … and Societies (Crossref).
- B5 n. 44: "Journal of Southeast European and Black Sea Studies" → Southeast European and Black Sea Studies (Crossref).
- B6 n. 11: Todorova's updated edition (2009) was published by Oxford University Press in New York (Crossref/Oxford
  Academic); the author writes "Oxford". Kept.
- B7 n. 67: the URL has no "https://" — added (the address answers, redirecting to its dated path; `srom-as-written`).
- Text (for the translator, not data): B8 "Cedric Robsinon’s" → Robinson; B9 "Pavli Qeshku" (text) vs "Qesku" (n. 62; the
  lexicographer is Qesku); B10 n. 26 "Frankenburg" → Frankenberg; B11 "what it means to be feel black" (a word too many);
  B12 "demonstrated by recent national data shows that between 90 and 95 per cent…" (garbled clause); B13 p. 138: "(‘Shqipëria,
  tani, është e prishur’ (‘Albania is now ruined’)." — the first parenthesis is never closed; B14 n. 50 "Isa Blumi." and
  n. 58 "Garner, Steve." (stop / inverted name in a note; no data change).
- Checked, no slip: "Iljazz Fishta" is the article's byline (Crossref); Tochka's "c.1906–1924"; Blumi 2018's volume is
  *Nostalgia, Loss and Creativity…* in the series *Modernity, Memory and Identity in South-East Europe* (Crossref lists both).

## C. Data we could add (proposals; nothing added) — C1: WOH-5, C2: GEN-10

- C1 chapter ranges (Crossref): Blumi 2018 37–71 (DOI added, A9); Zakharov & Law 2017 1–15; Bucur 2010 398–412. Not found:
  Malcolm 2002, Misha 2002 (*Albanian Identities*), Hysa 2010 (*Historični seminar 8*).
- C2 DOIs of books and chapters without pages from the author: Zakharov & Law 10.1057/978-1-137-47692-0_1; Bucur
  10.1093/oxfordhb/9780195373141.013.0024; Todorova 10.1093/oso/9780195387865.001.0001; Mëhilli
  10.7591/cornell/9781501714153.001.0001; Maghbouleh 10.1515/9781503603431; Rexhepi 10.1215/9781478023913; Wekker
  10.1215/9780822374565; Pierre 10.7208/chicago/9780226923048.001.0001; Kettler 10.1017/9781108854740; Turda 2010
  10.1057/9780230281332; Turda & Weindling 10.1515/9786155211041; Kalmar 10.1332/policypress/9781529213591.001.0001; Costa
  Vargas 10.5749/j.ctv3zp0cg. Not proposed: Frankenberg (the DOI is the 2010 digital edition's), Galaty (two DOIs),
  Bhattacharyya (a later platform DOI).

## WOH-6 · D. Questions to the author

- D1 The quotation "reinforced a *Tosk* [southerner] sense of power and later superiority which still permeates Albanian
  society today" (before n. 53) has no source. Blumi, "Politics" (n. 52)? Which page? (DO SPRAWDZENIA comment in the text.)
- D2 n. 49 "my forthcoming work, *Albania in Red, Black, and White* (manuscript in progress)": is it the book published as
  *Encountering Race in Albania: An Ethnography of the Communist Afterlife* (Cornell University Press 2025, Crossref)? If so,
  cite it? (comment in the text)
- D3 Pages for the quotations cited without one — query sheet `build/westohueri_src_pytania.md` (13 rows: nn. 8, 12, 14, 20,
  22, 25, 27, 30, 35, 36, 44, 52, 62); not caught by the sheet, same question: n. 37 (Ibid., after "signaled the general
  will…"), n. 56 (Berisha's 1992 speech via Kajsiu — also: the speech's own source?).
- D4 n. 14: the chapter's pages (1–15?) and the quotation's page.
- D5 n. 24: Linné's 10th edition 1758 (B3).

## E. For the translation (srom-tlumacz)

Group names: Roma, Romani, Balkan Egyptians / Egyptians (kartoteka: Egipcjanie (bałkańscy), present-day group), and the
Albanian words the author analyses — *jevg*, *jevgjit*, *evgjit* (slur for Egyptians), *gabel* (pejorative for Roma),
*dorë e bardhë* / *dorë e zezë* — not in the kartoteka. Gheg/Tosk (Albanian subgroups). "Vaso Pasha" is the Ottoman-title
form of Pashko Vasa. The quotation 'Feja e Shqyptarit asht Shqyptaria' is glossed by the author "The religion of Albania
is Albanianism" (literally "of the Albanian"). Interlocutor's "je bere si jevg" without Albanian diacritics (je bërë) —
their words, kept. n. 26 prints "Wekker (Wekker, *White Innocence*)": the author's name in the sentence and in the
citation — rephrase in Polish.

## Decided by MB (29.09.2026), applied

- A3 the dissertation's place "Austin, TX" (sourced; refs.json `srom-sourced`) — approved.
- A4 n. 29 "see also Baker, this volume" → cited as C. Baker, *Through the Balkans to Christchurch…*, in *Off White*, pp.
  328–347, DOI 10.7765/9781526172211.00023 (`baker2024`, data from Crossref and the chapter page).
- A5 the author's name: **"Ohueri, Chelsi West"** (as Crossref): notes "C.W. Ohueri", short form "Ohueri", sorted under O;
  the text's "West Ohueri, ‘Zor’" is the author's own form in the original notes.
- A7 block quotations roman — except what the Kanon sets in italics inside them: the Albanian words in the three
  fieldwork statements (*Jevgjit*, *jevgjit* ×2, ‘*je bere si jevg*’; Kanon § 3.4 foreign words and a foreign exonym).
  The main text keeps the author's roman ‘jevg’ etc. in quotation marks — for the translation stage (§ 3.4, E).
- A1 MB will ask the author and MUP for permission to translate (ND).
