# Online cover page — design data for the design system (MB's template 2, 07.10.2026)

Source of truth: `SROM_okladka_szablon_MB2.idml`; implemented in `.claude/skills/srom-quant/scripts/cover_page.py`
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
No hyphenation anywhere. Polish language. Italic only for the titles inside "Jak cytować" and "Pierwodruk".
| Element | Size / leading (pt) | Colour |
|---|---|---|
| Info block (top left) | 8 / 10.5 | ink |
| Polish title | 15 / 18 | red |
| English title | 12 / 16 | ink |
| Author line: name · ORCID · e-mail, "   |   " between | name 12 / 15, the rest 8 | name red, rest ink |
| Affiliation | 8 / 10.5 | ink |
| "Tłumaczenie:", "Pierwodruk:" | 8 / 10.5 | ink |
| Citation ("Jak cytować:") | 8 / 10.5 | ink, label red |
| Section labels ("Abstrakt", "Abstract") | 9.5 / 11.5 | red |
| Abstracts and keywords | 7.2 / 10 (fallback 7.0 / 10) | ink, justified (last line left), keyword label red |
| Footer (dates line; © + licence line) | 6 / 8.5, tracking −10 (−0.01 em) | ink |

## Grid (pt, from the top-left of the page)
- Label column x 17.0 (6 mm). Text column x 70.9–433.7 (25–153 mm).
- Info block x 70.9, top y 18.9: "Studia Romologica 18/2025" · ISSN · Strony · DOI (full https://doi.org/… URL, linked).
- Logo x 320.4–433.7, y 17.7–63.9, linked to the site.
- **Header block, fixed edges:** Polish title top y 83.8, citation bottom y 269.7. Inside: Polish title · English title ·
  author(s) (each: name | ORCID | e-mail, affiliation under it) · "Tłumaczenie:" + "Pierwodruk:" (translations only) · citation.
  Least gaps (frame to frame): 14 · 8.3 · 6 between authors · 9 · 10.1. They stretch together, up to 2×, to fill the block;
  a long header shrinks them down to ½, then runs over and pushes the abstracts down. An author line too long for one line
  puts the e-mail under it.
- **Abstract block, fixed edges:** Polish block top y 283.3 (label and text share it), English block 13.4 below it, as tall as
  its text, never below 218 mm (617.95). Keywords 14 pt baseline to baseline under the abstract's last line.
- Footer: dates line top y 629.3 ("Data publikacji: … | Data publikacji online: … | Okres redakcji: …", items left out when
  their field is empty); © + licence line top y 640.5, the licence name linked to its CC deed page (…/deed.en).
  Open Access mark x 17.0–62.2, y 639.8–656.1. No publisher line.

## Behaviour (the rules that make it a template, not a picture)
- One page strictly. Type sizes never shrink beyond the 7.2 → 7.0 step; if it still does not fit the run stops and names the overflow.
- A placeholder or empty field in anything printed (10.XXXXX DOI, TODO, empty date) stops the run; `--proof` prints it anyway and marks the page PODGLĄD.
- Texts without abstracts (reviews, chronicles) get the header alone.
- Data: e-mails from `volumes/autorzy.tsv` (`kontakt`, by ORCID, else by name); dates from the CSV's `pub_date_print`
  (optional) and `pub_date_online`; "Okres redakcji" from `editorial_period` (optional, printed as written).
- Hard spaces after one-letter words, s., t., nr, initials, before % (Kanon § 3.3). Dates dd.mm.rrrr. Keywords separated by semicolons.
- Output also carries: page labels (cover i, article keeps printed numbers), link annotations, PDF Info + XMP (Dublin Core, rights, PRISM).

## Character of the design (for reuse on other filing / metadata documents)
Flat and typographic: one family, two weights of emphasis (red vs ink, size), no rules, boxes or shading, generous white,
label column on the left as in a register or catalogue card, machine-readable identifiers (DOI, ISSN, ORCID) set as plain
linked text at the top right. Red is reserved for what identifies (titles, names, labels); everything descriptive is ink.
