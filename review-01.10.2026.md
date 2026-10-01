# Cross-module review — [general] 01.10.2026 (16:15–16:28)

Reviewer only: nothing in `srom-produkcja/` or `srom-tlumacz/` was changed. Builds, round trips, mutation tests and gate
re-runs ran on copies in a scratch folder. All three repos had clean working trees at the start and the end
(srom-produkcja 1a560da, srom-tlumacz 4d824eb, `_handoffs` 26ecda3 before this file). Covers everything since
`review-29.09.2026.md`: srom-produkcja 13 commits after 0c75f49, srom-tlumacz 5 after 1f0a96f, `_handoffs` 15 after
14e1c94, including MB's hooks of 01.10.2026 (`_handoffs/tools/hooks/`).

## Conclusions

1. **Tests are green, and the four drafts still measure clean.** SUITE ALL PASS 22/22; HANDOFF CONTRACT 33/33 against
   srom-produkcja 1a560da. Ndiaye, Ostendorf, Pahulich, Tittel: pair CHECK OK, `build --draft` PASS, FRONT OK, and each
   Word copy imports to CHECK OK. The sources srom-tlumacz translates from are byte-identical to srom-produkcja's
   (Pahulich `refs.json` 3b060a87, as T25). All five keyed sources: MUTATIONS CAUGHT 40/40.
2. **The hooks work as described, with one exception.** I fed the guard ten edits: it refused the other module's
   folder through `srom-typeset/`, `~/.claude/skills/srom-kanon` and `srom-quant`, and let the module's own folder,
   `_handoffs/` and broken input through. The exception: if the hook *script* cannot be found (the SROM folder moved or
   renamed, the script renamed), Python exits with code 2, which Claude Code reads as "refuse". Every edit in a module
   session would then be blocked, the opposite of "a broken guard never stops work". It's a one-line fix per module.
3. **srom-tlumacz has not had a session since 29.09 18:43.** T27, T28 and T29 have no status line. T28 asks for the 2026
   spelling in the drafts, and the drafts still carry exactly the warnings T28 counted (Ndiaye 9, Tittel 6, Pahulich 1).
   No Word copy has been edited yet (all match their commits), so this is still cheap to fix.
4. **The first delivery of Ndiaye will fail on a file name.** `take_back.py` accepts only `<id>_robocza.docx`.
   Ndiaye's Word copy for MB is `ndiaye_robocza_v2.docx`, and `handoff.md` itself allows `_v2` names.
5. **Last review's 13 findings: 11 fixed, 2 still open** (MB's source-changing decisions before the Word edits; the
   translation scripts never run in InDesign). New stale text has built up on both sides: the Kanon is v1.10, the suite
   22/22, the ledger uses PAH-/TIT-/GEN- codes. Some docs still say v1.7, 19/19 and D17–D26.
6. **Two rule texts in the root create noise.** The "Status of review" start-of-session check will flag the 28.09 and
   29.09 reviews forever: no module wrote that heading for them, because it was introduced later. The checkup skill
   still checks the ledger's "Needs MB now" section, which no longer exists ("At a glance" replaced it).

## Verdict lines as printed

