# refs.json for Pahulich, "Racialization of Roma, European Modernity, and the Entanglement of Empires"
# (Critical Romani Studies 8/1, 2025) — typed from pahulich_pdf_bib.txt (the author's list), nothing added.
# Kept as the author gives it, errors included (flagged in pahulich_queries.md, MB decides).
# Changed only where the Kanon prescribes the form: Cyrillic in the apparatus -> ALA-LC without ligatures
# (§ 9.6; checked against catalogues, sources in pahulich_queries.md), places of Cyrillic imprints in ALA-LC
# (§ 9.2), "Tom VI" -> volume 6 (§ 11), title glosses in [ ] in Polish (§ 4.3, `original-title`). The author's form
# of every changed field is kept in `srom-as-written`.
import json
def P(family, given=None, **kw):
    d = {"family": family}
    if given: d["given"] = given
    d.update(kw); return d
def Y(*a): return {"date-parts": [list(a)]}
def book(id, au, title, place, pub, year, **kw):
    d = {"id": id, "type": "book", "author": au, "title": title, "publisher-place": place, "publisher": pub, "issued": Y(year)}
    if place is None: del d["publisher-place"]
    if pub is None: del d["publisher"]
    d.update(kw); return d
def art(id, au, title, cont, vol, iss, page, year, **kw):
    d = {"id": id, "type": "article-journal", "author": au, "title": title, "container-title": cont, "issued": Y(year)}
    if vol: d["volume"] = vol
    if iss: d["issue"] = iss
    if page: d["page"] = page
    d.update(kw); return d
def chap(id, au, title, cont, eds, page, place, pub, year, **kw):
    d = {"id": id, "type": "chapter", "author": au, "title": title, "container-title": cont, "editor": eds, "page": page,
         "publisher-place": place, "publisher": pub, "issued": Y(year)}
    d.update(kw); return d

