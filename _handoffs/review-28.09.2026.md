# Cross-module review — 28.09.2026 (02:40–03:00)

Reviewer only: nothing in `srom-typeset/` or `srom-tlumacz/` was changed. All builds and round trips were run into a
scratch folder. No earlier `review-*.md` exists, so this covers the whole history (srom-typeset: 30 commits, a8ec0a9 → bb13dc8).
A srom-tlumacz session was still running during the review: `HANDOVER.md` changed at 02:51 (new § 7a, "chat closed"). Line numbers below are from after that change.

## Conclusions

1. **Tests are green on both sides.** I measured them myself (verdict lines below). The contract test confirms what srom-typeset reports.
2. **One item blocks the next milestone: E16.** The Word round trip splits the one title note into two blocks, and `check.py --pair`
   then fails. I reproduced it on `ndiaye_robocza_v2.docx`, the file MB is editing. srom-typeset has not answered E16 yet: it was
   filed at 02:42, after srom-typeset's last session (02:37). There is a workaround: re-merge the block by hand after import.
3. **One real contract contradiction: do open editor comments stop the build?** The binding contract and the code say no.
   srom-typeset's own SKILL.md and srom-md.md, and srom-tlumacz's PLAN, say yes. I built Ndiaye with 7 open
   `DO SPRAWDZENIA` (S1–S7) and got "RESULT: PASS — ready for InDesign".
4. **Kanon is consistent.** There is one normative text (v1.7). The version is the same in the Kanon header, § 17, RULES.md,
   srom-kanon SKILL.md, handoff.md and both modules' current docs. All 710 § citations in 112 files resolve to real Kanon headings.
   Two exceptions: srom-kanon SKILL.md's quick rule 9 contradicts § 3.4, and three docstrings still say v1.5/v1.6.
5. **MB-decisions.md holds only pending items** (D3, D5, D6 c). But two open MB/kolegium items in the Kanon (§ 13.2) are not in
   it, and srom-typeset's files still show D1/D2 (decisions 20/22) as open.
