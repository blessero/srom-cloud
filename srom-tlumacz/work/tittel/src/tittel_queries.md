# Tittel, "Racial and Social Dimensions of Antiziganism" (On_Culture 10, 2020) — stage-1 test 5: open points

Stage 1 done 28.09.2026 (srom-typeset). Source: `work/Racial_and_Social_Dimensions_of_Antiziga.pdf` (23 pp.; On_Culture:
The Open Journal for the Study of Culture, Issue 10 (2020): Metaphors of Migration, published 21.04.2021; Giessen, GCSC;
no DOI — URN urn:nbn:de:hebis:26-opus-160255). Endnotes with full Chicago-style citations (place and publisher given),
no bibliography.

Files: `tittel_src.md` (frozen source: 5 sections, title note + 100 notes; 97 keyed — 25 of them partly literal —,
3 literal), `refs.json` (63 works, from `refs.py`, typed from the notes), `tittel_src_front.md`,
`tittel_src_robocza.docx` (Word working copy, round trip lossless), `build/tittel_src_korekta.docx` (source proof: the
Polish apparatus as it will print), `build/tittel_src_pytania.md` (query sheet), `key_log.md` (every prep and keying
change), `doi_check.txt` (the 4 DOIs of the source: Crossref / DataCite). Pipeline: `pdf_extract.py` → `key.py` (prep +
keying) → `check.py --keyed` → `build.py --source` → `export_work.py`; `refs.py` → refs.json. `wordcheck.py`: every word
and number of the PDF is in the extraction (10 896 tokens; the only differences are line-end hyphens, all decided).

**Note numbers.** The original numbers its notes 1–101; note 1 is the author's acknowledgements (A1), which SROM sets as
the note on the title. In `tittel_src.md` the notes are therefore **1–100 = the original's 2–101** (original = label + 1).
Below: "n. 9 (orig. 10)".

What this PDF broke, fixed in the toolchain with tests (commits 27cc558, 5bd5794, 7f671f5, 25dfb19): headings with the
journal's underscore ("_Abstract", "_Endnotes", "1_Introduction") — the front matter and the endnotes heading had stayed
in the text; front matter over two pages; justified block quotations read as verse (each line a paragraph, hyphens
kept); a URL closed by ">" swallowing the next space; URL hyphens decided by the same address elsewhere in the document;
"anti- “gypsy”". The keyed check had four holes, found by a mutation test on this text: a page after "here:", Kant's
Akademie-Ausgabe page, a wrong volume of the same author's work, and a non-bare Ibidem (all passed silently; now errors).
Print: no full stop before the author's bracketed remark after a citation ("s. 63 (my translation)." — also Ndiaye n. 77).

## A. Needs MB

**A1. Note 1 (acknowledgements) is now the note on the title** (Kanon § 7.1: "przypis autora do tytułu (np.
podziękowania)"). In the original it is called from the end of the first sentence ("…through state measures.¹"), but it
only thanks the issue's editors and reviewers. Done provisionally in `key.py` (one line to undo); the translator puts the
translation note first in the same block (D12). *Recommendation:* approve. Alternative: keep it as numbered note 1 (then
the labels go back to 1–101).

**A2. Rights: CC BY 4.0 — no permission needed; nothing blocks the translation.** The PDF carries no licence; the journal's
page (journals.ub.uni-giessen.de/onculture/about, read 28.09.2026): "available under the Creative Commons license (CC BY;
4.0)", "the authors hold the copyright and publishing rights without restrictions". The article's own repository record
could not be read by script (the Giessen repository and the URN resolver answer with a bot check): please look at it once
in a browser (URN urn:nbn:de:hebis:26-opus-160255) to confirm the licence for Issue 10. The translation note follows the
Kanon § 12.2.3 formula for CC BY 4.0 ("niniejszy przekład stanowi zmianę utworu"). No DOI: the note and the CSV record give
the URN (and the current repository address; the permalink in the PDF now redirects to a broken address). *Recommendation:*
proceed; a courtesy notice to the author.

**A3. One gap: Ruch 1986** (n. 20, orig. 21), "Zur Wissenschaftsgeschichte der deutschsprachigen »Zigeunerforschung« …
(Freiburg, 1986), unpublished dissertation" — the university is not named → `[BRAK WYDAWCY]` (Kanon § 9: a thesis names
its university; also where the copy is kept, if it is a typescript). *Recommendation:* the catalogue step (D18 A3 / D19 A2)
or ask the author. Everything else has place and publisher.

