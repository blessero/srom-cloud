# SROM — arkusz stylów (v3)

Generated from `indesign/style_spec.json` by `scripts/make_style_setup.py`; do not edit by hand. Values in pt (mm where it
helps); each style lists only what differs from the style it is based on. The values are vol. 18's own (templates 03_Ellis and
09_Konferencja, read in InDesign); deliberate changes are listed under each style.

## Dokument

- Siatka bazowa: co 13.2945 pt od 62.362 pt (22 mm) od góry strony — jak w 18 tomach.
- Przypisy (Footnote Options): styl *Przypis*; numer w tekście w indeksie górnym (58 % / 33 %); po numerze w przypisie kropka + półfiret; 14.17 pt nad pierwszym przypisem; linia 0.5 pt × 40 mm; numeracja od nowa w każdej sekcji; długi przypis może przejść na następną stronę.
- Kapitaliki 70 %. [Basic Paragraph]: Cambria, polski.

**Tekst** (podstawa wszystkich stylów): krój Cambria; odmiana Regular; stopień 10.5; interlinia 13; światło 0; język Polish; składacz Adobe World-Ready Paragraph Composer; wyrównanie justowanie; wcięcie akapitowe 11.34 (4.0 mm); siatka tak; dzielenie tak; odstęp liter (pożądany) -1.

Justowanie i dzielenie Tekstu (dziedziczą je wszystkie style, o ile nie zmieniają): autoLeading 120; kerningMethod Optical; wcięcie z lewej 0; rightIndent 0; odstęp przed 0; odstęp po 0; hyphenateAfterFirst 3; hyphenateBeforeLast 3; hyphenateCapitalizedWords nie; hyphenateLadderLimit 2; hyphenateWordsLongerThan 6; hyphenationZone 21.25; minimumWordSpacing 85; desiredWordSpacing 100; maximumWordSpacing 115; minimumLetterSpacing -3; maximumLetterSpacing 1; minimumGlyphScaling 98; desiredGlyphScaling 100; maximumGlyphScaling 102; diacriticPosition OPENTYPE_POSITION.

Style GREP w Tekście (dziedziczone) — styl znakowy *Bez podziału*:

- `(?i)\b[aiouwz]\s` — one-letter words a i o u w z (the vol. 18 rule, unchanged)
- `(?<=\b(?:s|t|z|nr|r|w|k|sygn|ks|św|dr|prof|im|ul|pl|al|tzw|tj|np|zob|por|ok|ss)\.)\h` — after s. t. z. nr r. w. sygn. k. and common abbreviations (kanon § 3.3)
- `(?<=\b\u\.)\h(?=\u)` — between initials and surname: J. Ficowski (kanon § 3.3)
- `\h(?=%)` — before % (kanon § 3.3)
- `(?<=\d)\h(?=\d{3}\b)` — thousands: 13 000 (kanon § 3.3)
- `\h(?=–)` — a spaced dash never starts a line (kanon § 3.3)

## Na wierzchu (zestaw roboczy, od najczęstszych)

