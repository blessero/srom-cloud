# Gates: queue items 2 (kanon ↔ typeset overlap) and 3 (E8 asterisk notes) — 26.09.2026

Scope: the Polish Kanon becomes the master text inside srom-kanon (v1.6, with decisions and draft § 12.2);
srom-typeset stops bundling the linter and cites only Kanon sections that exist; non-author notes leave the
numbered footnotes and become one asterisk series (placed by hand above the numbered notes, footnote style).
Checks run from the repo root. K = .claude/skills/srom-kanon, T = .claude/skills/srom-typeset.

## Item 2 — overlap

- [x] A1: the Kanon lives in srom-kanon as references/kanon-redakcyjny.md, version 1.6
  CHECK: head -3 .claude/skills/srom-kanon/references/kanon-redakcyjny.md
  EXPECT: Wersja 1.6
  EVIDENCE: # STUDIA ROMOLOGICA – KANON EDYTORSKI (DOKUMENT WEWNĘTRZNY) | **Wersja 1.6 · obowiązuje od tomu 19/2026 · do użytku redakcji i składu**

- [x] A2: RULES.md is v1.6, names the Kanon as normative, no "canon governs" clause pointing outside the skill
  CHECK: head -3 .claude/skills/srom-kanon/RULES.md; grep -c "canon governs" .claude/skills/srom-kanon/RULES.md || true
  EXPECT: /v1\.6[\s\S]*references\/kanon-redakcyjny\.md[\s\S]*\n0\s*$/
  EVIDENCE: Normative text: `references/kanon-redakcyjny.md` — *Kanon edytorski Studia Romologica* (Polish, internal), in this skill. This file is its compact English digest; **section numbers are the Kanon's**. 

- [x] A3: srom-typeset no longer bundles the linter
  CHECK: test -e .claude/skills/srom-typeset/scripts/lint_srom.py && echo BUNDLED || echo GONE
  EXPECT: GONE
  EVIDENCE: GONE

- [x] A4: build without srom-kanon fails with a clear message naming srom-kanon; test_kanon.py checks versions and every § reference in srom-typeset against the Kanon's headings
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-typeset/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS \d+\/\d+/
  EVIDENCE: KANON ALL PASS 11/11

- [x] A5: decisions 1–9, 11–14, 16, 17 written into the Kanon in Polish, each in its own section; § 17 has a 1.6 row
  EVIDENCE: kanon-redakcyjny.md: [16]→§0, [13]→§3.3, [11]→§3.4, [17]→§4.1 (verse; §5.3/§10.1 already had examples/tables), [1][9] + E8→§7.1, [7]→§7.2 + §16, [2][3][8]→§7.3, [14]→§7.4, [12]→§8.6, [5]→§9.2, [6]→§9.3, [4]→§9.7; [10] was already in §2. 17 marker phrases grep-found; § 17 line 606 `| 1.6 | …`. [15][18][19] kept in srom-typeset as toolchain conventions (not house rules) — reported to the editor.

- [x] A6: draft § 12.2 (srom-tlumacz, settled 25.09.2026) incorporated, with its consequential edits in § 1, § 4.2, § 6.3, § 11
  CHECK: grep -c "^### 12.2\|§ 12.2" .claude/skills/srom-kanon/references/kanon-redakcyjny.md
  EXPECT: /\b(1[0-9]|[2-9][0-9])\b/
  EVIDENCE: 13

- [x] A7: RULES.md digest carries the same changes (English), each section pointing to its Kanon §; Ibidem "same column"
  EVIDENCE: RULES.md rewritten with Kanon numbering (§3.5, §5, §6, §9.6, §10, §11, §12.2 new/moved); test_kanon: 'every numbered RULES.md section exists in the Kanon' PASS; 'same column' at RULES.md:101 and §J 3; §J 15–16 added.

- [x] A8: decisions.md reduced to rule → implementing file/test map + implementation conventions + open items 20–22
  EVIDENCE: references/decisions.md: 24-row Kanon §→code→test table, 4 toolchain conventions ([15][18][19], E8), open 20–22. Two untested rules found while mapping (§8.6 hyperlinks, §7.4 multi-paragraph notes) → tests added to test_e2e (59/59).

- [x] A9: srom-kanon SKILL.md and linter docstring say v1.6; SKILL.md sends production linting to srom-typeset's build
  CHECK: grep -h "v1\.[0-9]" .claude/skills/srom-kanon/SKILL.md .claude/skills/srom-kanon/scripts/lint_srom.py | grep -v "1\.6" | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

## Item 3 — E8

- [x] B1: build turns "– przyp. tłum./red." notes into a marker (character style) + paragraphs in "Przypis gwiazdkowy" at the end of the DOCX, title note first; numbered footnotes exclude them
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-typeset/tests/test_e8.py | tail -1
  EXPECT: /E8 ALL PASS \d+\/\d+/
  EVIDENCE: E8 ALL PASS 18/18

