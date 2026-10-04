# Scholar Audit · Studia Romologica

A free, public toolkit from *Studia Romologica* for editors and researchers in Romani
studies. It checks a scholar's standing, finds reviewers without conflicts of interest,
shows who works on what, and maps how scholars relate. The interface is in English and
Polish.

Everything is fetched live from open scholarly sources at the moment you ask. There is no
server of our own, no account and no tracking — a saved library and notes live only in the
visitor's browser.

---

## Four tools, one job each

The tools are tabs in the masthead. Each has one purpose and keeps its state while you use
the others: shortlist reviewers, check one of them, come back, and the shortlist is still
there.

| Tool | Use it when | You give it | You get |
|---|---|---|---|
| **Check a scholar** · *Sprawdź dorobek* | vetting an author, a reviewer, a board candidate | a name, ORCID or OpenAlex ID | the full dossier: record, indexing, expertise, contacts, notes |
| **Find reviewers** · *Znajdź recenzentów* | a manuscript needs reviewers | title, abstract, keywords, authors | ranked candidates with conflicts checked |
| **Field directory** · *Katalog dziedziny* | looking for contributors, collaborators, speakers, supervisors | a theme, a country, a period | who publishes on it, with their figures |
| **Library** · *Biblioteka* | keeping track of the people you work with | — | saved scholars in folders, notes, backup, relations map |

Who it is for: the SROM editorial team first, and anyone in the field after that — other
journals' editors, researchers looking for collaborators, conference and project
organisers, students looking for a supervisor. Everything is built around one editorial
task: finding the right people and understanding how they are connected.

---

## Deploying to studiaromologica.pl

It is a static folder. Upload it as-is to a subdirectory served over HTTPS, for example
`public_html/scholar-audit/` → `https://studiaromologica.pl/scholar-audit/`. It runs
beside WordPress without touching it; no plugin, no database.

```
index.html  app.css  fonts.css  manifest.webmanifest  sw.js
js/      the application, one file per part (see below)
fonts/   12 files, self-hosted Epilogue, Fraunces, IBM Plex Mono — latin + latin-ext
icons/   SROM wheel: SVG favicon, PNG app icons
```

After uploading:

- **Link it** from the site menu or the *Dla autorów* section. Direct links work too:
  `…/scholar-audit/?tool=reviewers`, `?tool=directory&theme=holocaust&country=PL`.
- **On every later update**, bump `CACHE` in `sw.js` (now `srom-audit-v5`), so installed
  copies pick up the new version.
- **Optional:** set `CFG.mailto` near the top of `js/core.js` to the editorial address.
  OpenAlex then serves requests from its faster "polite pool". It is blank by default, so
  nothing is sent that you did not choose to send.

Served over HTTPS it is also an installable app: *Install app* in the menu, or the
browser's own install option, on Android, macOS and Windows.

### Running it locally

```bash
cd srom-scholar-audit && python3 -m http.server 8731
```

Then open <http://localhost:8731/>. Everything works locally except installing to a
home screen.

### The code

| File | What it holds |
|---|---|
| `js/i18n.js` | interface language: `t()`, Polish plurals, every string in English and Polish |
| `js/core.js` | configuration, themes, utilities, dialogs, network, storage, library, backup, stored dossiers, views |
| `js/scholar.js` | one scholar's record: resolution, enrichment, scoring, expertise, editorial notes, profile links |
| `js/dossier.js` | the Check a scholar tool |
| `js/library.js` | the Library and the relations map |
| `js/directory.js` | the Field directory |
| `js/reviewers.js` | the Reviewer finder |
| `js/app.js` | masthead, navigation, settings, start-up, deep links |

---

## Languages

**EN | PL** in the masthead switches the whole interface, and every open tool redraws in
place without fetching anything again. The first visit follows the browser's language.

