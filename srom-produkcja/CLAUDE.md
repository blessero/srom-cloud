# SROM tools — project instructions

Repository of the production tools for *Studia Romologica* (Polish-language annual, Romani studies,
ISSN 1689-4758); formerly srom-typeset (renamed 30.09.2026, MB). Six skills in `.claude/skills/`:
- **srom-kanon** — the house rules (normative) and their linter.
- **srom-produkcja** — manuscript → SROM-MD → DOCX → InDesign; citations via CSL; checks; Word working copies.
- **srom-quant** — metadata, DOI/Crossref, website (formerly srom-scholarly-curator; no session of its own, used here).
- **srom-zizek** — selection and critical review of papers for a volume (the stage before RIP).
- **wp-acf-plugin-builder**, **wp-elementor-builder** — the website's WordPress plugins and Elementor templates.

Code is the workshop: it builds and tests the skills. The texts, the volume data and MB's questions are Cowork's (root
CLAUDE.md § Cowork). Volume data: Cowork's `workspace/srom-produkcja/volumes/` is the master (vol. 18: MB 08.10.2026,
K14 (a)); this repository's `volumes/` (master CSV `volumes/<vol>/srom_master_v3.csv`, authors register
`volumes/autorzy.tsv`) is a reference copy, never edited, used for tests and scratch runs. Stage names (root CLAUDE.md):
RIP and INJECT are this module's, TRANS is srom-tlumacz's.

The EN→PL translation module **srom-tlumacz** is a separate folder (`../srom-tlumacz/`, its own session; its skill
`srom-tlumacz` since 03.10.2026, E20); it talks to srom-produkcja only through
`.claude/skills/srom-produkcja/references/handoff.md`.

State, open decisions and the work queue: `docs/HANDOVER-*.md` — read before starting.

## Environment (editor's Mac)
- `.claude/skills/` in this repo is the only working copy; `~/.claude/skills/srom-*` are symlinks to it
  (`tools/setup_mac.sh`). claude.ai gets copies via `sh tools/package_skills.sh` → `dist/*.skill` (upload by hand).
- Python: venv `~/.venvs/srom/bin/python` (3.13 + python-docx, lxml, PyMuPDF, pikepdf); `python3` on PATH is miniconda 3.13 with
  the packages, `/usr/bin/python3` is 3.9 without them; `run_all.py` switches to the venv itself, other scripts are called with the venv.
- pandoc 3.8.3, node + acorn (`~/.venvs/srom/node`), InDesign 2026, LibreOffice (Homebrew cask, 03.10.2026: `test_pdf.py` now runs
  its Word-made-PDF part too).

## Working rules
- The editor (Michał) writes tersely and wants conclusions first, honest critique, errors and limits flagged.
  English for work talk; Polish, in an elevated editorial register, for anything written for the journal.
- Never invent bibliographic data; missing data stays missing and is flagged (kanon §0).
- Every change: run `python3 .claude/skills/srom-produkcja/tests/run_all.py` → `SUITE ALL PASS n/n` before
  saying done; add a test for every new behaviour; commit after a green suite.
- Contract changes between skills are made in `handoff.md` first, then in both skills, with tests on both sides.
- Rules live in srom-kanon only; srom-produkcja implements them and cites them, never restates them.
- Kanon versions: a rule change gets its § 17 entry in a **new** version row (header, RULES.md, srom-kanon SKILL.md;
  `test_kanon.py` checks they agree) once the current version has been announced to srom-tlumacz; never append
  supplements to an announced version (v1.7 carried three, review 29.09.2026). Announce each new version in a T-item.
- InDesign scripts: ES3 (ExtendScript), report-only unless the editor asks otherwise; run on copies.
- Substantial tasks: use the unlazy discipline (gates with runnable checks in `GATES.md`). A gate's CHECK tests what
  the leaf produced here (a file, a test, its own commit found by message), not files meant to change later
  (`../_handoffs/MB-decisions.md`, handoff files, the suite's n/n): those drift, and the closed gate stops holding.
- Several sessions (one per article) share this working tree. Commit only your own files, by path
  (`git commit <paths>`; never `git add -A`, `commit -a` or `git stash`); never revert, reformat or commit
  another session's uncommitted changes. If the suite fails in code you did not touch, check `git status`/`git diff`
  for another session's work in progress before fixing anything; say so to MB rather than "fixing" it.
- IDs in shared files (T<n> in `../_handoffs/produkcja-to-tlumacz.md`, K<n> in `../_handoffs/code-to-cowork.md`; a question
  for MB is a K-item "needs MB"; Cowork enters it in its ledger with an ID such as PAH-11): re-read the file's
  tail for the next free ID immediately before appending, and commit `_handoffs` at once. Cite the other side's
  items with their [Author] tag ("E18 [Pahulich]"), since parallel sessions have reused IDs. Commit a shared file
  (GATES.md, MB-decisions.md) by path only when every change in it is yours.
