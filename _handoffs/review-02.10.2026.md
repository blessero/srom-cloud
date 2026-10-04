# Cross-module review — [general] 02.10.2026 (22:11–22:18)

Reviewer only for this review: nothing in `srom-produkcja/` or `srom-tlumacz/` was changed by the review. Builds, round trips,
mutation tests and gate re-runs ran on copies in a scratch folder. **Declared:** earlier in the same root session, at MB's
explicit request, I built SYS-5 (invisible DOI links in the online PDF) in srom-produkcja, commit 32a085e, and closed
SYS-5 in the ledger (`_handoffs` 1fb98ba). That work is reviewed here like any other.
Repos at start and end: srom-produkcja 32a085e, srom-tlumacz 4b4b16f, `_handoffs` 1fb98ba (before this file).
Uncommitted at start and end: srom-produkcja `work/ostendorf/ostendorf_uwagi.md` (one line, a srom-produkcja session,
18:57; not touched). Covers everything since `review-01.10.2026.md`: srom-produkcja 12 commits after 1a560da,
srom-tlumacz 4 after 4d824eb, `_handoffs` 21 after 985c896.

## Conclusions

1. **Tests are green and the drafts still measure clean.** SUITE ALL PASS 24/24 (srom-produkcja 32a085e); HANDOFF CONTRACT
   33/33 against 32a085e; draft_check clean. All four drafts: pair CHECK OK, `build --draft` PASS, FRONT OK, Word copy →
   import → CHECK OK; final builds fail only on the known `[BRAK …]` gaps. Mutation tests 5 × 40/40.
2. **srom-tlumacz has had no session since 01.10 17:23, and five Kanon versions have come since.** T31–T35 (Kanon
   v1.11–v1.15) have no status line. Two of them ask for changes in the drafts that are still undone: numbered headings
   (all four drafts; the build strips them with a warning) and the withdrawn annotation `tłum. z przekładu angielskiego`
   (Ostendorf 13, Pahulich 3, Tittel 2). Ostendorf's `src/refs.json` is two versions behind (T34).
3. **No Word copy has been opened by MB yet** (all five tracked and clean in git), so all of this is still a draft fix
   plus re-export, as with T28. Once MB starts editing, each becomes a hand edit in Word.
4. **The linter misses a capitalised annotation.** `TLUM-ADNOTACJA` matches `tłum.` only; Pahulich writes `[Tłum. z
   przekładu angielskiego …]` three times, so its build shows no warning.
5. **MB's ten decisions of 21:30 (GEN-4…GEN-14) are waiting for srom-produkcja** (Kanon v1.16: bibliography parts,
   no DOI in print, etc.). Not stale yet: decided an hour ago; the ledger section says so.
6. **Last review: 10 of 11 findings fixed**; finding 6 of 29.09 (translation scripts never run in InDesign) is fixed by
   the Ostendorf INJECT tests. One partial: T30's master-file rename is in `handoff.md` but not in srom-tlumacz's PLAN
   OUT-DELIVERY, although its status line says "done".
7. **SYS-5 (DOI links)** holds up: `test_doi.py` 20/20 in the suite; the live check in InDesign passes on Ostendorf (36/36)
   and on a SICI DOI. It prints nothing and touches no contract with srom-tlumacz.

## Verdict lines as printed

