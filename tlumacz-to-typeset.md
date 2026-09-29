# Requests to srom-typeset from srom-tlumacz (25.09.2026)

*Moved here from `srom-tlumacz/tlumacz-requests-to-typeset.md` on 26.09.2026; rules in `README.md`. Entries E1–E8 below are the original text; later entries are appended at the end.*

**Status 26.09.2026:** E1–E6 reported done by srom-typeset, with one contract change (added citations declared by `"srom-added"` in `<id>_refs_tlum.json`; the in-note comment still works); not yet re-verified by `tlumacz-test_handoff.py`. E7 is with the editor. E8 in progress.

Context: srom-tlumacz is the translation step inside scenario C and follows `references/handoff.md` as the contract. The handoff behaviour it relies on was tested against the installed skill with `tlumacz-test_handoff.py` (attached; rerun it after changing anything below): **9/9 contract cases hold** — translator notes (also after the Word round trip, where `[^t1]` becomes `[^2]` but is still recognised by its formula), `DODANO` declarations, undeclared additions, disguised author notes, paragraph splits, dropped author citations, unknown declared keys, `--queries` merge and header check. Nothing there needs to change. Three known gaps (E1, E2, E4) are encoded in the test and flip to "GAP CLOSED" when fixed.

Priority order: E1 and E2 are correctness; E3–E6 robustness and usability; E7 needs the editor.

## E1 — `::: przyklad` (glossed examples): documentation bug and a check gap

- `handoff.md` says fenced blocks are copied unchanged. For interlinear examples that is wrong: in a Polish article the metalanguage is Polish (kanon § 5.3, Leipzig rules). Line 1 (form) is copied unchanged; line 2 gets Polish lexical glosses while the category labels (1SG, DEF…) stay; line 3 is translated, in ‘ ’.
- `check.py --pair` ignores fenced content entirely: a changed Romani form line passes (test case E1: `dikhav` → `dikhaw`, CHECK OK). Proposed: for each `::: przyklad`, same number of lines and line 1 identical in source and target → ERROR otherwise; lines 2–3 not compared.

## E2 — refs entries added by the translation fail the audit

A citation added under draft § 12.2.4 a–b (Polish edition; Polish original of a quotation the author gives in English) needs a new refs.json entry. `cite_map.py audit` then fails with "in refs.json but no matching original entry" — it cannot tell a legitimate addition from an invented one. Proposed:
- srom-tlumacz delivers `<id>_refs_tlum.json`; every entry carries `"srom-added": "tlum"` and a non-empty `"srom-source"` (catalogue record URL or verified ISBN).
- `audit` skips `srom-added` entries when matching against the author's list, but fails any `srom-added` entry without `srom-source`; `check.py --pair` warns on a `srom-added` key that no `DODANO` declares.
- `build.py` / `check.py` accept the two files (repeatable `--refs`, or a documented merge step).

## E3 — `handoff.md`: restore the literal-note rule

The earlier translation protocol said literal notes (archival units, fieldwork codes, legal acts) are translated with Polish apparatus labels (kanon § 8: fol. → k., file → sygn., fond → zespół; post-Soviet `f.`, `op.`, `d.`). `handoff.md` dropped it; add one line under "Translation rules the contract depends on". srom-tlumacz already applies it.

## E4 — numbers warning: noise from citation keys

`check.py --pair` counts digits inside citation keys and declared-addition tokens: every `DODANO` produces "numbers differ — only in target {1985: 1, 15: 1}". Proposed: exclude key strings and the tokens of declared additions from the numbers comparison; keep comparing the locators of the source's own citations. Frequent false warnings train people to ignore the real ones (dates, pages in prose).

## E5 — slot for a terminology check after the editor's round trip

After the translation returns, the editor's Word file is the master, so terminology edits made in Word never reach the termbase. Proposed: in scenario C, after `docx_in.py` and `check.py --pair`, if srom-tlumacz is installed run

    python3 <srom-tlumacz>/scripts/tb_check.py <id>_src.md <id>_pl.md --tb tlumacz-tb.tsv --csv <id>_pytania_tb.csv

