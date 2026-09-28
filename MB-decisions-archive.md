# MB decisions — archive (full text of closed items)

*Verbatim copy of `MB-decisions.md` as it stood on 27.09.2026 before the clean-up MB asked for (srom-typeset). Frozen: nothing is appended. Items closed later are recorded where they take effect (Kanon, handover, handoff item, commit), per the rules in `MB-decisions.md`.*

---

# Decisions waiting for MB — all SROM modules

One list of everything only MB can decide. Any module appends; nobody deletes.

Rules:
- New item: `## D<n> — <subject> (dd.mm.yyyy, <module>)`, then: the question, the options, the module's
  recommendation, what it blocks, and where the detail is (file + item ID).
- MB's answer, or a module recording it: a new line under the item, `- dd.mm.yyyy DECIDED: … (MB)`.
  The module that acts on it adds `- dd.mm.yyyy done: …`.
- Take the next free D-number; check the file just before appending.

Seeded 27.09.2026 from both modules' handovers (items as they stood there; not re-decided here).

## D1 — Decision 20: the translation handoff rules (27.09.2026, srom-typeset)
Confirm the rule set in `handoff.md`: translator `[^t<n>]` and editorial `[^r<n>]` notes and the title note are
left out of the handoff check; an added citation passes only when declared; after translation the editor's Word
file is the master. Already implemented and tested on both sides. Detail: srom-typeset
`references/decisions.md` item 20.
- 27.09.2026 DECIDED: yes, as implemented (MB delegated the call to srom-typeset; recorded by srom-typeset).

## D2 — Decision 22: added citations declared by `"srom-added"` (27.09.2026, srom-typeset)
Confirm that citations added by the translation are declared by `"srom-added"` in `<id>_refs_tlum.json`
(survives Word); `DODANO` comments still accepted. Implemented; verified by srom-tlumacz (HANDOFF CONTRACT 14/14).
Detail: `decisions.md` item 22; `tlumacz-to-typeset.md` E2.
- 27.09.2026 DECIDED: yes, as implemented (MB delegated the call to srom-typeset; recorded by srom-typeset).

## D3 — Decision 21: house style v2 / reducing the style set (27.09.2026, srom-typeset)
39 paragraph styles proposed; reduction options to ≈ 23 listed. Needs a style discussion with MB, then the
cleaned template as IDML. Blocks: srom-typeset queue items 4–5. Detail: `docs/HANDOVER-typeset.md` § 4.
- 27.09.2026 re-scoped: InDesign styles wait. Order of work: stage 1 (PDF/Word source → SROM-MD → Word working copy) and stage 2 (translation, srom-tlumacz) are finished and tested first; stage 3 (typesetting, InDesign, this item) after (MB).

## D4 — Kanon v1.6 diff check (27.09.2026, srom-typeset / srom-tlumacz)
Check the Polish wording of the 1.6 additions (commit 97b846e) incl. § 12.2 as adopted; whether 1.6 applies
„od tomu 19/2026”; the new rule "no Ibidem in / right after a non-author note"; the stale 22.09 copy in
`0. ASSETS/LLM/Kanon zecera/` (replace or mark superseded). Detail: `docs/HANDOVER-typeset.md` § 7.2.
- 27.09.2026 DECIDED: no line-by-line review of the Kanon text (incl. § 12.2); it is reviewed by testing on a real document (see D7) and tweaking the procedure where the outcome is wrong (MB, recorded by srom-tlumacz).
- 27.09.2026 DECIDED: v1.6 applies from vol. 19/2026; `0. ASSETS/` and anything outside `SROM edit and trans/` is not touched by any module without MB's explicit permission, so the 22.09 copy stays as it is; every reference to the retired *Kodeks zecera* is removed (MB, recorded by srom-typeset).
- 27.09.2026 done: Kodeks references removed from srom-kanon, with a guard test (srom-typeset commit c9253f2). Open from D4: only the new Ibidem rule — covered by the D7 test run.

## D5 — Curator request C1: translator credit in the master CSV and Crossref (27.09.2026, srom-tlumacz)
Pass `tlumacz-to-curator.md` C1 to srom-scholarly-curator, and decide when. Detail: that file.
- 27.09.2026 DECIDED: srom-tlumacz updates the curator skill itself (MB, no curator chat); the translator is to be shown in WordPress, but only after the rest is finalised; desktop upload of the new .skill waits too (MB).
- 27.09.2026 done: C1 items 1–3, 5 — `curator-update-2026-09-27/CHANGES.md` (11/11 tests); installed in ~/.claude/skills. Open: WordPress display (C1 item 4), desktop upload.

