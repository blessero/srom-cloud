# Review 18.11.2026 — milestone checkup of the whole suite [general]

Run from the root session in Claude Code on the Mac, at MB's request ("run milestone check on the whole suite"), by
`checkup/SKILL.md`. Nothing in `srom-produkcja/` or `srom-tlumacz/` was changed during the review; the take-back, build
and Word export trials ran on copies in the session's scratchpad. One thing was done where no decision was needed: a
fresh backup (finding 8). The repository was even with `origin/main` at the start (0 ahead, 0 behind); one uncommitted
file not made by this session: `_handoffs/checkup/SKILL.md` (finding 11).

## Conclusions

1. The tools are green: suite **30/30** at 593b452 (one more test since 09.11: `test_output_sync.py`), the termbase
   checks (46 rows, 0 problems), selftest 9/9, the handoff contract 35/35, every Kanon § citation resolves, every skill
   link resolves, `tidy.py` has nothing to do, the hook's breaker is ok.
2. **The next milestone (delivery, INJECT, ≈16–30.11) is gated by the author letters, not by the tools.** Pahulich, the
   text furthest on, takes back cleanly on copies (`TAKE-BACK OK pahulich (4 files)`, pair CHECK OK), and the full build
   fails only on `[BRAK MIEJSCA]` in notes 46 and 144 — the dissertation places that wait on the author's answer
   (PAH-9 letter, drafted 13.11, not sent). The "Author query lists sent" milestone still has no date.
3. **Pahulich: one open check lost its Word comment.** S1 (Césaire, n. 5, Polish edition wording and page) is
   `[otwarte]` in the notes sheet, but no Word copy since MB's first master (12.11) carries its DO SPRAWDZENIA comment;
   the other nine do. The export tool keeps it (re-export of the 13.11 draft on a copy: S1–S10 all present), so it went
   in an edit round. The standing `draft_check --all` cannot see this: after MB's master it reads `marks 0≠10` and stays
   red for a known reason, which hides a real gap. Fix: draft_check counts the master's Word comments (srom-tlumacz,
   applied here); the S1 comment itself is Cowork's.
4. **Kanon v1.19 carries two supplements** (11.11 ORCID / author guide; 15.11 book-review header, GEN-144), against the
   rule that an announced version gets no appended changes; RULES.md lacks the review-header rule. Fold into v1.20 with a
   T-item (a srom-produkcja session, as with v1.19 on 26.10).
5. The ODT fix (C55 item 1, 3c76320) left three docs still telling sessions to convert by hand; C55 item 2 (the
   review-header style) is unblocked since GEN-144 and unbuilt. Bijak's review is the first Part III text of vol. 19.
6. The rest is record-keeping again: seven C-items committed with no K status line, K62–K68 without Cowork's line, the
   srom-tlumacz HANDOVER termbase count, the BIJ code missing from the README, Biurko `problems=5`, a 9-day-old backup.
7. Last review's findings: 1, 2, 5, 8, 9 closed; 3, 4, 6, 7 closed then and recurred (findings 8, 6, 9, 10 here);
   11 (milestone dates) and 12 (git garbage) still open.

## Verdict lines as printed

