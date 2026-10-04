# SROM in Cowork — session rules (workspace root)

This folder is the workspace of *Studia Romologica* (SROM) production: the volume data and every text in progress.
The procedures, house rules and tools are the **srom** plugin's skills; this file holds only the rules of a session.
Moved from Claude Code 03.10.2026 (MB). The person you work with is Michał Bartosz (MB), managing editor.

## The skills and the stages
- **srom-produkcja**: RIP (PDF or Word → frozen source ready for translation) and INJECT (MB's edited Word copy →
  build → InDesign). Owns the stage-gate spec: its `references/stages.md` (input, output, pass/fail of every stage).
- **srom-tlumacz**: TRANS (the English → Polish translation, up to MB's Word edit and its delivery).
- **srom-kanon**: the house rules. Its `references/kanon-redakcyjny.md` is normative; cite it as "Kanon v<n> § x".
- **srom-quant**: metadata, DOI/Crossref, website (formerly srom-scholarly-curator).
- Journal facts (ISSN, publisher, indexing, DOI state): the plugin's `SROM_knowledge_base.md`, nowhere else.
- One session runs all stages. What Claude Code did with messages between two modules is now the hand-off log in
  `STATUS.md` (sha256 of what goes from RIP to TRANS and back).

## Start of every session
1. Read `STATUS.md` (state of every text, hand-off log) and `MB-decisions.md` (MB's open questions).
2. Run the preflight of the skill you will use (srom-produkcja: `tests/run_all.py` → `SUITE ALL PASS`; srom-tlumacz:
   the termbase checks and `tlumacz-test_handoff.py`). The first time in a new environment: `sh setup.sh` at the
   srom plugin's root (two folders above any srom skill's folder): Python packages and pandoc.
3. Report to MB, before anything else: a failing check, and the open questions that block the work he asks for.

## Keep it lean (MB, 30.09.2026) — overrides the wish to be thorough
- The system has to work, not impress. Before adding a script, check, file type, field or procedure, ask whether a
  real, recurring problem needs it and whether a simpler way (an existing tool, a one-line rule, a minute of MB's
  manual work) is good enough. If it is, take it. Prefer extending what exists; one tool per job, no parallel copies.
- No new external service, dependency or paid tool unless it removes clear, measured work; say what it replaces.
- When proposing work to MB, name the cheapest version first, then the more automated options with their cost.

## The Word master
- MB edits every text in Word. From his first edit **the Word file (`<id>_robocza.docx`) is the master**: corrections
  go into it and the import is repeated; the md is never edited by hand after that.
- Never write a file MB edits from a check: export and import in a temporary folder.

## Never fabricate; doubts stay visible
- Never invent bibliographic, historical or institutional data. Missing data stays missing and is flagged
  (`[BRAK …]`). A bibliographic or historical claim needs two independent sources before it is delivered. No invented
  "official" Polish names for institutions, offices or acts.
- Anything in a source that looks wrong or makes no sense (a stray word in a reference, an odd name form, a garbled
  address) is flagged for discussion, never silently dropped or corrected. Keep what the source says until MB
  decides; say what you would do.

## Questions for MB (`MB-decisions.md`)
- Anything only MB can decide goes in `MB-decisions.md`. One question = one ID made of the text's code and a running
  number (`PAH-3`, `OST-1`; `GEN-` journal-wide, `V19-` all vol. 19 texts, `SYS-` tooling). The next free number is
  in the code's section ("Next free: PAH-11"); a new text gets a new code and section.
- Each question: a plain-language heading, its kind (Decide / Approve / Look up / Ask author / Later), what it blocks,
  the options with the recommended one marked, the red path to the detail, and a *Trail* line. Add a row to the
  "At a glance" table at the top.
- The notes sheet with the detail (`<id>_uwagi.md`) carries the same ID at the item's heading.
- Write for MB in plain words. Kanon §§, refs keys and category letters (A1, B12) go only in the *Trail* line. A
  question must make sense without opening another file.
- Don't act on an undecided item as if it were settled; say which choice you are assuming, if any.
- The ledger holds only what is pending. When MB decides, record the decision where it takes effect (Kanon request,
  notes sheet, `STATUS.md`, the files of the text) and remove the question and its table row.

## Files MB must open
- In any file MB reads, a file he has to open is written `` 🔴 `path` ``, the path relative to this folder. A path
  not found in this folder is in the plugin: under its skills (`srom-kanon/references/…`) or, for
  `SROM_knowledge_base.md`, at its root.
- End every reply with one line `Files to open: <paths>` listing only the files MB must act on, or
  `Files to open: none`.

## Dates and texts
- Every dated entry MB may read (STATUS lines, the ledger, notes sheets) carries date **and time**,
  `dd.mm.yyyy HH:MM`, taken from `date '+%d.%m.%Y %H:%M'`, never guessed. Older entries stay as they are.
- Every such entry names the text it concerns (`[<Author>]`, or `[general]`).

## Language and style
- Reply in the language MB writes in; internal analysis in English. Polish deliverables (translations, Kanon text,
  letters) in the elevated register of Polish academic and editorial writing.
- Conclusions first, terse, no re-explaining settled decisions. Candid critique; flag your own errors and limits.
  When MB says "explain" or "don't get it", use very plain language. Numbers in reports are measured, not estimated.

## Changing a skill: keep Cowork and Code in sync (MB, 03.10.2026 03:40)
Both systems run the same skills and must stay identical. A skill may be changed here (a Kanon rule, a termbase row,
a script), on these terms:
1. Change it, then run that skill's tests (srom-produkcja `tests/run_all.py`, srom-tlumacz preflight); all green.
2. Save the change as `skill-changes/<yyyymmdd-HHMM>_<skill>.patch` in this folder: `diff -u` of each changed file,
   paths relative to the skill's folder (`srom-kanon/references/kanon-redakcyjny.md`).
3. Add a line under `STATUS.md` § For the skills: date and time, skill, what changed, the patch file.
4. MB applies the patch in a Claude Code session (tests run there, commit) and ticks the line. Changes made in Code
   come back as a new plugin. Until a line is ticked, the two differ: say so before relying on the change.
A ruling for one text goes into that text's notes sheet, not into a skill.
