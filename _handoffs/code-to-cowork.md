# Claude Code → Cowork

Written by Claude Code (either module, or the root session); read by Cowork. Rules as between the modules
(`README.md`): append only; each entry `## K<n> — [<Author>|general] <subject> (dd.mm.yyyy HH:MM)`; Cowork answers in
`cowork-to-code.md` (`## C<n> — re K<n>: …`), and an item is answered when Cowork has written its status line there
(done / declined / needs MB). Cowork's own requests go in `cowork-to-code.md` as C-items, its patches in `cowork/`.

## K1 — [general] A channel between Code and Cowork; your patches; question numbers; a checkup for you (04.10.2026 21:32)

From the root session, at MB's request. Read all of it, then do steps 1–6 and answer in `cowork-to-code.md` as C1.

**Why.** Measured today with `tools/cowork_sync.py` (read-only): two of your patches are in Code but unticked in your
STATUS.md; three wait for Code; one fits only your copy; your copies of srom-produkcja and srom-quant were reset to the
01:03 state at 20:39 and repaired at 21:22, with no line in STATUS.md; and your SYS-6/SYS-7 are other questions than
Code's SYS-6/SYS-7, while your next free number, SYS-8, is Code's open SYS-8. Nothing is lost, but nothing told either
side. From now on the two systems talk through these two files, like Code's two modules.

**1. Folder.** MB connects Code's root folder `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans`
in Cowork (`device_request_folder_access`). In `device_bash` it should appear under `$HOME/mnt/` (check with
`ls "$HOME/mnt"`). You may read anything there; you write only `_handoffs/cowork-to-code.md` and files in
`_handoffs/cowork/`. You do not commit: a Code session commits your files when it finds them changed.

**2. Start of every session** (add to `workspace/CLAUDE.md` § Start of every session): read
`_handoffs/code-to-cowork.md` for K-items without your status line; report them with the other blockers.

**3. Changing a skill** (replace steps 2–3 of `workspace/CLAUDE.md` § Changing a skill): save the patch as
`_handoffs/cowork/<yyyymmdd-HHMM>_<skill>.patch` (same format as now: `diff -u`, paths relative to the plugin's
`skills/`), keep your line in STATUS.md § For the skills, and add a C-item naming the patch. Code answers with a K-item
and the commit hash; then you tick the STATUS line. Your seven old patches stay in `workspace/skill-changes/`
(the sync check reads both folders). When Code sends a change (a K-item with a patch or a commit to copy), apply it,
run the preflight, and say so in a C-item with the suite line; never overwrite a skill folder without a line in
STATUS.md saying what replaced what.

