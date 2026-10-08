# Review — [general] 07.10.2026 (23:22–23:41): milestone checkup on the Mac, after the cloud draft of 06.10

Full root pass on the Mac: tools, contract, Kanon, gates, the channels, hygiene, plus what the cloud draft could not
reach (Cowork's files, the Editorial Desk, the venv, InDesign). Built on `draft-review-06.10.2026-cloud.md` and its status
section (07.10 22:40); every row re-measured here. Repository: `main` was 117c3aa, pulled to e567548 (the cloud's four
root commits, fast-forward); one untracked folder, not this session's (F12). Cowork's folder was read, never written.

## Conclusions

1. **The tools are healthy.** SUITE ALL PASS 26/26 on the Mac (venv, pandoc 3.8.3, InDesign present: `test_install` 1/1),
   HANDOFF CONTRACT 33/33 at e567548, srom-tlumacz's checks clean, Kanon v1.16 everywhere, 468 § references with none
   unresolved, skill links right, backup verified.
2. **The data and the decisions are not.** Since the evening of 06.10 the journal's work moved from Cowork to Code (Mac
   and cloud) while its data stayed in Cowork. The vol. 18 master CSV now exists in two versions, two days before the
   release: Code's has MB's licences, the 09.10 online date and K12's columns; Cowork's (the declared master) has the 407
   references the Crossref deposit needs. A deposit made from either copy alone is wrong (F1).
3. **MB's desk answers were not lost: nothing read them.** Four answers (06.10, 23:07–23:58) sit in the desk's store.
   Only a Cowork session reads the desk, and none has run since 22:21 that evening. V19-2 („radziecki”) reverses what the
   Pahulich and West Ohueri drafts assume; MB has opened neither Word copy yet, so it can still go in cleanly (F2).
4. The cloud draft's two tool gaps are confirmed: the first INJECT build of a translated text stops on normalisation
   (F3), and a fresh Cowork VM cannot install the PDF library the cover page needs (F4).
5. Cowork's ledger and records stand at 06.10; the module handovers and some root text still describe the world before
   SYS-9 (a) (F5–F8). Small record gaps, cloud leftovers and Mac leftovers (F9–F12).
6. **Cloud sessions are discontinued** (MB's go-ahead 07.10.2026; root CLAUDE.md § Cloud sessions, this session). A third
   place of work that cannot see Cowork's data fed F1, F2 and half the rest; the repository and GitHub stay as the backup.

## Verdict lines as printed

srom-produkcja, `python3 .claude/skills/srom-produkcja/tests/run_all.py` (from `srom-produkcja/`; it switches to the venv:
Python 3.13.15, pandoc 3.8.3), commit e567548:
```
ok   test_check.py: CHECK ALL PASS 80/80
ok   test_citemap.py: CITEMAP ALL PASS 44/44
ok   test_csl.py: NOTES ALL PASS 38/38 | BIB ALL PASS 20/20 | POSITION ALL PASS 10/10
ok   test_docx_in.py: DOCXIN ALL PASS 23/23
ok   test_doi.py: DOI ALL PASS 20/20
ok   test_e10.py: E10 ALL PASS 9/9
ok   test_e2e.py: E2E ALL PASS 85/85
ok   test_e8.py: E8 ALL PASS 18/18
ok   test_examples.py: EXAMPLES ALL PASS 3/3
ok   test_install.py: INSTALL ALL PASS 1/1
ok   test_jsx.py: JSX-DONE | STYLES ALL PASS 23/23
ok   test_kanon.py: KANON ALL PASS 20/20
ok   test_kb.py: KB ALL PASS 4/4
ok   test_lint.py: LINT 0 ERROR
ok   test_lookup.py: LOOKUP ALL PASS 15/15
ok   test_normalize.py: NORMALIZE ALL PASS 49/49
ok   test_pdf.py: PDF ALL PASS 20/20
ok   test_pdf_crs.py: PDF-CRS ALL PASS 17/17
ok   test_pdf_cup.py: PDF-CUP ALL PASS 24/24
ok   test_pdf_de.py: PDF-DE ALL PASS 20/20
ok   test_pdf_layout.py: PDF-LAYOUT ALL PASS 26/26
ok   test_pdf_onculture.py: PDF-ONCULTURE ALL PASS 11/11
ok   test_quant.py: QUANT ALL PASS 42/42
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 12/12
SUITE ALL PASS 26/26
```

srom-tlumacz, the four checks of its CLAUDE.md (venv, through `~/.claude/skills/srom-tlumacz`), against srom-produkcja e567548:
```
shape: 40 rows, 0 problem(s)          (check_tb --schema --shape --vocab --precedent --evidence: exit 0;
precedent verified: 11/11              training quotes verified: 25/25)
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 33/33
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```
`tlumacz-draft_check.py --selftest`: `selftest: 8/8 negative controls caught`.

Other measurements (07.10.2026 23:22–23:41):
- `validate_master.py` on scratch copies of the vol. 18 CSV: Code's → `BLOCKING ERRORS (30)` (`pub_date_print`, `editorial_period`
  empty in 15 rows); Cowork's → `BLOCKING ERRORS (72)` (`pub_date_online '2025-12-TODO'`, licences `TODO`, the two columns missing).
