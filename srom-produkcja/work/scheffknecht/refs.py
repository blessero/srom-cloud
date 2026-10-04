# refs.json for Scheffknecht, "Zigeuner im Reichshof Lustenau" (Neujahrsblätter des Historischen Archivs der
# Marktgemeinde Lustenau 1, 2010, 77–105). The source has no bibliography: every work is typed from its first full
# citation in the notes (note numbers below are the PDF's). Nothing added: the notes give no publishers (German
# practice), so every book and edited volume prints [BRAK WYDAWCY] until MB decides (queries B1). Series are kept in
# collection-title/-number (the CSL does not print them yet: queries B2). Numeric ranges in titles set with an en dash
# (Kanon § 3.2; the PDF has hyphens) — typography, listed in the queries.
import json
def P(family, given=None, **kw):
    d = {"family": family}
    if given: d["given"] = given
    d.update(kw); return d
def Y(*a): return {"date-parts": [list(a)]}
def book(id, au, title, place, year, **kw):
    d = {"id": id, "type": "book", "author": au, "title": title, "publisher-place": place, "issued": Y(year)}
    d.update(kw); return d
def chap(id, au, title, cont, eds, page, place, year, **kw):
    d = {"id": id, "type": "chapter", "author": au, "title": title, "container-title": cont, "page": page,
         "publisher-place": place, "issued": Y(year)}
    if eds: d["editor"] = eds
    d.update(kw); return d
def art(id, au, title, cont, vol, page, year, **kw):
    d = {"id": id, "type": "article-journal", "author": au, "title": title, "container-title": cont, "page": page}
    if vol: d["volume"] = vol
    if year: d["issued"] = Y(year)
    d.update(kw); return d
def S(title, number=None):
    d = {"collection-title": title}
    if number: d["collection-number"] = number
    return d

SCH = [P("Scheffknecht", "Wolfgang")]
MINDERHEITEN = dict(cont="Minderheiten, Obrigkeit und Gesellschaft. Integrations- und Abgrenzungsprozesse im süddeutschen Raum",
                    eds=[P("Häberlein", "Mark"), P("Zürn", "Martin")], place="St. Katharinen", year=2001)
REICHSKREIS = dict(cont="Reichskreis und Territorium: Die Herrschaft über der Herrschaft? Supraterritoriale Tendenzen in Politik, "
                        "Kultur, Wirtschaft und Gesellschaft. Ein Vergleich süddeutscher Reichskreise",
                   eds=[P("Wüst", "Wolfgang")], place="Stuttgart", year=2000)
