"""G6: end-to-end build of the sample article + failure modes that MUST stop the build."""
import os, re, sys, json, shutil, subprocess, tempfile, zipfile
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(FX, "kanon_refs.json")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
results = []

def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  :: " + str(detail)))

def article_refs(md_path, refs):
    """an article's refs.json holds its author's bibliography only: the fixture's works this text cites (the build
    prints every entry of refs.json, Kanon § 9.2)"""
    keys = set(re.findall(r"@([\w-]+)", open(md_path, encoding="utf-8").read()))
    p = os.path.join(tempfile.mkdtemp(), "refs.json")
    json.dump([r for r in json.load(open(refs, encoding="utf-8")) if r["id"] in keys], open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return p

def build(md_text=None, md_path=None, extra=(), refs=None):
    d = tempfile.mkdtemp()
    if md_text is not None:
        md_path = os.path.join(d, "art.md")
        open(md_path, "w", encoding="utf-8").write(md_text)
    refs = refs or article_refs(md_path, REFS)
    out = os.path.join(d, "out")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), md_path, "--refs", refs,
                        "--out", out, *extra], capture_output=True, text=True)
    stem = os.path.splitext(os.path.basename(md_path))[0]
    rep = open(os.path.join(out, stem + "_report.md"), encoding="utf-8").read() if os.path.exists(os.path.join(out, stem + "_report.md")) else r.stderr
    return r.returncode, out, stem, rep

# ---------------------------------------------------------------- happy path
code, out, stem, rep = build(md_path=os.path.join(FX, "sample_article.md"))
check("sample builds (exit 0, PASS)", code == 0 and "PASS — ready" in rep, rep[:600])
from lxml import etree
z = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
styles = etree.fromstring(z.read("word/styles.xml"))
id2name = {s.get(W + "styleId"): s.find(W + "name").get(W + "val") for s in styles.iter(W + "style") if s.find(W + "name") is not None}
doc = etree.fromstring(z.read("word/document.xml"))
fn = etree.fromstring(z.read("word/footnotes.xml"))
def ptext(p): return "".join(t.text or "" for t in p.iter(W + "t"))
seq = [(id2name.get(p.find(W + "pPr/" + W + "pStyle").get(W + "val")), ptext(p)) for p in doc.iter(W + "p") if p.find(W + "pPr/" + W + "pStyle") is not None]
names = [s for s, _ in seq]
check("para after H1 = no-indent body", seq[1][0] == "Tekst BEZ WCIĘCIA", seq[:3])
check("second para = indented body", seq[2][0] == "Tekst", seq[2])
i_q = names.index("Cytat")
check("para after block quote = indented body (kanon §2)", names[i_q + 1] == "Tekst", names[i_q:i_q + 2])
lst = [p for p in doc.iter(W + "p") if p.find(W + "pPr/" + W + "pStyle") is not None and id2name.get(p.find(W + "pPr/" + W + "pStyle").get(W + "val")) == "Wyliczenie"]
check("list items styled, dash typed + real tab (one style with numbered lists, v3)", [ptext(p) for p in lst] == ["–pierwszy człon;", "–drugi człon;", "–ostatni człon."]
      and all(len(list(p.iter(W + "tab"))) == 1 for p in lst), [ptext(p) for p in lst])
bib = seq[max(i for i, (s, t) in enumerate(seq) if s == "Śródtytuł" and t.lower() == "bibliografia"):]
check("bibliography: only the sections used, without numerals (kanon), in kanon order", [t for s, t in bib if s == "Śródtytuł MAŁE"] ==
      ["Źródła archiwalne", "Źródła terenowe", "Opracowania"], bib)
lit = [t for s, t in bib if s == "Bibliografia"][2:]
check("Opracowania sorted Polish order", [t.split(" ")[0] for t in lit] == ["Ficowski", "Hancock", "Kołaczek", "Mróz"], lit)
sc = [ptext(r) for r in doc.iter(W + "r") if r.find(W + "rPr/" + W + "rStyle") is not None and id2name.get(r.find(W + "rPr/" + W + "rStyle").get(W + "val"), r.find(W + "rPr/" + W + "rStyle").get(W + "val")) == "Kapitaliki"]
check("surnames (only) in small-caps char style", sc == ["Ficowski", "Hancock", "Kołaczek", "Mróz"], sc)
check("author note via role div (Tekst BEZ WCIĘCIA, v3)", seq[-1][0] == "Tekst BEZ WCIĘCIA")
notes = [f for f in fn.iter(W + "footnote") if f.get(W + "type") is None]
nt = [ptext(f) for f in notes]
check("10 real footnotes", len(notes) == 10, len(notes))
check("note 3: mid-note citation unbracketed, no '.;', suffix 'i n.' kept",
      nt[2] == "L. Mróz, Tytuł rozdziału, w: Tytuł tomu, red. A. Kowalski, Wydawnictwo, Kraków 2011, s. 90; zob. też M. Kołaczek, Tytuł artykułu, „Studia Romologica”, 2012, nr 5, s. 215 i n.", nt[2])
