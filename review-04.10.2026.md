# Cross-module review — [general] 04.10.2026 (21:09–21:45)

Partial review at MB's request: the line between Code and Cowork, and readiness for a cloud phase. Not a full checkup:
texts, contract and Kanon were not re-checked beyond the standing tests. The root changed nothing in `srom-produkcja/`
or `srom-tlumacz/`. Repos at start: srom-produkcja 48982d1, srom-tlumacz fa0d755, `_handoffs` a34360a; all three
working trees clean. New here: `tools/cowork_sync.py` (the drift check), the channel files and rules (README § Cowork),
`checkup/COWORK.md`, SYS-9 and SYS-10 in the ledger; outside `_handoffs`: `_cloud/` and the root CLAUDE.md sections
§ Cowork and § Cloud sessions.

## Conclusions

1. **Both modules are green**: SUITE ALL PASS 24/24, HANDOFF CONTRACT 33/33, the four drafts as on 03.10.
2. **Cowork's patches are half carried over, and nobody can tell.** Of its seven patches, two are in Code (aa56f38,
   74449fc) but unticked in Cowork's STATUS.md; three apply cleanly to Code and wait; one fits only Cowork's copy (it
   restores Code's own wording there); the knowledge-base one has no file in Code.
3. **Code → Cowork has no defined route.** Code's changes reached Cowork by hand (two `.skill` files at 01:03, a patch
   at 02:34). At 20:39 Cowork's copies of srom-produkcja and srom-quant were reset to the 01:03 state (losing Code's
   02:34 normalize change and Cowork's own 02:54 Linux fixes); at 21:22 they were repaired. Neither step has a line in
   Cowork's STATUS.md; only file times show it.
4. **The two question ledgers already disagree.** Cowork used SYS-6 and SYS-7 for two other questions than this
   ledger's; Cowork's next free number, SYS-8, is this ledger's open SYS-8; SYS-1 has two wordings.
5. **No text has diverged yet** (work/ and volumes/ equal, except Ndiaye's `key.py`, an intended change, and Code-only
   cover proofs and per-text scripts): the right moment for SYS-9, before MB's first Word edit.
