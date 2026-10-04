# What needs MB — moved to Cowork

Since 04.10.2026 22:30 [general] (SYS-9 (a), MB 04.10.2026): the one list of MB's open questions is Cowork's
`/Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork/workspace/MB-decisions.md` (MB answers on the Editorial
Desk). A Code session with a question for MB writes it as a K-item in `code-to-cowork.md`, in the ledger's format
(README § Questions for MB), headed "needs MB"; Cowork enters it with its own ID and answers with that ID.
The text questions (GEN, V19, PAH, OST, TIT, NDI, WOH, SCH) and SYS-1 to SYS-4 were already in Cowork's list.
SYS-9 and SYS-10 were decided (a) on 04.10.2026 (K4). The three below went to Cowork in K4; delete them here once
Cowork's answer names their new IDs.

## Handed to Cowork in K4

### SYS-6 · Online cover page: approve the changes to your template
**Approve** · blocks the first online PDF

The cover page is built (`cover_page.py`, 03.10.2026 05:23 [general]): from the master CSV, put in front of the
InDesign PDF, no InDesign template. Your design kept (IBM Plex Sans, SROM red, label column, logo + journal block,
Open Access mark), at 165 × 235 mm. Look at the samples (vol. 18 data, still marked PODGLĄD), then one yes covers:
(Rows 1–2 settled by MB 03.10.2026 23:20 [general]: one page strictly, his template SROM_okladka_szablon_MB.idml, abstracts justified 7.5 pt.)
3. **Kanon over the template:** volume `t. 18`, not `t. XVIII` (§ 3.5); date `02.07.2026`, not `02/07/2026`; keywords
   separated by semicolons (§ 1 pt 9); ISSN and ORCID with hyphens (the template had dashes, which break the ORCID
   link); no line ending in a one-letter word (§ 3.3).
4. **Added:** for translations, „Tłumaczenie: …” and „Pierwodruk: …” (linked to the original's DOI when known); a footer
   line „Wydawca: Komitet … · studiaromologica.pl”; links on the DOI, ORCID, licence and logo; page numbers in the PDF
   viewer i, ii, then the printed pages; title, authors, DOI, licence in the PDF's properties.
5. **Licence sentence** for CC BY is yours. For CC BY-NC and BY-NC-ND (Pahulich, Ostendorf vol. 19, GEN-3) it reads
   „Artykuł w otwartym dostępie na licencji Creative Commons Uznanie autorstwa – Użycie niekomercyjne – Bez utworów
   zależnych 4.0 (CC BY-NC-ND 4.0), pełny tekst licencji: <adres>.” Approve, or give your wording.
6. The InDesign metadata script (`pdf_metadata.py` → `_metadane.jsx`) is no longer needed for the online PDF: the
   cover page writes the same fields. Delete that step.
7. „© 2025 <author>” is kept as in the template; for translations it waits on GEN-1.
Detail: 🔴 `srom-produkcja/work/okladki/proby_okladek_t18.pdf` (four articles: short, long, two authors, a review) and
🔴 `srom-produkcja/work/okladki/SROM_18_2025_Ostendorf_Historia_Romow_amerykanskich_proof.pdf` (cover + article; the
article is the Ostendorf test layout).

*Trail: srom-quant `scripts/cover_page.py`, template `srom-produkcja/dump/SROM Meta Page.idml`; Kanon § 1, 3.3, 3.5, 13.2.*

### SYS-7 · Print the dates of submission and acceptance on the cover page?
**Decide** · blocks nothing

The Kanon lists them among the article's editorial data („daty złożenia i przyjęcia”), but the master CSV has no
place for them and the template does not print them.
- (a) Two new columns in the master CSV (`date_received`, `date_accepted`), printed in the journal block as
  „Złożono: dd.mm.rrrr / Przyjęto: dd.mm.rrrr” when filled — **recommended** (indexes and DOAJ look for them)
- (b) Not printed; drop them from the Kanon list

*Trail: Kanon § 1 pt 13; master_schema.md.*

### SYS-8 · Vol. 18: who translated Ostendorf and Fotta?
**Look up** · blocks their online PDFs

Both are translations, but the master CSV names no translator, and the cover page (like the article header, Kanon
§ 12.2.3) must print „Tłumaczenie: …”. Give the name(s); they go into the CSV. Takács is marked „adaptacja”: say if it
also needs a translator line.

*Trail: `volumes/18/srom_master_v3.csv` column `translators_struct`.*
