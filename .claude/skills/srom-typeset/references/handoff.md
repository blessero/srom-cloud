# Handoff to translation (srom-tlumacz) and back

Translation is not done here. srom-typeset prepares the source and takes the translation back; srom-tlumacz
(its own chat and skill) translates. This file is the contract between the two.

## Out: what srom-typeset hands over (per article `<id>`)

| file | for | what it is |
|---|---|---|
| `<id>_src.md` | srom-tlumacz | frozen source in SROM-MD: text, italics, headings, quotes, notes under their paragraphs; every bibliographic reference already a citation token `[@key, s. N]` (author-date converted, footnote style keyed); lead-ins "see/cf." already "zob./por." |
| `refs.json` | both | the bibliography data behind the tokens (audited against the author's list) |
| `<id>_src_robocza.docx` | editor | the same text as a Word working copy (`export_work.py`): real footnotes, tokens visible and editable |
| `<id>_src_korekta.docx` | editor | reading proof with the full Polish apparatus rendered (`build.py --proof`): checks the conversion, not for editing |

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
- Translation note on the title (§ 12.2.3): a `::: przypis-tytulowy` block at the top; it becomes the first
  note of the asterisk series (first `*` on the article's first page).
- Open items may stay in the text as comments (`<!-- PRZYWRÓCIĆ ORYGINAŁ: … -->`, `<!-- DO SPRAWDZENIA: … -->`):
  in the editor's working copy they become ordinary Word comments. **Nothing in comments blocks anything**:
  the editor handles them; on import they are dropped and listed in the import report.
- Queries: rows in the `_pytania` columns `adresat;rodzaj;przypis;dzieło;szczegóły`, saved as a CSV; the
  `przypis` cell holds the note label from `<id>_src.md` — the build turns it into the printed number.

## Back: what srom-typeset accepts

`<id>_pl.md` from srom-tlumacz is turned into the editor's working copy; **the editor's Word file is the
master** from then on:

```
python3 $S/export_work.py <id>_pl.md -o <id>_robocza.docx        # editor works in Word
python3 $S/docx_in.py <id>_robocza.docx -o <id>_pl.md            # recognised as a working copy, lossless
python3 $S/check.py --pair <id>_src.md <id>_pl.md --refs refs.json --refs <id>_refs_tlum.json   # handoff check
# terminology slot (advisory, never blocks; when srom-tlumacz provides it):
#   python3 <srom-tlumacz>/scripts/tb_check.py <id>_src.md <id>_pl.md --tb tlumacz-tb.tsv --csv <id>_pytania_tb.csv
python3 $S/build.py <id>_pl.md --refs refs.json --refs <id>_refs_tlum.json --pair-src <id>_src.md \
        --queries <id>_pytania_tlum.csv [--queries <id>_pytania_tb.csv] --out build/
```

In Word: tokens can be corrected in place (keep the brackets and `@key`); paragraphs styled "SROM …" keep
their style; comments are yours to handle (dropped and listed on import); tracked changes are accepted on
import.

`check.py --pair` (handoff check): same paragraphs and headings, same note markers per paragraph, same
citation keys in each note in the same order — translator/editorial notes and the title note left out, declared
additions allowed (and listed); interlinear form lines identical. Differing numbers are warnings (dates and
centuries are written differently in Polish); digits in citation keys and in added citations are not counted.
