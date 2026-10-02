# srom-tlumacz — handover (updated 01.10.2026 17:20, Claude Code; originally from the claude.ai "SROM_Naczelny" project)

## 1. What exists

Leaves closed (ALL MET): 1.1 contracts, 1.2 blind baseline, 1.3.1 vol. 18 precedent, 1.3.2 vol. 19 concordance, 1.3.5/1.3.5b/1.3.5c training corpus (race vocabulary, 10 texts), 1.4.2a shared draft checker, 1.5.2a/b Ndiaye, 1.5.3a/b Ostendorf, 1.5.4a/b Pahulich, 1.5.5a/b Tittel (intake and preliminary translation each). Plan with tree, contract and status log: `tlumacz-PLAN.md`. The folder is a git repository since 28.09.2026 (`.gitignore` lists what is left out, with its sha256 file).

| File | What it is |
|---|---|
| `tlumacz-PLAN.md` | tree (leaves 1.1–1.5), file ownership, per-article outputs, interfaces with srom-produkcja / srom-kanon / srom-quant, pending handoffs, status log |
| `tlumacz-tb-schema.md` | termbase fields, controlled vocabularies, decision rule (LOCK, FLOOR, RANK-1…4), evidence standard |
| `tlumacz-tb.tsv` | termbase: 18 HOUSE rows, C-0001–C-0018 (vol. 18 precedent, 1.3.1, Ndiaye); 9 PROVISIONAL rows C-0041–C-0049 (1.3.2, vol. 19 drafts, awaiting MB: D26); 12 CANDIDATE rows (C-0019, C-0024–C-0028, C-0031, C-0036–C-0040; 1.3.5/1.3.5b, from MB's reading; not binding until MB decides, per text); rows only under schema § Admission (choice / convention / edition / trap), C-0020–C-0023, C-0029, C-0030, C-0032–C-0035 retired |
| `tlumacz-rasa.md` | register: race, racialisation and surroundings — how to decide loaded designations per case (three voices: period quotation / author reporting period usage / analytic voice), concepts, clusters B1–B10 (rasa and its period synonyms; Murzyn; Moors/Saracens/Turks; Moskwa/Ruś/Turanie; Aryans; cham/czerń; "savages"; Jews; blood and mixture; eugenics), Polish editions for quotations, doubts F1–F20. Load it only for texts on race |
| `training/` | MB's Polish reading corpus: texts git-ignored; `sources.tsv` (keys for `TR <key>: «…»` evidence) and `manifest.sha256` tracked |
| `tlumacz-decisions.md` | dated log of MB's termbase and house decisions |
| `tlumacz-front_check.py` | checker of `<id>_front_pl.md`; its docstring is the format (T11) |
| `work/<id>/` | per-article work (source copy + sha256, intake, `<id>_pl.md`, `<id>_front_pl.md`, queries, notes sheet `<id>_uwagi.md`, Word working copy) |
| `tlumacz-check_tb.py` | termbase integrity checks + negative-control selftest |
| `tlumacz-test_handoff.py` | contract test of srom-produkcja behaviour this module relies on |
| `tlumacz_paths.py` | finds skills and source files in any environment |
| `kanon-12-2-przeklady-PROJEKT.md` | **superseded** — adopted as Kanon v1.6 § 12.2 (srom-kanon skill, `references/kanon-redakcyjny.md`, which governs); kept for the record |
| `../_handoffs/tlumacz-to-produkcja.md` | messages/requests to srom-produkcja (E1–E19; E18 twice, cite it with its [Author] tag), append-only; rules in `../_handoffs/README.md`; replies expected in `../_handoffs/produkcja-to-tlumacz.md` |
| `sources/Studia_Romologica_nr_18_2025.txt` | text extraction of vol. 18 (broken diacritics in places; precedent line refs point here) |
| `sources/SROM_knowledge_base.md` | journal facts (publisher, indexing, etc.) — check here rather than assume |
| `sources/vol18-en/` | English originals of the vol. 18 translations (see § 5) |

## 2. How the module fits the pipeline

srom-tlumacz is the translation step inside **srom-produkcja scenario C** (its `references/handoff.md` is the contract):
srom-produkcja extracts the source and freezes citations → `<id>_src.md` + `refs.json` → **srom-tlumacz translates** → `<id>_pl.md`, `<id>_refs_tlum.json` (added citations flagged `"srom-added"` + `"srom-source"`), `<id>_pytania_tlum.csv` (query rows, `adresat;rodzaj;przypis;dzieło;szczegóły`), review sheet, quotes sheet, termbase rows → srom-produkcja `check.py --pair` → Word working copy (MB edits; Word is now the master) → build → InDesign.
srom-tlumacz does not duplicate srom-produkcja (structure, markers, keys, numbers, typography, kanon lint, DOCX).

## 3. MB's rulings (binding)

- **Scope:** EN→PL only. Single exception: author keywords of Polish-original articles are translated PL→EN for metadata. Other source languages possibly later, never at English's expense.
- **Vol. 18 terminology is binding house precedent.** A locked form changes only by MB's logged decision, from the next volume.
- **Tie-break for competing Polish equivalents:** established Polish usage > SROM precedent/consistency > fidelity to the source concept > clarity for non-specialists. **Fidelity floor** (confirmed): a form that distorts the source concept is excluded however established; every exclusion is raised to MB as a query.
- **Editing is a separate step** after translation; the translator applies only the translation-time kanon rules (§ 4.2–4.3, § 5 incl. § 5.3, § 6, § 8, § 12.2).
- **Author neologisms** (e.g. Ostendorf's "absence-ing" → „u-nieobecnianie”) are discussed individually.
- **§ 12.2 rulings** (adopted in Kanon v1.6; Kanon v1.7 governs): translator credited in the article header (and in the translation note); English title/abstract/keywords are the author's originals; Polish abstract trimmed to 1000 characters when needed; missing abstract/keywords written by the translator, English approved by the author; keywords always come from the author (EN kept, PL translated; spelling doubts settled as they arise and logged); quotes from works with a Polish edition use that edition (most recent, unless an older one is better), keeping both references; own translation only when the edition fails the argument; third-language sources available only in the author's English are translated from that English with no annotation (Kanon v1.13, T33); authors' deliberate term choices respected (Gypsy → Cyganie, Roma → Romowie, never swapped); group names in the journal's standard Polish form, no original in brackets; **all non-author notes (title, translator, editorial) form one asterisk series *, **, *** restarting on each page** (title note takes the first * on page one; formulas „– przyp. tłum.”, „– przyp. red.”); agreed corrections unmarked, substantial ones commented with the author; obvious typos fixed silently and listed.
- **Kartoteka wzorcowa** (standard group-name forms, Kanon § 6.3): see § 4 (srom-kanon owns it; seeded from our leaf 1.3.1).
- MB reviews in Word.
- **27.09.2026 rulings** (log: `tlumacz-decisions.md`): *urasowienie* canonical, „poddawani rasowej kategoryzacji” allowed as a secondary stylistic form; gypsylorists → „cyganolodzy” by default, „gypsyloryści” where the text criticises the old-school scholars; historical/political place names never hard-coded, decided per case by chronology, geography and politics; ask for pronouns before drafting; detailed error mapping is diagnostic only — most choices are per-case judgement.

## 4. State of the srom-produkcja interface (29.09.2026 17:46)

- `tlumacz-test_handoff.py` **34/34** (03.10.2026, against the Kanon v1.15 toolchain; +1 case: a `_v2` master renamed to `<id>_robocza.docx`, T30) (T11 front-matter and D12 one-title-note cases added 28.09; E3, E5 as contract text and E6 source label → printed number after the Word round trip, with a control, added 28.09 after the cross-module review); E16 closed 28.09 (T16, srom-produkcja ce291a2: GAP CLOSED). Run it with `~/.venvs/srom/bin/python` (CLAUDE.md § Checks). E1, E2, E4 closed; `"srom-added"` in `<id>_refs_tlum.json` verified, also after the Word round trip; E8 verified at the pair check; **E10/T7**: translator in YAML front matter `tlumaczenie:` (4 cases: ignored by the pair check, reported as `translators_struct`, empty = build error, survives Word).
- **Kanon v1.15 is normative** (v1.11–v1.15 in T31–T35, 02.10.2026: headings never numbered, § 12.2.4 c reversed — an English quotation is translated with no annotation, an annotation only for a Polish edition or a translation from the original made when it matters; reverse italics, series/conference names; cite "Kanon v1.15"; v1.7: 28.09.2026, one title note, § 7.1; the supplements became v1.8, § 12.3 spelling v1.9, v1.10 compound conjunctions — T27–T29; cite "Kanon v1.10") (`srom-kanon/references/kanon-redakcyjny.md`); § 3.4 amended 27.09 (T6): foreign unassimilated exonyms (*Ciganos*, *Gitanos*, *Bohémiens*, *Zigeuner*, *Tsiganes*, Nawar …) italic; endonyms and assimilated exonyms roman.
- **Kartoteka** now lives in srom-kanon (`references/kartoteka.tsv`, from our seed, T8); changes go through `_handoffs/`. `tlumacz-1.3.1/kartoteka-seed.tsv` is history, not the master.
- **Open comments never block** (`handoff.md`; `build.py` strips them and still passes). After the Word round trip they leave the text and appear only in the import report, so every open `DO SPRAWDZENIA` / `PRZYWRÓCIĆ ORYGINAŁ` is also a line in the article's `<id>_uwagi.md` until MB closes it.
- E9/T2 (hand-typed notes, `docx_in.py --typed-notes`) done (T17, 28.09). Awaiting srom-produkcja's status line: E17 [Ostendorf], E18 [Pahulich], E18 [Ostendorf], E19 [Tittel] (kartoteka rows, refs.json corrections, the § 12.2.4 c line). All four answered in T25 (29.09.2026 18:42): kartoteka rows added; Pahulich `refs.json` re-copied (3b060a87…1f3d5366; the five gloss rows left the query sheet); Urlsperger key and token stay (record fix B12, MB); MEW 741 is D20 B11 (token stays until MB); the § 12.2.4 c line waits for D26 (e). Ostendorf B13 (*Zingances* → *Zinganées*, Vowell's print) is MB's (D19); the draft keeps the author's form until he decides. **Hand-back (T26, `handoff.md` "Back")**: the Word file in `work/<id>/` is the master from MB's first edit — never export over it (a new export goes to a temp dir or `_v2`); after each editing round: `docx_in.py <id>_robocza.docx -o <id>_pl.md` (the md is never edited by hand afterwards; corrections go into Word), `check.py --pair`, `build.py … --draft`, `tlumacz-front_check.py`, then a delivery E-item with sha256 (PLAN OUT-DELIVERY); srom-produkcja takes it with `take_back.py`. Tested here: HANDOFF CONTRACT 33/33. E13 (Dom exonyms) sent; borderline assimilation cases (Mutribów, Gadżar, Garaczi) are theirs.

## 5. Vol. 18 material received (25.09.2026)

English originals are in `sources/vol18-en/`; MB's Polish DOCX are in `vol18-PL-HOLD/` (opened after leaf 1.2's hashes were recorded; git-ignored, sha256 in `vol18-PL-HOLD.sha256`); clean text of all eight in `sources/vol18-md/`.

