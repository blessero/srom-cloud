# Scheffknecht, "Zigeuner im Reichshof Lustenau" (Neujahrsblätter Lustenau 1, 2010) — stage-1 test 3 (German): open points

Stage 1 done 28.09.2026 (srom-produkcja). Source: `work/njb-2010-zigeuner-im-reichshof-lustenau_wolfgang-scheffknecht.pdf`,
PDF pp. 4–32 = printed pp. 77–105 (pp. 1–3: the volume's cover, imprint and contents; not extracted).
Files: `scheffknecht_src.md` (frozen source, 120 notes + title note, 46 notes keyed, 74 literal: 73 archival + 1 prose),
`refs.json` (35 works, from `refs.py`), `scheffknecht_src_front.md`, `scheffknecht_src_robocza.docx` (Word working copy),
`build/scheffknecht_src_korekta.docx` (source proof), `key_log.md` (every keying change). Pipeline: `pdf_extract.py
--pages 4-32` → `key.py` (relabel + keying) → `check.py --keyed` → `build.py --source` → `export_work.py`.
Page numbers below are the printed ones (77–105) unless marked "PDF". **Nothing was sent to srom-tlumacz** (A1).

## A. Needs MB

**SCH-1 · A1. Stage 2 — who translates?** srom-tlumacz is an EN→PL module; this source is German. Options: (a) keep this as a
stage-1 test only; (b) ask srom-tlumacz for a DE→PL trial (its terminology base, kartoteka and checks are built on English
sources — a scope decision for its session); (c) a human translator, the files as they are (the contract does not depend on
the language). *Recommendation:* (a) for now, (b) only as an explicit trial. Nothing in the files needs changing for (b)/(c).

**SCH-2 · A2. Rights.** The volume carries no licence. The volume's imprint (PDF p. 2): "Nachdrucke und Auszüge sind nur mit Quellenangabe
gestattet" — that covers quotation, not a translation. Rights holders: the author and the Marktgemeinde Lustenau (Historisches
Archiv, Medieninhaber). The two figures belong to the Vorarlberger Landesarchiv (Steckbrief 1749, p. 84) and the Staatsarchiv
Augsburg (map 1810, p. 96). *Recommendation:* written consent of the author and the Archiv before any translation is
published; image permissions at stage 3.

**GEN-4 · A3. No publishers — 29 of 35 works print `[BRAK WYDAWCY]`.** German citation practice gives place and year only; Kanon
§ 7.2/§ 9 require the publisher and § 0 keeps a text with a placeholder out of typesetting. Options: (a) the sourcing step you
planned (I look each one up in DNB/ÖNB/library catalogues and list them for your approval, item by item; nothing enters
refs.json unapproved); (b) ask the author; (c) a Kanon exception for sources cited without publishers (not recommended: the
bibliography would be inconsistent). *Recommendation:* (a). Blocks: typesetting, not translation. Any German, Austrian or
Swiss source will raise this.

**GEN-5 · A4. Series — no Kanon rule, not printed.** 14 works come with a series ("(Enzyklopädie Geschichte 34)"). They are kept in
refs.json (`collection-title`, `collection-number`) but the CSL prints nothing (Kanon § 12: a series "remains in the original",
but § 7.2/§ 9 give it no place in the description). Options: (a) print in parentheses at the end of the description, bibliography and
first citation: `…, Köln 1984 (Aus der Kölner Stadtgeschichte)`, `…, München 1995 (Enzyklopädie deutscher Geschichte, 34)`;
(b) bibliography only; (c) never. *Recommendation:* (a), the usual Polish form. Then: Kanon § 7.2/§ 9 text, CSL, test.

**A5. German "von" (von Hippel).** The Kanon has no rule for name particles. Now as the author writes it: notes "W. von
Hippel", short form "von Hippel", bibliography "von Hippel, Wolfgang" sorted under V. Alternative (library practice): "Hippel,
Wolfgang von", sorted under H, short form "Hippel". *Recommendation:* the library form for German/Austrian nobiliary "von";
a Kanon § 9 line, then one refs.json field.

**SCH-3 · A6. Archive abbreviations never expanded.** 73 notes cite VLA, HoA, HistA, PfA, StaatsA, StadtA; the article never gives the
full names. Kanon § 8.1 wants the full name at first use ("(dalej: …)") and a list in the bibliography. Proposed (to confirm
with the author): VLA = Vorarlberger Landesarchiv (Bregenz); HistA Lustenau = Historisches Archiv der Marktgemeinde Lustenau;
PfA Lustenau = Pfarrarchiv Lustenau; StaatsA Augsburg = Staatsarchiv Augsburg; StadtA Lindau = Stadtarchiv Lindau; **HoA —
not known to me** (a fonds of the VLA, presumably the Hohenems archive: ask). Blocks the "Źródła archiwalne" section only.