## D6 — Inputs for srom-tlumacz (27.09.2026, srom-tlumacz)
(a) Polish vol. 18 files, when leaf 1.2 asks for them (after the blind drafts are hashed);
(b) PRNG world-register export, 2019 KSNG list, KSNG country-names list (leaf 1.3.3);
(c) vol. 19 translation shortlist (deferred by MB 26.09.2026). Detail: `srom-tlumacz/HANDOVER.md` § 6.
- 27.09.2026 done: (a) Polish vol. 18 files received (`srom-tlumacz/vol18-PL-HOLD/`), leaf 1.2 closed 11/11. (b) and (c) still open (MB).
- 27.09.2026 (b) partly in: MB supplied `PolskaNazwaGeograficznaSwiata.json` (PRNG world names). It is page 1 of the API export (150 of 14,268 records); its source field is the 2019 KSNG world list, so the 2019 PDF is not needed. Recommendation (srom-tlumacz, MB to confirm): fetch the full export from the same public API (needs MB's OK), without geometry; drop all three KSNG PDFs and `NazwaGeograficznaRP`; the PRNG world export already carries country names (short and official), and the rare post-2019 change is checked per case in the 2025 country list.
- 27.09.2026 DECIDED (b): PRNG world register is enough; KSNG PDFs and NazwaGeograficznaRP not needed. Done: full export fetched (14,268 records, `srom-tlumacz/sources/prng/`) (MB, recorded by srom-tlumacz).

## D7 — First real article end to end (G12) (27.09.2026, srom-typeset)
Choose the article and run the InDesign checklist (`references/indesign.md`). Detail:
`docs/HANDOVER-typeset.md` § 3 item 6, § 7.5.
- 27.09.2026 re-scoped: the first real test is stage 1 on a PDF that MB uploads; the InDesign part (G12) waits with D3 (MB).

## D8 — Vol. 18 terminology: inconsistencies and candidate rows (27.09.2026, srom-tlumacz)
Leaf 1.3.1 mined the four vol. 18 translations (detail: `srom-tlumacz/tlumacz-1.3.1/findings.md`). Each point has a recommendation; **"all as recommended"** is a valid answer.
(a) *Romani studies*: vol. 18 has both „romologia” (Ostendorf, Marushiakova/Popov) and „studia romskie” (Fotta). Rec.: **romologia** canonical (the journal's own name), „studia romskie” allowed for style; the journal *Critical Romani Studies* stays in the original, and the field is „krytyczne studia romskie”.
(b) *urasowienie*, the imperfective member: vol. 18 has „urasowiania” (Ostendorf) and „urasawiane” (Fotta's abstract). Rec.: **urasawiać / urasawianie / urasawiany** (regular pattern, as in ustanowić → ustanawiać).
(c) Lom vs Łom: „Lomowie/Lomów” 16×, „Łomom” once (Dom, note 2). Rec.: **Lom / Lomowie**.
(d) Garachi / Karachi: the source uses both (Azerbaijani vs Russian-based transliteration of the same name); vol. 18 renders both „Garaczi”. Rec.: accept, and record Karachi as a variant in the kartoteka.
(e) Italics of historical foreign designations (*Ciganos*, *Gitanos*, *Bohémiens*): italic in vol. 18, but Kanon § 3.4 (from vol. 19) says ethnonyms are never italic. Rec.: **roman** from vol. 19 (they are group names); confirm, or ask srom-typeset to clarify § 3.4 (E11).
(f) Fotta distinguishes *Romanies* (umbrella) from *Roma*; vol. 18 renders both „Romowie”. Rec.: accept; a translator's note only where the author's distinction carries the argument.
(g) Sign-off of the termbase candidates (`tlumacz-1.3.1/tb-candidates.tsv`): antycyganizm (not antyromski, which is 'anti-Roma'), projekt rasowy, formacja rasowa, określenie zbiorcze, historyzacja; C-0005 + gypsiology; C-0001 + (b). Rec.: yes; they become HOUSE rows.
Blocks: G8 of leaf 1.3.1 (merge into the termbase). Nothing else waits on it.
- 27.09.2026 DECIDED: all as recommended, except: (d) Garachi / Karachi are both legitimate, the author's form decides; Karachi recorded as a variant in the kartoteka seed. (e) not decided: § 3.4 clearly covers endonyms, but *Ciganos*, *Gitanos*, *Bohémiens* are exonyms not used in Polish (foreign words, unlike *Cygan*), so italics may be right; srom-typeset to make the call by Polish academic practice, or discuss with MB (E12). Also: „Travellersi” is primary, „Wędrowcy” a synonym. Termbase merged (11 HOUSE rows); 1.3.1 closed (MB, recorded by srom-tlumacz).
- 27.09.2026 DECIDED (e): foreign exonyms not assimilated in Polish (*Ciganos*, *Gitanos*, *Bohémiens*, *Zigeuner*, *Tsiganes*) are italic, also when the word itself is discussed; endonyms and assimilated exonyms roman — Kanon § 3.4 (MB delegated the call to srom-typeset, E12).
- 27.09.2026 done (e): Kanon § 3.4/6.2/6.3/14/17 and RULES.md, commit 2830033. Nawar, Gurbati, Halabi: endonym or exonym not established — flagged `E12` in the kartoteka, asked of srom-tlumacz (T8).

## D9 — Kartoteka wzorcowa: where it lives, and adopting the vol. 18 seed (27.09.2026, srom-typeset)
Kanon § 6.3 foresees a kartoteka of standard group-name forms; it does not exist yet. srom-tlumacz sent a seed of
35 names from the four vol. 18 translations (`srom-tlumacz/tlumacz-1.3.1/kartoteka-seed.tsv`, E11).
Question: (a) keep the kartoteka as `srom-kanon/references/kartoteka.tsv`, next to the Kanon, edited only from the
srom-typeset session like the Kanon itself? (b) adopt the seed as its first content (rows flagged `MB` wait for
D8)? Recommendation: yes to both; the Polish-original articles of vol. 18 can be added later. Blocks: nothing
urgent; the kartoteka is used for the volume index, keywords and deposit. Detail: `tlumacz-to-typeset.md` E11,
`typeset-to-tlumacz.md` T4.
- 27.09.2026 DECIDED: yes to (a) and (b) (MB delegated the call to srom-typeset).
- 27.09.2026 done: `srom-kanon/references/kartoteka.tsv`, 35 rows from the seed + column `italic_house`; structure test in srom-typeset `test_kanon.py`; commit 2830033.
