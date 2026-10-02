"""srom-quant generate_crossref_xml.py (30.09.2026): references from volumes/<vol>/citations/<article_id>.json become
<citation_list> after <doi_data> (Kanon § 13.1); each institution of an affiliation is its own <institution>, with a
ROR ID from volumes/ror.tsv. Offline; the output was validated against the Crossref 5.4.0 XSD when this was built."""
import csv, json, os, re, subprocess, sys, tempfile
from lxml import etree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(os.path.dirname(ROOT), "srom-quant", "scripts", "generate_crossref_xml.py")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

d = tempfile.mkdtemp()
vol = os.path.join(d, "volumes", "19"); os.makedirs(os.path.join(vol, "citations"))
cols = ["article_id", "doi_suffix", "doi", "landing_url", "pdf_url", "volume", "year", "pub_date_online", "title_pl",
        "authors_struct", "abstract_pl", "abstract_en", "pages_from", "pages_to", "language", "license_url"]
rows = [dict(zip(cols, ["SROM-19-2026-001", "ab3k9x2q", "10.12345/ab3k9x2q", "https://x.pl/a/", "https://x.pl/a.pdf", "19", "2026",
                        "2026-12-15", "Tytuł", "Anna|Nowak|Wydział Historii, Gonzaga University; Instytut X / Muzeum Y|", "abs", "abs",
                        "1", "20", "pl", "https://creativecommons.org/licenses/by/4.0/"])),
        dict(zip(cols, ["SROM-19-2026-002", "cd4m8n1p", "10.12345/cd4m8n1p", "https://x.pl/b/", "https://x.pl/b.pdf", "19", "2026",
                        "2026-12-15", "Drugi", "Jan|Lis||", "", "", "21", "30", "pl", ""]))]