- The two CSVs compared field by field: they differ only in `pub_date_online` (15 rows), `license` and `license_url` (13 rows),
  all filled in Code's, and in Code's two extra columns. `volumes/autorzy.tsv`: Code's adds two e-mails (Fotta, Wesołkin);
  `ror.tsv` identical. Only Cowork has `volumes/18/citations/` (10 files) and `bib_from_pdf.py`.
- Editorial Desk store (`ArtifactData`, read only): `meta/sync` = `06.10.2026 17:41`; `decisions` with `status == "answered"`:
  V18-100 (06.10 21:07 UTC), V18-101 (21:07), V19-2 (21:10), V19-3 (21:58), none since.
- Word copies in Cowork's `srom-tlumacz/work/`: all at their export times (03.10.2026 01:10; West Ohueri 06.10.2026 15:29); no
  Office lock files.
- `python3 _cloud/check_pins.py`: `PINS OK (python-docx 1.2.0, lxml 6.1.3, PyMuPDF 1.28.2, pikepdf 10.16.0; vs Mac venv)`.
- PyPI `requires_python`: pikepdf 10.13.0.post1 `>=3.10` (7 cp310 wheels); 10.14.0, 10.15.0, 10.16.0 `>=3.11` (no cp310 wheels).
- `sh _cloud/verify_backup.sh`: `BACKUP OK srom-20261004-2120.tar.gz: 5248 paths, sha256 verified, 98M`.
- Kanon: 67 headings; 468 `§` references in the skills and module docs, 0 unresolved.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| F1 | **Vol. 18 data forked between Code and Cowork, two days before the release.** Code's copy (meant to be reference, SYS-9 (a)) is ahead; Cowork's (the master in its `STATUS.md`) lacks MB's 07.10 decisions and K12's columns but alone has the references. `generate_crossref_xml.py` takes references from `citations/` next to the CSV it is given and only notes a missing file: a deposit from Code's copy goes out silently without references, one from Cowork's fails validation. Cause: on 07.10 the vol. 18 work ran in Code (Mac 01:34–01:48: 3ec2d51, ef72369; cloud 21:45–22:03: 918fb44, d337459, 117c3aa); no Cowork session since 06.10 22:21. | Measurements above; `generate_crossref_xml.py:63-71, 238`; Cowork `STATUS.md` § Volume data ("this copy is the master") | **blocks** (vol. 18 release, 09.10.2026) | MB (which copy, two values), then Cowork (K14) |
| F2 | **MB's four desk answers were never applied.** Only Cowork reads the desk (srom-naczelny § Start of a session; § The desk, step 1); Code sessions have no desk step. V18-100/101 reached Code's CSV another way (3ec2d51), but neither the desk, Cowork's ledger nor Cowork's CSV. V19-2: MB made „Związek Radziecki/radziecki” the standard, „sowiecki” accepted; the termbase still has `sowiecki` as the house form, and the drafts use it (Pahulich 8×, West Ohueri 2×). V19-3: five of six terms approved; „uinnienie/uinniać” not; „sedentaryzacja” accepted beside „osiedlanie”. No Word copy edited yet, so the drafts can still change cleanly. (The second artifact, "Studia Romologica Desk", is a website dashboard, not a second desk.) | desk store (above); `srom-tlumacz/.claude/skills/srom-tlumacz/references/tlumacz-tb.tsv:39` (C-0048 „sowiecki”, "OPEN: radziecki"), `:33` (C-0042), `:40` (C-0049); `grep -c` in the drafts | will bite (MB edits two drafts with the wrong term; answers look lost) | Cowork (K14); MB opens a Cowork session |
| F3 | **INJECT has no normalise step** (cloud draft finding 1, confirmed). A final build fails on text `normalize.py` would still change, and its message says to run `normalize.py` on the file; the contract builds from `pl/`, which is never edited and sealed by `SHA256SUMS`; scenario C says "→ 2 → 6 from `work/<id>/pl/`", step 2 being an in-place run. A normaliser flag (e.g. DOUBLE-MARKER) can only be fixed in the Word master. On the cloud draft's copies: Ndiaye 9 changes + 1 flag, Ostendorf 9 changes. | `build.py:881-891`; `references/handoff.md:84-91, 98-108`; `references/stages.md:54-61`; `SKILL.md:38, 75` | will bite (first INJECT of a translated text) | srom-produkcja (srom-tlumacz if the tested wording changes) |
| F4 | **pikepdf missing for Cowork** (cloud draft findings 2–3, confirmed). `requirements.txt` (what `setup.sh` installs) has no pikepdf; `test_quant.py` imports it at module level; `cover_page.py` aborts without it, with a Mac-only hint. The Mac pin 10.16.0 needs Python ≥ 3.11, Cowork's VM is 3.10.12 (C3). Three pin lists (`requirements.txt`, `tools/setup_mac.sh` unpinned, `_cloud/setup-cloud.sh`); `check_pins.py` reads Cowork's retired plugin path, so on the Mac it compares the venv with the cloud script only and cannot see the file Cowork installs from. `SKILL.md:17` lists three packages; `setup.sh:5` still says it lives at the root of the srom plugin. | `requirements.txt:3-5`; `setup.sh:5, 12`; `test_quant.py:247`; `cover_page.py:355-358`; `tools/setup_mac.sh:14`; `_cloud/check_pins.py:7`; PyPI above | will bite (fresh Cowork VM: suite fails, no cover pages) | srom-produkcja |
| F5 | **Cowork's ledger and records stand at 06.10.** Open in the ledger but answered or settled: V18-100/101, V19-2/3 (F2); SYS-100 (K12: MB's own template 2; "SYS-6 moot"); SYS-102 (C6: translator default MB, `translators_struct` filled); SYS-101 is met by a different solution (K12 prints "Okres redakcji" from `editorial_period`), which MB has not confirmed as its answer. Not entered: K11 ("needs MB"), K12's question (vol. 18 `pub_date_print`, `editorial_period`: blocks the release). K8–K13 have no answer (`cowork-to-code.md` ends at C6, 06.10 17:40). `STATUS.md`: C5 and C6 lines unticked (committed 20f4f26, e0a51a2), "9 PROVISIONAL" (10 since C-0050), the online-PDF procedure names `_handoffs/cowork/fix_actualtext.py` (inside `cover_page.py` since K10). `workspace/reviews/` does not exist: Cowork's checkup has never run, so this checkup's step 2 had no review to read. | Cowork `MB-decisions.md` "At a glance", § V18, § SYS; `STATUS.md` § For the skills, § Translation module state, § Volume data; `code-to-cowork.md:173-183` | will bite (settled questions look open; a release blocker is missing from MB's list) | Cowork (K14); MB confirms SYS-101 |
| F6 | **The rendered views show a pointer and outdated copies.** Root CLAUDE.md sends every session to `_widok/MB-decisions.html` and the text pages; `mb_view.py` renders Code's `MB-decisions.md` (a pointer since SYS-9 (a)) and Code's reference notes sheets, which are already behind: Scheffknecht's and West Ohueri's notes sheets and West Ohueri's source front matter changed in Cowork on 06.10 15:08 (SCH-1, WOH-1, WOH-2 from the desk), and West Ohueri's translation exists only in Cowork. The render hook is wired in all three `settings.json`. MB's live questions are Cowork's ledger and the desk. | `CLAUDE.md:128-133`; `_handoffs/tools/mb_view.py:21, 179`; `_handoffs/tools/hooks/render_mb_view.py`; `diff -rq` of both `work/` trees | will bite (MB is shown outdated notes) | root (cleanup task) |
| F7 | **Module docs stale** (cloud draft finding 4, confirmed). srom-produkcja: handover "state at 02.10.2026", Code's `MB-decisions.md` as the one list, 24/24, "Choices awaiting MB: SYS-6, SYS-7"; CLAUDE.md "Three skills" (six), volume data in `volumes/` (Cowork's master), srom-tlumacz "not a skill here" (a skill since 03.10, E20), question IDs in `MB-decisions.md`. srom-tlumacz: HANDOVER "9 PROVISIONAL" (10), "33/33 against cb3cfe5", ledger in Code, West Ohueri "not started" (drafted in Cowork 06.10); CLAUDE.md "this folder is a git repository" (one repository since 05.10), IDs in `MB-decisions.md`; the PLAN status log ends 04.10 23:15 (nothing for a414512, C-0050). | `srom-produkcja/docs/HANDOVER-produkcja.md:1, 3-4, 28, 234, 400-402`; `srom-produkcja/CLAUDE.md:4, 9, 13, 44`; `srom-tlumacz/HANDOVER.md:12, 36, 55-61, 74`; `srom-tlumacz/CLAUDE.md:37, 40`; `srom-tlumacz/tlumacz-PLAN.md` (tail) | will bite (a new module session starts from these) | srom-produkcja, srom-tlumacz |
| F8 | **Root text about the ledger is stale.** `_handoffs/README.md` still calls Code's `MB-decisions.md` "every open question" (Files list, rule 5, "Next free"); root CLAUDE.md § Checkup step 3 ("Put items that need MB in `MB-decisions.md`") and § Messages ("PAH-11 in `MB-decisions.md`"). § Decisions for MB and the pointer file say it right. | `_handoffs/README.md:12, 26, 60`; `CLAUDE.md:79, 90` | cosmetic | root (cleanup task) |
| F9 | **Gaps in the record to Cowork.** (a) 39302d3 (knowledge base Scope line, srom-zizek's link to it, `test_kb.py`, suite 25 → 26) has no K-item; (b) C5's termbase row: K8 says "not done", 20f4f26 committed it, no done line; (c) the status of C6 was written into `produkcja-to-tlumacz.md`, which Cowork does not read; (d) ef72369 (depositor e-mail in `generate_crossref_xml.py`), made by a Mac session under "cowork:", has no item on either side. All four are stated in K14. | `git show 39302d3 ef72369`; `code-to-cowork.md:132-147`; `produkcja-to-tlumacz.md:719-721` | cosmetic | root (K14, done) |
| F10 | **Times and tags.** K8 says 15:52, its commit adc86d1 is 15:51:41; "[West Ouhueri]" in K8 and commits 1113fec, adc86d1; K3's heading "(04.10.2026 04.10.2026 21:46)"; fa0426d "quant:" with no text tag. Correction line for K8 in K14. | `code-to-cowork.md:64, 132`; `git log` | cosmetic | root (K14, done) |
| F11 | **Cloud machinery left behind.** `_cloud/GATES.md` G2 (`test_roundtrip.py` gone), G5 and G8 (`cowork_sync.py` retired), G7 (tests Code's `MB-decisions.md`, a file meant to change), G9 (`../srom-cloud` gone) no longer hold; G3 holds on the Mac but checks the wrong file (F4). Five merged `claude/*` branches on GitHub (lucid-lovelace, vibrant-mccarthy, gracious-darwin, zealous-galileo, serene-ramanujan; none has a commit outside `main`). With the cloud discontinued, all of `_cloud/` except `backup.sh`/`verify_backup.sh` has no job. | `_cloud/GATES.md`; `git log origin/main..origin/claude/*` (empty) | cosmetic | root (cleanup task) |
| F12 | **Leftovers.** Untracked `srom-produkcja/dump/crossref_test/` (07.10 01:21–01:47: four vol. 18 PDFs from Cowork's `dump/Crossref PDFs/`, `crossref_srom_18_test.xml`, a cut-down CSV with one citations file), not committed by its session; `CODE/SROM/SROM edit and trans.old` (152 MB; its 11 hashes are mapped since f4421cc); empty `CODE/SROM/_to_delete/`; `~/.claude/skills/wp-acf-plugin-builder` and `wp-elementor-builder` are July copies, not links, beside the repository's (differ in `references/srom-project.md`: the old skill name). | `git status`; `ls`, `du`; `diff -rq` | cosmetic | MB (cleanup task) |

Not findings (checked, fine): Kanon v1.16 in the header, the last § 17 row, RULES.md and srom-kanon SKILL.md, no rule text
changed since the last review (only the knowledge base, e0a51a2 and 39302d3); srom-kanon's "Open — do not invent" list still
true (GEN-1, GEN-2 open); no E- or T-item since the last review, so no group names to check; no new duplicate IDs (E9, E18
and T20 are old pairs, cited with their [Author] tag); T37 and
review 04.10.2026-2 answered on both sides; no contract change since the last review (`handoff.md`, `stages.md` untouched),
srom-tlumacz's SKILL.md step 6 and `outputs.md` § Back agree with `handoff.md`; root `.claude/skills/` links resolve (8);
`~/.claude/skills/srom-*` (srom-quant included) are links into the repository; `dist/` does not exist (nothing stale to upload);
srom-naczelny's card was re-saved 05.10.2026 15:07 with Code's paths and without `setup_font.sh` (draft's leftover: done);
`origin/main` = local `main`; G1 backup verifies.

## Last review's findings

Review 04.10.2026-2 (last full review): all eight items done — 1–5 in e079042 and 542dacf (status lines 04.10 23:11, 23:14);
the knowledge base's Scope line and srom-zizek's link completed only on 06.10 22:01 (39302d3, F9 a); 6 reversed with a reason
(`cards/.gitkeep`: srom-zizek SKILL.md copies the template "with an empty `cards/`"), accepted; 7 moot (`cowork_sync.py`
retired, K7); 8 done (K6; Cowork switched, C3).

Draft 06.10.2026 (cloud), against this pass: 1 → F3, open · 2, 3 → F4, open · 4 → F7, open · 5 closed (f4421cc) · 6 closed
(428df2f, K13) · 7 → F9, closed by K14 · 8 → F5, open (now K8–K13) · 9 → F10, closed by K14 · 10 → F11, open · 11: files
deleted (567fa59), branches → F11; whether modules may edit `_cloud/` pins is moot with the cloud discontinued · 12 superseded
by K12 → F1. Its "Checks not run", done here: skill links, `dist/`, `check_pins.py` against the venv (F4), the venv suite with
InDesign, `SROM edit and trans.old` (F12), `mb_view.py` and the hooks (F6), the backup (G1), srom-naczelny, Cowork's ledger and
records (F5), the desk (F2). Still not run: Cowork's texts (Cowork's checkup, F5), the Cowork VM's pikepdf (K14 step 1 checks it).

## For srom-produkcja

1. **Normalise at INJECT without editing `pl/`** (F3). Cheapest version: after `take_back.py`, `python3 $S/normalize.py
   work/<id>/pl/<id>_pl.md -o <a file outside pl/, e.g. work/<id>/build/<id>_pl.md> --log <…>_norm.md`, then `build.py` on that
   file with the same `--refs`, `--pair-src` and `--queries`. Write the step into `references/handoff.md` § Back item 4
   (lines 84–91) and the command block (98–108), `references/stages.md` § 3 Output and Pass (54–61), and `SKILL.md` scenario C
   (line 75: "→ 2 → 6 from `work/<id>/pl/`"). Say where a normaliser flag goes: the notes sheet, then the Word master and a new
   delivery (the md is never edited by hand). Make the hint at `build.py:890` name an output outside `pl/`. Test in
   `test_takeback.py`: a delivery that needs NOTE-FULLSTOP → take-back → normalise → build without `--draft` → PASS, and
   `SHA256SUMS` in `pl/` still verifies. Verify: SUITE ALL PASS. If you change wording that `tlumacz-test_handoff.py` checks, a
   T-item (contract change: tests on both sides).
2. **pikepdf for Cowork, one pin list** (F4). `requirements.txt`: `pikepdf==10.16.0; python_version >= "3.11"` and
   `pikepdf==10.13.0.post1; python_version < "3.11"` (10.13.0.post1 is the last release for Python 3.10; the cloud draft ran
   test_quant 42/42 with it). `tools/setup_mac.sh:14`: install `-r requirements.txt` instead of unpinned names. `SKILL.md:17`:
   add pikepdf (srom-quant's cover page). `setup.sh:5`: the header names its real place and command. `cover_page.py:358`: an
   abort hint without a Mac path (`pip install -r srom-produkcja/requirements.txt`). Leave `_cloud/` alone (retired with the
   cloud; root removes it). Verify: suite all pass; pip resolves the file for 3.10 and 3.13 (e.g. `pip install --dry-run
   --ignore-installed --only-binary=:all: --python-version 3.10 --target <tmp> -r requirements.txt`).
3. **Stale text** (F7): `docs/HANDOVER-produkcja.md` — header date; start sequence = root CLAUDE.md § Start of every session
   and § Cowork (Code builds and tests the skills; texts, volume data and MB's ledger are Cowork's); suite 26/26; line 234:
   SYS-6/SYS-7 are Cowork's SYS-100/SYS-101 and K12 has superseded the first; § 7: a question for MB goes as a K-item "needs MB";
   a short paragraph for 04–07.10 (SYS-9/10, `stages.md`, the knowledge base, one repository, C5/C6, cover page template 2,
   cloud discontinued). `CLAUDE.md:4` (six skills: srom-kanon, srom-produkcja, srom-quant, srom-zizek and the two WordPress
   skills), `:9` (Code's `volumes/` is a reference copy; write it as MB decides in For MB 1), `:13` (srom-tlumacz is a skill since
   03.10, E20), `:44` (question IDs: Cowork's ledger, through a K-item). Verify by reading.
4. **One K-item** to Cowork with the commits of items 1–2: Cowork re-runs `setup.sh`, then its preflight. (39302d3, C6, ef72369
   and the K8 correction are already in K14.)

## For srom-tlumacz

1. **Stale text** (F7): `HANDOVER.md:12` (termbase counts: re-count, 10 PROVISIONAL with C-0050), `:36` (HANDOFF CONTRACT
   against the current srom-produkcja commit), `:55-61` (MB's questions: Cowork's ledger; a new one as a K-item "needs MB" in
   `code-to-cowork.md`), `:74` (West Ohueri: drafted in Cowork 06.10.2026; the drafts in `work/` are reference copies, SYS-9 (a));
   `CLAUDE.md:37` (IDs → K-item), `:40` (one repository since 05.10.2026, `blessero/srom-cloud`; `.gitignore.module` inactive;
   commit by path and push, root CLAUDE.md); one `tlumacz-PLAN.md` status line for a414512 (K9) and C-0050 (20f4f26). Verify by
   reading; the four checks pass.
2. **V19-2 and V19-3 are Cowork's to apply** (F2: the termbase rows with the drafts, through the desk). Do not apply them here.
   When you find Cowork's termbase edit uncommitted, run your checks and commit it (root CLAUDE.md § Cowork).
3. If srom-produkcja's item 1 changes `handoff.md` wording your test checks: take its T-item, HANDOFF CONTRACT n/n, status line.

## For MB

In this order:

1. **Vol. 18 release (09.10): one copy of the data, and two values** (F1). Say in the Cowork session of step 2:
   - (a) **recommended:** Cowork's copy is made complete — it takes Code's CSV and authors register, which hold everything
     Cowork's has plus your 07.10 decisions; the references stay Cowork's. Cowork remains where the journal's data lives (your
     SYS-9 (a)), so the release runs in Cowork; Code sessions work on scratch copies.
   - (b) the release runs in Code on the Mac: Cowork's references are copied into Code, and Code's CSV becomes vol. 18's master.
   - The two values K12 needs: `pub_date_print` (the print date, YYYY-MM-DD) and `editorial_period` (as printed, e.g. „marzec
     2026 – czerwiec 2026”). Until then the cover pages and the validation stop.
2. **Open Cowork and say: "Do K14 in Code's `_handoffs/code-to-cowork.md`."** It applies step 1, your four desk answers (V19-2:
   „radziecki” in Pahulich and West Ohueri before you open their Word copies; five terms into the termbase), clears what is
   settled from the ledger (it will ask you about SYS-101 and „uinnienie”), enters K11 and K12, answers K8–K14 and runs its own
   checkup. **From now on: after answering on the desk, open Cowork — only Cowork reads the desk.**
   Run with: Opus · high effort — vol. 18 data before a release, plus editorial decisions applied to two drafts and the termbase.
3. **K11, before the vol. 18 website import:** DOI suffixes without look-alike characters (0 o 1 l i)? (a) **recommended:** for
   future volumes only; (b) re-mint vol. 18 now — impossible once the suffixes are imported; (c) leave as is. Answer in the same
   Cowork session.
4. **Apply this checkup in Code:** a session in `srom-produkcja/`, then one in `srom-tlumacz/`, each "apply checkup".
   Run with (srom-produkcja): Opus · high effort — a contract change across two modules with a new test.
   Run with (srom-tlumacz): Sonnet · medium effort — text updates and the standard checks.
5. **Cleanup and one folder, as a separate task** (F6, F8, F11, F12 and your Finder points): one folder for Cowork and Code (no
   "+" each session); a top level you use (an inbox for uploads, the Word files you edit now, PDFs for the website); Code's
   copies of the texts and volume data retired (they existed for the cloud); `_cloud/`, the rendered views, `.old`, the merged
   branches, `dump/` leftovers archived or deleted. Start it in the root session with: "Cleanup and folder structure (review
   07.10.2026, For MB 5)".
   Run with: Opus · xhigh effort — moves files and paths that every session and Cowork depend on.

## Status of For MB 5 (root session, 08.10.2026 02:17)
- **One folder:** done (2af8751, K16). `SROM/Redakcja/` holds `1. Inbox/`, `2. Word` (Smart Folder), `3. PDF online/`,
  `4. Archive/`, `SROM edit and trans/` (this repository, moved from `SROM/CODE/SROM/`; the old path is a link until
  15.10.2026) and `workspace/` (Cowork's, moved from `SROM/Cowork/srom-cowork/`). Skill links, InDesign script links and the
  project memory re-pointed; hooks wired through `$CLAUDE_PROJECT_DIR`. Rules: root CLAUDE.md § The one folder, Cowork's
  `workspace/CLAUDE.md` § The one folder. srom-naczelny's new card waits for MB's upload.
- **Code's copies of the texts and volume data:** retired (git history keeps them up to f24a568); srom-tlumacz's checks read
  Cowork's workspace (`tlumacz_paths.py`). F1's cause is gone: there is one copy.
- **F6** done: rendered views retired (`mb_view.py`, the hook, `_widok/` moved to `CODE/_backup/cleanup-20261008/`).
- **F8** done: README (files, rule 5, "Next free", notes sheets), root CLAUDE.md § Checkup step 3 and § Messages.
- **F11** done in the repository: `_cloud/` retired (`backup.sh`, `verify_backup.sh` → `_handoffs/tools/`), `_migracja/`
  retired, root § Cloud sessions → § Git, checkup without partial passes. The five merged `claude/*` branches (0 commits
  outside `main`, checked): not deleted, the session's permission check refused a remote deletion → MB.
- **F12** done: `dump/crossref_test/`, `_to_delete/` → `CODE/_backup/cleanup-20261008/`; `SROM edit and trans.old` →
  `CODE/_backup/`; `~/.claude/skills/wp-*` July copies → links into the repository (copies kept in the backup folder).
- **Finder points:** srom-typeset link removed; srom-produkcja's `dump/`, old cover templates (MB, 1.1, 1.2) and proofs → `4. Archive/`
  (the two IDMLs `test_jsx.py` needs → `tests/fixtures/idml/`); Cowork's bundle leftovers, old `dump/` and applied patches →
  `4. Archive/`. Nothing deleted.
- Verified after the move: SUITE ALL PASS 26/26; srom-tlumacz checks (shape 0 problems, selftest 9/9, HANDOFF CONTRACT 33/33,
  5 drafts clean, draft selftest 8/8), also as Cowork runs them from `workspace/srom-tlumacz/`; `desk_sync.py` on a copy
  (58 decisions, 0 unresolved, every path on the Mac).
