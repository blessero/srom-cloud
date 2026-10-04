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
