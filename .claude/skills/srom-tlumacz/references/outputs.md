# srom-tlumacz — per-article files

All in `work/<id>/` of the module folder; `<id>` = the master CSV `article_id` (the folder srom-produkcja names in its
T-item). The contract's source of truth is srom-produkcja `references/handoff.md`; `scripts/tlumacz-test_handoff.py`
proves the parts relied on here. srom-tlumacz does not duplicate what srom-produkcja enforces: structure, note markers,
citation keys, numbers, typography, Kanon lint, DOCX.

## In (from srom-produkcja, never edited)

`src/`: `<id>_src.md` (frozen SROM-MD, every reference a `[@key …]` token, note labels = printed numbers),
`refs.json`, `<id>_src_front.md` (title, abstract, keywords of the original), `<id>_queries.md` or `<id>_uwagi.md`
(their RIP notes), `manifest.sha256`. Copy them, then `shasum -a 256 -c manifest.sha256` against the values in the
T-item. A later T-item with a new `refs.json`: copy it in, update the manifest, re-run the pair check.

## Out

| File | What | Proof |
|---|---|---|
| `<id>_intake.md` | the plan (skeleton below); not updated after drafting | — |
| `<id>_pl.md` | the translation (OUT-TEXT) | `check.py --pair` → `CHECK OK`; `tlumacz-draft_check.py <id>` |
| `<id>_front_pl.md` | Polish title, subtitle, abstract, keywords (Kanon § 12.2.2); format in the docstring of `scripts/tlumacz-front_check.py` | `FRONT OK` |
| `<id>_refs_tlum.json` | CSL-JSON entries the translation adds (Polish editions, Polish originals: § 12.2.4 a–b) | pair check with both `--refs` |
| `<id>_pytania_tlum.csv` | query rows, merged by `build.py --queries` into the article's sheet | build report |
| `<id>_quotes.tsv` | quotation re-sourcing sheet | `tlumacz-draft_check.py <id> --quotes` |
| `<id>_uwagi.md` | notes sheet for MB (skeleton below): the lasting record of the draft's choices | `--marks` |
| `<id>_robocza.docx` | the Word working copy; **the master from MB's first edit** | import → pair check |
| `research/` | originals, catalogue extracts, comparisons the draft rests on (downloaded texts git-ignored, ids and sha256 kept) | — |

**OUT-TEXT `<id>_pl.md`.** SROM-MD (srom-produkcja `references/srom-md.md`) translated from `<id>_src.md` paragraph for
paragraph; tokens, markers, locators and block lines copied unchanged.
- YAML front matter at the top: `tlumaczenie: "Imię Nazwisko"` (a list for several). Never a body paragraph; not
  printed; the build reports it as `translators_struct` for the CSV; empty = build error.
- One `::: przypis-tytulowy` block per article: the translation note first (Kanon § 12.2.3, its order and formula),
  the author's own title note as a further paragraph (§ 7.1).
- Translator's notes `[^t<n>]`, ending `– przyp. tłum.`; supplements inside an author's note in `[… – przyp. tłum.]`
  (§ 12.2.7). They print as the asterisk series; after the Word round trip they come back numbered, the formula
  marks them.
- Added citations: the entry in `<id>_refs_tlum.json` carries `"srom-added": "tlum"` and a non-empty `"srom-source"`
  (catalogue record URL or verified ISBN). Data from a catalogue record, never from memory; a missing field stays
  missing (`[BRAK …]`).
- `::: przyklad`: line 1 (form) unchanged, line 2 Polish glosses with the Leipzig labels unchanged, line 3 translated
  in ‘ ’ (§ 5.3).
- Anything unresolved stays in the text as a comment: `<!-- DO SPRAWDZENIA: S<n> – … -->` (a page, a wording, a term,
  a query), `<!-- PRZYWRÓCIĆ ORYGINAŁ: … -->` (§ 12.2.4 a–b). **Comments never block**: the build strips them and
  passes; in Word they become comments and vanish on import. So every open comment is also an `S<n>` line in the
  notes sheet, open until MB closes it (`--marks` counts both sides).

**OUT-QUERIES `<id>_pytania_tlum.csv`.** UTF-8 with BOM, `;`, header `adresat;rodzaj;przypis;dzieło;szczegóły`.
`adresat`: autor / redakcja. `rodzaj` in Polish: „błąd w oryginale — do decyzji”, „termin do rozstrzygnięcia”,
„cytat — wydanie polskie / oryginał do ustalenia”, „niejednoznaczność oryginału — pytanie do autora”, „nota o
przekładzie”, „informacja” (an obvious slip fixed, § 12.2.8); add `(S<n>)` when a notes-sheet item carries it.
`przypis`: the note label of `<id>_src.md` (`--pair-src` turns it into the printed number); body-text items give the
place in `szczegóły`. Errors in the source are recorded here, never silently corrected.