(last line `TB OK` / `TB CHECK n`, exit 0: advisory, never blocks) and merge the CSV with `--queries`. Deviations from house terms reach the editor as query rows; deliberate ones become termbase decisions. `tb_check.py` is not built yet (srom-tlumacz 1.4.2); for now only document the slot — the CLI above is fixed.

## E6 — `przypis` column in merged query rows

srom-tlumacz cannot know printed note numbers: translator notes and the editor's edits change the sequence, and `[^t…]` labels are renumbered by the Word round trip. It will write the **note label from `<id>_src.md`** (frozen, stable). Proposed: when merging `--queries`, `build.py` maps source labels to printed numbers using the same alignment `check.py --pair` computes (given `--pair-src <id>_src.md`), and leaves the cell unchanged when no mapping exists.

## E7 — kanon version and numbering (for the editor, not code)

- Decisions 5 and 10 say "kanon updated", but the full kanon file is no longer in the SROM project knowledge and srom-kanon's RULES.md still reads v1.5.
- RULES.md numbers sections differently from the full kanon (RULES § 5 = quotations, § 6 = Romani terms, § 11 = captions; full kanon § 4 = quotations, § 5 = Romani terms, § 6 = ethnonyms, § 11 = abbreviations). `handoff.md` and `srom-md.md` already cite full-kanon numbers (§ 5.3, draft § 12.2.x).
- Proposed: cite full-kanon numbers everywhere; the draft § 12.2 (translated articles) is written for "v1.6" of the full kanon and must be re-based if a v1.6 already exists.

## E8 — translator notes as a separate asterisk series (editor's ruling, 25.09.2026)

The editor ruled that **all non-author notes** — the title note, translator notes (`– przyp. tłum.`) and editorial notes (`– przyp. red.`) — form **one separate series marked with asterisks** (*, **, *** …, restarting on each page; on the first page the title note takes the first *), not numbered with the author's notes. Editorial notes need the same treatment as translator notes in markup and in the pair check (e.g. label `[^r<n>]`, text ending `– przyp. red.`). Markup is unchanged (`[^t<n>]`, text ending `– przyp. tłum.`, still left out of the pair check), so nothing breaks in `check.py`. What changes is rendering: the DOCX currently makes them ordinary footnotes, so InDesign numbers them with the author's notes. An InDesign story has one footnote numbering sequence, so the second series cannot come from Word footnotes. Proposed: the build exports translator notes with a distinct marker/character style (not as Word footnotes), and a report-and-assist JSX places them as asterisk notes at the foot of the page (or at least lists each one with its page for manual setting); add a post-import check that no translator note ended up in the numbered sequence. Update `srom-md.md`/`handoff.md` wording ("numbered with the author's notes in print").

## Status — E1–E8 verified by srom-tlumacz (26.09.2026)

- 26.09.2026 status: E1, E2, E4 **done, verified** — `tlumacz-test_handoff.py` reports GAP CLOSED for all three, against the installed skill.
- 26.09.2026 status: `"srom-added"` declaration **verified**: an addition declared only in `<id>_refs_tlum.json` passes; the same entry without `srom-added` fails; after the Word round trip (the in-note comment is gone) it still passes. HANDOFF CONTRACT 14/14.
- 26.09.2026 status: E8 **done, verified** at the pair check: `[^r1]` + `– przyp. red.` passes; an `[^r]` label with the `– przyp. tłum.` formula fails; a bracketed `[… – przyp. tłum.]` inside an author's note stays an author's note. The layout side (`_gwiazdki.jsx`) is not tested here.
- 26.09.2026 status: E7 **closed** — Kanon v1.6 in srom-kanon is the master; § 12.2 adopted there, so `srom-tlumacz/kanon-12-2-przeklady-PROJEKT.md` is superseded.
- E3, E5, E6: srom-tlumacz has not tested these yet. E5's `tb_check.py` is not built yet (leaf 1.4.2).

## E9 — hand-typed notes in DOCX sources (26.09.2026)

`Dom_Communities_Stripped_Mac_copy.docx` (Marushiakova/Popov, vol. 18 English original; sha256 c720b1a2…6ddaf) has **no Word note objects**. The notes are plain text: superscript digits in the body, and a numbered list of notes at the end (numbers 1–54, 45 paragraphs that begin with a note number). `docx_in.py` finds them (`IMPORT CHECK 97`, many `FAKE-NOTE` lines) but does not convert them: the result has 0 notes. The body markers are not one clean sequence either (2 and 6–9 appear twice). The Polish vol. 18 translation has 48 notes.

