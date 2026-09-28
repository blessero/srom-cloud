# Requests to srom-scholarly-curator from srom-tlumacz

*Draft 27.09.2026 for MB to pass on (the curator has no chat that reads this folder yet). Rules: `README.md`. Basis: Kanon v1.6 § 12.2.2–12.2.3 (srom-kanon `references/kanon-redakcyjny.md`); curator files read as they are installed on 27.09.2026 (`references/master_schema.md`, `scripts/validate_master.py`, `scripts/generate_crossref_xml.py`).*

## C1 — translator credit in the master CSV and the Crossref deposit (27.09.2026)

**Why.** Kanon § 12.2.3 requires the translator's name in the article header (`Tłumaczenie: Imię Nazwisko`) and in the translation note. The master CSV has translation fields (`is_translation`, `original_title`, `original_source`, `original_doi`) but **no translator column**. `generate_crossref_xml.py` writes every `<person_name>` with `contributor_role="author"`, so a translator can't be deposited.

**Verified fact.** Crossref schema 5.4.0 allows `contributor_role="translator"`. Sources: (1) the Crossref markup guide, *Contributors* ("Supported values are: author, editor, chair, reviewer, review-assistant, stats-reviewer, reviewer-external, reader, translator"); (2) `common5.4.0.xsd` in gitlab.com/crossref/schema, line 1392 `<xsd:enumeration value="translator"/>`.

**Requested changes** (the curator decides the details; these are the outcomes):
1. `master_schema.md`: a new column `translators_struct`, in the same format as `authors_struct` (`Given|Surname|Affiliation|ORCID ;; …`; an empty affiliation or ORCID is allowed). Optionally a `translators_display` for cover pages and WordPress.
2. `validate_master.py`: warn when `is_translation` = `TAK` and `translators_struct` is empty. Warn when `translators_struct` is filled but `is_translation` is not `TAK`.
3. `generate_crossref_xml.py`: after the authors, one `<person_name sequence="additional" contributor_role="translator">` per translator (ORCID and affiliation as for authors). Check the output against the 5.4.0 XSD. Don't change the authors' `sequence` values.
4. WordPress/mu-plugin: show the translator on the article landing page, as printed. Add a `citation_*`/JSON-LD field only if the curator can document one that exists for translators. Don't invent one.
5. No change to `is_translation`, `original_title`, `original_source`, `original_doi` (they already match § 12.2.2).

**Where the value comes from.** The translator's name comes from the article's header line `Tłumaczenie: …`. srom-typeset is asked (E10 in `tlumacz-to-typeset.md`) how that line is marked up and whether the build can pass it on. Until that is settled, the editor keys it into the CSV by hand.

- 27.09.2026 status: C1 items 1–3 and 5 **done** by srom-tlumacz at MB's request (no curator chat): see `curator-update-2026-09-27/CHANGES.md` (11/11 tests, Crossref 5.4.0 XSD valid, mu-plugin untouched). Item 4 (showing the translator in WordPress) **not done**; it touches the live site and the Importer, so it needs MB's decision.
