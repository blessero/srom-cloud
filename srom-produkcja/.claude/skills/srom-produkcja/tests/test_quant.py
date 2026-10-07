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

# cover_page.py (03.10.2026): the online metadata page from the master row, prepended to the article's PDF
import pymupdf
CV = os.path.join(os.path.dirname(GEN), "cover_page.py")
spec = importlib.util.spec_from_file_location("cover_page", CV); cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
cdir = tempfile.mkdtemp()
ccols = ["article_id", "doi", "landing_url", "journal_title", "issn", "volume", "year", "publisher", "pub_date_online", "title_pl", "title_en",
         "authors_display", "authors_struct", "abstract_pl", "abstract_en", "keywords_pl", "keywords_en", "pages", "pages_from",
         "pages_to", "pdf_file", "language", "license", "license_url", "is_translation", "original_title", "original_source",
         "original_doi", "translators_struct"]
def crow(n, **kw):
    r = dict(article_id=f"SROM-19-2026-00{n}", doi=f"10.12345/ab3k9x2{n}", landing_url=f"https://x.pl/articles/10.12345/ab3k9x2{n}/", journal_title="Studia Romologica", issn="1689-4758",
             volume="19", year="2026", publisher="Komitet Opieki nad Zabytkami Kultury Żydowskiej w Tarnowie",
             pub_date_online="2026-07-02", title_pl="Romowie w Polsce i w Europie", title_en="Roma in Poland and in Europe",
             authors_display="Anna Nowak, Jan Lis", authors_struct="Anna|Nowak|Uniwersytet Jagielloński|https://orcid.org/0000-0002-1825-0097 ;; Jan|Lis||",
             abstract_pl="Krótki abstrakt o Romach w Polsce.", abstract_en="A short abstract.", keywords_pl="Romowie, Polska",
             keywords_en="Roma, Poland", pages="11–14", pages_from="11", pages_to="14", pdf_file=f"SROM_19_2026_Nowak_{n}.pdf",
             language="pl", license="CC-BY", license_url="https://creativecommons.org/licenses/by/4.0/", is_translation="",
             original_title="", original_source="", original_doi="", translators_struct="")
    r.update(kw); return r
long_pl, long_en = "Długie zdanie abstraktu o Romach w Polsce. " * 80, "A long sentence of the abstract about Roma. " * 80
crs = [crow(1), crow(2, abstract_pl=long_pl, abstract_en=long_en), crow(3, abstract_pl="", abstract_en="", keywords_pl="", keywords_en=""),
       crow(4, doi="10.XXXXX/todo0004", pub_date_online="2026-12-TODO"), crow(5, is_translation="TAK"),
       crow(6, is_translation="TAK", translators_struct="Michał|Bartosz||", original_title="Roma", original_source="„Romani Studies”, 2024",
            original_doi="10.3828/rs.2024.3", license_url="https://creativecommons.org/licenses/by-nc-nd/4.0/")]
ccp = os.path.join(cdir, "m.csv")
with open(ccp, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ccols); w.writeheader(); w.writerows(crs)
art = pymupdf.open()
for i in range(4):
    pg = art.new_page(width=cv.W, height=cv.H); pg.insert_text((72, 72), f"strona {11 + i}")
art.set_toc([[1, "Wstęp", 2]]); art.save(os.path.join(cdir, "art.pdf"))
def cvrun(*args):
    return subprocess.run([sys.executable, CV, ccp, *args, "--out", cdir], capture_output=True, text=True)
r = cvrun("SROM-19-2026-001", os.path.join(cdir, "art.pdf"))
fp = os.path.join(cdir, "SROM_19_2026_Nowak_1.pdf")
doc = pymupdf.open(fp) if os.path.exists(fp) else None
flat = lambda pg: " ".join(pg.get_text().replace("\u00a0", " ").split())
txt = flat(doc[0]) if doc else ""
t("cover_page: cover + article, page labels i, 11…14, bookmark still on the article's page",
  doc and len(doc) == 5 and [doc[i].get_label() for i in range(5)] == ["i", "11", "12", "13", "14"]
  and doc.get_toc() == [[1, "Wstęp", 3]] and "RESULT: OK" in r.stdout, r.stdout + r.stderr)
t("cover_page: page shows DOI URL, both authors, date dd.mm.rrrr, CC BY sentence, citation with t. 19",
  all(x in txt for x in ("https://doi.org/10.12345/ab3k9x21", "Anna Nowak", "Jan Lis", "Opublikowano online: 02.07.2026",
                          "Uznanie autorstwa 4.0 (CC BY 4.0)", "„Studia Romologica”, 2026, t. 19, s. 11–14.",
                          "Romowie; Polska")), txt[:1500])
