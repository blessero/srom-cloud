---
name: srom-ikonograf
description: Sourcing illustrations for Studia Romologica (SROM) articles. Reads a text, proposes an illustration brief (slots tied to passages, angles, search terms in period and catalogue vocabulary), searches digitised collections (APIs first, then deep links and the browser), builds a contact sheet with rights classes, and after MB's choice records files, draft captions, credits and permission requests. Use for "ikonograf", ilustracje, ryciny, zdjęcia do artykułu, "find images/illustrations for", sourcing visuals, prawa do ilustracji, zgody na ilustracje, permission letters for images, "where is a better copy of this image". Not for caption rules themselves (srom-kanon § 10), placing images in InDesign (srom-produkcja, INJECT) or the article licence (srom-kanon knowledge base).
---

# srom-ikonograf — illustrations for SROM articles

Many texts reach SROM with no or too few visuals. Ikonograf proposes what an article could show and finds it in
digitised collections that a Google search does not reach. MB decides; the angle on each article is his, and the
skill's job is to widen his options and do the slow parts: footnote mining, multilingual searching, rights triage,
files, credits, permission letters. Journal facts (publisher, ISSN, licences): srom-kanon
`references/SROM_knowledge_base.md`. Caption structure and register: Kanon § 10 (cite it; never restate it here).

**Place in the pipeline:** any time after a text is chosen (srom-zizek) — the earlier the better, because permissions
take weeks and Kanon § 10.1 wants them gathered before the text is accepted. Its output feeds INJECT (files and
captions placed in InDesign by MB).

## Files

| what | where |
|---|---|
| MB's way of illustrating: principles and worked cases (**read before every brief**) | `references/patterns.md` |
| where to search: repositories by tier, query templates, what was tested from Cowork and from Code | `references/sources.md` |
| rights classes, credits, permission letters (PL/EN/ES/FR) | `references/rights.md` |
| per-text record and contact sheet (templates) | `assets/template/ikonografia.md`, `assets/template/kontaktowka.html` |
| one text's work | workspace `srom-produkcja/work/<id>/ikonografia/`: `ikonografia.md`, `kontaktowka.html`, `pliki/` |

`<id>` is the text's work folder. Check in `STATUS.md` that `work/<id>/` holds the text MB means: one author can have
texts in two volumes (Ostendorf: the vol. 18 article, and the vol. 19 chapter in `work/ostendorf/`). A text with no
work folder of its own (a Polish original that skipped RIP, or a second text by an author who already has one): create
`work/<id>/ikonografia/` with the author's surname as `<id>`, plus the volume when the surname is taken
(`ostendorf18`); the record's heading names the text by title and volume.

**Who writes what.** The record, the contact sheet and `pliki/` are written by whichever session runs the skill:
Cowork, or Claude Code on the Mac (an exception to "Code never writes `workspace/`", like srom-zizek's data, and only
in `work/<id>/ikonografia/`). `STATUS.md` and `MB-decisions.md` stay Cowork's: a Code session sends the step 7
questions and the step 8 line as a K-item in `_handoffs/code-to-cowork.md` (headed "needs MB" when it carries a
question), and Cowork enters them.

## The steps

1. **Read.** The text (`work/<id>/<id>_src.md`, or the PDF/DOCX MB names), its `refs.json` if RIP made one, and
   any images the author supplied (count them; note their state and rights). Read `references/patterns.md`.
   Ask the author (Tier C) at once, in one short e-mail sent by MB (rights.md § Letters, Author): the author's own
   photographs of the archival documents cited, field photographs, and any images the author would suggest.
   Archival historians often hold the only usable copy (Ostendorf's photograph of the 1779 marriage record, vol. 18);
   record the date in § 4 and treat the answer as a slot's first candidates.
2. **Brief** (`ikonografia.md` § 1). Slots, each tied to a passage (page or heading + a few words): type (cited
   source, place/map, building, person, event, document/archive, ethnographic image, comparative addition), the idea
   in one line, the angle (documentary / immersive / argument / extension), search terms. Size: about **8 images for an
   average-length article**, more for long ones; about **4** when they supplement what the author supplied. Propose
   ~1.5× the target so MB can drop slots. Mark extensions beyond the text (patterns § 8) as such, and only where the
   author implies them here or in related work, or where the volume's axis calls for them (srom-zizek's
   `volumes/<vol>/concept.md`). Show MB the brief before searching more than the cited-source slots, unless he
   said to go straight on.
