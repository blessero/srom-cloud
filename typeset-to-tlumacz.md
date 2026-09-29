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
