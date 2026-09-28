"""G8: cite_map resolves unique author-date references (parenthetical, narrative, in-note, inflected,
multi, et al., editor, letter suffix, page-only), refuses ambiguous/unknown, and the converted article
builds cleanly. audit catches transcription errors in refs.json against the original bibliography."""
import os, sys, subprocess, tempfile, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures")
CM = os.path.join(ROOT, "scripts", "cite_map.py")
REFS = os.path.join(FX, "citemap_refs.json")
d = tempfile.mkdtemp()
res = []

def t(name, ok, out=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n" + str(out)[:3000]))

def cm(*args):
    r = subprocess.run([sys.executable, CM, *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

src = os.path.join(FX, "authordate_article.md")
out_md = os.path.join(d, "conv.md")
c, o = cm("scan", src, "--refs", REFS, "--apply", out_md, "--report", os.path.join(d, "r.md"))
t("scan + apply succeeds; page-only '(s. 21)' converted and listed, not blocking", c == 0 and os.path.exists(out_md) and "PAGE-ONLY" in o, o)
conv = open(out_md, encoding="utf-8").read() if os.path.exists(out_md) else ""
print(conv)
t("parenthetical after abbreviation: 'XV w.[^c1] ' (abbrev. period ends sentence)", "z XV w.[^c1] Ficowski" in conv, conv)
t("…note c1 = ficowski s. 15", "[^c1]: [@ficowski1985, s. 15]." in conv, conv)
t("narrative keeps name, marker after it", "Ficowski[^c2] twierdzi" in conv and "[^c2]: [@ficowski1985, s. 17–19]." in conv, conv)
t("page-only after quote inherits the work cited before it: marker after closing quote", "podwójna”[^c3]." in conv and "[^c3]: [@ficowski1985, s. 21]." in conv, conv)
t("inflected narrative 'Mroza' -> mroz2011", "Mroza[^c4]" in conv and "[@mroz2011, s. 90]" in conv, conv)
t("multi-item with prefix, ff. -> i n., capitalised Zob.", "[Zob. @kolaczek2012, s. 215 i n.; @hancock2007]." in conv, conv)
t("editor '(red.)' form -> kowalski2011", "[@kowalski2011]" in conv, conv)
t("et al. + table locator in braces", "[@fialkowska2020, {tabl. 3}]" in conv, conv)
t("letter suffix a/b via citation-label", "[@nowak2010]" in conv and "[@nowak2010b, s. 7]" in conv, conv)
t("in-note narrative + bare two-author cite converted", "[^1]: Szerzej o tym [@mroz2011, s. 92]; [zob. też @mroz1998, s. 40]." in conv, conv)
t("'Kraków 1985' in a note and '1939–1945 (okupacja)' untouched", "Wydanie: Kraków 1985." in conv and "Okres 1939–1945 (okupacja) nie jest cytatem." in conv, conv)
c2, o2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check.py"), out_md, "--refs", REFS], capture_output=True, text=True).returncode, ""
t("converted file passes check.py", c2 == 0)
b = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), out_md, "--refs", REFS, "--out", os.path.join(d, "b")], capture_output=True, text=True)
rep = open(os.path.join(d, "b", "conv_report.md"), encoding="utf-8").read()
t("converted file builds (PASS)", b.returncode == 0, rep[:2500])

amb2 = os.path.join(d, "red.md"); open(amb2, "w", encoding="utf-8").write("Tekst (Kowalski (red.) 2011: 5) i (Zob. Nowak, Kowalski i Mróz (red.) 1999).\n")
c, o = cm("scan", amb2, "--refs", REFS, "--report", os.path.join(d, "red_r.md"))
rr = open(os.path.join(d, "red_r.md"), encoding="utf-8").read()
t("nested '(red.)' parenthetical resolved to kowalski2011", "`(Kowalski (red.) 2011: 5)` | **OK** | kowalski2011" in rr, rr)
t("unresolvable nested one reported once, blocks", c == 1 and o.count("Nowak, Kowalski i Mróz") == 1, o)
amb = os.path.join(d, "amb.md"); open(amb, "w", encoding="utf-8").write("Tekst (Lee 2005: 3) i (Zieliński 1999).\n")
c, o = cm("scan", amb, "--refs", REFS, "--apply", os.path.join(d, "amb_out.md"))
t("ambiguous (two Lee 2005) and unknown author refuse to apply", c == 1 and "AMBIGUOUS" in o and "UNKNOWN" in o and not os.path.exists(os.path.join(d, "amb_out.md")), o)

