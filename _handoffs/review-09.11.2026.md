# Review 09.11.2026 — full-suite milestone checkup [general]

Run from the root session in Claude Code on the Mac, at MB's request ("full, thorough milestone/system checkup of the
whole srom suite including all skills and elements"), under unlazy gates. As on 02.11.2026, both scopes in one pass:
Code's checkup (`checkup/SKILL.md`) and Cowork's (`checkup/COWORK.md`). Nothing in `srom-produkcja/` or `srom-tlumacz/`
was changed during the review; every build, import, take-back and mutation test ran on copies in the session's
scratchpad. One thing was done where no decision was needed: a fresh backup (finding 3).

## Conclusions

1. The tools are green: suite 29/29 at 53cabc4, the three srom-tlumacz checks, the handoff contract 35/35, all nine
   hand-off manifests, 28 frozen `src/` copies, every draft's pair check, `--draft` build and Word round trip, the three
   keyed texts' mutation tests, Kanon v1.19 consistent, every Kanon § citation resolves, 81 Python files compile,
   every skill link resolves, `desk_sync.py` `problems=0` and Biurko's open items equal the ledger's (85).
2. **One thing will block a delivery: the Tittel PTA cut.** This morning's cut (09.11 04:33) put the cut text in new
   `_cut` files and kept the whole chapter under the names the tools read. At delivery, `take_back.py` pairs the Word
   master with `tittelpta_src.md` — the whole source — and fails (`CHECK FAIL 24`, `TAKE-BACK FAILED`); with the cut
   in the canonical name it passes (`TAKE-BACK OK tittelpta (5 files)`). The same split turns the standing
   `tlumacz-draft_check.py --all` red and doubles the recorded `--keyed` result (32 → 86). No tool change is needed:
   the cut files should take the canonical names (Cowork, K-item).
3. **The live-site hook guards the wrong connector.** It counts `mcp__Ae-*` as the SROM site, but that connector is
   EPLA's JetEngine staging (`darkblue-seal-673630.hostingersite.com`). A 403 there would trip the SROM breaker and
   block all SROM site work; EPLA work is paced as if it were SROM. A one-line config fix, MB's to approve.
4. The backup was again 7 days old across a big step (the Tittel PTA cut, the vol. 19 block choice, Davis TRANS).
   A fresh one is made: `BACKUP OK srom-20261109-1633.tar.gz: 2824 paths, sha256 verified, 593M`.
5. The rest is record-keeping: C-items committed without a K status line, two K-items without Cowork's, a stale
   termbase count in the srom-tlumacz HANDOVER, four text codes missing from the README table, and leftover scratch
   folders and files in `workspace/` and at the one folder's top level.
6. Last review's findings: 1–6 and 8 closed; 7 (two milestones without a date), 9 (git garbage) and 10 (K49) still open.

## Verdict lines as printed

```
SUITE ALL PASS 29/29                          (srom-produkcja tests/run_all.py at 53cabc4; 2:17 wall)
columns: 17/17 defined; schema fields: 17/17 present          (tlumacz-check_tb.py, exit 0)
shape: 43 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 14/14
precedent quotes in rows not yet HOUSE: 4/4
established rows: 14, all with >=2 sources
training quotes verified: 25/25
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 35/35                                        (tlumacz-test_handoff.py, at 53cabc4)
tlumacz-draft_check.py --all → exit 1:
  DRAFT davis: leftover 0, marks 12=12, quotes 11/11
  DRAFT ndiaye: leftover 0, marks 7=7, quotes –
  DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43
  DRAFT pahulich: leftover 0, marks 10=10, quotes –
  DRAFT steiner: leftover 0, marks 10=10, quotes 18/18
  DRAFT tittel: leftover 0, marks 12=12, quotes 34/34
  DRAFT tittelpta: leftover 0, marks 46≠43, quotes 6/10   (whole draft read against the cut's sheets: finding 1)
  DRAFT westohueri: leftover 0, marks 7=7, quotes 15/15
09.11.2026 16:25 decisions=85 glance=85 files=12 texts_v19=6/6 articles=17:10,18:15,19:0 milestones=23 archive=29
  preflight='SUITE ALL PASS 29/29' problems=0 ikonograf=8 pool=19-2026:65 selected:6,candidate:0,mark:0,
  background:35,out:24,other:0                                (desk_sync.py)
BACKUP OK srom-20261109-1633.tar.gz: 2824 paths, sha256 verified, 593M   (backup.sh, then verify_backup.sh)
```