| Article | Polish (notes) | English original | Usable |
|---|---|---|---|
| Takács | 32 | `Takacs_Serbian_Gypsies_rev.docx`, 33 Word notes = 1 title note ("adapted from a long-form digital publication…") + 32 numbered; matches the Polish 32 | full pair |
| Ostendorf | 81 | `Ann_Ostendorf_ENG_…docx`, no notes | body only; fetch the open-access (CC BY) version with notes |
| Fotta | 79 | RTF ripped from PDF, no note objects | body only; fetch the open-access (CC BY) version |
| Marushiakova/Popov | 48 | `Dom_Communities_Stripped_Mac_copy.docx`: notes present but **typed as plain text**, interleaved page by page as in a PDF (page-ID strings between); 52 body markers, notes numbered 1–54, region 48–50 garbled; no Word note objects | full pair after manual note alignment or E9 |

## 6. Pending — MB

Kept in one list for all modules: `../_handoffs/MB-decisions.md` (SYS-1 and V19-1–4 concern this module as a whole; OST-, PAH-, TIT-, NDI- its drafts). Not repeated here.

## 7a. Session handover (28.09.2026)

This chat closed at MB's request (context size). Next session: MB brings a second text to test translation (same folder, same procedure; no skill needed). Run it as leaf 1.5.2-style intake → draft (`work/<id>/`, gates files like `tlumacz-gates-1.5.2a/b.md`), using `work/ndiaye/ndiaye_intake.md` and `ndiaye_uwagi.md` as templates. Packaging the module as a skill (leaf 1.4.1) is deferred until the procedure has run on 1–2 more texts. Open: Ndiaye Word round trip after MB's edit (E16 fixed 28.09), S1–S7 pages (MB).