- [x] B2: no Ibidem in an asterisk note, none in a numbered note that follows one (covered in test_e8.py)
  EVIDENCE: test_e8 'PASS no Ibidem inside an asterisk note (short form instead)' and 'PASS numbered note after a non-author note: Ibidem replaced by the short form, reason in the report' (build.py after_na / ast_divs).

- [x] B3: check.py: [^r<n>] must end "– przyp. red." ([^t<n>] "– przyp. tłum."), in single and pair mode; r-notes left out of the pair comparison (covered in test_e8.py / test_check.py)
  EVIDENCE: test_check 40/40 incl. 5 new E8 cases (r-note excluded; r without formula ERROR; t with red formula ERROR; single-file check; '[… – przyp. tłum.]' closing an author's note stays compared — a latent bug in the old TN_FORMULA, fixed); test_e8 '[^r1] without … fails the build', 'printed numbers skip translator/editorial notes'.

- [x] B4: _postimport.jsx counts markers vs asterisk notes and flags a formula inside a numbered footnote; _gwiazdki.jsx (after layout) lists every asterisk note with page and asterisk count; both ES3
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-typeset/tests/test_jsx.py | grep -c "acorn es3"
  EXPECT: /\b[3-9]\b/
  EVIDENCE: 3

- [x] B5: style spec: "Przypis gwiazdkowy" based on "Przypis" (no own values), replaces "Przypis do tytułu"; character style "Odsyłacz gwiazdkowy"; setup JSX + style sheet regenerated
  CHECK: grep -c "Przypis gwiazdkowy\|Odsyłacz gwiazdkowy" .claude/skills/srom-typeset/references/style-sheet.md .claude/skills/srom-typeset/config/styles.json
  EXPECT: /style-sheet\.md:[1-9][\s\S]*styles\.json:[1-9]/
  EVIDENCE: .claude/skills/srom-typeset/references/style-sheet.md:2 | .claude/skills/srom-typeset/config/styles.json:2

- [x] B6: docs updated: no "numbered with the author's notes" left; srom-md, handoff, indesign, SKILL describe the series
  CHECK: grep -rn "numbered with the author" .claude/skills/srom-typeset | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

## Global

- [x] Z1: full suite green
  CHECK: python3 .claude/skills/srom-typeset/tests/run_all.py | tail -1
  EXPECT: /SUITE ALL PASS 1[1-9]\/1[1-9]/
  EVIDENCE: SUITE ALL PASS 11/11

- [x] Z2: committed, working tree clean
  CHECK: git status --porcelain | wc -l
  EXPECT: /^\s*0\s*$/
  EVIDENCE: 0

---

# Gates: batch 27.09.2026 — delegated decisions, E12, kartoteka (D9), E10

Scope: MB delegated D1, D2, D9, D8(e)→E12 and decisions 15/18/19 to srom-typeset (27.09.2026); record them,
put E12 into the Kanon, create the kartoteka from srom-tlumacz's seed, implement E10 (translator in YAML front
matter), re-scope D3/D7 (InDesign later; stage-1 test on MB's PDF next), answer srom-tlumacz.

- [ ] C1: MB-decisions.md records D1, D2, D9, D8(e)/E12 decisions and the D3/D7 re-scope
  CHECK: grep -c "delegated the call to srom-typeset\|re-scoped" ../_handoffs/MB-decisions.md
  EXPECT: /\b([5-9]|1[0-9])\b/
  EVIDENCE: pending

- [ ] C2: Kanon § 3.4, § 6.2, § 14, § 17 carry the exonym rule; RULES.md digest too
  CHECK: grep -c "egzonim" .claude/skills/srom-kanon/references/kanon-redakcyjny.md; grep -c "exonym" .claude/skills/srom-kanon/RULES.md
  EXPECT: /\b[4-9]\b[\s\S]*\b[2-9]\b/
  EVIDENCE: pending

- [ ] C3: kartoteka.tsv in srom-kanon, all 35 seed rows, house italics column, no open flags; structure test passes
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-typeset/tests/test_kanon.py | tail -1
  EXPECT: /KANON ALL PASS \d+\/\d+/
  EVIDENCE: pending

- [ ] C4: E10 — handoff.md + srom-md.md document `tlumaczenie:`; build reports translators_struct; survives the Word round trip
  CHECK: ~/.venvs/srom/bin/python .claude/skills/srom-typeset/tests/test_e10.py | tail -1
  EXPECT: /E10 ALL PASS \d+\/\d+/
  EVIDENCE: pending

- [ ] C5: typeset-to-tlumacz.md answers E12, reports E10 done (their test side), kartoteka created
  CHECK: grep -c "^## T[6-9]" ../_handoffs/typeset-to-tlumacz.md
  EXPECT: /\b[2-9]\b/
  EVIDENCE: pending

- [ ] C6: suite green, committed, clean tree
  CHECK: python3 .claude/skills/srom-typeset/tests/run_all.py | tail -1; git status --porcelain | wc -l
  EXPECT: /SUITE ALL PASS (\d+)\/\1[\s\S]*\n\s*0\s*$/
  EVIDENCE: pending
