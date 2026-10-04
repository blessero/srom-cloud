# SROM edit and trans — cooperation rules (all modules)

Loaded by every session under this folder, in addition to the module's own CLAUDE.md. It covers only how the
modules work together; everything else is in each module's own files.

## Names and stages (MB, 30.09.2026)
- **srom-produkcja** (`srom-produkcja/`, formerly srom-typeset): production, the managing module — RIP, INJECT,
  InDesign, volume data (`volumes/`: master CSV per volume, authors register). Its repo also holds the skills
  **srom-kanon** (house style) and **srom-quant** (formerly srom-scholarly-curator: metadata, DOI/Crossref, website).
  srom-quant has no session; srom-produkcja uses it. `_handoffs/tlumacz-to-quant.md` is read by srom-produkcja.
- **srom-tlumacz** (`srom-tlumacz/`): EN→PL translation.
- The three stages of a translated text, as MB names them (capitals where they should stand out):
  1. **RIP** (ripping, srom-produkcja): PDF or Word → source ready for translation (extraction, notes, keying, refs).
  2. **TRANS** (translating, srom-tlumacz): the translation, up to MB's Word edit.
  3. **INJECT** (injecting, srom-produkcja): MB's edited Word copy taken back, built, placed in InDesign.
  "Stage 1/2/3" in older files means the same.
- `srom-typeset` still resolves (a link to `srom-produkcja`, kept so older sessions open); older handoff entries,
  gates and reviews keep the old names as written. T<n> IDs keep their letter.

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

## Model and effort for every instruction to MB (MB, 04.10.2026) — hard rule
HARD RULE (MB, 04.10.2026). Every time you tell MB to do something in a session — in Claude Code or in Cowork: start a
session, apply or test a patch, run a check, paste a text, take a step on the Mac — you give, together with the
instructions, your best estimate of the Claude model and effort level that session should run at. An instruction to MB
without it is incomplete: do not send it. If unsure, say so and still give your best estimate. This includes
instructions you write for the Cowork session, and each item of a list of steps run in a different session.
Format, one line directly under the instruction:
  Run with: <Opus | Sonnet | Haiku> · <low | medium | high | xhigh | max> effort — <one clause: why>.
