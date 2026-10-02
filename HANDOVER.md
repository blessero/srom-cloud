# srom-tlumacz — handover (updated 03.10.2026 01:00, Claude Code; originally from the claude.ai "SROM_Naczelny" project)

## 1. What exists

Leaves closed (ALL MET): 1.1 contracts, 1.2 blind baseline, 1.3.1 vol. 18 precedent, 1.3.2 vol. 19 concordance, 1.3.5/1.3.5b/1.3.5c training corpus (race vocabulary, 10 texts), 1.4.1 the skill, 1.4.2a shared draft checker, 1.5.2a/b Ndiaye, 1.5.3a/b Ostendorf, 1.5.4a/b Pahulich, 1.5.5a/b Tittel (intake and preliminary translation each). Decided not to build (1.4.1, measured): 1.3.3 gazetteer files, 1.3.4 interference file, 1.4.2 tb_lookup/tb_check/calque_lint, 1.4.3 review sheet. Open in the tree: 1.5.1 (re-run of the 1.2 passages with the full module). Plan, tree and status log: `tlumacz-PLAN.md`. The folder is a git repository since 28.09.2026.

**The skill srom-tlumacz** (`.claude/skills/srom-tlumacz/`, linked as `~/.claude/skills/srom-tlumacz`) holds the procedure, the rules, the termbase and the checks; this folder holds the state:

