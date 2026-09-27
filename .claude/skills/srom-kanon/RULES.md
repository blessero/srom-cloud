# SROM RULES — English digest of the Kanon (v1.6)

Normative text: `references/kanon-redakcyjny.md` — *Kanon edytorski Studia Romologica* (Polish, internal), in this skill. This file is its compact English digest; **section numbers are the Kanon's**. If the two differ, the Kanon governs and this file is corrected. New rules go into the Kanon first (with a § 17 entry), then here.

The journal publishes **in Polish only**. English exists only in metadata (title, abstract, keywords) and, if the bilingual model is used, in an English online version (§ 12.1).

---

## 0. Integrity

Missing year/page/publisher, illegible or ambiguous element → **stop, flag, ask**. Never reconstruct. In the working file the gap is marked `[BRAK MIEJSCA]` / `[BRAK ROKU]` / `[BRAK WYDAWCY]`; a text with a marker does not go to typesetting. `b.m.` / `b.r.` only when the source itself lacks the element.

## 1. Front matter

Author · affiliation (or `badacz niezależny, [town]`) · **ORCID** · title PL · title EN · title RMN (optional) · abstract PL ≤1000 chars · abstract EN (translation of the PL) · keywords 5–10 PL+EN, `;`-separated, group names in authority form · body · bibliography · author note ≤500 chars. Editorial: DOI, dates, licence, volume, pages. Translated articles: EN title/abstract/keywords are the original's (§ 12.2.2).

## 2. Body

Two heading levels: `1. CAPS`, `1.2. Bold roman`; no unnumbered headings. First-line indent; **none after a heading; always after a block quote.** No paragraph spacing.

