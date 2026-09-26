# srom-typeset — handover (state at 26.09.2026)

For the next session (Claude Code). Read this, then `CLAUDE.md`, then `skills/srom-typeset/SKILL.md`.
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

Tests: `python3 tests/run_all.py` → `SUITE ALL PASS 10/10` (~230 checks, ~30 s). Unlazy ledger: `GATES.md`
(G1–G16 met; G12 = InDesign import, abandoned here: needs the editor or a machine with InDesign).

## 2. Decisions register (`references/decisions.md`)

✔ closed by the editor: 1–19 (incl. 5: only the sections used are printed, without numerals; 7: page-less
citations never block, listed in the query sheet; 10: numbered lists `1.` allowed; 15: comments never block
anything). Note: kanon RULES.md as currently in this project is v1.5 and does NOT yet encode these; do not
sync decisions into it until the editor confirms the kanon is being actively updated (see §5).
○ open: **20** handoff rules; **21** house style v2 (in the style discussion, §4); **22** translator additions
declared by `"srom-added"` in `<id>_refs_tlum.json`.

## 3. Queue for Claude (in order)

1. ~~**Repo setup**~~ — done 26.09.2026 (Claude Code): git repo, skills symlinked, venv; suite green on the
   Mac with pandoc 3.8.3 after one fix (the 3.8 DOCX reader put "Table Caption" inside the table caption →
   `docx_in.py` dropped every table caption in the working-copy round trip; fixed, test added). `GATES.md`
   was not in the uploaded archive — the G1–G16 ledger is lost; new gates start in `/GATES.md`.
2. **srom-kanon / srom-typeset overlap** — recommendation agreed in principle? (see §5) If yes: remove the bundled
   linter from srom-typeset (require srom-kanon; fail clearly if absent), move closed decisions into kanon RULES,
   renumber cross-references to RULES numbering, bump RULES header (still says v1.5).
3. **E8 — asterisk series for non-author notes** (spec §6).
4. **House style: reduce the style set** (§4) — editor ran the setup script: it works, but there are too many
   styles for a designer. Discuss first, then change `style_spec.json` (config can map several roles to one style).
5. **Template → config**: once the style set is settled, fill `config/styles.json` and `template_extra` from the
   real template (IDML), re-run `make_style_setup.py`.
6. **G12**: first real article end to end; InDesign checklist in `references/indesign.md`. In Claude Code on the
   editor's machine the JSX can possibly be run directly against InDesign (AppleScript `do script` on a Mac) —
   untested, worth trying.
7. Later: ICML output as a fallback to Word import (pandoc writes ICML with footnotes; needs a style-renaming
   step); `tb_check.py` slot when srom-tlumacz ships it (CLI fixed in `handoff.md`).

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

## 6. E8 — asterisk series for non-author notes (editor's ruling 25.09.2026)

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

1. Decide 20, 22; 21 in the style discussion (§4).
2. Kanon: normative text + version + numbering (§5); confirm the two-skill recommendation.
3. Relay to srom-tlumacz: E1–E6 done; additions declared via `"srom-added"`; comments never block; E8 queued
   on the srom-typeset side.
4. After the style discussion: the cleaned template as IDML.
5. First real article → G12 checklist.
