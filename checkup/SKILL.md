---
name: srom-checkup
description: Milestone health check (cross-module review) of the SROM tools — srom-produkcja, srom-kanon, srom-tlumacz, _handoffs, and the srom-quant skill's hygiene. Use when MB says "checkup", "perform checkup", "system checkup", "srom checkup", "milestone check" or "health checkup" in a session whose working directory is the root folder "SROM edit and trans" itself. Do NOT use in a session started inside srom-produkcja/ or srom-tlumacz/: there "checkup" means applying that module's section of the newest review (root CLAUDE.md), not running a new one. Do NOT use outside the SROM project.
---

# SROM checkup — cross-module review

Guard first: run `pwd`. Unless it is the folder that contains `srom-produkcja/`, `srom-tlumacz/` and `_handoffs/`, stop
and tell MB: "srom-checkup runs from the root session (SROM edit and trans); in a module session say 'apply checkup'."

You are the reviewer, not a module. Read everything, run everything, and change nothing in srom-produkcja/ or srom-tlumacz/.
The only file you write is the report (last step), committed in _handoffs. If MB later asks you to fix things, that is
a separate request.

## Safety
- Every build, round trip, mutation test or gate re-run goes on COPIES in your scratchpad, never in the module folders.
  Read a gate's CHECK before running it. Never run anything that writes a `<id>_robocza.docx` (the Word master) or
  anything else MB edits.
- Several module sessions may be running. Run `git status` on all three repos at the start and at the end. Don't touch
  uncommitted work, and name it in the report.
- Every time you write comes from `date '+%d.%m.%Y %H:%M'`. Give every shell command stdin `< /dev/null`.

## Read first
- `./CLAUDE.md`
- `_handoffs/README.md` and all of `_handoffs/` (MB-decisions.md, both outgoing files, the newest `review-*.md`)
- both modules' CLAUDE.md and handovers
- `srom-tlumacz/tlumacz-PLAN.md` (contract, tree, status log)
- `srom-produkcja/GATES.md`
- `srom-produkcja/.claude/skills/srom-produkcja/SKILL.md` and `references/handoff.md`
- the git log of srom-produkcja, srom-tlumacz and _handoffs since the last review

## Check, and measure rather than trust reports
1. **Tests.** srom-produkcja: `python3 .claude/skills/srom-produkcja/tests/run_all.py` (from srom-produkcja/). srom-tlumacz: the
   checks in its CLAUDE.md, including `tlumacz-test_handoff.py` and `tlumacz-draft_check.py --all`. Quote the verdict
   lines as printed, and name the srom-produkcja commit the contract test ran against.
2. **Texts.** For every text in progress (one section per text in MB-decisions.md):
   - srom-tlumacz's `src/` copies are byte-identical to srom-produkcja's frozen files, and the sha256 values equal those in
     the latest T-item
   - on copies: `check.py --pair`, `build.py --pair-src --queries --draft`, the build without --draft (only known
     `[BRAK …]` gaps may fail it), `tlumacz-front_check.py`, and import of the Word copy → pair check
   - keyed sources: `mutate_keyed.py` → MUTATIONS CAUGHT n/n
   - delivered texts: `take_back.py` verifies, and srom-produkcja builds from `work/<id>/pl/`
3. **Handoffs.**
   - every E<n>/T<n> has a status line from its receiver
   - no duplicate IDs; items cited with their [Author] tag
   - nothing "done" on one side that the other hasn't verified or has contradicted
   - no one writing in the other side's file
   - every dated entry has its time, and that time is not later than the commit that contains it
4. **Contract.** `handoff.md` (Out and Back) matches what both sides actually do: the scripts' behaviour, PLAN § Contract
   (including OUT-DELIVERY), and SKILL.md scenario C. Any contract change made on one side only, or without tests on
   both sides?
5. **Kanon and kartoteka.**
   - one normative text (srom-kanon `references/kanon-redakcyjny.md`)
   - the version is the same in the Kanon header, the last row of § 17, RULES.md, srom-kanon SKILL.md, the build report
     and every module's docs; no rule change appended to an already announced version
   - every § cited anywhere resolves in the Kanon
   - srom-kanon SKILL.md's quick rules don't contradict the Kanon
   - group names requested in E-items are in `kartoteka.tsv` or answered
6. **MB-decisions.md.**
   - only pending items, and the "At a glance" table lists every one of them (one row per section, "Next free" correct, Detail file exists)
   - nothing in it already decided elsewhere
   - nothing MB decided (in handovers, commits, handoff items) that a module still treats as open, or has not applied
   - no module acting on an undecided item without saying which choice it assumes
7. **Stale text.** Statements in CLAUDE.md files, handovers, PLAN, SKILL.md or decisions.md that the files or git now
   contradict (versions, counts, dates, "not yet built", "pending" items that are done).
8. **Gates.**
   - on copies, re-run the CHECKs of gates closed since the last review
   - report drift, CHECKs that test files meant to change, and any CHECK that writes a file MB edits
9. **Ownership and hygiene.**
   - no module wrote outside its folder or `_handoffs/`
   - all three working trees clean and committed
   - `~/.claude/skills/srom-*` are symlinks into the repo, not copies
   - `~/.claude/skills/srom-quant` is a symlink into the srom-produkcja repo like the other skills (moved there 30.09.2026)
   - `dist/*.skill` are current (they matter only before a claude.ai upload)
10. **Anything else** that will cause friction at the next milestone (the next hand-back, the first InDesign placement,
    a new text or source type).

## Report
Write `_handoffs/review-<dd.mm.yyyy>.md` (a second review on one day: add `-2`) and commit it:
`git -C _handoffs add <file> && git -C _handoffs commit -m "review: <date> [general]"`.

The file has these sections, with exactly these headings (module sessions look for them):
- `## Conclusions` — first.
- `## Verdict lines as printed`
- `## Findings` — a table: # | finding | evidence (file:line, command output) | severity (blocks / will bite /
  cosmetic) | who fixes it (srom-produkcja, srom-tlumacz, MB).
- `## Last review's findings` — fixed or still open.
- `## For srom-produkcja` and `## For srom-tlumacz` — numbered, self-contained instructions for that session (file:line,
  what to do, how to verify). Write "Nothing." if there is nothing.
- `## For MB` — only what needs MB's decision or action (including anything for srom-quant: website, DOI), in the order to
  decide it.

In chat, keep it legible and short:
- the conclusions (5–8 lines)
- a findings table with one line per finding: finding | severity | who fixes it
- the "For MB" list
- one closing line: "To apply: open a session in srom-produkcja/ and in srom-tlumacz/ and say 'apply checkup'."

Say plainly if there is nothing worth fixing. Don't invent problems to fill the report. Don't re-open decisions MB has made.