**Lists.** Unnumbered (no in-text reference to an item's number) → en-dash bullets, lowercase, semicolons, final period. Numbered (text refers to an item by number, or sequence/count matters) → arabic `1.` `2.` `3.` (never `1)`), lowercase, semicolons, final period.

## 3. Typography

Quotes `„ ”`, inner `» «`; glosses `‘ ’` (§ 3.1). `–` unspaced for ranges, spaced for dashes; **no em dash** (§ 3.2). Single-character `…`; omissions `[…]`.
**Non-breaking spaces** (after `s. t. z. nr r. w. sygn. k.`, initials, one-letter words; before `%`) are applied by the typesetter's GREP style — never typed by the editor and never stored in the text; a stray one is replaced by a plain space (§ 3.3).
Italics: titles; foreign/Romani common nouns. **Never: proper names** — except foreign exonyms not assimilated in Polish (*Ciganos*, *Gitanos*, *Bohémiens*, *Zigeuner*, *Tsiganes*): foreign words, italic every time, also when the word itself is discussed; endonyms (Calon, Sinti) and assimilated exonyms (Cyganie, Bosza) roman. A title inside an italic title is set roman (reverse italics). Small caps: bibliography surnames and gloss categories only. No bold, letter-spacing, underline or caps in running text (§ 3.4).
Breaks: no widows/orphans, no one-letter word at line end, no split surnames/abbreviations/dates/signatures; URLs break only after a slash or before a dot (§ 3.6).

### 3.5. Dates and numbers

| | Body | Apparatus |
|---|---|---|
| year | `w 1943 roku` | `1943 r.` |
| century | `w XX wieku` | `XX w.` |
| decade | `w latach 20. XX wieku` | `lata 20. XX w.` |
| month+year | `w marcu 1943 roku` | `03.1943` |
| full date | `12 marca 1943 roku` | `12.03.1943` |
| access | — | `[dostęp: 18.03.2025]` |

Apparatus dates `dd.mm.rrrr`, zero-padded, **no `r.` after a numeric date.** Exception: titles of legal acts and rulings keep official wording (`Ustawa z dnia 6 stycznia 2005 r.`). Centuries roman; everything else arabic (`wyd. 3`, `t. 2`, `z. 2`). Page ranges in full.

## 4. Quotations and foreign material

≤3 lines inline in quotes; longer as unquoted block; verse quotations keep their line breaks (§ 4.1). **Foreign quotes translated in body**; original in a note only if the wording is analysed. `[tłum. własne]` once — not in translated articles (§ 4.2, § 12.2.4 d).

> Translate what the reader must understand; keep the original for what the reader must be able to find. (§ 4.3)

| Element | Primary | Secondary |
|---|---|---|
| Title in notes/bibliography | original (Cyrillic → ALA-LC) | translation optional, **`[square brackets]` directly after the title** |
| Title mentioned in body | original italic (Cyrillic → Polish transcription) | Polish rendering (round brackets), first mention |
| Work with a Polish edition | Polish edition's title | original in brackets |
| Journal, archive, fonds, unit | original | never translated |
| Institution, Latin script | original | Polish gloss in brackets, first mention |
| Institution, Cyrillic | **body: Polish transcription of the original name** — no Polish equivalents | author may describe it in own words |
| Legal act | original | Polish translation in brackets |
| Term | Polish equivalent | original italic in brackets |

Examples: `N. Demeter, *Istoriia tsygan* [Historia Cyganów], Nauka, Moskva 2018, s. 5.` · body: *…(obecnie Archiw Wnieszniej Politiki Rossijskoj Impierii)…* · note: `Arkhiv vneshneĭ politiki Rossiĭskoĭ imperii (dalej: AVPRI)` — the abbreviation may be used in the body and bridges both forms.

## 5. Romani terms, glosses, linguistic examples

Common nouns italic on first use (§ 5.1). Gloss: `rom. *kris* ‘sąd’` (§ 5.2). Glossed examples: three lines — form italic, morpheme gloss with small-caps categories aligned, translation in `‘ ’`; Leipzig rules; Cyrillic forms in ALA-LC (§ 5.3).

## 6. Ethnonyms, group names, authority file

`Rom/Romowie/Romka` capitalised, `romski` lowercase. `Cyganie` capitalised, only in quotes/titles, historical source category, or self-identification, with a note on first use. `Porajmos`, `Samudaripen`, `Zagłada` capitalised (§ 6.1).
**Author chooses spelling of group names**; consistent within the article; roman, never italic (§ 6.2), except foreign exonyms (§ 3.4). Authority file: author's form in text; standard form in index/keywords/deposit; see-references from variants, kept in `references/kartoteka.tsv` (column `italic_house` marks the foreign exonyms); translated articles use the standard form in the text (§ 6.3, § 12.2.6).

## 7. Footnotes

### 7.1. Marker and note series
Superscript arabic, continuous, foot of page. Marker **before the period, comma, semicolon and colon**, after closing quote/bracket; after an abbreviation's own period (`XV w.³`).
**Non-author notes** — title note, translator's notes (ending `– przyp. tłum.`), editorial notes (`– przyp. red.`) — are **one separate series** marked `*`, `**`, `***` …, restarting on every page; on the first page the title note takes the first `*`. They stand **above** the numbered notes, same size and face. Continuous numbering covers the author's notes only.
**Author-date conversion:** parenthetical `(A 1985)` → marker in its place; narrative `Ficowski (1985) twierdzi` → marker right after the name; page-only `(s. 21)` → citation of the work cited just before; `Name (year)` where the name is no cited author (`w Warszawie (1920)`) stays.

### 7.2. First citation
**Journal rule:** title, **comma**, year, volume, issue/number — all comma-separated — **page last.**

| Type | Pattern |
|---|---|
| Book | `J. Ficowski, *Cyganie na polskich drogach*, Wydawnictwo Literackie, Kraków 1985, s. 15.` |
| 2–3 | `L. Mróz, A. Bartosz, *Tytuł*, Wydawnictwo, Warszawa 1998, s. 40–42.` |
| 4+ | `K. Fiałkowska i in., *Tytuł*, Wydawnictwo, Warszawa 2020, s. 12.` |
| Edited vol. | `A. Kowalski (red.), *Tytuł tomu*, Wydawnictwo, Kraków 2011, s. 88.` |
| Chapter | `L. Mróz, *Tytuł rozdziału*, w: *Tytuł tomu*, red. A. Kowalski, Wydawnictwo, Kraków 2011, s. 88–104.` |
| Article | `M. Kołaczek, *Tytuł*, „Studia Romologica”, 2012, nr 5, s. 217.` |
| Article vol+issue | `S. Płoski, *Tytuł*, „Dzieje Najnowsze”, 1947, t. 1, z. 2, s. 310.` |
| Translation | `I. Hancock, *Tytuł*, tłum. J. Nowak, Wydawnictwo, Warszawa 2007, s. 33.` |
| Edition | `A. Bartosz, *Tytuł*, wyd. 3 popr., Wydawnictwo, Tarnów 2019, s. 51.` |
| Multivolume | `A. Kowalski, *Tytuł*, t. 2: *Tytuł tomu*, …, s. 77.` |
| Foreign imprint | `A. Marsh, *Ethnicity and Identity*, w: *We are Here*, red. E. Uzpeder, EDROM, Istanbul 2008, s. 21.` |
| Unpublished | `J. Kopańska, *Tytuł*, Uniwersytet Jagielloński, Kraków 2018, s. 60 (maszynopis pracy doktorskiej, egzemplarz przechowywany w Bibliotece Jagiellońskiej).` |

Initial + surname (`R.L. Turner`). Publisher before place; no comma between place and year. **Imprint place as on title page, not Polonised**; Cyrillic imprints in ALA-LC (Polish exonyms stay in body prose). Publishers in original. Labels always Polish. `w:` unbracketed. Editor before title for whole volumes, after for chapters. **Physical-form/location notes in round brackets at the very end.**
**Locator:** always when a specific place is cited, without exception for a quotation. A reference to the work as a whole has no page (and no article page range — the bibliography has it); the editor confirms each; a quotation without a page is a query to the author.

### 7.3. Subsequent citations
`Ficowski, *Cyganie na polskich drogach…*, s. 51.` Short title fixed once; `…` when truncated, a short enough title given in full without `…`. Multi-author: `Mróz, Bartosz, *Tytuł…*`; 4+ `Fiałkowska i in., *Tytuł…*`; edited volume: editor's surname, no `(red.)`.
`*Ibidem*, s. 52.` only if the immediately preceding note cites the same work **and stands in the same column** (checked after layout). Never inside a sentence; never when this or the preceding note also cites a non-bibliographic source (archival unit, press issue, legal act); never in a non-author note, nor in the author's note right after one — short form instead.
**Forbidden:** `op. cit.` `dz. cyt.` `idem` `eadem` `tenże` `taż` `tamże` `loc. cit.` `passim` (as locator), year letters (`2012a`).

### 7.4. Substantive notes
Welcome: `Zob.`, `Por.`, `Szerzej zob.`, `Inaczej:`. A note may have more than one paragraph.

## 8. Special sources

**8.1 Archives A — Polish/Western descriptive:** `Archiwum Narodowe w Krakowie (dalej: ANK), zespół 29/456: Starostwo Powiatowe w Tarnowie, sygn. 12, k. 34v, Pismo …, 04.03.1937.` → `ANK, 29/456, sygn. 12, k. 41.`
**Archives B — post-Soviet:** name in ALA-LC + abbreviation; Russia `f. op. d. l.` (verso `ob.`); Ukraine/Belarus `f. op. spr. ark.` (verso `zv.`). `Arkhiv vneshneĭ politiki Rossiĭskoĭ imperii (dalej: AVPRI), f. 151, op. 482, d. 1234, l. 15 ob.`
**Archives C — coded:** `United States Holocaust Memorial Museum (dalej: USHMM), RG-25.004M, rolka 12.`
Archive names never translated.

**8.2 Fieldwork:** codes `W` `FN` `N` `K`. `Wywiad W12 (mężczyzna, ur. 1951, Polska Roma), Tarnów, 14.06.2019, rozmowa w jęz. polskim i romani; nagranie w Archiwum MET, sygn. AT/W/12.` → `Wywiad W12.` · `FN, Nowy Sącz, 03.08.2018.` Metryczka: sex, birth year/decade, group, town, date, language, deposit — **no occupation/function/kinship if identifying**; editor's call, recorded. First note: period, location, ethical basis.

**8.3 Press:** `J. Nowak, *Tytuł*, „Gazeta Krakowska”, 1963, nr 145, s. 3.` · unnumbered: `„Czas”, 03.05.1928, s. 2`.
**8.4 Legal (official wording):** `Ustawa z dnia 6 stycznia 2005 r. …, Dz.U. 2005 nr 17 poz. 141, art. 20.` · `Wyrok TK z dnia 8 listopada 2016 r., sygn. akt P 126/15.`
**8.6 Web:** `A. Kowalski, *Tytuł tekstu*, w: *Nazwa serwisu*, https://… [dostęp: 18.03.2025].` DOI replaces URL and access date. URLs are plain text in the typesetting file, never hyperlinks.
**8.7 AV:** `*Papusza*, reż. J. Kos-Krauze, K. Krauze, Polska 2013, 00:42:15.` · `*Tytuł nagrania*, nagranie audio, 1978 r., Archiwum MET, sygn. AT/N/45.`

## 9. Bibliography

Same construction as the note, four differences only: **`Surname, Given-name.`** (small caps at typesetting, full given names); all authors; full page range; DOI/ISBN. No colon after place (§ 9.1).

| Type | Pattern |
|---|---|
| Book | `Ficowski, Jerzy. *Cyganie na polskich drogach*, Wydawnictwo Literackie, Kraków 1985.` |
| 2–3 | `Mróz, Lech, Bartosz, Adam. *Tytuł*, Wydawnictwo, Warszawa 1998.` |
| 4+ | `Fiałkowska, Kamila, Garapich, Michał P., Mirga-Wójtowicz, Elżbieta, Kowalski, Jan. *Tytuł*, …` |
| Edited | `Kowalski, Andrzej (red.). *Tytuł tomu*, Wydawnictwo, Kraków 2011.` |
| Chapter | `Mróz, Lech. *Tytuł rozdziału*, w: *Tytuł tomu*, red. A. Kowalski, Wydawnictwo, Kraków 2011, s. 88–104.` |
| Article | `Kołaczek, Małgorzata. *Tytuł*, „Studia Romologica”, 2012, nr 5, s. 211–228. DOI: 10.1234/srom.2012.5.11.` |
| Cyrillic | `Demeter, Nadezhda. *Istoriia tsygan*, Nauka, Moskva 2018.` |
| Unpublished | `Kopańska, Joanna. *Tytuł*, Uniwersytet Jagielloński, Kraków 2018 (maszynopis pracy doktorskiej, egzemplarz przechowywany w Bibliotece Jagiellońskiej).` |
| Informant | `W12 – mężczyzna, ur. 1951, Polska Roma, Tarnów, wywiad 14.06.2019; nagranie: Archiwum MET, sygn. AT/W/12.` |

**9.2 Divisions**, in this order, only those present, headed but **unnumbered**; a bibliography with a single division has no division heading: Abbreviations · Archives (fonds level) · Fieldwork · Printed/legal · Web without DOI · Literature. Coverage: every cited work, except single archival units, single press issues, one-off legal acts.
**9.3 Small caps:** genuine OpenType (fallback: full caps, as in the index); surname only; particles lowercase and outside small caps (`de HEUSCH, Luc`); institutional authors not in small caps. **Character style, never data.** Comma kept for consistency with the volume index.
**9.5 Order:** Polish collation by transliterated form; same author chronological, then by title; sole-author works before co-authored.
**9.7 Identifiers:** DOI mandatory where one exists, printed `DOI: 10.1234/abcd` (no `https://doi.org/`). ISBN only in the bibliography, monographs after 1970, printed `ISBN 978-…` without a colon.

### 9.6. Cyrillic

| Where | System |
|---|---|
| Body | Polish transcription — PWN *Wielki słownik ortograficzny*; places per KSNG with Polish exonyms (Moskwa, Kijów, Lwów) |
| Notes, bibliography, linguistic examples | **ALA-LC, no tie-bars** |

Tables below verified against the LC PDFs (Russian 2012, Ukrainian 2011, Belarusian 2013, Bulgarian 2013), tie-bars dropped:

| | а б в г ґ д е є ё ж з и і ї й к л м н о п р с т у ў ф х ц ч ш щ ъ ы ь э ю я |
|---|---|
| RU | a b v g – d e – ë zh z i – – ĭ k l m n o p r s t u – f kh ts ch sh shch ʺ y ʹ ė iu ia |
| UK | a b v h g d e ie – zh z y i ï ĭ k l m n o p r s t u – f kh ts ch sh shch – – ʹ – iu ia |
| BE | a b v h g d e – io zh z – i – ĭ k l m n o p r s t u ŭ f kh ts ch sh – ʺ y ʹ ė iu ia |
| BG | a b v g – d e – – zh z i – – ĭ k l m n o p r s t u – f kh ts ch sh **sht** **ŭ** – ʹ – iu ia |

Pre-reform letters (19th-c. sources — Bessonov, Patkanov): RU і `ī`, ѣ `ie`, ѳ `ḟ`, ѵ `ẏ` (pre-1918); BG ѣ `ie`, ѫ `u̐`, final ъ `ʺ` (pre-1945); BE ѣ `ě`. Soft/hard signs `ʹ` U+02B9 / `ʺ` U+02BA — never `'` / `"`. No Cyrillic script, no ISO 9 letters (`ŝ`, and `â û ê` in transliterated Slavic words) and no tie-bar U+0361 in the apparatus.

**Sources (for rare letters or other languages):** index https://www.loc.gov/catdir/cpso/roman.html (PDFs — readable as text) · Word sources https://www.loc.gov/catdir/cpso/romansource.html (authoritative for copying, but binary). Relevant beyond the four above: Rusyn (Lemko), Serbian, Macedonian, Romanian in Cyrillic, Non-Slavic in Cyrillic. If a direct fetch is refused, web_search "ALA-LC romanization tables" and follow the index.

**UNCONFIRMED — check before first use:** whether LC's tables include a dedicated Romani table (search the roman.html index for "Romani"). If none exists, no ALA-LC mapping is defined for Cyrillic-script Romani text; flag this to the editor rather than improvising a table. Do not remove this note until confirmed either way; update it with the finding once checked.

Polish transcription, body-text sanity only: е after consonant → `ie` (Бессонов → Biessonow), final/pre-consonant в → `w`, х → `ch`, ц → `c`, ч → `cz`, ш → `sz`, щ → `szcz`, ж → `ż`. For anything non-trivial defer to PWN rules; do not improvise.

## 10. Illustrations, tables, captions

Structure: number, description, date, author/maker, source and signature, rights. `Il.`/`Tab.`/`Wykr.` numbered separately; table titles above, source below; every object referenced in text; apparatus date register; file requirements in the author guidelines (§ 10.1).

**Register:** extreme synthesis, dry, **no evaluative adjectives**; gravity emerges from facts. **Contextual resonance:** keep only what aligns with the article's axis; incidental attributes only if needed for rhythm or if they are the article's own territory. Unknown article → ask (§ 10.2).

Calibration (Polish, verbatim):
- Źle: *Gipsowe odlewy twarzy mieszkańców… stanowią dziś ponury relikt wczesnej antropologii fizycznej. Dokumentują one epokę, w której nauka – zdominowana przez zachodnią obsesję…*
- Dobrze: *Gipsowe odlewy twarzy mieszkańców indonezyjskiej wyspy Nias, sporządzone w 1910 r. przez holenderskiego antropologa J.P. Kleiwega de Zwaana dla wsparcia europejskich teorii rasowych.*

## 11. Abbreviations

Allowed: `s.` `t.` `z.` `nr` `cz.` `r.` `w.` `red.` `tłum.` `oprac.` `wyd.` `w:` `b.m.` `b.r.` `sygn.` `zesp.` `k.` post-Soviet `f. op. d. spr. l. ark. ob. zv.` `zob.` `por.` `i in.` (notes only) `W FN N K` `Ibidem` (italic) `przyp. tłum.` `przyp. red.` (formula closing a non-author note).
Never: `str.` `przeł.` `[w:]` `op. cit.` `dz. cyt.` `idem` `eadem` `tenże` `taż` `tamże` `loc. cit.` `vide` `cf.` `Hrsg.` `éd.` `под ред.`; roman numerals for editions, volumes, months.

## 12. Language

Polish throughout. **Apparatus labels are always Polish** (`red.`, `tłum.`, `w:`, `s.`, `i in.`, `dostęp`), including for foreign works. Only source-identifying elements stay in their language: title, journal, series, archive/fonds, imprint place, publisher.

### 12.1. English online version (bilingual model only)
Same system; changes: quotes `“ ”`/`‘ ’`; `ed.`, `trans.`, `in:`, `p.`/`pp.`, `et al.`, `[accessed: 18.03.2025]`; body Cyrillic in ALA-LC with English exonyms (Moscow, Kyiv). Linter: `--lang en`. Not for translated articles (their English version is the original).

### 12.2. Translated articles (from English; Kanon § 12.2 governs in a clash)
- **Metadata (12.2.2):** EN title/abstract/keywords as in the original, no back-translation; PL abstract is the translation (trimmed to 1000 chars by the editors if needed); missing abstract/keywords written by the translator, EN approved by the author; keywords always the author's (PL translated, group names in authority form); record fields `original_title`, `original_source`, `original_doi`.
- **Translation note (12.2.3):** mandatory title note `*`: original publication per § 7.2 with DOI; licence/permission (CC: the translation is an adaptation); translator; scope of interventions; formula on quotations. Translator also named under the author's affiliation: `Tłumaczenie: Imię Nazwisko`.
- **Quotations (12.2.4):** a) Polish edition exists → quote it, cite it, keep the author's reference after a semicolon; b) Polish source quoted in English → restore the original, `autor cytuje za:`; c) other language via the author's English → from the original if available, else `tłum. z przekładu angielskiego autora`; d) English source without Polish edition → translator's version, no annotation, no `[tłum. własne]`; e) verse/song/proverb as a–c. Unfound place or unavailable original → query; never typeset a provisional unmarked translation.
- **Terminology (12.2.5):** the editors' termbase; HOUSE entries (incl. all vol. 18/2025 rulings) binding; first mention Polish + original italic in brackets unless identical.
- **Group names (12.2.6):** authority form in the translation, no original in brackets; self-ethnonyms and analysed forms stay; Gypsy → `Cyganie` by function, never swapped with Roma → `Romowie`.
- **Translator's notes (12.2.7):** non-author series (§ 7.1), `– przyp. tłum.`; additions inside an author's note in `[… – przyp. tłum.]`; no square-bracket interventions in the body.
- **Interventions (12.2.8):** no silent corrections; agreed ones unmarked but mentioned in the note; obvious typos fixed after checking and listed; cuts only with the author's consent and a mention in the note.