srom-produkcja, `python3 .claude/skills/srom-produkcja/tests/run_all.py` (exit 0), commit 32a085e:
```
ok   test_check.py: CHECK ALL PASS 80/80
ok   test_citemap.py: CITEMAP ALL PASS 44/44
ok   test_csl.py: NOTES ALL PASS 36/36 | BIB ALL PASS 18/18 | POSITION ALL PASS 10/10
ok   test_docx_in.py: DOCXIN ALL PASS 23/23
ok   test_doi.py: DOI ALL PASS 20/20
ok   test_e10.py: E10 ALL PASS 9/9
ok   test_e2e.py: E2E ALL PASS 82/82
ok   test_e8.py: E8 ALL PASS 18/18
ok   test_install.py: INSTALL ALL PASS 1/1
ok   test_jsx.py: JSX-DONE | STYLES ALL PASS 23/23
ok   test_kanon.py: KANON ALL PASS 20/20
ok   test_lint.py: LINT 0 ERROR
ok   test_lookup.py: LOOKUP ALL PASS 15/15
ok   test_normalize.py: NORMALIZE ALL PASS 42/42
ok   test_pdf.py: PDF ALL PASS 10/10
ok   test_pdf_crs.py: PDF-CRS ALL PASS 17/17
ok   test_pdf_cup.py: PDF-CUP ALL PASS 24/24
ok   test_pdf_de.py: PDF-DE ALL PASS 20/20
ok   test_pdf_layout.py: PDF-LAYOUT ALL PASS 26/26
ok   test_pdf_onculture.py: PDF-ONCULTURE ALL PASS 11/11
ok   test_quant.py: QUANT ALL PASS 8/8
ok   test_roundtrip.py: ROUNDTRIP ALL PASS 18/18
ok   test_takeback.py: TAKEBACK ALL PASS 19/19
ok   test_volume_lists.py: VOLUME_LISTS ALL PASS 11/11
SUITE ALL PASS 24/24
```
srom-tlumacz, the checks in its CLAUDE.md (venv, all exit 0), contract test against srom-produkcja **32a085e**:
```
columns: 17/17 defined; schema fields: 17/17 present
shape: 39 rows, 0 problem(s)
vocab: all rows valid
precedent verified: 11/11
precedent quotes in rows not yet HOUSE: 9/9
established rows: 14, all with >=2 sources
training quotes verified: 25/25
candidate rows: 12, each with a verified training quote
selftest: 9/9 negative controls caught
HANDOFF CONTRACT 33/33          (E1, E2, E4: GAP CLOSED)
DRAFT ndiaye: leftover 0, marks 7=7, quotes –
DRAFT ostendorf: leftover 0, marks 2=2, quotes 43/43 (0 bad class, 0 open rows unmatched)
DRAFT pahulich: leftover 0, marks 10=10, quotes –
DRAFT tittel: leftover 0, marks 12=12, quotes 34/34 (0 bad class, 0 open rows unmatched)
```

Re-measured by me on copies (srom-produkcja 32a085e, its current `refs.json` per text):

| text | `check.py --pair` | `build --pair-src --queries --draft` | build without `--draft` | FRONT | Word master → import → pair | still to do from T31/T33 |
|---|---|---|---|---|---|---|
| Ndiaye | CHECK OK | PASS | PASS | OK | `_v2`: CHECK OK | 7 numbered headings |
| Ostendorf | CHECK OK | PASS | FAIL: `[BRAK …]` nn. 1, 2, 11, 12, 15, 17, 18, 34, 36, 47, 48 (OST-1) | OK | CHECK OK | 5 numbered headings; 13 × TLUM-ADNOTACJA |
| Pahulich | CHECK OK | PASS | FAIL: `[BRAK MIEJSCA]` nn. 47, 145 | OK | CHECK OK | 3 numbered headings; 3 × `[Tłum. z przekładu angielskiego …]` (not flagged: row 2) |
| Tittel | CHECK OK | PASS | FAIL: `[BRAK WYDAWCY]` n. 20 (GEN-4) | OK | CHECK OK | 5 numbered headings; 2 × TLUM-ADNOTACJA (T33 said 3) |

The import of each Word copy differs from `<id>_pl.md` only in the YAML form of `tlumaczenie:` (a list); a build from the
import PASSes with the translator in the report. Not a finding.
Source copies in `srom-tlumacz/work/<id>/src/` (all `manifest.sha256` OK) against srom-produkcja's files: `<id>_src.md` and
`<id>_src_front.md` identical for all four; `refs.json` identical for Ndiaye (6a058001, = T34), Pahulich (3b060a87, = T32),
Tittel (d83fe96e); **Ostendorf differs**: src 0704415d (T32), srom-produkcja 8958c705…30f09ce (T34).
Mutation tests (`mutate_keyed.py`, copies): Ndiaye, Ostendorf, Scheffknecht, Tittel, West Ohueri `MUTATIONS CAUGHT 40/40`.
No delivery yet, so `take_back.py` has nothing to verify.
Gates closed since the last review: srom-produkcja O1–O5 and S1 all hold (O1 NOTES/BIB/POSITION ALL PASS; O2 3; O3 `0 0`;
O4 KANON ALL PASS 20/20; O5 4; S1 DOI ALL PASS 20/20). O4 is named "Kanon v1.11" but runs the generic version test, so it now
measures v1.15: harmless. srom-tlumacz closed no gate. No CHECK writes a file MB edits.
Live InDesign (SYS-5, `tools/indesign_check/doi_check.py`, hidden copies): Ostendorf INJECT build and a SICI/`#?` fixture,
both INDESIGN DOI CHECK ALL PASS 7/7.