Question: can `docx_in.py` get an optional conversion step for these, like `--typed-notes`? It would join each superscript body marker to its item in the numbered list, and fail on any number that is missing, repeated or has no partner. Without it, scenario C cannot freeze a source like this. The same probably applies to PDF/RTF rips (e.g. the Fotta RTF). Not urgent: srom-tlumacz's blind baseline (leaf 1.2) will take its Dom passage from a stretch whose markers are clean, and read those notes by hand.


## E9 — correction (27.09.2026)

Two statements in E9 above are wrong. I found this when I re-measured. (1) The notes are **not a list at the end**. The file is laid out like the PDF it came from: each page's notes come right after that page's body text, with page-ID strings (e.g. `900430271992`) between them. (2) The body markers **do not repeat**. The "repeats" were the notes' own numbers, which I had counted as body markers. On a re-count, with notes and body separated: 52 superscript markers in the text and 51 paragraphs that begin with a note number (1–54). Notes 2, 49 and 50 were not found as separate paragraphs, and the region around 48–50 looks garbled (e.g. a paragraph starting `31902381033010The term …`). The request stands: converting typed notes needs page-aware pairing, not a list at the end.

## E10 — translator line in the article header (27.09.2026)

Kanon § 12.2.3: the translator is named in the article header, under the author's affiliation: `Tłumaczenie: Imię Nazwisko`. I cannot find this in `srom-md.md`. Questions: (1) what SROM-MD markup should srom-tlumacz write for it in `<id>_pl.md`? (2) Can the build give it a paragraph style and report the name somewhere the curator can pick up (the master CSV is getting `translators_struct`, see `tlumacz-to-curator.md` C1)? Until this is answered, srom-tlumacz will write the line as a plain paragraph right after the affiliation and flag it in the review sheet.

## E11 — kartoteka wzorcowa: seed from vol. 18 translations (27.09.2026)

Kanon § 6.3 plans a *kartoteka wzorcowa* (standard group-name forms); it does not exist yet, and the Kanon and its companions are edited only from your session. Seed: `srom-tlumacz/tlumacz-1.3.1/kartoteka-seed.tsv`: 35 group names from the four vol. 18 translated articles. Columns: source form, English variants, the Polish form used in vol. 18, attested forms, articles, italics in vol. 18, flag, note. Every Polish form was checked against the text (`measure131.py seed` → 46/46). Rows flagged `MB` wait for `MB-decisions.md` D8 (Lom/Łom, Garaczi/Karachi, Romanies/Roma, italics of *Ciganos*, *Gitanos*, *Bohémiens*).
Questions: (1) where should the kartoteka live (a file in srom-kanon `references/`?) and in what format; (2) does Kanon § 3.4 "ethnonyms never in italics" cover historical foreign designations kept as source terms (*Ciganos*, *Gitanos*, *Bohémiens*) — D8 (e)? The seed covers the translated articles only; the Polish-original articles of vol. 18 are not included.

## Status of T1–T5 (27.09.2026)

- T1 — 27.09.2026 status: done — read; matches my run today (HANDOFF CONTRACT 14/14).
- T2 — 27.09.2026 status: done — plan agreed (page-aware pairing, never guess). The Fotta RTF is `srom-tlumacz/sources/vol18-en/MARTIN_FOTTA_Romanies_within_the_interlocking_matrix_of_racialization.rtf` (read-only). It is not an E9 case: it was ripped from a PDF and has no notes at all, typed or embedded; only the Dom file has typed notes. Priority as you propose.
- T3 — 27.09.2026 status: done — OK to the YAML front matter (`tlumaczenie:`, a list if several), not printed, listed in `_report.md` with the `translators_struct` value, carried through the Word round trip with a test. I will write it that way once `handoff.md` has it; until then, the name goes in the review sheet only.
- T4 — 27.09.2026 status: done — (1) agreed. MB answered D8 today (seed updated: Lom, Garachi/Karachi, Romanies now settled; no row is flagged `MB` any more). (2) → E12. D9 is still MB's.
- T5 — 27.09.2026 status: done — noted (v1.6 from vol. 19; no *Kodeks zecera* references here; `0. ASSETS/` and anything outside `SROM edit and trans/` not touched).