## 13. Metadata and deposit

Record: DOI · titles · authors + ORCID + affiliation (**no capitals in surnames**) · abstracts · keywords (authority form) · pages/volume/year · licence · structured bibliography. Deposit structured fields; source of record is the master CSV.
**Licence unresolved:** author chooses CC BY / BY-NC / BY-NC-ND (default BY-NC); ND blocks the DOAJ Seal. Do not invent a policy.
**Pending:** vol. 18's printed *Informacje dla autorów* states a copyright transfer, contradicting the licence agreement — to be replaced before any OA announcement.

## 14. Rationale — settled, do not reopen

- Typography affects neither indexing nor deposit (record built from CSV). This argument was once used wrongly (year position) — do not revive it, in either direction.
- `op. cit.` removed: forces backward search, unparseable, fails on fragmentary access.
- Arabic apparatus dates: one format; `dd.mm` is the Polish/European default. Roman months considered and rejected (they help only US readers, marginal here). Earlier volumes stay as printed.
- Tie-bars dropped; ISO 9 not used anywhere. One system: ALA-LC.
- Imprint place unpolonised: it is a retrieval key.
- Transcription in body / ALA-LC in apparatus: reader vs retrieval.
- Title translation right after the title: the end-of-record slot belongs to physical-form notes.
- Romani group names roman: proper nouns are never italicised. Foreign exonyms italic: an outside label in a foreign language, not assimilated in Polish, is a foreign word, not a name.

