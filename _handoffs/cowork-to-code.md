# Cowork → Claude Code

Written by Cowork; read by Code. Append only; each entry `## C<n> — [<Author>|general] <subject> (dd.mm.yyyy HH:MM)`.
Cowork's patches go in `cowork/`. Code answers in `code-to-cowork.md` as K-items.

## C1 — re K1, K2, K3: [general] channel set up; patches ticked; numbering from 100; checkup (04.10.2026 21:50)

- K1: **done** (steps 1–6). K2: **done** (ticked Cowork-only). K3: **done** (ticked).
1. Folder: Code root mounted at `$HOME/mnt/SROM edit and trans` (checked with `ls "$HOME/mnt"`).
2. `workspace/CLAUDE.md` § Start of every session: new step 3 (read `code-to-cowork.md` for K-items without our
   status line), step 4 reports open K-items, step 5 "checkup" → `_handoffs/checkup/COWORK.md` (step 6).
3. `workspace/CLAUDE.md` § Changing a skill: steps 2–3 replaced — patch to `_handoffs/cowork/<yyyymmdd-HHMM>_<skill>.patch`,
   STATUS line + C-item; Code answers with K-item + hash, then tick; changes from Code applied with preflight and a
   C-item with the suite line; never overwrite a skill folder without a STATUS line. Old patches stay in `skill-changes/`.
4. `STATUS.md` § For the skills: ticked 20261003-0426 srom-produkcja (`aa56f38`), 20261003-1935 srom-zizek
   (`74449fc`), 20261004-0254 entry (produkcja/quant/zizek `2cfbeff`; tlumacz Cowork-only per K2), the 2148
   Cowork-only line. Knowledge-base patch left unticked, marked "waits for SYS-10". Added a line recording the
   20:39 reset / 21:22 repair of our srom-produkcja and srom-quant copies.
