# Gates: 1.5.4b Third text, draft — [Pahulich] "Racialization of Roma, European Modernity, and the Entanglement of Empires"

Deliverable: a preliminary translation for MB to edit (MB 29.09.2026: go ahead, decisions later):
`work/pahulich/pahulich_pl.md`, `pahulich_front_pl.md`, `pahulich_pytania_tlum.csv`, notes sheet `pahulich_uwagi.md`
(pages and wordings to look up, choices to confirm, decisions for MB), Word working copy `pahulich_robocza.docx`.
Open choices are applied as the intake proposes (`pahulich_intake.md` § 3) and listed for MB; nothing waits for MB.

- [x] G1: handoff check passes (structure, notes, citation keys)
  CHECK: ~/.venvs/srom/bin/python ~/.claude/skills/srom-typeset/scripts/check.py --pair work/pahulich/src/pahulich_src.md work/pahulich/pahulich_pl.md --refs work/pahulich/src/refs.json
  EXPECT: /CHECK OK/

- [x] G2: Polish header data well formed
  CHECK: ~/.venvs/srom/bin/python tlumacz-front_check.py work/pahulich/src/pahulich_src_front.md work/pahulich/pahulich_front_pl.md
  EXPECT: /^FRONT OK$/m

- [x] G3: the draft builds, and the translator is reported for the CSV
  CHECK: rm -rf work/pahulich/build; ~/.venvs/srom/bin/python ~/.claude/skills/srom-typeset/scripts/build.py work/pahulich/pahulich_pl.md --refs work/pahulich/src/refs.json --pair-src work/pahulich/src/pahulich_src.md --queries work/pahulich/pahulich_pytania_tlum.csv --out work/pahulich/build --draft >/dev/null 2>&1 && grep -h -c 'Michał|Bartosz||' work/pahulich/build/*_report.md
  EXPECT: /^1$/m

- [x] G4: no untranslated English prose left in the body (notes, italics, comments and citation tokens removed; count of "the"/"and"/"of"…)
  CHECK: python3 work/pahulich/pah_check.py
  EXPECT: /^leftover English: 0$/m

- [x] G5: every page / wording to look up is marked in the text and listed in the notes sheet (same set)
  CHECK: python3 work/pahulich/pah_check.py --marks
  EXPECT: /^marks: (\d+) in text, \1 in review sheet$/m

- [x] G6: re-read against the source, paragraph by paragraph (number and agent, quotation boundaries, negations, dates) — manual
  EVIDENCE: full re-read of `pahulich_pl.md` (431 lines) against `src/pahulich_src.md` (29.09.2026); 5 fixes: "Along with these policies" had become „Mimo tej polityki” (meaning error) → „Równolegle z tą polityką”; "Nonetheless … both recognizes and departs" → „Mimo to … zarówno uznaje…, jak i od nich odchodzi”; the author's slash "incorporating/converting" restored („włączając/przekształcając”); „koczowania zakazano” (case); a doubled „kształtuje” in one sentence. Quotation boundaries: „ 150 = ” 150, no English “. Dates, centuries and numbers checked by `check.py --pair` (only expected WARNs: decades as „lata 40.”, note 67 „1” → „2”).

- [x] G7: HOUSE terms and the intake's term table applied; group names per kartoteka or listed as open — manual
  EVIDENCE: counts in the draft, comments removed (29.09.2026): urasow-/urasaw- 28, rasializ- 0; antycyganizm 5 (incl. German's *antiziganism*), antyromsk- 17 (all 'anti-Roma'); kapitalizm rasowy 19; matryca rasowa 1; antyczarn- 7; Murzyn 4, all in quotation marks (Robinson, Wynter 2×, Browne); capitalised Czarn-/Biał- mid-sentence 0; sedentaryz- 0, sowiec- 10, radziec- 0; Litva 0 (Wielkie Księstwo Litewskie 3, choice listed); *Zigeuner* 2, all italic; „[C]yganie” 2 (Willems quotations) + t-note *t2*; Romki 1; kartoteka forms Sinti, Kale, Manusze, Rudari, Travellersi (n. 2, 67). Open: *Manoush* not a listed variant (E-item), term choices OPEN in `pahulich_uwagi.md` § 3.

- [x] G8: Word working copy round trip: export → import → pair check OK
  CHECK: cd work/pahulich && S=~/.claude/skills/srom-typeset/scripts && rm -rf rt && mkdir rt && ~/.venvs/srom/bin/python $S/export_work.py pahulich_pl.md -o pahulich_robocza.docx >/dev/null 2>&1 && ~/.venvs/srom/bin/python $S/docx_in.py pahulich_robocza.docx -o rt/pahulich_rt.md >/dev/null 2>&1 && ~/.venvs/srom/bin/python $S/check.py --pair src/pahulich_src.md rt/pahulich_rt.md --refs src/refs.json 2>&1 | tail -1
  EXPECT: /CHECK OK/