---

## §J. Judgment checks — what the linter cannot see

1. Short titles identical at every recurrence.
2. Note ↔ bibliography coverage, both directions.
3. `Ibidem` in the same column as the preceding note — after layout.
4. Metryczki: could town + group + birth year + role identify someone? Flag, never decide.
5. Register: `1943 r.` in body, or `w 1943 roku` in a caption.
6. Italics: common noun vs proper name; foreign exonym vs endonym (check the kartoteka).
7. Group-name spelling consistent; variants in the authority file; keywords in standard form.
8. Footnote names = initials; bibliography names = full.
9. Editor placement: before title (whole volume) vs after (chapter).
10. Cyrillic: body transcribed per PWN/KSNG; apparatus ALA-LC; `ʹ ʺ` not `' "`; Cyrillic institutions transcribed in body, not translated.
11. Imprint places match the title page.
12. Legal acts and rulings in official wording.
13. Captions: structure complete, register dry, only axis-relevant attributes.
14. CSV: surnames not capitalised, all authors present, DOIs resolve, ranges complete.
15. Page-less citations: a quotation without a page is a query; a whole-work reference is confirmed by the editor.
16. Non-author notes: every `– przyp. tłum./red.` note is in the asterisk series, not numbered; the title note takes the first `*` on page one.
