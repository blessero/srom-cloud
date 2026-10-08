# _handoffs — messages between SROM modules

Created 26.09.2026 at MB's request. Modules: **srom-tlumacz** (translation, `../srom-tlumacz/`) and **srom-produkcja** (extraction, build, InDesign, `../srom-produkcja/`). srom-kanon and srom-quant may join later on the same rules.

## Files

One file per direction, named `<sender>-to-<receiver>.md`:

- `tlumacz-to-produkcja.md` — srom-tlumacz writes; srom-produkcja reads
- `produkcja-to-tlumacz.md` — srom-produkcja writes; srom-tlumacz reads
- `tlumacz-to-quant.md` — srom-tlumacz writes; MB passes it on to srom-quant
- `MB-decisions.md` — a pointer only: MB's open questions are Cowork's ledger, `../../workspace/MB-decisions.md`
  (since 04.10.2026, SYS-9 (a)); a Code session asks MB through a K-item headed "needs MB" (format below)
- `cowork-to-code.md` — Cowork writes (IDs C<n>); `code-to-cowork.md` — any Code session writes (IDs K<n>). Same
  rules as below; who answers: root CLAUDE.md § Cowork (04.10.2026)
- `tools/hooks/guard_module.py` — Claude Code hook, wired in each module's `.claude/settings.json`: refuses edits in
  the other module's folder
- `tools/backup.sh`, `tools/verify_backup.sh` — one archive of the one folder before any big step (root CLAUDE.md § Git)
- `MB-decisions-archive.md`, `review-*.md`, `draft-review-*.md` — history

## Rules

1. **Only the sender writes its file.** The receiver never edits it; it answers in its own outgoing file, citing the item ID.
2. **Append, don't rewrite.** Each entry starts with a heading `## <ID> — [<Author>] <subject> (dd.mm.yyyy HH:MM)`; `[<Author>]` names the text it concerns (`[general]` if none), so MB can follow one article across files. Times from 28.09.2026 16:45 on; older entries keep their date only. IDs: srom-tlumacz uses `E<n>`, srom-produkcja `T<n>`. An answer entry quotes the ID it answers (e.g. `## T3 — re E9: …`).
3. **Status changes are new lines, not edits:** under the item, `- dd.mm.yyyy HH:MM status: done / declined / needs MB — one line why`.
4. **Contracts stay where they are.** The binding interface is still `srom-produkcja/.claude/skills/srom-produkcja/references/handoff.md` (and the Kanon in srom-kanon). This folder carries requests and news about them, not the contract itself.
5. **Decisions that belong to MB** go to Cowork's ledger as questions with a text-coded ID (next section): a Code session writes the question as a K-item headed "needs MB", Cowork enters it with its ID. A handoff item that needs MB says `needs MB: <ID>`. Module handovers point to the ledger instead of keeping their own list.
6. **Each module reads its incoming file at the start of every session** and reports new items before anything else.
7. **This folder is under git** (since 28.09.2026, MB; since 05.10.2026 a plain folder of the one repository, remote
   `blessero/srom-cloud`). After writing here, commit only your own change and push it at once:
   `git -C _handoffs add <files> && git -C _handoffs commit -m "<module>: <IDs>"`, then
   `git pull --rebase origin main && git push origin HEAD:main` (root CLAUDE.md § Git).

## Checkup

`checkup/SKILL.md` is the source of the root session's `srom-checkup` skill (symlinked from `../.claude/skills/srom-checkup`;
versioned here since 28.09.2026, when the root folder was not yet a git repository). Reviews it writes: `review-<dd.mm.yyyy>.md`. How module
sessions apply them: root `CLAUDE.md` § Checkup. A partial pass (e.g. in the cloud) writes `draft-review-<dd.mm.yyyy>-<where>.md`,
which no module applies; the next full pass turns it into a review (no partial passes since the cloud was discontinued).
Cowork's checkup: `checkup/COWORK.md`.

## Questions for MB (since 29.09.2026 23:04)

