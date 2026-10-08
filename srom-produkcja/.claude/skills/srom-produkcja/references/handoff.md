# Handoff to translation (srom-tlumacz) and back

Translation is not done here. srom-produkcja prepares the source and takes the translation back; the srom-tlumacz
skill translates. This file is the contract between the two (file formats and rules); the order of the stages and
their gates are in `stages.md`, the record of what was handed over (sha256) in the hand-off log of `STATUS.md`.

## Out: what srom-produkcja hands over (per article `<id>`)

| file | for | what it is |
|---|---|---|
| `<id>_src.md` | srom-tlumacz | frozen source in SROM-MD: text, italics, headings, quotes, notes under their paragraphs; every bibliographic reference already a citation token `[@key, s. N]` (author-date converted, footnote style keyed); lead-ins "see/cf./quoted in" already "zob./por./cyt. za" |
| `refs.json` | both | the bibliography data behind the tokens (audited against the author's list) |
| `<id>_src_front.md` | srom-tlumacz | the original's title, author and affiliation, abstract, keywords (if any), as in the source (`pdf_extract.py` → `_front.md`; from DOCX by hand); not part of the text |
| `<id>_src_robocza.docx` | editor | the same text as a Word working copy (`export_work.py`): real footnotes, tokens visible and editable |
| `<id>_src_korekta.docx` | editor | reading proof with the full Polish apparatus rendered (`build.py --source`: a proof in which the source's own typography — English quotes, em dashes, marker after the period — is counted, not reported as errors; `normalize.py` applies Polish typography to the translation): checks the conversion, not for editing |

The Polish apparatus (red., w:, s., tłum., short forms, *Ibidem*) is generated from refs.json at build time,
so nothing in the citations is translated. Titles in tokens stay as in the source (kanon). The source is not
run through `normalize.py`: Polish typography is applied to the translation, after it comes back.

## Translation rules the contract depends on

- Tokens `[@key …]`, note markers `[^n]`, `{…}` locators, `::: …` block lines: copied unchanged.
- Interlinear examples (`::: przyklad` fenced block, kanon § 5.3): line 1 (the form) copied unchanged; line 2 gets
  Polish lexical glosses, category labels (1SG, DEF…) stay; line 3 translated, in ‘ ’. The handoff check
  fails on a changed form line or a changed number of lines.
- Literal notes (archival units, fieldwork codes, legal acts) are translated with Polish apparatus labels
  (kanon § 8: fol. → k., file → sygn., fond → zespół; post-Soviet `f.`, `op.`, `d.`).
- Paragraph for paragraph: never merge or split paragraphs or notes.
- Translator's note: label `[^t<n>]`, text ending `– przyp. tłum.`; editorial note: `[^r<n>]`, ending `– przyp. red.`
  The formula must **end** the note (label and formula must agree; a mismatch is an error). In print they are
  not numbered: with the title note they form the asterisk series `*`, `**`, … (kanon § 7.1), set above the
  numbered notes; they take no number in the query sheet either (a query on one gets `*`). A translator's
  addition inside an author's note, `[… – przyp. tłum.]` (§ 12.2.7), leaves it an author's note.
- A citation added to an author's note (e.g. the Polish edition, § 12.2.4 a–b): its entry goes in
  `<id>_refs_tlum.json` with `"srom-added": "tlum"` and a non-empty `"srom-source"` (catalogue URL or
  verified ISBN). That marking is the declaration — it survives the Word round trip, unlike comments;
  `<!-- DODANO: @key -->` in the note is still accepted. `cite_map.py audit` skips these entries when
  matching the author's list and fails any without `srom-source`.
- Translator in the article header (Kanon § 12.2.3, E10): YAML front matter at the very top of `<id>_pl.md`,
  `tlumaczenie: "Imię Nazwisko"` (a YAML list if several). Never a body paragraph: SROM-MD has no header, and
  the header block is set in InDesign from the master CSV. The build does not print it; it lists it in
  `_report.md` under "Header data" with the `translators_struct` value for the CSV. It survives the Word working
  copy (stored as the Word custom property `srom-tlumaczenie`, restored on import); an empty value fails the build.
- Translation note on the title (§ 12.2.3): a `::: przypis-tytulowy` block at the top; it becomes the first
  note of the asterisk series (first `*` on the article's first page). **One block per article**: when the
  author has a note on the title too (acknowledgements), it follows the translation note as a further paragraph
  of the same block — one `*` at the title (Kanon § 7.1: the title note takes the first asterisk). Two blocks are
  an error in `check.py` and the build (E15; MB 28.09.2026, Kanon § 7.1).
- Open items may stay in the text as comments (`<!-- PRZYWRÓCIĆ ORYGINAŁ: … -->`, `<!-- DO SPRAWDZENIA: … -->`):
  in the editor's working copy they become ordinary Word comments. **Nothing in comments blocks anything**:
  the editor handles them; on import they are dropped and listed in the import report.
- Queries: rows in the `_pytania` columns `adresat;rodzaj;przypis;dzieło;szczegóły`, saved as a CSV; the
  `przypis` cell holds the note label from `<id>_src.md` — the build turns it into the printed number.

## Back: what srom-produkcja accepts, and how (29.09.2026, review row 3)

Who does what (practice since the first drafts, now the contract):

1. **Working copy.** srom-tlumacz exports `<id>_pl.md` to `<id>_robocza.docx` in `srom-tlumacz/work/<id>/`
   (`export_work.py`). The editor edits that file there. From the editor's first edit, **that Word file is the
   master**; the SROM-MD is only its import. Never re-export over it: a new export goes to a temp folder or a new
   name (`<id>_robocza_v2.docx`), and the editor says which file is the master. **At delivery the master is always named `<id>_robocza.docx`**
   (review 01.10.2026 row 4): srom-tlumacz renames the editor's master to that name and older exports to
   `<id>_robocza_old<n>.docx`; `take_back.py` takes only that name.
2. **Import and checks: srom-tlumacz**, in `srom-tlumacz/work/<id>/`, after each editing round the editor hands back:
   `docx_in.py <id>_robocza.docx -o <id>_pl.md` (recognised as a working copy, lossless), then `check.py --pair`,
   `build.py … --draft` and `tlumacz-front_check.py` as below. The imported `<id>_pl.md` is not edited by hand: a
   correction goes into the Word master and the import is repeated.
3. **Delivery line.** srom-tlumacz appends a delivery line to the hand-off log of `STATUS.md` (mirror of the
   hand-over line out), with the sha256 (`first8…last7`, or full) of every file delivered:

   | file | required | what |
   |---|---|---|
   | `<id>_robocza.docx` | yes | the editor's Word file, the master |
   | `<id>_pl.md` | yes | its import by `docx_in.py`, byte for byte |
   | `<id>_front_pl.md` | yes | Polish title, abstract, keywords (below) |
   | `<id>_refs_tlum.json` | if the translation adds citations | declared additions (`srom-added`) |
   | `<id>_pytania_tlum.csv` | if there are query rows | the translator's query sheet |

   It also names the srom-produkcja `refs.json` sha256 it was checked against (the one in the last hand-over line),
   and the verdicts (`CHECK OK`, build `PASS`, `FRONT OK`). A later editing round means a new delivery line that
   supersedes the earlier one. The copies at srom-produkcja are never edited.
4. **Take-back: srom-produkcja** copies the delivery into `srom-produkcja/work/<id>/pl/` and checks it:
   `take_back.py srom-tlumacz/work/<id> <id> --src-dir srom-produkcja/work/<id> --expect <file>=<sha256> …` (one
   `--expect` per file of the delivery line). It compares the sha256, requires `<id>_pl.md` to equal a fresh import of the Word master,
   runs `check.py --pair` against the frozen `<id>_src.md` and `refs.json`, and writes `SHA256SUMS`; the copies and `SHA256SUMS` are made read-only (sealed: Word opens them locked; MB 08.10.2026). If `refs.json`
   changed after the delivery's value (a later hand-over line), the pair check and build use the current one, and
   the take-back line in the log says so. srom-produkcja **normalises the copy from `work/<id>/pl/` into
   `work/<id>/build/<id>_pl.md`** (`normalize.py`, never in place: `pl/` stays as delivered and `SHA256SUMS`
   verifies), **builds that file** into `work/<id>/build/` and logs the take-back with its verdicts. A normaliser
   flag, like any other problem, goes to the notes sheet and is fixed in the Word master, with a new delivery; the md
   is never edited by hand (if MB must decide: a K-item "needs MB" for Cowork's ledger).

`<id>_front_pl.md` (Kanon § 12.2.2): the Polish title (title and subtitle kept apart), the Polish abstract, the
Polish keywords; the English ones stay as in the original. Header data for the master CSV, not built into the
DOCX. Its format (sections, order, headings) is the docstring of srom-tlumacz's `tlumacz-front_check.py`, which
checks it (`FRONT OK`).

The commands (`$S` = srom-produkcja's `scripts/`):

```
python3 $S/export_work.py <id>_pl.md -o <id>_robocza.docx        # srom-tlumacz, once; the editor works in Word
python3 $S/docx_in.py <id>_robocza.docx -o <id>_pl.md            # srom-tlumacz, after each round; lossless
python3 $S/check.py --pair <id>_src.md <id>_pl.md --refs refs.json --refs <id>_refs_tlum.json   # handoff check
python3 $S/take_back.py srom-tlumacz/work/<id> <id> --src-dir srom-produkcja/work/<id> --expect <id>_pl.md=… …   # srom-produkcja
python3 $S/normalize.py srom-produkcja/work/<id>/pl/<id>_pl.md -o srom-produkcja/work/<id>/build/<id>_pl.md \
        --log srom-produkcja/work/<id>/build/<id>_pl_norm.md       # srom-produkcja; never over pl/
python3 $S/build.py srom-produkcja/work/<id>/build/<id>_pl.md --refs srom-produkcja/work/<id>/refs.json --refs srom-produkcja/work/<id>/pl/<id>_refs_tlum.json \
        --pair-src srom-produkcja/work/<id>/<id>_src.md --queries srom-produkcja/work/<id>/pl/<id>_pytania_tlum.csv \
        --out srom-produkcja/work/<id>/build/
```

In Word: tokens can be corrected in place (keep the brackets and `@key`); paragraphs styled "SROM …" keep
their style — consecutive paragraphs in one block style (title note, motto, nota, dialog) come back as one block
(E16); comments are yours to handle (dropped and listed on import); tracked changes are accepted on import.
Note labels in the imported file are Word's numbering (translator's notes too, `[^t1]` comes back as a number);
the formula `– przyp. tłum.` still marks them, and `--pair-src` keeps the printed numbers and the query rows right.

`check.py --pair` (handoff check): same paragraphs and headings, same note markers per paragraph, same
citation keys in each note in the same order — translator/editorial notes and the title note left out, declared
additions allowed (and listed); interlinear form lines identical. Differing numbers are warnings (dates and
centuries are written differently in Polish); digits in citation keys and in added citations are not counted.
