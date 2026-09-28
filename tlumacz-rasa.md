# Register: race, racialisation and their surroundings (srom-tlumacz, leaves 1.3.5, 1.3.5b)

Started 28.09.2026 19:14, rebuilt 28.09.2026 20:23 [general]. A reference for translating EN texts on race and the
racialisation of Roma, and the material around them (Iberian, Atlantic, Russian-imperial, Polish 17th–20th c.).
**Not binding.** Binding forms are the HOUSE rows of `tlumacz-tb.tsv`. The CANDIDATE rows there (C-0019, C-0024–C-0028,
C-0031, C-0036–C-0040) point here. The termbase admits a row only for choice, convention, edition or trap (schema §
Admission, MB 28.09.2026). Everything else lives here, and **loaded designations are decided per case** (§ 0, § B).

**When to load it:** when translating a text on race, racialisation, colonial or early-modern othering. It is not
needed for other texts. Termbase lookup is exact-match and reports only hits, so the rows cost nothing elsewhere.

**Sources** (full texts in `training/`, keys and bibliographic lines in `training/sources.tsv`, sha256 in the
manifest). Cited below as [key]. Works they only cite are marked *via [key]*: these were not read and count as no
evidence.

| Key | Text | Use |
|---|---|---|
| taradejna | Folia Sociologica 88 (2024), sociology | vocabulary; weak on facts and names (§ F) |
| nowak | „Klio” 72/3 (2024), Romantic "racialisation of the nation" | solid |
| nowak2021 | SFPS 56 (2021), race nomenclature 1740s–1864 | period synonyms of „rasa” |
| wrzesinska | SFPS 56 (2021), „rasa” and synonyms 1864–1918 | period synonyms; "not every *rasa* is racism" |
| wolniewicz | „Przegląd Historyczny” 104/4 (2013), racial discourse in 1863 propaganda | Moskwa / Ruś / Turanie |
| malczynski | „Tematy z Szewskiej” 3 (13) (2014), race and nationalism | blood, mixture, passing, metysaż |
| malczynski_mincer | same issue, editorial | „uchodzenie za” (passing) |
| kubica | chapter (WUJ 2015), race in the history of anthropology | period anthropology terms; Polish editions of classics |
| rys | online essay (2023), glossary of class racism and related terms | protorasizm vs rasizm klasowy; dehumanisation terms |

"WK" marks my working knowledge, **not** from the corpus. It is a starting point to check when a text needs it,
never a citation.

## 0. How to decide per case

**Three voices.** The same designation is handled differently depending on who is speaking:

| Voice | Example | Treatment |
|---|---|---|
| **1. Period quotation** (a source quoted by the author) | a 1650 traveller's "Moors", a 1900 anthropologist's "Negro" | Polish original if one exists (Kanon § 12.2.4); otherwise translate **in period register**: the period designation, not a modern euphemism. Do not sanitise and do not add offence. |
| **2. Author reporting period usage** | "contemporaries called them *Egyptians*", "the category 'Negro' in the census" | Period designation, marked as the author marks it: quotation marks or italics where the author distances. MB D11 (4): period *Blackamoor* / *negro* → „Murzyn”; *Mores* → „Maurowie”. |
| **3. Author's analytic voice** | "Black Roma", "racialised Muslims" | The current neutral Polish form (HOUSE rows first: C-0013 czarni lower case, D11). If the author deliberately uses an old or loaded term in their own voice, respect it (§ 12.2: author's term choices), and query when it would read as the translator's own offence. |

**Rules of thumb from the corpus:**
1. **A period „rasa” is not automatically racism** [wrzesinska]. It often means nation, tribe or stock: "rasa polska", "rasa słowiańska", "rasa łacińska" [nowak; nowak2021; wrzesinska]. Keep the period sense; don't sharpen or soften it.
2. **Anachronism works both ways** [rys]: „protorasizm” (C-0019) for Old-Polish noble ideas, „rasizm klasowy” from the 19th century on. Don't call pre-modern othering „rasizm” unless the author does.
3. **The author's quotation marks around "race" are kept**: „rasa”, „urasowienie” (malczynski writes both in quotation marks throughout).
4. **Period Polish sources may not say „rasa” at all** before about 1850: ród, plemię, pokolenie, szczep, familia [nowak2021]. When quoting them from the Polish original, never "correct" the term.
5. **Offensive period forms appear only in voices 1 and 2.** The translator never introduces them into voice 3.
6. **Group names of Roma** are governed by the kartoteka (srom-kanon) and Kanon § 12.2.6, not by this register. Early-modern "Egyptians" → „Egipcjanie” (D13).

