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
