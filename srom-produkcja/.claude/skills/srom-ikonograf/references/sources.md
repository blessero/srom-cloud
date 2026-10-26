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
| Library of Congress | photos, prints, drawings, maps, FSA/OWI, newspapers | `https://www.loc.gov/photos/?q=<q>&fo=json&c=50` (also `/maps/`, `/collections/…/`) | tested, web fetch (not `/pictures/`: robots); field `rights` | **403** (Cloudflare challenge; WebFetch from Code too; the app's built-in browser loops on the "verify you are human" page even when MB clicks it, 24.10.2026: never try to pass it; the same box appears in MB's Chrome under Claude in Chrome, 26.10.2026: MB passes it by hand, once, never the model, and the JSON search then runs there). The image server answers (26.10.2026): `https://tile.loc.gov/storage-services/service/pnp/ppmsca/<NN>00/<digital id>v.jpg` (about 1000 px; `cwpb`, `cph`, `ds` have their own folders), so sheet thumbnails need no Commons. Workaround for the records: LoC images are mirrored on Commons with the LCCN in the file name (search Commons, read `Credit` for the LoC record); image files themselves open on `cdn.loc.gov` and `tile.loc.gov` |
| Wellcome Collection | medicine, anthropology, race science, anthropometry, prints | `https://api.wellcomecollection.org/catalogue/v2/images?query=<q>&pageSize=50` | tested, web fetch; licence id per image (pdm, cc-by …) | tested |
| Internet Archive | scanned books and periodicals (cited sources), Gypsy Lore Society journals | `https://archive.org/advancedsearch.php?q=title:(<q>)+AND+mediatype:texts&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json` | tested, web fetch (titles sometimes dropped: re-query by identifier) | tested; see the IA notes below |
| Wikimedia Commons | everything, uneven; the licence template is on each file page | `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<q>&srnamespace=6&srlimit=50&format=json`; file details (up to 50 files per call, `titles=File:A\|File:B`): `action=query&titles=File:<name>&prop=imageinfo&iiprop=url\|size\|extmetadata&iiurlwidth=400&format=json` | tested, Exa fetch only | tested; **429** after ~10 calls a minute with a bare User-Agent: send `-A "SROM-ikonograf/0.2 (Studia Romologica, non-commercial journal research; https://github.com/blessero)"` (no journal domain: the live-site hook would count the call as one to the site, 24.10.2026), ≥ 2 s apart, batch the file details. Tittel run (21.10.2026): 429 again at 4 s with a UA that had no URL; what held: honour the `retry-after` header (10 s) and wait 8 s between searches. Search matches file titles and descriptions, not subjects: plain English phrases and `intitle:` work better than catalogue terms (Pahulich run: `Roma slavery Romania poster` and `intitle:Münster Gypsies` hit, `Zigeuner Münster` and `robi țigani vânzare` did not). Many files are scans out of modern books or 19th-c. facsimiles (the 1852 slave poster from Hancock 1987, Münster's woodcut via Lacroix): read `Credit`, trace the original, and flag it in § 6 until then |
| MDZ (Bayerische Staatsbibliothek) | German prints and periodicals (*Berlinische Monatsschrift*), early modern edicts and single-sheet mandates (*Einblattdrucke*): the surest source for German cited sources | find the item through Europeana (`dataProvider` Bavarian State Library; `edmIsShownAt` holds the `bsb…` id) or the URN in refs.json; manifest `https://api.digitale-sammlungen.de/iiif/presentation/v2/<bsb-id>/manifest` (canvas labels = printed page numbers; metadata „Call number” = shelfmark); viewer `https://www.digitale-sammlungen.de/view/<bsb-id>?page=<n>`; full-text search inside a book `https://api.digitale-sammlungen.de/iiif/services/search/v1/<bsb-id>?q=<word>` (returns canvases; Fraktur OCR is poor: use the book's own index or register, e.g. Münster 1578 „Züginer oder Heiden ccclxxxv”, then the canvas whose label carries that folio, „CCCLXXXV (0525)”; Pahulich run, 24.10.2026) | untested | tested (Tittel); rights NoC-NC on books (class A for a public-domain work), CC BY-NC-SA on some single sheets (class C) |
| Gallica (BnF) | French prints, press, maps, colonial material | SRU: `https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query=gallica%20all%20%22<q>%22&maximumRecords=50` | failed both fetch tools | **403**: the site in the browser; much of Gallica is on Commons and Europeana (search there by `btv1b…`/ark) |
| Smithsonian Open Access | CC0 objects and photos, **NMAAHC (slavery and freedom photographs), NPG**, anthropology archives | `https://api.si.edu/openaccess/api/v1.0/search?q=<q>&rows=50&api_key=$(cat ~/.config/srom/smithsonian_api_key)` | failed | MB's api.data.gov key in `~/.config/srom/smithsonian_api_key` (mode 600, outside every repo; 1,000 requests an hour, tested 26.10.2026; `DEMO_KEY` allows about 4 searches an hour). `/search` returns title, date and the image id; `/content/<id>` the full note (verso inscriptions, names): read it before writing a caption. Image: `https://ids.si.edu/ids/deliveryService?id=<idno with . → _>_001&max_w=900` (the `_001` suffix is part of the id for most NMAAHC items; NPG ids end `_inex`); it hotlinks fine. Library records: archives (NMAH Archives Center, NAA) are on sova.si.edu, Tier B |
| Openverse | CC/PD aggregator (Commons, Flickr, museums) | `https://api.openverse.org/v1/images/?q=<q>&page_size=50` | failed | tested; thin for historical material (mostly recent Flickr, often NC-ND) |
| DPLA | US libraries, archives, historical societies | `https://api.dp.la/v2/items?q=<q>&sourceResource.type=image&page_size=50&api_key=$(cat ~/.config/srom/dpla_api_key)` | untested | tested 26.10.2026 (key in `~/.config/srom/dpla_api_key`, mode 600, outside every repo; MB's key: if absent, `curl -X POST https://api.dp.la/v2/api_key/<e-mail>` and use a Hotmail-type address: a custom domain's mail did not arrive). Dates: `&sourceResource.date.after=1839&sourceResource.date.before=1900`; several records in one call: `…/v2/items/<id1>,<id2>?api_key=…` |
| Northwestern University Digital Collections | Winterton Collection of East African photographs (Grant's 1860 scrapbook: the originals of the Zanzibar slave-market photographs, unwatermarked, free), Africana, Chicago | `https://api.dc.library.northwestern.edu/api/v2/search/works?query=<q>&size=100` (JSON: title, collection, `rights_statement`, thumbnail, `iiif_manifest`); a work's manifest `…/works/<id>?as=iiif` lists its canvases with their captions; image `https://iiif.dc.library.northwestern.edu/iiif/3/<file-set id>/full/!700,700/0/default.jpg` | untested | tested 26.10.2026 (q-slavery19c), no key |
| Metropolitan Museum | paintings, prints; CC0 for public-domain works | `https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=<q>` | untested | **410** to curl: the site in the browser |

Internet Archive notes (tested from Code): a periodical volume is found by its `volume` field, not by title and date
(`q=title:(congressional globe) AND volume:(39th Congress)`); page images are
`https://archive.org/download/<id>/page/n<k>.jpg` (`_w700` for a thumbnail; these redirect: `curl -L`, or the file is empty), and `n<k>` can be off by one from the
`leafNum` in `<id>_page_numbers.json`: open the page and read its printed number before citing it; the OCR text
(`<id>_djvu.txt`) finds the passage. Covers: `https://archive.org/services/img/<id>`. Lending-library items (`…0000…`
ids) answer 403 to search-inside: check a cited monograph's list of plates in the browser.
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
5 digits); MPI dlc (IIIF v3) — `…/full/max/0/default.jpg` (`full/full` answers 400); Commons — `imageinfo.url`.
Check that the file opens before listing it for MB.

**Smithsonian archives (SOVA, NMAH, `si.edu/object/archives`)**, learnt 25.10.2026 (Wendler-Funaro trace): every
Smithsonian page answers curl and WebFetch with 403 („temporarily unavailable” / „request verification”: never try to
pass it). The **Exa tools read them** (`web_search_exa`: describe the item in plain words and the folder or item record
comes back; `web_fetch_exa` on `americanhistory.si.edu/collections/archival-item/sova-<collection>-ref<n>`). A search
result for a series page (`sova.si.edu/record/<coll>/ref<n>`) carries the whole container list (box, folder, date,
extent, scope notes) in one go. The Open Access API above does not hold archival components. A record without the
„Click to open image viewer” line is **not digitised**.

## Tier B — search pages, browser

**Books and periodicals (cited sources: title pages, plates, quoted pages)**
- HathiTrust (403 to curl from Code, 21.10.2026; the built-in browser fails too; opens in Claude in Chrome, the extension in MB's Chrome, 26.10.2026) — full-text search finds the books that discuss or picture a subject; then the page images. Full text:
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
  `https://dlc.mpg.de/api/v2/records/<id>/manifest/`, image `…/files/images/<file>.tif/full/max/0/default.jpg`
  (v3: `full/full` answers 400; Pahulich run, 24.10.2026). Search the subject, not „Zigeunerwarntafel” (no hits anywhere). The same library holds early
  modern dissertations and law books (Thomasius, *De Cingaris*, 1671 print, PDM; Pahulich run).
- Romanian lands, Roma slavery: culturalia.ro (national heritage aggregator, via Europeana; Muzeul Național al
  Bucovinei's deeds and lists of „robi țigani”, CC BY-SA 4.0: class B), Biblioteca Academiei Române (charters, *hrisov*,
  on slaves: InC, class D; via Europeana). culturalia.ro also holds Szathmari's watercolours; BCU Cluj dspace (PD).
- Spanish royal decrees on „gitanos”, 1520–1734: Biblioteca Universidad de Sevilla on Internet Archive (PDM). BNE scans
  re-uploaded to IA by private users: credit BNE and give the BNE copy (bdh.bne.es) as `alt`.
- Costume books and early prints of „Ziegeuner”: Göttingen University collections (sammlungen.uni-goettingen.de, IIIF,
  CC BY-SA; Jost Amman 1577 „Ziegeunerin”); HAB Wolfenbüttel (Boissard, *Habitus* 1581; diglib.hab.de does not answer
  curl: reach it through Europeana, whose `w400` thumbnail proxy works for it); internetculturale.it (Biblioteca
  Marciana's Raffet lithographs). All Pahulich run, 24.10.2026.
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
A better copy found this way goes on the contact sheet as `alt` (link + why it is better; SKILL.md step 4).

**From a printed page or a PDF** (a thesis, an article; the only clue is a caption). Order that worked
(25.10.2026): (1) `pdftotext -layout` the page for the caption and credit; `pdfimages -list` for the embedded image's
size, then render it and look: **is it a scan, a publisher's reproduction or the author's snapshot** (paper edge, glare,
damage, uneven light = a snapshot, unfit for print; say so). (2) The caption names a collection or holder: open the
holder's finding aid, not a search engine first. (3) Match by **subject and title words** against folder and item
records; the title in the thesis is often the archivist's folder title cut short, not a caption on the object: say so in
§ 6 and state how sure the match is. (4) Read the open-access thesis itself (repository handle) for its list of
figures and sources: it names the holder of every picture, which is a lead list for the volume. (5) Date and maker:
the holder's catalogue decides; an author's „circa” is their inference (Kanon § 10.3, 1). (6) Then rights and contact.

## Thumbnails

The sheet's thumbnail is about **700 px wide** (MB, 24.10.2026: at 300–400 px a photograph cannot be judged). Ask the
holder's own resize service for it; nothing is downloaded and no tokens are spent:

| source | thumbnail URL |
|---|---|
| IIIF (BSB, MPG dlc, MDC, ÖNB `iiif.onb.ac.at/images/ABO/<id>/<page>/…`, Wellcome, e-codices, Gallica) | `…/full/700,/0/default.jpg` (ÖNB: `native.jpg`); `!800,800` for tall pages |
| Internet Archive page | `https://archive.org/download/<id>/page/n<k>_w700.jpg` (`services/img/<id>` is a small cover: use a page) |
| Wikimedia Commons | `https://commons.wikimedia.org/wiki/Special:FilePath/<file>?width=960` (resolves by name and redirects to the standard thumbnail: no hand-built hash path, which is easy to get wrong), or `…/commons/thumb/<a>/<ab>/<file>/960px-<file>`: Commons serves only standard widths (500 and 960 work; 700 is refused and 330 is too small, tested 24.10.2026); a file narrower than 960 px: the original URL |
| loc.gov | `…v.jpg` (about 1024 px), not `…t.jpg` or `_150px` |
| Europeana | the thumbnail API stops at `w400`: use the provider's own image (`edmIsShownBy`) as below. A thumbnail of exactly 293×293 px is Europeana's placeholder, not the image (Polona and some culturalia items): blank it |

No resize service, or only a TIFF or a very large file: from Cowork, a `miniatura` row in `pobierz.tsv`
(SKILL.md § Where it runs) does all of the following on the Mac. From Code: download it and make a local copy,
`curl -sL -o <tmp>/<id>.src <url> && sips -Z 800 -s format jpeg -s formatOptions 70 <tmp>/<id>.src --out miniatury/<id>.jpg`
(about 100 KB; JPEG is enough, WebP saves little at this size), and give the row `thumb: "miniatury/<id>.jpg"`, or
give it `src: "mini:<url>"` and let `scripts/kontaktowka_build.py` download it (with a browser User-Agent, for
servers that send curl a placeholder). Every build embeds all of `miniatury/` in the sheet, so that the side panel
and the browser pane show them (neither loads a relative path): there is no separate embed step to forget.

## Learnt in the q-stlouis1904 run (25.10.2026)

**CONTENTdm libraries (Saint Louis Public Library `cdm17210.contentdm.oclc.org`; the same API serves other CONTENTdm
sites).** All tested from Code with `curl` / WebFetch, no key: collections `…/digital/api/collections` (aliases for the
1904 fair: `lpe` glass plates, 6,700; `beals` Jessie Tarbox Beals; `lpephotos` three scrapbooks; `fair` ephemera);
search `…/digital/api/search/collection/<alias>/searchterm/<word>/order/nosort/page/1/maxRecords/100` (one word, plain;
returns titles and ids); metadata `…/digital/api/collections/<alias>/items/<id>/false` (title, description, call number,
rights statement, filename); image `…/digital/api/singleitem/image/<alias>/<id>/default.jpg` and IIIF
`…/digital/iiif/<alias>/<id>/full/700,/0/default.jpg` (the bare `…/iiif/<alias>/…` path answers 404). SLPL titles are
cataloguer's, not captions: „Chief of the Gypsies from the Streets of Cairo” is the library's wording.

**Whole-fair period publications on Internet Archive** (1904 St. Louis; the same pattern fits any exposition): list
them with `advancedsearch` (`title:` or `subject:` + `date:[1903-01-01 TO 1906-12-31]`), then grep each `_djvu.txt` for
the period's name for the people (`scripts/ia_find.py`). Halftone books carry their captions in the text layer.
Worked: *Jackson's famous photographs* (`jacksonsfamousph01jack`, the LoC copy: one hit, the target). OCR hits that
were only context: *On the Pike* (booklet of concessions), *Greatest of Expositions* („singing gypsies” of Cairo),
*World's fair manual* („Gypsy Lane of Barcelona”). Several good books have no `_djvu.txt` hit because the caption is
in the image only (the Missouri Historical Society albums).

**Missouri Historical Society albums, 11 volumes, 867 pages, on Commons** (`File:Louisiana Purchase Exposition- St.
Louis World's Fair Album <n> - DPLA - <hash> (page <k>).jpg`; MHS Open Access, NKC). List them with
`list=allpages&apnamespace=6&apprefix=Louisiana Purchase Exposition- St. Louis World's Fair Album`; a thumbnail at any
width with `prop=imageinfo&iiurlwidth=500` (30 titles per call). Vol. 10–11 = the Pike and the native peoples; the
handwritten caption is under each print (no OCR): look at them (`scripts/montage.py --grid`). Pages are good prints,
not the „bad quality” a user may remember.

**Hyku / university photograph archives** (University of Louisville `digital.library.louisville.edu`, Ford albums):
the catalogue search page works through the Exa fetch tool, not through WebFetch (503). Item pages carry the
rightsstatement.org URI and the handwritten caption in the description.

**Commons search.** `list=search&srnamespace=6` matches file titles and some wikitext, but returned 0 for phrases
that sit in the description of the album pages: enumerate the category or prefix instead. Category names: take them from
a `list=search&srnamespace=14` query on the subject (e.g. „… at the Louisiana Purchase Exposition”).

**Tools that did not work here:** LoC `loc.gov` search (403, as above); `collections.mohistory.org` (403);
`dp.la` search page (empty); Europeana `api2demo` for 1904-fair queries (0); Adam Matthew *World's Fairs* (subscription:
catalogue descriptions only, which name the subjects of a volume, useful for choosing the album volume).


## Routes found 25–26.10.2026 (slavery query q-slavery19c); read before searching

**Pages and records that curl cannot reach, but Exa can.** loc.gov, Brasiliana Fotográfica, Gallica, NMAAHC pages answer 403 to curl and WebFetch. `web_search_exa` returns cached copies of their record pages (title, call number, rights, verso notes) and `web_fetch_exa` reads a given URL (it times out on loc.gov, works on Brasiliana). Use it to read records and to find which items exist; the picture then comes from the image server, never from the page.
**Image servers that answer when the pages do not:** LoC `https://tile.loc.gov/storage-services/service/pnp/ppmsca/<NN>00/<digital id>v.jpg` (the id is the LC-DIG-ppmsca number; `cph`, `cwpb`, `ds` have their own folders); Getty `https://media.getty.edu/iiif/image/<uuid>/full/!700,700/0/default.jpg` (uuid from the object page's og:image); Smithsonian `ids.si.edu` (above); Commons `Special:FilePath/<file>?width=960`.
**Commons by category, not by search.** `list=categorymembers` on `Category:Photographs of slaves in <Brazil|Cuba|Zanzibar|Iran|Palestine|the United States>`, `Photographs of former slaves`, `Category:Photographs by <photographer>` returns whole sets with accurate file names (a title search found a third of them). Then `prop=imageinfo&iiprop=url|size|extmetadata` for 25 titles a call; read `Credit` for the holder and the LCCN/NAID. Several files are covers, verso scans or cropped details of a book plate: look at every thumbnail.
**Curated lists are the best seeds.** National Humanities Center *African Americans in Slavery, Photographs 1847–1863* (13 images with holders), LoC reference aids (`loc.gov/rr/print/list/…`, web.archive copies), the Center for Civil War Photography (*Battlefield Photographer*), Slavery Images' item sets, exhibition pages, and the scholarship an item is cited in (Skolnik on the Alexandria pens). A sample the user gives is traced first (its holder and neighbours: LoC 2018670634 → LC-B811-2299 → the sibling frames).
**Collections with an API:** University of Miami Cuban Heritage Collection (CONTENTdm): `…/digital/bl/dmwebservices/index.php?q=dmQuery/<alias>/subject^<term>^any^and/title/title/100/1/0/0/0/0/json`, items `dmGetItemInfo/<alias>/<pointer>/json`, images `…/digital/iiif/<alias>/<pointer>/full/700,/0/default.jpg`; **curl gets a grey placeholder (identical bytes for every item) and the browser refuses to hotlink: fetch with Python `urllib` and a browser-like User-Agent, save to `miniatury/` and embed**. Slavery Images: `…/database/search-result.php?ad_search=Y&row_si=Field20&row_cnd=6&row_st=<term>&page_n=<n>` (the paging parameter is `page_n`; a wrong one loops forever: cap the pages). Most of its 1,200 items are engravings reproduced from books; check `Source` on the item page. Internet Archive: `<id>_djvu.txt` for the list of illustrations, `_page_numbers.json` for leaf numbers (a Google scan often omits the plates).
**Brazil:** IMS (`acervos.ims.com.br`) is a JavaScript app; IMS releases about 10,000 public-domain images for download (page `ims.com.br/por-dentro-acervo/ims-disponibiliza-download-imagens-dominio-publico/`); the National Library's Brasiliana Fotográfica holds Christiano Júnior (handles `20.500.12156.1/6502–6504`, `5528`) and the Museu Histórico Nacional's 1865 album. **Cuba:** BNJM does not answer; Dumont and Mestre (1865–66) are in a UNAM thesis (Kitlinski) and the Montané Museum. **Indian Ocean:** RMG Graham-Stewart slavery collection (the Commons copies are watermarked record shots with the ZBA inventory number visible), TNA CO 1069/FO 84, Seychelles register B 85 (IHOI exhibit `ihoi.org/app/photopro.sk/ihoi_expo/publi?docid=91003`). IHOI search: `https://www.ihoi.org/searchBM?query=<term>` in the built-in browser (a canvas app: `get_page_text` for the titles, a region `zoom` screenshot for a thumbnail, saved to `miniatury/` and embedded). Zanzibar market photographs: take Northwestern's Winterton originals (Tier A) before the RMG copies. IMS (`acervos.ims.com.br`) shows the same Cloudflare box as loc.gov: MB, by hand.

**Shell and tool traps met (macOS, zsh):** `timeout` does not exist; `sed -i ''` needs the empty suffix; `set -- $p` does not word-split in zsh (it wrote files named `S11-c 1497.jpg`: use Python or `read`); `python3 -u` or `print(flush=True)` when output goes through `head`, or a stuck loop shows nothing; Commons answers 429 to a 12-image montage built in one go (sleep 6 s between files); a browser tab may be replaced after a long idle (`tab-1 shows a local file`): navigate again in the tab the tool names.

**loc.gov search through MB's Chrome (works):** after MB ticks Cloudflare's 'Verify you are human' once in the extension's own Chrome window (the tab group opens as a separate window; the model never clicks it), run in that tab a background loop (`window.__run=(async()=>{…})()`; the tool call dies at 45 s) over `fetch('/photos/?q=<q>&fo=json&c=100&sp=<n>&dates=1840/1899&fa=online-format:image')`, keep only records whose `item.medium` names a photograph, albumen print, stereograph, daguerreotype, tintype, ambrotype or negative, and read the result by writing it into the page body and calling `get_page_text` (the JS return value is cut at about 1,000 characters; localhost fetches are refused). Thumbnails: `image_url` without its `#h=…` suffix is a `tile.loc.gov` JPEG. Queries that found most: `enslaved`, `slaves`, `slave quarters`, `fugitive slave`, `freedmen`, `contrabands`, `slave pen`, `plantation negroes`.

**Yale (26.10.2026):** `archives.yale.edu` blocks (403/503); `collections.library.yale.edu/catalog?q=<q>&rows=100` works in the built-in browser; item pages carry `og:image` = `…/iiif/2/<file id>/full/!1200,630/0/default.jpg`; replace the size with `!700,700` for a thumbnail. The Beinecke 'Land of Zenj' collection (GEN MSS 619) holds the 'Slave-trade in East Africa' series (query `"Land of Zenj" slave`). **loc.gov rate limit:** about 150 JSON requests in 15 minutes ended in 403 for every request; space them (5 s, at most 40 per session) and expect to pass the check again.
