# Review 26.10.2026 (root, 26.10.2026 15:29) [general]

Milestone check asked by MB, mainly on srom-ikonograf (21–26.10.2026: register, queries, known-item search, the slavery
query's method, three new scripts), plus two requests: contact sheets at hand in `Claude outputs/`, and the sources.md
§ Routes notes that K43 addendum 5 calls missing. Range: 26 commits since review 21.10.2026 (68c6c30 … 56a016f).

## Conclusions
- **The tools are healthy.** srom-produkcja SUITE ALL PASS 29/29 before and after the changes; srom-tlumacz green on every
  check (contract 35/35 at 56a016f). The Kanon version agrees everywhere (test_kanon 20/20). Nothing blocks a text.
- **Ikonograf works, and its records are sound where measured.** The slavery query's candidates match the record's
  arithmetic and its sheet: 179 at 15:20 (121+17+17+13+11), 214 after the sixth pass at 15:28 (+35; 214 ids on the sheet); 177 thumbnails in the three sheets the browser pane can open load,
  0 broken (q-stlouis1904's target loaded on the second count: Internet Archive renders pages on demand).
- **Sheets at hand (MB's request): done.** `pobierz.py`, which already runs every 5 minutes on the Mac, now copies every
  record's `kontaktowka.html` that is new or changed to `Redakcja/Claude outputs/Kontaktowka - <Name>.html`; three tests.
  The two copies there before were stale (24.10 23:11; their sheets were rebuilt 25.10 02:28): now all five are current.
- **The § Routes notes were not missing.** They were committed in ff782ff (26.10 15:09) as an appended block dated
  „27.10.2026”, a day in the future; now folded into the tables they belong to, date fixed.
- **Dates are the one recurring fault.** The slavery session stamps 27.10.2026 (K43 addenda 5 and 6, sources.md, the record);
  addenda 2–6 and K45 carry no time. Fixed where Code may write; Cowork is told which dates are wrong (K46).
- **The new scripts had no tests** (ff782ff's „tests” was the `sips` skip only): now a compile test for all four scripts and two
  offline montage tests; `commons_pages.py` no longer crashes with a traceback when Commons stops answering.
- One Kanon bookkeeping slip (a supplement row appended to the already announced v1.18) and one unanswered T-item, both left
  for the module sessions. A backup was 5 days old while the ikonograf records (not in git) grew: new backup made.

## Verdict lines as printed
- srom-produkcja, before (at 56a016f): `SUITE ALL PASS 29/29` (IKONOGRAF ALL PASS 14/14)
- srom-produkcja, after: `SUITE ALL PASS 29/29` (`IKONOGRAF ALL PASS 20/20`; under /usr/bin/python3 3.9, launchd's interpreter, `IKONOGRAF ALL PASS 18/18`, `SKIP montage: 2 tests (no Pillow)`)
- srom-tlumacz (contract test against 56a016f): `selftest: 9/9 negative controls caught`; `HANDOFF CONTRACT 35/35`; termbase
  `established rows: 14, all with >=2 sources`, `training quotes verified: 25/25`, `candidate rows: 12, each with a verified training quote`;
  `DRAFT steiner|tittel|tittelpta|westohueri: leftover 0` (marks 10=10, 12=12, 46=46, 7=7; quotes 18/18, 34/34, 10/10, 15/15)
- backup: `BACKUP OK srom-20261026-1525.tar.gz: 1981 paths, sha256 verified, 352M` (previous: 21.10.2026 03:42)
- browser pane, broken thumbnails: q-slavery19c 0/153, q-stlouis1904 0/6 (2 on the first count at 5 s), Ostendorf18 0/18;
  Tittel (3.4 MB) and Pahulich (14 MB) do not open as a pane snapshot (size): checked byte-identical to their records only

## Findings
| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | Contact sheets buried in `work/<id>/ikonografia/`; the two copies MB used in `Claude outputs/` were stale, made by hand, under no rule; the folder is not in § The one folder | copies 24.10 23:11 vs sheets 25.10 02:28; root CLAUDE.md table; checkup § 9 | will bite | srom-produkcja (done, #1) |
| 2 | K43 addendum 5 says the § Routes notes (IHOI URL, Northwestern API, Chrome/HathiTrust) are still to write; they were committed, as an appended „Added 27.10.2026” block | `git blame` sources.md:233 → ff782ff 26.10 15:09 | cosmetic | srom-produkcja (done, #2); Cowork told (K46) |
| 3 | Future dates and missing times in dated entries | code-to-cowork.md: addenda 5, 6 „27.10.2026” (written by 15:28 on 26.10); addenda 2–6, K45 no time; q-slavery19c record 3 × 27.10 (record saved 26.10 14:56) | will bite (dates are evidence) | the slavery session; record fixed here; Cowork told (K46) |
| 4 | `ia_find.py`, `commons_pages.py`, `montage.py` not in the suite; `commons_pages.py` dies on `json.loads(None)` when Commons stops answering | ff782ff test diff = the `sips` guard only; commons_pages.py `api()` | will bite | srom-produkcja (done, #3) |
| 5 | Broken-image count can drop a good row: IA page images render on demand | q-stlouis1904 S1-a broken at 5 s, 1187 px on recount; curl 200 | cosmetic | srom-produkcja (done, #4) |
| 6 | C27–C30 have no status line from Code | code-to-cowork.md has none; work is in ff782ff (C27), 554f8fb (C29), 959ecfe (C30) | cosmetic | root (done, K46) |
| 7 | Kanon § 17 row „1.18, uzup. 26.10.2026” appended to v1.18, announced in T39 (24.10); no T-item for it | kanon-redakcyjny.md:718; root CLAUDE.md § Kanon versions; produkcja-to-tlumacz.md ends at T39 | cosmetic | srom-produkcja session (Kanon) |
| 8 | T39 [general] (Kanon v1.18) has no status line from srom-tlumacz | tlumacz-to-produkcja.md: no „T39” | cosmetic | srom-tlumacz |
| 9 | Uncommitted, another session's: one sources.md paragraph („loc.gov search through MB's Chrome”) and K43 addendum 6 | `git status`, 15:28; addendum 6 asks Code to commit | — | the slavery session, or a Code session on MB's word |
| 10 | Backup 5 days old while records not in git grew (179-candidate query, three new records) | verify_backup.sh: srom-20261021-0342 | will bite | root (done) |
| 11 | The q-slavery19c sheet is built by per-query scripts holding content in Python source (`_tools/items.py`, `build.py`); every rebuild wiped the embedded thumbnails twice | ikonograf-tooling-handoff.md item 1 | will bite on the next big query | MB decides (For MB 2) |
| 12 | Record q-slavery19c line 3: „proposed: 15 slots (S9–S15 secondary)” beside „16 slots” | ikonografia.md:3, S16² at line 30 | cosmetic | done here (16, S9–S16) |

## Last review's findings
Review 21.10.2026: all five srom-produkcja items done (68c6c30, f5b6e3b; status lines in produkcja-to-tlumacz.md:739). Its For MB
items (uploads, GEN-113, online date, folder name, old link) are MB's and Cowork's ledger's; not re-checked here.

## For srom-produkcja
1. Done in Apply: `srom-ikonograf/scripts/pobierz.py` mirrors each record's sheet to `Claude outputs/` (`mirror()`, `--mirror`);
   SKILL.md § Files row and step 5 Deliver; root CLAUDE.md § The one folder row and the Files-to-open example; checkup § 9.
   Verify: `test_ikonograf.py` → `PASS pobierz: sheet …` × 3.
2. Done in Apply: sources.md, the „Added 27.10.2026” block folded: Northwestern row in Tier A, DPLA date filter and batch call,
   loc.gov and IMS Cloudflare box (MB by hand, in Chrome), HathiTrust in Claude in Chrome, IHOI search and the Winterton
   originals in § Routes. Verify: `grep -c "27\.10\.2026" sources.md` → 0.
3. Done in Apply: test_ikonograf.py compiles every ikonograf script and runs `montage.py` offline (both modes);
   `commons_pages.py` exits with a message, not a traceback, when the API fails four times.
4. Done in Apply: SKILL.md step 5, count a broken thumbnail twice before dropping it (IA renders on demand).
5. **Left for a srom-produkcja session (Kanon):** at the next Kanon change, open v1.19 folding in the 26.10.2026 supplement
   (§ 12.2.3 masthead credit), as v1.18 folded 1.17's; and now one T-item to srom-tlumacz, for information, naming that
   supplement (the translator's credit moves to the masthead; nothing in its outputs changes). Verify: test_kanon.py.

## For srom-tlumacz
1. Status line for T39 [general] (Kanon v1.18, 24.10.2026 23:21) in `tlumacz-to-produkcja.md`: seen / applied.

## For MB
1. **Nothing to decide for the sheets:** open them from `Redakcja/Claude outputs/` (`Kontaktowka - Pahulich.html`, `… - Zapytanie
   slavery19c.html`, …). They refresh within 5 minutes of any rebuild; never edit them (the next rebuild replaces them).
2. **Optional, your call: the ikonograf tooling hand-off** (`_handoffs/ikonograf-tooling-handoff.md`). Cheapest: nothing until
   the next large query. Worth it then: item 1 (`kontaktowka_build.py`: sheet from a rows file, thumbnails embedded on every
   build) with its test (item 5); items 2–3 overlap `montage.py`/`commons_pages.py` and can wait; item 4 is your minute
   (a free api.data.gov key into `~/.config/srom/`, as for DPLA).
   Run with: Opus · high — scope checked: one new script replacing `_tools/build.py` + `items.py` (q-slavery19c), one test;
   the real risk is losing data held only in `items.py` when porting the 214 candidates (addendum 6).
3. **Uncommitted from the slavery session** (finding 9): say whether a Code session should commit its sources.md paragraph
   and addendum 6, or leave it to that session.