```
SUITE ALL PASS 30/30                                          (srom-produkcja tests/run_all.py at 593b452)
columns: 17/17 defined; schema fields: 17/17 present          (tlumacz-check_tb.py, exit 0)
shape: 46 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 16/16
precedent quotes in rows not yet HOUSE: 0/0
established rows: 14, all with >=2 sources
training quotes verified: 25/25
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 35/35                                        (tlumacz-test_handoff.py, at 593b452)
tlumacz-draft_check.py --all:
  DRAFT davis: leftover 0, marks 12=12, quotes 42/42 (double 11, single 32; 0 bad class, 0 open rows unmatched)
  DRAFT ndiaye: leftover 0, marks 7=7, quotes –
  DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (double 43, single 1; 0 bad class, 0 open rows unmatched)
    only in text: [] only in notes sheet: ['S1', 'S10', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
  DRAFT pahulich: leftover 0, marks 0≠10, quotes –                         (finding 1)
  DRAFT steiner: leftover 0, marks 10=10, quotes 18/18 (double 18, single 0; 0 bad class, 0 open rows unmatched)
  DRAFT tittel: leftover 0, marks 12=12, quotes 35/35 (double 34, single 1; 0 bad class, 0 open rows unmatched)
  DRAFT tittelpta: leftover 0, marks 44=44, quotes 6/6 (double 6, single 0; 0 bad class, 0 open rows unmatched)
  DRAFT westohueri: leftover 0, marks 7=7, quotes 15/15 (double 3, single 12; 0 bad class, 0 open rows unmatched)
TOTAL archive 0, tag 0, notes-docx 0  (dry run: nothing changed; add --apply)   (workspace/gen/tidy.py; every text "=")
18.11.2026 15:16 decisions=76 glance=76 files=17 texts_v19=6/6 articles=17:10,18:15,19:0 milestones=23 archive=29
  preflight='SUITE ALL PASS 29/29' problems=5 ikonograf=10 letters=0 ...  pool=19-2026:67 selected:6 ...  (desk_sync.py)
BACKUP OK srom-20261118-1515.tar.gz: 7361 paths, sha256 verified, 721M   (backup.sh, then verify_backup.sh)
breaker: ok; calls in the last hour: 0                        (srom-throttle.py --status)
```

