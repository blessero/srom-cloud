# Review 02.11.2026 — full-suite milestone checkup [general]

Run from the one folder in Claude Code on the Mac, at MB's request ("full suite milestone checkup"), under unlazy
gates. Both scopes in one pass: Code's checkup (`checkup/SKILL.md`: tools, contract, docs, Kanon, gates, channel,
hygiene) **and** Cowork's (`checkup/COWORK.md`: texts, ledger, desk, MB's folders), because one session had both.
Nothing in `srom-produkcja/` or `srom-tlumacz/` was changed. Three things were fixed where no decision was needed
(findings 2, 4, 6).

## Conclusions

1. The toolchain is green on every scripted check: suite 29/29, the three srom-tlumacz checks, the handoff contract
   35/35, `desk_sync.py` `problems=0`, all eight hand-off manifests, all seven frozen `src/` copies.
2. The one thing that is actually broken is the **off-Mac backup**. The GitHub push has not run since
   31.10.2026 00:34; today's commit sits on the Mac only, and `git push` from a non-interactive session fails for
   credentials. That repository is the only off-Mac copy of the skills; `workspace/` has no off-Mac copy at all,
   only the local tarballs, and the newest of those was 7 days old while the whole vol. 19 Zizek selection was
   written. A fresh one was made here.
3. MB's "SROM 2026: folder or file?" is answered: **folder.** It is a real directory. The row flipped because
   `desk_sync.py` stat'ed a path above the one folder, which Cowork cannot see. Fixed.
4. Two documents told sessions to write the pre-K37 `Files to open:` line (one of them contradicting itself three
   lines later). Fixed in both. The same staleness is in the installed srom-naczelny skill, which only MB can
   replace.
5. The first staged deep review (Tittel PTA ch. 2) is clean against its own spec: all eight pass files present and
   headed, 584 anchors checked, 0 missing, 0 close, and the card updated at the same minute as Pass 5.
6. The ledger, the Kanon, the module channel, MB's folders and the repository's hygiene have nothing to fix.

## Verdict lines as printed

```
SUITE ALL PASS 29/29                                     (srom-produkcja tests/run_all.py, at 53e95d2)
columns: 17/17 defined; schema fields: 17/17 present     (tlumacz-check_tb.py)
shape: 40 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 14/14
training quotes verified: 25/25
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 35/35                                   (tlumacz-test_handoff.py)
02.11.2026 22:13 decisions=97 glance=97 files=20 texts_v19=7/7 articles=17:10,18:15,19:0 milestones=23
  archive=7 preflight='SUITE ALL PASS 29/29' problems=0 ikonograf=6
  pool=19-2026:64 selected:0,candidate:21,mark:0,background:34,out:9,other:0      (desk_sync.py)
BACKUP OK srom-20261102-2215.tar.gz: 2341 paths, sha256 verified, 353M            (verify_backup.sh, after backup.sh)
```

Hand-off manifests (`shasum -a 256 -c`), 8 of 8, 33 entries, 0 failed:
ndiaye, ostendorf, pahulich, steiner, tittel, tittelpta, westohueri (4 each) and `srom-produkcja/work/ostendorf/pl/SHA256SUMS` (5).
srom-tlumacz `src/` against srom-produkcja's frozen files: 23 files compared, 0 differing.

