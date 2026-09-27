# srom-typeset — handover (state at 27.09.2026, evening)

For the next session (Claude Code). Start with `../_handoffs/tlumacz-to-typeset.md` (incoming) and
`../_handoffs/MB-decisions.md` (the one list of MB's decisions — this file keeps none), per `../CLAUDE.md`. Then this,
`CLAUDE.md`, and `skills/srom-typeset/SKILL.md`. Outgoing messages: `../_handoffs/typeset-to-tlumacz.md` (T-items).
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
| Word | `scripts/export_work.py` | SROM-MD → editor's Word working copy (tokens editable, lossless round trip) |
| build | `scripts/build.py` | DOCX + report + query sheet `_pytania` + `_postimport.jsx` + `_ibidem.jsx`; `--proof` reading copy |
| rules | `csl/srom.csl`, `lua/srom_post.lua`, `config/styles.json` | citation style; DOCX styling; role → style names |
| InDesign | `indesign/style_spec.json` → `scripts/make_style_setup.py` → `srom_style_setup.jsx` + `references/style-sheet.md` | house style definition and setup script |
| docs | `references/*.md` | srom-md (format), handoff (contract with srom-tlumacz), indesign, decisions, style-sheet |

Tests: `python3 tests/run_all.py` → `SUITE ALL PASS 14/14` (~330 checks). Unlazy ledger: `GATES.md`
(G1–G16 met; G12 = InDesign import, abandoned here: needs the editor or a machine with InDesign).

## 2. Decisions register (`references/decisions.md`)

✔ closed by the editor: 1–19 — **since 26.09.2026 in Kanon v1.6** (srom-kanon `references/kanon-redakcyjny.md`,
§ 17 row 1.6); `decisions.md` is now only a rule → code → test map plus toolchain conventions (15, 18, 19).
○ open: 20, 21, 22 → `MB-decisions.md` D1, D3, D2.

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
**Order of work (MB 27.09.2026, `MB-decisions.md` D3/D7):** stage 1 (source PDF/Word → SROM-MD → Word working
copy) and stage 2 (translation, srom-tlumacz) are finished and tested first; stage 3 (build for InDesign, styles,
G12) after.

4. **Stage-1 test on MB's PDF** — done 27.09.2026, waiting for MB's answers. Article: Ndiaye, "Black Roma" (RQ 75,
   2022), `work/ndiaye/` (git-ignored). Stage 1 complete: `ndiaye_src.md` (133 notes keyed, `check.py --keyed` OK),
   `refs.json` (84, `cite_map audit` OK), `ndiaye_src_robocza.docx` (round trip identical), `build/…_korekta.docx`
   (`build.py --source`, 0 issues). Open: `work/ndiaye/ndiaye_queries.md` Q1–Q17 (MB). Keying is scripted in
   `work/ndiaye/key.py` (re-run after any change to the extraction); refs in `refs.py`.
   What the PDF broke, all fixed with tests (commits d62b8b5 … 214da89): obfuscated italic font names, raised
   note-number lines, caps headings below body size, front matter, title note, verse, captions, reference list at
   note size, foot block below notes, URL breaks (now from the PDF's link targets), hyphen joins (document
   evidence), unlabelled short-form pages in the keyed check, English lists in the audit, source proof mode,
   bracket escapes in the Word round trip, Kanon § 3.2 full ranges (+ normalize RANGE-FULL), linter BIB-COLON on
   "Roma:". `test_pdf.py` hand-set pages now run on the Mac; new `test_pdf_layout.py`.
   28.09.2026: MB's answers applied (see `work/ndiaye/ndiaye_queries.md`, top). Next: process the text (MB):
   online-journal articles without DOI (year, URL) is the one open point; then hand `ndiaye_src.md`, refs.json,
   `ndiaye_src_front.md` to srom-tlumacz (stage 2). Future (MB, not now): a sourcing step for missing publisher/
   place (search, list for MB's approval per item) and ISBN lookup via a catalogue API.
5. **E9 typed notes** (T2): `docx_in.py --typed-notes`, page-aware pairing, never guess; test file
   `Dom_Communities Stripped Mac copy.docx` in srom-tlumacz's folder (read-only). The Fotta RTF is not a case
   (no notes at all).
6. ~~Kartoteka E12 flags~~ — done (E13/T9): Nawar, Gurbati, Halabi italic; Mutribowie, Gadżar, Garaczi roman (assimilated).
7. Stage 3, later: house style / reduce the style set (§4, D3) → template as IDML → `config/styles.json` and
   `template_extra` from it → G12 first article in InDesign (the JSX can possibly be run directly against InDesign
   via AppleScript `do script` — untested).
8. Later: ICML output as a fallback to Word import (pandoc writes ICML with footnotes; needs a style-renaming
   step); wire `tb_check.py` into scenario C when srom-tlumacz ships it (E5; CLI fixed in `handoff.md`).

Done 27.09.2026: E10 translator front matter (T7, `test_e10.py`); E11/D9 kartoteka (`srom-kanon/references/
kartoteka.tsv`, T8); E12 foreign exonyms italic (Kanon § 3.4, T6); Kodeks zecera references removed; decisions
15, 18, 19 stay in srom-typeset as toolchain conventions (MB delegated the call).

## 4. House style — everything needed for the style discussion

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
- **Kanon housekeeping for the editor**: the full Polish kanon is no longer in the project, but RULES.md still
  says "where this file and the canon differ, the canon governs" and "v1.5" — decide which text is normative
  (RULES.md, or restore the full kanon inside the kanon skill as `references/`), bump the version, and use one
  section numbering everywhere (E7). Single bibliography division: heading or not — not covered by RULES (we
  print none).

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

Moved to `../_handoffs/MB-decisions.md` (27.09.2026): D1 (decision 20), D2 (22), D3 (21, style set), D4 (Kanon
v1.6 — decided), D7 (first article, G12), D9 (kartoteka). The template as IDML follows D3.
