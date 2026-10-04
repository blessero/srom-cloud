# refs.json for Tittel, "Racial and Social Dimensions of Antiziganism: The Representation of “Gypsies” in Political
# Theory", On_Culture: The Open Journal for the Study of Culture 10 (2020), published 21.04.2021, 23 pp.
# The source has no bibliography: every work is typed from its first full citation in the endnotes (note numbers
# below are the printed ones). Chicago-style notes with place and publisher; nothing added except where marked
# VERIFIED (a primary page or Crossref/DataCite, evidence in tittel_queries.md B); the author's form of any changed
# field is kept in `srom-as-written`. Missing data print [BRAK …] and are listed (queries A). DOIs checked
# (doi_check.txt). Abbreviated ranges in full (Kanon § 3.2). Inner quotation marks in titles as “ ” (as in the other
# refs files). Short titles: the author's where she uses one, else the main title (Kanon § 7.3).
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
def AW(**kw): return {"srom-as-written": kw}

KANT = [P("Kant", "Immanuel")]
AHE = "Anthropology, History, and Education"
AHE_EDS = [P("Louden", "Robert"), P("Zoller", "Gunter")]          # as written (Robert B. Louden, Günter Zöller: B6)
CUP = "Cambridge University Press"
HUND_ED = [P("Hund", "Wulf D.")]
FFF = "Faul, fremd und frei"
AUA = "Aufklärung und Antiziganismus"
KN = "Königshausen & Neumann"
UNRAST = "Unrast Verlag"
MARX = [P("Marx", "Karl")]
STAT = "The Statutes at Large, of England and of Great-Britain: From Magna Carta to the Union of the Kingdoms of Great Britain and Ireland. In Twenty Volumes"
EYRE = "G. Eyre and A. Strahan"
EYRE_AW = "Printed by G. Eyre and A. Strahan, printers to the King"
ZR = [P("Zeller", "Gustav Hermann"), P("Reyscher", "August Ludwig")]
ZR_SERIES = "Vollständige, historisch und kritisch bearbeitete Sammlung der württembergischen Gesetze"
R = [
 # 2 — co-authors VERIFIED (Heinrich-Böll-Stiftung chapter page; the author writes "Oliver Decker et al."; Kanon § 9.1)
 chap("decker2018", [P("Decker", "Oliver"), P("Kiess", "Johannes"), P("Schuler", "Julia"), P("Handke", "Barbara"),
                     P("Brähler", "Elmar")], "Die Leipziger Autoritarismus-Studie 2018: Methode, Ergebnisse und Langzeitverlauf",
      "Flucht ins Autoritäre: Rechtsextreme Dynamiken in der Mitte der Gesellschaft. Die Leipziger Autoritarismus-Studie 2018",
      [P("Decker", "Oliver"), P("Brähler", "Elmar")], "Psychosozial-Verlag", "Gießen", 2018, "65–115",
      **S("Die Leipziger Autoritarismus-Studie 2018…"), **AW(author="Decker")),
 # 3 — "Human rights interventions" after the title: the Palgrave series (B1)
 book("vanbaar2019", None, "The Securitization of the Roma in Europe", "Palgrave Macmillan", "Cham, Switzerland", 2019,
      editor=[P("Baar", "Huub", **{"non-dropping-particle": "van"}), P("Ivasiuc", "Ana"), P("Kreide", "Regina")],
      **{"collection-title": "Human Rights Interventions"},
      **AW(**{"title": "The Securitization of the Roma in Europe. Human rights interventions"})),
 # 4 — series "Schriftenreihe" 12 (of the Dokumentations- und Kulturzentrum Deutscher Sinti und Roma) as written
 book("end2019", [P("End", "Markus")], "Antiziganismus und Polizei: Mit Dokumentation der Fachveranstaltung “Die Polizei und "
      "Minderheiten – Das Beispiel Antiziganismus” und einem ergänzenden Beitrag zum OEZ-Attentat",
      "Zentralrat Deutscher Sinti und Roma", "Heidelberg", 2019, **{"collection-title": "Schriftenreihe", "collection-number": "12"},
      **S("Antiziganismus und Polizei…")),
 # 5
 book("lucassen1996", [P("Lucassen", "Leo")], "Zigeuner: Die Geschichte eines polizeilichen Ordnungsbegriffes in Deutschland "
      "1700–1945", "Böhlau", "Köln/Weimar/Wien", 1996, **S("Zigeuner…")),
 book("willems1997", [P("Willems", "Wim")], "In Search of the True Gypsy: From Enlightenment to Final Solution", "Frank Cass",
      "London/Portland, OR", 1997, **S("In Search of the True Gypsy")),
 book("patrut2014", [P("Patrut", "Iulia-Karin")], "Phantasma Nation: “Zigeuner” und Juden als Grenzfiguren des “Deutschen” "
      "(1770–1920)", KN, "Würzburg", 2014, **S("Phantasma Nation")),
 # 6
 chap("meuser2014", [P("Meuser", "Maria")], "Vagabunden und Arbeitsscheue: Der Zigeunerbegriff der Polizei als soziale Kategorie",
      FFF, HUND_ED, UNRAST, "Münster", 2014, "105–123", **S("Vagabunden und Arbeitsscheue")),
 # 8
 chap("hund2011", [P("Hund", "Wulf D.")], "“It Must Come from Europe”: The Racisms of Immanuel Kant", "Racisms Made in Germany",
      [P("Hund", "Wulf D."), P("Koller", "Christian"), P("Zimmermann", "Moshe")], "LIT-Verlag", "Münster, Berlin", 2011, "69–98",
      **S("“It Must Come from Europe”")),
 # 9 — the lecture series' page (URL verified: the line-end hyphen in "ras-sist" is the typesetter's; see tittel_queries C)
 {"id": "bbaw2020", "type": "webpage", "title": "Kant – Ein Rassist? Interdisziplinäre Diskussionsreihe",
  "URL": "https://www.bbaw.de/mediathek/archiv-2020/kant-ein-rassist-interdisziplinaere-diskussionsreihe",
  "accessed": Y(2020, 11, 24), "srom-undated": True},     # page read 28.09.2026: no date on it (Kanon § 8.6)
 # 10 — Canadian Journal of Philosophy, Supplementary Volume 25 (Crossref; the author: "25", B2)
 art("larrimore1999", [P("Larrimore", "Mark")], "Sublime Waste: Kant on the Destiny of the “Races”",
     "Canadian Journal of Philosophy", "25", None, 1999, "99–125", "10.1080/00455091.1999.10716832", **S("Sublime Waste")),
 chap("hill2000", [P("Hill", "Thomas E."), P("Boxill", "Bernard")], "Kant and Race", "Race and Racism", [P("Boxill", "Bernard")],
      "Oxford University Press", "Oxford", 2000, "448–471"),
 chap("bernasconi2001", [P("Bernasconi", "Robert")], "Who Invented the Concept of Race? Kant’s Role in the Enlightenment "
      "Construction of Race", "Race", [P("Bernasconi", "Robert")], "Blackwell Publishers", "Malden, Mass./Oxford", 2001, "11–36",
      **S("Who Invented the Concept of Race?…")),
 # publisher as written "Oxford University Press"; Crossref: Wiley (Blackwell), DOI 10.1002/9780470753514.ch8 (B3)
 chap("bernasconi2002", [P("Bernasconi", "Robert")], "Kant as an Unfamiliar Source of Racism", "Philosophers on Race: Critical "
      "Essays", [P("Lott", "Tommy L."), P("Ward", "Julie K.")], "Oxford University Press", "Oxford", 2002, "145–166",
      **S("Kant as an Unfamiliar Source")),
 # 11
 book("fenves2003", [P("Fenves", "Peter D.")], "Late Kant: Towards Another Law of the Earth", "Routledge", "New York/London", 2003,
      **S("Late Kant…")),
 chap("shell2006", [P("Shell", "Susan M.")], "Kant’s Concept of a Human Race", "The German Invention of Race",
      [P("Eigen", "Sara"), P("Larrimore", "Mark")], "State Univ. of New York Press", "Albany, NY", 2006, "55–72"),
 art("kleingeld2007", [P("Kleingeld", "Pauline")], "Kant’s Second Thoughts on Race", "The Philosophical Quarterly", "57", "229",
     2007, "573–592", **S("Kant’s Second Thoughts")),
 art("zhavoronkov2018", [P("Zhavoronkov", "Alexey"), P("Salikov", "Alexey")], "The Concept of Race in Kant’s Lectures on "
     "Anthropology", "Con-Textos Kantianos. International Journal of Philosophy", "7", None, 2018, "275–292",
     "10.5281/zenodo.1299140", **S("Concept of Race")),
 # 12
 book("lagier2004", [P("Lagier", "Raphaël")], "Les races humaines selon Kant", "Presses Univ. de France", "Paris", 2004),
 art("eberl2019", [P("Eberl", "Oliver")], "Kant on Race and Barbarism: Towards a More Complex View on Racism and "
     "Anti-Colonialism in Kant", "Kantian Review", "24", "3", 2019, "385–413", "10.1017/S1369415419000189", **S("Kant on Race")),
 # 14
 art("vangorkom2020", [P("Gorkom", "Joris", **{"non-dropping-particle": "van"})], "Immanuel Kant on Race Mixing: The Gypsies, "
     "the Black Portuguese, and the Jews on St. Thomas", "Journal of the History of Ideas", "81", "3", 2020, "407–427",
     "10.1353/jhi.2020.0025", **S("Immanuel Kant on Race Mixing…")),
 # 15 — journal "Kant-Studien" (the author: "Kant Studien"; Crossref DOI 10.1515/kant.1997.88.1.60, B4)
 art("rottgers1997", [P("Röttgers", "Kurt")], "Kants Zigeuner", "Kant Studien", "88", None, 1997, "60–86"),
 # 18
 book("rottgers1993", [P("Röttgers", "Kurt")], "Kants Kollege und seine ungeschriebene Schrift über die Zigeuner", "Manutius",
      "Heidelberg", 1993, **S("Kants Kollege…")),
 # 19 — the journal is "Berlinische Monatsschrift" (the text says "Berliner Monatsschrift", B5); two parts
 art("biester1793", [P("Biester", "Johann Erich")], "Über die Zigeuner", "Berlinische Monatsschrift", "21", None, 1793,
     "108–165, 360–393"),
 # 21 — unpublished dissertation, Freiburg: university not named (queries A)
 {"id": "ruch1986", "type": "thesis", "author": [P("Ruch", "Martin")], "title": "Zur Wissenschaftsgeschichte der "
  "deutschsprachigen “Zigeunerforschung” von den Anfängen bis 1900", "publisher-place": "Freiburg", "issued": Y(1986),
  "note": "maszynopis pracy doktorskiej", "title-short": "Wissenschaftsgeschichte “Zigeunerforschung”",
  "srom-as-written": {"note": "unpublished dissertation"}},
 # the editors' "(im Auftrag der Gesellschaft für Antiziganismusforschung e.V.)" left out (belongs to the volume; queries B7)
 chap("engbringromang2003", [P("Engbring-Romang", "Udo")], "Vorurteile – naturwissenschaftlich begründet: Beiträge aufgeklärter "
      "Wissenschaftler zur Begründung des rassistischen Antiziganismus", AUA, [P("Engbring-Romang", "Udo"), P("Strauß", "Daniel")],
      "I-Verb.de", "Seeheim", 2003, "34–49", **S("Vorurteile – naturwissenschaftlich begründet…")),
 book("solms2008", [P("Solms", "Wilhelm")], "Zigeunerbilder: Ein dunkles Kapitel der deutschen Literaturgeschichte. Von der "
      "frühen Neuzeit bis zur Romantik", KN, "Würzburg", 2008, **S("Zigeunerbilder…")),
 # 22 — a chapter in Rüdiger's book (the note gives the book's title, the URL, the year and the range in prose)
 chap("rudiger1782", [P("Rüdiger", "Johann Christian Christoph")], "Von der Sprache und Herkunft der Zigeuner aus Indien",
      "Neuester Zuwachs der teutschen, fremden und allgemeinen Sprachkunde in einigen Aufsätzen, Bücheranzeigen und Nachrichten",
      None, "Kummer", "Leipzig", 1782, "37–84", URL="http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb10583110-8",
      **S("Von der Sprache und Herkunft der Zigeuner…")),
 # 23
 book("grellmann1783", [P("Grellmann", "Heinrich Moritz Gottlieb")], "Die Zigeuner: Ein historischer Versuch über die "
      "Lebensart und Verfassung, Sitten und Schicksahle dieses Volkes in Europa, nebst ihrem Ursprunge",
      "Buchhandlung der Gelehrten", "Dessau/Leipzig", 1783, **S("Die Zigeuner…")),
 # 24
 book("grellmann1787", [P("Grellmann", "Heinrich Moritz Gottlieb")], "Historischer Versuch über die Zigeuner betreffend die "
      "Lebensart und Verfassung, Sitten und Schicksale dieses Volks seit seiner Erscheinung in Europa, und dessen Ursprung",
      "Dieterich", "Göttingen", 1787, edition="2", URL="http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb11256263-6",
      **S("Historischer Versuch über die Zigeuner…")),
 book("grellmann1787en", [P("Grellmann", "Heinrich Moritz Gottlieb")], "Dissertation on the Gipsies, Being an Historical "
      "Enquiry, Concerning the Manner of Life, Oeconomy, Customs and Conditions of These People in Europe, and Their Origin",
      "G. Bigg", "London", 1787, **S("Dissertation on the Gipsies…")),
 chap("ufen2014", [P("Ufen", "Katrin")], "Aus Zigeunern Menschen machen: Heinrich Moritz Gottlieb Grellmann und das "
      "Zigeunerbild der Aufklärung", FFF, HUND_ED, UNRAST, "Münster", 2014, "70–90", **S("Aus Zigeunern Menschen machen")),
 # 25 — editor "Daniel Strauss" here, "Strauß" in note 21 (B7): one form, as in note 21
 chap("breger2003", [P("Breger", "Claudia")], "Grellmann – der “Zigeunerforscher” der Aufklärung", AUA,
      [P("Engbring-Romang", "Udo"), P("Strauß", "Daniel")], "I-Verb.de", "Seeheim", 2003, "50–65",
      **S("Grellmann – der “Zigeunerforscher”"), **AW(editor="Engbring-Romang; Strauss")),
 # 32 — a recorded lecture in the Thuringian repository (Digitale Bibliothek Thüringen): a web source, as the author cites it;
# its date could not be read (the repository answers scripts with a bot check): left to the query sheet (queries C)
 {"id": "geulen2020", "type": "webpage", "author": [P("Geulen", "Christian")],
  "title": "“Rasse” und “Rassismus”: Lecture in the Lecture Series “Kant – Ein Rassist?”", "issued": Y(2020),
  "URL": "https://www.db-thueringen.de/receive/dbt_mods_00046963", "accessed": Y(2020, 11, 24), **S("“Rasse” und “Rassismus”…")},
 # 33, 40, 43, 44 — Kant in the Cambridge Edition (the author adds the year of the original to each title)
 chap("kant2010a", KANT, "Anthropology from a Pragmatic Point of View (1798)", AHE, AHE_EDS, CUP, "Cambridge", 2010, "227–429",
      **S("Anthropology from a Pragmatic Point of View")),
 # 34 — edited by G. Schmid Noerr, translated by E. Jephcott (after the imprint in the note)
 book("horkheimer2002", [P("Horkheimer", "Max"), P("Adorno", "Theodor W.")], "Dialectic of Enlightenment: Philosophical "
      "Fragments", "Stanford University Press", "Stanford, CA", 2002, editor=[P("Schmid Noerr", "Gunzelin")],
      translator=[P("Jephcott", "Edmund")], **S("Dialectic of Enlightenment…")),
 # 36
 book("timbers2016", [P("Timbers", "Frances")], "“The Damned Fraternitie”: Constructing Gypsy Identity in Early Modern England, "
      "1500–1700", "Routledge", "London/New York", 2016, **S("“The Damned Fraternitie”…")),
 # 38 — Akademie-Ausgabe vol. 15 (editor: the Prussian Academy)
 chap("kant1923", KANT, "Reflexionen zur Anthropologie", "Gesammelte Schriften", [L("Preussische Akademie der Wissenschaften")],
      "De Gruyter", "Berlin/Leipzig", 1923, "55–654", volume="15"),
 chap("kant2010b", KANT, "Of the Different Races of Human Beings (1775)", AHE, AHE_EDS, CUP, "Cambridge", 2010, "82–97",
      **S("Of the Different Races of Human Beings")),
 chap("kant1996", KANT, "Religion within the Boundaries of Mere Reason (1793)", "Religion and Rational Theology",
      [P("Wood", "Allen W."), P("Di Giovanni", "George")], CUP, "Cambridge", 1996, "39–216",
      **S("Religion within the Boundaries of Mere Reason")),
 chap("kant2010c", KANT, "Determination of the Concept of a Human Race (1785)", AHE, AHE_EDS, CUP, "Cambridge", 2010, "143–159",
      **S("Determination of the Concept of a Human Race")),
 chap("kant2010d", KANT, "On the Use of Teleological Principles in Philosophy (1788)", AHE, AHE_EDS, CUP, "Cambridge", 2010,
      "192–218", **S("Teleological Principles")),
 # 47
 chap("scholz2009", [P("Scholz", "Roswitha")], "Antiziganismus und Ausnahmezustand: Der “Zigeuner” in der Arbeitsgesellschaft",
      "Antiziganistische Zustände: Zur Kritik eines allgegenwärtigen Ressentiments",
      [P("End", "Markus"), P("Herold", "Kathrin"), P("Robel", "Yvonne")], UNRAST, "Münster", 2009, "24–40",
      **S("Antiziganismus und Ausnahmezustand…")),
 # 48
 book("amin1974", [P("Amīn", "Samīr")], "Accumulation on a World Scale: A Critique of the Theory of Underdevelopment",
      "Monthly Review Press", "New York, NY", 1974, **S("Accumulation on a World Scale…")),
 book("mies1988", [P("Mies", "Maria")], "Patriarchat und Kapital: Frauen in der internationalen Arbeitsteilung", "Rotpunktverlag",
      "Zürich", 1988, **S("Patriarchat und Kapital…")),
 book("federici2004", [P("Federici", "Silvia")], "Caliban and the Witch. Women, the Body and Primitive Accumulation", "Autonomedia",
      "New York, NY", 2004, **S("Caliban and the Witch…")),
 # 50, 53, 56 — Marx-Engels-Werke (MEW): the volume number as the series number, as written ("Karl Marx / Friedrich
 # Engels: Werke 23"); the author's siglum "MEW 23" (queries A4)
 book("marx1962", MARX, "Das Kapital: Kritik der politischen Ökonomie. Erster Band", "Dietz", "Berlin", 1962,
      **{"collection-title": "Karl Marx / Friedrich Engels: Werke", "collection-number": "23"}, **S("Das Kapital…")),
 book("marx1958", [P("Marx", "Karl"), P("Engels", "Friedrich")], "Schriften 1845–1846", "Dietz", "Berlin", 1958,
      **{"collection-title": "Karl Marx / Friedrich Engels: Werke", "collection-number": "3"}),
 book("marx1983", MARX, "Ökonomische Manuskripte 1857/1858", "Dietz", "Berlin", 1983,
      **{"collection-title": "Karl Marx / Friedrich Engels: Werke", "collection-number": "42"}),
 # 58, 59, 64 — the statutes (Kanon § 9: printed and legal sources, section IV); vol. II ed. Tomlins, III–IV Raithby
 book("tomlins1811", [P("Tomlins", "Thomas Edlyne")], STAT, EYRE, "London", 1811, volume="2",
      **{"volume-title": "From 1 Ric. II A.D. 1377 – To 19 Hen. VII. A.D. 1507", "srom-section": "IV"},
      **S("The Statutes at Large…"), **AW(publisher=EYRE_AW)),
 book("raithby1811a", [P("Raithby", "John")], STAT, EYRE, "London", 1811, volume="3",
      **{"volume-title": "From 1 Hen. VIII. A.D. 1509–10. – To 7 Edw. VI. A.D. 1553", "srom-section": "IV"},
      **S("The Statutes at Large…"), **AW(publisher=EYRE_AW)),
 book("raithby1811b", [P("Raithby", "John")], STAT, EYRE, "London", 1811, volume="4",
      **{"volume-title": "From 1 Mary, A.D. 1553. – To 16 Charles I. A.D. 1640", "srom-section": "IV"},
      **S("The Statutes at Large…"), **AW(publisher=EYRE_AW)),
 # 62 — place "Hertfordshire" (a county) and the publisher as written (B8)
 book("mayall1995", [P("Mayall", "David")], "English Gypsies and State Policies", "Gypsy Research Centre Univ. of Hertfordshire "
      "Press", "Hertfordshire", 1995, **S("English Gypsies")),
 book("mayall2004", [P("Mayall", "David")], "Gypsy Identities 1500–2000: From Egipcyans and Moon-Men to the Ethnic Romany",
      "Routledge", "London/New York", 2004, **S("Gypsy Identities")),
 # 70
 chap("bohlender1999", [P("Bohlender", "Matthias")], "Der Malthus-Effekt: Vom Ethos der Aufklärung zur Geburt des Liberalismus",
      "Neustart des Weltlaufs? Fiktion und Faszination der Zeitwende", [P("Fischer", "Karsten")], "Suhrkamp", "Frankfurt am Main",
      1999, "36–64", **S("Der Malthus-Effekt…")),
 # 80, 82 — Württemberg law collections (section IV); series as written ("… Gesetze Bd. 12")
 book("zeller1841", ZR, "Sammlung der württembergischen Regierungs-Gesetze: Erster Theil, enthaltend die Regierungs-Gesetze vom "
      "Jahre 1489 bis zum Jahre 1634", "Fues", "Tübingen", 1841,
      **{"collection-title": ZR_SERIES, "collection-number": "12", "srom-section": "IV"},
      **S("Sammlung der württembergischen Regierungs-Gesetze: Erster Theil…")),
 book("zeller1842", ZR, "Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil, enthaltend die Regierungs-Gesetze vom "
      "Jahre 1638 bis zum Jahre 1726", "Fues", "Tübingen", 1842,
      **{"collection-title": ZR_SERIES, "collection-number": "13", "srom-section": "IV"},
      **S("Sammlung der württembergischen Regierungs-Gesetze: Zweiter Theil…")),
 # 81
 chap("landwehr2001", [P("Landwehr", "Achim")], "Norm, Normalität, Anomale: Zur Konstitution von Mehrheit und Minderheit in "
      "württembergischen Polizeiordnungen der Frühen Neuzeit: Juden, Zigeuner, Bettler, Vaganten", "Minderheiten, Obrigkeit und "
      "Gesellschaft in der frühen Neuzeit: Integrations- und Abgrenzungsprozesse im süddeutschen Raum",
      [P("Häberlein", "Mark"), P("Zürn", "Martin")], "Scripta Mercaturae Verlag", "St. Katharinen", 2001, "41–74",
      **S("Norm, Normalität, Anomale")),
 # 97
 chap("reiss2011", [P("Reiss", "Matthias")], "Zwischen Revolte und Resignation: Das Bild des Arbeitslosen seit dem "
      "19. Jahrhundert", "Armut: Perspektiven in Kunst und Gesellschaft",
      [P("Uerlings", "Herbert"), P("Trauth", "Nina"), P("Clemens", "Lukas")], "Primus Verlag", "Darmstadt", 2011, "326–335",
      **S("Zwischen Revolte und Resignation…")),
 # 98
 chap("balibar1991", [P("Balibar", "Étienne")], "Is There a “Neo-Racism”?", "Race, Nation, Class: Ambiguous Identities",
      [P("Balibar", "Étienne"), P("Wallerstein", "Immanuel")], "Verso", "London", 1991, "17–28"),
 # 99
 book("reuss2015", [P("Reuss", "Anja")], "Kontinuitäten der Stigmatisierung: Sinti und Roma in der deutschen Nachkriegszeit",
      "Metropol", "Berlin", 2015, **S("Kontinuitäten der Stigmatisierung…")),
 # 100
 book("brittnacher2012", [P("Brittnacher", "Hans Richard")], "Leben auf der Grenze: Klischee und Faszination des Zigeunerbildes "
      "in Literatur und Kunst", "Wallstein Verlag", "Göttingen", 2012, **S("Leben auf der Grenze…")),
 book("reuter2014", [P("Reuter", "Frank")], "Der Bann des Fremden: Die fotografische Konstruktion des Zigeuners",
      "Wallstein Verlag", "Göttingen", 2014, **S("Der Bann des Fremden…")),
 # 101
 book("holert2006", [P("Holert", "Tom"), P("Terkessidis", "Mark")], "Fliehkraft: Gesellschaft in Bewegung – von Migranten und "
      "Touristen", "Kiepenheuer & Witsch", "Köln", 2006, **S("Fliehkraft…")),
]
ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"refs.json: {len(R)} works")
