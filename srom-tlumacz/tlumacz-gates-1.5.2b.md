# Gates: 1.5.2b Pilot article draft — Ndiaye, "Black Roma"

Deliverable: a preliminary translation for MB to edit (D11, 28.09.2026): `work/ndiaye/ndiaye_pl.md`, `ndiaye_front_pl.md`, `ndiaye_refs_tlum.json`, `ndiaye_pytania_tlum.csv`, review sheet `ndiaye_uwagi.md` (open points, pages to look up, term decisions applied).

- [x] G1: handoff check passes (structure, notes, citation keys, declared additions)
  CHECK: python3 ~/.claude/skills/srom-produkcja/scripts/check.py --pair work/ndiaye/src/ndiaye_src.md work/ndiaye/ndiaye_pl.md --refs work/ndiaye/src/refs.json --refs work/ndiaye/ndiaye_refs_tlum.json
  EXPECT: /CHECK OK/
  EVIDENCE: WARN  block 65 (p): numbers differ — only in source {2010: 1}, only in target {10: 1}: Jedną z największych pułapek pisania o „Cyganach” … | CHECK OK

- [x] G2: Polish header data well formed
  CHECK: python3 tlumacz-front_check.py work/ndiaye/src/ndiaye_src_front.md work/ndiaye/ndiaye_front_pl.md
  EXPECT: /^FRONT OK$/m
  EVIDENCE: FRONT OK

- [x] G3: the draft builds, and the translator is reported for the CSV (E15 fixed upstream, T14: plain `build.py`, exit 0)
  CHECK: rm -rf work/ndiaye/build; python3 ~/.claude/skills/srom-produkcja/scripts/build.py work/ndiaye/ndiaye_pl.md --refs work/ndiaye/src/refs.json --refs work/ndiaye/ndiaye_refs_tlum.json --pair-src work/ndiaye/src/ndiaye_src.md --queries work/ndiaye/ndiaye_pytania_tlum.csv --out work/ndiaye/build --draft >/dev/null 2>&1 && grep -h -c 'Michał|Bartosz||' work/ndiaye/build/*_report.md
  EXPECT: /^1$/m
  EVIDENCE: 1

- [x] G4: no untranslated English prose left in the body (paragraphs outside notes, italics and quotes of titles removed; count of "the"/"and"/"of")
  CHECK: python3 work/ndiaye/leftover_en.py
  EXPECT: /^leftover English: 0$/m
  EVIDENCE: leftover English: 0

- [x] G5: every page to look up and every quotation still to verify is marked in the text and listed in the review sheet (counts equal)
  CHECK: python3 work/ndiaye/leftover_en.py --marks
  EXPECT: /^marks: (\d+) in text, \1 in review sheet$/m
  EVIDENCE: marks: 7 in text, 7 in review sheet

- [x] G6: re-read against the source, paragraph by paragraph (number and agent, quotation boundaries, negations, dates) — manual
  EVIDENCE: full re-read of `ndiaye_pl.md` against `src/ndiaye_src.md` (28.09.2026); 9 fixes applied: agreement after the 'status' correction („podkopała”), quotation boundary of Convention art. II (author's bracket kept), maître/seigneur („panem i władcą”), *capitaine* (author's word), „(źle) potraktowałby” for (mis)use, „Maurki”, „zniewoleni są nie oni sami”, verse '?' kept, Brooks „teoretycy, którzy mnie ukształtowali”. Boy quotes S2–S6 matched verbatim against `research/boy_skapen.txt` (8/8 strings). Remaining judgement calls listed in `work/ndiaye/ndiaye_uwagi.md` § 3.

- [x] G7: HOUSE terms and the D11 term table applied; group names per kartoteka or listed as open (E14) — manual
  EVIDENCE: counts in the draft (comments removed): urasow-/urasaw- 11, rasializ- 0; „biała supremacja” 9, „supremacja białych” 0; „studia nad czarnością” 7; Murzyn 10 (English *Blackamoor*/*negro* only), Maur- 12 (French *Mores*, English *Moor*); antyromsk- 4 (all 'anti-Roma'); capitalised Czarn-/Biał- mid-sentence 1 (the name gloss „Czarny Wróżbita”). Kartoteka: Romowie, Rom, Cyganie, *Bohémiens*/*Gitanos* italic; Romni, Romnia, Gadjo/Gadji/Gadje and historical „Egipcjanie” open → E14, listed in `ndiaye_uwagi.md` § 4.