hist = os.path.join(d, "hist.md"); open(hist, "w", encoding="utf-8").write("Urodził się w Tarnowie (1951), a pokój podpisano (Ryga 1921). Ficowski (1985: 5) pisał.\n")
c, o = cm("scan", hist, "--refs", REFS, "--apply", os.path.join(d, "hist_out.md"))
t("'Tarnowie (1951)' NOT-CITED? (non-blocking); '(Ryga 1921)' UNKNOWN blocks", c == 1 and "NOT-CITED?" in o and "UNKNOWN" in o, o)
c, o = cm("scan", hist, "--refs", REFS, "--apply", os.path.join(d, "hist_out.md"), "--allow-unknown")
ho = open(os.path.join(d, "hist_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "hist_out.md")) else ""
t("--allow-unknown: non-citations left verbatim, the real citation converted", c == 0 and "w Tarnowie (1951)" in ho and "(Ryga 1921)" in ho and "Ficowski[^c1] pisał" in ho, o + ho)

# ---- audit: original bibliography vs refs.json
bib = os.path.join(d, "bib.txt")
open(bib, "w", encoding="utf-8").write(
    "Ficowski, Jerzy (1985). Cyganie na polskich drogach. Kraków: Wydawnictwo Literackie.\n"
    "Kołaczek, Małgorzata (2012). Tytuł artykułu. Studia Romologica 5: 211–228. https://doi.org/10.1234/srom.2012.5.11\n")
sub = os.path.join(d, "sub.json")
refs = json.load(open(REFS, encoding="utf-8"))
json.dump([r for r in refs if r["id"] in ("ficowski1985", "kolaczek2012")], open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: faithful refs pass", c == 0 and "CITEMAP OK" in o, o)
bad = [dict(r) for r in json.load(open(sub))]
for r in bad:
    if r["id"] == "kolaczek2012": r["page"] = "211-218"
    if r["id"] == "ficowski1985": r["publisher"] = "Czytelnik"
json.dump(bad, open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: wrong page range and wrong publisher caught", c == 1 and "kolaczek2012" in o and "228" in o and "ficowski1985" in o and "literackie" in o, o)
json.dump([r for r in refs if r["id"] == "ficowski1985"], open(sub, "w"), ensure_ascii=False)
c, o = cm("audit", "--refs", sub, "--bib", bib)
t("audit: original entry with no ref caught", c == 1 and "not mapped to exactly one ref" in o, o)

# ---- audit, English (Chicago) reference list: names of more than one word, literal author, abbreviated ranges,
# volume labels, month names (stage-1 test on a journal PDF, 27.09.2026)
ebib = os.path.join(d, "ebib.txt")
open(ebib, "w", encoding="utf-8").write(
    "Touam Bona, Dénètem. Fugitif, où cours-tu? Paris: Presses Universitaires de France, 2016.\n"
    "Van Lannep, William, ed. The London Stage. Carbondale: Southern Illinois University Press, 1965.\n"
    "M. W., M. A. A comedy called The marriage broaker. London: Printer, 1662.\n"
    "McKee, Sally. “Domestic Slavery in Renaissance Italy.” Slavery and Abolition 29.3 (2008): 305–26.\n"
    "Plésiat, Mathieu. Les Tsiganes; Tome 2. Paris: L’Harmattan, 2010.\n"
    "Matache, Margareta. “Roma Share a Common Struggle.” Guardian, 20 February 2018.\n")
eref = [
    {"id": "touambona2016", "type": "book", "author": [{"family": "Touam Bona", "given": "Dénètem"}], "title": "Fugitif, où cours-tu?",
     "publisher": "Presses Universitaires de France", "publisher-place": "Paris", "issued": {"date-parts": [[2016]]}},
    {"id": "vanlannep1965", "type": "book", "editor": [{"family": "Van Lannep", "given": "William"}], "title": "The London Stage",
     "publisher": "Southern Illinois University Press", "publisher-place": "Carbondale", "issued": {"date-parts": [[1965]]}},
    {"id": "mw1662", "type": "book", "author": [{"literal": "M. W., M. A."}], "title": "A comedy called The marriage broaker",
     "publisher": "Printer", "publisher-place": "London", "issued": {"date-parts": [[1662]]}},
    {"id": "mckee2008", "type": "article-journal", "author": [{"family": "McKee", "given": "Sally"}], "title": "Domestic Slavery in Renaissance Italy",
     "container-title": "Slavery and Abolition", "volume": "29", "issue": "3", "page": "305–326", "issued": {"date-parts": [[2008]]}},
    {"id": "plesiat2010", "type": "book", "author": [{"family": "Plésiat", "given": "Mathieu"}], "title": "Les Tsiganes", "volume": "2",
     "publisher": "L’Harmattan", "publisher-place": "Paris", "issued": {"date-parts": [[2010]]}},
    {"id": "matache2018", "type": "article-newspaper", "author": [{"family": "Matache", "given": "Margareta"}],
     "title": "Roma Share a Common Struggle", "container-title": "Guardian", "issued": {"date-parts": [[2018, 2, 20]]}}]
esub = os.path.join(d, "esub.json"); json.dump(eref, open(esub, "w", encoding="utf-8"), ensure_ascii=False)
c, o = cm("audit", "--refs", esub, "--bib", ebib)
t("audit, English list: Touam Bona, Van Lannep, literal M. W., 305–26 = 305–326, Tome = t., February = 2 -> OK", c == 0 and "CITEMAP OK" in o, o)
eref[1]["editor"][0]["family"] = "Van Lennep"; eref[1]["srom-as-written"] = {"editor": "Van Lannep"}
json.dump(eref, open(esub, "w", encoding="utf-8"), ensure_ascii=False)
c, o = cm("audit", "--refs", esub, "--bib", ebib)
t("audit: approved correction (Van Lannep -> Van Lennep, srom-as-written) still matches the author's list", c == 0 and "CITEMAP OK" in o, o)
eref[3]["page"] = "305–316"
json.dump(eref, open(esub, "w", encoding="utf-8"), ensure_ascii=False)
c, o = cm("audit", "--refs", esub, "--bib", ebib)
t("audit, English list: wrong end of an abbreviated range (305–26 vs 305–316) caught", c == 1 and "mckee2008" in o and "326" in o, o)

# ---- audit: a list ripped from a PDF with decomposed accents; "Translated by" (stage-1 test 28.09.2026, Pahulich)
nbib = os.path.join(d, "nbib.txt")
open(nbib, "w", encoding="utf-8").write(
    "Horva\u0301thova\u0301, Emilia. 1964. Cigа\u0301ni na Slovensku. Bratislava: SAV.\n".replace("Cigа", "Ciga")
    + "Willems, Wim. 1997. In Search of the True Gypsy. Translated by Don Bloch. London: F. Cass.\n")
nref = [
    {"id": "horvathova1964", "type": "book", "author": [{"family": "Horváthová", "given": "Emilia"}], "title": "Cigáni na Slovensku",
     "publisher": "SAV", "publisher-place": "Bratislava", "issued": {"date-parts": [[1964]]}},
    {"id": "willems1997", "type": "book", "author": [{"family": "Willems", "given": "Wim"}], "title": "In Search of the True Gypsy",
     "translator": [{"family": "Bloch", "given": "Don"}], "publisher": "F. Cass", "publisher-place": "London", "issued": {"date-parts": [[1997]]}}]
nsub = os.path.join(d, "nsub.json"); json.dump(nref, open(nsub, "w", encoding="utf-8"), ensure_ascii=False)
c, o = cm("audit", "--refs", nsub, "--bib", nbib)
t("audit: decomposed accents (a + U+0301) match the composed refs; 'Translated by' is a label", c == 0 and "CITEMAP OK" in o, o)

qi = os.path.join(d, "qi.md"); open(qi, "w", encoding="utf-8").write("Zdanie (quoted in Ficowski 1985: 3).\n")
c, o = cm("scan", qi, "--refs", REFS, "--apply", os.path.join(d, "qi_out.md"))
qo = open(os.path.join(d, "qi_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "qi_out.md")) else o
t("lead-in 'quoted in' -> 'cyt. za' (Kanon § 7.2)", "Cyt. za @ficowski1985, s. 3" in qo, qo)

po = os.path.join(d, "po.md"); open(po, "w", encoding="utf-8").write("Pierwszy akapit (s. 4).\n\nDrugi (Ficowski 1985: 3).\n\nTrzeci akapit (s. 9).\n")
c, o = cm("scan", po, "--refs", REFS, "--apply", os.path.join(d, "po_out.md"))
t("page-only with no earlier citation blocks; later one follows the previous paragraph's work", c == 1 and "PAGE-ONLY?" in o and "['ficowski1985']" in o, o)

# E2: the translator's added refs are not matched against the author's list, but need a source
json.dump([r for r in refs if r["id"] == "ficowski1985"], open(sub, "w"), ensure_ascii=False)
tlr = os.path.join(d, "tl.json")
json.dump([{"id": "ficowski1985pl", "type": "book", "author": [{"family": "Ficowski"}], "title": "X", "srom-added": "tlum"}], open(tlr, "w"))
bib1 = os.path.join(d, "bib1.txt"); open(bib1, "w", encoding="utf-8").write(open(bib, encoding="utf-8").read().splitlines()[0] + "\n")
c, o = cm("audit", "--refs", sub, "--refs", tlr, "--bib", bib1)
t("E2: srom-added entry without srom-source -> PROBLEM; not treated as a missing original", c == 1 and "no srom-source" in o and "no matching original entry" not in o, o)
json.dump([{"id": "ficowski1985pl", "type": "book", "author": [{"family": "Ficowski"}], "title": "X", "srom-added": "tlum", "srom-source": "ISBN 978-83-0"}], open(tlr, "w"))
c, o = cm("audit", "--refs", sub, "--refs", tlr, "--bib", bib1)
t("E2: srom-added entry with a source passes the audit", c == 0, o)

# ---- English author-date prose (stage-1 test 28.09.2026, Pahulich): possessive, first name ending in a particle,
# comma before the name, year without a name, block quotation, transliterated name kept as the author wrote it
eref2 = [
    {"id": "robinson2000", "type": "book", "author": [{"family": "Robinson", "given": "Cedric J."}], "title": "Black Marxism", "issued": {"date-parts": [[2000]]}},
    {"id": "melamed2015", "type": "article-journal", "author": [{"family": "Melamed", "given": "Jodi"}], "title": "Racial Capitalism", "issued": {"date-parts": [[2015]]}},
    {"id": "grellmann1807", "type": "book", "author": [{"family": "Grellmann", "given": "H.M.G."}], "title": "Dissertation", "issued": {"date-parts": [[1807]]}},
    {"id": "law2018", "type": "book", "author": [{"family": "Law", "given": "Ian"}, {"family": "Kovats", "given": "Martin"}], "title": "Rethinking Roma", "issued": {"date-parts": [[2018]]}},
    {"id": "law2012", "type": "book", "author": [{"family": "Law", "given": "Ian"}], "title": "Red Racisms", "issued": {"date-parts": [[2012]]}},
    {"id": "hancock2008", "type": "chapter", "author": [{"family": "Hancock", "given": "Ian"}], "title": "Stereotype", "issued": {"date-parts": [[2008]]}},
    {"id": "bielikov2003", "type": "thesis", "author": [{"family": "Bielikov", "given": "Oleksandr"}], "title": "Tsyhansʹke naselennia",
     "issued": {"date-parts": [[2003]]}, "srom-as-written": {"author": "Byelikov"}},
    {"id": "kirei1984", "type": "chapter", "author": [{"family": "Kireĭ", "given": "N.I."}, {"family": "Serdiuk", "given": "A.O."}], "title": "Izuchenie",
     "editor": [{"family": "Kireĭ", "given": "N.I."}], "issued": {"date-parts": [[1984]]}, "srom-as-written": {"author": "Kirey; Serdyuk", "editor": "Kirey"}}]
esub2 = os.path.join(d, "esub2.json"); json.dump(eref2, open(esub2, "w", encoding="utf-8"), ensure_ascii=False)
eng = os.path.join(d, "eng.md")
open(eng, "w", encoding="utf-8").write(
    "These histories support Cedric Robinson’s (2000) argument. As Jodi Melamed (2015) notes, it is so.\n\n"
    "Claiming to produce the first work about Roma, Grellmann (1807) synthesized it. Ian Law and Martin Kovats state that it began "
    "as early as 1422 (2018, 78). Münster wrote *Cosmographia* (1544).\n\n"
    "Romani scholar Ian Hancock asserts:\n\n> […] the need to categorize the plants (2008, 183).\n\n"
    "Settled lives (Byelikov 2003, 87; Kirey and Serdyuk 1984, 113–114).\n")
c, o = cm("scan", eng, "--refs", esub2, "--apply", os.path.join(d, "eng_out.md"))
eo = open(os.path.join(d, "eng_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "eng_out.md")) else ""
t("possessive: Robinson’s (2000) -> Robinson’s[^c1]", "Robinson’s[^c1] argument" in eo and "[^c1]: [@robinson2000]." in eo, o + eo)
t("'Jodi Melamed (2015)': 'di' inside a first name is no particle", "Jodi Melamed[^c2] notes" in eo and "[@melamed2015]" in eo, o + eo)
t("'…, Grellmann (1807)': matched on the name after the comma, TRIMMED (listed)", "about Roma, Grellmann[^c3] synthesized" in eo and "TRIMMED" in o, o + eo)
t("'(2018, 78)' with Law and Kovats named earlier -> law2018 (not law2012), YEAR-ONLY listed",
  "1422[^c4]." in eo and "[^c4]: [@law2018, s. 78]." in eo and "YEAR-ONLY" in o, o + eo)
t("'(1544)' after a title: no work of that year by a named author -> left, YEAR-ONLY? (not blocking)",
  "*Cosmographia* (1544)." in eo and "YEAR-ONLY?" in o and c == 0, o + eo)
t("block quotation '(2008, 183)': author named in the lead-in paragraph -> hancock2008", "[@hancock2008, s. 183]" in eo, o + eo)
t("author's spelling of a transliterated name (srom-as-written 'Byelikov', 'Kirey; Serdyuk') resolves",
  "[@bielikov2003, s. 87; @kirei1984, s. 113–114]" in eo, o + eo)

enote = os.path.join(d, "enote.md")
open(enote, "w", encoding="utf-8").write("Text.[^1]\n\n[^1]: They kept their affairs (1992, 81); Law and Kovats 2018, 78. See also Law 2012.\n")
c, o = cm("scan", enote, "--refs", esub2, "--apply", os.path.join(d, "enote_out.md"))
no = open(os.path.join(d, "enote_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "enote_out.md")) else ""
t("in a note: comma locator inside the token ('Law and Kovats 2018, 78' -> [@law2018, s. 78]); 'See also' -> 'Zob. też'",
  "[@law2018, s. 78]." in no and "[Zob. też @law2012]." in no, o + no)
t("in a note: '(1992, 81)' with no author named -> left as written, YEAR-ONLY?", "affairs (1992, 81);" in no and "YEAR-ONLY?" in o, o + no)

ren = os.path.join(d, "ren.md")
open(ren, "w", encoding="utf-8").write("First (Law 2012).[^1] Then Melamed (2015) and more.[^t1]\n\n[^1]: An author's note (Law and Kovats 2018, 78).\n\n"
                                       "[^t1]: A translator's note – przyp. tłum.\n\nNext (Robinson 2000).[^2]\n\n[^2]: Second author's note.\n")
c, o = cm("scan", ren, "--refs", esub2, "--apply", os.path.join(d, "ren_out.md"), "--renumber")
ro = open(os.path.join(d, "ren_out.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "ren_out.md")) else ""
t("--renumber: labels 1…N in marker order, definitions sorted per paragraph, t-labels untouched, author's notes mapped",
  ro.startswith("First[^1].[^2] Then Melamed[^3] and more.[^t1]\n\n[^1]: [@law2012].\n\n[^2]: An author's note [@law2018, s. 78].\n\n"
                "[^3]: [@melamed2015].\n\n[^t1]: A translator's note – przyp. tłum.\n\nNext[^4].[^5]\n\n[^4]: [@robinson2000].\n\n[^5]: Second author's note.")
  and "1→2" in o and "2→5" in o, o + ro)
c2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check.py"), os.path.join(d, "ren_out.md"), "--refs", esub2], capture_output=True, text=True)
t("--renumber output passes check.py", c2.returncode == 0, c2.stdout + c2.stderr)

n, ok = len(res), sum(res)
print(f"CITEMAP ALL PASS {n}/{n}" if ok == n else f"CITEMAP FAILED {n - ok}/{n}")
