# MANIFEST — srom plugin and workspace (03.10.2026)

## Skills (`plugin/srom/skills/`)

| Skill | Role and owner of | Stage | Depends on | Example |
|---|---|---|---|---|
| **srom-produkcja** | the tested toolchain: extraction, keying, checks, Word copies, take-back, build for InDesign, InDesign scripts and template; **owns the stage-gate spec** `references/stages.md` and the hand-off contract `references/handoff.md` | RIP, INJECT (and the scripts for stage 4) | srom-kanon (required: the build runs its linter); pandoc, Python packages (`requirements.txt`) | `assets/example/`: INJECT build of three paragraphs of the Ostendorf translation |
| **srom-tlumacz** | EN→PL translation: procedure, termbase, race register, MB's decision log, draft checks | TRANS | srom-produkcja (`check.py`, `build.py`, `export_work.py`, `docx_in.py`), srom-kanon (Kanon, kartoteka); `anthropic-skills:unlazy` for its gate files (in MB's account, not shipped) | `assets/example/`: Ndiaye's opening, source → Polish, with the pair check |
| **srom-kanon** | the house rules: `references/kanon-redakcyjny.md` (normative, Polish, v1.16), `RULES.md` (English digest), the kartoteka of group names, the linter | all stages | none | `assets/example/`: the linter on a Pahulich paragraph |
| **srom-quant** | metadata and publication: master CSV schema and validator, DOI suffixes, Crossref XML, PDF metadata, Wikidata lines, the site's mu-plugin `assets/srom-scholarly.php` (formerly srom-scholarly-curator) | after stage 4 (and the CSV row at INJECT) | wp-acf-plugin-builder (the site's importer plugin), wp-elementor-builder (site templates) | `assets/example/`: pre-deposit check of the vol. 18 CSV |
| **wp-acf-plugin-builder** | general-purpose: WordPress plugins with an ACF content model; carries the SROM importer plugin in `assets/srom-importer/` | website | none | — (shipped unchanged) |
| **wp-elementor-builder** | general-purpose: Elementor templates and kits | website | wp-acf-plugin-builder (the fields it presents) | — (shipped unchanged) |

Every SROM skill points to `plugin/srom/SROM_knowledge_base.md`, the one file of journal facts, and none repeats
them. Each SROM skill's description ends with what it is not for, naming the sibling that is.

## Layout decisions

1. The workspace mirrors the Code folders (`workspace/srom-produkcja/{volumes,work}`, `workspace/srom-tlumacz/{work,
   sources,training,tlumacz-1.3.2}`), so every relative path in the notes sheets, the ledger and the contract still
   works.
2. srom-produkcja keeps its tested sub-folders (`config/ csl/ lua/ indesign/ tests/`) next to `scripts/ references/
   assets/`: moving them would rewrite paths in about forty files for no gain.
3. `setup.sh` and `requirements.txt` sit at the plugin root, so a Cowork session can reach them from the plugin.
4. The Mac-only InDesign installer is in `local/`, outside the plugin.

## Workspace (`workspace/`)

| Path | What |
|---|---|
| `CLAUDE.md` | session rules for Cowork |
| `STATUS.md` | state of every text; § For the skills; the hand-off log (sha256) |
| `MB-decisions.md` | MB's open questions, one ID each |
| `srom-produkcja/volumes/` | master CSV of vol. 18, authors register, institution IDs |
| `srom-produkcja/work/` | the source PDFs; per text: extraction, keyed source, refs.json, notes sheet, Word copy, proofs (Ndiaye, Ostendorf, Pahulich, Tittel, West Ohueri, Scheffknecht, Dom) |
| `srom-tlumacz/work/` | per translated text: frozen source (`src/`), draft, notes sheet, queries, quotations, Word copy, research (Ndiaye, Ostendorf, Pahulich, Tittel) |
| `srom-tlumacz/sources/` | vol. 18 texts in English and Polish (precedent), the PRNG world register |
| `srom-tlumacz/training/` | MB's Polish reading corpus with `sources.tsv` and `manifest.sha256` |
| `srom-tlumacz/tlumacz-1.3.2/` | the vol. 19 concordance (`vol19_terms.py`, re-run after each draft) |

Every copied file is byte-identical to its Code original (checked when the bundle was built).
