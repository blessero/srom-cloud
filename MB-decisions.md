# Decisions for MB — all SROM modules

Only what is still pending and only MB can decide. Any module appends. Whichever session receives MB's
decision on an item, or is asked to resolve it itself, **removes the item** once it is actually resolved; the
decision is recorded where it takes effect (Kanon, handover, handoff item, commit). No history here.

Rules:
- **Grouped by text.** Each article has its own `## Text: <Author> — <short title> (<source>)` section; items that
  concern no single text go under `## Journal-wide` or `## Tooling and workflow`. An item about two texts goes in
  each text's section as a one-line pointer to the full item. Remove a text's section when it is empty.
- New item: `### D<n> — <subject> (dd.mm.yyyy HH:MM, <module>)`, then the question, the options, the module's
  recommendation, what it blocks, and where the detail is (file + item ID). Next free number: **D22**.
- A partial answer (item still open) is a new line under the item: `- dd.mm.yyyy HH:MM DECIDED: … (MB)`.
- Times (from 28.09.2026 16:45) are local time from the machine clock (`date '+%d.%m.%Y %H:%M'`); older entries
  keep their date only.
- `MB-decisions-archive.md` keeps the text of items closed before 27.09.2026; it is not appended to.

## Needs MB now
- **Pahulich:** D17 — nothing in it blocks the translation.
- **Scheffknecht:** D18 — German stage-1 test.
- **Ostendorf:** D19 — A1 (CC BY-NC, as D17 A1) and A2 (14 imprint gaps by hand); nothing blocks the translation.
  D21 — the translation is drafted; your choices are collected, none blocks your Word edit.
- **Tittel:** D20 — nothing blocks the translation (CC BY 4.0); A1 (acknowledgements as the title note) and A4 (the MEW
  siglum) touch the source the translator works on.

## Text: Pahulich — CRS 8/1 (2025)
Stage 1 done, source with srom-tlumacz (T18).

### D17 — Pahulich (CRS 8/1, 2025), stage 1: open points (28.09.2026, srom-typeset)
Source frozen and handed to srom-tlumacz (T18); none of this blocks the translation. Detail and proposals:
`srom-typeset/work/pahulich/pahulich_queries.md` (items A–E).
- A1 **licence of the original: CC BY-NC 4.0** (Crossref; the PDF has no statement). Is SROM's distribution
  non-commercial, and do we ask the author/CRS for consent? Recommendation: ask for written consent. Blocks
  publication (the translation note's licence line), not the translation.
- A2 a converted citation and the author's note 1 stand side by side (printed 1 and 2): keep two notes, or merge.
  Recommendation: merge (then notes renumber, new T-item).
- B1–B11 errors in the author's bibliography (titles, a wrong DOI for Césaire 2000, garbled Slovak imprint, missing
  places of two dissertations, a Facebook tracking parameter in a URL): kept as written; "approve B" = all proposals.
- D1–D2 questions to the author: an author-less "(1992, 81)" in the original's note 2 — by the rule of 28.09 (Kanon
  § 7.1) the work cited before it is Červinski 2008 (year differs), so it goes to Fraser 1992, the only 1992 work,
  flagged; "Jenkins and Leroy (2021)" missing from the bibliography — Crossref: D. Jenkins, J. Leroy (eds.),
  *Histories of Racial Capitalism*, Columbia UP 2021, DOI 10.7312/jenk19074 (or its Introduction), for the author to
  confirm.
- 28.09.2026 DECIDED: E1 (web publication date) — Kanon § 8.6: dated web texts print their publication date, taken
  from the page when missing (MB).

## Text: Scheffknecht — Neujahrsblätter Lustenau 1 (2010)
Stage 1 done (German test), not handed to srom-tlumacz.

### D18 — German stage-1 test (Scheffknecht, Neujahrsblätter Lustenau 1, 2010): open points (28.09.2026, srom-typeset)
Stage 1 done, source frozen in `srom-typeset/work/scheffknecht/`; **not handed to srom-tlumacz**. Detail and proposals:
`srom-typeset/work/scheffknecht/scheffknecht_queries.md` (A–E).
- A1 stage 2: srom-tlumacz is EN→PL. Keep as a test (recommended), a DE→PL trial in srom-tlumacz, or a human translator.
- A2 rights: no licence; the imprint allows quotation with attribution only. Recommendation: written consent of the author
  and the Historisches Archiv Lustenau before publication; image permissions (VLA, Staatsarchiv Augsburg) at stage 3.
