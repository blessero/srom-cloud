# Pahulich, "Racialization of Roma, European Modernity, and the Entanglement of Empires" (CRS 8/1, 2025) — open points

Stage 1 done 28.09.2026 (srom-typeset). Source: `work/Pahulich.pdf` (CRS 8 (1): 40–61, DOI 10.29098/crs.v8i1.208).
Nothing below blocks the translation; B and C touch refs.json only, A2 and D1–D2 touch a few words of the text.

## A. Needs MB

**A1. Licence of the original — CC BY-NC 4.0.** Crossref gives CC BY-NC 4.0 (from 11.12.2025); the PDF itself carries
no licence or copyright statement. A translation is an adaptation: allowed under BY-NC, but only for non-commercial
use, and the translation note must name the licence (Kanon § 12.2.3 pt 2). Whether SROM's distribution counts as
non-commercial (printed volume for sale?) is MB's call; it also touches D15 (SROM's own licence).
*Recommendation:* ask the author / CRS (crs.ceu.edu) for written consent to the Polish translation; that settles
both the NC question and the note's "podstawa zgody na przekład". Blocks: publication, not the translation.

**A2. Two note markers side by side (printed notes 1 and 2).** The first sentence ends with an author-date citation
and the author's own note: "…across Eastern Europe (Demeter et al. 2000; …; Kóczé 2020).[1]" → after conversion
"Europe¹.²" (in Polish "Europe¹²."). The Kanon has no rule for this. (a) keep two notes; (b) one note: the citations,
then the author's note text. *Recommendation:* (b). If (b), I change `pahulich_src.md` before srom-tlumacz drafts
(notes renumber from 2 on: 145 notes).

## B. The author's bibliography — errors kept as written until MB decides

Proposal for each; "approve B" = all proposals, each recorded in refs.json `srom-as-written` (the author's form stays
on record, the build lists it), as for Ndiaye.

| # | entry | the author's form | proposal (source) |
|---|---|---|---|
| B1 | Clark 2004, volume title | *The Role of the Romanies Images and Counter Images of ‘Gypsies’ / Romanies in European cultures* | *The Role of the Romanies: Images and Counter-Images of ‘Gypsies’/Romanies in European Cultures* (Crossref/LUP) |
| B2 | Holler 2015, title | Historical Predecessors of the Term ‘Anti-Gypsyism | closing quote: …‘Anti-Gypsyism’ |
| B3 | Kóczé 2020, co-editor | Angéla Kócze | Kóczé (the same person, the author of the chapter) |
| B4 | Horváthová 1964 | Emilia; *Cigáni Na Slovensku: Historiko-Etnograficky Náčrt*; Vytadel’stvo Siovenskej Akademie Vied | Emília; *Cigáni na Slovensku: historicko-etnografický náčrt*; Vydavateľstvo Slovenskej akadémie vied (library catalogues) |
| B5 | Wippermann 1997, title | Wie Die Zigeuner: Antisemitismus Und Antiziganismus Im Vergleich | Wie die Zigeuner: Antisemitismus und Antiziganismus im Vergleich (German capitalisation) |
| B6 | O’Keeffe 2014, title | Fin-De-Siecle | Fin-de-Siècle (Crossref: "Fin-de-siècle") |
| B7 | Gheorghe 1991, title | Roma-Gypsy Ethnicity in Eastern Europe. (Nationalism in Central and Eastern Europe) | drop the parenthesis: it is the theme of that *Social Research* issue, not part of the title |
| B8 | Césaire 2000 | DOI 10.4324/9781003101406-19; "Edited by Robin D. G. Kelley" | drop the DOI: it is a chapter of a 2022 Routledge reader (*Postcolonialism*), not this book (Crossref). Kelley wrote the introduction, he did not edit it — keep as the author gives it, or drop the editor role (no data added) |
| B9 | Bielikov 2003, title | (16–20 st.) | (XVI–XX st.), as on the dissertation (catalogue record) |
| B10 | Bielikov 2003; Marsh 2008 (dissertations) | no place → `[BRAK MIEJSCA]` in the proof | Donetsʹk; London (seat of the named university) — or ask the author |
| B11 | Matache 2020, URL | …/roma-slavery/?fbclid=IwAR16… (a Facebook tracking parameter) | the URL without `?fbclid=…` (checked: it opens) |

## C. The Kanon applied where the author's form differs — for information (reversible, all in `srom-as-written`)

