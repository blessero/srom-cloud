# Gates: queue items 2 (kanon ↔ typeset overlap) and 3 (E8 asterisk notes) — 26.09.2026

Scope: the Polish Kanon becomes the master text inside srom-kanon (v1.6, with decisions and draft § 12.2);
srom-produkcja stops bundling the linter and cites only Kanon sections that exist; non-author notes leave the
numbered footnotes and become one asterisk series (placed by hand above the numbered notes, footnote style).
Checks run from the repo root. K = .claude/skills/srom-kanon, T = .claude/skills/srom-produkcja.

**Re-running closed gates (29.09.2026 17:59, review 29.09.2026 row 12).** Some closed CHECKs read files that are meant to
change: `../_handoffs/MB-decisions.md` (items are removed once MB decides), the handoff files, the suite's
`n/n` count. They held when the gate closed. They are records, not re-runnable: C1, F6, P5, O7, T6, S6, W6, R1
(S6 expects `### D21` once and R1 none, so they cannot both hold), W7. From now on a CHECK tests what the leaf
produced in this repo (a file, a test, its own commit found by message), never `MB-decisions.md`, or counts that
will move (CLAUDE.md, working rules).

## Item 2 — overlap

- [x] A1: the Kanon lives in srom-kanon as references/kanon-redakcyjny.md, version 1.6
  CHECK: head -3 .claude/skills/srom-kanon/references/kanon-redakcyjny.md
  EXPECT: Wersja 1.6
  EVIDENCE: # STUDIA ROMOLOGICA – KANON EDYTORSKI (DOKUMENT WEWNĘTRZNY) | **Wersja 1.6 · obowiązuje od tomu 19/2026 · do użytku redakcji i składu**

- [x] A2: RULES.md is v1.6, names the Kanon as normative, no "canon governs" clause pointing outside the skill
  CHECK: head -3 .claude/skills/srom-kanon/RULES.md; grep -c "canon governs" .claude/skills/srom-kanon/RULES.md || true
  EXPECT: /v1\.6[\s\S]*references\/kanon-redakcyjny\.md[\s\S]*\n0\s*$/
  EVIDENCE: Normative text: `references/kanon-redakcyjny.md` — *Kanon edytorski Studia Romologica* (Polish, internal), in this skill. This file is its compact English digest; **section numbers are the Kanon's**. 

- [x] A3: srom-produkcja no longer bundles the linter
  CHECK: test -e .claude/skills/srom-produkcja/scripts/lint_srom.py && echo BUNDLED || echo GONE
  EXPECT: GONE
  EVIDENCE: GONE

- [x] A4: build without srom-kanon fails with a clear message naming srom-kanon; test_kanon.py checks versions and every § reference in srom-produkcja against the Kanon's headings
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS \d+\/\d+/
  EVIDENCE: KANON ALL PASS 11/11

- [x] A5: decisions 1–9, 11–14, 16, 17 written into the Kanon in Polish, each in its own section; § 17 has a 1.6 row
  EVIDENCE: kanon-redakcyjny.md: [16]→§0, [13]→§3.3, [11]→§3.4, [17]→§4.1 (verse; §5.3/§10.1 already had examples/tables), [1][9] + E8→§7.1, [7]→§7.2 + §16, [2][3][8]→§7.3, [14]→§7.4, [12]→§8.6, [5]→§9.2, [6]→§9.3, [4]→§9.7; [10] was already in §2. 17 marker phrases grep-found; § 17 line 606 `| 1.6 | …`. [15][18][19] kept in srom-produkcja as toolchain conventions (not house rules) — reported to the editor.

- [x] A6: draft § 12.2 (srom-tlumacz, settled 25.09.2026) incorporated, with its consequential edits in § 1, § 4.2, § 6.3, § 11
  CHECK: grep -c "^### 12.2\|§ 12.2" .claude/skills/srom-kanon/references/kanon-redakcyjny.md
  EXPECT: /\b(1[0-9]|[2-9][0-9])\b/
  EVIDENCE: 13

- [x] A7: RULES.md digest carries the same changes (English), each section pointing to its Kanon §; Ibidem "same column"
  EVIDENCE: RULES.md rewritten with Kanon numbering (§3.5, §5, §6, §9.6, §10, §11, §12.2 new/moved); test_kanon: 'every numbered RULES.md section exists in the Kanon' PASS; 'same column' at RULES.md:101 and §J 3; §J 15–16 added.

- [x] A8: decisions.md reduced to rule → implementing file/test map + implementation conventions + open items 20–22
  EVIDENCE: references/decisions.md: 24-row Kanon §→code→test table, 4 toolchain conventions ([15][18][19], E8), open 20–22. Two untested rules found while mapping (§8.6 hyperlinks, §7.4 multi-paragraph notes) → tests added to test_e2e (59/59).

- [x] A9: srom-kanon SKILL.md and linter docstring say v1.6; SKILL.md sends production linting to srom-produkcja's build
  CHECK: grep -h "v1\.[0-9]" .claude/skills/srom-kanon/SKILL.md .claude/skills/srom-kanon/scripts/lint_srom.py | grep -v "1\.6" | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

## Item 3 — E8

- [x] B1: build turns "– przyp. tłum./red." notes into a marker (character style) + paragraphs in "Przypis gwiazdkowy" at the end of the DOCX, title note first; numbered footnotes exclude them
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_e8.py | tail -1
  EXPECT: /E8 ALL PASS \d+\/\d+/
  EVIDENCE: E8 ALL PASS 18/18

- [x] B2: no Ibidem in an asterisk note, none in a numbered note that follows one (covered in test_e8.py)
  EVIDENCE: test_e8 'PASS no Ibidem inside an asterisk note (short form instead)' and 'PASS numbered note after a non-author note: Ibidem replaced by the short form, reason in the report' (build.py after_na / ast_divs).