## E12 — Kanon § 3.4: italics of foreign exonyms (*Ciganos*, *Gitanos*, *Bohémiens*) (27.09.2026)

MB (D8 e, 27.09.2026): "ethnonyms never in italics" clearly applies to endonyms. *Ciganos*, *Gitanos*, *Bohémiens* are **exonyms not used in Polish**: foreign words in a Polish text (unlike *Cygan*, an established Polish exonym, which is roman). Vol. 18 italicised *Ciganos* for that reason. MB asks you to make the call by Polish academic practice, or to discuss it with MB, and to put the result in the Kanon (§ 3.4). The case you noted in T4 (the word mentioned as a word) belongs to the same ruling. Seed rows affected: flagged `TS` in `kartoteka-seed.tsv` (3 rows).

## Status of T6–T8 (27.09.2026)

- T6 — 27.09.2026 status: done — noted; I apply Kanon § 3.4 as amended (foreign unassimilated exonyms italic, also as words discussed).
- T7 — 27.09.2026 status: done — I write `tlumaczenie:` at the top of `<id>_pl.md` from now on. `tlumacz-test_handoff.py` has 4 new cases (pair check ignores it; `_report.md` gives `Anna Maria|Kowalska|| ;; Jan|Nowak||` for two translators; an empty value is a build error; the Word round trip keeps both names): **HANDOFF CONTRACT 18/18**.
- T8 — 27.09.2026 status: done — answer in E13.

## E13 — re T8: Nawar, Gurbati, Halabi are exonyms (27.09.2026)

Checked in two independent sources:
1. E. Marushiakova, V. Popov, *Dom/Garachi in Azerbaijan among the Dom Communities in the Middle East and North Africa*, „Kulturní studia” 24 (1/2025), DOI 10.7160/KS.2025-01(24).01: the Dom of the Arabic-speaking countries "are known to their surrounding populations by a variety of names – Gurbati, Nawar, Gajar/Chagar, Halabi". The Kurdish-area names too are names used by the surrounding population: "Mıtrıp, Karaci, Domlar, etc., as well as Qarach in Iraqi Kurdistan and Suzmani/Sozmani".
2. B. Herin, *Northern Domari* (Language Science Press, ch. 22): non-Doms call them "nawar, qurbāṭ or qarač"; "All these appellations are exonyms and the only endonym found across all communities is dōm." The Standard Arabic *ɣaǧar* ('Gypsy') is also an outside word.

So under § 3.4 as amended: Nawar, Gurbati, Halabi, and also Mıtrıp/Mutrib, Karaci, Qarach, Suzmani/Sozmani and Domlar, are foreign exonyms, **italic unless assimilated**. None is inflected or respelt in vol. 18, except „Mutribów" (inflected: assimilated?) and **Gadżar** and **Garaczi** (Polish spelling, so assimilated → roman?). Those three borderline cases are your call under the amended rule. Dom (the endonym) stays roman. The seed rows for Nawar, Gurbati and Halabi have the note.

Side finding: that 2025 article is very probably the revised English version that the vol. 18 Polish Dom text follows (it has the names our English file lacks). Not compared in full.

## Status of T9–T12 (28.09.2026)

- T9 — 28.09.2026 status: done — noted (assimilation test applied; D1, D2 closed; D3 deferred).
- T10 — 28.09.2026 status: done — noted (keyed short forms, RANGE-FULL, `build.py --source`).
- T11 — 28.09.2026 status: done on my side — format of `<id>_front_pl.md` and a checker, `srom-tlumacz/tlumacz-front_check.py` (docstring = format); 5 new cases in `tlumacz-test_handoff.py` (contract names both files; good file passes; dropped subtitle, 4 keywords, drafted English keywords without the approval line fail): **HANDOFF CONTRACT 23/23**. See E14 for the format.
- T12 — 28.09.2026 status: received — `ndiaye_src.md`, `refs.json`, `ndiaye_src_front.md`, `ndiaye_queries.md` copied into `srom-tlumacz/work/ndiaye/src/` with sha256 (identical to yours). Draft waits for MB (`MB-decisions.md` D11: pronouns, translator credit). Intake: `srom-tlumacz/work/ndiaye/ndiaye_intake.md`.

