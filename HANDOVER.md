# srom-tlumacz — handover (updated 27.09.2026, Claude Code; originally from the claude.ai "SROM_Naczelny" project)

## 1. What exists

Leaf **1.1 (contracts) is complete**: 14/14 gates met (`tlumacz-gates-1.1.md`). Plan with tree, contract and status log: `tlumacz-PLAN.md`.

| File | What it is |
|---|---|
| `tlumacz-PLAN.md` | tree (leaves 1.1–1.5), file ownership, per-article outputs, interfaces with srom-typeset / srom-kanon / srom-scholarly-curator, pending handoffs, status log |
| `tlumacz-tb-schema.md` | termbase fields, controlled vocabularies, decision rule (LOCK, FLOOR, RANK-1…4), evidence standard |
| `tlumacz-tb.tsv` | termbase: 4 HOUSE rows from vol. 18 (urasowienie, subaltern/subalterni, spleciona matryca, u-nieobecnianie) |
| `tlumacz-check_tb.py` | termbase integrity checks + negative-control selftest |
| `tlumacz-test_handoff.py` | contract test of srom-typeset behaviour this module relies on |
| `tlumacz_paths.py` | finds skills and source files in any environment |
| `kanon-12-2-przeklady-PROJEKT.md` | **superseded** — adopted as Kanon v1.6 § 12.2 (srom-kanon skill, `references/kanon-redakcyjny.md`, which governs); kept for the record |
| `../_handoffs/tlumacz-to-typeset.md` | messages/requests to srom-typeset (E1–E9), append-only; rules in `../_handoffs/README.md`; replies expected in `../_handoffs/typeset-to-tlumacz.md` |
| `sources/Studia_Romologica_nr_18_2025.txt` | text extraction of vol. 18 (broken diacritics in places; precedent line refs point here) |
| `sources/SROM_knowledge_base.md` | journal facts (publisher, indexing, etc.) — check here rather than assume |
| `sources/vol18-en/` | English originals of the vol. 18 translations (see § 5) |

## 2. How the module fits the pipeline

srom-tlumacz is the translation step inside **srom-typeset scenario C** (its `references/handoff.md` is the contract):
srom-typeset extracts the source and freezes citations → `<id>_src.md` + `refs.json` → **srom-tlumacz translates** → `<id>_pl.md`, `<id>_refs_tlum.json` (added citations flagged `"srom-added"` + `"srom-source"`), `<id>_pytania_tlum.csv` (query rows, `adresat;rodzaj;przypis;dzieło;szczegóły`), review sheet, quotes sheet, termbase rows → srom-typeset `check.py --pair` → Word working copy (MB edits; Word is now the master) → build → InDesign.
srom-tlumacz does not duplicate srom-typeset (structure, markers, keys, numbers, typography, kanon lint, DOCX).

## 3. MB's rulings (binding)