On copies (scratchpad): Pahulich take-back from srom-tlumacz `work/pahulich/` (master 9c4aa031…4b05241, `_pl.md`
a0ccc7b9…db04fc2) with srom-produkcja's `pahulich_src.md` and `refs.json` → `check.py --pair: CHECK OK`,
`TAKE-BACK OK pahulich (4 files)`; `normalize.py` 3 changes, 3 flags (ENDASH-IN-WORD „czarno–białość”, QUOTE-AMBIG
„nie-»Europejczyków«”); `build.py` → `FAIL — do not typeset`, one error: `[BRAK MIEJSCA]` in notes 46, 144. Re-export
of the archived 13.11 draft (`_archiwum/kalibracja_20261113/before_prepass.md`) with `export_work.py`: 10 S-comments,
S1 included.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | **Pahulich S1's Word comment is gone, and the standing check cannot see it.** The notes sheet has S1 `[otwarte]` (Césaire, n. 5); the master and every Word copy since 12.11 hold S2–S10 only. `draft_check --marks` compares `_pl.md` with the sheet, but after MB's first master `_pl.md` is a Word import with no comments, so it reads 0≠10 for every text past that point and `--all` stays red for a known reason | `word/comments.xml` of `pahulich_robocza{,_old1,_old2,_old3,_v2}.docx`: S2–S10, no S1; `pahulich_uwagi.md:14`; the 13.11 draft re-exported on a copy keeps S1; `tlumacz-draft_check.py:45` reads only `_pl.md`; STATUS.md l. 99 "S-marks 0/10 … as expected" | will bite | srom-tlumacz (draft_check reads the master's comments: done here); Cowork (S1 back into the master as a Word comment, or the sheet's line closed if MB settled it) |
| 2 | **Kanon v1.19 has two appended supplements** ("1.19, uzup. 11.11.2026", "1.19, uzup. 15.11.2026") although v1.19 was announced (T40, 26.10). RULES.md has the ORCID change but not the review header | `kanon-redakcyjny.md:721–722`; srom-produkcja `CLAUDE.md` § Working rules ("never append supplements to an announced version"); `grep -i recenzj RULES.md` → none | will bite | srom-produkcja session (Kanon change): v1.20 folding both, RULES.md, SKILL.md, `test_kanon.py` agree; T-item |
| 3 | **Stale ODT instructions** after 3c76320 (`docx_in.py` converts a non-DOCX with soffice, zizek `extract.py` reads `.odt`): three docs still say convert first / `docx_in.py` reads DOCX only / it stops with a `KeyError` | `rip-pitfalls.md:10–12`; `polish-original.md:12–14`; srom-zizek `references/review.md:20`; `test_docx_in.py` C55 cases pass in the suite | cosmetic | srom-produkcja (done here) |
| 4 | **C55 item 2, the review-header style, is unbuilt** though GEN-144 is decided (C56). The Bijak review (Part III, vol. 19) is the first text that needs it | C55, C56 in `cowork-to-code.md`; no `recenzj` style in `config/styles.json` | will bite (at InDesign) | srom-produkcja session (template and setup script need InDesign); cheapest: MB styles the header by hand, as in vol. 18 |
| 5 | **Seven C-items committed with no status line in `code-to-cowork.md`**: C46 (c536433), C48 (6930020), C50 (6086cb6), C53 (8ab6911), C54 (cb7cc20), C55 (item 1 3c76320; item 2 open), C56 (36cdcce). C47, C49, C51, C52 have theirs (K66, K65, K64, K67) | `grep -cE '\bC(46\|48\|50\|53\|54\|55\|56)\b' code-to-cowork.md` → 0 each; `git log` by message | cosmetic | root (one K-item, here) |
| 6 | **K62–K68 have no status line from Cowork.** K68's asks are done in workspace (`workspace/CLAUDE.md:29`, `desk_sync.py:193`), so only the line is missing | `grep -cE '\bK6[2-8]\b' cowork-to-code.md` → 0 each | cosmetic | Cowork |
| 7 | srom-tlumacz `HANDOVER.md:12` says 43 rows (24 HOUSE, 7 PROVISIONAL); the termbase has 46 (29 HOUSE, 5 PROVISIONAL, 12 CANDIDATE). The scripts row lacks `tlumacz-polish_check.py` and `tlumacz-track.py` | `csv` count of `tlumacz-tb.tsv`; `check_tb --shape` 46 rows; `ls scripts/` | cosmetic | srom-tlumacz (counts, no judgement: done here) |
| 8 | **The backup was 9 days old across big steps** (Pahulich's two Word rounds and three polonizacja passes, Ndiaye and Tittel PTA polonizacja, `2. Output/`). Paths 2824 → 7361 | `verify_backup.sh` before: `srom-20261109-1633`; after: `BACKUP OK srom-20261118-1515.tar.gz: 7361 paths, sha256 verified, 721M` | will bite | done here |
| 9 | `_handoffs/README.md` § Text codes lacks **BIJ** (Bijak review), in use in STATUS.md | STATUS.md l. 177 `— code BIJ`; README table ends at IDEA | cosmetic | root (done here) |
| 10 | **Biurko `problems=5`.** Two are false hits: STATUS.md's "Grellmann research done (PAH-1, PAH-100 …)" reads as PAH-1 and PAH-100 being decided, while they stay MB's. Three milestones are past their dates (source-changing questions ≈16.11; Word edits ≈15.11; West Ohueri permission ≈15.11), and two still have `?` (author query lists; the quiet announcement) | `desk_sync.py` output above; STATUS.md § Milestones | will bite (red box on Teraz) | Cowork (reword the 18.11 00:23 line, e.g. "research for PAH-1, PAH-100 done"); MB (dates) |
| 11 | `_handoffs/checkup/SKILL.md` is modified and uncommitted (a `tidy.py` step, "MB 18.11.2026", file time 04:31); not this session's work, no C-item names it. This review followed it (dry run only: Code does not write `workspace/`) | `git status --short` at start and end; `git diff` | cosmetic | MB (commit it: yes / no) |
| 12 | Five stray `tmp_obj_*` in `.git/objects` (reviews 02.11, 09.11) | `git count-objects -vH` → garbage: 5 | cosmetic | root, on MB's word (`git gc`) |

Checked and clean, so not findings: no duplicate C/K IDs; every dated C/K heading since 09.11 is no later than its
commit; no gates file changed since the last review, so no tool gate to re-run; no `.skill` packages in `dist/` (they
matter only before a claude.ai upload); no stale `Claude outputs` / `2. Word` path in the skills or CLAUDE.md files
(only in a closed handoff file); top level of Redakcja holds only the four numbered folders, the repository and
`workspace/`; K65's two quote misses (davis n. 205, tittel n. 21) no longer show (42/42, 35/35). `1. Inbox/
come-aloft-jack-little-ape.txt` is still there, left for MB since 09.11 (C45).

## Last review's findings

Review 09.11.2026: 1 (Tittel PTA cut names) fixed — C45 status 09.11 17:14, `draft_check` tittelpta 44=44; 2 (hook)
fixed — eaa7a6a, K61; 3 (backup) done then, recurred (finding 8); 4 (C status lines) fixed — 2ffafab, recurred
(finding 5); 5 (K49, K50) fixed — C45; 6 (HANDOVER count) fixed — afb065e, recurred (finding 7); 7 (README codes) fixed —
8cf9702, recurred for BIJ (finding 9); 8 (leftovers) fixed — C45; 9 (SYS-1 path) fixed — C45; 10 (K59 time) noted;
11 (milestone dates) open (finding 10); 12 (git garbage) open (finding 12).

## For srom-produkcja

1. Kanon v1.20 (finding 2): fold "1.19, uzup. 11.11.2026" and "1.19, uzup. 15.11.2026" into a new row 1.20
   (`kanon-redakcyjny.md` header and § 17; RULES.md gains the § 1 review-header rule; srom-kanon SKILL.md title;
   every module doc that cites v1.19); `test_kanon.py` and the suite green; T-item to srom-tlumacz announcing v1.20.
   Verify: `grep -c 'uzup\.' kanon-redakcyjny.md` has no 1.19 rows; `grep -i recenzj RULES.md` → 1+.
2. ODT docs (finding 3): `references/rip-pitfalls.md:10–12`, `references/polish-original.md:12–14` and srom-zizek
   `references/review.md:20` — say that `docx_in.py` converts ODT/RTF/DOC with soffice itself (and notes it in
   `_import.md`), and that `extract.py` reads `.odt`; keep "check footnotes after conversion". Verify:
   `grep -n 'KeyError\|reads DOCX only\|convert to DOCX first' <the three files>` → none; suite green.
3. C55 item 2 (finding 4): the review-header paragraph style per Kanon § 1 *Nagłówek recenzji* (styles.json,
   style_spec.json, the template, `srom_style_setup.jsx`, a build check of the elements), tested in InDesign. Or, the
   cheapest version, say in `polish-original.md` § Book reviews that MB styles the header by hand as in vol. 18 until
   the style exists.

## For srom-tlumacz

1. `tlumacz-draft_check.py --marks` (finding 1): when `<id>_pl.md` carries no `DO SPRAWDZENIA: S<n>` and
   `<id>_robocza.docx` exists (the text is past MB's first master), take the S-labels from the master's
   `word/comments.xml` and say so in the line (`marks (Word) a=b`). Add a selftest case. Verify: `--all` → pahulich
   `marks (Word) 9≠10` with S1 named; the other texts unchanged; selftest passes; HANDOFF CONTRACT 35/35.
2. `HANDOVER.md:12` (finding 7): termbase 46 rows (18.11.2026): 29 HOUSE, 5 PROVISIONAL (C-0042, C-0050,
   C-0051–C-0053), 12 CANDIDATE; the scripts row adds `tlumacz-polish_check.py`, `tlumacz-track.py`. Verify:
   `tlumacz-check_tb.py --shape` → 46 rows.

## For MB

1. **Author letters** (conclusion 2): the "Author query lists sent" milestone needs a date. Pahulich's build is blocked
   only by the two dissertation places that the PAH-9 letter asks for; the other three letters (OST-4, TPA-107, WOH-6)
   gate their texts the same way.
2. **Pahulich S1** (finding 1): the check on Césaire's Polish edition (n. 5) is open in the notes sheet but its Word
   comment is not in your master. Did you settle it in Word? If not, Cowork puts the comment back.
3. **Three past milestone dates** (finding 10): source-changing questions (≈16.11), Word edits of the six drafts
   (≈15.11), West Ohueri's written permission (≈15.11): new dates, or mark done.
4. `_handoffs/checkup/SKILL.md` (finding 11): the uncommitted `tidy.py` step — commit it: yes / no.
5. `git gc` to clear five harmless temp objects: yes / leave it.
