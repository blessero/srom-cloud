# RIP of a Polish original — formatting plus the editorial checks

Scenario A of `SKILL.md`, for any text written in Polish: articles (Parts I–II) and the reviews and chronicles of
Part III. A translated article gets its quotations, names, transcription and facts checked at srom-tlumacz's intake;
a Polish original goes 1 → 3 → 4 (`stages.md`) and skips TRANS, so those checks are done here, in RIP, and the text
reaches MB as checked as a translation does. The editorial assessment (is it good enough, what must the author change)
comes before this, from srom-zizek: `deep` for an article, `review` for a book review (`../../srom-zizek/references/`).
Written 15.11.2026 (MB: "the ripping procedure … skipping all parts that are only necessary for translations").

## In
- The author's file, copied into `work/<id>/orig/` as received (never edited; MB's inbox file stays where it is).
  DOCX goes straight to step 1a. **ODT, RTF or DOC**: convert first,
  `soffice --headless --convert-to docx --outdir work/<id>/ work/<id>/orig/<file>`; `docx_in.py` reads DOCX only
  (`rip-pitfalls.md`, C55).
- `<id>` = the author's surname (lower case, ASCII); a new three-letter code and the text's sections in `STATUS.md` and
  `MB-decisions.md` (workspace `CLAUDE.md` § Questions for MB), with the volume and the Part (I–III) as MB gave them;
  not given → "volume and Part: MB" in the STATUS section, not a guess.
- The editorial assessment if one exists (srom-zizek `volumes/<vol>/deep/<slug>-5.md` or `reviews/<slug>.md`): a revised
  file is checked against its *Do autora* list, point by point, in the intake (§ Verification 8).
- MB's standing rulings R1, R4–R6 (workspace `CLAUDE.md` § Questions for MB) were made for translated texts; whether they
  bind Polish originals too is GEN-144 point 2. Until he answers, a session follows them and says so in the notes sheet.

## Steps
1a → 2 → 3 → 4b (footnoted) or 4a (author-date) exactly as in `SKILL.md` § Scenarios A/B → **V** (verification) →
**L** (language) → 5 (Word copy) → MB's edit → INJECT (`stages.md` § 3: `docx_in.py` of his master, 2, 6). Before 1a,
read `rip-pitfalls.md`. The Lite variant (notes literal) only for a text whose notes are already kanon-clean; a review
with notes is keyed like an article (Kanon § 1: reviews lose only the abstract and keywords, not the bibliography).

## Verification (V)
Recorded in `<id>_intake.md` (English): srom-tlumacz's intake skeleton (`../../srom-tlumacz/references/outputs.md`)
with § 3 Terminology dropped and two sections added: **Names and transcription**, **Facts**. Each line: what was
checked, against what, the outcome. A bibliographic or historical claim needs two independent sources (record ids in
the sources register); a missing datum stays missing. Nothing in the author's text is corrected silently (Kanon § 0).

1. **Bibliographic data** — the step-3 tools (`lookup.py dois`, `imprints`, `webdates`, `missing`). A slip confirmed
   by a named record is corrected, the author's form kept as `srom-as-written` (standing ruling R1; the author is told
   in the letter).
2. **Quotations** — every quotation of four or more words, one row each in `<id>_quotes.tsv` (columns as in
   srom-tlumacz `outputs.md` OUT-QUOTES; classes here: `PL` a Polish source, wording and page checked against the
   edition cited; `OWN-TR` the author's own translation of a foreign source: `[tłum. własne]` once, Kanon § 4.2;
   `PL-EDITION?` a Polish edition exists that the author did not use: a query, never a change; `VERSE`). A wording only
   MB's books can confirm goes to the volume's quotations checklist (R4).
3. **Names and transcription** — group names against the kartoteka (Kanon § 6; the author's form stays in the text,
   § 6.3; a missing variant: a proposed row in the notes sheet); persons' names and their inflection; non-Latin scripts
   per Kanon § 9.6 and § 4.3: Polish transcription (WSO PWN) in the main text, ALA-LC in notes and bibliography, **no
   Cyrillic in the apparatus**; places by KSNG with Polish exonyms in the text, the title-page form in the apparatus
   (§ 7.2); historical places from srom-tlumacz `sources/prng/` as in its intake. Each conversion is a tracked change
   (L below): it changes the author's text.
4. **Facts** — dates, figures, events, institutions, laws, attributions (who coined a term): each checked against two
   sources, or listed as unverified. A wrong or doubtful one → an author query (`<id>_pytania.csv`) and a Word comment
   in the `_v2` copy; never changed in the text. Name the community, the period and the source (srom-naczelny
   § Editorial work).