6. **Done at the root**: a channel in `_handoffs/` with the module rules (`cowork-to-code.md` / `code-to-cowork.md`,
   IDs C/K, Cowork's patches in `_handoffs/cowork/`), Cowork's question numbers from 100 up until SYS-9, the drift check
   (read-only, in both checkups), a slim checkup for Cowork. K1 tells Cowork; MB connects the folder there once.
7. **Cloud**: `_cloud/` carries this folder to a GitHub mirror and back (round trip on scratch copies: 24/24); the
   mirror is built here, not pushed. Rules for cloud sessions: root CLAUDE.md § Cloud sessions.

## Verdict lines as printed

srom-produkcja, `run_all.py`, commit 48982d1 (tail):
```
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 12/12
SUITE ALL PASS 24/24
```
srom-tlumacz, the four checks of its CLAUDE.md (venv), commit fa0d755:
```
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 33/33
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```
`python3 _handoffs/tools/cowork_sync.py` (21:27, after Cowork's repair), section 1:
```
  ok 20261003-0426_knowledge-base.patch: Code has no such file (knowledge base)
  !! 20261003-0426_srom-produkcja.patch: in Code, in Cowork; not ticked in Cowork's STATUS.md
  !! 20261003-1935_srom-zizek.patch: in Code, in Cowork; not ticked in Cowork's STATUS.md
  !! 20261004-0254_srom-produkcja.patch: not in Code: Code to apply (applies cleanly)
  !! 20261004-0254_srom-quant.patch: not in Code: Code to apply (applies cleanly)
  !! 20261004-0254_srom-tlumacz.patch: not in Code, does not apply to Code: look at it (a Cowork-only fix?)
  !! 20261004-0254_srom-zizek.patch: not in Code: Code to apply (applies cleanly)
```

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | Cowork's 02:54 patches for srom-produkcja, srom-quant, srom-zizek are not in Code; all three apply cleanly | cowork_sync.py § 1 | will bite (the cloud VM is Linux: font folders, PyMuPDF's new import name) | srom-produkcja |
| 2 | Cowork's 02:54 srom-tlumacz patch does not apply to Code and is not needed: it turns Cowork's T26 back to Code's wording | `patch --dry-run` fails on `tlumacz-test_handoff.py`; Code's `handoff.md:69` says "Delivery item", T26 passes 33/33 | cosmetic | srom-tlumacz (a K-item: declined, Cowork-only) |
| 3 | 03.10 04:26 srom-produkcja and 19:35 srom-zizek are in Code (aa56f38, 74449fc), still unticked in Cowork | Cowork STATUS.md § For the skills, all four lines `[ ]` | cosmetic | srom-produkcja (K-item) → Cowork ticks |
| 4 | No route for Code's changes to Cowork; Cowork's copy reset at 20:39, repaired 21:22, no STATUS line | file times in `plugin/srom/skills/`; cowork_sync.py before and after | will bite | root: channel made; Cowork: K1 |
| 5 | Question IDs collide: Cowork's SYS-6/SYS-7 ≠ Code's; Cowork's next free SYS-8 = Code's open SYS-8 | cowork_sync.py § 3 | will bite | Cowork (K1: from 100 up); MB (SYS-9) |
| 6 | Skill files differ beyond the patches (the bundle's edits: descriptions, stages page, examples, paths) | cowork_sync.py § 2: srom-tlumacz 5 differ + 5 only in Cowork; srom-kanon SKILL.md + 3 | will bite at every Code change | MB (SYS-10) |

## Last review's findings

Review 03.10.2026: rows 1–2 (srom-produkcja) have their status lines (`produkcja-to-tlumacz.md:678`, 03.10.2026 01:40);
srom-tlumacz had nothing.

## For srom-produkcja

1. Apply Cowork's patches `20261004-0254_srom-produkcja.patch`, `20261004-0254_srom-quant.patch` and
   `20261004-0254_srom-zizek.patch` from `/Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork/workspace/skill-changes/`:
   read each, then `patch -p0 -d .claude/skills -i <file>` (paths are relative to the skills folder). What they do:
   `docx_in.py` computes a footnote count before an f-string (Python < 3.12); `test_doi.py` finds `install_scripts.sh`
   in `tools/` or Cowork's `local/`; `test_quant.py` no longer crashes when no cover PDF was made; `cover_page.py`
   also looks in `$SROM_FONT_DIR`, `~/.local/share/fonts`, `~/.fonts`, `/usr/share/fonts…` (Mac unchanged);
   `extract.py` imports `pymupdf` with a fallback to `fitz`. Decline one, with the reason, if it goes against Code's
   own direction. Verify: suite 24/24; `python3 ../_handoffs/tools/cowork_sync.py` shows the three as "in Code, in
   Cowork". Commit ("Cowork patches 20261004-0254: …").
2. Write a K-item in `_handoffs/code-to-cowork.md` (root CLAUDE.md § Cowork; next free K: re-read the file's end):
   Cowork's patches now in Code, with hashes: 20261003-0426 srom-produkcja → aa56f38, 20261003-1935 srom-zizek → 74449fc,
   the three of item 1 → your commit. Cowork ticks them. Commit `_handoffs` at once.
3. From now on, at the start of a session also read `_handoffs/cowork-to-code.md` (root CLAUDE.md § Start, § Cowork).

## For srom-tlumacz

1. Cowork's `20261004-0254_srom-tlumacz.patch` is not for Code: it puts Cowork's copy of T26 back to Code's wording
   ("Delivery item", `handoff.md:69`). Write a K-item in `_handoffs/code-to-cowork.md`: declined, Cowork-only, nothing
   to apply in Code. Verify: HANDOFF CONTRACT stays 33/33. Commit `_handoffs` at once.
2. From now on, at the start of a session also read `_handoffs/cowork-to-code.md`.

## For MB

### SYS-9 · Texts and your questions: kept in Cowork or in Code?
The evidence behind the question in the ledger: Conclusions 4–5 and finding 5 above. What each answer means for the
channel: (a) Cowork's `MB-decisions.md` becomes the one list; Code's SYS questions move there through K-items, and this
ledger keeps only what a module is still working on until it is empty; the Code copies of the texts stay as they are
(no session edits them) until you delete them. (b) the reverse: Cowork's ledger and texts are frozen, Cowork asks
through C-items. (c) nothing moves; `cowork_sync.py` after each working session in either system.

### SYS-10 · Make the skill files the same in Code and Cowork?
The evidence: Conclusion 3, findings 2 and 6. With (a), srom-produkcja takes the knowledge-base file, `stages.md`, the
examples and the "Not for" lines into Code (the bundle's sources are in `_migracja/build/srom-cowork/plugin/`) and
srom-tlumacz its five files; the suite and the contract test decide. Afterwards a Code release to Cowork is a copy of
the skill folders (a K-item names the commit), and `cowork_sync.py` § 2 should show 0 differences.

Also for you, in order: claim the cloud credit before 07.10.2026 (`_cloud/README.md` § 1); connect Code's folder in
Cowork and paste the prompt from `_cloud/README.md` § 5; then SYS-9 and SYS-10.

To apply: open a session in srom-produkcja/ and in srom-tlumacz/ and say "apply checkup".
