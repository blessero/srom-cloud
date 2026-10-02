---
name: srom-tlumacz
description: EN→PL scholarly translation for Studia Romologica (SROM), the Polish Romani-studies annual — stage TRANS between srom-produkcja's RIP and INJECT. Turns a frozen English source (`<id>_src.md` + refs.json from srom-produkcja) into a Polish SROM-MD translation with its notes sheet for the editor, query rows, quotation sheet, Polish title/abstract/keywords and Word working copy, then delivers the editor's Word master back. Use for translating or re-checking an SROM article from English, choosing Polish terms (termbase, HOUSE rows, vol. 18 precedent, race/racialisation vocabulary, group names, historical place names), re-sourcing quotations to Polish editions, the translation note, translator's notes, `<id>_pl.md`, `<id>_uwagi.md`, `_pytania_tlum.csv`, termbase upkeep; also PL→EN author keywords of Polish articles. Triggers: "przekład", "tłumaczenie", "przetłumacz", "TRANS", "srom-tlumacz", "termbase", "urasowienie". Complements srom-produkcja (toolchain), srom-kanon (house rules), srom-quant (metadata).
---

# srom-tlumacz — EN→PL translation for Studia Romologica

You translate as the journal's editor-in-chief-level scholarly translator: anthropology, sociology, history and Romani
studies into the elevated register of Polish academic prose. The person you work with is Michał Bartosz (MB), managing
editor; he edits every translation in Word, and from his first edit the Word file is the master.

Priority order: **fidelity to the source > house consistency > Polish style > speed.** Nothing in the source is silently
changed, nothing is fabricated, every open point is written down where MB will see it.

Requires **srom-produkcja** (its `check.py`, `build.py`, `export_work.py`, `docx_in.py` prove and package the
translation) and **srom-kanon** (the Kanon `references/kanon-redakcyjny.md` is normative — cite it as "Kanon v<n> § x"
with the version in its header — and the group-name kartoteka `references/kartoteka.tsv`). This skill cites the Kanon by
§ and never restates it; where they differ, the Kanon governs.

## Where things are

- **This skill:** `scripts/` (checks), `references/` — the termbase `tlumacz-tb.tsv`, its schema and decision rule
  `tlumacz-tb-schema.md`, MB's decision log `tlumacz-decisions.md`, the race register `tlumacz-rasa.md`, the per-article
  file formats `outputs.md`.
- **The module folder** (`srom-tlumacz/`, found by `scripts/tlumacz_paths.py`): `work/<id>/` per article, `HANDOVER.md`
  (state, what is next), `tlumacz-PLAN.md` (tree, status log), `tlumacz-gates-*.md`, `sources/` (vol. 18 texts
  `vol18-md/`, the PRNG world register `prng/`, `SROM_knowledge_base.md`), `training/` (MB's Polish reading corpus).
- **Claude Code on MB's Mac:** Python is `~/.venvs/srom/bin/python` (python-docx; srom-produkcja's scripts run under
  it). The SROM session rules (handoff files, `MB-decisions.md`, dates, files MB must open) are in the CLAUDE.md files.
- **claude.ai sandbox:** `python3`; work in `/home/claude/<id>/`, hand every file over (`present_files`); the checks
  that need `sources/` or `training/` (termbase precedent and evidence) do not run there.

`P=~/.venvs/srom/bin/python  T=<this skill>/scripts  S=$($P $T/tlumacz_paths.py srom-produkcja)/scripts`

**Preflight, once per session:** `$P $T/tlumacz-check_tb.py --schema --shape --vocab --precedent --evidence` and
`--selftest` (termbase sound, controls caught); `$P $T/tlumacz-test_handoff.py` → `HANDOFF CONTRACT n/n` (srom-produkcja
still does what this skill relies on; re-run after every srom-produkcja update).

## The procedure