links = {l.get("uri") for l in doc[0].get_links()} if doc else set()
t("cover_page: DOI line links to the landing page; ORCID, licence, site",
  {"https://x.pl/articles/10.12345/ab3k9x21/", "https://orcid.org/0000-0002-1825-0097", "https://creativecommons.org/licenses/by/4.0/",
   "https://studiaromologica.pl"} <= links, links)
x = doc.get_xml_metadata() if doc else ""
t("cover_page: Info + XMP metadata (title, PRISM DOI, licence)",
  doc and doc.metadata["title"] == "Romowie w Polsce i w Europie" and "<prism:doi>10.12345/ab3k9x21</prism:doi>" in x
  and "<xmpRights:WebStatement>https://creativecommons.org/licenses/by/4.0/</xmpRights:WebStatement>" in x
  and etree.fromstring(x.split("?>", 1)[1].rsplit("<?xpacket", 1)[0].encode()) is not None, x[:600])
t("cover_page: Kanon § 3.3 hard spaces (one-letter words, t., initials)",
  cv.nbsp("Romowie w Polsce i w Europie, t. 5, J. Ficowski, 5 %") == "Romowie w\u00a0Polsce i\u00a0w\u00a0Europie, t.\u00a05, J.\u00a0Ficowski, 5\u00a0%"
  and cv.nbsp("Tow. Wszechnicy") == "Tow. Wszechnicy", cv.nbsp("Romowie w Polsce i w Europie, t. 5, J. Ficowski, 5 %"))
r = cvrun("SROM-19-2026-002")
t("cover_page: one page strictly — abstracts too long → ABORT, nothing written", r.returncode != 0 and "does not fit on one page" in r.stderr
  and not os.path.exists(os.path.join(cdir, "SROM-19-2026-002_okladka.pdf")), r.stdout + r.stderr)
t("cover_page: MB's template — 88 % black ink, red edge bars, justified abstracts",
  cv.INK == "#424241" and "text-align:justify" in cv.p(7.5, 11.52, "x", extra="; text-align:justify")
  and doc is not None and len([d for d in doc[0].get_drawings() if d.get("fill") and abs(d["fill"][0] - 227 / 255) < .01 and d["rect"].height > 600]) == 2, "")
# MB's template 1.2 (04.10.2026): abstract blocks flex between the citation and 218 mm; 7.2 pt, then 7 pt, then stop
def cover_size(n):
    ws = ["Romowie", "w", "Polsce"]; ew = ["Roma", "in", "Poland"]
    row = crow(1, abstract_pl=" ".join((ws * n)[:n]), abstract_en=" ".join((ew * n)[:n]))
    try:
        d, size = cv.cover(row)
    except SystemExit:
        return None, None
    return d, size
seq = [cover_size(n)[1] for n in range(278, 312)]
t("cover_page: abstracts 7.2 pt while they fit, then 7 pt, then stop — never anything else",
  seq[0] == 7.2 and seq[-1] is None and set(seq) == {7.2, 7.0, None}
  and seq == sorted(seq, key=lambda v: (v is None, -(v or 0))), seq)
last = max(n for n in range(278, 312) if cover_size(n)[1] == 7.0)
dl, szl = cover_size(last)
words = dl[0].get_text("words")
kw_bottom = max(w[3] for w in words if w[4] == "Keywords:")
lab = {w[4]: w[0] for w in words if w[4] in ("Abstrakt", "Abstract")}
t("cover_page: the longest abstracts that fit end above 218 mm; labels Abstrakt / Abstract share one left edge",
  szl == 7.0 and 0 < kw_bottom <= cv.ABSTRACT_BOTTOM and len(lab) == 2 and abs(lab["Abstrakt"] - lab["Abstract"]) < .5,
  (szl, kw_bottom, cv.ABSTRACT_BOTTOM, lab))
sp = cover_size(1)[0][0]
at = lambda s: sp.search_for(s)[0]
t("cover_page: template 1.2 — journal block under the logo, info block order Strony · DOI · licence · © · date",
  abs(at("ISSN: 1689-4758").x0 - cv.TX) < 2 and 64 < at("ISSN: 1689-4758").y0 < 86 and at("Strony: 11–14").x0 > 250
  and at("Strony: 11–14").y0 < at("https://doi.org/10.12345/ab3k9x21").y0 < at("CC BY 4.0").y0 < at("© 2026").y0
  < at("Opublikowano online: 02.07.2026").y0, "")
