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
