# Polonizacja — the second pass (language), a separate stage

A separate pass that makes a finished, checked draft read as native Polish academic prose. Trial: Pahulich,
10.11.2026 (121 changes, judged a substantial improvement); corrected after MB's Word edit of pp. 42–44 showed the
pass had over-edited and drifted from the source (12.11.2026, `workspace/srom-tlumacz/polonizacja_brief.md`).
The rules below exist to stop both.

## When
- **Only on MB's explicit request** („polonizacja: <text>”, „szlif językowy”, „language pass”), in a **fresh session**,
  after the first pass (translation, steps 1–7) is complete. Never in the same session as the first pass, never
  started by a request to translate. (SKILL.md § Two passes.)
- Terms, facts, editions and checks are done by then, so the pass has one concern only: good, native Polish that
  still says what the English says. It reads only: the md or MB's master, `src/<id>_src.md`, the termbase, this file,
  the text's STATUS section and notes sheet.
- Before MB's first Word edit: work in the md (exact-match replacements, part by part).
- After MB has edited: never touch the md. Deliver the pass as tracked changes (author „Claude”) in
  `<id>_robocza_v2.docx`, MB's master untouched (step 6, `outputs.md` § Back).

## Protected text (never polished)
- **Everything MB has edited in Word.** The text's STATUS section names the stretches („edited by MB: never
  re-polished, proofread only”). There the pass may only fix slips (rule 7), never style.
