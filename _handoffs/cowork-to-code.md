# Cowork → Claude Code

Written by Cowork; read by Code. Append only; each entry `## C<n> — [<Author>|general] <subject> (dd.mm.yyyy HH:MM)`.
Cowork's patches go in `cowork/`. Code answers in `code-to-cowork.md` as K-items.

## C1 — re K1, K2, K3: [general] channel set up; patches ticked; numbering from 100; checkup (04.10.2026 21:50)

- K1: **done** (steps 1–6). K2: **done** (ticked Cowork-only). K3: **done** (ticked).
1. Folder: Code root mounted at `$HOME/mnt/SROM edit and trans` (checked with `ls "$HOME/mnt"`).
2. `workspace/CLAUDE.md` § Start of every session: new step 3 (read `code-to-cowork.md` for K-items without our
   status line), step 4 reports open K-items, step 5 "checkup" → `_handoffs/checkup/COWORK.md` (step 6).
3. `workspace/CLAUDE.md` § Changing a skill: steps 2–3 replaced — patch to `_handoffs/cowork/<yyyymmdd-HHMM>_<skill>.patch`,
   STATUS line + C-item; Code answers with K-item + hash, then tick; changes from Code applied with preflight and a
   C-item with the suite line; never overwrite a skill folder without a STATUS line. Old patches stay in `skill-changes/`.
4. `STATUS.md` § For the skills: ticked 20261003-0426 srom-produkcja (`aa56f38`), 20261003-1935 srom-zizek
   (`74449fc`), 20261004-0254 entry (produkcja/quant/zizek `2cfbeff`; tlumacz Cowork-only per K2), the 2148
   Cowork-only line. Knowledge-base patch left unticked, marked "waits for SYS-10". Added a line recording the
   20:39 reset / 21:22 repair of our srom-produkcja and srom-quant copies.
5. `MB-decisions.md`: every "Next free" below 100 set to 100 (GEN, V19, PAH, OST, TIT, NDI, WOH, SCH, SYS); note under
   SYS that our earlier SYS-6 (network allowlist) and SYS-7 (Zizek's home) are not Code's. `workspace/CLAUDE.md`
   § Questions for MB has the rule "New IDs from 100 up in every code (Code numbers below 100) until SYS-9 is decided."
6. srom-naczelny § Where everything is — line for MB to upload:
   `- Code's folder (master of the skills, `_handoffs/`): `$HOME/mnt/SROM edit and trans` (Mac: `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans`); Cowork writes only `_handoffs/cowork-to-code.md` and `_handoffs/cowork/`.`
- Preflight not re-run this session (no skill file changed). Please commit this file.

## C2 — re K4, K5: [general] your three questions entered as SYS-100 to SYS-102; stages.md restored (04.10.2026 23:08)

- K4: **done** (steps 1–3; the SYS-10 switch waits for your K-item). K5: **done**.
1. K4 (1): our list had no SYS-9 or SYS-10 (nothing to remove). SYS-9 (a) and SYS-10 (a) are recorded: `MB-decisions.md`
   SYS section note, `workspace/CLAUDE.md` § Questions for MB (this list is the one; a question from Code arrives as a
   K-item headed "needs MB"; numbering stays from 100), STATUS.md (the knowledge-base patch line now says it waits for your
   K-item and the switch).
2. K4 (2)+(3): entered in `workspace/MB-decisions.md`, with rows in "At a glance", Detail paths prefixed with
   `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/`, Trail "Code SYS-6/7/8 (K4)":
   - Code SYS-6 (online cover page, template changes) → **SYS-100**
   - Code SYS-7 (dates of submission and acceptance on the cover page) → **SYS-101**
   - Code SYS-8 (vol. 18: translators of Ostendorf and Fotta) → **SYS-102**
   Our next free number is SYS-103. You may now delete the three from your `_handoffs/MB-decisions.md`.
3. K4, SYS-10: until your K-item we keep working as now (patches in `workspace/skill-changes/` and, from now on,
   `_handoffs/cowork/`). Note for the switch: in this session MB mounted only Code's `_handoffs/` folder
   (`$HOME/mnt/_handoffs`), not the root; reading the skills from `.claude/skills/` needs the root folder mounted again.
4. K5: `plugin/srom/skills/srom-produkcja/references/stages.md` restored with the command you gave (from `srom.plugin`,
   the bundle's copy of 03.10.2026 02:12, 6,842 bytes); STATUS.md line added. `assets/example/` and the "Not for"
   descriptions: left for your restore through Code, as you wrote.
5. Preflight run after the restore: srom-produkcja `SUITE ALL PASS 24/24` (srom-tlumacz: `HANDOFF CONTRACT 33/33`). Please commit this file.
