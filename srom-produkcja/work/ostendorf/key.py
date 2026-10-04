# Ostendorf, "Familiar Outsiders Abroad": ostendorf_pdf.md -> ostendorf_pre.md (the extraction; note labels are the
# printed numbers 1–62, no title note) -> ostendorf_src.md (citations keyed). Every change is logged to key_log.md;
# check.py --keyed pre src proves no page, note or work was lost.
#  1. Chicago full citations and the author's short forms ("Cressy, *Gypsies*, 5–10") -> [@key, s. N] (srom-md.md;
#     refs.py). Locators get the Polish labels (Kanon § 7.2): s., t. (volume: "5:365" -> the volume goes to refs.json
#     when it identifies the work cited, else {t. 1, s. 103}), przyp. ("103n24" -> {s. 103, przyp. 24}); abbreviated
#     ranges in full (§ 3.2). A journal article's own range, cited whole, goes to refs.json `page`.
#  2. Prose lead-ins ("For an English equivalent, see", "For some examples, see") stay: text to translate.
#  3. Archival units (notes 29, 30, 32) and single press issues (49, 50, 52, 53, 54, 59) stay literal (Kanon § 8.1,
#     § 8.3); the digitised manuscript in note 14 (a URL with no work to key) stays literal too.
import re

src = open("ostendorf_pdf.md", encoding="utf-8").read()
log = ["# key.py log — ostendorf", ""]
open("ostendorf_pre.md", "w", encoding="utf-8").write(src)
n_def = len(re.findall(r"^\[\^\d+\]:", src, re.M))
assert re.findall(r"^\[\^(\d+)\]:", src, re.M) == [str(i) for i in range(1, n_def + 1)], "labels not 1…n"
log.append(f"labels: 1–{n_def} = printed note numbers (no title note)")

