# Online cover page — design B, website typography (MB, 21.10.2026) [general]

In use since 21.10.2026 (MB: "we switch to this version"). Implemented in `.claude/skills/srom-quant/scripts/cover_page.py`
(constants at the top) and, as an InDesign template, in `scripts/cover_idml.py`. The page is a quiet, industrial
record page in front of the article: it reads as a digital add-on, never as printed matter.

Design B is template 2 (`SROM_okladka_szablon_MB2.idml`, 07.10.2026; appendix below) with the website's type and red.
The grid, frame positions, gaps, data and every rule of behaviour are unchanged. Proposal and its sample (Fotta, vol. 18
no. 2, before the red and title-rule changes): `_okladki_v18_v3_web/`.

## Page
- Trim 165 × 235 mm (467.72 × 666.14 pt), one page, no bleed, no marks, portrait, white.
- Two full-height red bars at the outer edges, 1.5 mm (4.25 pt) wide. Nothing else is filled.
- Everything is drawn from data (one master-CSV row); no free text on the page.

## Colour
| Role | Value |
|---|---|
| Red: bars, titles, author name, red labels | the website's accent `#DF261E` = RGB 223 38 30 (MB 21.10.2026; template 2 had `#E3000B`) |
| Ink: all other type | 88 % black = CMYK 0 0 0 88 → RGB 66 66 65 = `#424241` |
| Links (DOI, ORCID, licence, site) | ink, no underline |

Logo and Open Access mark: placed PDFs (`assets/cover/sr_logo.pdf`, `open_access.pdf`), unchanged.

## Faces by role (from the website: Elementor kit, `custom.css`)
| role | face | website precedent |
|---|---|---|
| Polish title, author name | Epilogue SemiBold | H1/H2, author name 600 |
| English title, titles of works | Fraunces 9pt Regular / Italic | `srom_serif_title` |
| running text: affiliation, translator, original, citation, abstracts, keywords, footer | Epilogue Regular | body, `srom_small`, `srom_meta` |
| labels ABSTRAKT, ABSTRACT, SŁOWA KLUCZOWE, KEYWORDS, JAK CYTOWAĆ, TŁUMACZENIE, PIERWODRUK | IBM Plex Mono Medium, caps, tracking 140 (0.14 em) | `srom_mono` eyebrows |
| identifier block: volume, ISSN, pages, DOI | IBM Plex Mono Medium | DOI badge, volume number |

Italic is used only for titles of works (Kanon); the website has no italics. No hyphenation anywhere. Ligatures off.

## Sizes (pt, size / leading)
| element | size / leading | colour |
|---|---|---|
| identifier block | 7.5 / 10.5 | ink |
| Polish title | 15 / 17.5 SemiBold | red |
| English title | 12 / 15 Fraunces | ink |
| author name · ORCID, e-mail | 11.5 SemiBold · 7.5, line 15 | name red, rest ink |
| affiliation, translator, original, citation | 8 / 10.5; titles of works in Fraunces Italic 8.4 | ink |
| column labels ABSTRAKT / ABSTRACT | 7 mono caps, first baseline on the abstract's | red |
| inline labels | 6 mono caps, no colon, then a word space | JAK CYTOWAĆ, SŁOWA KLUCZOWE, KEYWORDS red; TŁUMACZENIE, PIERWODRUK ink |
| abstracts | 6.8 / 9.6 justified (fallback 6.6) | ink |
| keywords | as the abstract, flush left | ink |
| footer (dates; © + licence) | 6 / 8.5 | ink |

Why 6.8: Epilogue sets about 9 % wider than Plex Sans and has a larger x-height (0.531 vs 0.516 em). At 6.8 pt it matches
template 2's Plex Sans at 7.2 pt in both, so the page holds the same text. Capacity before the fallback is needed matched
template 2 within ±4 % on vol. 18 nos. 2, 3 and 5.

