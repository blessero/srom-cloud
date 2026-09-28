# SROM-MD and refs.json

SROM-MD is Pandoc Markdown restricted to what the journal prints. Read with
`markdown-smart-superscript-subscript-strikeout-raw_html-raw_tex-tex_math_dollars-implicit_figures-fancy_lists-example_lists-task_lists-auto_identifiers`
(the constant `FROM` in `build.py`). Typography is already final in the file: „ ” » « ‘ ’, en dashes,
… — the reader does no "smart" conversion. Non-breaking spaces are **not** typed; the template's GREP
style sets them (kanon §3.3), and `normalize.py` turns stray nbsp into plain spaces.

## Text

| element | write | becomes (config key → style) |
|---|---|---|
| level-1 heading | `# 1. ROMANIPEN JAKO KATEGORIA` | h1 |
| level-2 heading | `## 1.2. Ujęcia normatywne` | h2 — level 3 fails the build |
| paragraph | one line per paragraph | body_first after a heading or at start, else body (after a block quote: body, kanon §2) |
| block quote | `> …` | quote |
| list | `- człon;` (the dash is not printed — the style supplies it) | list |
| numbered list | `1. człon;` | list_numbered; the number is typed ("1." + tab), the style sets the indents |
| italics | `*…*`; a title inside an italic title: `*Tytuł _wewnętrzny_ tomu*` → inner run roman + warning | character style italic |
| small caps | `[Ficowski]{.smallcaps}` | character style smallcaps |
| bold, underline | not used (kanon §3.4) — removed with a warning | — |
| special paragraph | `::: podpis` … `:::` (also `tabela-tytul`, `tabela-zrodlo`, `nota`, `bez-wciecia`, `przypis-tytulowy`) | caption / table_title / table_source / author_note / body_first / asterisk_note (the title note: first note of the asterisk series, see Notes) |
| motto (opening quotation) | `::: motto` … `:::`; optional source line in `::: motto-zrodlo` | Motto (italic; titles inside turn roman) / Motto – źródło; the next paragraph starts unindented |
| dialogue inside an article (interview, hearing) | `::: dialog` with one turn per paragraph: `Przewodniczący Coe: Na jakim statku…`; a turn without "Name:" continues the previous speaker; stage directions typed in capitals: `[POPRZEDNIA DECYZJA PODTRZYMANA]` | Dialog; "Name:" gets the character style Mówca – etykieta automatically |
| transcript (conference, discussion) | `::: mowca` with the name on line 1 and the affiliation on line 2 (no blank line between), then the speech as ordinary paragraphs | Mówca / Mówca – afiliacja; the speech starts unindented |
| verse quotation | `> wers pierwszy\` newline `> wers drugi` (backslash = forced line break), or a line block (lines starting with a vertical bar) | quote_verse, line breaks kept; elsewhere a forced break becomes a space (warned) |
| table | pipe table; title as `Table: Tab. 1. …` under it or a `::: tabela-tytul` div above; source in `::: tabela-zrodlo` below (kanon §10) | table_title, table_cell, table_source — rules and widths from the template's table style |
| interlinear example (§5.3) | `::: przyklad` with a fenced block: line 1 form, line 2 gloss, line 3 translation, columns aligned with 2+ spaces | example_form / example_gloss / example_trans, columns as real tabs |
| editor comment | `<!-- … -->` | removed before building; one containing PRZYWRÓCIĆ / DO SPRAWDZENIA / TODO / FIXME **fails the build** until resolved |

## Front matter

SROM-MD has no header: title, author, affiliation, abstract and keywords are set in InDesign from the master CSV
(Kanon § 13.3). The only front-matter field the toolchain reads is `tlumaczenie` (translated articles, Kanon
§ 12.2.3), a string or a YAML list; not printed, reported for the CSV, kept through the Word working copy:

```
---
tlumaczenie: "Imię Nazwisko"
---
```

## Notes

- Marker: `[^n]` **before** . , ; : and after a closing quote or parenthesis; after an abbreviation
  period it stays after the period (`XV w.[^3]`) — normalize.py applies this.
- Definition: `[^n]: …` directly under the paragraph that contains the marker (keeps chunks
  self-contained for translation). Continuation paragraphs indented by 4 spaces (warned: rare in SROM).
- Labels just need to be unique; pandoc numbers notes by order of appearance.
- Non-author notes (kanon § 7.1): translator's `[^t1]` … ending `– przyp. tłum.`, editorial `[^r1]` … ending
  `– przyp. red.` (a note ending with the formula counts even with another label; `[^t…]`/`[^r…]` without it is
  an error). With the title note (`::: przypis-tytulowy`) they are one asterisk series, not Word footnotes:
  the build puts a `*` in character style asterisk_ref at the marker and the note, opening `* `, in
  asterisk_note at the end of the DOCX (title note first). The typesetter sets them above the numbered notes
  and the asterisks per page (`_gwiazdki.jsx`). No Ibidem in them or in the author's note right after one.
  A citation the translator adds to an author's note is declared (see `handoff.md`).

## Citations inside notes

| need | write | prints (first / later) |
|---|---|---|
| one work, page | `[@ficowski1985, s. 15]` | J. Ficowski, *Cyganie…*, Wydawnictwo Literackie, Kraków 1985, s. 15. / Ficowski, *Cyganie na polskich drogach…*, s. 15. / *Ibidem*, s. 15. |
| several works | `[@a, s. 1; @b, s. 2]` or `[@a, s. 1]; zob. też [@b]` | joined with "; " |
| see / compare | `[Zob. @a, s. 5]` or `Zob. [@a]` | prefix kept; without a page = whole work |
| page range, "and following" | `[@a, s. 215–220]`, `[@a, s. 215 i n.]` | |
| non-page locator | `{tabl. 14}`, `{k. 34v}`, `{rys. 2}`; `rozdz. 3` is recognised | printed as written |
| no page | `[@a]` | allowed everywhere, nothing printed in place of the page; listed in the query sheet (quotation source → ask the author) |

Forbidden: `@key` without brackets and `[-@key]` — pandoc would print the first citation without its
author. Write the name in prose and cite normally. A citation after prose inside a note ("Szerzej
pisze [@mroz2011]") is fine: if it would come out as *Ibidem*, the build prints the short form.

**Keying short-form notes** (English and French journals: "Hornback, 35–69.", "Ndiaye, 2022, 214–31.", "Brome, 4.1.883."):
- A bare number after the author (and the year, where the author has several works) is the page:
  `Hornback, 35–69.` → `[@hornback2018, s. 35–69].` `check.py --keyed` reads these unlabelled pages and fails if one
  is lost, exactly as with `s.`/`p.`; the year is dropped by the short form, which is normal.
- Abbreviated ranges are keyed in full: `214–31` → `s. 214–231` (the check counts them as equal).
- Other locators in braces, as written or with the Polish label: act.scene.line `{4.1.883}`, signatures `{S2ʳ}`,
  lines `{w. 93–96}`; "n.p." = no page → `[@key]`, but a book/chapter given with it is the locator:
  "n.p. (book 11, chapter 2)" → `{ks. 11, rozdz. 2}`. Forms without a Kanon rule (act.scene.line, signatures) are
  queries for the editor.
- The same work named in another form in one note (`M.W., 60` where the list and the other notes have
  `M. W., M. A.`) is keyed to the same work; the check accepts the name without spaces and a literal author's
  first part. List the variant in the report: the printed short form comes from refs.json and is uniform.
- Lead-ins: see → zob., see also → zob. też, cf. → por., quoted in / cited in → cyt. za (Kanon § 7.2; handoff.md).

Stay **literal** (plain text in the note, kanon §8): archival units (§8.1), fieldwork codes (§8.2),
single press issues, legal acts cited once, statistics tables without a stable record.

## Bibliography block

```
::: {#bibliografia}
# Bibliografia

## Źródła archiwalne

Archiwum Narodowe w Krakowie (ANK), zespół 29/456: Starostwo Powiatowe w Tarnowie, sygn. 1–48.

## Źródła terenowe

W12 – mężczyzna, ur. 1951, Polska Roma, Tarnów, wywiad 14.06.2019; nagranie: Archiwum MET, sygn. AT/W/12.
:::
```

Section headings are the kanon names — Wykaz skrótów, Źródła archiwalne, Źródła terenowe, Źródła drukowane
i prawne, Źródła internetowe, Literatura przedmiotu — without numerals (an unknown name stops the build).
Write literal sections only (archives, fieldwork, legal acts); sections filled from refs.json are
generated: every cited key goes to its `srom-section` (I–VI = the six sections in that order; default VI,
a webpage without DOI → V). A section may not have both literal and generated entries. Only the sections
an article uses are printed, in kanon order; a single section gets no subheading. Surnames in literal
entries: `[Mróz]{.smallcaps}, Lech.`

## refs.json (CSL-JSON) — conventions

Typed by Claude from the author's bibliography and notes, then verified: `cite_map.py audit --bib`
(against the original bibliography) and `check.py --keyed` (against the original notes).

| field | rule |
|---|---|
| `id` | `surnameYEAR`, ASCII, lower case; suffix for collisions (`nowak2010b`) |
| `type` | book, chapter, article-journal, article-newspaper, entry-encyclopedia, thesis, report, webpage, motion_picture, paper-conference |
| `author` / `editor` / `translator` / `director` | `{"family": "Mróz", "given": "Lech"}` — normal case, never capitals; particles `{"family": "Heusch", "non-dropping-particle": "de"}`; institution `{"literal": "GUS"}` |
| `title` | as published; Cyrillic transliterated per kanon §9.6; an omission marked in the author's list (". . ." in a long early-modern title) → `[…]` (§ 3.5, § 4.1), the words stay |
| `title-short` | the short title for later citations, **with** `…` if truncated (`Cyganie na polskich drogach…`) |
| `original-title` | Polish translation of a foreign title, printed in [ ] |
| `container-title` | journal / volume / encyclopedia / website |
| `volume`, `volume-title` | `t. 2: *Tytuł tomu*` |
| `issue` | numeric → "nr 5"; anything else verbatim (`"z. 2"`) |
| `edition` | verbatim after "wyd." (`"3"`) |
| `page` | article/chapter range, hyphen or en dash |
| `issued` | `{"date-parts": [[1985]]}`; press with day: `[[1928, 5, 3]]`; unknown year → leave out (prints `[BRAK ROKU]`) |
| `original-date` | first edition year for reprints (author-date "1985/2002") |
| `publisher`, `publisher-place` | never guessed; missing → `[BRAK WYDAWCY]`/`[BRAK MIEJSCA]` |
| `ISBN` | monographs after 1970 (kanon §9.1) — build warns if missing |
| `DOI` | bare `10.xxxx/…` |
| `URL`, `accessed` | web sources |
| `note` | physical-form remark, printed in ( ) at the end (`maszynopis pracy doktorskiej…`) |
| `citation-label` | the author-date label when a/b suffixes exist (`"Nowak 2010b"`) — used by cite_map |
| `srom-section` | `I`–`VI` override of the bibliography section |
| `srom-as-written` | an approved correction of the author's data keeps the author's form: `{"editor": "Van Lannep", "publisher-place": "Droit"}`; the audit and `check.py --keyed` accept it, the build report lists it |