srom-produkcja, `python3 .claude/skills/srom-produkcja/tests/run_all.py` (python3 = miniconda 3.13; exit 0):
```
ok   test_check.py: CHECK ALL PASS 80/80
ok   test_citemap.py: CITEMAP ALL PASS 44/44
ok   test_csl.py: NOTES ALL PASS 30/30 | BIB ALL PASS 15/15 | POSITION ALL PASS 10/10
ok   test_docx_in.py: DOCXIN ALL PASS 23/23
ok   test_e10.py: E10 ALL PASS 9/9
ok   test_e2e.py: E2E ALL PASS 78/78
ok   test_e8.py: E8 ALL PASS 18/18
ok   test_jsx.py: JSX-DONE | STYLES ALL PASS 23/23
ok   test_kanon.py: KANON ALL PASS 20/20
ok   test_lint.py: LINT 0 ERROR
ok   test_lookup.py: LOOKUP ALL PASS 15/15
ok   test_normalize.py: NORMALIZE ALL PASS 42/42
ok   test_pdf.py: PDF ALL PASS 10/10
ok   test_pdf_crs.py: PDF-CRS ALL PASS 17/17
ok   test_pdf_cup.py: PDF-CUP ALL PASS 24/24
ok   test_pdf_de.py: PDF-DE ALL PASS 20/20
ok   test_pdf_layout.py: PDF-LAYOUT ALL PASS 26/26
ok   test_pdf_onculture.py: PDF-ONCULTURE ALL PASS 11/11
ok   test_quant.py: QUANT ALL PASS 5/5
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 11/11
SUITE ALL PASS 22/22
```
srom-tlumacz, the checks in its CLAUDE.md (venv, all exit 0), contract test against srom-produkcja **1a560da**:
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
HANDOFF CONTRACT 33/33          (E1, E2, E4: GAP CLOSED)
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```

Re-measured by me on copies (srom-produkcja 1a560da):

| text | `check.py --pair` | `build --pair-src --queries --draft` | build without `--draft` | FRONT | Word copy → import → pair | 2026 spelling (linter WARN) |
|---|---|---|---|---|---|---|
| Ndiaye | CHECK OK | PASS | PASS | OK | `_v2`: CHECK OK | 8 ORTH-OWSKI, 1 ORTH-NIE-IMIESLOW |
| Ostendorf | CHECK OK | PASS | FAIL: `[BRAK …]` nn. 1, 2, 11, 12, 15, 17, 18, 34, 36, 47, 48 (OST-1) | OK | CHECK OK | 0 |
| Pahulich | CHECK OK | PASS | FAIL: `[BRAK MIEJSCA]` nn. 47, 145 | OK | CHECK OK | 1 ORTH-OWSKI |
| Tittel | CHECK OK | PASS | FAIL: `[BRAK WYDAWCY]` n. 20 (GEN-4) | OK | CHECK OK | 6 ORTH-OWSKI |

The non-draft failures are exactly the known imprint gaps; nothing else is in the reports' error sections.
Source copies: all four `src/manifest.sha256` OK, and `cmp` with srom-produkcja's `<id>_src.md`, `<id>_src_front.md` and `refs.json`
shows them identical. Mutation tests (`mutate_keyed.py`): Ndiaye, Ostendorf, Scheffknecht, Tittel, West Ohueri
`MUTATIONS CAUGHT 40/40`. No delivery yet, so `take_back.py` has nothing to verify.
Gates: srom-produkcja V1–V6 (closed since the last review) all hold. srom-tlumacz has no newly closed gates. I re-ran all
95 CHECK/EXPECT pairs of its 17 gate files on a copy: 86 hold. Four of the nine drifts are annotated old records (1.1 G4, G9; 1.3.1 G6; 1.5.2a G5). Five are new
(row 11). Every Word copy's sha256 was unchanged after the run.
Hooks (`_handoffs/tools/hooks/`): `guard_module.py` refused 4/4 cross-module edits (Kanon via `~/.claude/skills`, a new file via
`../srom-typeset/`, srom-quant via `~`, srom-tlumacz from a session opened at `srom-typeset/`) and the NotebookEdit case. It passed
own notes, `_handoffs/`, a look-alike path `srom-produkcja-old/` and broken JSON. `/usr/bin/python3 <missing script>` → exit 2.

## Findings

| # | Finding | Evidence | Severity | Fixes |
|---|---|---|---|---|
| 1 | **A missing guard script blocks every edit in a module session.** The hook command runs `/usr/bin/python3 "<absolute path>/guard_module.py"`. If the file isn't there (SROM folder moved or renamed, `_handoffs/tools/hooks` renamed), Python exits 2, and a PreToolUse exit 2 means "refuse". The fail-open promise only covers errors *inside* the script. | `srom-produkcja/.claude/settings.json:9`, `srom-tlumacz/.claude/settings.json:9`; `echo '{}' \| /usr/bin/python3 /nonexistent/guard_module.py` → rc=2 | will bite (only on a move, but then totally) | srom-produkcja, srom-tlumacz (own settings.json) |
| 2 | **The guard has not been seen working in a live session** (MB's test not done yet; the render hook fired live here, 16:30). The suggested test ("add a line to the Kanon") edits the Kanon for real if the guard fails. | MB, 01.10.2026 | will bite if wrong | MB (harmless test below) |
| 3 | **T27, T28, T29 unanswered; T28's spelling fixes not made.** T28 (30.09 00:06, "action for you") asks for the 2026 spelling in the drafts (Kanon v1.9 § 12.3). Re-measured: Ndiaye 8 ORTH-OWSKI + 1 ORTH-NIE-IMIESLOW, Tittel 6, Pahulich 1, which is T28's own count. The Word copies are unedited (sha256 = committed), so the md can still be fixed and re-exported. | `produkcja-to-tlumacz.md` T27–T29 (last lines); `tlumacz-to-produkcja.md` ends with "Status of T25, T26"; srom-tlumacz git log: no module session after 349ac75 (29.09 18:43). | will bite | srom-tlumacz (after MB answers For MB 2) |
| 4 | **`take_back.py` accepts only `<id>_robocza.docx`; Ndiaye's master is `ndiaye_robocza_v2.docx`.** `handoff.md` "Back" step 1 allows a new name (`_v2`) and lets the editor say which file is the master. The tool then takes v1 (the old draft) and fails the "md = import of the master" check. It fails loudly, but it fails on the first text expected back (and G12). Each further re-export to `_v2` (T28) repeats this. | `take_back.py:24` (`REQUIRED = ("{id}_robocza.docx", …)`), `:96`; `handoff.md` Back 1; MB-decisions NDI section names `ndiaye_robocza_v2.docx` | will bite (first delivery) | srom-produkcja (contract), then srom-tlumacz |
| 5 | **The start-of-session review check will flag old reviews forever.** Root CLAUDE.md: "if a `review-*.md` exists that your outgoing file has no 'Status of review' heading for, tell MB." Neither outgoing file has such a heading. The 28.09 and 29.09 reviews were applied before the heading was introduced (29.09 23:05). So every module session reports them. | `CLAUDE.md:49–50`; `grep "Status of review" _handoffs/*.md` → none; applied: srom-tlumacz 56b5801, srom-produkcja f13209c/6e9ea9e | cosmetic (noise every session) | MB (root CLAUDE.md: "the newest `review-*.md`") |
| 6 | **The checkup skill checks a section the ledger no longer has.** Item 6 says "'Needs MB now' lists every one of them". Since 29.09 23:04 the ledger has an "At a glance" table instead. I checked that table: 65 rows = 65 sections, every "Next free" correct, every Detail file exists and carries its ID. | `_handoffs/checkup/SKILL.md:60`; `MB-decisions.md:13` | cosmetic | MB (root session edits the skill) |
| 7 | **Kartoteka has a row MB hasn't approved yet, unmarked.** *Anglo-Romani* → „angielscy Romowie” is entered as the standard form, while OST-6 still asks MB to approve it. Rows 42–43 cite "ostendorf_queries B13/B14": that file is now `ostendorf_uwagi.md`, and the items are OST-3. If MB says no to OST-6, nothing tells a later session the row was provisional. | `srom-kanon/references/kartoteka.tsv:39, 42, 43` (flag column empty); `MB-decisions.md` OST-6 | cosmetic | srom-produkcja |
| 8 | **srom-produkcja's notes sheets have no history.** `work/` is git-ignored. Since 29.09 the ledger drops a question once MB's answer is "recorded where it takes effect", often the notes sheet. For srom-produkcja's sheets, that record can be overwritten with no trace. srom-tlumacz's sheets are tracked. (Frozen sources are safe: sha256 in T-items, copies tracked in srom-tlumacz.) | `srom-produkcja/.gitignore:8` (`work/`); `git check-ignore work/pahulich/pahulich_uwagi.md` → ignored | will bite (low) | srom-produkcja |
| 9 | **Stale text, srom-produkcja.** | `CLAUDE.md:20` "system `python3` is 3.9 and too old" (in Claude's shell `python3` is miniconda 3.13 with python-docx, lxml, PyMuPDF 1.28.0; `/usr/bin/python3` is 3.9). `SKILL.md:18` same; `:23` "SUITE ALL PASS 19/19" (22/22). `HANDOVER-produkcja.md:1` "state at 29.09.2026 17:59" (holds 30.09 content); `:28` "20/20"; `:345` "open items there: D17 … D20, D24, D26 (e), D15" (now PAH, SCH, OST, TIT, WOH, GEN-11, GEN-2). `srom-quant/SKILL.md:89`, `scripts/validate_master.py:25` "Kanon v1.6 § 12.2.3" (the § holds, the version label is old). `dist/*.skill` (30.09 01:56) predate v1.10 (02:17): rebuild before any claude.ai upload. | cosmetic | srom-produkcja |
| 10 | **Stale text, srom-tlumacz.** | `CLAUDE.md:35` "Kanon v1.7 § 12.2" (v1.10). `HANDOVER.md:1` date; `:46` "30/30 … against 0c75f49" (33/33, T26); `:47` "Kanon v1.7 is normative … three dated supplements" (v1.8 absorbed them, now v1.10); § 6 "D5 and D26 … D22, D23, D25" (now SYS-1, V19-1–4, OST-, PAH-, TIT-). `tlumacz-PLAN.md:55` IF-KANON "v1.7"; `:89` "D24"; `:93` "D5"; `:94` "D20 B11"; `:95` "D26 (e)" (WOH-1, SYS-1, TIT-7, GEN-11). | cosmetic | srom-tlumacz |
| 11 | **srom-tlumacz gate drift (5 new).** 1.5.2a, 1.5.3a, 1.5.4a, 1.5.5a G1 run `shasum -c` in srom-produkcja's `work/<id>/` against a manifest that lists `<id>_queries.md`. srom-produkcja renamed that file `<id>_uwagi.md` (29.09 23:13), so the count is 3, not 4. 1.1 G12: selftest 9/9, expect 7/7 (the selftest grew), unannotated. | re-run above | cosmetic | srom-tlumacz (NOTE lines; no CHECK rewrite needed) |

Not findings:
- The guard covers only Claude's edit tools, not shell writes (`sed -i`, `cp`). That's accepted and written down as a rule. A module
  session can also edit its own `.claude/settings.json` and so switch its guard off. That's fine: the guard is a seatbelt, not a lock.
- No hook against the "system Python": agreed. In Claude's shell `python3` is miniconda 3.13 with the same packages
  (PyMuPDF 1.28.0 vs the venv's 1.28.2), so the hook would refuse working commands.
- The root `.claude/settings.json` (render hook only, 14 lines) is outside git. It's cheap to rebuild. If you want it versioned, it could be a
  symlink into `_handoffs/` like the checkup skill; not needed.
- The per-article `wordcheck.py`/`source_imprints.py` copies stay after promotion, by a documented choice (closed gates re-run
  them; `work/` is git-ignored). srom-produkcja's 30.09 work has tests but no GATES batch. The suite covers it.
- The `[BRAK …]` gaps (OST-1, GEN-4, Pahulich nn. 47/145), West Ohueri not taken (WOH-1), and E5 (`tb_check.py`) as a slot are all
  known and in the ledger or the contract.

## Last review's findings

| # (29.09) | Finding | Now |
|---|---|---|
| 1 | E17–E19 unanswered | fixed: T25 and status lines (29.09 17:52), kartoteka now 42 rows |
| 2 | Gates overwrite MB's Word copies | fixed: 1.5.4b/1.5.5b G8 use a temp dir; re-running all 95 CHECKs left every Word copy unchanged |
| 3 | Hand-back contract vs practice | fixed: `handoff.md` "Back", `take_back.py` + 19 tests, OUT-DELIVERY, contract test 33/33. New sub-issue: row 4 |
| 4 | ID collisions | fixed: rule in root CLAUDE.md and both modules; no collision since |
| 5 | Source-changing decisions before MB's Word edits | **still open** (MB): PAH-2 (merge notes 1/2), TIT-2 (title note), TIT-7 (MEW 741), V19-1. The Word copies are still unedited, so these are still cheap now |
| 6 | Translation JSX (`_postimport`, `_ibidem`, `_gwiazdki`) never run in InDesign | **still open**: G12 is queued as a translated article (`HANDOVER-produkcja.md` § 3 item 7) |
| 7 | Guessed times | fixed: correction lines; every time since is ≤ its commit (T25–T29, status lines, ledger entries checked) |
| 8 | MB's decisions shown open / not applied | fixed: D21 closed in the docs, D18 A5 applied, T20→T21 |
| 9 | Stale text, srom-typeset | fixed then; new stale text: row 9 |
| 10 | Stale text, srom-tlumacz | fixed then; new stale text: row 10 |
| 11 | "v1.7" with supplements | fixed: v1.8, then v1.9 and v1.10 as new rows; header, § 17, RULES, SKILL and the build report all say v1.10 |
| 12 | srom-typeset gates check files meant to change | fixed: marked as records, rule in CLAUDE.md; V1–V6 test only their own outputs |
| 13 | srom-tlumacz gate drift | fixed then; 5 new drifts: row 11 |

## For srom-produkcja

1. **Guard fails closed when its script is missing** (row 1). In `.claude/settings.json:9`, make the PreToolUse command
   exit 0 when the file is absent, e.g.
   `H="/Users/…/SROM edit and trans/_handoffs/tools/hooks/guard_module.py"; [ -f "$H" ] || exit 0; /usr/bin/python3 "$H" srom-produkcja`.
   Verify: run the command with `H` pointing at a missing file → exit 0; with the real file and a srom-tlumacz path
   on stdin → exit 2. Commit. (srom-tlumacz does the same for its copy.)
2. **Master file name at delivery** (row 4). `take_back.py:24, :96` require `<id>_robocza.docx`. Cheapest: one rule in
   `handoff.md` "Back" step 3: the delivered master is always named `<id>_robocza.docx`; before delivering, srom-tlumacz
   renames MB's master to that name (older exports → `<id>_robocza_old<n>.docx`). Alternative, ~10 lines + a test: a
   `--master <file>` option in `take_back.py`. Either way, add a case to `test_takeback.py`, announce it in a T-item, and ask
   srom-tlumacz to align OUT-DELIVERY and its contract test. Ndiaye (`ndiaye_robocza_v2.docx`) is the first case.
3. **Kartoteka** (row 7): `kartoteka.tsv:39` *Anglo-Romani*: say in the note that the row waits for MB's OST-6 (or
   use the flag column), so a "no" is traceable. `:42`, `:43`: `ostendorf_queries B13/B14` → `ostendorf_uwagi.md`, OST-3.
   Verify: `test_kanon.py` green.
4. **Notes sheets in git** (row 8): un-ignore `work/*/*_uwagi.md` (e.g. `work/*` plus `!work/*/` and `!work/*/*_uwagi.md` in
   `.gitignore`), commit the six sheets. Optional: the keying scripts `work/*/refs.py`, `key.py`. Verify: `git check-ignore`
   no longer matches a notes sheet.
5. **Stale text** (row 9): `CLAUDE.md:20` (use srom-tlumacz's wording: `python3` on PATH is miniconda 3.13 with the packages;
   `/usr/bin/python3` is 3.9 without them; scripts still with the venv); `SKILL.md:18`, `:23` (19/19 → say "SUITE ALL PASS"
   without a count, so it can't go stale); `HANDOVER-produkcja.md:1`, `:28`, `:345` (ledger codes); `srom-quant/SKILL.md:89` and
   `validate_master.py:25` (drop the version label, keep § 12.2.3). Rebuild `dist/*.skill` only before an upload.
6. Status lines under `## Status of review 01.10.2026` in `produkcja-to-tlumacz.md`, one per item above.

## For srom-tlumacz

1. **Answer T27, T28, T29** with status lines (root CLAUDE.md: every incoming item gets one). T27 and T29 are information:
   "noted" is enough, with "Kanon v1.10" cited from now on.
2. **T28, the 2026 spelling** (row 3): the drafts still have Ndiaye 9 (`Molierowski…` ×8, „nie kontrastującego”), Tittel 6
   (`Kantowsk…`, `Marksowsk…`), Pahulich 1 (`Grellmannowskiej`). No Word copy has been edited (sha256 = committed). Ask MB first
   (For MB 2) whether he has opened any of them. If not, fix `<id>_pl.md` and re-export the Word copy in place (git keeps the old one).
   If he has, list the places in the text's notes sheet for his Word pass. Verify: `build.py … --draft` report shows no
   ORTH-/PUNCT-SPOJNIK warnings, pair CHECK OK, `draft_check --all` clean, and the new Word copy imports to CHECK OK.
3. **Guard fails closed when its script is missing** (row 1): in `.claude/settings.json:9`, the same change as srom-produkcja's
   item 1 (`[ -f "$H" ] || exit 0;` before the python call, module name `srom-tlumacz`). Verify the same way; commit.
4. **After srom-produkcja's T-item on the master file name** (row 4): align PLAN OUT-DELIVERY and `tlumacz-test_handoff.py`.
5. **Stale text** (row 10): `CLAUDE.md:35`; `HANDOVER.md:1`, `:46`, `:47`, § 6; `tlumacz-PLAN.md:55`, `:89`, `:93`, `:94`, `:95`: Kanon v1.10,
   33/33, and the ledger IDs (WOH-1, SYS-1, TIT-7, GEN-11, V19-1–4, OST-/PAH-/TIT-) instead of D-numbers.
6. **Gate drift** (row 11): a NOTE line under 1.5.2a, 1.5.3a, 1.5.4a, 1.5.5a G1 (srom-produkcja renamed `<id>_queries.md` to
   `<id>_uwagi.md` on 29.09 23:13; 3 of 4 now; the copy in `src/` keeps the old name) and under 1.1 G12 (selftest grew to 9/9).
7. Status lines under `## Status of review 01.10.2026` in `tlumacz-to-produkcja.md`, one per item above.

## For MB

1. **Test the guard, harmlessly.** Open a new session in `srom-tlumacz/` and ask it to create
   `../srom-produkcja/guard-test.txt` with one word in it. It should be refused. If the file appears, the guard is not
   working: delete the file and tell any session. Don't use "add a line to the Kanon" as the test: if the guard
   fails, the Kanon really changes. The render hook is proven live: writing this file in this root session rebuilt `_widok/` (16:30).
2. **Before you edit any Word copy:**
   - Tell srom-tlumacz whether you have opened any of the four. If not, it fixes the 16 spelling points (T28) in the drafts
     and re-exports them. If you have, it lists them for your Word pass.
   - Still from the last review: PAH-2, TIT-2, TIT-7 and V19-1 change the text or its numbering. Decided after your
     edit, each one has to be made by hand in the Word file.
3. **Two root rule fixes, one yes covers both:** root `CLAUDE.md:49` "if a `review-*.md` exists…" → "if the newest
   `review-*.md`…" (row 5), and the checkup skill's "Needs MB now" → "the At a glance table" (row 6). A root session makes the edits.
4. Still at the top of the ledger: GEN-1 (blocks the open-access announcement) and TIT-1 (blocks the Tittel delivery).