5. **Web sources** — live, dated, archived where the Kanon asks (§ 8.6; `lookup.py webdates`).
6. **Kanon points the build cannot see** — headings (§ 2), italics of foreign words and the reversed italics (§ 3.4),
   Romani terms and glosses (§ 5), ethnonyms (§ 6.1: pejorative exonyms only inside quotations), abbreviations (§ 11).
   Parts I–II also: Polish abstract ≤ 1000 characters, 5–10 keywords, the English abstract a translation of the Polish
   one, not a paraphrase (§ 1 items 7–9): a mismatch is an author query.
7. **Doubts** — anything else that looks wrong, with what you would do.
8. **A revised file** — each point of the *Do autora* list: answered / partly / not, with the anchor.

## Language (L)
The author's voice is the text: no polonizacja (that pass exists for translations). Two levels, both as **tracked
changes** (author „Claude”) in `<id>_robocza_v2.docx`, made with srom-tlumacz `scripts/tlumacz-track.py` on a copy of
the clean export (`<id>_robocza.docx`), never in the md:
- **Korekta**, always: spelling, inflection, agreement, punctuation (Kanon § 12.3, PWN), typos, missing or doubled
  words; the § 9.6 / § 4.3 conversions from V3. One change per fault.
- **Styl**, only for a clear fault: an ungrammatical, broken or ambiguous sentence; the change carries a Word comment
  saying why. Register, word choice and rhythm that are merely not ours stay as the author wrote them; at most a
  handful of suggestions go to the notes sheet instead.
House typography that `normalize.py` applies (quotation marks, dashes, spaces, ellipses) is not tracked: it is listed
in `_norm.md`. The notes sheet gives the counts by class (korekta / styl / Kanon). MB accepts or rejects in Word and
saves the result as the master `<id>_robocza.docx` (the clean export renamed `_old1`).

## Not done (translation only)
TRANS; termbase rows; `check.py --pair`; `tlumacz-front_check.py`; `tlumacz-draft_check.py`; the hand-off to
srom-tlumacz (no `src/` copy, no RIP → TRANS log line); polonizacja; the translation note.

## Out
In `work/<id>/`: `<id>.md` (SROM-MD), `refs.json`, `_norm.md`, `<id>_intake.md`, `<id>_quotes.tsv` (if any
quotation), `<id>_pytania.csv` (format: srom-tlumacz `outputs.md` OUT-QUERIES; `adresat` autor / redakcja),
`<id>_uwagi.md` (Polish, for MB: srom-tlumacz's notes-sheet skeleton, sections 1, 2 and 4, plus "Poprawki językowe" with
the counts), `<id>_robocza.docx` (clean export) and `<id>_robocza_v2.docx` (tracked corrections and comments: the file
MB opens), `build/` (`build.py <id>.md --refs refs.json --queries <id>_pytania.csv --out build --draft`: proof, report,
query sheet). STATUS.md: the text's section, stage "RIP done, waiting for MB's Word edit"; questions for the author go
into one letter (R5).

## Gates
`work/<id>/<id>_gates_rip.md` (unlazy format), ALL MET before the reply: `IMPORT OK` (or every CHECK line read) ·
`normalize.py` 0 flags · `CITEMAP OK`, or `check.py --keyed` `CHECK OK` + `MUTATIONS CAUGHT n/n` · `check.py` `CHECK OK`
· `build.py --draft` `PASS`, report read · intake has all its sections · one quotes row per quotation (count both) ·
the `_v2` copy imports (`docx_in.py` to a temp dir) and its check is `CHECK OK` · every S-item in the notes sheet has
its comment or query and the reverse · the sources register has a line for every outside source used.

## Book reviews (Part III)
The same procedure, plus:
- **No abstract, no keywords** (Kanon § 1). The English title of the review is still needed for the master CSV: the
  author's, or drafted and shown to MB as a Word comment (R6).
- **The header** (the book under review): the Kanon has no rule yet (GEN-144). Until MB decides, the vol. 18 layout
  (Kledzik, Paszko): after the review's title, one paragraph each — the book's author (as on the title page; editors
  `red.`), the title in italics with subtitle, publisher, place year, `ss.` page count, ISBN. Plain paragraphs in the
  SROM-MD before the first body paragraph; MB gives them the header style in InDesign as in vol. 18 (C55 asks for a
  style). Every element from a catalogue record of the book (the national library of the country of publication, or
  WorldCat) and the publisher's page, two sources; the ISBN check digit computed. A book in Cyrillic: GEN-144's
  recommended form (ALA-LC, the Polish translation of the title in square brackets, place as on the title page) until
  MB decides; the original-script form goes in the notes sheet.
- The book's title in the running text: Kanon § 4.3 (original in italics; Cyrillic in Polish transcription; a Polish
  translation in brackets at the first mention).
- Order of work: srom-zizek `review` first. When its verdict asks only for small changes, the assessment and this RIP
  may run in one session, and the *Do autora* points and the RIP queries go to the author in one letter (R5).