check("note 2 Ibidem", nt[1] == "Ibidem, s. 17.", nt[1])
check("note 6 short form after literal notes", nt[5] == "Ficowski, Cyganie na polskich drogach…, s. 51.", nt[5])
check("note 8 short form after multi-work note", nt[7] == "Ficowski, Cyganie na polskich drogach…, s. 60.", nt[7])
check("literal archival note untouched", nt[3].startswith("Archiwum Narodowe w Krakowie (dalej: ANK)"), nt[3])
ital = [ptext(r) for r in fn.iter(W + "r") if r.find(W + "rPr/" + W + "rStyle") is not None]
check("Ibidem italic via char style", "Ibidem" in ital, ital)
refrpr = [r for r in list(doc.iter(W + "r")) + list(fn.iter(W + "r")) if (r.find(W + "footnoteReference") is not None or r.find(W + "footnoteRef") is not None) and r.find(W + "rPr") is not None]
check("footnote markers carry no Word style/formatting", not refrpr, len(refrpr))
fstyle = [s.find(W + "name").get(W + "val") for s in styles.iter(W + "style") if s.get(W + "styleId") == "FootnoteText"]
check("footnote paragraph style renamed to template name", fstyle == ["Przypis"], fstyle)
check("no w:lang anywhere", b"w:lang" not in z.read("word/styles.xml") and b"w:lang" not in z.read("word/document.xml"))
body = seq[1][1]
check("sentence text intact around markers (abbrev. period, closing quote)", "XV w. Jerzy" in body and "marginalizację”" in body)
jsx = open(os.path.join(out, stem + "_ibidem.jsx"), encoding="utf-8").read()
check("ibidem JSX lists notes 2, 7, 9 with short-form fallback", all(f"  {n}: {{" in jsx for n in (2, 7, 9)) and "EXPECTED_TOTAL = 10;" in jsx)
check("postimport JSX has whitelist + total", "EXPECTED_TOTAL = 10;" in open(os.path.join(out, stem + "_postimport.jsx"), encoding="utf-8").read())
check("no ISBN query (Kanon § 9.1, 9.7: ISBN only when the author gives it)", "ISBN" not in open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read())

# the author's whole bibliography is printed (Kanon § 9.2); an early print without a printer is not a gap (§ 0)
eb = os.path.join(tempfile.mkdtemp(), "refs.json")
json.dump([r for r in json.load(open(REFS, encoding="utf-8")) if r["id"] == "ficowski1985"] + [
    {"id": "mw1662", "type": "book", "author": [{"literal": "M. W., M. A."}], "title": "A comedy called The marriage broaker",
     "publisher-place": "London", "issued": {"date-parts": [[1662]]}},
    {"id": "nopub1990", "type": "book", "author": [{"family": "Nowy", "given": "Jan"}], "title": "Książka bez wydawcy",
     "publisher-place": "Kraków", "issued": {"date-parts": [[1990]]}}], open(eb, "w", encoding="utf-8"), ensure_ascii=False)
code_b, out_b, stem_b, rep_b = build(md_text="Tekst[^1] i dalej[^2].\n\n[^1]: [@ficowski1985, s. 15].\n\n[^2]: [@mw1662, s. 30].\n",
                                     refs=eb, extra=("--draft",))
txt_b = open(os.path.join(out_b, stem_b + ".txt"), encoding="utf-8").read()
bib_b = txt_b[txt_b.find("Bibliografia"):]
# inner title inside an italic title (Kanon § 3.4): a separate roman run, in the text, the notes and the bibliography
ib = os.path.join(tempfile.mkdtemp(), "refs.json")
json.dump([{"id": "levin1967", "type": "article-journal", "author": [{"family": "Levin", "given": "Harry"}],
            "title": "A Note on <i>Les Fourberies de Scapin</i>", "container-title": "Yale French Studies", "volume": "38",
            "page": "128–137", "issued": {"date-parts": [[1967]]}}], open(ib, "w", encoding="utf-8"), ensure_ascii=False)
code_i, out_i, stem_i, rep_i = build(md_text="Tekst o *Tytule _wewnętrznym_ tomu*[^1].\n\n[^1]: [@levin1967, s. 130].\n", refs=ib)
zi = zipfile.ZipFile(os.path.join(out_i, stem_i + ".docx"))
def runs(xml, after):
    x = xml[xml.find(after):]
    return [((re.search(r'w:rStyle w:val="([^"]+)"', r) or [None, "roman"])[1], "".join(re.findall(r"<w:t[^>]*>([^<]*)", r)))
            for r in re.findall(r"<w:r>(.*?)</w:r>", x)[:8]]
body_r, note_r = runs(zi.read("word/document.xml").decode(), "Tekst o"), runs(zi.read("word/footnotes.xml").decode(), "Levin")
bib_r = runs(zi.read("word/document.xml").decode(), ">Levin<")
roman = lambda rs, w: any(st == "roman" and w in t for st, t in rs) and not any(st != "roman" and w in t for st, t in rs)
check("inner title roman in body text (*Tytule _wewnętrznym_ tomu*)", roman(body_r, "wewnętrznym") and any("Tytule" in t and st != "roman" for st, t in body_r), body_r)
check("inner title roman at the end of an italic title, in the note and the bibliography (no stray **)",
      roman(note_r, "Les Fourberies") and roman(bib_r, "Les Fourberies") and "**" not in zi.read("word/document.xml").decode(), (note_r, bib_r))
# v1.16: places joined with an en dash (GEN-6), sections in the new order and names, a legacy section name still read (GEN-8)
gb = os.path.join(tempfile.mkdtemp(), "refs.json")
json.dump([{"id": "luc1996", "type": "book", "author": [{"family": "Lucassen", "given": "Leo"}], "title": "Zigeuner", "publisher": "Böhlau",
            "publisher-place": "Köln/Weimar/Wien", "issued": {"date-parts": [[1996]]}},
           {"id": "kant1923", "type": "book", "author": [{"family": "Kant", "given": "Immanuel"}], "title": "Reflexionen", "publisher": "De Gruyter",
            "publisher-place": "Berlin", "issued": {"date-parts": [[1923]]}, "srom-section": "IV"},
           {"id": "www2020", "type": "webpage", "author": [{"family": "Adamski", "given": "Jan"}], "title": "Strona", "container-title": "Serwis",
            "URL": "https://example.org/a", "issued": {"date-parts": [[2020]]}}], open(gb, "w", encoding="utf-8"), ensure_ascii=False)
