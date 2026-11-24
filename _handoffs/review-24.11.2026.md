# Review 24.11.2026 — milestone checkup of the whole suite [general]

Run from the root session in Claude Code on the Mac, at MB's request ("perform a full milestone checkup of the srom
suite"), by `checkup/SKILL.md`, with `checkup/COWORK.md`'s text checks in the same pass (srom-naczelny § Where the
session runs). Nothing in `srom-produkcja/`, `srom-tlumacz/` or `workspace/` was changed during the review; the
take-back and build trial ran on copies in the session's scratchpad. Done where no decision was needed: a fresh backup
(finding 7). The repository was even with `origin/main` at start (0 ahead, 0 behind, clean, HEAD 403d115).

## Conclusions

1. **The tools are green and the next milestone is not blocked by them.** Suite **31/31** at 403d115 (one more file
   since 18.11: `test_review_header.py`), termbase 46 rows / 0 problems, selftest 9/9, handoff contract 35/35, every
   draft balanced (Pahulich now `marks (Word) 10=10`: S1 is back), every Kanon § cited in the skills and CLAUDE.md files
   resolves, Biurko `problems=0`, breaker ok.
2. **Pahulich is buildable.** On copies of today's files: `TAKE-BACK OK pahulich (5 files)`, `check.py --pair: CHECK
   OK`, `normalize` 0 changes / 3 flags, **`build.py` → PASS** (on 18.11 it failed on `[BRAK MIEJSCA]` in notes 46 and
   144; B10 on 22.11 closed them). INJECT for Pahulich waits only on the author letter, not on the toolchain.
3. **One substantive gap: the PAH-9 letter misses two certain findings.** K75 (21.11) found that the Thomasius words
   (n. 84) are Lewy's paraphrase, not a quotation, and that Browne's „artificial Negroes” is not in the 1646 edition the
   article dates it to. The letter was put in its final form on 22.11 without either question; S9 in the notes sheet
   still plans a translator's note for an original that does not exist, and Browne has no S-item. The letter is unsent,
   so it is cheap to fix now and expensive after.
4. **Kanon v1.21 is consistent** (header, § 17, RULES.md, srom-kanon SKILL.md; T42 announced it). The v1.20 supplements
   of 24.11 (C62, C63) were folded the same night, so the "no appended supplements" finding of 18.11 did not recur in
   the end.
5. **Bijak is already in InDesign** (23.11 23:53, built fresh from `SROM_szablon_v3.idml`, scripts RESULT: OK), so
   the new *Recenzja NAGŁÓWEK* style has met InDesign — but no record says the header took it, so K70's check is
   still formally open, and that session's one lesson (an old template with „Cambria (TT)” breaks
   `srom_style_setup.jsx`) waits unrouted.
6. Record-keeping again, for the third review running: since 19.11 Code sessions write their answers to C-items into
   Cowork's own file (C58, C61, C62, C63) instead of `code-to-cowork.md`, and C59 has no answer; K70 and K73–K80 have no
   Cowork line. Nothing is lost — the work is done — but the channel rule is not holding.
7. Last review's findings: 1–4, 7–12 closed; 5 and 6 (status lines) recurred as findings 2 and 3 here.

## Verdict lines as printed

```
SUITE ALL PASS 31/31                                          (srom-produkcja tests/run_all.py at 403d115)
columns: 17/17 defined; schema fields: 17/17 present          (tlumacz-check_tb.py, exit 0)
shape: 46 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 16/16
precedent quotes in rows not yet HOUSE: 0/0
established rows: 14, all with >=2 sources
training quotes verified: 25/25
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 35/35                                        (tlumacz-test_handoff.py, at 403d115)
tlumacz-draft_check.py --all (exit 0):
  DRAFT davis: leftover 0, marks 12=12, quotes 42/42 (double 11, single 32; 0 bad class, 0 open rows unmatched)
  DRAFT ndiaye: leftover 0, marks 7=7, quotes –
  DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (double 43, single 1; 0 bad class, 0 open rows unmatched)
  DRAFT pahulich: leftover 0, marks (Word) 10=10, quotes –
  DRAFT steiner: leftover 0, marks 10=10, quotes 18/18 (double 18, single 0; 0 bad class, 0 open rows unmatched)
  DRAFT tittel: leftover 0, marks 12=12, quotes 35/35 (double 34, single 1; 0 bad class, 0 open rows unmatched)
  DRAFT tittelpta: leftover 0, marks 44=44, quotes 6/6 (double 6, single 0; 0 bad class, 0 open rows unmatched)
  DRAFT westohueri: leftover 0, marks 7=7, quotes 15/15 (double 3, single 12; 0 bad class, 0 open rows unmatched)
