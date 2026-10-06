# DRAFT checkup — [general] 06.10.2026 (22:05–22:54), partial pass in the cloud

**This is not a review.** The file name keeps it out of `review-*.md` on purpose, so no module session applies it.
It was written by a root session in a cloud container (claude.ai/code), with no Cowork workspace, no InDesign or
Word, and no rendered views (`_widok/`, `mb_view.py`). MB asked for review only, apart from plain repo-internal
faults; none of the faults found turned out to be plain (see finding 2), so **nothing was changed** in the
repository except this file.

**For the next pass (a full root checkup on the Mac):** re-check the rows labelled *may depend on Mac/Cowork state*,
run the checks listed under "Checks not run", then write `review-<dd.mm.yyyy>.md` from this draft. Only that file
goes to the modules ("apply checkup").

Labels:
- **repo-only confirmed**: measured in the repository alone; nothing outside it can change the result.
- **may depend on Mac/Cowork state**: depends on something only the Mac or Cowork holds (Cowork's texts,
  `STATUS.md`, its ledger, the venv, old repositories).

Repository at start and end: `main` = `39302d3` (06.10.2026 22:01), working tree clean, nothing uncommitted.
The last review is `review-04.10.2026-2.md`; module commits since then: 1113fec, adc86d1, a414512, 0460016, 20f4f26,
e2829ba, e0a51a2, f109090, 07699c7, 6d6e8c7, 9415109, 39302d3 (plus the export snapshots 258ae9e, ff44289, 73d9638 and
the move to one repository, 48a28ce).

## Conclusions