(Opus, Sonnet, Haiku = the current version of each.) Rough scale, adjust to the task: Haiku/Sonnet low = one fully
specified mechanical step; Sonnet medium = apply and test patches, preflights, routine work that follows a written
procedure; Sonnet/Opus high = debugging or building across several files, difficult RIP/INJECT, CSV/DOI/Crossref work;
Opus high–xhigh = editorial judgement, translation, referee-grade reviews, Zizek cards and block choice, anything MB
relies on without checking every line; Opus xhigh–max = system-wide audits, changing rules or skills, reconciling Cowork
and Code. Does not apply to chat answers or to what you do yourself in the session you are in.
(Cowork's copy: its `workspace/CLAUDE.md` § "Tasks you hand to MB".)

## Start of every session
1. Read your incoming file in `_handoffs/` (`tlumacz-to-produkcja.md` if you are srom-produkcja,
   `produkcja-to-tlumacz.md` if you are srom-tlumacz) and Cowork's `workspace/MB-decisions.md` (§ Cowork). Both modules also read
   `_handoffs/cowork-to-code.md` (from Cowork, if it exists) for items about their own skills (§ Cowork).
2. Report to MB, before anything else: new incoming items not yet answered, and open decisions that block you.

## Cowork (MB, 04.10.2026; SYS-9 and SYS-10 decided (a) 04.10.2026 22:30) — who does what
- **Cowork is where the journal is made**: the texts (RIP → TRANS → INJECT), the volume data, each text's state
  (`STATUS.md`) and the one list of MB's questions (its `workspace/MB-decisions.md`, answered on the Editorial Desk),
  all in `SROM/Cowork/srom-cowork/workspace/`. **Code is the workshop**: it builds and tests the skills (new
  functionality, fixes). Code's copies of the texts in `work/` are reference only: no session edits them.
- **One copy of the skills, Code's** (this repository). Until the switch (review 04.10.2026-2), Cowork still runs its
  own copy and sends patches; after it, Cowork reads the skills from this folder and makes small changes (a Kanon rule,
  a termbase row) here directly, after its preflight, with a C-item. A session that finds such uncommitted changes
  runs the module's tests and commits them first: `git commit -m "cowork: C<n> …"`.
- **Channel**, rules as between the modules (`_handoffs/README.md`): `cowork-to-code.md` (Cowork writes, C<n>; its
  patches in `_handoffs/cowork/`) and `code-to-cowork.md` (any Code session writes, K<n>). An item about a skill is
  answered by the module that owns it, with the commit hash. A Code change Cowork must know about (new or changed
  behaviour, a test count) is a K-item with the commit. A question for MB is a K-item headed "needs MB".
  Cowork does not commit: a session that finds its files changed commits them
  (`git -C _handoffs add cowork-to-code.md cowork && git -C _handoffs commit -m "cowork: <IDs>"`).
- `python3 _handoffs/tools/cowork_sync.py` (on the Mac) measures the drift until the switch; the checkup runs it.

## Checkup (cross-module review)
- In the root session (working directory `SROM edit and trans` itself), "checkup" / "system checkup" / "srom checkup" /
  "milestone check" / "health checkup" runs the skill `srom-checkup` (source `_handoffs/checkup/SKILL.md`).
- In a module session (srom-produkcja/, srom-tlumacz/), the same words mean **apply checkup**, never a new review:
  1. Open the newest `_handoffs/review-*.md` and follow only its `## For srom-produkcja` or `## For srom-tlumacz`
     section.
  2. Do the items that need no decision from MB, with your module's usual tests and commits.
  3. Put items that need MB in `MB-decisions.md`.
  4. Write one status line per item in your outgoing file, under `## Status of review <dd.mm.yyyy>`
     (done / declined / needs MB), and commit.
  5. Report to MB in a few lines.
- At the start of every module session: if the newest `review-*.md` has no "Status of review" heading in your
  outgoing file, tell MB.

## Messages between modules
- Rules: `_handoffs/README.md`. One file per direction; only the sender writes it; append, never rewrite;
  answers go in your own outgoing file, citing the item ID (E<n> from srom-tlumacz, T<n> from srom-produkcja).
- Several sessions of one module may run at once (29.09.2026). Immediately before adding a new ID (E<n>, T<n>, or a
  question ID such as PAH-11 in `MB-decisions.md`),
  re-read the end of the file to find the next free number, then commit straight away, so two sessions never
  take the same number. Cite items with their text tag, e.g. "E18 [Pahulich]".
- An item is answered when the receiver writes a status line for it (done / declined / needs MB). Don't leave
  incoming items without one.
- The binding interface stays in `srom-produkcja/.claude/skills/srom-produkcja/references/handoff.md`. A contract change
  is made there first, then in both modules, with tests on both sides (`run_all.py`, `tlumacz-test_handoff.py`).
- `_handoffs/` is a git repository (MB, 28.09.2026): after writing there, commit your own change at once
  (`git -C _handoffs add <files> && git -C _handoffs commit -m "<module>: <IDs>"`). Never rewrite its history.

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
- In any file MB reads, a file MB has to open (the ledger, a notes sheet, a Word copy to edit, a list to send to an
  author) is written `` 🔴 `path` ``. The rendered view shows it as a red link, colour **#ea3d39**. Chat text cannot be
  coloured: in replies the marker is the ⭕ described below.
- **End every reply with one line** listing the files MB needs to open for what the reply is about, or
  `Files to open: none`. Only files MB must act on, not every file you touched. Each file is its name as a link
  (relative path: opens in the app) followed by ⭕ as a second link to the same file as an absolute `file://` URL
  (opens in the browser; spaces as `%20`), e.g.
  `Files to open: [MB-decisions](_widok/MB-decisions.html) [⭕](file:///…/_widok/MB-decisions.html) · …`
- **Side panel by default:** before that line, send the rendered pages listed in it with SendUserFile (display:
  render), so they open in the app's side panel without a click. Word copies and CSV lists are only linked.
- For the ledger and notes sheets, link the rendered page, not the Markdown: first run
  `~/.venvs/srom/bin/python <SROM root>/_handoffs/tools/mb_view.py --all` (a few seconds), then link
  `_widok/MB-decisions.html` or the text's page (`_widok/PAH_pahulich.html`). Link paths relative to your working
  directory (from a module session: `../_widok/…`).
- On request ("show me", "as a document"), render with `mb_view.py` (HTML only; MB dropped Word output 29.09.2026) and send the HTML
  with SendUserFile (display: render) if you have it, or open it (`open <file>`). The rendered files embed the Claude
  app's fonts: they stay on this Mac, never published.

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
- Use the local skills (`~/.claude/skills/srom-*`, symlinks into srom-produkcja's repo). Never use copies synced
  from claude.ai (`anthropic-skills:srom-*`): they may be out of date.
- Never edit another module's folder. The only shared folder is `_handoffs/`.
- Before reporting a cross-module fact (a version, a test result, what the other side has done), check it in the
  files or by running the test. Don't rely on memory or the other side's report.

## Cloud sessions (MB, 04.10.2026)
A cloud session (claude.ai/code, or "Cloud" in the desktop app) works in the GitHub repository `srom-cloud`, a copy
of this folder that MB carries out and back on his Mac with `_cloud/cloud.py` (guide: `_cloud/README.md`). This
folder stays the home: while a cloud phase runs, nobody works in it locally (Cowork goes on as usual).
- **Which module you are.** The session starts at the repository root. MB's first words say it ("produkcja: …",
  "tlumacz: …", "root: …"); if they don't, ask. Then read that module's CLAUDE.md and handover and keep its rules as
  if your working directory were its folder. No hook guards the other module's folder here: keep out of it yourself.
- **Git.** Work on `main`, not on a session branch: `git pull --rebase origin main` first and before taking a new ID;
  after each commit, at once, `git pull --rebase origin main && git push origin HEAD:main` (parallel sessions see each
  other's items only after a push). The module folders are plain folders of one repository: `git -C _handoffs add
  <files> && git -C _handoffs commit …` still works; add only your own files, never `git add -A` at the root.
  Hashes cited in handoff items resolve (`git show <hash>`); a module's log before the move: `git log <its head>`
  (the heads are in the first "export" commit's message).
- **Data** the modules keep out of git (texts, PDFs, Word copies) is committed here on purpose (a module's
  `.gitignore` is stored as `.gitignore.module`): commit new data files with your work. `_handoffs/cowork-to-code.md`
  and `_handoffs/cowork/` are Cowork's: read them, never write them (an edit made here is dropped on the way back).
- **Skills** come from the repository's `.claude/skills/` (links into the modules), not from `~/.claude/skills`.
- **Dates.** The environment sets `TZ=Europe/Madrid`, so `date '+%d.%m.%Y %H:%M'` gives MB's time; if `date +%Z`
  says UTC, prefix the command with `TZ=Europe/Madrid`.
- **Not here:** InDesign and Word (MB's Mac), Cowork's folder, the rendered views (`_widok/`, `mb_view.py`: the hook
  is silent off the Mac). A file MB must open goes in the "Files to open" line as its repository path, without links
  or SendUserFile; MB opens it after `cloud.py import`. Sites outside the environment's network list do not answer:
  say that a scripted check did not run.
