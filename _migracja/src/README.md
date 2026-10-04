# SROM for Cowork — the bundle

Everything Cowork needs to run *Studia Romologica* production (RIP → TRANS → INJECT) and carry on with the work in
progress. Built 03.10.2026 from the Claude Code system, which stays as it is. Contents and roles: `MANIFEST.md`.

```
srom-cowork/
  plugin/srom/         the plugin: six skills, SROM_knowledge_base.md, setup.sh, requirements.txt
  srom.plugin          the same plugin as one file, for upload
  workspace/           the folder Cowork works in: CLAUDE.md, STATUS.md, MB-decisions.md, both modules' texts
  local/               Mac-only helper for InDesign (run by you in Terminal, not by Cowork)
  README.md, MANIFEST.md
```

## 1. Install

Two ways. **Recommended: let a Cowork session merge it** into the journal's main (managing) skill there:
1. Unzip the bundle somewhere it can stay (the InDesign helper in `local/` links to files inside it).
2. In Cowork, select the bundle folder and say: "Read README.md and MANIFEST.md, then merge this into our SROM
   skills. Keep the rules of § 1a." Review its plan before it changes anything.

**1a. What the merge must keep** (or the tools break, or Cowork and Code drift apart):
- Each skill's internal folders and file names unchanged (`scripts/ references/ tests/ config/ csl/ lua/ indesign/
  assets/`): scripts find each other by these paths, and changes travel to Code as patches with these paths
  (workspace `CLAUDE.md` § Changing a skill).
- The four SROM skills stay separate skills (srom-kanon, srom-produkcja, srom-tlumacz, srom-quant), with
  `SROM_knowledge_base.md` two folders above them (`../../`). The main skill can sit above them and route to them;
  overlapping text belongs in one place only (journal facts: the knowledge base; stages: srom-produkcja
  `references/stages.md`; house rules: srom-kanon).
- After the merge, the two preflights green (§ 2), and `workspace/` used as the working folder, its layout unchanged.
- Report every change it made to a skill's files as a patch (§ Changing a skill), so Code can take it over.

**Plain install** (no main skill): upload `srom.plugin` in the desktop app, then start a Cowork task with
`workspace/` selected. Cowork should read `workspace/CLAUDE.md`; if it does not, paste it into the task instructions.

## 2. Environment

The tools need Python ≥ 3.10 with python-docx, lxml and PyMuPDF (pinned in `plugin/srom/requirements.txt`) and pandoc
≥ 3.1 (tested with 3.8.3). Once per new environment, ask Cowork to run `sh setup.sh` at the plugin's root: it installs
the Python packages, checks pandoc and downloads 3.8.3 into `~/.local/bin` if it is missing. Node with the npm
package acorn is optional (only the ES3 syntax test of the InDesign scripts).

Then the two preflights, which every session runs anyway (workspace `CLAUDE.md`):
- srom-produkcja: `python3 skills/srom-produkcja/tests/run_all.py` → `SUITE ALL PASS 23/23`
- srom-tlumacz: the termbase checks and `tlumacz-test_handoff.py` → `HANDOFF CONTRACT 33/33`

Both were green in a clean Linux-like run (Python 3.10, empty home folder, the bundle at a path with spaces), from
the zip itself.

## 3. Local apps (your Mac)

Stage 4, the InDesign layout, stays on your Mac: Cowork builds the DOCX and the `.jsx` scripts into
`workspace/srom-produkcja/work/<id>/build/`; you place the DOCX in the template and run the scripts. To get the
scripts into InDesign's Scripts Panel, in Terminal:

```
sh local/install_scripts.sh                                   # the general scripts, once
sh local/install_scripts.sh workspace/srom-produkcja/work/<id>/build   # one article's scripts
```

The template is `plugin/srom/skills/srom-produkcja/indesign/SROM_szablon_v3.idml` (save it as .indt); the import
preset and the order of the scripts: `skills/srom-produkcja/references/indesign.md` and `references/stages.md` § 4.
Word: you edit the `<id>_robocza.docx` copies as before; they live in `workspace/`.

## 4. First session

Say: "Read STATUS.md and MB-decisions.md, run the preflights, tell me where things stand." Expect: both preflights
green; four translations waiting for your Word edit (Ndiaye, Ostendorf, Pahulich, Tittel; Tittel's delivery waits
for TIT-1); West Ohueri waiting for WOH-1. Your next task, the first Crossref deposit (vol. 18), starts from
srom-quant and `srom-produkcja/volumes/18/srom_master_v3.csv`. The questions to settle before editing any Word copy:
PAH-2, TIT-2, TIT-7, V19-1 (`STATUS.md`, top).

## 5. What changed from Claude Code

- **One session for all stages.** The two module sessions talked through `_handoffs/` (T- and E-items). Gone: the
  sha256 of what goes from RIP to TRANS and back is now a line in the hand-off log at the end of `STATUS.md`
  (format: srom-produkcja `references/stages.md`, the one stage-gate spec). The last items were read and carried into
  `STATUS.md`; none was left without an answer.
- **State in two files.** `STATUS.md` replaces the two module handovers and the plan status logs;
  `MB-decisions.md` is the same ledger, with three Code paths rewritten and SYS-1 restated. `workspace/CLAUDE.md` replaces the root and module CLAUDE.md files.
- **Journal facts in one file**, `plugin/srom/SROM_knowledge_base.md` (merged from the July knowledge base, the
  quant skill and the module files, confirmed by you 03.10.2026); the skills point to it and no longer repeat facts.
- **srom-quant** is the former srom-scholarly-curator, renamed 30.09.2026; its two WordPress companions
  (wp-acf-plugin-builder, wp-elementor-builder) ship unchanged, as general-purpose skills.
- **Skills can be changed in either system, kept in sync by patches:** a change made in Cowork is tested, saved as a
  patch in `workspace/skill-changes/` and logged in `STATUS.md` § For the skills; you apply it in Code. Changes made
  in Code come back as a new plugin.
- **Not shipped:** the hooks (module guard, automatic HTML views of the ledger), `_widok/` and `mb_view.py` (you read
  the Markdown directly; red file links are now just 🔴 paths), the checkup skill and the reviews, the `_handoffs/`
  history, the git history of both modules, closed leaves and their gates, the 1.2 blind baseline and
  `vol18-PL-HOLD/`, `dump/`, `dist/`, the old InDesign scripts (`legacy/v2/`), the InDesign test tools, and derived
  build folders (the translation drafts' builds, Ostendorf's INJECT trial: `build.py` regenerates them).
- **The Mac-only InDesign installer** moved out of the skill into `local/`, with its test: the suite is 23 tests
  instead of Code's 24.
- **No git.** The workspace is a plain folder; keep a backup (Time Machine, or a copy before big steps).

## 6. Untested points (could not be tried from Claude Code)

1. Whether Cowork reads `workspace/CLAUDE.md` by itself. If not, paste it into the task or project instructions.
2. Network inside Cowork's sandbox: `setup.sh` needs PyPI (pip) and, if pandoc is missing, github.com. If they are
   blocked, the tools cannot run there; tell me what the sandbox offers.
3. The Python version in the sandbox (needs ≥ 3.10; tested on 3.10, 3.11, 3.13).
4. Whether the plugin's folder is writable: the examples in `skills/*/assets/example/` write their output next to
   themselves; real work always goes into `workspace/`.
5. srom-tlumacz closes a translation with the unlazy skill's gate checker (`anthropic-skills:unlazy`, in your
   account, not shipped): it needs node in the sandbox.
6. Upload limits for `srom.plugin` (2.2 MB unpacked) and for the workspace (36 MB, of which the source PDFs and the
   training corpus are most).
7. `workspace/srom-produkcja/work/ndiaye/key.py` points at the Code layout (one `sys.path` line, said in `STATUS.md`).