cp = os.path.join(vol, "srom_master_v3.csv")
with open(cp, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
json.dump([{"key": "a", "doi": "10.1017/x.1", "text": "Kowalski, Jan. Tytuł & podtytuł, Kraków 2001."},
           {"key": None, "doi": "", "text": "Archiwum Narodowe w Krakowie, sygn. 1."}],
          open(os.path.join(vol, "citations", "SROM-19-2026-001.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(d, "volumes", "ror.tsv"), "w", encoding="utf-8").write(
    "institution\tror\tror_name\tsource\nWydział Historii, Gonzaga University\thttps://ror.org/03ze70h02\tGonzaga University\ttest\n")
out = os.path.join(d, "dep.xml")
r = subprocess.run([sys.executable, GEN, cp, out], capture_output=True, text=True)
t("generator runs; the article without a references file is named", r.returncode == 0 and "SROM-19-2026-002" in r.stdout, r.stdout + r.stderr)
X = etree.parse(out) if os.path.exists(out) else None
ns = {"c": "http://www.crossref.org/schema/5.4.0"}
arts = X.findall(".//c:journal_article", ns) if X is not None else []
cl = arts[0].find("c:citation_list", ns) if arts else None
t("<citation_list> after <doi_data>, one <citation> per entry, DOI where known, text escaped",
  cl is not None and arts[0].index(cl) == arts[0].index(arts[0].find("c:doi_data", ns)) + 1
  and len(cl) == 2 and cl[0].findtext("c:doi", namespaces=ns) == "10.1017/x.1"
  and cl[0].findtext("c:unstructured_citation", namespaces=ns) == "Kowalski, Jan. Tytuł & podtytuł, Kraków 2001."
  and cl[1].find("c:doi", ns) is None and arts[1].find("c:citation_list", ns) is None, etree.tostring(arts[0]) if arts else "")
inst = arts[0].findall(".//c:institution", ns) if arts else []
t("three institutions from 'A; B / C'; ROR ID only for the one in ror.tsv",
  [i.findtext("c:institution_name", namespaces=ns) for i in inst] == ["Wydział Historii, Gonzaga University", "Instytut X", "Muzeum Y"]
  and inst[0].findtext("c:institution_id", namespaces=ns) == "https://ror.org/03ze70h02" and inst[1].find("c:institution_id", ns) is None,
  [etree.tostring(i) for i in inst])

# wikidata_qs.py: QuickStatements for the journal item and for articles with a final DOI (offline)
WQ = os.path.join(os.path.dirname(GEN), "wikidata_qs.py")
j = subprocess.run([sys.executable, WQ, "journal"], capture_output=True, text=True).stdout
t("wikidata journal: scientific journal, ISSN, Polish, Romani studies",
  j.startswith("CREATE") and "LAST\tP31\tQ5633421" in j and 'LAST\tP236\t"1689-4758"' in j and "LAST\tP921\tQ2037434" in j, j)
rows[1]["doi"] = "10.XXXXX/cd4m8n1p"
with open(cp, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
r = subprocess.run([sys.executable, WQ, "articles", cp, "--journal", "Q1"], capture_output=True, text=True)
t("wikidata articles: only final DOIs (upper case), journal, pages, date, CC BY, authors in order; placeholder DOI skipped",
  r.stdout.count("CREATE") == 1 and 'LAST\tP356\t"10.12345/AB3K9X2Q"' in r.stdout and "LAST\tP1433\tQ1" in r.stdout
  and 'LAST\tP304\t"1-20"' in r.stdout and "P577\t+2026-12-15T00:00:00Z/11" in r.stdout and "P275\tQ20007257" in r.stdout
  and 'P2093\t"Anna Nowak"\tP1545\t"1"' in r.stdout and "SROM-19-2026-002: no final DOI" in r.stderr, r.stdout + r.stderr)

# pdf_metadata.py (02.10.2026): the master row → <id>_metadane.jsx; a placeholder DOI is never written
PM = os.path.join(os.path.dirname(ROOT), "srom-quant", "scripts", "pdf_metadata.py")
r = subprocess.run([sys.executable, PM, cp, "SROM-19-2026-001", "--out", d], capture_output=True, text=True)
jsx = open(os.path.join(d, "SROM-19-2026-001_metadane.jsx"), encoding="utf-8").read() if r.returncode == 0 else ""
t("pdf_metadata: title, author, licence, DOI, pages, PRISM namespace registered",
  all(x in jsx for x in ('"prism:doi", "10.12345/ab3k9x2q"', '"dc:identifier", "doi:10.12345/ab3k9x2q"', 'CC BY 4.0', '"prism:startingPage", "1"', 'registerNamespace')), r.stdout + r.stderr + jsx[:600])
rows[0]["doi"] = "10.XXXXX/todo"
with open(cp, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
r = subprocess.run([sys.executable, PM, cp, "SROM-19-2026-001", "--out", d], capture_output=True, text=True)
jsx = open(os.path.join(d, "SROM-19-2026-001_metadane.jsx"), encoding="utf-8").read()
t("pdf_metadata: a placeholder DOI is left out and named", "prism:doi" not in jsx and "DOI not written" in r.stdout, r.stdout + jsx[:400])
es = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), os.path.join(d, "SROM-19-2026-001_metadane.jsx")], capture_output=True, text=True)
t("pdf_metadata: valid ES3", "JSX-DONE" in es.stdout and "FAIL" not in es.stdout, es.stdout)

# mint_suffixes.py (03.10.2026): placeholders -> opaque [a-z0-9]{8}, unique across volumes, doi + landing_url follow, frozen after
MS = os.path.join(os.path.dirname(GEN), "mint_suffixes.py")
mdir = tempfile.mkdtemp(); mcols = ["article_id", "doi_suffix", "doi", "landing_url", "title_pl"]
def mwrite(p, rs):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=mcols); w.writeheader(); w.writerows(rs)
def mrow(n, suf, pre="10.XXXXX", vol=19):
    return {"article_id": f"SROM-{vol}-2026-00{n}", "doi_suffix": suf, "doi": f"{pre}/{suf}",
            "landing_url": f"https://x.pl/articles/{pre}/{suf}/", "title_pl": f"Tytuł, \"{n}\"; z przecinkiem"}
mp = os.path.join(mdir, "volumes", "19", "srom_master_v3.csv")
mwrite(mp, [mrow(1, "todo0001"), mrow(2, "todo0002"), mrow(3, "ab3k9x2q")])
mwrite(os.path.join(mdir, "volumes", "18", "srom_master_v3.csv"), [mrow(1, "zz9y8x7w", "10.12345", 18)])
before = open(mp, "rb").read()
r = subprocess.run([sys.executable, MS, mp, "--prefix", "10.12345", "--dry-run"], capture_output=True, text=True)
t("mint_suffixes --dry-run: reports, writes nothing", r.returncode == 0 and open(mp, "rb").read() == before and "dry run" in r.stdout, r.stdout + r.stderr)
r = subprocess.run([sys.executable, MS, mp, "--prefix", "10.12345"], capture_output=True, text=True)
raw = open(mp, "rb").read(); got = list(csv.DictReader(open(mp, encoding="utf-8-sig", newline="")))
sf = [g["doi_suffix"] for g in got]
t("mint_suffixes: 2 minted, the final suffix kept, all 8 chars [a-z0-9] and unique",
  r.returncode == 0 and "2 suffix(es) minted" in r.stdout and sf[2] == "ab3k9x2q" and len(set(sf)) == 3
  and all(re.fullmatch(r"[a-z0-9]{8}", s) and not s.startswith("todo") for s in sf), r.stdout + r.stderr + str(sf))
t("mint_suffixes: doi = prefix/suffix and landing_url follows, for the kept row too; other cells untouched",
  all(g["doi"] == "10.12345/" + g["doi_suffix"] and g["landing_url"] == f"https://x.pl/articles/10.12345/{g['doi_suffix']}/" for g in got)
  and got[0]["title_pl"] == 'Tytuł, "1"; z przecinkiem', got)
t("mint_suffixes: BOM and CRLF kept", raw.startswith(b"\xef\xbb\xbf") and raw.count(b"\r\n") == raw.count(b"\n") == 4, raw[:80])
r = subprocess.run([sys.executable, MS, mp, "--prefix", "10.12345"], capture_output=True, text=True)
t("mint_suffixes: second run changes nothing (suffixes freeze)", r.returncode == 0 and "0 suffix(es) minted, 0 row(s) changed" in r.stdout and open(mp, "rb").read() == raw, r.stdout + r.stderr)
r = subprocess.run([sys.executable, MS, mp, "--prefix", "10.99999"], capture_output=True, text=True)
t("mint_suffixes: a different real prefix aborts, file unchanged", r.returncode != 0 and "already has prefix 10.12345" in r.stderr and open(mp, "rb").read() == raw, r.stdout + r.stderr)
r = subprocess.run([sys.executable, MS, mp, "--prefix", "10.XXXXX"], capture_output=True, text=True)
t("mint_suffixes: placeholder prefix aborts", r.returncode != 0 and "not of the form" in r.stderr, r.stdout + r.stderr)
import importlib.util
spec = importlib.util.spec_from_file_location("mint_suffixes", MS); ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)
seq = iter("aaaaaaaa" + "todo1234" + "bbbbbbbb")
ms.secrets.choice = lambda alpha: next(seq)
t("mint_suffixes.mint: skips a taken suffix and a todo-looking one", ms.mint({"aaaaaaaa"}) == "bbbbbbbb", "")
mp2 = os.path.join(mdir, "volumes", "20", "srom_master_v3.csv")
mwrite(mp2, [mrow(1, "todo0001", vol=20)])
seq = iter("zz9y8x7w" + "cccccccc")          # first draw collides with volume 18's suffix
ms.run(mp2, "10.12345")
t("mint_suffixes: another volume's suffix is never reused",
  [g["doi_suffix"] for g in csv.DictReader(open(mp2, encoding="utf-8-sig", newline=""))] == ["cccccccc"], "")

n, ok = len(res), sum(res)
print(f"QUANT ALL PASS {n}/{n}" if ok == n else f"QUANT FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