## Grid
Unchanged from template 2 (appendix): label column x 17.0, text column x 70.9–433.7, info block at y 18.9, logo
320.4–433.7 × 17.7–63.9, header block from 83.8 to 269.7 with stretching gaps, abstracts from 283.3 to at most 218 mm,
footer at 629.3 / 640.5, Open Access mark 17.0–62.2 × 639.8–656.1.

## Behaviour
Everything in template 2's list stands (one page strictly; placeholders stop the run; texts without abstracts get the
header alone; e-mails from `autorzy.tsv`; dates from the CSV; hard spaces, Kanon § 3.3). Added in design B:
- **Short title words (MB 21.10.2026):** in the Polish and the English title, a word of 4 letters or fewer never ends a
  line; it moves to the next with the word after it (`title_words()`, a no-break space after the word). The last word has
  no next word, so a short word is never left alone on the last line. Dashes and other punctuation are not words.
  The header titles only, not the title inside the citation.
- A page range in the citation never splits at its dash (no-break span).
- The original's source line ("Pierwodruk") gets the Kanon § 3.3 hard spaces too ("t. 34").

## Identifier marks (MB 28.11.2026: "discreet, preferably monochrome")
- **ORCID iD** before each ORCID in the author line: MB's ring icon (`assets/cover/orcid_id.pdf`, recoloured to the ink),
  6.5 pt, linked to the iD; the iD URL stays as text. `ORCID_ICON = "orcid_id_green.pdf"` gives ORCID's green (its display
  guidelines ask for green "in most circumstances", black-and-white only for contrast).