Per text, on copies (srom-tlumacz `work/<id>/`; Tittel PTA with its `_cut` files):

| text | pair | front | `--draft` build Errors | Word copy → `docx_in` → pair | keyed source: `--keyed` / `mutate_keyed` |
|---|---|---|---|---|---|
| davis | CHECK OK | FRONT OK | none | CHECK OK | CHECK OK / MUTATIONS CAUGHT 40/40 |
| ndiaye | CHECK OK | FRONT OK | none | CHECK OK (`_v2`) | — |
| ostendorf | CHECK OK | FRONT OK | none | CHECK OK | — |
| pahulich | CHECK OK | FRONT OK | none | CHECK OK | — |
| steiner | CHECK OK | FRONT OK | DOCX verification: no em dash 4 (known, `refs.json`) | CHECK OK | CHECK OK / 39/40 (note 62, known: K54) |
| tittel | CHECK OK | FRONT OK | none | CHECK OK | — |
| tittelpta (cut) | CHECK OK | FRONT OK | none | CHECK OK | live `refs.json`: CHECK FAIL 86; with the archived whole `refs.json`: CHECK FAIL 32 (the recorded, read 32) / 40/40 |
| westohueri | CHECK OK | FRONT OK | none | CHECK OK | CHECK OK / 40/40 |

The full builds without `--draft` fail only on the expected: "not normalised" (take-back normalises) or known
`[BRAK …]` gaps (pahulich n. 47, 145; tittel n. 20; tittelpta 10 notes); westohueri: Errors none.

