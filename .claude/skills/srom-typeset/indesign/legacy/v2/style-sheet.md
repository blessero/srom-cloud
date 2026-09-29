# SROM — arkusz stylów (house style v2)

Generated from `indesign/style_spec.json` by `scripts/make_style_setup.py`; do not edit by hand. Values in pt; only what
differs from the parent style is listed (inheritance does the rest). SROM house style — single source for srom_style_setup.jsx, config/styles.json and references/style-sheet.md. Units: pt. Page 165×235 mm, text measure 126 mm (357 pt), body 10.5/13 on a 13 pt baseline grid.

**Podstawa** (root of every text style): krój Cambria; odmiana Regular; stopień 10.5; interlinia 13; język Polish; wyrównanie LEFT_JUSTIFIED; dzielenie tak; wcięcie 1. wiersza 0; wcięcie lewe 0; rightIndent 0; odstęp przed 0; odstęp po 0; siatka ALIGN_TO_BASELINE.

GREP styles in Podstawa (inherited by all text styles) — character style *Bez podziału*:

- `(?<=\b\w)\h` — after one-letter words (w, z, i, a, o, u)
- `(?<=\b(?:s|t|z|nr|r|w|k|sygn|ks|św|dr|prof|im|ul|pl|al|tzw|tj|np|zob|por|ok|ss)\.)\h` — after s. t. z. nr r. w. sygn. k. and common abbreviations
- `(?<=\b\u\.)\h(?=\u)` — between initials and surname (J. Ficowski)
- `\h(?=%)` — before %
- `(?<=\d)\h(?=\d{3}\b)` — thousands (13 000)
- `\h(?=–)` — a spaced dash never starts a line

## 1 Czołówka

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Tytuł artykułu** | Podstawa | odmiana Bold; stopień 18; interlinia 22; wyrównanie LEFT_ALIGN; dzielenie nie; światło -10; siatka NONE; odstęp po 13 | Rozdzial |  |
| **Autor** | Podstawa | odmiana Bold; stopień 13; interlinia 16; wyrównanie LEFT_ALIGN; dzielenie nie; siatka NONE | Autor |  |
| **Afiliacja** | Podstawa | wyrównanie LEFT_ALIGN; dzielenie nie; siatka NONE; odstęp po 13 | — | roman: kanon — no italics for proper names |
| **Abstrakt – nagłówek** | Podstawa | stopień 10; wersaliki ALL_CAPS; światło 50; wyrównanie LEFT_ALIGN; dzielenie nie; siatka NONE; odstęp przed 13 | Abstrakt tytul |  |
| **Abstrakt** | Podstawa | stopień 10; interlinia 12.5; siatka NONE | Abstrakt, Abstrakt ang |  |
| **Słowa kluczowe** | Abstrakt | odstęp przed 6.5 | — |  |

## 2 Tekst

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Tekst** | Podstawa | wcięcie 1. wiersza 11.34 | Tekst |  |
| **Tekst bez wcięcia** | Tekst | wcięcie 1. wiersza 0 | Bez wciecia |  |
| **Tekst – inicjał** | Tekst bez wcięcia | inicjał (znaki) 1; inicjał (wiersze) 2 | Inicjal |  |
| **Śródtytuł 1** | Podstawa | odmiana Bold; wersaliki ALL_CAPS; wyrównanie LEFT_ALIGN; dzielenie nie; odstęp przed 13; z następnym (wiersze) 2 | Podrozdzial |  |
| **Śródtytuł 2** | Podstawa | odmiana Bold; wyrównanie LEFT_ALIGN; dzielenie nie; odstęp przed 13; z następnym (wiersze) 2 | Podrozdział SECONDARY |  |
| **Wyliczenie** | Tekst bez wcięcia | wcięcie lewe 11.34; wcięcie 1. wiersza -11.34; punktor – | Punktury | en-dash bullet from the style; items typed without a dash |
| **Wyliczenie numerowane** | Tekst bez wcięcia | wcięcie lewe 11.34; wcięcie 1. wiersza -11.34 | — | number typed as 1. + tab |

## 3 Cytaty

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Cytat blokowy** | Podstawa | stopień 9.5; interlinia 12; wcięcie lewe 28.35; odstęp przed 6.5; odstęp po 6.5; odstęp w obrębie stylu 0; siatka NONE | Cytat blokowy, Cytat_blokowy |  |
| **Cytat – wiersz** | Cytat blokowy | wyrównanie LEFT_ALIGN; dzielenie nie | — | verse: line breaks kept |
| **Motto** | Cytat blokowy | odmiana Italic; wcięcie lewe 85.04; wyrównanie LEFT_ALIGN; dzielenie nie; odstęp przed 0; odstęp po 13 | — | opening quotation; titles inside it set roman |
| **Motto – źródło** | Motto | odmiana Regular; stopień 9; wyrównanie RIGHT_ALIGN; odstęp po 13 | — |  |
| **Dialog** | Cytat blokowy | wyrównanie LEFT_JUSTIFIED | — | one turn per paragraph, speaker label 'Name:' in character style Mówca; turns without space between them |

