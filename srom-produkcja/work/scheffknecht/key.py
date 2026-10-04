# Scheffknecht, "Zigeuner im Reichshof Lustenau": scheffknecht_pdf.md -> scheffknecht_pre.md (labels = printed numbers)
# -> scheffknecht_src.md (citations keyed). Every change is logged to key_log.md; check.py --keyed pre src proves no
# page, note or work was lost.
#  1. The PDF's note 1 is the note on the title (::: przypis-tytulowy); SROM numbers the author's notes 1…120, so the
#     label of PDF note n becomes n-1 (label = printed number, as with --renumber).
#  2. Full German citations and "(wie Anmerkung n)" short forms -> [@key, s. N] (srom-md.md; refs.py). Locators get
#     the Polish labels (Kanon § 7.2: s., szp. = column, przyp. = note); ranges with an en dash. Lead-in "Zitiert nach"
#     -> "Cyt. za" (as "quoted in" in the English sources). Prose lead-ins ("Dazu allgemein:") stay: text to translate.
#  3. Archival units, the printed broadsheets held in archives and the newspaper extract stay literal (Kanon § 8.1).
import re

src = open("scheffknecht_pdf.md", encoding="utf-8").read()
log = ["# key.py log — scheffknecht", ""]

# ---- 1. relabel
n_def = len(re.findall(r"^\[\^\d+\]:", src, re.M))
pre = re.sub(r"\[\^(\d+)\]", lambda m: f"[^{int(m.group(1)) - 1}]", src)
assert re.findall(r"^\[\^(\d+)\]:", pre, re.M) == [str(i) for i in range(1, n_def + 1)], "labels not 1…n"
log.append(f"relabel: PDF notes 2–{n_def + 1} -> labels 1–{n_def} (PDF note 1 = ::: przypis-tytulowy)")
open("scheffknecht_pre.md", "w", encoding="utf-8").write(pre)

# ---- 2. keying: PDF note number -> [(literal, keyed)]; "T" = the title note
LAND = ("Achim Landwehr, Norm, Normalität, Anomale. Zur Konstitution von Mehrheit und Minderheit in württembergischen "
        "Policeyordnungen der Frühen Neuzeit: Juden, Zigeuner, Bettler, Vaganten. In: Minderheiten, Obrigkeit und Gesellschaft. "
        "Integrations- und Abgrenzungsprozesse im süddeutschen Raum, hg. von Mark Häberlein/Martin Zürn. St. Katharinen 2001, "
        "S.41-74, hier S.56, Anm. 52.")