Short strings are their own English key (`t("Save")`); long texts have a key
(`t("note.venues")`) with both languages in `js/i18n.js`. Polish has three plural forms
(1 praca · 2 prace · 5 prac), handled by `tn()`. Polish phrasing avoids gendered nouns for
a person where it can: *"Romologia to główny obszar pracy"* rather than *"Specjalista…"*.
Titles of works, journals and institutions are never translated; they are shown as the
sources record them.

To change a translation, edit its line in `PL` in `js/i18n.js`.

---

## Check a scholar

Type a **name**, an **ORCID** or an **OpenAlex ID**. A name gives a list to choose from
first, each candidate annotated with how many of their works are in Romani studies — which
usually settles who is who at a glance. The start page lists the scholars you opened
recently, one tap away.

- **Expertise profile** — the headline: what, inside Romani studies, this person works on.
  Twenty themes matched on multilingual cues (Polish, German, French, Bulgarian, Czech,
  Hungarian, Spanish), tiered into *core*, *secondary* and *touched on*. Core is capped at
  three and needs sustained work; below five in-field works the tool declines to name a
  specialism at all.
- **Field relevance** — share of the record in Romani studies, and output per year.
- **Publication record** — every work with venue, indexing tier, open-access status,
  citations and FWCI. Three views: chronological, by venue, by indexing tier; filters for
  years, type, tier, venue, text, in-field only, open access only. Book front matter
  deposited as "chapters" (*Illustrations*, *Index*, *Contents*…) is excluded, and chapters
  are gathered under their parent book, so one monograph is not counted as forty papers.
- **Venues & indexing** — one row per venue with DOAJ and OpenAlex signals, and a place
  to record ERIH PLUS, Scopus, Web of Science and MEiN verdicts once for every later dossier.
- **Identity & profiles** — *How to reach them*, then every identifier: resolved
  (certain), inferred from name (verify), pinned by you, and searches only where the
  destination actually holds records about a person.
- **Peer review** — venues reviewed for, from ORCID.
- **Editorial notes** — observations to weigh, never a score.

**Export…** on the dossier gives it as JSON, the publication list as CSV or as **RIS** for
Zotero, EndNote and Mendeley, or a printable page.

### Stored dossiers

A dossier costs about a hundred requests to build. Each one is kept in the browser, so
opening a saved scholar again is instant — about a tenth of a second instead of up to half
a minute — and a relations map of stored scholars draws without downloading anything.

- Saved scholars are kept for as long as they are saved; the last 25 others you opened are
  kept too, oldest dropped first.
- A stored dossier shows its age and an **Update now** button; past 30 days it is flagged.
  Venue verdicts are re-applied on opening, so a verdict recorded since still counts.
- **Settings → Stored dossiers** chooses what happens when one exists: open it and offer an
  update (default), ask each time, or always fetch fresh — and can clear them all.
- Stored copies are not in the backup file: they rebuild from the sources, and would make
  every backup many megabytes.

### Getting in touch