## E14 — `<id>_front_pl.md` format; four group names for the kartoteka (28.09.2026)

1. **Format** (sections in this order, headings exact): `# Tytuł` (no final full stop) · `# Podtytuł` ("—" if the original has none) · `# Abstrakt` · `# Słowa kluczowe` (5–10, `; `, no final full stop) · `# Keywords` ("jak w oryginale" if the original has keywords; otherwise my drafted English ones followed by `<!-- do zatwierdzenia przez autora -->`, § 12.2.2). English title and abstract are not repeated (they stay as the original's). Checker: `tlumacz-front_check.py <id>_src_front.md <id>_front_pl.md` → `FRONT OK`. If you read the file in the build, tell me and I'll keep the checker in step with you. Draft for Ndiaye: `srom-tlumacz/work/ndiaye/ndiaye_front_pl.md` (FRONT OK; Ndiaye has no keywords, so the English ones need the author's approval).
2. **Kartoteka — four forms not yet settled (§ 12.2.6: settled before delivery).** Ndiaye follows Ethel C. Brooks's Romani terms (her note 1): *Romni* (sg. f.), *Rom* (sg. m.), *Roma* (pl.), *Romnia* (pl. f.), *Romani* (adj.), and *Gadjo* / *Gadji* / *Gadje* for non-Roma. Proposal: **Romni** (sg. f., uninflected in the text where possible: „Romni”, gen. „Romni”), **Romnia** kept only where the author contrasts it with Romni, otherwise „Romki”?; **gadżo / gadzi / gadże**? — I do not want to guess the Polish Romani-studies spelling (gadźo / gadzio / gadżo): please settle it with MB, with the kartoteka's usual evidence. Italic: these are Romani common nouns (§ 5.1) or group designations (§ 3.4)? Your call under § 3.4.
3. **"Egyptians"**: the kartoteka row `Egyptians → Egipcjanie (bałkańscy)` is the present-day Balkan group. In Ndiaye (and in any early modern text) "Egyptians" / *Égyptiens* / *Egiptiens* is the historical designation of Roma. Suggest a second row or a note, so the Balkan form isn't applied to early modern sources: historical sense „Egipcjanie” (in quotation marks when a designation), as in Old Polish sources — evidence to be found; I have not verified it yet.
- E14 (2), clarified 28.09.2026: my only firm proposal is **Romni** (sg. f.). The plural (*Romnia* or a Polish form) and the Polish spelling of *Gadjo / Gadji / Gadje* I leave to you with MB; I have no verified evidence for either.

## E15 — Ndiaye draft: three build findings (28.09.2026)

Draft: `srom-tlumacz/work/ndiaye/ndiaye_pl.md` (preliminary translation for MB; `check.py --pair` → CHECK OK).
1. **Build crash (bug).** `build.py` dies with `UnicodeDecodeError` reading pandoc's stderr. Cause: `lua/srom_post.lua:243` `seen:sub(-90)` takes the last 90 **bytes**, so the SROM-NOPAGE context can start inside a UTF-8 character (here „porównywalne” cut after `c3`, note 127). `short()` at line 15 (`s:sub(1, 70)`) has the same pattern. Any Polish text can trigger it; the position decides. Fix suggestion: cut on a character boundary (`utf8.offset`), and/or decode subprocess output with `errors="replace"`. Until then I build with a wrapper that only adds `errors="replace"` (`srom-tlumacz/work/ndiaye/build_tolerant.py`); please tell me when it can go.
2. **Two title notes.** A translated article can have both the translation note (§ 12.2.3, mine) and the author's own title note (here: acknowledgements). I wrote two `::: przypis-tytulowy` blocks, translation note first. The pair check accepts it; the build's DOCX verification fails: "'Przypis gwiazdkowy' notes 4 / expected 2 + 1". Is two blocks the right markup (→ `*` and `**`), or should they be one note with two paragraphs? Contract point for `handoff.md`.
3. **Lint** (5 errors in the build report): 4× SPACE-BEFOREPUNCT come from the Ruggle title in `refs.json` (". . ." as published) — yours to judge; 1× BIB-COLON is a false positive on the colon inside the original title in my translation note („Pierwodruk: N. Ndiaye, *Black Roma: Afro-Romani…*”).

## Status of T13–T15 (28.09.2026)

- T13 — 28.09.2026 status: done — noted (build doesn't read `<id>_front_pl.md`; kartoteka note on "Egyptians"). Superseded for the draft by T15.
- T14 — 28.09.2026 status: done — (1) `build_tolerant.py` deleted; plain `build.py` on `ndiaye_pl.md` → exit 0, Errors: none. (2) Title blocks merged in `ndiaye_pl.md` (translation note, then acknowledgements, one block); `tlumacz-test_handoff.py` +2 cases (one block with two paragraphs passes; two blocks fail with your message). (3) `refs.json` re-copied, sha256 6a058001…ad988a verified; lint 0 errors. **HANDOFF CONTRACT 25/25** — but see E16.
- T15 — 28.09.2026 status: done in the draft — D12 (one block); D13: Romni → Romka, Romnia → Romki (15 places, inflected), *gadjo* / *gadji* / *gadje* lower case, italic at first use, the author's spelling; note 1 keeps her list in the original; early-modern „Egipcjanie” in quotation marks in running text (5 places; quotations and title glosses unchanged). D14: my files now refer to Kanon v1.7. No Old Polish attestation of „Egipcjanie” found yet (not searched systematically).

## E16 — Word round trip splits the one title note into two blocks (28.09.2026)

The one-block rule (D12) fails after the editor's Word copy: `export_work.py` → `docx_in.py` turns a `::: przypis-tytulowy` block with two paragraphs back into **two** blocks, and `check.py --pair` then reports "2 title-note blocks". Reproduced on `ndiaye_pl.md` (→ `ndiaye_robocza_v2.docx` → import) and on a minimal fixture in `tlumacz-test_handoff.py` (case "E16", recorded as KNOWN GAP, not counted; it flips when fixed). Since the Word file is the master after MB's edit, every translated article with an author's title note would fail at hand-back. Please fix the import (one block per consecutive run of asterisk-note paragraphs, or a marker kept through Word) and add the case on your side.
- T15 status, correction 28.09.2026: Romka/Romki forms in running text and notes (outside note 1): 11, not 15.

## Status after the cross-module review (28.09.2026)

- E3 — 28.09.2026 status: done, verified — `tlumacz-test_handoff.py` checks that `handoff.md` keeps the literal-note line (kanon § 8).
- E5 — 28.09.2026 status: done, verified as a documented slot — the test checks that `handoff.md` keeps the `tb_check.py` CLI unchanged. Wiring waits for `tb_check.py` (my leaf 1.4.2); I'll file a new E-item then.
- E6 — 28.09.2026 status: done, verified — new case where source label, target label and printed number all differ (a citation in the main text, two translator notes, Word round trip): source labels 2, 3 → printed 3, 4 with `--pair-src`; control without `--pair-src` keeps 2, 3. **HANDOFF CONTRACT 30/30** against your commit bb13dc8.
- T15 status, second correction 28.09.2026: Romka/Romki outside note 1: **9** (measured). My "11" counted the two in the bracketed gloss in note 1 (`ndiaye_pl.md:15`).
- E16: not answered yet. For information: against your working tree at 03:10 (uncommitted changes to `docx_in.py`, `export_work.py`, `test_roundtrip.py`) my E16 case already reads GAP CLOSED. I'll treat E16 as done when you commit and answer with a T-item.

## Status of T16 (28.09.2026)

- T16 — 28.09.2026 status: done — verified here against your commit ce291a2: E16 GAP CLOSED, HANDOFF CONTRACT 30/30; MB's `ndiaye_robocza_v2.docx` → `docx_in.py` → `check.py --pair` CHECK OK → `build.py --pair-src --queries` PASS. Rest noted (comments never block; T11 docs; D15, D16). Note: `_handoffs/` is now a git repository (MB, 28.09.2026): commit your own changes here, rule 7 in `README.md`.

## Status of T17–T21 — [general], [Pahulich], [Ostendorf], [Tittel] (29.09.2026 03:20)

- T17 — 29.09.2026 03:20 status: done — noted (`docx_in.py --typed-notes`; Dom not frozen until MB wants it and the missing page is supplied).
- T18 — 29.09.2026 03:20 status: received, not started — [Pahulich] MB has not scheduled it; I copy and verify the files (sha256) at intake.
- T19 — 29.09.2026 03:20 status: received — [Ostendorf] translation started today at MB's request (leaf 1.5.3). Superseded by T21 where they differ.
- T20 — 29.09.2026 03:20 status: received, not started — [Tittel] MB has not scheduled it; I copy and verify the files (sha256) at intake.
- T21 — 29.09.2026 03:20 status: received — [Ostendorf] `ostendorf_src.md` 66aa4b80…710e5ae, `refs.json` 0704415d…f4d45c5, `ostendorf_src_front.md` ce7860cc…2bdc9f0 and `ostendorf_queries.md` copied to `srom-tlumacz/work/ostendorf/src/`, `shasum -c` 4/4 OK against yours. B/D items will be put to MB with the draft. Queries and group names (not in the kartoteka: *cingani*, *Zingaros*/*Zingari*, *Zingances*, *Chinganéros*, *Bohemes*, "Gipsies", "Anglo-Romani") follow in an E-item.

## E17 — [Ostendorf] draft done; group names for the kartoteka; one Kanon gap (§ 12.2.4 c) (29.09.2026 03:41)

Preliminary translation for MB: `srom-tlumacz/work/ostendorf/ostendorf_pl.md` (+ `ostendorf_refs_tlum.json`: 2 Polish editions, Scott 1975 and Pratt 2011, declared `srom-added`; `ostendorf_pytania_tlum.csv`, 17 rows; Word copy `ostendorf_robocza.docx`). `check.py --pair` CHECK OK; `build.py --pair-src --queries --draft` PASS, Errors: none, lint clean; Word round trip IMPORT OK → CHECK OK. Nothing needed from you for the draft.
1. **Group names outside the kartoteka** (Kanon § 12.2.6: settle before delivery). What the draft does, for your rows:
   - *Anglo-Romani* (adj., 5× in the source: "Anglo-Romani woman / community / family / population / circumstance") → „angielscy Romowie”, „angielska Romka”, „rodzina angielskich Romów”. Proposed row: `Anglo-Romani` → `angielscy Romowie`, italic n.
   - Foreign exonyms kept in the author's form, italic (§ 3.4): *cingani* (Italian, Pasqualigo), *Zingaros* / *Zingari* (Anchieta's Latin via English), *Zingances* (Vowell), *Chinganéros* (Vowell; a South American group name as a foreign word), *Bohèmes* (Berquin-Duvallon; the author writes "Bohemes", the 1803 print has the accent), *Bohemian* (English word in a French marriage record, quoted).
   - Women: *Bohémienne*, *Bohémiennes* (4×) where the author writes "Bohémien" of a woman. Is the feminine a kartoteka variant of *Bohémiens*?
   - *Gitano* (adj.), *Indio*, *de nación Gitana* / *Indiana* italic as Spanish words.
2. **Kanon § 12.2.4 c** has only „tłum. z przekładu angielskiego autora”. Here many third-language quotations come from a **published English translation** the author cites (Weinstein, Robertson, Herzog, Loewald et al., Tappert): I wrote „tłum. z przekładu angielskiego” (no „autorki”) in brackets at the end of the note, „– przyp. tłum.” (§ 12.2.7). Also the feminine „autorki”. Please say whether the Kanon wants a line for both; MB decides (`MB-decisions.md` D21).
3. For information: 6 quotations translated from the original found online (Poisson, Berquin-Duvallon, Milfort, Loskiel 1789, Galletti, Roldán in Galletti); refs.json keys unchanged, the originals are in works already cited. `ostendorf_quotes.tsv` lists all 46.
- E17, correction 29.09.2026 03:41: the MB item is **D22**, not D21 (srom-typeset's D21 was written two minutes earlier).

## Status of T22 — [general] (29.09.2026 03:41)

- T22 — 29.09.2026 03:41 status: done — noted; `tlumacz-test_handoff.py` re-run against srom-typeset 3239f36: HANDOFF CONTRACT 30/30. The Ostendorf draft (E17) was built before and after the rename: PASS both times.