MB could not follow the old ledger (D-numbers holding A1, B12, S10, § 12.2.4 c, E18 …). The rules below replace it.

**Text codes.** Every question belongs to one text or to one of three general groups. This table is the only list;
the session that starts a new text adds its row.

| Code | Text | Folder |
|---|---|---|
| NDI | Ndiaye, "Black Roma" (RQ 75, 2022) | ndiaye |
| PAH | Pahulich, "Racialization of Roma, European Modernity, and the Entanglement of Empires" (CRS 8/1, 2025) | pahulich |
| OST | Ostendorf, "Familiar Outsiders Abroad" (The Romani Atlantic, CUP 2026) | ostendorf |
| TIT | Tittel, "Racial and Social Dimensions of Antiziganism" (On_Culture 10, 2020) | tittel |
| WOH | West Ohueri, "Peripheral whiteness…" (Off White, MUP 2024) | westohueri |
| SCH | Scheffknecht, "Zigeuner im Reichshof Lustenau" (Neujahrsblätter Lustenau 1, 2010) | scheffknecht |
| V19 | Volume 19, all translated texts (shared terminology) | — |
| GEN | Journal-wide policy and Kanon gaps | — |
| SYS | Tooling and workflow | — |

**IDs.** `<CODE>-<n>` (PAH-1, GEN-4), one running number per code, shared by both modules, never reused. The next free
number stands in the text's section of Cowork's ledger ("Next free: PAH-100"); Cowork takes it when it enters a
question (new IDs from 100 up since SYS-9 (a)). One ID = one call MB makes; a list MB can approve with one yes (bibliography slips,
questions for the author) is one ID with numbered rows inside. A question for several texts goes under GEN or V19, and
each text's section names it in its first lines.

**In the ledger** (Cowork's `MB-decisions.md`; a K-item "needs MB" uses the same shape) each question is:

    ### PAH-1 · <the question itself, in plain words, ending with "?" where it is one>
    **Decide|Approve|Look up|Ask author|Later** · blocks <nothing | the translation | typesetting | publication …>

    <1–3 sentences: the situation, in words; the concrete thing (author, note number, book), never a category letter>
    - (a) … — **recommended**
    - (b) …
    Detail: 🔴 `<path from workspace/ to the notes sheet>` → PAH-1

    *Trail: <old codes, E/T items, Kanon §§ — for the modules; MB may skip it>*

and one row in the "At a glance" table at the top (same ID, short question, kind, blocks). A question is removed
(section and row) once MB has answered and the answer is recorded where it takes effect (Kanon, notes sheet, handoff
item, commit). No history in the ledger: the git log keeps it.

**In the notes sheet** (the detail), the same ID heads the item: a heading `### PAH-1 · …`, or, in lists a checker reads
(the `- S<n>` lines of srom-tlumacz), the ID right after the line's own marker: `- S10 [otwarte] [PAH-1] – …`.

**Writing for MB.** Plain words first. Kanon sections, handoff items (E/T), refs keys and old codes go only in the
*Trail* line, never in the question or the options. Each question must make sense without opening another file; the
notes sheet adds evidence, not the question.

**Notes sheets** are `<id>_uwagi.md` in both modules' folders of Cowork's workspace (`srom-produkcja/work/<id>/`: RIP,
the source; `srom-tlumacz/work/<id>/`: TRANS, the translation). srom-produkcja's were called `<id>_queries.md` until 29.09.2026;
copies handed over before that (`srom-tlumacz/work/<id>/src/<id>_queries.md`) keep the old name, and so do older
entries in the handoff files. The author's query sheets stay `*_pytania*`.

## Files MB must open

- A file MB has to open (a notes sheet, a Word copy to edit, a list to send) is written `` 🔴 `path` `` in any
  Markdown MB reads; in chat replies, the "Files to open" line (root CLAUDE.md). MB answers questions on the
  Editorial Desk. The rendered views (`_widok/`, `tools/mb_view.py`) were retired 08.10.2026.