## 4 Rozmowa

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Mówca** | Podstawa | odmiana Bold; wyrównanie LEFT_ALIGN; dzielenie nie; odstęp przed 13; z następnym (wiersze) 2 | Panelant | speaker's own line in a transcript; roman bold, not italic (kanon: proper names) |
| **Mówca – afiliacja** | Podstawa | stopień 9; wyrównanie LEFT_ALIGN; dzielenie nie; z następnym (wiersze) 1 | Uni |  |

## 5 Aparat

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Podpis** | Podstawa | stopień 9; interlinia 10.8; wyrównanie CENTER_JUSTIFIED; dzielenie nie; siatka NONE | Podpisy, Podpisy BLACK |  |
| **Tabela – tytuł** | Podpis | odmiana Bold; wyrównanie CENTER_ALIGN; odstęp po 2.83 | Tytuł tabeli |  |
| **Tabela – treść** | Podpis | wyrównanie LEFT_ALIGN | — |  |
| **Tabela – źródło** | Podpis | stopień 8.5; wyrównanie LEFT_ALIGN; odstęp przed 2.83 | — |  |
| **Przykład – forma** | Cytat blokowy | odmiana Italic; wyrównanie LEFT_ALIGN; dzielenie nie; odstęp po 0 | — |  |
| **Przykład – glosa** | Przykład – forma | odmiana Regular; odstęp przed 0 | — |  |
| **Przykład – przekład** | Przykład – glosa | odstęp po 6.5 | — |  |

## 6 Bibliografia

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Bibliografia – tytuł** | Śródtytuł 1 | — | — |  |
| **Bibliografia – dział** | Śródtytuł 2 | — | — |  |
| **Bibliografia** | Podstawa | stopień 10; wcięcie lewe 11.34; wcięcie 1. wiersza -11.34 | Literatura |  |
| **Nota o autorze** | Podstawa | stopień 9; interlinia 11; siatka NONE; odstęp przed 13 | — |  |

## 7 Przypisy

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Przypis** | (bez zmian) | bez zmian | Przypis | footnotes: definition left as it is (handled separately) |
| **Przypis gwiazdkowy** | Przypis | — | Przypis do tytułu | non-author notes — title note, przyp. tłum., przyp. red. — one asterisk series *, **, … per page, set by hand ABOVE the numbered notes (kanon § 7.1); same values as Przypis |

## 8 Strona

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Pagina** | Podstawa | stopień 8; wyrównanie LEFT_ALIGN; dzielenie nie; siatka NONE | — | running head (now [Basic Paragraph] + overrides on the masters) |
| **Folio** | Pagina | wyrównanie RIGHT_ALIGN | Folio |  |

## 9 Spis treści

| styl | na bazie | wartości (różnice) | zastępuje | uwagi |
|---|---|---|---|---|
| **Spis treści** | Podstawa | wcięcie lewe 19.84; wyrównanie RIGHT_ALIGN; siatka NONE | Spis_tresci |  |
| **Spis treści – autor** | Spis treści | odmiana Italic; wcięcie lewe 0; wyrównanie LEFT_ALIGN; odstęp przed 7.09; odstęp po 1.42 | tresci_autor |  |
| **Spis treści – języki** | Spis treści | stopień 9; interlinia 10; wyrównanie LEFT_ALIGN; odstęp przed 2.83 | spis tresci - jezyki |  |

## Style znakowe

| styl | wartości | zastępuje | uwagi |
|---|---|---|---|
| **Kursywa** | odmiana Italic | — |  |
| **Proste** | odmiana Regular | — | roman inside an italic paragraph (titles in a motto) |
| **Kapitaliki** | wersaliki SMALL_CAPS | — | surnames in the bibliography (typed in normal case) |
| **Kapitaliki – glosa** | wersaliki CAP_TO_SMALL_CAP | — | gloss categories 1SG.NOM (typed in capitals); applied by GREP |
| **Mówca – etykieta** | odmiana Bold | — | speaker label in a dialogue; applied by the build (Word forbids one name for a paragraph and a character style) |
| **Bez podziału** | noBreak tak | NO BREAK | non-breaking spaces (kanon §3.3); applied by GREP |
| **Odsyłacz gwiazdkowy** | położenie SUPERSCRIPT | — | asterisk marker of a non-author note in the text (kanon § 7.1); the build types one * — set the count per page |

Bez zmian (przypisy): Indeks gorny, Footnote reference.

## Usuwane (pozostałości importów z Worda) → zastępowane stylem Tekst

Normalny, Normal, Tekst przypisu dolnego, Znak, Tekst przypisu dolnego, footnote text, Normalny (Web), Tekst przypisu końcowego, Bez odstępów, sdendnote, Footnote text, Footnote, Normal_wrd_1, Footnote text_wrd_1, Endnote text, Średnie cieniowanie 1 — akcent 1, Standard, Text body, Heading 1, Normal (Web), Body Text, Footnote Text; znakowe: Panelant, Style list zaimportowanych z dokumentu Worda lub pliku RTF:Styl listy importowanych słów1.