R = [
 # title note (PDF note 1)
 chap("landwehr2001", [P("Landwehr", "Achim")], "Norm, Normalität, Anomale. Zur Konstitution von Mehrheit und Minderheit in "
      "württembergischen Policeyordnungen der Frühen Neuzeit: Juden, Zigeuner, Bettler, Vaganten", page="41–74",
      **{"title-short": "Norm, Normalität, Anomale…"}, **MINDERHEITEN),
 # 2
 book("reynolds1956", [P("Reynolds", "James")], "Panorama of Austria in which I relate also some Pleasures to be experienced "
      "while Traveling in Bavaria and Switzerland", "New York", 1956, **{"title-short": "Panorama of Austria…"}),
 # 6, 7: two editions, subtitles differ
 book("vetter1919", [P("Vetter", "Benedikt")], "Der Reichshof Lustenau. Kurzgefaßte Heimatkunde von Lustenau", "Bregenz", 1919,
      **{"title-short": "Der Reichshof Lustenau…"}),
 book("vetter1935", [P("Vetter", "Benedikt")], "Der Reichshof Lustenau. Kurzgefaßte Heimatkunde", "Bregenz", 1935, edition="2",
      **{"title-short": "Der Reichshof Lustenau…"}),
 # 8
 book("jutz1965", [P("Jutz", "Leo")], "Vorarlbergisches Wörterbuch mit Einschluß des Fürstentums Liechtenstein", "Wien", 1965,
      volume="2", **{"title-short": "Vorarlbergisches Wörterbuch…"}),
 # 9
 book("scheffknecht2003", SCH, "100 Jahre Marktgemeinde Lustenau 1902 bis 2002. Eine Chronik", "Lustenau", 2003,
      **{"title-short": "100 Jahre Marktgemeinde Lustenau…"}),
 # 10
 book("riedmann1982", [P("Riedmann", "Herbert")], "Zigünar-dütsch", "Lustenau", 1982),
 # 11
 chap("francois2002", [P("François", "Etienne"), P("Schulze", "Hagen")], "Einleitung", "Deutsche Erinnerungsorte",
      [P("François", "Etienne"), P("Schulze", "Hagen")], "9–24", "München", 2002, volume="1", edition="3"),
 chap("kiessling2009", [P("Kiessling", "Rolf"), P("Schiersner", "Dietmar")], "Einführung",
      "Erinnerungsorte in Oberschwaben. Regionale Identität im kulturellen Gedächtnis",
      [P("Kiessling", "Rolf"), P("Schiersner", "Dietmar")], "11–23", "Konstanz", 2009,
      **S("Forum Suevicum. Beiträge zur Geschichte Ostschwabens und der benachbarten Regionen", "8")),
 # 13
 book("irsigler1984", [P("Irsigler", "Franz"), P("Lassotta", "Arnold")],
      "Bettler und Gaukler, Dirnen und Henker. Randgruppen und Außenseiter in Köln 1300–1600", "Köln", 1984,
      **{"title-short": "Bettler und Gaukler, Dirnen und Henker…"}, **S("Aus der Kölner Stadtgeschichte")),
 book("hippel1995", [P("Hippel", "Wolfgang", **{"dropping-particle": "von"})],
      "Armut, Unterschichten, Randgruppen in der frühen Neuzeit", "München", 1995,
      **{"title-short": "Armut, Unterschichten, Randgruppen…"}, **S("Enzyklopädie Geschichte", "34")),
 chap("hergemoller2001", [P("Hergemöller", "Bernd-Ulrich")],
      "Randgruppen in der spätmittelalterlichen Gesellschaft. Wege und Ziele der Forschung",
      "Randgruppen in der spätmittelalterlichen Gesellschaft", [P("Hergemöller", "Bernd-Ulrich")], "1–57", "Warendorf", 2001,
      edition="3", **{"title-short": "Randgruppen in der spätmittelalterlichen Gesellschaft…"}),
 # "S.147- 166 und 52-53, hier Bd. 4, S.151": the chapter in vol. 4, its notes in vol. 9 (in `note`, Polish labels)
 chap("niederhauser2003", [P("Niederhäuser", "Andreas")], "Am Rande der Gesellschaft: Fahrende in der Frühen Neuzeit",
      "Sankt-Galler Geschichte", None, "147–166", "St. Gallen", 2003, volume="4",
      **{"volume-title": "Frühe Neuzeit: Bevölkerung und Kultur", "title-short": "Am Rande der Gesellschaft…",
         "note": "przypisy w t. 9 (Register und Dokumentation), s. 52–53"}),
 # 18
 chap("viehofer1995", [P("Viehöfer", "Erich")],
      "„Der Schrecken seiner Zeit und die Bewunderung aller Jauner und Zigeuner“: Jakob Reinhardt, genannt Hannikel",
      "Schurke oder Held? Historische Räuber und Räuberbanden", [P("Siebenmorgen", "Harald")], "67–74", "Sigmaringen", 1995,
      **{"title-short": "„Der Schrecken seiner Zeit…“"}, **S("Volkskundliche Veröffentlichungen des Badischen Landesmuseums", "3")),
 # 20
 book("nagel1989", [P("Nagel", "Adalbert")], "Armut im Barock. Die Kehrseite einer glanzvollen Epoche", "Ravensburg", 1989,
      edition="2", **{"title-short": "Armut im Barock…"}),
 # 24
 chap("roodenburg1998", [P("Roodenburg", "Herman")],
      "Ehre in einer pluralistischen Gesellschaft: die Republik der Vereinigten Niederlande",
      "Ehrkonzepte in der Frühen Neuzeit. Identitäten und Abgrenzungen",
      [P("Backmann", "Sibylle"), P("Künast", "Hans-Jörg"), P("Ullmann", "Sabine"), P("Tlusty", "B. Ann")], "366–387", "Berlin", 1998,
      **{"title-short": "Ehre in einer pluralistischen Gesellschaft…"}, **S("Colloquia Augustana", "8")),
 # 25
 chap("schwerhoff2000", [P("Schwerhoff", "Gerd")],
      "Kriminalitätsgeschichte im deutschen Sprachraum. Zum Profil eines „verspäteten“ Forschungszweiges",
      "Kriminalitätsgeschichte. Beiträge zur Sozial- und Kulturgeschichte der Vormoderne",
      [P("Blauert", "Andreas"), P("Schwerhoff", "Gerd")], "21–67", "Konstanz", 2000,
      **{"title-short": "Kriminalitätsgeschichte im deutschen Sprachraum…"}, **S("Konflikte und Kultur – Historische Perspektiven", "1")),
 # 28
 art("scheffknecht1990", SCH, "Armut und Not als soziales Problem. Aspekte der Geschichte vagierender Randgruppen im Bereich "
     "Vorarlbergs vom 16. bis zum 18. Jahrhundert", "Innsbrucker Historische Studien", "12/13", "69–96", 1990,
     **{"title-short": "Armut und Not als soziales Problem…"}),
 # 30, 31 (Specker: container from note 30; note 31 spells it "Territotium")
 chap("wust2000", [P("Wüst", "Wolfgang")], "Grenzüberschreitende Landfriedenspolitik im Schwäbischen Kreis: Maßnahmen gegen "
      "Bettler, Gauner und Vaganten", page="153–178", **{"title-short": "Grenzüberschreitende Landfriedenspolitik…"},
      **S("Augsburger Beiträge zur Landesgeschichte Bayerisch-Schwabens", "7"), **REICHSKREIS),
 chap("specker2000", [P("Specker", "Hans Eugen")], "Die Reichsstadt Ulm als Tagungsort des Schwäbischen Reichskreises",
      page="179–196", **{"title-short": "Die Reichsstadt Ulm als Tagungsort…"},
      **S("Augsburger Beiträge zur Landesgeschichte Bayerisch-Schwabens", "7"), **REICHSKREIS),
 book("dotzauer1998", [P("Dotzauer", "Winfried")], "Die deutschen Reichskreise (1383–1806). Geschichte und Aktenedition",
      "Stuttgart", 1998, **{"title-short": "Die deutschen Reichskreise…"}),
 # 32
 art("brauns1951", [P("Brauns", "Karl")], "Das Zucht- und Arbeitshaus in Ravensburg 1725–1808",
     "Zeitschrift für württembergische Landesgeschichte", "10", "158–165", 1951,
     **{"title-short": "Das Zucht- und Arbeitshaus in Ravensburg…"}),
 book("fritz2004", [P("Fritz", "Gerhard")], "„Eine Rotte von allerhandt rauberischem Gesindt“. Öffentliche Sicherheit in "
      "Südwestdeutschland vom Ende des Dreißigjährigen Krieges bis zum Ende des Alten Reiches", "Ostfildern", 2004,
      **{"title-short": "„Eine Rotte von allerhandt rauberischem Gesindt“…"},
      **S("Stuttgarter historische Studien zur Landes- und Wirtschaftsgeschichte", "6")),
 # 35
 chap("scheffknecht2004", SCH, "Reichsfreie Territorien im frühneuzeitlichen Vorarlberg: Blumenegg, St. Gerold, Hohenems und Lustenau",
      "200 Jahre Blumenegg bei Österreich. Beiträge zur Regionalgeschichte", [P("Tschaikner", "Manfred")], "110–144", "Bludenz", 2004,
      **{"title-short": "Reichsfreie Territorien im frühneuzeitlichen Vorarlberg…"}, **S("Bludenzer Geschichtsblätter", "72–74")),
 chap("scheffknecht2001", SCH, "Fremde Wanderkrämer und Keßler in der Grafschaft Hohenems und im Reichshof Lustenau",
      page="233–267", **{"title-short": "Fremde Wanderkrämer und Keßler…"}, **MINDERHEITEN),
 # 40: an annual school report "1987/88" (no place, publisher or year of printing given)
 art("scheffknecht1988", SCH, "Die Hinrichtung der Barbara Waldnerin 1749 in Lustenau",
     "Jahresbericht des Bundesoberstufen-Realgymnasiums Lauterach", None, "55–59", None,
     issued={"literal": "1987/88"}, **{"title-short": "Die Hinrichtung der Barbara Waldnerin…"}),
 chap("scheffknecht1991", SCH, "„Arme Weiber“. Zur Rolle der Frau in den Unter- und Randschichten der vorindustiellen Gesellschaft",
      "Hexe oder Hausfrau. Das Bild der Frau in der Geschichte Vorarlbergs",
      [P("Niederstätter", "Alois"), P("Scheffknecht", "Wolfgang")], "77–109", "Sigmaringendorf", 1991,
      **{"title-short": "„Arme Weiber“…"}),
 # 69, 108
 book("ammerer2003", [P("Ammerer", "Gerhard")], "Heimat Straße. Vaganten im Österreich des Ancien Régime", "Wien-München", 2003,
      **{"title-short": "Heimat Straße…"}, **S("Sozial- und wirtschaftshistorische Studien", "29")),
 chap("ammerer2006", [P("Ammerer", "Gerhard")], "„…dem müssigen Vaganten Leben zugethan“ – Betrachtungen zur nichtsesshaften Bevölkerung",
      "Lesebuch Altes Reich", [P("Wendehorst", "Stephan"), P("Westphal", "Siegrid")], "168–175", "München", 2006,
      **{"title-short": "„…dem müssigen Vaganten Leben zugethan“…"}, **S("bibliothek Altes Reich", "1")),
 # 109
 book("schubert1990", [P("Schubert", "Ernst")], "Arme Leute, Bettler und Vaganten im Franken des 18. Jahrhunderts",
      "Neustadt an der Aisch", 1990, edition="2", **{"title-short": "Arme Leute…"},
      **S("Veröffentlichungen der Gesellschaft für fränkische Geschichte, Reihe IX: Darstellungen aus der fränkischen Geschichte", "26")),
 # 110
 chap("welti1965", [P("Welti", "Ludwig")], "Vom karolingischen Königshof zur größten österreichischen Marktgemeinde",
      "Lustenauer Heimatbuch", None, "82–537", "Lustenau", 1965, volume="1", **{"title-short": "Vom karolingischen Königshof…"}),
 art("welti1970", [P("Welti", "Ludwig")], "Fahrendes Volk im Reichshof Lustenau", "Jahrbuch des Vorarlberger Landesmuseumsvereins",
     "114", "145–148", 1970),
 # 119
 art("welti1930", [P("Welti", "Ludwig")], "Der Heimfall Lustenaus an Österreich", "Heimat", "11", "65–68", 1930),
 art("scheffknecht2002", SCH, "Grenzlage, Identitätsbildung und Schmuggel in Spätmittelalter und früher Neuzeit: Der Reichshof "
     "Lustenau als Beispiel", "Schriften des Vereins für Geschichte des Bodensees und seiner Umgebung", "120", "161–202", 2002,
     **{"title-short": "Grenzlage, Identitätsbildung und Schmuggel…"}),
 # 121
 book("gabriel1963", [P("Gabriel", "Eugen")], "Die Mundarten an der alten churrätisch-konstanzischen Bistumsgrenze im Vorarlberger "
      "Rheintal. Eine sprachwissenschaftliche und sprachpsychologische Untersuchung der Mundarten von Dornbirn, Lustenau und "
      "Hohenems (Mit Flexionslehre)", "Marburg", 1963, **{"title-short": "Die Mundarten an der alten churrätisch-konstanzischen Bistumsgrenze…"},
      **S("Deutsche Dialektgeographie", "66")),
]
ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), "duplicate id"
json.dump(R, open("refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"refs.json: {len(R)} works")
