# InDesign: template, import, checks

The DOCX from `build.py` carries **no local formatting at all**: every paragraph has a named paragraph
style, every italic/small-caps run a named character style, footnote numbers have no Word style, no
language is set. InDesign therefore takes everything from the template — provided the names match.

## Template requirements

The house style is defined in `indesign/style_spec.json` and listed in `references/style-sheet.md`;
`indesign/srom_style_setup.jsx` builds it in a copy of the template (renames the old styles, so existing
text keeps its formatting). What must hold afterwards:

1. Paragraph styles named exactly as the values in `config/styles.json` → `paragraph` — including the
   ones the DOCX uses only occasionally: verse quotation, numbered list (hanging indent, tab stop — the
   number is typed), table title/cell/source, title note (asterisk), the three interlinear-example lines
   (with tab stops; form line italic in the style; gloss categories via a GREP style → small-caps
   character style)
   (case, Polish letters, spaces, en dash). If a template name differs, change the config, not the
   template; `config/styles.json` → `template_extra` lists template styles the DOCX never uses
   (title block, running heads, footnote-number styles) so the post-import check does not flag them.
2. Character styles for `italic` and `smallcaps`. Small caps = **OpenType small caps** of the text font
   (kanon §9.3), Case: Small Caps (surnames are stored in normal case: `Mróz` → M + small caps).
3. Footnote Options (Type ▸ Document Footnote Options): numbering and the reference/number character
   styles are set here — the DOCX deliberately brings none. Paragraph style of the note = the
   `footnote` name in the config. Restart numbering: per story/document as per volume practice.
4. GREP styles for non-breaking spaces (kanon §3.3) in body, quote, list, footnote and bibliography
   styles: after `s.` `t.` `z.` `nr` `r.` `w.` `sygn.` `k.`, after initials, before `%`, after one-letter
   words `i a o u w z` (and capitals). The pipeline never types nbsp.
5. Language Polish in all text styles (the DOCX sets none, so hyphenation follows the style).

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

Copy the two JSX files from the build folder to the Scripts Panel folder (Window ▸ Utilities ▸
Scripts ▸ User ▸ Reveal in Finder/Explorer) and double-click. Report-only; changes nothing. If the
document holds more than one article, put the text cursor in the article first — both scripts then
check only that story. If this InDesign version does not expose paragraph overrides to scripts, the
report says so instead of claiming zero.
`RESULT: OK — import is clean` requires: footnote count = build report, every paragraph style from
the whitelist, no foreign character styles, **zero paragraphs with overrides** (the "+"), no straight
quotes / double spaces / em dash / "..." / “.

## After final layout: `<article>_ibidem.jsx`

Kanon §7.3: *Ibidem* only when the previous note is the same work **and in the same column**. The build
already printed the short form wherever *Ibidem* would be ambiguous or ungrammatical (listed in the
build report); only the layout knows the column. The script checks every CSL *Ibidem* against the
note before it (page, text frame, column) and prints `REPLACE … with: Ficowski, *Cyganie…*, s. 17.` —
type that text, `*…*` in the italic character style, and run the script again until `RESULT: OK`.
Report file `<document>_ibidem.txt` is saved next to the INDD. Literal (non-CSL) Ibidem notes are
listed in the build report — check them by eye. Re-run after any reflow.

## First real article — verification (gate G12)

The toolchain is tested up to the DOCX; InDesign behaviour must be confirmed once by the editor:

1. Paragraph Styles panel after Place: no new styles, no "+" anywhere → post-import script OK.
2. Footnote reference numbers in text formatted by Footnote Options (superscript), numbers in notes
   likewise; no stray space after the number.
3. Italic and small-caps runs carry the character styles (Find/Change ▸ Find Format ▸ character style
   → count ≈ the counts in the build report's DOCX verification line).
4. Bibliography: `Bibliografia – dział` headings, surnames in small caps, `de` and institutions not.
5. nbsp GREP styles visibly working (`s. 15`, `J. Ficowski`, `w Krakowie`).

Record the result (screenshot or the two script reports) — that closes G12.

## If Word import misbehaves

Fallback worth testing on the first article: pandoc also writes ICML (InCopy), which InDesign places
natively with paragraph/character styles and footnotes — no Word import heuristics at all. Its style
names follow pandoc's scheme, so it would need a small renaming step (not built yet; ask for it if the
Word route shows problems).