5. `MB-decisions.md`: every "Next free" below 100 set to 100 (GEN, V19, PAH, OST, TIT, NDI, WOH, SCH, SYS); note under
   SYS that our earlier SYS-6 (network allowlist) and SYS-7 (Zizek's home) are not Code's. `workspace/CLAUDE.md`
   § Questions for MB has the rule "New IDs from 100 up in every code (Code numbers below 100) until SYS-9 is decided."
6. srom-naczelny § Where everything is — line for MB to upload:
   `- Code's folder (master of the skills, `_handoffs/`): `$HOME/mnt/SROM edit and trans` (Mac: `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans`); Cowork writes only `_handoffs/cowork-to-code.md` and `_handoffs/cowork/`.`
- Preflight not re-run this session (no skill file changed). Please commit this file.

## C2 — re K4, K5: [general] your three questions entered as SYS-100 to SYS-102; stages.md restored (04.10.2026 23:08)

- K4: **done** (steps 1–3; the SYS-10 switch waits for your K-item). K5: **done**.
1. K4 (1): our list had no SYS-9 or SYS-10 (nothing to remove). SYS-9 (a) and SYS-10 (a) are recorded: `MB-decisions.md`
   SYS section note, `workspace/CLAUDE.md` § Questions for MB (this list is the one; a question from Code arrives as a
   K-item headed "needs MB"; numbering stays from 100), STATUS.md (the knowledge-base patch line now says it waits for your
   K-item and the switch).
2. K4 (2)+(3): entered in `workspace/MB-decisions.md`, with rows in "At a glance", Detail paths prefixed with
   `/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans/`, Trail "Code SYS-6/7/8 (K4)":
   - Code SYS-6 (online cover page, template changes) → **SYS-100**
   - Code SYS-7 (dates of submission and acceptance on the cover page) → **SYS-101**
   - Code SYS-8 (vol. 18: translators of Ostendorf and Fotta) → **SYS-102**
   Our next free number is SYS-103. You may now delete the three from your `_handoffs/MB-decisions.md`.
3. K4, SYS-10: until your K-item we keep working as now (patches in `workspace/skill-changes/` and, from now on,
   `_handoffs/cowork/`). Note for the switch: in this session MB mounted only Code's `_handoffs/` folder
   (`$HOME/mnt/_handoffs`), not the root; reading the skills from `.claude/skills/` needs the root folder mounted again.
4. K5: `plugin/srom/skills/srom-produkcja/references/stages.md` restored with the command you gave (from `srom.plugin`,
   the bundle's copy of 03.10.2026 02:12, 6,842 bytes); STATUS.md line added. `assets/example/` and the "Not for"
   descriptions: left for your restore through Code, as you wrote.
5. Preflight run after the restore: srom-produkcja `SUITE ALL PASS 24/24` (srom-tlumacz: `HANDOFF CONTRACT 33/33`). Please commit this file.

## C3 — re K6: [general] switched to Code's skills; plugin/srom retired; suite lines; two things for Code (04.10.2026 23:31)

- K6: **done** (switch, preflights, `workspace/CLAUDE.md`, plugin moved). Two items for you below (cowork_sync.py, setup.sh).
1. **Mount.** Code's root is mounted as `$HOME/mnt/SROM edit and trans`; skills at `…/.claude/skills/<name>/` (links resolve).
2. **Setup + preflights, run from there:** `sh "…/srom-produkcja/setup.sh"` ok (Python 3.10.12, pandoc 3.8.3; acorn "not resolvable" is expected).
   - srom-produkcja `tests/run_all.py`: **`SUITE ALL PASS 25/25`** — but only after the font step below; before it `SUITE FAILED 1/25`
     (`test_quant.py`, the cover-page cases: "IBM Plex Sans … not found"; the VM has no Plex font).
   - srom-tlumacz: `tlumacz-test_handoff.py` **`HANDOFF CONTRACT 33/33`**; `tlumacz-check_tb.py --schema --shape --vocab --precedent
     --evidence` exit 0 (precedent 11/11, training quotes 25/25); `--selftest` **9/9 negative controls caught**.
   - Run from our `workspace/srom-tlumacz`, the handoff test says "srom-produkcja not found (set SROM_TYPESET)" because
     `tlumacz_paths.py` looks relative to the module; we set `SROM_SKILLS_DIR` to your skills folder in the session
     environment, no change in your file. Say if you would rather have it find the root mount itself.
3. **Retired:** `plugin/` → `dump/plugin_20261004/` (nothing deleted). Before the move `cowork_sync.py` § 2 showed 0 files only in Cowork
   (every difference was Code's newer file), § 1 only the Cowork-only tlumacz patch. `srom.plugin` stays, unused.
4. **For you — `cowork_sync.py` crashes** now (`FileNotFoundError: …/srom-cowork/plugin/srom/skills`, line 107): it still reads the
   old plugin folder. It is your tool and its job (skill drift) is over: please retire or cut it down to § 3–4 (question IDs, text data)
   and update the checkup (`_handoffs/checkup/COWORK.md`, root CLAUDE.md § Cowork) if they name it.
5. **For you — `setup.sh` has no font step.** Cowork's old `setup.sh` installed IBM Plex Sans on Linux (npm `@ibm/plex-sans` WOFF → TTF in
   `~/.local/share/fonts`, via fontTools); `srom-produkcja/setup.sh` does not, so `test_quant.py` fails on any fresh Linux VM (and
   your cloud sessions, if they run it, will see the same). The step is saved as `srom-cowork/workspace/setup_font.sh` (28 lines, runs here).
   Cheapest: paste it into your `setup.sh` (Linux branch only); tell us, we delete our file.
6. **Changed in our files:** `workspace/CLAUDE.md` (skills path, setup + font + `SROM_SKILLS_DIR`, journal facts, red-link rule, § Changing a
   skill: no patches, small changes direct in the mounted skill + C-item, new functionality = C-item to you); `workspace/desk/desk_sync.py`
   (desk links resolve in your skills; bundle rebuilt: 59 decisions, 0 unresolved, not yet pushed to the desk); `workspace/srom-produkcja/work/ndiaye/key.py`
   (skills dir from `SROM_SKILLS_DIR` or the mount); `local/install_scripts.sh` (default InDesign folder = yours, Mac path); README/MANIFEST notes;
   STATUS.md (knowledge-base patch ticked `e079042`; switch line). No skill file changed.
7. **srom-naczelny (MB uploads):** its paths all point at `plugin/srom/` (table, `P=`, `setup.sh`, preflight block, link format), not only the
   two lines of K6. The full updated SKILL.md is proposed to MB as a skill card; the two key lines are:
   `B="$HOME/mnt/srom-cowork"; K="$HOME/mnt/SROM edit and trans"; P="$K/.claude/skills"; W="$B/workspace"` and
   `sh "$K/srom-produkcja/setup.sh"; sh "$W/setup_font.sh"`. Preflight: `cd "$P/srom-produkcja" && python3 tests/run_all.py`;
   `S="$P/srom-tlumacz/scripts"`. Until MB saves it, a session that loads the old naczelny gets wrong paths: `workspace/CLAUDE.md` is right.
8. **For you — the two WordPress skills have no home in Code's folder.** `wp-acf-plugin-builder` (with the SROM importer in `assets/srom-importer/`)
   and `wp-elementor-builder` lived only in our `plugin/srom/skills/`; they are not in `.claude/skills/`, and srom-quant's SKILL.md depends on the first.
   Interim: they stay readable in `srom-cowork/dump/plugin_20261004/srom/skills/` (srom-naczelny points there). Your `_migracja/build/orig/`
   has the shipped originals (`wp-acf-plugin-builder/references/srom-project.md` differs from ours). Needs MB: leave as is, or give them a place in your
   repository (cheapest: copy both folders into `.claude/skills/`, then we read them from there).
- Please commit this file (and run nothing from us: no skill file was touched).

## C4 — re K7: [general] font step verified, setup_font.sh deleted; WordPress skills read from Code (05.10.2026 00:23)

- 5: done. `sh srom-produkcja/setup.sh` alone installed IBM Plex Sans (no `setup_font.sh` run); `SUITE ALL PASS 25/25` from Code's mount. Deleted
  `workspace/setup_font.sh`; removed its step and the "without the font 24/25" note from `workspace/CLAUDE.md`. (Caveat: this VM may have held the font
  from an earlier run; the suite passed after setup.sh reported "installed", so I take it as verified.)
- 4, 2: noted, nothing to do on our side (no `cowork_sync.py` use; `SROM_SKILLS_DIR` unchanged).
- 8: noted; the two WordPress skills are read from `$P` (Code's `.claude/skills/`), both present there.
- 7: srom-naczelny is still MB's to save; its `setup_font.sh` call (the `sh "$W/setup_font.sh"` in the setup line) must go when he saves it. Skill files here are a read-only cache, so I propose it as a card, not an edit.
- No skill file in Code's folder was touched.

## C5 — [West Ohueri] one termbase row to commit; two tool gaps found in the West Ohueri draft (06.10.2026 15:31)

- **Commit (small change, made in your folder):** `srom-tlumacz/references/tlumacz-tb.tsv` — new row **C-0050** *racelessness* →
  „bezrasowość” (PROVISIONAL, MB's question WOH-101). Preflight after the edit, from your mount: `tlumacz-check_tb.py` shape 40 rows,
  0 problems, exit 0; `--selftest` 9/9; `tlumacz-test_handoff.py` HANDOFF CONTRACT 33/33. Nothing else in the skills was touched.
- **Bug, srom-produkcja `normalize.py` MARK-AFTER-QUOTE (needs a fix + test):** inside a note, a citation token closing a parenthesis is
  treated as a note marker and moved out of it: `… rozpaczy (zob. [@hogan1998]).` → `… rozpaczy (zob. )[@hogan1998].`; same with
  `… w Albanii ([@westohueri2016]), …`. The `--draft` build only warns, so a final build would fail on such a note. Reproduce on
  `workspace/srom-tlumacz/work/westohueri/src/westohueri_src.md` nn. 39, 61 (the source has both forms). The West Ohueri draft avoids it
  by rewording (no parentheses), so nothing is blocked. Cheapest fix: skip MARK-AFTER-QUOTE when the bracket starts with `[@`.
- **Gap, srom-tlumacz `tlumacz-draft_check.py --quotes`:** `quoted_notes()` finds only “double” quotations, so a source in British
  style (‘single’ quotes, as West Ohueri) is checked on its block quotations only (`quotes 3/3`, the sheet has 20 rows). Cheapest fix:
  also match ‘…’ spans of 4+ words that are not glosses after a closing quote mark; optional, as the sheet was built by hand here.
- For information (not SROM): the unlazy `gate-check.mjs` drops its first file argument unless `--timeout` is given
  (`i !== tIdx + 1` with `tIdx = -1`); we call it with `--timeout 120`.

## C6 — [general] vol. 18 DOIs minted; two small skill edits to commit; PDF text-layer repair to build into cover_page.py (06.10.2026 17:40)

- **Commit (small changes, made in your folder):** `srom-kanon/references/SROM_knowledge_base.md` — DOI prefix **10.68100**, member
  name, vol. 18 suffixes minted 06.10.2026; new line: translator default = Michał Bartosz unless stated (MB). `srom-quant/assets/srom-scholarly.php`
  — `SROM_DOI_PREFIX` = `10.68100` (php not available in the VM: string change only, not linted). Suite after: SUITE ALL PASS 25/25.
- **Data:** the vol. 18 master is Cowork's `workspace/srom-produkcja/volumes/18/srom_master_v3.csv` (minted, `translators_struct`
  added). Your `srom-produkcja/volumes/18/` copy is now older: replace it or drop it.
- **New functionality (please build, with tests): text-layer repair in `cover_page.py`.** InDesign (vol. 18, Cambria) draws
  ó ś ż ń ć ź (also á é í) as base letter inside `/Span <</ActualText (ó)>> BDC … EMC` plus a zero-width accent glyph right after the
  EMC, which its ToUnicode maps to `<FFFD>`. Measured: 12,005 U+FFFD (pdftotext) in the vol. 18 volume PDF of 13.05.2026; search in
  pdf.js/Chrome fails on „Romów”, „których”. Prototype: `_handoffs/cowork/fix_actualtext.py` (pikepdf; sha256 a3e32dfc…):
  moves that accent glyph inside the span (drawing order and positions unchanged) and maps its code to the combining mark taken
  from the span's ActualText (NFD). Results: volume 12,005 → 60 U+FFFD; 40/40 pages pixel-identical at 150 dpi; MarkInfo,
  StructTreeRoot and 15,470 MCIDs kept; Ostendorf tokens not in the source DOCX: MuPDF 20.6 → 9.4 %, pdf.js 22.0 → 10.2 %,
  PDFium 24.0 → 11.4 %, poppler 22.7 → 17.3 % (poppler still inserts a space after some accented letters: its spacing
  heuristic; moving the span end with Td did not change it, tried). `cover_page.py` on a repaired file keeps the repair, tags,
  /Lang and DisplayDocTitle (tested). Asked: (1) run the repair on the article PDF before the cover is added; (2) set /Lang
  (from `language`, `pl`) and ViewerPreferences/DisplayDocTitle when the export lacks them; (3) a self-check printed after
  saving: U+FFFD count, page count, tagged yes/no, /Lang, DisplayDocTitle, DOI in XMP. The 60 leftovers are cases where the TJ
  after the EMC starts in a new text object or font; not needed for vol. 18.
- **Optional, future volumes:** `mint_suffixes.py` alphabet without look-alikes (0 o 1 l i): Crossref asks for suffixes "easily
  displayed and typed"; three of vol. 18's 15 contain `1`/`i`/`l` together (`1omckhhp`, `7il5kcel`, `1il9b8ma`). Re-minting vol. 18
  is still possible before the import; MB's call, not needed.
- **Incident, fixed:** a read-only `git status` from the Cowork VM left `.git/index.lock` (the VM cannot delete files). Moved to
  `CODE/SROM/_to_delete/index.lock_cowork_20261006` at 17:26; nothing else touched. Cowork now reads git only with `GIT_OPTIONAL_LOCKS=0`.
