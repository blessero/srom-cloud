# Cross-module review — [general] 03.10.2026 (01:25–01:29)

Delta review, at MB's request: only what changed since `review-02.10.2026.md` (22:19). Main subject: srom-tlumacz
packaged as a skill (leaf 1.4.1, srom-tlumacz 675d2b6, E20 [general]). Minor: srom-quant `mint_suffixes.py`
(srom-produkcja e71b068). Reviewer only: nothing in `srom-produkcja/` or `srom-tlumacz/` was changed by this review.
Repos at start and end: srom-produkcja e71b068, srom-tlumacz fa0d755, `_handoffs` 61212a8 (before this file); all
three working trees clean at start and end.

## Conclusions

1. **The packaging holds.** `~/.claude/skills/srom-tlumacz` is a symlink into the srom-tlumacz repo; the scripts find
   srom-produkcja, srom-kanon, srom-quant and the module folder from any working directory; all four checks in
   srom-tlumacz's CLAUDE.md pass as written. Each file has one home: no copies left at the module root or in `work/`.
   SKILL.md is 133 lines and cites the Kanon by § without pinning a version.
2. **Tests are green on both sides.** SUITE ALL PASS 24/24 (srom-produkcja e71b068); HANDOFF CONTRACT 33/33 (34 → 33:
   the withdrawn E5 terminology-slot case, as E20 says); draft_check unchanged from 1.4.1's pre-move measurement.
3. **Gate 1.4.1 re-measured:** every CHECK that does not depend on git (G1, G2, G6–G11) gives its EVIDENCE again;
   G3–G5 are the standing checks above.
4. **The move left one broken pointer outside srom-tlumacz.** srom-produkcja's closed gate F3 (`GATES.md:156`) still
   calls `../srom-tlumacz/tlumacz-test_handoff.py`, which now fails with "No such file". It is a closed gate, so this
   only bites a re-run. srom-tlumacz's own closed gates cite old paths too, but leaf 1.4.1 says so once in its gates
   file and in HANDOVER, which is enough.
5. **E20 has no status line from srom-produkcja yet.** E20 came 1 minute before srom-produkcja's last commit, so this
   is not a lapse. The terminology slot E20 withdraws is still in `handoff.md`.
6. **The checkup skill still points to the PLAN for srom-tlumacz's file formats**, which have moved to the skill's
   `references/outputs.md`. The PLAN now points there too, so this is cosmetic.
7. **`mint_suffixes.py`:** tested (`test_quant.py`, in the 24/24 suite). It writes only the master CSV, refuses a
   foreign prefix, never changes a final suffix, and touches no contract with srom-tlumacz. Nothing to fix.
8. **Last review: all rows done.** G12 is deliberately kept open by srom-produkcja, and 29.09 #5 is still with MB.

## Verdict lines as printed

srom-produkcja, `python3 .claude/skills/srom-produkcja/tests/run_all.py`, commit e71b068 (tail):
```
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 12/12
SUITE ALL PASS 24/24
```
srom-tlumacz, the four commands of its CLAUDE.md § Checks (venv), against srom-produkcja e71b068:
```
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 33/33
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```
Gate 1.4.1 CHECKs re-run (read-only): `FRONTMATTER OK` · `PATHS OK 14 (10 in this skill)` · `4` / `TB-OK` (from a
temp dir) · `0` (no root copies) · `CLAUDE CHECKS 4/4 ok` · `LEAN 133` · `0` (no old script calls) · `2`.
`tlumacz_paths.py` from `/private/tmp`: srom-produkcja, srom-kanon, srom-quant → `~/.claude/skills/…`; `--module` →
`…/srom-tlumacz`.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | Closed gate F3 calls srom-tlumacz's contract test at its pre-1.4.1 path | `srom-produkcja/GATES.md:156`; run → `can't open file '…/srom-tlumacz/tlumacz-test_handoff.py'` | cosmetic (fails only on a re-run) | srom-produkcja |
| 2 | E20 [general] has no status line; the withdrawn terminology slot is still in the contract | `_handoffs/produkcja-to-tlumacz.md` (no E20); `handoff.md:102–103` (commented `tb_check.py` lines), `:107` `[--queries <id>_pytania_tb.csv]` | cosmetic | srom-produkcja |
| 3 | The checkup skill reads srom-tlumacz's contract only from the PLAN; the file formats (OUT-*, incl. OUT-DELIVERY) now live in the skill's `references/outputs.md`, and the skill's SKILL.md is not in its reading list | `_handoffs/checkup/SKILL.md:27`, `:50`; `tlumacz-PLAN.md:45` | cosmetic | MB (root session) |

## Last review's findings

| # (02.10) | finding | now |
|---|---|---|
| 1 | T31–T35 unanswered, drafts behind | fixed: status lines 03.10 00:11; 0 numbered headings and 0 `tłum./Tłum. z przekładu angielskiego` in the four drafts (grep) |
| 2 | Linter misses capitalised annotation | fixed (srom-produkcja, 03.10 00:10, test case) |
| 3 | T30 rename step missing in OUT-DELIVERY | fixed: `references/outputs.md:69–70`; handoff test case added (then 34/34) |
| 4 | MB's decisions of 21:30 not applied | fixed: Kanon v1.16, T36, answered by srom-tlumacz 01:11 |
| 5 | Uncommitted notes-sheet line | fixed |
| 6 | Entry times later than commits | fixed (T35 correction line); root-session times: not re-checked here |
| 7 | Stale text, srom-produkcja | fixed; G12 kept open by decision (until an MB-edited text with an asterisk series is placed) |
| 8 | Stale text, srom-tlumacz | fixed: IF-KANON v1.16; SKILL.md cites the header version, so it cannot go stale |
| 29.09 #5 | Source-changing decisions before the Word edits | **still open** (MB) |

## For srom-produkcja

1. `GATES.md:156` (gate F3): change the CHECK's path to `~/.claude/skills/srom-tlumacz/scripts/tlumacz-test_handoff.py`
   and add `NOTE <date time>: path updated after srom-tlumacz leaf 1.4.1 (review 03.10.2026 row 1); gate closed as of
   its original date.` Verify: run the CHECK; expect `GAP CLOSED ok  E16` and `HANDOFF CONTRACT 33/33`.
2. E20 [general]: write its status line. When you next touch `references/handoff.md` (no need to do it just for this),
   delete the two commented terminology-slot lines (`:102–103`) and `[--queries <id>_pytania_tb.csv]` (`:107`). Verify: suite
   24/24, and srom-tlumacz's `tlumacz-test_handoff.py` still 33/33.

## For srom-tlumacz

Nothing.

## For MB

1. Optional, root session, a two-line edit to `_handoffs/checkup/SKILL.md` (row 3): add srom-tlumacz's
   `.claude/skills/srom-tlumacz/SKILL.md` and `references/outputs.md` to "Read first", and in check 4 read "OUT-DELIVERY"
   from `outputs.md`. Say the word and the root session makes it.
2. Unchanged from earlier reviews: the source-changing decisions (PAH-2, TIT-2, TIT-7, V19-1) are best made before you
   start editing the Word copies.
