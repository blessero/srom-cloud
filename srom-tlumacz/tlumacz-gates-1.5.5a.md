# Gates: 1.5.5a Fourth text, intake — [Tittel] "Racial and Social Dimensions of Antiziganism: The Representation of “Gypsies” in Political Theory" (On_Culture 10, 2020; T20)

Scope: receive the source (T20), survey what the article needs (quotation rules per quote, Polish editions, originals of
third-language quotes, terminology, group names, doubts in the source). MB asked (29.09.2026) to go ahead without his
feedback and collect his decisions for later, so no gate waits for MB: open choices are recorded as assumptions in the
intake and the notes sheet. The draft is leaf 1.5.5b.

- [x] G1: the four source files in `work/tittel/src/` are identical to srom-produkcja's (T20 hashes)
  NOTE 01.10.2026 17:21 [general]: srom-produkcja renamed `<id>_queries.md` to `<id>_uwagi.md` (29.09.2026 23:13); the manifest here still lists the old name, so the count is now 3, not 4. The copy in `src/` keeps the old name. No CHECK change (review 01.10.2026 item 6).
  CHECK: cd "../srom-produkcja/work/tittel" && shasum -a 256 -c "../../../srom-tlumacz/work/tittel/src/manifest.sha256" | grep -c ': OK$'
  EXPECT: /^4$/m

- [x] G2: intake file covers procedure features, Polish editions and originals, terminology, doubts in the source, plan
  CHECK: grep -c '^## [1-5]\. ' work/tittel/tittel_intake.md
  EXPECT: /^5$/m

- [x] G3: every quotation in the source has one row in the quotes sheet (count of quotation rows = quotations found by hand, listed in the intake)
  CHECK: awk -F'\t' 'NR>1' work/tittel/tittel_quotes.tsv | wc -l | tr -d ' '
  EXPECT: /^3[0-9]$/m

- [x] G4: every Polish-edition and original-text claim in the intake is backed by a catalogue or text check (manual)
  EVIDENCE: BN data.bn.org.pl queries 29.09.2026: Kant *Antropologia w ujęciu pragmatycznym* (IFiS PAN 2005); *Religia w obrębie samego rozumu* (Znak 1993, Homini 2007, Dzieła zebrane t. 5 UMK 2011); *Pisma przedkrytyczne* (Dzieła zebrane t. 1, UMK 2010) with the publisher's table of contents (PDF sample: „O różnorodnych rasach ludzkich”, s. 859); *Pisma po roku 1781* (Dzieła zebrane t. 6, UMK 2012) with the publisher's page (product 2503: „Określenie pojęcia rasy ludzkiej” s. 99, „O użytku zasad teleologicznych w filozofii” s. 161); *Rozprawy z filozofii historii* (Antyk 2005, contents incl. the teleology essay); Marx *Dzieła* t. 23 (KiW 1968), t. 3 (1961, 1975), *Zarys krytyki ekonomii politycznej* (KiW 1986). Originals read: Kant AA II 439, VI 136–137, VII 324–325, VIII 105, 172, 174, XV 597 (korpora.org); MEW 23 ch. 23–24 with MEW pagination (biancahoegel.de; pages checked by script: 9 match, n. 49 = p. 741 not 743); 1926–33 Polish *Kapitał* (Wikisource) for comparison; Leipzig study items (Uniklinikum Leipzig press release, Zentralrat). Not reached, labelled in the intake: MEW 3 and 42 German text, Röttgers 1997, Geulen lecture, Decker book pp. 102–103; Also BN: *Dialektyka oświecenia* (IFiS PAN 1994; KP 2010, 2023), *18 brumaire'a Ludwika Bonaparte* (KiW 1949–1980; KP 2011). Detail: `work/tittel/research/originals.md`.
