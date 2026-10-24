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

**Place in the pipeline:** whenever MB asks, whatever the text's state (a pool candidate, chosen, translated or not)
— the earlier the better, because permissions take weeks and Kanon § 10.1 wants them gathered before the text is
accepted. Its output feeds INJECT (files and captions placed in InDesign by MB).

**Every run is meticulous** (MB, 24.10.2026). The text's state, its place in the queue or the volume never lowers the
effort and is not commented on. MB would rather look at many candidates and discard most of them, hoping for a rare find
or an angle he had not thought of, than get a lean set: give him the surplus (secondary slots, more candidates per
slot, finds seen in passing). The limit is relevance, not count: every slot and every candidate is tied to a passage, a
cited source or the volume's axis, and says why in one line; nothing is added to fill a number. A slot that yields
nothing good says so in § 5 instead of being padded.

## Files

| what | where |
|---|---|
| MB's way of illustrating: principles and worked cases (**read before every brief**) | `references/patterns.md` |
| where to search: repositories by tier, query templates, what was tested from Cowork and from Code | `references/sources.md` |
| rights classes, credits, finding the contact, permission letters (EN; PL/ES/FR on request) | `references/rights.md` |
| per-text record and contact sheet (templates) | `assets/template/ikonografia.md`, `assets/template/kontaktowka.html` |
| one text's work | workspace `srom-produkcja/work/<id>/ikonografia/`: `ikonografia.md`, `kontaktowka.html`, `zgody.md` (letters, step 7), `pliki/` (chosen files), `miniatury/` (local thumbnails, step 5) |

`<id>` is the text's work folder. Check in `STATUS.md` that `work/<id>/` holds the text MB means: one author can have
texts in two volumes (Ostendorf: the vol. 18 article, and the vol. 19 chapter in `work/ostendorf/`). A text with no
work folder of its own (a Polish original that skipped RIP, or a second text by an author who already has one): create
`work/<id>/ikonografia/` with the author's surname as `<id>`, plus the volume when the surname is taken
(`ostendorf18`); the record's heading names the text by title and volume. Always there, never in a scratchpad, test
runs included: a scratchpad is wiped and the volume's next run cannot read it.

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
   Read the other texts of the same volume that have an `ikonografia/` record (`ls work/*/ikonografia/`): vol. 19's
   texts share sources (Grellmann in four of them, the *Zigeunerstock* in two). Reuse their finds and searches, and log
   nothing they already logged as failed. An image another text already proposes is **proposed again** where it fits
   this text, with `also` on the contact sheet ("Tittel S1-a"; another edition or page of the same work too, saying
   so) and the same note added to the other sheet: MB decides which text it serves better (MB, 24.10.2026). Once he
   has chosen it for one text, the other sheet's row says so.
2. **Brief** (`ikonografia.md` § 1). Slots, each tied to a passage (page or heading + a few words): type (cited
   source, place/map, building, person, event, document/archive, ethnographic image, comparative addition), the idea
   in one line, the angle (documentary / immersive / argument / extension), search terms. Size: the **printed target**
   stays about **8 images for an average-length article**, more for long ones, about **4** when they supplement what
   the author supplied (patterns § 1). What is proposed is about **twice the target**: core slots (≈1.5× the target)
   plus **secondary slots**, marked ², for less obvious angles, comparative material and images that might inspire a
   choice MB had not planned. Mark extensions beyond the text (patterns § 8) as such, and only where the author
   implies them here or in related work, or where the volume's axis calls for them (srom-zizek's
   `volumes/<vol>/concept.md`). Flag permission-needed slots with holder and lead time (patterns § 12).
