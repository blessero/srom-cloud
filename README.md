# _handoffs — messages between SROM modules

Created 26.09.2026 at MB's request. Modules: **srom-tlumacz** (translation, `../srom-tlumacz/`) and **srom-typeset** (extraction, build, InDesign, `../srom-typeset/`). srom-kanon and srom-scholarly-curator may join later on the same rules.

## Files

One file per direction, named `<sender>-to-<receiver>.md`:

- `tlumacz-to-typeset.md` — srom-tlumacz writes; srom-typeset reads
- `typeset-to-tlumacz.md` — srom-typeset writes; srom-tlumacz reads
- `tlumacz-to-curator.md` — srom-tlumacz writes; MB passes it on to srom-scholarly-curator

## Rules

1. **Only the sender writes its file.** The receiver never edits it; it answers in its own outgoing file, citing the item ID.
2. **Append, don't rewrite.** Each entry starts with a heading `## <ID> — [<Author>] <subject> (dd.mm.yyyy HH:MM)`; `[<Author>]` names the text it concerns (`[general]` if none), so MB can follow one article across files. Times from 28.09.2026 16:45 on; older entries keep their date only. IDs: srom-tlumacz uses `E<n>`, srom-typeset `T<n>`. An answer entry quotes the ID it answers (e.g. `## T3 — re E9: …`).
3. **Status changes are new lines, not edits:** under the item, `- dd.mm.yyyy HH:MM status: done / declined / needs MB — one line why`.
4. **Contracts stay where they are.** The binding interface is still `srom-typeset/.claude/skills/srom-typeset/references/handoff.md` (and the Kanon in srom-kanon). This folder carries requests and news about them, not the contract itself.
5. **Decisions that belong to MB** are marked `needs MB` and entered in `MB-decisions.md` (one list for all modules, any module appends; added 27.09.2026). Module handovers point to it instead of keeping their own list. Resolved items are removed from it; it is grouped by text (rules at its top).
6. **Each module reads its incoming file at the start of every session** and reports new items before anything else.
7. **This folder is a git repository** (since 28.09.2026, MB). After writing here, commit only your own change:
   `git -C _handoffs add <files> && git -C _handoffs commit -m "<module>: <IDs>"`. Local only, no remote.

## Checkup

`checkup/SKILL.md` is the source of the root session's `srom-checkup` skill (symlinked from `../.claude/skills/srom-checkup`;
versioned here because the root folder is not a git repository). Reviews it writes: `review-<dd.mm.yyyy>.md`. How module
sessions apply them: root `CLAUDE.md` § Checkup.