UPP = "University of Pennsylvania Press"
K = {
 1: [("Margareta Matache, *The Permanence of Anti-Roma Racism:(Un)uttered Sentences* (Routledge, 2026); Lesia Pahulich, "
      "“Racialization of Roma, European Modernity, and the Entanglement of Empires,” *Critical Romani Studies* 8, no. 1 (2025): "
      "40–61, https://doi.org/10.29098/crs.v8i1.208; Jelena Savić, “Gadjo Supremacy and Gadjo Privileges,” Conference Paper "
      "presented at Critical Approaches to Romani Studies Conference, Södertörn University, 2022; Małgorzata Mirga-Tas and "
      "Margareta Matache, “Gadjoness: An Uncounted Shade of Whiteness,” *The Funambulist*, June 22, 2023; Noémie Ndiaye, "
      "“Black Roma: Afro-Romani Connections in Early Modern Drama (and Beyond),” *Renaissance Quarterly* 75, no. 4 (2022): "
      "1266–302, http://doi.org/10.1017/rqx.2022.332.",
      "[@matache2026; @pahulich2025; @savic2022; @mirgatas2023; @ndiaye2022].")],
 2: [("Klaus-Michael Bogdal, *Europe and the Roma: A History of Fascination and Fear*, trans. Jefferson Chase (Penguin, 2023).",
      "[@bogdal2023].")],
 3: [("Noémie Ndiaye, *Scripts of Blackness: Early Modern Performance Culture and the Making of Race* (University of "
      "Pennsylvania Press, 2022), 3–8; Natalia Molina, “The Power of Racial Scripts: What the History of Mexican Immigration "
      "to the United States Teaches Us about Relational Notions of Race,” *Latino Studies* 8, no. 2 (2010): 156–175, "
      "https://doi.org/10.1057/lst.2010.20; Natalia Molina, Daniel Martinez HoSang and Ramón A. Gutiérrez, eds., *Relational "
      "Formations of Race: Theory, Method, and Practice* (University of California Press, 2019); Laura Tabili, “Race Is a "
      "Relationship, and Not a Thing,” *Journal of Social History* 37, no. 1 (2003): 125–130, "
      "https://dx.doi.org/10.1353/jsh.2003.0162.",
      "[@ndiaye2022b, s. 3–8; @molina2010; @molina2019; @tabili2003].")],
 4: [("Patricia Galletti, “Los Gitanos como Otro y como Horizonte de Otredad en la Hispanoaméria Colonial (S. XV a XIX),” "
      "*International Journal of Roma Studies* 3, no. 2 (2021): 119, https://doi.org/10.17583/ijrs.8527.",
      "[@galletti2021, s. 119].")],
 5: [("Tamar Herzog, “Indigenous Reducciones and Spanish Resettlement: Placing Colonial and European History in Dialogue,” "
      "*Ler História* 72 (2018): 9–30, https://doi.org/10.4000/lerhistoria.3146; Tamar Herzog, “Beyond Race: Exclusion in "
      "Early Modern Spain and Spanish America,” in *Race and Blood in the Iberian World*, ed. Max S. Hering Torres, María "
      "Elena Martínez and David Nirenberg (LIT Verlag, 2012), 151–67.", "[@herzog2018; @herzog2012]."),
     ("David Cressy, *Gypsies: An English History* (Oxford University Press, 2018), 89.", "[@cressy2018, s. 89].")],
 6: [("Dalen Wakeley-Smith, “‘The One Primitive People Who Contact with Civilization has Failed to Exterminate’: New York and "
      "‘Gypsy’ Madness in the 1920s,” *Journal of American Ethnic History* 43, no. 1 (2023): 67–87, "
      "https://doi.org/10.5406/19364695.43.1.03; Jodie Matthews, *The Gypsy Woman: Representations in Literature and Visual "
      "Culture* (Bloomsbury, 2018); Sarah Houghton-Walker, *Representations of the Gypsy in the Romantic Period* (Oxford "
      "University Press, 2014); Deborah Epstein Nord, *Gypsies and the British Imagination, 1807–1930* (Columbia University "
      "Press, 2006); Lou Charnon-Deutsch, *The Spanish Gypsy: The History of a European Obsession* (Pennsylvania State "
      "University Press, 2004).",
      "[@wakeleysmith2023; @matthews2018; @houghtonwalker2014; @nord2006; @charnondeutsch2004].")],
 7: [("Kate Flint, *The Transatlantic Indian: 1776–1930* (Princeton University Press, 2009); Sherry L. Smith, *Reimagining "
      "Indians: Native Americans through Anglo Eyes, 1880–1940* (Oxford University Press, 2000); Philip J. Deloria, *Playing "
      "Indian* (Yale University Press, 1998).", "[@flint2009; @smith2000; @deloria1998].")],
 8: [("Alejandro de la Fuente and Ariela J. Gross, *Becoming Free, Becoming Black: Race, Freedom, and Law in Cuba, Virginia, "
      "and Louisiana* (Cambridge University Press, 2020); Rana A. Hogarth, *Medicalizing Blackness: Making Racial Difference "
      "in the Atlantic World, 1780–1840* (University of North Carolina Press, 2017)*;* Ibram X. Kendi, *Stamped from the "
      "Beginning: The Definitive History of Racist Ideas in America* (Nation, 2016).",
      "[@delafuente2020; @hogarth2017; @kendi2016].")],
 9: [("Cressy, *Gypsies*, 5–10.", "[@cressy2018, s. 5–10].")],
 10: [("Katie Trumpener, “The Time of the Gypsies: A ‘People without History’ in the Narratives of the West,” *Critical "
       "Inquiry* 18, no. 4 (1992): 843–84, https://doi.org/10.1086/448659.", "[@trumpener1992].")],
 11: [("Donald Weinstein, *Ambassador from Venice: Pietro Pasqualigo in Lisbon, 1501* (University of Minnesota Press, 1960), "
       "73, 103n24; *A Memoir of Sebastian Cabot; with a Review of the History of Maritime Discovery* (Philadelphia, 1831), "
       "236; *The Journal of Christopher Columbus*, trans. Clements R. Markham (London, 1893), 235–38.",
       "[@weinstein1960, {s. 73, 103, przyp. 24}; @memoircabot1831, s. 236; @columbus1893, s. 235–238]."),
      ("George C. Soulis, “The Gypsies in the Byzantine Empire and the Balkans in the Late Middle Ages,” *Dumbarton Oaks "
       "Papers* 15 (1961): 152.", "[@soulis1961, s. 152]."),
      ("see Francisco Mangas, “A Outra Minoria: Uma história dos Ciganos portugueses durante a Época Moderna” (PhD diss., "
       "University of Porto, 2024), 55–56, 68, 229–30.", "see [@mangas2024, s. 55–56, 68, 229–230].")],
 12: [("Sebastiano Beretario, *Iosephi Anchietae Societatis Iesv Sacerdotis in Brasilia Defvncti Vita* (1617), 39;",
       "[@beretario1617, s. 39];"),
      ("A Gentleman of Elvas, *The True Relation of the Hardships Suffered by Governor Hernando de Soto*, trans. and ed. James "
       "Robertson (Florida State Historical Society, 1932), 118.", "[@elvas1932, s. 118].")],
 13: [("Gabriel Martínez-Serna, “Procurators and the Making of the Jesuits’ Atlantic Network,” in *Soundings in Atlantic "
       "History: Latent Structures and Intellectual Currents, 1530–1830*, ed. Bernard Bailyn and Patricia L. Denault (Harvard "
       "University Press, 2009), 196.", "[@martinezserna2009, s. 196].")],
 14: [("Ulrico Schmidl, *Derrotero y viaje a España y las Indias, 1534–1554*, trans. Edmundo Wernicke (Universidad Nacional "
       "de Litoral, 1938), 44.", "[@schmidl1938, s. 44].")],
 15: [("*Actas da Camara da Villa de S. Paulo, 1640–1652* (Archivo Municipal, 1915), 5:365; John M. Monteiro, *Blacks of the "
       "Land: Indian Slavery, Settler Society, and the Portuguese Colonial Enterprise in South America*, trans. and ed. James "
       "Woodard and Barbara Weinstein (Cambridge University Press, 2018), 98; Martin Fotta, “The Figure of the Gypsy "
       "(*Cigano*) as a Signpost for Crises of the Social Hierarchy (Bahia, 1590s– 1900s),” *International Review of Social "
       "History* 65, no. 2 (2019): 8–10, https://doi.org/10.1017/S0020859019000713.",
       "[@actas1915, s. 365; @monteiro2018, s. 98; @fotta2019, s. 8–10].")],
 16: [("Tamar Herzog, *Defining Nations: Immigrants and Citizens in Early Modern Spain and Spanish America* (Yale University "
       "Press, 2003), 129, 249n36.", "[@herzog2003, {s. 129, 249, przyp. 36}].")],
 17: [("Antonio Gómez Alfaro, Elisa Maria Lopes da Costa and Sharon Sillers Floate, *Deportaciones de Gitanos* (Centre de "
       "recherches tsiganes, 1999), 19.", "[@gomezalfaro1999, s. 19].")],
 18: [("Gómez Alfaro, et al., *Deportaciones de Gitanos*, 27–33; Antonio Gómez Alfaro, *The Great Gypsy Round-Up: Spain, the "
       "General Imprisonment of Gypsies in 1749* (University of Hertfordshire Press, 1993).",
       "[@gomezalfaro1999, s. 27–33; @gomezalfaro1993].")],
 19: [("William O’Reilly, “*Divide et impera*: Race, Ethnicity, and Administration in Early 18th-Century Habsburg Hungary,” in "
       "*Racial Discrimination and Ethnicity in European History*, ed. Gudmundur Hálfdánarson and Anne Katherine Isaacs "
       "(Edizioni Plus, 2003): 77–100.", "[@oreilly2003].")],
 20: [("Gómez Alfaro, et al., *Deportaciones de Gitanos*, 30.", "[@gomezalfaro1999, s. 30].")],
 21: [("Herzog, *Defining Nations*, 133.", "[@herzog2003, s. 133].")],
 22: [("Herzog, *Defining Nations*, 133; Gómez Alfaro, et al., *Deportaciones de Gitanos*, 30; Richard Pym, *The Gypsies of "
       "Early Modern Spain* (Palgrave Macmillan, 2007), 145–47.",
       "[@herzog2003, s. 133; @gomezalfaro1999, s. 30; @pym2007, s. 145–147].")],
 23: [("Florian Paucke, *Zwettler Codex 420*, ed. Etta Becker-Donner (Wilhelm Braumuller University, 1959), I:183, 239, 303 "
       "and II:452.", "[@paucke1959, {t. 1, s. 183, 239, 303 i t. 2, s. 452}].")],
 24: [("Galletti, “Los Gitanos como Otro,” 121–22; Cynthia Radding, *Wandering Peoples: Colonialism, Ethnic Spaces, and "
       "Ecological Frontiers in Northwestern Mexico, 1700–1850* (Duke University Press, 1997), 148.",
       "[@galletti2021, s. 121–122; @radding1997, s. 148].")],
 25: [("Manuel Moreno Alonso, “De Cadiz a Veracruz en 1745,” *Historiografía y bibliografía Americanistas* 27 (1983): 18, 32; "
       "Francisco A. Scarano, “The Jíbaro Masquerade and the Subaltern Politics of Creole Identity Formation in Puerto Rico, "
       "1745–1823,” *American Historical Review* 101, no. 5 (1996): 1415, https://doi.org/10.2307/2170177.",
       "[@morenoalonso1983, s. 18, 32; @scarano1996, s. 1415].")],
 26: [("“Lettre au P.re Paul du Poisson; aux Akensas, October 3, 1727,” in *The Jesuit Relations and Allied Documents*, ed. "
       "Reuben Gold Thwaites (Cleveland, 1900), 67:314–15.", "[@poisson1900, s. 314–315].")],
 27: [("Pierre-Louis Berquin-Duvallon, *Vue de la colonie Espagnole du Mississipi, ou des provinces de Louisiane et Floride "
       "Occidentale,en l’année 1802* (Paris, 1803), 32.", "[@berquinduvallon1803, s. 32].")],
 28: [("Ann Ostendorf, “Louisiana Bohémiens: Community, Race, and Empire,” *Early American Studies: An Interdisciplinary "
       "Journal* 19, no. 4 (2021): 686, https://doi.org/10.1353/eam.2021.0021; Ann Ostendorf, “Racializing American "
       "‘Egyptians’: Shifting Legal Discourse, 1690s–1860s,” *Critical Romani Studies* 2, no. 2 (2019): 42–59 "
       "https://doi.org/10.29098/crs.v2i2.50.", "[@ostendorf2021, s. 686; @ostendorf2019].")],
 30: [("Ostendorf, “Louisiana Bohémiens,” 681–83; Ann Laura Stoler, *Carnal Knowledge: Race and the Intimate in Colonial "
       "Rule* (University of California Press, 2002), 76.", "[@ostendorf2021, s. 681–683; @stoler2002, s. 76].")],
 31: [("Louis LeClerc Milfort, *Mémoire; ou Coup-d’Oeil Rapide Sur mes Différens Voyages et mon séjour dans la nation Crëck* "
       "(Paris, 1802), 57.", "[@milfort1802, s. 57].")],
 33: [("Ann Ostendorf, “‘To Get Himself Out of Slavery’: Escape, Justice, and Honor in the Life of a Colonial French Louisiana "
       "Bohemian (Gypsy),” *Frühneuzeit-Info* 31 (2020): 140–56.", "[@ostendorf2020].")],
 34: [("*A Relation or Journall of the beginning and proceedings of the English* (John Bellamie, 1622), 34; *Mourt’s "
       "Relation, or Journal of the Plantation at Plymouth, 1622*, ed. Henry Dexter (Boston, 1865), 88.",
       "[@relation1622, s. 34; @mourt1865, s. 88].")],
 35: [("William Penn, “A Letter from William Penn, Proprietary and Governor of Pennsylvania in America, to the Committee of the "
       "Free Society of Traders, 1683,” in *Narratives of Early Pennsylvania, West New Jersey, and Delaware, 1630–1707*, ed. "
       "Albert Cook Myers (New York, 1912), 230.", "[@penn1912, s. 230].")],
 36: [("Cressy, *Gypsies*, 39–53, 75–77; Dan Cunniffe, “Pretending and Performing Gypsy Identity in Early Modern England, "
       "*c.* 1607–1623” (PhD diss., King’s College London, 2023).", "[@cressy2018, s. 39–53, 75–77; @cunniffe2023].")],
 37: [("Frederick Stone, “A Vindication of William Penn,” *The Pennsylvania Magazine of History and Biography* 6, no. 2 "
       "(1882): 180.", "[@stone1882, s. 180].")],
 38: [("Georg Heinrich Loskiel, *Geschichte der Mission der Evangelischen Brüder unter den Indianern in Nordamerika* (1789), "
       "167; George Henry Loskiel, *History of the Mission of the United Brethren among the Indians in North America*, trans. "
       "Christian La Trobe (London, 1794), 130.", "[@loskiel1789, s. 167; @loskiel1794, s. 130].")],
 39: [("Cressy, *Gypsies*, 53.", "[@cressy2018, s. 53].")],
 40: [("Anonymous, *The Jamaica Lady* (London, 1720), 8, 9, 85.", "[@jamaicalady1720, s. 8, 9, 85].")],
 41: [("Klaus G. Loewald, Beverly Starika and Paul S. Taylor, trans. and eds., “Johann Martin Bolzius Answers a Questionnaire "
       "on Carolina and Georgia, Part I,” *The William and Mary Quarterly* 14, no. 2 (1957): 220, "
       "https://doi.org/10.2307/1922111; Klaus G. Loewald, Beverly Starika and Paul S. Taylor, trans. and eds., “Johann Martin "
       "Bolzius Answers a Questionnaire on Carolina and Georgia, Part II,” *The William and Mary Quarterly* 15, no. 2 (1958): "
       "245, https://doi.org/10.2307/1919443; Samuel Urlsperger, ed., *Der ausführlichen nachrichten von der "
       "königlich-gross-britannischen colonie saltzburgischer emigranten in America erster* (Halle, 1751), 3:979, University "
       "of Pennsylvania Library Special Collections.",
       "[@loewald1957, s. 220; @loewald1958, s. 245; @urlsperger1751, {t. 3, s. 979}].")],
 42: [("*The Journals of Henry Melchior Muhlenberg*, trans. Theodore G. Tappert and John W. Doberstein (Muhlenberg Press, "
       "1945), 2:638.", "[@muhlenberg1945, {t. 2, s. 638}].")],
 43: [("Ann Ostendorf, “Contextualizing American Gypsies: Experiencing Criminality in the Colonial Chesapeake,” *Maryland "
       "Historical Magazine* 113 (2018): 192–222; Sharon Block, *Colonial Complexions: Race and Bodies in Eighteenth Century "
       "America* (University of Pennsylvania Press, 2021), 103–07.", "[@ostendorf2018; @block2021, s. 103–107].")],
 44: [("George Webb, *Office and Authority of a Justice of Peace* (Williamsburg, 1736), 349; St. George Tucker, *Blackstone’s "
       "Commentaries: With Notes of Reference to the Constitution and Laws of the Federal Government of the United States and "
       "the Commonwealth of Virginia* (Philadelphia, 1803), 33, 165–66.", "[@webb1736, s. 349; @tucker1803, s. 33, 165–166].")],
 45: [("Emily B. Todd, “Establishing Routes for Fiction in the United States: Walter Scott’s Novels and the Early "
       "Nineteenth-Century American Publishing Industry,” *Book History* 12 (2009): 102, https://dx.doi.org/10.1353/bh.0.0016.",
       "[@todd2009, s. 102].")],
 46: [("Andrew Cayton, “The Authority of the Imagination in an Age of Wonder,” *Journal of the Early Republic* 33, no. 1 "
       "(2013): 24, https://dx.doi.org/10.1353/jer.2013.0009.", "[@cayton2013, s. 24].")],
 47: [("Walter Scott, *Guy Mannering; Or, the Astrologer* (Edinburgh, 1815), 1:103.", "[@scott1815, {t. 1, s. 103}].")],
 48: [("Barbara Hofland, *The Stolen Boy, an Indian Tale* (New York, 1830), 7; Katie Trumpener, *Bardic Nationalism: The "
       "Romantic Novel and the British Empire* (Princeton University Press, 1997), 346n50.",
       "[@hofland1830, s. 7; @trumpener1997, {s. 346, przyp. 50}].")],
 51: [("*The Life and Writings of De Witt Clinton*, ed. William Cambell (New York, 1849), 196.", "[@clinton1849, s. 196].")],
 55: [("Mary Louise Pratt, *Imperial Eyes: Travel Writing and Transculturation* (Routledge, 1992), 5.", "[@pratt1992, s. 5].")],
 56: [("Jennifer L. Morgan, *Laboring Women: Reproduction and Gender in New World Slavery* (University of Pennsylvania Press, "
       "2004), 49.", "[@morgan2004, s. 49].")],
 57: [("Dorothy Wollon and Margaret Kinard, “Notes and Documents: Sir Augustus J. Foster and ‘the Wild Natives of the Woods,’ "
       "1805–1807,” *The William and Mary Quarterly* 9, no. 2 (1952): 206, https://doi.org/10.2307/1925349.",
       "[@wollon1952, s. 206].")],
 58: [("John Lambert, *Travels through Canada, and the United States of North America, in the Years 1806, 1807, & 1808* "
       "(London, 1813), 1: iv, 358.", "[@lambert1813, {t. 1, s. iv, 358}].")],
 60: [("Richard Longeville Vowell, *Campaigns and Cruises in Venezuela and New Granada* (London, 1831), 2: 324.",
       "[@vowell1831, {t. 2, s. 324}].")],
 61: [("Godfrey Vigne, *Six Months in America* (Philadelphia, 1833), 148.", "[@vigne1833, s. 148].")],
 62: [("Alistair Robinson, *Vagrancy in the Victorian Age: Representing the Wandering Poor in Nineteenth-Century Literature and "
       "Culture* (Cambridge University Press, 2021), 37.", "[@robinson2021, s. 37].")],
}
LITERAL = {14: "digitised manuscript (URL, no work)", 29: "archival (AGI)", 32: "archival (Huntington Library)",
           49: "press", 50: "press", 52: "press", 53: "press", 54: "press", 59: "press",
           30: "archival (St. Louis Cathedral); the other citations keyed"}
