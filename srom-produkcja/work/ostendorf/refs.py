# refs.json for Ostendorf, "Familiar Outsiders Abroad: Relational Racialization in the Romani Atlantic World", in
# M. Fotta, A. Ostendorf (eds.), The Romani Atlantic (Cambridge University Press 2026), 86–108, ch. 3.
# The source has no bibliography: every work is typed from its first full citation in the notes (note numbers below
# are the printed ones). Chicago notes as CUP sets them: publisher without place for modern books, place without
# publisher for old ones. Nothing added: missing places print [BRAK MIEJSCA], missing publishers after 1800
# [BRAK WYDAWCY] (queries A2); early prints (to 1800) need no publisher (Kanon § 0). DOIs checked against Crossref
# (doi_check.txt); the author's data are kept where Crossref differs, the differences are queries (B). Abbreviated
# ranges set in full (Kanon § 3.2). Short titles: the author's where she uses one, else the main title (Kanon § 7.3).
import json
def P(family, given=None, **kw):
    d = {"family": family}
    if given: d["given"] = given
    d.update(kw); return d
def L(name): return {"literal": name}
def Y(*a): return {"date-parts": [list(a)]}
def book(id, au, title, pub, place, year, **kw):
    d = {"id": id, "type": "book", "title": title, "issued": Y(year)}
    if au: d["author"] = au
    if pub: d["publisher"] = pub
    if place: d["publisher-place"] = place
    d.update(kw); return d
def chap(id, au, title, cont, eds, pub, place, year, page=None, **kw):
    d = {"id": id, "type": "chapter", "title": title, "container-title": cont, "issued": Y(year)}
    if au: d["author"] = au
    if eds: d["editor"] = eds
    if pub: d["publisher"] = pub
    if place: d["publisher-place"] = place
    if page: d["page"] = page
    d.update(kw); return d
def art(id, au, title, cont, vol, issue, year, page=None, doi=None, **kw):
    d = {"id": id, "type": "article-journal", "title": title, "container-title": cont, "issued": Y(year)}
    if au: d["author"] = au
    if vol: d["volume"] = vol
    if issue: d["issue"] = issue
    if page: d["page"] = page
    if doi: d["DOI"] = doi
    d.update(kw); return d
def S(short): return {"title-short": short}