## Findings

| # | Finding | Evidence | Severity | Fixes |
|---|---|---|---|---|
| 1 | **T31–T35 unanswered; srom-tlumacz still cites Kanon v1.10.** No srom-tlumacz session since 01.10 17:23. Undone in the drafts: numbered headings (T31: Ndiaye 7, Ostendorf 5, Pahulich 3, Tittel 5) and the withdrawn annotation (T33: Ostendorf 13, Pahulich 3, Tittel 2). Ostendorf `src/refs.json` is T32's 0704415d, not T34's 8958c705. | `tlumacz-to-produkcja.md` ends with "Status of review 01.10.2026"; build reports "heading number removed (kanon §2)"; lint TLUM-ADNOTACJA; `cmp` above; `CLAUDE.md:35`, `tlumacz-PLAN.md:55` "v1.10" | will bite (cheap only until MB opens a Word copy) | srom-tlumacz |
| 2 | **The linter misses the capitalised annotation.** The TLUM-ADNOTACJA pattern is `tłum\. z przekładu angielskiego` (case-sensitive). Pahulich has `[Tłum. z przekładu angielskiego – przyp. tłum.]` ×3 (one with "autorki"): build shows 0 warnings. | `srom-kanon/scripts/lint_srom.py:156`; `grep -c 'Tłum\. z przekładu' pahulich_pl.md` → 3 | will bite (the warning is what srom-tlumacz works from) | srom-produkcja |
| 3 | **T30 marked done, but PLAN OUT-DELIVERY has no rename step.** `handoff.md` Back 1: at delivery the master is renamed to `<id>_robocza.docx`, older exports to `_old<n>`. srom-tlumacz's T30 status says this was "aligned in T26", which predates T30; OUT-DELIVERY still imports `<id>_robocza.docx` with no word on `_v2`, and the contract test has no case for it. Ndiaye's master is `ndiaye_robocza_v2.docx`; `take_back.py` would fail loudly on the first delivery. | `tlumacz-PLAN.md:50`; `handoff.md` Back 1; `tlumacz-to-produkcja.md` T30 status | will bite (first delivery, Ndiaye) | srom-tlumacz |
| 4 | **MB's ten decisions of 21:30 not yet applied** (GEN-4, 5, 6, 7, 8, 9, 10, 12, 13, 14): Kanon still has "Źródła drukowane i prawne", "(bez DOI)", "Literatura przedmiotu" and the DOI rule (§ 9.2 l. 322, § 9.7 l. 399, § 12.2.3); `build.py` SECTIONS too. Expected (decided at 21:30, no srom-produkcja session since); listed so it is not lost. Kanon v1.15 is announced, so this is a new row v1.16 and a T-item. | `MB-decisions.md:72–97`; `kanon-redakcyjny.md:322, 399`; `build.py:28–29` | will bite (next build of any text) | srom-produkcja |
| 5 | **Uncommitted notes-sheet line.** `work/ostendorf/ostendorf_uwagi.md` +1 line (Isaacs vs "Anne Katherine Isaacs", OST-3), written 18:57:22, 20 s after commit e019316; not in any commit. | `git -C srom-produkcja diff` | cosmetic (lost on a careless checkout) | srom-produkcja |
| 6 | **Three entry times later than their commit.** T35 "20:10" in 528bb81 (20:08:17); ledger "Decided by MB 02.10.2026 21:30" in eb64da7 (21:22:32); GEN-10 "(MB, 02.10.2026 21:50)" in 71cf393 (21:49:03). Times typed, not taken from `date`. Two are root-session entries. | `git show <commit>` vs the added lines | cosmetic | srom-produkcja (T35 correction line); MB (root sessions) |
| 7 | **Stale text, srom-produkcja.** `HANDOVER-produkcja.md:225` "Open: GEN-14" (decided 21:30: nothing to change); `:239–240` "Open: whether 'z dużych liter' … every word" (settled by v1.15); `:241–244` § 3 item 7 "`_postimport.jsx`, `_ibidem.jsx`, `_gwiazdki.jsx`, never yet run in InDesign" (run on the Ostendorf INJECT layouts 02.10, incl. the asterisk series; G12 can be recorded on that evidence or kept for an MB-edited text); § 1 Kanon list stops at v1.12 (`:46`). Ledger: SCH section "Also concerns GEN-4, GEN-5, GEN-6", WOH "GEN-9" (decided). `dist/*.skill` 30.09 01:56 predate v1.11–v1.15 and SYS-5 (only before an upload; SYS-1). | files as cited | cosmetic | srom-produkcja |
| 8 | **Stale text, srom-tlumacz.** `CLAUDE.md:35` "Kanon v1.10"; `tlumacz-PLAN.md:55` IF-KANON "v1.10"; `:56` IF-TYPESET "30/30 … 0c75f49" next to the later 33/33; HANDOVER Kanon lines. Part of row 1. | files as cited | cosmetic | srom-tlumacz |

