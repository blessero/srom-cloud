"""Back catalogue (Cowork C19, 19.10.2026): year-only print date, no licence (NONE), copyright holder, organisation
author, split_volume.py, pdf_enhance.py, rip_volume.py. Fixtures are made here (PyMuPDF, IBM Plex from cover_page's
font search). Last line: BACKCAT ALL PASS n/n or BACKCAT FAILED."""
import csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.environ.get("SROM_SKILLS_DIR") or os.path.normpath(os.path.join(HERE, "..", ".."))
S = os.path.join(SK, "srom-quant", "scripts")
sys.path.insert(0, S)
import pymupdf                                    # noqa: E402
import cover_page                                 # noqa: E402
from pdf_metadata import build                    # noqa: E402

RES = []
def t(name, ok, detail=""):
    RES.append(ok); print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))

def run(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)

FD = cover_page.font_dir()
FF = os.path.join(FD, cover_page.FONTS["normal"])
W, H = cover_page.W, cover_page.H
TMP = tempfile.mkdtemp(prefix="backcat_")

def lines(p, y, ls, size=10, x=50):
    for l in ls:
        p.insert_text((x, y), l, fontsize=size, fontname="plex", fontfile=FF); y += size * 1.3
    return y

# ---------------------------------------------------------------- fixtures
BASE = dict(article_id="SROM-17-2024-001", doi_suffix="t7mv3myq", doi="10.68100/t7mv3myq",
            landing_url="https://studiaromologica.pl/articles/10.68100/t7mv3myq/",
            pdf_url="https://studiaromologica.pl/wp-content/uploads/archive/17-2024/Studia_Romologica_17_2024_Test.pdf",
            journal_title="Studia Romologica", issn="1689-4758", volume="17", year="2024", issue_signature="SROM·17·2024",
            issue_theme="", publisher="Komitet Opieki nad Zabytkami Kultury Żydowskiej w Tarnowie", pub_date_online="2026-10-20",
            pub_date_print="2024", editorial_period="", section_nr="I", section_label="Część I", seq="1",
            title_pl="Tytuł testowy", title_en="Test title", authors_display="Jan Kowalski",
            authors_struct="Jan|Kowalski|Uniwersytet Testowy|", affiliation_display="Uniwersytet Testowy", orcid_display="",
            abstract_pl="", abstract_en="", keywords_pl="", keywords_en="", bio_note="", pages="3–4", pages_from="3",
            pages_to="4", pdf_file="Studia_Romologica_17_2024_Test.pdf", language="pl", license="CC-BY-NC",
            license_url="https://creativecommons.org/licenses/by-nc/4.0/", is_translation="", original_title="",
            original_source="", original_doi="", translators_struct="", copyright_holder="Komitet Testowy")
def row(**kw):
    r = dict(BASE); r.update(kw); return r
ROWS = [row(),
        row(article_id="SROM-17-2024-002", doi_suffix="mr8hq5bh", doi="10.68100/mr8hq5bh",
            landing_url="https://studiaromologica.pl/articles/10.68100/mr8hq5bh/", seq="2", pdf_file="Studia_Romologica_17_2024_Two.pdf",
            pdf_url="https://studiaromologica.pl/wp-content/uploads/archive/17-2024/Studia_Romologica_17_2024_Two.pdf",
            license="NONE", license_url="", copyright_holder="2018 Tom Lantos Institute"),
        row(article_id="SROM-17-2024-003", doi_suffix="673ss5jb", doi="10.68100/673ss5jb",
            landing_url="https://studiaromologica.pl/articles/10.68100/673ss5jb/", seq="3", pdf_file="Studia_Romologica_17_2024_Three.pdf",
            pdf_url="https://studiaromologica.pl/wp-content/uploads/archive/17-2024/Studia_Romologica_17_2024_Three.pdf",
            authors_display="Redakcja „Studia Romologica”", authors_struct="", affiliation_display="")]