- Quotations (Polish editions pending or MB's own decision), HOUSE terms, facts, content. A wording problem at the
  edge of a term or a quotation goes to MB as a question, never changed silently. Exception: a fidelity correction
  inside a quotation (a lost conjunction, a case forced by a corrected verb) is allowed and logged as `fix`; style
  inside a quotation never (MB 15.11.2026, PAH-104).

## Procedure
1. Snapshot the md (or note the master's sha256). Split the unprotected body into parts of about 1,500–2,000 words
   (smaller where the prose is dense) at paragraph boundaries; number them once and record the boundaries in the
   notes sheet and the parts' state (polished / left / MB-protected) in the text's STATUS section. Later sessions
   continue from the next part; step 2 is done once, in the first session.
2. Before part 1, scan the whole text for tics that only show across parts (sentence-initial markers, recurring
   verbs and nouns) and decide one treatment for each.
3. Per part: read sentence by sentence with the English beside it; list the changes, **each with its fault class**
   (below); apply only those that pass the revert test (rule 2); then the audit (rule 5).
4. After each part: `tlumacz-polish_check.py <before.md> <after.md> --src src/<id>_src.md --log <id>_polish_log.tsv
   [--protect "<start>..<end>"]` (one log row per change: part, paragraph, class, before, after; exit 0 needed), pair check,
   build --draft, draft check; one log line in the notes sheet (`<id>_uwagi.md`
   § Szlif językowy: part, changes per class, reverts, questions).
5. Borderline cases: at most a few per part, **numbered once and never renumbered**; MB decides them at the end in
   one batch.

## Rules
1. **A change names its fault.** Classes: *grammar* (agreement, case, aspect/tense clash, a „wprawdzie” without its
   pair); *calque* (name the English it copies); *ambiguity* the Polish creates (and the English does not); *echo*
   (a repeated non-term word within a sentence or two); *order* (word order that hampers reading); *register* (a
   break in the elevated academic register); *drift* (the Polish says less, more or other than the English).
   „Sounds better” is not a class. A change without a class is not made.
2. **Revert test.** Before applying: is the draft wording *wrong* by one of the classes? Merely different → leave it.
   Synonym swaps (analizuję / przyglądam się, regionach / obszarach) are out. Pahulich: about six such swaps undid
   good draft wording, and MB had to restore it.
3. **Stance and logic markers stay.** *Notably, Importantly, Therefore, Ultimately, In particular* keep a Polish
   equivalent („Warto zauważyć, że”, „Co istotne”, „zatem”, „ostatecznie”, „zwłaszcza”); a marker is rephrased,
   never deleted. Only purely additive ones (*Furthermore, Also*) may go when the logic is plain.
4. **Fidelity floor.** Every content word of the English keeps a home in the Polish. Reporting and key verbs one to
   one (*discuss* „omawiać”, not „pisać o”; *construct* „skonstruować”; *contribute to* „przyczynić się do”). No
   added words („konkretną”). Quoted spans are compared word by word with the English after the pass: a change
   inside a quotation is a logged fix or it is reverted. First-use glosses of HOUSE rows present. The rule binds the
   pass's own wording: a faithful draft equivalent is not swapped for the listed one („wnieść wkład w” stays).
   Claim-strength verbs (*suggest*, *propose* vs *argue*, *theorize*): a numbered question for MB, never a silent change.
5. **Audit after each part.** Diff before/after; re-read only the changed sentences against the draft and the
   English; revert every change that fails rule 2 or rule 4. Report the number of reverts in the log line.
6. **HOUSE terms keep the termbase's word order** („rasizm antyromski”); collocations that are not terms may move an
   adjective, e.g. to keep a relative pronoun next to its noun („pod rasową logikę, którą…”).
7. **After every MB round:** proofread only the sentences MB changed (diff of the import against the previous md)
   for slips (agreement, typos, a dropped „że”, a „zaś” opening a clause, commas), and return them as one list or as
   tracked changes in a `_v2` copy, before any further pass.

## Stance markers (list read by `scripts/tlumacz-polish_check.py`)
English: Notably, Importantly, Therefore, Ultimately, In particular, Thus, Hence. A source paragraph with one must keep
its Polish markers through the pass (rule 3); extend the line when a text needs another equivalent.
Polish markers: warto zauważyć | warto podkreślić | co istotne | istotne | co ważne | co znamienne | znamienne | zatem | więc | tak więc | stąd | toteż | ostatecznie | koniec końców | zwłaszcza | w szczególności | szczególnie

## What to look for (suspects, not rules: every text is different)
- **Grammar:** case agreement with *jako*; masculine-personal agreement; verb–noun collocation; pronoun reference
  („jego” pointing at the wrong noun; a pronoun with no antecedent at all); a missing „że” after „Warto zauważyć,”;
  parallel members kept parallel (*class-based or solely social*).
- **Word choices to check** (from the 13.11.2026 calibration): „Tymczasem” for *Meanwhile* (adversative: „natomiast”);
  „przywracać uwagę czemuś”; „skupienie na” (*focus on*); „zwykle … sporadycznie” (*tend to*); „cel” for *target*;
  „znaczenie X … dla Y” with „dla” far off; *emphasize* „podkreślać”; *rates* „wskaźniki”; *including* „w tym”.
  Consistency: „Europa Wschodnia/Zachodnia” capitalised one way; „/ ” spacing. *Anti-Roma attacks*: „ataki
  antyromskie” and „ataki na Romów” are both right (MB 15.11.2026); neither is a suspect.
- **„który” chains:** two or more in one sentence = suspect; a lone short defining clause becomes an adjectival
  participle („system, który spycha” → „system spychający”) only when the paragraph already has three or more „który”. Adverbial -ąc participles expressing a result are the suspect, not
  the adjectival ones.
- **Calques:** of discourse markers rendered word for word („Mówiąc konkretnie”); of collocations („szeroka
  publiczność” → „ogół społeczeństwa”, „brać na cel”, „warunki wstępne”); of English plurals („konteksty”,
  „eksploracje”); „historycznie” for *historically* („na przestrzeni dziejów”); „zaledwie” or „nie tylko” for *not
  simply X but Y* („nie tyle X, ile Y”); genitive of a group for a named tradition („myśl czarnych” → „czarna myśl
  radykalna”, C-0055).
- **Nominal style and the agentive passive** („odnotowywane są przez badaczy”): prefer a verb; to keep an English
  topic-first order, use Polish object–verb–subject order („…wyobrażenia… nawiedza zwłaszcza logika…”).
- **End weight:** long qualifiers go last, not in dashes mid-clause; a verb is not parked at the end of a 40-word
  sentence.
- **Complex sentences may be rebuilt outright.** When the English is ambiguous, search the author's own text for
  the reading she supports; when both readings converge, a „co” referring to the whole clause keeps both.
- **Echoes and inconsistency:** one rendering per event or concept within a paragraph („wypędzenie”, not
  „wygnanie” then „wypędzenie”).
- **Register is MB's, not the pass's.** Register and synonym lifts (≈30 of MB's edits on pp. 42–44: nie sposób,
  stanowi, bądź, tym samym…) stay out of the pass: that is where the 10.11.2026 pass over-edited. The gap is
  recorded, not to be "fixed" later (MB 15.11.2026, PAH-104).

## Test before a new text (calibration)
When the rules change, calibrate on a **held-out stretch**, not one the rules were drawn from (Pahulich pp. 42–44 are
training data now: a test on them is circular). The pass runs blind: it reads this file only, not MB's version or the
method brief; MB's term decisions are applied to the input first; MB edits the stretch afterwards and the two are
compared: what MB changed that the pass missed, and what the pass changed that MB left or reverted. Adjust the rules and
suspects first (MB 15.11.2026, PAH-104; report `pahulich/kalibracja_20261113/raport.md`).
