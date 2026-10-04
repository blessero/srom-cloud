# Tittel, "Racial and Social Dimensions of Antiziganism" (On_Culture 10, 2020):
#   tittel_pdf.md (the extraction) -> tittel_pre.md (prep: joins, a URL, the title note; logged)
#   -> tittel_src.md (citations keyed). Every change is logged to key_log.md; check.py --keyed pre src proves no page,
#   note or work was lost. Re-run after any re-extraction or change to refs.py.
#  1. Prep (not keying): line-end hyphen decisions the extractor left open (its report), the BBAW URL (checked online),
#     and note 1 — the author's acknowledgements, called from the first sentence — as the note on the title (Kanon § 7.1:
#     "przypis autora do tytułu (np. podziękowania)"); in tittel_pre.md the notes keep the original's numbers 2–101,
#     in tittel_src.md they are 1–100, the numbers SROM prints (step 4).
#  2. Chicago full citations and short forms -> [@key, s. N] (srom-md.md; refs.py). Kant's Akademie-Ausgabe references
#     after the page ("420/AA VII 324–325") stay in the locator: {s. 420 / AA VII 324–325} (queries A); "(FN)" -> przyp.
#     A chapter's own range goes to refs.json; "here:" gives the page. A citation standing in the author's sentence
#     ("what Ruch stated", "in his book in 1782") goes in brackets. Short forms of the statutes (one title, three
#     volumes): the volume as a locator, {t. 3, s. 89}. Lead-ins: See -> Zob., see -> zob., cf. -> por.,
#     See as well -> Zob. też (handoff.md). Prose around a citation stays (text to translate).
#  3. Literal: prose notes (39, 49, 57) and the quotations of the German originals (82–94, 96: "Original: …"); the
#     Marx archive URL in note 50 (a website named in prose, queries C).
import re, sys
src = open("tittel_pdf.md", encoding="utf-8").read()
log = ["# key.py log — tittel", ""]


def sub(text, old, new, why, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"key.py: expected {count}× {old!r}, found {n}")
    log.append(f"prep: {old!r} -> {new!r}: {why}")
    return text.replace(old, new)


# ---- 1. prep
pre = src
pre = sub(pre, "inter-views", "interviews", "PDF 'inter-|views' at a line end; the extractor kept the hyphen (prefix list)")
pre = sub(pre, "pre-sents", "presents", "PDF 'pre-|sents' at a line end; the extractor kept the hyphen (prefix list)")
pre = sub(pre, "landdamaging", "land-damaging", "PDF 'land-|damaging' at a line end ('Landschädliche'); 'landdamaging' is no "
          "English word — the hyphen is the author's (listed in queries C)")
pre = sub(pre, "kant-ein-ras-sist-interdisziplinaere", "kant-ein-rassist-interdisziplinaere",
          "PDF 'ras-|sist' at a line end, no link target: the address with the hyphen gives 404, without it 200 "
          "(checked 28.09.2026)")
m = re.search(r"^\[\^1\]: (.*)\n\n", pre, re.M)
title_note = m.group(1)
pre = pre[:m.start()] + pre[m.end():]
pre = sub(pre, "through state measures.[^1] Consequently", "through state measures. Consequently",
          "note 1 (acknowledgements) is the note on the title (Kanon § 7.1): marker removed here")
pre = "::: przypis-tytulowy\n" + title_note + "\n:::\n\n" + pre
log.append("prep: note 1 -> ::: przypis-tytulowy at the top (acknowledgements; queries A1)")
open("tittel_pre.md", "w", encoding="utf-8").write(pre)
n_def = re.findall(r"^\[\^(\d+)\]:", pre, re.M)
assert n_def == [str(i) for i in range(2, 102)], "labels not 2…101"
log.append("labels: 2–101 = printed note numbers (note 1 is the title note)")
log.append("")

