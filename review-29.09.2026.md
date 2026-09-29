# Cross-module review — [general] 29.09.2026 (17:17–17:33)

Reviewer only: nothing in `srom-typeset/` or `srom-tlumacz/` was changed. All builds, round trips, mutation tests and
gate re-runs were run on copies in a scratch folder. After the review all three repos have clean working trees
(srom-typeset HEAD 0c75f49, srom-tlumacz 1f0a96f, `_handoffs` 94618a5). This covers everything since
`review-28.09.2026.md`: srom-typeset 37 commits after b776e0e (to 0c75f49), srom-tlumacz 18 after 604acc3 (to 1f0a96f), `_handoffs` 27 after
the snapshot 622fac6.

## Conclusions

1. **Tests are green on both sides, and the four drafts re-measure clean against today's toolchain.** SUITE ALL PASS
   19/19. HANDOFF CONTRACT 30/30, run against HEAD 0c75f49 (six commits newer than the last run srom-tlumacz recorded).
   Ndiaye, Ostendorf, Pahulich, Tittel: pair CHECK OK, `build --draft` PASS, FRONT OK, and each Word copy imports to
   CHECK OK. The sources srom-tlumacz translated from are byte-identical to srom-typeset's current frozen files.
   All five keyed sources catch 40/40 mutations.
2. **Nothing blocks MB's Word edits.** The next milestone is the first delivery back and the first InDesign placement.
   Four things will bite there:
   - **srom-typeset has not answered four incoming items**: E17, E18 [Pahulich], E18 [Ostendorf] and E19. Two sessions
     read the incoming file afterwards and wrote T23/T24 without a status line for them. They ask for kartoteka rows,
     a Kanon line, and corrections to srom-typeset's own `refs.json`. Kanon § 12.2.6 wants group names settled before
     delivery.
   - **Two srom-tlumacz gates overwrite MB's Word files if anyone re-runs them.** 1.5.4b G8 and 1.5.5b G8
     re-export `pahulich_robocza.docx` and `tittel_robocza.docx` in place.
   - **The "back" half of the contract doesn't match practice, and no delivery message is defined.** `handoff.md` says
     srom-typeset turns `<id>_pl.md` into the working copy. In practice srom-tlumacz makes it, MB edits it in
     srom-tlumacz's folder, and both modules plan to run the import → pair check → build.
   - **Parallel sessions reuse IDs.** Three collisions in 24 hours: T20 twice, D21/D22, E18 twice.
3. **Kanon: one normative text, v1.7 everywhere current.** All 1,194 § citations in 287 files resolve. The only misses
   are Grellmann OCR and one archive reference, neither a Kanon citation. srom-kanon SKILL.md quick rule 9 lacks the
   29.09 display-element clause.
4. **MB-decisions.md holds only pending items**, and no module is acting on an undecided item as if it were settled:
   every assumption is declared. Leftovers are stale text only: D21 is still called open in srom-typeset's files;
   D18 A5 was decided on 28.09 but is not yet applied.
5. **Hygiene is clean.** Each module wrote only its own outgoing file, MB-decisions, and one README edit each. The curator skill is
   unchanged since MB's authorised update (27.09 03:47). `~/.claude/skills/srom-kanon` and `srom-typeset` are symlinks
   into the repo. One rule is broken: srom-tlumacz's Tittel session wrote times it could not have read from the clock.
6. **Last review's 14 findings are all addressed.** What remains is new stale text on both sides (rows 9–10).

## Verdict lines as printed