- A3 **29 of 35 works have no publisher** (German practice) → `[BRAK WYDAWCY]`, which Kanon § 0 keeps out of typesetting.
  Recommendation: the publisher-sourcing step you planned (catalogue lookup, each item for your approval). Will recur with
  every German/Austrian/Swiss source.
- A4 series (14 works): no Kanon form, the CSL prints nothing. Recommendation: "(Series, n)" at the end of the description.
- A5 German "von" (von Hippel): no Kanon rule. Recommendation: library form "Hippel, Wolfgang von", sorted under H.
  - 28.09.2026 21:28 DECIDED (MB via D19 A4: "whatever the custom is"): Kanon § 9.3/§ 9.5 (commit ea50df6) — "Hippel, Wolfgang von",
    sorted under H. To apply in `work/scheffknecht/refs.py`: hippel1995 `non-dropping-particle` → `dropping-particle`
    (not done by the Ostendorf session: another session's files).
- A6 archive abbreviations (VLA, HoA, HistA, PfA, StaatsA, StadtA) never expanded in the source (Kanon § 8.1); HoA unknown.
- A7 a stray raised "1" after the text's last word: delete (recommended) or ask the author. A8 early printed lists held in
  archives stay literal (recommended).
- B1–B7 slips in the author's data kept as written ("approve B" = all proposals).
- 28.09.2026 17:35 pointer (srom-typeset): A3 and A5 recur for Ostendorf — D19 A2 (places/publishers, CUP Chicago
  style) and D19 A4 (particles, sorting); one decision for both.

## Text: Ostendorf — The Romani Atlantic, ch. 3 (CUP 2026)
Stage 1 done, source with srom-tlumacz (T19, T20); open access CC BY-NC 4.0.

### D19 — Ostendorf, "Familiar Outsiders Abroad" (The Romani Atlantic, CUP 2026), stage 1: open points (28.09.2026 17:35, srom-typeset)
Source frozen in `srom-typeset/work/ostendorf/` and handed to srom-tlumacz (T19). Detail, evidence and proposals:
`srom-typeset/work/ostendorf/ostendorf_queries.md` (A–D).
- A1 **rights: © Cambridge University Press, not open access** (Cambridge Core terms; no licence). Permission of CUP and
  the author needed (Kanon § 12.2.3 (2): basis of consent in the translation note). Recommendation: ask now; you decide
  whether srom-tlumacz starts before permission. Blocks publication (and the translation, if you say so).
- A2 **place missing in 44 works, publisher in 14** (58 of 83; CUP's Chicago notes: publisher without place, old works
  place without publisher) → `[BRAK …]`. Same as D18 A3. Recommendation: the sourcing step (catalogue lookup, item by item
  for your approval) for both texts.
- A3 two printing conventions with no Kanon line, implemented provisionally because the CSL dropped data (`decisions.md`
  23): an edition of a source prints its editor after the title (`red.`; "trans. and ed." → `tłum. i red.`); a chapter
  without an author (a letter in an edited volume) opens with its title, the volume's editor after the volume title.
  Recommendation: approve, then a line each in Kanon § 7.2 (alternative for editions: `oprac.`).
- A4 particles and sorting ("de la Fuente" under D; "A Gentleman of Elvas" and titles "A …" under A): decide with D18 A5.
- A5 the original is a book chapter (Kanon § 12.2 and the master CSV assume a journal article): curator check before the
  record; no abstract/keywords in the original → translator drafts both, author approves the English (§ 12.2.2).
- B1–B10 slips in the author's data, several verified (Galletti "Hispanoaméria"; Fotta's year/pages are FirstView;
  note 26 is a letter **by** du Poisson, checked in Thwaites vol. 67; "Cambell" → Campbell; "New Granada" → Grenada;
  "Braumuller University"; "de Litoral"; "Notes and Documents:"): kept as written; "approve B" = all proposals.
- D1–D5 questions to the author: 1747 vs 1745 and whose journey (Moreno Alonso, text vs note 25); Penn 1686 vs 1683
  (note 35); Fotta's print pages; Urlsperger "erster" vs vol. 3; Tucker's volume.