Not findings:
- The root session wrote in srom-produkcja (SYS-5) at MB's explicit request; MB authorised it in chat. Committed by path, suite
  green, nothing of the other session's uncommitted work touched.
- SYS-5 and GEN-10 fit together: the links sit behind the printed text, whatever it is; when the DOI leaves the printed
  bibliography the `_doi.jsx` matches the new text, since it is generated by the same build. `citations.json` keeps `doi`
  from the reference data, so the Crossref citation list does not depend on print.
- The `tlumaczenie:` YAML becoming a list on import (above): docx_in's normal form; the build reads both.
- Ndiaye's one ORTH-OWSKI (a title in the bibliography, kept per T28 status) and two ABBR-VIDE warnings: known, by choice.

## Last review's findings

| # (01.10) | Finding | Now |
|---|---|---|
| 1 | Guard fails closed when its script is missing | fixed on both sides (`[ -f "$H" ] \|\| exit 0`; d3c3924, MB by hand in srom-tlumacz) |
| 2 | Guard never seen live | fixed: MB's test, refused a write into srom-produkcja (srom-tlumacz status 01.10 17:21) |
| 3 | T27–T29 unanswered; T28 spelling | fixed: status lines 01.10 17:21; drafts fixed and re-exported (b848ce3); 0 ORTH warnings except the kept title |
| 4 | Master file name at delivery | **partly**: rule in `handoff.md` (T30); srom-tlumacz's PLAN and test not aligned (row 3) |
| 5 | Old reviews flagged forever | fixed: root CLAUDE.md "the newest `review-*.md`" |
| 6 | Checkup skill "Needs MB now" | fixed: "At a glance" (752c3fa) |
| 7 | Kartoteka provisional row | fixed (d3c3924) |
| 8 | Notes sheets not in git | fixed: `work/*/*_uwagi.md` tracked (one uncommitted line now: row 5) |
| 9 | Stale text, srom-produkcja | fixed; new stale text: row 7 |
| 10 | Stale text, srom-tlumacz | fixed then; v1.10 is stale again after five versions (rows 1, 8) |
| 11 | srom-tlumacz gate drift | fixed: NOTE lines |
| 29.09 #5 | Source-changing decisions before the Word edits (PAH-2, TIT-2, TIT-7, V19-1) | **still open** (MB); the Word copies are still unedited |
| 29.09 #6 | Translation JSX never run in InDesign | fixed: Ostendorf INJECT tests 02.10 (postimport, Ibidem, asterisks), handover not updated (row 7) |

## For srom-produkcja

1. **Linter: capitalised annotation** (row 2). `srom-kanon/scripts/lint_srom.py:156`: make the pattern case-insensitive for
   the first letter (`[Tt]łum\. z przekładu angielskiego`). Add a `test_lint.py` case with `[Tłum. z przekładu angielskiego –
   przyp. tłum.]`. Verify: a copy of srom-tlumacz's `pahulich_pl.md` built with `--draft` reports 3 × TLUM-ADNOTACJA. No
   Kanon change (the rule is unchanged), so no new version; mention it in the next T-item.
2. **Apply MB's decisions of 21:30** (row 4), per the ledger section "Decided by MB 02.10.2026 21:30": Kanon v1.16 as a new
   § 17 row (§§ 7.2, 7.3, 9.1, 9.2, 9.4, 9.7, 12.2, 12.2.3), `build.py` SECTIONS (GEN-8 names and order), CSL (GEN-5, 6, 9, 10),
   `volume_lists.py` (GEN-13), `autorzy.tsv` (GEN-12), tests; check Tittel and Scheffknecht for GEN-8. Then a T-item, and
   delete the section from the ledger. Keep `doi` in `_citations.json` when the DOI leaves print (it comes from refs.json).
