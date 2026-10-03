# Online cover page — design data for the design system (MB's template 1.2, 04.10.2026)

Source of truth: `SROM_okladka_szablon_MB1.2.idml`; implemented in `.claude/skills/srom-quant/scripts/cover_page.py`
(constants at the top). What follows is the page as a reusable "metadata / filing sheet": a quiet, industrial
record page that sits in front of a document, reads as a digital add-on and never as printed matter.

## Page
- Trim 165 × 235 mm (467.72 × 666.14 pt), one page, no bleed, no marks, portrait.
- Two full-height red bars at the outer edges, 1.5 mm (4.25 pt) wide, SROM red. Nothing else is filled.
- Background white. Everything is drawn from data (one master-CSV row); no free text on the page.

## Colour
| Role | Value |
|---|---|
| SROM red (bars, titles, author name, labels, "Jak cytować:" / "Pierwodruk:" / keyword labels) | RGB 227 0 11 = `#E3000B` |
| Ink (all other type) | 88 % black = CMYK 0 0 0 88 → RGB 66 66 65 = `#424241` |
| Links (DOI, ORCID, licence, site) | same ink, no underline |
Only these two colours. The logo and the Open Access mark are placed as PDFs (`assets/cover/sr_logo.pdf`, `open_access.pdf`;
the OA mark keeps its own orange).

## Type — IBM Plex Sans, Regular and Italic only (no bold, no other weights)
No hyphenation anywhere. Polish language. Italic only for the title inside "Jak cytować" and "Pierwodruk".
| Element | Size / leading (pt) | Colour |
|---|---|---|
| Info block (right) and journal block (under logo) | 8 / 10.5 | ink |
| Polish title | 16 / 19 | red |
| English title | 12 / 16 | ink |
| Author name | 12.5 / 15 | red |
| Affiliation, ORCID, translator | 9.5 / 12 | ink |
| Citation ("Jak cytować:") and "Pierwodruk:" | 8 / 10.5 | ink, label red |
| Section labels ("Abstrakt", "Abstract") | 9.5 / 11.5 | red |
| Abstracts and keywords | 7.2 / 10 (fallback 7.0 / 10) | ink, justified (last line left), keyword label red |
| Footer (licence sentence, publisher line) | 6 / 8.5, tracking −10 (−0.01 em); 3 pt above the publisher line | ink |

## Grid (pt, from the top-left of the page; mm in brackets)
- Label column starts at x 17.0 (6 mm). Text column from x 70.9 (25 mm) to x 433.7 (153 mm): width 362.8 pt (128 mm).
  Right margin 12 mm. The label column and the text column overlap in width only; labels are short.
- Logo box x 70.9–184.3, y 11.3–57.5 (25–65 mm, 4–20.3 mm), linked to the site.
- Info block (right): left edge x 290.4 (102.5 mm), top y 12.5 (4.4 mm), width to the right margin. Lines in this order:
  Strony · DOI (full https://doi.org/… URL, linked) · licence short name (CC BY 4.0) · © year + authors ·
  Opublikowano online dd.mm.rrrr. If a line is too long the whole block moves left; it never wraps.
- Journal block: x 70.9, top y 61.8 (21.8 mm), two lines: "Studia Romologica 18/2025", "ISSN: 1689-4758".
- Title starts at y 95.8 (33.8 mm) at the earliest (journal block bottom + 13.1 pt).
- Header chain, gaps frame to frame (pt): journal → title 13.1 · Polish title → English title 7.3 · English title → author 7.2 ·
  author → author 6 · author → translator 6 · author → citation 10.3 · citation → "Pierwodruk" 4 · citation → first abstract 15.6.
- Abstract blocks: label at x 17.0 and text at x 70.9 share one top edge. Polish block, then English block 13.4 pt below it.
  Keywords stand 14 pt baseline to baseline under the last line of the abstract (a 4 pt extra space).
  The blocks are as tall as their text; the English block may reach 218 mm from the top (617.95 pt), never further.
- Footer: text frame x 70.9–433.7, top y 627.2 (221.2 mm); Open Access mark x 17.0–62.2, y 630.2–646.5 (6–21.9 mm, 222.3–228.1 mm).
  Licence sentence first, publisher line below with the site.

## Behaviour (the rules that make it a template, not a picture)
- One page strictly. Type sizes never shrink beyond the 7.2 → 7.0 step; if it still does not fit the run stops and names the overflow.
- A placeholder or empty field in anything printed (10.XXXXX DOI, TODO, empty date) stops the run; `--proof` prints it anyway and marks the page PODGLĄD.
- Texts without abstracts (reviews, chronicles) get the header alone.
- Translations add "Tłumaczenie: …" under the authors and "Pierwodruk: …" (original title in italic, source, DOI link) under the citation.
- Hard spaces after one-letter words, s., t., nr, initials, before % (Kanon § 3.3). Dates dd.mm.rrrr. Keywords separated by semicolons.
- Output also carries: page labels (cover i, article keeps printed numbers), link annotations, PDF Info + XMP (Dublin Core, rights, PRISM).

## Character of the design (for reuse on other filing / metadata documents)
Flat and typographic: one family, two weights of emphasis (red vs ink, size), no rules, boxes or shading, generous white,
label column on the left as in a register or catalogue card, machine-readable identifiers (DOI, ISSN, ORCID) set as plain
linked text at the top right. Red is reserved for what identifies (titles, names, labels); everything descriptive is ink.