**A4. The author's siglum "MEW".** N. 49 (orig. 50): "(hereafter abbreviated as MEW 23). I will quote from the German books
(MEW 1–43) and use the translations from the Marx Engels Archive <URL>." The later notes ("MEW 23, 746") are keyed to the
work, so they print the Kanon short form ("Marx, *Das Kapital…*, s. 746") and the sentence about the abbreviation points
to nothing. *Recommendation:* the translator leaves out "(hereafter abbreviated as MEW 23)" (a DO SPRAWDZENIA comment
stands there in the source); the sentence about the German edition and the Marx archive stays. Alternative: keep MEW as a
siglum (Kanon has sigla only for archives, "dalej:"; would need a line and a Wykaz skrótów entry). Related: the series
"Karl Marx / Friedrich Engels: Werke 23 / 3 / 42" is in refs.json but not printed (series: D18 A4) — until then the MEW
volume number is lost from print.

**A5. Kant's Akademie-Ausgabe references** (n. 32, 37, 39, 40, 42, 43, 44): the author gives the page of the Cambridge
Edition and then the Academy edition ("420/AA VII 324–325", "163 (FN)/AA VI 136–137 (FN)"). Kept as the locator:
`s. 420 / AA VII 324–325`, "(FN)" → `przyp.` No Kanon line for standard-edition references (Kant AA, also MEW, classical
texts). *Recommendation:* keep this form now; a line in Kanon § 7.2 later (usual Polish form: "AA VII, 324–325").

**A6. Kanon gaps this text raises (journal-wide).**
(a) Several places of publication: "Köln/Weimar/Wien", "London/New York", "Dessau/Leipzig" (8 works) — kept with slashes
as written; the Kanon has no line. Polish practice: an en dash ("Köln–Weimar–Wien"). Decide once; the refs change is one
line per work.
(b) "Zob. *Ibidem*" / "Zob. Ibidem" with a capital after a lead-in (here n. 30 and 66; also Ndiaye, 2×): Polish usage writes
"zob. ibidem" in lower case after the lead-in? The build keeps the capital (CSL term); no Kanon ruling.
(c) Sections of the bibliography: I put the English statutes (Tomlins, Raithby) and the Württemberg law collections (Zeller
and Reyscher) in "Źródła drukowane i prawne" (IV). Kant, Marx, Grellmann, Biester and Rüdiger (18th–19th-century printed
sources) stay in "Literatura przedmiotu" (default). Move them to IV?
(d) Series (Palgrave "Human Rights Interventions"?, "Schriftenreihe 12", MEW, "Sammlung … Gesetze Bd. 12/13"): D18 A4.
(e) Particles: "van Baar", "van Gorkom" — sorting with D18 A5 / D19 A4.

## B. Slips in the author's data (kept as written in refs.json; "approve B" = all proposals)

- **B1** n. 2 (orig. 3): "*The Securitization of the Roma in Europe*. Human rights interventions" — the second part is not
  the title (Crossref: title only); probably Palgrave's series *Human Rights Interventions* (not verified: the publisher's
  page needs a login). Set as series in refs.json (not printed, A6 d); the as-written form recorded.
- **B2** n. 9 (orig. 10): Larrimore 1999 appeared in the *Canadian Journal of Philosophy*, **Supplementary Volume** 25
  (Crossref, DOI 10.1080/00455091.1999.10716832); the author: "Canadian Journal of Philosophy 25". *Proposal:* container
  "Canadian Journal of Philosophy. Supplementary Volume", vol. 25.
- **B3** n. 9 (orig. 10): Bernasconi, "Kant as an Unfamiliar Source of Racism", in *Philosophers on Race* (2002) — the
  publisher is **Blackwell** (Crossref: Wiley, DOI 10.1002/9780470753514.ch8), not "Oxford University Press". *Proposal:*
  Blackwell Publishers, Oxford (place as the book gives it: to confirm).
- **B4** n. 14 (orig. 15): the journal is ***Kant-Studien*** (Crossref, DOI 10.1515/kant.1997.88.1.60), not "Kant Studien".
- **B5** text (section 2) "the publisher of the famous *Berliner Monatsschrift*" vs n. 18 (orig. 19) "*Berlinische
  Monatsschrift*" — the journal is the *Berlinische Monatsschrift* (the note is right). *Proposal:* the translation uses
  "Berlinische Monatsschrift"; kept as printed in the source.