**OUT-QUOTES `<id>_quotes.tsv`.** Columns `ID location cited work class action status` (tab-separated). One row per
quotation of four or more words (location `n. <label>`). Classes = Kanon § 12.2.4: `PL-EDITION` (a), `PL-ORIGINAL`
(b), `THIRD-LANG` (c), `EN-NO-PL` (d), `VERSE` (e). Status: `done`; `open (S<n>)` naming its notes-sheet item;
`optional` (an improvement that is not a decision for MB).

**OUT-FRONT `<id>_front_pl.md`.** Sections `# Tytuł`, `# Podtytuł` („—” when none), `# Abstrakt`, `# Słowa kluczowe`
(5–10, `; `, no final full stop), `# Keywords` („jak w oryginale”, or drafted ones + `<!-- do zatwierdzenia przez
autora -->`). The English title and abstract stay the original's. Header data for the CSV; the build does not read it.

**Termbase rows.** No per-article file: new rows go straight into `references/tlumacz-tb.tsv` as PROVISIONAL and
become HOUSE on MB's sign-off (`references/tlumacz-tb-schema.md`, `references/tlumacz-decisions.md`).

## Back: delivery after each editing round (handoff.md "Back")

1. MB says which Word file is his master. Rename it `<id>_robocza.docx`, older exports `<id>_robocza_old<n>.docx`
   (`take_back.py` takes only that name). Never export over the master; a fresh export goes to a temp folder or `_v2`.
2. `docx_in.py <id>_robocza.docx -o <id>_pl.md`. From now on the md is never edited by hand: corrections go into Word
   and the import is repeated.
3. `check.py --pair` (both `--refs`) → `CHECK OK`; `build.py … --pair-src <id>_src.md --queries <id>_pytania_tlum.csv
   --draft` → `PASS`; `tlumacz-front_check.py` → `FRONT OK`.
4. E-item `## E<n> — [<Author>] delivery: …` with the sha256 (`first8…last7`) of `<id>_robocza.docx`, `<id>_pl.md`,
   `<id>_front_pl.md` and, when they exist, `<id>_refs_tlum.json`, `<id>_pytania_tlum.csv`; the sha256 of the
   srom-produkcja `refs.json` checked against; the three verdicts. A new round = a new item that supersedes the old.

## Skeleton: `<id>_intake.md` (English; the plan)

```
# [<Author>] "<original title>" (<venue, year>) — intake (dd.mm.yyyy HH:MM)
Source: src/… copied from srom-produkcja (T<n>); manifest n/n OK.
Size (measured, wc -w): … words; … notes (… keyed, … literal); headings; block quotations.
Author: <name> — pronouns <from the source, quoted | asked MB>. Translator credit: <confirmed | assumed, MB to confirm>.
## 1. What the article needs   | Feature | Where | Rule (Kanon §) | Handling in the draft |
## 2. Polish editions and originals (§ 12.2.4) — checked dd.mm.yyyy   | Work | Polish edition / original found (two sources) | Use |
## 3. Terminology   HOUSE rows that apply; then | EN | Proposal | Why / alternative | (OPEN until MB decides)
## 4. Doubts in the source (flagged, not corrected; what I would do)
## 5. Plan   files, checks, MB items, E-items
```

## Skeleton: `<id>_uwagi.md` (Polish; for MB, rendered by `_handoffs/tools/mb_view.py`)

```
# [<Author>] „<tytuł polski>” — przekład wstępny: arkusz uwag dla MB (dd.mm.rrrr HH:MM)
Pliki: … Word do pracy: `<id>_robocza.docx`. Autor(ka): …, formy …
Komentarze nie zatrzymują kompilacji i po imporcie z Worda znikają z tekstu: pozycje S są jedynym trwałym zapisem.
Stan dd.mm.rrrr: n otwartych.
## <KOD>-<n> · 1. Do uzupełnienia przez MB — wydania polskie, strony, brzmienie
- S1 [otwarte] [<KOD>-<n>] – przyp. 12: <co sprawdzić, gdzie, co jest w tekście teraz>
## <KOD>-<n> · 2. Decyzje (rekomendacja przy każdej)
## 3. Terminy i nazwy grup przyjęte w szkicu (forma, liczba wystąpień, dlaczego)
## 4. Wątpliwości w oryginale (bez poprawiania; co bym zrobił)
```
An S-item closes as `[zamknięte dd.mm.rrrr (MB)]`. Each item that needs MB also gets its question in
`_handoffs/MB-decisions.md` under the same ID (format: `_handoffs/README.md` § Questions for MB).