out = src
for n, pairs in K.items():
    m = re.search(rf"^\[\^{n}\]: (.*)$", out, re.M)
    body = m.group(1)
    for lit, keyed in pairs:
        assert body.count(lit) == 1, f"note {n}: literal not found once: {lit[:60]!r}"
        body = body.replace(lit, keyed)
        log.append(f"note {n}: {lit} -> {keyed}")
    out = out[:m.start(1)] + body + out[m.end(1):]
for n in range(1, n_def + 1):
    if n not in K:
        why = LITERAL.get(n)
        assert why, f"note {n}: neither keyed nor listed as literal"
        log.append(f"note {n}: literal — {why}")
    elif n in LITERAL:
        log.append(f"note {n}: partly literal — {LITERAL[n]}")
# ---- 4. discrepancies between text and notes: kept as printed, flagged where they stand (queries D1, D2)
C = [("during his 1747 journey between Cadiz and Veracruz",
      "during his 1747 journey between Cadiz and Veracruz <!-- DO SPRAWDZENIA (pytania D1): przypis 25 cytuje "
      "„De Cadiz a Veracruz en 1745” – 1747 czy 1745? Manuel Moreno Alonso to autor artykułu z 1983 r.; "
      "czyja to podróż (wydany diariusz)? -->"),
     ("similarly noted in a 1686 promotional tract distributed throughout England,",
      "similarly noted in a 1686 promotional tract distributed throughout England, <!-- DO SPRAWDZENIA (pytania D2): "
      "przypis 35 cytuje list Penna z 1683 r. – 1686 czy 1683? -->")]
for a, b in C:
    assert out.count(a) == 1, a
    out = out.replace(a, b)
    log.append(f"text: comment added after {a!r}")
open("ostendorf_src.md", "w", encoding="utf-8").write(out)
open("key_log.md", "w", encoding="utf-8").write("\n".join(log) + "\n")
print(f"keyed {len(K)} notes (2 of them partly literal), literal {n_def - len(K)}; log key_log.md")
