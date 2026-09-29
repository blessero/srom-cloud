# Gates: 1.5.3b Second text, draft — Ostendorf, "Familiar Outsiders Abroad"

Deliverable: a preliminary translation for MB to edit, as for Ndiaye: `work/ostendorf/ostendorf_pl.md`,
`ostendorf_front_pl.md`, `ostendorf_refs_tlum.json`, `ostendorf_pytania_tlum.csv`, `ostendorf_quotes.tsv`, notes sheet
`ostendorf_uwagi.md`, Word working copy `ostendorf_robocza.docx`. MB's decisions are collected, not awaited (29.09.2026).

- [x] G1: handoff check passes (structure, notes, citation keys, declared additions)
  CHECK: ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/check.py --pair work/ostendorf/src/ostendorf_src.md work/ostendorf/ostendorf_pl.md --refs work/ostendorf/src/refs.json --refs work/ostendorf/ostendorf_refs_tlum.json
  EXPECT: /CHECK OK/

- [x] G2: Polish header data well formed
  CHECK: ~/.venvs/srom/bin/python tlumacz-front_check.py work/ostendorf/src/ostendorf_src_front.md work/ostendorf/ostendorf_front_pl.md
  EXPECT: /^FRONT OK$/m

- [x] G3: the draft builds without errors, and the translator is reported for the CSV
  CHECK: rm -rf work/ostendorf/build; ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/build.py work/ostendorf/ostendorf_pl.md --refs work/ostendorf/src/refs.json --refs work/ostendorf/ostendorf_refs_tlum.json --pair-src work/ostendorf/src/ostendorf_src.md --queries work/ostendorf/ostendorf_pytania_tlum.csv --out work/ostendorf/build --draft >/dev/null 2>&1 && R=work/ostendorf/build/ostendorf_pl_report.md && echo "errors-none $(grep -A1 '^## Errors' $R | grep -c '^- none$') translator $(grep -c 'Michał|Bartosz||' $R)"
  EXPECT: /^errors-none 1 translator 1$/m

- [x] G4: no untranslated English prose left in the body
  CHECK: python3 work/ostendorf/ost_check.py
  EXPECT: /^leftover English: 0$/m

- [x] G5: every page/wording to look up is marked in the text and listed in the review sheet (counts equal)
  CHECK: python3 work/ostendorf/ost_check.py --marks
  EXPECT: /^marks: (\d+) in text, \1 in review sheet$/m

- [x] G6: the Word working copy imports back and passes the pair check
  CHECK: T=$(mktemp -d) && ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/docx_in.py work/ostendorf/ostendorf_robocza.docx -o $T/rt.md >/dev/null 2>&1 && ~/.venvs/srom/bin/python ~/.claude/skills/srom-produkcja/scripts/check.py --pair work/ostendorf/src/ostendorf_src.md $T/rt.md --refs work/ostendorf/src/refs.json --refs work/ostendorf/ostendorf_refs_tlum.json
  EXPECT: /CHECK OK/

- [x] G7: re-read against the source, paragraph by paragraph (number and agent, quotation boundaries, negations, dates) — manual
  EVIDENCE: full re-read of `ostendorf_pl.md` against `src/ostendorf_src.md` (29.09.2026), 39 paragraphs + 62 notes; 3 fixes: „kluczowym składnikiem” (crucial), „kontrolować i podporządkować” (bound to control and dominate), „w kilku częściach Niemiec” (several); a doubled full stop after 16 translator annotations in notes removed (seen in the built text). Quotation boundaries kept as the author's where translated from the original (Milfort: „leniwych”, not „bardzo leniwych”; Berquin-Duvallon without „cinq ou six”; Roldán without the last clause). Leftover-English checker strengthened after a failed negative control (now case-insensitive; control caught: 2).

- [x] G8: HOUSE terms applied; group names per kartoteka or listed as open (E17) — manual
  EVIDENCE: counts in the draft (comments removed): urasow-/urasaw- 20, rasializ- 0; matryc- 13; skrypt- 12; „cygańska zasłona” 7; Murzyn 5 and Mulat 3 (period quotations only); czarni/biali lower case; *Gitanos*, *Ciganos*, *Bohémiens*, *Zigeuner* italic per kartoteka; „Egipcjanie” 5, in quotation marks (D13); outside the kartoteka, listed in `ostendorf_uwagi.md` § 4 and E17: Anglo-Romani → „angielscy Romowie” 7, *Bohémienne(s)* 4, *cingani*, *Zingaros*/*Zingari*, *Zingances*, *Chinganéros*, *Bohèmes*, *Bohemian*.