Hand-off manifests, `shasum -a 256 -c`: 9 of 9, 37 entries, 0 failed (davis, ndiaye, ostendorf, pahulich, steiner,
tittel, westohueri 4 each; tittelpta 5; `srom-produkcja/work/ostendorf/pl/SHA256SUMS` 5). srom-tlumacz `src/` against
srom-produkcja's frozen files: 28 compared, 0 differing (six old `*_queries.md` copies have no twin by design: README
§ Notes sheets).

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | **Tittel PTA: the cut is not in the names the tools read.** `tittelpta_src.md` and `tittelpta_pl.md` are still the whole chapter, while `refs.json`, the notes sheet, the quotes sheet and the query sheet were pruned to the cut. `take_back.py` has no option for another source name: at delivery it pairs the Word master (the cut) with the whole source and fails. `draft_check --all` reads the whole draft against the cut's sheets and exits 1; `check.py --keyed` on the recorded pair now reports 86 errors (21 keys gone from `refs.json`), not the 32 that were read | on copies: delivery = import of `tittelpta_robocza.docx` + `tittelpta_front_pl_cut.md` as `_front_pl.md`; `take_back.py … --src-dir <copy of srom-produkcja/work/tittelpta>` → `CHECK FAIL 24 error(s)`, `TAKE-BACK FAILED tittelpta: 1 problem(s)`; the same with `tittelpta_src_cut.md` copied in as `tittelpta_src.md` → `TAKE-BACK OK tittelpta (5 files)`. `take_back.py:64` (`{id}_src.md`), `:116`; STATUS.md l. 97 "INJECT pairs the Word copy with `src/tittelpta_src_cut.md`"; the cut gates file ran draft_check in a temp dir with the cut renamed (`tittelpta_gates_cut.md` gate at l. 24), which is the workaround, not the record | will bite (blocks the TPA hand-back) | Cowork (K-item): give the cut the canonical names (`_src.md`, `_pl.md`, `_front_pl.md` in both modules' folders) and move the whole versions to `_archive/20261109/tittelpta_whole/`, new manifest + a hand-off log line; not while MB has the Word copy open (`~$ttelpta_robocza.docx`, 06:20) — only the Markdown files move, the Word master keeps its name |
| 2 | **The live-site hook throttles EPLA's staging connector as if it were SROM.** `connector_prefixes: ["mcp__Ae-"]`; the only `Ae-` server is JetEngine on `darkblue-seal-673630.hostingersite.com`, which the epla-platform skill names as EPLA's staging host. A block answer from that host trips the SROM breaker | `~/.claude/hooks/srom-throttle.py:41`; `~/.claude.json` mcpServers: `Ae-j98zfDHrD4Mz https://darkblue-seal-673630.hostingersite.com/wp-json/jet-engine/v1/mcp`; `~/.claude/skills/epla-platform/SKILL.md:13`; `--status`: last call `connector, mcp__Ae-j98zfDHrD4Mz__resource-get-configuration` | will bite | MB (approve: `~/.claude/srom-throttle/config.json` with `"connector_prefixes": []`; the WordPress MCP `emcp-tools-*` / `core-get-*` stay paced) |
| 3 | **The backup was 7 days old across a big step** (02.11 → the vol. 19 block choice 08.11, Davis TRANS, the Tittel PTA cut 09.11 04:33). `workspace/` is not in git | `verify_backup.sh` before: `BACKUP OK srom-20261102-2215…`; after `backup.sh`: `BACKUP OK srom-20261109-1633.tar.gz: 2824 paths, sha256 verified, 593M` | will bite | done here |
| 4 | **C-items committed with no status line in `code-to-cowork.md`**: C32, C33, C34 (commits f361823, c0ca62a, de662b7), C41 ("seen", needs none), C42 (e1d98e5), C43 (0f62a4f), C44 (f993111, 7c38fc0). Cowork does not read git, so it cannot see they are done | `grep -E 'C3[234]\|C4[1-4]' code-to-cowork.md` → none; `git log` by message | cosmetic | root (one K-item, here) |
| 5 | K49 (31.10, 9 days) and K50 (03.11, 6 days) have no status line from Cowork; K59 (09.11 06:22) is fresh. Last review's For srom-tlumacz 1 asked srom-tlumacz for the K49 line, but a K-item is answered by Cowork, so it went to the wrong reader and has no status line either | `grep -c 'K49\|K50' cowork-to-code.md` → 0; no `Status of review 02.11.2026` in `tlumacz-to-produkcja.md` | cosmetic | Cowork; root closes the misrouted item |
| 6 | srom-tlumacz `HANDOVER.md:12` says the termbase has 40 rows, 4 PROVISIONAL; it has 43, 7 PROVISIONAL (C-0051–C-0053 added by C42) | `csv` count of `tlumacz-tb.tsv`: 43, HOUSE 24, CANDIDATE 12, PROVISIONAL 7; `check_tb --shape` 43 rows | cosmetic | srom-tlumacz (a count, no judgement: root) |
| 7 | `_handoffs/README.md` § Text codes lacks DAV, STE, TPA and V18, all in use in the ledger and STATUS.md ("the session that starts a new text adds its row") | README table: NDI PAH OST TIT WOH SCH V19 GEN SYS IDEA; STATUS.md `— code DAV/STE/TPA`; ledger codes include V18 | cosmetic | root |
| 8 | **Leftovers outside their place.** One folder's top level: `_tmp_nonexistent/` (empty, 03.11 23:51) and `SROM19_szacunek_przekladow.xlsx` (08.11 22:06, in no record). `workspace/`: `srom-tlumacz/_chk_tmp/` (15 page renders, 04.11), `_c19/` (empty, 19.10), `_to_delete/` (2 PNG, 21.10). `srom-tlumacz/work/tittelpta/src/pl/`: four Polish-edition PDFs (167 MB) and `txt/` inside the frozen `src/` folder, in no record (they also account for most of the backup's growth, 351M → 593M). `1. Inbox/come-aloft-jack-little-ape.txt` is an `extract.py` output (11.10) written into MB's Inbox | `ls -la`; `grep` of STATUS.md, the ledger, `pool.md`, the cards and the notes sheets | cosmetic | Cowork (housekeeping: archive what a session made); MB (the xlsx: yours?) |
| 9 | Ledger SYS-1's Detail path `srom-quant/assets/srom-scholarly.php` is not from `workspace/` (it is in Code's skills), so the red path leads nowhere | `MB-decisions.md:942`; the file exists at `$P/srom-quant/assets/` | cosmetic | Cowork |
| 10 | K59's heading time (06:22) is later than its commit (06:21:28): typed, not taken from `date` | `git blame` on `code-to-cowork.md:888`, commit 53cabc4 | cosmetic | — (noted; the rule stands) |
| 11 | Two milestones still have `?` and passed dates: the quiet author-facing announcement, the author query lists (last review 7) | STATUS.md § Milestones | will bite | MB |
| 12 | Five stray `tmp_obj_*` in `.git/objects` (last review 9) | `git count-objects -vH` → garbage: 5 | cosmetic | root, on MB's word (`git gc`) |