CSVP = os.path.join(TMP, "vol", "srom_master_v3.csv")
os.makedirs(os.path.dirname(CSVP))
def write_csv(path, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
write_csv(CSVP, ROWS)

ART = os.path.join(TMP, "art.pdf")
d = pymupdf.open()
p = d.new_page(width=W, height=H)
lines(p, 30, ["3   Studia Romologica 17/2024"], 8)
lines(p, 80, ["Tytuł testowy"], 16)
lines(p, 120, ["WSTĘP"], 10)
lines(p, 140, ["Treść artykułu, zdanie pierwsze i drugie o historii Romów w Polsce."] * 10)
lines(p, 560, ["1 Zob. https://wyborcza.pl/magazyn/7,124059,31109096,wiersze-papuszy-ktore-znalismy-",
               "-to-glownie-falsyfikaty.html [odczyt: 17 grudnia 2024].",
               "2 DOI: 10.12797/Politeja.17.2020.66.13."], 7.5)
p = d.new_page(width=W, height=H)
lines(p, 30, ["Jan Kowalski – Tytuł testowy   4"], 8)
lines(p, 80, ["BIBLIOGRAFIA"], 10)
lines(p, 100, ["KOWALSKI, Jan, Książka, Wydawnictwo, Kraków 2020."] * 4)
d.set_metadata({"title": "Tytuł testowy"}); d.save(ART)

# ---------------------------------------------------------------- validate_master
v = run(os.path.join(S, "validate_master.py"), CSVP)
out = v.stdout
t("validate: year-only print date accepted", "pub_date_print" not in out, out[-400:])
t("validate: NONE licence is a warning, not an error", "no licence: free to read" in out and "license unfilled" not in out, out[-400:])
t("validate: unsigned text deposited as organisation (warning)", "organisation author" in out and "authors_struct empty\n" not in out, out[-400:])
t("validate: 0 blocking", v.returncode == 0, out[-400:])
bad = [row(license="NONE")]                                   # NONE with a URL left in
write_csv(os.path.join(TMP, "bad.csv"), bad)
t("validate: NONE with a licence URL blocks", run(os.path.join(S, "validate_master.py"), os.path.join(TMP, "bad.csv")).returncode == 1)

# ---------------------------------------------------------------- Crossref XML
xmlp = os.path.join(TMP, "dep.xml")
g = run(os.path.join(S, "generate_crossref_xml.py"), CSVP, xmlp)
x = open(xmlp, encoding="utf-8").read() if g.returncode == 0 else ""
art = x.split("<journal_article")
t("crossref: year-only print date", re.search(r'<publication_date media_type="print">\s*<year>2024</year>\s*</publication_date>', x) is not None, g.stdout + g.stderr)
t("crossref: NONE → free_to_read, no license_ref", len(art) == 4 and "<free_to_read/>" in art[2] and "license_ref" not in art[2]
  and "license_ref" in art[1], x[:0])
t("crossref: organisation author for an unsigned text", len(art) == 4 and '<organization sequence="first" contributor_role="author">Redakcja „Studia Romologica”</organization>' in art[3])
try:
    from lxml import etree
    etree.fromstring(x.encode()); t("crossref: well-formed", True)
except Exception as e:
    t("crossref: well-formed", False, str(e))

# ---------------------------------------------------------------- PDF metadata notice
m1, _ = build(ROWS[0]); m2, w2 = build(ROWS[1])
t("metadata: © holder + CC", m1["notice"] == "© 2024 Komitet Testowy. CC BY-NC 4.0", m1["notice"])
t("metadata: holder with its own year, NONE", m2["notice"] == "© 2018 Tom Lantos Institute. Wszelkie prawa zastrzeżone"
  and not any("licence" in w for w in w2), m2["notice"])

# ---------------------------------------------------------------- cover page
outd = os.path.join(TMP, "ready")
c1 = run(os.path.join(S, "cover_page.py"), CSVP, "SROM-17-2024-001", ART, "--out", outd)
c2 = run(os.path.join(S, "cover_page.py"), CSVP, "SROM-17-2024-002", ART, "--out", outd)
t("cover: CC row OK", "RESULT: OK" in c1.stdout, c1.stdout[-300:] + c1.stderr[-300:])
t("cover: NONE row OK", "RESULT: OK" in c2.stdout, c2.stdout[-300:] + c2.stderr[-300:])
f1 = os.path.join(outd, "Studia_Romologica_17_2024_Test.pdf"); f2 = os.path.join(outd, "Studia_Romologica_17_2024_Two.pdf")
txt1 = pymupdf.open(f1)[0].get_text().replace("\n", " ") if os.path.exists(f1) else ""
txt2 = pymupdf.open(f2)[0].get_text().replace("\n", " ") if os.path.exists(f2) else ""
t("cover: footer © publisher, CC BY-NC, print year", "© 2024 Komitet Testowy." in txt1 and "Użycie niekomercyjne" in txt1
  and "Data publikacji: 2024" in txt1, txt1[-300:])
t("cover: footer NONE: © 2018 TLI, rights reserved", "© 2018 Tom Lantos Institute." in txt2 and "Wszelkie prawa zastrzeżone" in txt2
  and "licencji" not in txt2, txt2[-300:])

# ---------------------------------------------------------------- pdf_enhance
if os.path.exists(f1):
    before = [pg.get_text() for pg in pymupdf.open(f1)]
    e = run(os.path.join(S, "pdf_enhance.py"), f1)
    dd = pymupdf.open(f1)
    toc = dd.get_toc(); links = [l["uri"] for pg in dd for l in pg.get_links() if l.get("uri")]
    t("enhance: outline cover + title + WSTĘP + BIBLIOGRAFIA",
      [x[1] for x in toc] == ["Strona metadanych", "Tytuł testowy", "WSTĘP", "BIBLIOGRAFIA"], str(toc) + e.stdout + e.stderr)
    t("enhance: broken URL joined (repeated hyphen once), DOI linked",
      links.count("https://wyborcza.pl/magazyn/7,124059,31109096,wiersze-papuszy-ktore-znalismy-to-glownie-falsyfikaty.html") == 2
      and "https://doi.org/10.12797/Politeja.17.2020.66.13" in links, str(links))
    t("enhance: text unchanged, labels kept", before == [pg.get_text() for pg in dd] and dd.get_page_labels() == pymupdf.open(f1).get_page_labels()
      and [dd[i].get_label() for i in range(3)] == ["i", "3", "4"], str([dd[i].get_label() for i in range(len(dd))]))
    e2 = run(os.path.join(S, "pdf_enhance.py"), f1)
    t("enhance: a second run keeps the outline, adds no link", "bookmarks 4 (kept) · links 0 added" in e2.stdout, e2.stdout)
else:
    t("enhance: input from cover page", False, "cover page missing")

# ---------------------------------------------------------------- split_volume + rip_volume
VD = os.path.join(TMP, "vol2"); os.makedirs(VD)
vol = os.path.join(VD, "vol.pdf")
d = pymupdf.open()
for i in range(14):
    p = d.new_page(width=W, height=H)
    if i in (7,):
        continue
    if i > 0:
        lines(p, 26, [f"{i}    Studia Romologica 17/2024"], 8)     # running head and folio on one line, as InDesign sets them (18–20 pt)
    if i == 3: lines(p, 80, ["Jan Kowalski", "Uniwersytet Testowy", "Tytuł testowy", "Pełny kontekst badań i kontekst społeczny."])
    if i == 5: lines(p, 80, ["STRESZCZENIE:", "Jan Kowalski", "TYTUŁ TESTOWY", "Artykuł bada szerszy kon-", "tekst historyczny Romów i ich",
                             "losy.", "Słowa kluczowe: Romowie, historia,", "pamięć"])
    if i == 6: lines(p, 80, ["SUMMARY:", "Jan Kowalski", "TEST TITLE", "The article examines the well-", "known context of Roma history.",
                             "Keywords: Roma, history, memory"])
    if i == 10: lines(p, 80, ["Noty o autorach", "Dr Jan Kowalski – historyk, adiunkt w Uni-", "wersytecie Testowym; bada dzieje",
                              "Romów. Kurator wystawy na 59.", "Międzynarodowej Wystawie Sztuki – La Biennale di Venezia.",
                              "Kontakt: jan@example.org", "Anna Nowak – etnolog.", "Kontakt: anna@example.org"])
d.save(vol)
cfg = {"volume": "17", "year": "2024", "publisher": "Komitet Testowy", "pub_date_print": "2024", "pub_date_online": "2026-10-20",
       "license": "CC-BY-NC", "license_url": "https://creativecommons.org/licenses/by-nc/4.0/", "copyright_holder": "Komitet Testowy",
       "volume_pdf": "vol.pdf", "page_offset": 0, "notes_pages": [10, 10], "keep_hyphen": ["well-known"],
       "articles": [{"id": "001", "section": "I", "from": 3, "to": 6, "title_pl": "Tytuł testowy", "title_en": "Test title",
                     "display": "Jan Kowalski", "authors": [["Jan", "Kowalski", "Uniwersytet Testowy", None]], "bio": "Jan Kowalski",
                     "short": "Kowalski_Tytul"},
                    {"id": "002", "section": "III", "from": 8, "to": 9, "title_pl": "Recenzja", "title_en": "Review",
                     "display": "Redakcja „Studia Romologica”", "authors": [], "short": "Recenzja", "license": "NONE",
                     "copyright_holder": "2018 Tom Lantos Institute"}]}
json.dump(cfg, open(os.path.join(VD, "volume.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(TMP, "autorzy.tsv"), "w", encoding="utf-8").write(
    "sortuj\tosoba\torcid\tafiliacja\tnota\tkontakt\tzrodlo\tuwagi\nKowalski\tDr Jan Kowalski\thttps://orcid.org/0000-0002-1825-0097\tUT\t\t\t\t\n")
r = run(os.path.join(S, "rip_volume.py"), os.path.join(VD, "volume.json"))
rows = list(csv.DictReader(open(os.path.join(VD, "srom_master_v3.csv"), encoding="utf-8-sig"))) if r.returncode == 0 else [{}, {}]
a1 = rows[0]
t("rip: abstracts with exact joins, keep_hyphen", a1.get("abstract_pl") == "Artykuł bada szerszy kontekst historyczny Romów i ich losy."
  and a1.get("abstract_en") == "The article examines the well-known context of Roma history.", r.stdout + r.stderr)
t("rip: keywords (EN joined with ;)", a1.get("keywords_pl") == "Romowie, historia, pamięć" and a1.get("keywords_en") == "Roma; history; memory",
  f"{a1.get('keywords_pl')!r} / {a1.get('keywords_en')!r}")
t("rip: bio ends at its contact line, no false split on „Sztuki – La Biennale”",
  (a1.get("bio_note") or "").startswith("Historyk, adiunkt w Uniwersytecie Testowym") and "La Biennale" in (a1.get("bio_note") or ""), a1.get("bio_note"))
t("rip: PDF named with the journal title in full", a1.get("pdf_file", "").startswith("Studia_Romologica_17_2024_")
  and a1.get("pdf_url", "").endswith("/archive/17-2024/" + a1.get("pdf_file", "-")), a1.get("pdf_url"))
t("rip: ORCID from the register", a1.get("authors_struct", "").endswith("|https://orcid.org/0000-0002-1825-0097"))
t("rip: NONE row has no licence URL, own holder", rows[1].get("license") == "NONE" and rows[1].get("license_url") == ""
  and rows[1].get("copyright_holder") == "2018 Tom Lantos Institute")
rows[0]["doi_suffix"] = "q2wexbgk"
rows[0]["title_en"] = "Hand-edited title"                                   # an edit made in the CSV, lost on a re-run
write_csv(os.path.join(VD, "srom_master_v3.csv"), rows)
rr = run(os.path.join(S, "rip_volume.py"), os.path.join(VD, "volume.json"))
again = list(csv.DictReader(open(os.path.join(VD, "srom_master_v3.csv"), encoding="utf-8-sig")))
t("rip: a re-run keeps a minted suffix", again[0]["doi_suffix"] == "q2wexbgk" and again[1]["doi_suffix"] == "todo0002")
t("rip: a re-run names the CSV cells it changes (and only those)",
  "cells changed against the previous srom_master_v3.csv: 1: 001:title_en" in rr.stdout, rr.stdout)
import rip_volume                                                            # noqa: E402
REG = [{"osoba": "Dr Anna Piotrowska", "orcid": "https://orcid.org/0000-0003-1510-8682"},
       {"osoba": "Jan Kowalski-Nowak", "orcid": "https://orcid.org/0000-0002-1825-0097"}]
t("rip: ORCID only on whole words of the register's name (review 20.10.2026)",
  rip_volume.orcid_for("Ann", "Piotrowska", REG) == "" and rip_volume.orcid_for("Anna", "Piotr", REG) == ""
  and rip_volume.orcid_for("Anna", "Piotrowska", REG) == REG[0]["orcid"]
  and rip_volume.orcid_for("Jan", "Kowalski-Nowak", REG) == REG[1]["orcid"] and rip_volume.orcid_for("", "", REG) == "")
s = run(os.path.join(S, "split_volume.py"), os.path.join(VD, "srom_master_v3.csv"), vol, "--out", os.path.join(VD, "split"))
sp = os.path.join(VD, "split", "SROM-17-2024-001.pdf")
t("split: offset from folios, pages of the range", "offset 0 (from folios" in s.stdout and os.path.exists(sp)
  and len(pymupdf.open(sp)) == 4 and "Jan Kowalski" in pymupdf.open(sp)[0].get_text(), s.stdout + s.stderr)

n = len(RES)
print(f"BACKCAT ALL PASS {n}/{n}" if all(RES) else f"BACKCAT FAILED {RES.count(False)}/{n}")
