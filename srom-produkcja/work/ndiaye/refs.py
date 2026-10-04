# refs.json for Ndiaye, "Black Roma" (RQ 75, 2022) — typed from ndiaye_pdf_bib.txt (the author's list), nothing added.
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
def chap(id, au, title, cont, page, place, pub, year, **kw):
    d = {"id": id, "type": "chapter", "author": au, "title": title, "container-title": cont, "page": page,
         "publisher-place": place, "publisher": pub, "issued": Y(year)}
    d.update(kw); return d
MOL = [P("Molière", "Jean-Baptiste")]
R = [
 {"id": "admant2015", "type": "thesis", "author": [P("Admant", "Jules")],
  "title": "L’existence régionale de la “nation bohémienne”: Les Bohémiens lorrains à la fin de l’Ancien Régime; (XVIIe–XVIIIe siècles)",
  "publisher-place": "Dijon", "publisher": "Université de Bourgogne", "issued": Y(2015),
  "srom-as-written": {"publisher-place": "Droit"}},   # "Droit" is a slip for Dijon (MB 28.09.2026)
 book("andrews1993", [P("Andrews", "Richard")], "Scripts and Scenarios: The Performance of Comedy in Renaissance Italy", "Cambridge", "Cambridge University Press", 1993),
 chap("asseo1974", [P("Asséo", "Henriette")], "Le traitement administratif des Bohémiens", "Problèmes socio-culturels en France au XVIIe siècle", "11–87", "Paris", "Klincksieck", 1974),
 art("asseo2009", [P("Asséo", "Henriette")], "Travestissement et divertissement: Bohémiens et Égyptiens à l’époque moderne", "Les Dossiers du Grihl", None, None, None, 2009, DOI="10.4000/dossiersgrihl.3680"),
 art("boulanger2000", [P("Boulanger", "Marc")], "Justice et absolutisme: La grande ordonnance criminelle d’août 1670", "Revue d’histoire moderne et contemporaine", "47", "1", "9–36", 2000),
 {"id": "brome", "type": "webpage", "author": [P("Brome", "Richard")], "editor": [P("Steggle", "Matthew")],
  "title": "The English Moor, or the Mock-Marriage", "container-title": "Richard Brome Online", "URL": "http://www.dhi.ac.uk/brome"},
 art("brooks2012", [P("Brooks", "Ethel C.")], "The Possibilities of Romani Feminism", "Signs: Journal of Women in Culture & Society", "38", "1", "1–11", 2012),
 book("browne1672", [P("Browne", "Thomas")], "Pseudodoxia epidemica, or Enquiries into the very many received tenents and commonly presumed truths", "London", "Printed by J. R. for Nath. Ekins", 1672, edition="6"),
 book("camus1640", [P("Camus", "Jean-Pierre")], "L’amphithéatre sanglant où sont représentées plusieurs actions tragiques de nostre temps. Par Monsieur l’evesque de Belley", "Rouen", "chez Jean de la Mare", 1640),
 book("carlell1657", [P("Carlell", "Lodowick")], "The fool would be a favourit, or, The discreet lover: A trage-comedy", "London", "Printed for Humphrey Moseley", 1657),
 art("cathelin2004", [P("Cathelin", "Annie")], "Imaginaire et réalités de la discrimination chez les Gitans et les <i>Paios</i>", "Esprit critique", "6", "1", "110–124", 2004),
 book("cervantes1617", [P("Cervantes Saavedra", "Miguel", **{"dropping-particle": "de"})], "Novelas exemplares", "Pamplona", "por Nicolas de Assiayn", 1617),
 book("chang2020", [P("Chang", "Felix B."), P("Rucker-Chang", "Sunnie T.")], "Roma Rights and Civil Rights: A Transatlantic Comparison", "Cambridge", "Cambridge University Press", 2020),
 book("chevreau1656", [P("Chevreau", "Urbain")], "Poésies", "Paris", "chez Antoine de Sommaville", 1656),
 art("cressy2016", [P("Cressy", "David")], "Trouble with the Gypsies in Early Modern England", "Historical Journal", "59", "1", "45–70", 2016),
 book("crooks1931", [P("Crooks", "Esther Josephine")], "The Influence of Cervantes in France in the Seventeenth Century", "Baltimore, MD", "Johns Hopkins University Press", 1931),
 book("damon1997", [P("Damon", "Cynthia")], "The Mask of the Parasite: A Pathology of Roman Patronage", "Ann Arbor", "University of Michigan Press", 1997),
 book("daugeroth2019", [P("Dauge-Roth", "Katherine")], "Signing the Body: Marks on Skin in Early Modern France", "New York", "Routledge", 2019),
 book("davity1660", [P("Davity", "Pierre")], "Description générale de l’Afrique, seconde partie du monde", "Paris", "chez Denys Béchet et Louis Billaine", 1660),
 book("dodoens1578", [P("Dodoens", "Rembert"), P("Lyte", "Henry")], "A nievve herball, or historie of plantes. First set foorth in the Doutche or Almaigne tongue, by that learned D. Rembert Dodoens, physition to the Emperour: and nowe first translated out of French into English, by Henry Lyte Esquyer", "London [i.e., Antwerp]", "Printed by Henry Loë, sold by my Gerard Dewes", 1578),
 {"id": "filhol2010", "type": "article-journal", "author": [P("Filhol", "Emmanuel")], "title": "La France contre ses Tsiganes", "container-title": "La vie des idées",
  "issued": Y(2010), "URL": "https://laviedesidees.fr/La-France-contre-ses-Tsiganes.html"},
 chap("filhol2013", [P("Filhol", "Emmanuel")], "De la couleur des Tsiganes en France", "De quelle couleur sont les blancs? Des “petits Blancs” des colonies au “racisme anti-Blancs”", "269–277", "Paris", "La Découverte", 2013, editor=[P("Laurent", "Sylvie")]),
 book("fleay1891", [P("Fleay", "Frederick")], "A Biographical Chronicle of the English Drama, 1559–1642", "London", "Reeves and Turner", 1891, volume="2"),
 book("forestier1988", [P("Forestier", "Georges")], "Esthétique de l’identité dans le théâtre français, 1550–1680: Le déguisement et ses avatars", "Genève", "Droz", 1988),
 book("framolinero1995", [P("Fra-Molinero", "Baltasar")], "La imagen de los negros en el teatro del Siglo de Oro", "Madrid", "Siglo XXI", 1995),
 art("galland2017", [P("Galland", "Nora")], "Name-Calling the Egyptian Queen in <i>Antony and Cleopatra</i>: A Case in Point of the Distortion of Africa through the Racial Slur ‘Gypsy’", "Shakespeare en devenir", "12", None, None, 2017, URL="https://shakespeare.edel.univ-poitiers.fr/shakespeare/index.php?id=1859"),
 book("goldberg2019", [P("Goldberg", "K. Meira")], "Sonidos Negros: On the Blackness of Flamenco", "Oxford", "Oxford University Press", 2019),
 book("harbage1940", [P("Harbage", "Alfred")], "Annals of English Drama, 975–1700: An Analytical Record of All Plays, Extant or Lost, Chronologically Arranged and Indexed by Authors, Titles, Dramatic Companies, Etc.", "Philadelphia; Oxford", "University of Pennsylvania Press in cooperation with the Modern Language Association of America; Oxford University Press", 1940),
 book("head1688", [P("Head", "Richard")], "The English rogue, containing a brief discovery of the most eminent cheats, robberies, and other extravagancies, by him committed. To which is added a canting dictionary of words now in use with beggars and gypsies", "London", "for J. Blare", 1688),
 {"id": "hendricks1994", "type": "book", "editor": [P("Hendricks", "Margo"), P("Parker", "Patricia")], "title": "Women, “Race,” and Writing in the Early Modern Period",
  "publisher-place": "New York", "publisher": "Routledge", "issued": Y(1994)},
 book("hitchcock2016", [P("Hitchcock", "David J.")], "Vagrancy in English Culture and Society, 1650–1750", "London", "Bloomsbury Academic", 2016),
 book("hornback2018", [P("Hornback", "Robert")], "Racism and Early Blackface Comic Traditions: From the Old World to the New", "Cham", "Palgrave Macmillan", 2018),
 book("hutner2001", [P("Hutner", "Heidi")], "Colonial Women: Race and Culture in Stuart Drama", "Oxford", "Oxford University Press", 2001),
 book("jaffeberg2015", [P("Jaffe-Berg", "Erith")], "Commedia Dell’arte and the Mediterranean: Charting Journeys and Mapping “Others”", "Farnham", "Ashgate", 2015),
 book("katritzky2006", [P("Katritzky", "M. A.")], "The Art of Commedia: The Study in the Commedia Dell’arte 1560–1620 with Special Reference to the Visual Records", "Leiden", "Brill", 2006),
 book("king2019", [P("King", "Tiffany Lethabo")], "The Black Shoals: Offshore Formations of Black and Native Studies", "Durham, NC", "Duke University Press", 2019),
 chap("kocze2020", [P("Kóczé", "Angéla")], "Gendered and Racialized Social Insecurity of Roma in East Central Europe", "The Roma and Their Struggle for Identity in Contemporary Europe", "124–149", "New York", "Berghahn Books", 2020,
      editor=[P("Baar", "Huub", **{"non-dropping-particle": "van"}), P("Kóczé", "Angéla")]),
 book("krantz1520", [P("Krantz", "Albert")], "Saxonia", "Cologne", "J. Soter alias Heil", 1520),
 book("lawrence1912", [P("Lawrence", "William J.")], "The Elizabethan Playhouse, and Other Studies", "Stratford-upon-Avon", "Shakespeare Head Press", 1912),
 art("levin1967", [P("Levin", "Harry")], "From Terence to Tabarin: A Note on <i>Les Fourberies de Scapin</i>", "Yale French Studies", "38", None, "128–137", 1967),
 book("lowe2015", [P("Lowe", "Lisa")], "The Intimacies of Four Continents", "Durham, NC", "Duke University Press", 2015),
 art("lucassen2003", [P("Lucassen", "Leo"), P("Willems", "Wim")], "The Weakness of Well-Ordered Societies: Gypsies in Western Europe, the Ottoman Empire, and India, 1400–1914", "Review (Fernand Braudel Center)", "26", "3", "283–313", 2003),
 book("mw1662", [{"literal": "M. W., M. A."}], "A comedy called The marriage broaker: or, The pander", "London", None, 1662),
 {"id": "matache2018", "type": "article-newspaper", "author": [P("Matache", "Margareta"), P("West", "Cornel")], "title": "Roma and African-Americans Share a Common Struggle",
  "container-title": "Guardian", "issued": Y(2018, 2, 20), "URL": "https://www.theguardian.com/commentisfree/2018/feb/20/roma-african-americans-common-struggle"},
 book("matras2014", [P("Matras", "Yaron")], "I Met Lucky People: The Story of the Romany Gypsies", "London", "Penguin Books", 2014),
 book("mayall2004", [P("Mayall", "David")], "Gypsy Identities, 1500–2000: From Egipcyans and Moon-Men to the Ethnic Romany", "New York", "Routledge", 2004),
 art("mckee2008", [P("McKee", "Sally")], "Domestic Slavery in Renaissance Italy", "Slavery and Abolition", "29", "3", "305–326", 2008),
 art("mejialaperle2017", [P("Mejia-LaPerle", "Carol")], "An Unlawful Race: Shakespeare’s Cleopatra and the Crimes of Early Modern Gypsies", "Shakespeare", "13", "3", "226–238", 2017),
 book("menestrier1682", [P("Ménestrier", "Claude-François")], "Des ballets anciens et modernes selon les règles du théâtre", "Paris", "René Guignard", 1682),
 book("mills1997", [P("Mills", "Charles W.")], "The Racial Contract", "Ithaca, NY", "Cornell University Press", 1997),
 book("moliere1663", MOL, "L’étourdi ou les contre-temps", "Paris", "Gabriel Quinet", 1663),
 book("moliere1668", MOL, "Le mariage forcé, comédie", "Paris", "chez Jean Ribou", 1668),
 book("moliere1671", MOL, "Les fourberies de Scapin", "Paris", "chez Pierre le Monnier", 1671),
 chap("moliere1673", MOL, "Monsieur de Pourceaugnac", "Les oeuvres de Monsieur Molière", "1–90", "Paris", "Claude Barbin", 1673, volume="6"),
 book("moliere1674", MOL, "Le malade imaginaire, comédie en trois actes mêlez de danses et de musique", "Amsterdam", "Daniel Elzevir", 1674),
 chap("moliere1827", MOL, "La pastorale comique", "Œuvres complètes de Molière", "37–50", "Paris", "Baudouin Frères, Éditeurs", 1827, volume="4"),
 book("montluc1654", [P("Montluc", "Adrien", **{"dropping-particle": "de"})], "La comédie des proverbes", "Troyes", "chez Nicolas Oudot", 1654),
 art("ndiaye2021", [P("Ndiaye", "Noémie")], "‘Come Aloft, Jack-Little-Ape!’: Race and Dance in <i>The Spanish Gypsie</i>", "English Literary Renaissance", "51", "1", "121–151", 2021),
 book("ndiaye2022", [P("Ndiaye", "Noémie")], "Scripts of Blackness: Early Modern Performance Culture and the Making of Race", "Philadelphia", "University of Pennsylvania Press", 2022),
 book("netzloff2003", [P("Netzloff", "Mark")], "England’s Internal Colonies: Class, Capital, and the Literature of Early Modern English Colonialism", "New York", "Palgrave Macmillan", 2003),
 art("newman2015", [P("Newman", "Karen")], "‘La gitanilla’ in France, from Page to Stage", "Republics of Letters", "4", "2", "1–10", 2015, URL="https://arcade.stanford.edu/rofl/la-gitanilla-france-page-stage"),
 book("nicoll1963", [P("Nicoll", "Allardyce")], "The World of Harlequin: A Critical Study of the Commedia Dell’arte", "Cambridge", "Cambridge University Press", 1963),
 book("nocentelli2013", [P("Nocentelli", "Carmen")], "Empires of Love: Europe, Asia, and the Making of Early Modern Identity", "Philadelphia", "University of Pennsylvania Press", 2013),
 book("parkhong2021", [P("Park Hong", "Cathy")], "Minor Feelings: An Asian American Reckoning", "New York", "One World", 2021),
 book("pasquier1621", [P("Pasquier", "Étienne")], "Les recherches de la France d’Estienne Pasquier", "Paris", "chez Laurens Sonnius", 1621),
 book("patterson1982", [P("Patterson", "Orlando")], "Slavery and Social Death: A Comparative Study", "Cambridge, MA", "Harvard University Press", 1982),
 art("phillips2008", [P("Phillips", "Susan")], "Schoolmasters, Seduction, and Slavery: Polyglot Dictionaries in Pre-Modern England", "Medievalia et humanistica", "34", None, "129–158", 2008),
 book("plesiat2010", [P("Plésiat", "Mathieu")], "Les Tsiganes: L’intégration éprouvée", "Paris", "L’Harmattan", 2010, volume="2"),
 book("ravenscroft1672", [P("Ravenscroft", "Edward")], "The citizen turn’d gentleman: a comedy", "London", "T. Dring", 1672),
 book("ravenscroft1677", [P("Ravenscroft", "Edward")], "Scaramouch a philosopher, Harlequin a school-boy, bravo, merchant, and magician. A comedy after the Italian manner: Acted at the Theatre-Royal", "London", "Printed for Robert Sollers", 1677),
 book("ravenscroft1678", [P("Ravenscroft", "Edward")], "The English lawyer: a comedy: acted at the Royal Theatre", "London", "Printed by J. M. for James Vade", 1678),
 book("reynolds2002", [P("Reynolds", "Bryan")], "Becoming Criminal: Transversal Performance and Cultural Dissidence in Early Modern England", "Baltimore, MD", "Johns Hopkins University Press", 2002),
 book("robinson1983", [P("Robinson", "Cedric")], "Black Marxism: The Making of the Black Radical Tradition", "Chapel Hill", "University of North Carolina Press", 1983),
 book("ruggle1662", [P("Ruggle", "George")], "Ignoramus: a comedy as it was several times acted with extraordinary applause before the Majesty of King James. With a supplement which (out of respect to the students of the common law), was hitherto wanting. Written in Latine by R. Ruggles […] and translated into English by R. C. […]", "London", "Printed for W. Gilbertson", 1662),
 book("sallebray1642", [P("Sallebray", "Monsieur")], "La belle Egyptienne: Tragi-comedie", "Paris", "Antoine de Sommaville and Augustin Courbé", 1642),
 book("scudery1649", [P("Scudéry", "Georges", **{"dropping-particle": "de"})], "Poésies diverses", "Paris", "chez Augustin Courbe", 1649),
 book("sentaurens1984", [P("Sentaurens", "Jean")], "Séville et le théâtre: De la fin du Moyen Age à la fin du XVIIe siècle", "Lille; Talence", "Atelier national de reproduction des thèses, Université de Lille III; Diffusion, Presses universitaires de Bordeaux, Université de Bordeaux III", 1984),
 book("taylor2014", [P("Taylor", "Becky")], "Another Darkness, Another Dawn: A History of Gypsies, Roma and Travellers", "London", "Reaktion Books", 2014),
 book("thompson2008", [P("Thompson", "Ayanna")], "Performing Race and Torture on the Early Modern Stage", "New York", "Routledge", 2008),
 book("touambona2016", [P("Touam Bona", "Dénètem")], "Fugitif, où cours-tu?", "Paris", "Presses Universitaires de France", 2016),
 book("vallee1657", [P("Vallée")], "Le fidelle esclave, comédie", "Paris", "chez Jean Cochart", 1657),
 {"id": "vanlennep1965", "type": "book", "editor": [P("Van Lennep", "William")], "srom-as-written": {"editor": "Van Lannep"},
  "title": "The London Stage, 1660–1800: A Calendar of Plays, Entertainments and Afterpieces, Together with Casts, Box-Receipts and Contemporary Comment; Part 1, 1660–1700",
  "publisher-place": "Carbondale", "publisher": "Southern Illinois University Press", "issued": Y(1965)},
 {"id": "wagner2019", "type": "article-journal", "author": [P("Wagner", "Sydnee"), P("Andrzejewski", "Alicia")],
  "title": "‘Bodies Mutilated for the Nation’: Reproductive Rights and Women of Color Across Time", "container-title": "Synapsis", "issued": Y(2019, 6, 10),
  "URL": "https://medicalhealthhumanities.com/2019/06/10/bodies-mutilated-for-the-nation-reproductive-rights-and-women-of-color-across-time/"},
 book("zysberg1987", [P("Zysberg", "André")], "Les galériens: Vies et destins de 60,000 forçats sur les galères de France, 1680–1748", "Paris", "Editions du Seuil", 1987),
]
assert len(R) == 84 and len({r["id"] for r in R}) == 84, (len(R), len({r["id"] for r in R}))
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("refs.json", len(R))
