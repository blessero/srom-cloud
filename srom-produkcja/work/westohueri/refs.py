# refs.json for West Ohueri, "Peripheral whiteness and racial belonging and non-belonging: accounts from Albania", ch. 6
# in C. Baker, B.C. Iacob, A. Imre, J. Mark (eds), Off White: Central and Eastern Europe and the Global History of Race,
# Manchester University Press 2024, pp. 138–155, DOI 10.7765/9781526172211.00013 (open access, CC BY-NC-ND 4.0).
# The chapter has no bibliography: every work is typed from its first full citation in the endnotes (note numbers below
# are the printed ones). Chicago notes with place and publisher (MUP house style: 'single quotes', "40:3 (2021)",
# abbreviated ranges). Nothing added except: DOIs of articles and chapters found in Crossref whose volume, issue and
# pages equal the author's (Kanon § 9.7; `srom-sourced`, evidence in doi_check.txt); ranges in full (Kanon § 3.2).
# The author's slips are kept as written and listed (queries B); missing data print [BRAK …] or nothing (pages of
# chapters) and are listed (queries A/C). Inner quotation marks in titles as “ ” (as in the other refs files). Short
# titles: the main title (before the colon), with … when cut (Kanon § 7.3).
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
    if doi:
        d["DOI"] = doi
        d["srom-sourced"] = {"DOI": "Crossref: volume, issue and pages equal the author's (doi_check.txt)"}
    d.update(kw); return d
def S(short): return {"title-short": short}
def AW(**kw): return {"srom-as-written": kw}
def SRC(**kw): return {"srom-sourced": kw}

WO = [P("Ohueri", "Chelsi West")]      # MB 29.09.2026 (D24 A5): "Ohueri, Chelsi West", as Crossref; she cites herself
                                       # "West Ohueri, ‘Zor’" (the notes print "C.W. Ohueri", short form "Ohueri")
