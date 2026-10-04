# Gates: 1.3.1 Vol. 18 precedent mining (+ kartoteka seed)

Scope (MB 27.09.2026): harvest from the four vol. 18 translations only what recurs and needs consistency: Romani and related **group names** (kartoteka seed, kanon § 6.3) and **recurring field concepts** (termbase). Everything else stays per-case judgement. No hard-coding of historical/political place names.

Files: `sources/vol18-md/` (clean texts), `tlumacz-1.3.1/` (`kartoteka-seed.tsv`, `tb-candidates.tsv`, `measure131.py`, `findings.md`).

Harvest rule (declared): group names = capitalised tokens in the English texts that name Romani, Dom/Lom or related groups (list fixed in `measure131.py`, taken from the capitalised-token counts of 27.09.2026); concepts = field-specific terms with ≥ 3 occurrences or in ≥ 2 articles (counts of 27.09.2026), general vocabulary excluded.

- [x] G1: clean text of all eight vol. 18 files present and unchanged
  CHECK: cd sources/vol18-md && shasum -a 256 -c manifest.sha256 | grep -c ': OK$'
  EXPECT: /^8$/m
  EVIDENCE: 8

- [x] G2: every Polish form in the kartoteka seed occurs in the vol. 18 article(s) it cites
  CHECK: python3 tlumacz-1.3.1/measure131.py seed
  EXPECT: /^seed: (\d+)\/\1 forms found/m
  EVIDENCE: seed: 46/46 forms found

- [x] G3: every group name on the harvest list has a seed row
  CHECK: python3 tlumacz-1.3.1/measure131.py coverage
  EXPECT: /^coverage: all \d+ harvested names have a row/m
  EVIDENCE: coverage: all 36 harvested names have a row

- [x] G4: termbase candidates are schema-valid and their precedent quotes are found (checked on a temporary merge)
  CHECK: python3 tlumacz-1.3.1/measure131.py candidates
  EXPECT: /^candidates: valid, \d+ rows, precedent ok/m
  EVIDENCE: established rows: 1, all with >=2 sources | candidates: valid, 8 rows, precedent ok

- [x] G5: urasowienie family — occurrences counted in the four Polish texts and a proposal for the OPEN member raised to MB
  EVIDENCE: counts (regex `\w*uras[oa]w\w*` over `sources/vol18-md/*_pl.md`): fotta urasowienia 8, urasowienie 5, urasowionych 1, urasowionej 1; ostendorf urasowiania 1, urasowieniu 1; takacs, dom 0. „urasawiane” only in Fotta's Polish abstract (full-volume text l. 2408). Proposal urasawiać / urasawianie / urasawiany → `MB-decisions.md` D8 (b); candidate C-0001 in `tb-candidates.tsv`.

- [x] G6: inconsistencies inside vol. 18 raised to MB in one decision item
  CHECK: grep -c '^## D8 ' ../_handoffs/MB-decisions.md
  EXPECT: /^1$/m
  EVIDENCE: 1
  NOTE 28.09.2026: a re-run now gives 0: D8 was answered and removed from MB-decisions.md, as its rules require. Gate closed as of 27.09.2026.

- [x] G7: kartoteka seed passed to srom-produkcja (Kanon/kartoteka are edited only there)
  CHECK: grep -c '^## E11 ' ../_handoffs/tlumacz-to-produkcja.md
  EXPECT: /^1$/m
  EVIDENCE: 1

- [x] G8: MB's sign-off on the candidates; approved rows merged into `tlumacz-tb.tsv`, checks green
  EVIDENCE: MB 27.09.2026 D8 "all good calls" (recorded in `../_handoffs/MB-decisions.md` D8). Merged: check_tb `shape: 11 rows, 0 problem(s)`, `precedent verified: 11/11`, selftest 7/7; all 11 rows HOUSE. (e) italics passed to srom-produkcja (E12), not a termbase row.