- 28.09.2026 21:28 DECIDED (MB): A3 — `tłum. i red.`, edition `red.`, unsigned texts flagged: Kanon § 7.2/§ 9.4 (ea50df6). A4 — custom of
  the name's language (LC NAF, Chicago): Kanon § 9.3/§ 9.5 (ea50df6). A5 withdrawn (the curator's fields fit a chapter;
  the original has summary and keywords online). B1–B11, D1–D5 → the translation stage (T20). A1 corrected by srom-typeset:
  the chapter **is open access, CC BY-NC 4.0** (Cambridge Core) — now the same question as D17 A1. A2: 44 of 58 sourced
  (LoC, evidence in refs.json); **14 left for MB by hand** — list in `ostendorf_queries.md` A2.
- 28.09.2026 21:29 correction (srom-typeset): 43 values sourced (not 44); the 14 left are unchanged.

## Text: Tittel — On_Culture 10 (2020)
Stage 1 done, source with srom-tlumacz (T20).

### D20 — Tittel, "Racial and Social Dimensions of Antiziganism" (On_Culture 10, 2020), stage 1: open points (28.09.2026 21:09, srom-typeset)
Source frozen in `srom-typeset/work/tittel/` and handed to srom-tlumacz (T20). Detail, evidence and proposals:
`srom-typeset/work/tittel/tittel_queries.md` (A–D).
- A1 the author's note 1 (acknowledgements only, called from the first sentence) set as the **note on the title** (Kanon
  § 7.1), notes renumbered 1–100 (original 2–101). Recommendation: approve (done provisionally, one line to undo).
- A2 **rights: CC BY 4.0**, author keeps copyright (the journal's page; the PDF has no licence; the repository record is
  behind a bot check — please confirm once in a browser: URN urn:nbn:de:hebis:26-opus-160255). No DOI (URN). Recommendation:
  proceed; courtesy notice to the author. Blocks nothing.
- A3 one gap: Ruch 1986 (unpublished dissertation, "Freiburg", university not named) → `[BRAK WYDAWCY]`. Catalogue step
  (D18 A3 / D19 A2) or the author.
- A4 the author's siglum "MEW 23" ("hereafter abbreviated as"): the notes print the Kanon short form; recommendation: the
  translation leaves out the parenthesis. Alternative: a siglum rule in the Kanon. The MEW series number is not printed
  until D18 A4 (series).
- A5 Kant's Akademie-Ausgabe references ("s. 420 / AA VII 324–325") kept as the author gives them; no Kanon line for
  standard-edition references. Recommendation: keep; a Kanon line later.
- A6 journal-wide gaps: (a) several places "Köln/Weimar/Wien" (slashes as written; Polish practice: en dash); (b) "Zob.
  *Ibidem*" with a capital after a lead-in (also Ndiaye 2×); (c) statutes and law collections put in "Źródła drukowane i
  prawne" — also Kant, Marx, Grellmann (18th–19th-c. sources)?; (d) series → D18 A4; (e) "van" → D18 A5 / D19 A4.
- B1–B10 slips in the author's data, most verified (Larrimore's journal is the Supplementary Volume; *Philosophers on Race*
  is Blackwell, not OUP; *Kant-Studien*; "Berliner" vs *Berlinische Monatsschrift*; Zöller, and the volume dated 2007 not
  2010; Strauß/Strauss; Mayall's imprint; Decker's co-authors added, verified): kept as written; "approve B" = all proposals.
  Also: four DOIs the author does not give — add? (C).
- D1–D3 questions to the author: Ruch's university; the Kant volume's year; "Berliner Monatsschrift".
- The Geulen lecture (n. 31): its date could not be read by script (bot check) — please look once (Kanon § 8.6).

### D21 — Ostendorf translation: choices collected for MB (29.09.2026 03:41, srom-tlumacz)
Draft done without MB's feedback, as MB asked (29.09.2026): `srom-tlumacz/work/ostendorf/ostendorf_robocza.docx` (Word copy),
`ostendorf_pl.md`. Everything is in the notes sheet `srom-tlumacz/work/ostendorf/ostendorf_uwagi.md`; nothing blocks editing.
- Assumed, to confirm: author's pronouns she/her (from MB's vol. 18 translation of Ostendorf); translator credit Michał
  Bartosz (as Ndiaye).
- S1, S2 (uwagi § 1): wording and page of the Polish editions — Scott, *Guy Mannering czyli Astrolog* (NK 1975), Pratt,
  *Imperialne spojrzenie* (WUJ 2011). Only MB can look these up.
- Terms (uwagi § 3): title „Swojscy obcy za oceanem”; „cygańska zasłona”; skrypty rasowe; obcy miejscowi; antyczarność;
  wolni kolorowi; *voyageurs*; „Wielka Obława”. Recommendation: as drafted; termbase rows after MB's word.
