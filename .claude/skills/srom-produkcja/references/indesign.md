# InDesign: template, import, checks

The DOCX from `build.py` carries **no local formatting at all**: every paragraph has a named paragraph
style, every italic/small-caps run a named character style, footnote numbers have no Word style, no
language is set. InDesign therefore takes everything from the template — provided the names match.

## Template: house style v3 (29.09.2026)

The styles are defined in `indesign/style_spec.json`, readable in `references/style-sheet.md`. They are
vol. 18's own values (read from `dump/03_Ellis.idml` and `dump/09_Konferencja.idml` in InDesign), under new
names and in a designer's order:

- **Root, most used first (15):** Tekst · Tekst BEZ WCIĘCIA · Przypis · Śródtytuł · Śródtytuł MAŁE · Cytat ·
  Bibliografia · Podpis · Podpis LINIA · Wyliczenie · Tytuł · Autor · Afiliacja · Mówca · Tekst INICJAŁ;
  **then the rarer ones (9), also at the root:** Motto · Motto ŹRÓDŁO · Cytat WIERSZ · Przypis GWIAZDKOWY · Tabela TYTUŁ ·
  Tabela TREŚĆ · Przykład FORMA / GLOSA / PRZEKŁAD. Every style the DOCX uses must be at the root: InDesign's Word
  import does not look into folders and makes its own copy (the "Rzadkie" folder, 29.09–02.10.2026, gave a Przypis
  GWIAZDKOWY based on Word's Normal).
- **Folder "Numer" (5):** Pagina · Folio · Spis treści · Spis AUTOR · Spis JĘZYKI.
- **Character styles (8):** Kursywa · Kapitaliki · Indeks górny · Bez podziału · Proste · Pogrubienie · Gwiazdka ·
  Kapitaliki GLOSA.
- **Naming:** the family name first, then a short capitalised qualifier, so the styles read in a narrow panel.
- **Shared styles:** several pipeline roles use one style. Dialogue → Cytat; numbered list → Wyliczenie; bibliography
  title and divisions → Śródtytuł / Śródtytuł MAŁE; table source → Podpis; author note → Tekst BEZ WCIĘCIA;
  speaker's affiliation → Afiliacja.

**Set-up: `indesign/srom_style_setup.jsx`.** Run it on a blank document, or on a copy of an old one to keep its
margins and masters. It:

1. sets the document values: baseline grid every 13.2945 pt from 62.362 pt, relative to the top of the page;
   Footnote Options (style Przypis, superscript reference, an en space after the number (no full stop, Kanon § 7.1), 0.5 pt × 40 mm rule,
   numbering restarts per section, long notes may split); superscript 58 %/33 %; small caps 70 %;
2. **purges** every paragraph and character style. Text in an old style takes its new one (Podrozdzial →
   Śródtytuł, Bez wciecia → Tekst BEZ WCIĘCIA …, the table in `style-sheet.md`); unknown styles → Tekst;
3. builds the house set in panel order, with GREP styles (non-breaking spaces, Kanon § 3.3), the nested style
   of Przypis (note number superscript through the 1-line drop cap, as vol. 18), tab stops and next styles;
4. reads every value back and reports (`<document>_style_setup.txt`): `RESULT: OK` or the lines marked `!`.

The text frame, masters and running-head frames are not the script's business. With a blank document, take the
page (165 × 235 mm) and frames from an old issue, then run the script.

**Verified in InDesign 2026:** `tools/indesign_check/indesign_check.py` (needs InDesign running; hidden windows,
copies only). It runs the script on both vol. 18 files. With the two deliberate changes undone (the Kanon's
no-break rules, the unified Cytat), the PDF equals vol. 18 **line for line** (603/603 and 468/468 lines: text,
position, size, font). With them, the page count stays the same and about 6 % (Ellis) / 3 % (Konferencja) of body
lines re-break where the new no-break rules glue words; Ellis's quotes re-break under Tekst's justification.
`--specimen file.pdf` sets every style on two pages.

What must hold for the import:

1. Paragraph and character style names exactly as the values in `config/styles.json` (case, Polish letters,
   spaces). `template_extra` lists styles the DOCX never uses (title block, running heads, drop cap, captions with
   a rule, footnote number), so the post-import check does not flag them.
2. Small caps = **OpenType small caps** of Cambria, Case: Small Caps (surnames are stored in normal case:
   `Mróz` → M + small caps; Kanon § 9.3).
3. The DOCX brings no footnote formatting. Numbering and the note style come from Footnote Options (set by the
   script).
4. The pipeline never types a non-breaking space; the GREP styles of Tekst (inherited by every style) apply them.
5. Language Polish in all text styles (the DOCX sets none, so hyphenation follows the style).

## The clean template: `indesign/SROM_szablon_v3.idml`

Built by `tools/indesign_check/indesign_check.py --template …` (`make_template.jsx`) from vol. 18's Ellis file:
- **Kept:** its page (165 × 235 mm), margins, masters and threaded text frame.
- **Rebuilt:** every style (house style v3), with placeholder text in each title-block style and one footnote.
- **Running heads:** in *Pagina* ("Imię Nazwisko – Tytuł skrócony", "Studia Romologica 19/2026"); page numbers in *Folio*.
- **Page numbering:** starts at 1.
- **Cleaned out:** unused swatches, imported Word numbering lists, links, hyperlinks, bookmarks, conditions, XML tags,
  empty layers, and 0 pt strokes that carry a colour.

To use it: open the IDML, save it as .indt, and start each article from it. Then place the DOCX into the first
frame (Place, with "Replace Selected Item").

## After final layout: Ibidem, asterisks, bookmarks, DOI links

`<article>_ibidem.jsx` and `<article>_gwiazdki.jsx` report first, then ask whether to make the changes themselves
(MB, 02.10.2026): Ibidem notes on a page or column turn are retyped in full (italics as character style); markers
and asterisk notes get their asterisks. One undo step each; run again after reflow. Moving the asterisk notes above
the numbered notes of their page stays by hand.
`indesign/srom_zakladki.jsx` (general, in the panel): PDF bookmarks from Tytuł / Śródtytuł / Śródtytuł MAŁE; a rerun
replaces its own bookmarks. Export the PDF with General ▸ Include ▸ **Bookmarks** ticked.
`<article>_doi.jsx` (written when a printed work has a DOI; SYS-5): every citation in the notes and every bibliography
entry whose work has a DOI gets an **invisible** hyperlink to `https://doi.org/…`; nothing is printed (GEN-10). The build
finds each citation's text (several works in one note are cut apart with a marked copy of the CSL) and encodes the URL
(everything but letters, digits, `- . _ ~ /`: old SICI DOIs carry `< > ; ( ) :`). The script finds the text in its
note or entry, reports, asks, then links; a note retyped since the build (an Ibidem written in full) that cites one work
becomes one link; anything not found is listed. Run it **last**, right before the export (text retyped after it loses
its link); a rerun replaces its own links. Export with General ▸ Include ▸ **Hyperlinks** ticked. Proven live:
`tools/indesign_check/doi_check.py <build dir>` (places the DOCX in the template, runs the script twice, reads the PDF:
Ostendorf 36/36 links, a SICI DOI intact).
PDF metadata: `srom-quant/scripts/pdf_metadata.py <master CSV> <article_id> --out <build dir>` → `<article_id>_metadane.jsx`;
run it on the document before the export (title, author, citation line, keywords, licence, DOI and PRISM fields from the
master row; a placeholder DOI is left out and named).

## After final layout: `indesign/srom_final_pass.jsx` (Kanon § 3.6)

Run it once the pages are final (after `_ibidem.jsx` and `_gwiazdki.jsx`) and again after any reflow. It checks
the story with the text cursor, or every story. Footnotes are checked too: a split note is a paragraph.

| Report | What it means | Fix mode |
|---|---|---|
| SZEWC | first line of a paragraph alone at the foot of a column | tracking |
| BĘKART | last line alone at the top of a column (Kanon: min. 2 lines on each side of a break) | tracking |
| WDOWA | last line shorter than 5 characters, or only the end of a hyphenated word | tracking |
| PUSTY WIERSZ | spaces or a line break before the paragraph end make an empty line | removed |
| ŚRÓDTYTUŁ | a heading closes a column (the styles keep with next; this finds overrides) | by hand |
| SIEROTKA | a one-letter word at a line end | by hand |
| PÓŁPAUZA | a dash starting a line (outside lists) | by hand |
| URL | a URL broken other than after "/" or before "." | by hand |
| DZIELENIE | a name, abbreviation or number split at a line end | by hand |
| OVERSET | text does not fit | by hand |
| fonts | fonts other than Cambria, or missing fonts | by hand |
| info | a hyphen at a page turn (last line of a right-hand page) | by hand |

**Fix mode.** It does what vol. 18 did by hand: paragraph tracking −5/−10/+5/+10 (never beyond ±10). The
tracking goes on the paragraph or on one of the three before it in the same column. A change is kept only if the
problem goes away, no new one appears in that column or the next, and no new overset text appears. All changes
are **one undo step**. Report: `<document>_final_pass.txt` (every fix with its page and paragraph; every
remaining problem marked `!`). The limits (characters, tracking steps, time budget 5 min) are in
`style_spec.json` → `final_pass`.

## Word import preset "SROM – pandoc" (create once)

File ▸ Place ▸ select DOCX ▸ ✓ Show Import Options:

- Include: ✓ Footnotes · ✗ Endnotes · ✗ Table of Contents Text · ✗ Index Text
- Options: ✗ Use Typographer's Quotes (quotes are already final) 
- Formatting: ● Preserve Styles and Formatting from Text and Tables · Manual Page Breaks: No Breaks ·
  ✗ Import Inline Graphics · ✗ Import Unused Styles · ✗ Track Changes · Convert Bullets & Numbers: n/a
- Style Name Conflicts: Paragraph → **Use InDesign Style Definition** · Character → **Use InDesign Style Definition**
- Save Preset… → `SROM – pandoc`

If names cannot be made identical, use Customize Style Import → Style Mapping instead (same result,
more clicks per article).

## After placing: `<article>_postimport.jsx`

Link the scripts into the Scripts Panel with `sh tools/install_scripts.sh <build dir>` (symlinks; each text gets its
own panel folder `srom_<stem>`, so several texts never mix; works with InDesign closed, the scripts appear at the next
launch; also links the two general scripts). Then double-click a script in the panel. Report-only; changes nothing. If the
document holds more than one article, put the text cursor in the article first — both scripts then
check only that story. If this InDesign version does not expose paragraph overrides to scripts, the
report says so instead of claiming zero.
`RESULT: OK — import is clean` requires: footnote count = build report, every paragraph style from
the whitelist, no foreign character styles, **zero paragraphs with overrides** (the "+"), no straight
quotes / double spaces / em dash / "..." / “, the asterisk markers and notes as counted by the build, and
no "– przyp. tłum./red." note among the numbered footnotes.

## After final layout: `<article>_ibidem.jsx`

Kanon §7.3: *Ibidem* only when the previous note is the same work **and in the same column**. The build
already printed the short form wherever *Ibidem* would be ambiguous or ungrammatical (listed in the
build report); only the layout knows the column. The script checks every CSL *Ibidem* against the
note before it (page, text frame, column) and prints `REPLACE … with: Ficowski, *Cyganie…*, s. 17.` —
type that text, `*…*` in the italic character style, and run the script again until `RESULT: OK`.
Report file `<document>_ibidem.txt` is saved next to the INDD. Literal (non-CSL) Ibidem notes are
listed in the build report — check them by eye. Re-run after any reflow.

## After final layout: `<article>_gwiazdki.jsx` (only if the article has non-author notes)

Kanon §7.1: the title note, translator's (`– przyp. tłum.`) and editorial (`– przyp. red.`) notes are one
series `*`, `**`, `***` …, restarting on every page, set **above the numbered notes**, in the style
*Przypis GWIAZDKOWY* (= *Przypis*). They cannot be InDesign footnotes (one footnote sequence per story), so the
build delivers them as paragraphs at the end of the story (title note first, each opening `* `) and a `*` in
*Gwiazdka* at each marker. By hand: move each note to the foot of its page above the numbered
notes (e.g. a separate text frame; shorten the main frame so the numbered notes sit below it). The script
lists every marker with its page and the asterisks it gets (`p. 12  **  Uwaga…`), the title note first on
the article's first page — set marker and note to that count. Report `<document>_gwiazdki.txt`. Re-run after
any reflow.

## First real article — verification (gate G12)

The toolchain is tested up to the DOCX; InDesign behaviour must be confirmed once by the editor:

1. Paragraph Styles panel after Place: no new styles, no "+" anywhere → post-import script OK.
2. Footnote reference numbers in text formatted by Footnote Options (superscript), numbers in notes
   likewise; no stray space after the number.
3. Italic and small-caps runs carry the character styles (Find/Change ▸ Find Format ▸ character style
   → count ≈ the counts in the build report's DOCX verification line).
4. Bibliography: `Śródtytuł MAŁE` division headings, surnames in small caps, `de` and institutions not.
5. nbsp GREP styles visibly working (`s. 15`, `J. Ficowski`, `w Krakowie`).
6. With non-author notes: markers in *Gwiazdka*, notes in *Przypis GWIAZDKOWY*; after placing them
   above the numbered notes, `_gwiazdki.jsx` gives the asterisk count per page.

Record the result (screenshot or the two script reports) — that closes G12.

## If Word import misbehaves

Fallback worth testing on the first article: pandoc also writes ICML (InCopy), which InDesign places
natively with paragraph/character styles and footnotes — no Word import heuristics at all. Its style
names follow pandoc's scheme, so it would need a small renaming step (not built yet; ask for it if the
Word route shows problems).
