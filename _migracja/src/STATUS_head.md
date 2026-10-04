# SROM — state of every text (workspace root)

Read at the start of every session, with `MB-decisions.md`. One section per text; the hand-off log at the end is
appended, never rewritten (format: srom-produkcja `references/stages.md` § The hand-off log). Carried over from
Claude Code on 03.10.2026 02:49 [general]: the module handovers, the last handoff items and the newest review were
read; the verdicts below were re-measured on the moved files with the bundle's tools (Python 3.10, pandoc 3.8.3).

Stages: **RIP** (srom-produkcja) → **TRANS** (srom-tlumacz) → MB's Word edit → **INJECT** (srom-produkcja) →
InDesign (MB's Mac). MB's open questions are not repeated here: each text names its codes in `MB-decisions.md`.

## Before MB edits any Word copy
The questions that change the source are best decided first (review 03.10.2026): PAH-2, TIT-2, TIT-7, V19-1. Also
V19-2 and V19-3 (shared terms) apply to all four drafts.

## Volume 19 — translated texts

### Ndiaye, "Black Roma" (*Renaissance Quarterly* 75, 2022) [Ndiaye] — code NDI
- RIP done (133 notes keyed, 84 works in `refs.json`); handed to TRANS (log below).
- TRANS: draft done; **waiting for MB's Word edit** of the master 🔴 `srom-tlumacz/work/ndiaye/ndiaye_robocza_v2.docx`
  (`ndiaye_robocza.docx` is the older export, kept). Notes sheet `srom-tlumacz/work/ndiaye/ndiaye_uwagi.md`.
- 03.10.2026 02:49: pair `CHECK OK`, `FRONT OK`, `--draft` build `PASS` (Errors none), draft check leftover 0, marks 7=7.
- Open for Claude: whether *Gitans* in the title of cathelin2004 is italic in the author's original (look at the
  source PDF `srom-produkcja/work/Noemie Ndiaye Black Roma.pdf`; Kanon v1.14 § 3.4).