- **Scope:** EN→PL only. Single exception: author keywords of Polish-original articles are translated PL→EN for metadata. Other source languages possibly later, never at English's expense.
- **Vol. 18 terminology is binding house precedent.** A locked form changes only by MB's logged decision, from the next volume.
- **Tie-break for competing Polish equivalents:** established Polish usage > SROM precedent/consistency > fidelity to the source concept > clarity for non-specialists. **Fidelity floor** (confirmed): a form that distorts the source concept is excluded however established; every exclusion is raised to MB as a query.
- **Editing is a separate step** after translation; the translator applies only the translation-time kanon rules (§ 4.2–4.3, § 5 incl. § 5.3, § 6, § 8, draft § 12.2).
- **Author neologisms** (e.g. Ostendorf's "absence-ing" → „u-nieobecnianie”) are discussed individually.
- **Draft § 12.2 rulings:** translator credited in the article header (and in the translation note); English title/abstract/keywords are the author's originals; Polish abstract trimmed to 1000 characters when needed; missing abstract/keywords written by the translator, English approved by the author; keywords always come from the author (EN kept, PL translated; spelling doubts settled as they arise and logged); quotes from works with a Polish edition use that edition (most recent, unless an older one is better), keeping both references; own translation only when the edition fails the argument; third-language sources available only in the author's English carry „tłum. z przekładu angielskiego autora”; authors' deliberate term choices respected (Gypsy → Cyganie, Roma → Romowie, never swapped); group names in the journal's standard Polish form, no original in brackets; **all non-author notes (title, translator, editorial) form one asterisk series *, **, *** restarting on each page** (title note takes the first * on page one; formulas „– przyp. tłum.”, „– przyp. red.”); agreed corrections unmarked, substantial ones commented with the author; obvious typos fixed silently and listed.
- **Kartoteka wzorcowa** (standard group-name forms, kanon § 6.3) is planned but does not exist; its seed is harvested from vol. 18 in leaf 1.3.1 and handed to srom-kanon.
- MB reviews in Word.
- **27.09.2026 rulings** (log: `tlumacz-decisions.md`): *urasowienie* canonical, „poddawani rasowej kategoryzacji” allowed as a secondary stylistic form; gypsylorists → „cyganolodzy” by default, „gypsyloryści” where the text criticises the old-school scholars; historical/political place names never hard-coded, decided per case by chronology, geography and politics; ask for pronouns before drafting; detailed error mapping is diagnostic only — most choices are per-case judgement.

## 4. State of the srom-typeset interface (27.09.2026)

- `tlumacz-test_handoff.py` **25/25** (T11 front-matter and D12 one-title-note cases added 28.09); KNOWN GAP E16: Word round trip splits the title note: E1, E2, E4 closed; `"srom-added"` in `<id>_refs_tlum.json` verified, also after the Word round trip; E8 verified at the pair check; **E10/T7**: translator in YAML front matter `tlumaczenie:` (4 cases: ignored by the pair check, reported as `translators_struct`, empty = build error, survives Word).
- **Kanon v1.7 is normative** (v1.7: 28.09.2026, D14; one title note, § 7.1) (`srom-kanon/references/kanon-redakcyjny.md`); § 3.4 amended 27.09 (T6): foreign unassimilated exonyms (*Ciganos*, *Gitanos*, *Bohémiens*, *Zigeuner*, *Tsiganes*, Nawar …) italic; endonyms and assimilated exonyms roman.
- **Kartoteka** now lives in srom-kanon (`references/kartoteka.tsv`, from our seed, T8); changes go through `_handoffs/`. `tlumacz-1.3.1/kartoteka-seed.tsv` is history, not the master.
- E9/T2 (hand-typed notes, `docx_in.py --typed-notes`) queued at srom-typeset. E13 (Dom exonyms) sent; borderline assimilation cases (Mutribów, Gadżar, Garaczi) are theirs.

## 5. Vol. 18 material received (25.09.2026)

MB holds the files; English originals are in `sources/vol18-en/`; **Polish translations are kept outside the folder until leaf 1.2's hash is recorded.**

| Article | Polish (notes) | English original | Usable |
|---|---|---|---|
| Takács | 32 | `Takacs_Serbian_Gypsies_rev.docx`, 33 Word notes = 1 title note ("adapted from a long-form digital publication…") + 32 numbered; matches the Polish 32 | full pair |
| Ostendorf | 81 | `Ann_Ostendorf_ENG_…docx`, no notes | body only; fetch the open-access (CC BY) version with notes |
| Fotta | 79 | RTF ripped from PDF, no note objects | body only; fetch the open-access (CC BY) version |
| Marushiakova/Popov | 48 | `Dom_Communities_Stripped_Mac_copy.docx`: notes present but **typed as plain text**, interleaved page by page as in a PDF (page-ID strings between); 52 body markers, notes numbered 1–54, region 48–50 garbled; no Word note objects | full pair after manual note alignment or E9 |

## 6. Pending — MB

Kept in one list for all modules: `../_handoffs/MB-decisions.md` (D4–D6 concern this module). Not repeated here.

## 7a. Session handover (28.09.2026)

This chat closed at MB's request (context size). Next session: MB brings a second text to test translation (same folder, same procedure; no skill needed). Run it as leaf 1.5.2-style intake → draft (`work/<id>/`, gates files like `tlumacz-gates-1.5.2a/b.md`), using `work/ndiaye/ndiaye_intake.md` and `ndiaye_uwagi.md` as templates. Packaging the module as a skill (leaf 1.4.1) is deferred until the procedure has run on 1–2 more texts. Open: Ndiaye Word round trip (after MB's edit; E16), S1–S7 pages (MB).

## 7. Next — Claude, in order

1. **Pilot article: Ndiaye, "Black Roma"** — preliminary translation, updated 28.09.2026 for T14/T15 (one title note; Romka/Romki, *gadjo*; „Egipcjanie”; new `refs.json`): `work/ndiaye/ndiaye_robocza_v2.docx` for MB (v1 left untouched in case MB began editing it), `ndiaye_pl.md`, `ndiaye_front_pl.md`, `ndiaye_pytania_tlum.csv` (14), `ndiaye_uwagi.md`. Build: exit 0, no errors. Waiting for: **MB** — pages / Boy text S1–S7, judgement calls in `ndiaye_uwagi.md` § 3; **srom-typeset** — E16 (Word round trip splits the title note; until fixed, re-merge the block by hand after import). After MB returns the Word file: `docx_in.py` → (merge title note) → `check.py --pair` → `build.py`.
2. Termbase: 18 rows, all HOUSE; C-0012–C-0018 added 28.09.2026 from Ndiaye (D11), pl_standing UNCHECKED — survey native Polish use when convenient.
3. Later: 1.3.2 (vol. 19 vocabulary), 1.4.x tooling, 1.5.x evaluation — per PLAN tree.


## 8. Facts worth keeping

- *urasowienie* is ESTABLISHED: Nowak, „Klio” 2024 (her own English title equates it with "racialisation") and Małczyński (CEJSH) — see TSV evidence.
- *subalterni* rests on one occurrence (an allusion to Spivak); quotes from Spivak follow the published Polish translation, to be identified.
- CoE, OSCE and UN have no Polish official language: only EU acts (EUR-Lex/IATE) and treaties published in Dziennik Ustaw have official Polish names; otherwise attested convention, otherwise original + Polish gloss.
- In Polish law Roma are a *mniejszość etniczna* (Act of 6.01.2005).
- The claude.ai memory and project knowledge are not visible here; this file and the PLAN replace them.