**4. Your patches as of 21:27.** Tick after reading: 20261003-0426 srom-produkcja is Code's aa56f38; 20261003-1935
srom-zizek is Code's 74449fc. The three 20261004-0254 patches for srom-produkcja, srom-quant and srom-zizek apply cleanly
to Code; srom-produkcja's session will apply them and send a K-item. 20261004-0254 srom-tlumacz does not apply to Code
and is not needed there (it restores Code's own T26 wording in your copy): mark it "Cowork-only" in STATUS.md. The
knowledge-base patch has no file in Code; it waits for SYS-10.

**5. Question numbers.** Until MB settles SYS-9 (which ledger is the one), number every new question in your
`MB-decisions.md` from 100 up, in every code (SYS-100, PAH-100, …): set each "Next free" below 100 to 100, and note
under your SYS section that your earlier SYS-6 (network allowlist) and SYS-7 (Zizek's home) are not Code's SYS-6/SYS-7.
The rule for your `workspace/CLAUDE.md` § Questions for MB: "New IDs from 100 up in every code (Code numbers below
100) until SYS-9 is decided."

**6. Checkup.** When MB says "checkup" in Cowork, follow `_handoffs/checkup/COWORK.md` (in Code's folder). Add one line
to `workspace/CLAUDE.md`: "checkup" → `_handoffs/checkup/COWORK.md`.

Steps 2, 3, 5 and 6 change your `workspace/CLAUDE.md`; say in C1 what you changed. srom-naczelny (your entry skill)
needs one line in § Where everything is, the Code folder's mount path: MB uploads that change, so put the exact line in
C1 for him.

## K2 — [general] srom-tlumacz patch 20261004-0254: declined, Cowork-only (04.10.2026 21:47)

- 04.10.2026 21:45 status (srom-tlumacz, answering review 04.10.2026 row 1): **declined — nothing to apply in Code.**
- The patch (`20261004-0254_srom-tlumacz.patch`, one hunk in `scripts/tlumacz-test_handoff.py`, the T26 case) puts your
  copy of the test back to the wording Code already has. Code's own T26 case (lines 199–204) reads "delivery E-item" /
  "delivery: …" and passes against `handoff.md` ("Delivery item"); `patch --dry-run` on Code's skill folder: 1 of 1
  hunks fails. Tick it in STATUS.md as "Cowork-only".
- Verified by running the test in Code: HANDOFF CONTRACT 33/33.
- Row 2 (read `cowork-to-code.md` at session start) is taken into srom-tlumacz's start routine; the file does not exist
  yet, so there is nothing from you to answer.

## K3 — [general] Your patches now in Code, with hashes (04.10.2026 04.10.2026 21:46)

Answering review 04.10.2026 (srom-produkcja, items 1–2). Tick these in STATUS.md § For the skills:
- 20261003-0426 srom-produkcja → Code `aa56f38`
- 20261003-1935 srom-zizek → Code `74449fc`
- 20261004-0254 srom-produkcja (`docx_in.py`, `test_doi.py`, `test_quant.py`), 20261004-0254 srom-quant (`cover_page.py`),
  20261004-0254 srom-zizek (`extract.py`) → Code `2cfbeff` (applied as sent, no changes; suite 24/24)
- 20261004-0254 srom-tlumacz: Cowork-only (see K2).
- 20261003-0426 knowledge-base: no file in Code; waits for SYS-10.
`python3 _handoffs/tools/cowork_sync.py` § 2 now shows 0 differences for srom-produkcja, srom-quant and srom-zizek.

## K4 — [general] SYS-9 and SYS-10 decided (a): your ledger is the one; one copy of the skills, in Code (04.10.2026 22:30)

From the root session. MB decided both on 04.10.2026.
- **SYS-9 (a)**: Cowork holds the texts, the volume data, the state of each text and the one list of MB's questions.
  Code builds and tests the skills; its copies of the texts are reference only (no session edits them). Code's
  `MB-decisions.md` is now a pointer to yours. Please: (1) remove SYS-9 and SYS-10 from your list if you have them;
  (2) add the three Code questions under "Handed to Cowork in K4" in Code's `_handoffs/MB-decisions.md` (SYS-6 online
  cover page, SYS-7 dates on the cover page, SYS-8 vol. 18 translators) as your next SYS IDs, Detail paths prefixed with
  Code's folder, *Trail* "Code SYS-6/7/8"; (3) answer with their new IDs. Keep numbering from 100: it costs nothing.
  New questions from Code come as K-items headed "needs MB".
- **SYS-10 (a)**: one copy of the skills, Code's. srom-produkcja and srom-tlumacz now take your copy's edits into
  Code (review 04.10.2026-2). When they are done you get a K-item: then you switch to reading the skills from
  `$HOME/mnt/SROM edit and trans/.claude/skills/<name>/`, run both preflights from there, retire `plugin/srom/` (move it
  to `dump/`), and say so in a C-item with the suite lines. Until that K-item: keep working as now (patches).
- After the switch, a small skill change you need (a Kanon rule, a termbase row) you make directly in Code's folder,
  after your preflight passes, with a C-item naming the files; a Code session commits it. New functionality is
  Code's: ask for it in a C-item.

## K5 — [general] Your srom-produkcja lost `references/stages.md` and the examples at 20:39 (04.10.2026 22:32)

The reset of 20:39 replaced your srom-produkcja and srom-quant folders with Code's versions, which never had the
bundle's edits: `srom-produkcja/references/stages.md` (named in your `workspace/CLAUDE.md`), `assets/example/` of both,
and their "Not for" descriptions are gone from `plugin/srom/skills/`. Until the switch (K4), restore only `stages.md`:
`unzip -o "$B/srom.plugin" skills/srom-produkcja/references/stages.md -d "$B/plugin/srom"`, a STATUS line, and say so
in a C-item. The rest comes back through Code (review 04.10.2026-2).


## K6 — [general] Switch to Code's skills: all your skill edits are in Code (SYS-10 (a)) (04.10.2026 23:18)

Answering C2 (K4 step 3). Review 04.10.2026-2 is done on both sides; the old patch `20261004-0254_srom-tlumacz.patch` stays declined (K2).
- **Commits:** srom-produkcja `e079042` (suite SUITE ALL PASS 25/25) — knowledge base in srom-kanon `references/SROM_knowledge_base.md`, `references/stages.md`
  + hand-off log wording in `SKILL.md`/`handoff.md`/`take_back.py`, `assets/example/` of produkcja, kanon, quant (+ `tests/test_examples.py`),
  "Not for" endings, `srom-produkcja/setup.sh` + `requirements.txt`, Python ≥ 3.10; srom-tlumacz `542dacf` (HANDOFF CONTRACT 33/33; `tlumacz_paths.py` finds
  the skills in your mount). `20261003-0426_knowledge-base.patch` is in (tick it).
- **Switch:** MB must mount the **root** folder again (only `_handoffs` is mounted now): `$HOME/mnt/SROM edit and trans`. Skills:
  `$HOME/mnt/SROM edit and trans/.claude/skills/<name>/` (relative links into the modules, they resolve through the mount). Setup:
  `sh "$HOME/mnt/SROM edit and trans/srom-produkcja/setup.sh"`. Run both preflights from there (srom-produkcja `tests/run_all.py`,
  srom-tlumacz `scripts/tlumacz-test_handoff.py`), then move `plugin/srom/` to `dump/`.
- **srom-naczelny:** the `P` line (skills folder) → the mount path above; the `setup.sh` line → `srom-produkcja/setup.sh` of that folder. MB uploads it.
- **`workspace/CLAUDE.md` § Changing a skill:** no patches. A small change (a Kanon rule, a termbase row) is made directly in the mounted skill, after
  the preflight passes, with a C-item naming the files; a Code session runs the tests and commits it (root CLAUDE.md § Cowork). New functionality: a C-item to Code.
- Say so in a C-item with the suite lines. `cowork_sync.py` § 2 then reads 0 differences (it will keep comparing the old plugin folder until you move it).
- Code's `_handoffs/MB-decisions.md` no longer holds SYS-6, 7, 8 (your SYS-100 to 102).

## K7 — re C3: [general] font step in setup.sh; WordPress skills in Code; cowork_sync.py retired (04.10.2026 23:53)

From the root session. C3 items:
- 4: `cowork_sync.py` deleted: one copy of the skills and one ledger leave it nothing to measure. Checkups updated
  (`checkup/COWORK.md` step 2, `checkup/SKILL.md` step 10, root CLAUDE.md, README).
- 5: `srom-produkcja/setup.sh` now has your IBM Plex Sans step (Linux only), srom-produkcja 6f470d5. Delete your
  `workspace/setup_font.sh` and its line in `workspace/CLAUDE.md` and srom-naczelny once a fresh VM gives SUITE ALL PASS.
- 8: `wp-acf-plugin-builder` and `wp-elementor-builder` copied from your `dump/plugin_20261004/` into Code
  (`srom-produkcja/.claude/skills/`, links in `.claude/skills/`), 6f470d5: read them from `$P` like the others.
- 2: `SROM_SKILLS_DIR` in your session environment is fine; no change in `tlumacz_paths.py`.
- 7: srom-naczelny is MB's to save (the card you proposed).


## K8 — re C5: [West Ouhueri] normalize.py fix done (1113fec); termbase row and quote check not done (06.10.2026 15:52)
- `normalize.py`: in notes, a citation inside a bracket or quote ("(por. [@a, s. 3])") is no longer moved out of it
  (MARK-AFTER-QUOTE now main text only). Regression tests added; normalize 49/49, suite 25/25. 1113fec.
- Termbase row: not done. C5 is not in the repository (Cowork's file is not pushed yet); a Mac session must push
  `cowork-to-code.md`, then a Code session adds the row.
- Single-quote check: lives in srom-tlumacz's `tlumacz-draft_check.py` (only “…” is matched), not in produkcja;
  left for a srom-tlumacz session.

## K9 — re C5: [West Ohueri] `--quotes` finds ‘single’ quotations (done, a414512) (06.10.2026 16:18)
- `tlumacz-draft_check.py`: if a source has no “double” quotation of 4+ words, `quoted_notes()` matches ‘…’ spans of 4+ words
  instead (closing ’ not an apostrophe; ‘twas/‘tis skipped; title case and short glosses still fall below the bar).
- Measured on the West Ohueri source (copy of your `work/westohueri`): before `quotes 3/3`, after `quotes 15/15` (15 notes carry one of
  the 20 spans; 0 missing from your sheet, 0 bad class). Existing articles unchanged: ostendorf 43/43, tittel 34/34, ndiaye and pahulich no sheet.
- Why a style switch and not both kinds at once: matching ‘…’ in double-quote sources added two false positives (ostendorf ‘the rest of the
  world’, tittel a German title in ‘…’). With the switch: none.
- Tests: `--selftest` 8/8 (2 new), `tlumacz-test_handoff.py` 33/33, `--all` clean. The West Ohueri sheet is not in Code's `work/`, so the selftest uses synthetic text.

## K10 — re C6: [general] text-layer repair built into `cover_page.py` (done, 07699c7) (06.10.2026 21:04)
- `srom-quant/scripts/fix_actualtext.py`: your prototype (sha256 a3e32dfc…), moved there from `_handoffs/cowork/`, which no longer
  holds it (one copy; use the skill's). Only change: `main()` split into `repair(pdf)`; on the fixture its output equals the prototype's.
- `cover_page.py <master> <id> <article.pdf>`: (1) repairs the article PDF before the cover goes in; (2) sets /Lang (`language`,
  else `pl`) and ViewerPreferences/DisplayDocTitle when the export lacks them, keeps the export's own (a /Lang that disagrees with the
  CSV's `language` warns, RESULT: CHECK); (3) prints, after saving: `text layer: N accent glyph(s) moved …` and
  `self-check: U+FFFD n · pages n · tagged yes/no · /Lang … · DisplayDocTitle … · DOI in XMP yes/no` (read back from the written file).
- Fixture `vol18_actualtext_3pp.pdf` moved to `srom-produkcja/.claude/skills/srom-produkcja/tests/fixtures/pdf/`. It shows the defect
  (152 U+FFFD, 151 right after an accented letter); after the run 0, pages pixel-identical at 150 dpi. Note: the 3-page cut has no
  MarkInfo/StructTreeRoot (150 MCIDs are still in the streams), so the tests add a minimal tree and check it is kept.
- The ~60 leftovers (show operator not next after the EMC) are documented in `fix_actualtext.py` and counted by the self-check, not hidden;
  none occurs in the fixture, so a test makes them (an operator after each EMC) and checks the count stays 152.
- test_quant 34 → 42; SUITE ALL PASS 25/25. Not run here: the full 72 MB volume (12,005 → ~60 U+FFFD, 40/40 pages identical); a Mac run is
  needed. pikepdf is now in `tools/setup_mac.sh` and `_cloud/setup-cloud.sh` (==10.16.0); your `requirements.txt` needs it too.

## K11 — needs MB: [general] DOI suffixes without look-alike characters (0 o 1 l i)? (06.10.2026 21:04)
- Kind: Decide. Blocks: nothing (vol. 18 can go out as minted).
- Crossref asks for suffixes that are easy to read and type; three of vol. 18's 15 mix `1`, `i` and `l` (`1omckhhp`, `7il5kcel`, `1il9b8ma`).
- (a) **Recommended:** drop 0 o 1 l i from `mint_suffixes.py` for future volumes only. Cost: one line and one test, about 10 min in Code.
- (b) As (a), and re-mint vol. 18 before the website import (still possible, nothing deposited). Cost: (a) plus a re-run on Cowork's
  master CSV and the knowledge-base line; about 20 min, Cowork's CSV replaces Code's copy again.
- (c) Leave as is.
- *Trail:* C6 optional item; `srom-quant/scripts/mint_suffixes.py` ALPHABET.

## K12 — [general] cover page template 2 (MB2) in `cover_page.py` (918fb44 + this commit) (07.10.2026 21:58)
- Layout per `srom-produkcja/SROM_okladka_szablon_MB2.idml`: info block top left (journal · ISSN · Strony · DOI), logo right;
  author line name | ORCID | e-mail (e-mail from `volumes/autorzy.tsv` `kontakt`, by ORCID, else name); "Tłumaczenie:" and
  "Pierwodruk:" (title, source, original DOI) for translations; header block fixed between title top 83.8 and citation bottom
  269.7 pt, gaps stretch ≤ 2× / shrink ≥ ½; abstracts from 283.3 pt, ≤ 218 mm. Footer: "Data publikacji | Data publikacji online |
  Okres redakcji", then © + licence name linked to the CC deed (…/deed.pl). Publisher line and CC BY clause dropped (SYS-6 moot).
  Open Access mark recoloured to ink grey (`assets/cover/open_access.pdf`).
- **New required master CSV columns** `pub_date_print` (YYYY-MM-DD) and `editorial_period` (printed as written, e.g.
  "marzec 2026 – czerwiec 2026"), after `pub_date_online`; `validate_master.py` and `cover_page.py` stop without them. Added
  empty to vol. 18's CSV: **needs MB's values before the 09.10.2026 release** (until then vol. 18 is "NOT deposit-ready").
- Emails added to autorzy.tsv: Fotta, Wesołkin. Proofs: `srom-produkcja/_okladki_v18_v2/`. test_quant 42/42, SUITE 26/26.

## K13 — [general] Your checkup takes over the text checks; Code's checkup no longer re-checks texts (07.10.2026 22:39)
From the root session; MB approved 07.10.2026 (draft checkup 06.10.2026, finding 6). Files: `_handoffs/checkup/COWORK.md`,
`_handoffs/checkup/SKILL.md`, `_handoffs/README.md` § Checkup.
- `checkup/COWORK.md` step 4 (Texts) now also runs, on temp copies: the build without `--draft` (only known `[BRAK …]` gaps
  may fail it), `tlumacz-front_check.py`, the Word copy imported with `docx_in.py` → pair check, and `mutate_keyed.py` on
  each keyed source → `MUTATIONS CAUGHT n/n`. A failure that lies in the tools or the contract, not in the text, comes to
  Code as a C-item. Code's checkup no longer checks texts; it reads your newest review in `workspace/reviews/`.
- Step 5: "Next free" from 100 up (the SYS-9 clause is gone); every K-item headed "needs MB" is in your ledger.
  Step 6: every change you make in Code's folder has its C-item (no `plugin/srom/` any more).
- Nothing to apply in a skill. Your status line in `cowork-to-code.md` is enough.

## K14 — [general] Checkup 07.10.2026: vol. 18 data in one place, MB's desk answers, the ledger, records (07.10.2026 23:44)
From the root session (`_handoffs/review-07.10.2026.md`, F1, F2, F5, F9, F10). MB starts you with "Do K14". In this order:
1. **Vol. 18 data (blocks the 09.10 release).** Your `srom-produkcja/volumes/18/srom_master_v3.csv` and `volumes/autorzy.tsv` are
   behind Code's. Code's hold everything yours do (compared field by field, 07.10.2026 23:3x) plus MB's 07.10 decisions — the licences
   of 13 articles and `pub_date_online` 2026-10-09 (3ec2d51; V18-100/101) — and K12's two columns and the e-mails of Fotta and
   Wesołkin (d337459). Only you have `volumes/18/citations/` and `bib_from_pdf.py`. Ask MB which copy is the master (review § For MB 1):
   - (a) recommended: `cp "$K/srom-produkcja/volumes/18/srom_master_v3.csv" "$W/srom-produkcja/volumes/18/" && cp
     "$K/srom-produkcja/volumes/autorzy.tsv" "$W/srom-produkcja/volumes/"`; keep your `citations/`; a STATUS.md line; the release runs here.
   - (b) copy your `volumes/18/citations/` and `bib_from_pdf.py` into `$K/srom-produkcja/volumes/18/`; a STATUS.md line saying Code's
     CSV is the vol. 18 master; a Code session commits.
   Then MB's two values into all 15 rows (`pub_date_print`, YYYY-MM-DD; `editorial_period`, as printed) and `validate_master.py`:
   0 blocking errors. Before the cover pages: `python3 -c 'import pikepdf'`; if that fails, `pip install pikepdf==10.13.0.post1`
   (the last release for Python 3.10; srom-produkcja is adding it to `requirements.txt`).
2. **MB's answers waiting on the desk** since 06.10.2026 23:07–23:58 (srom-naczelny § The desk, step 1; `meta/sync` 06.10 17:41):
   - V18-100, V18-101: in the CSV after step 1 → out of the ledger, resolved on the desk.
   - V19-2: MB: „Związek Radziecki/radziecki” is the standard, „Związek Sowiecki/sowiecki” accepted. Termbase C-0048 (house form,
     variants, decision log) and the drafts with „sowiecki”: Pahulich 8×, West Ohueri 2×. MB has saved no Word copy (all at their
     export times, no lock files, 07.10 23:30): check again, then change the drafts and re-export the Word copies in place (as for
     T36). If "accepted" means the drafts may stay as they are, ask MB first.
   - V19-3: approved except „uinnienie/uinniać” (MB: "needs to be established": ask what that asks for; C-0042 stays PROVISIONAL);
     „sedentaryzacja” is fine beside „osiedlanie” (C-0049, a variant). The other rows of the six → HOUSE.
   Termbase edits are a small skill change: preflight, a C-item naming the files, a STATUS line (a Code session commits).
3. **Ledger.** Remove once MB confirms in chat: SYS-100 (K12: MB's own template 2 replaced the proposed changes; publisher line and
   CC BY clause dropped) and SYS-102 (C6: translator default MB, `translators_struct` filled; ask about Takács's "adaptacja").
   SYS-101: K12 prints „Okres redakcji” (`editorial_period`) instead of the dates of submission and acceptance; ask MB whether that
   answers it. Enter K11 (Decide; blocks nothing, but vol. 18's suffixes freeze at the website import) and K12's question (blocks
   the vol. 18 release), unless MB answers both in the same session.
4. **Records.** Tick in STATUS.md § For the skills: C5's termbase row C-0050 (20f4f26, 06.10 16:09; `tlumacz-check_tb.py` 07.10
   23:25: 40 rows, 0 problems); C6's small changes (e0a51a2), the CSV replacement (f109090), the text-layer repair (07699c7, K10);
   the model-and-effort rule (in Code's root CLAUDE.md since 04.10). Correct "9 PROVISIONAL" (10 with C-0050) and the online-PDF
   procedure (`fix_actualtext.py` runs inside `cover_page.py` since K10; the `_handoffs/cowork/` prototype is gone). From Code,
   unannounced until now: 39302d3 (06.10 22:01: the knowledge base's Scope line, srom-zizek's link to it, `tests/test_kb.py`: SUITE
   ALL PASS 26/26) and ef72369 (07.10 01:48: depositor e-mail michalbartosz@studiaromologica.pl in `generate_crossref_xml.py`;
   made by a Mac Code session, despite "cowork:" in its message). Correction to K8: its time is 15:51 (commit adc86d1), its text
   [West Ohueri].
5. **Cloud sessions are discontinued** (MB 07.10.2026; root CLAUDE.md § Cloud sessions); your start step 5 (Code's folder current
   against GitHub) still holds. The desk's hint under each answer box says "a SROM session reads it on 'sync the desk'": when you
   next publish the desk page, say that Cowork reads it at the start of every session (MB looked for his answers in Code).
6. Answer K8–K14 in `cowork-to-code.md` (C7), then run your checkup (`checkup/COWORK.md`; `workspace/reviews/` does not exist yet)
   and give its verdict lines.

## K15 — [general] Re C7; review 07.10.2026 For srom-produkcja 1–2: INJECT normalise step, pikepdf pin; re-run `setup.sh` (08.10.2026 00:52)

Status of C7 (srom-produkcja, srom-quant):
- **K11 (a)** — done, a150f34: `mint_suffixes.py` mints from `[a-z0-9]` without `0 o 1 l i` (31 characters); vol. 18's 15 suffixes
  stay (the validators still accept `[a-z0-9]{8}`). srom-quant SKILL.md says so; the knowledge base does not name the alphabet.
  test_quant 44/44.
- **`validate_master.py` on ADAPTACJA rows** — done, a150f34: `translators_struct` on an `ADAPTACJA` row no longer warns (one
  condition, with a test).
- **V18-103** — noted; nothing built until MB answers.
- **K14 (a)** — noted: Code's `volumes/18/` is a reference copy, never edited (srom-produkcja `CLAUDE.md`, 5ffbbc9); the cleanup
  task (review 07.10.2026, For MB 5) retires or refreshes it.
- **`dump/crossref_test/`** — not Cowork's: a Mac Code session's leftover of 07.10 (review F12), for the cleanup task.
- **The termbase commit** (`tlumacz-tb.tsv`, `tlumacz-decisions.md`) — still uncommitted: it is srom-tlumacz's folder, and the
  review gives it to the srom-tlumacz session (its checks, then the commit). MB's next step 4 runs that session.

From the review:
1. **INJECT normalises without editing `pl/`** (280bf2a). After `take_back.py`, `normalize.py` writes the copy into
   `work/<id>/build/<id>_pl.md` (+ `_norm.md`), and `build.py` builds that file; `pl/` and its `SHA256SUMS` stay as delivered.
   `take_back.py` prints both commands, quoted. A normaliser flag goes to the notes sheet and the Word master, with a new
   delivery. `handoff.md` § Back item 4 and its command block, `stages.md` § 3, SKILL.md scenario C. HANDOFF CONTRACT 33/33.
2. **pikepdf pinned for your VM** (d7ad719): `requirements.txt` has `pikepdf==10.16.0` (Python ≥ 3.11) and
   `pikepdf==10.13.0.post1` (< 3.11); pip resolves both. **Please re-run `sh srom-produkcja/setup.sh`, then your preflight**, and
   give the suite line (SUITE ALL PASS 26/26 expected; `test_quant` 44/44).

## K16 — [general] Re C8; the one folder `SROM/Redakcja`: your folder moved, Code keeps no copies, MB's four folders (08.10.2026 02:17)

C8 — read; nothing to do (suite 26/26 in your VM, normalise step noted).

From the root session (review 07.10.2026, For MB 5; MB chose: now, a new `SROM/Redakcja`, English names). Commit 2af8751.
1. **Where things are.** MB starts you on `SROM/Redakcja` (`$HOME/mnt/Redakcja`): no "+". Inside: `workspace/` (your folder,
   moved from `SROM/Cowork/srom-cowork/workspace/`; `SROM/Cowork/` is gone), `SROM edit and trans/` (Code's repository, moved
   from `SROM/CODE/SROM/`) and MB's `1. Inbox/`, `2. Word` (a Finder Smart Folder of every `*_robocza.docx` in `workspace/`),
   `3. PDF online/` (+ `ready/`), `4. Archive/`. srom-env: `R="$HOME/mnt/Redakcja"; K="$R/SROM edit and trans"; P="$K/.claude/skills";
   W="$R/workspace"`. MB uploads a new srom-naczelny card with this block (it also finds the folder if renamed); until he
   has, a session that loads the old card takes the block from `workspace/CLAUDE.md` § The one folder.
2. **Changed in your files, from the Mac** (nothing to apply; check and say if anything is wrong): `workspace/CLAUDE.md`
   (§ The one folder with the rules for MB's folders; start steps 2–5 use `$K`; files; changing a skill), `desk/desk_sync.py`
   (paths for the one folder; files bar: `1. Inbox`, `2. Word`, `3. PDF online` in place of `dump`; run on a copy: 58
   decisions, 0 unresolved, every path exists on the Mac), `srom-produkcja/work/ndiaye/key.py` (finds the skills from its
   own place), `STATUS.md` (two lines 08.10.2026 02:07: § Known limits, § Volume data). Moved to `4. Archive/`: the bundle's
   README, MANIFEST, `srom.plugin`, `local/` (same as Code's `srom-produkcja/tools/install_scripts.sh`), `Claude outputs/`;
   your old `dump/` (as `Cowork dump/`, with `vol18_cowork_20261008/` and the Crossref PDFs); `skill-changes/` and
   `for-code_model-effort-rule.md` (as `Cowork skill-changes (applied)/`). Nothing deleted.
3. **Online PDFs** from now on: MB exports into `3. PDF online/`; `cover_page.py … --out "$R/3. PDF online/ready"`; the vol. 18
   references re-run reads `ready/` (`bib_from_pdf.py` takes PDFs named as `pdf_file`, cover allowed). Replaces
   `volumes/18/export/` → `volumes/18/online/`. Inbox: copy what is needed into place, say it in STATUS.md, never move or
   delete there. `checkup/COWORK.md` has a step 7 for both folders.
4. **Code side.** Code's copies of the texts and volume data are gone (git history keeps them): your workspace is the only
   copy. srom-tlumacz's checks run from Code now read your `workspace/srom-tlumacz/` (`tlumacz_paths.py` falls back to it;
   read only, drafts are copied to a temp folder). `test_jsx.py`'s fidelity check now has its two vol. 18 IDMLs in the skill
   (`tests/fixtures/idml/`), so it runs in your VM too (it was skipped there: `dump/` missing). Retired: `_cloud/`,
   `_migracja/`, the rendered views (Code links the desk for MB's questions), `_handoffs/cowork/` (no longer named anywhere).
5. **Please, in your next session:** the new srom-env block, `setup.sh`, the preflight (SUITE ALL PASS 26/26 expected), then
   **sync the desk** (the files bar's links still name `Cowork/srom-cowork` and `CODE/SROM` until you do), and answer in C9.

## K17 — [general] The sealed copy in `pl/` is read-only (08.10.2026 15:15)
MB 08.10.2026: `take_back.py` now makes the copies in `work/<id>/pl/` and `SHA256SUMS` read-only, so Word opens the
sealed `<id>_robocza.docx` locked (it also shows in `2. Word`); a new delivery replaces them as before. Commit be3aa5e;
`handoff.md` § Back says so; test_takeback 26/26, SUITE ALL PASS 26/26, HANDOFF CONTRACT 33/33. Ostendorf's existing `pl/`
(a test run) is left as it is (MB). Nothing to apply; give the suite line in your next C-item.

## K18 — re C11 [general] srom-cowork leftover fixed (09.10.2026 18:42)
The "nested" `srom-produkcja/.claude/skills/` is not a stale copy: it is the live location (`~/.claude/skills/srom-*` link into it), so I did not remove it.
Fixed the one line instead: `srom-zizek/SKILL.md` l. 53 now says `/mnt/user-data/uploads/…` (no `srom-cowork`). No other `srom-cowork` in srom-produkcja or srom-tlumacz.
Doc-only change, tests not affected. Biurko noted, nothing to do.

## K19 — re C10 [general] editorial_period change committed; suite line (09.10.2026 18:52)
C10's four srom-quant files committed (73363bc). Run here: QUANT ALL PASS 45/45, SUITE ALL PASS 26/26.

## K20 — re C14 [Steiner] front-check `[BRAK …]` fix committed with two controls (13.10.2026 19:09)
`tlumacz-front_check.py` diff reviewed (one function, precedence of the `and/or` line is as intended) and committed. Added two controls to
`tlumacz-test_handoff.py`: `[BRAK …]` after Keywords → drafted keywords accepted; real keywords after Keywords → still „jak w oryginale”.
Run here: HANDOFF CONTRACT 35/35 (was 33), `tlumacz-check_tb.py --selftest` 9/9, `tlumacz-draft_check.py --selftest` 8/8. C12, C13: no action (C12 parked; C13 not started).

## K21 — [general] cover_page.py: output PDF no longer 1.2 MB larger than the article (13.10.2026 22:27)
MB noticed that the cover added over 1 MB per article. Cause: PyMuPDF embedded a full copy of IBM Plex Sans for every text block of the cover (12 copies, 1.2 MB), and the final save did not merge identical objects. The cover page itself is 0.26 MB alone.
Change in `srom-quant/scripts/cover_page.py`: the cover's two fonts are subset (cover only, never the article), the final save merges identical objects and uses object streams (`garbage=4`, `use_objstms`), and the run prints a `size:` line. Vol. 18 no. 5: 7.39 → **5.91 MB** (the InDesign export alone is 5.99 MB).
Checked against the old output, nothing differs: all 31 pages render pixel-identical; the article's page contents, ToUnicode maps (the accent/ActualText repair) and font programs are byte-identical; same text and character positions in MuPDF and poppler (pdftotext output identical); structure tree (525 elements), Info, XMP, page labels, bookmarks, 33 links. Test added (Plex embedded once per style, as a subset): QUANT ALL PASS 46/46, SUITE ALL PASS 26/26.
**Action for you:** none needed for new runs. Files already in `3. PDF online/ready/` keep the old size until `cover_page.py` is run on them again (vol. 18 no. 5 is 7.2 MB there). Cowork's VM needs PyMuPDF with `Document.subset_fonts` (1.28 here); without it the run still works and prints `note: cover fonts not subset`, the file is then about 0.2 MB larger.

## K22 — re C15 [general] Kanon v1.17 and print-date test committed; C15 items 3 and 4 open (14.10.2026 04:35)
Status of C15: (1) `print_date_xml()` and the knowledge base committed as df28b66 (Cowork's files); test added (row with `pub_date_print` gives print + online, row without only online); (2) Kanon v1.17 done: § 13.2 CC BY 4.0, § 17 row, RULES.md, SKILL.md, version comments, expected report. Commit e5e3d91. Suite: SUITE ALL PASS 26/26 (KANON 20/20, QUANT 47/47, E2E 85/85). Addendum (`check_deposit.py` into srom-quant) and `fix_actualtext.py`: open, not started.

## K23 — re C15 [general] check_deposit.py in srom-quant (step 8a); fix_actualtext repair 3: doubled accents 576 → 0 (14.10.2026 15:33)
Commit cbcff0f. Suite: SUITE ALL PASS 26/26 (QUANT 54/54).
- **check_deposit.py** now in `srom-quant/scripts/`, step 8a of the deposit in SKILL.md (`DEPOSIT CHECK OK n/n` is a precondition for the upload); fixture test (no-ORCID contributor, damaged reference, wrong page). **Cowork: drop your copy** `workspace/srom-produkcja/volumes/check_deposit.py`. Not run here on real vol. 18 data nor with `--site`.
- **fix_actualtext.py repair 3.** Cause was not "span leftovers": a precomposed letter (ć) is one glyph followed in the same text operator by a zero-width accent glyph with no ActualText; repair 2 mapped it to U+0301, giving "ć́". Fix: wrap such an accent glyph in an empty `/Span <</ActualText ()>> BDC…EMC` (text operator split, positions unchanged). On the 15 vol. 18 exports in `3. PDF online/`: doubled accents 576 → 0, U+FFFD not above the old output, pages pixel-identical at 100 dpi. `cover_page.py` report line now ends "N doubled accent(s) wrapped". Checked with MuPDF and pdftotext, not Acrobat/PDFium. No PDFs touched.
**Action for you (Cowork):** re-run `cover_page.py` on the 15 vol. 18 files in `3. PDF online/` into `ready/`, confirm the report shows doubled accents wrapped and `pdftotext` finds 0 doubled accents, then MB re-uploads the 15 files under the same names. Run with: Sonnet · low effort — one specified rerun of a finished script on 15 files.

## K24 — re C16–C20 [general] back catalogue reviewed and committed; mu-plugin v2.5 replaces v2.4 (20.10.2026 01:38)
- C16, C18: seen, nothing to apply (C18's README committed in ed5e014). C17: committed in cc68c2f; its test added now (54f464b:
  "Vgl. ebd., S. 40" accepted after the previous note's work, rejected for another; fails on the pre-C17 check.py). C17's Kanon
  wording („zatwierdzona przez kolegium 14.10.2026”) waits for the next Kanon version with a rule change; C17 requests 1–2 (sigla,
  two page ranges) not started.
- C19, C20: your files reviewed and committed (26cfc4c), with fixes:
  - **mu-plugin v2.5** (39 KB, `srom-quant/assets/srom-scholarly.php`): v2.3's fatal catcher and `?srom_off=1` kill switch removed;
    an article without DOI no longer prints `dc.identifier "doi:"` and a bare `https://doi.org/` in its JSON-LD; the srom-no-* body
    classes come from the page itself (on an archive they were taken from the first post and hid rows on every item);
    `[srom_volume_license]` gives „według artykułu (CC BY-NC 4.0, wszelkie prawa zastrzeżone)” for vol. 17 (v2.4 said CC BY-NC 4.0,
    wrong for Chiriac); `[srom_flipbook]` cannot recurse. New `test_muplugin.py` runs it under PHP with WordPress stubbed
    (MUPLUGIN ALL PASS 25/25; your VM has no php: the line there is `MUPLUGIN SKIP`, which the suite accepts).
  - **rip_volume.py:** ORCIDs from `autorzy.tsv` by whole words (the substring match gave „Ann” Anna Piotrowska's ORCID, 89 such
    partial-name hits on the register); a re-run prints `cells changed against the previous srom_master_v3.csv: n: …`, so a hand
    edit in the CSV is seen before it is lost; any CSV column given as an article key in volume.json wins (put corrections there).
    Vol. 17 re-run: byte-identical to your CSV.
  - SKILL.md manifest and master_schema.md (#42 `copyright_holder`, `license` NONE, year-only print date) done.
  - Vol. 17 deposit dry run here (scratch copy): `generate_crossref_xml.py` → `check_deposit.py`: DEPOSIT CHECK OK 10/10 (no references yet).
- Ledger: **GEN-122 now uploads v2.5, not v2.4** (see K25). For GEN-116 (housekeeping, no decision): `wp-content/backupwordpress-…-backups/`
  holds 2.3 GB of June–July backups of an inactive plugin (protected: 403); delete them in the file manager when convenient.
- Suite: SUITE ALL PASS 28/28 (BACKCAT 28/28, QUANT 54/54, MUPLUGIN 25/25, CHECK 82/82). Backup: BACKUP OK srom-20261020-0134.

## K25 — needs MB: [general] site plugin v2.5 and the order of vol. 17's import and deposit (20.10.2026 01:38)
1. **GEN-122 changed: upload v2.5 instead of v2.4, delete one stray file, switch on PHP's error log.** Kind: Do. Blocks: GEN-121, GEN-123.
   In the host's file manager: (1) replace `wp-content/mu-plugins/srom-scholarly.php` with 🔴 `srom-quant/assets/srom-scholarly.php`
   (v2.5); (2) delete `wp-content/mu-plugins/srom-loops.php.bak` (the retired loop plugin: not loaded, but anyone can download it);
   (3) in `wp-config.php`, change the existing `define( 'WP_DEBUG', false );` line (or, if none, add above "That's all, stop editing")
   to `define('WP_DEBUG', true); define('WP_DEBUG_LOG', true); define('WP_DEBUG_DISPLAY', false);` (each once) for about a week: PHP then logs any fatal to `wp-content/debug.log`, which the host already
   refuses to serve (403, checked 20.10.2026). Say "done": a session checks a vol. 18 article, a volume page and `debug.log`, and
   later tells you when to set WP_DEBUG back to false. Why the plugin's own fatal logger went: its log would have been a public URL,
   and `?srom_off=1` let any visitor switch off the grids' scoping.
   *Trail:* audit of 20.10.2026 (fatal catcher, kill switch); review 20.10.2026; commit 26cfc4c.
2. **Vol. 17: register the DOIs on the day of the import, or import without them?** Kind: Decide. Blocks: GEN-123.
   Vol. 17's CSV and covers carry DOIs; importing it (GEN-123) puts 10 DOI links on the site that lead nowhere until vol. 17 is deposited,
   which BACK-CATALOGUE.md itself says to avoid ("import back volumes with `doi` empty unless deposited in the same run").
   - (a) **Recommended:** deposit vol. 18 first (V18-107, ready since 14.10), then import vol. 17 and deposit it the same day without
     references (Crossref accepts that; a re-deposit adds them when the reference step exists for back volumes). Cost: one more
     upload for you; the XML is a two-minute job for a session.
   - (b) Import vol. 17 now with `doi` empty (pages at /articles/<suffix>/, 301 to the DOI address after the deposit, already built in);
     the covers keep their DOI line, dead until the deposit. Cost: a session makes the import copy of the CSV.
   - (c) Import as is and accept dead DOI links for a while.
   *Trail:* GEN-123, GEN-118, BACK-CATALOGUE.md § The pipeline; mu-plugin `post_type_link` fallback.
Run with: Sonnet · medium effort — the post-upload checks and the vol. 17 deposit XML follow written procedures.

## K26 — re K25 [general] MB's answers; GEN-122 checked on the live site (20.10.2026 21:10)
- **K25 item 1 (GEN-122): MB did it (20.10.2026 21:10, "done").** Checked: `mu-plugins/` holds `srom-scholarly.php` 39,530 bytes = the repository's v2.5 (header `Version: 2.5`) and `elementor-safe-mode.php`; `srom-loops.php.bak` is gone (404). A vol. 18 article (10.68100/n61tj1yi) and `/tom/18-2025/` answer 200; the article carries `citation_doi`, `dc.identifier`, the `srom-backcat` style, and no `srom-no-*` body class; the volume page none either. `wp-content/debug.log` does not exist yet (no PHP error since WP_DEBUG_LOG was switched on, or the setting is not live: look again in a few days; a session can read it with the site connector). **Action for you:** ledger GEN-122 → resolved. GEN-121 (template rows) is unblocked; a week from now ask MB to set WP_DEBUG back to false.
- **K25 item 2: MB chose (a), later:** vol. 18 deposit first (V18-107); vol. 17 is imported and deposited **some days after** the vol. 18 upload, not the same day. **Action for you:** change GEN-123's wording (import waits for the vol. 18 deposit report plus a few days; import and deposit of vol. 17 on one day). The vol. 17 covers carry the online date 2026-10-20: if the import is later than that, the dates change and the covers are rebuilt first (`cover_page.py`, two minutes), as GEN-123 already says. Deposit XML for vol. 17 without references: scratch run `DEPOSIT CHECK OK 10/10`; rebuild it on the import day.

## K27 — [general] MB dropped the model/effort lines; the root now applies checkups itself (20.10.2026 21:31)
- **"Run with:" dropped (MB, 20.10.2026).** No more model or effort estimates in instructions to MB, unless he asks: they had no
  feedback to calibrate them and were given even for steps MB does by hand. Root CLAUDE.md § "No model or effort advice" replaces the
  hard rule of 04.10.2026. **Action for you:** remove your copy, `workspace/CLAUDE.md` § "Tasks you hand to MB: always say which model
  and effort" (line 68 on), and any other place in your files that asks for the line; stop writing it in C-items. Old entries stay.
- **Checkup applied by the root (MB, 20.10.2026).** After a checkup the root session applies every module item that needs no MB
  decision and writes the module's status lines itself; a module session is needed only for a Kanon rule change, translation
  judgment, or a module with a session running. MB no longer opens module sessions to say "apply checkup". Root CLAUDE.md
  § Checkup, `_handoffs/README.md` rule 1 (one exception: the root's `Status of review` sections), `checkup/SKILL.md` § Apply.
  Nothing for you to change unless `checkup/COWORK.md` or your files tell MB to apply a Code review in module sessions.
