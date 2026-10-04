"""SYS-5 (MB 02.10.2026): DOI links in the online PDF, never printed (GEN-10). build.py writes <stem>_doi.jsx: per footnote
the text of each citation with a DOI, cut apart where one note cites several works, and every bibliography entry with a
DOI, each with its https://doi.org/ link percent-encoded. The InDesign side (hyperlinks surviving the PDF export) is
proven live by tools/indesign_check/doi_check.py."""
import os, re, sys, json, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

SICI = "10.1002/(SICI)1097-4571(199806)49:8<693::AID-ASI3>3.0.CO;2-O"
u, why = build.doi_url(SICI)
t("SICI DOI: < > ; ( ) : percent-encoded, slash kept", u == "https://doi.org/10.1002/%28SICI%291097-4571%28199806%2949%3A8%3C693%3A%3AAID-ASI3%3E3.0.CO%3B2-O"
  and why is None, (u, why))
t("DOI given as a URL or with doi: → the bare DOI", build.doi_url("https://doi.org/10.1234/ab.c")[0] == "https://doi.org/10.1234/ab.c"
  and build.doi_url("doi: 10.1234/ab.c")[0] == "https://doi.org/10.1234/ab.c" and build.doi_url("http://dx.doi.org/10.1234/x")[0] == "https://doi.org/10.1234/x")
t("not a DOI → no link, said why", build.doi_url("1234/abc") == (None, "not a DOI (10.<prefix>/<suffix>): not linked"))
u, why = build.doi_url("10.5555/a%28b%29")
t("URL-encoded DOI decoded once (no %2528) and flagged", u == "https://doi.org/10.5555/a%28b%29" and "URL-encoded" in why, (u, why))
t("# and ? in a DOI never end the link early", build.doi_url("10.1234/a#b?c")[0] == "https://doi.org/10.1234/a%23b%3Fc")

work = tempfile.mkdtemp()
def ref(id_, title, doi=None, fam="Kowalski", typ="article-journal", year=2020):
    r = {"id": id_, "type": typ, "title": title, "author": [{"family": fam, "given": "Jan"}], "issued": {"date-parts": [[year]]}}
    if typ == "article-journal":
        r.update({"container-title": "Studia Testowe", "volume": "3", "issue": "1", "page": "10-20"})
    else:
        r.update({"publisher": "Wydawnictwo", "publisher-place": "Kraków"})
    if doi:
        r["DOI"] = doi
    return r
refs = [ref("kowalski2020", "Romowie; studium przypadku", SICI),
        ref("nowak2019", "Cyganie w Polsce", "https://doi.org/10.1234/abc.def", "Nowak", "book", 2019),
        ref("bezdoi2001", "Książka bez DOI", None, "Wiśniewski", "book", 2001),
        ref("zly2005", "Zły numer", "bad doi", "Zieliński", "article-journal", 2005)]
rp = os.path.join(work, "refs.json")
json.dump(refs, open(rp, "w", encoding="utf-8"), ensure_ascii=False)
md = os.path.join(work, "doitest.md")
open(md, "w", encoding="utf-8").write("""Tekst pierwszy[^1]. Tekst drugi[^2]. Tekst trzeci[^3]. Tekst czwarty[^4].

[^1]: Zob. [@kowalski2020, s. 12; @bezdoi2001, s. 7; @nowak2019].

[^2]: [@kowalski2020, s. 14].

[^3]: [@kowalski2020, s. 15].

[^4]: Tak twierdzi [@nowak2019, s. 3], inaczej niż [@zly2005].
""")
out = os.path.join(work, "out")
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md, "--refs", rp, "--out", out, "--draft"], capture_output=True, text=True)
rep = open(os.path.join(out, "doitest_report.md"), encoding="utf-8").read()
t("build passes", r.returncode == 0, rep[:1500])
jp = os.path.join(out, "doitest_doi.jsx")
t("_doi.jsx written", os.path.exists(jp))
src = open(jp, encoding="utf-8").read() if os.path.exists(jp) else ""
def arr(name):
    m = re.search(r"var %s = (?:\{|\[)\n(.*?)\n(?:\}|\]);" % name, src, re.S)
    return m.group(1) if m else ""