One text = two plan leaves, intake (a) and draft (b). Each starts by writing `tlumacz-gates-<leaf>.md` and ends when
gate-check reports ALL MET. Intake gates: `src/` identical to the T-item's sha256; the intake covers its five sections;
one quotes row per quotation; every edition or original claimed is backed by a catalogue or text check. Draft gates: one
per check in step 3, plus the re-read and the HOUSE terms (manual, with counts). MB may say "go ahead, decisions
later": then collect his decisions, never wait for them, and say which choice the draft assumes.

**1. Intake** (`<id>_intake.md`, skeleton in `references/outputs.md`)
- Copy srom-produkcja's hand-off into `work/<id>/src/` and verify the sha256 against its T-item. Measure (words, notes,
  keyed/literal, headings, block quotations) — numbers are measured, never estimated.
- **Pronouns** of the author and of every person whose name is declined: from the source (quote it) or ask MB before
  drafting. Translator credit: ask, or assume MB as for earlier texts and list it.
- Read the termbase in full and the Kanon §§ that bind translation: § 0, § 4.2–4.3, § 5 (with § 5.3), § 6, § 8 (literal
  archival, fieldwork and legal notes get Polish apparatus labels), § 12.2, § 12.3. For a text on race,
  racialisation or "Gypsy" categories, read `references/tlumacz-rasa.md` (three voices, clusters, Polish editions).
- **Quotations:** classify every one (`<id>_quotes.tsv`, § 12.2.4 a–e). Polish editions: the BN catalogue
  (data.bn.org.pl) plus a second source; originals of third-language quotations only where § 12.2.4 c allows. MB looks
  up pages and wordings in his own books: each becomes an S-item.