6. **srom-tlumacz is not under version control** (neither is `_handoffs/`).
7. **Clean:** no module wrote in the other's folder or outgoing file. Every E/T item has a status line from its receiver,
   except E16 (new). `~/.claude/skills/srom-kanon` and `srom-typeset` are symlinks into the repo. The curator skill that
   srom-tlumacz edited (with MB's permission) matches its package byte for byte. D12–D14 are applied on both sides: kartoteka
   rows, one title-note block, Romka/Romki, v1.7. The Ndiaye source copies are byte-identical, and refs.json matches the
   sha256 in T14.

Everything else is stale text.

## Verdict lines as printed

srom-typeset, `python3 .claude/skills/srom-typeset/tests/run_all.py` (exit 0):
```
ok   test_check.py: CHECK ALL PASS 48/48
ok   test_citemap.py: CITEMAP ALL PASS 29/29
ok   test_csl.py: NOTES ALL PASS 21/21 | BIB ALL PASS 11/11 | POSITION ALL PASS 10/10
ok   test_docx_in.py: DOCXIN ALL PASS 12/12
ok   test_e10.py: E10 ALL PASS 9/9
ok   test_e2e.py: E2E ALL PASS 67/67
ok   test_e8.py: E8 ALL PASS 18/18
ok   test_jsx.py: JSX-DONE | STYLES ALL PASS 8/8
ok   test_kanon.py: KANON ALL PASS 19/19
ok   test_lint.py: LINT 0 ERROR
ok   test_normalize.py: NORMALIZE ALL PASS 42/42
ok   test_pdf.py: PDF ALL PASS 10/10
ok   test_pdf_layout.py: PDF-LAYOUT ALL PASS 25/25
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 15/15
SUITE ALL PASS 14/14
```
srom-tlumacz, the checks in its CLAUDE.md (all exit 0):
```
columns: 17/17 defined; schema fields: 17/17 present
shape: 18 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 11/11
established rows: 8, all with >=2 sources
selftest: 7/7 negative controls caught
   KNOWN GAP FAIL  E16: Word round trip keeps the two-paragraph title note as one block
HANDOFF CONTRACT 25/25
tlumacz-gates-1.1.md: 14 gates
ALL MET (14 met)
```
Ndiaye, re-measured by me:
- `check.py --pair` → CHECK OK (3 number warnings)
- `build.py` (both refs files, `--pair-src`, `--queries`) → PASS, Errors: none, lint 0 errors
- `tlumacz-front_check.py` → FRONT OK
- `export_work.py` → `docx_in.py` → `check.py --pair` → **CHECK FAIL 1 error(s)** ("2 title-note blocks")

## Findings

| # | Finding | Evidence | Severity | Fixes |
|---|---|---|---|---|
| 1 | **E16 unanswered.** The Word round trip splits a two-paragraph `::: przypis-tytulowy` into two blocks, so the pair check fails at the pilot's hand-back. | `tlumacz-to-typeset.md:136–138`; no T-item after T15 (`typeset-to-tlumacz.md:203`). Reproduced: `ndiaye_pl.md` → `export_work` → `docx_in` gives 2 blocks, and `ndiaye_robocza_v2.docx` imports as 2 blocks. Both give `CHECK FAIL 1 error(s)`. tlumacz test: `KNOWN GAP FAIL E16`. | blocks (the manual re-merge works) | srom-typeset |
| 2 | **Open comments: the contract says they never block; three documents say the build fails.** In practice, nothing stops an unresolved Polish-edition quote (Kanon § 12.2.4) from reaching the typesetter, and after the Word round trip the comments leave the text and are listed only in the import report. The contradiction has been there since the baseline commit (a8ec0a9). | Contract and code: `handoff.md:49–51` ("Nothing in comments blocks anything"); `build.py:617` ("never printed, never blocking"). Contrary docs: srom-typeset `SKILL.md:81` and `srom-md.md:29` ("fails the build"); `tlumacz-PLAN.md:40` ("blocking comment, so srom-typeset's build fails") and `:43`. Measured: Ndiaye with S1–S7 open → `RESULT: PASS — ready for InDesign`. | will bite | srom-typeset (SKILL.md, srom-md.md); srom-tlumacz (PLAN). MB only if he wants a hard stop: that is a contract change, `handoff.md` first. |
| 3 | **srom-kanon SKILL.md contradicts § 3.4.** A session that loads only SKILL.md would set *Ciganos* in roman. | `srom-kanon/SKILL.md:43` "Proper names never italic, including Romani group names in any spelling". Kanon `kanon-redakcyjny.md:69`: foreign exonyms italic. RULES.md:27 is correct. | will bite | srom-typeset |
| 4 | **Open MB items outside MB-decisions.md**, which says "Needs MB now: nothing" (`MB-decisions.md:13`). | Kanon § 13.2 (`kanon-redakcyjny.md:512`): licence ND option, marked "DO ROZSTRZYGNIĘCIA – kolegium". `:516`: vol. 18 copyright-transfer clause, marked "PILNE – przed ogłoszeniem otwartego dostępu". Both also in RULES.md:202–203 and srom-kanon SKILL.md:59. Curator: `curator-update-2026-09-27/CHANGES.md:27–33` asks MB to confirm mu-plugin v2.3 before the desktop upload; D5 does not mention it. | will bite (at deposit / OA announcement / desktop upload) | srom-typeset (Kanon items → D-items, or MB rules them out of the list); srom-tlumacz (add v2.3 to D5) |
| 5 | **srom-tlumacz and `_handoffs/` have no version control.** Nothing can be checked against history: HANDOVER.md changed mid-review with no diff to read, the append-only rule can't be verified, and D10 has no trace anywhere. | `git -C srom-tlumacz rev-parse` → "not a git repository"; 97 files, 22 MB. `typeset-to-tlumacz.md:119` "Next free D-number: D10"; the next one used is D11. | will bite | srom-tlumacz (git init); MB for `_handoffs/` |
| 6 | **Next milestone: the "second text" route is only written down on the srom-tlumacz side.** srom-typeset's handover doesn't mention it. The procedure starts with srom-typeset stage 1 (freeze `<id>_src.md` + refs.json, then a T-item). A DOCX with typed notes can't be frozen until E9 is built. | tlumacz `HANDOVER.md:63` (§ 7a: "MB brings a second text … same procedure"); `HANDOVER-typeset.md:77–79` (E9 queued, not started). | will bite | MB (send the text to srom-typeset first) |
| 7 | **MB's decisions shown as open in srom-typeset.** | `references/decisions.md:50–56`: items 20 and 22 marked "○ … not yet confirmed". `HANDOVER-typeset.md:33` ("open: 20, 21, 22"), and `:169–170` lists D1, D2, D4, D7 and D9 as pending. But D1 and D2 were decided 27.09 (`MB-decisions-archive.md:25,31`), and D4, D7 and D9 are closed. | cosmetic | srom-typeset |
| 8 | **Contract change T11 reached `handoff.md` but not the other descriptions.** | srom-typeset `SKILL.md:59–64` (scenario C) hands over only `<id>_src.md` + refs.json. It doesn't mention `<id>_src_front.md` out or `<id>_front_pl.md` back, and the return path lacks `--refs <id>_refs_tlum.json` and `--pair-src`. `tlumacz-PLAN.md:36–45` has no output entry for `<id>_front_pl.md` and doesn't mention `tlumaczenie:`. The format of `<id>_front_pl.md` exists only in the `tlumacz-front_check.py` docstring (T13); `handoff.md` doesn't point to it. | cosmetic (will bite when the CSV step reads it) | srom-typeset (SKILL.md; one pointer in handoff.md); srom-tlumacz (PLAN) |
| 9 | **"ALL MET" is not a re-measurement.** gate-check only runs the CHECK of gates that are unticked or have pending evidence. When I re-ran the closed gates by hand, 4 no longer hold. All four are harmless drift, but check 4 in tlumacz's CLAUDE.md gives false assurance. | `gate-check.mjs:117–118`. The 4 gates: 1.1 G4 (expects precedent 4/4, now 11/11); 1.1 G9 (the superseded PROJEKT draft now lints with 1 ERROR); 1.3.1 G6 and 1.5.2a G5 (grep for D8/D11 in MB-decisions.md → 0, because both were removed as resolved). The other 30 checks hold. | cosmetic | srom-tlumacz |
| 10 | **E3, E5, E6: srom-typeset says done, srom-tlumacz never verified them.** | `tlumacz-to-typeset.md:59`, `tlumacz-PLAN.md:50` ("not tested here"). E3 and E5 are present in `handoff.md:26–27` and `:68–69`. E6 is covered in srom-typeset's `test_e2e`. On Ndiaye the source labels equal the printed numbers (133 author notes, t-notes unnumbered), so the pilot proves nothing either way. | cosmetic | srom-tlumacz |
| 11 | **Stale text in srom-typeset.** | `SKILL.md:23` says 10/10 (measured 14/14). `CLAUDE.md:4–8` lists srom-tlumacz as a skill in `.claude/skills/` (there are two skills; tlumacz is a folder, and its packaging is deferred). `CLAUDE.md:17` says test_pdf SKIPs (it now runs, 10/10). `HANDOVER-typeset.md`: `:5` wrong path; `:26–27` "G1–G16 met" vs `:39–40` "ledger is lost"; `:49` points to D7 (gone); `:56` "Q1–Q17 open" (answered); `:140–144` § 5 advice (done 26.09). Old versions: `lint_srom.py:3` (v1.6), `test_csl.py:2` (v1.5), `kanon_path.py:29`. `test_kanon.py:46` misses all three: it matches only lowercase "kanon v1.[0-5]" and scans srom-typeset only. Kanon § 17 row 1.6 (`:611`) carries the 27.09 § 3.4 exonym rule, although D14 says the 27–28.09 rulings have their own row. `GATES.md` has no gates for the 17 commits since f2c8bc0 (27.09 20:26), which include two contract changes (T11, D12); CLAUDE.md:28 asks for gates. `dist/srom-kanon.skill` is still v1.6 (and `srom-typeset/srom-kanon.skill` v1.5); git-ignored, so this only matters if uploaded to claude.ai. | cosmetic | srom-typeset |
| 12 | **Stale text in srom-tlumacz.** | `HANDOVER.md`: `:1` still dated 27.09; `:11` "4 HOUSE rows" (18); `:16` "E1–E9" (now E1–E16); `:32`, `:34` "draft § 12.2"; `:35` says the kartoteka "does not exist" (contradicts `:43`); `:48` Polish files "outside the folder" (they are in `vol18-PL-HOLD/`); `:59` "D4–D6" (now D5, D6 c); `:68` C-0012–C-0018 "UNCHECKED" (the TSV has ESTABLISHED / "MB verified 28.09.2026", per `tlumacz-decisions.md:13–14`). `tlumacz-PLAN.md`: `:49` IF-KANON (v1.5, "kartoteka location not yet known"); `:50` IF-TYPESET (14/14, "E9 open"); `:51` IF-CURATOR (C1 was done 27.09); `:76` Inputs still needed; `:78–82` Pending handoffs; status log lacks § 7a. `tlumacz-to-typeset.md:139`: Romka/Romki "outside note 1: 11". I measure 9 outside note 1; 11 includes the bracketed gloss in note 1 (`ndiaye_pl.md:15`). | cosmetic | srom-tlumacz |
| 13 | **`_handoffs/` housekeeping.** | `MB-decisions-archive.md:3` "New closed items are appended here" contradicts `MB-decisions.md:11` "it is not appended to". `README.md:18` gives the contract path as `srom-typeset/references/handoff.md` (it is `srom-typeset/.claude/skills/srom-typeset/references/handoff.md`; root CLAUDE.md has it right). | cosmetic | srom-typeset (it wrote the archive); README: whichever session MB asks |
| 14 | **The two modules run the typeset scripts under different Pythons.** srom-tlumacz uses `python3` (miniconda 3.13); srom-typeset uses the venv. Both work today. If conda is not first on PATH, `python3` is /usr/bin 3.9 with no python-docx, and the tlumacz checks fail. | `tlumacz-test_handoff.py:28` (`sys.executable`); `which -a python3` → /opt/miniconda3, /usr/bin; srom-typeset `CLAUDE.md:15–16`. | cosmetic | srom-tlumacz |

Not findings: E8's InDesign side (`_gwiazdki.jsx`) is untested, and D3/G12 wait. Both are deferred by MB and both sides say so.

## Message for srom-typeset (paste)

```
Cross-module review 28.09.2026: _handoffs/review-28.09.2026.md. Your suite: SUITE ALL PASS 14/14, tree clean. In order:
1. E16 blocks the Ndiaye hand-back. docx_in.py splits a two-paragraph ::: przypis-tytulowy into two blocks, and
   check.py --pair then fails ("2 title-note blocks"). Reproduced on srom-tlumacz/work/ndiaye/ndiaye_robocza_v2.docx,
   the file MB is editing. Fix it, add the case to your suite, answer with a T-item (their test then flips from
   KNOWN GAP).
2. Open comments. handoff.md:49–51 and build.py:617 say comments never block; your SKILL.md:81 and srom-md.md:29 say
   PRZYWRÓCIĆ / DO SPRAWDZENIA fail the build. Align SKILL.md and srom-md.md with the contract. Ndiaye with S1–S7 open
   builds "PASS — ready for InDesign". If MB wants a hard stop, that is a contract change: handoff.md first.
3. srom-kanon SKILL.md:43 ("Proper names never italic, including Romani group names in any spelling") contradicts
   Kanon § 3.4. Add the foreign-exonym exception.
4. Kanon § 13.2 has two open items (licence ND option — kolegium; PILNE: vol. 18 copyright-transfer clause) that are
   not in MB-decisions.md. Add them under Open (next free: D15), or ask MB whether they belong there.
5. Your files still show MB's decisions as open: references/decisions.md:50–56 (20 and 22 = D1 and D2, decided
   27.09); HANDOVER-typeset.md:33 and § 7 (:169–170).
6. T11 outside handoff.md: SKILL.md scenario C (:59–64) should hand over <id>_src_front.md and take back
   <id>_front_pl.md, <id>_refs_tlum.json and --pair-src. In handoff.md, one line: the format of <id>_front_pl.md is
   srom-tlumacz/tlumacz-front_check.py's docstring.
7. Stale text:
   - SKILL.md:23 (10/10 → 14/14).
   - CLAUDE.md:4–8 (srom-tlumacz is not a skill in .claude/skills) and :17 (test_pdf now runs).
   - HANDOVER-typeset.md :5 (path), :26–27 vs :39–40 (G1–G16), :49 (D7 gone), :56 (Q1–Q17 answered), § 5 :140–144
     (done 26.09).
   - Old versions in lint_srom.py:3 (v1.6), test_csl.py:2 (v1.5), kanon_path.py:29. Widen test_kanon.py:46 so it
     catches them: any version other than the current one, any case, srom-kanon included.
   - Kanon § 17: the 27.09 § 3.4 exonym rule sits in row 1.6, while D14 says the 27–28.09 rulings have their own
     1.7 row. Your call whether to move it.
   - _handoffs/MB-decisions-archive.md:3 says new items are appended; MB-decisions.md:11 says it is not appended
     to. Fix the archive's header line.
8. GATES.md has no gates for the 17 commits since f2c8bc0 (incl. contract changes T11 and D12). Start a batch for
   E16 + E9.
9. dist/srom-kanon.skill is v1.6: rebuild before any claude.ai upload.
```

## Message for srom-tlumacz (paste)

```
Cross-module review 28.09.2026: _handoffs/review-28.09.2026.md.
Measured:
- check_tb OK (18 rows), selftest 7/7, HANDOFF CONTRACT 25/25 + KNOWN GAP E16 (reproduced on ndiaye_robocza_v2.docx)
- Ndiaye: pair CHECK OK, build PASS (0 errors), FRONT OK; src copies identical to srom-typeset's
In order:
1. Put srom-tlumacz under git (git init + first commit; decide on sources/prng/*.jsonl and vol18-PL-HOLD/ in
   .gitignore). Today there is no history: HANDOVER.md changed during the review and there was no diff to read.
2. The build does not stop on open comments: handoff.md:49–51, build.py:617 "never blocking". Ndiaye with S1–S7
   open → "PASS — ready for InDesign". After the Word round trip the comments leave the text and are listed only in
   the import report. tlumacz-PLAN.md:40 and :43 say the opposite: correct them. Keep S1–S7 tracked in
   ndiaye_uwagi.md until MB closes each one; the build won't catch them.
3. PLAN § Contract is stale:
   - IF-KANON :49 (v1.5; kartoteka location "not yet known")
   - IF-TYPESET :50 (14/14; "E9 open")
   - IF-CURATOR :51 (C1 done 27.09)
   - :76 Inputs still needed; :78–82 Pending handoffs
   Add <id>_front_pl.md (T11) and the `tlumaczenie:` front matter (T7) to the per-article outputs. Log § 7a (chat
   closed, 1.4.1 deferred) in the status log.
4. HANDOVER.md is stale:
   - :1 date; :11 (4 → 18 rows); :16 (E1–E9 → E1–E16); :32 and :34 "draft § 12.2"
   - :35 says the kartoteka doesn't exist (contradicts :43)
   - :48 (the Polish files are in vol18-PL-HOLD/); :59 (D4 is closed; yours are D5, D6 c)
   - :68 C-0012–C-0018 are ESTABLISHED / MB verified (tlumacz-decisions.md:13–14), not UNCHECKED
5. Check 4 in CLAUDE.md (gate-check --run) re-measures nothing: gate-check.mjs:118 runs CHECK only for unticked
   gates. Re-run by hand, 4 closed gates no longer hold:
   - 1.1 G4 (precedent 4/4 vs 11/11)
   - 1.1 G9 (lint of the superseded PROJEKT draft)
   - 1.3.1 G6 and 1.5.2a G5 (grep D8/D11 in MB-decisions.md, now removed)
   Drop check 4 or replace it. In new gates, don't CHECK files that are meant to change.
6. E3, E5, E6 are still "not tested here" (tlumacz-to-typeset.md:59). E3 and E5 are in handoff.md (:26–27, :68–69).
   E6 needs a test case where source labels ≠ printed numbers (Ndiaye is identity). Then write a status line.
7. MB-decisions.md D5: add the open question from _handoffs/curator-update-2026-09-27/CHANGES.md:27–33 (confirm
   mu-plugin v2.3 before the desktop upload).
8. Run the checks that call srom-typeset scripts with ~/.venvs/srom/bin/python. Today `python3` is miniconda 3.13;
   /usr/bin/python3 (3.9) has no python-docx.
9. T15 correction (tlumacz-to-typeset.md:139): Romka/Romki outside note 1 are 9. The 11 includes the bracketed
   gloss in note 1 (ndiaye_pl.md:15).
```

## For MB

- The second text for translation: send it to srom-typeset first (stage 1), as with Ndiaye. If it is a DOCX with typed
  notes, it can't be frozen until E9 is built.
- Version control: srom-tlumacz (its session can do it) and `_handoffs/` (your call where it lives).
- Open comments don't block the build today (row 2). Keep it that way unless you want a hard stop.
- Kanon § 13.2 (licence ND; the PILNE copyright clause) is open but in no decision list (row 4).