R = [
 book("achim2004", [P("Achim", "Viorel")], "The Roma in Romanian History", "Budapest", "CEU Press", 2004),
 book("acton1974", [P("Acton", "Thomas")], "Gypsy Politics and Social Change: The Development of Ethnic Ideology and Pressure Politics among British Gypsies from Victorian Reformism to Romany Nationalism",
      "London; Boston", "Routledge and Kegan Paul", 1974, **{"srom-as-written": {"publisher-place": "London and Boston"}}),
 book("baker2018", [P("Baker", "Catherine")], "Race and the Yugoslav Region: Postsocialist, Post-conflict, Postcolonial?", "Manchester", "Manchester University Press", 2018,
      DOI="10.7765/9781526126610"),
 book("barannikov1931", [P("Barannikov", "Alekseĭ")], "Tsygany SSSR", "Moskva", "Tsentrizdat", 1931,
      **{"original-title": "Cyganie ZSRR", "srom-as-written": {"given": "Alexey", "publisher-place": "Moscow", "original-title": "Gypsies of USSR"}}),
 {"id": "bielikov2003", "type": "thesis", "author": [P("Bielikov", "Oleksandr")], "title": "Tsyhansʹke naselennia Ukraïny (16–20 st.)",
  "original-title": "Ludność cygańska Ukrainy (XVI–XX w.)", "publisher": "Donetsk National University", "issued": Y(2003), "note": "praca doktorska",
  "srom-as-written": {"author": "Byelikov", "title": "Tsyhansʹke Naselennya Ukrayiny (16–20 st.)",
                      "original-title": "Gypsy population of Ukraine (16th–20th centuries)", "note": "PhD dissertation"}},
 chap("bielikov2008", [P("Bielikov", "Oleksandr")], "Derzhavna polityka stosovno tsyhan Ukraïny: istoriia i suchasnistʹ",
      "Naukovi zapysky. Zbirnyk pratsʹ molodykh vchenykh ta aspirantiv", [P("Sokhanʹ", "P.S.")], "24–56", "Kyïv", "NAN Ukraïny", 2008,
      volume="15", **{"original-title": "Polityka państwa wobec Cyganów Ukrainy: historia i współczesność",
                      "srom-as-written": {"author": "Byelikov", "title": "Derzhavna Polityka stosovno Tsyhan Ukrayiny: Istoriya i Suchasnistʹ",
                                          "original-title": "State politics towards Gypsies in Ukraine: History and modern",
                                          "container-title": "Naukovi zapysky. Zbirnyk prats’ molodykh vchenykh ta aspirantiv, t. 15",
                                          "editor": "Sokhan’", "editors": "P. S. Sokhan’, et al.", "publisher-place": "Kyiv", "publisher": "NAN Ukrayiny"}}),
 art("chervinski2008", [P("Chėrvinski", "Iaŭheniĭ")], "Tatary i tsyhany na tėrytoryi Vialikaha Kniastva Litoŭskaha: pravavy i satsyialʹny status",
     "Zhurnal mezhdunarodnogo prava i mezhdunarodnykh otnosheniĭ", None, "3", "70–72", 2008,
     **{"original-title": "Tatarzy i Cyganie na terytorium Wielkiego Księstwa Litewskiego: status prawny i społeczny",
        "srom-as-written": {"author": "Červinski", "given": "Jaŭhienij", "title": "Tatary i Cyhany na Terytoryi Vialikaha Kniastva Litoŭskaha: Pravavy i Sacyjaĺny Status",
                            "original-title": "Tatars and Gypsies in the Grand Duchy of Lithuania/Litva",
                            "container-title": "Žurnal mieždunarodnoho prava i mieždunarodnych otnošjenij"}}),
 book("cesaire2000", [P("Césaire", "Aimé")], "Discourse on Colonialism", "New York", "Monthly Review Press", 2000,
      editor=[P("Kelley", "Robin D.G.")], DOI="10.4324/9781003101406-19"),
 chap("clark2004", [P("Clark", "Colin")], "‘Severity Has Often Enraged but Never Subdued a Gipsy’: The History and Making of European Romani Stereotypes",
      "The Role of the Romanies Images and Counter Images of ‘Gypsies’ / Romanies in European cultures", [P("Saul", "Nicholas"), P("Tebbutt", "Susan")],
      "226–246", "Liverpool", "Liverpool University Press", 2004, DOI="10.5949/liverpool/9780853236795.003.0015"),
 book("crowe2007", [P("Crowe", "David")], "A History of the Gypsies of Eastern Europe and Russia", "New York", "Palgrave Macmillan", 2007,
      DOI="10.1007/978-1-137-10596-7"),
 book("dal1883", [P("Dalʹ", "Vladimir")], "Sochineniia V.I. Dalia: Povesti i rasskazy", "S.-Peterburg", "Izd. knigoprodavtsa-tip. M.O. Volʹfa", 1883,
      volume="6", **{"original-title": "Dzieła W.I. Dala: powieści i opowiadania", "srom-as-written": {"author": "Dal’", "title": "Sochineniya V.I. Dalya: Povesti i Rasskazy",
                                                                            "original-title": "Works of V.I. Dal’", "volume": "Tom VI",
                                                                            "publisher": "Izd. knigoprodavtsa-tip. M.O. Vol’fa"}}),
 book("demeter2000", [P("Demeter", "Nadezhda"), P("Bessonov", "Nikolaĭ"), P("Kutenkov", "Vladimir")], "Istoriia tsygan: novyĭ vzgliad",
      "Voronezh", "IPF Voronezh", 2000, **{"original-title": "Historia Cyganów: nowe spojrzenie",
                                            "srom-as-written": {"given": "Nikolay", "title": "Istoriya Tsygan: Novyy Vzglyad", "original-title": "History of Gypsies"}}),
 book("federici2004", [P("Federici", "Silvia")], "Caliban and the Witch", "Brooklyn, NY", "Autonomedia", 2004),
 chap("fernandez2021", [P("Fernández", "Cayetano")], "The Roma Collective Memory and the Epistemological Limits of Western Historiography",
      "The Pluriverse of Human Rights: The Diversity of Struggles for Dignity", [P("Santos", "Boaventura de Sousa"), P("Martins", "Bruno Sena")],
      "205–217", "London", "Routledge", 2021, DOI="10.4324/9781003177722-13"),
 book("fraser1992", [P("Fraser", "Angus M.")], "The Gypsies", "Oxford", "Blackwell", 1992),
 art("gheorghe1991", [P("Gheorghe", "Nicolae")], "Roma-Gypsy Ethnicity in Eastern Europe. (Nationalism in Central and Eastern Europe)", "Social Research",
     "58", "4", "829–844", 1991),
 book("grellmann1807", [P("Grellmann", "Heinrich Moritz Gottlieb")],
      "Dissertation on the Gipseys: Representing their Manner of Life, Family Economy, Occupations & Trades, Marriages & Education, Sickness, Death and Burial, Religion, Language, Sciences & Arts, &c. &c. &c.: with an Historical Enquiry Concerning their Origin & First Appearance in Europe",
      "London", "Printed by W. Ballintine", 1807, translator=[P("Raper", "Matthew")]),
 book("hancock1987", [P("Hancock", "Ian")], "The Pariah Syndrome: An Account of Gypsy Slavery and Persecution", "Ann Arbor", "Karoma", 1987),
 chap("hancock2008", [P("Hancock", "Ian")], "The ‘Gypsy’ Stereotype and the Sexualization of Romani Women", "“Gypsies” in European Literature and Culture",
      [P("Glajar", "Valentina"), P("Radulescu", "Domnica")], "181–191", "New York", "Palgrave Macmillan", 2008, DOI="10.1057/9780230611634_10"),
 chap("holler2015", [P("Holler", "Martin")], "Historical Predecessors of the Term ‘Anti-Gypsyism", "Antiziganism: What’s in a Word?",
      [P("End", "Markus"), P("Kiuchukov", "Khristo"), P("Laskar", "Pia"), P("Templer", "Bill"), P("Selling", "Jan")], "82–92",
      "Newcastle upon Tyne", "Cambridge Scholars Publishing", 2015),
 book("horvathova1964", [P("Horváthová", "Emilia")], "Cigáni Na Slovensku: Historiko-Etnograficky Náčrt", "Bratislava", "Vytadel’stvo Siovenskej Akademie Vied", 1964,
      **{"original-title": "Cyganie na Słowacji: szkic historyczno-etnograficzny", "srom-as-written": {"original-title": "Gypsies in Slovakia"}}),
 chap("kirei1984", [P("Kireĭ", "N.I."), P("Serdiuk", "A.O.")], "Izuchenie tsygan evropeĭskoĭ chasti Rossii i Kavkaza v dorevoliutsionnoĭ otechestvennoĭ ėtnografii",
      "Arkheologo-ėtnograficheskie issledovaniia Severnogo Kavkaza. Sbornik nauchnykh trudov", [P("Kireĭ", "N.I.")], "107–131", "Krasnodar",
      "Kubanskiĭ gosudarstvennyĭ universitet", 1984,
      **{"original-title": "Badania nad Cyganami europejskiej części Rosji i Kaukazu w przedrewolucyjnej etnografii rodzimej",
         "srom-as-written": {"author": "Kirey; Serdyuk",
                             "title": "Izucheniye Tsygan Yevropeyskoy Chasti Rossii i Kavkaza v Dorevolyutsionnoy Otechestvennoy Etnografii",
                             "original-title": "Study of Gypsies of the European part of Russia and the Caucasus in pre-revolutionary domestic ethnography",
                             "container-title": "Arkheologo-etnograficheskiye issledovaniya Severnogo Kavkaza. Sbornik nauchnykh trudov",
                             "editor": "Kirey", "editors": "N. I. Kirey et al.", "publisher": "Kubanskiy gosudarstvenniy universitet"}}),
 {"id": "kistiakovskii1879", "type": "book", "editor": [P("Kistiakovskiĭ", "Aleksandr")], "title": "Prava, po kotorym suditsia malorossīĭskīĭ narod",
  "original-title": "Prawa, według których sądzony jest lud małoruski", "publisher-place": "Kiev", "publisher": "Univ. tip.", "issued": Y(1879),
  "srom-as-written": {"editor": "Kistyakovskiy", "title": "Prava, po kotorym Suditsya Malorossiyskiy Narod",
                      "original-title": "Rights by which the Malorossian people are judged"}},
 chap("kocze2020", [P("Kóczé", "Angéla")], "Gendered and Racialized Social Insecurity of Roma in East Central Europe",
      "The Roma and their Struggle for Identity in Contemporary Europe", [P("Baar", "Huub", **{"non-dropping-particle": "van"}), P("Kócze", "Angéla")],
      "124–149", "New York", "Berghahn Books", 2020, DOI="10.1515/9781789206432-009"),
 book("law2012", [P("Law", "Ian")], "Red Racisms: Racism in Communist and Post-communist Contexts", "London", "Palgrave Macmillan", 2012,
      DOI="10.1057/9781137030849"),
 book("law2018", [P("Law", "Ian"), P("Kovats", "Martin")], "Rethinking Roma: Identities, Politicisation and New Agendas", "London", "Palgrave Macmillan", 2018,
      DOI="10.1057/978-1-137-38582-6"),
 chap("law2019", [P("Law", "Ian"), P("Zakharov", "Nikolay")], "Race and Racism in Eastern Europe: Becoming White, Becoming Western",
      "Relating Worlds of Racism: Dehumanisation, Belonging, and the Normativity of European Whiteness",
      [P("Essed", "Philomena"), P("Farquharson", "Karen"), P("Pillay", "Kathryn"), P("White", "Elisa Joy")], "113–139", "London", "Palgrave Macmillan", 2019,
      DOI="10.1007/978-3-319-78990-3_5"),
 book("lewy2000", [P("Lewy", "Guenter")], "The Nazi Persecution of the Gypsies", "Oxford", "Oxford University Press", 2000,
      DOI="10.1093/oso/9780195125566.001.0001"),
 chap("lucassen1998", [P("Lucassen", "Leo")], "Eternal Vagrants? State Formation, Migration and Travelling Groups in Western Europe, 1350–1914",
      "Gypsies and Other Itinerant Groups: A Socio-Historical Approach", [P("Lucassen", "Leo"), P("Willems", "Wim"), P("Cottaar", "Annemarie")],
      "55–73", "New York", "St. Martin’s Press", 1998, DOI="10.1007/978-1-349-26341-7_4"),
 art("lucassen2008", [P("Lucassen", "Leo")], "Between Hobbes and Locke. Gypsies and the Limits of the Modernization Paradigm", "Social History",
     "33", "4", "423–441", 2008, DOI="10.1080/03071020802410411"),
 {"id": "marsh2008", "type": "thesis", "author": [P("Marsh", "Adrian")], "title": "No Promised Land: History, Historiography and the Origins of the Gypsies",
  "publisher": "University of Greenwich", "issued": Y(2008), "note": "praca doktorska", "srom-as-written": {"note": "PhD diss."}},
 {"id": "matache2016", "type": "webpage", "author": [P("Matache", "Margareta")], "title": "Word, Image and Thought: Creating the Romani Other",
  "container-title": "François-Xavier Bagnoud Center for Health and Human Rights at Harvard University", "issued": Y(2016, 10, 5),
  "URL": "https://fxb.harvard.edu/2016/10/05/word-image-and-thought-creating-the-romani-other"},
 {"id": "matache2020", "type": "article-newspaper", "author": [P("Matache", "Margareta")],
  "title": "It Is Time Reparations Are Paid for Roma Slavery: Romanians Continue to Actively Deny the History of Roma Enslavement in Romanian Lands",
  "container-title": "Al Jazeera", "issued": Y(2020, 10, 5),
  "URL": "https://www.aljazeera.com/opinions/2020/10/5/it-is-time-reparations-are-paid-for-roma-slavery/?fbclid=IwAR16IM_B7KGwlxHwAF1nIsNIMuUPdgRukdw2jOMhZ-lT6jid71DrOji-bWQ"},
 art("melamed2015", [P("Melamed", "Jodi")], "Racial Capitalism", "Critical Ethnic Studies", "1", "1", "76–85", 2015, DOI="10.5749/jcritethnstud.1.1.0076"),
 book("mroz2015", [P("Mróz", "Lech")], "Roma-Gypsy Presence in the Polish-Lithuanian Commonwealth (15th–18th Centuries)", "Budapest", "CEU Press", 2015,
      DOI="10.1515/9789633861097"),
 art("okeeffe2014", [P("O’Keeffe", "Brigid")], "Gypsies as a Litmus Test for Rational, Tolerant Rule: Fin-De-Siecle Russian Ethnographers Confront the Comparative History of Roma in Europe",
     "International Journal of Comparative and Applied Criminal Justice", "38", "2", "109–131", 2014, DOI="10.1080/01924036.2013.804638"),
 book("parvulescu2022", [P("Parvulescu", "Anca"), P("Boatcă", "Manuela")], "Creolizing the Modern: Transylvania across Empires", "Ithaca", "Cornell University Press", 2022),
 book("robinson2000", [P("Robinson", "Cedric J.")], "Black Marxism: The Making of the Black Radical Tradition", "Chapel Hill", "UNC Press", 2000),
 book("said1978", [P("Said", "Edward W.")], "Orientalism", "New York", "Pantheon Books", 1978),
 chap("shahar2007", [P("Shahar", "Shulamith")], "Religious Minorities, Vagabonds and Gypsies in Early Modern Europe",
      "Roma: A Minority in Europe: Historical, Political and Social Perspectives", [P("Stauber", "Roni"), P("Vago", "Raphael")], "1–18", "Budapest", "CEU Press", 2007),
 art("shaidurov2018", [P("Shaidurov", "Vladimir")], "Gypsies in the Russian Empire: Theories and Practices Addressing Their Situation during the Eighteenth and First Half of the Nineteenth Century",
     "Romani Studies", "28", "2", "195–217", 2018, DOI="10.3828/rs.2018.8"),
 book("shmidt2020", [P("Shmidt", "Victoria"), P("Jaworsky", "Bernadette Nadya")], "Historicizing Roma in Central Europe: Between Critical Whiteness and Epistemic Injustice",
      "London", "Routledge", 2020, DOI="10.4324/9781003034094"),
 book("shohat2012", [P("Shohat", "Ella"), P("Stam", "Robert")], "Race in Translation: Culture Wars around the Postcolonial Atlantic", "New York", "NYU Press", 2012,
      DOI="10.18574/nyu/9780814798379.001.0001"),
 art("smirnovaseslavinskaya2021", [P("Smirnova-Seslavinskaya", "Marianna")], "Service Nomadism of the Roma / Gypsies in the Russian Empire: A Social Norm and the Letter of the Law",
     "Ab Imperio", None, "1", "51–92", 2021, DOI="10.1353/imp.2021.0003"),
 chap("taba2021", [P("Taba", "Marius")], "Antigypsyism in a Time of Neoliberalism: Challenging the Radical Right Through Transformative Change",
      "Romani Communities and Transformative Change: A New Social Europe", [P("Ryder", "Andrew"), P("Taba", "Marius"), P("Trehan", "Nidhi")], "65–92",
      "Bristol", "Policy Press", 2021),
 book("thomas2018", [P("Thomas", "Alun")], "Nomads and Soviet Rule: Central Asia Under Lenin and Stalin", "New York", "I.B. Tauris", 2018, DOI="10.5040/9781350987364"),
 art("vincze2015", [P("Vincze", "Enikő")], "Adverse Incorporation of the Roma and the Formation of Capitalism in Romania", "Intersections", "1", "4", "14–37", 2015,
     DOI="10.17356/ieejsp.v1i4.88"),
 book("willems1997", [P("Willems", "Wim")], "In Search of the True Gypsy: From Enlightenment to Final Solution", "London", "F. Cass", 1997,
      translator=[P("Bloch", "Don")], DOI="10.4324/9781315810225"),
 book("wippermann1997", [P("Wippermann", "Wolfgang")], "Wie Die Zigeuner: Antisemitismus Und Antiziganismus Im Vergleich", "Berlin", "Elefanten Press", 1997),
 art("wynter2003", [P("Wynter", "Sylvia")], "Unsettling the Coloniality of Being/Power/Truth/Freedom: Towards the Human, After Man, Its Overrepresentation – An Argument",
     "The New Centennial Review", "3", "3", "257–337", 2003, DOI="10.1353/ncr.2004.0015"),
 book("zelenchuk1979", [P("Zelenchuk", "Valentin")], "Naselenie Bessarabii i Podnestrovʹia v XIX v.", "Kishinev", "Shtiintsa", 1979,
      **{"original-title": "Ludność Besarabii i Naddniestrza w XIX w.",
         "srom-as-written": {"title": "Naseleniye Bessarabii i Podnestrov’ya v XIX v", "original-title": "Population of Bessarabia and Subnistria in the nineteenth century"}}),
 art("zinevych2001", [P("Zinevych", "Nataliia")], "Tsyhany v Ukraïni: formuvannia etnosu i suchasnyĭ stan", "Ukraïnsʹkyĭ istorychnyĭ zhurnal", None, "1", "40–52", 2001,
     **{"original-title": "Cyganie na Ukrainie: kształtowanie się etnosu i stan obecny", "srom-as-written": {"given": "Nataliya", "title": "Tsyhany v Ukrayini: Formuvannya Etnosu i Suchasnyy Stan",
                                                                    "original-title": "Gypsies in Ukraine", "container-title": "Ukrayins’kyy istorychnyy zhurnal"}}),
]
assert len(R) == 52 and len({r["id"] for r in R}) == 52, (len(R), len({r["id"] for r in R}))
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("refs.json", len(R))
