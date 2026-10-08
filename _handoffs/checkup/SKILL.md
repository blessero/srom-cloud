---
name: srom-checkup
description: Milestone health check (cross-module review) of the SROM tools — srom-produkcja, srom-kanon, srom-tlumacz, _handoffs, and the srom-quant skill's hygiene. Use when MB says "checkup", "perform checkup", "system checkup", "srom checkup", "milestone check" or "health checkup" in a session whose working directory is the root folder "SROM edit and trans" itself (the repository root, in SROM/Redakcja). Do NOT use in a session started inside srom-produkcja/ or srom-tlumacz/: there "checkup" means applying that module's section of the newest review (root CLAUDE.md), not running a new one. Do NOT use outside the SROM project.
---

# SROM checkup — cross-module review

Guard first: run `pwd`. Unless it is the folder that contains `srom-produkcja/`, `srom-tlumacz/` and `_handoffs/`, stop
and tell MB: "srom-checkup runs from the root session (SROM edit and trans); in a module session say 'apply checkup'."

You are the reviewer, not a module. Read everything, run everything, and change nothing in srom-produkcja/ or srom-tlumacz/.
The only file you write is the report (last step), committed in _handoffs. If MB later asks you to fix things, that is
a separate request.

Scope (SYS-9 (a), 04.10.2026): Code builds and tests the skills; Cowork makes the journal. The texts, `STATUS.md` (the
hand-off log) and MB's question ledger are Cowork's, and Cowork's own checkup (`checkup/COWORK.md`) checks them. This
checkup checks the tools, their contract and docs, the Kanon, the gates, the channel between the modules and to Cowork,
and hygiene. Code keeps no copies of the texts (retired 08.10.2026): they are in `../workspace/`, read only.

## Safety
- Every build, round trip, mutation test or gate re-run goes on COPIES in your scratchpad, never in the module folders.
  Read a gate's CHECK before running it. Never run anything that writes a `<id>_robocza.docx` (the Word master) or
  anything else MB edits.
- Several sessions may be running. At the start `git pull --rebase origin main`; at the start and at the end
  `git status` at the root (one repository since 05.10.2026). Cowork's uncommitted files: commit them first as root
  CLAUDE.md § Cowork says. Any other uncommitted work: don't touch it, and name it in the report.
- Every time you write comes from `date '+%d.%m.%Y %H:%M'`. Give every shell command stdin `< /dev/null`.

## Read first
- `./CLAUDE.md`
- `_handoffs/README.md` and all of `_handoffs/`: both module files, the Cowork channel files, the newest `review-*.md`
  (`MB-decisions.md` is only a pointer to Cowork's ledger)
- Cowork's newest review (`../workspace/reviews/`)
- both modules' CLAUDE.md and handovers
- `srom-tlumacz/tlumacz-PLAN.md` (contract, tree, status log)
- `srom-tlumacz/.claude/skills/srom-tlumacz/SKILL.md` and its `references/outputs.md` (per-article file formats, OUT-*)
- `srom-produkcja/GATES.md`
- `srom-produkcja/.claude/skills/srom-produkcja/SKILL.md`, `references/handoff.md` and `references/stages.md`
- `git log` since the last review (one repository: each commit message names its module)

## Check, and measure rather than trust reports
1. **Tests.** srom-produkcja: `python3 .claude/skills/srom-produkcja/tests/run_all.py` (from srom-produkcja/). srom-tlumacz: the
   checks in its CLAUDE.md, including `tlumacz-test_handoff.py` and `tlumacz-draft_check.py --all` (they read Cowork's
   `../workspace/srom-tlumacz/` and only copy from it). Quote the verdict lines as printed, and name the commit the
   contract test ran against.
2. **Texts** are checked by Cowork's checkup (`checkup/COWORK.md` step 4: hand-off log, frozen copies, pair check,
   builds, Word import, mutation test, take-back). Here: carry into Findings any tool or contract problem that Cowork's
   newest review reports, and any C-item about one that has no answer.
3. **Handoffs.**
   - every E<n>/T<n> has a status line from its receiver
   - no duplicate IDs; items cited with their [Author] tag
   - nothing "done" on one side that the other hasn't verified or has contradicted
   - no one writing in the other side's file
   - every dated entry has its time, and that time is not later than the commit that contains it