| styl | na bazie | wartości (różnice) | zastępuje (tom 18) | uwagi |
|---|---|---|---|---|
| **Tekst BEZ WCIĘCIA** | Tekst | wcięcie akapitowe 0 | Bez wciecia, Abstrakt, Abstrakt ang | first paragraph after a heading, motto or speaker line; abstract and summary text (as Ellis) |
| **Przypis** | Tekst | stopień 9; interlinia 10.8; wcięcie akapitowe 0; siatka nie; inicjał (znaki) 1; inicjał (wiersze) 1; styl zagnieżdżony *Indeks górny* przez inicjał | Przypis, Tekst przypisu dolnego, Tekst przypisu dolnego, Znak, footnote text, Footnote text, Footnote Text, Footnote, Footnote text_wrd_1, Tekst przypisu końcowego, Endnote text, sdendnote | footnotes, 9/10.8, not on the grid (a grid-aligned note would get 13.29 pt lines). The 1-line drop cap + nested style set the note number superscript — kept from vol. 18. |
| **Śródtytuł** | Tekst | odmiana Bold; wersaliki tak; składacz Adobe World-Ready Single-line Composer; wyrównanie do lewej; wcięcie akapitowe 0; dzielenie nie | Podrozdzial, Heading 1, Abstrakt tytul | section heading: 10.5 bold capitals, left, no hyphenation (= vol. 18 'Podrozdzial'); also the bibliography title |
| **Śródtytuł MAŁE** | Śródtytuł | wersaliki nie | Podrozdział SECONDARY | second-level heading and bibliography divisions: Śródtytuł without capitals **Zmiana:** replaces the unused 'Podrozdział SECONDARY' (11 pt, tracking −10, default H&J) — now Śródtytuł in lower case. |
| **Cytat** | Tekst | stopień 9; interlinia 10.8; wcięcie akapitowe 0; wcięcie z lewej 28.35 (10.0 mm) | Cytat blokowy, Cytat_blokowy | block quotation and dialogue: 9 pt, indent 1 cm, on the grid, the H&J of Tekst **Zmiana:** leading 12 → 10.8 (= Przypis; prints the same, the grid sets the line). **Zmiana:** Ellis: 9 pt with default H&J and tracking −10 → Tekst's H&J, tracking 0 (MB 29.09.2026); Konferencja: 9.5 → 9 pt. |
| **Bibliografia** | Tekst | stopień 10; wcięcie akapitowe -11.34 (-4.0 mm); wcięcie z lewej 11.34 (4.0 mm) | Literatura | bibliography entry: 10 pt on the grid, hanging indent = the paragraph indent (4 mm) |
| **Podpis** | Tekst | stopień 9; interlinia 10.8; wyrównanie justowanie, ostatni wiersz do środka; wcięcie akapitowe 0; siatka nie; dzielenie nie | Podpisy, Podpisy BLACK | caption (also the source line under a table) **Zmiana:** based on Tekst instead of Przypis (same values; drops the inherited drop cap). |
| **Podpis LINIA** | Podpis | linia pod tak; grubość linii 0.4; odsunięcie linii 9.92 (3.5 mm) | Podpisy (z linią) | caption with the 0.4 pt rule below (as Ellis) |
| **Wyliczenie** | Tekst | wcięcie akapitowe -11.34 (-4.0 mm); wcięcie z lewej 11.34 (4.0 mm) | Punktury | list item; the marker is typed ('–' or '1.' + tab), the tab stops at the hanging indent (4 mm = the paragraph indent) **Zmiana:** replaces the unused 'Punktury' (Word auto-numbering); one style for bulleted and numbered lists. |
| **Tytuł** | Tekst | odmiana Bold; stopień 18; interlinia 21.6; światło -10; wyrównanie do lewej; wcięcie akapitowe 0; siatka nie; dzielenie nie; odstęp liter (pożądany) 0 | Rozdzial | article title, 18/21.6 bold **Zmiana:** leading Auto → 21.6 (the same value, written out). **Zmiana:** based on Tekst instead of 'Normalny'. |
| **Autor** | Tekst | odmiana Bold; stopień 13; interlinia 14; wyrównanie do lewej; wcięcie akapitowe 0; siatka nie; dzielenie nie; ruleAbove tak; ruleAboveLineWeight 0; ruleAboveOffset 45.35; keepRuleAboveInFrame tak | Autor | author's name above the title. The 0 pt rule above, offset 16 mm, is the first-page sink: it pushes the title block down (space before is ignored at the top of a frame) — keep it **Zmiana:** left-aligned, no hyphenation (was justified: the same for a one-line name). |
| **Afiliacja** | Tekst BEZ WCIĘCIA | odmiana Italic; siatka nie | Uni | affiliation under the author's or the speaker's name: 10.5/13 italic, off the grid (= vol. 18 'Uni'). NB kanon § 3.4 sets proper names roman — for MB |
| **Mówca** | Tekst BEZ WCIĘCIA | odmiana Bold Italic; wcięcie z lewej 2.83 (1.0 mm); punktor „>” + tab; tabulator 9.92 pt | Panelant | speaker's own line in a transcript: '> Name', bold italic (= vol. 18 'Panelant'). NB kanon § 3.4 — for MB |
| **Tekst INICJAŁ** | Tekst BEZ WCIĘCIA | inicjał (znaki) 1; inicjał (wiersze) 2 | Inicjal | opening paragraph with a two-line drop cap (by hand) |

## Folder „Rzadkie”

