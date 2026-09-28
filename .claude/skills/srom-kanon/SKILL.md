---
name: srom-kanon
description: House style enforcement for Studia Romologica, the Polish-language Romani studies annual. Use when checking, correcting, copyediting or typesetting any article for this journal, or when asked about SRom citation format, footnotes, bibliography, dates, Cyrillic transcription/transliteration, archival citation, interview coding, captions, or Romani-name capitalisation. Also use when preparing SRom bibliography data for the master CSV or Crossref deposit, and when an article arrives in the wrong style and needs normalising. Triggers on "Studia Romologica", "SRom", "kanon edytorski", or a Polish humanities article that must follow the journal's footnote system.
---

# Studia Romologica — house style (Kanon v1.7)

Polish-language journal. Footnotes + full end bibliography; **never author-date.** English appears only in metadata (title, abstract, keywords).

- **Normative text:** `references/kanon-redakcyjny.md` — *Kanon edytorski*, Polish, § 0–17. Read the relevant § before ruling on anything not settled below; quote it by its §.
- **Digest:** `RULES.md` — the same rules in English, same § numbers; load this first.
- **Checks:** `scripts/lint_srom.py`. New rules: Kanon first (with a § 17 entry), then RULES.md; ask the editor before changing either.
- The author guidelines (*Wskazówki dla autorów*) are a separate human text outside this skill, derived from the Kanon.

## Workflow

Production articles (import → DOCX for InDesign) go through the **srom-typeset** skill: its build runs this linter on the rendered text and fails on any ERROR. For a spot check of a text outside that pipeline:

1. **Run the linter** on the plain text (extract DOCX with `pandoc -t plain` first):
   ```
   python3 scripts/lint_srom.py article.txt
   python3 scripts/lint_srom.py article.txt --json
   ```
   Use `--lang en` only for the English online version of an article (bilingual model).
2. **Fix** ERROR → WARN. WARN items can be legitimate (French/Romanian `â`, a place-year in prose) — judge each.
3. **Judgment checks**, RULES.md §J.
4. **Report** changes and open questions.

## STOP rule

Missing year, page or publisher, or an illegible/ambiguous element → **do not reconstruct it.** List the gap for the author; leave the record flagged.

## Highest-frequency corrections

1. `op. cit.`, `dz. cyt.`, `idem`, `tenże`, `tamże` → short title: `Ficowski, *Cyganie na polskich drogach…*, s. 51.` `*Ibidem*` only in the same column as the preceding note (after layout), never in a non-author note (§ 7.3).
2. Journal: comma after title, commas throughout, page last — `„Dzieje Najnowsze”, 1947, t. 1, z. 2, s. 310.`
3. `w:` not `[w:]`; `tłum.` not `przeł.`; arabic `wyd. 3`, `t. 2`.
4. Apparatus dates `dd.mm.rrrr`, no `r.` after them: `04.03.1937`, `[dostęp: 18.03.2025]`. Legal acts keep official wording (`Ustawa z dnia 6 stycznia 2005 r.`). Body text: words (`12 marca 1943 roku`).
5. Imprint place as on the title page, never Polonised: `London`, `Moskva`.
6. Cyrillic: body → Polish transcription (PWN; KSNG for places). Apparatus → ALA-LC, no tie-bars. `Biessonow` in text, `Bessonov` in notes.
7. Notes: `J. Ficowski`. Bibliography: `Ficowski, Jerzy.` (small caps by typesetting; **never capitals in the CSV**), all authors, no colon after place.
8. Title translation `[in square brackets]` right after the title; physical-form note `(maszynopis…)` at the very end.
9. Proper names never italic, including Romani group names in any spelling.
10. Labels always Polish, even for foreign works: `red.`, never `Hrsg.`/`ed.`.

## Do not do silently

- Enrich or de-anonymise interview metryczki.
- Normalise an author's spelling of a group name (flag for the authority file).
- Change typographic layout on machine-readability grounds — the deposit comes from the CSV.
- Translate a Cyrillic-script institution name in body text — transcribe it.

## Captions

Dry, no evaluative adjectives; keep only what resonates with the article's axis. Calibration sample in RULES.md § 10. Unknown article → ask first.

## Open — do not invent

Licensing policy (ND option); replacement of vol. 18's printed copyright-transfer clause; whether ALA-LC has a Romani table (RULES.md § 9.6 — unconfirmed).
