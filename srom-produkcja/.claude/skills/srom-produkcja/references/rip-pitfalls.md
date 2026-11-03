# RIP pitfalls — what cost time in earlier rips (read before step 1b/3/4b)

One line per trap: the symptom, the cheap fix. Added from the Davis RIP (03.11.2026); append a line when a rip loses more than
ten minutes to something a note here would have prevented. Tool bugs are not listed here (they go to a C-item), only what to do meanwhile.

## PDF in (step 1b)
- **Publisher boilerplate mid-paragraph.** Open-access T&F/Routledge PDFs put CONTACT, ©, the licence text and the first footnote on the
  page-2 foot, which the extractor leaves in the middle of the Introduction's paragraph ("…both states aimed to transform removed |
  CONTACT… | children into…"). Look at page 2 as an image; cut the block and rejoin the paragraph. Same for running heads.
- **Tables float in print** (top of a page, mid-paragraph, even rotated 90° on their own page) and the extractor splits the paragraph
  around them and shreds the cells. Rebuild each table as a pipe table by hand from the page image, put it after the first paragraph
  boundary, rejoin the paragraph, and leave a `<!-- DO SPRAWDZENIA -->` comment with the printed position. Never trust cell text from the extractor.
- **Table notes break the extractor's marker order** (EXTRACT CHECK "marker order", "unmarked"): expected, read and resolve, do not chase.
- **Write the clean-up as a script** (`work/<id>/prep.py`: regex cuts, each asserted to match exactly once, logged to `prep_log.md`), never by
  hand-editing `_pdf.md`: a re-run after a fix must give the same file. Do the cuts that open a long dependency chain first (what you cut out
  of a paragraph must not be needed by a later cut).

## refs.json (step 3)
- **No `null` anywhere.** A `None` field (`container-title`, `publisher`, `issued`) makes pandoc stop with "expected String or Number, but encountered
  Null" and no key name. In `refs.py` helpers drop `None` values before dumping; if the error appears, grep refs.json for `null`.
- **A work cited only by a short form** ("Kaps, ‘Differences’, 146–7") still needs an entry, with `[BRAK …]` for what the author did not give:
  a note that mixes a key and the literal short form fails `check.py --keyed` ("page numbers lost"), and a literal note that names an author in
  refs.json fails it ("cited but not keyed"). Enter it, key the note, put the missing data in the queries. Never complete it from memory.
- **The author's slips stay as written** (`srom-as-written` for the form the original note uses: a misspelt surname, a shortened title), flagged in
  the notes sheet; otherwise the keyed check cannot find the author in the original note.
- **The year is not a page.** "*Title*, 1990 on page 235" makes the check count 1990 as a page: leave such a note literal and say so.

## Keying (step 4b)
- **Run `check.py --keyed` on a skeleton early** (every note literal, 5 notes keyed), then widen: 25 errors at once hide which are real.
- **Notes in table cells**: the check does not walk tables (C38), so any note in a cell shifts the pairing of all later notes. Put a table's note in
  `::: tabela-zrodlo` when it is the table's source (Kanon § 10); a note inside `::: tabela-tytul` breaks the alignment too. If a cell note must stay,
  gate on a throwaway copy of `scripts/` patched as in C38 and say so in the notes sheet; never edit `$P` for it in a rip.
- **A press/archive locator next to a key** ("*PZ* (31 May 1780): 5; [@x, s. 210]"): the check reads the colon page only when a key is present and
  then finds it lost. Write "…, s. 5" and flag the normalisation, or key the whole note.
- **`mutate_keyed.py` misses** on "Name, ‘Title’, 322", "*Short,* 1st ed., 107", "[Letter], 168": the check does not see those locators (C38). Verify by
  hand with the check's "other numbers not in rendering" warnings: whatever remains must be an edition, volume, month or year.
- **Same page twice in one note** (two "cited in Robinson, 104"): citeproc prints the second as Ibidem without the page; the check flags a lost page.
  Expected; confirm both are the same work and page.
