# SROM tools — project instructions

Repository of the production tools for *Studia Romologica* (Polish-language annual, Romani studies,
ISSN 1689-4758). Three skills in `.claude/skills/`:
- **srom-kanon** — the house rules (normative) and their linter.
- **srom-typeset** — manuscript → SROM-MD → DOCX → InDesign; citations via CSL; checks; Word working copies.
- **srom-tlumacz** — EN→PL translation module (judgement layer); talks to srom-typeset only through
  `srom-typeset/references/handoff.md`.

State, open decisions and the work queue: `docs/HANDOVER-*.md` — read before starting.

## Environment (editor's Mac)
- `.claude/skills/` in this repo is the only working copy; `~/.claude/skills/srom-*` are symlinks to it
  (`tools/setup_mac.sh`). claude.ai gets copies via `sh tools/package_skills.sh` → `dist/*.skill` (upload by hand).
- Python: venv `~/.venvs/srom/bin/python` (3.13 + python-docx, lxml, PyMuPDF); system `python3` is 3.9 and too
  old — `run_all.py` switches to the venv itself, other scripts must be called with the venv.
- pandoc 3.8.3, node + acorn (`~/.venvs/srom/node`), InDesign 2026. No LibreOffice → `test_pdf.py` reports SKIP.

## Working rules
- The editor (Michał) writes tersely and wants conclusions first, honest critique, errors and limits flagged.
  English for work talk; Polish, in an elevated editorial register, for anything written for the journal.
- Never invent bibliographic data; missing data stays missing and is flagged (kanon §0).
- Every change: run `python3 .claude/skills/srom-typeset/tests/run_all.py` → `SUITE ALL PASS n/n` before
  saying done; add a test for every new behaviour; commit after a green suite.
- Contract changes between skills are made in `handoff.md` first, then in both skills, with tests on both sides.
- Rules live in srom-kanon only; srom-typeset implements them and cites them, never restates them.
- InDesign scripts: ES3 (ExtendScript), report-only unless the editor asks otherwise; run on copies.
- Substantial tasks: use the unlazy discipline (gates with runnable checks in `GATES.md`).
