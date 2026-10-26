# Hand-off: ikonograf tooling from the slavery query (26.10.2026), for a higher model

Context: query `q-slavery19c` (168 candidates, 16 slots). The work was done with ad hoc scripts, now in
`workspace/srom-produkcja/work/q-slavery19c/ikonografia/_tools/` (`cs.py` Commons search, `cat.py` Commons category
listing, `info.py` Commons imageinfo batch, `sia.py`/`sic.py` Smithsonian search/content, `si.py`/`sir.py` Slavery
Images, `eu.py` Europeana, `items.py` + `build.py` the sheet builder). Method notes are already in
`srom-ikonograf/SKILL.md` § Method that worked and `references/sources.md` § Routes found. What remains is
**new functionality (not for a Sonnet session)**:

1. **`scripts/kontaktowka_build.py`**: one command that turns a rows file (`rows.tsv`/JSON: id, slot, source kind,
   source key, title, date, creator, holder, class, why, metryka, alt) into `kontaktowka.html`. Source kinds:
   `commons:<file>` (thumb via FilePath, full via imageinfo, size, page), `loc:<ppmsca id>` (tile.loc.gov),
   `si:<ids id>`, `getty:<uuid>`, `url:<thumb>`; `mini:<id>` = download with Python urllib + browser UA into
   `miniatury/` and embed (sources.md § Thumbnails) so that the embed step cannot be forgotten (it is wiped by every
   rebuild: it happened twice). Replaces `items.py`/`build.py`, which hold content in Python source.
2. **`scripts/montage_check.py`** (or a JS snippet in the sheet): after build, report broken images and write a
   contact montage JPEG for a look by eye; Commons rate limit means sleeping 6 s per file.
3. **`scripts/commons_info.py` + `commons_category.py`**: the two Commons helpers cleaned up (retry on 429 with the
   `retry-after` header, resumable cache, `Credit` parsed for LCCN/NAID/IA ids).
4. **Smithsonian**: add a personal api.data.gov key to `~/.config/srom/` (like the DPLA key) and use it in `sia.py`;
   DEMO_KEY lets about four searches an hour.
5. **Test**: a small fixture sheet built by (1), and the preflight line, once it is in `scripts/`.
6. **Check rule to add to Kanon-side or the skill**: a row's `metryka` draft is built from the data fields only
   (date, maker, holder, shelfmark, rights); the generator can produce it from the structured fields so that it cannot
   drift from the row (today written by hand in `items.py`).

Also open: connect Claude in Chrome (MB logged in 26.10.2026) for loc.gov search, HathiTrust; built-in browser for
IHOI, IMS, Yale and Northwestern Winterton (JavaScript sites); Louisiana State Museum and Kentucky Gateway Museum
need letters (rights.md § Letters), not searches.

## Status (root, 26.10.2026 16:01) [general]
1. **Done:** `srom-ikonograf/scripts/kontaktowka_build.py` — the sheet built from `kontaktowka.json` (the DATA shape; `src` kinds
   commons, loc, si, ia, iiif, getty, mini), the current template on every build, `miniatury/` re-embedded on every build,
   MB's copy in `Claude outputs/` refreshed; `pobierz.py` rebuilds a record whose rows file is newer. `--from-html` ported all
   five sheets (Ostendorf18 21, Pahulich 74, q-slavery19c 232, q-stlouis1904 7, Tittel 21 rows: DATA identical, every thumbnail
   still embedded). `_tools/items.py` + `build.py` are superseded (they could no longer run: `info1–7.json` were not kept, and
   passes 6–7 were edited into the sheet by hand).
2. **Partly:** broken images need a browser, so the count stays SKILL.md step 5 (count twice); the build lists rows with no
   thumbnail, holder or metryka; `montage.py` makes the montage.
3. **Folded into 1:** Commons imageinfo (`--commons-info`: 25 a call, `retry-after` honoured, cached in
   `kontaktowka.commons.json`); category listing is `commons_pages.py --category`. No separate scripts.
4. **MB's:** a free api.data.gov key into `~/.config/srom/` (as for DPLA) when Smithsonian is searched again.
5. **Done:** 11 tests in `test_ikonograf.py` (fixture build, every `src` kind, `</script>` escaped, re-embed on rebuild,
   four refusals, pobierz rebuild, from-html).
6. **Declined:** generating the metryka from the fields would be worse than the hand drafts (Kanon § 10.3 wants technique
   and Polish date forms the fields do not carry); the build reports rows without one instead.