3. **Commit** `work/ostendorf/ostendorf_uwagi.md` (row 5) by path, after checking with MB's OST-3 that the line belongs there.
4. **T35 time** (row 6): a correction line under T35 ("T35, correction <now>: written 20:08, not 20:10").
5. **Stale text** (row 7): `HANDOVER-produkcja.md:225` (GEN-14 decided: nothing to change), `:239–240` (settled by v1.15),
   `:241–244` (the three scripts ran on Ostendorf's INJECT layouts on 02.10; decide whether that closes G12 or G12 waits for an
   MB-edited text, and say so), § 1 Kanon list (add v1.13–v1.15, then v1.16). Ledger: drop "GEN-4, GEN-5, GEN-6" from the SCH
   intro and "GEN-9" from the WOH intro once they are applied. Rebuild `dist/*.skill` only before an upload.
6. Status lines under `## Status of review 02.10.2026` in `produkcja-to-tlumacz.md`, one per item above.

## For srom-tlumacz

1. **Answer T31–T35** with status lines; cite "Kanon v1.15" (then v1.16 when it comes) in `CLAUDE.md:35`, PLAN IF-KANON
   (`:55`), HANDOVER (row 8).
2. **Before MB opens any Word copy** (they are all unedited: tracked and clean in git), as with T28:
   - T31: unnumber the headings in all four drafts (Ndiaye 7, Ostendorf 5, Pahulich 3, Tittel 5), and reword any
     cross-reference to a section number;
   - T33: remove the withdrawn annotation: Ostendorf 13 (nn. listed in T33 and its correction), Tittel 2, Pahulich 3 (they are
     capitalised, `[Tłum. z przekładu angielskiego …]`, so the build does not flag them yet: grep `[Tt]łum\. z przekładu`);
     Ostendorf's translations from the originals: keep one only where it matters (MB's call, list them for MB);
   - re-export each Word copy in place (git keeps the old one; Ndiaye's master is `_v2`).
   Verify: `build.py … --draft`: no "heading number removed" lines, no TLUM-ADNOTACJA; pair CHECK OK; `draft_check --all`
   clean; the new Word copies import to CHECK OK. If MB has opened a copy in the meantime, list the places in the text's notes
   sheet for his Word pass instead.
3. **Ostendorf intake** (T34): copy srom-produkcja's `work/ostendorf/refs.json` (8958c705…30f09ce) into `work/ostendorf/src/`,
   update `manifest.sha256`, `shasum -c` OK, then pair check and `--draft` build against it.
4. **Master file name** (row 3): add T30's step to PLAN OUT-DELIVERY (`:50`): before the import, rename the editor's master to
   `<id>_robocza.docx` and older exports to `<id>_robocza_old<n>.docx`; add a case to `tlumacz-test_handoff.py` (a `_v2`
   master renamed → TAKE-BACK OK). Correct the T30 status line ("done" → what is now done).
5. Status lines under `## Status of review 02.10.2026` in `tlumacz-to-produkcja.md`, one per item above.

## For MB

1. **Don't open the Word copies yet** — or tell srom-tlumacz which ones you have opened. Each still needs the T31 and T33
   changes (numbered headings, the withdrawn annotation); before your edit they are a quick fix and re-export, after it they
   are hand edits in Word. Start a srom-tlumacz session and say "apply checkup".
2. Still from 29.09: **PAH-2, TIT-2, TIT-7, V19-1** change the text or its numbering; decide them before your Word edit for the
   same reason.
3. **Ostendorf: which translations from the originals stay** (T33: only where it matters, MB's call). srom-tlumacz will list
   them in the Ostendorf notes sheet.
4. **DOI links (SYS-5, built today):** for the online PDF, run `<article>_doi.jsx` (in the article's Scripts Panel folder) last,
   after the other scripts, and export with General ▸ Include ▸ **Hyperlinks** ticked (with Bookmarks). The links are invisible.
5. Root sessions: take entry times from `date` (row 6: "21:30" was written at 21:22).
6. Still at the top of the ledger: GEN-1 (blocks the open-access announcement) and TIT-1 (blocks the Tittel delivery).
