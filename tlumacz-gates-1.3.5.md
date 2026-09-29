# Gates: 1.3.5 Training corpus — Polish vocabulary of race and racialisation (MB's reading)

Opened 28.09.2026 19:14 at MB's request [general]. Input: two native Polish articles MB put in `training/`
(Taradejna, Folia Sociologica 88, 2024; Nowak, „Klio” 72, 2024). Aim: harvest the Polish forms a translator of
EN race/racialisation texts will need, without pretending they are house decisions.

Declared approach (MB delegated the choice, "your call"):
- The two-source rule is **not** relaxed. It describes standing, not usability: a form found in one of the two
  articles is ATTESTED, in both ESTABLISHED. Nothing stops the translator from using an ATTESTED form.
- New termbase status **CANDIDATE** (harvested from reading, not a house decision; becomes HOUSE by MB's decision
  when a text first needs it). Evidence cites the training text with a quote the checker verifies (`TR <key>: «…»`).
- General concepts with an EN counterpart → termbase rows. Historical, etymological and literary material (Maurowie,
  Murzyn, czerń, cham, Turańczycy, old Polish texts and their editions) → a separate register, `tlumacz-rasa.md`.
- Errors found in the two articles are flagged in the register (§ F), not silently corrected or adopted.

- [x] G1: both training texts registered: key, file, bibliographic line; sha256 recorded and matching
  CHECK: cd training && shasum -a 256 -c manifest.sha256 | grep -cE '^(POMIĘDZY PROTORASIZMEM SZLACHECKIM A RASIZMEM NAUKOWYM\.txt|Urasowienie narodu i przenarodowienie rasy\.md): OK$'
  EXPECT: /^2$/m
  NOTE 29.09.2026 17:44: CHECK rewritten after the cross-module review of 29.09.2026 (finding 13): it counted every file in the manifest (2 → 10 as later batches were added); it now checks this leaf's two texts (Taradejna, Nowak) by name. Gate closed as of its original date.

- [x] G2: schema defines CANDIDATE and the TR evidence form; all termbase checks green
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence
  EXPECT: /^training quotes verified: (\d+)\/\1$/m

- [x] G3: every CANDIDATE row carries at least one verified training quote
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --evidence
  EXPECT: /^candidate rows: \d+, each with a verified training quote$/m

- [x] G4: negative controls: a corrupted training quote and a CANDIDATE row without one are caught
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --selftest
  EXPECT: /^selftest: 9\/9 negative controls caught$/m

- [x] G5: the register cross-references every CANDIDATE row of the termbase
  CHECK: ~/.venvs/srom/bin/python -c "import csv,re;r=[x for x in csv.DictReader(open('tlumacz-tb.tsv'),delimiter='\t') if x['status']=='CANDIDATE'];t=open('tlumacz-rasa.md').read();m=[x['concept_id'] for x in r if x['concept_id'] not in t];print('register: %d/%d candidate rows referenced'%(len(r)-len(m),len(r)),*m)"
  EXPECT: /^register: (\d+)\/\1 candidate rows referenced\s*$/m

- [x] G6: doubts in the two articles and in the web sources MB pointed to are listed in the register (§ F), each
  with what the source says and what I would do
  CHECK: grep -c '^- \*\*F[0-9]' tlumacz-rasa.md
  EXPECT: /^([5-9]|[1-9]\d)$/m

- [x] G7: list of referenced works worth sourcing, for MB (register § G), each with where it is cited
  CHECK: grep -c '^| G[0-9]' tlumacz-rasa.md
  EXPECT: /^([1-9]\d)$/m

- [x] G8: leaf recorded (PLAN tree + status log, HANDOVER) and committed
  CHECK: git log --format=%s | grep -cE '^1\.3\.5: gates ALL MET'
  EXPECT: /^[1-9][0-9]*$/m
  NOTE 29.09.2026 17:44: CHECK rewritten after the cross-module review of 29.09.2026 (finding 13): `git log -1` tested the newest commit, which drifts with every later commit; it now looks for this leaf's own commit by its message. Gate closed as of its original date.
