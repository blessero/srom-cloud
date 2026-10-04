# Review — [general] 04.10.2026 (22:30): one copy of the skills (SYS-10 (a))

Not a checkup: the work order for SYS-10 (a) and SYS-9 (a), decided by MB 04.10.2026 (K4, root CLAUDE.md § Cowork).

## Conclusions

1. Cowork makes the journal (texts, volume data, STATUS.md, MB's one ledger); Code builds and tests the skills.
2. The skills will exist once, in Code. Cowork's copy (`/Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork/plugin/srom/`)
   carries edits Code never took (from the 03.10 packing, L1–L5 of `_migracja/PLAN.md`); they come into Code now, and
   then Cowork reads the skills from Code's folder: no copy, no patches, nothing to sync.
3. The rule for every file: **the skill says what to do; how this environment does it lives outside the skill**
   (Code: CLAUDE.md files and `_handoffs/`; Cowork: srom-naczelny and its `workspace/CLAUDE.md`). Where one wording fits
   both, use it; where the environments really differ (a path, a shell limit), say both in one line.
4. Stage records: since the texts live in Cowork, the record of a hand-over between stages is the `STATUS.md`
   hand-off log (Cowork's form). E/T items stay for news about the tools between Code's modules.

## Verdict lines as printed

At 22:35: `cowork_sync.py` § 2 — srom-produkcja 0, srom-quant 0, srom-zizek 0 (Cowork's copies of these were
replaced by Code's at 20:39, so the bundle's edits are gone there too); srom-kanon 1 differ + 3 only in Cowork;
srom-tlumacz 5 differ + 5 only in Cowork. Target after the work: all 0, with the bundle's edits in.

## Findings

| # | finding | evidence | severity | who fixes it |
|---|---|---|---|---|
| 1 | Cowork's copy has the knowledge base, `stages.md`, examples, "Not for" descriptions, setup files; Code has none | `cowork_sync.py` § 2; `plugin/srom/` | will bite | srom-produkcja, srom-tlumacz |

## Last review's findings

Review 04.10.2026: all rows done (status lines 21:45 and 21:47; Cowork's C1 21:50).

## For srom-produkcja

Source: the bundle as shipped, `_migracja/build/srom-cowork/plugin/srom/` (Cowork's live copy lost the srom-produkcja
and srom-quant edits when it was reset at 20:39: no `stages.md`, no examples, Code's descriptions), and Cowork's live
copy for srom-kanon. Read each file against yours; take the better text; never take a Cowork-only mechanic
(`device_bash`, the desk, `$HOME/mnt`). Work locally: `_migracja/build/` is not in the cloud mirror.
1. `SROM_knowledge_base.md` → `srom-kanon/references/SROM_knowledge_base.md`. Every skill names it as "srom-kanon's
   `references/SROM_knowledge_base.md`" (no `../../` path: the skills sit in two repositories here and in one folder
   in Cowork). Journal facts left in a SKILL.md or reference move into it.
2. `srom-produkcja/references/stages.md` (the one stage-gate spec) and the hand-off log format in it; `handoff.md`
   points to it for stage records and keeps E/T items for tool news only. Both contract tests follow (suite here,
   `tlumacz-test_handoff.py` there: tell srom-tlumacz in a T-item what changed).
3. `assets/example/` of srom-produkcja, srom-kanon, srom-quant, with their expected outputs; one test in the suite that
   rebuilds each example and compares (the bundle's checker: `_migracja/tools/check_examples.py`).
4. The "Not for …" ending of each description (srom-produkcja, srom-kanon, srom-quant, srom-zizek; ≤ 1024 chars).
5. `setup.sh` and `requirements.txt` → `srom-produkcja/setup.sh`, `srom-produkcja/requirements.txt` (pins = the venv).
6. srom-zizek: the empty `assets/template/cards/` folder is Cowork's; keep it out unless a file needs it.
7. Verify: suite all pass; `python3 _handoffs/tools/cowork_sync.py` § 2 shows 0 for your four skills; commit.
8. After srom-tlumacz's done line: write the K-item that tells Cowork to switch (K4): the commit hashes, the paths
   (`$HOME/mnt/SROM edit and trans/.claude/skills/<name>/`, setup at `…/srom-produkcja/setup.sh`), and what Cowork
   must change in srom-naczelny (the `P` and `setup.sh` lines) and `workspace/CLAUDE.md` (§ Changing a skill: direct
   edits after the preflight, with a C-item; no patches).

## For srom-tlumacz

After srom-produkcja's T-item for item 2:
1. Take Cowork's five differing files and five extra files (`cowork_sync.py` § 2 lists them; source as above):
   `SKILL.md` (description "Not for …"), `references/outputs.md` (delivery = the `STATUS.md` hand-off row, per
   stages.md), `tlumacz-draft_check.py`, `tlumacz-test_handoff.py`, `tlumacz_paths.py` (one finder for both layouts:
   `$SROM_SKILLS_DIR`, the root `.claude/skills/` links, `~/.claude/skills`, Cowork's mount), `assets/example/`.
2. Verify: your four checks; HANDOFF CONTRACT n/n with the new contract; `cowork_sync.py` § 2 shows 0 for srom-tlumacz.
   Commit; done line in your outgoing file.

## For MB

Nothing to decide. Open a session in srom-produkcja/ and say "apply checkup"; when it has written its T-item, the same
in srom-tlumacz/. Then tell Cowork: "Read K-items in Code's `_handoffs/code-to-cowork.md` and do them."
