# Leaf 1.2 — error-class inventory (27.09.2026)

Basis: four blind drafts (`<art>_blind.md`, hashes in `manifest.sha256`, unchanged when compared) against MB's published vol. 18 Polish (`<art>_mb.md`). Every divergence is in `divergences.tsv`. Counts come from `python3 tlumacz-baseline-1.2/measure.py inventory`.

**Selection (declared):** the table records every divergence an editor would mark: meaning, terms, syntax, register, quotations, kanon points, and punctuation/agreement errors. It leaves out synonym choices with no consequence and the apparatus (citations and notes are rebuilt by srom-typeset).

**Verdicts are mine, so they are biased toward my own text.** Codes: MB = MB's version better or binding; ME = mine better; EQ = equivalent, or a decision for MB; SV = the source versions differ (not a translation divergence); BOTH = both wrong. **G11 needs MB's review of the verdicts before this inventory is final.**

## Numbers

- 81 divergences: Takács 16, Ostendorf 19, Fotta 25, Dom 21.
- Verdicts (after MB's review, 27.09.2026): ME 41, MB 14, EQ 15, SV 9, BOTH 2.
- **My errors (MB + BOTH): 16.** QUOTE 3, MEANING 3, TERM 3, GENDER 3, TERM-HOUSE 2, KANON 2. (Before the review: 15. The pronouns given by MB turned T4 and F18 into GENDER errors; O9 and F11 became context decisions.)

## My error classes and the remedy for each (feeds 1.3.4 and the procedure)

| Class | Cases | Remedy |
|---|---|---|
| TERM-HOUSE (3) | O9 gypsylorists → „cyganolodzy”; F4 Ciganologia → „cyganologia”; D2 Garachi → „Garaczi” | Missed only because the run was blind. **1.3.1 (precedent mining) must precede any real translation**, as planned. Three termbase candidates; O9 also needs a fidelity-floor ruling. |
| QUOTE (3) | T3b I moved a quoted word outside the quotation marks; O14 a quotation from an article in the same volume did not use that article's Polish; F25 a false-alarm date query (Williams 1997 is a reprint) | Rules: never re-cut a quotation's boundaries. For quotes from articles in the same volume, take the wording from their Polish. Check the author's bibliography before raising a date query. |
| MEANING (3) | T10 singular for a plural ("nationals"); F19 agent shifted from "matrix" to "projects"; D16 elliptic "The dwelling" left unclear | A final re-read pass checking number and agent against the source, sentence by sentence. |
| TERM (3) | T13 "cover" (journalism) → »obsługiwał«; F10 „egipska oftalmia” (historical medical term); D4 toponyms left in the authors' romanisation | Journalism and medical-history terms go to the termbase. Toponyms wait for 1.3.3 (PRNG/KSNG). |
| KANON (2) | T6 titles of works (photographs) given without a Polish rendering; F2 hypothetical titles in quotes, not italics | Checklist item: § 4.3 (translation of titles on first mention) and § 3.4 (titles in italics). |
| GENDER (1) | F3 avoiding gendered forms changed "could" into "can"; also F18 (EQ): avoidance dropped a name | **Intake step:** before translating, ask MB for the pronouns of the author(s) and of any person whose name must be declined. Never rewrite the modality to avoid gender. |

## Findings for MB

1. **Inconsistency within vol. 18:** Fotta uses *urasowienie*, but Takács renders "racialized" as „poddawani rasowej kategoryzacji” (T3). Does HOUSE *urasowienie* bind every article? (My reading of the ruling: yes.)
2. **„cyganolodzy” for "gypsylorists"** (O9) is binding precedent. But Polish *cyganolog* has also been a neutral label for scholars. Fidelity floor: does it distort the concept?
3. **Ostendorf misquotes Fotta** (O14): "disembodied 'truth'", where Fotta wrote "disembedded". Fotta's Polish is „powracająca formułka” / „oderwanej »prawdy«”, and MB's Ostendorf differs from it. Worth recording for the procedure (§ 12.2.4 a within one volume).
4. **Dom:** MB's Polish follows a revised English version. It confirms four of my queries (D5–D8) and has additions whose origin I cannot tell (D10, D19).
5. **Gender:** MB's texts use masculine forms for Dalen Wakeley-Smith and for Victoria Shmidt (T4, F18). The sources state no pronouns for either. Please confirm.
6. **MB-side patterns in the published text** (for information): SYNTAX/calques 11, PUNCT/agreement 11, MEANING 8, TERM 7, KANON 3. Examples: *dyskretne* for "discrete" (F16), "critical" as „decydującego” (O12), „Zakarpacie” for 1920s Podkarpatská Rus (F11), a quotation closed twice (O15).

## Limits

- The verdicts are self-assessed. A second reader (MB) is the check.
- Four passages, about 6,300 English words, one translator (me) and one set of conditions (blind, no termbase beyond four rows). These are error classes, not error rates.
- Dom: some divergences come from source versions, not translation (SV 9).

## MB's review (27.09.2026) — closes G11

- Overall: "mostly good calls". **Use of this inventory:** it is a one-off diagnostic, not a rulebook. Most choices depend on context and are decided case by case. The remedies above are therefore **procedural checks** (pronouns at intake, quotation boundaries, same-volume quotes, the house-term lookup), not an expanding lexicon. The termbase holds only recurring concepts where consistency matters.
- **gypsylorists:** default „cyganolodzy” (vol. 18). Polish *cyganolog* is close to neutral, English 'gypsylorist' is pejorative, so a text that criticises the old-school scholars may use „gypsyloryści” (a coinage, not in broad use). Decided per article → termbase C-0005.
- **urasowienie:** the canonical term; „poddawani rasowej kategoryzacji” is allowed as a secondary stylistic form (to avoid repetition, or where the construction works better) → C-0001.
- **Historical and political toponyms** (F11: Podkarpatská Rus / Zakarpacie / Ukraina Zakarpacka / Ruś Podkarpacka / Ruś Zakarpacka): decided each time by chronology, topology and politics. **Never hard-coded**, especially for short-lived or contested entities. Rule for 1.3.3: the gazetteer records the candidate forms with their period and scope, never a single mapping.
- **Pronouns:** Dalen Wakeley-Smith is a man; Victoria Shmidt is a woman (T4 → MB's form correct; F18 → both wrong, correct: „artykuł Shmidt”).

