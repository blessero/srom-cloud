# Gates: 1.1 Contracts (srom-tlumacz v1, EN→PL)

Scope: fix every interface later leaves depend on — plan, termbase schema and decision rule, seed rows for the four named vol. 18 precedents, output contracts, and the draft kanon section on translated articles.

- [x] G1: PLAN has Contract, Tree and Status log sections
  CHECK: grep -c -E '^## (Contract|Tree|Status log)$' tlumacz-PLAN.md
  EXPECT: 3
  EVIDENCE: 3

- [x] G2: every TSV header column is defined in the schema doc, and every schema field is a TSV column
  CHECK: python3 tlumacz-check_tb.py --schema
  EXPECT: /columns: (\d+)\/\1 defined; schema fields: \1\/\1 present/
  EVIDENCE: columns: 17/17 defined; schema fields: 17/17 present

- [x] G3: every row uses only controlled values for domain, status and pl_standing
  CHECK: python3 tlumacz-check_tb.py --vocab
  EXPECT: vocab: all rows valid
  EVIDENCE: vocab: all rows valid

- [x] G4: the four named vol. 18 precedents are present as HOUSE and each precedent quote is found verbatim in the vol. 18 text in project knowledge
  CHECK: python3 tlumacz-check_tb.py --precedent
  EXPECT: precedent verified: 4/4
  EVIDENCE: precedent verified: 4/4
  NOTE 28.09.2026: a re-run now gives 11/11 (rows added in 1.3.1): drift in a file meant to change. Gate closed as of 26.09.2026.

- [x] G5: every ESTABLISHED row cites at least two sources
  CHECK: python3 tlumacz-check_tb.py --evidence
  EXPECT: /established rows: \d+, all with >=2 sources/
  EVIDENCE: established rows: 1, all with >=2 sources

- [x] G6: decision rule encodes precedent lock, fidelity floor and the 4-step ranking in MB's order
  CHECK: grep -c -E 'LOCK|FLOOR|RANK-1 established|RANK-2 consistency|RANK-3 fidelity|RANK-4 clarity' tlumacz-tb-schema.md
  EXPECT: /^([6-9]|\d{2,})$/m
  EVIDENCE: 6

- [x] G7: PLAN specifies all six per-article outputs and all three cross-module interfaces
  CHECK: grep -c -E '^- OUT-(TEXT|REVIEW|QUERIES|QUOTES|TBROWS|REFS)|^- IF-(KANON|CURATOR|TYPESET)' tlumacz-PLAN.md
  EXPECT: /^9$/m
  EVIDENCE: 9

- [x] G8: kanon § 12.2 draft covers all eight subsections and marks open decisions
  CHECK: grep -c -E '^### 12\.2\.[1-8]\.' kanon-12-2-przeklady-PROJEKT.md; grep -c '▲' kanon-12-2-przeklady-PROJEKT.md
  EXPECT: /^8\n\d+$/m
  EVIDENCE: 8 | 2

- [x] G9: § 12.2 draft passes srom-kanon lint with no ERROR
  CHECK: python3 "$(python3 tlumacz_paths.py srom-kanon)/scripts/lint_srom.py" kanon-12-2-przeklady-PROJEKT.md --json | python3 -c "import json,sys; d=json.load(sys.stdin); print('lint errors:', sum(i['severity']=='ERROR' for i in d['issues']))"
  EXPECT: lint errors: 0
  EVIDENCE: lint errors: 0
  NOTE 28.09.2026: a re-run now gives 1 ERROR: the draft is superseded (Kanon v1.6 § 12.2) and the linter has changed since. Gate closed as of 24.09.2026.

- [x] G10: manual — § 12.2 read adversarially against kanon v1.5 for conflicts; every conflict either resolved in the draft or listed as ▲
  EVIDENCE: first pass fixed 7 conflicts (§ 1 pkt 9, § 6.3 ×2, § 7.1, § 4.3 main-text additions, § 12.1, § 6.1 quote register) and added bibliography for case a. Review pass added: scope limited to English originals (metadata rules assume an English title); CC BY attribution completed (licence URI, copyright notice); several Polish translations of one work (▲ 12); field-material formula in case c; identity rule for first use; Polish-edition terminology kept in quotations. Lint 0 ERROR after edits; open items measured: 12. 25.09.2026: MB's rulings written in; asterisk series for translator notes stated as an exception to § 7.1; 3 open items remain (3, 6, 7); lint 0 ERROR. Later 25.09.2026: items 3, 6, 7 ruled; non-author notes (title, translator, editorial) as one asterisk series; `przyp. red.` added to § 11; 0 open items; lint 0 ERROR.

- [x] G11: every row well-formed: full width, unique ids, HOUSE rows dated, shared English forms disambiguated by `sense`
  CHECK: python3 tlumacz-check_tb.py --shape
  EXPECT: /shape: \d+ rows, 0 problem\(s\)/
  EVIDENCE: shape: 4 rows, 0 problem(s)

- [x] G12: the checker itself is proven to fail on corrupted data (negative controls)
  NOTE 01.10.2026 17:21 [general]: the selftest has grown to 9/9 (was 7/7); the EXPECT/EVIDENCE below are the old figure. No CHECK change (review 01.10.2026 item 6).
  CHECK: python3 tlumacz-check_tb.py --selftest
  EXPECT: selftest: 7/7 negative controls caught
  EVIDENCE: selftest: 7/7 negative controls caught

- [x] G13: manual — contract reviewed against srom-produkcja (scenario C); no duplicated responsibility left, every required change there stated as a numbered requirement
  EVIDENCE: source = srom-produkcja build chat (translation protocol, check.py --pair spec, blocking comments, _pytania sheet). Removed duplicates: preserve_check (= check.py --pair), own DOCX conversion (= build.py), separate query list (= _pytania), hand-kept glossary (= tb_lookup view). Conflicts stated as IF-TYPESET R1 (translator notes vs marker count), R2 (added Polish-edition keys vs key invariance), R3 (own-translation marking vs § 12.2.4 d), R4 (title asterisk note). 25.09.2026: installed srom-produkcja implements R1, R2, R4 (verified by G14); R3 moot (translation.md replaced by handoff.md, no such rule).

- [x] G14: srom-produkcja handoff behaviour relied on by the contract holds on the installed skill
  CHECK: python3 tlumacz-test_handoff.py
  EXPECT: /^HANDOFF CONTRACT (\d+)\/\1$/m
  EVIDENCE: KNOWN GAP FAIL  E4: numbers from added citation keys not reported | HANDOFF CONTRACT 9/9
