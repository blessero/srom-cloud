# Studia Romologica — reference facts (knowledge base)

*Merged 03.10.2026 02:20 for the move to Cowork, from: the knowledge base of 04.07.2026 (srom-tlumacz `sources/`), the
journal paragraph and roadmap of srom-quant's SKILL.md, the module instructions (CLAUDE.md files) and the vol. 18 master
CSV.* This file is the **only** place in the plugin for facts about the journal: the skills point here and do not repeat
them. Update here, with the date. Facts confirmed by MB 03.10.2026 03:40.

## Identity

- **Title:** *Studia Romologica* (house abbreviation SROM; "SRom" in older texts).
- **ISSN (print):** 1689-4758. No eISSN yet (application blocked until the online edition is live).
- **Founded:** 2008.
- **Field:** Romani studies (romologia): anthropology, sociology, history, linguistics.
- **Scope** (from MB's srom-naczelny skill, moved here 03.10.2026): Romani studies, the history and contemporary life of
  Romani communities, culture, art, religion, language, integration policy, law, social sciences; interdisciplinary work
  welcome. The test of an article's or a translation's fit.
- **Language:** exclusively Polish: every article, translated ones included, is published in Polish. Only the
  abstracts, keywords, titles and contents are also given in English. The journal is not bilingual.
- **Translator:** unless stated otherwise, Michał Bartosz translates every translated text (MB, 06.10.2026); the
  master CSV's `translators_struct` then reads `Michał|Bartosz||` (no ORCID on record).
- **Website:** https://studiaromologica.pl (WordPress; article landing pages `/articles/{full DOI}/`, volumes `/tom/{vol}-{year}/`).
- **Cadence:** annual, one volume a year, usually published in December. Vol. 18 = 2025 (theme *Romski Atlantyk*);
  vol. 19 = 2026 (in production: the texts in the workspace).

## Publisher

- **Current (from vol. 18 / 2025):** Komitet Opieki nad Zabytkami Kultury Żydowskiej w Tarnowie / The Committee for the
  Preservation of Jewish Cultural Heritage in Tarnów. Also the Crossref registrant.
- **Past (through vol. 17 / 2024):** Muzeum Ziemi Tarnowskiej / Tarnów Region Museum (formerly Muzeum Okręgowe w
  Tarnowie / District Museum in Tarnów).
- **Origin:** the journal grew out of work at the Ethnographic Museum in Tarnów (systematic collection of Romani
  artefacts from the 1990s, the permanent Roma history exhibition). Provenance only: never in masthead or application
  metadata.

## Structure and peer review

- **Part I–II:** scholarly articles, **peer-reviewed** (a minimal but genuine double-blind procedure).
- **Part III:** *Recenzje – Informacje – Opinie* (reviews, information, opinion), not peer-reviewed.
- Sections on the website are the generic terms *Część I*–*Część IV* (data contract: srom-quant).

## Open access and licences

- **Diamond open access**, print-first, now with an online edition.
- Licences: authors choose CC BY, BY-NC or BY-NC-ND (default BY-NC); whether to keep the choice is MB's open question
  GEN-2 (the rule itself: Kanon § 13.2).

## DOIs and metadata

- DOIs through **Crossref** only (never DataCite, never Humanities Commons/CORE: any input saying otherwise is stale);
  article-level DOIs only, no volume DOIs; deposit schema 5.4.0. Locked decisions: srom-quant.
- **Crossref membership:** obtained, with full access (MB, 03.10.2026). Member name: Komitet Opieki nad Zabytkami
  Kultury Żydowskiej w Tarnowie. **DOI prefix: 10.68100** (MB, 06.10.2026). Vol. 18 suffixes minted 06.10.2026 in the
  workspace master CSV; nothing deposited yet (suffixes freeze at the website import). The first deposit is MB's next task.
- **Metadata infrastructure (03.10.2026):** essentially done (master CSV v3, suffix minting, Crossref XML, PDF
  metadata, Highwire tags and JSON-LD in the mu-plugin `srom-scholarly.php` v2.3 in srom-quant's `assets/`); needs
  polishing. The live site was enough to pass Crossref's membership review but still needs work, and runs an older
  plugin version (SYS-1).
- Older back issues have no DOIs; registration starts with the most recent volume.
- Not on Wikidata yet (checked 30.09.2026; MB's question SYS-2).

## Indexing and ranking (confirmed by MB 03.10.2026)

- **Indexed in:** CEJSH, CEEOL.
- **Targets for re-listing by the ministry (MNiSW/MEiN):** ERIH+, DOAJ, EBSCO-Ultimate, ICI JML; the journal is in none
  of the four. Points: 20 (July 2023); zero now (delisted when the new regulation took effect; still zero on 03.10.2026). Goal: re-listing
  within one year, which drives the ERIH+ application and the website/DOI work.

## Roadmap (not built; context for scoping)

eISSN application (after the online edition is live; XMP re-injection into PDFs is safe afterwards) · court register
update Pr 162 · ERIH+ and DOAJ applications (peer-review procedure and OA policy drafted) · a Ministry of Interior grant
framed around the open-access infrastructure · possibly a photo-archive showcase (Manifold/Quire) on a subdomain,
separate from the journal's core infrastructure.

## Where these facts are also hard-coded (code: must match this file)

- `srom-quant/scripts/generate_crossref_xml.py` CONFIG: depositor and registrant (publisher), journal title, ISSN.
- `srom-quant/scripts/wikidata_qs.py`: title, ISSN.
- The master CSV repeats title, ISSN and publisher in every row (columns `journal_title`, `issn`, `publisher`).
