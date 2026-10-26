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