code, out_g, stem_g, rep_g = build(md_text="A[^1] b[^2] c[^3].\n\n[^1]: [@luc1996, s. 1].\n\n[^2]: [@kant1923, s. 2].\n\n[^3]: [@www2020].\n", refs=gb)
txt_g = open(os.path.join(out_g, stem_g + ".txt"), encoding="utf-8").read()
secs = [ln for ln in txt_g.split("Bibliografia")[-1].splitlines() if ln.strip() in ("Źródła drukowane", "Opracowania", "Źródła internetowe")]
check("v1.16: places with an en dash; sections Źródła drukowane · Opracowania · Źródła internetowe in that order",
      "Köln–Weimar–Wien" in txt_g and "Köln/Weimar" not in txt_g and [x.strip() for x in secs] == ["Źródła drukowane", "Opracowania", "Źródła internetowe"], txt_g[-900:])
code, out_i, stem_i, rep_i = build(md_text="A[^1] b[^2] c[^3] d[^4].\n\n[^1]: [@ficowski1985, s. 1].\n\n[^2]: Zob. [@ficowski1985, s. 2].\n\n"
                                    "[^3]: Zob. też [@ficowski1985, s. 3].\n\n[^4]: [@ficowski1985, s. 4].\n")
txt_i = open(os.path.join(out_i, stem_i + ".txt"), encoding="utf-8").read()
check("v1.16 (GEN-7): lower case after a lead-in (zob. ibidem, zob. też ibidem), capital at the start of a note",
      "Zob. ibidem, s. 2." in txt_i and "Zob. też ibidem, s. 3." in txt_i and "] Ibidem, s. 4." in txt_i, txt_i[-500:])
# article without DOI (online journal): URL in the bibliography in the DOI's place (Kanon § 9.7); with DOI: DOI only
ub = os.path.join(tempfile.mkdtemp(), "refs.json")
json.dump([{"id": "online2019", "type": "article-journal", "author": [{"family": "Wagner", "given": "Sydnee"}], "title": "Bodies",
            "container-title": "Synapsis", "issued": {"date-parts": [[2019, 6, 10]]}, "URL": "https://example.org/bodies/"},
           {"id": "doi2009", "type": "article-journal", "author": [{"family": "Asséo", "given": "Henriette"}], "title": "Travestissement",
            "container-title": "Les Dossiers du Grihl", "issued": {"date-parts": [[2009]]}, "DOI": "10.4000/x.1", "URL": "https://doi.org/10.4000/x.1"}],
          open(ub, "w", encoding="utf-8"), ensure_ascii=False)
code_u, out_u, stem_u, rep_u = build(md_text="A[^1] b[^2].\n\n[^1]: [@online2019].\n\n[^2]: [@doi2009].\n", refs=ub)
bib_u = open(os.path.join(out_u, stem_u + ".txt"), encoding="utf-8").read().split("Bibliografia")[-1]
check("article without DOI: year and URL printed in the bibliography; with DOI: neither DOI nor URL (v1.16, GEN-10)",
      "2019" in bib_u and "https://example.org/bodies/" in bib_u and "10.4000/x.1" not in bib_u and "https://doi.org" not in bib_u and "DOI:" not in bib_u, bib_u)
check("uncited work of the author's list printed, reported", "Książka bez wydawcy" in bib_b and "printed though not cited" in rep_b and "nopub1990" in rep_b, rep_b[:800])
check("early print (1662) without printer: no [BRAK WYDAWCY]; a 1990 book without publisher still has it",
      "marriage broaker, London 1662" in txt_b and "Książka bez wydawcy, [BRAK WYDAWCY], Kraków 1990" in bib_b, txt_b[-800:])
q_b = open(os.path.join(out_b, stem_b + "_pytania.md"), encoding="utf-8").read()
check("uncited entry with [BRAK WYDAWCY]: a query row for the author (the build fails on it)", "nopub1990" in q_b, q_b[-600:])
# E15: the no-page context is the last 90 characters before the note; a byte cut split "ó" and build.py died on stderr
code_8, out_8, stem_8, rep_8 = build(md_text="Tekst " + "ó" * 60 + "x[^1].\n\n[^1]: [@ficowski1985].\n", extra=("--draft",))
q_8 = open(os.path.join(out_8, stem_8 + "_pytania.md"), encoding="utf-8").read() if os.path.exists(os.path.join(out_8, stem_8 + "_pytania.md")) else rep_8[-400:]
check("no-page context cut on a character boundary (E15): build runs, query row has whole letters",
      "óx" in q_8 and "\ufffd" not in q_8, q_8[-400:])

# ---------------------------------------------------------------- failure modes
def fails(label, md, needle, extra=()):
    code, out, stem, rep = build(md_text=md, extra=extra)
    check(label, code == 1 and needle in rep, rep[:900])
fails("E15: two title-note blocks -> build error naming the one-block form (handoff.md)",
      "::: przypis-tytulowy\nNota o przekładzie.\n:::\n\n::: przypis-tytulowy\nPodziękowania.\n:::\n\nTekst[^1].\n\n[^1]: [@ficowski1985, s. 15].\n",
      "2 title-note blocks")

