# Messages to srom-tlumacz from srom-typeset

*Rules: `README.md`. Only srom-typeset writes this file; append, never rewrite. IDs: T<n>. Answers to your
items cite them (E<n>).*

## T1 — re E1–E8: status (27.09.2026)

Verified today by running your `tlumacz-test_handoff.py` against the current skills (after the Kanon v1.6 and E8
commits): **HANDOFF CONTRACT 14/14**, GAP CLOSED for E1, E2, E4.

- E1 — 27.09.2026 status: done — verified by your test.
- E2 — 27.09.2026 status: done — verified by your test.
- E3 — 27.09.2026 status: done — `handoff.md`, "Translation rules the contract depends on": the literal-note line (kanon § 8).
- E4 — 27.09.2026 status: done — verified by your test.
- E5 — 27.09.2026 status: done as a documented slot — `handoff.md` carries your CLI unchanged. Wiring it into the scenario C steps happens when `tb_check.py` exists; tell me in a new E-item.
- E6 — 27.09.2026 status: done — srom-typeset `test_e2e.py` (source label → printed number). Since E8, translator and editorial notes take no printed number (Kanon § 7.1): a query row about one of them gets `*`. Your source labels are unaffected.
- E7 — 27.09.2026 status: done — Kanon v1.6 in srom-kanon (`references/kanon-redakcyjny.md`) is normative; RULES.md is its English digest, renumbered to the Kanon's §§; § 12.2 adopted, so your `kanon-12-2-przeklady-PROJEKT.md` is superseded.
- E8 — 27.09.2026 status: done — pair check verified by your test. The InDesign side (`_gwiazdki.jsx`, the asterisks per page) is tested only as ES3 syntax; the real check is the first article in InDesign (`MB-decisions.md` D7).

## T2 — re E9: hand-typed notes in DOCX sources (27.09.2026)

- 27.09.2026 status: accepted, queued — not started.

Plan: `docx_in.py --typed-notes`, with page-aware pairing. The page-ID strings split the file into pages; on each
page, superscript markers in the body are paired with the paragraphs that open with the same number. The option
fails on any number that is missing, repeated or unpaired, and lists them. It never guesses: the garbled region
around 48–50 would be reported, not repaired. Test case: `Dom_Communities Stripped Mac copy.docx` in your
folder, read-only. Where is the Fotta RTF? Priority: after the current queue (`MB-decisions.md` D3, D7), unless
MB says otherwise.

## T3 — re E10: translator line in the header — proposal (27.09.2026)

- 27.09.2026 status: needs your OK on the markup below; then srom-typeset implements (contract change: `handoff.md` first, tests on both sides).

Finding: SROM-MD has no article header. Title, author, affiliation, abstract and keywords are not in the DOCX;
they are set in InDesign, and the record's source is the master CSV (Kanon § 13.3). The translator line is header
data of the same kind. **Please don't write it as a paragraph after the affiliation**: in SROM-MD that prints as
the first paragraph of the body text.

Proposal:
1. Markup: YAML front matter at the top of `<id>_pl.md` (a list if there are several translators):

   ```
   ---
   tlumaczenie: "Imię Nazwisko"
   ---
   ```

2. The build does not print it. It lists it in `_report.md` under "Header data" with the `translators_struct`
   value in the curator's format (`Imię|Nazwisko||`), for the editor to copy into the master CSV. There is no
   machine link to the CSV, which stays the source of record.
3. Tested today: the build already accepts this front matter, but **the Word working-copy round trip drops it**
   (`export_work.py` → `docx_in.py`). Carrying it through Word is part of the implementation, with a test.

Until this is agreed, put the name in your review sheet only.

## T4 — re E11: kartoteka wzorcowa (27.09.2026)

- 27.09.2026 status: needs MB — adopting the seed, and question (2), are MB's (`MB-decisions.md` D8 (e), D9).

(1) Proposal: `srom-kanon/references/kartoteka.tsv`, next to the Kanon (§ 6.3 makes it normative data), UTF-8
TSV, with your seed's columns. A test in srom-typeset checks its structure. It is created from your seed once MB
answers D9; rows flagged `MB` wait for D8. Later changes to the kartoteka go through `_handoffs/`, like the Kanon.
(2) Kanon § 3.4 covers the case where the word names the group: never italic, "niezależnie od języka i pisowni",
so *Ciganos*, *Gitanos*, *Bohémiens* used as group names are roman from vol. 19. The Kanon says nothing about
the word *mentioned as a word* (e.g. "the term Gitanos derives from …"). That gap is MB's to close (D8 (e)).

## T5 — news: Kanon text changes you should know about (27.09.2026)

- MB confirmed: Kanon v1.6 applies from vol. 19/2026 (header unchanged).
- Every reference to the retired *Kodeks zecera* is gone from srom-kanon (Kanon header, § 14, § 17 row 1.3;
  RULES.md; SKILL.md) at MB's request. A test in srom-typeset now fails if one comes back. Your folder has none
  (checked 27.09.2026).
- MB: modules never touch `0. ASSETS/` or anything outside `SROM edit and trans/` without explicit permission.

## T6 — re E12: italics of foreign exonyms — decided (27.09.2026)

- 27.09.2026 status: done — MB delegated the call to srom-typeset (D8 e).

Kanon § 3.4 now has an exception. An outside label for a group, in a foreign language and not assimilated in
Polish (neither spelling nor inflection), is a foreign word, not a proper name, in a Polish text: *Ciganos*,
*Gitanos*, *Bohémiens*, *Zigeuner*, *Tsiganes* are **italic every time, also when the word itself is discussed**.
Endonyms (Calon, Sinti, Kelderasze) and assimilated exonyms (Cyganie, Bosza) stay roman. Cross-references in
§ 6.2 and § 6.3, rationale in § 14, entry in § 17 (1.6); RULES.md § 3 and § 6 carry the digest. Commit 2830033.

## T7 — re E10: translator in the front matter — done (27.09.2026)

- 27.09.2026 status: done on the srom-typeset side. Your side: please write `tlumaczenie:` into `<id>_pl.md` and add a
  case to `tlumacz-test_handoff.py` (contract rule: changes are tested on both sides).

Contract (`handoff.md`, `srom-md.md` "Front matter"): YAML at the very top of `<id>_pl.md`,
`tlumaczenie: "Imię Nazwisko"` (a list if several). Not printed. The build lists it in `_report.md` under "Header
data" as `translators_struct` (`Imię|Nazwisko||`, split at the last space; ` ;; ` between translators). An empty
value fails the build. It survives the Word working copy: stored as the custom property `srom-tlumaczenie` and
restored on import (pandoc alone drops it). The handoff check ignores it. srom-typeset `test_e10.py` 9/9. Your
`tlumacz-test_handoff.py` rerun after this: HANDOFF CONTRACT 14/14.

## T8 — re E11: kartoteka created; one question for you (27.09.2026)

- 27.09.2026 status: done — MB delegated D9: `srom-kanon/references/kartoteka.tsv`, your 35 seed rows with your
  columns plus `italic_house` (y/n, the house rule from vol. 19). The 5 foreign exonyms are `y`; your `TS` flags are
  resolved (note says E12). A test checks the structure and that § 3.4's examples match the `y` rows.

Question: **Nawar, Gurbati, Halabi** — are these self-designations (endonyms, roman) or outside labels (exonyms,
italic if not assimilated)? I did not guess: they carry the flag `E12` until you check the Dom source (and your
`SV` note says they appear only in the Polish). Answer as an E-item; I update the kartoteka. Changes to the
kartoteka go through `_handoffs/`, like the Kanon.

## T9 — re E13 and T7; state of D1–D3 (27.09.2026)

- E13 — 27.09.2026 status: done. Nawar, Gurbati, Halabi → `italic_house = y` in the kartoteka (your sources in the
  note). Borderline cases, under § 3.4 as written ("nieprzyswojone ani w pisowni, ani w odmianie": assimilation in
  either counts): **Mutribowie** (inflected), **Gadżar** and **Garaczi** (Polish spelling) are assimilated → **roman**.
  The Kurdish-branch names (Mıtrıp, Karaci, Qarach, Suzmani/Sozmani, Domlar) have no vol. 18 Polish form, so no
  rows yet; when one appears in a translation, the same test applies (Polish form unadapted → italic).
- T7 — noted: your side tested, HANDOFF CONTRACT 18/18.
- For your pending list: D1 and D2 are **closed** (yes, as implemented); D3 is deferred by MB until stages 1–2
  are tested. `MB-decisions.md` was cleaned up at MB's request: open items at the top, closed ones as one line
  each, full text in `MB-decisions-archive.md`. Next free D-number: D10.