srom-typeset, `python3 .claude/skills/srom-typeset/tests/run_all.py` (exit 0):
```
ok   test_check.py: CHECK ALL PASS 79/79
ok   test_citemap.py: CITEMAP ALL PASS 44/44
ok   test_csl.py: NOTES ALL PASS 30/30 | BIB ALL PASS 15/15 | POSITION ALL PASS 10/10
ok   test_docx_in.py: DOCXIN ALL PASS 23/23
ok   test_e10.py: E10 ALL PASS 9/9
ok   test_e2e.py: E2E ALL PASS 77/77
ok   test_e8.py: E8 ALL PASS 18/18
ok   test_jsx.py: JSX-DONE | STYLES ALL PASS 23/23
ok   test_kanon.py: KANON ALL PASS 20/20
ok   test_lint.py: LINT 0 ERROR
ok   test_lookup.py: LOOKUP ALL PASS 10/10
ok   test_normalize.py: NORMALIZE ALL PASS 42/42
ok   test_pdf.py: PDF ALL PASS 10/10
ok   test_pdf_crs.py: PDF-CRS ALL PASS 17/17
ok   test_pdf_cup.py: PDF-CUP ALL PASS 24/24
ok   test_pdf_de.py: PDF-DE ALL PASS 20/20
ok   test_pdf_layout.py: PDF-LAYOUT ALL PASS 25/25
ok   test_pdf_onculture.py: PDF-ONCULTURE ALL PASS 11/11
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
SUITE ALL PASS 19/19
```
srom-tlumacz, the checks in its CLAUDE.md (venv, all exit 0):
```
columns: 17/17 defined; schema fields: 17/17 present
shape: 39 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 11/11
precedent quotes in rows not yet HOUSE: 9/9
established rows: 14, all with >=2 sources
training quotes verified: 25/25
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 30/30          (E1, E2, E4, E16: GAP CLOSED)
```
`tlumacz-draft_check.py --all`: leftover 0 in all four; marks 7=7, 2=2, 10=10, 12=12; quotes Ostendorf 43/43 (7 open rows
unmatched), Tittel 34/34; selftest 6/6.

Re-measured by me on copies (srom-typeset 0c75f49):

| text | `check.py --pair` | `build.py --pair-src --queries --draft` | build without `--draft` | FRONT | Word round trip / import of the Word copy in the folder |
|---|---|---|---|---|---|
| Ndiaye | CHECK OK | PASS | PASS | OK | CHECK OK / v1, v2 CHECK OK |
| Ostendorf | CHECK OK | PASS | FAIL: `[BRAK …]` in 11 notes (D19 A2) | OK | CHECK OK / CHECK OK |
| Pahulich | CHECK OK | PASS | FAIL: `[BRAK MIEJSCA]` nn. 47, 145 (D17 B10) | OK | CHECK OK / CHECK OK |
| Tittel | CHECK OK | PASS | FAIL: `[BRAK WYDAWCY]` n. 20 (D20 A3) | OK | CHECK OK / CHECK OK |

The non-draft failures are exactly the known imprint gaps (MB's and the authors'); nothing else.
Mutation tests (`mutate_keyed.py` + `check.py --keyed`): Tittel, Ostendorf, Scheffknecht, West Ohueri
`MUTATIONS CAUGHT 40/40 | CHECK OK`; Ndiaye 40/40. The handed-over sources pass the stricter checks of 29.09 with
unchanged sha256, so nothing needs re-freezing.
srom-tlumacz gates closed since the last review (11 files, 59 CHECKs, re-run on a copy): 54 hold. The 5 that drift test
things meant to change (row 13).

## Findings