| styl | na bazie | wartości (różnice) | zastępuje (tom 18) | uwagi |
|---|---|---|---|---|
| **Motto** | Cytat | odmiana Italic | — | opening quotation = Cytat in italics (as Ellis); a title inside it in Proste |
| **Motto ŹRÓDŁO** | Cytat | wyrównanie do prawej; dzielenie nie | — | source line under the motto, roman, right |
| **Cytat WIERSZ** | Cytat | wyrównanie do lewej; dzielenie nie | — | verse: lines kept (a justified line before a forced break would stretch) |
| **Przypis GWIAZDKOWY** | Przypis | inicjał (znaki) 0; inicjał (wiersze) 0; GREP `^\*+` → *Indeks górny* | — | title note, translator's and editorial notes (one * series per page, above the numbered notes, kanon § 7.1); = Przypis |
| **Tabela TYTUŁ** | Tekst | odmiana Bold; stopień 9; interlinia 10.8; wyrównanie do środka; wcięcie akapitowe 0; odstęp po 2.83 (1.0 mm) | Tytuł tabeli | table title, 9 bold centred, on the grid **Zmiana:** leading 13 → 10.8 (prints the same on the grid). |
| **Tabela TREŚĆ** | Podpis | wyrównanie do lewej | — | table cell: the caption's 9/10.8, left |
| **Przykład FORMA** | Cytat | odmiana Italic; wyrównanie do lewej; dzielenie nie | — | interlinear example (kanon § 5.3), line 1: the form, italic; columns by tabs |
| **Przykład GLOSA** | Przykład FORMA | odmiana Regular; GREP `(?<!\l)\u{2,}(?!\l)` → *Kapitaliki GLOSA* | — | line 2: morpheme gloss, categories in small caps |
| **Przykład PRZEKŁAD** | Przykład FORMA | odmiana Regular | — | line 3: translation in ‘ ’ |

## Folder „Numer”

| styl | na bazie | wartości (różnice) | zastępuje (tom 18) | uwagi |
|---|---|---|---|---|
| **Pagina** | Tekst | stopień 8; interlinia 9.6; światło -10; wyrównanie od grzbietu; wcięcie akapitowe 0; siatka nie; dzielenie nie; odstęp liter (pożądany) 0 | Folio | running head (author – title; Studia Romologica 18/2025): 8 pt, tracking −10, aligned away from the spine, so one style serves both pages **Zmiana:** vol. 18: [Basic Paragraph] + local overrides on the masters; the unused 'Folio' had these values. |
| **Folio** | Pagina | stopień 9; interlinia 10.8; światło 0 | — | page number: 9 pt, away from the spine **Zmiana:** vol. 18: [Basic Paragraph] + 9 pt override on the masters. |
| **Spis treści** | Tekst | wyrównanie do prawej; wcięcie akapitowe 0; wcięcie z lewej 19.84 (7.0 mm); siatka nie; tabulator 337.32 pt z kropkami | Spis_tresci | contents: title … page |
| **Spis AUTOR** | Spis treści | odmiana Italic; światło -10; wyrównanie do lewej; wcięcie z lewej 0; odstęp przed 7.09 (2.5 mm); odstęp po 1.42; odstęp liter (pożądany) 0 | tresci_autor | contents: author line |
| **Spis JĘZYKI** | Spis treści | stopień 9; interlinia 10; wyrównanie do lewej; odstęp przed 2.83 (1.0 mm) | spis tresci - jezyki | contents: other-language titles |

Zmiany w Tekście: based on nothing instead of 'Normalny' (same values, one style fewer); five GREP rules of kanon § 3.3 added to the vol. 18 one.

## Style znakowe

| styl | wartości | zastępuje | uwagi |
|---|---|---|---|
| **Kursywa** | odmiana Italic | — | italics (the DOCX carries no local formatting) |
| **Kapitaliki** | wersaliki kapitaliki | — | surnames in the bibliography, typed in normal case (kanon § 9.3) |
| **Indeks górny** | położenie indeks górny | Indeks gorny, Footnote reference | footnote number in the note (nested style of Przypis); any superscript by hand |
| **Bez podziału** | bez podziału tak; język Polish | NO BREAK | non-breaking spaces (kanon § 3.3); applied by the GREP styles of Tekst |
| **Proste** | odmiana Regular | — | roman inside an italic paragraph (a title inside the motto) |
| **Pogrubienie** | odmiana Bold | — | speaker label 'Name:' in a dialogue (applied by the build) |
| **Gwiazdka** | położenie indeks górny | — | asterisk marker of a non-author note in the text (kanon § 7.1); the build types one * — the count per page is set by hand (_gwiazdki.jsx) |
| **Kapitaliki GLOSA** | wersaliki wersaliki → kapitaliki | — | gloss categories 1SG.NOM, typed in capitals; applied by GREP in Przykład GLOSA |

## Porządki (skrypt)

Skrypt usuwa **wszystkie** dotychczasowe style akapitowe i znakowe dokumentu. Tekst w starym stylu dostaje nowy według kolumny
„zastępuje”; nieznane style akapitowe → *Tekst*, znakowe → brak stylu. Wbudowane [Basic Paragraph] i [None] zostają.