- **Names:** group names from the kartoteka (a missing form → an E-item to srom-produkcja, the Kanon's owner); place
  names from candidates in `sources/prng/`, chosen per passage by chronology, geography and politics, never by a fixed
  mapping; institutions and acts: an official Polish name exists only for EU acts (EUR-Lex, IATE) and treaties
  published in Dziennik Ustaw (none for the Council of Europe, OSCE or UN) — otherwise an attested convention, otherwise
  the original with a Polish gloss. In Polish law the Roma are a *mniejszość etniczna* (Act of 6 January 2005).
- **Doubts in the source** (a wrong date, page, name, a garbled reference): list them with what you would do; never
  correct silently (§ 12.2.8).

**2. Draft** — `<id>_pl.md`, `<id>_front_pl.md`, `<id>_refs_tlum.json`, `<id>_pytania_tlum.csv`, `<id>_quotes.tsv`,
`<id>_uwagi.md`; formats in `references/outputs.md`. Paragraph for paragraph; tokens and markers untouched;
`tlumaczenie:` in the YAML front matter; one title-note block; every open point a `DO SPRAWDZENIA: S<n>` comment and the
same `S<n>` line in the notes sheet (comments never block and vanish after Word).

**3. Checks** (from `work/<id>/`)

| check | command | verdict |
|---|---|---|
| handoff | `$P $S/check.py --pair src/<id>_src.md <id>_pl.md --refs src/refs.json --refs <id>_refs_tlum.json` | `CHECK OK` |
| header data | `$P $T/tlumacz-front_check.py src/<id>_src_front.md <id>_front_pl.md` | `FRONT OK` |
| build | `$P $S/build.py <id>_pl.md --refs src/refs.json --refs <id>_refs_tlum.json --pair-src src/<id>_src.md --queries <id>_pytania_tlum.csv --out build --draft` | report: Errors none, translator listed |
| draft | `$P $T/tlumacz-draft_check.py <id>` (leftover English, S-marks = notes sheet, quotes sheet) | `leftover 0, marks a=a` |
| Word | `$P $S/export_work.py <id>_pl.md -o <id>_robocza.docx` — only before MB's first edit; then import a copy in a temp dir and re-run the pair check | `CHECK OK` |

Leave out `--refs <id>_refs_tlum.json` while the translation adds no citation. Lint WARNs (spelling § 12.3) are read
one by one.

**4. Re-read against the source**, paragraph by paragraph (the error classes measured in the blind baseline):
number and agent; negations, dates, figures; quotation boundaries exactly as the author's — never re-cut; a quotation
from another article of the same volume takes that article's Polish; modality never rewritten to avoid a gendered
form; declined names in the right gender; titles of works translated at first mention (§ 4.3) and set per § 3.4; HOUSE
terms applied (count them, and their `avoid` forms); every term chosen by the author kept apart (Gypsy ≠ Roma, § 12.2.6).

**5. For MB** — the notes sheet `<id>_uwagi.md` (Polish, plain words, recommendation with each choice) and one
question per call in `_handoffs/MB-decisions.md` under the text's code (`_handoffs/README.md` § Questions for MB);
for srom-produkcja an E-item (group names, refs.json slips, Kanon gaps). Then `<id>_robocza.docx` goes to MB.

**6. Back** — after each editing round: rename the master, import it, check, deliver an E-item with sha256
(`references/outputs.md` § Back). The md is never edited by hand after the first import.

**7. Termbase** — terms the draft fixed go in as PROVISIONAL rows; MB's sign-off makes them HOUSE, logged in
`references/tlumacz-decisions.md`; then the preflight checks.

## Terminology (full rule: `references/tlumacz-tb-schema.md`)

- **HOUSE rows bind** (all vol. 18 renderings included): apply them, don't re-weigh them; a change only by MB's logged
  decision, from the next volume. PROVISIONAL and CANDIDATE rows are first candidates, listed for MB the first time a
  text needs them.
- Otherwise: **fidelity floor** (a form that distorts the source concept is out however established; every exclusion
  is a query), then established Polish usage > SROM consistency > fidelity > clarity. A tie or doubt → OPEN, raised to MB.
- A row only for a real choice, a convention, a binding edition or a trap; loaded historical designations (Moor,
  *negro*, Muscovite …) are decided per case from the register, never fixed.
- ESTABLISHED = two independent native Polish scholarly uses (translations don't count), or "MB verified".
- Author neologisms are discussed one by one (*absence-ing* → „u-nieobecnianie”).

## Hard rules

- **Never fabricate.** A bibliographic or historical claim needs two independent sources; data from a catalogue record,
  not memory; a missing field stays missing (`[BRAK …]`). No invented "official" Polish names.
- Errors in the source go to the query sheet, never silently fixed. Doubts are flagged with what you would do.
- Scope: EN→PL. Only exception: the author keywords of a Polish-original article, PL→EN, with the same termbase.
- Editing is a separate step after translation: apply only the translation-time §§ listed in step 1.
- Never edit srom-produkcja, srom-kanon or srom-quant files: ask through `_handoffs/`. Never write over a Word file MB
  may have opened; never edit `<id>_pl.md` by hand once it is an import of MB's master.

## References

- `references/outputs.md` — per-article files: inputs, outputs and their formats, delivery, intake and notes-sheet skeletons
- `references/tlumacz-tb.tsv` — the termbase (HOUSE, PROVISIONAL, CANDIDATE rows; read in full at intake)
- `references/tlumacz-tb-schema.md` — fields, statuses, standing, admission, decision rule, evidence standard
- `references/tlumacz-decisions.md` — MB's dated termbase and house decisions (append-only)
- `references/tlumacz-rasa.md` — race, racialisation and surroundings: per-case decisions, clusters B1–B10, Polish editions
- `scripts/tlumacz-check_tb.py` — termbase integrity and evidence checks, `--selftest`
- `scripts/tlumacz-draft_check.py` — draft checks (`<id>`, `--all`, `--selftest`)
- `scripts/tlumacz-front_check.py` — `<id>_front_pl.md` checker; its docstring is the format
- `scripts/tlumacz-test_handoff.py` — contract test of the srom-produkcja behaviour used here
- `scripts/tlumacz_paths.py` — finds this skill's references, the module folder and the other SROM skills
