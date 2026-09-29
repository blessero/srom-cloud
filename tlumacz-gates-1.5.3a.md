# Gates: 1.5.3a Second text, intake — Ostendorf, "Familiar Outsiders Abroad" (T19, T21)

Scope: receive the source (T19 as corrected by T21), survey what the chapter needs (quotation rules per quote, Polish
editions, originals of third-language quotes, terminology, group names, doubts in the source), answer the incoming
T-items. MB asked (29.09.2026) to go ahead without his feedback and collect his decisions for later, so no gate waits for
MB: open choices are recorded as assumptions in the intake and the notes sheet. The draft is leaf 1.5.3b.

- [x] G1: the four source files in `work/ostendorf/src/` are identical to srom-typeset's (T21 hashes)
  CHECK: cd "../srom-typeset/work/ostendorf" && shasum -a 256 -c "../../../srom-tlumacz/work/ostendorf/src/manifest.sha256" | grep -c ': OK$'
  EXPECT: /^4$/m

- [x] G2: intake file covers procedure features, Polish editions and originals, terminology, doubts in the source, plan
  CHECK: grep -c '^## [1-5]\. ' work/ostendorf/ostendorf_intake.md
  EXPECT: /^5$/m

- [x] G3: every quotation from a source (not scare quotes, not single-word designations) has one row in the quotes sheet, with a class from PLAN OUT-QUOTES
  CHECK: python3 work/ostendorf/ost_check.py --quotes
  EXPECT: /^quotes: (\d+) in text, \1 in sheet, 0 bad class$/m

- [x] G4: receipt of T17–T21 answered with status lines
  CHECK: grep -oE '^- T(17|18|19|20|21) — 29\.09\.2026 [0-9:]+ status:' ../_handoffs/tlumacz-to-typeset.md | cut -c3-5 | sort -u | wc -l | tr -d ' '
  EXPECT: /^5$/m
  NOTE 29.09.2026 17:44: CHECK rewritten after the cross-module review of 29.09.2026 (finding 13): it counted status lines, and later sessions added more for the same items (5 → 7); it now counts distinct items answered. Gate closed as of its original date.

- [x] G5: every Polish-edition and original-text claim in the intake is backed by a catalogue or text check (manual)
  EVIDENCE: BN data.bn.org.pl API 29.09.2026: Scott „Guy Mannering czyli Astrolog” b0000002107111 (NK 1962), b0000001621265 (NK 1975, wyd. 2), przeł. A. Przedpełska-Trzeciakowska; Pratt „Imperialne spojrzenie” b0000002639481 (WUJ 2011, ISBN 9788323330370); Casanova „Światowa republika literatury” (WUJ 2017); no records for Paucke, Bogdal, Ndiaye, Kendi (author queries). Originals read in archive.org OCR / OA PDF, excerpts with line numbers in `work/ostendorf/research/originals.md`: Poisson Thwaites 67 p. 314 (l. 12209–12214), Berquin-Duvallon p. 32 (l. 1673–1675), Milfort p. 57 (l. 1636–1646), Loskiel 1789 BSB copy (l. 8711–8715, page not identified), Galletti IJRS 3/2 pp. 119, 122 (PDF). Paucke's birthplace and San Javier: es.wikipedia + RAH Historia Hispánica 35593.
