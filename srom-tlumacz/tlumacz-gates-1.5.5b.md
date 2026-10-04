# Gates: 1.5.5b Fourth text, draft — [Tittel] "Racial and Social Dimensions of Antiziganism: The Representation of “Gypsies” in Political Theory"

Deliverable: a preliminary translation for MB to edit (MB 29.09.2026: go ahead, decisions later):
`work/tittel/tittel_pl.md`, `tittel_front_pl.md`, `tittel_pytania_tlum.csv`, notes sheet `tittel_uwagi.md`
(pages and wordings to look up, choices to confirm, decisions for MB), Word working copy `tittel_robocza.docx`.
Open choices are applied as the intake proposes (`tittel_intake.md` § 3) and listed for MB; nothing waits for MB.

- [x] G1: handoff check passes (structure, notes, citation keys)
  CHECK: ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/check.py --pair work/tittel/src/tittel_src.md work/tittel/tittel_pl.md --refs work/tittel/src/refs.json
  EXPECT: /CHECK OK/

- [x] G2: Polish header data well formed
  CHECK: ~/.venvs/srom/bin/python tlumacz-front_check.py work/tittel/src/tittel_src_front.md work/tittel/tittel_front_pl.md
  EXPECT: /^FRONT OK$/m

- [x] G3: the draft builds, and the translator is reported for the CSV
  CHECK: rm -rf work/tittel/build; ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/build.py work/tittel/tittel_pl.md --refs work/tittel/src/refs.json --pair-src work/tittel/src/tittel_src.md --queries work/tittel/tittel_pytania_tlum.csv --out work/tittel/build --draft >/dev/null 2>&1 && grep -h -c 'Michał|Bartosz||' work/tittel/build/*_report.md
  EXPECT: /^1$/m

- [x] G4: no untranslated English prose left in the body (notes, italics, comments and citation tokens removed; count of "the"/"and"/"of"…)
  CHECK: python3 work/tittel/tit_check.py
  EXPECT: /^leftover English: 0$/m

- [x] G5: every page / wording to look up is marked in the text and listed in the notes sheet (same set)
  CHECK: python3 work/tittel/tit_check.py --marks
  EXPECT: /^marks: (\d+) in text, \1 in review sheet$/m

- [x] G6: re-read against the source, paragraph by paragraph (number and agent, quotation boundaries, negations, dates) — manual
  EVIDENCE: full re-read of `tittel_pl.md` against `src/tittel_src.md` (29.09.2026 04:35); body paragraphs aligned by script (51 = 51, note markers identical in every paragraph); 3 fixes: „debaty prawnicze o to, czy” → „spory prawnicze o to, czy” (syntax); „rozstrzygający przykład na to” → „kluczowy dowód na to” (Hund); "origin myth" once „mit o pochodzeniu”, twice „mit założycielski” → made consistent. Quotation boundaries follow the originals translated from (German Kant, MEW, edicts; the author's English where the original was not reached). Numbers, dates, centuries: `check.py --pair` warnings are only the expected forms (decades „lata 80.”, Roman centuries, „2020/2021”, „t. 3 i 23” in the translator's bracket). Block-quote markers moved before the final full stop (linter NOTE-AFTERDOT, 6); „[...]” → „[…]” in the German of n. 87.
  NOTE 29.09.2026 17:47: time correction — the stamp „04:35” was not read from the clock: this file was committed at 04:33:09 (f3d7bec), so the work was done before then. Evidence unchanged.

- [x] G7: HOUSE terms and the intake's term table applied; group names per kartoteka or listed as open — manual
  EVIDENCE: counts in the draft, comments removed (29.09.2026 04:36): antycygan- 9, antyzygan-/antiziga- 0 (C-0007); urasow-/urasaw- 6, rasializ- 0 (C-0001); „Cygan-” in quotation marks 81, without them only inside source quotations and act titles (Hund, Kant 2×, Marx 3×, Württemberg titles 3×, edict block), as § 12.2.6 wants; „Egipcjan-” 13 (kartoteka, D13); Porajmos 1, Porrajmos 0; Sinti 14; *Zigeuner*/*Zigeiner* italic in text 2; Indus- 4, Hindus- 2 (Kant, OPEN). Open: the form of “gypsy” (capital vs lower case) and the intake § 3 proposals, listed in `tittel_uwagi.md` § 2–3 and in the query sheet.
  NOTE 29.09.2026 17:47: time correction — the stamp „04:36” was not read from the clock: this file was committed at 04:33:09 (f3d7bec), so the work was done before then. Evidence unchanged.

- [x] G8: Word working copy round trip: export → import → pair check OK
  CHECK: cd work/tittel && S=~/.claude/skills/srom-produkcja/scripts && T=$(mktemp -d) && ~/.venvs/srom/bin/python $S/export_work.py tittel_pl.md -o $T/tittel_rt.docx >/dev/null 2>&1 && ~/.venvs/srom/bin/python $S/docx_in.py $T/tittel_rt.docx -o $T/tittel_rt.md >/dev/null 2>&1 && ~/.venvs/srom/bin/python $S/check.py --pair src/tittel_src.md $T/tittel_rt.md --refs src/refs.json 2>&1 | tail -1
  NOTE 29.09.2026 17:43: CHECK rewritten after the cross-module review of 29.09.2026 (finding 2): it exported in place over `tittel_robocza.docx`, the file MB edits (the master once he has), so a re-run would have replaced his edits with the draft. It now exports and imports in a temp dir, as 1.5.3b does; `tittel_robocza.docx` is never written. Same test, same result; gate closed as of 29.09.2026.
  EXPECT: /CHECK OK/