r = cvrun("SROM-19-2026-003"); d3 = pymupdf.open(os.path.join(cdir, "SROM-19-2026-003_okladka.pdf")) if r.returncode == 0 else None
t("cover_page: no abstracts (review) → header alone, one page", d3 and len(d3) == 1 and "Abstrakt" not in d3[0].get_text(), r.stdout + r.stderr)
r = cvrun("SROM-19-2026-004")
t("cover_page: placeholder DOI / date → ABORT, nothing written", r.returncode != 0 and "doi is a placeholder" in r.stderr
  and "pub_date_online" in r.stderr and not os.path.exists(os.path.join(cdir, "SROM-19-2026-004_okladka.pdf")), r.stdout + r.stderr)
r = cvrun("SROM-19-2026-004", "--proof"); pf = os.path.join(cdir, "SROM-19-2026-004_okladka_proof.pdf")
t("cover_page --proof: written as *_proof, marked PODGLĄD", os.path.exists(pf) and "PODGLĄD" in pymupdf.open(pf)[0].get_text()
  and "PROOF" in r.stdout, r.stdout + r.stderr)
r = cvrun("SROM-19-2026-005")
t("cover_page: translation without translators_struct → ABORT (Kanon § 12.2.3)", r.returncode != 0 and "translators_struct" in r.stderr, r.stdout + r.stderr)
r = cvrun("SROM-19-2026-006"); d6 = pymupdf.open(os.path.join(cdir, "SROM-19-2026-006_okladka.pdf")) if r.returncode == 0 else None
t6 = flat(d6[0]) if d6 else ""
t("cover_page: translation → translator, Pierwodruk linked to the original's DOI; CC BY-NC-ND named in Polish",
  all(x in t6 for x in ("Tłumaczenie: Michał Bartosz", "Pierwodruk:", "Użycie niekomercyjne – Bez utworów zależnych 4.0 (CC BY-NC-ND 4.0)"))
  and "https://doi.org/10.3828/rs.2024.3" in {l.get("uri") for l in d6[0].get_links()}, r.stdout + r.stderr + t6[:800])
r = cvrun("SROM-19-2026-001", os.path.join(cdir, "art.pdf"))
t("cover_page: article PDF page count = CSV range → no warning", "article PDF has" not in r.stdout
  and "RESULT: OK" in r.stdout, r.stdout)
crs[1].update(pages_to="20", abstract_pl="Krótki.", abstract_en="Short.")
with open(ccp, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ccols); w.writeheader(); w.writerows(crs)
r = cvrun("SROM-19-2026-002", os.path.join(cdir, "art.pdf"))
t("cover_page: article PDF page count ≠ CSV range → warning, RESULT: CHECK", "article PDF has 4 pages, the CSV says 11–20 (10)" in r.stdout
  and "RESULT: CHECK" in r.stdout, r.stdout)

# text-layer repair (Cowork C6, 06.10.2026): fix_actualtext.py runs on the article before the cover goes in. Fixture: three
# pages of the vol. 18 PDF (Ostendorf, InDesign export of 13.05.2026); the cut lost the structure tree, so the tests add one.
import pikepdf
FX = os.path.join(ROOT, "tests", "fixtures", "pdf", "vol18_actualtext_3pp.pdf")
CLEAN = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP          # as pdftotext: no CIDs for unknown Unicode
fffd = lambda d, pages, fl=CLEAN: sum(d[i].get_text(flags=fl).count("�") for i in pages)
mcids = lambda d, pages: sum(d[i].read_contents().count(b"/MCID") for i in pages)
def variant(name, lang=None, vp=None, break_spans=False):
    p = pikepdf.open(FX)
    p.Root.MarkInfo = pikepdf.Dictionary(Marked=True)
    st = p.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.StructTreeRoot, ParentTree=pikepdf.Dictionary(Nums=[])))
    st.K = p.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.StructElem, S=pikepdf.Name.Document, P=st))
    p.Root.StructTreeRoot = st
    if lang:
        p.Root.Lang = pikepdf.String(lang)
    if vp is not None:
        p.Root.ViewerPreferences = vp
    if break_spans:      # an operator between EMC and the accent glyph: the leftover case the repair does not touch
        for pg in p.pages:
            out = []
            for ins in pikepdf.parse_content_stream(pg):
                out.append(ins)
                if ins.operator == pikepdf.Operator("EMC"):
                    out += [pikepdf.ContentStreamInstruction([], pikepdf.Operator(o)) for o in ("BX", "EX")]
            pg.obj.Contents = p.make_stream(pikepdf.unparse_content_stream(out))
    path = os.path.join(cdir, name + ".pdf"); p.save(path); return path