# ---- 2. keying
GS = ("Karl Marx / Friedrich Engels: Werke")
K = {
 2: [("Oliver Decker et al., “Die Leipziger Autoritarismus-Studie 2018: Methode, Ergebnisse und Langzeitverlauf,” in *Flucht "
      "ins Autoritäre: Rechtsextreme Dynamiken in der Mitte der Gesellschaft. Die Leipziger Autoritarismus-Studie 2018*, eds. "
      "Oliver Decker and Elmar Brähler (Gießen: Psychosozial-Verlag, 2018), 65–115, here: 102–103.", "[@decker2018, s. 102–103].")],
 3: [("Huub van Baar, Ana Ivasiuc, and Regina Kreide, eds., *The Securitization of the Roma in Europe*. Human rights "
      "interventions (Cham, Switzerland: Palgrave Macmillan, 2019).", "[@vanbaar2019].")],
 4: [("Markus End, *Antiziganismus und Polizei*: *Mit Dokumentation der Fachveranstaltung \"Die Polizei und Minderheiten - Das "
      "Beispiel Antiziganismus\" und einem ergänzenden Beitrag zum OEZ-Attentat.* Schriftenreihe 12 (Heidelberg: Zentralrat "
      "Deutscher Sinti und Roma, 2019).", "[@end2019].")],
 5: [("Leo Lucassen, *Zigeuner*: *Die Geschichte eines polizeilichen Ordnungsbegriffes in Deutschland 1700–1945* "
      "(Köln/Weimar/Wien: Böhlau, 1996); Wim Willems, *In Search of the True Gypsy*: *From Enlightenment to Final Solution* "
      "(London/Portland, OR: Frank Cass, 1997); Iulia-Karin Patrut, *Phantasma Nation*: *‘Zigeuner’ und Juden als Grenzfiguren "
      "des ‘Deutschen’ (1770–1920)* (Würzburg: Königshausen & Neumann, 2014).",
      "[@lucassen1996; @willems1997; @patrut2014].")],
 6: [("See Maria Meuser, “Vagabunden und Arbeitsscheue: Der Zigeunerbegriff der Polizei als soziale Kategorie,” in *Faul, "
      "fremd und frei*, ed. Wulf D. Hund (Münster: Unrast Verlag, 2014), 105–123.", "Zob. [@meuser2014].")],
 7: [("See Patrut, *Phantasma Nation*, 18.", "Zob. [@patrut2014, s. 18].")],
 8: [("Wulf D. Hund, “‘It Must Come from Europe’: The Racisms of Immanuel Kant,” in *Racisms Made in Germany*, eds. Wulf D. "
      "Hund, Christian Koller, and Moshe Zimmermann (Münster, Berlin: LIT-Verlag, 2011), 69–98, here: 83.", "[@hund2011, s. 83].")],
 9: [("See the on-going", "Zob. the on-going"),
     ("“Kant – Ein Rassist? Interdisziplinäre Diskussionsreihe,” accessed November 24, 2020, "
      "<https://www.bbaw.de/mediathek/archiv-2020/kant-ein-rassist-interdisziplinaere-diskussionsreihe>.", "[@bbaw2020].")],
 10: [("Mark Larrimore, “Sublime Waste: Kant on the Destiny of the ‘Races’,” in *Canadian Journal of Philosophy* 25 (1999), "
       "99–125, <https://doi.org/10.1080/00455091.1999.10716832>; Thomas E. Hill and Bernard Boxill, “Kant and Race,” in *Race "
       "and Racism*, ed. Bernard Boxill (Oxford: Oxford University Press, 2000), 448–471; Robert Bernasconi, “Who Invented the "
       "Concept of Race? Kant's Role in the Enlightenment Construction of Race,” in *Race*, ed. Robert Bernasconi (Malden, "
       "Mass./Oxford: Blackwell Publishers, 2001), 11–36; Robert Bernasconi, “Kant as an Unfamiliar Source of Racism,” in "
       "*Philosophers on Race: Critical Essays*, eds. Tommy L. Lott and Julie K. Ward (Oxford: Oxford University Press, 2002), "
       "145–166.", "[@larrimore1999; @hill2000; @bernasconi2001; @bernasconi2002].")],
 11: [("Peter D. Fenves, *Late Kant*: *Towards Another Law of the Earth* (New York/London: Routledge, 2003); Susan M. Shell, "
       "“Kant's Concept of a Human Race,” in *The German Invention of Race*, eds. Sara Eigen and Mark Larrimore (Albany, NY: "
       "State Univ. of New York Press, 2006), 55–72; Pauline Kleingeld, “Kant's Second Thoughts on Race,” in *The Philosophical "
       "Quarterly* 57. 229 (2007), 573–592; Alexey Zhavoronkov and Alexey Salikov, “The Concept of Race in Kant’s Lectures on "
       "Anthropology,” in *Con-Textos Kantianos. International Journal of Philosophy*, 7 (2018), 275–292, "
       "<https://doi.org/10.5281/zenodo.1299140>.", "[@fenves2003; @shell2006; @kleingeld2007; @zhavoronkov2018].")],
 12: [("Raphaël Lagier, *Les races humaines selon Kant* (Paris: Presses Univ. de France, 2004); Oliver Eberl, “Kant on Race and "
       "Barbarism: Towards a More Complex View on Racism and Anti-Colonialism in Kant,” in *Kantian Review* 24. 3 (2019), "
       "385–413, <https://doi.org/10.1017/S1369415419000189>.", "[@lagier2004; @eberl2019].")],
 13: [("See Larrimore, “Sublime Waste,” 110; Bernasconi, “Kant as an Unfamiliar Source,” 148; Kleingeld, “Kant's Second "
       "Thoughts,” 581; Eberl, “Kant on Race,” 404.",
       "Zob. [@larrimore1999, s. 110; @bernasconi2002, s. 148; @kleingeld2007, s. 581; @eberl2019, s. 404].")],
 14: [("See Joris van Gorkom, “Immanuel Kant on Race Mixing: The Gypsies, the Black Portuguese, and the Jews on St. Thomas,” in "
       "*Journal of the History of Ideas* 81. 3 (2020), 407–427, <https://doi.org/10.1353/jhi.2020.0025>.",
       "Zob. [@vangorkom2020].")],
 15: [("Kurt Röttgers, “Kants Zigeuner,” in *Kant Studien* 88 (1997), 60–86, here: 63 (my translation).",
       "[@rottgers1997, s. 63] (my translation).")],
 16: [("Röttgers, “Kants Zigeuner,” 73–75.", "[@rottgers1997, s. 73–75].")],
 17: [("Röttgers, “Kants Zigeuner,” 64.", "[@rottgers1997, s. 64].")],
 18: [("Röttgers, “Kants Zigeuner,” 64. Even", "[@rottgers1997, s. 64]. Even"),
      ("(Röttgers, “Kants Zigeuner,” 64–75)", "([@rottgers1997, s. 64–75])"),
      ("see Kurt Röttgers, *Kants Kollege und seine ungeschriebene Schrift über die Zigeuner* (Heidelberg: Manutius, 1993).",
       "zob. [@rottgers1993].")],
 19: [("Johann Erich Biester, “Über die Zigeuner”, in *Berlinische Monatsschrift* 21 (1793), 108–165 and 360–393.",
       "[@biester1793].")],
 20: [("Röttgers, “Kants Zigeuner,” 67.", "[@rottgers1997, s. 67].")],
 21: [("Martin Ruch, *Zur Wissenschaftsgeschichte der deutschsprachigen \"Zigeunerforschung\" von den Anfängen bis 1900* "
       "(Freiburg, 1986), unpublished dissertation; Udo Engbring-Romang, “Vorurteile – naturwissenschaftlich begründet: "
       "Beiträge aufgeklärter Wissenschaftler zur Begründung des rassistischen Antiziganismus,” in *Aufklärung und "
       "Antiziganismus*, eds. Udo Engbring-Romang and Daniel Strauß (im Auftrag der Gesellschaft für Antiziganismusforschung "
       "e.V.) (Seeheim: I-Verb.de, 2003), 34–49; Wilhelm Solms, *Zigeunerbilder*: *Ein dunkles Kapitel der deutschen "
       "Literaturgeschichte. Von der frühen Neuzeit bis zur Romantik* (Würzburg: Königshausen & Neumann, 2008), 117–127.",
       "[@ruch1986; @engbringromang2003; @solms2008, s. 117–127].")],
 22: [("see Ruch, *Wissenschaftsgeschichte \"Zigeunerforschung,\"* 99.", "zob. [@ruch1986, s. 99]."),
      ("who published a chapter called ‘Von der Sprache und Herkunft der Zigeuner aus Indien’ in his book *Neuester Zuwachs der "
       "teutschen, fremden und allgemeinen Sprachkunde in einigen Aufsätzen, Bücheranzeigen und Nachrichten* (Leipzig: Kummer), "
       "<http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb10583110-8> in 1782 (37–84), and",
       "who published a chapter called ‘Von der Sprache und Herkunft der Zigeuner aus Indien’ in his book in 1782 "
       "([@rudiger1782]), and")],
 23: [("See Heinrich Moritz Gottlieb Grellmann, *Die Zigeuner*: *Ein historischer Versuch über die Lebensart und Verfassung, "
       "Sitten und Schicksahle dieses Volkes in Europa, nebst ihrem Ursprunge* (Dessau/Leipzig: Buchhandlung der Gelehrten, "
       "1783).", "Zob. [@grellmann1783]."),
      ("In contrast to what Ruch, *Wissenschaftsgeschichte \"Zigeunerforschung,\"* 103 stated, the first edition",
       "In contrast to what Ruch stated ([@ruch1986, s. 103]), the first edition")],
 24: [("Heinrich Moritz Gottlieb Grellmann, *Historischer Versuch über die Zigeuner betreffend die Lebensart und Verfassung, "
       "Sitten und Schicksale dieses Volks seit seiner Erscheinung in Europa, und dessen Ursprung*. 2nd ed. (Göttingen: "
       "Dieterich, 1787), <http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb11256263-6>. The English",
       "[@grellmann1787]. The English"),
      ("with the following title: *Dissertation on the Gipsies, Being an Historical Enquiry, Concerning the Manner of Life, "
       "Oeconomy, Customs and Conditions of These People in Europe, and Their Origin* (London: G. Bigg, 1787), and",
       "with the following title: [@grellmann1787en], and"),
      ("see Katrin Ufen, “Aus Zigeunern Menschen machen: Heinrich Moritz Gottlieb Grellmann und das Zigeunerbild der "
       "Aufklärung,” in *Faul, fremd und frei*, ed. Wulf D. Hund (Münster: Unrast Verlag, 2014), 70–90, here: 87.",
       "zob. [@ufen2014, s. 87].")],
 25: [("Ruch, *Wissenschaftsgeschichte \"Zigeunerforschung\"*; Willems, *In Search of the True Gypsy*. See as well Claudia "
       "Breger, “Grellmann – der ‘Zigeunerforscher’ der Aufklärung,” in *Aufklärung und Antiziganismus*, eds. Udo "
       "Engbring-Romang and Daniel Strauss (Seeheim: I-Verb.de, 2003), 50–65 and Ufen, “Aus Zigeunern Menschen machen.”",
       "[@ruch1986; @willems1997]. Zob. też [@breger2003] i [@ufen2014].")],
 26: [("Ruch, *Wissenschaftsgeschichte \"Zigeunerforschung,\"* 143–153.", "[@ruch1986, s. 143–153].")],
 27: [("(Eberl, “Kant on Race,” 390)", "([@eberl2019, s. 390])"), ("(Eberl, “Kant on Race,” 408)", "([@eberl2019, s. 408])")],
 28: [("Hund, “‘It Must Come from Europe’,” 83.", "[@hund2011, s. 83].")],
 29: [("Hund, “‘It Must Come from Europe’,” 84–85.", "[@hund2011, s. 84–85].")],
 30: [("see Larrimore, “Sublime Waste.”", "zob. [@larrimore1999].")],
 31: [("See Larrimore, “Sublime Waste,” 101.", "Zob. [@larrimore1999, s. 101].")],
 32: [("Christian Geulen, “*‘Rasse’ und ‘Rassismus’*: *Lecture in the Lecture Series ‘Kant – Ein Rassist?’*” (2020), accessed "
       "November 24, 2020, <https://www.db-thueringen.de/receive/dbt_mods_00046963>.", "[@geulen2020].")],
 33: [("Immanuel Kant, “Anthropology from a Pragmatic Point of View (1798),” in *Anthropology, History, and Education*, eds. "
       "Robert Louden and Gunter Zoller (Cambridge: Cambridge University Press, 2010), 227–429, here: 420/AA VII 324–325",
       "[@kant2010a, {s. 420 / AA VII 324–325}]")],
 34: [("Max Horkheimer and Theodor W. Adorno, *Dialectic of Enlightenment*: *Philosophical Fragments* (Stanford, CA: Stanford "
       "University Press, 2002), edited by Gunzelin Schmid Noerr; transl. by Edmund Jephcott, 24.", "[@horkheimer2002, s. 24].")],
 35: [("see Zhavoronkov and Salikov, “Concept of Race,” 285–287.", "zob. [@zhavoronkov2018, s. 285–287].")],
 36: [("(Ruch, *Wissenschaftsgeschichte \"Zigeunerforschung,\"* 150–153)", "([@ruch1986, s. 150–153])"),
      ("see Frances Timbers, *“The Damned Fraternitie”*: *Constructing Gypsy Identity in Early Modern England, 1500–1700* "
       "(London/New York: Routledge, 2016), 7–38.", "zob. [@timbers2016, s. 7–38].")],
 37: [("see Hund, “‘It Must Come from Europe’,” 84, 86, and 90.", "zob. [@hund2011, s. 84, 86, 90].")],
 38: [("Immanuel Kant, “Reflexionen zur Anthropologie,” in *Gesammelte Schriften.* Vol. 15, ed. Preussische Akademie der "
       "Wissenschaften (Berlin/Leipzig: De Gruyter, 1923), 55–654, here: 597/AA XV 597 (my translation).",
       "[@kant1923, {s. 597 / AA XV 597}] (my translation)."),
      ("cf. Larrimore, “Sublime Waste,” 111–112.", "por. [@larrimore1999, s. 111–112].")],
 40: [("Immanuel Kant, “Of the Different Races of Human Beings (1775),” in *Anthropology, History, and Education*, eds. Robert "
       "Louden and Gunter Zoller (Cambridge: Cambridge University Press, 2010), 82–97, here: 93/AA II 439.",
       "[@kant2010b, {s. 93 / AA II 439}].")],
 41: [("Immanuel Kant, “Religion within the Boundaries of Mere Reason (1793),” in *Religion and Rational Theology*, eds. Allen "
       "W. Wood and George Di Giovanni (Cambridge: Cambridge University Press, 1996), 39–216, here: 163 (FN)/AA VI 136–137 (FN).",
       "[@kant1996, {s. 163, przyp. / AA VI 136–137, przyp.}].")],
 42: [("Breger, “Grellmann – der ‘Zigeunerforscher’,” 65.", "[@breger2003, s. 65].")],
 43: [("Immanuel Kant, “Determination of the Concept of a Human Race (1785),” in *Anthropology, History, and Education*, eds. "
       "Robert Louden and Gunter Zoller (Cambridge: Cambridge University Press, 2010), 143–159, here: 158/AA VIII 105.",
       "[@kant2010c, {s. 158 / AA VIII 105}]."),
      ("see Hund, “‘It Must Come from Europe’,” 84–85.", "zob. [@hund2011, s. 84–85].")],
 44: [("Immanuel Kant, “On the Use of Teleological Principles in Philosophy (1788),” in *Anthropology, History, and "
       "Education*, eds. Robert Louden and Gunter Zoller (Cambridge: Cambridge University Press, 2010), 192–218, here: "
       "207/AA VIII 172", "[@kant2010d, {s. 207 / AA VIII 172}]")],
 45: [("Kant, “Teleological Principles,” in *Anthropology, History, and Education*, 209/AA VIII 174.",
       "[@kant2010d, {s. 209 / AA VIII 174}].")],
 46: [("Eberl, “Kant on Race,” 406.", "[@eberl2019, s. 406].")],
 47: [("Roswitha Scholz, “Antiziganismus und Ausnahmezustand: Der ‘Zigeuner’ in der Arbeitsgesellschaft,” in "
       "*Antiziganistische Zustände: Zur Kritik eines allgegenwärtigen Ressentiments*, eds. Markus End, Kathrin Herold, and "
       "Yvonne Robel (Münster: Unrast Verlag, 2009), 24–40, here: 34.", "[@scholz2009, s. 34].")],
 48: [("(Samīr Amīn, *Accumulation on a World Scale*: *A Critique of the Theory of Underdevelopment* [New York, NY: Monthly "
       "Review Press, 1974])", "([@amin1974])"),
      ("(Maria Mies, *Patriarchat und Kapital*: *Frauen in der internationalen Arbeitsteilung* [Zürich: Rotpunktverlag, 1988])",
       "([@mies1988])"),
      ("(Silvia Federici: *Caliban and the Witch. Women, the Body and Primitive Accumulation*. [New York, NY: Autonomedia, 2004])",
       "([@federici2004])")],
 50: [("Karl Marx, *Das Kapital*: *Kritik der politischen Ökonomie. Erster Band*. Karl Marx / Friedrich Engels: Werke 23 "
       "(Berlin: Dietz, 1962), 743 (hereafter", "[@marx1962, s. 743] (hereafter")],
 51: [("MEW 23, 746.", "[@marx1962, s. 746].")],
 52: [("MEW 23, 748–49.", "[@marx1962, s. 748–749].")],
 53: [("Karl Marx and Friedrich Engels, *Schriften 1845–1846*. Karl Marx / Friedrich Engels: Werke 3 (Berlin: Dietz, 1958), 56.",
       "[@marx1958, s. 56].")],
 54: [("See MEW 23, 761–62.", "Zob. [@marx1962, s. 761–762].")],
 55: [("MEW 23, 762.", "[@marx1962, s. 762].")],
 56: [("Karl Marx, *Ökonomische Manuskripte 1857/1858*. Karl Marx / Friedrich Engels: Werke 42 (Berlin: Dietz, 1983), 631.",
       "[@marx1983, s. 631].")],
 58: [("Thomas Edlyne Tomlins, *The Statutes at Large, of England and of Great-Britain*: *From Magna Carta to the Union of the "
       "Kingdoms of Great Britain and Ireland. In Twenty Volumes* (London: Printed by G. Eyre and A. Strahan, printers to the "
       "King, 1811), Vol. II. From 1 Ric. II A.D. 1377 – To 19 Hen. VII. A.D. 1507, 763–764.", "[@tomlins1811, s. 763–764].")],
 59: [("John Raithby, *The Statutes at Large, of England and of Great-Britain*: *From Magna Carta to the Union of the Kingdoms "
       "of Great Britain and Ireland. In Twenty Volumes* (London: Printed by G. Eyre and A. Strahan, printers to the King, "
       "1811), Vol. III. From 1 Hen. VIII. A.D. 1509–10. – To 7 Edw. VI. A.D. 1553, 91–92.", "[@raithby1811a, s. 91–92].")],
 60: [("MEW 23, 762.", "[@marx1962, s. 762].")],
 61: [("Raithby, *Statutes at large Vol. III*, 89.", "[@raithby1811a, {t. 3, s. 89}].")],
 62: [("David Mayall, *English Gypsies and State Policies* (Hertfordshire: Gypsy Research Centre Univ. of Hertfordshire Press, "
       "1995), 25.", "[@mayall1995, s. 25].")],
 63: [("David Mayall, *Gypsy Identities 1500–2000*: *From Egipcyans and Moon-Men to the Ethnic Romany* (London/New York: "
       "Routledge, 2004), 65–66; Mayall, *English Gypsies*, 18–26.", "[@mayall2004, s. 65–66; @mayall1995, s. 18–26].")],
 64: [("John Raithby, *The Statutes at Large, of England and of Great-Britain*: *From Magna Carta to the Union of the Kingdoms "
       "of Great Britain and Ireland. In Twenty Volumes* (London: Printed by G. Eyre and A. Strahan, printers to the King, "
       "1811), Vol. IV. From 1 Mary, A.D. 1553. – To 16 Charles I. A.D. 1640, 34.", "[@raithby1811b, s. 34].")],
 65: [("Mayall, *Gypsy Identities*, 79.", "[@mayall2004, s. 79]."),
      ("(Raithby, *Statutes at large Vol. IV*, 233)", "([@raithby1811b, {t. 4, s. 233}])")],
 66: [("MEW 23, 762.", "[@marx1962, s. 762].")],
 67: [("See MEW 23, 762–70.", "Zob. [@marx1962, s. 762–770].")],
 68: [("MEW 23, 764 (FN).", "[@marx1962, {s. 764, przyp.}].")],
 69: [("MEW 23, 746.", "[@marx1962, s. 746].")],
 70: [("Matthias Bohlender, “Der Malthus-Effekt: Vom Ethos der Aufklärung zur Geburt des Liberalismus,” in *Neustart des "
       "Weltlaufs? Fiktion und Faszination der Zeitwende*, ed. Karsten Fischer (Frankfurt am Main: Suhrkamp, 1999), 36–64, "
       "here: 44–45.", "[@bohlender1999, s. 44–45].")],
 71: [("See MEW 23, 663.", "Zob. [@marx1962, s. 663].")],
 72: [("MEW 23, 724.", "[@marx1962, s. 724].")],
 73: [("MEW 23, 711.", "[@marx1962, s. 711].")],
 74: [("MEW 23, 722.", "[@marx1962, s. 722].")],
 75: [("MEW 23, 723.", "[@marx1962, s. 723].")],
 76: [("MEW 23, 724.", "[@marx1962, s. 724].")],
 77: [("MEW 23, 724.", "[@marx1962, s. 724].")],
 78: [("MEW 23, 724–25.", "[@marx1962, s. 724–725].")],
 79: [("See Meuser, “Vagabunden und Arbeitsscheue.”", "Zob. [@meuser2014].")],
 80: [("Gustav Hermann Zeller and August Ludwig Reyscher, *Sammlung der württembergischen Regierungs-Gesetze*: *Erster Theil, "
       "enthaltend die Regierungs-Gesetze vom Jahre 1489 bis zum Jahre 1634*. Vollständige, historisch und kritisch bearbeitete "
       "Sammlung der württembergischen Gesetze Bd. 12 (Tübingen: Fues, 1841), 115, 767–768.", "[@zeller1841, s. 115, 767–768].")],
 81: [("Achim Landwehr, “Norm, Normalität, Anomale: Zur Konstitution von Mehrheit und Minderheit in württembergischen "
       "Polizeiordnungen der Frühen Neuzeit: Juden, Zigeuner, Bettler, Vaganten,” in *Minderheiten, Obrigkeit und Gesellschaft "
       "in der frühen Neuzeit: Integrations- und Abgrenzungsprozesse im süddeutschen Raum*, eds. Mark Häberlein and Martin Zürn "
       "(St. Katharinen: Scripta Mercaturae Verlag, 2001), 41–74, here: 61.", "[@landwehr2001, s. 61].")],
 82: [("Gustav Hermann Zeller and August Ludwig Reyscher, *Sammlung der württembergischen Regierungs-Gesetze*: *Zweiter Theil, "
       "enthaltend die Regierungs-Gesetze vom Jahre 1638 bis zum Jahre 1726*. Vollständige, historisch und kritisch bearbeitete "
       "Sammlung der württembergischen Gesetze Bd. 13 (Tübingen: Fues, 1842), 81 (my translation, as will be the following); "
       "see Landwehr, “Norm, Normalität, Anomale,” 61.",
       "[@zeller1842, s. 81] (my translation, as will be the following); zob. [@landwehr2001, s. 61].")],
 95: [("See Meuser, “Vagabunden und Arbeitsscheue.”", "Zob. [@meuser2014].")],
 96: [("Landwehr, “Norm, Normalität, Anomale,” 59 (my translation).", "[@landwehr2001, s. 59] (my translation).")],
 97: [("Matthias Reiss, “Zwischen Revolte und Resignation: Das Bild des Arbeitslosen seit dem 19. Jahrhundert,” in *Armut: "
       "Perspektiven in Kunst und Gesellschaft*, eds. Herbert Uerlings, Nina Trauth and Lukas Clemens (Darmstadt: Primus "
       "Verlag, 2011), 326–335, here: 327.", "[@reiss2011, s. 327].")],
 98: [("see Étienne Balibar, “Is There a ‘Neo-Racism’?” in *Race, Nation, Class: Ambiguous Identities*, eds. Étienne Balibar "
       "and Immanuel Wallerstein (London: Verso, 1991), 17–28.", "zob. [@balibar1991].")],
 99: [("See Anja Reuss, *Kontinuitäten der Stigmatisierung*: *Sinti und Roma in der deutschen Nachkriegszeit* (Berlin: "
       "Metropol, 2015).", "Zob. [@reuss2015].")],
 100: [("Hans Richard Brittnacher, *Leben auf der Grenze*: *Klischee und Faszination des Zigeunerbildes in Literatur und Kunst* "
        "(Göttingen: Wallstein Verlag, 2012); Frank Reuter, *Der Bann des Fremden*: *Die fotografische Konstruktion des "
        "Zigeuners* (Göttingen: Wallstein Verlag, 2014).", "[@brittnacher2012; @reuter2014].")],
 101: [("Tom Holert and Mark Terkessidis, *Fliehkraft*: *Gesellschaft in Bewegung - von Migranten und Touristen* (Köln: "
        "Kiepenheuer & Witsch, 2006).", "[@holert2006].")],
}
# the German originals quoted in notes 83–94 (Zeller and Reyscher, Bd. 13): the quotation stays, the citation is keyed
for n, pg in {83: "81", 84: "489", 85: "490", 86: "822", 87: "822", 88: "823", 89: "823", 90: "823", 91: "824", 92: "823",
              93: "823", 94: "824"}.items():
    K[n] = [(f"Zeller and Reyscher, *Sammlung Bd. 13*, {pg}.", f"[@zeller1842, s. {pg}].")]