fails("unknown citation key stops the build", "Tekst[^1].\n\n[^1]: [@nieistnieje, s. 5].\n", "citation keys not in refs")
fails("marker without definition stops the build (pandoc alone would print '[^2]')", "Tekst[^1] i[^2].\n\n[^1]: Nota.\n", "[^2] has no definition")
code, out, stem, rep = build(md_text="# 1. WSTĘP\n\nTekst.\n\n## 1.2. Ujęcia\n\nTekst.\n\n# II. DALEJ\n\nTekst.\n\n# 1989 I POTEM\n\nTekst.\n")
hd = ["".join(t.text or "" for t in p.iter(W + "t")) for p in etree.fromstring(zipfile.ZipFile(os.path.join(out, stem + ".docx")).read("word/document.xml")).iter(W + "p")]
check("headings unnumbered (kanon §2): '1.', '1.2.', 'II.' dropped with a warning, a year kept",
      code == 0 and "WSTĘP" in hd and "Ujęcia" in hd and "DALEJ" in hd and "1989 I POTEM" in hd and rep.count("heading number removed") == 3, (hd, rep[:600]))
sty = zipfile.ZipFile(os.path.join(out, stem + ".docx")).read("word/styles.xml").decode()
def jc_of(name):
    m = re.search(r'<w:style [^>]*>(?:(?!</w:style>).)*?<w:name w:val="' + re.escape(name) + r'"/>((?:(?!</w:style>).)*)</w:style>', sty, re.S)
    j = re.search(r'<w:jc w:val="(\w+)"', m.group(1)) if m else None
    return j.group(1) if j else None
check("DOCX styles carry the template's alignment (InDesign keeps a missing one as a left-align override)",
      [jc_of(n) for n in ("Tekst", "Tekst BEZ WCIĘCIA", "Przypis", "Cytat", "Bibliografia", "Śródtytuł")] == ["both"] * 5 + ["left"],
      [jc_of(n) for n in ("Tekst", "Tekst BEZ WCIĘCIA", "Przypis", "Cytat", "Bibliografia", "Śródtytuł")])
check("DOCX default font is the template's (no Word theme font for the import to carry into italic runs)",
      re.search(r'<w:docDefaults>.*?<w:rFonts w:ascii="Cambria"', sty, re.S) is not None and "asciiTheme" not in re.search(r"<w:docDefaults>.*?</w:docDefaults>", sty, re.S).group(0),
      re.search(r"<w:docDefaults>.*?</w:docDefaults>", sty, re.S).group(0)[:300])
fails("heading level 3 stops the build", "# 1. A\n\n### za głęboko\n\nTekst.\n", "heading level 3")
code, out, stem, rep = build(md_text="Tekst.\n\n1. pierwszy;\n2. drugi.\n")
nl = [p for p in etree.fromstring(zipfile.ZipFile(os.path.join(out, stem + ".docx")).read("word/document.xml")).iter(W + "p")]
nl_txt = ["".join(t.text or "" for t in p.iter(W + "t")) for p in nl]
check("numbered list: typed numbers + real tab, list_numbered style", code == 0 and "1.pierwszy;" in nl_txt and "2.drugi." in nl_txt and sum(1 for p in nl for _ in p.iter(W + "tab")) == 2, (code, nl_txt, rep[:500]))
fails("image stops the build", "Tekst ![x](a.png) dalej.\n", "image in text flow")
fails("literal + CSL entries in one section stop the build",
      "Tekst[^1].\n\n[^1]: [@ficowski1985, s. 5].\n\n::: {#bibliografia}\n# Bibliografia\n\n## Opracowania\n\nRęczny wpis.\n:::\n", "both literal entries and CSL entries")
code, out, stem, rep = build(md_text="Jak pisał, „cytat bez strony”[^1].\n\n[^1]: [@ficowski1985].\n")
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("quotation cited without page: builds, placeholder not printed, author asked for the page", code == 0 and "cytat bez numeru strony" in q and "| 1 | ficowski1985" in q and "[BRAK" not in open(os.path.join(out, stem + ".txt"), encoding="utf-8").read(), q + rep[:500])
# a British source (Manchester UP): ‘single quotes’ and the marker after the stop; an apostrophe is not a quotation
code, out, stem, rep = build(md_text="Todorova notes that it began ‘to acquire different overtones’.[^1] Such is Albania’s "
                             "past.[^2] The Balkans are ‘Europe’s abnormals’, a phrase of Bjelić’s.[^3] We know “this”.[^4]\n\n"
                             "[^1]: [@ficowski1985].\n\n[^2]: [@mroz1998].\n\n[^3]: [@ficowski1985].\n\n[^4]: [@mroz1998].\n",
                             extra=("--source",))
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
rows = {r.split("|")[3].strip(): r for r in q.splitlines() if r.startswith("| ")}
check("English source: ‘quotation’.[^1] and “quotation”.[^4] -> page asked; an apostrophe (Albania’s) and a possessive "
      "after a closed quotation (Bjelić’s) -> whole work", "cytat bez numeru" in rows.get("1", "") and "cytat bez numeru"
      in rows.get("4", "") and "całości" in rows.get("2", "") and "całości" in rows.get("3", ""), q)
code, out, stem, rep = build(md_text="> Cytat blokowy[^1].\n\n[^1]: [@mroz1998].\n")
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("block quote cited without page: builds, listed as quotation query", code == 0 and "cytat bez numeru strony" in q, q + rep[:500])
noplace = os.path.join(tempfile.mkdtemp(), "np.json")
json.dump([{"id": "bezmiejsca", "type": "book", "author": [{"family": "Nowak", "given": "Jan"}], "title": "Książka", "publisher": "Wyd.", "issued": {"date-parts": [[1950]]}}], open(noplace, "w"), ensure_ascii=False)
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@bezmiejsca, s. 3].\n", refs=noplace)
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("missing place of publication -> [BRAK MIEJSCA] stops the build, author asked", code == 1 and "[BRAK MIEJSCA]" in rep and "bezmiejsca" in q, rep[:700] + q)
unsigned = os.path.join(tempfile.mkdtemp(), "us.json")
json.dump([{"id": "list1900", "type": "chapter", "title": "Lettre au Père", "container-title": "Relations", "editor": [{"family": "Thwaites", "given": "Reuben"}],
            "publisher": "Burrows", "publisher-place": "Cleveland", "issued": {"date-parts": [[1900]]}}], open(unsigned, "w"), ensure_ascii=False)
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@list1900, s. 314].\n", refs=unsigned)
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("unsigned text in a collection: builds title-first, listed for the editors to establish the author (§ 7.2)",
      code == 0 and "tekst bez autora w tomie zbiorowym" in q and "list1900" in q, q + rep[:400])