## 7. Next — Claude, in order

0. **Ostendorf, "Familiar Outsiders Abroad"** (29.09.2026 03:42) — preliminary translation done without MB's feedback, as he asked: `work/ostendorf/ostendorf_robocza.docx` for MB, `ostendorf_pl.md`, `ostendorf_front_pl.md`, `ostendorf_refs_tlum.json`, `ostendorf_pytania_tlum.csv` (19), `ostendorf_quotes.tsv` (46), `ostendorf_uwagi.md` (MB's choices: S1–S2 pages, terms, group names, doubts; `MB-decisions.md` D22). Assumed: she/her (vol. 18), translator MB. Schmidl (n. 14) and Bolzius (n. 41) translated from the originals (03:55). Waiting for: MB (D22), srom-produkcja (E17, E18 [Ostendorf]: the Urlsperger key may change, then `ostendorf_pl.md` changes). Then, after MB returns the Word file: the hand-back per `handoff.md` "Back" (T26): import the Word master here, checks, delivery E-item (PLAN OUT-DELIVERY).

1. **Pilot article: Ndiaye, "Black Roma"** — preliminary translation, updated 28.09.2026 for T14/T15 (one title note; Romka/Romki, *gadjo*; „Egipcjanie”; new `refs.json`): `work/ndiaye/ndiaye_robocza_v2.docx` for MB (v1 left untouched in case MB began editing it), `ndiaye_pl.md`, `ndiaye_front_pl.md`, `ndiaye_pytania_tlum.csv` (14), `ndiaye_uwagi.md`. Build: exit 0, no errors (open comments don't stop it: S1–S7 are tracked in `ndiaye_uwagi.md` § 1). Waiting for: **MB** — pages / Boy text S1–S7, judgement calls in `ndiaye_uwagi.md` § 3; srom-produkcja: nothing (E16 fixed, T16; `ndiaye_robocza_v2.docx` imports → CHECK OK → build PASS, verified 28.09). Then, after MB returns the Word file: the hand-back per `handoff.md` "Back" (T26): import the Word master here, checks, delivery E-item (PLAN OUT-DELIVERY).
2. Termbase: 39 rows — 18 HOUSE (C-0001–C-0018; C-0012–C-0018 from Ndiaye, D11, MB verified 28.09.2026), 9 PROVISIONAL (C-0041–C-0049, 1.3.2, D26), 12 CANDIDATE (1.3.5/1.3.5b); see § 1.
3. Training corpus (1.3.5): MB may add further Polish texts to `training/` (a row in `sources.tsv`, sha256 in the manifest); harvest as CANDIDATE rows + `tlumacz-rasa.md`. Sourcing list closed by MB (28.09.2026, "skip the rest"). CANDIDATE → HOUSE only through an article's queries. Pahulich (T18, racialisation of Roma) and Ostendorf (T19, Iberian: Moors, limpieza de sangre) will use it first.
4. Incoming T17–T22 answered 29.09.2026 03:42; Pahulich (T18) drafted 29.09.2026 03:54 (leaf 1.5.4): `work/pahulich/pahulich_robocza.docx` for MB, notes sheet `pahulich_uwagi.md` (S1–S10; S10 Grellmann is the one real decision), `pahulich_pytania_tlum.csv` (18; 5 gloss rows applied upstream, T25), MB items in `MB-decisions.md` D23, E18 [Pahulich] to srom-produkcja; then the hand-back (as for Ndiaye above). Tittel (T20) drafted 29.09.2026, committed 04:33 (f3d7bec; the 04:40–04:42 stamps of that session were not read from the clock, corrected in the PLAN log) (leaf 1.5.5): `work/tittel/tittel_robocza.docx` for MB, notes sheet `tittel_uwagi.md` (S1–S12: Polish editions of Kant and Marx to look up, licence, page range), `tittel_pytania_tlum.csv` (26), MB item D25 (the form of “gypsy” is the one real decision), E19 to srom-produkcja; then `tittel_refs_tlum.json` with the Polish editions and the hand-back. West Ohueri (T23, re-frozen T24) received, not started (rights: D24; MB says when).
5. 1.3.2 done (29.09.2026): vol. 19 concordance `tlumacz-1.3.2/` — re-run `vol19_terms.py` after each new draft (West Ohueri next; add probes for its terms and vol. 18 as a column, findings L4). D26 waits for MB; on his word, PROVISIONAL C-0041–C-0049 → HOUSE (log in `tlumacz-decisions.md`).
6. Draft checks: **use `tlumacz-draft_check.py <id>`** (or `--all`) for every draft; the per-article scripts are kept only for their closed gates (1.4.2a, 29.09.2026). The Ostendorf quotes sheet's 7 bare "open" rows were fixed 29.09.2026 17:46: Q32, Q39 → `open (S1)`, `open (S2)`; Q03–Q05, Q12 → `optional` (originals not searched or not accessible; MB can make Q12 an S-item); Q24 → `done`, its open points being the query to the author (n. 38). `draft_check --all`: 0 open rows unmatched.
7. Then 1.4.x tooling (tb_lookup, tb_check), 1.5.x evaluation — per PLAN tree.


## 8. Facts worth keeping

- *urasowienie* is ESTABLISHED: Nowak, „Klio” 2024 (her own English title equates it with "racialisation") and Małczyński (CEJSH) — see TSV evidence.
- *subalterni* rests on one occurrence (an allusion to Spivak); quotes from Spivak follow the published Polish translation, to be identified.
- CoE, OSCE and UN have no Polish official language: only EU acts (EUR-Lex/IATE) and treaties published in Dziennik Ustaw have official Polish names; otherwise attested convention, otherwise original + Polish gloss.
- In Polish law Roma are a *mniejszość etniczna* (Act of 6.01.2005).
- The claude.ai memory and project knowledge are not visible here; this file and the PLAN replace them.
