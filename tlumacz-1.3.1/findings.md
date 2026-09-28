# Leaf 1.3.1 — vol. 18 precedent mining: findings (27.09.2026)

Sources: the four vol. 18 translations and their English originals, as clean text (`sources/vol18-md/`, `manifest.sha256`). Scope per MB (27.09.2026): only what recurs and needs consistency. Per-case choices (style, historical/political place names, most general vocabulary) are **not** mined into rules.

## Group names → `kartoteka-seed.tsv` (35 rows)

- Harvest: capitalised tokens of the four English texts, filtered by hand for Romani, Dom/Lom and related group names. 36 names are listed in `measure131.py` (`coverage`: all have a row).
- Every Polish form checked against the article text: `measure131.py seed` → 46/46. Negative controls (an invented form, a deleted row) are caught.
- **House distinctions kept in vol. 18**, to keep (correction 27.09.2026: MB – „Travellersi” and „Wędrowcy” are synonyms, „Travellersi” primary; not a distinction):
  - „Travellersi” for the ethnic group vs „Wędrowcy” for the general category;
  - „antycygański” (antigypsy) vs „antyromski” (anti-Roma);
  - „Gadżar” in body text, „Ghajar” kept in titles.
- **Inconsistencies / questions** (→ `MB-decisions.md` D8): Lom vs Łom; Garachi and Karachi both rendered „Garaczi”; *Ciganos*, *Gitanos*, *Bohémiens* in italics, against Kanon § 3.4; Fotta's *Romanies* vs *Roma*, both „Romowie”.
- Three names (Mutrib, Gurbati, Halabi) occur only in the Polish Dom text. **The Polish followed a revised English version** that we do not hold (as in leaf 1.2).
- Scope limit: the translated articles only; the Polish-original articles of vol. 18 are not harvested.

## Concepts → `tb-candidates.tsv` (6 new, 2 changed rows)

Harvest: field-specific terms with ≥ 3 occurrences or in ≥ 2 articles (counts of 27.09.2026); general vocabulary excluded (stereotype, mobility, anthropology …).

| Row | EN | vol. 18 | State |
|---|---|---|---|
| C-0006 | Romani studies | romologia **and** studia romskie | OPEN (D8 a) |
| C-0007 | antigypsyism / antiziganism | antycyganizm, antycygański | PROVISIONAL |
| C-0008 | racial project | projekt rasowy | PROVISIONAL |
| C-0009 | racial formation | formacja rasowa | PROVISIONAL |
| C-0010 | umbrella term | określenie zbiorcze (3×), termin zbiorczy (1×) | PROVISIONAL |
| C-0011 | historicization | historyzacja | PROVISIONAL |
| C-0001 (change) | racialization | + imperfective proposal urasawiać / urasawianie | D8 b |
| C-0005 (change) | gypsylorist | + gypsiology → cyganologia | — |

Checked on a temporary merge with `tlumacz-check_tb.py` (schema, shape, vocab, precedent, evidence). Every quote is found in the clean text (`measure131.py candidates`); a falsified quote is caught.

## urasowienie family (D8 b)

Counts in the four translated texts: urasowienia 8, urasowienie 5, urasowionych 1, urasowionej 1 (Fotta); urasowiania 1, urasowieniu 1 (Ostendorf). „urasawiane” occurs once, in Fotta's Polish abstract (full-volume text, l. 2408), which is not in the article DOCX. Proposal: imperfective urasawiać / urasawianie / urasawiany (regular -owić → -awiać).

## Anchors

The termbase checker now also accepts `md <art>: «…»` citations, verified in `sources/vol18-md/<art>_pl.md` (clean text). The old `l. N` citations into the full-volume extraction keep working (5/5, selftest 7/7).

## MB's answers (27.09.2026, D8)

All as recommended, with: (d) Garachi / Karachi both legitimate, the author's form decides; Karachi recorded as a variant in the seed. (e) MB: § 3.4 clearly covers endonyms; *Ciganos*, *Gitanos*, *Bohémiens* are exonyms not used in Polish (foreign words, unlike *Cygan*), so italics may be right → passed to srom-typeset (E12). Travellers: „Travellersi” primary, „Wędrowcy” a synonym. Merged: `tlumacz-tb.tsv` 11 rows, all HOUSE (C-0006 romologia, C-0001 imperfective urasawiać / urasawianie / urasawiany).