tagged = os.path.join(tempfile.mkdtemp(), "tg.json")
json.dump([{"id": "tagged", "type": "thesis", "author": [{"family": "Nowak", "given": "Jan"}], "title": "Tożsamość w Anglii, <i>c.</i> 1607–1623",
            "publisher": "Uniwersytet", "issued": {"date-parts": [[2023]]}}], open(tagged, "w"), ensure_ascii=False)
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@tagged, s. 3].\n", refs=tagged, extra=("--draft",))
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("query sheet: a title's CSL rich-text tags (<i>c.</i>) are not printed in the row", "c. 1607" in q and "<i>" not in q, q)
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@bezmiejsca, s. 3].\n", refs=noplace, extra=("--draft",))
check("--draft lets [BRAK …] through as warning", code == 0 and "[BRAK MIEJSCA]" in rep, rep[:700])
code, out, stem, rep = build(md_text="O dziejach Cyganów pisano wiele[^1].\n\n[^1]: [@ficowski1985]; zob. [@mroz1998].\n")
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("whole-work reference (no quote): builds, listed for the editor to confirm", code == 0 and q.count("odwołanie do całości dzieła") == 2 and "[BRAK" not in open(os.path.join(out, stem + ".txt"), encoding="utf-8").read(), q)
code, out, stem, rep = build(md_text="Tekst **pogrubiony** i __podkreślony__.\n")
check("bold removed with warning (kanon §3.4), build passes", code == 0 and "bold removed" in rep, rep[:700])
code, out, stem, rep = build(md_text="Tekst *z tytułem _wewnętrznym_ w środku*.\n")
check("nested italics: inner run roman, no warning (§ 3.4)", code == 0 and "nested italics" not in rep, rep[:700])

