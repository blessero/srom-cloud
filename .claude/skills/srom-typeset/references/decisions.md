# Decisions where the kanon was silent (candidates for the §17 register)

Implemented and covered by tests. Status: ✔ confirmed by the editor · ○ taken, not yet confirmed.

| # | decision | where |
|---|---|---|
| 1 | ✔ Note marker goes before `, ; :` as well as before the period (§7.1 names only the period); after an abbreviation period it stays after it (`XV w.[^3]`). | normalize.py |
| 2 | ✔ (notes only; the bibliography always gives every author in full) Short form of multi-author works: `Mróz, Bartosz, *Tytuł…*`; four or more: `Fiałkowska i in., *…*`; edited volume: surname only, no "(red.)". | srom.csl |
| 3 | ✔ Short title = `title-short` when given (with `…` if truncated), otherwise the full title. | srom.csl |
| 4 | ✔ ISBN printed `ISBN 978-…` without a colon (§9.4 shows only the DOI form `DOI: …`). | srom.csl |
| 5 | ✔ Bibliography: only the sections an article uses are printed, **without numerals**; a single section gets no subheading. | build.py |
| 6 | ✔ Name particles lower case and outside small caps (`de HEUSCH`); institutional authors not in small caps. | srom_post.lua, build.py |
| 7 | ✔ **Revised with the editor:** a citation without a page is always allowed and never printed with a placeholder. Every one is listed in the query sheet: as the source of a quotation (marker after ” or «, or in a block quote) → "prosimy o stronę" to the author; otherwise → "odwołanie do całości dzieła", for the editor to confirm. A whole-work citation of an article prints no page range in the note (the range is in the bibliography). | srom_post.lua, build.py |
| 8 | ✔ *Ibidem* is printed only where it is unambiguous: never inside a sentence, never when the same or the preceding note also cites a literal source (archival unit, press issue…). There the short form is printed instead — never wrong, only less compact. | build.py |
| 9 | ✔ Author-date conversion: parenthetical → marker at its place (`tekst (A 1985).` → `tekst[^n].`); narrative → marker right after the name (`Ficowski (1985) twierdzi` → `Ficowski[^n] twierdzi`); page-only `(s. 21)` → citation of the work cited just before it (listed; blocks only when there is none); "Name (year)" whose name is no ref author (`w Warszawie (1920)`) is left alone and listed. | cite_map.py |
| 10 | ✔ Numbered lists (now kanon RULES §2): arabic `1.` never `1)`; number typed as "1." + tab, own style. | srom_post.lua |
| 11 | ✔ A title inside an italic title is set roman (reverse italics) — flagged for checking. | srom_post.lua |
| 12 | ✔ Hyperlinks become plain text; URLs stay as text (InDesign can hyperlink them later). | srom_post.lua |
| 13 | ✔ Non-breaking spaces never stored in the text; stray nbsp → plain space (the template's GREP style is the only source, §3.3). | normalize.py |
| 14 | ✔ Multi-paragraph footnotes allowed, flagged. | srom_post.lua |
| 15 | ✔ Comments `<!-- … -->` never print and never block anything; in the Word working copy they are ordinary Word comments, handled by the editor, dropped and listed on import. | build.py, export_work.py, docx_in.py |
| 16 | ✔ Missing bibliographic data is printed as `[BRAK MIEJSCA]`, `[BRAK ROKU]`, `[BRAK WYDAWCY]` and blocks the build (§0) unless `--draft`. | srom.csl, build.py |
| 17 | ✔ Verse quotations keep their line breaks (own style, `quote_verse`); interlinear examples (§5.3) are typed in a `::: przyklad` fenced block and become three styled lines with real tabs; tables get cell/title/source styles, formatting from the template's table style. | srom_post.lua, build.py |
| 18 | ✔ `@key` (author in text) and `[-@key]` (author suppressed) are forbidden: pandoc would print the first citation without its author. | srom_post.lua, check.py |
| 19 | ✔ The author's own reference list is taken out of the text on import (`_bib.txt`); SROM prints only the bibliography generated from refs.json plus literal sections I–III. | docx_in.py, pdf_extract.py |
| 20 | ○ Translation handoff (`handoff.md`): the translator's notes `[^t<n>]` … `– przyp. tłum.` and the title note are outside the handoff check; an added citation passes only when declared (`<!-- DODANO: @key -->`); after translation the editor's Word working copy is the master. | check.py, export_work.py, docx_in.py |
| 21 | ○ House style v2 (`style-sheet.md`): one root style *Podstawa* (Cambria 10.5/13, Polish, baseline grid, non-breaking-space GREP styles — **missing from both current templates**), nine groups; speakers and affiliations roman, not italic (kanon: no italics for proper names); motto italic, indented 30 mm; dialogue = block-quote measure, "Name:" bold via character style, turns without space between; transcript speaker on its own line, bold. | style_spec.json |
| 22 | ○ Additions by the translation are declared by `"srom-added"` in `<id>_refs_tlum.json` (survives Word); `DODANO` comments still accepted. | check.py, cite_map.py |