3. **Cited sources first.** From the footnotes and bibliography, list primary sources (prints, edicts, periodicals,
   archival files, maps, early travel and ethnographic books) and look for digitised copies: title page, plate,
   frontispiece, the page with the quoted passage. These are the surest hits (sources.md § Books and periodicals).
4. **Search.** Per slot, a term ladder: the subject in the archive's language; period ethnonyms and exonyms
   (Cyganie, Zigeuner, Bohémiens, Égyptiens, Gitanos, Egyptians, Gypsies, Cigány, Țigani …), historic place names
   (Lemberg/Lwów/Lviv, Nouvelle-Orléans, Warschau), catalogue subject headings; date ranges. Order: Tier A APIs →
   Tier B deep links (and the browser for the one or two most promising) → Tier C asks → paid. Stop a slot at 2–4
   good candidates, at least one of them needing no permission (patterns § 12). Log searches that found nothing
   (§ 5 of the record), so nobody repeats them.
5. **Contact sheet.** Fill `kontaktowka.html` (copy the template; edit only the `DATA` block): per candidate the
   thumbnail URL, title as catalogued, date, creator, holder and shelfmark, rights class (rights.md), largest size
   available, the item page and the full-resolution URL, one line on why it fits. Tell MB to open it from Finder.
   Look at the thumbnails yourself when a browser tool is available (open the sheet, screenshot); otherwise say the
   triage was by metadata only.
6. **MB chooses.** For each chosen image (`ikonografia.md` § 3): `Il. n`, file name `<id>_il<nn>_<slug>.<ext>` in
   `pliki/`, a draft caption in Polish per Kanon § 10.1–10.2 (dry; date and place as they really are, patterns § 3),
   the credit, the rights class, the permission state. Files: from Claude Code on the Mac, `curl -L -o` the
   full-resolution URLs into `pliki/` (the Commons User-Agent from sources.md; a few seconds apart); from Cowork the
   VM shell reaches none of the repositories, so give MB the list of full-resolution links to save into `pliki/`
   (one click each).
7. **Permissions** (rights.md): for class D, a letter in the holder's language from the templates, the date sent and
   the answer in § 4 of the record; for class E, the due-diligence record. Anything that needs MB (a fee, a risky
   orphan, a crop of an ND image) is one question in `MB-decisions.md` under the text's code.
8. **Close.** One line in the text's section of `STATUS.md` (from Code: in the K-item, § Who writes what): `Ikonografia: <chosen>/<target>, <k> permissions
   pending (<holders>)`. When MB explains a choice or a rejection worth keeping, add it to `patterns.md` § Cases
   (a small skill change: C-item for Code to commit).

## What MB can ask for

| MB says | Ikonograf does |
|---|---|
| **ikonograf** <text> / brief | steps 1–3: brief plus cited-source hits |
| **szukaj** / search <text or slot> | step 4–5 for the brief's open slots (or the one slot named) |
| **lepsza kopia** <image or link> | trace the original holder and the largest copy of a known image (sources.md § Tracing) |
| **zgody** <text> | step 7 for the chosen images: letters, due diligence, the state of each |
| **podpisy** <text> | captions for the chosen images (Kanon § 10), credits checked against the item pages |

## Limits (tested 21.10.2026 from Cowork and from Claude Code)

- The VM shell on MB's Mac reaches none of the repositories; Cowork searches with the session's web fetch tools.
  Working: Europeana, loc.gov `fo=json`, Wellcome, Internet Archive (web fetch), Wikimedia Commons API (Exa fetch).
  Not reachable that way: Gallica SRU, Smithsonian, Openverse.
- Claude Code on the Mac (curl): Europeana, Wellcome, Internet Archive, Commons (with a named User-Agent),
  Smithsonian (demo key), Openverse work; loc.gov search, HathiTrust and Gallica SRU answer 403 (Cloudflare), the Met
  API 410. Neither route reaches every source: the table in sources.md says which to use, and the browser covers the
  rest.
- Contact sheet in the browser pane: a `file://` page cannot be driven; serve the folder (`python3 -m http.server`
  on 127.0.0.1) and open it by URL to look at the thumbnails.
- Alamy's API is for partners only: links for MB, no automation.
- Taste is calibrated on two cases so far (vol. 18: Gontarek, Ostendorf); expect misses until patterns.md has more.
  A test run on a text already in § Cases is not blind: the case lists the answers. Test on a text that is not there.