BLUMI = [P("Blumi", "Isa")]
AI_EDS = [P("Schwandner-Sievers", "Stephanie"), P("Fischer", "Bernd Jürgen")]
AI = "Albanian Identities: Myth and History"
IUP = "Indiana University Press"
DUKE = "Duke University Press"
OUP = "Oxford University Press"
RL = "Rowman and Littlefield"
UMN = "University of Minnesota Press"
R = [
 # 1
 art("westohueri2021", WO, "On Living and Moving with Zor: Exploring Racism, Embodiment, and Health in Albania",
     "Medical Anthropology", "40", "3", 2021, "241–253", "10.1080/01459740.2020.1807539", **S("On Living and Moving with Zor")),
 # 2 — the volume is in the series "Modernity, Memory and Identity in South-East Europe" (Crossref; not printed: D18 A4)
 chap("blumi2018", BLUMI, "Battles of Nostalgic Proportion: The Transformations of Islam-as-Historical-Force in Western Balkan "
      "Reconstitutions of the Past", "Nostalgia, Loss and Creativity in South-East Europe: Political and Cultural "
      "Representations of the Past", [P("Raudvere", "Catharina")], "Springer International", "Cham", 2018,
      DOI="10.1007/978-3-319-71252-9_3", **S("Battles of Nostalgic Proportion"),
      **{"srom-sourced": {"DOI": "Crossref: chapter in this volume, pp. 37–71 (the author's page 40 inside it); pages not "
                                 "added (queries C1)"}}),
 # 3 — "Sevati" as written; Crossref and the article: Sevasti (B1)
 art("trubeta2005", [P("Trubeta", "Sevati")], "Balkan Egyptians and Gypsy/Roma Discourse", "Nationalities Papers", "33", "1",
     2005, "71–95", "10.1080/00905990500053788"),
 # 4
 art("essed2008", [P("Essed", "Philomena"), P("Trienekens", "Sandra")],
     "“Who Wants to Feel White?”: Race, Dutch Culture and Contested Identities", "Ethnic and Racial Studies", "31", "1", 2008,
     "52–72", "10.1080/01419870701538885", **S("“Who Wants to Feel White?”")),
 # 5
 book("cornell2007", [P("Cornell", "Stephen"), P("Hartmann", "Douglas")],
      "Ethnicity and Race: Making Identities in a Changing World", "Pine Forge Press", "Thousand Oaks, CA", 2007, edition="2",
      **S("Ethnicity and Race")),
 book("pierre2012", [P("Pierre", "Jemima")], "The Predicament of Blackness: Postcolonial Ghana and the Politics of Race",
      "University of Chicago Press", "Chicago, IL", 2012, **S("The Predicament of Blackness")),
 # "Yural-Davis" as written; Crossref and the article: Yuval-Davis (B2)
 art("yuvaldavis2006", [P("Yural-Davis", "Nira")], "Belonging and the Politics of Belonging", "Patterns of Prejudice", "40",
     "3", 2006, "197–214", "10.1080/00313220600769331"),
 # 6 — reprint 2000 of the 1983 first edition
 book("robinson2000", [P("Robinson", "Cedric J.")], "Black Marxism: The Making of the Black Radical Tradition",
      "University of North Carolina Press", "Chapel Hill, NC", 2000, **{"original-date": Y(1983)}, **S("Black Marxism")),
 # 7 — Crossref gives only the first page (76); the range is the author's
 art("melamed2015", [P("Melamed", "Jodi")], "Racial Capitalism", "Critical Ethnic Studies", "1", "1", 2015, "76–85",
     "10.5749/jcritethnstud.1.1.0076"),
 # 8
 book("bhattacharyya2018", [P("Bhattacharyya", "Gargi")], "Rethinking Racial Capitalism: Questions of Reproduction and Survival",
      RL, "London", 2018, **S("Rethinking Racial Capitalism")),
 # 9 — a film (Kanon § 8.7); director as the author (queries A6)
 {"id": "card2020", "type": "motion_picture", "director": [P("Card", "Kenton")],
  "title": "Geographies of Racial Capitalism with Ruth Wilson Gilmore: An Antipode Foundation Film",
  "publisher": "BFD Productions", "publisher-place": "New York", "issued": Y(2020),
  **S("Geographies of Racial Capitalism…")},
 # 10
 art("goldberg2006", [P("Goldberg", "David Theo")], "Racial Europeanization", "Ethnic and Racial Studies", "29", "2", 2006,
     "331–364", "10.1080/01419870500465611"),
 # 11
 book("said1979", [P("Said", "Edward W.")], "Orientalism", "Vintage", "New York", 1979),
 book("todorova2009", [P("Todorova", "Maria")], "Imagining the Balkans", OUP, "Oxford", 2009, edition="2"),
 # 13
 art("bjelic2022", [P("Bjelić", "Dušan I.")], "Abolition of a National Paradigm: The Case Against Benedict Anderson and Maria "
     "Todorova’s Raceless Imaginaries", "Interventions", "24", "2", 2022, "239–262", "10.1080/1369801X.2020.1863842",
     **S("Abolition of a National Paradigm")),
 # 14 — the authors edited the volume; pages not given (Crossref: 1–15, DOI 10.1057/978-1-137-47692-0_1; queries C1)
 chap("zakharov2017", [P("Zakharov", "Nikolay"), P("Law", "Ian")], "The Logics and Legacy of Soviet Racialization",
      "Post-Soviet Racisms", [P("Zakharov", "Nikolay"), P("Law", "Ian")], "Palgrave Macmillan", "London", 2017),
 # 15 — PhD dissertation (srom-md: thesis, university as publisher); the author gives no place: sourced (queries A3)
 {"id": "westohueri2016", "type": "thesis", "author": WO,
  "title": "Mapping Race and Belonging in the Margins of Europe: Albanian, Romani, and Egyptian Sentiments",
  "publisher": "The University of Texas at Austin", "publisher-place": "Austin, TX", "issued": Y(2016), "note": "praca doktorska",
  **SRC(**{"publisher-place": "the university's name; its repository record (repositories.lib.utexas.edu, item "
                              "8b1a9c1f-0cb1-441e-9d1e-77c438e54107, 29.09.2026): The University of Texas at Austin, 2016; "
                              "state as in the author's other US places"}),
  **S("Mapping Race and Belonging…")},
 # 16
 book("rexhepi2023", [P("Rexhepi", "Piro")], "White Enclosures: Racial Capitalism and Coloniality Along the Balkan Route", DUKE,
      "Durham, NC", 2023, **S("White Enclosures")),
 # 17
 book("kalmar2022", [P("Kalmar", "Ivan")], "White But Not Quite: Central Europe’s Illiberal Revolt", "Bristol University Press",
      "Bristol", 2022, **S("White But Not Quite")),
 # 18
 book("frankenberg1993", [P("Frankenberg", "Ruth")], "White Women, Race Matters: The Social Construction of Whiteness", UMN,
      "Minneapolis, MN", 1993, **S("White Women, Race Matters")),
 # 19
 book("wekker2016", [P("Wekker", "Gloria")], "White Innocence: Paradoxes of Colonialism and Race", DUKE, "Durham, NC", 2016,
      **S("White Innocence")),
 # 21
 book("maghbouleh2017", [P("Maghbouleh", "Neda")], "The Limits of Whiteness: Iranian Americans and the Everyday Politics of Race",
      "Stanford University Press", "Stanford, CA", 2017, **S("The Limits of Whiteness")),
 # 22
 book("durham1909", [P("Durham", "Edith")], "High Albania", "E. Arnold", "London", 1909),
 # 23
 book("jezernik2004", [P("Jezernik", "Božidar")], "Wild Europe: The Balkans in the Gaze of Western Travellers", "Saqi", "London",
      2004, **S("Wild Europe")),
 # 24 — facsimile reprint 1964 of the 10th edition; "J. Kramer" as written (the Weinheim publisher is J. Cramer), the 10th
 # edition is dated 1758 (vol. 1) (B3). "Carl von Linné": the author's form, as the LC NAF heading "Linné, Carl von"
 book("linne1964", [P("Linné", "Carl", **{"dropping-particle": "von"})], "Systema Naturae", "J. Kramer", "Weinheim", 1964,
      edition="10", **{"original-date": Y(1759)}),
 # 27 — pages of the chapter not given (queries C1)
 chap("malcolm2002", [P("Malcolm", "Noel")], "Myths of Albanian National Identity: Some Key Elements, as Expressed in the Works "
      "of Albanian Writers in America in the Early Twentieth Century", AI, AI_EDS, IUP, "Bloomington, IN", 2002,
      **S("Myths of Albanian National Identity")),
 # 29 — "see also Baker, this volume": her chapter in the same book (MB 29.09.2026, D24 A4); data from Crossref (DOI
 # 10.7765/9781526172211.00023: title, subtitle, book, editors, publisher, date) and its manchesterhive page (pp. 328–347);
 # place = the publisher's seat
 chap("baker2024", [P("Baker", "Catherine")], "Through the Balkans to Christchurch: Southeast Europe and Global White "
      "Nationalist Historical Mythology", "Off White: Central and Eastern Europe and the Global History of Race",
      [P("Baker", "Catherine"), P("Iacob", "Bogdan C."), P("Imre", "Anikó"), P("Mark", "James")], "Manchester University Press",
      "Manchester", 2024, "328–347", DOI="10.7765/9781526172211.00023", **S("Through the Balkans to Christchurch"),
      **SRC(all="not in the author's note ('Baker, this volume'): Crossref and the chapter page, 29.09.2026")),
 # 30 — volume given in short form in the note ("in Schwandner-Sievers and Fischer (eds), Albanian Identities"): the data of
 # note 27; pages not given
 chap("misha2002", [P("Misha", "Piro")], "Invention of a Nationalism: Myth and Amnesia", AI, AI_EDS, IUP, "Bloomington, IN", 2002,
      **S("Invention of a Nationalism")),
 # 31 — "Iljazz" as written; Crossref has the same form (the article's byline). Journal: The European Legacy: Toward New
 # Paradigms (the author drops "The")
 art("fishta1997", [P("Fishta", "Iljazz"), P("Schmidt-Neke", "Michael")], "Nationalism and National Myth: Skanderbeg and the "
     "Twentieth-Century Albanian Regimes", "European Legacy: Toward New Paradigms", "2", "1", 1997, "1–7",
     "10.1080/10848779708579680", **S("Nationalism and National Myth")),
 # 32 — "c." in italics in the PDF (a Latin abbreviation), kept as a plain title word here
 art("tochka2015", [P("Tochka", "Nicholas")], "To “Enlighten and Beautify”: Western Music and the Modern Project of Personhood "
     "in Albania, c.1906–1924", "Ethnomusicology", "59", "3", 2015, "398–420", "10.5406/ethnomusicology.59.3.0398",
     **S("To “Enlighten and Beautify”")),
 # 35 — institutional author
 book("fwp1939", [L("Federal Writers’ Project")], "The Albanian Struggle in the Old World and New", "The Writer", "Boston, MA",
      1939, **S("The Albanian Struggle…")),
 # 38 — Multicultural Shakespeare 22 (37), 2020
 art("golemi2020", [P("Golemi", "Marinela")], "Othello in the Balkans: Performing Race Rhetoric on the Albanian Stage",
     "Multicultural Shakespeare: Translation, Appropriation and Performance", "22", "37", 2020, "125–138",
     "10.18778/2083-8530.22.08", **S("Othello in the Balkans")),
 # 39
 art("hogan1998", [P("Hogan", "Patrick C.")], "“Othello”, Racism, and Despair", "CLA Journal", "41", "4", 1998, "431–451"),
 # 41 — "East European Politics and Society" as written; the journal: … Societies (Crossref, B4)
 art("blumi1998", BLUMI, "The Commodification of Otherness and the Ethnic Unit in the Balkans: How to Think About Albanians",
     "East European Politics and Society", "12", "3", 1998, "527–569", "10.1177/0888325498012003006",
     **S("The Commodification of Otherness…")),
 book("galaty2018", [P("Galaty", "Michael")], "Memory and Nation Building: From Ancient Times to the Islamic State", RL,
      "Lanham, MD", 2018, **S("Memory and Nation Building")),
 # 42 — issue only (no volume numbering)
 art("nishku2020", [P("Nishku", "Genta")], "The Wretched on the Walls: A Fanonian Reading of a Revolutionary Albanian Orphanage",
     "Feminist Critique", None, "3", 2020, "39–63", "10.52323/309702", **S("The Wretched on the Walls")),
 # 43
 book("mehilli2017", [P("Mëhilli", "Elidor")], "From Stalin to Mao: Albania and the Socialist World", "Cornell University Press",
      "Ithaca, NY", 2017, **S("From Stalin to Mao")),
 # 44 — "Journal of Southeast European and Black Sea Studies" as written; the journal: Southeast European and Black Sea
 # Studies (Crossref, B5)
 art("peshkopia2021", [P("Peshkopia", "Ridvan"), P("Giakoumis", "Konstantinos")], "Nationalistic Education and its Colourful "
     "Role in Intergroup Prejudice Reduction: Lessons from Albania", "Journal of Southeast European and Black Sea Studies", "21",
     "3", 2021, "457–480", "10.1080/14683857.2021.1932161", **S("Nationalistic Education…")),
 # 46 — pages not given
 chap("hysa2010", [P("Hysa", "Armanda")], "Ethnography in Communist Albania: Nationalist Discourse and Relations with History",
      "Historični seminar 8", [P("Keber", "Katarina"), P("Vidmar", "Luka")], "Založba ZRC", "Ljubljana", 2010,
      **S("Ethnography in Communist Albania")),
 # 48 — an edited volume (no author)
 book("turda2007", None, "Blood and Homeland: Eugenics and Racial Nationalism in Central and Southeast Europe, 1900–1940",
      "CEU Press", "Budapest", 2007, editor=[P("Turda", "Marius"), P("Weindling", "Paul J.")], **S("Blood and Homeland")),
 book("turda2010", [P("Turda", "Marius")], "Modernism and Eugenics", "Palgrave Macmillan", "Basingstoke", 2010),
 # pages not given (Crossref: 398–412, DOI 10.1093/oxfordhb/9780195373141.013.0024; queries C1)
 chap("bucur2010", [P("Bucur", "Maria")], "Eugenics in Eastern Europe, 1870s–1945", "The Oxford Handbook of the History of "
      "Eugenics", [P("Bashford", "Alison"), P("Levine", "Philippa")], OUP, "Oxford", 2010, **S("Eugenics in Eastern Europe…")),
 # 50 — not in Crossref
 art("blumi1997", BLUMI, "The Politics of Culture and Power: The Roots of Hoxha’s Postwar State", "East European Quarterly", "31",
     "3", 1997, "379–398", **S("The Politics of Culture and Power")),
 # 55
 art("nixon2010", [P("Nixon", "Nicola")], "Always Already European: The Figure of Skënderbeg in Contemporary Albanian "
     "Nationalism", "National Identities", "12", "1", 2010, "1–20", "10.1080/14608940903542540", **S("Always Already European")),
 art("kuus2004", [P("Kuus", "Merje")], "Europe’s Eastern Expansion and the Reinscription of Otherness in East-Central Europe",
     "Progress in Human Geography", "28", "4", 2004, "472–489", "10.1191/0309132504ph498oa", **S("Europe’s Eastern Expansion…")),
 # 56
 book("kajsiu2011", [P("Kajsiu", "Blendi")], "Albanian Democratization Between Europeanization and Neoliberalism",
      "Albanian Institute for International Studies", "Tirana", 2011, **S("Albanian Democratization…")),
 # 58 — "Garner, Steve." inverted in the note (B6); not in Crossref
 art("garner2007", [P("Garner", "Steve")], "The European Union and the Racialization of Immigration, 1985–2006",
     "Race/Ethnicity: Multidisciplinary Global Contexts", "1", "1", 2007, "61–87",
     **S("The European Union and the Racialization of Immigration…")),
 # 62 — "Qesku" here; "Qeshku" in the text (B7); ed. = editor after the title (Kanon § 7.2)
 book("qesku2004", [P("Qesku", "Pavli")], "Fjalor Shqip-Anglisht", "Botime EDFA", "Tirana", 2004,
      editor=[P("Xhaferi", "Fatmir")]),
 # 64
 book("kettler2020", [P("Kettler", "Andrew")], "The Smell of Slavery: Olfactory Racism and the Atlantic World",
      "Cambridge University Press", "Cambridge", 2020, **S("The Smell of Slavery")),
 # 66 — a recorded lecture (video) (queries A6); two people as the author gives them
 {"id": "hall2002", "type": "motion_picture", "author": [P("Hall", "Stuart"), P("Jhally", "Sut")],
  "title": "Race the Floating Signifier: Stuart Hall in Lecture", "publisher": "Media Education Foundation",
  "publisher-place": "Northampton, MA", "issued": Y(2002), **S("Race the Floating Signifier")},
 # 67 — dated web text (Kanon § 8.6): date and author confirmed on the page (29.09.2026: article:published_time
 # 2020-05-26, byline Gjergj Erebara); the author's URL has no scheme ("www.reporter.al/…"), the page answers at it
 {"id": "erebara2020", "type": "webpage", "author": [P("Erebara", "Gjergj")],
  "title": "Organizatat dënojnë dhunën e policisë bashkiake ndaj ricikluesit", "container-title": "Reporter.al",
  "issued": Y(2020, 5, 26), "URL": "https://www.reporter.al/organizatat-denojne-dhunen-e-policise-bashkiake-ndaj-ricikluesit/",
  "accessed": Y(2022, 12, 5), **AW(URL="www.reporter.al/organizatat-denojne-dhunen-e-policise-bashkiake-ndaj-ricikluesit/"),
  **S("Organizatat dënojnë dhunën…")},
 # 68 — Brazilian compound surname: Kanon § 9.5 sorts it under Vargas (Crossref/LC: "Vargas, João H. Costa"); not
 # expressible in CSL-JSON (srom-md.md): full surname in family, listed (queries A5)
 book("vargas2018", [P("Costa Vargas", "João Helion")], "The Denial of Antiblackness: Multiracial Redemption and Black Suffering",
      UMN, "Minneapolis, MN", 2018, **S("The Denial of Antiblackness")),
]
ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), "duplicate id"
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"refs.json: {len(R)} works")
