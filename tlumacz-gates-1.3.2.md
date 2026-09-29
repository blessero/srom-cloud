# Gates: 1.3.2 Vol. 19 vocabulary, driven by the translation shortlist

Opened 29.09.2026 14:10 [general], after a read-only survey (intake and notes sheets, sources, drafts). No translation in
this leaf (MB, 29.09.2026: "you won't be translating anything here"): the drafts are read, never edited.

Shortlist (MB 29.09.2026, closes `MB-decisions.md` D6 (c)): the vol. 19 translations are the texts srom-produkcja handed
over: Ndiaye (T12), Ostendorf (T19/T21), Pahulich (T18), Tittel (T20) — drafted in parallel sessions — and West Ohueri
(T23/T24, source frozen, not started, rights pending).

Declared approach:
- A measured concordance: `tlumacz-1.3.2/vol19_terms.py` over the five sources and four drafts, probes in `probes.tsv`
  (concepts that recur in ≥ 2 vol. 19 sources and carry a choice). Verdicts are leads; each flagged probe is read in
  context and the result recorded in `findings.md`.
- Vol. 18 precedent checked for every divergence (`sources/vol18-md/`).
- Termbase: PROVISIONAL rows (used in a current draft, awaiting MB) only for concepts that pass schema § Admission and
  recur in the volume or are needed before West Ohueri; one cross-text decision item for MB; per-text choices stay in
  the per-text items (D22, D23, D25).
- Lessons for the module (tooling, procedure) recorded in `findings.md`, acted on in their own leaves.

- [x] G1: D6 (c) closed: removed from MB-decisions, the shortlist recorded in `tlumacz-decisions.md`
  CHECK: printf '%s %s\n' "$(grep -c '^### D6' ../_handoffs/MB-decisions.md)" "$(grep -c 'D6 (c)' tlumacz-decisions.md)"
  EXPECT: /^0 [1-9]$/m

- [x] G2: concordance runs over 5 sources and 4 drafts and writes the table
  CHECK: cd tlumacz-1.3.2 && python3 vol19_terms.py | tail -1 && test -s vol19-concordance.tsv && echo table-ok
  EXPECT: /^concordance: 25 probes, .*\n^table-ok$/m

- [x] G3: negative control: a planted divergence and a planted missing rendering are both caught
  CHECK: cd tlumacz-1.3.2 && python3 vol19_terms.py --selftest | tail -1
  EXPECT: /^selftest: planted divergence caught, planted missing rendering caught$/m

- [x] G4: every probe flagged divergent or missing has a reviewed line in findings.md (by id)
  CHECK: cd tlumacz-1.3.2 && python3 -c "import csv,re;f=open('findings.md').read();r=[x['id'] for x in csv.DictReader(open('vol19-concordance.tsv'),delimiter='\t') if x['verdict'] in('divergent','missing')];m=[i for i in r if not re.search(r'^\| '+i+r' ',f,re.M)];print('flagged reviewed: %d/%d'%(len(r)-len(m),len(r)),*m)"
  EXPECT: /^flagged reviewed: (\d+)\/\1\s*$/m

- [x] G5: termbase checks green with the new PROVISIONAL rows; each new row states its admission reason
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence | tail -3 && python3 -c "import csv;r=[x for x in csv.DictReader(open('tlumacz-tb.tsv'),delimiter='\t') if x['status']=='PROVISIONAL'];b=[x['concept_id'] for x in r if not x['note'].startswith('Admission:')];print('provisional rows: %d, without admission reason: %d'%(len(r),len(b)),*b)"
  EXPECT: /^candidate rows: \d+, each with a verified training quote\nprovisional rows: [1-9]\d*, without admission reason: 0\s*$/m

- [x] G6: selftest of the termbase checker still 9/9
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --selftest
  EXPECT: /^selftest: 9\/9 negative controls caught$/m

- [x] G7: one cross-text item for MB committed in `_handoffs` (per-text points stay in D22/D23/D25)
  CHECK: git -C ../_handoffs log --format=%s | grep -c '1.3.2'
  EXPECT: /^[1-9]$/m

- [x] G8: leaf recorded (PLAN tree + status log, HANDOVER) and committed
  CHECK: git log --format=%s | grep -cE '^1\.3\.2: gates ALL MET'
  EXPECT: /^[1-9][0-9]*$/m
  NOTE 29.09.2026 17:44: CHECK rewritten after the cross-module review of 29.09.2026 (finding 13): `git log -1` tested the newest commit, which drifts with every later commit; it now looks for this leaf's own commit by its message. Gate closed as of its original date.