## T10 — news: first real source (Ndiaye, RQ 2022) and what changed for sources (27.09.2026)

- 27.09.2026 status: news, no action needed yet. The stage-1 test on MB's PDF (Ndiaye, "Black Roma", *Renaissance
  Quarterly* 75, 2022) is done in srom-typeset; the source goes to you after MB answers its queries.
- What you will see in sources keyed from short-form notes (`srom-typeset/references/srom-md.md`, "Keying
  short-form notes"): pages as `s.` with ranges in full; non-page locators in braces with Polish labels
  (`{ks. 11, rozdz. 2}`, provisional `{akt 4, sc. 1, w. 883}` pending MB); lead-ins zob./zob. też/por.; other
  lead-ins ("Quoted in") left for you.
- Kanon § 3.2 now says ranges are always written in full (MB, 27.09.2026); `normalize.py` rule RANGE-FULL
  expands elided ranges in the translation (logged).
- The editor's source proof is now `build.py --source` (handoff.md): the source's own typography is counted, not
  reported as errors. No change to what you hand back.

## T11 — contract: front matter to you; cyt. za; whole bibliography (28.09.2026)

- 28.09.2026 status: needs your side — `handoff.md` changed (srom-typeset tests green); please add the front-matter
  step to your skill and a case to `tlumacz-test_handoff.py`, then answer with a status line.
- **Out:** `<id>_src_front.md` — the original's title, author/affiliation, abstract, keywords (if any), as in the
  source. **Back:** `<id>_front_pl.md` — Polish title (title and subtitle kept apart), Polish abstract, Polish
  keywords (Kanon § 12.2.2; the English ones stay as in the original). Header data for the CSV, not built.
- Lead-in "quoted in / cited in" → `cyt. za` (Kanon § 7.2), in the source already.
- Kanon (MB 28.09.2026): the author's whole bibliography is printed, cited or not (§ 9.2); access dates and ISBNs
  only when the author gives them (§ 8.6, 9.7); non-page locators with Polish labels (§ 7.2: `akt 4, sc. 1, w. 883`,
  `k. S2r`, `ks. 11, rozdz. 2`); early prints without printer: no marker (§ 0).
- Fixed: a title inside an italic title was printed italic in every build (the report said roman). Proofs you
  have seen may show it wrong.

## T12 — source ready: Ndiaye, "Black Roma" (RQ 75, 2022) (28.09.2026)

- 28.09.2026 status: ready for you — please confirm receipt with a status line; queries go in an E-item.
- Files (read-only for you; `srom-typeset/work/ndiaye/`, git-ignored): `ndiaye_src.md` (text, 133 notes, every
  reference a token), `refs.json` (84 works, the author's whole list, audited), `ndiaye_src_front.md` (title,
  author, abstract, licence line — for `ndiaye_front_pl.md`, T11). For reference: `build/ndiaye_src_korekta.docx`
  (the Polish apparatus as it will print), `ndiaye_queries.md` (what MB decided on this article).
- Checks at hand-off: `cite_map audit` OK, `check.py --keyed` OK against the PDF text, `check.py` OK,
  `--pair` of the source with itself OK, Word round trip identical.
- In the source, as the author has it (Polish form comes with the translation and `normalize.py`): English quotes,
  closed em dashes, markers after the full stop, ". . ." omissions (normalize makes them `[…]` and logs them),
  elided ranges in running text (normalize writes them in full).
- Structure: title note (acknowledgements) `::: przypis-tytulowy`; 5 verse quotations (`>` lines with `\`);
  3 figure captions `::: podpis` ("Figure n." → Polish caption form, Kanon § 10); headings in capitals (h1).
- Tokens carry Polish apparatus already: `s.`, `zob.`, `zob. też`, `cyt. za` (note 30), `{ks. 11, rozdz. 2}`
  (note 23), `{akt 4, sc. 1, w. 883}` (notes 90–91), `{k. S2r}` (notes 82–83), `{w. 93–96}` (note 70).
- Titles in refs.json stay as published (Kanon); inner titles are marked and print roman.


## T13 — re E14: front-matter format; Romni/Gadje and "Egyptians" go to MB (28.09.2026)

- E14 — 28.09.2026 status: (1) done — noted; (2) and (3) needs MB (`MB-decisions.md` D13).
- T11 — your side confirmed: `tlumacz-front_check.py` → FRONT OK on `ndiaye_front_pl.md`, `tlumacz-test_handoff.py`
  → 23/23 (run here 28.09.2026).
- (1) The build does not read `<id>_front_pl.md`; it is header data for the CSV (stage 3 / curator). Your checker's
  docstring is the format. If the build ever reads it, I say so here first.
- (2) Not settled here: no evidence for a Polish spelling of *gadjo* in our files. What vol. 18 (binding, § 12.2) does
  have: **Romka, Romki** and **nie-Rom, nie-Romowie**; no *Romni*, no *gadźo/gadzio/gadżo*. Classification (my
  reading): Romni/Romnia/gadjo/gadji/gadje are Romani common nouns (§ 5.1: italic at first occurrence), not group
  names; the kartoteka (group names, § 6.3) covers them only if MB rules they are group designations. Options and my
  recommendation are in D13. Until MB decides, keep what you have and mark it (`<!-- DO SPRAWDZENIA: D13 -->`).
- (3) Kartoteka row `Egyptians → Egipcjanie (bałkańscy)` now says in its note: present-day Balkan group only, not the
  early-modern designation of Roma. The historical Polish form is not added: the kartoteka holds settled forms only
  (`test_kanon.py`), and there is no evidence yet. In D13.

## T14 — re E15: build crash fixed; one title-note block; lint cleared (28.09.2026)

- E15 — 28.09.2026 status: done — (1) fixed, (2) contract changed (needs your side), (3) fixed.
- (1) `srom_post.lua` cut the no-page context and `short()` by bytes; both now cut by characters, and `build.py` reads
  pandoc's output with `errors="replace"`. Test: `test_e2e.py` (a note after 60× "ó"). Your draft builds without
  crashing, no wrapper needed: **`build_tolerant.py` can go.**
- (2) **Contract (`handoff.md`)**: one `::: przypis-tytulowy` block per article — the translation note first, the
  author's note on the title (acknowledgements) as a further paragraph of the same block; one `*` at the title
  (Kanon § 7.1: the title note takes the first asterisk). Two blocks are now an error in `check.py` (so `--pair`
  catches it) with that instruction. Pending MB's confirmation (D12). Checked here on a copy of your draft: with the
  two blocks merged, `ndiaye_pl.md` + both refs files → build exit 0, no errors, asterisk notes 3 = 2 + 1.
  Please: merge the blocks in `ndiaye_pl.md`, add a case to `tlumacz-test_handoff.py`, and a status line.
- (3) BIB-COLON: the linter now takes a place as an imprint only when it opens an element (after `, ` `. ` `; ` or
  `(`) — "*Black Roma: Afro-Romani…*" in your note no longer fires. SPACE-BEFOREPUNCT (4×): the ". . ." in the
  Ruggle title were omissions in the author's list → `[…]` (Kanon § 3.5, § 4.1; the words unchanged).
  **`refs.json` changed** — please re-copy: sha256 `6a05800129d01caf631c575c9184f066f9eacc79f0f3be364834fb1956ad988a`
  (audit OK, `check.py` OK, `--source` build 0 errors). With it your draft's build shows 0 lint errors.
- For information, from the stage-1 review: `normalize.py` RANGE-FULL skipped a range right before a full stop
  ("s. 214–31." stayed); fixed. `normalize.py` runs here on the returned translation, so nothing for you to do.

## T15 — MB's decisions on D12–D14 (28.09.2026)

- 28.09.2026 status: decided by MB — please apply to the Ndiaye draft and confirm with a status line.
- **D12:** one title note (Kanon v1.7 § 7.1): translation note first, the author's note on the title as a further
  paragraph of the same `::: przypis-tytulowy` block. Contract in `handoff.md` is now final (see T14).
- **D13:** Romni → **Romka**, Romnia → **Romki**, Rom/Roma → Rom/Romowie (kartoteka rows added);
  gadjo / gadji / gadje **kept** as Romani words: lower case, italic at first use (§ 5.1), the author's spelling;
  note 1 keeps her list of Romani words in the original. Early-modern "Egyptians" / *Égyptiens* → „Egipcjanie” in
  quotation marks (kartoteka note); an Old Polish attestation is still welcome if you find one.
- **D14:** Kanon is now **v1.7** (the 27–28.09 rulings in their own changelog row, plus the one-title-note sentence).

## T16 — re E16: Word round trip keeps the one title note; cross-module review 28.09.2026 (28.09.2026)

- E16 — 28.09.2026 status: done — fixed in `docx_in.py` (commit ce291a2); your test reports `GAP CLOSED ok E16`,
  **HANDOFF CONTRACT 30/30** (run here with the venv, read-only).
- **E16.** Word styles are per paragraph, so every multi-paragraph `:::` block came back as one block per paragraph.
  The importer now re-joins consecutive paragraphs of one block style: `przypis-tytulowy`, `nota`, `motto`,
  `motto-zrodlo`, `dialog`, `bez-wciecia`. `podpis`, `tabela-*`, `przyklad` and `mowca` stay one block each (two
  adjacent captions are two captions). Tests: `test_roundtrip.py` +3, all failing on the old scripts.
- **Two more round-trip faults found on your draft**, both fixed:
  (a) `[@molier1922] <!-- DO SPRAWDZENIA: S2 … -->;` came back as `[@molier1922] ;` (Word drops the comment, keeps
  the space; the linter then fails the build: 2 errors on `ndiaye_robocza_v2.docx`). Export now anchors such a
  comment after the punctuation; import also closes `[@key] ;` left by older exports, so MB's v2 file is fine.
  (b) `::: mowca` lost the line break between speaker and affiliation (not in Ndiaye).
- **Measured on MB's file:** `ndiaye_robocza_v2.docx` → `docx_in.py` → `check.py --pair ndiaye_src.md …
  --refs refs.json --refs ndiaye_refs_tlum.json` → CHECK OK (1 title-note block; before: CHECK FAIL 1) →
  `build.py … --pair-src` → PASS, Errors: none. Your own `ndiaye_pl.md` → working copy → import → build: printed text
  identical to the direct build.
- **Comments never block** (review row 2): the contract (`handoff.md`) and `build.py` were right; my `SKILL.md`
  and `srom-md.md` said the opposite and are corrected. S1–S7 stay yours to track in `ndiaye_uwagi.md`: the build
  lists comments as a warning in `_report.md`; after the Word round trip only `_import.md` lists them.
- **T11 docs**: `handoff.md` now says the format of `<id>_front_pl.md` is your `tlumacz-front_check.py` docstring;
  `SKILL.md` scenario C names `<id>_src_front.md` out and `<id>_front_pl.md`, `<id>_refs_tlum.json`, `--pair-src`
  back. No change in behaviour.
- For information: srom-kanon SKILL.md quick rule 9 now carries the § 3.4 foreign-exonym exception; Kanon § 17
  moves the 27.09 exonym rule and the kartoteka file into row 1.7 (text of the rules unchanged, still v1.7);
  MB-decisions D15 (licence ND option) and D16 (vol. 18 copyright clause) added from Kanon § 13.2.

## T17 — re E9: typed notes in DOCX sources — `docx_in.py --typed-notes` (28.09.2026)

- E9 — 28.09.2026 status: done — built and tested; the Dom file converts. Scenario C can now freeze a source like it.
- `docx_in.py art.docx -o art.md --typed-notes`: superscript body digits + each page's typed note paragraphs → real
  notes, **labelled with the source numbers** (labels = printed numbers, as the contract expects). It pairs in
  sequence, splits a note typed inside another, joins a note's continuation lines, joins body paragraphs split by
  a page break, drops page-ID-only lines. It never guesses: every repair, gap and unpaired number goes in `_import.md`
  and makes the import say IMPORT CHECK. A file that already has real Word notes is refused.
- **Dom file** (sha256 c720b1a2…): 52 notes paired; independent check against the DOCX (note openings and the word
  before each marker): **52/52 right**. Listed for MB/you:
  (1) **a page is missing from this file**: the text breaks off at "…whether and how the Dom communities from" and
  resumes at "anthropology, an example of people…"; notes **49 and 50 and their markers are on that page**. Not in the
  DOCX at all; needs the PDF or the 2025 *Kulturní studia* version you found (E13).
  (2) marker **48** was typed at a paragraph start ("48. In the case…"): repaired to "…appellation[^48]. In the
  case…" — to verify against the PDF.
  (3) note 2 was inside note 1's paragraph (your E9 correction): split off.
  12 page-split paragraphs joined, all listed. No page-ID strings in this file (the `900430271992` in your E9
  correction must come from another rip; the importer drops such lines and flags ones glued to text).
- Result (git-ignored, for reading): `srom-typeset/work/dom/dom_src_typed.md` + `_import.md`. **Not frozen**:
  stage 1 (keying the 54 references into refs.json, check, T-item with sha256) waits until MB wants Dom translated
  and the missing page is supplied. One author-date leftover in the text: "(Szakonyi 2008: 8)".

## T18 — source ready: Pahulich, "Racialization of Roma, European Modernity, and the Entanglement of Empires" (CRS 8/1, 2025) (28.09.2026)

- 28.09.2026 status: ready for you — please confirm receipt with a status line; queries go in an E-item. MB's open
  points on this article (`pahulich_queries.md`) do not block your intake or draft; see "may still change" below.
- Files (read-only for you; `srom-typeset/work/pahulich/`, git-ignored), sha256:
  `pahulich_src.md` 11df7758…7145e17 (text, 146 notes, every reference a token), `refs.json` 6eefd2b4…292674c
  (52 works, the author's whole list, audited), `pahulich_src_front.md` 268810af…f3c08 (title, author, e-mail,
  affiliation, bio, journal line, abstract, 6 keywords — for `pahulich_front_pl.md`, T11; **no licence line**: the
  PDF has none). For reference: `build/pahulich_src_korekta.docx` (the Polish apparatus as it will print),
  `pahulich_queries.md` (MB's open points and what was settled).
- The original is **author-date**; converted to notes (Kanon § 7.1): 142 converted + the author's 4 (now **2, 37, 67,
  128**); labels = printed numbers (`cite_map --renumber`, new). The author's acknowledgements (an end section) are now
  the title note `::: przypis-tytulowy` — your translation note goes first in the same block (D12).
- Checks at hand-off: `cite_map audit` OK; `check.py` OK; `--pair` of the source with itself OK; Word round trip
  identical (bar the two comments, which become Word comments); every word compared with the PDF: nothing lost.
- In the source, as the author has it: English quotes, markers after the full stop, "Ibid." gone (resolved to tokens,
  the build decides *Ibidem*), `– ` spaced dashes, "[G]ypsies" (the author's bracket, § 4.1), "racial/ human" and
  "“Zigeuner”/ “Gipsey,”" with the space the PDF has.
- Notes whose wording is not the author's sentence as printed: **6** "For similar inquiry, [zob. @parvulescu2022]."
  and **144** "[Zob. też @thomas2018] on Soviet politics …" (prose from a parenthesis, lead-in keyed); **37** keeps the
  author's "(1992, 81)" with no author name (question to the author, D1 in the queries; comment in the text).
  "Jenkins and Leroy (2021)" in section 3 is not in the bibliography: left as text, with a comment (D2).
- refs.json: Cyrillic in **ALA-LC** (Kanon § 9.6; the author uses another romanization, kept in `srom-as-written`),
  checked against catalogues except Chėrvinski 2008. **Title glosses in [ ]** (`original-title`) are Polish, my
  translations of the original titles: please review them; changes as query rows (`adresat;rodzaj;przypis;dzieło;
  szczegóły`), since refs.json is mine. Running-text names from Cyrillic (Dal’, Barannikov, Kistyakovsky, Zelenchuk…)
  are yours to transcribe (PWN), as usual.
- For your § 12.2.4 check (information, not verified by me): the Polish sources in section 3 (Przyłuski 1553, Bielski
  1564, the 1510 and 1578 Diet acts, the chancellor's letter 1553) are quoted via Mróz 2015 (CEU Press); Mróz also has
  a Polish book on the same material, *Dzieje Cyganów-Romów w Rzeczypospolitej XV–XVIII w.* (2001) — whether it holds
  these passages I have not checked.
- May still change after MB (`pahulich_queries.md`): A2 — if MB merges printed notes 1 and 2 (a citation next to the
  author's note), notes renumber from 2 on (145); B/C — refs.json fields only (tokens and keys stay); A1 — the
  original is **CC BY-NC 4.0** (Crossref), MB decides on consent/NC before publication (your translation note's
  licence line). Any change comes as a new T-item with new sha256.

## T19 — source ready: Ostendorf, "Familiar Outsiders Abroad" (The Romani Atlantic, CUP 2026, ch. 3) (28.09.2026 17:40)

- 28.09.2026 status: ready for you, **rights pending** — please confirm receipt with a status line; queries go in an
  E-item. The chapter is © Cambridge University Press, not open access: MB decides (`MB-decisions.md` D19 A1) whether you
  start before CUP and the author give permission. Nothing else in D19 blocks the translation.
- Files (read-only for you; `srom-typeset/work/ostendorf/`, git-ignored), sha256:
  `ostendorf_src.md` 66aa4b80…710e5ae (text, 5 sections, 62 notes: 54 keyed, 2 of them partly literal; 8 literal),
  `refs.json` 81e15276…c25dca5 (83 works, typed from the notes: the chapter has no bibliography),
  `ostendorf_src_front.md` 3c6ffd4b…b926eec (title with subtitle, author, the book line from Crossref; **no abstract, no
  keywords, no affiliation** in the original → Kanon § 12.2.2: you draft abstract and keywords, Polish and English; the
  author approves the English). For reference: `build/ostendorf_src_korekta.docx` (the Polish apparatus as it will
  print), `ostendorf_queries.md` (MB's points, verified slips, questions to the author).
- The original: a book chapter with Chicago full notes, labels = printed numbers 1–62, no title note (your translation
  note is the only one; the first-edition description needs the place of publication, D19 A2/A5).
- Checks at hand-off: `check.py --keyed` OK (now reading Chicago pages), `check.py` OK, `--pair` with itself OK, Word
  round trip identical (bar the two comments), every word and number of the PDF in the extraction (its text layer had no
  digits and no small capitals; the digits were verified against the PDF's link targets).
- Literal notes (Kanon § 8): archival 29, 32 and the first half of 30; press 49, 50, 52, 53, 54, 59 (19th-century US
  newspapers — the § 8.3 date form is yours); note 14 keeps the URL of the digitised Schmidl manuscript. Author's prose
  inside notes: 11, 12, 14, 38; lead-ins in 5, 11, 52 ("see" → zob.).
- Two comments in the text (DO SPRAWDZENIA, D1 and D2 of the queries): the year of Moreno Alonso's "journey" (1747 vs
  "1745" in note 25) and Penn's "1686 promotional tract" (note 35: 1683). Translate as printed until the author answers.
- Group names: the author italicises *Bohémiens*, *Zigeuner* but not Gitanos/Ciganos (italic in the kartoteka, T6). Not in
  the kartoteka: *cingani*, *Zingaros*/*Zingari*, *Zingances*, *Chinganéros*, *Bohemes*, "Gipsies" (variant),
  "Anglo-Romani" — yours to settle before delivery (§ 12.2.6), via E-items. Early-modern "Egyptians" → „Egipcjanie” (D13).
- May still change after MB: B-items (refs.json fields only; tokens and keys stay — except B3, note 26, where the key
  `poisson1900` stays and gains an author), A2 (places/publishers filled in refs.json), A3 (how an edition's editor
  prints). Any change comes as a new T-item with new sha256.

## T20 — [Tittel] source ready: "Racial and Social Dimensions of Antiziganism" (On_Culture 10, 2020) (28.09.2026 21:09)

- 28.09.2026 21:09 status: ready for you — please confirm receipt with a status line; queries go in an E-item. Rights are no
  obstacle: the journal is CC BY 4.0, the author keeps copyright (MB to confirm the licence on the repository record,
  `MB-decisions.md` D20 A2); the translation note follows the Kanon § 12.2.3 formula for CC BY 4.0. Nothing in D20 blocks
  the translation.
- Files (read-only for you; `srom-typeset/work/tittel/`, git-ignored), sha256:
  `tittel_src.md` 0a366130…ac36a43 (text, 5 sections, the title note + 100 notes: 97 keyed, 25 of them partly literal;
  3 literal), `refs.json` d83fe96e…035c459 (63 works, typed from the notes: no bibliography in the original),
  `tittel_src_front.md` 81522b81…c42c891 (title, author, affiliation, the journal line with URN — **no DOI** —, the
  English abstract and 6 keywords: you draft the Polish ones, Kanon § 12.2.2). For reference: `build/tittel_src_korekta.docx`
  (the Polish apparatus as it will print), `tittel_queries.md` (MB's points, verified slips, questions to the author).
- **Note numbers: labels 1–100 = the numbers SROM prints; the original's note = label + 1.** The original's note 1 (the
  author's acknowledgements, called from the first sentence) is the `::: przypis-tytulowy` block at the top (Kanon § 7.1;
  D20 A1, provisional): your translation note goes first in that block, the acknowledgements after it (D12).
- Checks at hand-off: `check.py --keyed` OK (mutation-tested), `check.py` OK, `--pair` with itself OK, Word round trip
  identical (bar one comment), every word and number of the PDF in the extraction.
- Literal notes: 38, 48, 56 (the author's prose). Partly literal: the German originals quoted in 37 and 81–93, 95 ("Original:
  „…”" + the keyed citation) and the author's "(my translation)" (14, 37, 81, 95); prose around citations in 8, 17, 21–23,
  26, 41, 47, 49, 64. Lead-ins are already zob./por./zob. też.
- One comment in the text (DO SPRAWDZENIA, D20 A4): n. 49 "(hereafter abbreviated as MEW 23)" points to nothing once the
  MEW notes print the short form; MB's recommendation pending — leave the parenthesis out unless MB decides otherwise.
- Kanon § 12.2.4 a (Polish editions) is yours: quotations from Kant (block quotes in section 2: *Anthropology*,
  *Determination of the Concept of a Human Race*, *On the Use of Teleological Principles*; short ones from *Of the
  Different Races* and *Religion within the Boundaries*), Marx (*Capital* I, *Grundrisse*, *German Ideology*),
  Horkheimer/Adorno; the English statutes (1494, 1530, 1554, 1562) and the Württemberg edicts (German originals in the
  notes, the author's English in the text) — § 12.2.4 on translating from the original.
- Group names: the author writes “gypsy/gypsies” in scare quotes, lower case, throughout (the term under discussion), and
  Sinti, Roma; *Egyptians* (italic, the English acts) = early-modern „Egipcjanie” (D13, kartoteka); *Zigeuner*, *Zigeiner*
  in German titles and quotations; "Porrajmos" (text, section 5); "vagabonds", "vagrants". The form of the scare-quoted
  “gypsy” in Polish (Cygan/cygański in quotation marks? lower case?) is yours to settle before delivery (§ 12.2.6), via E.
- May still change after MB: D20 A1 (title note — labels would go back to the original's 1–101), A3 (Ruch's university in
  refs.json), A6 (places with slashes, sections of the bibliography), B-items (refs.json fields only; tokens and keys stay).
  Any change comes as a new T-item with new sha256.

## T20 — Ostendorf (T19): corrections after MB's answers; list for the translation stage (28.09.2026 21:28)

- 28.09.2026 21:28 status: ready for you — please confirm with a status line. Supersedes T19 where they differ.
- **Rights corrected: open access, CC BY-NC 4.0** (Cambridge Core chapter page; book copyright page "© Cambridge University
  Press & Assessment 2026"; OA funder: Institute of Ethnology, Czech Academy of Sciences). T19's "rights pending / not OA"
  was my error. The NC question is MB's (D19 A1, as Pahulich D17 A1); it does not hold up the translation. Your translation
  note: licence + "przekład stanowi zmianę utworu" + the copyright notice (§ 12.2.3).
- **The original has a summary and 10 keywords** (on Cambridge Core, not in the PDF): now in `ostendorf_src_front.md`
  (new sha256 below). So: translate the summary; Keywords "jak w oryginale" — nothing to draft. Affiliation: Gonzaga
  University. The first-edition description: "…, Cambridge University Press, Cambridge 2026, s. 86–108, DOI: 10.1017/
  9781009706032.005".
- Files: `ostendorf_src.md` unchanged (66aa4b80…710e5ae); `refs.json` 0704415d…f4d45c5 (44 places/publishers sourced from
  the LoC catalogue, evidence in `srom-sourced`; "de la Fuente" as a dropping particle; Hálfdánarson as a literal name);
  `ostendorf_src_front.md` ce7860cc…2bdc9f0. Keys and tokens unchanged.
- Kanon (commit ea50df6, supplement to v1.7): § 7.2/§ 9.4 edition of a source (`red.` after the title), `tłum. i red.`,
  unsigned text in a collection; § 9.3/§ 9.5 names with particles by their language ("A. de la Fuente", short "Fuente";
  "Hippel, Wolfgang von").
- **Please remind MB at the translation stage** (MB's instruction: flag to you, decide then) — detail in
  `ostendorf_queries.md` B and D: B1 Galletti "Hispanoaméria"; B2 Fotta's year/pages (FirstView); **B3 note 26 is a letter
  by Paul du Poisson** ("Lettre au Père ***", verified in Thwaites vol. 67 — the build lists it as a text without an
  author); B4 "Cambell" → Campbell; B5 "New Granada" → Grenada; B6 Paucke's publisher (Wien, W. Braumüller); B7 "de
  Litoral" → del Litoral; B8 "Notes and Documents:"; B9 Matache 2026/2025; B11 Matthews (I.B. Tauris), Block (2018),
  Muhlenberg (publisher), O'Reilly's volume (PLUS), Guðmundur Hálfdanarson; D1 1747/1745 and whose journey (comment in the
  text); D2 Penn 1686/1683 (comment in the text); D3 Fotta's print pages; D4 Urlsperger's volume; D5 Tucker's volume.
- Still open for MB (typesetting only): 14 imprint gaps to be filled by hand (D19 A2).
- T20, correction 28.09.2026 21:29: refs.json has **43** sourced values (not 44); 14 gaps remain for MB. sha256 unchanged.

## T21 — [Ostendorf] renumbering: the second "T20" above (21:28, "Ostendorf (T19): corrections…") is T21 (28.09.2026 22:57)

- 28.09.2026 22:57 status: information — two srom-typeset sessions both used T20. **T20 = [Tittel]** (21:09); the Ostendorf corrections
  (OA licence CC BY-NC 4.0, summary and keywords in `ostendorf_src_front.md`, refs.json 0704415d…f4d45c5, the B/D list to
  remind MB of at the translation stage) are **T21**. Please cite them as T21 in your status lines.

## T22 — [general] InDesign styles renamed (house style v3); nothing to do on your side (29.09.2026 03:39)

MB's style discussion (29.09.2026): the InDesign style set is rebuilt from vol. 18's own values (commit 81babb2).
The DOCX from `build.py` now names the v3 styles, so build reports and `_postimport.jsx` show new names:
*Przypis GWIAZDKOWY* (was *Przypis gwiazdkowy*), *Gwiazdka* (was *Odsyłacz gwiazdkowy*), *Tekst BEZ WCIĘCIA*,
*Śródtytuł*, *Cytat* … The handoff contract (`handoff.md`) names no InDesign style and is unchanged; SROM-MD is
unchanged. One build change you may notice in proofs: a bulleted list item now carries a typed "–" + tab (as a
numbered item carries "1." + tab). Suite: SUITE ALL PASS 19/19.

## T23 — [West Ohueri] source ready: "Peripheral whiteness and racial belonging and non-belonging: accounts from Albania" (Off White, MUP 2024, ch. 6) (29.09.2026 04:13)

- 29.09.2026 04:13 status: ready for you, **rights block publication** (CC BY-NC-ND 4.0: ND forbids sharing a translation without
  permission — MB decides whether you start before permission, `MB-decisions.md` D24). Please confirm receipt with a
  status line when MB schedules it; queries go in an E-item.
- Files in `srom-typeset/work/westohueri/`: `westohueri_src.md` 39a9c1f4…fa73a1eb (6 sections, 68 notes — endnotes in the
  original, footnotes here, labels = printed numbers 1–68; 65 keyed, 3 literal: nn. 29, 33, 49), `refs.json` 2a36e666…f73a1eb
  (51 works typed from the notes; the chapter has no bibliography), `westohueri_src_front.md` 10320303…77006523 (title,
  author, book, licence, the online abstract — 1,508 characters, § 12.2.2 — and 10 keywords; affiliation and copyright
  line still missing: MB), `westohueri_queries.md` (A–E; **E is for you**: group names and Albanian words not in the
  kartoteka — *jevg*/*jevgjit*/*evgjit*, *gabel*, *dorë e bardhë*/*zezë*; Balkan Egyptians = kartoteka „Egipcjanie
  (bałkańscy)”; Gheg/Tosk; "Vaso Pasha"; n. 26 prints the author's name twice). Word copy `westohueri_src_robocza.docx`,
  proof `build/westohueri_src_korekta.docx`.
- Three DO SPRAWDZENIA comments in the text: the unsourced Tosk quotation (before n. 53, queries D1), n. 29 "Baker, this
  volume" (A4: I propose citing her chapter; until MB approves the note stays literal), n. 49 the forthcoming book (D2).
- Fieldwork: the three interlocutors' statements are block quotations without italics (Kanon § 4.1; italic in the
  original), no interview codes (none given); § 12.2.4 c — one formula in the note.
- New for you in the source: the author's text uses 'single quotes' (British); the query sheet now reads them as
  quotations. Build change you may notice: an Ibidem after a lead-in whose sentence goes on ("Zob. Ibidem, gdzie …") is
  printed as the short form (Kanon § 7.3; commit 4a088a2). Contract (`handoff.md`) unchanged. Suite: SUITE ALL PASS 19/19.
- T23, correction 29.09.2026 04:13: `westohueri_src.md` is **39a9c1f4…16008fd21** (the value above was refs.json's ending); `refs.json`
  2a36e666…0fa73a1eb. Full values: `shasum -a 256` in `srom-typeset/work/westohueri/`.

## T24 — [West Ohueri] source re-frozen after MB's answers; mutation test per text (29.09.2026 04:42)

- 29.09.2026 04:42 status: ready for you (supersedes T23 where they differ); rights unchanged — MB is asking for permission (ND), MB
  says when you start. Please confirm with a status line when you take it.
- Files in `srom-typeset/work/westohueri/`: `westohueri_src.md` 80964b34…598bd7be, `refs.json` 224e6627…2f332e0d951,
  `westohueri_src_front.md` be23da23…ec79bb3e9 (full values: `shasum -a 256` there).
- MB's decisions (D24): n. 29 "see also Baker, this volume" is keyed to Baker's chapter in the same book (`@baker2024`;
  note: "On mythologies of warfare against the Ottomans, zob. też [@baker2024]."); the author's name is **"Ohueri, Chelsi
  West"** (notes print "C.W. Ohueri", short form "Ohueri"); block quotations are roman except what the Kanon italicises
  inside them — in the three fieldwork statements the Albanian words are now italic (*Jevgjit*, *jevgjit* ×2,
  ‘*je bere si jevg*’). The main text keeps the author's roman ‘jevg’ in quotation marks: § 3.4 at your stage.
- The publisher's HTML full text (found by MB) agrees with the source word for word and in italics.
- Procedure (MB): every keyed source now gets a mutation test (`scripts/mutate_keyed.py`, SKILL.md step 4b); all five
  keyed sources 40/40 after two more `check.py --keyed` fixes (commit 42a2397). `handoff.md` unchanged.

## T25 — re E17 [Ostendorf], E18 [Pahulich], E18 [Ostendorf], E19 [Tittel]: kartoteka, title glosses, Urlsperger, MEW page (29.09.2026 17:52)

- 29.09.2026 17:52 status: ready for you. Only **Pahulich's refs.json** changes (new sha256 below); no source, key or token changes
  anywhere, so none of the four Word copies is affected.
- **Kartoteka** (srom-kanon `references/kartoteka.tsv`, commit 4187da2, 42 rows), for E17 (1) and E18 [Pahulich] (2):
  *Anglo-Romani* → „angielscy Romowie” (roman; the people, not the language Angloromani), as your draft has it;
  *Bohémienne*, *Bohémiennes* = variants of the *Bohémiens* row (italic, French form and gender). Where the author writes
  "Bohémien" of a woman (Gaspart), changing it is MB's call (D22), not the kartoteka's. *Manoush* = variant of Manush →
  Manusze. New italic rows (foreign exonyms, § 3.4): *cingani*, *Zingari* (variant *Zingaros*, each passage keeps its
  form), *Zinganées*, *Bohèmes*. Also variants *Gipsies* (Gypsies), *Gitano* (Gitanos), *Zigeiner* (Zigeuner, Tittel).
  No row: *Chinganéros* (Vowell's Creole minstrels, not a Romani group; a foreign word in a quotation, italic, § 5.1);
  *Bohemian* inside the quoted marriage record; *Indio*, *de nación …* (Spanish words, italic). Tittel "gypsy": no row
  needed, agreed (D25 a).
- **Two slips found while checking E17** (`ostendorf_queries.md` B13, B14; MB decides with the B list, D19):
  **B13** before n. 60, Vowell 1831, Notes p. 324 (note 14), page image read: "resemble **those of** the *Zinganées*, or
  Eastern gypsies". The author has "the *Zingances*". *Chinganéros* is as printed. Your translation follows the original
  (§ 12.2.4), so *Zinganées*, flagged, unless MB says otherwise. **B14** *Bohemes* → *Bohèmes* (your reading of the 1803
  print; I did not re-check it).
- **E18 [Pahulich] (1), title glosses: all five applied** as you proposed (chervinski2008, horvathova1964, zinevych2001,
  dal1883 with subtitles; kirei1984 „…etnografii rodzimej”). `work/pahulich/refs.json` **3b060a87…1f3d5366** (was
  6eefd2b4…292674c). `pahulich_src.md` unchanged (11df7758…7145e17). Checked: `check.py` CHECK OK; proof rebuilt;
  your `pahulich_pl.md` with the new refs.json: `check.py --pair` CHECK OK, `build.py --pair-src --queries --draft` PASS,
  glosses in the output. Please re-copy the file and mark those five query rows done.
- **E18 [Ostendorf], Urlsperger (n. 41): the key `urlsperger1751` and the token `{t. 3, s. 979}` stay.** Nothing changes in
  `ostendorf_pl.md`. Verified (JCB Library record on archive.org, `derachtzehenteco00urls`): the work has three volumes with
  continuous pagination. Vol. 3 (collective title page 1752) holds Continuations 13–18, and the 18th runs pp. 777–1004. So
  the author's "3:979" is right, and her title ("… erster", 1751) is volume 1's. The record fix (whole work, Halle
  1741–1752) is **B12** for MB. refs.json fields only, no new sha256 until MB approves (then a T-item). Stage-1 D4 is
  answered. "Kühe" and Schmidl n. 14 stay with your query sheet / D22.
- **E19 [Tittel] (2), n. 49 MEW 743 → 741: verified** (mlwerke.de MEW 23 with page marks, Wayback capture; the live site is
  offline): the passage ends before ⟨742⟩. Now **D20 B11** (`tittel_queries.md`). The token stays `s. 743` until MB
  decides. If approved, a T-item follows for the source, and you change the token in `tittel_pl.md`.
- **E17 (2) / E18 [Pahulich] (3), Kanon § 12.2.4 c**: needs MB (D26 e). I put the proposed wording under D26 (e):
  „tłum. z przekładu angielskiego autora/autorki” (the author's own translation) vs „tłum. z przekładu angielskiego”
  (a published translation the author cites; the note points to it). Grellmann stays with D23 S10. Keep your drafts as
  they are.
- Suite: SUITE ALL PASS 19/19.

## Status of E17, E18 [Pahulich], E18 [Ostendorf], E19 [Tittel] (29.09.2026 17:52)

- E17 [Ostendorf] — 29.09.2026 17:52 status: done — (1) kartoteka rows (T25); (2) needs MB — the Kanon line waits for D26 (e), wording proposed; (3) noted.
- E18 [Pahulich] — 29.09.2026 17:52 status: done — (1) five glosses applied, new refs.json (T25); (2) Manoush row; (3) needs MB (D26 e, D23 S10); (4) noted.
- E18 [Ostendorf] — 29.09.2026 17:52 status: done — key and token stay; record correction B12 for MB (D19); D4 answered (T25).
- E19 [Tittel] — 29.09.2026 17:52 status: done — (1) no row, agreed; (2) D20 B11, verified; (3) noted, no Kanon line for titles as printed.

## T26 — [general] contract change: the hand-back (`handoff.md` "Back"), a delivery E-item, `take_back.py` (29.09.2026 17:58)

- 29.09.2026 17:58 status: ready for you. Contract change (review 29.09.2026 row 3), commit 6e9ea9e. Please align PLAN (OUT-*,
  IF-TYPESET) and HANDOVER, and add a delivery case to `tlumacz-test_handoff.py`. Answer with a status line.
- **What the contract now says** (`srom-typeset/.claude/skills/srom-typeset/references/handoff.md`, "Back", steps 1–4):
  1. You export `<id>_robocza.docx` into your `work/<id>/`, and MB edits it there. From his first edit that Word
     file is **the master**. Never re-export over it: use a temp dir or `_v2`, and MB says which file is the master.
     (This is what the review's row 2 is about: gates 1.5.4b/1.5.5b G8.)
  2. **You import** after each editing round (`docx_in.py` → `<id>_pl.md`) and run `check.py --pair`, `build.py … --draft`
     and `tlumacz-front_check.py`. The imported md is not edited by hand: corrections go into the Word file, and you
     re-import.
  3. **Delivery E-item** `## E<n> — [<Author>] delivery: …` with the sha256 (`first8…last7` or full) of every file:
     `<id>_robocza.docx`, `<id>_pl.md`, `<id>_front_pl.md` (required), `<id>_refs_tlum.json`, `<id>_pytania_tlum.csv` (when
     they exist). Also the sha256 of my `refs.json` you checked against, and your verdicts. A new round means a new
     item that supersedes the old one.
  4. **I take it back**: `take_back.py <srom-tlumacz>/work/<id> <id> --src-dir work/<id> --expect <file>=<sha> …`. It copies
     into my `work/<id>/pl/` (your folder is only read), compares the sha256, requires `<id>_pl.md` to be byte for byte a
     fresh import of the Word master, runs `check.py --pair` and writes `SHA256SUMS`. I build from `work/<id>/pl/` and
     answer with a status line.
- **Consequence for the current drafts**: today your `<id>_pl.md` files are the drafts the Word copies were exported
  *from*, not imports *of* them. On Ostendorf the re-import differs in 191 lines: the YAML list form of
  `tlumaczenie:`, and note labels, since Word renumbers `[^t1]` into the sequence. The build is identical: same text,
  query sheet and asterisk JSX (checked). So the md in a delivery must be `docx_in.py`'s own output, or
  `take_back.py` fails, by design.
- Test on my side: `tests/test_takeback.py` (19 cases: clean delivery, abbreviated and full sha256, a wrong or missing
  sha256, an md edited after the import, a missing front file, a note lost in Word, `--out` inside your folder refused,
  contract text). Your `tlumacz-test_handoff.py` against 6e9ea9e: **HANDOFF CONTRACT 30/30** (the lines you check are
  kept). Suite: SUITE ALL PASS 20/20.

## T27 — [general] Kanon v1.8 (29.09.2026 19:22)

- 29.09.2026 19:22 status: information. Commit 6890113: the three dated supplements of 28–29.09.2026 (§ 7.1, § 8.6, § 7.2/§ 9.4,
  § 9.3/§ 9.5, § 3.4 display elements) that were appended to v1.7 are now § 17 row **1.8**. No rule text changed.
  Please cite "Kanon v1.8" from now on. Later rule changes go into new version rows, each announced in a T-item.
  Suite: SUITE ALL PASS 20/20.

## T28 — [general] Kanon v1.9: § 12.3 Pisownia, the 2026 spelling (30.09.2026 00:06)

- 30.09.2026 00:06 status: action for you. MB (30.09.2026): the Rada Języka Polskiego spelling changes in force from 01.01.2026
  apply at once, to vol. 19 and every translation. srom-typeset 15ef855: Kanon **v1.9**, new § 12.3 (header, § 17 row
  1.9, RULES.md, SKILL.md agree). Please cite "Kanon v1.9" from now on.
- What it means for translations: `-owski` adjectives from personal names are lowercase whatever the meaning
  (`przekład molierowski`, `ujęcie kantowskie`, `opisami marksowskimi`); `nie` + inflected participle is joined
  (`nieznane`, `niekontrastujący`); names of inhabitants capitalised; `-by` after conjunctions separate. Quotations
  and titles keep the source's spelling. Vol. 18 house forms take the new spelling without a change of wording (not a
  terminology change: termbase and kartoteka rows keep their decisions).
- The linter now warns (WARN, never blocks): `ORTH-OWSKI`, `ORTH-NIE-IMIESLOW`. On your drafts today:
  Ndiaye 9 (Molierowski… ×8, "nie kontrastującego" ×1), Tittel 6 (Kantowskie/Kantowską/Kantowskiego,
  Marksowskie/Marksowskiego/Marksowskimi), Pahulich 1 (Grellmannowskiej), Ostendorf 0.
- Where to fix: the Word copy MB edits is the master (T26). If MB has started on a file, the fix goes into his Word
  file (tell him the places), not into `<id>_pl.md`; if not, fix the md and re-export to a new file, never over his.
- Tests: SUITE ALL PASS 20/20; your `tlumacz-test_handoff.py` against 15ef855: HANDOFF CONTRACT 33/33.

## T29 — [general] Kanon v1.10; pair-check length warning; lookup tools you can use (30.09.2026 02:17)

- 30.09.2026 02:17 status: information (one suggestion at the end). MB approved the root session's proposals (30.09.2026);
  srom-produkcja 53f3a07 and ab28b31. Please cite "Kanon v1.10".
- **Kanon v1.10, § 12.3**: compound conjunctions take no comma inside (`, mimo że`, not `mimo, że`; also `pomimo że`,
  `zwłaszcza że`, `szczególnie że`, `tym bardziej że`, `jako że`). Linter WARN `PUNCT-SPOJNIK`. Your four drafts: 0.
- **`check.py --pair`** now warns when a paragraph's target/source length leaves 0.8–1.25 of the text's usual ratio (a
  dropped or added sentence). Measured on your four drafts: 182 paragraphs of 300+ characters, all within 0.86–1.16,
  0 warnings. Advisory only; nothing blocks.
- **Tools you may use for OUT-REFS** (`<id>_refs_tlum.json`, data from a catalogue record): `lookup.py imprints
  <refs> --tsv …` reads the Library of Congress, DNB and BN (Polish National Library) catalogues and gives place and
  publisher with the record as evidence; `lookup.py dois <refs>` checks DOIs against their registry.
- **Suggestion for your interference checklist (leaf 1.3.4), no tool**: Zawisławska (Poradnik Językowy 2025) names two
  frequent errors a linter cannot see and translation from English invites: participial clauses with a different
  subject or no simultaneity (the English -ing clause: *Zliczając głosy…, zwycięzcą została…*), and foreign surnames
  left undeclined (*Pierre* for *Pierre'a*). Worth a line in your re-read.
- Tests: SUITE ALL PASS 22/22; your `tlumacz-test_handoff.py` against 53f3a07: HANDOFF CONTRACT 33/33.

## T30 — [general] master file name at delivery (01.10.2026 16:42)
Review 01.10.2026 row 4. `handoff.md` "Back" step 1 now says: at delivery the master is always named `<id>_robocza.docx`;
srom-tlumacz renames the editor's master (e.g. `ndiaye_robocza_v2.docx`) to that name and older exports to
`<id>_robocza_old<n>.docx`. `take_back.py` is unchanged. Action for you: align PLAN OUT-DELIVERY and `tlumacz-test_handoff.py`.

## Status of review 01.10.2026 (srom-produkcja, 01.10.2026 16:42) [general]
1. Guard fails closed: **done** — `[ -f "$H" ] || exit 0;` in `.claude/settings.json`; missing file → exit 0, real file runs (d3c3924).
2. Master file name: **done** (cheapest variant: rule in `handoff.md` "Back" 1, announced as T30; no `--master` option, no code change).
3. Kartoteka: **done** — *Anglo-Romani* row marked provisional pending OST-6; rows 42–43 cite `ostendorf_uwagi.md` OST-3.
4. Notes sheets in git: **done** — `.gitignore` un-ignores `work/*/*_uwagi.md`, six sheets committed. Keying scripts left out (not asked).
5. Stale text: **done** — CLAUDE.md, SKILL.md (no count), HANDOVER-produkcja (date, 22/22, ledger pointer), srom-quant label. `dist/*.skill` not rebuilt (only before an upload).
Suite: SUITE ALL PASS 22/22.

## T31 — [general] [Ostendorf] [Pahulich] Kanon v1.11 after MB's first InDesign test; two refs.json changed (02.10.2026 02:30)

- 02.10.2026 02:30 status: action for you (small). MB placed the Ostendorf draft in the v3 template (02.10.2026) and
  decided four rules; srom-produkcja 4e4186a: Kanon **v1.11** (header, § 17 row, RULES.md, SKILL.md agree). Please cite
  "Kanon v1.11".
- **§ 2: headings are never numbered**, even where the original numbers them. Your drafts write `# 1. WSTĘP`: the build
  now drops the number with a warning, so nothing breaks, but please stop adding numbers, and reword any cross-reference
  to a section number ("w części 3") — tell me if a text has one.
- § 2: one line before a heading and around block quotations — set by the template; nothing for you.
- § 7.1: the note number has no full stop after it (Footnote Options); nothing for you.
- § 9.1, § 9.3–9.5: bibliography without a comma after the surname (`Paucke Florian`); the CSL does it; nothing for you.
- § 7.2/§ 9.4: an anonymous edition of a source and an edited text in a journal open with the title, the editor after it
  ("*Mourt's Relation…*, red. H. Dexter"). Data, not your tokens: **[Ostendorf]** `refs.json` 566a17cc…574754ba
  (`mourt1865`, `clinton1849` → type `classic`); **[Pahulich]** `refs.json` 95e34fe8…6e02e7a (`kistiakovskii1879` →
  `classic`). Keys and tokens unchanged; please copy both into `work/<id>/src/` and verify (sha256) at your next intake.
  Who stands first in Ostendorf nn. 41, 51, 34 is MB's (OST-9).
- Tests: SUITE ALL PASS 23/23; your `tlumacz-test_handoff.py` against 4e4186a: HANDOFF CONTRACT 33/33.
- T31, correction 02.10.2026 02:30: [Ostendorf] the hash in the usual form is `566a17cc…74754ba` (first 8 … last 7).

## T32 — [general] [Ostendorf] [Pahulich] Kanon v1.12: the editor never stands first; refs.json again (02.10.2026 16:45)

- 02.10.2026 16:45 status: information (one intake step). MB's second InDesign test (02.10.2026): srom-produkcja 853dfeb, Kanon
  **v1.12** — the editor never stands in the author's place: an edited volume is "*Tytuł tomu*, red. A. Kowalski, …",
  its short form the title alone, sorted by title in the bibliography. The CSL does it; nothing in your tokens changes.
  Please cite "Kanon v1.12".
- T31's `classic` type is gone again (not needed now): **[Ostendorf]** `refs.json` 0704415d…fd45c5, **[Pahulich]**
  `refs.json` back to 3b060a87…1f3d5366 (the file you have from T25). Copy and verify at your next intake; T31's
  hashes are void.
- Tests: SUITE ALL PASS 23/23; your `tlumacz-test_handoff.py` against 853dfeb: see the status line you add.
- T32, correction 02.10.2026 16:46: your `tlumacz-test_handoff.py` against 853dfeb: HANDOFF CONTRACT 33/33. [Ostendorf] hash in the usual form: `0704415d…0fd45c5`.

## T33 — [general] [Ostendorf] [Pahulich] [Tittel] [Ndiaye] Kanon v1.13: translator's annotations reversed; refs.json (02.10.2026 18:56)

- 02.10.2026 18:56 status: action for you. MB's review of Ostendorf's INJECT build (02.10.2026), srom-produkcja e019316,
  Kanon **v1.13**. Please cite "Kanon v1.13".
1. **§ 12.2.4 c reversed (MB):** a quotation the author gives in English (her own translation or someone else's) is
   translated from that English **with no annotation**; the translation note's formula covers it. `tłum. z przekładu
   angielskiego (autorki)` is withdrawn (the linter now warns, TLUM-ADNOTACJA). An annotation stays only for
   (a) an existing Polish edition (always used when it exists, as before) and (b) a translation from the original,
   which is now made **only when it matters** (the English is doubtful or the wording carries the argument; MB's
   call): `[przekład z oryginału – przyp. tłum.]`, with the original's record when the author gives none.
   **Once per work:** later quotations from the same work on the same basis: short form, no annotation.
   Your drafts carry the old formula: [Ostendorf] 12 (nn. 11, 12 ×2, 16, 17, 18, 21, 23, 25, 29, 32, 33, 42),
   [Tittel] 3, [Pahulich] 3 — please remove them. [Ostendorf] the quotations you translated from the French,
   Spanish and German originals (`research/originals.md`): keep the original only where it matters (then one
   annotation per work), and the title note's extra clause on originals goes; the standard formula stays.
   MB-decisions: GEN-11 and PAH-4 removed (settled by this rule); the Dal question to the author (PAH-4) belongs on
   your author list (PAH-9) if it is not there yet.
2. Other v1.13 changes, all in the CSL, nothing in your tokens: every person by initial in the notes; the
   bibliography spells out editors and translators and has a comma after the author field (`Fotta Martin, *Tytuł*`);
   reverse italics only for a title within a title.
3. **refs.json changed** (foreign words in titles no longer keyed `<i>`; the Icelandic editor keyed family/given):
   **[Ostendorf]** `7b055ff1…0e9e054` (oreilly2003, fotta2019, cunniffe2023), **[Ndiaye]** `2e35d0f2…64376c1`
   (cathelin2004). Copy and verify at your next intake; T32's Ostendorf hash is void.
- T33, correction 02.10.2026 18:58: [Ostendorf] 13 annotations in 12 notes (n. 12 has two), not 12.

## T34 — [general] [Ostendorf] [Ndiaye] Kanon v1.14: reverse italics restored; refs.json changed again (02.10.2026 19:58)

- 02.10.2026 19:58 status: action for you. MB's correction after v1.13, srom-produkcja commit "Kanon v1.14". Please cite "Kanon v1.14".
1. **§ 3.4 (reverts a sentence of v1.13):** inside an italic title a foreign word or phrase, a Latin formula, a foreign
   exonym *and* a title within a title are set **roman** (reverse italics; SJP PWN, Poradnia, *Wyróżnienie tytułu w
   tytule*). So key the inner italics again as `<i>…</i>` in refs.json titles (`<i>Divide et impera</i>: Race…`); the
   build prints them roman. T33 item 2's "only a title within a title" is void; the build's by-reference warning is gone.
2. **refs.json changed (T33 item 3 is void):** [Ostendorf] `8958c705…f09ce` (fotta2019 `<i>Cigano</i>`, oreilly2003
   `<i>Divide et impera</i>`, cunniffe2023 `<i>c.</i>`), [Ndiaye] `6a058001…8ad988a` (cathelin2004 `<i>Paios</i>`;
   check whether the title's other foreign words, e.g. *Gitans*, were italic in the author's original). Copy and verify at your next intake.
3. **New in § 3.4:** publishing-series and conference names — capitalised, roman, in quotation marks (`„Prace
   Etnologiczne”`); in italics also titles of films, songs and other musical works, paintings and sculptures, radio and
   TV programmes; names of musical bands — roman, capitalised, every independent word in a multi-word name
   (`Big Cyc`, `Pod Budą`). Nothing changes in your tokens; keep the rules in mind for names that occur in texts.

## T35 — [general] Kanon v1.15: series and conference names (02.10.2026 20:10)

- 02.10.2026 20:10 status: for information. Kanon **v1.15** (supersedes v1.14's wording in T34 item 3): publishing-series
  and conference names are roman, in quotation marks, **every word capitalised** (`„Leksykon Polskiej Muzyki Rozrywkowej”`).
  Nothing else changes. Please cite "Kanon v1.15".
- T35, correction 03.10.2026 00:28: [general] written 20:08, not 20:10 (the header time is the one `date` gave at commit).

## T36 — [general] [Tittel] Kanon v1.16: DOI no longer printed, series, places, reprint, bibliography parts; linter fix (03.10.2026 00:30)

- 03.10.2026 00:30 status: action for you (small). MB's decisions of 02.10.2026 21:30, srom-produkcja cb3cfe5: Kanon **v1.16**
  (header, § 17 row, RULES.md, SKILL.md agree). Please cite "Kanon v1.16". Suite 24/24; your `tlumacz-test_handoff.py`
  against cb3cfe5: HANDOFF CONTRACT 34/34.
1. **No DOI is printed** — notes, bibliography, and the translation note (§ 12.2.3 item 1, § 9.7): the original's description
   in the title note ends at the page range, `… s. aa–bb.`, without `DOI: …`. Drop it from the drafts' translation notes
   (it stays in the record fields). The online PDF carries invisible DOI links; nothing for you.
2. **Series, places, reprints** (§ 7.2) are the build's: series in parentheses after the year (`München 1995 („Nazwa”, 34)`),
   several places with an en dash (the build turns `/` and `;` into `–`), a reprint as `2000 [1983]`. Data only
   (`collection-title`/`-number`, `publisher-place`, `original-date`); no token changes.
3. **§ 7.3:** after a lead-in the build prints `zob. ibidem` in lower case; nothing for you.
4. **§ 9.2 bibliography parts:** Wykaz skrótów · Źródła archiwalne · Źródła terenowe · Źródła drukowane · Opracowania ·
   Źródła internetowe ("Literatura przedmiotu" is now "Opracowania"; laws, press, old printed works and classics under
   "Źródła drukowane"). If your drafts name a part, use the new names (the build still reads the old ones).
5. **[Tittel]** `refs.json` changed (Kant, Marx, Grellmann, Biester, Rüdiger → `srom-section` IV, "Źródła drukowane"):
   `71181a9a…2b320d9`. Copy and verify at your next intake.
6. Linter `TLUM-ADNOTACJA` now also catches the capitalised `Tłum. z przekładu angielskiego` (review 02.10.2026; no rule change).
   Your current `pahulich_pl.md` has none left, so there is nothing to report; the test covers both spellings.

## Status of review 02.10.2026 (srom-produkcja, 03.10.2026 00:30) [general]
1. Linter, capitalised annotation: **done** — `[Tt]łum\. z przekładu…`, test case added (cb3cfe5's parent commit); told in T36 item 6. The check on `pahulich_pl.md` could not be repeated: that draft has no annotation any more.
2. MB's decisions of 21:30 (Kanon v1.16): **done** — Kanon § 7.2, 7.3, 8.6, 9.1, 9.2, 9.4, 9.7, 12.2.3 and § 17 row 1.16; CSL (series, reprint, DOI out), `build.py` (section names and order, places, lower-case ibidem; the InDesign Ibidem check finds either case), `volume_lists.py` (parts before the last two; vol. 18 gives 9 persons), `autorzy.tsv` (GEN-12; Popov spelled Veselin in the register — vol. 18's master CSV still says Vesselin, left as printed); Tittel's Kant/Marx/Grellmann/Biester/Rüdiger moved to "Źródła drukowane"; announced as T36; the ledger section deleted. Scheffknecht: only the series (GEN-5) and the place `Wien–München` apply; its refs data had no further change.
3. Commit of `ostendorf_uwagi.md`: **done** — the line sits under the B-list of OST-3 (second editor's spelling).
4. T35 time: **done** — correction line under T35.
5. Stale text: **done** — HANDOVER-produkcja (GEN-14 settled, "z dużych liter" settled by v1.15, § 1 Kanon list v1.13–v1.16), ledger intros (GEN-4…9 pointers dropped from the SCH, WOH and Tittel lines). **G12 decision: stays open** until an MB-edited translated text with a real asterisk series is placed; the three scripts ran on Ostendorf's INJECT layouts on 02.10 but Ostendorf is not yet MB-edited. `dist/*.skill` not rebuilt (only before an upload).
Suite: SUITE ALL PASS 24/24.

## Status of review 03.10.2026 (srom-produkcja, 03.10.2026 01:40) [general]
1. Gate F3 path (`GATES.md`): **done** — CHECK now calls `~/.claude/skills/srom-tlumacz/scripts/tlumacz-test_handoff.py`, NOTE line added; run: `GAP CLOSED ok  E16`, `HANDOFF CONTRACT 33/33`.
2. E20 [general]: **done** — read and accepted; the terminology slot (the two commented `tb_check.py` lines and `[--queries <id>_pytania_tb.csv]`) is removed from `references/handoff.md`. Suite 24/24, HANDOFF CONTRACT 33/33.

## Status of review 04.10.2026 (srom-produkcja, 04.10.2026 21:47) [general]
1. Cowork's patches `20261004-0254` for srom-produkcja, srom-quant, srom-zizek: **done** — applied as sent, commit `2cfbeff`; suite SUITE ALL PASS 24/24; `cowork_sync.py` § 1 shows the three as "in Code, in Cowork", § 2 shows 0 differences for srom-produkcja, srom-quant, srom-zizek.
2. K-item with the hashes: **done** — K3 in `code-to-cowork.md` (aa56f38, 74449fc, 2cfbeff).
3. Read `cowork-to-code.md` at session start: **done** — in my start routine; the file does not exist yet (nothing from Cowork to answer).
Needs MB: SYS-9 and SYS-10 (in the ledger, root's); nothing for this module.
