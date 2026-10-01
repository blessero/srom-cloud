# Gates: 1.5.4a Third text, intake — [Pahulich] "Racialization of Roma, European Modernity, and the Entanglement of Empires" (CRS 8/1, 2025; T18)

Scope: receive the source (T18), survey what the article needs (quotation rules per quote, Polish editions, originals of
third-language quotes, terminology, group names, doubts in the source). MB asked (29.09.2026) to go ahead without his
feedback and collect his decisions for later, so no gate waits for MB: open choices are recorded as assumptions in the
intake and the notes sheet. The draft is leaf 1.5.4b. (Leaf 1.5.3 is Ostendorf, run by a parallel session.)

- [x] G1: the four source files in `work/pahulich/src/` are identical to srom-produkcja's (T18 hashes)
  NOTE 01.10.2026 17:21 [general]: srom-produkcja renamed `<id>_queries.md` to `<id>_uwagi.md` (29.09.2026 23:13); the manifest here still lists the old name, so the count is now 3, not 4. The copy in `src/` keeps the old name. No CHECK change (review 01.10.2026 item 6).
  CHECK: cd "../srom-produkcja/work/pahulich" && shasum -a 256 -c "../../../srom-tlumacz/work/pahulich/src/manifest.sha256" | grep -c ': OK$'
  EXPECT: /^4$/m

- [x] G2: intake file covers procedure features, Polish editions and originals, terminology, doubts in the source, plan
  CHECK: grep -c '^## [1-5]\. ' work/pahulich/pahulich_intake.md
  EXPECT: /^5$/m

- [x] G3: every Polish-edition and original-text claim in the intake is backed by a catalogue or text check (manual)
  EVIDENCE: BN data.bn.org.pl queries 29.09.2026: Fraser „Dzieje Cyganów” (Klekot, PIW 2001); Federici „Kaliban i czarownica” (Król, Karakter 2025, 2 records); Césaire „Rozprawa z kolonializmem” (Jaremko-Pytowska, Czytelnik 1950); Said „Orientalizm” (PIW 1991; Zysk 2018); Mróz CEU 2015 record with uniform title „Dzieje Cyganów-Romów w Rzeczypospolitej”, translator J. Fomina (+ AUP/CEU page: "translation of the Polish original") and DiG 2001; Bielski 1564 „Kronika tho iesth, Historya Swiata…” (+ 1551 first ed., 1976 facsimile); Przyłuski „Leges seu Statuta…” dated 1551; no records for Robinson, Wynter, Lewy (Nazi Persecution), Willems, Shohat, Melamed, Grellmann. Texts: Grellmann German 1787 and English 1787/1807 downloaded from Internet Archive, parallels in `work/pahulich/research/grellmann_de.md` (German normalised from OCR, marked to check against the scan); Dal' «Цыганка» full text (ru.wikisource, `research/dal_cyganka.wiki`) searched: quoted phrases absent. Unverified items are labelled in the intake (Przyłuski date, Ghica, Münster, Dal' text).