OST = [P("Ostendorf", "Ann")]
HER = [P("Herzog", "Tamar")]
UPP = "University of Pennsylvania Press"
WMQ = "The William and Mary Quarterly"
LOEWALD = [P("Loewald", "Klaus G."), P("Starika", "Beverly"), P("Taylor", "Paul S.")]
R = [
 # 1
 book("matache2026", [P("Matache", "Margareta")], "The Permanence of Anti-Roma Racism: (Un)uttered Sentences", "Routledge",
      None, 2026, **S("The Permanence of Anti-Roma Racism…"), **{"srom-as-written": {"title": "The Permanence of Anti-Roma "
      "Racism:(Un)uttered Sentences"}}),
 art("pahulich2025", [P("Pahulich", "Lesia")], "Racialization of Roma, European Modernity, and the Entanglement of Empires",
     "Critical Romani Studies", "8", "1", 2025, "40–61", "10.29098/crs.v8i1.208", **S("Racialization of Roma…")),
 {"id": "savic2022", "type": "speech", "author": [P("Savić", "Jelena")], "title": "Gadjo Supremacy and Gadjo Privileges",
  "publisher": "Critical Approaches to Romani Studies Conference, Södertörn University", "issued": Y(2022),
  "note": "referat konferencyjny", "srom-as-written": {"note": "Conference Paper presented at"}},
 {"id": "mirgatas2023", "type": "article-newspaper", "author": [P("Mirga-Tas", "Małgorzata"), P("Matache", "Margareta")],
  "title": "Gadjoness: An Uncounted Shade of Whiteness", "container-title": "The Funambulist", "issued": Y(2023, 6, 22),
  **S("Gadjoness…")},
 art("ndiaye2022", [P("Ndiaye", "Noémie")], "Black Roma: Afro-Romani Connections in Early Modern Drama (and Beyond)",
     "Renaissance Quarterly", "75", "4", 2022, "1266–1302", "10.1017/rqx.2022.332", **S("Black Roma…")),
 # 2
 book("bogdal2023", [P("Bogdal", "Klaus-Michael")], "Europe and the Roma: A History of Fascination and Fear", "Penguin",
      None, 2023, translator=[P("Chase", "Jefferson")], **S("Europe and the Roma…")),
 # 3
 book("ndiaye2022b", [P("Ndiaye", "Noémie")], "Scripts of Blackness: Early Modern Performance Culture and the Making of Race",
      UPP, None, 2022, **S("Scripts of Blackness…")),
 art("molina2010", [P("Molina", "Natalia")], "The Power of Racial Scripts: What the History of Mexican Immigration to the "
     "United States Teaches Us about Relational Notions of Race", "Latino Studies", "8", "2", 2010, "156–175",
     "10.1057/lst.2010.20", **S("The Power of Racial Scripts…")),
 book("molina2019", None, "Relational Formations of Race: Theory, Method, and Practice", "University of California Press",
      None, 2019, editor=[P("Molina", "Natalia"), P("HoSang", "Daniel Martinez"), P("Gutiérrez", "Ramón A.")],
      **S("Relational Formations of Race…")),
 art("tabili2003", [P("Tabili", "Laura")], "Race Is a Relationship, and Not a Thing", "Journal of Social History", "37", "1",
     2003, "125–130", "10.1353/jsh.2003.0162"),
 # 4
 art("galletti2021", [P("Galletti", "Patricia")], "Los Gitanos como Otro y como Horizonte de Otredad en la Hispanoaméria "
     "Colonial (S. XV a XIX)", "International Journal of Roma Studies", "3", "2", 2021, None, "10.17583/ijrs.8527",
     **S("Los Gitanos como Otro…")),
 # 5
 art("herzog2018", HER, "Indigenous Reducciones and Spanish Resettlement: Placing Colonial and European History in Dialogue",
     "Ler História", "72", None, 2018, "9–30", "10.4000/lerhistoria.3146", **S("Indigenous Reducciones…")),
 chap("herzog2012", HER, "Beyond Race: Exclusion in Early Modern Spain and Spanish America", "Race and Blood in the Iberian "
      "World", [P("Hering Torres", "Max S."), P("Martínez", "María Elena"), P("Nirenberg", "David")], "LIT Verlag", None,
      2012, "151–167", **S("Beyond Race…")),
 book("cressy2018", [P("Cressy", "David")], "Gypsies: An English History", "Oxford University Press", None, 2018,
      **S("Gypsies…")),
 # 6
 art("wakeleysmith2023", [P("Wakeley-Smith", "Dalen")], "“The One Primitive People Who Contact with Civilization has Failed "
     "to Exterminate”: New York and “Gypsy” Madness in the 1920s", "Journal of American Ethnic History", "43", "1", 2023,
     "67–87", "10.5406/19364695.43.1.03", **S("“The One Primitive People…”")),
 book("matthews2018", [P("Matthews", "Jodie")], "The Gypsy Woman: Representations in Literature and Visual Culture",
      "Bloomsbury", None, 2018, **S("The Gypsy Woman…")),
 book("houghtonwalker2014", [P("Houghton-Walker", "Sarah")], "Representations of the Gypsy in the Romantic Period",
      "Oxford University Press", None, 2014, **S("Representations of the Gypsy…")),
 book("nord2006", [P("Nord", "Deborah Epstein")], "Gypsies and the British Imagination, 1807–1930", "Columbia University Press",
      None, 2006, **S("Gypsies and the British Imagination…")),
 book("charnondeutsch2004", [P("Charnon-Deutsch", "Lou")], "The Spanish Gypsy: The History of a European Obsession",
      "Pennsylvania State University Press", None, 2004, **S("The Spanish Gypsy…")),
 # 7
 book("flint2009", [P("Flint", "Kate")], "The Transatlantic Indian: 1776–1930", "Princeton University Press", None, 2009,
      **S("The Transatlantic Indian…")),
 book("smith2000", [P("Smith", "Sherry L.")], "Reimagining Indians: Native Americans through Anglo Eyes, 1880–1940",
      "Oxford University Press", None, 2000, **S("Reimagining Indians…")),
 book("deloria1998", [P("Deloria", "Philip J.")], "Playing Indian", "Yale University Press", None, 1998),
 # 8
 book("delafuente2020", [P("Fuente", "Alejandro", **{"dropping-particle": "de la"}), P("Gross", "Ariela J.")],
      "Becoming Free, Becoming Black: Race, Freedom, and Law in Cuba, Virginia, and Louisiana", "Cambridge University Press",
      None, 2020, **S("Becoming Free, Becoming Black…")),
 book("hogarth2017", [P("Hogarth", "Rana A.")], "Medicalizing Blackness: Making Racial Difference in the Atlantic World, "
      "1780–1840", "University of North Carolina Press", None, 2017, **S("Medicalizing Blackness…")),
 book("kendi2016", [P("Kendi", "Ibram X.")], "Stamped from the Beginning: The Definitive History of Racist Ideas in America",
      "Nation", None, 2016, **S("Stamped from the Beginning…")),
 # 10
 art("trumpener1992", [P("Trumpener", "Katie")], "The Time of the Gypsies: A “People without History” in the Narratives of "
     "the West", "Critical Inquiry", "18", "4", 1992, "843–884", "10.1086/448659", **S("The Time of the Gypsies…")),
 # 11
 book("weinstein1960", [P("Weinstein", "Donald")], "Ambassador from Venice: Pietro Pasqualigo in Lisbon, 1501",
      "University of Minnesota Press", None, 1960, **S("Ambassador from Venice…")),
 book("memoircabot1831", None, "A Memoir of Sebastian Cabot; with a Review of the History of Maritime Discovery", None,
      "Philadelphia", 1831, **S("A Memoir of Sebastian Cabot…")),
 book("columbus1893", None, "The Journal of Christopher Columbus", None, "London", 1893,
      translator=[P("Markham", "Clements R.")]),
 art("soulis1961", [P("Soulis", "George C.")], "The Gypsies in the Byzantine Empire and the Balkans in the Late Middle Ages",
     "Dumbarton Oaks Papers", "15", None, 1961, **S("The Gypsies in the Byzantine Empire…")),
 {"id": "mangas2024", "type": "thesis", "author": [P("Mangas", "Francisco")], "title": "A Outra Minoria: Uma história dos "
  "Ciganos portugueses durante a Época Moderna", "publisher": "University of Porto", "issued": Y(2024),
  "note": "praca doktorska", "title-short": "A Outra Minoria…", "srom-as-written": {"note": "PhD diss."}},
 # 12
 book("beretario1617", [P("Beretario", "Sebastiano")], "Iosephi Anchietae Societatis Iesv Sacerdotis in Brasilia Defvncti Vita",
      None, None, 1617, **S("Iosephi Anchietae…")),
 book("elvas1932", [L("A Gentleman of Elvas")], "The True Relation of the Hardships Suffered by Governor Hernando de Soto",
      "Florida State Historical Society", None, 1932, translator=[P("Robertson", "James")],
      editor=[P("Robertson", "James")], **S("The True Relation…")),
 # 13
 chap("martinezserna2009", [P("Martínez-Serna", "Gabriel")], "Procurators and the Making of the Jesuits’ Atlantic Network",
      "Soundings in Atlantic History: Latent Structures and Intellectual Currents, 1530–1830",
      [P("Bailyn", "Bernard"), P("Denault", "Patricia L.")], "Harvard University Press", None, 2009,
      **S("Procurators and the Making of the Jesuits’ Atlantic Network")),
 # 14
 book("schmidl1938", [P("Schmidl", "Ulrico")], "Derrotero y viaje a España y las Indias, 1534–1554",
      "Universidad Nacional de Litoral", None, 1938, translator=[P("Wernicke", "Edmundo")],
      **S("Derrotero y viaje a España y las Indias…")),
 # 15
 book("actas1915", None, "Actas da Camara da Villa de S. Paulo, 1640–1652", "Archivo Municipal", None, 1915, volume="5",
      **S("Actas da Camara da Villa de S. Paulo…")),
 book("monteiro2018", [P("Monteiro", "John M.")], "Blacks of the Land: Indian Slavery, Settler Society, and the Portuguese "
      "Colonial Enterprise in South America", "Cambridge University Press", None, 2018,
      translator=[P("Woodard", "James"), P("Weinstein", "Barbara")], editor=[P("Woodard", "James"), P("Weinstein", "Barbara")],
      **S("Blacks of the Land…")),
 art("fotta2019", [P("Fotta", "Martin")], "The Figure of the Gypsy (Cigano) as a Signpost for Crises of the Social "
     "Hierarchy (Bahia, 1590s–1900s)", "International Review of Social History", "65", "2", 2019, None,
     "10.1017/S0020859019000713", **S("The Figure of the Gypsy…")),
 # 16
 book("herzog2003", HER, "Defining Nations: Immigrants and Citizens in Early Modern Spain and Spanish America",
      "Yale University Press", None, 2003, **S("Defining Nations…")),
 # 17
 book("gomezalfaro1999", [P("Gómez Alfaro", "Antonio"), P("Lopes da Costa", "Elisa Maria"), P("Floate", "Sharon Sillers")],
      "Deportaciones de Gitanos", "Centre de recherches tsiganes", None, 1999),
 # 18
 book("gomezalfaro1993", [P("Gómez Alfaro", "Antonio")], "The Great Gypsy Round-Up: Spain, the General Imprisonment of "
      "Gypsies in 1749", "University of Hertfordshire Press", None, 1993, **S("The Great Gypsy Round-Up…")),
 # 19
 chap("oreilly2003", [P("O’Reilly", "William")], "Divide et impera: Race, Ethnicity, and Administration in Early "
      "18th-Century Habsburg Hungary", "Racial Discrimination and Ethnicity in European History",
      [P("Hálfdánarson", "Gudmundur"), P("Isaacs", "Anne Katherine")], "Edizioni Plus", None, 2003, "77–100",
      **S("Divide et impera…")),
 # 22
 book("pym2007", [P("Pym", "Richard")], "The Gypsies of Early Modern Spain", "Palgrave Macmillan", None, 2007),
 # 23
 book("paucke1959", [P("Paucke", "Florian")], "Zwettler Codex 420", "Wilhelm Braumuller University", None, 1959,
      editor=[P("Becker-Donner", "Etta")]),
 # 24
 book("radding1997", [P("Radding", "Cynthia")], "Wandering Peoples: Colonialism, Ethnic Spaces, and Ecological Frontiers in "
      "Northwestern Mexico, 1700–1850", "Duke University Press", None, 1997, **S("Wandering Peoples…")),
 # 25
 art("morenoalonso1983", [P("Moreno Alonso", "Manuel")], "De Cadiz a Veracruz en 1745",
     "Historiografía y bibliografía Americanistas", "27", None, 1983),
 art("scarano1996", [P("Scarano", "Francisco A.")], "The Jíbaro Masquerade and the Subaltern Politics of Creole Identity "
     "Formation in Puerto Rico, 1745–1823", "American Historical Review", "101", "5", 1996, None, "10.2307/2170177",
     **S("The Jíbaro Masquerade…")),
 # 26
 chap("poisson1900", None, "Lettre au P.re Paul du Poisson; aux Akensas, October 3, 1727", "The Jesuit Relations and Allied "
      "Documents", [P("Thwaites", "Reuben Gold")], None, "Cleveland", 1900, volume="67",
      **S("Lettre au P.re Paul du Poisson…")),
 # 27
 book("berquinduvallon1803", [P("Berquin-Duvallon", "Pierre-Louis")], "Vue de la colonie Espagnole du Mississipi, ou des "
      "provinces de Louisiane et Floride Occidentale, en l’année 1802", None, "Paris", 1803,
      **S("Vue de la colonie Espagnole du Mississipi…"), **{"srom-as-written": {"title": "Vue de la colonie Espagnole du "
      "Mississipi, ou des provinces de Louisiane et Floride Occidentale,en l’année 1802"}}),
 # 28
 art("ostendorf2021", OST, "Louisiana Bohémiens: Community, Race, and Empire", "Early American Studies: An Interdisciplinary "
     "Journal", "19", "4", 2021, None, "10.1353/eam.2021.0021", **S("Louisiana Bohémiens…")),
 art("ostendorf2019", OST, "Racializing American “Egyptians”: Shifting Legal Discourse, 1690s–1860s", "Critical Romani "
     "Studies", "2", "2", 2019, "42–59", "10.29098/crs.v2i2.50", **S("Racializing American “Egyptians”…")),
 # 30
 book("stoler2002", [P("Stoler", "Ann Laura")], "Carnal Knowledge: Race and the Intimate in Colonial Rule",
      "University of California Press", None, 2002, **S("Carnal Knowledge…")),
 # 31
 book("milfort1802", [P("Milfort", "Louis LeClerc")], "Mémoire; ou Coup-d’Oeil Rapide Sur mes Différens Voyages et mon séjour "
      "dans la nation Crëck", None, "Paris", 1802, **S("Mémoire…")),
 # 33
 art("ostendorf2020", OST, "“To Get Himself Out of Slavery”: Escape, Justice, and Honor in the Life of a Colonial French "
     "Louisiana Bohemian (Gypsy)", "Frühneuzeit-Info", "31", None, 2020, "140–156", **S("“To Get Himself Out of Slavery”…")),
 # 34
 book("relation1622", None, "A Relation or Journall of the beginning and proceedings of the English", "John Bellamie", None,
      1622, **S("A Relation or Journall…")),
 book("mourt1865", None, "Mourt’s Relation, or Journal of the Plantation at Plymouth, 1622", None, "Boston", 1865,
      editor=[P("Dexter", "Henry")], **S("Mourt’s Relation…")),
 # 35
 chap("penn1912", [P("Penn", "William")], "A Letter from William Penn, Proprietary and Governor of Pennsylvania in America, to "
      "the Committee of the Free Society of Traders, 1683", "Narratives of Early Pennsylvania, West New Jersey, and Delaware, "
      "1630–1707", [P("Myers", "Albert Cook")], None, "New York", 1912, **S("A Letter from William Penn…")),
 # 36
 {"id": "cunniffe2023", "type": "thesis", "author": [P("Cunniffe", "Dan")], "title": "Pretending and Performing Gypsy "
  "Identity in Early Modern England, c. 1607–1623", "publisher": "King’s College London", "issued": Y(2023),
  "note": "praca doktorska", "title-short": "Pretending and Performing Gypsy Identity…", "srom-as-written": {"note": "PhD diss."}},
 # 37
 art("stone1882", [P("Stone", "Frederick")], "A Vindication of William Penn", "The Pennsylvania Magazine of History and "
     "Biography", "6", "2", 1882),
 # 38
 book("loskiel1789", [P("Loskiel", "Georg Heinrich")], "Geschichte der Mission der Evangelischen Brüder unter den Indianern in "
      "Nordamerika", None, None, 1789, **S("Geschichte der Mission…")),
 book("loskiel1794", [P("Loskiel", "George Henry")], "History of the Mission of the United Brethren among the Indians in North "
      "America", None, "London", 1794, translator=[P("La Trobe", "Christian")], **S("History of the Mission…")),
 # 40
 book("jamaicalady1720", None, "The Jamaica Lady", None, "London", 1720, **{"srom-as-written": {"author": "Anonymous"}}),
 # 41
 art("loewald1957", None, "Johann Martin Bolzius Answers a Questionnaire on Carolina and Georgia, Part I", WMQ, "14", "2",
     1957, None, "10.2307/1922111", editor=LOEWALD, translator=LOEWALD, **S("Johann Martin Bolzius Answers a Questionnaire…, "
     "Part I")),
 art("loewald1958", None, "Johann Martin Bolzius Answers a Questionnaire on Carolina and Georgia, Part II", WMQ, "15", "2",
     1958, None, "10.2307/1919443", editor=LOEWALD, translator=LOEWALD, **S("Johann Martin Bolzius Answers a Questionnaire…, "
     "Part II")),
 book("urlsperger1751", None, "Der ausführlichen nachrichten von der königlich-gross-britannischen colonie saltzburgischer "
      "emigranten in America erster", None, "Halle", 1751, editor=[P("Urlsperger", "Samuel")],
      note="University of Pennsylvania Library Special Collections", **S("Der ausführlichen nachrichten…")),
 # 42
 book("muhlenberg1945", None, "The Journals of Henry Melchior Muhlenberg", "Muhlenberg Press", None, 1945,
      translator=[P("Tappert", "Theodore G."), P("Doberstein", "John W.")], **S("The Journals of Henry Melchior Muhlenberg")),
 # 43
 art("ostendorf2018", OST, "Contextualizing American Gypsies: Experiencing Criminality in the Colonial Chesapeake",
     "Maryland Historical Magazine", "113", None, 2018, "192–222", **S("Contextualizing American Gypsies…")),
 book("block2021", [P("Block", "Sharon")], "Colonial Complexions: Race and Bodies in Eighteenth Century America", UPP, None,
      2021, **S("Colonial Complexions…")),
 # 44
 book("webb1736", [P("Webb", "George")], "Office and Authority of a Justice of Peace", None, "Williamsburg", 1736,
      **S("Office and Authority of a Justice of Peace")),
 book("tucker1803", [P("Tucker", "St. George")], "Blackstone’s Commentaries: With Notes of Reference to the Constitution and "
      "Laws of the Federal Government of the United States and the Commonwealth of Virginia", None, "Philadelphia", 1803,
      **S("Blackstone’s Commentaries…")),
 # 45
 art("todd2009", [P("Todd", "Emily B.")], "Establishing Routes for Fiction in the United States: Walter Scott’s Novels and the "
     "Early Nineteenth-Century American Publishing Industry", "Book History", "12", None, 2009, None, "10.1353/bh.0.0016",
     **S("Establishing Routes for Fiction…")),
 # 46
 art("cayton2013", [P("Cayton", "Andrew")], "The Authority of the Imagination in an Age of Wonder", "Journal of the Early "
     "Republic", "33", "1", 2013, None, "10.1353/jer.2013.0009", **S("The Authority of the Imagination…")),
 # 47
 book("scott1815", [P("Scott", "Walter")], "Guy Mannering; Or, the Astrologer", None, "Edinburgh", 1815, **S("Guy Mannering…")),
 # 48
 book("hofland1830", [P("Hofland", "Barbara")], "The Stolen Boy, an Indian Tale", None, "New York", 1830,
      **S("The Stolen Boy…")),
 book("trumpener1997", [P("Trumpener", "Katie")], "Bardic Nationalism: The Romantic Novel and the British Empire",
      "Princeton University Press", None, 1997, **S("Bardic Nationalism…")),
 # 51
 book("clinton1849", None, "The Life and Writings of De Witt Clinton", None, "New York", 1849, editor=[P("Cambell", "William")],
      **S("The Life and Writings of De Witt Clinton")),
 # 55
 book("pratt1992", [P("Pratt", "Mary Louise")], "Imperial Eyes: Travel Writing and Transculturation", "Routledge", None, 1992,
      **S("Imperial Eyes…")),
 # 56
 book("morgan2004", [P("Morgan", "Jennifer L.")], "Laboring Women: Reproduction and Gender in New World Slavery", UPP, None,
      2004, **S("Laboring Women…")),
 # 57
 art("wollon1952", [P("Wollon", "Dorothy"), P("Kinard", "Margaret")], "Notes and Documents: Sir Augustus J. Foster and “the Wild "
     "Natives of the Woods”, 1805–1807", WMQ, "9", "2", 1952, None, "10.2307/1925349", **S("Sir Augustus J. Foster…"),
     **{"srom-as-written": {"title": "Notes and Documents: Sir Augustus J. Foster and ‘the Wild Natives of the Woods,’ "
     "1805–1807"}}),
 # 58
 book("lambert1813", [P("Lambert", "John")], "Travels through Canada, and the United States of North America, in the Years "
      "1806, 1807, & 1808", None, "London", 1813, **S("Travels through Canada…")),
 # 60
 book("vowell1831", [P("Vowell", "Richard Longeville")], "Campaigns and Cruises in Venezuela and New Granada", None, "London",
      1831, **S("Campaigns and Cruises…")),
 # 61
 book("vigne1833", [P("Vigne", "Godfrey")], "Six Months in America", None, "Philadelphia", 1833),
 # 62
 book("robinson2021", [P("Robinson", "Alistair")], "Vagrancy in the Victorian Age: Representing the Wandering Poor in "
      "Nineteenth-Century Literature and Culture", "Cambridge University Press", None, 2021, **S("Vagrancy in the Victorian Age…")),
]
# ---- sourced imprints (MB 28.09.2026, queries A2): LoC catalogue (SRU, MARC 264/260), evidence in imprints.tsv; a record
# counts only if title, year and (where given) publisher and place match. Place = the first city of the imprint; imprint
# formulas reduced to the name ("Printed for …", "Published by …", "De l'Imprimerie …"). Not taken: two editions possible
# (Beretario 1617: Cologne and Lyon; Gómez Alfaro 1993: three co-publishers), joint imprints (Scott 1815), catalogue
# records that are aggregates (Hofland 1830, Open Library) — listed for the translation stage.
SOURCED = {
 "ndiaye2022b": ("publisher-place", "Philadelphia", "LCCN 2022000555"),
 "molina2019": ("publisher-place", "Oakland", "LCCN 2018051806"),
 "herzog2012": ("publisher-place", "Zürich", "LCCN 2015300781 (Zürich ; Berlin : Lit)"),
 "cressy2018": ("publisher-place", "Oxford", "LCCN 2017952087"),
 "matthews2018": ("publisher-place", "London", "LCCN 2019275276 (London ; New York : I.B. Tauris — a Bloomsbury imprint)"),
 "houghtonwalker2014": ("publisher-place", "Oxford", "LCCN 2014939130"),
 "nord2006": ("publisher-place", "New York", "LCCN 2005034050"),
 "charnondeutsch2004": ("publisher-place", "University Park", "LCCN 2003010254"),
 "flint2009": ("publisher-place", "Princeton", "LCCN 2008030164"),
 "smith2000": ("publisher-place", "Oxford", "LCCN 99059096"),
 "deloria1998": ("publisher-place", "New Haven", "LCCN 97030936"),
 "delafuente2020": ("publisher-place", "Cambridge", "LCCN 2019018404"),
 "hogarth2017": ("publisher-place", "Chapel Hill", "LCCN 2017011938"),
 "kendi2016": ("publisher-place", "New York", "LCCN 2015033671"),
 "weinstein1960": ("publisher-place", "Minneapolis", "LCCN 60014289"),
 "elvas1932": ("publisher-place", "DeLand", "LCCN 33005239"),
 "martinezserna2009": ("publisher-place", "Cambridge, Mass.", "LCCN 2008053246 (the volume)"),
 "schmidl1938": ("publisher-place", "Santa Fe", "LCCN 40034323 (the record reads “Sante Fe”; publisher there: Instituto Social, Universidad Nacional del Litoral)"),
 "herzog2003": ("publisher-place", "New Haven", "LCCN 2002011548"),
 "oreilly2003": ("publisher-place", "Pisa", "LCCN 2004430927 (the volume; Pisa : PLUS, Università di Pisa)"),
 "pym2007": ("publisher-place", "Basingstoke", "LCCN 2006051019"),
 "paucke1959": ("publisher-place", "Wien", "LCCN 66083415 (Wien, W. Braumüller)"),
 "radding1997": ("publisher-place", "Durham", "LCCN 96035147"),
 "stoler2002": ("publisher-place", "Berkeley", "LCCN 2002005540"),
 "loskiel1789": ("publisher-place", "Barby", "LCCN 19002213"),
 "muhlenberg1945": ("publisher-place", "Philadelphia", "LCCN 42018316 (Philadelphia, Evangelical Lutheran Ministerium…, 1942–58)"),
 "block2021": ("publisher-place", "Philadelphia", "LCCN 2017046033 (the 2018 edition)"),
 "trumpener1997": ("publisher-place", "Princeton", "LCCN 96039166"),
 "pratt1992": ("publisher-place", "London", "LCCN 91021435"),
 "morgan2004": ("publisher-place", "Philadelphia", "LCCN 2003066597"),
 "robinson2021": ("publisher-place", "Cambridge", "LCCN 2021028584"),
 "memoircabot1831": ("publisher", "Carey and Lea", "LCCN 06036141 (Philadelphia : Carey and Lea)"),
 "columbus1893": ("publisher", "Hakluyt Society", "LCCN 02007950 (London : Printed for the Hakluyt Society)"),
 "poisson1900": ("publisher", "The Burrows Brothers Company", "vol. 67 title page (archive.org jesuitrelationsa67jesuuoft): Cleveland: The Burrows Brothers Company"),
 "berquinduvallon1803": ("publisher", "Imprimerie expéditive", "LCCN 01008750 (Paris : De l'Imprimerie expéditive)"),
 "milfort1802": ("publisher", "Imprimerie de Giguet et Michaud", "LCCN 06020497"),
 "mourt1865": ("publisher", "J.K. Wiggin", "LCCN 03008746 (Boston, J. K. Wiggin)"),
 "penn1912": ("publisher", "C. Scribner’s Sons", "LCCN 12004611 (the volume; New York, C. Scribner's Sons)"),
 "tucker1803": ("publisher", "William Young Birch and Abraham Small", "LCCN 12013568 (Philadelphia : Published by William Young Birch, and Abraham Small …)"),
 "clinton1849": ("publisher", "Baker and Scribner", "LCCN 07019566"),
 "lambert1813": ("publisher", "C. Cradock and W. Joy", "LCCN 02000843 (London, Printed for C. Cradock and W. Joy; Edinburgh, Doig and Stirling [etc.])"),
 "vowell1831": ("publisher", "Longman and Co.", "LCCN 01021439"),
 "vigne1833": ("publisher", "Thomas T. Ash", "LCCN 01028360 (Philadelphia, Published by Thomas T. Ash)"),
}
for r in R:
    if r["id"] in SOURCED:
        f, v, ev = SOURCED[r["id"]]
        assert not r.get(f), (r["id"], f)
        r[f] = v
        r.setdefault("srom-sourced", {})[f] = ev

ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"refs.json: {len(R)} works")