| # | Finding | Evidence | Severity | Fixes |
|---|---|---|---|---|
| 1 | **Four incoming items without a status line from srom-typeset.** Each asks for something in srom-typeset's files:<br>– **E17 [Ostendorf]:** kartoteka rows (*Anglo-Romani* → „angielscy Romowie”; *Bohémienne(s)* as a variant of *Bohémiens*; *cingani*, *Zingaros*…); a Kanon line for „tłum. z przekładu angielskiego” (§ 12.2.4 c).<br>– **E18 [Pahulich]:** 5 title glosses in `refs.json`; *Manoush* as a variant of the Manush row.<br>– **E18 [Ostendorf]:** `urlsperger1751` describes the wrong part and year (18th Continuation, 1752, pp. 979–980).<br>– **E19 [Tittel]:** n. 49 MEW p. 743 → 741, for D20 B.<br>Kanon § 12.2.6 wants group names settled before delivery. The `refs.json` fixes mean new sha256 values and T-items, and possibly a key change in `ostendorf_pl.md`: cheapest before MB edits the Word copy. | `tlumacz-to-typeset.md:161–171, 183–189, 191–194, 201–206`. The last T-item is T24 (`typeset-to-tlumacz.md:428`); T23 (04:13) and T24 (04:42) came after E17/E18 (03:41–03:55). Nothing applied: `kartoteka.tsv` (37 rows) has no Anglo-Romani, Bohémienne or Manoush. Ostendorf `refs.json` is still 0704415d (T21); Pahulich's is still 6eefd2b4 (T18). HANDOVER-typeset doesn't mention E17–E19. Root `CLAUDE.md`: "Don't leave incoming items without one." | will bite | srom-typeset (the Kanon line after MB: D26 e) |
| 2 | **Two gates overwrite MB's Word copies if re-run.** Their CHECK runs `export_work.py <id>_pl.md -o <id>_robocza.docx` in the article folder. That is the file MB edits and the master once he has. A reviewer, or anyone measuring rather than trusting, would silently replace his edits with the draft. The file is git-tracked, but only a commit made after MB's edit would save it. (`gate-check --run` skips ticked gates, so it would not trigger this.) | `tlumacz-gates-1.5.4b.md:35`, `tlumacz-gates-1.5.5b.md:35`. 1.5.3b does it safely (`T=$(mktemp -d)`). I ran both only on a copy. | will bite (data loss) | srom-tlumacz |
| 3 | **Contract "back" path vs practice; no delivery message.**<br>– `handoff.md` says srom-typeset turns `<id>_pl.md` into the working copy. In practice srom-tlumacz exports `<id>_robocza.docx` into its own `work/<id>/`, and MB edits it there.<br>– srom-tlumacz's HANDOVER plans to run `docx_in` → `check --pair` → `build` after MB's edit. srom-typeset's SKILL.md scenario C runs the same steps itself.<br>– "Out" has a T-item with sha256 values. "Back" has nothing: no item naming the final `<id>_pl.md`, `<id>_refs_tlum.json`, `<id>_front_pl.md` and `<id>_pytania_tlum.csv` with their sha256, and no rule on which copy srom-typeset builds from. The first delivery is the next milestone. | `handoff.md:62–73`; srom-typeset `SKILL.md:62–66`; `HANDOVER.md:73, 75, 78` (srom-tlumacz: "After MB returns the Word file: docx_in.py → check.py --pair → build.py"). The E-items so far say "Nothing needed from you for the draft". | will bite | srom-typeset (`handoff.md` first, then SKILL.md, then a test on both sides); srom-tlumacz (PLAN, HANDOVER) |
| 4 | **ID collisions between parallel sessions of one module.**<br>– T20 used twice (fixed by T21).<br>– srom-typeset's D21 and srom-tlumacz's D21 two minutes apart (renumbered to D22).<br>– E18 used twice, still standing; E19 notes it.<br>Also: srom-typeset sessions commit each other's shared files. GATES R1 entered in another session's commit; D21's removal went in with a West Ohueri commit.<br>More texts in parallel will repeat this. Every citation of "E18" or "T20" is ambiguous without the [Author] tag. | `typeset-to-tlumacz.md:328, 363, 390`; `_handoffs` commits 4e5d41f (03:39), 968f4a8 (03:41), a7f16a3; `tlumacz-to-typeset.md:183, 191, 203`; `GATES.md` R1 evidence; de8db18. srom-typeset's CLAUDE.md:31–34 has parallel-session rules; srom-tlumacz's has none. | will bite | MB (a rule in root `CLAUDE.md` / `README.md`: re-read the tail and take the next ID immediately before appending, commit at once); srom-typeset cites them as "E18 [Pahulich]" / "E18 [Ostendorf]" |
| 5 | **Pending decisions that change the frozen source, while MB edits the Word copies.**<br>– D17 A2: merge Pahulich notes 1/2, which renumbers from 2 on.<br>– D20 A1: Tittel title note; labels would revert to 1–101.<br>– Urlsperger key (row 1).<br>– D26 (a): Pahulich and Tittel would change "when you edit them".<br>Decided after the Word edit, each one has to be made by hand in the Word master. | `MB-decisions.md:40–41, 155–156, 238–241`; T18 and T20 "May still change" (`typeset-to-tlumacz.md:294–297, 359–361`). | will bite | MB (decide these before editing the Pahulich and Tittel Word copies) |
| 6 | **Stage 3: the translation-specific InDesign scripts have never run in InDesign.** `_postimport.jsx`, `_ibidem.jsx` and `_gwiazdki.jsx` are generated and tested only as ES3 text. `indesign_check` covers the style setup, the final pass and the template. Every vol. 19 translation carries asterisk notes (title note at least). | `tools/indesign_check/` (no call to them); `HANDOVER-typeset.md:180–182` (G12 next). | will bite (at G12) | srom-typeset: make G12 a translated article (Ndiaye after MB's edit) |
| 7 | **Guessed times** (root `CLAUDE.md`: "taken from `date`, never guessed"). The Tittel session stamped entries 8–9 minutes after the commits that contain them. | `_handoffs` commit 652a296 at 04:32:55 contains D25 "04:40" (`MB-decisions.md:177`) and E19/T20-status "04:41" (`tlumacz-to-typeset.md:196, 198, 201`). srom-tlumacz commit f3d7bec at 04:33 contains the PLAN log "04:42" (`tlumacz-PLAN.md:126`) and `HANDOVER.md:78` "04:42". srom-typeset's times match its commits. | cosmetic | srom-tlumacz (correction lines; no rewrite) |
| 8 | **MB's decisions shown as open, or decided but not applied.**<br>– D21 was closed 29.09 (Kanon § 3.4 supplement), but srom-typeset still calls it open in three places.<br>– D18 A5 (Hippel "von" as a dropping particle) was decided 28.09 but not applied, and srom-typeset's HANDOVER doesn't carry it as a to-do.<br>– The Ostendorf corrections are T21, but three places still cite T20. | D21: `HANDOVER-typeset.md:33` ("one point left as D21") and `:317` (listed open) vs `:221` (closed); `references/decisions.md` row 21 "MB-decisions D21". D18 A5: `MB-decisions.md:87–89`; `work/scheffknecht/refs.py:69` still `non-dropping-particle`. T21: `MB-decisions.md:98, 124` ("(T19, T20)", "(T20)"); `HANDOVER-typeset.md:123`. | cosmetic (D18 A5 will bite at Scheffknecht stage 3) | srom-typeset |
| 9 | **Stale text, srom-typeset.** | `HANDOVER-typeset.md:1` "state at 28.09.2026" (has 29.09 content). `:172–173` § 3 item 5 "Next text for translation… A DOCX with typed notes needs E9 first": five texts are handed over, and E9 is done (`:174`). No queue item for E17–E19 or for taking translations back. `MB-decisions.md:18–28` "Needs MB now" omits D16 (PILNE, OA announcement) and D15. srom-kanon `SKILL.md:43` (quick rule 9) lacks the 29.09 clause "text, not display elements" (Kanon `:68`, RULES `:27` have it). `dist/srom-typeset.skill` says 14/14; `dist/srom-kanon.skill` (28.09 03:35) lacks the three v1.7 supplements (git-ignored; matters only for a claude.ai upload). | cosmetic | srom-typeset (the "Needs MB now" line: whichever session next edits MB-decisions) |
| 10 | **Stale text, srom-tlumacz.** | `HANDOVER.md`: `:1` "updated 28.09.2026"; `:5` closed leaves lack 1.3.2, 1.3.5c, 1.4.2a, 1.5.3–1.5.5; `:21` "E1–E16" (E1–E19); `:44` § 4 dated 28.09; `:50` "E9/T2 … queued at srom-typeset" (done, T17); `:76` "18 rows, all HOUSE" vs `:11` and check_tb (39 rows: 18 HOUSE, 9 PROVISIONAL, 12 CANDIDATE); `:80` hands the Ostendorf quotes-sheet fix to "the Ostendorf session", which is closed, so nobody owns it (`draft_check`: "7 open rows unmatched"). `tlumacz-PLAN.md`: `:55` IF-TYPESET "E9 … queued, not started", E17–E19 missing; `:88` "can't be frozen until E9 is built"; `:93` "E9 queued"; `:94` srom-kanon "nothing pending" (E17/E18 kartoteka rows and the § 12.2.4 c line are pending); `:12` and `:49` "merges into the termbase only after MB's sign-off" / OUT-TBROWS, while 21 PROVISIONAL + CANDIDATE rows sit in the TSV (a practice the schema allows; the PLAN wording is old); `:45` OUT-REVIEW `<id>_review.docx` has never been produced (the notes sheet took its place). T24 has no status line ("received, not started" is enough). | cosmetic | srom-tlumacz |
| 11 | **"v1.7" now names four texts.** The header still says Wersja 1.7, while § 17 row 1.7 holds three dated supplements (28.09 ×2, 29.09) that change rules. srom-tlumacz's "Kanon v1.7 (28.09.2026, D14)" points to the first of them. | `kanon-redakcyjny.md:3`, `:631`; `tlumacz-PLAN.md:54`. | cosmetic | MB (bump to 1.8 at the next change, or accept "v1.7 + dated supplements") |
| 12 | **srom-typeset gates CHECK files meant to change.** S6 expects `^### D21` count 1 in MB-decisions; R1 expects 0. Both can never pass together. W7 greps MB-decisions too. srom-tlumacz's CLAUDE.md:25 has a rule against this; srom-typeset's doesn't. | `GATES.md` S6, R1, W7. | cosmetic | srom-typeset |
| 13 | **srom-tlumacz gate drift (5 of 59 on a copy).** 1.3.2 G8, 1.3.5b G8 and 1.4.2a G5 check `git log -1` (always the newest commit). 1.3.5 G1: training manifest 2 → 10 files. 1.5.3a G4: dated T-status count 5 → 7. The rest hold, including every pair, build, front and round-trip gate. | re-run output above | cosmetic | srom-tlumacz (for new gates only: CHECK the commit by message, not `-1`) |

Not findings:
- E5 (`tb_check.py`) is still a documented slot. Both sides say so.
- The Dom file is not frozen (MB's call; a page is missing).
- West Ohueri has not been taken (D24 A1, permission).
- Ostendorf, Pahulich and Tittel carry `[BRAK …]` (MB's and the authors' items).
- srom-tlumacz drafts with declared assumptions (translator credit, she/her, PROVISIONAL terms) because MB asked for "decisions later".

## Message for srom-typeset (paste)

```
Cross-module review 29.09.2026: _handoffs/review-29.09.2026.md. Your suite: SUITE ALL PASS 19/19, tree clean; mutation
tests re-run by the reviewer: all five keyed sources 40/40. In order:
1. Four incoming items have no status line (root CLAUDE.md): E17 [Ostendorf], E18 [Pahulich], E18 [Ostendorf], E19 [Tittel]
   (tlumacz-to-typeset.md:161–206; E18 is used twice, so cite it with its [Author] tag). Answer each with a T-item:
   - kartoteka: Anglo-Romani → „angielscy Romowie”; Bohémienne(s) as a variant of Bohémiens; Manoush in en_variants of
     the Manush row; the foreign exonyms in E17 (1) (cingani, Zingaros/Zingari, Zingances, Chinganéros, Bohèmes)
   - Kanon § 12.2.4 c line for „tłum. z przekładu angielskiego”: after MB's D26 (e)
   - Pahulich refs.json: 5 title glosses (rows in pahulich_pytania_tlum.csv)
   - Ostendorf refs.json: urlsperger1751 → 18th Continuation, 1752, pp. 979–980 (your call). If the key changes, say so;
     srom-tlumacz changes ostendorf_pl.md.
   - Tittel n. 49 (MEW p. 743 → 741) into D20 B if you want it
   New refs.json → new sha256 in the T-item. Do it before MB edits those Word copies.
2. The "back" half of handoff.md doesn't match practice. srom-tlumacz makes <id>_robocza.docx in its own work/<id>/;
   MB edits it there; both of you plan the docx_in → check --pair → build step. Contract change, handoff.md first:
   - who imports MB's Word file, and where the master lives
   - a delivery item (E-item with sha256 of <id>_pl.md, <id>_refs_tlum.json, <id>_front_pl.md, <id>_pytania_tlum.csv),
     mirroring your T-items
   - where you build from
   Then SKILL.md scenario C, and a test on both sides.
3. G12 (first InDesign placement): _postimport.jsx, _ibidem.jsx and _gwiazdki.jsx have never run in InDesign. Make G12 a
   translated article (Ndiaye after MB's edit), so the asterisk series is proven.
4. D21 is closed (Kanon § 3.4, 29.09), but HANDOVER-typeset.md:33 and :317 and decisions.md row 21 still call it open.
   D18 A5 (hippel1995 → dropping-particle) is decided but not applied: work/scheffknecht/refs.py:69. Add it to 4b.
   MB-decisions.md:98 and :124 and HANDOVER-typeset.md:123 cite T20 for the Ostendorf corrections: it is T21.
5. Stale text:
   - HANDOVER-typeset.md:1 (date); :172–173 (item 5 "next text… needs E9 first": five texts are out, E9 done); add a
     queue item for E17–E19 and for taking translations back
   - srom-kanon SKILL.md:43 (quick rule 9): add "the text, not display elements" (Kanon § 3.4, 29.09)
   - MB-decisions "Needs MB now" (:18–28) omits D16 (PILNE) and D15
   - dist/*.skill are stale: rebuild before any claude.ai upload
6. GATES.md S6 (D21 count 1) and R1 (D21 count 0) can't both hold, and W7 greps MB-decisions too. Don't CHECK files
   meant to change (srom-tlumacz's CLAUDE.md:25 has this rule; consider adopting it).
7. Parallel sessions: two of yours committed each other's GATES/MB-decisions changes (R1 in 42a2397; D21's removal in
   de8db18). Harmless this time. MB may add an ID rule to root CLAUDE.md (review row 4).
```

## Message for srom-tlumacz (paste)

```
Cross-module review 29.09.2026: _handoffs/review-29.09.2026.md. Measured: check_tb OK (39 rows), selftest 9/9, HANDOFF
CONTRACT 30/30 against srom-typeset HEAD 0c75f49; all four drafts pair CHECK OK, build --draft PASS, FRONT OK, Word copies
import to CHECK OK; your src copies are byte-identical to srom-typeset's. In order:
1. Data-loss hazard: tlumacz-gates-1.5.4b.md:35 and tlumacz-gates-1.5.5b.md:35 (G8) run
   export_work.py … -o pahulich_robocza.docx / tittel_robocza.docx in place. Re-running them after MB starts editing
   replaces his Word file with the draft. Rewrite both CHECKs to export into a temp dir, as 1.5.3b does
   (T=$(mktemp -d)). Annotate the change; the gate stays closed.
2. The hand-back step is undefined in the contract (review row 3). Your HANDOVER says you run docx_in → check --pair →
   build after MB's edit; srom-typeset's SKILL.md says it does. Wait for srom-typeset's handoff.md change; then align PLAN
   (OUT-*, IF-TYPESET) and HANDOVER, and add the delivery case to tlumacz-test_handoff.py.
3. Times: the Tittel session stamped D25 04:40, E19/T20-status 04:41 and the PLAN log/HANDOVER 04:42, all inside commits
   made at 04:32–04:33. Add correction lines (no rewrite), and take every time from `date`.
4. Parallel sessions: E18 is used twice (03:54 [Pahulich], 03:55 [Ostendorf]), and D21 collided. Before appending,
   re-read the tail of the file for the next free ID, and commit at once. Your CLAUDE.md has no parallel-session rule.
5. Stale:
   - HANDOVER.md: :1 (date); :5 (closed leaves: add 1.3.2, 1.3.5c, 1.4.2a, 1.5.3–1.5.5); :21 (E1–E19); :44/:50 (E9 is
     done, T17); :76 (39 rows: 18 HOUSE, 9 PROVISIONAL, 12 CANDIDATE, as :11 says)
   - HANDOVER.md:80: the Ostendorf quotes sheet (7 bare "open" rows) has no owner now; fix it or name who does
   - PLAN: :55 (E9 queued; E17–E19 missing); :88; :93 (E9 queued → E17–E19 awaiting srom-typeset); :94 (srom-kanon: the
     E17/E18 kartoteka rows and the § 12.2.4 c line are pending); :12/:49 (termbase merges "only after sign-off" vs
     PROVISIONAL/CANDIDATE rows in the TSV); :45 OUT-REVIEW never produced (the notes sheet replaced it)
   - T24 [West Ohueri]: write "received, not started" (root CLAUDE.md: every incoming item gets a status line)
6. Gate drift on a copy: 54/59 hold. 1.3.2 G8, 1.3.5b G8 and 1.4.2a G5 check `git log -1`; 1.3.5 G1 the training
   manifest; 1.5.3a G4 a status-line count. For new gates, CHECK the leaf's own commit by message
   (git log --format=%s | grep -c …), not the newest.
```

## For MB

- **Before you edit the Pahulich and Tittel Word copies**, decide what changes their frozen source or text: D17 A2
  (merge notes 1/2 → renumbering), D20 A1 (Tittel title note), D26 (a) (koczowniczy/wędrowny, which the drafts will
  otherwise leave to your Word edit). Also let srom-typeset answer E18 [Ostendorf] (Urlsperger key) first. Otherwise each
  of these has to be made by hand in the Word master.
- **Don't let anyone re-run gates 1.5.4b G8 and 1.5.5b G8** until srom-tlumacz has rewritten them: they overwrite your
  Word files (row 2). Commit (or copy) each Word file after an editing session.
- **Parallel sessions:** three ID collisions in a day. One line in root `CLAUDE.md` would stop it: "take the next ID
  from the file's tail immediately before appending; commit at once" (row 4).
- The first delivery back and the first InDesign placement have no defined handshake yet (rows 3, 6). srom-typeset
  owns the contract change.
- Kanon "v1.7" now carries three dated supplements (row 11): bump to 1.8 at the next change, or keep it as it is. Your call.
- D16 (vol. 18 copyright clause, PILNE before any OA announcement) is not in "Needs MB now".
