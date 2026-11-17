# Review — the editor's assessment of a submitted book review (Part III)

For a book review (recenzja, omówienie) submitted to SROM's Part III, and on MB's word for a review essay or a
chronicle note. Part III is not peer-reviewed (knowledge base § Structure and peer review): this read is the editor's,
and it decides what goes back to the author. Written 15.11.2026 (MB: reviews "done right", without the whole apparatus
of a deep review).

**Why not a card or a deep review.** A card compares candidates for the block (scores, fit with the concept); a deep
review is a staged referee read of a long argument, with a blind subagent and a rebuttal. A review of 1,000–4,000 words
needs one careful read and checks against the book: one session, no subagents, one file. A review essay that argues a
thesis of its own over more than about 4,000 words: ask MB whether he wants `deep` instead.

**What a good review is** (the standard every section below applies): it tells the SROM reader what the book is —
genre, scope, sources, method, structure — accurately and in proportion; it judges the book and argues the judgement,
strengths and weaknesses with reasons and examples; it places the book among what Polish and international readers
already have; its facts are right; it is readable. A review is not asked for a method section or a thesis; a review
that only retells or only praises fails the second point, however well written, and that is the commonest fault.

## Before writing
1. `extract.py` the file (ODT: convert to DOCX first, `soffice --headless --convert-to docx`; C55) and read the whole
   text from `text/<slug>.txt`.
2. Identify the book: a catalogue record (the national library of the country of publication; WorldCat; BN for
   Polish books) and the publisher's page — author and name forms (a pseudonym: both), title and subtitle, publisher,
   place, year, pages, ISBN (compute the check digit). Two sources.
3. What can be known of the book without holding it: the publisher's description and table of contents, other
   reviews, the author's other work. Say plainly whether the book itself was seen; MB may hold it (a Look-up only if a
   finding depends on it).
4. `grep` `context/srom-abstracts.tsv` for the author, the book and its subject (has SROM reviewed it, or its author,
   before?); `context/polish-field.md` for the Polish lens.
Rules 1–10 of `SKILL.md` hold, rule 10 above all: an unpublished review goes to no outside tool; searches carry short
conceptual queries, never its sentences.

## Output: `volumes/<vol>/reviews/<slug>.md`
First line `review · <dd.mm.yyyy> · text: text/<slug>.txt` (so `check.py` finds the text). About 600–1,500 words
before *Do autora*. Anchors: 5–10 verbatim words per finding. Severity L / M / m.

1. **The book and the review** — two or three lines: what the book is, who wrote it, what the reviewer concludes.
2. **Identification** — the review's header against the records, element by element (a table); every difference, with
   the record that settles it.
3. **Description** — is the book accurately and proportionately described (what is covered, what is missing; a claim
   about the book's content that no source confirms is marked "not verified: book not seen").
4. **Evaluation** — does the reviewer judge, and argue the judgement; strengths and weaknesses named; the book placed
   in the literature (Polish and international, SROM's back catalogue); claims about the field each with a retrieved
   source (rule 3).
5. **Facts** — every checkable claim (dates, figures, events, names, who coined a term, quoted terms in other
   languages): checked against two sources, or listed as unverified. This list goes to the RIP (srom-produkcja
   `references/polish-original.md` § Verification 4), so it is not checked twice.
6. **Form** — the title (does it say what the review is about), structure and length, register (a personal, essayistic
   voice is welcome where it carries the judgement; asides and colloquialisms that do not are noted), the apparatus
   (notes, missing references). Language errors only as a count with two or three examples: correcting them is RIP's
   (§ Language).
7. **Non-scholarly** (rule 8; record, don't weigh): ties between reviewer, author and publisher; whether the book is
   available to Polish readers (language, translation); images the review relies on (a cover: rights, srom-ikonograf).
8. **Verdict** — *przyjąć* / *przyjąć po drobnych poprawkach* / *poprawki zasadnicze* / *odrzucić*, with the
   load-bearing reasons.

## Do autora
In Polish, the points to send, most important first; nothing SROM-internal. MB edits it before anything is sent. When
the RIP of the same text runs (polish-original.md § Book reviews), its queries go into the same letter (R5).

Short and collegial, as MB writes (his cut of the Bijak letter, 15.11.2026, kept about two thirds of the draft):
- Plain paragraphs, no numbers, no bold headings. Related small points share one paragraph (page numbers wanted and
  a missing source: one paragraph).
- Each point is the ask, with at most one clause of reason. One example, not a list of three; a tentative one as a
  question: „może coś w reportażach budzi wątpliwości (proporcja dokumentu i narracji literackiej?)”.
- Soft forms: *Prosimy o* for the main asks, *Dobrze byłoby…*, *wymagałoby*, *zapewne*. A query as a plain question
  with what the record says: „Chodzi zapewne o X? Jest też Y.” Not „Prosimy o potwierdzenie, który…”.
- Short names after the first: SR, EiK; the book's author is not named again.
- Leave out what the editor does anyway: a slip with an obvious fix (a date, a typo), house transcription and name
  forms, the language edit, choices the editor can make. An R1 notice is one short sentence („Dodajemy Dyskursus jako
  wydawcę”).
- Where the records disagree (pages 189, 190, 192), ask with the figures; don't impose one.

## Sources
Every record and page used, with URL or record id; also in the workspace sources register.

## After writing
`python3 "$Z/check.py" volumes/<vol>/reviews/<slug>.md` (`--online` only for DOIs of published works) → 0 missing,
0 close. One line in the text's STATUS.md section: verdict, file. No card, no `pool.md` row: the pool is for selection.