- **B6** n. 32, 39, 42, 43 (orig. 33, 40, 43, 44): the volume editors are Robert B. Louden and **Günter Zöller** (Crossref,
  DOI 10.1017/CBO9780511791925), the author writes "Gunter Zoller"; Crossref dates the volume **2007**, the author 2010
  (a reprint? — to confirm with the author or the copy she used).
- **B7** n. 20/24 (orig. 21/25): the co-editor is "Daniel Strauß" in one note and "Daniel Strauss" in the other: one form
  (Strauß) in refs.json. "(im Auftrag der Gesellschaft für Antiziganismusforschung e.V.)" after the editors (n. 20) left
  out of the description (it belongs to the volume's title page, not the editors' names).
- **B8** n. 61 (orig. 62): Mayall 1995, "(Hertfordshire: Gypsy Research Centre Univ. of Hertfordshire Press)" —
  Hertfordshire is a county, not a town; the imprint looks garbled (University of Hertfordshire Press, Hatfield?). Not
  verified (not in Crossref). *Proposal:* catalogue lookup.
- **B9** n. 1 (orig. 2): "Oliver Decker et al." — the chapter's five authors (Decker, Kiess, Schuler, Handke, Brähler) are
  in refs.json (verified on the Heinrich-Böll-Stiftung's page of the chapter): Kanon § 9.1 lists all authors in the
  bibliography; the note prints "O. Decker i in.".
- **B10** typography in the source, no action (the translation sets Polish quotation marks): headings 4 and 5 open with a
  closing quotation mark ("4_”Gypsies” …"); "these ’findings’" (section 2).

## C. For information

- **Prep changes** (`key_log.md`): "inter-views" → "interviews", "pre-sents" → "presents" (line-end hyphens after a prefix);
  "landdamaging" → "land-damaging" (a line-end hyphen in a coined compound for *Landschädliche*: the hyphen is the
  author's — no English word "landdamaging"); the BBAW URL in n. 8 (orig. 9) with the typesetter's hyphen removed
  ("kant-ein-ras-sist" gives 404, "kant-ein-rassist" 200, checked 28.09.2026).
- **Prose around citations** stays for the translator; two citations standing in the author's sentence are in brackets
  (n. 21: "…in his book in 1782 ([@rudiger1782])"; n. 22: "In contrast to what Ruch stated ([@ruch1986, s. 103])").
  Lead-ins: See → Zob., cf. → por. (contract). Ostendorf's source kept two "see" in prose (n. 11, 36): a small
  inconsistency there, harmless (the translator writes "zob.").
- **Query sheet** (`build/tittel_src_pytania.md`): 27 citations of a whole work (for the editor to confirm), the Ruch gap
  (A3), and one web text: Geulen's lecture (n. 31) — its date could not be read (the repository blocks scripts; a bot check
  I did not pass): please read it once in a browser (Kanon § 8.6), or mark it undated. The BBAW page (n. 8) has no date:
  marked `srom-undated`. The row "cytat bez numeru strony" for Amīn (n. 47) is a false alarm: the marker follows a chapter
  title in quotation marks, not a quotation — dismiss.
- **DOIs the author does not give** (Kanon § 9.7): Röttgers 1997 (10.1515/kant.1997.88.1.60), Kleingeld 2007
  (10.1111/j.1467-9213.2007.498.x), van Baar et al. 2019 (10.1007/978-3-319-77035-2), Bernasconi 2002 (see B3). Not added
  (nothing enters refs.json unapproved): add them?
- **For the translator** (T-item): quotations from works with Polish editions (Kanon § 12.2.4 a) — Kant (several essays),
  Marx (*Kapitał*, *Grundrisse*, *Ideologia niemiecka*), Horkheimer/Adorno, possibly Federici and Balibar/Wallerstein; the
  German originals quoted in n. 37, 81–93, 95 and the author's "(my translation)"; "Egyptians" in the English acts =
  early-modern "Egipcjanie" (kartoteka); "Porrajmos"; the author writes “gypsy/gypsies” in scare quotes, lower case.
- **Side finding (Ndiaye, no action):** re-running the extractor on the Ndiaye PDF gives "African-American" where the
  frozen `ndiaye_src.md` has "African- American" (an older extractor's join, one place). The translation does not contain
  the phrase; nothing to do unless the source is re-frozen.

## D. Questions to the author (via MB)

1. Ruch 1986: at which university was the dissertation submitted (A3)?
2. Kant, *Anthropology, History, and Education*: the 2007 volume or a 2010 reprint (B6)?
3. "Berliner Monatsschrift" in the text = the *Berlinische Monatsschrift* of the note (B5)?