LITERAL = {39: "prose", 49: "prose", 57: "prose (a gloss: 'Wooden boards restraining one’s feet')"}
PARTLY = {9: "prose about the lecture series", 18: "prose", 22: "prose (Büttner's 1771 book named in prose, no citation)",
          23: "prose; the digitised first edition's URL stays in the prose ('available online')",
          24: "prose", 27: "a quotation from Eberl", 38: "the German original quoted", 42: "prose", 48: "prose",
          50: "prose: '(hereafter abbreviated as MEW 23)' and the Marx Engels Archive URL (queries A4, C)",
          65: "a quotation from the 1562 act", 82: "the German original quoted", 96: "the German original quoted"}
PARTLY.update({n: "the German original quoted" for n in range(83, 95)})
out = pre
for n, pairs in K.items():
    m = re.search(rf"^\[\^{n}\]: (.*)$", out, re.M)
    body = m.group(1)
    for lit, keyed in pairs:
        assert body.count(lit) == 1, f"note {n}: literal not found once: {lit[:70]!r}"
        body = body.replace(lit, keyed)
        log.append(f"note {n}: {lit} -> {keyed}")
    out = out[:m.start(1)] + body + out[m.end(1):]
for n in range(2, 102):
    if n not in K:
        assert n in LITERAL, f"note {n}: neither keyed nor listed as literal"
        log.append(f"note {n}: literal — {LITERAL[n]}")
    elif n in PARTLY:
        log.append(f"note {n}: partly literal — {PARTLY[n]}")