srom-zizek deep review, `check.py volumes/19-2026/deep/tittel-pta-ch2-*.md`:
pass 0 314/314 found · 1 91/91 · 2 56/56 · 2b 3/3 · 3 8/8 · 4 21/21 · 5 4/4 · rebuttal 87/87 — 584 anchors, 0 close, 0 missing.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | **The GitHub push has not run since 31.10.2026 00:34.** `origin/main` = 27b2b3f (31.10 00:34); local HEAD = 53e95d2 (02.11 21:59, C37). Push from this session fails on credentials, so every session that commits and cannot push leaves the backup behind silently | `git ls-remote origin main` → 27b2b3f; `git log -1 origin/main` 2026-10-31 00:34; `git push origin HEAD:main` → `fatal: could not read Username for 'https://github.com': Device not configured`; `credential.helper=osxkeychain`; `gh: command not found` | blocks | MB (push from a terminal), then root |
| 2 | **Biurko's `SROM 2026` row flipped folder ↔ file with the host the sync ran on.** `desk_sync.py` set `dir` from `os.path.isdir()` on a path above the one folder; Cowork mounts only `Redakcja/`, so `SROM/SROM 2026` came back `dir: False` there and `True` on the Mac. Same for `SRom art dump`. Each sync then wrote the row back the other way | bundle of 02.11 21:54 (Cowork run): `SROM 2026 dir=False`; Mac run 22:13: `dir=True`; on disk `drwxr-xr-x 10 … SROM 2026`; `desk_sync.py:161–177` | will bite | done here (`add(..., isdir=True)` for the two rows above the one folder, with the reason in a comment) |
| 3 | **`SROM/Czytelnia/SRom art dump` does not exist**, so that row of the files bar is a dead link; `add()` never checks existence for an absolute path | `ls -ld` → No such file or directory; `find SROM -maxdepth 3 -iname '*art*dump*'` → nothing | will bite | MB (the new path, or drop the row) |
| 4 | **Root `CLAUDE.md` § Files MB must open contradicted itself**: l. 171 "in replies the marker is the ⭕ described below" against l. 176 "No ⭕ or `file://` links: they did not open in the app (MB, 24.10.2026)". `workspace/CLAUDE.md` § Files MB must open still carried the pre-K37 one-line format | the two lines; K37 (`code-to-cowork.md:547`, commit 15719c7) | will bite | done here (both files) |
| 5 | **The installed srom-naczelny skill is stale on two points**: its preflight line says `SUITE ALL PASS 26/26` (real 29/29), and § Language and conduct tells sessions to end a production reply with `computer:///…` links, which K37 retired. It is changed only by a new upload | the skill text as loaded in this session; `run_all.py` → 29/29; K37 | will bite | MB (new upload) |
| 6 | **The backup was 7 days old** (srom-20261026-1525) while `workspace/`, which is not in git, grew by the whole vol. 19 Zizek selection (27.10–02.11: ~30 cards, pool, block, 8 deep-review files) | `verify_backup.sh` before: `BACKUP OK srom-20261026-1525…`; `ls -t` on the cards and `deep/` folders | will bite | done here (`backup.sh`, then `verify_backup.sh` → BACKUP OK srom-20261102-2215, 2341 paths, 353M) |
| 7 | **Two milestones are past their date with no new one and are waiting on MB.** `desk_sync.py` does not flag them because their `when` is `?`, so they are invisible to the clean-sync rule | STATUS.md § Milestones: "Quiet author-facing announcement" (`?`, "≈30.10.2026 passed"), "Author query lists sent" (`?`, "not sent by ≈20.10.2026") | will bite | MB (a date for each) |
| 8 | `1. Inbox/zizek-prep-prompts.md` is the one file in the Inbox that no record names | grepped each loose Inbox name against STATUS.md, `pool.md` and the ledger: 15 of 16 accounted for (by slug, pool row or STATUS line), this one in none | cosmetic | MB or Cowork (say what it is, or that it is MB's own) |
| 9 | Five stray `tmp_obj_*` in `.git/objects` from an interrupted write | `git count-objects -vH` → 5 `warning: garbage found`; `ls .git/objects/*/tmp_obj_*` → 5 | cosmetic | root (`git gc` on MB's word; harmless) |
| 10 | K49 (31.10.2026 00:14) has no status line from Cowork; it is two days old | `grep "K49" cowork-to-code.md` → 0 | cosmetic | Cowork |

Checked and clean, so not findings: K31 and K42–K45 are Code reporting its own work and ask nothing; K36 and K37 fold
into K38, which is applied (workspace `CLAUDE.md` srom-ikonograf line, STATUS.md Pahulich/Tittel ikonografia lines);
K33, K34, K40, K46–K48 are recorded in STATUS.md and K32 in the ledger. The duplicate IDs E9, E18 and T20 are the known
pre-move collisions already named in the reviews of 29.09 and 07.10.2026; no new ones. E17–E19 all have status lines
(`produkcja-to-tlumacz.md:481–486`), T39 and T40 both have theirs (`tlumacz-to-produkcja.md:300, 307`).
Kanon v1.19 is consistent across the Kanon header, the last row of § 17, `RULES.md` and srom-kanon `SKILL.md`.
Ledger: 97 glance rows = 97 sections, no duplicates, every "Next free" above the highest open number in its code
(12 codes checked). Hygiene: the one folder's top level holds only MB's four folders, `SROM edit and trans/`,
`workspace/` and `Claude outputs/`; all nine `.claude/skills/` links and all eight `~/.claude/skills/srom-*` /
`wp-*` links resolve into the repository; the working tree is clean. `3. PDF online/`: 15 vol. 18 exports, 15 results
in `ready/` under their contract names, plus vol. 17's 10 — nothing unaccounted.

## Last review's findings

Review 26.10.2026: items 1–6, 10 and 12 were marked done there and the files agree. Item 7 (no T-item for the
Kanon "1.18, uzup. 26.10.2026" row) and item 8 (T39 without a status line from srom-tlumacz) are now closed: T40
carries Kanon v1.19 and both T39 and T40 have status lines. Item 9 (another session's uncommitted sources.md
paragraph and K43 addendum 6) is committed — the tree is clean. Item 11 (per-query scripts holding sheet content in
Python source) is MB's decision and is untouched here.

## For srom-produkcja

Nothing. Its tests, gates, contract and docs are consistent, and nothing in finding 1–10 lies in its folder.

## For srom-tlumacz

1. One status line, when a session next opens the channel: K49 (`code-to-cowork.md:754`) — read and nothing to do, or
   what you changed. It is the only K-item older than two days without one.

## For MB

1. **GitHub: keep it, and push.** The repository `blessero/srom-cloud` is private and is the **only off-Mac copy of
   the skills and the hand-off records**. It has nothing to do with cloud sessions (those ended 07.10.2026, K14) —
   that is only what the name says. What to drop is the idea that sessions can keep it current: push from a terminal,
   where the keychain can answer:
   `cd "/Users/michalbartosz/ARBEIT/Bima/SROM/Redakcja/SROM edit and trans" && git push origin HEAD:main`
   If you would rather sessions did it themselves, install `gh` and `gh auth login` once, or switch the remote to SSH.
   Say which, and the rule in root `CLAUDE.md` § Git is rewritten to match — as it stands it tells every session to do
   something that fails.
2. **`SROM 2026`: it stays a folder.** Done; nothing for you.
3. **`SRom art dump`:** `SROM/Czytelnia/SRom art dump` is gone. Where is it now, or should the row leave Biurko?
4. **srom-naczelny:** it needs a new upload (finding 5). Say the word and the corrected text is prepared.
5. **Two milestones need a date:** the quiet author-facing announcement, and the author query lists.
6. `1. Inbox/zizek-prep-prompts.md`: yours, or something a session should take?
