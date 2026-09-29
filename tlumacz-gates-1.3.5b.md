# Gates: 1.3.5b Training corpus, batch 2 — and a leaner termbase (MB's reading)

Opened 28.09.2026 20:23 [general]. Input: six more Polish texts in `training/` (Wolniewicz 2013, Małczyński 2014,
Małczyński & Mincer 2014, Nowak 2021, Wrzesińska 2021, Kubica 2015) and P.W. Ryś's online essay (2023, saved as
text). No translation in this leaf: reference base only (MB).

MB's steer (28.09.2026): terms a competent translator gets right unaided (rasizm naukowy, dyskurs rasowy, przemoc
symboliczna, Cham/Jafet, Moskal …) are overkill in the termbase. Loaded historical designations (Murzyn, Saracen vs
Maur …) matter for their history, register and current status, and are decided per case; etymology is secondary.

Declared approach:
- Termbase admission rule written into the schema; CANDIDATE rows that fail it are retired (ids not reused; logged).
- New rows only where the rule admits them.
- Register `tlumacz-rasa.md` rebuilt around per-case use: three voices (period quotation / author reporting period
  usage / author's analytic voice) and clusters of loaded designations, each with period forms, register, current
  status and sources. Unsourced working knowledge is marked as such.
- Correct my earlier line that „Murzyn” translates no EN term we use: MB's D11 (4) maps period *Blackamoor* / *negro*
  to „Murzyn”.

- [x] G1: all training texts registered (key → file) and hashed; hashes match
  CHECK: cd training && shasum -a 256 -c manifest.sha256 | grep -c ': OK$'
  EXPECT: /^10$/m
  NOTE 29.09.2026: MB removed the Kubica DOCX from `training/` (its pandoc conversion, the text of record, stays) and added Urbanek (leaf 1.3.5c); a re-run still gives 10, over a different set. Gate closed as of 28.09.2026.

- [x] G2: termbase checks green, every training quote found
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence
  EXPECT: /^training quotes verified: (\d+)\/\1$/m

- [x] G3: the admission rule is in the schema, and the ten retired rows are gone from the termbase
  CHECK: ~/.venvs/srom/bin/python -c "import csv;ids={r['concept_id'] for r in csv.DictReader(open('tlumacz-tb.tsv'),delimiter='\t')};ret=['C-00%d'%n for n in (20,21,22,23,29,30,32,33,34,35)];print('retired absent: %d/%d'%(sum(i not in ids for i in ret),len(ret)));print('rule:','### Admission' in open('tlumacz-tb-schema.md').read())"
  EXPECT: /^retired absent: 10\/10\s+rule: True/m

- [x] G4: negative controls still caught
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --selftest
  EXPECT: /^selftest: 9\/9 negative controls caught$/m

- [x] G5: the register references every CANDIDATE row and has the per-case clusters (at least 7)
  CHECK: ~/.venvs/srom/bin/python -c "import csv;r=[x['concept_id'] for x in csv.DictReader(open('tlumacz-tb.tsv'),delimiter='\t') if x['status']=='CANDIDATE'];t=open('tlumacz-rasa.md').read();m=[i for i in r if i not in t];print('register: %d/%d candidate rows referenced'%(len(r)-len(m),len(r)),*m);print('clusters:',t.count('\n### B'))"
  EXPECT: /^register: (\d+)\/\1 candidate rows referenced\s+clusters: ([7-9]|\d\d)$/m

- [x] G6: every cluster cites at least one training source by key or MB's decision
  CHECK: ~/.venvs/srom/bin/python -c "import re;t=open('tlumacz-rasa.md').read();b=re.split(r'\n### ',t.split('\n## B.')[1].split('\n## C.')[0])[1:];bad=[x.split('\n')[0] for x in b if not re.search(r'\[(taradejna|nowak|nowak2021|wolniewicz|malczynski|malczynski_mincer|wrzesinska|kubica|rys)\b|MB|D11',x)];print('clusters sourced: %d/%d'%(len(b)-len(bad),len(b)),*bad)"
  EXPECT: /^clusters sourced: (\d+)\/\1\s*$/m

- [x] G7: the retirement is logged in `tlumacz-decisions.md`
  CHECK: grep -c 'retired' tlumacz-decisions.md
  EXPECT: /^[1-9]$/m

- [x] G8: leaf recorded (PLAN, HANDOVER) and committed
  CHECK: git log -1 --format=%s
  EXPECT: /1\.3\.5b/