3. **Cited sources first.** From the footnotes and bibliography, list every primary source (prints, edicts, laws,
   periodicals, archival files, maps, dissertations, early travel and ethnographic books) and look for digitised
   copies of each, not only the ones a slot names: title page, plate, frontispiece, and **the page with the quoted
   passage** (sources.md: search inside the scan; read the printed page number by eye). These are the surest hits
   (sources.md § Books and periodicals). A source cited second-hand ("cyt. za") is looked up in the original too.
   **Footnote leads** (`ikonografia.md` § 7). The notes also point to images the main text never names: an illustrated
   monograph, travel book or exhibition catalogue, an article with figures, a photo collection, an image the note
   describes. Read every note once; each note that carries a lead gets a row (note, cited work, what it may hold),
   whether or not it is checked now. Check cheaply: open the cited work's list of illustrations, plates or figures
   (digitised copy, publisher page), not its text; a lead that opens a new one gets its own row. Most leads give
   nothing: record that in one word, so the table shows what was looked at and nobody looks again. Unchecked rows stay
   open for **przypisy** (below). Every lead is fair game, including secondary literature MB would not reach from the text.
4. **Search** every slot, core and secondary. Per slot, a term ladder: the subject in the archive's language; period
   ethnonyms and exonyms (Cyganie, Zigeuner, Bohémiens, Égyptiens, Gitanos, Egyptians, Gypsies, Cigány, Țigani, robi …),
   historic place names (Lemberg/Lwów/Lviv, Nouvelle-Orléans, Warschau), catalogue subject headings, the title of the
   printed collection a law or decree appeared in; date ranges. Order: Tier A APIs → Tier B deep links (and the browser
   for the most promising) → Tier C asks → paid. Aim at **3–6 candidates a slot**, at least one needing no permission
   (patterns § 12); more when they are good. Finds seen in passing that fit another slot, or no slot yet but the text,
   go in too (marked "seen in passing"). Trace every weak copy to its holder (sources.md § Tracing). A better copy found
   (larger scan, the original's holder rather than an aggregator, colour, a freer licence) goes on the sheet as
   `alt`: a direct link (to the item or page itself where it can be found, else the collection, saying so) and why it is
   better in a few words; never "better holder" without the link and the reason. Log searches that
   found nothing (§ 5 of the record), so nobody repeats them.
   **Doubts** (§ 6 of the record): anything that does not square is flagged there, never silently corrected or left
   out (root CLAUDE.md § Doubts in the material): a quoted phrase not found in the cited edition (full-text search,
   then by eye; then the later editions' full text, since a phrase can enter in a later edition: Browne's „Artificial
   Negroes, or Gypsies” is in 1658 and 1672, not in the 1646 Pahulich cites); an image on Commons or in a book that is a later facsimile or copy, not the original, or a
   modern re-typeset text passed off as a document (a Commons „sale of 200 Gypsy families”, typeset from Hancock 2002:
   the thumbnail check by eye catches it); a known image
   whose original holder cannot be traced; dates or editions that differ between the article, the catalogue and the
   aggregator; an aggregator's description (a Commons title) that is not the holder's catalogue title. Each doubt says
   what was checked and what would settle it. MB finds these among the most useful parts of a record.
5. **Contact sheet.** Fill `kontaktowka.html` (copy the template; edit only the `DATA` block): per candidate the
   thumbnail URL (about **700 px wide**, enough to judge a photograph without opening the holder's page: sources.md
   § Thumbnails), title as catalogued, date, creator, holder and shelfmark, rights class (rights.md), largest size
   available, the item page and the full-resolution URL, one line on why it fits; `alt` and `also` where they apply.
   **Deliver** as the root CLAUDE.md § Files MB must open says: send `kontaktowka.html` and `ikonografia.md` with
   SendUserFile (display render) as the turn's last tool call: the card is MB's button. End the reply with the
   `Files to open:` line (name, text, absolute path; 🔴 is for files, never for chat).
   Look at the thumbnails yourself when a browser tool is available (open the sheet, screenshot); otherwise say the
   triage was by metadata only. Also count the broken ones (in the browser pane:
   `[...document.images].filter(i => !i.naturalWidth).length` after a few seconds) and fix or drop each. Open the key
   pages (a cited source's title page, the quoted page) at size, in a montage of thumbnails if there are many, to see
   that each shows what its row says: a scan's first leaf is often a cover or a blank.
6. **MB chooses.** For each chosen image (`ikonografia.md` § 3): `Il. n`, file name `<id>_il<nn>_<slug>.<ext>` in
   `pliki/`, a draft caption in Polish per Kanon § 10.1–10.2 (dry; date and place as they really are, patterns § 3),
   the credit, the rights class, the permission state. Files: from Claude Code on the Mac, `curl -L -o` the
   full-resolution URLs into `pliki/` (the Commons User-Agent from sources.md; a few seconds apart); from Cowork the
   VM shell reaches none of the repositories, so give MB the list of full-resolution links to save into `pliki/`
   (one click each).
7. **Permissions** (rights.md), for the chosen images only. Per holder: find the best contact (rights.md § Finding
   the contact: a named person and e-mail where one can be found, alternatives when unsure, each with where it was
   found), then draft one English letter listing all that holder's items with their catalogue data, into `zgody.md`,
   ready for MB to send (`🔴 zgody.md` in the record's § 4). MB sends; the date and the answer go in § 4. For class E,
   the due-diligence record. Anything that needs MB (a fee, a risky
   orphan, a crop of an ND image) is one question in `MB-decisions.md` under the text's code.
8. **Close.** One line in the text's section of `STATUS.md` (from Code: in the K-item, § Who writes what): `Ikonografia: <chosen>/<target>, <k> permissions
   pending (<holders>)`. When MB explains a choice or a rejection worth keeping, add it to `patterns.md` § Cases
   (a small skill change: C-item for Code to commit).

## What MB can ask for

| MB says | Ikonograf does |
|---|---|
| **ikonograf** <text> | steps 1–5 in full: brief, every cited source, every slot searched, contact sheet; MB cuts on the sheet |
| **brief** <text> | steps 1–3 only: brief plus cited-source hits, when MB wants to cut slots before the search |
| **szukaj** / search <text or slot> | steps 4–5 for the brief's open slots (or the one slot named) |
| **lepsza kopia** <image or link> | trace the original holder and the largest copy of a known image (sources.md § Tracing) |
| **zgody** <text> | step 7 for the chosen images: contacts, letters in `zgody.md`, due diligence, the state of each |
| **przypisy** <text> | the open rows of § 7 (footnote leads): check each, add what they yield to the sheet |
| **podpisy** <text> | captions for the chosen images (Kanon § 10), credits checked against the item pages |

## Limits (tested 21.10.2026 from Cowork and from Claude Code)

- The VM shell on MB's Mac reaches none of the repositories; Cowork searches with the session's web fetch tools.
  Working: Europeana, loc.gov `fo=json`, Wellcome, Internet Archive (web fetch), Wikimedia Commons API (Exa fetch).
  Not reachable that way: Gallica SRU, Smithsonian, Openverse.
- Claude Code on the Mac (curl): Europeana, Wellcome, Internet Archive, Commons (with a named User-Agent),
  Smithsonian (demo key), Openverse work; loc.gov search, HathiTrust and Gallica SRU answer 403 (Cloudflare), the Met
  API 410. Neither route reaches every source: the table in sources.md says which to use, and the browser covers the
  rest.
- Contact sheet in the browser pane: a `file://` page opens as a static `data:` snapshot (screenshots and the
  broken-image count above work; clicks do not; relative paths do not load, hence the embedded local thumbnails);
  to click through, serve the folder (`python3 -m http.server` on 127.0.0.1). The app's side panel renders the sheet
  with remote thumbnails (Pahulich, 22.10.2026); Ostendorf's sheet, the one with `loading="lazy"`, showed only
  placeholders there (the likely cause, not proven): the template has no lazy images.
- The live-site hook (`~/.claude/hooks/srom-throttle.py`) treats any curl naming the journal's domain as a call to the
  site, User-Agent included: never put the domain in a User-Agent or a query (sources.md gives one without it).
- Alamy's API is for partners only: links for MB, no automation.
- Taste is calibrated on two cases so far (vol. 18: Gontarek, Ostendorf); expect misses until patterns.md has more.
  The vol. 19 test runs (Tittel, Pahulich, 21–22.10.2026) become cases once MB has chosen from them.
  A test run on a text already in § Cases is not blind: the case lists the answers. Test on a text that is not there.