Checked and clean, so not findings: the repository is clean and `origin/main` = HEAD (0 ahead, 0 behind): last
review's push failure is gone. No new duplicate IDs (E9, E18, T20 are the known pre-move ones); no E/T items since the
last review. Every "needs MB" K-item since then (K56–K58) is in the ledger (OST-100, OST-101, DAV-107, DAV-108); K59 is
nine hours old. No gates file changed since the last review, so no tool gate to re-run. All nine root
`.claude/skills/` links and all eight `~/.claude/skills/srom-*` / `wp-*` links resolve into the repository; every
relative reference in the nine skills' Markdown resolves (the cross-skill ones in the named skill). The installed
srom-naczelny now says 29/29 and no `computer://` links (last review 5: fixed). Biurko: no answered items or new notes
waiting; open items 85 = ledger 85 (30 older docs carry no `status` and count as open in `desk_push.py`); last sync
05:11, after the last record change (04:51). Throttle breaker ok, 0 calls in the last hour; this review made no site
call. `3. PDF online/`: 15 exports, 25 results in `ready/` (vol. 17's 10 included) plus three `_superseded_*` folders.
Inbox: everything else is accounted for by a record.

## Last review's findings

Review 02.11.2026: 1 (push) fixed — `origin/main` = HEAD; 2 (SROM 2026 row) holds — `dir: True` in today's bundle;
3 (`SRom art dump`) closed — row dropped on MB's word (GEN-139, `desk_sync.py:195`); 4 (⭕ clause) holds; 5
(srom-naczelny) fixed by MB's upload; 6 (backup) done then, recurred (finding 3 here); 7 (two milestones) open
(finding 11); 8 (`zizek-prep-prompts.md`) closed — no longer in the Inbox; 9 (git garbage) open (finding 12); 10 (K49)
open (finding 5).

## For srom-produkcja

Nothing. Its tests, contract and docs are consistent; finding 1 needs no tool change.

## For srom-tlumacz

1. `srom-tlumacz/HANDOVER.md:12`: "40 rows, 08.10.2026: 24 HOUSE, 4 PROVISIONAL — C-0042 othering (V19-100), C-0046,
   C-0047, C-0050 —, 12 CANDIDATE" → 43 rows (09.11.2026): 24 HOUSE, 7 PROVISIONAL (C-0042, C-0046, C-0047, C-0050,
   C-0051–C-0053 from the Davis draft, C42), 12 CANDIDATE. Verify: `tlumacz-check_tb.py --shape` → 43 rows.
2. Review 02.11.2026, For srom-tlumacz 1 (a K49 status line): declined as misrouted — K-items are answered by Cowork;
   carried into this review's K-item.

## For MB

1. **The live-site hook** (finding 2): say yes and `~/.claude/srom-throttle/config.json` gets
   `"connector_prefixes": []`, so EPLA's staging connector no longer counts as the SROM site. The SROM WordPress MCP
   and every call naming studiaromologica.pl or seohost.pl stay paced.
2. **Tittel PTA** (finding 1): nothing to decide. Cowork renames the Markdown files when you have closed the Word copy;
   your Word master keeps its name and is not touched.
3. **Two milestones need a date** (still): the quiet author-facing announcement, and the author query lists.
4. `SROM19_szacunek_przekladow.xlsx` at the top of Redakcja (08.11 22:06): yours, or a session's to file?
5. `git gc` to clear five harmless temp objects: yes / leave it.
