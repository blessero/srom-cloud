"""On_Culture (Giessen, open-access journal; stage-1 test 5, 28.09.2026: Tittel, "Racial and Social Dimensions of
Antiziganism", On_Culture 10, 2020). What broke the extractor there:
- headings carry the journal's decoration, a leading underscore: "_Abstract", "_Endnotes", "1_Introduction". The
  abstract heading was not recognised (front matter stopped at page 1), the endnotes heading stayed in the text as a
  heading, the section headings came out as "## 1_Introduction"
- the front matter runs over two pages: page 1 the author, bio, keywords, publication date, how to cite (headings in
  capitals); page 2 the title again, "_Abstract" and the abstract, then "1_Introduction"
- block quotations set justified to their own right edge, indented on both sides: every line was short of the text's
  right margin, so each line became a paragraph and the run a "verse" (line breaks and line-end hyphens kept)
- a URL closed by ">" at a line end ("…-6>." | "The English version") swallowed the space after it
- a URL broken after a hyphen with no link target, whose address is written whole elsewhere in the document
  ("mdz-nbn-resol-" | "ving.de" beside "mdz-nbn-resolving.de"): the document decides
- a hyphen before an opening quotation mark ("anti-" | "“gypsy” laws") got a space after it
Runs with PyMuPDF only."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
res = []


def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))


FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit"), "bo": pymupdf.Font("tibo")}
doc = pymupdf.open()
W, H = 430, 650
BS, QS, NS, LEAD, QLEAD, NLEAD = 10.0, 9.0, 8.0, 14, 11, 10
X0, MEAS = 60, 300
QX, QMEAS = 80, 250                     # block quotation: indented on both sides, justified to its own edge


def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    put(pg, 150, 30, "On_Culture: The Open Journal for the Study of Culture", fs=6)
    return pg


def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)


def spread(pg, y, words, fs=BS, x=X0, meas=MEAS):
    """a justified line: every word its own text object, the last word ending exactly at x + meas"""
    wid = sum(FB["rg"].text_length(w, fontsize=fs) for w in words)
    gap = (meas - wid) / (len(words) - 1)
    for w in words:
        x = put(pg, x, y, w, fs=fs) + gap


FILL = ("the police regulations of the early modern state treated the poor and the foreign alike and the "
        "chronicles of the time record the edicts and their failures in every district " * 12).split()
_k = [0]


def words(width, fs=BS, end=""):
    out = []
    while FB["rg"].text_length(" ".join(out + [FILL[_k[0] % len(FILL)]]) + end, fontsize=fs) < width - 8:
        out.append(FILL[_k[0] % len(FILL)]); _k[0] += 1
    return out


def body(pg, y, n, first_indent=True):
    for j in range(n):
        ws = words(MEAS - (12 if j == 0 and first_indent else 0))
        spread(pg, y, ws, x=X0 + (12 if j == 0 and first_indent else 0), meas=MEAS - (12 if j == 0 and first_indent else 0))
        y += LEAD
    return y


# ---- page 1: metadata page (keywords, publication date, how to cite: headings in capitals)
p1 = page()
put(p1, 100, 60, "Published as _Article in On_Culture", fs=BS)
put(p1, X0, 110, "RACIAL AND SOCIAL DIMENSIONS OF ANTIZIGANISM", fs=9.5)
put(p1, X0, 135, "LAURA AUTHOR", fs=9.5)
put(p1, X0, 160, "Laura Author is a research associate at the chair of Political Theory.")
put(p1, X0, 200, "KEYWORDS", fs=9.5)
put(p1, X0, 220, "antiziganism, history of ideas, Kant, Marx, police work, racism")
put(p1, X0, 260, "PUBLICATION DATE", fs=9.5)
put(p1, X0, 280, "Issue 10, April 21, 2021")
put(p1, X0, 320, "HOW TO CITE", fs=9.5)
put(p1, X0, 340, "Author, Laura. “Racial and Social Dimensions.” On_Culture 10 (2020).")

# ---- page 2: title again, _Abstract, abstract (indented, smaller), 1_Introduction, text, a justified quotation
p2 = page()
put(p2, X0, 70, "Racial and Social Dimensions of Antiziganism", fs=15)
put(p2, X0, 100, "_Abstract", fn="bo")
y = 118
for j in range(3):
    spread(p2, y, words(QMEAS, fs=QS), fs=QS, x=QX, meas=QMEAS); y += QLEAD
put(p2, QX, y, "the end of the abstract.", fs=QS); y += 2.4 * LEAD
put(p2, X0, y, "1_Introduction", fn="bo"); y += 1.6 * LEAD
y = body(p2, y, 3, first_indent=False)
spread(p2, y, words(MEAS - 40) + ["first", "anti-"]); y += LEAD              # a full line ending "anti-"
put(p2, X0, y, "“gypsy” laws in England and the following analysis:"); y += LEAD + 4
qlines = [["The", "human", "being", "is", "destined", "by", "his", "reason", "to", "live", "in"],
          ["a", "society", "with", "human", "beings", "and", "in", "it", "to", "cultivate"],
          ["himself", "by", "means", "of", "the", "arts", "and", "the", "sciences", "and"],
          ["struggling", "with", "the", "obstacles", "that", "cling", "to", "his", "na-"]]
for ws in qlines:
    spread(p2, y, ws, fs=QS, x=QX, meas=QMEAS); y += QLEAD
x = put(p2, QX, y, "ture.", fs=QS)
put(p2, x, y - 3, "1", fs=5.5)
y += LEAD + 4
y = body(p2, y, 2, first_indent=False)
x = put(p2, X0, y, "the end of the paragraph.")
put(p2, x, y - 3.5, "2", fs=6)
put(p2, 210, 620, "2", fs=9)

# ---- page 3: a verse quotation (control), the text's end, _Endnotes
p3 = page()
y = 60
y = body(p3, y, 2)
put(p3, X0, y, "as the song has it:"); y += LEAD + 2
for v in ("Green grow the rushes,", "the wind blows over the heath", "and we go on"):
    put(p3, QX, y, v, fs=QS); y += QLEAD
y += 4
x = put(p3, X0, y, "Similar approaches can be adopted in the social research.")
put(p3, x, y - 3.5, "3", fs=6)
y += 2.4 * LEAD
put(p3, X0, y, "_Endnotes", fn="bo"); y += 1.8 * LEAD
NX = X0 + 14
notes = [("1", ["Immanuel Kant, Anthropology (Cambridge: Cambridge University Press, 2010), 420."]),
         ("2", ["Rudiger, Neuester Zuwachs (Leipzig: Kummer), <http://mdz-nbn-resol-",
                "ving.de/urn:nbn:de:bvb:12-bsb10583110-8> in 1782; <https://www.db-",
                "thueringen.de/receive/dbt_mods_00046963>. Grellmann, Historischer Versuch, <http://x.org/a-6>.",
                "The English version was published in the same year."]),
         ("3", ["The first edition is available online <http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb1073838> now."])]
for n, ls in notes:
    put(p3, X0, y, n, fs=NS)
    for ln in ls:
        put(p3, NX, y, ln, fs=NS); y += NLEAD
    y += 3
put(p3, 210, 620, "3", fs=9)

tmp = tempfile.mkdtemp()
pdf = os.path.join(tmp, "onc.pdf")
doc.save(pdf)
out = os.path.join(tmp, "onc.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
rd = lambda f: open(os.path.join(tmp, f), encoding="utf-8").read() if os.path.exists(os.path.join(tmp, f)) else ""
md, front, rep = rd("onc.md"), rd("onc_front.md"), rd("onc_extract.md")

t("extracts: EXTRACT OK, 3 notes, 3 markers", "EXTRACT OK" in r.stdout and "notes 3 · markers 3" in r.stdout,
  r.stdout + r.stderr + rep)
t("front matter over two pages up to '1_Introduction': keywords, publication date, title again, abstract",
  all(s in front for s in ("KEYWORDS", "PUBLICATION DATE", "HOW TO CITE", "Racial and Social Dimensions of Antiziganism",
                           "_Abstract", "the end of the abstract."))
  and not any(s in md for s in ("KEYWORDS", "PUBLICATION", "Abstract", "the end of the abstract")), front + "\n---\n" + md[:400])
t("'_Abstract' is an abstract heading (front matter listed up to the text's first heading)",
  "front matter: pages 1–2 up to the heading '1_Introduction'" in rep, rep)
t("'1_Introduction' -> '# 1. Introduction' (level 1, decoration listed)",
  md.startswith("# 1. Introduction\n") and "heading decoration: '1_Introduction' -> '1. Introduction'" in rep, md[:200] + rep)
t("'_Endnotes' is the endnotes heading: not in the text", "Endnotes" not in md and "endnotes section found" in rep, md[-600:])
q = re.findall(r"^> .*$", md, re.M)
t("a justified quotation set to its own right edge is one paragraph (not verse), the line-end hyphen joined",
  any(s.startswith("> The human being is destined") and "cling to his nature.[^1]" in s and "\\" not in s for s in q), q)
t("a verse quotation (short lines, ragged) keeps its line breaks",
  "> Green grow the rushes,\\\n> the wind blows over the heath\\\n> and we go on" in md, md)
t("a hyphen before an opening quotation mark: no space (anti-“gypsy”), listed",
  "anti-“gypsy” laws" in md and "anti-|“gypsy” -> hyphen kept, no space (quotation mark follows)" in rep, rep)
n2 = re.search(r"^\[\^2\]: (.*)$", md, re.M)
n2 = n2.group(1) if n2 else ""
t("a URL closed by '>' at a line end: the space after it kept ('-6>. The English')",
  "<http://x.org/a-6>. The English version" in n2, n2)
t("URL broken after a hyphen, the address written whole elsewhere in the document -> joined, listed",
  "<http://mdz-nbn-resolving.de/urn:nbn:de:bvb:12-bsb10583110-8>" in n2
  and "hyphen removed (the same address elsewhere in the document)" in rep, n2 + rep)
t("URL broken after a hyphen, no link and no evidence -> hyphen kept, flagged",
  "<https://www.db-thueringen.de/receive/dbt_mods_00046963>" in n2 and "db-|thueringen.de" in rep
  and "no link in the PDF — check the address" in rep, n2)

n, ok = len(res), sum(res)
print(f"PDF-ONCULTURE ALL PASS {n}/{n}" if ok == n else f"PDF-ONCULTURE FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
