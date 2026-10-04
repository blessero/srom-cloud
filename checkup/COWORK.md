# SROM checkup in Cowork

For Cowork, when MB says "checkup" there (Code's root checkup is `SKILL.md` here). Cowork runs every stage in one
session, so the cross-module checks of Code's checkup (handoff items between modules, the contract seen from two sides)
have no object; what can drift in Cowork is its line to Code, its texts, and its own records. One session does it all:
check, report, then fix what needs no decision once MB says go, put the rest in `MB-decisions.md`, and send Code what
is Code's as a C-item.

Before: the srom-env block and `setup.sh` (srom-naczelny § Start of a session); `C` = Code's folder as mounted in
`device_bash` (`ls "$HOME/mnt"`). Nothing below writes a file MB edits: builds and imports go to `mktemp -d`.

## Check, and measure rather than trust a line in STATUS.md
1. **Preflights.** srom-produkcja `run_all.py` and srom-tlumacz's three checks (srom-naczelny § Start). Quote the
   verdict lines. If a pass depends on a skill change not yet ticked in STATUS.md § For the skills, say so.
2. **Line to Code.** `python3 "$C/_handoffs/tools/cowork_sync.py" --cowork "$B"`. Quote sections 1 and 3. For every `!!`
   name the action: yours (tick a line, re-apply a patch you lost, renumber a question) or Code's (a C-item).
   Section 4 (text data) matters once MB edits Word copies: until SYS-9 is decided, any difference there is a finding.
3. **Channel.** Every K-item in `$C/_handoffs/code-to-cowork.md` has your status line in `cowork-to-code.md`; every
   C-item older than two days has Code's answer; no ID twice in either file; every patch in `_handoffs/cowork/` has
   its C-item and its STATUS line.
4. **Texts** (one per section of STATUS.md): each hand-off log line's sha256 equals the files it names (`sha256sum`);
   srom-tlumacz's `src/` copies are byte-identical to srom-produkcja's frozen files; on temp copies, for each draft
   `check.py --pair` and `build.py --pair-src --queries --draft`; a delivered text: `take_back.py` verifies and
   srom-produkcja builds from `work/<id>/pl/`.
5. **Ledger and desk.** The "At a glance" table lists every open question once, "Next free" is right (from 100 up while
   SYS-9 is open), each Detail file exists; nothing decided in STATUS.md or a notes sheet is still open; the desk's
   open decisions equal the ledger's (`desk_sync.py` bundle against the desk's `decisions` with status open).
6. **Records.** Every change to `plugin/srom/` since the last checkup has a line in STATUS.md (file times newer than
   the last line); statements in STATUS.md or `workspace/CLAUDE.md` the files now contradict.

## Report
`workspace/reviews/review-<dd.mm.yyyy>.md`: `## Conclusions` (first), `## Verdict lines as printed`, `## Findings`
(table: # | finding | evidence | severity: blocks / will bite / cosmetic | who: Cowork, Code (C-item), MB),
`## Last review's findings`, `## For MB`. In chat: the conclusions in a few lines, one line per finding, the For MB
list. Don't invent problems; say plainly when there is nothing to fix; don't reopen MB's decisions.