- **ROR** after each institution of the affiliation that has a ROR ID in `volumes/ror.tsv` (split as in the deposit:
  "A; B", "A / B"): ROR's icon in black (`ror_icon.pdf`, MB 28.11.2026; ROR allows #53BAA1, #2C2C2C, black or white),
  7.5 pt high with its own margin, linked to ror.org. An institution without a ROR ID in ror.tsv (an independent
  scholar, a museum ROR does not list) gets no icon. ROR asks that the ID text be shown too where the icon is; the
  cover shows the icon alone (MB's call).
- **Crossmark** (only on an article whose deposit carries it: `CROSSMARK_POLICY_DOI` set and its volume in
  not in `CROSSMARK_EXCLUDE` in `generate_crossref_xml.py`: every volume deposited since 28.11.2026; vols 17–18 after their
  Feb–Mar 2027 back-fill; every
  `--proof` shows it, as a design preview): Crossref's
  black-and-white horizontal "Check for updates" button (`crossmark_bw_horizontal.pdf`, unaltered), 62 pt wide, at the
  text column's left edge 6.5 pt under the DOI line, above the title (Crossref: "next to or above the title"); linked to
  `https://crossmark.crossref.org/dialog?doi=<DOI>&domain=pdf&date_stamp=<pub_date_online>`. XMP gains `crossmark:DOI`,
  `crossmark:MajorVersionDate`, `pdfx:doi`, `pdfx:CrossmarkMajorVersionDate`. The header block below does not move.
- Mechanics: the text holds a run of no-break spaces in the mono face where an icon goes (so lines break around it and
  the text layer reads clean); the icon is drawn into that gap after the layout. A count of gaps that does not match the
  icons wanted stops the run.
- Icons: vector PDFs converted once by LibreOffice from the publishers' SVGs (Crossmark CDN `CROSSMARK_BW_horizontal.svg`,
  ROR `ror-icon-bw.svg` (CC BY-ND 4.0, unaltered), MB's `ORCID icon.svg`), 28.11.2026; MuPDF's own
  SVG reader drops the Crossmark button's styles and gradient.

## Fonts (`.claude/skills/srom-quant/assets/cover/fonts/`, OFL; licences beside them)
Static cuts from the Google Fonts variable files (the website's source), made for MuPDF:
- Epilogue 400 and 600; Fraunces opsz 9, wght 400, SOFT 0, WONK 0 (Regular and Italic).
- Fraunces: the `rvrn` substitutions (n, m, h… to their text-size forms, which the site also shows at text sizes) are
  written into the cmap. Without that, the PDF text layer of every Fraunces line is garbled ("Ro,a.ie4").
- Epilogue and Fraunces: the `liga` feature is removed, because MuPDF writes ligature glyphs into the text layer wrongly
  (fi → U+FB01; ff → U+0239, "diȹerent"). Template 2 had the same fault.
- `SROMLabelMono-Medium`: Plex Mono Medium with 0.14 em added to every advance. MuPDF ignores CSS `letter-spacing`, so the
  tracking is in the font. It is renamed because of the OFL Reserved Font Name "Plex", and is for the renderer only.
The cover no longer depends on fonts installed on the machine (template 2 searched the Mac and Linux font folders).

## InDesign template (`cover_idml.py <master.csv> <article_id> <out.idml>`)
- Built on template 2's IDML. It writes paragraph and character styles (group "Okladka web") and one frame per block, at
  the positions and first baselines `cover_page.py` gives that article. The swatch "SROM red" carries `#DF261E`; "SROM ink"
  is CMYK 0 0 0 88. Links are not written: the PDF gets them from `cover_page.py`.
- Fonts in InDesign: Epilogue, Fraunces Italic and IBM Plex Mono Medium come from Adobe Fonts; install
  `assets/cover/fonts/Fraunces9pt-Regular.ttf` for the English title. InDesign 2026 imports Adobe's variable "Fraunces Regular"
  at 12 pt as a custom instance "9pt-12.000" that loses its weight and falls back to Thin, whatever the optical-size
  preference, and even from its own exported markup.
- Set for parity with the renderer: Single-line Composer, minimum word spacing 100 % (MuPDF never squeezes), ligatures off,
  a 2.3 pt right inset in every text frame (MuPDF breaks about 2.0–2.1 pt before the edge; InDesign measures to the outline),
  document optical size off.
- Checked in InDesign 2026 (21.10.2026) on vol. 18 no. 2, vol. 17 no. 1 (two authors, e-mail under the line) and vol. 18
  no. 5: the InDesign export breaks every line as the PDF does (42, 38 and 50 lines). Baselines are within 0.1 pt, except
  1 pt on a line where the e-mail moved under the author line.

## Open
- InDesign's IDML import of variable Fraunces (above): for Adobe or for a later InDesign. Nothing to do on our side
  while the static cut is installed.

---

## Appendix: template 2 (MB 07.10.2026), retired 21.10.2026
Source: `SROM_okladka_szablon_MB2.idml`; proofs `_okladki_v18_v2/`. IBM Plex Sans Regular and Italic only; red `#E3000B`.
Sizes: info 8 / 10.5; Polish title 15 / 18 red; English title 12 / 16; author name 12 / 15 red with ORCID and e-mail at 8;
affiliation, "Tłumaczenie:", "Pierwodruk:", citation 8 / 10.5 (labels with colons, "Jak cytować:" red); section labels
"Abstrakt" and "Abstract" 9.5 / 11.5 red; abstracts and keywords 7.2 / 10 justified (fallback 7.0), keyword label red;
footer 6 / 8.5 with tracking −10. Grid and behaviour as in design B above.
Character: flat and typographic, one family, no rules, boxes or shading, a label column on the left as on a catalogue card.

**If MB asks for template 2 again, fix these first.** `cover_page.py` no longer draws it; git history before 21.10.2026 has it.
1. Page range in the citation can split at its dash ("s. 51–" / "84."): put it in a no-break span.
2. "Pierwodruk": the source string goes out without the Kanon § 3.3 hard spaces ("t. 34" can split): pass it through `pl()`.
3. The footer's tracking −10 is never applied: MuPDF ignores CSS `letter-spacing`. Bake it into a font cut, or drop it.
4. Ligature glyphs in the text layer (fi → U+FB01, ff → U+0239): remove `liga` from the Plex Sans cuts used.
5. Font search: template 2 read IBM Plex Sans from the Mac (`~/Library/Fonts/FontBase`) or Linux font folders. Ship the
   cuts in `assets/cover/fonts/` as design B does.
6. Red: template 2's `#E3000B` differs from the website's `#DF261E`. Ask MB which.