- Group names (uwagi § 4, E17): Anglo-Romani → „angielscy Romowie”; *Bohémienne(s)* for women.
- Quotation annotations (uwagi § 2): „tłum. z przekładu angielskiego” (no „autorki”) where the author quotes someone
  else's published English translation — the Kanon has no such formula. Recommendation: accept; a Kanon line via E17.
  Also: search further originals (Anchieta, Pasqualigo, Schmidl, Bolzius, Elvas)? Recommendation: yes for Schmidl and
  Bolzius (German prints are digitised), no for the rest.
- Doubts in the source, to the author (uwagi § 5; `ostendorf_pytania_tlum.csv`): Paucke "Polish Jesuit" (born in Winzig /
  Wińsko, Silesia); Moqoit "in today's Paraguay" (San Javier, Santa Fe, Argentina); Loskiel's German ≠ author's English;
  "typographies", "crows". With stage 1's B1–B11 and D1–D5 (D19, T21), which MB asked to be reminded of now.

## Journal-wide (policy, not tied to one text)

### D21 — [general] InDesign house style v3: speaker's name and affiliation in italics vs Kanon § 3.4 (29.09.2026 03:39, srom-typeset)
Vol. 18 sets the speaker line "> Name" bold italic (Panelant) and affiliations in italics (Uni; in Ellis the author's
affiliation too). Kanon § 3.4: proper names – names, institutions – are never italic. House style v3 keeps the vol. 18
look (styles *Mówca*, *Afiliacja*) for continuity. Options: (a) keep italics – the Kanon rule is read as a rule for
running text, not for display lines (then one sentence in § 3.4 says so); (b) roman – Mówca bold roman, Afiliacja
roman (one value each in `style_spec.json`). srom-typeset's recommendation: (a), the usual journal convention and
18 volumes' practice. Blocks nothing until the first issue is typeset. Detail: `srom-typeset/docs/HANDOVER-typeset.md` § 4.

### D15 — Licence: withdraw the CC BY-NC-ND option? (28.09.2026, srom-typeset)
Kanon § 13.2 marks it "DO ROZSTRZYGNIĘCIA – kolegium redakcyjne". Today the author chooses CC BY / BY-NC / BY-NC-ND
(default BY-NC). Options: (a) keep the choice; (b) withdraw ND, keep BY / BY-NC; (c) one licence for the whole journal.
srom-typeset's recommendation: (b) at least — ND rules out the DOAJ Seal (§ 13.2); (c) is the dominant practice.
Blocks nothing in stages 1–2; matters for the licence field of the master CSV and the Crossref deposit.
Kolegium's decision, via MB. Detail: `srom-typeset/.claude/skills/srom-kanon/references/kanon-redakcyjny.md` § 13.2.

### D16 — PILNE before any open-access announcement: vol. 18 copyright-transfer clause (28.09.2026, srom-typeset)
Kanon § 13.2: the printed *Informacje dla autorów* in vol. 18/2025 say authors transfer copyright to the Redakcja;
the licence agreement says the opposite. The text in print and on the website must be **replaced**, not supplemented.
Needed from MB: the replacement wording (or who writes it) and where it goes (website page; vol. 19 front matter).
srom-typeset can draft the Polish text on request. Blocks: the OA announcement. Detail: Kanon § 13.2.

## Volume 19 planning

### D6 (c) — Vol. 19 translation shortlist (27.09.2026, srom-tlumacz)
Deferred by MB (26.09.2026). (a) and (b) are closed.

## Tooling and workflow (scheduled, waiting for a later moment)

### D5 — Translator credit: what is still open (27.09.2026, srom-tlumacz)
Curator skill updated (C1 items 1–3, 5). Waiting, by MB's decision, until the rest is finalised: showing the
translator on the WordPress page (C1 item 4) and the desktop upload of the new curator .skill.
Question before that upload: **is mu-plugin v2.3 the current one?** The .skill MB attached on 27.09 carried v2.0; the
update was built on the copy installed for Claude Code (v2.3, checked again 28.09.2026: `srom-scholarly.php` Version 2.3),
so uploading it brings v2.3 and locked decision #4 to desktop Claude. This is the skill's copy, not what runs on the site.
Detail: `curator-update-2026-09-27/CHANGES.md` ("Which version this is built on").
- 28.09.2026 DECIDED: the live site is old (untouched since about June 2026). No upload now: when the work here is
  finished, MB updates the curator skill in desktop Claude and the plugin on the site together. (MB)