notes = json.loads("{" + arr("NOTES") + "}")
bib = json.loads("[" + arr("BIB") + "]")
txt = open(os.path.join(out, "doitest.txt"), encoding="utf-8").read()
n1 = notes.get("1", [])
t("note 1: three works cited, the two with a DOI linked, each to its own text (a '; ' inside a title does not cut it)",
  [x[2] for x in n1] == ["kowalski2020", "nowak2019"] and "Romowie; studium przypadku" in n1[0][0] and "Wiśniewski" not in n1[0][0]
  and n1[0][0].endswith("s. 12") and n1[1][0].startswith("J. Nowak, Cyganie w Polsce"), n1)
t("each linked text is in the printed note as it stands", all(x[0] in txt for v in notes.values() for x in v),
  [x[0] for v in notes.values() for x in v if x[0] not in txt])
t("the short form and Ibidem are linked too (notes 2, 3)", notes.get("2", [[""]])[0][0].startswith("Kowalski, Romowie")
  and notes.get("3", [[""]])[0][0].startswith("Ibidem, s. 15"), notes)
t("note 4: only the work with a valid DOI", [x[2] for x in notes.get("4", [])] == ["nowak2019"], notes.get("4"))
t("bibliography: the two entries with a valid DOI, text as printed", sorted(x[2] for x in bib) == ["kowalski2020", "nowak2019"]
  and all(x[0].split(",")[0] in txt for x in bib), bib)
t("bibliography text intact around a DOI with parentheses (Crossref unstructured_citation too)",
  any(x[0].endswith("DOI: " + SICI + ".") or ("Romowie; studium przypadku" in x[0] and x[0].rstrip(".").endswith("s. 10–20"))
      for x in bib if x[2] == "kowalski2020") and all(x[0] in txt for x in bib), [x[0] for x in bib])
urls = re.findall(r'"(https://doi\.org/[^"]*)"', src)
t("every link in the script is encoded (no raw < > ; ( ) # ? or space)", urls and not any(re.search(r"[<>;()#? ]", x.split("doi.org/")[1]) for x in urls), urls)
t("invalid DOI reported in the build warnings", "DOI of zly2005 “bad doi”: not a DOI" in rep, rep[:2000])
t("report line: counts and when to run the script",
  "DOI links (online PDF, not printed): 5 citations in notes, 2 bibliography entries, 2 works with a DOI (run doitest_doi.jsx" in rep, re.findall(r"- DOI links.*", rep))
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), jp], capture_output=True, text=True)
t("_doi.jsx is valid ES3", "JSX-DONE" in r.stdout, r.stdout)
tpl = open(os.path.join(ROOT, "indesign", "srom_doi.jsx.tpl"), encoding="utf-8").read()
t("script: invisible links, replaces only its own, one undo step, asks first, writes no other file than its report",
  "h.visible = false" in tpl and 'PREFIX = "srom-doi "' in tpl and "UndoModes.ENTIRE_SCRIPT" in tpl and "confirm(" in tpl
  and tpl.count("new File(") == 2 and "_doi.txt" in tpl)
# no DOI at all: no script, and an old one is removed
refs2 = [{k: v for k, v in x.items() if k != "DOI"} for x in refs]
json.dump(refs2, open(rp, "w", encoding="utf-8"), ensure_ascii=False)
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md, "--refs", rp, "--out", out, "--draft"], capture_output=True, text=True)
t("no DOI in the refs: no _doi.jsx (the old one removed)", r.returncode == 0 and not os.path.exists(jp), r.stdout)
# Code: <repo>/tools/; the Cowork bundle: <bundle>/local/ (the plugin sits at plugin/srom/skills/srom-produkcja)
inst_p = next((p for p in (os.path.join(ROOT, "..", "..", "..", "tools", "install_scripts.sh"),
                           os.path.join(ROOT, "..", "..", "..", "..", "local", "install_scripts.sh")) if os.path.exists(p)), "")
inst = open(inst_p, encoding="utf-8").read() if inst_p else ""
t("install_scripts.sh links the article's _doi.jsx into the panel", "postimport ibidem gwiazdki doi" in inst)
n, ok = len(res), sum(res)
print(f"DOI ALL PASS {n}/{n}" if ok == n else f"DOI FAILED {n - ok}/{n}")