The contact panel lists only routes the scholar has made public: an email published on
their ORCID record, their current institution's website, the pages they list themselves,
their latest paper (journals print the corresponding author's address), and messaging
profiles such as Academia.edu.

Email addresses are **not scraped from the web**, deliberately. Harvesting and republishing
personal addresses on a public EU site needs a lawful basis under GDPR that a directory
tool does not have — and a browser cannot read arbitrary pages anyway. An address you
already hold can be recorded under *Pin identifiers*; it stays in your browser.

---

## Find reviewers

Paste the manuscript's **title** and **abstract**, optionally **keywords**, and its
**authors** — one per line, as a name, an ORCID or an OpenAlex ID.

1. **Key terms** are picked from the text: your keywords first, then word pairs that recur
   or sit in the title, then single words weighted by frequency and by the title. Words
   that name the field itself (*Roma*, *Romani*, *Cyganie*…) are left out — every in-field
   work has them, so they rank nothing. The terms are shown as switches above the results:
   turn one off, or add your own, and the search re-runs.
2. **OpenAlex** is searched for works on those terms within Romani and Gypsy Studies, in
   the period you choose (10 years by default); the best 400 matches are read.
3. **Their authors are ranked** by how closely each work matches, how recent it is, and
   their share of its authorship — a sole author gets the whole work, one of nine a third.
   One matching paper is a lead rather than an expert, so breadth counts; someone whose own
   record OpenAlex files under Romani studies ranks slightly higher. Each candidate shows
   the matching works, the themes they share with the manuscript, h-index, output and
   activity, and — from ORCID — a public email and how many journals they review for.
4. **Conflicts of interest** are checked against every author you listed:
   - **Conflict** — co-authored within the window you set (5 years by default), or at the
     same institution now. These are set aside in their own section, with the reason.
   - **Check before inviting** — co-authored longer ago, or at the same institution at the
     same time in the recent past. Shown in the list, marked, with the reason.
   - The manuscript's authors themselves are set aside, and you can exclude anyone by hand.
   - Optionally, only reviewers outside the authors' countries.

   An author matched by name is shown as such, with **change** to pick the right profile —
   a conflict check against a namesake would be worse than none.

**Confidentiality.** The title and abstract never leave the browser. Only the search terms
shown with the results are sent to OpenAlex, with the authors' names or ORCIDs for the
conflict check. Nothing is saved, and the manuscript never appears in the page address:
leave the page and it is gone.

**What it cannot see.** Co-authorship and shared institutions in the indexed record, yes;
supervision, friendship, joint grants or rivalry, no. Reviewers still declare conflicts.
Polish-language scholarship without an English abstract is under-represented, so paste the
English abstract where there is one.

Tick candidates to **save the shortlist** into a folder (a name is suggested from the
title), **export it as CSV** with the conflict reasons and public emails, or **map it with
the authors** — the relations map then shows every citation, co-authorship and shared
reference between the candidates and the manuscript's authors.

---

## Field directory

Who publishes in Romani studies, filtered by **theme** (the same twenty), the **country**
they are based in, and the **period** (last 5, 10, 15 or 25 years, or any). Sorted by
in-field works in the period, h-index, citations, most recent activity or name.

It is built from one OpenAlex query that groups the field's works by author and counts
them, and a second that fills in each person's record — six requests, a few seconds, the
top 200 people for any filter.

- **Based in** means the country of their current institution, or one they were at in the
  last three years. A work counts toward a country if any co-author is there, so
  co-authors based elsewhere are left out, and the page says how many.
- Profiles with no citations at all are hidden by default. They are almost always
  indexing artefacts — one "author" with ninety works in a single year, say.
- A theme is matched on words in titles and abstracts, in English and the main field
  languages; counts are in-field works in the period, not whole careers.

Save anyone with ☆, or tick several to save them into a folder together, **map how they
relate**, or export the list as CSV. The address carries the filters, so a filtered list
can be bookmarked or sent.

---

## Library and relations

- **Save** any dossier, or anyone from the directory or the reviewer finder, file them in
  any number of folders, add a note. Someone saved from a list shows *Not evaluated yet*
  until their dossier is first opened; it then fills in, keeping the folders and note.
- Stored in IndexedDB, backed up automatically to a folder you choose (Chrome/Edge) or to
  Downloads (elsewhere); restore merges and never overwrites.
- **Map relations** between 2–12 scholars: citations, co-authorship, shared references and
  thematic overlap. On a wide screen the page runs in two columns — the map with the ranked
  pair table under it on the left; the detail of whatever you tap, then the side-by-side
  theme profiles, on the right. The map opens in the tool it was started from, with a way
  back. Exports as SVG, CSV and JSON.

### Sharing

Every view has its own address: `?q=0000-0001-5333-2330` for a dossier,
`?tool=directory&theme=education&country=HU` for a filtered directory,
`?compare=A5062997866,A5032529636` for a map. **Share link** sends a colleague the same
live view. The reviewer finder's address never carries the manuscript.

---

## Design

Built on the Studia Romologica design system ("Papier"): one palette, `#DF261E` as the
sole accent, reserved for identity and primary action; links in blue; **Epilogue** for
every structural level, **Fraunces** as a quiet accent for work titles and summary lines,
**IBM Plex Mono** for eyebrows and identifiers; hairline rules, 3px corners, the 16-spoke
wheel as the mark. A dark theme is derived from the site footer palette.

Fonts are **self-hosted** rather than loaded from Google — no third-party request on page
load (a recognised GDPR issue for EU sites) and the installed app keeps its typography
offline. The site's Adobe Typekit face (quincy-cf) is not used: the design system does not
call for it, and Adobe's licence does not allow self-hosting.

**Accessibility.** Every text/background pair in both themes meets WCAG AA contrast
(white on the red button: 4.74:1 light, 5.6:1 dark). Keyboard focus is always visible, a
skip link leads past the masthead, the map's nodes and lines are keyboard-operable, dialogs
are native `<dialog>` elements, and motion is removed under *reduce motion*. **A− / A+**
scale the whole interface together.

**Responsive.** Checked at 320, 390, 768, 1024, 1280 and 1440px, in both languages, across
every tool, the relations map and the dialogs: no horizontal page overflow, nothing
clipped. Below 1180px the tools move to a row of their own under the wordmark; below 560px
they take short names (*Check · Reviewers · Directory · Library*).

---

## The indexing tiers

"How well-indexed is this venue" — not a quality judgement.

| Tier | Meaning | Derived from |
|---|---|---|
| **A** | Core indexed | Your Scopus/WoS/ERIH+ verdict, or DOAJ-listed *and* in the OpenAlex core collection |
| **B** | Indexed journal | DOAJ, or OpenAlex core, or venue h-index ≥ 20 |
| **C** | Journal, limited indexing | Registered ISSN or named publisher |
| **D** | Book or chapter | Named academic publisher, via Crossref |
| **E** | Repository or unverifiable | No identifiable venue or publisher |

Every work carries its own rationale on hover. The **seed list** holds only claims checked
against a published source — *Romani Studies* in Scopus and Web of Science; *Studia
Romologica* at 0 MEiN points — shown with a dashed outline until you confirm them.

---

## What cannot be resolved, and why

No API key or login changes these:

| Service | Situation |
|---|---|
| **Scopus** | Elsevier's API needs a key *and* institutional entitlement, and returns no CORS headers — a browser cannot call it. Pin the Author ID. |
| **Academia.edu** | No public API; search is login-walled; scraping is forbidden. Resolves through Wikidata where recorded, otherwise pin it. |
| **Google Scholar** | No API, aggressive bot-blocking. Search link only. |
| **LinkedIn** | HTTP 999 to automated requests; partner-only API. The profile *URL* resolves via Wikidata where recorded. |
| **ERIH PLUS** | No open API, and it indexes journals, not people — a venue-level check. |

Semantic Scholar is resolved through a DOI rather than by name; Wikidata federates
Academia.edu, Scopus, VIAF, ISNI, GND, Library of Congress and IdRef where a scholar has
an item.

## Reading the numbers honestly

Bibliometric coverage of humanities and Central/Eastern European scholarship is thin, and
the tool says so in context: a low tier distribution is often an indexing artefact; missing
DOIs suppress every citation metric; only about a quarter of these works carry reference
lists, so citation and shared-reference ties are minimums. When OpenAlex splits one person
across profiles sharing an ORCID, they are merged and h-index is recomputed from the
merged record. The browser console shows refused lookups from DOAJ and Crossref for items
they do not hold; those are expected and handled.

## Sources

OpenAlex · ORCID · Crossref · DOAJ · Wikidata · Semantic Scholar — all open, all keyless.
Only these services are contacted, and only with the lookup itself.