HIP = "von Hippel, Armut, Unterschichten, Randgruppen (wie Anmerkung 13), "
IRS = "Irsigler/Lassotta, Bettler und Gaukler, Dirnen und Henker (wie Anmerkung 13), "
LW = "Landwehr, Norm, Normalität, Anomale (wie Anmerkung 1), "
K = {
 "T": [(LAND, "[@landwehr2001, {s. 56, przyp. 52}].")],
 2: [("James Reynolds, Panorama of Austria in which I relate also some Pleasures to be experienced while Traveling in Bavaria "
      "and Switzerland. New York 1956, S.25-26.", "[@reynolds1956, s. 25–26].")],
 6: [("Benedikt Vetter, Der Reichshof Lustenau. Kurzgefaßte Heimatkunde von Lustenau. Bregenz 1919, S.6-7.", "[@vetter1919, s. 6–7].")],
 7: [("Benedikt Vetter, Der Reichshof Lustenau. Kurzgefaßte Heimatkunde. Bregenz ²1935, S.24.", "[@vetter1935, s. 24].")],
 8: [("Leo Jutz, Vorarlbergisches Wörterbuch mit Einschluß des Fürstentums Liechtenstein, Bd. 2. Wien 1965, Sp.1717.",
     "[@jutz1965, {szp. 1717}].")],
 9: [("Wolfgang Scheffknecht, 100 Jahre Marktgemeinde Lustenau 1902 bis 2002. Eine Chronik. Lustenau 2003, S.316.",
     "[@scheffknecht2003, s. 316].")],
 10: [("Herbert Riedmann, Zigünar-dütsch. Lustenau 1982, S.21, 24 und 119.", "[@riedmann1982, s. 21, 24, 119].")],
 11: [("Etienne François/Hagen Schulze, Einleitung. In: Deutsche Erinnerungsorte, Bd. 1, hg. von Etienne François/Hagen Schulze. "
       "München ³2002, S.9-24; Rolf Kiessling/Dietmar Schiersner, Einführung. In: Erinnerungsorte in Oberschwaben. Regionale "
       "Identität im kulturellen Gedächtnis (Forum Suevicum. Beiträge zur Geschichte Ostschwabens und der benachbarten Regionen 8), "
       "hg. von Rolf Kiessling/Dietmar Schiersner. Konstanz 2009, S.11-23, hier S.12-14.",
       "[@francois2002; @kiessling2009, s. 12–14].")],
 12: [("Reynolds, Panorama of Austria (wie Anmerkung 2), S.24.", "[@reynolds1956, s. 24].")],
 13: [("Franz Irsigler/Arnold Lassotta, Bettler und Gaukler, Dirnen und Henker. Randgruppen und Außenseiter in Köln 1300-1600 "
       "(Aus der Kölner Stadtgeschichte). Köln 1984, S.168-169; Wolfgang von Hippel, Armut, Unterschichten, Randgruppen in der "
       "frühen Neuzeit (Enzyklopädie Geschichte 34). München 1995, S.42; Bernd-Ulrich Hergemöller, Randgruppen in der "
       "spätmittelalterlichen Gesellschaft. Wege und Ziele der Forschung. In: Randgruppen in der spätmittelalterlichen "
       "Gesellschaft, hg. von Bernd-Ulrich Hergemöller. Warendorf ³2001, S.1-57, hier S.8; Andreas Niederhäuser, Am Rande der "
       "Gesellschaft: Fahrende in der Frühen Neuzeit. In: Sankt-Galler Geschichte, Bd. 4: Frühe Neuzeit: Bevölkerung und Kultur, "
       "und Bd. 9: Register und Dokumentation, St. Gallen 2003, S.147- 166 und 52-53, hier Bd. 4, S.151.",
       "[@irsigler1984, s. 168–169; @hippel1995, s. 42; @hergemoller2001, s. 8; @niederhauser2003, s. 151].")],
 14: [(HIP + "S.42.", "[@hippel1995, s. 42].")],
 15: [(IRS + "S.169-170; " + HIP + "S.42.", "[@irsigler1984, s. 169–170; @hippel1995, s. 42].")],
 16: [("Hergemöller, Randgruppen in der spätmittelalterlichen Gesellschaft (wie Anmerkung 13), S.8.", "[@hergemoller2001, s. 8].")],
 17: [(IRS + "S.170.", "[@irsigler1984, s. 170].")],
 18: [("Erich Viehöfer, „Der Schrecken seiner Zeit und die Bewunderung aller Jauner und Zigeuner“: Jakob Reinhardt, genannt "
       "Hannikel. In: Schurke oder Held? Historische Räuber und Räuberbanden (Volkskundliche Veröffentlichungen des Badischen "
       "Landesmuseums 3), hg. von Harald Siebenmorgen. Sigmaringen 1995, S.67-74, hier S.67.", "[@viehofer1995, s. 67].")],
 19: [(IRS + "S.171.", "[@irsigler1984, s. 171].")],
 20: [(HIP + "S.42.", "[@hippel1995, s. 42]."),
      ("Adalbert Nagel, Armut im Barock. Die Kehrseite einer glanzvollen Epoche. Ravensburg ²1989, S.62.", "[@nagel1989, s. 62].")],
 21: [(LW + "S.56-57.", "[@landwehr2001, s. 56–57].")],
 22: [("Zitiert nach " + LW + "S.57.", "Cyt. za [@landwehr2001, s. 57].")],
 23: [(LW + "S.57.", "[@landwehr2001, s. 57].")],
 24: [("Herman Roodenburg, Ehre in einer pluralistischen Gesellschaft: die Republik der Vereinigten Niederlande. In: Ehrkonzepte in "
       "der Frühen Neuzeit. Identitäten und Abgrenzungen (Colloquia Augustana 8), hg. von Sibylle Backmann/Hans-Jörg Künast/Sabine "
       "Ullmann/B. Ann Tlusty. Berlin 1998, S.366- 387, hier S.381.", "[@roodenburg1998, s. 381].")],
 25: [("Gerd Schwerhoff, Kriminalitätsgeschichte im deutschen Sprachraum. Zum Profil eines „verspäteten“ Forschungszweiges. In: "
       "Kriminalitätsgeschichte. Beiträge zur Sozial- und Kulturgeschichte der Vormoderne (Konflikte und Kultur – Historische "
       "Perspektiven 1), hg. von Andreas Blauert/Gerd Schwerhoff. Konstanz 2000, S.21-67, hier S.41.", "[@schwerhoff2000, s. 41].")],
 27: [(HIP + "S.42.", "[@hippel1995, s. 42].")],
 28: [("Wolfgang Scheffknecht, Armut und Not als soziales Problem. Aspekte der Geschichte vagierender Randgruppen im Bereich "
       "Vorarlbergs vom 16. bis zum 18. Jahrhundert. In: Innsbrucker Historische Studien 12/13 (1990), S.69-96, hier S.76-81.",
       "[@scheffknecht1990, s. 76–81].")],
 29: [("Nagel, Armut im Barock (wie Anmerkung 20), S.62.", "[@nagel1989, s. 62].")],
 30: [("Wolfgang Wüst, Grenzüberschreitende Landfriedenspolitik im Schwäbischen Kreis: Maßnahmen gegen Bettler, Gauner und "
       "Vaganten. In: Reichskreis und Territorium: Die Herrschaft über der Herrschaft? Supraterritoriale Tendenzen in Politik, "
       "Kultur, Wirtschaft und Gesellschaft. Ein Vergleich süddeutscher Reichskreise (Augsburger Beiträge zur Landesgeschichte "
       "Bayerisch-Schwabens 7), hg. von Wolfgang Wüst. Stuttgart 2000, S.153-178, hier S.153-154.", "[@wust2000, s. 153–154].")],
 31: [("Hans Eugen Specker, Die Reichsstadt Ulm als Tagungsort des Schwäbischen Reichskreises. In: Reichskreis und Territotium "
       "(wie Anmerkung 30), S.179-196; Winfried Dotzauer, Die deutschen Reichskreise (1383-1806). Geschichte und Aktenedition. "
       "Stuttgart 1998, S.595.", "[@specker2000; @dotzauer1998, s. 595].")],
 32: [("Karl Brauns, Das Zucht- und Arbeitshaus in Ravensburg 1725-1808. In: Zeitschrift für württembergische Landesgeschichte, "
       "10 (1951), S.158-165; Nagel, Armut im Barock (wie Anmerkung 20), S.36-39; Gerhard Fritz, „Eine Rotte von allerhandt "
       "rauberischem Gesindt“. Öffentliche Sicherheit in Südwestdeutschland vom Ende des Dreißigjährigen Krieges bis zum Ende des "
       "Alten Reiches (Stuttgarter historische Studien zur Landes- und Wirtschaftsgeschichte 6). Ostfildern 2004, S.781-783.",
       "[@brauns1951; @nagel1989, s. 36–39; @fritz2004, s. 781–783].")],
 34: [("Viehöfer, Hannikel (wie Anmerkung 18), S.67.", "[@viehofer1995, s. 67].")],
 35: [("Fritz, Öffentliche Sicherheit (wie Anmerkung 32), S.501-558; Wüst, Grenzüberschreitende Landfriedenspolitik (wie "
       "Anmerkung 30), S.170-172.", "[@fritz2004, s. 501–558; @wust2000, s. 170–172]."),
      ("Nagel, Armut im Barock (wie Anmerkung 20), S.62-63.", "[@nagel1989, s. 62–63]."),
      ("Wolfgang Scheffknecht, Reichsfreie Territorien im frühneuzeitlichen Vorarlberg: Blumenegg, St. Gerold, Hohenems und "
       "Lustenau. In: 200 Jahre Blumenegg bei Österreich. Beiträge zur Regionalgeschichte (Bludenzer Geschichtsblätter 72-74), hg. "
       "von Manfred Tschaikner. Bludenz 2004, S.110-144, hier S.130-134.", "[@scheffknecht2004, s. 130–134]."),
      ("Wolfgang Scheffknecht, Fremde Wanderkrämer und Keßler in der Grafschaft Hohenems und im Reichshof Lustenau. In: "
       "Minderheiten, Obrigkeit und Gesellschaft. Integrations- und Abgrenzungsprozesse im süddeutschen Raum, hg. von Mark "
       "Häberlein/Martin Zürn. St. Katharinen 2001, S.233-267, hier S.243-249.", "[@scheffknecht2001, s. 243–249].")],
 40: [("Wolfgang Scheffknecht, Die Hinrichtung der Barbara Waldnerin 1749 in Lustenau. In: Jahresbericht des "
       "Bundesoberstufen-Realgymnasiums Lauterach 1987/88, S.55- 59; Wolfgang Scheffknecht, „Arme Weiber“. Zur Rolle der Frau in "
       "den Unter- und Randschichten der vorindustiellen Gesellschaft. In: Hexe oder Hausfrau. Das Bild der Frau in der Geschichte "
       "Vorarlbergs, hg. von Alois Niederstätter/Wolfgang Scheffknecht. Sigmaringendorf 1991, S. 77-109, hier S.97-98.",
       "[@scheffknecht1988; @scheffknecht1991, s. 97–98].")],
 41: [(HIP + "S.101.", "[@hippel1995, s. 101].")],
 42: [(HIP + "S.100.", "[@hippel1995, s. 100].")],
 44: [(HIP + "S.42.", "[@hippel1995, s. 42].")],
 69: [("Gerhard Ammerer, Heimat Straße. Vaganten im Österreich des Ancien Régime (Sozial- und wirtschaftshistorische Studien 29). "
       "Wien-München 2003, S.171.", "[@ammerer2003, s. 171].")],
 90: [("Wüst, Grenzüberschreitende Landfriedenspolitik (wie Anmerkung 30), S.173.", "[@wust2000, s. 173].")],
 95: [(LW + "S.57-58.", "[@landwehr2001, s. 57–58].")],
 108: [("Ammerer, Heimat Straße (wie Anmerkung 69), S.171-172.", "[@ammerer2003, s. 171–172]."),
       ("Gerhard Ammerer, „…dem müssigen Vaganten Leben zugethan“ – Betrachtungen zur nichtsesshaften Bevölkerung. In: Lesebuch "
        "Altes Reich (bibliothek Altes Reich 1), hg. von Stephan Wendehorst/Siegrid Westphal. München 2006, S.168-175, hier "
        "S.172-173.", "[@ammerer2006, s. 172–173].")],
 # the citation is the subject of the sentence that follows: the token stands where the citation stood
 109: [("Ernst Schubert, Arme Leute, Bettler und Vaganten im Franken des 18. Jahrhunderts (Veröffentlichungen der Gesellschaft "
        "für fränkische Geschichte, Reihe IX: Darstellungen aus der fränkischen Geschichte 26). Neustadt an der Aisch ²1990, S.268,",
        "[@schubert1990, s. 268],")],
 110: [("Scheffknecht, Armut und Not als soziales Problem (wie Anmerkung 28), S.90-96; Ludwig Welti, Vom karolingischen "
        "Königshof zur größten österreichischen Marktgemeinde. In: Lustenauer Heimatbuch, Bd. 1. Lustenau 1965, S.82-537, hier "
        "S.141-143; Ludwig Welti, Fahrendes Volk im Reichshof Lustenau. In: Jahrbuch des Vorarlberger Landesmuseumsvereins 114 "
        "(1970), S.145-148.", "[@scheffknecht1990, s. 90–96; @welti1965, s. 141–143; @welti1970].")],
 111: [("Schubert, Arme Leute (wie Anmerkung 109), S.268.", "[@schubert1990, s. 268].")],
 112: [("Schubert, Arme Leute (wie Anmerkung 109), S.236.", "[@schubert1990, s. 236].")],
 113: [("Scheffknecht, Armut und Not als soziales Problem (wie Anmerkung 28), S.95.", "[@scheffknecht1990, s. 95].")],
 114: [("Welti, Königshof (wie Anmerkung 110), S.141-143.", "[@welti1965, s. 141–143].")],
 119: [("Ludwig Welti, Der Heimfall Lustenaus an Österreich. In: Heimat 11 (1930), S.65-68; Wolfgang Scheffknecht, Grenzlage, "
        "Identitätsbildung und Schmuggel in Spätmittelalter und früher Neuzeit: Der Reichshof Lustenau als Beispiel. In: Schriften "
        "des Vereins für Geschichte des Bodensees und seiner Umgebung 120 (2002), S.161-202.", "[@welti1930; @scheffknecht2002].")],
 120: [("Scheffknecht, 100 Jahre Marktgemeinde Lustenau (wie Anmerkung 9), S.49.", "[@scheffknecht2003, s. 49].")],
 121: [("Eugen Gabriel, Die Mundarten an der alten churrätisch-konstanzischen Bistumsgrenze im Vorarlberger Rheintal. Eine "
        "sprachwissenschaftliche und sprachpsychologische Untersuchung der Mundarten von Dornbirn, Lustenau und Hohenems (Mit "
        "Flexionslehre) (Deutsche Dialektgeographie 66). Marburg 1963.", "[@gabriel1963].")],
}