fx = pymupdf.open(FX)
fxt = "".join(fx[i].get_text(flags=CLEAN) for i in range(3))
t("text layer: the fixture shows the defect (152 U+FFFD, 151 right after the accented letter its span gives: „Romó�”)",
  fffd(fx, range(3)) == 152 and len(re.findall("[óśżńćźáéí]�", fxt)) == 151 and "Romó�" in fxt, fffd(fx, range(3)))
crs += [crow(7, pages="29–31", pages_from="29", pages_to="31", pdf_file="SROM_19_2026_Fix_7.pdf"),
        crow(8, pages="29–31", pages_from="29", pages_to="31", pdf_file="SROM_19_2026_Fix_8.pdf"),
        crow(9, pages="29–31", pages_from="29", pages_to="31", pdf_file="SROM_19_2026_Fix_9.pdf", language="en")]
with open(ccp, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ccols); w.writeheader(); w.writerows(crs)
r = cvrun("SROM-19-2026-007", variant("tagged"))
d7 = pymupdf.open(os.path.join(cdir, "SROM_19_2026_Fix_7.pdf")) if r.returncode == 0 else None
t("text layer: U+FFFD 152 → 0, for readers with and without ActualText; „Romów” searchable",
  d7 and fffd(d7, range(1, 4)) == 0 and fffd(d7, range(1, 4), CLEAN | pymupdf.TEXT_IGNORE_ACTUALTEXT) == 0
  and d7[1].search_for("Romów") and "text layer: 149 accent glyph(s) moved" in r.stdout, r.stdout + r.stderr)
t("text layer: the article's pages render pixel-identical at 150 dpi",
  d7 and all(d7[i + 1].get_pixmap(dpi=150).samples == fx[i].get_pixmap(dpi=150).samples for i in range(3)), "")
t("text layer: MarkInfo, StructTreeRoot, all 150 MCIDs and the ActualText spans kept",
  d7 and mcids(d7, range(1, 4)) == mcids(fx, range(3)) == 150
  and sum(d7[i].read_contents().count(b"/ActualText") for i in range(1, 4)) == sum(fx[i].read_contents().count(b"/ActualText") for i in range(3))
  and d7.xref_get_key(d7.pdf_catalog(), "MarkInfo/Marked")[1] == "true" and d7.xref_get_key(d7.pdf_catalog(), "StructTreeRoot/K/S")[1] == "/Document", "")
t("text layer: repaired file gets its cover (labels i, 29–31, DOI); /Lang pl and DisplayDocTitle set; self-check line",
  d7 and len(d7) == 4 and [d7[i].get_label() for i in range(4)] == ["i", "29", "30", "31"]
  and "https://doi.org/10.12345/ab3k9x27" in d7[0].get_text()
  and "self-check: U+FFFD 0 · pages 4 · tagged yes · /Lang pl · DisplayDocTitle true · DOI in XMP yes" in r.stdout
  and "RESULT: OK" in r.stdout, r.stdout + r.stderr)
r = cvrun("SROM-19-2026-008", variant("tagged_lang", lang="pl-PL", vp=pikepdf.Dictionary(HideToolbar=False)))
p8 = pikepdf.open(os.path.join(cdir, "SROM_19_2026_Fix_8.pdf")) if r.returncode == 0 else None
t("text layer: the export's own /Lang and ViewerPreferences kept, DisplayDocTitle added",
  p8 is not None and str(p8.Root.Lang) == "pl-PL" and p8.Root.ViewerPreferences.HideToolbar is False
  and p8.Root.ViewerPreferences.DisplayDocTitle is True and "RESULT: OK" in r.stdout, r.stdout + r.stderr)
r = cvrun("SROM-19-2026-009", os.path.join(cdir, "tagged_lang.pdf"))
t("text layer: /Lang of the PDF ≠ the CSV's language → warning, RESULT: CHECK",
  "the PDF's /Lang is pl-PL, the CSV's language is en" in r.stdout and "RESULT: CHECK" in r.stdout, r.stdout + r.stderr)
r = cvrun("SROM-19-2026-007", variant("leftover", break_spans=True))
t("text layer: the known leftovers (accent glyph not next after the span) are left as they are and counted, not hidden",
  "text layer: 0 accent glyph(s) moved" in r.stdout and "self-check: U+FFFD 152 ·" in r.stdout, r.stdout + r.stderr)

n, ok = len(res), sum(res)
print(f"QUANT ALL PASS {n}/{n}" if ok == n else f"QUANT FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