# ---- 3. the author's abbreviation for MEW 23 has nothing to point to once keyed: flagged where it stands (queries A4)
C = [("(hereafter abbreviated as MEW 23).",
      "(hereafter abbreviated as MEW 23). <!-- DO SPRAWDZENIA (pytania A4): skrót MEW 23 nie jest używany w przypisach "
      "(krótka forma z refs.json); proponuję pominąć to zdanie w przekładzie -->")]
for a, b in C:
    assert out.count(a) == 1, a
    out = out.replace(a, b)
    log.append(f"text: comment added after {a!r}")
# ---- 4. labels = the numbers SROM prints (1–100): the title note takes no number, so the original's note n is label
# n − 1 here (key_log and T-item give the offset); the Word working copy numbers its footnotes the same way (lossless)
out = re.sub(r"\[\^(\d+)\]", lambda m: f"[^{int(m.group(1)) - 1}]", out)
assert re.findall(r"^\[\^(\d+)\]:", out, re.M) == [str(i) for i in range(1, 101)]
log.append("labels: renumbered 2–101 -> 1–100 in tittel_src.md (= SROM's printed numbers; the original's note = label + 1)")
open("tittel_src.md", "w", encoding="utf-8").write(out)
open("key_log.md", "w", encoding="utf-8").write("\n".join(log) + "\n")
print(f"keyed {len(K)} notes ({len(PARTLY)} partly literal), literal {100 - len(K)}; title note 1; log key_log.md")