- [x] B3: check.py: [^r<n>] must end "– przyp. red." ([^t<n>] "– przyp. tłum."), in single and pair mode; r-notes left out of the pair comparison (covered in test_e8.py / test_check.py)
  EVIDENCE: test_check 40/40 incl. 5 new E8 cases (r-note excluded; r without formula ERROR; t with red formula ERROR; single-file check; '[… – przyp. tłum.]' closing an author's note stays compared — a latent bug in the old TN_FORMULA, fixed); test_e8 '[^r1] without … fails the build', 'printed numbers skip translator/editorial notes'.

- [x] B4: _postimport.jsx counts markers vs asterisk notes and flags a formula inside a numbered footnote; _gwiazdki.jsx (after layout) lists every asterisk note with page and asterisk count; both ES3
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_jsx.py | grep -c "acorn es3"
  EXPECT: /\b[3-9]\b/
  EVIDENCE: 3

- [x] B5: style spec: "Przypis gwiazdkowy" based on "Przypis" (no own values), replaces "Przypis do tytułu"; character style "Odsyłacz gwiazdkowy"; setup JSX + style sheet regenerated
  CHECK: grep -c "Przypis gwiazdkowy\|Odsyłacz gwiazdkowy" .claude/skills/srom-produkcja/references/style-sheet.md .claude/skills/srom-produkcja/config/styles.json
  EXPECT: /style-sheet\.md:[1-9][\s\S]*styles\.json:[1-9]/
  EVIDENCE: .claude/skills/srom-produkcja/references/style-sheet.md:2 | .claude/skills/srom-produkcja/config/styles.json:2

- [x] B6: docs updated: no "numbered with the author's notes" left; srom-md, handoff, indesign, SKILL describe the series
  CHECK: grep -rn "numbered with the author" .claude/skills/srom-produkcja | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

## Global

- [x] Z1: full suite green
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1
  EXPECT: /SUITE ALL PASS 1[1-9]\/1[1-9]/
  EVIDENCE: SUITE ALL PASS 11/11

- [x] Z2: committed, working tree clean
  CHECK: git status --porcelain | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

---

# Gates: batch 27.09.2026 — delegated decisions, E12, kartoteka (D9), E10

Scope: MB delegated D1, D2, D9, D8(e)→E12 and decisions 15/18/19 to srom-produkcja (27.09.2026); record them,
put E12 into the Kanon, create the kartoteka from srom-tlumacz's seed, implement E10 (translator in YAML front
matter), re-scope D3/D7 (InDesign later; stage-1 test on MB's PDF next), answer srom-tlumacz.

- [x] C1: MB-decisions.md records D1, D2, D9, D8(e)/E12 decisions and the D3/D7 re-scope
  CHECK: grep -c "delegated the call to srom-produkcja\|re-scoped" ../_handoffs/MB-decisions.md
  EXPECT: /\b([5-9]|1[0-9])\b/
  EVIDENCE: 6

- [x] C2: Kanon § 3.4, § 6.2, § 14, § 17 carry the exonym rule; RULES.md digest too
  CHECK: grep -c "egzonim" .claude/skills/srom-kanon/references/kanon-redakcyjny.md; grep -c "exonym" .claude/skills/srom-kanon/RULES.md
  EXPECT: /\b[4-9]\b[\s\S]*\b[2-9]\b/
  EVIDENCE: 6 | 7

- [x] C3: kartoteka.tsv in srom-kanon, all 35 seed rows, house italics column, no open flags; structure test passes
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS \d+\/\d+/
  EVIDENCE: KANON ALL PASS 18/18

- [x] C4: E10 — handoff.md + srom-md.md document `tlumaczenie:`; build reports translators_struct; survives the Word round trip
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_e10.py | tail -1
  EXPECT: /E10 ALL PASS \d+\/\d+/
  EVIDENCE: E10 ALL PASS 9/9

- [x] C5: produkcja-to-tlumacz.md answers E12, reports E10 done (their test side), kartoteka created
  CHECK: grep -c "^## T[6-9]" ../_handoffs/produkcja-to-tlumacz.md
  EXPECT: /\b[2-9]\b/
  EVIDENCE: 3

- [x] C6: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 13/13 | 0

---

# Gates: batch 28.09.2026 — cross-module review, E16; E9 (queued)

Scope: the cross-module review of 28.09.2026 (`../_handoffs/review-28.09.2026.md`, message for srom-produkcja items
1–9): E16 (Word round trip splits the one title note), docs aligned with the contract, stale text, D15/D16, packages.
E9 (typed notes in DOCX sources) is queued here with its gates open.
Note: commits f2c8bc0..bb13dc8 (27–28.09.2026, incl. contract changes T11 and D12) ran without a gate batch; their
evidence is the suite cases named in the commit messages. Not reconstructed.
Checks run from the repo root. K = .claude/skills/srom-kanon, T = .claude/skills/srom-produkcja.

- [x] F1: E16 — multi-paragraph blocks survive the Word round trip; comment before punctuation; mowca line break
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_roundtrip.py | tail -1
  EXPECT: /ROUNDTRIP ALL PASS (\d+)\/\1/
  EVIDENCE: ROUNDTRIP ALL PASS 18/18 (the 3 new cases fail on the scripts of bb13dc8)

- [x] F2: MB's working copy imports to one title-note block, pair CHECK OK, build PASS
  CHECK: N=../srom-tlumacz/work/ndiaye; D=$(mktemp -d); V=~/.venvs/srom/bin/python; T=.claude/skills/srom-produkcja; $V $T/scripts/docx_in.py $N/ndiaye_robocza_v2.docx -o $D/v2.md >/dev/null; grep -c przypis-tytulowy $D/v2.md; $V $T/scripts/check.py --pair $N/src/ndiaye_src.md $D/v2.md --refs $N/src/refs.json --refs $N/ndiaye_refs_tlum.json | tail -1; $V $T/scripts/build.py $D/v2.md --refs $N/src/refs.json --refs $N/ndiaye_refs_tlum.json --pair-src $N/src/ndiaye_src.md --out $D/b | tail -1 | cut -c1-4
  EXPECT: /^1\s+CHECK OK\s+PASS\s*$/
  EVIDENCE: 1 | CHECK OK | PASS (file dated 28.09.2026 02:41; it is MB's working file and will change)

- [x] F3: srom-tlumacz's contract test sees E16 closed (run read-only)
  CHECK: ~/.venvs/srom/bin/python ../srom-tlumacz/tlumacz-test_handoff.py | grep -E "E16|HANDOFF CONTRACT"
  EXPECT: /GAP CLOSED ok\s+E16[\s\S]*HANDOFF CONTRACT (\d+)\/\1/
  EVIDENCE: GAP CLOSED ok  E16: … | HANDOFF CONTRACT 30/30

- [x] F4: SKILL.md and srom-md.md no longer say comments fail the build (contract: never block)
  CHECK: cat .claude/skills/srom-produkcja/SKILL.md .claude/skills/srom-produkcja/references/srom-md.md | grep -c "open editor comments\|fails the build\*\* until resolved"
  EXPECT: /^0\s*$/
  EVIDENCE: 0 | 0

- [x] F5: srom-kanon SKILL.md quick rule 9 carries the § 3.4 foreign-exonym exception
  CHECK: grep -c "Exception (§ 3.4)" .claude/skills/srom-kanon/SKILL.md
  EXPECT: /^1\s*$/
  EVIDENCE: 1

- [x] F6: Kanon § 13.2 open items are D15/D16 in MB-decisions.md; the archive header says it is frozen
  CHECK: grep -c "^## D1[56] " ../_handoffs/MB-decisions.md; grep -c "nothing is appended" ../_handoffs/MB-decisions-archive.md
  EXPECT: /^2\s+1\s*$/
  EVIDENCE: 2 | 1

- [x] F7: decisions 20 and 22 (D1, D2) no longer shown open; handover § 2 and § 7 current
  CHECK: grep -cE "^\| 2[02] \| ○" .claude/skills/srom-produkcja/references/decisions.md
  EXPECT: /^0\s*$/
  EVIDENCE: 0

- [x] F8: scenario C (SKILL.md) names the T11 files and --pair-src; handoff.md points to the front_pl format
  CHECK: grep -c "_front_pl.md\|_refs_tlum.json\|--pair-src" .claude/skills/srom-produkcja/SKILL.md; grep -c "tlumacz-front_check.py" .claude/skills/srom-produkcja/references/handoff.md
  EXPECT: /^[3-9]\s+[1-9]\s*$/
  EVIDENCE: 3 | 1

- [x] F9: no Kanon version other than the current one in either skill, any case (test widened)
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS (\d+)\/\1/
  EVIDENCE: KANON ALL PASS 20/20 (the new case failed on 5 files before the fix)

- [x] F10: E16 answered in the outgoing file
  CHECK: grep -c "^## T16 — re E16" ../_handoffs/produkcja-to-tlumacz.md
  EXPECT: /^1\s*$/
  EVIDENCE: 1

- [x] F11: packages rebuilt for claude.ai: dist/srom-kanon.skill is v1.7
  CHECK: unzip -p dist/srom-kanon.skill srom-kanon/SKILL.md | grep -c "Kanon v1.7"
  EXPECT: /^[1-9]\s*$/
  EVIDENCE: 1 (dist/ rebuilt after commit 2 of this batch; git-ignored)

- [x] F12: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 14/14 | 0

## E9 — typed notes in DOCX sources (T2) — done 28.09.2026

- [x] G1: `docx_in.py --typed-notes` pairs each superscript body marker with the typed note of the same number, in
  sequence; never guesses: missing, repeated or unpaired numbers, repairs and gaps are listed and the import says
  IMPORT CHECK
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_docx_in.py | tail -1
  EXPECT: /DOCXIN ALL PASS (\d+)\/\1/
  EVIDENCE: DOCXIN ALL PASS 23/23 (11 new E9 cases: labels = source numbers, italics, note inside note, note
  continuation, page-split body + page ID, repaired marker, no join across a lost page, marker without note,
  integrity, no conversion without the flag, mixed notes refused)

- [x] G2: on the Dom file (srom-tlumacz sources, read-only) every pair made is right and every number not paired is listed
  CHECK: D=../srom-tlumacz/sources/vol18-en/Dom_Communities_Stripped_Mac_copy.docx; V=~/.venvs/srom/bin/python; $V .claude/skills/srom-produkcja/scripts/docx_in.py $D -o work/dom/dom_src_typed.md --typed-notes | tail -1; $V work/dom/dom_verify.py $D work/dom/dom_src_typed.md | head -1; grep -c "GAP: notes 49–50\|LOST TEXT\|REPAIRED: marker 48" work/dom/dom_src_typed_import.md
  EXPECT: /IMPORT CHECK 3\s+pairs checked: 52; wrong: 0\s+3\s*$/
  EVIDENCE: IMPORT CHECK 3 | pairs checked: 52; wrong: 0 | 3 (verifier reads the DOCX with python-docx, independent
  of the converter; work/ is git-ignored)

- [x] G3: docs (docx_in docstring, SKILL.md step 1a) and a T-item to srom-tlumacz
  CHECK: grep -c "typed-notes" .claude/skills/srom-produkcja/SKILL.md; grep -c "^## T.* re E9" ../_handoffs/produkcja-to-tlumacz.md
  EXPECT: /^[1-9]\s+[1-9]\s*$/
  EVIDENCE: 1 | 2 (T2 plan, T17 done)

- [x] G4: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 14/14 | 0

## Stage-1 test 2 — Pahulich (CRS 8/1, 2025, author-date PDF) — done 28.09.2026

- [x] P1: the PDF extracts clean: notes/markers contiguous, front matter out of the text, reference list complete
  CHECK: cd work && ~/.venvs/srom/bin/python ../.claude/skills/srom-produkcja/scripts/pdf_extract.py Pahulich.pdf -o pahulich/pahulich_pdf.md | tail -1; wc -l < pahulich/pahulich_pdf_bib.txt
  EXPECT: /EXTRACT OK\s+52\s*$/
  EVIDENCE: EXTRACT OK | 52 (4 notes, 4 markers; every word compared with the PDF text: nothing lost)

- [x] P2: refs.json matches the author's list (52 works); DOIs checked against Crossref (work/pahulich/doi_check.txt)
  CHECK: cd work/pahulich && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/cite_map.py audit --refs refs.json --bib pahulich_pdf_bib.txt | tail -1
  EXPECT: /CITEMAP OK/
  EVIDENCE: CITEMAP OK

- [x] P3: every author-date reference converted or listed; source passes check and builds as a source proof
  CHECK: cd work/pahulich && V=~/.venvs/srom/bin/python; S=../../.claude/skills/srom-produkcja/scripts; $V prep.py >/dev/null && $V $S/cite_map.py scan pahulich_pre.md --refs refs.json --apply /tmp/p.md --renumber | tail -1; cmp /tmp/p.md pahulich_src.md && echo SAME; $V $S/check.py pahulich_src.md --refs refs.json | tail -1; $V $S/build.py pahulich_src.md --refs refs.json --source --out build/ | tail -1
  EXPECT: /CITEMAP OK\s+SAME\s+CHECK OK\s+PROOF .*\(0 issue/
  EVIDENCE: CITEMAP OK | SAME | CHECK OK | PROOF … (0 issue(s)); 25 Ibid and 17 year-only resolutions checked by hand

- [x] P4: Word working copy round trip lossless (comments aside)
  CHECK: cd work/pahulich && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/docx_in.py pahulich_src_robocza.docx -o /tmp/rt.md | tail -1; diff <(sed 's/ *<!--.*-->//' pahulich_src.md) /tmp/rt.md | grep -c "^[<>] ."
  EXPECT: /IMPORT OK\s+0\s*$/
  EVIDENCE: IMPORT OK | 0

- [x] P5: hand-off: T18 to srom-tlumacz, D17 for MB, both committed in _handoffs
  CHECK: grep -c "^## T18" ../_handoffs/produkcja-to-tlumacz.md; grep -c "^## D17" ../_handoffs/MB-decisions.md; git -C ../_handoffs status --porcelain | wc -l
  EXPECT: /^1\s+1\s+0\s*$/
  EVIDENCE: 1 | 1 | 0

- [x] P6: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 15/15 | 0


## Stage-1 test 3 — Scheffknecht (Neujahrsblätter Lustenau 1/2010, German, endnotes, full-note citations) — done 28.09.2026

- [x] S1: extractor handles this layout generically, each with a test (test_pdf_de.py): ragged right with block
  paragraphs (no false breaks at short lines), quotations indented ~1 em (one quotation, inner paragraphs), a
  quoted numbered list (no Markdown list), InDesign control characters (U+0007) and soft hyphens (U+00AD) removed,
  suspended hyphen before a conjunction kept ("Diebs- und"), line-end slash spaced as the document spaces it,
  marker in the title -> title note, raised digit inside a note is not a marker (²1990), caption beside an image
  without "Abb." -> ::: podpis
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_pdf_de.py | tail -1
  EXPECT: /PDF-DE ALL PASS \d+\/\d+/
  EVIDENCE: PDF-DE ALL PASS 18/18
- [x] S2: no regression on the earlier PDFs: Ndiaye and Pahulich extract byte-identical to the baseline taken before
  the change (or every difference explained)
  CHECK: see EVIDENCE (diff against scratchpad baselines)
  EVIDENCE: Ndiaye and Pahulich .md, _bib.txt, _front.md byte-identical to the baseline; _extract.md differs only by
  new report lines (layout line; captions matched by image; soft hyphen label on Enlighten~|ment; two Pahulich
  page breaks after a sentence end now listed: pp. 46/47 "…Eastern Europe." | "In Moldavia…", pp. 54/55
  "…Lucassen 1998)." | "Many historians…" — possibly lost paragraph breaks in the Pahulich source, see handover)
- [x] S3: the article extracts clean: 120 numbered notes + title note, markers contiguous, every word of the PDF's
  article pages present in the output (word-bag comparison), stray marker(s) flagged, not dropped
  CHECK: cd work && ~/.venvs/srom/bin/python ../.claude/skills/srom-produkcja/scripts/pdf_extract.py njb-2010-zigeuner-im-reichshof-lustenau_wolfgang-scheffknecht.pdf --pages 4-32 -o scheffknecht/scheffknecht_pdf.md | tail -1
  EXPECT: /EXTRACT (OK|CHECK 1)/
  EVIDENCE: EXTRACT CHECK 1 issue(s) = the stray "1" after the last word (kept as a comment, D18 A7); 120 notes + title
  note; wordcheck.py: 10482 words, "lost 3 / extra 8" all the checker's own joins (Diebs- und, württem~-bergischen) and
  five superscript edition digits — nothing lost
- [x] S4: refs.json: every published work cited in the notes keyed (no bibliography in the source: built from the
  first full citations); archival sources stay literal; nothing invented, gaps as [BRAK …] and listed
  CHECK: cd work/scheffknecht && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed scheffknecht_pre.md scheffknecht_src.md --refs refs.json | tail -1
  EXPECT: /CHECK OK/
  EVIDENCE: CHECK OK (35 works, 46 notes keyed + the title note, 74 literal; warnings only for series numbers the CSL does
  not print, D18 A4); 29 × [BRAK WYDAWCY] listed in the query sheet
- [x] S5: source passes check and builds as a source proof; Word working copy round trip lossless
  CHECK: cd work/scheffknecht && V=~/.venvs/srom/bin/python; S=../../.claude/skills/srom-produkcja/scripts; $V $S/check.py scheffknecht_src.md --refs refs.json | tail -1; $V $S/build.py scheffknecht_src.md --refs refs.json --source --out build/ | tail -1
  EXPECT: /CHECK OK[\s\S]*PROOF/
  EVIDENCE: CHECK OK | PROOF … (0 issue(s)); working copy: IMPORT OK, 0 differing lines (comments aside)
- [x] S6: what the German test showed about the toolchain (CSL/Kanon for German sources, citation keying) written
  up; open points for MB in MB-decisions.md (D18) with a queries file; nothing for srom-tlumacz sent without MB
  EVIDENCE: _handoffs b37aa1e (D18); work/scheffknecht/scheffknecht_queries.md A–E; handover § 3 item 4b
- [x] S7: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 16/16 | 0

## Stage-1 test 4 — Ostendorf (The Romani Atlantic, CUP 2026, ch. 3; Chicago full notes, PUA text layer) — done 28.09.2026

- [x] O1: extractor repairs this text layer generically, each with a test (test_pdf_cup.py): PUA old-style figures and
  small capitals, TeX accent, "¼" from a math font, word spaces set as gaps, chapter numeral above the title, notes running
  over a page with no rule, compounds kept on document evidence
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_pdf_cup.py | tail -1
  EXPECT: /PDF-CUP ALL PASS (\d+)\/\1/
  EVIDENCE: PDF-CUP ALL PASS 20/20 (the integration cases fail on the pre-change extractor)
- [x] O2: no regression on the earlier PDFs (Ndiaye, Pahulich, Scheffknecht byte-identical to the baseline, or explained)
  CHECK: see EVIDENCE (scratchpad baselines)
  EVIDENCE: Ndiaye, Scheffknecht .md/_bib/_front identical; Pahulich one word: "religiopolitical" -> "religio-political"
  (compound rule; frozen pahulich_src.md unchanged, listed in ostendorf_queries C and to the Pahulich session); reports
  gain the gap-space count, running heads now spaced
- [x] O3: the article extracts clean: 62 notes, 62 markers, every word and number of the PDF in the output; digits
  confirmed independently (17 DOIs/URLs = the PDF's link targets)
  CHECK: cd work/ostendorf && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/pdf_extract.py ../11.3_pp_86_108_Familiar_Outsiders_Abroad.pdf -o /tmp/o.md | tail -2
  EXPECT: /notes 62 · markers 62[\s\S]*EXTRACT OK/
  EVIDENCE: notes 62 · markers 62 · EXTRACT OK; wordcheck.py: 9297 tokens, lost 6 / extra 12 = the checker's own joins
  (heading words without spaces in the text layer; co-developed, light-brown, mulatto-like)
- [x] O4: refs.json (83 works, from the notes; nothing added, gaps as [BRAK …] and listed); keying proven, now with
  Chicago pages counted (a lost page is an ERROR: mutation test — old check OK, new check 3 errors)
  CHECK: cd work/ostendorf && ~/.venvs/srom/bin/python refs.py >/dev/null && ~/.venvs/srom/bin/python key.py >/dev/null && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed ostendorf_pre.md ostendorf_src.md --refs refs.json 2>/dev/null | grep -c "WARN\|ERROR"; ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed ostendorf_pre.md ostendorf_src.md --refs refs.json 2>/dev/null | tail -1
  EXPECT: /^0\s+CHECK OK\s*$/
  EVIDENCE: 0 | CHECK OK
- [x] O5: source checks, builds as a source proof with 0 issues; Word working copy round trip lossless
  CHECK: cd work/ostendorf && V=~/.venvs/srom/bin/python; S=../../.claude/skills/srom-produkcja/scripts; $V $S/check.py ostendorf_src.md --refs refs.json | tail -1; $V $S/build.py ostendorf_src.md --refs refs.json --source --out build/ 2>/dev/null | tail -1; $V $S/docx_in.py ostendorf_src_robocza.docx -o /tmp/rt.md | tail -1; diff <(sed 's/ *<!--.*-->//' ostendorf_src.md) /tmp/rt.md | grep -c "^[<>] ."
  EXPECT: /CHECK OK\s+PROOF .*\(0 issue[\s\S]*IMPORT OK\s+0\s*$/
  EVIDENCE: CHECK OK | PROOF … (0 issue(s)) | IMPORT OK | 0
- [x] O6: CSL no longer drops data: editor of an authored book, "trans. and ed." once, anonymous chapter title-first
  (provisional, decisions.md 23, D19 A3); query sheet without CSL tags
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_csl.py | tail -3
  EXPECT: /NOTES ALL PASS (\d+)\/\1\s+BIB ALL PASS (\d+)\/\2/
  EVIDENCE: NOTES ALL PASS 27/27 | BIB ALL PASS 13/13 (new cases fail on the old CSL)
- [x] O7: hand-off: T19 to srom-tlumacz (rights pending), D19 for MB, both committed in _handoffs; queries file with
  verified evidence (Thwaites vol. 67, catalogue records, Crossref)
  CHECK: grep -c "^## T19" ../_handoffs/produkcja-to-tlumacz.md; grep -c "^### D19" ../_handoffs/MB-decisions.md; git -C ../_handoffs status --porcelain | wc -l
  EXPECT: /^1\s+1\s+0\s*$/
  EVIDENCE: 1 | 1 | 0
- [x] O8: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 18/18 | 0

## Stage-1 test 5 — Tittel (On_Culture 10, 2020; endnotes, Chicago full notes with place/publisher) — done 28.09.2026

- [x] T1: extractor handles the On_Culture layout generically, each with a test (test_pdf_onculture.py): underscore-decorated
  headings, front matter over two pages, justified block quotations not verse, URL closed by ">", URL hyphen decided by the
  document, hyphen before an opening quotation mark
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_pdf_onculture.py | tail -1
  EXPECT: /PDF-ONCULTURE ALL PASS (\d+)\/\1/
  EVIDENCE: PDF-ONCULTURE ALL PASS 11/11 (10 of the 11 fail on the pre-change extractor; the verse control passes on both)
- [x] T2: no regression on the earlier PDFs (Ndiaye, Pahulich, Ostendorf, Scheffknecht identical to HEAD's extractor)
  CHECK: see EVIDENCE (scratchpad baselines, HEAD's pdf_extract.py run side by side)
  EVIDENCE: all four byte-identical to HEAD's output; the two diffs against the stored extractions (Ndiaye
  "African- American", Pahulich "religio-political") come from earlier commits, listed in tittel_queries C
- [x] T3: the article extracts clean: 101 notes, 101 markers; every word and number of the PDF in the extraction
  CHECK: cd work/tittel && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/pdf_extract.py ../Racial_and_Social_Dimensions_of_Antiziga.pdf -o /tmp/t.md | tail -2
  EXPECT: /notes 101 · markers 101[\s\S]*EXTRACT OK/
  EVIDENCE: notes 101 · markers 101 · EXTRACT OK; wordcheck.py: 10 896 tokens, differences = line-end hyphen decisions only
- [x] T4: refs.json (63 works, from the notes; one gap [BRAK WYDAWCY] listed); keying proven, the keyed check mutation-tested
  (mutations: cut page after "here:", dropped AA page ×2, statute vol. III for vol. IV, wrong Zeller page, cut MEW range,
  Zeller Bd. 12 for Bd. 13, changed Ufen page — all errors after 7f671f5; before it, 4 of the first 6 passed)
  CHECK: cd work/tittel && ~/.venvs/srom/bin/python refs.py >/dev/null && ~/.venvs/srom/bin/python key.py >/dev/null && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed tittel_pre.md tittel_src.md --refs refs.json | grep -c "WARN\|ERROR"; ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed tittel_pre.md tittel_src.md --refs refs.json | tail -1
  EXPECT: /^0\s+CHECK OK\s*$/
  EVIDENCE: 0 | CHECK OK
- [x] T5: source checks, builds as a source proof with 0 issues; Word working copy round trip lossless
  CHECK: cd work/tittel && V=~/.venvs/srom/bin/python; S=../../.claude/skills/srom-produkcja/scripts; $V $S/check.py tittel_src.md --refs refs.json | tail -1; $V $S/build.py tittel_src.md --refs refs.json --source --out build/ 2>/dev/null | tail -1; $V $S/docx_in.py tittel_src_robocza.docx -o /tmp/rt.md | tail -1; diff <(sed 's/ *<!--.*-->//' tittel_src.md) /tmp/rt.md | grep -c "^[<>] ."
  EXPECT: /CHECK OK\s+PROOF .*\(0 issue[\s\S]*IMPORT OK\s+0\s*$/
  EVIDENCE: CHECK OK | PROOF … (0 issue(s)) | IMPORT OK | 0
- [x] T6: hand-off: T20 to srom-tlumacz, D20 for MB, both committed in _handoffs
  CHECK: grep -c "^## T20" ../_handoffs/produkcja-to-tlumacz.md; grep -c "^### D20" ../_handoffs/MB-decisions.md; git -C ../_handoffs status --porcelain | wc -l
  EXPECT: /^1\s+1\s+0\s*$/
  EVIDENCE: 1 | 1 | 0
- [x] T7: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: SUITE ALL PASS 19/19 | 0
- [x] O9 (after MB's answers): licence verified on the publisher's pages (CC BY-NC 4.0); imprint gaps sourced with evidence;
  the rest listed for MB; Kanon § 7.2/§ 9.3/§ 9.5 with tests
  CHECK: cd work/ostendorf && grep -c "BRAK MIEJSCA\]\|BRAK WYDAWCY\]" build/ostendorf_src_pytania.md; ~/.venvs/srom/bin/python -c "import json;print(sum(1 for r in json.load(open('refs.json')) if r.get('srom-sourced')))"
  EXPECT: /^14\s+43\s*$/
  EVIDENCE: 14 | 43 (43 works, one value each; the 14 in ostendorf_queries A2)

## House style v3 — InDesign styles (MB's style discussion) — done 29.09.2026

Brief: vol. 18's main styles untouchable (body 10.5/13 on the 13.2945 grid, notes 9/10.8, Cambria, tracking/H&J);
≈20 styles a designer can work with, most used at the root; script for a blank document (purge + build); v2 kept.

- [x] S1: v2 kept, runnable on its own
  CHECK: ls .claude/skills/srom-produkcja/indesign/legacy/v2/; grep -c '"groups"' .claude/skills/srom-produkcja/indesign/legacy/v2/srom_style_setup.jsx
  EXPECT: /README\.md[\s\S]*srom_style_setup\.jsx[\s\S]*style_spec\.json[\s\S]*\n1\s*$/
  EVIDENCE: README.md make_style_setup.py srom_style_setup.jsx srom_style_setup.jsx.tpl style-sheet.md style_spec.json | 1
- [x] S2: spec consistent, script and style sheet current, sacred values, every vol. 18 style mapped, kept styles = dump/*.idml
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_jsx.py | tail -2
  EXPECT: /kept styles resolve to the vol\. 18 values[\s\S]*STYLES ALL PASS (\d+)\/\1/
  EVIDENCE: PASS kept styles resolve to the vol. 18 values (dump/*.idml; 232 values compared) | STYLES ALL PASS 17/17
  (mutation: Bibliografia 10 → 10.2 pt fails it)
- [x] S3: in InDesign: the script ends RESULT: OK on both vol. 18 files and a blank document; with the two deliberate
  changes undone the PDF equals vol. 18 line for line; page counts kept; panel order = spec
  CHECK: ~/.venvs/srom/bin/python tools/indesign_check/indesign_check.py | tail -1   (InDesign running)
  EXPECT: /INDESIGN CHECK ALL PASS (\d+)\/\1/
  EVIDENCE: INDESIGN CHECK ALL PASS 11/11 (Ellis 603/603, Konferencja 468/468 lines; 14 → 14 and 12 → 12 pages)
- [x] S4: build emits only v3 names; lists get a typed dash; dialogue in Cytat with Pogrubienie labels
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_e2e.py | tail -1
  EXPECT: /E2E ALL PASS (\d+)\/\1/
  EVIDENCE: E2E ALL PASS 75/75
- [x] S5: a test that crashes after an early verdict fails the suite
  CHECK: grep -c "a crash after an early verdict must not pass" .claude/skills/srom-produkcja/tests/run_all.py
  EXPECT: 1
  EVIDENCE: 1
- [x] S6: suite green, committed; D3 closed and D21 filed in _handoffs, committed
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; grep -c "^### D3 " ../_handoffs/MB-decisions.md; grep -c "^### D21" ../_handoffs/MB-decisions.md
  EXPECT: /SUITE ALL PASS (\d+)\/\1\s+0\s+1\s*$/
  EVIDENCE: SUITE ALL PASS 19/19 | 0 | 1 (commits 81babb2; _handoffs 4e5d41f)

## Stage-1 test 6: West Ohueri (Off White, MUP 2024, ch. 6) — done 29.09.2026

Source: MB's manchesterhive PDF (`work/Peripheral whiteness …pdf`), Chicago endnotes (British: 'single quotes', "40:3
(2021)"), no bibliography, CC BY-NC-ND 4.0. Work folder `work/westohueri/` (git-ignored); MB's points `MB-decisions.md` D24.

- [x] W1: every word and number of the PDF is in the extraction (small-caps font read as capitals: "1000 BCE")
  CHECK: cd work/westohueri && ~/.venvs/srom/bin/python wordcheck.py westohueri.pdf westohueri_pdf.md westohueri_pdf_front.md westohueri_pdf_extract.md | tail -1; grep -c "1000 BCE" westohueri_pdf.md
  EXPECT: /TOKENS \d+ in PDF · lost 2 · extra 2\s+1\s*$/
  EVIDENCE: TOKENS 8431 in PDF · lost 2 · extra 2 | 1 (lost: the "Notes" heading; a URL hyphen the checker joins itself)
- [x] W2: keying complete: no page, note or work lost
  CHECK: cd work/westohueri && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/check.py --keyed westohueri_pre.md westohueri_src.md --refs refs.json | tail -1
  EXPECT: CHECK OK
  EVIDENCE: CHECK OK (no warnings)
- [x] W3: the check catches keying errors (mutation test; before the fixes of 950f46e: 5 of 17 hand-made mutants missed;
  the generic `mutate_keyed.py` then found the "(eds)" hole, fixed)
  CHECK: cd work/westohueri && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/mutate_keyed.py westohueri_pre.md westohueri_src.md --refs refs.json | tail -1
  EXPECT: /MUTATIONS CAUGHT (\d+)\/\1/
  EVIDENCE: MUTATIONS CAUGHT 40/40
- [x] W4: source proof builds with 0 issues; quotations without a page reach the query sheet
  CHECK: cd work/westohueri && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/build.py westohueri_src.md --refs refs.json --out build/ --source | tail -1; grep -c "cytat bez numeru" build/westohueri_src_pytania.md
  EXPECT: /0 issue\(s\)[\s\S]*\n13\s*$/
  EVIDENCE: PROOF — … (0 issue(s) …) | 13
- [x] W5: DOIs equal Crossref's volume/issue/pages; Word round trip lossless
  CHECK: cd work/westohueri && grep -c "^[a-z0-9]*: 10\." doi_check.txt; grep -c MISMATCH doi_check.txt; ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/docx_in.py westohueri_src_robocza.docx -o /tmp/claude-501/rt.md | tail -1
  EXPECT: /^16\s+0\s+IMPORT OK\s*$/
  EVIDENCE: 16 | 0 | IMPORT OK (pandoc AST of the import = the source without its comments, which travel as Word comments)
- [x] W6: suite green, toolchain commits by path; T23 and D24 in _handoffs, committed
  CHECK: python3 .claude/skills/srom-produkcja/tests/run_all.py | tail -1; grep -c "^## T23" ../_handoffs/produkcja-to-tlumacz.md; grep -c "^### D24" ../_handoffs/MB-decisions.md
  EXPECT: /SUITE ALL PASS (\d+)\/\1\s+1\s+1\s*$/
  EVIDENCE: SUITE ALL PASS 19/19 | 1 | 1 (commits 950f46e, 9163315, 4a088a2; _handoffs 948e66e, 6b27bfe)

## House style v3, round 2 (MB 29.09.2026: § 3.4 ruling, junk, final pass, template) — done 29.09.2026

- [x] R1: Kanon § 3.4: no-italics rule governs the text, not display elements (MB); RULES digest; § 17 row; D21 closed
  CHECK: grep -c "wydzielonych składu" .claude/skills/srom-kanon/references/kanon-redakcyjny.md; grep -c "not display elements" .claude/skills/srom-kanon/RULES.md; grep -c "D21" ../_handoffs/MB-decisions.md
  EXPECT: /^2\s+1\s+0\s*$/
  EVIDENCE: 2 | 1 | 0 (gates R1–R4 entered GATES.md in another session's commit 42a2397; evidence added here)
- [x] R2: junk out of the spec (hyphenation zone, auto-leading; sink rule colour None), headings keep with next (§ 3.6);
  the control run still equals vol. 18 line for line; keep-with-next changes only the stranded speaker (Konferencja p. 6)
  CHECK: ~/.venvs/srom/bin/python tools/indesign_check/indesign_check.py --no-final | grep "control =\|keep-with-next\|ALL PASS"
  EXPECT: /603\/603[\s\S]*468\/468[\s\S]*Tobi Górniak[\s\S]*INDESIGN CHECK ALL PASS/
  EVIDENCE: control 603/603 and 468/468; keep-with-next moves text only from Konferencja p. 6 ('> Tobi Górniak'); page counts kept
- [x] R3: srom_final_pass.jsx generated from the spec, ES3, one undo step, all § 3.6 checks; runs on both vol. 18 files;
  fix mode never leaves more problems, never adds overset or pages
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_jsx.py | tail -1; ~/.venvs/srom/bin/python tools/indesign_check/indesign_check.py | grep "final pass"
  EXPECT: /STYLES ALL PASS (\d+)\/\1[\s\S]*final pass fix mode/
  EVIDENCE: STYLES ALL PASS 23/23 | Ellis 8 problems → 5 (p. 8 szewc fixed by −10 on the paragraph above; pp. 10–11 note split
  gone with it), Konferencja 4 → 3 (empty last line p. 12); no new overset, page counts kept; INDESIGN CHECK ALL PASS 25/25
- [x] R4: clean template SROM_szablon_v3.idml: built from Ellis, re-opened: 29 + 8 styles, grid, footnotes, nothing overset
  CHECK: ~/.venvs/srom/bin/python tools/indesign_check/indesign_check.py --no-final --template /tmp/t.idml | grep "template"
  EXPECT: /PASS template built[\s\S]*PASS template re-opened/
  EVIDENCE: PASS template built (RESULT: OK) | PASS template re-opened: 29 + 8 styles, grid, footnotes in Przypis; preview checked
  by eye (title block, running heads towards the spine, numbers outside, as vol. 18)
- [x] W7 (after MB's answers 29.09.2026): Baker's chapter keyed (n. 29), name "Ohueri, Chelsi West", Albanian words italic
  in the roman blocks; queries and D24 cleaned; T24 with new sha256
  CHECK: cd work/westohueri && grep -c "@baker2024" westohueri_src.md; grep -c '"family": "Ohueri"' refs.json; grep -c "\*jevgjit\*" westohueri_src.md; grep -c "see also Baker, this volume\|A3 the dissertation" ../../../_handoffs/MB-decisions.md
  EXPECT: /^1\s+2\s+3\s+0\s*$/
  EVIDENCE: 1 | 2 | 3 | 0
- [x] W8: mutation test on every keyed text (MB 29.09.2026: one per text, SKILL.md step 4b); holes found are fixed in
  check.py with tests ("(eds)" before the title — West Ohueri n. 48; surname-only short forms — Ndiaye nn. 60, 120)
  CHECK: cd work && for a in tittel ostendorf scheffknecht; do (cd $a && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/mutate_keyed.py ${a}_pre.md ${a}_src.md --refs refs.json | tail -1); done; cd ndiaye && ~/.venvs/srom/bin/python ../../.claude/skills/srom-produkcja/scripts/mutate_keyed.py ndiaye_pdf.md ndiaye_src.md --refs refs.json | tail -1
  EXPECT: /(MUTATIONS CAUGHT (\d+)\/\2\s*){4}$/
  EVIDENCE: 40/40 each (Tittel, Ostendorf, Scheffknecht, Ndiaye; Ndiaye 38/40 before the surname-only rule). Pahulich is
  author-date (cite_map), not keyed: not applicable

## Review 29.09.2026 follow-up (E17–E19, hand-back contract, stale text) — done 29.09.2026

- [x] V1: kartoteka rows for E17 / E18 [Pahulich] (Anglo-Romani, Manoush, foreign exonyms), Kanon test green
  CHECK: grep -c "^Anglo-Romani	" .claude/skills/srom-kanon/references/kartoteka.tsv; grep -c "Manoush" .claude/skills/srom-kanon/references/kartoteka.tsv; grep -c "^Zinganées	" .claude/skills/srom-kanon/references/kartoteka.tsv; ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_kanon.py | tail -1
- [x] V2: Pahulich title glosses (E18 [Pahulich] 1) in refs.json; D18 A5 applied in Scheffknecht
  CHECK: grep -c "etnografii rodzimej\|szkic historyczno-etnograficzny\|kształtowanie się etnosu\|powieści i opowiadania\|status prawny i społeczny" work/pahulich/refs.json; grep -c '"dropping-particle": "von"' work/scheffknecht/refs.json
- [x] V3: B11 (Tittel), B12–B14 (Ostendorf) in the queries files
  CHECK: grep -c "^- \*\*B11\*\* (29.09" work/tittel/tittel_uwagi.md; grep -c "^- \*\*B1[234]\*\*" work/ostendorf/ostendorf_uwagi.md
- [x] V4: hand-back contract: take_back.py + test, handoff.md "Back", scenario C; committed
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_takeback.py | tail -1; git log --format=%s | grep -c "^Contract, hand-back"
- [x] V5: T25 (answers + status lines for E17–E19) and T26 committed in _handoffs
  CHECK: git -C ../_handoffs log --format=%s | grep -c "^typeset: T25\|^typeset: T26"
- [x] V6: stale text: quick rule 9, decisions row 21, handover (no D21 open, G12 translated, 5a/5b), gate rule
  CHECK: grep -c "not in display elements" .claude/skills/srom-kanon/SKILL.md; grep -c "MB-decisions D21\.$\|D21 (speaker" .claude/skills/srom-produkcja/references/decisions.md docs/HANDOVER-produkcja.md; grep -c "a translated article" docs/HANDOVER-produkcja.md; grep -c "not files meant to change later" CLAUDE.md

## Ostendorf INJECT test (MB, 02.10.2026) — Kanon v1.11, DOCX/template/report fixes — done 02.10.2026

- [x] O1: editor first only for an edited volume; `classic` and edited articles title first; bibliography without the comma
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_csl.py | tail -3
  EXPECT: /NOTES ALL PASS[\s\S]*BIB ALL PASS[\s\S]*POSITION ALL PASS/
- [x] O2: headings unnumbered; DOCX styles carry alignment and the Cambria default font
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_e2e.py | grep -c "PASS headings unnumbered\|PASS DOCX styles carry\|PASS DOCX default font"
  EXPECT: /^3$/
- [x] O3: template v3 rebuilt (gaps, no dot after the note number, range rule, every DOCX style at the root) and checked in InDesign
  CHECK: grep -c '"group": "Rzadkie"' .claude/skills/srom-produkcja/indesign/style_spec.json; unzip -p .claude/skills/srom-produkcja/indesign/SROM_szablon_v3.idml Resources/Styles.xml | grep -c 'ParagraphStyleGroup[^>]*Rzadkie'
  EXPECT: /^0\s+0$/
  EVIDENCE: indesign_check.py --template: INDESIGN CHECK ALL PASS 26/26 (control = vol. 18 603/603, 468/468)
- [x] O4: Kanon v1.11 everywhere it is cited
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS/
- [x] O5: post-import check: real attributes, duplicate styles, `~"`, notes in text order, attention list at the end
  CHECK: grep -c 'notesInOrder\|exists twice\|"~\\""' .claude/skills/srom-produkcja/indesign/srom_postimport.jsx.tpl
  EXPECT: /^[3-9]$/
  EVIDENCE: in InDesign: MB's test file → 6 items (duplicate Przypis GWIAZDKOWY, 185 left-aligned paragraphs, Aptos);
  the rebuilt DOCX in the rebuilt template → "RESULT: OK — import is clean"; Ibidem finds nn. 18, 22 on page turns

## SYS-5 DOI links in the online PDF (02.10.2026 22:11, root session, MB's request)
- [x] S1: build writes <stem>_doi.jsx (citation texts per note cut apart, bibliography entries, encoded URLs); invisible links, rerun replaces
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-produkcja/tests/test_doi.py | tail -1
  EXPECT: /DOI ALL PASS/
  EVIDENCE: live in InDesign 2026, tools/indesign_check/doi_check.py: Ostendorf INJECT build 36/36 links (19 note citations,
  17 bibliography entries, 17 DOIs), SICI + "#?" DOIs 6/6, border 0, URLs encoded in the PDF — INDESIGN DOI CHECK ALL PASS 7/7 both
