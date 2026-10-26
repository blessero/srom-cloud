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
- **Translator:** unless stated otherwise, Michał Bartosz translates every translated text (MB, 06.10.2026). He is
  not named as translator anywhere public (MB, 22.10.2026; Kanon § 12.2.3, editorial translations are unsigned): no
  `tlumaczenie` front matter, no „Tłumaczenie:” in the title note or the article header, no line on the online cover,
  `translators_struct` empty (so no translator in the Crossref deposit); the masthead and the site's Redakcja page do name him („tłumaczenia”; MB 25.10.2026). The translation note itself stays (original, licence or permission).
  A translator from outside the editorial team is named as before, unless they ask for anonymity.
- **Website:** https://studiaromologica.pl (WordPress; article landing pages `/articles/{full DOI}/`, volumes `/volumes/{vol}-{year}/`, until 21.10.2026 `/tom/…`, 301-redirected).
  **Host: seohost.pl** (LiteSpeed server; file manager, `wp-config.php` and PHP settings in its panel). Hostinger only ever held a
  staging copy, never the live site: never ask MB for Hostinger access for studiaromologica.pl (MB, 21.10.2026). The site blocks
  bursts (host 429, Wordfence; MB's IP was blocked for a while on 21.10.2026): a handful of requests per check, at least 5 s apart,
  one REST listing rather than many page loads.
- **Cadence:** annual, one volume a year, usually published in December. Vol. 18 = 2025 (theme *Romski Atlantyk*);
  vol. 19 = 2026 (in production: the texts in the workspace).

## Publisher

- **Current (from vol. 18 / 2025):** Komitet Opieki nad Zabytkami Kultury Żydowskiej w Tarnowie / The Committee for the
  Preservation of Jewish Cultural Heritage in Tarnów. Also the Crossref registrant.
- **Past (through vol. 17 / 2024):** Muzeum Ziemi Tarnowskiej / Tarnów Region Museum (formerly Muzeum Okręgowe w
  Tarnowie / District Museum in Tarnów). Vol. 17's colophon names both: „Wydawca ©2024 Komitet Opieki nad Zabytkami
  Kultury Żydowskiej w Tarnowie” and „©Muzeum Ziemi Tarnowskiej (dawniej Muzeum Okręgowe w Tarnowie)”; its title page
  lists both (read 18.10.2026).
- **Origin:** the journal grew out of work at the Ethnographic Museum in Tarnów (systematic collection of Romani
  artefacts from the 1990s, the permanent Roma history exhibition). Provenance only: never in masthead or application
  metadata.

## Structure and peer review

- **Part I–II:** scholarly articles, **peer-reviewed** (a minimal but genuine double-blind procedure).
- **Part III:** *Recenzje – Informacje – Opinie* (reviews, information, opinion), not peer-reviewed.
- Sections on the website are the generic terms *Część I*–*Część IV* (data contract: srom-quant).

## Open access and licences

- **Diamond open access**, print-first, now with an online edition.
- Licences: **from vol. 19 one licence for the whole journal, CC BY 4.0**; the author no longer chooses a variant (MB,
  12.10.2026; approved by the kolegium redakcyjne, MB 14.10.2026). Vol. 18 and earlier keep each author's consented licence (CC BY,
  BY-NC or BY-NC-ND; master CSV `license`), not relabelled CC BY.
