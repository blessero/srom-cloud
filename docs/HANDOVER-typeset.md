# srom-typeset — handover (state at 29.09.2026 17:59)

For the next session (Claude Code). Start with `../_handoffs/tlumacz-to-typeset.md` (incoming) and
`../_handoffs/MB-decisions.md` (the one list of MB's decisions — this file keeps none), per `../CLAUDE.md`. Then this,
`CLAUDE.md`, and `.claude/skills/srom-typeset/SKILL.md`. Outgoing messages: `../_handoffs/typeset-to-tlumacz.md` (T-items).
Nothing here needs re-deriving; decisions marked ✔ are the editor's and closed.

## 1. What exists

`srom-typeset` is a tested toolchain for *Studia Romologica*: author's Word/PDF → SROM-MD (Pandoc Markdown)
→ CSL citations (first citation / short form / *Ibidem*) → DOCX with named styles only → InDesign Word import.

| part | file | job |
|---|---|---|
| import | `scripts/docx_in.py` | Word → SROM-MD; Zotero/Mendeley harvest; author's reference list → `_bib.txt`; working-copy round trip |
| import | `scripts/pdf_extract.py` | born-digital PDF → SROM-MD (italics, markers, notes, endnotes, reference list) |
| clean | `scripts/normalize.py` | Polish typography (quotes, dashes, markers before punctuation…) with change log |
| refs | `scripts/cite_map.py` | author-date → footnote citations (`scan`), refs.json vs author's list (`audit`) |
| checks | `scripts/check.py` | integrity; `--keyed` (literal notes → citations); `--pair` (handoff check source ↔ translation) |
| checks | `scripts/mutate_keyed.py` | mutation test of a keyed text: does `check.py --keyed` catch page/work/key errors (step 4b) |
| back | `scripts/take_back.py` | takes a delivered translation from srom-tlumacz's `work/<id>/` into `work/<id>/pl/` (sha256, re-import of the Word master, `--pair`) |
| Word | `scripts/export_work.py` | SROM-MD → editor's Word working copy (tokens editable, lossless round trip) |
| build | `scripts/build.py` | DOCX + report + query sheet `_pytania` + `_postimport.jsx` + `_ibidem.jsx`; `--proof` reading copy |
| rules | `csl/srom.csl`, `lua/srom_post.lua`, `config/styles.json` | citation style; DOCX styling; role → style names |
| InDesign | `indesign/style_spec.json` → `scripts/make_style_setup.py` → `srom_style_setup.jsx` + `references/style-sheet.md` | house style definition and setup script |
| docs | `references/*.md` | srom-md (format), handoff (contract with srom-tlumacz), indesign, decisions, style-sheet |

Tests: `python3 tests/run_all.py` → `SUITE ALL PASS 20/20` (~510 checks). Unlazy ledger: `/GATES.md`, batches from
26.09.2026 on (the older G1–G16 ledger was lost, § 3 item 1; its G12, the InDesign import, is stage 3 / D3).

## 2. Decisions register (`references/decisions.md`)

✔ closed by the editor: 1–19 — **since 26.09.2026 in Kanon v1.6** (srom-kanon `references/kanon-redakcyjny.md`,
§ 17 row 1.6); `decisions.md` is now only a rule → code → test map plus toolchain conventions (15, 18, 19).
21 ✔ 29.09.2026 (house style v3; D3 closed; D21, italic speaker/affiliation, closed the same day: Kanon § 3.4). 20 and 22 ✔ decided 27.09.2026 (D1, D2: as implemented).
**Kanon v1.8** (29.09.2026, review 29.09.2026 row 11): the three rulings of 28–29.09 that had been added to v1.7 as
dated supplements are now § 17 row 1.8; no rule text changed. T27 told srom-tlumacz.

## 3. Queue for Claude (in order)

1. ~~**Repo setup**~~ — done 26.09.2026 (Claude Code): git repo, skills symlinked, venv; suite green on the
   Mac with pandoc 3.8.3 after one fix (the 3.8 DOCX reader put "Table Caption" inside the table caption →
   `docx_in.py` dropped every table caption in the working-copy round trip; fixed, test added). `GATES.md`
   was not in the uploaded archive — the G1–G16 ledger is lost; new gates start in `/GATES.md`.
2. ~~**srom-kanon / srom-typeset overlap**~~ — done 26.09.2026. The Polish Kanon (it existed outside the skills:
   `0. ASSETS/LLM/Kanon zecera/` 22.09 and `Downloads/srom-kanon 26 Sept/` 26.09 — the newer used) is now
   `srom-kanon/references/kanon-redakcyjny.md`, **normative, v1.6**: decisions 1–9, 11–14, 16, 17 written into their
   sections, draft § 12.2 (srom-tlumacz, settled 25.09) incorporated, E8 in § 7.1. `RULES.md` = English digest,
   renumbered to the Kanon's §§ (it had its own numbering: Cyrillic §10 → § 9.6, captions §11 → § 10 …).
   srom-typeset: bundled linter removed, `scripts/kanon_path.py` finds srom-kanon, `tests/test_kanon.py` checks
   versions and that every § cited exists. srom-typeset's § references were Kanon numbers all along — no renumbering.
3. ~~**E8**~~ — done 26.09.2026 (§6 below: editor ruled *above* the numbered notes, set by hand; style = footnotes).
**Order of work (MB 27.09.2026; D3 closed 29.09.2026, D7 resolved):** stage 1 (source PDF/Word → SROM-MD → Word working
copy) and stage 2 (translation, srom-tlumacz) are finished and tested first; stage 3 (build for InDesign, styles,
G12) after.

4. **Stage-1 test on MB's PDF** — done 27.09.2026, waiting for MB's answers. Article: Ndiaye, "Black Roma" (RQ 75,
   2022), `work/ndiaye/` (git-ignored). Stage 1 complete: `ndiaye_src.md` (133 notes keyed, `check.py --keyed` OK),
   `refs.json` (84, `cite_map audit` OK), `ndiaye_src_robocza.docx` (round trip identical), `build/…_korekta.docx`
   (`build.py --source`, 0 issues). `work/ndiaye/ndiaye_queries.md` Q1–Q17: answered by MB 28.09.2026, applied. Keying is scripted in
   `work/ndiaye/key.py` (re-run after any change to the extraction); refs in `refs.py`.
   What the PDF broke, all fixed with tests (commits d62b8b5 … 214da89): obfuscated italic font names, raised
   note-number lines, caps headings below body size, front matter, title note, verse, captions, reference list at
   note size, foot block below notes, URL breaks (now from the PDF's link targets), hyphen joins (document
   evidence), unlabelled short-form pages in the keyed check, English lists in the audit, source proof mode,
   bracket escapes in the Word round trip, Kanon § 3.2 full ranges (+ normalize RANGE-FULL), linter BIB-COLON on
   "Roma:". `test_pdf.py` hand-set pages now run on the Mac; new `test_pdf_layout.py`.
   28.09.2026: MB's answers applied; online-journal articles print year + URL (Kanon § 9.7); source handed to
   srom-tlumacz (T12; D7 removed from MB-decisions as resolved). Waiting: srom-tlumacz's receipt (T12) and its side
   of T11 (front matter). Figures: image files/permissions at stage 3. Future (MB, not now): a sourcing step for
   missing publisher/place (search, list for MB's approval per item) and ISBN lookup via a catalogue API.
   28.09.2026, later: review of the stage-1 commits (d62b8b5..70b8242) found four bugs, fixed with tests:
   RANGE-FULL skipped a range before a full stop; uncited entries with `[BRAK …]` had no query row; the Lua filter
   cut the no-page context by bytes (split "ó", build.py died on stderr — E15); BIB-COLON fired on titles ("Black
   Roma: Afro-Romani"). E15: one title-note block per article (contract; check.py error), pending MB D12. E14:
   Romni/gadjo and early-modern "Egyptians" → MB D13. Ruggle title ". . ." → `[…]` in `work/ndiaye/refs.py`
   (refs.json re-generated; T14 gives the new sha256). MB decided D12–D14 the same day (T15): one title note; Romka/Romki, gadjo kept, „Egipcjanie” (kartoteka); Kanon v1.7. Waiting: srom-tlumacz's side of T14/T15.
   28.09.2026, after the cross-module review (`../_handoffs/review-28.09.2026.md`): E16 fixed (Word round trip
   re-joins multi-paragraph blocks; comment before punctuation; `::: mowca` line break) → T16; MB's
   `ndiaye_robocza_v2.docx` imports to pair CHECK OK and builds with 0 errors. Docs aligned with the contract
   (comments never block), scenario C / T11, stale versions (now caught by `test_kanon.py`), D15/D16 from Kanon
   § 13.2. Gates: `GATES.md` batch 28.09.2026. Not mine, left open: `_handoffs/README.md:18` contract path (whichever
   session MB asks); stale `srom-kanon.skill` / `srom-typeset.skill` at the repo root (26.09, git-ignored).
   Known, not fixed (minor): `pdf_extract.link_fix` replaces URL text by a link target differing in ≤ 2 characters
   (listed in the report, can pick a sibling URL); range expansion exists twice (`normalize.py` RANGE-FULL,
   `cite_map.expand_ranges`).
4a. **Stage-1 test 2: Pahulich** (CRS 8/1, 2025, author-date, `work/pahulich/`, git-ignored) — done 28.09.2026, source
   handed over (T18), MB's points in `MB-decisions.md` D17 (detail `work/pahulich/pahulich_queries.md`). Pipeline:
   `pdf_extract` → `prep.py` (hand conversions, logged) → `refs.py` → `cite_map scan --apply pahulich_src.md
   --renumber` → `check.py` → `build.py --source` → `export_work.py`. Re-run from `prep.py` after any change.
   What this layout broke, all fixed with tests (a64edb3 … 57c8f08): bracketed superscript markers "[1]"; note size
   taken from the separator rule (reference list at a larger small size); front matter over two pages with a
   keywords column; drawn repeated-author rule; hyphen before a capital / slash at a line end; left-indented block
   quotes; URL broken inside a token; NFD accents from the text layer; in cite_map: year-only "(2018, 78)"
   (YEAR-ONLY), possessive, "di" particle inside "Jodi", comma before a name (TRIMMED), author's spelling via
   `srom-as-written` (ALA-LC names), italic "(*Ibid.*, 2)", comma locator and "See also" in notes, `--renumber`.
   After MB answers D17: B-items into `refs.py`; A2 (merge notes 1/2) in `prep.py`; new T-item with new sha256.
4b. **Stage-1 test 3: Scheffknecht, German** (Neujahrsblätter Lustenau 1/2010, endnotes, full-note citations, no
   bibliography; `work/scheffknecht/`, git-ignored) — done 28.09.2026, **not handed over** (srom-tlumacz is EN→PL): MB's
   points in `MB-decisions.md` D18 (detail `work/scheffknecht/scheffknecht_queries.md`). Pipeline: `pdf_extract --pages
   4-32` → `key.py` (relabel PDF 2–121 → 1–120, keying, `key_log.md`) → `check.py --keyed` → `build.py --source` →
   `export_work.py`; `refs.py` → refs.json (35 works typed from the notes). `wordcheck.py` there: every PDF word in the output.
   29.09.2026 17:59: D18 A5 applied — hippel1995 `dropping-particle` "von" (bibliography "Hippel, Wolfgang von", notes "W. von
   Hippel", short "Hippel"; Kanon § 9.3/§ 9.5); refs.json 4637100e…40e5, CHECK OK, proof rebuilt. Not handed over, so no T-item.
   What German/this layout broke, fixed with tests (e1d52df … and the next commits): ragged right + space-marked paragraphs
   (layout measured first), ~1-em quotations, recto/verso margins, InDesign U+0007/tabs, soft and suspended hyphens,
   virgule slashes, marker in the title → title note, endnote pages without heading, raised edition digits in notes,
   captions beside images, numbered items, overprinted unmapped glyphs (`test_pdf_de.py`); a citation in the title note
   (build: through citeproc as the first note, then back into the asterisk series); `check.py --keyed` for full
   citations (range before "hier S.", Sp./Anm., "wie Anmerkung"); refs `note` "word:" swallowed by pandoc → error.
   Found on the way: Pahulich may have lost two paragraph breaks at page breaks (pp. 46/47 "…Eastern Europe." | "In
   Moldavia…", pp. 54/55 "…Lucassen 1998)." | "Many historians…"): the extractor now lists such breaks; check against
   the journal's HTML before D17 is applied. Kanon gaps raised in D18: publishers missing in German citation practice,
   series, "von".
4c. **Stage-1 test 4: Ostendorf** ("Familiar Outsiders Abroad", ch. 3 of M. Fotta, A. Ostendorf (eds.), *The Romani
   Atlantic*, CUP 2026; Cambridge Core PDF, Chicago full notes, no bibliography; `work/ostendorf/`, git-ignored) — done
   28.09.2026, handed over (T19) with **rights pending** (CUP, not OA): MB's points in `MB-decisions.md` D19 (detail
   `work/ostendorf/ostendorf_queries.md`). Pipeline: `pdf_extract` → `key.py` (keying + two DO SPRAWDZENIA comments,
   `key_log.md`) → `check.py --keyed` → `build.py --source` → `export_work.py`; `refs.py` → refs.json (83 works);
   `wordcheck.py` (words and numbers). Re-run from `refs.py`/`key.py` after MB's answers; new T-item with sha256.
   What it broke, fixed with tests (aaecba0, ea04d6a, next): the text layer had no digits and no small caps (Sabon LT Std
   PUA; the first run said EXTRACT OK with 0 notes), "¼" for "=", "Savi´c", word spaces as gaps, a chapter numeral above
   the title, notes over a page with no rule, compounds at a line end (`test_pdf_cup.py`); `check.py --keyed` did not
   count Chicago pages (a lost page passed); the CSL dropped the editor of an authored book and printed an anonymous
   chapter's volume editor as its author (provisional fix, `decisions.md` 23 / D19 A3); query rows showed `<i>` tags.
   Note: another session committed my in-progress `pdf_extract.py` as aaecba0 while I worked (content is mine, fine).
   Known, not fixed (minor): the query sheet prints broken asterisks around a roman phrase inside an italic title
   (O'Reilly, *Divide et impera*); the DOCX is right.
   28.09.2026, after MB's answers (T21 — first numbered T20 by a parallel session, D19): the chapter **is OA, CC BY-NC 4.0** (my T19 "not OA" was wrong: the PDF stamp
   and Crossref name only the Cambridge Core terms — always check the publisher's landing page); summary + 10 keywords
   exist online only (in `_src_front.md`). Imprint gaps sourced from the LoC catalogue (`work/ostendorf/source_imprints.py`,
   SRU/MARC, evidence in `imprints.tsv` and refs `srom-sourced`): 43 values, 14 left to MB by hand. Kanon § 7.2/§ 9.4 and
   § 9.3/§ 9.5 (particles by the name's language, LC NAF) in ea50df6. Reusable for D18 A3 (German publishers):
   `source_imprints.py` works for any refs.json (run in the article folder).
4d. **Stage-1 test 5: Tittel** ("Racial and Social Dimensions of Antiziganism", *On_Culture* 10, 2020, Giessen; endnotes
   with full Chicago citations incl. place and publisher, no bibliography; `work/tittel/`, git-ignored) — done 28.09.2026,
   handed over (T20); rights no obstacle (CC BY 4.0). MB's points in `MB-decisions.md` D20 (detail
   `work/tittel/tittel_queries.md`). Pipeline: `pdf_extract` → `key.py` (prep: joins, a URL, note 1 → title note; keying;
   labels renumbered 2–101 → 1–100; `key_log.md`) → `check.py --keyed tittel_pre.md tittel_src.md` → `build.py --source` →
   `export_work.py`; `refs.py` → refs.json (63 works). `wordcheck.py`: every word of the PDF in the extraction. Re-run from
   `refs.py`/`key.py` after MB's answers; new T-item with sha256.
   What it broke, fixed with tests (27cc558, 5bd5794, 7f671f5, 25dfb19): underscore-decorated headings ("_Abstract",
   "_Endnotes", "1_Introduction"), front matter over two pages, justified block quotations read as verse, a URL closed by
   ">" eating the next space, URL hyphens decided by the same address elsewhere, "anti- “gypsy”" (`test_pdf_onculture.py`);
   `check.py --keyed`: Ibidem after a quotation, the author's siglum (MEW 23), "*Journal*, 7 (2018)" volume, series numbers;
   a **mutation test** on this text found four holes, now errors: page after "here:", Kant AA page, wrong volume of one
   title, a non-bare Ibidem hiding a changed page (older than this text); Lua: no full stop before the author's bracketed
   remark after a citation (also Ndiaye n. 77). Regression: the four earlier PDFs extract identically (two old diffs are
   from earlier commits: Ndiaye "African- American" in the frozen source, Pahulich "religio-political"); their keyed checks
   still pass.
   Known, not fixed: the query sheet flags a citation after a quoted chapter title as "cytat bez numeru strony" (Amīn, n. 47);
   repositories behind proof-of-work bot checks (Giessen GEB/JLUpub, DB Thüringen, nbn-resolving) are not read — left to MB.
4e. **Stage-1 test 6: West Ohueri** ("Peripheral whiteness and racial belonging and non-belonging: accounts from Albania",
   ch. 6 of C. Baker et al. (eds), *Off White*, Manchester UP 2024, DOI 10.7765/9781526172211.00013; manchesterhive PDF,
   British Chicago endnotes, no bibliography; `work/westohueri/`, git-ignored) — done 29.09.2026, announced to srom-tlumacz
   (T23). **Rights: CC BY-NC-ND 4.0 — the ND needs written permission before a translation is published** (D24 A1; the first
   ND text). MB's points in `MB-decisions.md` D24 (detail `work/westohueri/westohueri_queries.md` A–E). Pipeline:
   `pdf_extract` → `key.py` (prep: fieldwork blocks without italics, § 4.1; three DO SPRAWDZENIA comments; keying,
   `key_log.md`) → `check.py --keyed westohueri_pre.md westohueri_src.md` → `build.py --source` → `export_work.py`;
   `refs.py` → refs.json (51 works; 16 DOIs from Crossref, `doi_check.txt`; the dissertation's place sourced).
   `wordcheck.py` (every PDF word; the publisher's HTML full text, found later by MB, agrees word for word and in
   italics). MB's answers of 29.09.2026 applied (T24): n. 29 cites Baker's chapter; "Ohueri, Chelsi West"; block
   quotations roman except what the Kanon italicises inside them (Albanian words); Austin, TX approved; MB asks for the
   ND permission. Open: D24.
   What it broke, fixed with tests (950f46e, 9163315, 4a088a2): a separate small-capitals font's text layer ("bce");
   `check.py --keyed` read "40:3 (2021)", "2nd ed.", "26 May 2020" as lost pages, and — **mutation test** — let a work
   dropped from a multi-work note or a key swapped for another named work pass (now checked both ways, citation shape
   only, also the author's short forms; the claim "no work lost" in SKILL.md was not true before); the query sheet missed
   quotations in 'single quotes' with the marker after the stop (2 → 13 rows); "Zob. *Ibidem*, for more on …" (Ibidem with
   the sentence going on, § 7.3) is now the short form. Regression: the five earlier PDFs extract identically (the two old
   diffs), their keyed checks pass, their Ibidem handling is unchanged.
   **Mutation test per text** (MB 29.09.2026): `scripts/mutate_keyed.py` (SKILL.md step 4b) — page changed/dropped, a
   work dropped, a key swapped; on its first run it found "(eds)" between name and title hiding a dropped edited volume
   (fixed). West Ohueri 40/40; the earlier texts: see T24 / GATES.
   Known, not fixed: reprint years ("2000 [1983]") are not printed — no Kanon line (D24 A8); films lose their producer
   (§ 8.7 pattern); a quotation whose marker stands later in the sentence (n. 37) or after a stray space (n. 56) is not
   on the query sheet (listed by hand in queries D3); Brazilian compound surnames cannot sort under the last part (CSL).
5. **Next text for translation**: MB sends it here first — stage 1 (freeze `<id>_src.md` + refs.json +
   `<id>_src_front.md`, mutation test, T-item), as with the five texts so far (Ndiaye, Pahulich, Ostendorf, Tittel, West
   Ohueri). A DOCX with typed notes: `docx_in.py --typed-notes` (E9, done 28.09.2026, T17). Dom file 52/52 pairs right
   (`work/dom/`), one page missing from that DOCX (notes 49–50), marker 48 repaired — both for MB; Dom not frozen
   (stage 1 when MB wants it). The Fotta RTF is not a case (no notes at all).
   Known, not fixed: the docx import keeps Word's right-to-left quote marks as spans (`[’]{dir="rtl"}`, Dom notes
   11, 46; any file) — strip them in import or normalize.
5a. **E17–E19 answered** (29.09.2026 17:59, T25): kartoteka rows (commit 4187da2); Pahulich title glosses applied (refs.json
   3b060a87…1f3d5366). Waiting for MB, then a T-item with new sha256: **B12** Urlsperger record (Ostendorf; key and token
   stay), **B13** *Zinganées*, **B14** *Bohèmes* (D19), **B11** Tittel n. 49 MEW 741 (D20; changes the token). The Kanon
   § 12.2.4 c line („tłum. z przekładu angielskiego”) after D26 (e): wording proposed there; then Kanon + § 17 row.
5b. **Taking translations back** (contract 29.09.2026 17:59, T26, commit 6e9ea9e; `handoff.md` "Back"): MB edits
   `<id>_robocza.docx` in srom-tlumacz's `work/<id>/` (the master); srom-tlumacz imports and sends a delivery E-item
   with sha256; here `take_back.py` → `work/<id>/pl/` → `build.py` from there → status line. First expected: Ndiaye.
   Waiting for srom-tlumacz to align its PLAN/HANDOVER and test (T26).
6. ~~Kartoteka E12 flags~~ — done (E13/T9): Nawar, Gurbati, Halabi italic; Mutribowie, Gadżar, Garaczi roman (assimilated).
7. Stage 3: ~~house style / reduce the style set (§4, D3)~~ — done 29.09.2026 (house style v3, §4). Next: G12, the first
   real article placed in a v3 template — **a translated article** (Ndiaye after MB's edit, via 5b; review
   29.09.2026 row 6), so that `_postimport.jsx`, `_ibidem.jsx` and `_gwiazdki.jsx`, never yet run in InDesign, are proven
   with a real asterisk series (title note + translator's notes) (the JSX runs in InDesign via AppleScript `do script` — proven, see
   `tools/indesign_check/`).
8. Later: ICML output as a fallback to Word import (pandoc writes ICML with footnotes; needs a style-renaming
   step); wire `tb_check.py` into scenario C when srom-tlumacz ships it (E5; CLI fixed in `handoff.md`).

Done 27.09.2026: E10 translator front matter (T7, `test_e10.py`); E11/D9 kartoteka (`srom-kanon/references/
kartoteka.tsv`, T8); E12 foreign exonyms italic (Kanon § 3.4, T6); Kodeks zecera references removed; decisions
15, 18, 19 stay in srom-typeset as toolchain conventions (MB delegated the call).

## 4. House style — v3 done 29.09.2026 (below it, the v2 notes of 25–27.09, kept as history)

**MB's brief (29.09.2026):** a designer's style set (about 20, most used on top, the rest folded away); vol. 18's
main styles untouchable (19th issue: consistency); body 10.5/13 on the baseline grid and notes 9/10.8 are the two
references; Cambria everywhere; tracking and H&J of the main styles not touched; the 13.2945 pt grid stays (odd, but
18 volumes use it); quote 9 pt, indents 1 cm unless there is a reason; renaming welcome ("Śródtytuł", "Śródtytuł
MAŁE"…); set up for a blank document (purge, then build). Answers: Cytat on Tekst's H&J with tracking 0; two
captions, with and without the 0.4 pt rule, no white variant; long notes may split (as Ellis); Śródtytuł = the old
Podrozdzial exactly.

**What was built:** `indesign/style_spec.json` v3 → `srom_style_setup.jsx` + `references/style-sheet.md`. 29
paragraph styles (15 at the root) and 8 character styles, down from 39 + 7. The values were read from the two vol. 18
IDMLs in InDesign itself (every property, not the XML), each new style defined as the differences from its parent.
Several pipeline roles now share one style (config). Build change: bulleted lists get a typed "–" + tab.
v2 kept in `indesign/legacy/v2/`.

**Found on the way:** the grid is 13.2945 pt from 62.362 pt (not 13); the note number is superscript through a 1-line
drop cap + nested style (kept); Autor's 0 pt rule above with "keep in frame" is the first-page sink (kept — dropping
it moved page 1 up by 35 pt); Ellis's Cytat blokowy had no parent (default H&J, tracking −10), Konferencja's was
9.5 pt; vol. 18 abstracts were set in the body styles (Ellis), the Abstrakt styles were unused leftovers (dropped);
running heads were [Basic Paragraph] + overrides (now Pagina, towards the spine, and Folio, on the outer edge, as in vol. 18).

**Proof:** `tests/test_jsx.py` (17 checks, incl. 232 values of the kept styles against `dump/*.idml`) in the suite;
`tools/indesign_check/indesign_check.py` in InDesign: the control run equals vol. 18 line for line (Ellis 603/603,
Konferencja 468/468); the real run keeps page counts; line breaks change only through the Kanon § 3.3 no-break rules
(new: vol. 18 had only the one-letter-word rule) and the unified Cytat. Also: `run_all.py` now fails a test that
crashes after an early verdict (test_jsx.py had been reported ok while crashing).

**Second round (MB 29.09.2026, later the same day):**
- **Kanon § 3.4.** MB ruled: the no-italics rule for proper names governs the text (body, notes, captions,
  bibliography), not display elements (running heads, speaker and affiliation, contents). Written into the Kanon and
  RULES; D21 closed.
- **Junk sweep of the spec, each item proven not to move vol. 18.**
  - Tekst's hyphenation zone 21.25 (a Word leftover) and auto-leading 120 (the default) are no longer written.
  - Autor's sink rule got colour None. InDesign's PDF export draws nothing for it either way; now it cannot print
    whatever its weight.
- **Keep with next on Śródtytuł, Mówca, Afiliacja and Tabela TYTUŁ** (Kanon § 3.6: a heading never closes a column).
  It changes exactly one place in the two files: Konferencja p. 6, where the speaker "> Tobi Górniak" stood alone at
  the foot of the page. Page counts are unchanged.
- **`indesign/srom_final_pass.jsx`** (generated with the setup script; limits in the spec's `final_pass`): the
  Kanon § 3.6 checks after layout, plus a fix mode (paragraph tracking ±5/±10, as vol. 18 did by hand; one undo step).
  - Found in the vol. 18 files after the v3 setup: Ellis p. 8 szewc; p. 1, 10 and 11 split notes with one line;
    a URL break on p. 8; an Arial font. Konferencja p. 3 bękart; an empty last line on p. 12 (a space before the
    return); a Times New Roman font.
  - Both vol. 18 IDMLs already have **overset text** in the main story (Ellis 46,485 characters, Konferencja 32,142).
  - The first version scanned into the overset text on every trial and kept InDesign busy for about 25 minutes. The
    scan now stops at overset text, with a 5-minute budget.
- **`indesign/SROM_szablon_v3.idml`**: the clean template (`indesign_check.py --template`; `make_template.jsx`).

**By eye, before the first issue:** the specimen (`indesign_check.py --specimen`) and the template.

### v2 notes (history)

**What the two templates contained** (03_Ellis.idml, 09_Konferencja.idml, 25.09.2026):
- Page 165×235 mm; margins top 23.5, bottom 16, inside 22, outside 17 mm; measure 126 mm (357 pt); body Cambria
  10.5/13 on a baseline grid; composer "HL Composer Optyca" on Tekst (not set by the script — inherited only where
  Tekst is the parent).
- Ellis: 15 styles, 11 used. Konferencja: 45 styles, 12 used; the rest Word leftovers (Normal, Footnote text…).
- Motto (Ellis) and dialogue (Ellis, "Przewodniczący Coe:") were **local overrides** on "Cytat blokowy"
  (italic / bold speaker), not styles. Konferencja speakers: "Panelant" (bold italic) + "Uni" (italic affiliation).
- **Neither template has GREP styles for non-breaking spaces**, though the kanon (RULES §3) assigns them to the
  typesetter's GREP style — so that rule is currently applied nowhere. "NO BREAK" character style exists, unused.
- Speaker names and affiliations in italics contradict the kanon (no italics for proper names).
- Two names for one thing: "Cytat blokowy" / "Cytat_blokowy"; "Podpisy" / "Podpisy BLACK".

**What was proposed** (`indesign/style_spec.json`, readable in `references/style-sheet.md`): root *Podstawa*
(Cambria 10.5/13, Polish, grid, the six non-breaking-space GREP rules) + 9 groups, **39 paragraph styles**, 6
character styles. Speakers bold roman in both forms (dialogue: "Name:" via character style *Mówca – etykieta*,
added by the build; transcript: speaker on its own line + affiliation line). Motto italic, indent 30 mm, titles
inside roman. Word forbids one name for a paragraph and a character style → "Mówca – etykieta".
Values **invented, not from the templates**: spacing before headings/speaker lines 13 pt, around quotes 6.5 pt,
motto indent 30 mm, "Abstrakt – nagłówek" tracking 50.

**Why 39**: one style per role the pipeline emits + every role the templates had (title block, TOC, page) + the
new elements (motto, dialogue, transcript, verse, tables, interlinear examples, title note).

**Reduction options** (config maps roles → names, so several roles can share one InDesign style at no cost to
the pipeline): Bibliografia – tytuł/dział → Śródtytuł 1/2 (−2); Tekst – inicjał out (−1); Motto – źródło out (−1);
Słowa kluczowe → Abstrakt (−1); one Afiliacja for author and speaker (−1); Tabela – treść/źródło → Podpis (−2);
Przykład ×3 → one style, form line italicised by the build (−2); Cytat – wiersz and Dialog → Cytat blokowy
(same metrics; line breaks and speaker labels come from the text) (−2); Spis treści ×3 → volume/TOC template
only (−3); Wyliczenie numerowane → Wyliczenie with the dash typed instead of auto-bullet (−1). ≈ 39 → 23.
Also possible: the script creates only styles in use + core; groups without number prefixes.

**Script facts**: renames an old style into the new name (formatted text keeps formatting), merges duplicates,
retires Word leftovers into "Tekst", leaves footnote styles ("Przypis", "Indeks gorny", "Footnote reference")
untouched, writes `<doc>_style_setup.txt`. Tested as ES3 only; the editor ran it successfully on a copy.

## 5. srom-kanon vs srom-typeset — recommendation

Keep two skills, remove the duplication.
- **Different jobs, different users.** srom-kanon = the rules (the *what*): copyediting, author guidelines,
  metadata, and srom-tlumacz loads its sections at translation time. srom-typeset = the machinery (the *how*).
  Merging would load the whole toolchain into translation and copyediting sessions and blur which text is normative.
- **Duplication to remove**: (a) srom-typeset bundles `lint_srom.py` (identical today, will drift) → require the
  kanon's; (b) closed decisions live in `decisions.md` → move them into kanon RULES, keep in srom-typeset only a
  table "rule → implementing file/test"; (c) kanon SKILL.md tells users to lint DOCX by hand → point production
  work to srom-typeset's build (which runs the linter).
- **Keep on purpose**: `tests/test_csl.py` mirrors kanon §7/§9 example strings — it is the drift detector between
  rules and CSL.
- ~~Kanon housekeeping~~ — done 26.09.2026 (§ 3 item 2): the Polish Kanon is normative inside srom-kanon
  (`references/kanon-redakcyjny.md`), one section numbering everywhere; one bibliography division has no heading
  (Kanon v1.6).

## 6. E8 — asterisk series for non-author notes (editor's ruling 25.09.2026) — DONE 26.09.2026

Implemented: notes ending `– przyp. tłum./red.` and the title note → `*` in *Odsyłacz gwiazdkowy* at the marker +
paragraphs in *Przypis gwiazdkowy* (based on *Przypis*) at the end of the DOCX, title note first, each opening `* `;
no number, no Ibidem in or right after them; checks in the build, `_postimport.jsx`, new `_gwiazdki.jsx`
(asterisks per page after layout). Editor's answers: **above** the numbered notes, placed by hand; same style
as footnotes. Original spec kept below for the record.

Title note, translator notes (`– przyp. tłum.`) and editorial notes (`– przyp. red.`) form one series marked
*, **, *** …, restarting on each page; on the first page the title note takes the first *. Not numbered with the
author's notes.
- Markup: translator `[^t<n>]` + text ending `– przyp. tłum.`; editorial `[^r<n>]` + `– przyp. red.`; title
  note `::: przypis-tytulowy`. `check.py --pair`: add r-notes / "przyp. red." to the exclusion (today only t-notes).
- Rendering: an InDesign story has one footnote numbering sequence → these cannot be Word footnotes. Proposed:
  the build turns them into an inline marker (character style, placeholder) + the note text as a separate
  paragraph (style "Przypis gwiazdkowy") collected at the end of the DOCX; a JSX lists every marker with its page
  and sets the asterisk count per page (assist) — at minimum a report for manual setting.
- Post-import check: fail if any "przyp. tłum./red." text sits in the numbered footnotes.
- To ask the editor: position on the page (above or below numbered notes), separator, style of the asterisk note.
- Update wording in `srom-md.md` and `handoff.md` ("numbered with the author's notes" is now wrong).

## 7. Pending for the editor

Only in `../_handoffs/MB-decisions.md`. srom-typeset's open items there: D17 (Pahulich), D18 (German test), D19 (Ostendorf, with B12–B14), D20 (Tittel, with B11), D24 (West Ohueri), D26 (e) (Kanon line § 12.2.4 c, wording proposed), D15 (licence ND option, kolegium), D16 (vol. 18 copyright clause, PILNE before any OA announcement).
D1, D2, D4, D7, D9, D12–D14 are closed.