| Where | What |
|---|---|
| skill `SKILL.md` | the procedure (intake, draft, checks, re-read, MB items, delivery, termbase upkeep), terminology rule, hard rules |
| skill `references/` | `tlumacz-tb.tsv` termbase (18 HOUSE, 9 PROVISIONAL C-0041–C-0049 awaiting V19-1–3, 12 CANDIDATE), `tlumacz-tb-schema.md`, `tlumacz-decisions.md` (MB's log), `tlumacz-rasa.md` (race register; only for texts on race), `outputs.md` (per-article file formats, delivery, skeletons) |
| skill `scripts/` | `tlumacz-check_tb.py`, `tlumacz-draft_check.py`, `tlumacz-front_check.py`, `tlumacz-test_handoff.py`, `tlumacz_paths.py` |
| `work/<id>/` | per-article work: `src/` (srom-produkcja's frozen hand-off + sha256), intake, `<id>_pl.md`, `<id>_front_pl.md`, queries, quotes, notes sheet `<id>_uwagi.md`, Word working copy, `research/` |
| `tlumacz-PLAN.md`, `tlumacz-gates-*.md` | tree, contract, status log; acceptance gates of each leaf (closed gates cite pre-1.4.1 paths: the scripts and the termbase moved into the skill, the per-article checker copies were deleted; see gates 1.4.1) |
| `training/` | MB's Polish reading corpus: texts git-ignored; `sources.tsv` (keys for `TR <key>: «…»` evidence) and `manifest.sha256` tracked |
| `sources/` | `vol18-md/` (clean vol. 18 EN + PL, precedent anchors), `vol18-en/` (originals, § 5), `Studia_Romologica_nr_18_2025.txt` (old extraction, line refs), `prng/` (PRNG world register), `SROM_knowledge_base.md` (journal facts: check here rather than assume) |
| `tlumacz-baseline-1.2/`, `tlumacz-1.3.1/`, `tlumacz-1.3.2/` | closed leaves; `tlumacz-1.3.2/vol19_terms.py` is re-run after each vol. 19 draft |
| `../_handoffs/tlumacz-to-produkcja.md` | messages to srom-produkcja (E-items; E18 twice, cite it with its [Author] tag); replies in `produkcja-to-tlumacz.md` |

## 2. How the module fits the pipeline

srom-tlumacz is the translation step inside **srom-produkcja scenario C** (its `references/handoff.md` is the contract):
srom-produkcja extracts the source and freezes citations → `<id>_src.md` + `refs.json` → **srom-tlumacz translates** → `<id>_pl.md`, `<id>_refs_tlum.json` (added citations flagged `"srom-added"` + `"srom-source"`), `<id>_pytania_tlum.csv` (query rows, `adresat;rodzaj;przypis;dzieło;szczegóły`), review sheet, quotes sheet, termbase rows → srom-produkcja `check.py --pair` → Word working copy (MB edits; Word is now the master) → build → InDesign.
srom-tlumacz does not duplicate srom-produkcja (structure, markers, keys, numbers, typography, kanon lint, DOCX).

## 3. MB's rulings

Every standing ruling now sits where it takes effect: the Kanon (§ 12.2, § 12.3, § 6.3 kartoteka; srom-kanon), the skill
(SKILL.md: scope, procedure, terminology rule, hard rules), the termbase schema and MB's decision log
(`references/tlumacz-decisions.md`). Not repeated here (checked in leaf 1.4.1, gate G13). A new ruling for every text
goes into the skill; a ruling for one text into its notes sheet.

## 4. State of the srom-produkcja interface (03.10.2026)

- `tlumacz-test_handoff.py` **33/33** against srom-produkcja cb3cfe5 (the E5 terminology-slot case removed in 1.4.1:
  tb_check is not built; srom-produkcja told in an E-item). Run it after every srom-produkcja update.
- The Kanon is at **v1.16** (T36, 03.10.2026); cite the version in its header. Kartoteka: srom-kanon
  `references/kartoteka.tsv`; changes through `_handoffs/`.
- Hand-back (T26, T30): `references/outputs.md` § Back in the skill. No delivery made yet: MB has returned none of the
  four Word copies.
- **T36 [general] [Tittel] not yet answered** (03.10.2026 00:30): drop `DOI: …` from the translation notes of the
  drafts (§ 12.2.3 item 1), copy Tittel's new `refs.json` (71181a9a…2b320d9), bibliography part names if a draft names
  one. Then the Word copies are re-exported (only if MB has opened none) and a status line goes out.

## 5. Vol. 18 material received (25.09.2026)

English originals are in `sources/vol18-en/`; MB's Polish DOCX are in `vol18-PL-HOLD/` (opened after leaf 1.2's hashes were recorded; git-ignored, sha256 in `vol18-PL-HOLD.sha256`); clean text of all eight in `sources/vol18-md/`.

| Article | Polish (notes) | English original | Usable |
|---|---|---|---|
| Takács | 32 | `Takacs_Serbian_Gypsies_rev.docx`, 33 Word notes = 1 title note ("adapted from a long-form digital publication…") + 32 numbered; matches the Polish 32 | full pair |
| Ostendorf | 81 | `Ann_Ostendorf_ENG_…docx`, no notes | body only; fetch the open-access (CC BY) version with notes |
| Fotta | 79 | RTF ripped from PDF, no note objects | body only; fetch the open-access (CC BY) version |
| Marushiakova/Popov | 48 | `Dom_Communities_Stripped_Mac_copy.docx`: notes present but **typed as plain text**, interleaved page by page as in a PDF (page-ID strings between); 52 body markers, notes numbered 1–54, region 48–50 garbled; no Word note objects | full pair after manual note alignment or E9 |

## 6. Pending — MB

Kept in one list for all modules: `../_handoffs/MB-decisions.md` (SYS-1 and V19-1–4 concern this module as a whole; OST-, PAH-, TIT-, NDI- its drafts). Not repeated here.

## 7. Next — Claude, in order

Four preliminary translations wait for MB's Word edit; MB's questions are in `../_handoffs/MB-decisions.md` under each
text's code. After MB returns a Word file: the hand-back (skill `references/outputs.md` § Back).

0. **Ostendorf**, "Familiar Outsiders Abroad" (leaf 1.5.3): `work/ostendorf/ostendorf_robocza.docx`, notes sheet
   `ostendorf_uwagi.md`; MB: OST-1–OST-10 (OST-10: which of the eight translations from the originals to keep).
   Assumed: she/her (vol. 18), translator MB (V19-4).
1. **Ndiaye**, "Black Roma" (leaf 1.5.2, the pilot): the master is `work/ndiaye/ndiaye_robocza_v2.docx` (v1 kept);
   notes sheet `ndiaye_uwagi.md`; MB: NDI-1–NDI-3. Open from T34: whether *Gitans* in the cathelin2004 title was
   italic in the author's original.
2. **Pahulich** (leaf 1.5.4): `work/pahulich/pahulich_robocza.docx`, `pahulich_uwagi.md`; MB: PAH-1–PAH-10 (PAH-1,
   Grellmann's edition, is the one real decision).
3. **Tittel** (leaf 1.5.5): `work/tittel/tittel_robocza.docx`, `tittel_uwagi.md`; MB: TIT-1–TIT-12 (TIT-1, the form
   of "gypsy", blocks delivery); then `tittel_refs_tlum.json` with the Polish editions once MB has the pages.
4. **West Ohueri** (T23, T24): received, not started — WOH-1 (rights).
5. **Termbase:** V19-1–V19-3 decide PROVISIONAL C-0041–C-0049 → HOUSE (log in `references/tlumacz-decisions.md`).
   Training corpus: MB may add Polish texts to `training/` (row in `sources.tsv`, sha256 in the manifest) → CANDIDATE
   rows and the register. Re-run `tlumacz-1.3.2/vol19_terms.py` after each new vol. 19 draft (West Ohueri: add probes
   for its terms, vol. 18 as a column; findings L4).
6. T36 (Kanon v1.16): see § 4 — the next small job.
7. Next in the tree: 1.5.1 (re-run of the 1.2 passages with the full module), when MB wants it; otherwise the next
   text from srom-produkcja, run per the skill.


## 8. Facts worth keeping

Module facts now live in the skill (official Polish names, Roma as a *mniejszość etniczna*), the termbase (*urasowienie*
ESTABLISHED, *subalterni* on one occurrence) and `sources/SROM_knowledge_base.md`.
