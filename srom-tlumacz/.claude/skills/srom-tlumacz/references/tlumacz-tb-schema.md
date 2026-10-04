# srom-tlumacz — termbase schema (`tlumacz-tb.tsv`)

One row per **concept**, not per English word. Every inflected or spelling variant of the English term lives in `en_variants`; later source languages attach as extra columns on the same row (see Extension). The file is read by scripts with exact matching; it is never retrieved by semantic search.

## Fields

| Field | Content | Rules |
|---|---|---|
| `concept_id` | stable identifier | `C-0001` onward; never reused, never renumbered |
| `domain` | concept class | controlled list below |
| `en_term` | canonical English form | lemma, lower case unless a proper name |
| `en_variants` | every form the lookup script must match | ` \| `-separated; both -ise and -ize spellings; inflected forms |
| `sense` | short disambiguator | required on every row whose English forms also occur in another row (e.g. *settlement* as sedentarisation vs. as a place); the lookup then reports the hit as ambiguous and never applies a rendering automatically |
| `pl_house` | the Polish form the translator uses | lemma; empty only when `status` = OPEN; with standing NONE it holds the retained original |
| `pl_family` | derived and inflected forms decided so far | ` \| `-separated; undecided members named with `OPEN:` |
| `status` | decision state | controlled list below |
| `pl_standing` | standing of `pl_house` in native Polish scholarship | controlled list below |
| `pl_variants` | other Polish renderings in circulation | each with its source; ` \| `-separated |
| `avoid` | forms not to use, with reason | ` \| `-separated |
| `first_use` | form at first occurrence in the article | kanon § 4.3: Polish form, then the original in italics in round brackets, as spelled in the source |
| `grammar` | gender, declension, number, aspect | anything a translator could get wrong in inflection |
| `note` | scope, connotation, conditions of use | including interference with other Polish senses |
| `evidence` | sources for `pl_standing` | ` \| `-separated; bibliographic data only as far as verified (kanon § 0: no reconstruction). A source in the training corpus is cited `TR <key>: «quote»` (`<key>` from `training/sources.tsv` in the module folder); the checker finds the quote in the file (whitespace-normalised). Works the training article only cites count for nothing until read: they go in `note` as "via <key>" |
| `precedent` | SROM occurrences | `SRom vol/year, author, line` in the project text file |
| `decided` | date and decider | `dd.mm.rrrr MB`; empty for OPEN |

### `domain`
THEORY · NEOLOGISM · ETHNONYM · ROMANI · IDENTITY · HISTORY · LAW · INSTITUTION · OFFICE · PLACE · METHOD · REALIA

ETHNONYM rows point to the *kartoteka wzorcowa* (kanon § 6.3) in `note` and do not duplicate its forms. PLACE, LAW, INSTITUTION and OFFICE rows appear here only when they carry a conceptual decision; plain name mappings live in the gazetteers.

### `status`
- **HOUSE** — binding. Applied without re-weighing. Includes every vol. 18 rendering.
- **PROVISIONAL** — used in a current draft, awaiting MB's sign-off; becomes HOUSE or is replaced.
- **OPEN** — no decision; raised to MB before drafting, never settled silently by the translator.
- **CANDIDATE** — a Polish form harvested from native scholarship read for reference (`training/`, leaf 1.3.5), not a house decision. The translator takes it as the first candidate, still applies FLOOR and the ranks to the passage, and lists it in the article's queries the first time a text needs it; MB's decision then makes it HOUSE (or replaces it). `evidence` carries at least one verified training quote (see `evidence` below).

### `pl_standing`
- **ESTABLISHED** — at least two independent native Polish scholarly publications use the form (different authors; translations do not count). The two-source rule binds the translator's (Claude's) own survey. When MB has verified the form himself, `evidence` = `MB verified dd.mm.yyyy` is sufficient (MB 28.09.2026).
- **COMPETING** — two or more Polish forms, each with native use.
- **ATTESTED** — one native use found. The training corpus does not relax the two-source rule (1.3.5, MB left the choice to the translator 28.09.2026): a form in one training article is ATTESTED, in two by different authors ESTABLISHED.
- **COINED** — no prior Polish use found; house or translator coinage.
- **NONE** — no Polish equivalent; the original is retained (kanon § 4.3).
- **UNCHECKED** — not yet surveyed.

Standing describes the Polish literature, not the house decision: a HOUSE form can be COINED (u-nieobecnianie) or ESTABLISHED (urasowienie).

### Admission (MB 28.09.2026)
A concept gets a row only if at least one holds:
1. **choice** — a competent translator could plausibly choose another Polish form, and consistency across the journal matters;
2. **convention** — a house or field convention the plain form does not show (capitalisation, italics, retained original, first-use form);
3. **edition** — a published Polish rendering binds quotations (a theorist's term);
4. **trap** — a false friend, an anachronism, an obsolete or offensive form.

Terms a competent translator renders right unaided get no row (e.g. *scientific racism*, *racial discourse*, *symbolic violence*). Loaded historical designations (Moor, Saracen, *negro*, Muscovite …) are decided per case from the register `tlumacz-rasa.md`; a row for one exists only as a lookup pointer to it, never as a fixed equivalent. Retired rows keep their ids unused (log in `tlumacz-decisions.md`).

## Decision rule

1. LOCK — HOUSE rows are binding. The translator applies them and does not re-weigh them, even where the survey later shows a different form dominating. A HOUSE form changes only by an explicit decision of the managing editor, logged in `tlumacz-decisions.md`, effective from the next volume (published volumes are not harmonised retroactively, kanon § 17). The survey still reports such divergences, for information. The lock binds the decided form, not incidental slips in the precedent text: a one-off variant (e.g. a second aspect form used once) is recorded as an OPEN member of `pl_family` and settled once.
2. FLOOR — for terms not yet HOUSE, a candidate that misrepresents the source concept is ineligible however established it is: one that shifts the meaning, collapses a distinction the source relies on, or imports an unwanted Polish sense. The floor is a threshold, not a weight; below it the rank order does not apply. Confirmed by MB 25.09.2026. Every exclusion under the floor is raised to MB as a query (`rodzaj`: „termin do rozstrzygnięcia”), naming the excluded form and why; the translator never applies it silently.
3. Among eligible candidates, in this order:
   - RANK-1 established — the dominant form in recent native scholarship of the article's discipline (sociology, history and linguistics may differ; the survey is disciplinary, not global).
   - RANK-2 consistency — agreement with HOUSE rows: derivational families (a HOUSE noun fixes its adjective and verb unless a form is marked OPEN) and sibling concepts (related terms from the same theoretical source are rendered coherently).
   - RANK-3 fidelity — closeness to the source concept where rank 1 and 2 leave a choice.
   - RANK-4 clarity — transparency for a non-specialist reader.
4. A tie, or doubt at any step → OPEN, raised to MB before drafting.

Published Polish translations of a theorist's work are recorded in `pl_variants`. They are binding for **quotations** from that work (Kanon § 12.2.4 a), not automatically for the term; they count toward standing only when the rendering has been taken up in native scholarship.

## Extension to further source languages

Add `<lang>_term` and `<lang>_variants` columns (e.g. `de_term`, `de_variants`); nothing else changes. Source-language-specific interference checklists live in separate files and are loaded only for that language, so no English row, rule or check is affected.
