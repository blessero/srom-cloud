# Gates: 1.2 Baseline (blind translation, divergence analysis, error-class inventory)

Scope: translate four vol. 18 English passages (one per article, per MB 26.09.2026) **without seeing the published Polish**. Record the drafts' sha256 here before any Polish file is opened. Then compare with MB's Polish and inventory error classes. Part A (G1–G8) needs no input from MB. Part B (G9–G11) waits for MB's Polish vol. 18 files.

Files: `tlumacz-baseline-1.2/` — `<art>_src.md` (English passage, cleaned from the srom-produkcja extraction), `<art>_blind.md` (Polish blind draft), `<art>_pytania_tlum.csv` (queries), `manifest.sha256`.

Passage rule (fixed before reading the passages closely): whole sections, 1,300–2,000 words of body text (notes not counted), no abstract, bibliography or acknowledgements; chosen for density of argument and terminology. Chosen: Takács "Roma at America's gates" + "Assembling the clues"; Ostendorf "The nature of history" + "The missing historicization of Romani American history"; Fotta "Studying the racialization of Romanies relationally"; Marushiakova/Popov "Territorial Distributions and Identities" (to a paragraph end within the range).

Blind rule: before G4 is met, do not open the vol. 18 Polish text (`sources/Studia_Romologica_nr_18_2025.txt`), the Polish DOCX files, or termbase rows other than the four HOUSE precedents already known (urasowienie, subaltern/subalterni, spleciona matryca, u-nieobecnianie). The HOUSE rows are applied, as at translation time.

## Part A

- [x] G1: four source passages exist, each 1,300–2,000 body words
  CHECK: python3 tlumacz-baseline-1.2/measure.py words
  EXPECT: /^words: 4\/4 in range/m
  EVIDENCE: dom: 1686 body words ok | words: 4/4 in range

- [x] G2: four blind drafts exist; each keeps the source's paragraph count and note labels
  CHECK: python3 tlumacz-baseline-1.2/measure.py structure
  EXPECT: /^structure: 4\/4 match/m
  EVIDENCE: dom: 14 paragraphs, 2 notes ok | structure: 4/4 match

- [x] G3: drafts follow kanon § 3 marks: no em dash, no straight double quotes in the Polish text, Polish opening quotes present
  CHECK: python3 tlumacz-baseline-1.2/measure.py marks
  EXPECT: /^marks: 4\/4 clean/m
  EVIDENCE: dom: clean | marks: 4/4 clean

- [x] G4: sha256 of the four sources and four drafts recorded in `manifest.sha256`, and the manifest's own sha256 recorded here; files unchanged since
  MANIFEST: sha256 956ef922bb7aff97f3bbe8c2e78d4ca2fe7329d2c3a58717437c3e78eb221fec, recorded 27.09.2026 03:22, before any Polish vol. 18 text was opened
  CHECK: cd tlumacz-baseline-1.2 && shasum -a 256 -c manifest.sha256 | grep -c ': OK$'
  EXPECT: /^8$/m
  EVIDENCE: 8

- [x] G5: every HOUSE source term present in a passage is rendered with its HOUSE form (racialization → urasowienie family; interlocking matrix → spleciona matryca; absence-ing → u-nieobecnianie; subaltern → subaltern/subalterni)
  CHECK: python3 tlumacz-baseline-1.2/measure.py house
  EXPECT: /^house: all \d+ occurrences rendered/m
  EVIDENCE: house: all 9 occurrences rendered

- [x] G6: one query sheet per article, with the srom-produkcja header `adresat;rodzaj;przypis;dzieło;szczegóły`, and at least one row each
  CHECK: python3 tlumacz-baseline-1.2/measure.py queries
  EXPECT: /^queries: 4\/4 valid/m
  EVIDENCE: dom: 8 rows ok | queries: 4/4 valid

- [x] G7: source errors noticed while translating are in the query sheets, not silently fixed; quotations with a possible Polish edition are in the query sheets (§ 12.2.4)
  EVIDENCE: 31 rows in total (takacs 9, ostendorf 7, fotta 7, dom 8; `measure.py queries`). Source errors: takacs row 1 (missing word, P1), row 2 (six obvious typos, fixed and listed per § 12.2.8), row 3 (nuclear families of 20+); ostendorf row 6; fotta row 2 (Williams 1997?); dom rows 3–5 (Autonomous Region, Khudatin/Chavchadze, "so that … remains open"). Quotations: takacs row 4 (Hancock), ostendorf rows 2 (Fotta, same volume) and 4 (Roach et al.), fotta row 1 (Portuguese sources via the author's English).

- [x] G8: blind rule kept up to G4 (manual; what was and was not opened)
  EVIDENCE: Not opened in this session (26–27.09.2026): `sources/Studia_Romologica_nr_18_2025.txt`, any Polish vol. 18 DOCX (none is in the folder), `tlumacz-tb.tsv` beyond the checker's count output. The only contact with the vol. 18 Polish text was `tlumacz-check_tb.py --precedent`, which prints "precedent verified: 4/4" and no text. Opened: the four English originals in `sources/vol18-en/`, their srom-produkcja extractions (scratchpad), Kanon v1.6, srom-produkcja/curator skill files. HOUSE forms were used from memory of the four known rows. Limit: this is self-reported. The hash in G4 is what proves the drafts were not changed after the Polish is opened.

## Part B — waits for MB's Polish vol. 18 files

- [x] G9: MB's Polish text of the four passages located and saved beside the drafts (`<art>_mb.md`), located only after G4
  EVIDENCE: 27.09.2026, after `shasum -c manifest.sha256` → 8 OK (manifest 956ef922…). Source: `vol18-PL-HOLD/*.docx` → srom-produkcja docx_in.py → `extract_mb.py` (only RTL artefacts cleaned). Spans: takacs lines 33–69, ostendorf 41–91, fotta 48–117, dom 100–123 of the extractions.

- [x] G10: divergence table per passage: each divergence classed (terminology, syntax/calque, register, meaning error, omission/addition, apparatus, punctuation/typography, preference) with a verdict on whose version is better and why
  CHECK: python3 tlumacz-baseline-1.2/measure.py inventory
  EXPECT: /^inventory: valid, \d+ errors of mine in \d+ divergences/m
  EVIDENCE: MB-side issues by class: {'SYNTAX': 11, 'TERM-HOUSE': 1, 'MEANING': 8, 'TERM': 7, 'PUNCT': 11, 'QUOTE': 1, 'KANON': 3, 'OMIT-ADD': 1} | inventory: valid, 15 errors of mine in 81 divergences

- [x] G11: error-class inventory (counts per class, measured) that feeds 1.3.4, with MB's review of disputed verdicts
  EVIDENCE: MB reviewed 27.09.2026 (in chat): overall "mostly good calls"; rulings on gypsylorists (C-0005), urasowienie (C-0001), historical toponyms (per case) and pronouns (T4, F18) recorded in `inventory.md` § MB's review; recount `measure.py inventory` → 16 errors of mine in 81 divergences.