**SCH-4 · A7. A stray note number at the end of the text.** After the last word ("… bilden.") the PDF has a raised "1" — the number
of the note on the title. Kept as a comment `DO SPRAWDZENIA` in `scheffknecht_src.md` (not printed). *Recommendation:*
delete (a leftover of the note's move to the title); or ask the author.

**SCH-4 · A8. Printed early-modern sources held in archives** (HoA 78,2: *Beschreibung …* Bregenz 1749; HoA 103,25: *Jauner- Und
Diebs-Lista* 1733; StadtA Lindau 56,1 (Ravensburg 1754) and 56,2 (Memmingen 1773); the *Zürcher Zeitung* extract, HoA 83,6)
stay literal archival references, as the author cites them. Alternative: key them as printed sources (bibliography section
"Źródła drukowane"). *Recommendation:* literal (they are cited as archive holdings). Low priority.

## SCH-5 · B. The author's data — kept as written until MB decides

| # | where | the author's form | proposal |
|---|---|---|---|
| B1 | von Hippel 1995 (PDF note 13), series | Enzyklopädie Geschichte 34 | Enzyklopädie deutscher Geschichte 34 (the series' name — from my knowledge; to verify in DNB) |
| B2 | Scheffknecht 1991 (PDF note 40), title | … der vorindustiellen Gesellschaft | vorindustriellen (typo; to verify on the book) |
| B3 | Ammerer 2003 (PDF note 69), place | Wien-München | Wien–München (two places; no Kanon rule) |
| B4 | Vetter's quotation (text, p. 78) | "in der heutigen Mudart" | Mundart — Vetter's or the author's slip; [sic] or correct? ask the author |
| B5 | quotations (text, pp. 87, 90; note 97 = PDF 98, p. 104) | omission "[..]" (two dots); once "[...]" (p. 77) | "[…]" — typography, the translation normalises it anyway; for information |
| B6 | Specker 2000 (PDF note 31) | container "Reichskreis und Territotium (wie Anmerkung 30)" | typo in a cross-reference; the container comes from note 30 — for information, nothing kept |
| B7 | Niederhäuser 2003 (PDF note 13) | "Bd. 4 … und Bd. 9: Register und Dokumentation, S.147-166 und 52-53, hier Bd. 4, S.151" | chapter in vol. 4; its notes in vol. 9 go to `note` ("przypisy w t. 9 (Register und Dokumentation), s. 52–53") — for information |

## C. Applied in processing — for information (reversible, all in `key.py` / `refs.py` / `key_log.md`)

- Note labels: the PDF's note 1 is the note on the title (`::: przypis-tytulowy`), so PDF notes 2–121 are labels 1–120
  (label = printed number in SROM). The PDF's "(wie Anmerkung n)" numbers refer to the old numbering; they vanish with keying.
- The title note cites Landwehr 2001 (first citation there; later notes print the short form).
- Locators with Polish labels (Kanon § 7.2): `s.`, `szp.` (Jutz, "Sp.1717"), `przyp.` (Landwehr, "Anm. 52"); "S.21, 24 und
  119" → "s. 21, 24, 119"; "Zitiert nach" → "Cyt. za". Ranges with an en dash in locators and in three titles (1300–1600,
  1383–1806, 1725–1808; the PDF has hyphens). Chapter/article ranges given before "hier S." are in refs.json `page`
  (bibliography), not in the notes (Kanon § 7.2).
- Short titles per Kanon § 7.3 (beginning of the title + "…"), not the author's keywords ("Hannikel", "Öffentliche
  Sicherheit", "Königshof").
- 7 notes cite a work as a whole (the author gives only the article/chapter range, or nothing): query sheet
  `build/scheffknecht_src_pytania.md`, "odwołanie do całości dzieła — potwierdzić": notes 10 (François 2002), 30 (Specker
  2000), 31 (Brauns 1951), 39 (Scheffknecht 1988), 109 (Welti 1970), 118 (Welti 1930, Scheffknecht 2002), 120 (Gabriel 1963).
- Note 108 (PDF 109): the citation is the subject of the sentence ("Ernst Schubert, Arme Leute …, S.268, zeigt …") → the
  token stands in its place; the translator will recast the sentence.
- Edition numbers (²1935, ³2002, ³2001, ²1989, ²1990) → `edition`; the school report "1987/88" → date as written.

## D. Extraction doubts (low priority)

- D1. Two page breaks after a sentence end on a full line, taken as one paragraph each (the layout gives no evidence):
  pp. 88/89 "…bassgeigen.⁵⁴ | Johannes Leimberger gab im Verhör an…" and pp. 90/91 "…umbs Leben gebracht.⁷³ | Außerdem
  ließen sich…". Split if you see a paragraph break in print.
- D2. The inner paragraphs of Vetter's long quotation (pp. 77–78) come from the source's tabs: 4 paragraphs.
- D3. Figures: two captions → `::: podpis`; the images are placed by hand at stage 3.

## E. Terminology (for whoever translates; not decided here)

The author explains in the title note why he uses the source term "Zigeuner" (Landwehr: a period term, a social category).
Polish: "Cyganie" (kartoteka: established Polish exonym, roman) seems to follow that intent; also "Heiden/Haiden" (period
designation), "Jauner", "Vaganten", "Reichshof", "Unterschlaufgeber/Receptatores", "Frevelrodel". To settle with the
translator and MB before stage 2.