- **Back volumes (vols ≤ 17; MB 19.10.2026, GEN-117):** the authors ceded their rights to the publisher (for print;
  online use probably not named in the old agreements: a known risk, MB's decision). The publisher declares **CC BY-NC
  4.0** for them; the © line names the publisher(s) of the volume (master CSV `copyright_holder`). Exception: a text
  whose rights are a third party's stays rights-reserved and free to read (`license` = NONE), e.g. vol. 17 Chiriac,
  © 2018 Tom Lantos Institute. Kanon § 13.2 carries the CC BY rule for new volumes; this back-volume rule
  lives here only (the Kanon governs new volumes; its § 17: published volumes are not unified retroactively).
- **Non-commercial status (MB, 08.10.2026):** SROM is always funded by a ministerial grant, has no permission to sell
  copies, gives them away free, and pays all open-access processing itself: its distribution is wholly non-commercial.
  So SROM's own use of a CC BY-NC source needs no separate consent. But a translation published from vol. 19 on goes
  out under CC BY, so a CC BY-NC (or ND, or non-CC) source needs the rights-holder's consent to CC BY or a kolegium
  exception for that text; the translation note names the licence (Kanon § 12.2.3 pt 2).

## DOIs and metadata

- DOIs through **Crossref** only (never DataCite, never Humanities Commons/CORE: any input saying otherwise is stale);
  article-level DOIs only, no volume DOIs; deposit schema 5.4.0. Locked decisions: srom-quant.
- **Crossref membership:** obtained, with full access (MB, 03.10.2026). Member name: Komitet Opieki nad Zabytkami
  Kultury Żydowskiej w Tarnowie. **DOI prefix: 10.68100** (MB, 06.10.2026). Vol. 18 suffixes minted 06.10.2026 in the
  workspace master CSV; nothing deposited yet (suffixes freeze at the website import). The first deposit is MB's next task.
- **Metadata infrastructure (03.10.2026):** essentially done (master CSV v3, suffix minting, Crossref XML, PDF
  metadata, Highwire tags and JSON-LD in the mu-plugin `srom-scholarly.php`, v2.9 in srom-quant's `assets/` since
  21.10.2026); needs polishing. The live site was enough to pass Crossref's membership review but still needs work;
  it runs the plugin v2.8 since 21.10.2026 (vol. 18 article pages live at their DOI addresses).
- Older back issues have no DOIs; registration starts with the most recent volume. Back catalogue (GEN-118, MB
  19.10.2026): DOIs for vols 17 to 13 now, older ones later; article pages for every volume. Vol. 17: suffixes minted
  18.10.2026, print date the year only („2024”, MB 19.10.2026); workflow in workspace
  `srom-produkcja/volumes/BACK-CATALOGUE.md`.
- Not on Wikidata yet (checked 30.09.2026; MB's question SYS-2).

## Indexing and ranking (confirmed by MB 03.10.2026; ministry rules and criteria verified 21.10.2026)

- **Indexed in:** CEJSH, CEEOL (neither counts for the ministry list).
- **Targets for re-listing by the ministry (MNiSW):** ERIH+, DOAJ, EBSCO-Ultimate (the regulation names five EBSCO collections), ICI Journals
  Master List: the four databases through
  which a journal outside Scopus/WoS can enter the list (Rozporządzenie MNiSW of 30.04.2026, Dz.U. 2026 poz. 630, § 6 ust. 2).
  The journal is in none of the four. Points: 20 (July 2023); zero now (delisted when the new regulation took effect; still
  zero on 03.10.2026).
- **How the list is made now** (the regulation; gov.pl and Forum Akademickie, both 02.06.2026): the list in preparation takes
  database membership as of **1 July 2026** and is to be published by the end of 2026 and signed early in 2027, so it cannot
  include SROM. A journal cannot apply: the regulation has no application route and no fixed update cycle; the minister sets
  each cut-off date (§ 6 ust. 4), and a journal from the four databases is listed only if the Komisja Ewaluacji Nauki selects
  it (§ 11: national and international renown, influence on its discipline, ethical and scientific standards). So the goal is
  to be in ERIH+ and DOAJ before the next cut-off, whose date has not been announced; this drives the website and DOI work.

### Indexing criteria (official pages read 21.10.2026; read them again before filing)

**ERIH+** (erihplus.hkdir.no, *Criteria for Inclusion*, last updated 22.09.2026). Judged on the last two years of published
issues; the journal active for at least two years; ISSN confirmed in the ISSN Portal.
- Each issue should contain at least 5 research articles. English abstracts for all original articles; affiliations for all authors.
- The first author of each research article must have a doctorate; authors without one may only be co-authors.
- Authorship not local: no more than two thirds of the last two years' authors from one institution.
- Board: at least 3 members, listed on the site with affiliation and academic title; when an institution publishes the
  journal, at least a third of the board from other institutions.
- Website: ISSN; board; archive of at least the last two years; aims, theme and audience; the peer review described clearly
  and in detail (saying that articles are reviewed is not enough); periodicity matching the history; ethics, copyright,
  plagiarism, open-access and APC policies. Editors must avoid conflicts of interest between authors and reviewers.

**DOAJ** (doaj.org/apply/guide v2.9; *Licensing & copyright* v2.1).
- At least 5 research articles a year; more than one year of history, or 10 open-access research articles.
- An open licence on every article (Creative Commons or equivalent; DOAJ names no particular one, so CC BY-NC qualifies),
  including republished articles and **translations**. All content free at once: no embargo, no registration; a charge
  for print is allowed. Free-to-read but rights-reserved content may not be scholarly articles. An open-access statement on the site.
- A journal that turned open access states on the site the date of the change and the access and reuse terms of the
  earlier archive (DOAJ's rule for "flipped" journals; the closest fit for vols ≤ 17, e.g. vol. 17 Chiriac, rights reserved).
- Every article reviewed by at least two independent reviewers; **arts and humanities journals may instead use editorial
  review by at least two editors** (which subjects count is DOAJ's call; not checked for SROM). The process described on the site.
- Endogeny at most 25 % in either of the latest two issues (MB keeps this check himself, 14.10.2026).
- Easy to reach from the homepage: open-access policy; aims and scope; board with affiliations (at least five editors
  recommended); instructions for authors; peer review; licensing; copyright (separate from the website's, never "all rights
  reserved"); author charges (say there are none); the publisher's name and address, a contact person and the journal's
  dedicated e-mail address. The journal's name must match issn.org.
- Strongly recommended: submitted, accepted and published dates on each article.
- After a rejection, no new application for six months (unless it was for the ISSN, the website or too little content, then fixed).

**Neither says** whether a translation counts as a research article. Plan each volume with at least five original research
articles in Parts I–II, each with a doctor as first author; translations come on top.

## Roadmap (not built; context for scoping)

eISSN application (after the online edition is live; XMP re-injection into PDFs is safe afterwards) · court register
update Pr 162 · ERIH+ and DOAJ applications (peer-review procedure and OA policy drafted) · a Ministry of Interior grant
framed around the open-access infrastructure · possibly a photo-archive showcase (Manifold/Quire) on a subdomain,
separate from the journal's core infrastructure.

## Where these facts are also hard-coded (code: must match this file)

- `srom-quant/scripts/generate_crossref_xml.py` CONFIG: depositor and registrant (publisher), journal title, ISSN.
- `srom-quant/scripts/wikidata_qs.py`: title, ISSN.
- The website address `https://studiaromologica.pl`: `rip_volume.py`, `cover_page.py`, `validate_master.py` (`SITE`), `wikidata_qs.py`.
- The master CSV repeats title, ISSN and publisher in every row (columns `journal_title`, `issn`, `publisher`).

## Installed on MB's Mac (pointer, 24.10.2026)

What the suite has put on the machine outside the repository (the launchd agent `pl.srom.ikonograf-pobierz`, the
live-site hook `srom-throttle`, skill and InDesign symlinks, the `~/.venvs/srom` packages, pandoc/node/LibreOffice) and how
to remove each: srom-produkcja `references/machine-installs.md`. Keep that register current with any new install.