code, out, stem, rep = build(md_text="A[^1] b[^2].\n\n[^1]: [@ficowski1985, s. 5].\n\n[^2]: Szerzej o tym pisze [@ficowski1985, s. 7].\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()
check("Ibidem that would stand mid-sentence is printed as the short form", code == 0 and "Szerzej o tym pisze Ficowski, Cyganie na polskich drogach…, s. 7." in txt and "replaced by the short form" in rep, txt + rep[:900])
code, out, stem, rep = build(md_text="A[^1] b[^2] c[^3] d[^4].\n\n[^1]: [@ficowski1985, s. 5].\n\n[^2]: Uwaga. Zob. [@ficowski1985], "
                             "gdzie więcej o tym.\n\n[^3]: [@ficowski1985, s. 7] (przekład własny).\n\n[^4]: [@ficowski1985, {akt 4, sc. 1, w. 782–806}].\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()
check("Ibidem after a lead-in with the sentence going on ('Zob. Ibidem, gdzie …', West Ohueri n. 53) -> short form; "
      "an author's bracketed remark or a drama locator (akt, sc., w.) after it does not continue the sentence -> Ibidem kept",
      code == 0 and "Zob. Ficowski, Cyganie na polskich drogach…, gdzie" in txt and "Ibidem, s. 7 (przekład własny)" in txt
      and "Ibidem, akt 4, sc. 1, w. 782–806." in txt,
      txt + rep[:900])
code, out, stem, rep = build(md_text="A[^1] b[^2].\n\n[^1]: ANK, 29/456, sygn. 12, k. 41; [@ficowski1985, s. 5].\n\n[^2]: [@ficowski1985, s. 7].\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()
check("after a note citing an archival unit AND a work, the next note gets the short form, not Ibidem", code == 0 and "[2] Ficowski, Cyganie na polskich drogach…, s. 7." in txt, txt)

code, out, stem, rep = build(md_text="Tekst <!-- uwaga redakcji --> dalej[^1].\n\n<!-- luźna notatka -->\n\n[^1]: [@ficowski1985, s. 5].\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()
check("editor comments stripped from the output, text joined cleanly", code == 0 and "uwaga" not in txt and "Tekst dalej" in txt, txt)
code, out, stem, rep = build(md_text="Cytat „z polskiego oryginału”[^1]. <!-- PRZYWRÓCIĆ ORYGINAŁ: [@ficowski1985, s. 15] -->\n\n[^1]: [@ficowski1985, s. 15].\n")
check("comments never block (PRZYWRÓCIĆ included); listed; the citation inside is not counted", code == 0 and "PRZYWRÓCIĆ" in rep and "footnotes: 1 " in rep, rep[:900])

pref = os.path.join(tempfile.mkdtemp(), "p.json")
json.dump([{"id": "heusch1966", "type": "book", "author": [{"family": "Heusch", "given": "Luc", "dropping-particle": "de"}],
            "title": "À la découverte des Tsiganes", "publisher": "Institut de Sociologie", "publisher-place": "Bruxelles", "issued": {"date-parts": [[1966]]}},
           {"id": "gus2022", "type": "report", "author": [{"literal": "Główny Urząd Statystyczny"}], "title": "Raport",
            "publisher": "GUS", "publisher-place": "Warszawa", "issued": {"date-parts": [[2022]]}}], open(pref, "w"), ensure_ascii=False)
code, out, stem, rep = build(md_text="A[^1] B[^2].\n\n[^1]: [@heusch1966, s. 5].\n\n[^2]: [@gus2022, s. 3].\n", refs=pref)
zz = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
dx = etree.fromstring(zz.read("word/document.xml"))
sid = {s_.get(W + "styleId"): s_.find(W + "name").get(W + "val") for s_ in etree.fromstring(zz.read("word/styles.xml")).iter(W + "style") if s_.find(W + "name") is not None}
scs = ["".join(t.text or "" for t in r.iter(W + "t")) for r in dx.iter(W + "r") if r.find(W + "rPr/" + W + "rStyle") is not None and sid.get(r.find(W + "rPr/" + W + "rStyle").get(W + "val")) == "Kapitaliki"]
check("particle 'de' outside small caps, institution not small-capped (kanon §9.3)", code == 0 and scs == ["Heusch"], (code, scs, rep[:500]))

code, out, stem, rep = build(md_text="A[^1] b[^2].\n\n[^1]: [@ficowski1985, s. 5].\n\n[^2]: ANK, 29/456, sygn. 12, k. 41; [@ficowski1985, s. 7].\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read()
check("Ibidem that would follow an archival reference in the same note -> short form", code == 0 and "k. 41; Ficowski, Cyganie na polskich drogach…, s. 7." in txt, txt)

# ---- tables, verse, interlinear examples reach the DOCX with template styles only
blk = open(os.path.join(FX, "blocks.md"), encoding="utf-8").read()
code, out, stem, rep = build(md_text=blk)
zz = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
dx = etree.fromstring(zz.read("word/document.xml"))
sid = {s_.get(W + "styleId"): s_.find(W + "name").get(W + "val") for s_ in etree.fromstring(zz.read("word/styles.xml")).iter(W + "style") if s_.find(W + "name") is not None}
used = Counter(sid.get(p.find(W + "pPr/" + W + "pStyle").get(W + "val")) for p in dx.iter(W + "p") if p.find(W + "pPr/" + W + "pStyle") is not None)
check("table/verse/example build PASS with template styles only", code == 0 and all(k in used for k in ("Cytat WIERSZ", "Tabela TYTUŁ", "Tabela TREŚĆ", "Podpis", "Przykład FORMA", "Przykład GLOSA", "Przykład PRZEKŁAD")), (code, dict(used), rep[:800]))
verse_p = [p for p in dx.iter(W + "p") if p.find(W + "pPr/" + W + "pStyle") is not None and sid.get(p.find(W + "pPr/" + W + "pStyle").get(W + "val")) == "Cytat WIERSZ"]
check("verse keeps its forced line breaks (w:br)", verse_p and len(list(verse_p[0].iter(W + "br"))) == 2, [etree.tostring(p)[:300] for p in verse_p])
form_p = [p for p in dx.iter(W + "p") if p.find(W + "pPr/" + W + "pStyle") is not None and sid.get(p.find(W + "pPr/" + W + "pStyle").get(W + "val")) == "Przykład FORMA"]
check("interlinear columns become real tabs (w:tab), no tab characters in text", form_p and len(list(form_p[0].iter(W + "tab"))) == 4 and not any("\t" in (t.text or "") for t in dx.iter(W + "t")), [etree.tostring(p)[:400] for p in form_p])
fails("code block outside ::: przyklad stops the build", "Tekst.\n\n```\nkod\n```\n", "::: przyklad")
fails("@key without brackets (author-in-text) stops the build", "Jak pisze @ficowski1985 [s. 5], tak.\n", "author-in-text")
fails("[-@key] (author suppressed) stops the build", "Tekst[^1].\n\n[^1]: Por. [-@mroz1998, s. 7].\n", "suppresses the author")

fails("unknown bibliography section name stops the build", "Tekst.\n\n::: {#bibliografia}\n# Bibliografia\n\n## Archiwalia\n\nWpis.\n:::\n", "unknown bibliography section")

# ---- motto, dialogue, transcript speaker (house style v2)
dl = open(os.path.join(FX, "dialog.md"), encoding="utf-8").read()
code, out, stem, rep = build(md_text=dl)
dx2 = etree.fromstring(zipfile.ZipFile(os.path.join(out, stem + ".docx")).read("word/document.xml"))
sid2 = {s_.get(W + "styleId"): s_.find(W + "name").get(W + "val") for s_ in etree.fromstring(zipfile.ZipFile(os.path.join(out, stem + ".docx")).read("word/styles.xml")).iter(W + "style") if s_.find(W + "name") is not None}
seq2 = []
for p in dx2.iter(W + "p"):
    ps = p.find(W + "pPr/" + W + "pStyle")
    runs = []
    for r in p.iter(W + "r"):
        rs = r.find(W + "rPr/" + W + "rStyle")
        runs.append((sid2.get(rs.get(W + "val")) if rs is not None else None, "".join(t.text or "" for t in r.iter(W + "t"))))
    seq2.append((sid2.get(ps.get(W + "val")) if ps is not None else None, runs))
names2 = [x[0] for x in seq2]
check("motto: own style, title inside it roman (Proste), next paragraph unindented", code == 0 and names2[0] == "Motto" and any(r == ("Proste", "O fotografii") for r in seq2[0][1]) and names2[1] == "Tekst BEZ WCIĘCIA", (names2, seq2[0]))
dlg = [x for x in seq2 if x[0] == "Cytat"]
check("dialogue: 4 turns in Cytat, speaker labels in Pogrubienie, continuation turn plain", len(dlg) == 4 and [r[0][0] for r in (x[1] for x in dlg)] == ["Pogrubienie"] * 3 + [None] and dlg[0][1][0][1] == "Przewodniczący Coe:", dlg)
check("paragraph after a dialogue is indented (as after a block quote)", names2[names2.index("Cytat") + 4] == "Tekst", names2)
i_m = names2.index("Mówca")
check("transcript: speaker line + affiliation line, speech starts unindented", names2[i_m:i_m + 3] == ["Mówca", "Afiliacja", "Tekst BEZ WCIĘCIA"], names2[i_m:i_m + 3])

# ---- proof of an English source (before translation): always a reading copy, never a PASS/FAIL gate
code, out, stem, rep = build(md_text="The first records date from the “fifteenth century”.[^1]\n\n[^1]: [@ficowski1985, s. 15].\n", extra=("--proof",))
check("--proof: English source gives _korekta.docx with the Polish apparatus, exit 0", code == 0 and os.path.exists(os.path.join(out, stem + "_korekta.docx")) and "PROOF" in rep and not os.path.exists(os.path.join(out, stem + "_ibidem.jsx")), rep[:600])
# ---- translator's query rows merged into the one sheet per article
qcsv = os.path.join(tempfile.mkdtemp(), "q.csv")
open(qcsv, "w", encoding="utf-8-sig").write("adresat;rodzaj;przypis;dzieło;szczegóły\nautor;TERM-OPEN;3;;termin 'absence-ing'\n")
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@ficowski1985, s. 5].\n", extra=("--queries", qcsv))
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("--queries: srom-tlumacz rows merged into _pytania", code == 0 and "TERM-OPEN" in q and "absence-ing" in q, q)
# E6: a query row naming the frozen source's note label gets the printed note number
srcp = os.path.join(tempfile.mkdtemp(), "src.md")
open(srcp, "w", encoding="utf-8").write("A[^a1] b[^a2].\n\n[^a1]: Pierwszy.\n\n[^a2]: Drugi.\n")
q6 = os.path.join(tempfile.mkdtemp(), "q6.csv")
open(q6, "w", encoding="utf-8-sig").write("adresat;rodzaj;przypis;dzieło;szczegóły\nautor;AUTHOR-QUERY;a2;;pytanie\n")
code, out, stem, rep = build(md_text="Tekst [@ficowski1985, s. 3], A[^1] dalej[^t1] i b[^2].\n\n[^1]: Pierwszy.\n\n[^t1]: Uwaga – przyp. tłum.\n\n[^2]: Drugi.\n", extra=("--queries", q6, "--pair-src", srcp))
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("E6: source label a2 -> printed note 3 (main-text citation counted; translator note is in the * series, kanon § 7.1)", "| autor | AUTHOR-QUERY | 3 |" in q, q)
code, out, stem, rep = build(md_text="::: przypis-tytulowy\nPrzekład z języka angielskiego: Jan Nowak.\n:::\n\nTekst.\n")
check("title note: asterisk-note style, reminder in the report", code == 0 and "asterisk series" in rep and "title note" in rep, rep[:600])

# a citation in the title note (German source, 28.09.2026): first citation there, the numbered notes unshifted, the
# later citation a short form (never Ibidem: the title note is in the asterisk series)
code, out, stem, rep = build(md_text="::: przypis-tytulowy\nNach Landwehr [@ficowski1985, s. 3].\n\nZweiter Absatz.\n:::\n\n"
                                     "# Titel\n\nTekst[^1] dalej[^2].\n\n[^1]: [@ficowski1985, s. 5].\n\n[^2]: Drugi.\n")
zx = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
body, fnx = zx.read("word/document.xml").decode(), zx.read("word/footnotes.xml").decode()
fn_texts = ["".join(t.text or "" for t in f.iter(W + "t")) for f in etree.fromstring(fnx.encode()).iter(W + "footnote")
            if f.get(W + "id") not in ("-1", "0")]
check("citation in the title note: rendered inside it (first citation), 2 numbered notes, the next one a short form, "
      "no empty paragraph left at the top", code == 0 and len(fn_texts) == 2 and "Cyganie na polskich drogach, Wydawnictwo" in
      re.sub(r"\s+", " ", "".join(t.text or "" for t in etree.fromstring(body.encode()).iter(W + "t")))
      and fn_texts[0].strip().startswith("Ficowski, ") and "Ibidem" not in fn_texts[0] and "Zweiter Absatz" in body
      and "multi-paragraph footnote" not in rep, (rep[:900], fn_texts))

code, out, stem, rep = build(md_text="::: przypis-tytulowy\nNach [@ficowski1985, s. 3].\n:::\n\nTekst[^1] dalej[^2].\n\n"
                                     "[^1]: Pierwszy.\n\n[^2]: Zob. [@ficowski1985].\n")
q = open(os.path.join(out, stem + "_pytania.md"), encoding="utf-8").read()
check("citing title note: query rows keep the printed note numbers (whole-work citation in note 2, not 3)",
      re.search(r"\| 2 \| ficowski1985 \|", q) is not None and "| 3 |" not in q, q)

# refs `note` opening "word:" is swallowed by pandoc's citeproc (read as a CSL field): an error, not silent loss
nr = os.path.join(tempfile.mkdtemp(), "note_refs.json")
json.dump([{"id": "nied2003", "type": "book", "author": [{"family": "Niederhäuser", "given": "A."}], "title": "Am Rande",
            "publisher": "X", "publisher-place": "St. Gallen", "issued": {"date-parts": [[2003]]},
            "note": "przypisy: t. 9, s. 52–53"}], open(nr, "w", encoding="utf-8"), ensure_ascii=False)
code, out, stem, rep = build(md_text="Tekst[^1].\n\n[^1]: [@nied2003, s. 5].\n", refs=nr)
check("refs note 'przypisy: …' (read by pandoc as a field, lost) -> build error naming it", code == 1 and "nied2003: note" in rep, rep[:600])

# kanon §8.6: a URL is plain text, never a hyperlink; §7.4: a note may have several paragraphs (flagged)
code, out, stem, rep = build(md_text="Zob. [serwis](https://przyklad.pl/tekst) i <https://przyklad.pl/b>[^1].\n\n"
                                     "[^1]: Pierwszy akapit.\n\n    Drugi akapit przypisu.\n")
zx = zipfile.ZipFile(os.path.join(out, stem + ".docx"))
body = zx.read("word/document.xml").decode()
fnx = zx.read("word/footnotes.xml").decode()
check("hyperlinks become plain text, URL kept as text (kanon §8.6)", code == 0 and "<w:hyperlink" not in body
      and "https://przyklad.pl/b" in body and "serwis" in body, rep[:600])
check("multi-paragraph footnote kept (2 paragraphs) and flagged (kanon §7.4)",
      fnx.count("Drugi akapit przypisu") == 1 and "multi-paragraph footnote" in rep, rep[:600])

# the author's remark in brackets after a citation (stage-1 test 5, Tittel: "…, 63 (my translation)."): no layout period
# before the bracket; an abbreviation that ends the citation keeps its period
code, out, stem, rep = build(md_text="A[^1] b[^2] c[^3].\n\n[^1]: [@ficowski1985, s. 15] (tłum. własne).\n\n"
                                     "[^2]: [@hancock2007, s. 3 i n.] (cytat na s. 4).\n\n"
                                     "[^3]: [@mroz2011, s. 90]. (Zdanie autora w nawiasie.)\n")
txt = open(os.path.join(out, stem + ".txt"), encoding="utf-8").read() if os.path.exists(os.path.join(out, stem + ".txt")) else rep
check("a bracketed remark after a citation: 's. 15 (tłum. własne).' — no period before the bracket",
      "Kraków 1985, s. 15 (tłum. własne)." in txt and "s. 15. (" not in txt, txt[:900])
check("… but an abbreviation ending the citation keeps its period ('s. 3 i n. (cytat na s. 4).')",
      "s. 3 i n. (cytat na s. 4)." in txt, txt[:900])
check("… and a sentence in brackets after the citation's own full stop is untouched", "s. 90. (Zdanie autora w nawiasie.)" in txt, txt[:900])

# the printed bibliography for the Crossref deposit (srom-quant <citation_list>)
code, out, stem, rep = build(md_path=os.path.join(FX, "sample_article.md"))
cit = json.load(open(os.path.join(out, stem + "_citations.json"), encoding="utf-8")) if os.path.exists(os.path.join(out, stem + "_citations.json")) else []
fic = [c for c in cit if c["key"] == "ficowski1985"]
check("_citations.json: every printed entry as plain text, CSL entries with their key (and DOI), literal entries keyless",
      len(cit) >= 3 and fic and fic[0]["text"].startswith("Ficowski Jerzy, Cyganie na polskich drogach")
      and not any("smallcaps" in c["text"] or "](" in c["text"] or "*" in c["text"] for c in cit)
      and any(c["key"] is None for c in cit), [c for c in cit if "smallcaps" in c["text"] or "](" in c["text"] or "*" in c["text"]] or cit[:3])

# keying fault that prints wrong without failing (MB 02.10.2026, Ostendorf): a person keyed as a literal name (full
# name in the notes, § 7.2) -> report warning; an institution and a pseudonym stay silent. Italics inside an italic
# title (foreign word, title in a title) are right by § 3.4: no report by reference
md = "---\ntitle: T\n---\n\nA [@w1, s. 1]. B [@w2, s. 2].\n"
d = tempfile.mkdtemp(); rp = os.path.join(d, "refs.json")
json.dump([{"id": "w1", "type": "chapter", "title": "<i>Divide et impera</i>: Race (<i>Cigano</i>)", "container-title": "V",
            "author": [{"family": "O’Reilly", "given": "William"}], "editor": [{"literal": "Gudmundur Hálfdánarson"}],
            "publisher": "P", "publisher-place": "Pisa", "issued": {"date-parts": [[2003]]}},
           {"id": "w2", "type": "book", "title": "On <i>Antony and Cleopatra</i>", "author": [{"literal": "A Gentleman of Elvas"}],
            "editor": [{"literal": "Preussische Akademie der Wissenschaften"}, {"literal": "Federal Writers’ Project"}],
            "publisher": "P", "publisher-place": "M", "issued": {"date-parts": [[2003]]}}], open(rp, "w", encoding="utf-8"), ensure_ascii=False)
code, out, stem, rep = build(md, refs=rp, extra=["--draft"])
warn = rep.split("## Warnings")[-1]
check("literal person name -> warning; legit literals silent; no by-reference report for italics inside a title (§ 3.4)",
      "“Gudmundur Hálfdánarson”" in warn and "Elvas" not in warn and "Akademie" not in warn and "Writers" not in warn
      and "italics inside a title" not in warn, warn)

# typography never left to memory (MB 04.10.2026): text normalize.py would still change fails the build; a proof warns
md = "---\ntitle: T\n---\n\nTekst...  z \"cytatem\" [@w1, s. 1].\n"
code, out, stem, rep = build(md, refs=rp)
code2, _, _, rep2 = build(md, refs=rp, extra=["--draft"])
check("not normalised: final build fails and names normalize.py; --draft (srom-tlumacz) only warns",
      code == 1 and "not normalised" in rep.split("## Warnings")[0] and "normalize.py" in rep
      and "not normalised" in rep2.split("## Warnings")[-1], rep[:800])

n, ok = len(results), sum(results)
print(f"E2E ALL PASS {n}/{n}" if ok == n else f"E2E FAILED {n - ok}/{n}")
