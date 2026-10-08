# SROM checkup in Cowork

For Cowork, when MB says "checkup" there (Code's root checkup is `SKILL.md` here). Cowork runs every stage in one
session, so the cross-module checks of Code's checkup (handoff items between modules, the contract seen from two sides)
have no object; what can drift in Cowork is its line to Code, its texts, and its own records. One session does it all:
check, report, then fix what needs no decision once MB says go, put the rest in `MB-decisions.md`, and send Code what
is Code's as a C-item.

Before: the srom-env block and `setup.sh` (srom-naczelny § Start of a session); `C` = Code's folder inside the one
folder, `$K` of the srom-env block (`$HOME/mnt/Redakcja/SROM edit and trans`). Nothing below writes a file MB edits:
builds and imports go to `mktemp -d`.

## Check, and measure rather than trust a line in STATUS.md
1. **Preflights.** srom-produkcja `run_all.py` and srom-tlumacz's three checks (srom-naczelny § Start). Quote the
   verdict lines. If a pass depends on a skill change not yet ticked in STATUS.md § For the skills, say so.
2. **Skills.** You read them from Code's folder: nothing to compare. If a skill file there has uncommitted changes
   you did not make, say so (a Code session is working); never edit a file a Code session is changing.
3. **Channel.** Every K-item in `$C/_handoffs/code-to-cowork.md` has your status line in `cowork-to-code.md`; every
   C-item older than two days has Code's answer; no ID twice in either file.
4. **Texts** (one per section of STATUS.md): each hand-off log line's sha256 equals the files it names (`sha256sum`);
   srom-tlumacz's `src/` copies are byte-identical to srom-produkcja's frozen files; on temp copies, for each draft
   `check.py --pair`, `build.py --pair-src --queries --draft`, the same build without `--draft` (only known `[BRAK …]`
   gaps may fail it), `tlumacz-front_check.py`, and its Word copy imported (`docx_in.py`) → pair check; each keyed
   (footnoted) source: `mutate_keyed.py` (srom-produkcja SKILL.md step 4b) → `MUTATIONS CAUGHT n/n`; a delivered text:
   `take_back.py` verifies and srom-produkcja builds from `work/<id>/pl/`. A failure that lies in the tools or the
   contract, not in the text, goes to Code as a C-item (Code's checkup no longer runs these checks: SYS-9 (a)).
5. **Ledger and desk.** The "At a glance" table lists every open question once, "Next free" is right (from 100 up),
   each Detail file exists; nothing decided in STATUS.md or a notes sheet is still open; every K-item headed "needs MB"
   is in the ledger; the desk's open decisions equal the ledger's (`desk_sync.py` bundle against the desk's `decisions`
   with status open).
6. **Records.** Every change you made in Code's folder since the last checkup has its C-item; statements in STATUS.md or
   `workspace/CLAUDE.md` the files now contradict.
7. **MB's folders** (root CLAUDE.md § The one folder). Anything in `1. Inbox/` that a session took is said in
   STATUS.md; every PDF in `3. PDF online/` has its result in `ready/`, or a STATUS line saying why not.

## Report
`workspace/reviews/review-<dd.mm.yyyy>.md`: `## Conclusions` (first), `## Verdict lines as printed`, `## Findings`
(table: # | finding | evidence | severity: blocks / will bite / cosmetic | who: Cowork, Code (C-item), MB),
`## Last review's findings`, `## For MB`. In chat: the conclusions in a few lines, one line per finding, the For MB
list. Don't invent problems; say plainly when there is nothing to fix; don't reopen MB's decisions.
