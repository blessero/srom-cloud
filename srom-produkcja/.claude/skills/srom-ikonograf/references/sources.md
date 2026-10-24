# Where to search

Order of work: Tier A (an API the session can query, rights in the data) → Tier B (no usable API: deep links for MB,
the browser for the most promising) → Tier C (ask an institution or person) → paid. Rights notes are defaults; the
item page decides (rights.md). "Tested" = queried successfully on 21.10.2026: from a Cowork session (its web fetch
tools) or from Claude Code on the Mac (curl). Access changes without notice (Cloudflare challenges, rate limits): a
source that fails goes to § 5 of the record and to the next tier; anything untested is a pattern from the provider's
documentation, to be confirmed on first use and marked here.

## Tier A — APIs

| source | strong for | query (replace `<q>`) | from Cowork | from Code (curl) |
|---|---|---|---|---|
| Europeana | aggregator of thousands of European institutions (incl. Hispana/BNE, part of Gallica, many national and regional archives; also BSB, ÖNB, MPI Legal History, Memòria Digital de Catalunya, Romania's culturalia.ro); rights URI per item | `https://api.europeana.eu/record/v2/search.json?query=<q>&qf=TYPE:IMAGE&rows=50&wskey=api2demo` (add `&qf=YEAR:[1700 TO 1900]`, `&reusability=open`; `&profile=rich` adds `edmIsShownBy`, often a direct full-size IIIF image) | tested, web fetch; `edmIsShownAt` = holder's page; `api2demo` is a shared demo key: a free personal key (pro.europeana.eu) if it throttles | tested. Drop `TYPE:IMAGE` for books, laws and dissertations (they are `TEXT`). A law is found by the title of the printed collection it appeared in, not by its own name (Pahulich run: `bulas y pragmáticas` found the Castilian *Pragmáticas*, `pragmática 1499 gitanos` nothing). The thumbnail API returns a grey placeholder for Polona and MBC items: open those in the browser |
| Library of Congress | photos, prints, drawings, maps, FSA/OWI, newspapers | `https://www.loc.gov/photos/?q=<q>&fo=json&c=50` (also `/maps/`, `/collections/…/`) | tested, web fetch (not `/pictures/`: robots); field `rights` | **403** (Cloudflare challenge; WebFetch from Code too). Workaround: LoC images are mirrored on Commons with the LCCN in the file name (search Commons, read `Credit` for the LoC record); image files themselves open on `cdn.loc.gov` and `tile.loc.gov` |
| Wellcome Collection | medicine, anthropology, race science, anthropometry, prints | `https://api.wellcomecollection.org/catalogue/v2/images?query=<q>&pageSize=50` | tested, web fetch; licence id per image (pdm, cc-by …) | tested |
| Internet Archive | scanned books and periodicals (cited sources), Gypsy Lore Society journals | `https://archive.org/advancedsearch.php?q=title:(<q>)+AND+mediatype:texts&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json` | tested, web fetch (titles sometimes dropped: re-query by identifier) | tested; see the IA notes below |
| Wikimedia Commons | everything, uneven; the licence template is on each file page | `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<q>&srnamespace=6&srlimit=50&format=json`; file details (up to 50 files per call, `titles=File:A\|File:B`): `action=query&titles=File:<name>&prop=imageinfo&iiprop=url\|size\|extmetadata&iiurlwidth=400&format=json` | tested, Exa fetch only | tested; **429** after ~10 calls a minute with a bare User-Agent: send `-A "SROM-ikonograf/0.1 (https://studiaromologica.pl; non-commercial journal research)"`, ≥ 2 s apart, batch the file details. Tittel run (21.10.2026): 429 again at 4 s with a UA that had no URL; what held: honour the `retry-after` header (10 s) and wait 8 s between searches. Search matches file titles and descriptions, not subjects: plain English phrases and `intitle:` work better than catalogue terms (Pahulich run: `Roma slavery Romania poster` and `intitle:Münster Gypsies` hit, `Zigeuner Münster` and `robi țigani vânzare` did not). Many files are scans out of modern books or 19th-c. facsimiles (the 1852 slave poster from Hancock 1987, Münster's woodcut via Lacroix): read `Credit`, trace the original, and flag it in § 6 until then |
| MDZ (Bayerische Staatsbibliothek) | German prints and periodicals (*Berlinische Monatsschrift*), early modern edicts and single-sheet mandates (*Einblattdrucke*): the surest source for German cited sources | find the item through Europeana (`dataProvider` Bavarian State Library; `edmIsShownAt` holds the `bsb…` id) or the URN in refs.json; manifest `https://api.digitale-sammlungen.de/iiif/presentation/v2/<bsb-id>/manifest` (canvas labels = printed page numbers; metadata „Call number” = shelfmark); viewer `https://www.digitale-sammlungen.de/view/<bsb-id>?page=<n>` | untested | tested (Tittel); rights NoC-NC on books (class A for a public-domain work), CC BY-NC-SA on some single sheets (class C) |
| Gallica (BnF) | French prints, press, maps, colonial material | SRU: `https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query=gallica%20all%20%22<q>%22&maximumRecords=50` | failed both fetch tools | **403**: the site in the browser; much of Gallica is on Commons and Europeana (search there by `btv1b…`/ark) |
| Smithsonian Open Access | CC0 objects and photos, NMAAHC, anthropology archives | `https://api.si.edu/openaccess/api/v1.0/search?q=<q>&rows=50&api_key=<api.data.gov key>` | failed | tested with `api_key=DEMO_KEY` (low hourly limit); mostly library records: archives (NMAH Archives Center, NAA) are on sova.si.edu, Tier B |
| Openverse | CC/PD aggregator (Commons, Flickr, museums) | `https://api.openverse.org/v1/images/?q=<q>&page_size=50` | failed | tested; thin for historical material (mostly recent Flickr, often NC-ND) |
| DPLA | US libraries, archives, historical societies | `https://api.dp.la/v2/items?q=<q>&sourceResource.type=image&api_key=<key>` (free key by e-mail) | untested; site dp.la meanwhile | untested |
| Metropolitan Museum | paintings, prints; CC0 for public-domain works | `https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=<q>` | untested | **410** to curl: the site in the browser |

Internet Archive notes (tested from Code): a periodical volume is found by its `volume` field, not by title and date
(`q=title:(congressional globe) AND volume:(39th Congress)`); page images are
`https://archive.org/download/<id>/page/n<k>.jpg` (`_w400` for a thumbnail), and `n<k>` can be off by one from the
`leafNum` in `<id>_page_numbers.json`: open the page and read its printed number before citing it; the OCR text
(`<id>_djvu.txt`) finds the passage. Covers: `https://archive.org/services/img/<id>`.
Search inside one item (tested, Tittel run): `https://<server>/fulltext/inside.php?item_id=<id>&doc=<doc>&path=<dir>&q=<word>`
(`server` and `dir` from `https://archive.org/metadata/<id>`, `doc` = the name of its `_djvu.xml` file without that
ending) returns the matching leaves with a snippet: the fastest way to the page a footnote cites. The leaf it gives
was 3 off from `n<k>` in `daskapitalkritik67marx` (exact in `berlinischemona06unkngoog`): look before listing.
Fraktur OCR is poor (`Zigeuner` read as `Bigeuner`: search a neighbouring word, e.g. `Abstamme`), and some items have
no OCR at all (*Teutscher Merkur* 1788: no matches; find the page by its number). Early modern English has the long s
(`Gipſies` OCRs as `Gipfies`): try both, then a neighbouring plain word. A phrase not found in two copies of the cited
edition is a § 6 doubt, not proof it is absent (Pahulich run: Browne 1646 „artificial Negroes”). Google scans on IA
are about 800 px wide and ignore `_w400`: too small for a full page in print, so look for a library's own scan
(HathiTrust, the holder); the Wellcome copies (`b3…` ids) are full size.

Full-resolution files (IIIF, where offered): Library of Congress — the `image_url` with `pct:50.0` replaced by `full`
(`…/full/full/0/default.jpg`); Wellcome — `https://iiif.wellcomecollection.org/image/<id>/full/max/0/default.jpg`;
Gallica — `https://gallica.bnf.fr/iiif/ark:/12148/<ark>/f<page>/full/full/0/native.jpg`; MDZ —
`https://api.digitale-sammlungen.de/iiif/image/v2/<bsb-id>_<nnnnn>/full/full/0/default.jpg` (`<nnnnn>` = canvas,
5 digits); Commons — `imageinfo.url`.
Check that the file opens before listing it for MB.

## Tier B — search pages, browser

**Books and periodicals (cited sources: title pages, plates, quoted pages)**
- HathiTrust (403 to curl from Code, 21.10.2026: the browser) — full-text search finds the books that discuss or picture a subject; then the page images. Full text:
  `https://babel.hathitrust.org/cgi/ls?q1=<q>;anyall1=phrase;lmt=ft` (full view only); catalogue:
  `https://catalog.hathitrust.org/Search/Home?lookfor=<q>`. Rights per volume (pd, pdus = public domain in the US only:
  check the date).
- Google Books, Internet Archive (above), Polona (polona.pl: Polish prints, press, ephemera; filter public domain),
  Biblioteca Digital Hispánica (bdh.bne.es), Gallica, "Internet Archive Book Images" on Flickr (illustrations cut out of
  scanned books, searchable by caption text).

**Photographs and archives — Poland and Central Europe**
- Narodowe Archiwum Cyfrowe (audiovis.nac.gov.pl, szukajwarchiwach.gov.pl): interwar and wartime Poland; reuse terms on
  the item page. IPN: permission needed (a slow route: rights.md § lead times).
- fotopolska.eu: places and buildings, user uploads; authors often unknown (rights.md class E).
- zbioryspoleczne.pl (social archives), Muzeum Budownictwa Ludowego w Sanoku (Reinfuss), Fortepan (fortepan.hu:
  Hungarian photographs, CC BY-SA, credit "Fortepan / <donor>"), Deutsche Digitale Bibliothek, Bundesarchiv (much of it
  on Commons as `Bundesarchiv Bild …`, CC BY-SA 3.0 DE).
- Law, police, edicts: Max-Planck-Institut für Rechtsgeschichte und Rechtstheorie, Digital Libraries Connected
  (dlc.mpg.de; reached through Europeana): the Sammlung Fehr photographs of legal monuments, subject „Abweisezeichen”
  (warning posts such as a „Zigeunerstock”), Public Domain Mark; IIIF v3 manifest
  `https://dlc.mpg.de/api/v2/records/<id>/manifest/`, image `…/files/images/<file>.tif/full/full/0/default.jpg`
  (tested, Tittel run). Search the subject, not „Zigeunerwarntafel” (no hits anywhere). The same library holds early
  modern dissertations and law books (Thomasius, *De Cingaris*, 1671 print, PDM; Pahulich run).
- Romanian lands, Roma slavery: culturalia.ro (national heritage aggregator, via Europeana; Muzeul Național al
  Bucovinei's deeds and lists of „robi țigani”, CC BY-SA 4.0: class B), Biblioteca Academiei Române (charters, *hrisov*,
  on slaves: InC, class D; via Europeana).
- Spanish and Catalan prints: Memòria Digital de Catalunya (mdc.csuc.cat, IIIF `…/iiif/2/<collection>:<id>/full/full/0/default.jpg`,
  PD mark; tested, Pahulich run), Biblioteca Digital Hispánica (above).
- Swiss illuminated chronicles (Schilling: Spiezer, Luzerner, Berner): e-codices (e-codices.unifr.ch, CC BY-NC: class C);
  no answer to curl on 22.10.2026, the browser. Commons copies are small.
- Romani and persecution: RomArchive (romarchive.eu), USHMM collections (collections.ushmm.org), Arolsen Archives
  (collections.arolsen-archives.org).
- Romani Americans (found 21.10.2026, Ostendorf test): NMAH Archives Center, Carlos de Wendler-Funaro Gypsy Research
  Collection, c. 1920–1975 (sova.si.edu/record/nmah.ac.0161; Steve Kaslov among its creators; class D); NYPL, Augustus
  Sherman's Ellis Island portraits (William Williams papers; on Commons via NYPL's Flickr, "No restrictions"); LoC,
  Bain News Service and FSA/OWI photographs (on Commons by LCCN).

**Colonial and Atlantic**
- Archives nationales d'outre-mer (ANOM: the IREL image base, the Colonies series, DFC maps and plans), FranceArchives
  (francearchives.gouv.fr: the national portal of French archival finding aids).
- PARES (pares.mcu.es: Archivo General de Indias incl. Mapas y Planos; Simancas), Hispana (via Europeana).
- Louisiana colonial records (Louisiana State Museum, Louisiana Colonial Judicial Records); NYPL Digital Collections
  (digitalcollections.nypl.org); Newberry (collections.newberry.org); Folger (digitalcollections.folger.edu: early modern
  English prints and theatre, CC BY-SA); Denver Art Museum and other museums for *pinturas de castas* (often via photos on
  Flickr/Commons: trace the museum's own image).

**Maps**
- David Rumsey (davidrumsey.com, CC BY-NC-SA: rights.md class C), Old Maps Online (oldmapsonline.org: a finder across
  map libraries), Library of Congress maps (Tier A), Gallica, AGI Mapas y Planos (PARES).

**Image aggregators (use to find, then trace to the holder)**
- pdimagearchive.org, worldhistory.org (rights per image, many contributed photos), picryl, Look and Learn
  (lookandlearn.com: historical illustration, licensed for a fee).

## Tier C — ask

The author (own archive, field photos); Muzeum Etnograficzne w Tarnowie, part of Muzeum Ziemi Tarnowskiej (formerly
Muzeum Okręgowe w Tarnowie; Roma collection and the Roma history exhibition; the journal's origin and publisher through
vol. 17, so permission should be quick); museums and archives holding an in-copyright item found in
Tier A/B. Letters: rights.md.

## Paid

Alamy (alamy.com): editorial licences; API for partners only, so MB searches by hand from the links the brief gives:
`https://www.alamy.com/search.html?qt=<q>`. Last resort, for a slot with no free or askable candidate.

## Tracing a better copy

For an image known only from a weak copy (Pinterest, a blog, a small Commons file): reverse image search (Google Lens,
TinEye, Yandex: in the browser, or MB by hand); search the catalogued title or the artist and date in Tier A; read the
`source`/`author` fields of the Commons page and the `dataProvider` of a Europeana record; go to the holder's own
page, then its IIIF or download. Record the chain in the record's § 3 (credit = the holder, not the aggregator);
a chain that ends before the holder stays a doubt in § 6.