4. **Contract.** `handoff.md` (Out and Back) and `stages.md` (stages 1–3) match what both sides actually do: the scripts'
   behaviour, PLAN § Contract, srom-tlumacz's `references/outputs.md` (including OUT-DELIVERY) and SKILL.md step 6, and
   srom-produkcja's SKILL.md scenario C. Any contract change made on one side only, or without tests on
   both sides?
5. **Kanon and kartoteka.**
   - one normative text (srom-kanon `references/kanon-redakcyjny.md`)
   - the version is the same in the Kanon header, the last row of § 17, RULES.md, srom-kanon SKILL.md, the build report
     and every module's docs; no rule change appended to an already announced version
   - every § cited anywhere resolves in the Kanon
   - srom-kanon SKILL.md's quick rules don't contradict the Kanon
   - group names requested in E-items are in `kartoteka.tsv` or answered
6. **Questions for MB.** The ledger itself (pending only, "At a glance", "Next free", Detail files) is Cowork's checkup
   (`checkup/COWORK.md` step 5). Here:
   - Code's `MB-decisions.md` holds no questions (only the pointer)
   - every K-item headed "needs MB" has Cowork's answer naming its ledger ID
   - nothing MB decided (C-items, handovers, commits, handoff items) that a module still treats as open, or has not applied
   - no module acting on an undecided item without saying which choice it assumes
7. **Stale text.** Statements in the CLAUDE.md files (root and modules), handovers, PLAN, SKILL.md or decisions.md that the
   files or git now contradict (versions, counts, dates, "not yet built", "pending" items that are done).
8. **Gates** (`srom-produkcja/GATES.md`, `srom-tlumacz/tlumacz-gates-*.md`).
   - on copies, re-run the CHECKs of tool gates closed since the last review. Gates of a text leaf (CHECK runs in
     `work/<id>/`) are history: the texts left the repository on 08.10.2026, and Cowork's checkup checks them
   - report drift, CHECKs that test files meant to change, and any CHECK that writes a file MB edits
9. **Ownership and hygiene.**
   - no module wrote outside its folder or `_handoffs/`
   - the repository clean and `main` pushed (`git status`; `git log origin/main..HEAD` empty)
   - the root `.claude/skills/` links resolve; `~/.claude/skills/srom-*` (srom-quant included) and the two WordPress
     skills are symlinks into the repository, not copies
   - the one folder's top level holds only MB's four numbered folders, `SROM edit and trans/` and `workspace/` (root
     CLAUDE.md § The one folder); a backup newer than the last big step (`_handoffs/tools/verify_backup.sh`)
   - `dist/*.skill` are current (they matter only before a claude.ai upload)
10. **Cowork.** Every C-item in `cowork-to-code.md` has a status line in `code-to-cowork.md`, and every K-item has
    Cowork's answer. Findings for Cowork go into a K-item the root writes after the report (Cowork's own checkup:
    `checkup/COWORK.md`).
11. **Anything else** that will cause friction at the next milestone (the next hand-back, the first InDesign placement,
    a new text or source type).

## Report
Write `_handoffs/review-<dd.mm.yyyy>.md` (a second review on one day: add `-2`) and commit it:
`git -C _handoffs add <file> && git -C _handoffs commit -m "review: <date> [general]"`, then push (root CLAUDE.md
§ Git).

The file has these sections, with exactly these headings (module sessions look for them):
- `## Conclusions` — first.
- `## Verdict lines as printed`
- `## Findings` — a table: # | finding | evidence (file:line, command output) | severity (blocks / will bite /
  cosmetic) | who fixes it (srom-produkcja, srom-tlumacz, MB).
- `## Last review's findings` — fixed or still open.
- `## For srom-produkcja` and `## For srom-tlumacz` — numbered, self-contained instructions for that session (file:line,
  what to do, how to verify). Write "Nothing." if there is nothing.
- `## For MB` — only what needs MB's decision or action (including anything for srom-quant: website, DOI), in the order to
  decide it. Each step MB takes in a session carries its "Run with:" line (root CLAUDE.md, hard rule).

In chat, keep it legible and short:
- the conclusions (5–8 lines)
- a findings table with one line per finding: finding | severity | who fixes it
- the "For MB" list
- one closing line: "To apply: open a session in srom-produkcja/ and in srom-tlumacz/ and say 'apply checkup'.", with
  its "Run with:" line

Say plainly if there is nothing worth fixing. Don't invent problems to fill the report. Don't re-open decisions MB has made.