- Next: after MB's edit, the delivery (srom-tlumacz step 6) → INJECT → the first MB-edited translated text placed in
  InDesign with a real asterisk series (title note + translator's notes): the last open test of stage 4.
- MB: NDI-1 to NDI-3, V19-1 to V19-4.

### Ostendorf, "Familiar Outsiders Abroad" (*The Romani Atlantic*, ch. 3, CUP 2026) [Ostendorf] — code OST
- RIP done (83 works); licence CC BY-NC (GEN-3). Handed to TRANS (log below; `refs.json` last changed for Kanon v1.13–v1.14,
  copy in `src/` matches).
- TRANS: draft done; **waiting for MB's Word edit** of 🔴 `srom-tlumacz/work/ostendorf/ostendorf_robocza.docx`;
  notes sheet `ostendorf_uwagi.md`; quotations sheet `ostendorf_quotes.tsv`.
- 03.10.2026 02:49: pair `CHECK OK`, `FRONT OK`, `--draft` build `PASS`, draft check leftover 0, marks 2=2, quotes 43/43.
- INJECT trial (02.10.2026, before MB's edit): `srom-produkcja/work/ostendorf/pl/` holds the taken-back draft
  (`SHA256SUMS`); it was built and placed in the v3 template to test the InDesign scripts. The build folder of that
  trial is not carried over (regenerate with `build.py` from `pl/`). Not a delivery: the real one follows MB's edit.
- MB: OST-1 to OST-10 (OST-10: which of the eight quotations translated from the originals to keep), GEN-3, V19-3, V19-4.

### Pahulich, "Racialization of Roma, European Modernity, and the Entanglement of Empires" (CRS 8/1, 2025) [Pahulich] — code PAH
- RIP done (author-date source converted to notes); licence CC BY-NC (GEN-3). Handed to TRANS (log below).
- TRANS: draft done; **waiting for MB's Word edit** of 🔴 `srom-tlumacz/work/pahulich/pahulich_robocza.docx`; notes
  sheet `pahulich_uwagi.md`.
- 03.10.2026 02:49: pair `CHECK OK`, `FRONT OK`, `--draft` build `PASS`, draft check leftover 0, marks 10=10.
- Known from RIP: two paragraph breaks may have been lost at page breaks (pp. 46/47 "…Eastern Europe." | "In
  Moldavia…", pp. 54/55 "…Lucassen 1998)." | "Many historians…"): check against the journal's HTML when the text is
  next touched (`srom-produkcja/work/pahulich/pahulich_uwagi.md`).
- MB: PAH-1 to PAH-10 (PAH-1, Grellmann's edition, is the one real decision), GEN-3, V19-1 to V19-4.

### Tittel, "Racial and Social Dimensions of Antiziganism" (*On_Culture* 10, 2020) [Tittel] — code TIT
- RIP done; handed to TRANS (log below; `refs.json` last changed for Kanon v1.16).
- TRANS: draft done; **delivery blocked by TIT-1** (the form of "gypsy"); Word copy
  🔴 `srom-tlumacz/work/tittel/tittel_robocza.docx`; notes sheet `tittel_uwagi.md`; quotations `tittel_quotes.tsv`.
- 03.10.2026 02:49: pair `CHECK OK`, `FRONT OK`, `--draft` build `PASS`, draft check leftover 0, marks 12=12, quotes 34/34.
- After MB has the Polish editions' pages (TIT-3): `tittel_refs_tlum.json` with the Polish editions.
- MB: TIT-1 to TIT-12, V19-1, V19-3, V19-4.

### West Ohueri, "Peripheral whiteness and racial belonging and non-belonging" (*Off White*, ch. 6, MUP 2024) [West Ohueri] — code WOH
- RIP done and frozen after MB's answers of 29.09.2026 (51 works, mutation test 40/40); `check.py` on the source:
  `CHECK OK` (03.10.2026 02:49). Licence CC BY-NC-ND: no translation is published without written permission (MB is
  asking the author and MUP).
- **Not handed to TRANS** (no `srom-tlumacz/work/westohueri/` yet): waits for WOH-1.
- MB: WOH-1 to WOH-6, V19-2, V19-3.

## Other texts

### Scheffknecht, "Zigeuner im Reichshof Lustenau" (*Neujahrsblätter Lustenau* 1, 2010) [Scheffknecht] — code SCH
- German; RIP done as a test of the extractor (endnotes, full-note citations, 35 works typed from the notes;
  `srom-produkcja/work/scheffknecht/`, notes sheet `scheffknecht_uwagi.md`);
  `CHECK OK` (03.10.2026 02:49). Not handed over: srom-tlumacz works from English. MB: SCH-1 to SCH-5.

### Marushiakova/Popov, Dom communities (vol. 18) [Dom] — no code
- A test of `docx_in.py --typed-notes` on the vol. 18 DOCX whose notes are typed as text: 52/52 note pairs right
  (`srom-produkcja/work/dom/`), marker 48 repaired; one page is missing from that DOCX (notes 49–50). Not frozen;
  RIP when MB wants it. Nothing pending.

## Volume data
- `srom-produkcja/volumes/18/srom_master_v3.csv`: the vol. 18 master CSV, before any Crossref deposit (placeholder DOI
  prefix and dates; no `translators_struct` column yet for its two translated articles). `volumes/autorzy.tsv` (authors
  register), `volumes/ror.tsv` (institution IDs, SYS-3). Vol. 19's CSV does not exist yet: it is filled at INJECT.

## Translation module state
- Termbase (in the srom-tlumacz skill): 18 HOUSE rows, 9 PROVISIONAL (C-0041–C-0049, waiting for V19-1 to V19-3),
  12 CANDIDATE. After each new vol. 19 draft re-run `srom-tlumacz/tlumacz-1.3.2/vol19_terms.py` (today: 25 probes,
  16 consistent, 3 divergent, 1 missing, 5 single).
- MB may add Polish texts to `srom-tlumacz/training/` (a row in `sources.tsv`, sha256 in `manifest.sha256`).
- Not carried over from Code: the blind baseline of leaf 1.2 and its planned re-run (1.5.1); MB's vol. 18 Polish DOCX
  held back for that test (`vol18-PL-HOLD/`).

## Known limits of the moved files
- `srom-produkcja/work/ndiaye/key.py` adds `../../.claude/skills/srom-typeset/scripts` to `sys.path` (the Code
  layout). To re-run the keying, change that line to the plugin's `srom-produkcja/scripts`. The other per-text scripts
  (`key.py`, `refs.py`, `prep.py`) import nothing from the skills.
- The old build reports (`srom-produkcja/work/<id>/build/*_report.md`) name the linter by its Mac path: history, not
  a setting.

## For the skills
Skill changes made in Cowork, to apply in Claude Code (CLAUDE.md § Changing a skill). Append with date and time and
the patch file; MB ticks a line when Code has it.

- (none yet)

## Hand-off log
