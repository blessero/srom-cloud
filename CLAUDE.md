# SROM edit and trans — cooperation rules (all modules)

Loaded by every session under this folder, in addition to the module's own CLAUDE.md. It covers only how the
modules work together; everything else is in each module's own files.

## Names and stages (MB, 30.09.2026)
- **srom-produkcja** (`srom-produkcja/`, formerly srom-typeset): production, the managing module — RIP, INJECT,
  InDesign, the tools for the volume data (the data itself is Cowork's: § The one folder). Its folder also holds the
  skills **srom-kanon** (house style), **srom-quant** (formerly srom-scholarly-curator: metadata, DOI/Crossref, website)
  and **srom-zizek** (selection, before RIP). srom-quant has no session; srom-produkcja uses it.
  `_handoffs/tlumacz-to-quant.md` is read by srom-produkcja.
- **srom-tlumacz** (`srom-tlumacz/`): EN→PL translation.
- The three stages of a translated text, as MB names them (capitals where they should stand out):
  1. **RIP** (ripping, srom-produkcja): PDF or Word → source ready for translation (extraction, notes, keying, refs).
  2. **TRANS** (translating, srom-tlumacz): the translation, up to MB's Word edit.
  3. **INJECT** (injecting, srom-produkcja): MB's edited Word copy taken back, built, placed in InDesign.
  "Stage 1/2/3" in older files means the same.
- Older handoff entries, gates and reviews keep the old names (srom-typeset) and paths as written. T<n> IDs keep
  their letter.

## The one folder (MB, 08.10.2026; review 07.10.2026, For MB 5)
Everything lives in `SROM/Redakcja/` (Mac: `/Users/michalbartosz/ARBEIT/Bima/SROM/Redakcja`). MB starts Cowork on this
folder (no "+"), and it is his Finder favourite. The four numbered folders are MB's; sessions keep their own files out
of the top level.

| folder | what it holds | rule |
|---|---|---|
| `1. Inbox/` | anything MB drops in: author files, PDFs, texts for the corpus | a session copies what it needs into place and says where; the original stays until MB clears it (Cowork cannot delete) |
| `2. Word` | a Finder Smart Folder: every `*_robocza.docx` in `workspace/` | the Word copies MB edits, in place; one in a `pl/` folder is a sealed delivery, never edited |
| `3. PDF online/` | MB's InDesign exports for the website (preset "SROM online") | Cowork repairs the text layer and adds the cover (`cover_page.py`) into `3. PDF online/ready/` |
| `4. Archive/` | old material (Cowork's bundle and dump, old cover templates and proofs, Code's dump) | no session reads it unless MB asks |
| `SROM edit and trans/` | this repository: the skills, `_handoffs/`, the module records | Code sessions start here or in a module folder |
| `workspace/` | Cowork's: the texts, the volume data, `STATUS.md`, `MB-decisions.md`, the desk, srom-zizek's data | not in git; Code reads it (`../workspace/` from here) but never writes it, except srom-zizek's data and srom-ikonograf's `work/<id>/ikonografia/` folders, as those skills say |

The old Code path `SROM/CODE/SROM/SROM edit and trans` is a link to this repository until MB deletes it (planned
15.10.2026), so sessions started there still open; start new sessions from `SROM/Redakcja/`. Code keeps no copies of
the texts or the volume data (retired 08.10.2026; git history has them).

## Keep it lean (MB, 30.09.2026) — overrides the wish to be thorough
The system has to work, not impress. Never let it grow into an outsized, byzantine clump.
- Before adding a script, check, file type, field, service, gate or procedure, ask: does a real, recurring problem
  need it, and is there a simpler way (an existing tool, a one-line rule, a manual step MB can do in a minute)?
  If the simpler way is good enough, take it. A bit more manual beats a lot more machinery.
- Prefer extending what exists over adding something new. One tool per job; no parallel copies (promote a
  per-article script into the tested toolchain only when it has recurred, and then delete the copies).
- No new external service, dependency or paid tool unless it removes clear, measured work. Say what it replaces.
- Checks that only warn must earn their noise: measure the false positives on real texts before adding one.
- When proposing work to MB, name the cheapest version first. Remove what is no longer used.
- Lean is about what gets built, not what MB hears: always tell MB about more automated options worth knowing
  (with their cost), then let him choose.

## Model and effort for a task in another session (MB, 20.10.2026; replaces the hard rule of 04.10.2026)
When you hand MB a task to run in another session (Code or Cowork), put one line under it:
  Run with: <Opus | Sonnet | Haiku> · <effort> — <the scope you checked: what it touches, how big, the one real risk>.
- Give it only after looking at what the task touches (the files, the size of the change). If you have not looked,
  write "scope not checked" in the clause: it is then a guess and says so.
- Judge the task, not its label: a "rule change" of a few lines with no code is medium work; a small-sounding request
  that runs across many files, or needs editorial or translation judgement, is high or more. No lookup table.
- Never for steps MB does by hand, chat answers, or what you do in your own session.
- It is a reference point for MB, not a verdict: he weighs it against his own sense of how the models do.

## Start of every session
1. Read your incoming file in `_handoffs/` (`tlumacz-to-produkcja.md` if you are srom-produkcja,
   `produkcja-to-tlumacz.md` if you are srom-tlumacz) and Cowork's `../workspace/MB-decisions.md` (§ Cowork). Both modules also read
   `_handoffs/cowork-to-code.md` (from Cowork, if it exists) for items about their own skills (§ Cowork).
2. Report to MB, before anything else: new incoming items not yet answered, and open decisions that block you.

## Cowork (MB, 04.10.2026; SYS-9 and SYS-10 decided (a) 04.10.2026 22:30) — who does what
- **Cowork is where the journal is made**: the texts (RIP → TRANS → INJECT), the volume data, each text's state
  (`STATUS.md`) and the one list of MB's questions (its `MB-decisions.md`, answered on the Editorial Desk), all in
  `../workspace/` (§ The one folder). **Code is the workshop**: it builds and tests the skills (new functionality,
  fixes). A Code session that needs a text (to reproduce a bug) reads it there, or works on a copy in its scratchpad.
- **One copy of the skills, Code's** (this repository; since K6, C3, 04.10.2026 23:31). Cowork reads them from here
  and makes small changes (a Kanon rule, a termbase row) directly, after its preflight, with a C-item. Committing
  those changes: see "Auto-commit" below.
- **Channel**, rules as between the modules (`_handoffs/README.md`): `cowork-to-code.md` (Cowork writes, C<n>) and
  `code-to-cowork.md` (any Code session writes, K<n>). An item about a skill is answered by the module that owns it,
  with the commit hash. A Code change Cowork must know about (new or changed behaviour, a test count, a path) is a
  K-item with the commit. A question for MB is a K-item headed "needs MB".
  Cowork does not commit. `cowork-to-code.md` itself: a Mac session that finds it changed commits and pushes it
  (`git -C _handoffs add cowork-to-code.md && git -C _handoffs commit -m "cowork: <IDs>"`, then push: § Git).
  Skill files changed by Cowork: "Auto-commit" below.
- **Auto-commit** (skill files changed by Cowork, named in a C-item) (MB, 08.10.2026; from Cowork's proposal): at the start of every session, after
  reading `_handoffs/cowork-to-code.md`, if its newest C-item names a small skill change for Code to commit, run
  `git status --short` and check that only the files that C-item lists are changed. If so, run the module's tests
  (srom-produkcja's `run_all.py` for its skills), and if they pass, commit at once without asking MB: add only those
  files (never `git add -A`), `cowork: C<n> … [<text or general>]`, then
  `git pull --rebase origin main && git push origin HEAD:main`. If other files changed, or a test fails, do not
  commit; tell MB.

## Checkup (cross-module review; who applies it: MB, 20.10.2026)
- In the root session (working directory `SROM edit and trans` itself), "checkup" / "system checkup" / "srom checkup" /
  "milestone check" / "health checkup" runs the skill `srom-checkup` (source `_handoffs/checkup/SKILL.md`). **The root
  session then applies the review itself**, in the same session, without waiting for "apply checkup":
  1. Every item in `## For srom-produkcja` and `## For srom-tlumacz` that needs no decision from MB, with that
     module's usual tests (srom-produkcja's `run_all.py`; srom-tlumacz's checks in its CLAUDE.md) and commits named
     after the module (`produkcja: review <date> #<n> [<text>]`).
  2. Except these, left to a session in the module (the status line says which and why):
     - a Kanon rule change (the Kanon is changed only from a srom-produkcja session, § Shared rules);
     - translation judgment: choosing a Polish term or wording, a termbase or HOUSE row, anything in a translation;
     - a module with a session running now (MB says so, or `git status --short <module>/` shows uncommitted
       changes there): all of that module's items.
  3. Items that need MB: one K-item headed "needs MB" (§ Decisions for MB).
  4. Status lines, for a module whose section has items (not "Nothing."): in that module's outgoing file, under
     `## Status of review <dd.mm.yyyy> (root, dd.mm.yyyy HH:MM) [general]`, one line per item: done (commit) /
     declined / needs MB (K<n>) / left for srom-<module> (why). Commit and push at once (§ Git). This is the one
     place the root writes in a module's outgoing file (`_handoffs/README.md` rule 1).
  5. Report to MB in a few lines; name any item left for a module session.
  A root session asked only for "apply checkup" does steps 1–5 for the newest review's items that have no status line.
- In a module session (srom-produkcja/, srom-tlumacz/), "checkup" means **apply checkup**, never a new review: do the
  newest review's items in your section that are marked "left for <your module>" (or that have no status line), with
  your usual tests and commits; then append, at the end of your outgoing file, `## Status of review <dd.mm.yyyy>,
  continued (<module>, dd.mm.yyyy HH:MM) [general]` with one line per item, and commit.
- At the start of every module session: if the newest `review-*.md` lists items for your module and your outgoing
  file has no status line for one of them, or one is "left for" your module and has no later line, tell MB.

## Messages between modules
- Rules: `_handoffs/README.md`. One file per direction; only the sender writes it (one exception: the root's
  review status lines, § Checkup); append, never rewrite;
  answers go in your own outgoing file, citing the item ID (E<n> from srom-tlumacz, T<n> from srom-produkcja).
- Several sessions of one module may run at once (29.09.2026). Immediately before adding a new ID (E<n>, T<n>, K<n>),
  re-read the end of the file to find the next free number, then commit straight away, so two sessions never
  take the same number. Cite items with their text tag, e.g. "E18 [Pahulich]".
- An item is answered when the receiver writes a status line for it (done / declined / needs MB). Don't leave
  incoming items without one.
- The binding interface stays in `srom-produkcja/.claude/skills/srom-produkcja/references/handoff.md`. A contract change
  is made there first, then in both modules, with tests on both sides (`run_all.py`, `tlumacz-test_handoff.py`).
- `_handoffs/` is under git (MB, 28.09.2026; since 05.10.2026 as part of the one repository, § Git): after
  writing there, commit your own change at once (`git -C _handoffs add <files> && git -C _handoffs commit -m
  "<module>: <IDs>"`) and push. Never rewrite its history.

## Decisions for MB (format since 29.09.2026 23:04; full rules: `_handoffs/README.md` § Questions for MB)
- Anything only MB can decide goes to Cowork's ledger (since 04.10.2026: § Cowork) as a K-item headed "needs MB",
  written in the format below; `_handoffs/MB-decisions.md` is only a pointer now. Your handover may point to it but
  should not keep a second list.
- One question = one ID made of the text's code and a running number: `PAH-3`, `OST-1`, `GEN-4` (journal-wide),
  `V19-2` (all vol. 19 texts), `SYS-1` (tooling). Codes are listed in the README table; a new text gets its row there.
  The next free number is in the text's section of the ledger. The old D<n> numbers survive only in *Trail* lines.
- Each question in the ledger: a plain-language heading, its kind (Decide / Approve / Look up / Ask author / Later),
  what it blocks, the options with the recommended one marked, the red path to the detail, and a *Trail* line. Add
  a row to the "At a glance" table at the top.
- The notes sheet with the detail (`<id>_uwagi.md`, in both modules; srom-produkcja's were `<id>_queries.md`) carries
  the same ID at the item's heading or label.
- Write for MB in plain words. Kanon §§, E/T items, refs keys, category letters (A1, B12, S10) go only in the *Trail*
  line. A question must make sense without opening another file.
- Don't act on an undecided item as if it were settled; say which choice you are assuming, if any.
- `MB-decisions.md` holds only what is still pending. Whichever session receives MB's decision on an item, or is
  asked to resolve it itself, removes the item (its section and its table row) once it is actually resolved
  (decision recorded where it takes effect: Kanon, notes sheet, handover, handoff item, commit). No history there.

## Files MB must open (MB, 29.09.2026) — hard rule, every session
- In any file MB reads, a file MB has to open (a notes sheet, a Word copy to edit, a list to send to an author) is
  written `` 🔴 `path` ``. Chat text cannot be coloured: in replies the marker is the ⭕ described below.
- **End every reply with one line** listing the files MB needs to open for what the reply is about, or
  `Files to open: none`. Only files MB must act on, not every file you touched. Each file is its name, a word saying
  which text it belongs to, and its absolute path in backticks (MB copies it), e.g.
  `` Files to open: kontaktowka.html (Tittel) — `/Users/michalbartosz/ARBEIT/Bima/SROM/Redakcja/workspace/srom-produkcja/work/tittel/ikonografia/kontaktowka.html` ``
  No ⭕ or `file://` links: they did not open in the app (MB, 24.10.2026).
- **The button is the SendUserFile card** (MB, 24.10.2026: it opens the file reliably). Send every Markdown, HTML or
  PDF file in that line with SendUserFile (display: render) as the **last tool call** of the turn, so the card sits
  right above the closing reply; Word copies and CSV lists get the path only.
- MB's questions: he reads and answers them on the Editorial Desk (`https://claude.ai/artifact/9w8QwRuni5c3fAPVtmRb61`);
  link the desk, not the ledger file. Only Cowork reads the answers (srom-naczelny § The desk).
- The rendered views (`_widok/`, `mb_view.py`) were retired 08.10.2026: they showed Code's pointer file and outdated
  copies of the notes sheets.

## Dates and texts (MB, 28.09.2026)
- Every dated entry MB may read (handoff items, status lines, MB-decisions, handovers, notes sheets) carries date
  **and time**: `dd.mm.yyyy HH:MM`, taken from `date '+%d.%m.%Y %H:%M'`, never guessed. Older entries stay as they are.
- Every such entry names the text it concerns (`[<Author>]`, or `[general]`), since several texts run in parallel.

## Doubts in the material
- Anything in a source that looks wrong or makes no sense (a stray word in a reference, an odd name form, a
  garbled address) is flagged for discussion, never silently dropped or corrected. Keep what the source says
  until MB decides; say what you would do.

## Shared rules and skills
- **Kanon** (house rules): `srom-produkcja/.claude/skills/srom-kanon/references/kanon-redakcyjny.md` is normative.
  It is edited only from the srom-produkcja session; other modules ask for changes through `_handoffs/`.
- Use the local skills (`~/.claude/skills/srom-*` and the two WordPress skills: symlinks into this repository; if
  one is broken, `sh srom-produkcja/tools/setup_mac.sh`, and for srom-tlumacz
  `ln -sfn "$PWD/srom-tlumacz/.claude/skills/srom-tlumacz" ~/.claude/skills/` from here). Never use copies synced from
  claude.ai (`anthropic-skills:srom-*`): they may be out of date.
- Never edit another module's folder. The only shared folder is `_handoffs/`.
- Before reporting a cross-module fact (a version, a test result, what the other side has done), check it in the
  files or by running the test. Don't rely on memory or the other side's report.

## Git (one repository since 05.10.2026; cloud sessions discontinued 07.10.2026)
This repository (`SROM edit and trans/`) is one git repository, remote `blessero/srom-cloud` (GitHub, private): history
and the off-Mac backup. **No SROM sessions in the cloud** (MB 07.10.2026): work on the Mac (Code) and in Cowork only.
- **Every session.** Work on `main`, not on a session branch: `git pull --rebase origin main` first and before taking
  a new ID; after each commit, at once, `git pull --rebase origin main && git push origin HEAD:main`. The module
  folders are plain folders of the one repository: `git -C _handoffs add <files> && git -C _handoffs commit …` works;
  add only your own files, never `git add -A` at the root. Never rewrite pushed history. Hashes cited in handoff items
  resolve (`git show <hash>`); a module's log before the move: `git log <its head>` (the heads are in the first
  "export" commit's message). Except commits made in the old module repos between the first export and the move
  (04.10.2026 21:42 – 05.10.2026 00:31): only the next export snapshot holds them (`git show <snapshot>:<path>`):
  2cfbeff, aa1096b, ffeaf34, c52ed2f → 258ae9e; e079042, 542dacf, 593440d, 4f00cb1, b653484 → ff44289; 6f470d5,
  eb4d3e1 → 73d9638.
- **Not in git:** Cowork's `../workspace/` (texts, volume data, ledger) and MB's numbered folders. Before any big step,
  `sh _handoffs/tools/backup.sh` (the whole one folder except `4. Archive`, into `SROM/CODE/_backup/`), then
  `sh _handoffs/tools/verify_backup.sh` → `BACKUP OK`. Code's old copies of the texts and volume data are in the
  history up to 08.10.2026 (`git show f24a568:<path>`).
- **Cowork** does not commit: a Mac session that finds Cowork's files in this repository changed (`_handoffs/cowork-to-code.md`,
  a small skill change named in a C-item) commits and pushes them (§ Cowork).