out = pre
for n, pairs in K.items():
    if n == "T":
        m = re.search(r"(?s)(::: przypis-tytulowy\n)(.*?)(\n:::)", out)
        where = "title note"
    else:
        m = re.search(rf"(?m)^(\[\^{n - 1}\]: )(.*)$()", out)
        where = f"note {n - 1} (PDF {n})"
    assert m, where
    body = m.group(2)
    for old, new in pairs:
        assert body.count(old) == 1, f"{where}: literal not found once: {old[:60]}"
        body = body.replace(old, new)
        log.append(f"- {where}: {old}\n  -> {new}")
    out = out[:m.start(2)] + body + out[m.end(2):]
open("scheffknecht_src.md", "w", encoding="utf-8").write(out)
left = [(int(l), t) for l, t in re.findall(r"(?m)^\[\^(\d+)\]: (.*)$", out) if "wie Anmerkung" in t or re.search(r"\bhg\. von\b|\bS\.\s?\d", t)]
log += ["", "## notes left literal that still carry a page or 'hg. von' (checked: archival units, broadsheets, press)"] + \
       [f"- note {l}: {t[:140]}" for l, t in left]
open("key_log.md", "w", encoding="utf-8").write("\n".join(log) + "\n")
print(f"keyed {sum(len(v) for v in K.values())} citation groups in {len(K)} notes; literal with page/editor left: {len(left)}")