## A. Concepts

Rows exist only where the admission rule holds. The rest is listed so that it is not harvested again.

| Polish | English | Row / note |
|---|---|---|
| urasowienie / urasawianie | racialisation | C-0001 (HOUSE). The imperfective is native: taradejna's title; Bobako 2010's title „…jako urasawianie” (via rys); rys: „urasawiający”, „samourasawiający”. |
| protorasizm (szlachecki), szlachecki protorasizm stanowy | proto-racism (gentry) | C-0019. Ryś's full form is for Old-Polish noble ideas about commoners and foreigners. |
| Inny / Obcy | the Other / the alien | C-0024. Capitalisation follows the source. |
| piętno; stygmatyzacja | stigma; stigmatisation | C-0025. Goffman: Polish edition *Piętno*. |
| heteroreferencyjny / autoreferencyjny, samoreferencyjny | hetero- / self-referential | C-0028 (Ryś's coinage in this field). |
| bytowość | entitativity | C-0038 (Bilewicz et al., via rys). |
| metysaż | mestizaje, métissage | C-0037. |
| uchodzenie za / przechodzenie | passing | C-0036 (COMPETING). |
| rasizm kulturowy; neorasizm, „rasizm bez ras” | cultural racism; neo-racism, racism without races | No row (obvious calques). Blaut's Polish translation 2003 [malczynski; rys]; Balibar [rys]. |
| rasizm inteligencji | racism of intelligence | No row. Bourdieu; the Polish translation (2006) covers **only the opening paragraphs** [rys]: quote the rest in our own translation, flagged. |
| rasizm klasowy | class racism | Retired C-0020: obvious. Period use per rys: 19th c. on (Balibar, Traverso). |
| dehumanizacja, infrahumanizacja, animalizacja, demonizacja, biologizacja, mechanizacja, reifikacja; hiperhumanizacja | dehumanisation etc.; hyper-humanisation (rys's own) | No row (obvious) [rys]. |
| esencjalizm, esencjalizacja, naturalizacja | essentialism, -isation, naturalisation | Retired C-0023. *naturalizacja* = also the grant of citizenship: watch the passage. |
| klasizm; chamofobia | classism; (no EN equivalent: contempt for the "boorish" rural and lower classes) | No row. *chamofobia* is Polish-only (A. Tatarkiewicz, H. Domański, via rys). |
| akulturacja (Pasolini) | acculturation | **Trap, no row:** in Pasolini's sense it is the destruction of popular cultures by consumerism [rys]; in anthropology *acculturation* is culture contact. Follow the author's source. |
| orientalizacja | orientalisation | No row [rys]. |
| prymordializm; etnia; etnonacjonalizm; nacjonalizm obywatelski / etniczny | primordialism; ethnie; ethno-nationalism; civic / ethnic nationalism | No row [malczynski]. *ethnie* (A.D. Smith, van den Berghe) → „etnia”. |
| naród polityczny / kulturowy | *Staatsnation* / *Kulturnation* | No row [wolniewicz n. 6]. |
| argument rasowy, argument rasowo-antropologiczny | racial (-anthropological) argument | No row [nowak; wolniewicz]. |
| urasowienie narodu; przenarodowienie rasy; unarodowienie / unaradawianie | racialisation of the nation; (nowak: "transmutation of race"); nationalisation | No row [nowak; taradejna]. *przenarodowienie* is a period term (TDP, 1848/49). Nowak's English is free, not literal. |
| atrybutywne / dystrybutywne rozumienie kultury | attributive / distributive concept of culture | No row [kubica]. |
| monogeneza / poligeneza; ewolucjonizm | monogenesis / polygenesis | No row [kubica]. |
| typ rasowy, typ ludzki, typ rasowo-antropologiczny | racial type, human type | No row. The last is Krzywicki's period term [wrzesinska; kubica]. |
| *Rassenkunde*, antropologia ras, eugenika | race science (German), eugenics | No row. Keep the German, italic [kubica]. |
| rasizm naukowy, dyskurs rasowy, mit rasowy, przemoc symboliczna, medykalizacja, biologizm, przedmurze, przekleństwo Chama | scientific racism, racial discourse, racial myth, symbolic violence, medicalisation, biologism, bulwark (*antemurale*), curse of Ham | Retired rows C-0021, C-0022, C-0029, C-0030, C-0032–C-0035 (MB: obvious). |
| zwrot plebejski; władza dyskursywna | plebeian turn; discursive power | No row [taradejna; rys]. |

## B. Loaded designations: history, register, current status

Each cluster gives the period Polish forms with their sources, what they carried, where they stand today, and how to
treat them in the three voices (§ 0). The decision is always made per passage.

### B1 „Rasa” and its period synonyms
- **Before about 1850** the foreign word *rasa* was rare, explained or avoided in Polish writing. First anthropological use: W. Majewski 1827, "Rassa (race), czyli plemię" [nowak2021]. Linde 1812 knows only „rasa” as a woollen cloth / from Arras [nowak2021]. The stand-ins were: *ród* (all humankind, or a race, or a clan; also social rank: „ród szlachecki”), *pokolenie*, *plemię* („plemię ludzkie”, or a race: „plemię kaukaskie”), *szczep* (usually a group of related peoples: „szczep słowiański”), *familia*, *gatunek*, *odmiana*, and descriptive phrases such as „ludzie innego koloru” [nowak2021].
- **1864–1918**: *rasa* spreads, still used interchangeably with plemię, szczep, gałąź, lud, naród, typ, odmiana [wrzesinska]. Period collocations include: rasa indoeuropejska / indo-kaukaska / kaukaska; rasa łacińska; rasa europejska; plemię Jafeta (dying out); aryowie, aryjczycy [wrzesinska]. Also: przesąd rasowy, nienawiść rasowa, antypatia rasowa, walka ras (Gumplowicz), dusza rasy, instynkt rasy, czysta krew [wrzesinska]. The adjectives *rasowy*, *etniczny*, *etnologiczny* and *etnograficzny* were used as near-synonyms [wrzesinska].
- **"race" = nation** in Romantic writing: „rasa polska”, „rasa sarmacka” (Fisz), „rasa mongolska” for Russians (Krasiński) [nowak; nowak2021]. „Rasa szlachecka” means a social estate [nowak2021].
- **Voices.** In voice 1, EN period "race" → „rasa”; don't archaise to *plemię* unless the source itself distinguishes "race" from "tribe". In Polish originals keep whatever word they use. In voice 3, keep the author's marks („rasa”).

### B2 Black people: Murzyn, negr, czarny, czarnoskóry, Mulat
- **Period forms:**
  - „Murzyn” is an old Polish word, from Bible translation (nck.pl; to check in Boryś).
  - 19th-century print has the lower-case common noun: „murzyni” in an 1865 list of Morocco's peoples [wrzesinska]; the title „Cywilizacja ziemi murzynów” (1842); „trzy szczepy: Indianie, Murzyni i biali Anglosasi” (1864) [nowak2021].
  - Collocations: „lud rodu czarnego” (1827–28 travel press) and Duchiński's „trzy wielkie rody tzw. biały, żółty i czarny” [nowak2021]; „rasa murzyńska” (Krzywicki 1893) [kubica]; „rasa czarna” [taradejna].
  - Tylor's Polish translation (1889) has both „afrykański Murzyn” and „głowa negra” (so *negr* is a period loan) [kubica].
  - Huxley–Haddon (Polish ed. 1937): „czarnych, białych, żółtych i brunatnych” [kubica].
- **20th–21st-c. scholarship:** Małczyński capitalises „Czarny”, „nie-Biały”, „krew Czarnych” and uses „Mulat” as a period category [malczynski]; Taradejna uses „czarnoskórzy”, „Afroamerykanie” [taradejna]. **House:** lower-case *czarni / biali* (C-0013, MB D11). The capitalised forms are native precedent, reported for information only: the lock stands.
- **Current status:** the Rada Języka Polskiego adopted M. Łaziński's opinion on 26.10.2020: *Murzyn* only „na prawach historycznego cytatu”. The opinion discusses *czarnoskóry*, *czarny*, nationality names and *Afrykanie* (rjp.pan.pl, read 28.09.2026).
- **Voices:**
  - 1 and 2: MB D11 (4): period *negro* / *Blackamoor* → „Murzyn”. Keep the source's case and spelling in quotations from Polish originals.
  - 3: czarny / czarnoskóry / Afroamerykanin as the author has it (Black → czarni, lower case).
  - WK, OPEN: EN "colored / coloured" (US period category) and South African "Coloured" (a legal category): no Polish form in the corpus. Keep the original in the SA case and query.
- **Etymology** (secondary, as MB asked): Boryś — Old Czech *muřín* < Latin *Maurus*; Brückner 1927 — German *Mohr* < Latin *maurus*; Bańkowski — doubts the Latin origin. The semantic link to *Maur* is the point: for centuries the Polish word covered dark-skinned Africans and "Moors" loosely.

### B3 Moors, Saracens, Turks, Moriscos, "Mahometans"
- **Corpus:**
  - „Maurowie” in 1828 is a mixed people: „ród pomieszany z potomków dawnych Numidów czyli Mauretanów, Arabów, Hiszpanów, Saracenów i Turków”, defined by culture rather than descent [nowak2021].
  - 1865, lower case: „maurowie, arabowie, berbery, murzyni i żydzi” as the „plemiona” of Morocco [wrzesinska].
  - „pokolenie mahometańskie” (1836) means a community of faith [nowak2021].
  - Taradejna uses „Maurowie” for Iberian Muslims after the Reconquista, with „konwertyci” [taradejna].
  - MB D11 (4): *Mores* → „Maurowie”. Row C-0027 (pointer).
- **WK (to check when a text needs it):**
  - *Saracen*: a late-antique name for Arab tribes; in medieval Latin Christendom a generic name for Muslims (crusades, Sicily, the Mediterranean); Polish „Saraceni” in medieval and crusade historiography.
  - *Moor*: Iberia and the Maghreb; early-modern English also uses it loosely for any dark-skinned African or Muslim.
  - *Turk* in early-modern Europe often means any Muslim or Ottoman subject; "to turn Turk" → „poturczyć się”, „poturczeniec”.
  - *Mahometan* → period „mahometanie”, „mahometański”; today „muzułmanie”.
  - *Moriscos* → Moryskowie (baptised Muslims in Spain; expelled 1609–1614); *mudéjares* → mudejarowie; *conversos*, "New Christians" → konwertyci, „nowi chrześcijanie”; *marranos* (pejorative) → marrani, in quotation marks.
  - These are Christian exonyms of their period.
- **Voices:**
  - 1 and 2: keep the period exonym (Saraceni ≠ Maurowie ≠ Turcy: don't merge them).
  - 3: follow the author. „Maurowie” is still standard in Polish historiography of al-Andalus. Where the author says "Muslims of al-Andalus", don't substitute „Maurowie”.
  - Never render *Moor* as „Murzyn” (C-0027 avoid). The reverse, *Blackamoor* → „Murzyn”, is MB's D11.

### B4 Russia and its neighbours: Moskwa, Moskale, Ruś, Rusini, Tatarzy, Turanie
- **Corpus** [wolniewicz]:
  - The 1863 propaganda and Duchiński separated *Moskwa* (Muscovy) from *Ruś*. Duchiński wanted "Moskwa", never "Rosja", and the whole 1772 Commonwealth as Aryan Slavdom against „Turanian” Muscovites.
  - Latin *dux Moscorum* vs *dux Russorum et Ruthenorum*.
  - French *Russie* vs *Ruthénie*, *ruthène*. *Ruthènes* was also the official Austrian name of Ukrainians in Galicia (n. 81).
  - The „świat czudzki / fiński”; the „Ruś finno-normańska”; „ziemie zabrane”.
  - Nowak: „Moskale”, „jak ich pejoratywnie określano”; „horda”, „dzicz”, „rasa mongolska”, „Mongolczyk” (Trentowski) and „Kałmuk” (Mochnacki) as insults [nowak].
  - Turanie: C-0039.
- **Voices:**
  - 1 and 2: keep *Moskale*, *horda* and the rest as quoted period terms.
  - 3: follow the author.
  - EN "Russian" in early-modern or Commonwealth contexts may stand for Latin *Rutheni* → „ruski”, „Rusini”, not „rosyjski”: check the source language behind the English.
  - EN "Ruthenian(s)" → Rusini / ruski (period). Modern Ukrainians or Belarusians only if the author means them.
  - EN "Muscovy" → Moskwa, Państwo Moskiewskie (WK; per case, like place names, MB 27.09.2026). "Muscovites": WK „Moskwicini” in historiography, never „Moskale” in voice 3.
  - Group names (Rusini etc.) belong to the kartoteka (srom-kanon): raise them there if a text needs them.

### B5 Aryans, Indo-Europeans, "Caucasians", Japhet
- **Corpus:**
  - Ariowie / Aryans vs Turanie [wolniewicz; nowak].
  - Period spellings: aryowie, aryjczycy, aryoeuropejczycy; „naród praaryjski”; rasa kaukaska / indo-kaukaska / indoeuropejska; „plemię Jafeta”, fading by the 1870s [wrzesinska].
  - „familia indo-europejska” (Libelt); „mowa hindo-germańska” (Majewski 1827) [nowak2021].
  - Krzywicki: „rasa słowiańska”, „romańska” mean only linguistic solidarity; „rasa biała”, „murzyńska” each contain several types [kubica].
  - Huxley–Haddon 1937: „rasa aryjska”, „rasa łacińska” "nie do przyjęcia" [kubica].
  - Row: C-0040.
- **Voices:**
  - 1 and 2: the period form.
  - 3: „Indoeuropejczycy” for the linguistic sense.
  - Trap: *Arian* (Arius) is a different word.
  - WK: in Nazi-era contexts „aryjczycy”, „aryjski” („strona aryjska”, „papiery aryjskie”).

### B6 Peasants and the gentry: cham / Cham / Jafet, Sarmaci, czerń
- **Corpus:**
  - The gentry's genealogies: nobles from Jafet, peasants from Cham, or from Cain (the „mit chamicko-jafetycki”) [rys; taradejna].
  - **Trap:** these ideas "had little to do with Sarmatism", because the Sarmatian genealogy covered all Poles; Trepka and Potocki, "the greatest noble proto-racists", did not invoke it [rys]. Taradejna links the two („szlachcice jako legendarni Sarmaci, chłopi jako podbici tubylcy”, after Ryś 2019) — so don't render "Sarmatism" as the source of noble racism unless the author does.
  - *czerń*: WSJP: 'chłopstwo', a 17th-c. name for the peasantry of Ukraine, from *czarny*. Koziołek (via taradejna) has 'monastic peasants', from *czerniec* (F9). Ryś quotes a present-day „wiejskiej czerni” as a chamophobic slur [rys].
- **Voices:** the capitalised biblical Cham vs the insult *cham*; keep the source's.

### B7 "Savages", "natives", "tribes", "Indians"
- **Corpus:**
  - Kubica (quoting Polish translations of 1889–1913): „dzicy” (in quotation marks), „ludy pozbawione kultury / historii”, „rasy jasne i ciemne” (Haberlandt), „krajowcy” (Torres Strait) [kubica].
  - „tubylcy”, in quotation marks [taradejna].
  - Indians: „pokolenia Indian koloru miedzianego” (1828) [nowak2021]; „rasa czerwono-skórnych” (1872) and a dehumanising 1866 description [wrzesinska].
- **Voices:**
  - 1 and 2: the period word, in quotation marks where the author distances.
  - 3, WK: *natives* → „rdzenni mieszkańcy”. *Indians* → „Indianie” is still standard Polish; „rdzenni Amerykanie” where the author says *Native Americans*.
  - *tribe* → „plemię” is loaded in both languages: keep the author's choice.

### B8 Jews in racial vocabulary
- **Corpus:**
  - „lud hebrajski”, „plemię semickie”, „rasa semicka”, „plemię Izraela” (1880s–1890s) [wrzesinska].
  - Lower-case „żydzi” in the 1865 list [wrzesinska].
  - Huxley–Haddon: no "Jewish race"; the Jews are a „grupa pseudo-narodowa” (Polish ed. 1937) [kubica].
  - „krew żydowska” in racial beliefs (Ossowski) [malczynski].
- **Voices:** keep period forms in voices 1 and 2. WK: current Polish spelling has *Żyd* (nation) vs *żyd* (religion); follow the author's meaning.

### B9 Blood, mixture, crossing
- **Corpus** [malczynski]:
  - After Ossowski, *Więź społeczna i dziedzictwo krwi*: „dziedzictwo krwi”, „obca krew”, „dominacja i recesja krwi”, „więzy krwi”.
  - „zasada jednej kropli krwi” (the US *one-drop rule*), „międzyrasowy mezalians”, „mieszańcy”, „Mulat”.
  - „metysaż” (C-0037); „przechodzenie (tzw. passing)” (C-0036); „rasizm kulturowy”, „rasizm religijny”; WASP.
- **Other sources:**
  - „czystość rasowa”, „tygiel rasowy” (*melting pot*, Polish ed. 1937), „mieszaniec” [kubica].
  - „czysta krew” [wrzesinska].
  - „czystość krwi”, „statuty czystości krwi”, Poliakov's „kult czystości krwi” (C-0026) [taradejna; rys].
- **Voices:**
  - These are the actors' categories: in voice 3 keep the author's quotation marks.
  - *miscegenation* (a US period legal term): no row. WK: „związki / małżeństwa międzyrasowe”; in voice 1 „mieszanie ras”; laws → „zakazy małżeństw międzyrasowych”.

## C. US figures and stereotypes

| EN | Polish treatment | Note |
|---|---|---|
| *acting white* | original + gloss „zachowywanie się jak biały” | C-0031. |
| Sambo | original | Taradejna prints „Santo” (F2). |
| Jezebel | original | Taradejna: „Jezebelle” (F2). |
| welfare queen | original + gloss | Taradejna: „Welfare Mother” (F2). |
| myth of the Black rapist | „mit czarnego gwałciciela” | Taradejna, after Davis; quote the Polish edition (§ E). |
| drapetomania | *drapetomania* + gloss | Cartwright 1851 (F7). |
| one-drop rule | „zasada jednej kropli krwi” | [malczynski]. |

## D. Old Polish texts (for quotations: Kanon § 12.2.4, the Polish original wins)

- **Trepka**, *Liber generationis plebeanorum („Liber chamorum”)*, wyd. W. Dworzaczek, J. Bartyś, Z. Kuchowicz, Wrocław:
  Ossolineum 1963, cz. 1–2 (BPP B 13). *Verified* in WorldCat and HathiTrust / Open Library.
- **Potocki**, *Transakcja wojny chocimskiej*: redaction 1, ed. A. Brückner, BN I 75 (1924; one source); redaction 2, ed.
  M. Kuran, J. Okoń (Wydawnictwo UŁ; year to check).
- 19th-c. Polish sources quoted in the corpus (Mochnacki, Duchiński, Trentowski, Norwid, Krasiński, Pol, Staszic,
  Surowiecki, Krzywicki, Gumplowicz, emigré periodicals …): use the bibliographies of nowak, nowak2021, wrzesinska and
  wolniewicz as finding aids. Nothing is re-listed here, and nothing has been verified by me.
- Pahulich (T18): Przyłuski 1553, Bielski 1564, Diet acts 1510 and 1578 (via Mróz): Polish texts needed for § 12.2.4.

## E. Polish editions of works cited in the corpus (for quotations; as cited, not checked)

| Work | Polish edition as cited | Cited in |
|---|---|---|
| Goffman, *Stigma* | *Piętno. Rozważania o zranionej tożsamości*, GWP (2007) | taradejna |
| Foucault, *L'ordre du discours*; *Histoire de la sexualité* | *Porządek dyskursu*; *Historia seksualności*, słowo/obraz terytoria | taradejna |
| A.Y. Davis, *Women, Race & Class* | *Kobiety, rasa, klasa*, Karakter 2022 | taradejna |
| E. Traverso, *La violence nazie* | *Europejskie korzenie przemocy nazistowskiej*, KiP 2011 (chapter „Rasizm klasowy”) | taradejna; rys |
| P. Bourdieu, "Le racisme de l'intelligence" | „Rasizm inteligencji”, „Le Monde Diplomatique” (ed. pol.) 2006, nr 3: **opening paragraphs only** | rys |
| J.M. Blaut, "The Theory of Cultural Racism" | „Teoria rasizmu kulturowego”, „Lewą Nogą” 2003, nr 15 | malczynski; rys |
| L. Poliakov, *Histoire de l'antisémitisme*, t. 1 | *Historia antysemityzmu*, t. 1, Universitas 2008 | rys |
| D. Eribon, *Retour à Reims* | *Powrót do Reims*, Karakter 2019 | rys |
| M. Billig; B. Anderson; E. Said; M. Douglas; C. Geertz; A.D. Smith; C. Calhoun; T.H. Eriksen | *Banalny nacjonalizm* 2008; *Wspólnoty wyobrażone* 1997; *Orientalizm* 2005; *Czystość i zmaza* 2007; *Interpretacja kultur* 2005; *Nacjonalizm* 2007; *Nacjonalizm* 2007; *Etniczność i nacjonalizm* 2013 | malczynski |
| J. Vasconcelos, *La raza cósmica*; G. Freyre, *Casa-grande & senzala* | *Rasa kosmiczna. Wybór*, CESLA 1993; *Panowie i niewolnicy*, PIW 1985 | malczynski |
| C. Darwin, *The Descent of Man* | *O pochodzeniu człowieka*, 1935 | wrzesinska |
| E.B. Tylor, *Anthropology*; R.R. Marett, *Anthropology* | *Antropologja*, 1889 (repr. Cieszyn 1997); *Antropologia*, tr. L. Krzywicki, 1913 | kubica |
| J. Huxley, A.C. Haddon, *We Europeans* | *My Europejczycy. Przegląd zagadnień „rasowych”*, 1937 | kubica |
| C. Lévi-Strauss, *Race et histoire* | „Rasa a historia”, in *Rasa a nauka. Trzy studia*, 1961 | kubica |
| B. Malinowski, "Anthropology" (EB) | in *Dzieła*, t. 8, 2000 | kubica |

No Polish edition was named in the corpus for: Balibar–Wallerstein, *Race, Nation, Class* (Ryś quotes it in English,
a hint, not proof); Fredrickson, *Racism*; Miles, *Racism*; Reisigl–Wodak; Omi–Winant. Check BN when a text needs one.

## F. Doubts found (flagged, not corrected; what I would do)

- **F1** taradejna file: a machine conversion of the PDF (it ends with the converting tool's note). The termbase quotes are verified against this copy; check the PDF before anything goes to print. The same applies to all the corpus files, which are MB's conversions; kubica is my pandoc conversion of MB's DOCX.
- **F2** taradejna: misspelt US figures: „Santo” (surely *Sambo*), „Jezebelle” (*Jezebel*), „Welfare Mother” (usually *welfare queen*). Would use the standard names.
- **F3** taradejna: name slips: „Lewotina” beside „Lewontin”; „Enzo Travesero” vs Traverso; „Michele'a Foucaulta”; „zniweolonych”, „biologi”, „perfomatywną”, „ów urasowienie”.
- **F4** taradejna: "*American Association of Anthropologists*" 1997. As far as I know (WK), the 1997 statement on the US race categories came from the American Anthropological Association.
- **F5** taradejna: two subtitles for Wielgosz: note 1 „Jak kapitalizm wynalazł Innych…” vs the bibliography (and nowak n. 5, rys n. 26) „Jak kapitalizm dzieli, by rządzić”. The second is right, three to one.
- **F6** taradejna: „Ashenburg 2009” is cited but missing from the bibliography; „Tomala 2023” is listed but not cited; Foucault's *Porządek dyskursu* is dated 1970 with a Polish publisher.
- **F7** taradejna: Cartwright's *drapetomania* is given only as „uciekinierstwo”.
- **F8** taradejna: „samooznaczanie” as Goffman's term: not traceable to *Stigma*; check the Polish edition.
- **F9** czerń: taradejna (< Koziołek, a Newsweek piece) gives *czerniec* 'monk'; WSJP gives *czarny*. Would follow WSJP.
- **F10** Murzyn: pl.wikipedia „Maurowie” = Brückner (German *Mohr*); „Murzyn” = Boryś (Old Czech *muřín*); Bańkowski dissents. Would cite Boryś, never Wikipedia.
- **F11** nowak: *Drang nach Osten* first in Klaczko 1849: her claim, not checked.
- **F12** nowak: n. 28 „Demokrata Polska” (elsewhere „Polski”); n. 25 title vs text („historii statystyki” / „historii i statystyki”); Mochnacki quotation „jakącą się” garbled.
- **F13** nowak n. 17: Górny in „Kwartalnik Historyczny” 2011 as „t. 68”; the 2011 volume should be around 118 (WK).
- **F14** taradejna cites Ryś 2019 as „Podziały **rasowe** a kategoria rasy…”; Ryś himself cites his own article as „Podziały **społeczne** a kategoria rasy…” [rys n. 24]. Ryś's form is almost certainly right.
- **F15** taradejna: „Kubica-Heller G. (2015) … s. 94–117”. The chapter in MB's copy is signed „Grażyna Kubica”, and its running heads show pp. 89–109; the conclusions taradejna quotes are on p. 107 there. The page range needs checking against the book; cite the name as printed in it.
- **F16** taradejna quotes Kubica's conclusion (2) as „nie potrafiono ujmować”; the chapter reads „nie potrafi ono ujmować”. Quote from the book.
- **F17** malczynski n. 55: Kuzio 2002 in „Racial and Ethnic Studies”; the journal is *Ethnic and Racial Studies* (WK).
- **F18** nowak2021 bibliography: „Nowe książki o Ameryce. (1864). *Biblioteka Warszawska*, 1964(4)”: 1964 for 1864.
- **F19** Tool error, not a source doubt: the web-page summariser gave Ryś's source as "Bernard Isaac"; the page has „B. Isaac” (WK: Benjamin Isaac, *Proto-racism in Graeco-Roman Antiquity*). Quotes in this register come only from saved texts, never from summaries.
- **F20** Own error, corrected 28.09.2026: the first version of this register said „Murzyn” translates no EN term we use. MB's D11 (4) maps period *Blackamoor* / *negro* to „Murzyn” (§ B2).

## G. Works to source (list of 28.09.2026; MB closed it the same day: "skip the rest")

| # | Work | Status |
|---|---|---|
| G1 | Nowak 2021, „Rasa czyli plemię” (SFPS 56) | received → nowak2021 |
| G2 | Wrzesińska 2021, Termin rasa i jego synonimy (SFPS 56) | received → wrzesinska |
| G3 | Małczyński 2014, „Rasa” a nacjonalizm | received → malczynski (+ the editorial, malczynski_mincer) |
| G4 | Ryś 2023, Rasizm klasowy i terminy pokrewne | received (MB's link) → rys |
| G5 | Górny 2011, „Pięć wielkich armii…” | dropped (MB) |
| G6 | Wolniewicz 2013, „Żeby Moskwa była Moskwą” | received → wolniewicz |
| G7 | Ryś 2019, „Obaczymy, czy masz dobrą krew w sobie” | dropped (MB) |
| G8 | Wrzesińska 2015, Ariowie i Turańczycy | dropped (MB) |
| G9 | Kubica 2015, Antropologiczny dyskurs rasowy | received → kubica |
| G10 | Twardowski 2014 | dropped (MB) |
| G11 | Strzałko 2009 | dropped (MB) |
| G12 | Kendziorek 2011 | dropped (MB) |
| G13 | Koziołek 2016, Czerń i literatura | dropped (MB) |
| G14 | Wielgosz 2021, *Gra w rasy* | dropped (MB) |
| G15 | Tazbir 2004, *Polska przedmurzem Europy* | dropped (MB) |
| G16 | Górny 2014, *Wielka Wojna profesorów* | dropped (MB) |
| G17 | Pobłocki, Rauszer, Leszczyński | dropped (MB) |
| G18 | Mróz 2001, *Dzieje Cyganów-Romów…* | open only if Pahulich's quotations need it (T18) |