24.11.2026 18:37 decisions=73 glance=73 files=16 texts_v19=6/6 articles=17:10,18:15,19:8 milestones=23 archive=29
  preflight='SUITE ALL PASS 31/31' problems=0 ikonograf=10 czytnik=32 letters=1 ...       (desk_sync.py, read-only)
TOTAL archive 1, tag 4, notes-docx 4  (dry run: nothing changed; add --apply)          (workspace/gen/tidy.py)
BACKUP OK srom-20261124-1836.tar.gz: 8279 paths, sha256 verified, 833M   (backup.sh, then verify_backup.sh)
breaker: ok; calls in the last hour: 0                        (srom-throttle.py --status)
src manifests (shasum -c): davis, ndiaye, ostendorf, pahulich, steiner, tittel, tittelpta, westohueri: 0 bad each
```

On copies (scratchpad): Pahulich take-back from srom-tlumacz `work/pahulich/` (master 9a4d8834…5b5010d, `_pl.md`
e483e2ad…7a328a2) with srom-produkcja's `pahulich_src.md` and `refs.json` → `check.py --pair: CHECK OK`,
`TAKE-BACK OK pahulich (5 files)`; `normalize: 0 changes, 3 flags`; `build.py` → `PASS`.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | **The PAH-9 letter lacks K75's two questions** (Thomasius n. 84 = Lewy's paraphrase, not a quotation; Browne „artificial Negroes” not in 1646, found in 1658 p. 403 and 1672 p. 376). The letter was finalised 22.11 05:40, after K75 (21.11 06:47); `pahulich_uwagi.md` S9 still plans „Tłum. z przekładu angielskiego” for a Latin original that does not exist; no S-item for Browne; K75 has no Cowork line | `grep -c 'Thomasius\|Browne' srom-tlumacz/tom19_listy_do_autorow.md` → 0; `pahulich_uwagi.md:30` (S9 „oryginał łaciński nieodszukany”); STATUS.md l. 111; K75 | will bite (letter is unsent: fix before it goes) | Cowork (S9 updated, a Browne S-item, the two questions drafted into § 1 of the letter); MB (wording, and whether they go in) |
| 2 | **C-item answers written in Cowork's file, not `code-to-cowork.md`**: C58 (c9b1eef, 1313ffe), C61 items 1 and 3, C62 (ceee8c9, 389140c); C63's heading is itself a done-report in Cowork's file, dated „24.11.2026 24.11.2026 01:10”. **C59** (rip-pitfalls § INJECT, committed 5746083) has no answer anywhere | `git blame cowork-to-code.md` l. 751, 752, 764, 770, 772, 774; `grep -cE '\bC(58\|59\|61\|62\|63)\b' code-to-cowork.md` → 0 each | cosmetic (recurring: 09.11 #4, 18.11 #5) | root (one K-item with the status of C57–C64, here) |
| 3 | **K70, K73–K80 have no status line from Cowork.** Their asks are mostly done in workspace (K71: milestones and the Grellmann line reworded; K78: no 🔴 left before the two superseded paths), K75 is not (finding 1) | `grep -cE '\bK(70\|7[3-9]\|80)\b' cowork-to-code.md` → 0 each | cosmetic | Cowork |
| 4 | **K70's InDesign check of *Recenzja NAGŁÓWEK* is not recorded.** K70 (18.11) asks MB to check the style in InDesign. Bijak was laid out from `SROM_szablon_v3.idml` on 23.11 (scripts OK, "for MB's eye"), but the STATUS line does not say whether the header took the style; no ledger item. The same line's lesson — a vol. 18 template with „Cambria (TT)” breaks `srom_style_setup.jsx` — is a tool lesson, unrouted (it waits in `lessons.md` by design) | STATUS.md l. 192; `grep -niE 'nagłówek\|K70' MB-decisions.md STATUS.md` → none; K70 l. 1095 | cosmetic | MB (one look at the header in `12_Bijak_work.indd` closes K70); Cowork (route the lesson: one line in srom-produkcja `references/indesign.md`, "start from the v3 template", is the cheapest) |
| 5 | **The one folder's top level holds `ws2.json`** (19.11, a Wikisource search dump: „Antologja literatury francuskiej/Molier”), against root CLAUDE.md § The one folder. Also `.claude/launch.json` (21.11, the Kontaktówki preview config of K76): a session config, harmless, left | `ls -la Redakcja/` | cosmetic | MB (archive to `workspace/_archive/`: yes / no) |
| 6 | **`tidy.py` has work**: Pahulich `pahulich_pl_import.md` to `_archiwum/`; 4 Finder tags (ndiaye 2, pahulich 2); 4 `_uwagi.docx` re-renders (davis, ndiaye, pahulich, westohueri) | dry run above | cosmetic | root (`--apply`, as `checkup/SKILL.md` § 9 says) |
| 7 | **Backup 6 days old** across big steps (Pahulich test layout 19.11, ikonograf passes 19–21.11, Bijak and Opocki RIP, Kanon v1.21). Paths 7361 → 8279 | `verify_backup.sh` before: `srom-20261118-1515`; after: `BACKUP OK srom-20261124-1836.tar.gz: 8279 paths, sha256 verified, 833M` | will bite | done here |
| 8 | srom-naczelny's preflight line still expects `SUITE ALL PASS 29/29` (now 31/31). That skill is Cowork's own and changes only by an upload | srom-naczelny SKILL.md § Start of a session, the produkcja preflight comment | cosmetic | MB (next upload of srom-naczelny) |
| 9 | K79 and T42 are headed 02:40 but were committed at 02:38 (35d3280): typed times, not `date` | `git log -1 --format=%cd 35d3280` | cosmetic | noted |

Checked and clean, so not findings: no duplicate C/K IDs; no handoff contract change since 18.11 (`handoff.md`,
`stages.md` untouched; outputs.md only by b5ebecd), so no two-sided test needed beyond 35/35; no gates file changed
since 18.11, so no tool gate to re-run; no web-date lookup instruction left in any skill after v1.21; every Kanon version
cited outside the Kanon that is not 1.21 is historical (HANDOVER/PLAN log lines); every skill link (root
`.claude/skills/`, `~/.claude/skills/srom-*`, the two WordPress skills) resolves into the repository; K76's
`ikonografia_view.py` and `md_html.py` are committed (a8b71aa); `git count-objects` garbage 0; no `dist/`; all eight
`src/manifest.sha256` verify. Pahulich's frozen `src/refs.json` differs from srom-produkcja's (B10, 22.11): known and
logged in STATUS.md ("sync at the next hand-off"), so not a finding. The milestone table already flags that the letters
run past the delivery row (K71 item 1).

## Last review's findings

Review 18.11.2026: 1 (Pahulich S1) fixed — b5ebecd (draft_check reads the master's comments), S1 back in the master
(`marks (Word) 10=10`); 2 (Kanon v1.19 supplements) fixed — 32ca216 (v1.20), recurred briefly and folded again in
35d3280 (v1.21); 3 (ODT docs) fixed — f4e67c0; 4 (review-header style) done in code — 1e7e591, InDesign check open
(finding 4); 5 (C status lines) fixed then, recurred (finding 2); 6 (K62–K68 lines) recurred for K70–K80 (finding 3);
7 (tlumacz HANDOVER) fixed — 9a7405d; 8 (backup) done then, recurred (finding 7); 9 (BIJ code) fixed — a540084;
10 (Biurko problems) fixed — `problems=0`; 11 (checkup SKILL.md) fixed — 63ed4a5; 12 (git garbage) fixed — K72.

## For srom-produkcja

Nothing.

## For srom-tlumacz

Nothing.

## For MB

1. **Pahulich letter (PAH-9)** (finding 1): before it goes, add the two questions K75 drafted — Thomasius (n. 84: Lewy's
   paraphrase, may we drop the quotation marks?) and Browne (n. 83: 1658, not 1646; date it 1658 or "later
   editions"?). Cowork drafts them into the letter and fixes S9 on your word.
2. **Review header in InDesign** (finding 4): when you look at `12_Bijak_work.indd`, check that the review header
   carries *Recenzja NAGŁÓWEK*; that closes K70.
3. `ws2.json` at the top of Redakcja (finding 5): archive it — yes / no.
4. Next srom-naczelny upload (finding 8): the preflight line should read `SUITE ALL PASS 31/31`.