- **Cyrillic in the apparatus → ALA-LC without ligatures** (§ 9.6); the author uses another romanization ("Istoriya
  Tsygan: Novyy Vzglyad", "Byelikov", "Kistyakovskiy"). Checked against catalogues / the volume itself: Barannikov
  1931 (*Цыганы СССР*, RSL/Wikipedia: the author's "Tsygany" is right), Bielikov 2003 (disslib), Bielikov 2008 (the
  volume's title page and contents, NAN Ukraïny, t. 15, s. 24–56), Demeter et al. 2000 (NEB), Kireĭ/Serdiuk 1984,
  Kistiakovskiĭ 1879 (pre-reform title page: *malorossīĭskīĭ*), Zelenchuk 1979, Zinevych 2001 (UIZh 2001 nr 1,
  s. 40–52), Dalʹ 1883 (RSL record, 2nd ed. 1883–1884). **Not verified:** Chėrvinski 2008 (no catalogue record found;
  article title read as Belarusian, journal as Russian — both reconstructed from the author's Latin forms) and Dalʹ
  1883 in pre-reform spelling (title page not seen; modern spelling used). Titles in sentence case, places Moskva,
  Kyïv, Kiev (1879), Kishinev, S.-Peterburg.
- Kistiakovskiĭ 1879: the author gives "ed."; entry under the editor. Bielikov 2008: "edited by P. S. Sokhan’, et al."
  — Sokhanʹ is the executive editor of the series' board; printed as red. P.S. Sokhanʹ (the board not listed).
- **Title glosses in [ ]** (§ 4.3, optional): the author's English glosses of Cyrillic and Slovak titles are given in
  Polish (my translations of the original titles, not of the English glosses; srom-tlumacz asked to review).
- "Tom VI" → t. 6 (§ 11); abbreviated page ranges written in full (§ 3.2); dissertations: "(praca doktorska)".
- DOIs: all 24 checked against Crossref. Wrong: Césaire (B8). Later reissues of the same text (acceptable, listed):
  Kóczé 2020 (De Gruyter 2022), Mróz 2015 (De Gruyter 2016), Willems 1997 (Routledge 2014), Shohat/Stam 2012 (NYU
  Scholarship Online 2020).

## D. The text — questions for the author (via MB)

- **D1. Note 2 of the original (printed 37):** "(1992, 81; Crowe 2007, 109)" — year and page with no author. Probably
  Fraser 1992 (cited twice in the paragraph the note belongs to). Kept as written, Crowe keyed; comment in the
  text. Ask the author.
- **D2. "Jenkins and Leroy (2021)"** (section 3) is not in the author's bibliography. Probably D. Jenkins, J. Leroy
  (eds.), *Histories of Racial Capitalism*, Columbia UP 2021 — not added (§ 0). Ask the author for the reference.
- D3. Wynter quotation (printed note 21): the PDF breaks "religio-|political" at a line end; the hyphen is kept.
  Check against Wynter 2003, p. 309 if at hand (low priority; the translation is unaffected).

## E. Kanon gap (MB, low priority)

- **E1. Web sources: publication date.** § 8.6's pattern has no publication date, so Matache 2016 (FXB Center, "5
  October 2016") prints without it, while the newspaper article (Matache 2020) prints 05.10.2020. Proposal: print the
  date of a web text when the author gives it (`„Serwis”, 05.10.2016, URL`) — a CSL change + Kanon § 8.6 line.

## Settled in processing (28.09.2026)

- Acknowledgements (an end section in the original) → the one title note (Kanon § 7.1); srom-tlumacz puts the
  translation note before it in the same block (D12).
- Author-date → footnotes (§ 7.1): 146 notes = 142 converted + the author's 4 (now printed 2, 37, 67, 128); 25
  "Ibid." resolved to the work cited just before (each checked by hand); 17 year-only parentheses ("… Law and Kovats
  state … (2018, 78)") resolved to the author named in the sentence (each checked); 2 prose parentheses ("for similar
  inquiry, see …") → notes with the prose; "(viii)", "(74)" → the work named in the same sentence. Every step:
  `prep.py` (log `prep_log.md`), `pahulich_pre_citemap.md`.
- Extraction: PDF text layer fixed where it broke (tool changes with tests, commits a64edb3…57c8f08); every word
  compared with the PDF: nothing lost.