1. **Both modules are green**: SUITE ALL PASS 26/26 (one more test file since K10's 25/25: `test_kb.py`, 39302d3),
   HANDOFF CONTRACT 33/33. All four drafts held in Code pass the pair check, the draft build, the front check and the
   Word import. All five keyed sources catch 40/40 mutants. Kanon v1.16 is the same everywhere, and every § cited
   in the skills exists.
2. **The next hand-back will stop at INJECT.** Since 04.10 the final build fails on any text `normalize.py` would
   still change. The contract (`handoff.md` Back, `stages.md` § 3) has no normalise step after the take-back, and
   `SKILL.md` scenario C normalises in place a copy that must never be edited. Measured on Code's copies: Ndiaye
   fails only on this (9 changes, 1 flag), Ostendorf on this plus its known `[BRAK …]`.
3. **pikepdf is missing from the one requirements file Cowork installs from**, and the pin used on the Mac and in
   the cloud (10.16.0) needs Python ≥ 3.11, while Cowork's VM runs 3.10 and the file promises ≥ 3.10. On a fresh
   Cowork VM the suite would fail and cover pages would abort. 10.13.0.post1 installs on both versions and passes
   test_quant 42/42 (measured here). The pin check that should catch this still reads Cowork's retired plugin folder.
4. **Both handovers predate MB's 04.10 decision** that the texts and the ledger live in Cowork (SYS-9 (a)). A new
   module session reading them would work on Code's reference copies and write questions to a ledger that no longer
   exists.
5. **Eleven commit hashes cited in K3, K6, K7 and the T37 status lines do not exist in this repository**, although
   the root CLAUDE.md says they resolve. They live only in the Mac's `SROM edit and trans.old`, which the cloud guide
   says to keep for one week from 05.10.
6. **The checkup itself is out of date**: it still assumes three repositories and a ledger with one section per text
   in Code. Its text and ledger checks now belong to Cowork's checkup (`checkup/COWORK.md`).
7. Smaller items: two gaps in the record to Cowork (39302d3 told nobody; C5's termbase row has no done line); one
   time later than its commit; the misspelt tag "[West Ouhueri]"; and six closed cloud gates that no longer hold.

## Verdict lines as printed

srom-produkcja, `python3 .claude/skills/srom-produkcja/tests/run_all.py` (from `srom-produkcja/`), commit 39302d3,
Python 3.13.16, pandoc 3.9 (tail):
```
ok   test_quant.py: QUANT ALL PASS 42/42
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 12/12
SUITE ALL PASS 26/26
```
(`test_install.py: INSTALL ALL PASS 0/0 (no InDesign here: SKIP)`.)

srom-tlumacz, the four checks of its CLAUDE.md, run with `python3` and the root `.claude/skills/srom-tlumacz/scripts/`
(no venv in the cloud), against srom-produkcja 39302d3:
```
shape: 40 rows, 0 problem(s)            (check_tb --schema --shape --vocab --precedent --evidence: exit 0)
training quotes verified: 25/25
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 33/33
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```
`tlumacz-draft_check.py --selftest`: `selftest: 8/8 negative controls caught` (K9's count).

Texts, on scratch copies of `srom-tlumacz/work/<id>/` (Code's reference copies; SYS-9 (a): the live texts are
Cowork's):

| text | `src/` = srom-produkcja's frozen files; manifest | sha256 = last T-item | pair | `--draft` build | final build | front | Word import → pair |
|---|---|---|---|---|---|---|---|
| ndiaye | identical; 4/4 OK | refs 6a058001…8ad988a (T34) | CHECK OK | PASS | FAIL: not normalised (8× INITIALS, 1× NOTE-FULLSTOP) | FRONT OK | v1 and v2: CHECK OK |
| ostendorf | identical; 4/4 OK | refs 8958c705…30f09ce (T34) | CHECK OK | PASS | FAIL: not normalised (9× NOTE-FULLSTOP) + `[BRAK MIEJSCA]`, `[BRAK WYDAWCY]` | FRONT OK | CHECK OK |
| pahulich | identical; 4/4 OK | refs 3b060a87…1f3d5366 (T32) | CHECK OK | PASS | FAIL: `[BRAK MIEJSCA]` nn. 47, 145 only | FRONT OK | CHECK OK |
| tittel | identical; 4/4 OK | refs 71181a9a…2b320d9 (T36) | CHECK OK | PASS | FAIL: `[BRAK WYDAWCY]` n. 20 only | FRONT OK | CHECK OK |

(`<id>_queries.md` in `src/` is the frozen copy of the notes sheet; srom-produkcja's is now `<id>_uwagi.md`, as
intended. Build report: `linter … (Kanon v1.16)`.)

`mutate_keyed.py` on copies (GATES.md CHECK commands): `tittel: MUTATIONS CAUGHT 40/40`, `ostendorf: 40/40`,
`scheffknecht: 40/40`, `westohueri: 40/40`, `ndiaye: 40/40`.

`normalize.py` on copies of the two drafts: `ndiaye: 9 changes, 1 flags` (flag: `L172 DOUBLE-MARKER: [^49][^t1]`);
`ostendorf: 9 changes, 0 flags`.

Delivered texts: none in the repository (no delivery line; Code has no `STATUS.md`). `srom-produkcja/work/ostendorf/pl/`
holds the 02.10 INJECT-test copy: `sha256sum -c SHA256SUMS` 5/5 OK, older than the current draft. It is not a delivery.

Other measurements:
- `validate_master.py volumes/18/srom_master_v3.csv` (copy): exit 1, 41 blocking errors: `pub_date_online
  '2025-12-TODO'` ×15, `license` and `license_url` `'TODO'` ×13 each.
- `python3 _cloud/check_pins.py`: `PINS DIFFER … found {python-docx 1.2.0, lxml 6.1.3, PyMuPDF 1.28.2, pikepdf 10.16.0} / []`
  (no source to compare with in the cloud).
- `pip download pikepdf==10.16.0 --python-version 3.10`: `10.16.0 Requires-Python >=3.11` (also 10.14.0, 10.15.0);
  `pikepdf==10.13.0.post1`: wheels saved for cp310 and cp313. `test_quant.py` with pikepdf 10.13.0.post1 (scratch venv,
  Python 3.13): `QUANT ALL PASS 42/42`.
- `git cat-file -t` after `git fetch --unshallow`: 2cfbeff, e079042, 542dacf, 593440d, 6f470d5, c52ed2f, b653484,
  eb4d3e1, 4f00cb1, aa1096b, ffeaf34 → `Not a valid object name`; aa56f38, 74449fc, cb3cfe5, 48982d1, fa0d755, df9da77
  → `commit`.

## Findings

| # | finding | evidence | severity | who fixes it | label |
|---|---|---|---|---|---|
| 1 | INJECT has no normalise step, but the final build fails on text `normalize.py` would change (since 48982d1, 04.10 02:34). The contract builds straight from `pl/`; SKILL.md says "→ 2 →" (normalise in place) on copies that are "never edited". A normaliser flag (DOUBLE-MARKER) can only be fixed in the Word master, i.e. by a new delivery. | `handoff.md:83-89, 105`; `stages.md:50-60` (Pass: take-back, then build without `--draft`); `SKILL.md:75`; `build.py:881-891`; Ndiaye and Ostendorf final builds above | will bite (first INJECT of a translated text) | srom-produkcja (contract and test); srom-tlumacz if the contract text its test checks changes | repo-only confirmed (the per-text counts come from Code's copies: may depend on Mac/Cowork state) |
| 2 | `srom-produkcja/requirements.txt` has no pikepdf. Cowork installs from it (`sh srom-produkcja/setup.sh`, C3/C4). `test_quant.py` imports pikepdf at the top and `cover_page.py:318-321` aborts without it. The Mac/cloud pin 10.16.0 needs Python ≥ 3.11; Cowork's VM is 3.10.12 (C3); the file promises ≥ 3.10. K10 passed the line to Cowork ("your requirements.txt"), but the file is Code's. | `requirements.txt:1-5`; pip measurements above; `test_quant` 42/42 with 10.13.0.post1 | will bite (the next fresh Cowork VM: suite fails, no cover pages) | srom-produkcja | repo-only confirmed (impact may depend on Mac/Cowork state: the VM that ran the C6 prototype has some pikepdf) |
| 3 | `_cloud/check_pins.py` compares with Cowork's retired `plugin/srom/requirements.txt` (moved to `dump/` 04.10, C3). In the cloud it finds no source and exits 1. On the Mac it compares only with the venv, so it cannot see finding 2. Gate G3 of `_cloud/GATES.md` fails here. | `check_pins.py:7`; run above | will bite (the guard for 2 is blind) | srom-produkcja with 2 (it already maintains these pins: 07699c7); `_cloud/` is root's | repo-only confirmed |
| 4 | Handovers and CLAUDE.md files stale since SYS-9 (a), the one repository and 06.10 | `srom-produkcja/docs/HANDOVER-produkcja.md:1` ("state at 02.10.2026"), `:4` (ledger in Code), `:28` (24/24); unchanged since 48982d1. `srom-produkcja/CLAUDE.md:4` ("Three skills": six), `:13` (srom-tlumacz "not a skill here, packaging deferred": a skill since 03.10, E20), `:44` (question IDs in `MB-decisions.md`). `srom-tlumacz/HANDOVER.md:12` (9 PROVISIONAL: now 10, C-0050), `:55-76` (ledger in Code; drafts in Code's `work/`; West Ohueri "not started": Cowork has a draft, C5). `srom-tlumacz/CLAUDE.md:40` ("this folder is a git repository", `.gitignore`). No PLAN status line for a414512 (K9). | will bite (a new module session starts from these) | srom-produkcja, srom-tlumacz | repo-only confirmed |
| 5 | 11 hashes cited in K3, K6, K7 and the T37 status lines do not resolve in `blessero/srom-cloud`. They were made in the old module repos between the first export (04.10 21:42) and the move (05.10 00:31) and came over only as snapshots. Root CLAUDE.md § Cloud sessions says "Hashes cited in handoff items resolve". This pass could not verify K6/T37 by hash. | `git cat-file` above; snapshots 258ae9e (2cfbeff, aa1096b, ffeaf34), ff44289 (e079042, 4f00cb1), 73d9638 (6f470d5, b653484, eb4d3e1); `_cloud/README.md` § 1 step 4 (`.old` kept a week) | will bite (once `.old` is deleted, ~12.10) | MB (choose), then root | repo-only confirmed that they don't resolve; whether `.old` still exists may depend on Mac/Cowork state |
| 6 | The checkup procedure assumes the pre-05.10 world: "three repos", `git -C _handoffs`, texts "one section per text in MB-decisions.md", § 6 ledger checks, `~/.claude/skills` links. Code's ledger is a pointer, and the live texts and `STATUS.md` are Cowork's (`checkup/COWORK.md` steps 4–5 already check them). As written, a full Code checkup re-checks reference copies. | `checkup/SKILL.md:19, 38, 62-66, 74-76, 86` | will bite (the next full checkup) | root (MB approves: a skill change) | repo-only confirmed |
| 7 | Gaps in the record to Cowork: (a) 39302d3 found K6's "knowledge-base patch is in" incomplete (the Scope line was missing) and srom-zizek's link to the knowledge base broken since the switch. It fixed both and added `test_kb.py` (suite 25 → 26), but sent no K-item; root CLAUDE.md § Cowork asks for one when a test count changes. (b) C5's first item (termbase row C-0050) has no done line: K8 says "not done", 20f4f26 committed it later. | `git show 39302d3`; `code-to-cowork.md:132-147` | cosmetic | srom-produkcja (a), srom-tlumacz (b) | repo-only confirmed |
| 8 | K8–K11 have no answer from Cowork in the repository (C6, 17:40, came after K8 and K9 and does not mention them) | `cowork-to-code.md` ends at C6 | cosmetic | Cowork; a Mac session pushes its file | may depend on Mac/Cowork state |
| 9 | Times and tags: K8 says 15:52, its commit adc86d1 is 15:51:41; K8 and commits 1113fec, adc86d1 tag the text "[West Ouhueri]" (README: West Ohueri); K3's heading reads "(04.10.2026 04.10.2026 21:46)" | `code-to-cowork.md:64, 132`; `git log` | cosmetic | srom-produkcja (one correction line, as T21 did) | repo-only confirmed |
| 10 | `_cloud/GATES.md`: closed gates G2, G3, G5, G7, G8, G9 no longer hold (`test_roundtrip.py` and `cowork_sync.py` retired, the mirror replaced by the repository, G7 tests `MB-decisions.md`, a file meant to change), and there are no NOTE lines | `_cloud/GATES.md`; `ls` of the tools: not found | cosmetic | root | repo-only confirmed |
| 11 | Ownership and leftovers: 07699c7 (srom-produkcja) edited root's `_cloud/check_pins.py` and `_cloud/setup-cloud.sh` (sensible, announced in K10). Unused: `srom-produkcja/srom-typeset.skill`, `srom-kanon.skill` (old dist copies, ignored before the move), `_handoffs/curator-update-2026-09-27/`; merged session branches `claude/lucid-lovelace-qcgsgi`, `claude/vibrant-mccarthy-lnarty` on the remote. | `git show --stat 07699c7`; `ls`; `git ls-remote` | cosmetic | MB (delete or keep; a rule if modules may edit `_cloud/` pins) | repo-only confirmed |
| 12 | The vol. 18 master CSV (Cowork's minted copy, f109090) is not deposit-ready: no online publication date (15 rows) and no licence (13 rows); the licence policy is listed as open in srom-kanon `SKILL.md` ("Open — do not invent") | `validate_master.py` above | blocks (the Crossref deposit and the website import of vol. 18) | MB | may depend on Mac/Cowork state (Cowork's copy or ledger may be ahead) |

Not findings (checked, fine): Kanon v1.16 in the header, the last § 17 row, RULES.md, srom-kanon SKILL.md and the build
report; every `§ n.n` in the skills is a Kanon heading (67 headings, 0 unresolved); srom-kanon SKILL.md's quick rules
read against v1.16: no contradiction found; no new E-items, so no new group names; no duplicate C/K IDs; root
`.claude/skills/` links resolve (8 skills); module hooks point at existing files; all module commits since the last
review stay inside their folders and `_handoffs/`, except finding 11.

## Last review's findings

Review 04.10.2026-2:
- Row 1 / items 1–5 (Cowork's skill edits into Code): done (e079042, 542dacf; status lines `produkcja-to-tlumacz.md:705`,
  `tlumacz-to-produkcja.md:280`). The knowledge-base Scope line and the srom-zizek link were completed only on
  06.10.2026 22:01 (39302d3); see finding 7.
- Item 6 (srom-zizek `cards/` kept out): reversed in 39302d3 (`assets/template/cards/.gitkeep`), with a reason:
  `srom-zizek/SKILL.md:69` copies the template "with an empty `cards/`". Accept.
- Item 7 (`cowork_sync.py` § 2 = 0): the tool was retired (K7); nothing to measure.
- Item 8 (K-item to switch): done, K6; Cowork switched (C3).

Review 04.10.2026: all rows done (status lines of 04.10 21:45 and 21:47; K2, K3; C1).

## For srom-produkcja

*Proposed; the next full pass confirms before a module applies it.*

1. **Normalise at INJECT without editing `pl/`** (finding 1). Cheapest version: `normalize.py pl/<id>_pl.md -o
   build/<id>_pl.md --log build/<id>_norm.md`, then build from `build/<id>_pl.md`. Write that step into
   `references/handoff.md` (Back item 4, line 89, and the command block, line 105), `references/stages.md` § 3 (Output
   and Pass, lines 54–60) and `SKILL.md` scenario C (line 75). Say where a normaliser flag goes (the notes sheet,
   then the Word master and a new delivery: the md is never edited by hand). Add a case to `test_takeback.py`:
   take-back → normalise → build without `--draft` → PASS on a delivery that needs NOTE-FULLSTOP. Verify: suite all
   pass. If the wording of `handoff.md` that srom-tlumacz's test checks changes, write a T-item (contract change:
   both sides' tests).
2. **pikepdf for Cowork** (findings 2, 3). Cheapest version: in `requirements.txt` two lines with markers,
   `pikepdf==10.16.0; python_version >= "3.11"` and `pikepdf==10.13.0.post1; python_version < "3.11"` (10.13.0.post1
   passed test_quant 42/42 here). Alternatively pin 10.13.0.post1 everywhere (Mac venv, `_cloud/setup-cloud.sh`, this
   file), which is simpler to check but changes the Mac venv. Then point `_cloud/check_pins.py:7` at
   `srom-produkcja/requirements.txt` (relative to the repository) instead of the retired plugin path, so the check
   runs in the cloud too and compares with what Cowork installs. Make the abort hint in `cover_page.py:321`
   environment-neutral ("pip install -r srom-produkcja/requirements.txt"). Verify: `python3 _cloud/check_pins.py` →
   PINS OK in the cloud; suite all pass. Tell Cowork in a K-item: the commit, and to re-run `setup.sh` then the
   preflight.
3. **Stale text** (finding 4): `docs/HANDOVER-produkcja.md` (state date, start sequence = root CLAUDE.md § Start and
   § Cowork, suite count, a short § for 04–06.10: SYS-9/10, `stages.md`, knowledge base, one repository, C5/C6 work);
   `CLAUDE.md:4, 13, 44`. Verify by reading.
4. **K-item** (finding 7a): 39302d3: the knowledge-base Scope line and srom-zizek's link fixed, `test_kb.py`, suite
   26/26, plus the commits of items 1–2. One item is enough.
5. **Correction line** (finding 9) under K8: time 15:51, tag [West Ohueri]. Append it; never rewrite.

## For srom-tlumacz

*Proposed; the next full pass confirms before a module applies it.*

1. **Stale text** (finding 4): `HANDOVER.md:12` (termbase counts), § 6–7 (`:55-76`): the ledger is Cowork's
   (questions as K-items "needs MB"); the drafts in `work/` are reference copies (SYS-9 (a)); West Ohueri is being
   drafted in Cowork. `CLAUDE.md:40` (one repository since 05.10; `.gitignore.module` inactive). One PLAN status line
   for a414512 (K9). Verify by reading.
2. **Done line for C5's termbase row** (finding 7b) in `code-to-cowork.md`: C-0050 committed in 20f4f26, check_tb
   40 rows, 0 problems (re-run it).
3. If srom-produkcja's item 1 changes the `handoff.md` wording your test checks: take its T-item, HANDOFF CONTRACT
   n/n.

## For MB

In the order to decide:

1. **Claim the cloud credit by 07.10.2026, 23:59 US Pacific**, if not done yet (`_cloud/README.md` § 3). It is
   tomorrow.
   Run with: Haiku · low effort — one slash command (`claude`, then `/claim-credit`); the model does not matter.
2. **Keep the old commit hashes before deleting `SROM edit and trans.old`?** (finding 5). (a) **recommended,
   cheapest:** one line in the root CLAUDE.md § Cloud sessions mapping the eleven hashes to their export snapshots
   (2 minutes, root session). (b) Before deleting `.old`, push the old module heads to GitHub as tags (a few
   commands on the Mac; keeps the full history). (c) Nothing: K6/T37 stay verifiable only by their content.
   Run with: Sonnet · low effort — one line of text, or a few git commands, fully specified here.
3. **Licence and online date for vol. 18** (finding 12): the deposit needs both. The licence policy is an open
   question in srom-kanon. If Cowork's ledger does not have it yet, it is one question there.
   Run with: Opus · high effort — Crossref/CSV work in Cowork, after your decision.
4. **Update the checkup** (finding 6): Code's checkup keeps tests, contract, Kanon, gates, hygiene and the channel;
   texts, `STATUS.md` and the ledger go to Cowork's checkup. Cheapest: trim `checkup/SKILL.md` steps 2 and 6 to
   "see COWORK.md" and fix the repository wording (root session).
   Run with: Opus · xhigh effort — changing a skill that every review depends on.
5. **Leftovers** (finding 11): delete the two old `.skill` files, `_handoffs/curator-update-2026-09-27/` and the two
   merged session branches? (Recommended: yes; a root session does it in a minute.) And may modules update the pins
   in `_cloud/`? (Recommended: yes, `setup-cloud.sh` and `check_pins.py` only, with the module's suite run.)
   Run with: Haiku · low effort — deleting listed files.
6. Then the full checkup on the Mac (below).
   Run with: Opus · xhigh effort — a system-wide audit across Code and Cowork.

Also pending from earlier, not checkable here: saving the srom-naczelny card without the `setup_font.sh` call (C3
item 7, C4).

## Checks not run (for the next pass)

- **Cowork:** `STATUS.md` hand-off log (sha256 of every hand-over and delivery against the files); Cowork's texts
  (the live drafts, West Ohueri and Scheffknecht included, any editing round after 04.10); Cowork's `MB-decisions.md`
  (pending only, "At a glance", "Next free", Detail files, nothing decided elsewhere, K11 entered); the desk sync;
  C-items written but not pushed (K8–K11 answers); srom-naczelny's current text; whether Cowork's VM has pikepdf and
  which version.
- **Mac:** `~/.claude/skills/srom-*` and `srom-quant` symlinks; `dist/*.skill` freshness (`dist/` is not in git);
  `check_pins.py` against the venv; the venv's own suite run (here: system Python 3.13, pandoc 3.9 vs the Mac's
  3.8.3); `SROM edit and trans.old` and the old module repositories (finding 5); `mb_view.py --all` and the hooks;
  the backup (G1).
- **InDesign / Word:** `test_install.py` skipped (0/0); the INJECT layouts and G12; the full vol. 18 volume repair
  (K10: 72 MB PDF, 12,005 → ~60 U+FFFD, a Mac run); Word copies were imported with `docx_in.py` only, never opened.
- **Python 3.10** (Cowork's version): no interpreter here; the 3.10 claim rests on pip's metadata and the cp310 wheel.
- **Network lookups** (`lookup.py dois/imprints`, Crossref): not needed for this pass, not run.
- **Gates:** no gate in `srom-produkcja/GATES.md` or `srom-tlumacz/tlumacz-gates-*.md` was closed since the last
  review; `_cloud/GATES.md` G1 and G9 need the Mac.
- **K-item to Cowork:** a checkup normally ends with one for Cowork's findings. Not written, since this is a draft
  (finding 8 is the only Cowork row).
