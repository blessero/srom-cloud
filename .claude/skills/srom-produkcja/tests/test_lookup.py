"""lookup.py (28.09.2026): a work cited but missing from the author's bibliography -> Crossref candidates + a query
row, never refs.json; a web text's publication date from the page (Kanon § 8.6). Offline: --from-file fixtures."""
import csv, json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(ROOT, "scripts", "lookup.py")
d = tempfile.mkdtemp()
res = []

def t(name, ok, out=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n" + str(out)[:2000]))

def run(*args):
    r = subprocess.run([sys.executable, L, *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

cr = {"message": {"items": [
    {"type": "book-chapter", "DOI": "10.7312/jenk19074-002", "title": ["Introduction: The Old History of Capitalism"],
     "author": [{"family": "Jenkins", "given": "Destin"}, {"family": "Leroy", "given": "Justin"}],
     "container-title": ["Histories of Racial Capitalism"], "issued": {"date-parts": [[2021]]}, "publisher": "Columbia University Press"},
    {"type": "edited-book", "DOI": "10.7312/jenk19074", "title": ["Histories of Racial Capitalism"],
     "editor": [{"family": "Jenkins", "given": "Destin"}, {"family": "Leroy", "given": "Justin"}],
     "issued": {"date-parts": [[2021, 1, 25]]}, "publisher": "Columbia University Press"},
    {"type": "journal-article", "DOI": "10.5070/x", "title": ["Review of Histories of Racial Capitalism"],
     "author": [{"family": "Platt", "given": "L."}], "issued": {"date-parts": [[2021]]}},
    {"type": "book", "DOI": "10.1/other", "title": ["Another Book"], "author": [{"family": "Jenkins"}, {"family": "Leroy"}],
     "issued": {"date-parts": [[2019]]}}]}}
crf = os.path.join(d, "cr.json"); json.dump(cr, open(crf, "w", encoding="utf-8"))
q, cj = os.path.join(d, "q.csv"), os.path.join(d, "c.json")
c, o = run("missing", "Jenkins and Leroy", "2021", "--from-file", crf, "--csv", q, "--json", cj, "--note", "m9")
t("missing: candidates = year matches and both names among authors/editors (a review and a 2019 book left out); book first",
  "CANDIDATE 1: Destin Jenkins, Justin Leroy (red.), Histories of Racial Capitalism" in o and "CANDIDATE 2: Destin Jenkins, Justin Leroy, Introduction" in o
  and "Platt" not in o and "Another Book" not in o and "LOOKUP OK 2" in o, o)
rows = list(csv.reader(open(q, encoding="utf-8-sig"), delimiter=";")) if os.path.exists(q) else []
t("missing: one query row to the author, in the _pytania columns (build.py --queries)",
  rows[:1] == [["adresat", "rodzaj", "przypis", "dzieło", "szczegóły"]] and len(rows) == 2 and rows[1][0] == "autor"
  and rows[1][2] == "m9" and "DOI: 10.7312/jenk19074" in rows[1][4], rows)
cand = json.load(open(cj, encoding="utf-8")) if os.path.exists(cj) else []
t("missing: CSL-JSON drafts marked srom-candidate, with srom-source (the DOI)", cand and all(x.get("srom-candidate") for x in cand)
  and cand[0]["type"] == "book" and cand[0]["srom-source"] == "https://doi.org/10.7312/jenk19074" and cand[0]["id"] == "jenkins2021", cand)
c, o = run("missing", "Nobody", "2021", "--from-file", crf, "--csv", os.path.join(d, "q2.csv"))
t("missing: nothing found -> LOOKUP NONE, query row asks the author", "LOOKUP NONE" in o
  and "prosimy o opis" in open(os.path.join(d, "q2.csv"), encoding="utf-8-sig").read(), o)

page = os.path.join(d, "p.html")
open(page, "w", encoding="utf-8").write('<html><head><meta property="og:type" content="article" />'
                                        '<meta property="article:published_time" content="2016-10-05T14:00:30+00:00" /></head></html>')
c, o = run("webdate", "https://example.org/x", "--from-file", page)
t("webdate: article:published_time -> 05.10.2016", "WEBDATE 05.10.2016 (article:published_time)" in o, o)
ld = os.path.join(d, "ld.html"); open(ld, "w", encoding="utf-8").write('<script type="application/ld+json">{"datePublished": "2020-10-05"}</script>')
c, o = run("webdate", "https://example.org/y", "--from-file", ld)
t("webdate: JSON-LD datePublished", "WEBDATE 05.10.2020 (datePublished)" in o, o)
nd = os.path.join(d, "nd.html"); open(nd, "w", encoding="utf-8").write("<html><body>No date here.</body></html>")
c, o = run("webdate", "https://example.org/z", "--from-file", nd)
t("webdate: no date on the page -> srom-undated advice, LOOKUP NONE", "srom-undated" in o and "LOOKUP NONE" in o, o)

refs = [{"id": "a2016", "type": "webpage", "title": "A", "URL": "https://example.org/a", "issued": {"date-parts": [[2016]]}},
        {"id": "b", "type": "post-weblog", "title": "B", "URL": "https://example.org/b", "srom-undated": True},
        {"id": "c2016", "type": "webpage", "title": "C", "URL": "https://example.org/c", "issued": {"date-parts": [[2016, 10, 5]]}},
        {"id": "d2000", "type": "book", "title": "D"}]
rf = os.path.join(d, "refs.json"); json.dump(refs, open(rf, "w", encoding="utf-8"))
q3 = os.path.join(d, "q3.csv")
c, o = run("webdates", rf, "--from-file", page, "--csv", q3)
t("webdates: only web texts without a full date and not srom-undated; year kept, day/month from the page",
  "a2016: page 05.10.2016" in o and "b:" not in o and "c2016" not in o and "d2000" not in o and "LOOKUP OK 1" in o, o)
t("webdates: query row for the editor", "a2016" in open(q3, encoding="utf-8-sig").read(), o)

# build.py lists a cited web text without a full publication date (unless srom-undated)
bref = [{"id": "web2016", "type": "webpage", "author": [{"family": "Nowak", "given": "Anna"}], "title": "Tekst", "container-title": "Serwis",
         "URL": "https://example.org/t", "issued": {"date-parts": [[2016]]}},
        {"id": "webnd", "type": "webpage", "author": [{"family": "Kowal", "given": "Jan"}], "title": "Strona", "container-title": "Serwis",
         "URL": "https://example.org/s", "srom-undated": True}]
brf = os.path.join(d, "brefs.json"); json.dump(bref, open(brf, "w", encoding="utf-8"), ensure_ascii=False)
bmd = os.path.join(d, "art.md"); open(bmd, "w", encoding="utf-8").write("Tekst.[^1] Dalej.[^2]\n\n[^1]: [@web2016].\n\n[^2]: [@webnd].\n")
subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), bmd, "--refs", brf, "--out", os.path.join(d, "b")], capture_output=True, text=True)
pyt = open(os.path.join(d, "b", "art_pytania.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "b", "art_pytania.md")) else ""
t("build: query row for a web text with year only; none for one marked srom-undated",
  [l for l in pyt.splitlines() if "bez pełnej daty" in l and "web2016" in l]
  and not [l for l in pyt.splitlines() if "bez pełnej daty" in l and "webnd" in l], pyt)

# dois (Kanon § 9.7): registry check of given DOIs; a Crossref DOI proposed only when year, first author, title agree
drefs = [{"id": "yd2006", "type": "article-journal", "author": [{"family": "Yural-Davis", "given": "Nira"}], "title": "Belonging",
          "container-title": "Patterns", "volume": "40", "page": "197-214", "issued": {"date-parts": [[2006]]}, "DOI": "10.1/yd"},
         {"id": "gb2006", "type": "article-journal", "author": [{"family": "Goldberg", "given": "David Theo"}], "title": "Racial Europeanization",
          "volume": "29", "page": "331-364", "issued": {"date-parts": [[2006]]}, "DOI": "10.1/gb"},
         {"id": "tu2010", "type": "book", "author": [{"family": "Turda", "given": "Marius"}], "title": "Modernism and Eugenics",
          "issued": {"date-parts": [[2010]]}},
         {"id": "xx2010", "type": "book", "author": [{"family": "Turda", "given": "Marius"}], "title": "Another Title Entirely",
          "issued": {"date-parts": [[2010]]}}]
canned = {"works/10.1/yd": json.dumps({"message": {"title": ["Belonging"], "author": [{"family": "Yuval-Davis"}], "volume": "40",
                                                     "page": "197-214", "issued": {"date-parts": [[2006]]}}}),
          "works/10.1/gb": json.dumps({"message": {"title": ["Racial Europeanization"], "author": [{"family": "Theo Goldberg", "given": "David"}],
                                                     "volume": "29", "page": "331-364", "issued": {"date-parts": [[2006, 2]]}}}),
          "query.bibliographic": json.dumps({"message": {"items": [
              {"DOI": "10.1057/9780230281332", "title": ["Modernism and Eugenics"], "author": [{"family": "Turda"}],
               "issued": {"date-parts": [[2010]]}}]}})}
cf = os.path.join(d, "canned.json"); json.dump(canned, open(cf, "w", encoding="utf-8"))
drf = os.path.join(d, "drefs.json"); json.dump(drefs, open(drf, "w", encoding="utf-8"))
q4 = os.path.join(d, "q4.csv")
c, o = run("dois", drf, "--canned", cf, "--csv", q4)
t("dois: misspelt author caught (Yural-Davis); a registry family 'Theo Goldberg' is not a difference",
  "yd2006\tDIFFERS" in o and "Yuval-Davis" in o and "gb2006\tOK" in o, o)
t("dois: DOI proposed only for the work whose title agrees", "tu2010\tPROPOSED\t10.1057/9780230281332" in o and "xx2010\tNONE" in o, o)
rows4 = open(q4, encoding="utf-8-sig").read() if os.path.exists(q4) else ""
t("dois: query rows to the editor, refs.json untouched", "redakcja" in rows4 and "10.1057/9780230281332" in rows4
  and "DOI" not in [k for r in json.load(open(drf, encoding="utf-8")) for k in r if r["id"] == "tu2010"], rows4)

# imprints (GEN-4): LoC, DNB, BN MARC records; title words + year must agree; conflicting records are not resolved
def marc(title, place, pub, date, rid):
    return (f'<record xmlns="http://www.loc.gov/MARC21/slim"><controlfield tag="001">{rid}</controlfield>'
            f'<controlfield tag="008">000000s{date}</controlfield><datafield tag="245" ind1="1" ind2="0"><subfield code="a">{title}</subfield></datafield>'
            f'<datafield tag="264" ind1=" " ind2="1"><subfield code="a">{place}</subfield><subfield code="b">{pub}</subfield>'
            f'<subfield code="c">{date}</subfield></datafield></record>')
coll = lambda *r: "<collection>" + "".join(r) + "</collection>"
irefs = [{"id": "bogdal2011", "type": "book", "author": [{"family": "Bogdal"}], "title": "Europa erfindet die Zigeuner", "issued": {"date-parts": [[2011]]}},
         {"id": "fic1986", "type": "book", "author": [{"family": "Ficowski"}], "title": "Cyganie na polskich drogach", "publisher": "Wydawnictwo Literackie",
          "issued": {"date-parts": [[1986]]}},
         {"id": "amb2000", "type": "book", "author": [{"family": "Amb"}], "title": "Ambiguous Book", "issued": {"date-parts": [[2000]]}},
         {"id": "art", "type": "article-journal", "author": [{"family": "X"}], "title": "Journal article", "issued": {"date-parts": [[2000]]}}]
icanned = {"lx2.loc.gov": coll(marc("Ambiguous book", "London :", "Routledge,", "2000", "L1")),
           "dnb.de": coll(marc("Europa erfindet die Zigeuner :", "Berlin", "Suhrkamp", "2011", "D1"),
                          marc("Ambiguous book", "[Oxford]", "Blackwell", "2000", "D2")),
           "bn.org.pl": coll(marc("Cyganie na polskich drogach /", "Kraków ;", "Wydaw. Literackie,", "1986", "B1"))}
icf = os.path.join(d, "icanned.json"); json.dump(icanned, open(icf, "w", encoding="utf-8"))
irf = os.path.join(d, "irefs.json"); json.dump(irefs, open(irf, "w", encoding="utf-8"))
c, o = run("imprints", irf, "--canned", icf)
t("imprints: German book from DNB (place and publisher), Polish place from BN, publisher already known not asked",
  "bogdal2011\tpublisher-place\tBerlin" in o and "bogdal2011\tpublisher\tSuhrkamp" in o and "fic1986\tpublisher-place\tKraków" in o
  and "fic1986\tpublisher\t" not in o, o)
t("imprints: two catalogues disagree -> CONFLICT, not a value; journal articles skipped",
  "amb2000\tpublisher-place\tCONFLICT: London / Oxford" in o and "art\t" not in o, o)

n, ok = len(res), sum(res)
print(f"LOOKUP ALL PASS {n}/{n}" if ok == n else f"LOOKUP FAILED {n - ok}/{n}")
