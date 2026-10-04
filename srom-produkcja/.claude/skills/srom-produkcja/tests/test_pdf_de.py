"""German local-history yearbook layout (stage-1 test 3, 28.09.2026: Neujahrsblätter Lustenau 2010, set in InDesign
from Word text). A hand-set 8-page PDF reproduces what broke the extractor there:
- ragged right, paragraphs marked by space only (no first-line indent): a line short of the measure is not a
  paragraph end; a quotation is indented only ~1 em, with a hanging first line and an inner paragraph opened by a tab
- recto/verso margins differ (a quotation running from a recto onto a verso stays one quotation)
- InDesign control characters in the text layer (U+0007 "indent to here", tabs): tested on clean_text() — PyMuPDF
  cannot write them into a test PDF (they come back as U+FFFD)
- soft hyphens (U+00AD) at line ends and inside lines; a hard hyphen + soft hyphen at a line end
- suspended hyphen at a line end ("Diebs-" | "und"); slashes spaced as the document spaces them (early-modern
  virgules in italic quotations "Betretten/ mit" vs. "Irsigler/Lassotta")
- a marker in the title (the author's note on the title is note 1); the same number raised again at the text's end
- a space set in the marker size before each marker
- endnotes at the end without a heading, numbers on the baseline; a note continued at the top of the next notes
  page; a raised edition number inside a note ("Neustadt ²1990")
- a figure caption beside the image, without "Abb."; the paragraph interrupted by the figure page goes on in lower case
- a quoted numbered list with a hanging indent (the number must not become a Markdown list)
- paragraph ends at page breaks: a very short last line ends a paragraph; a full line ending a sentence is listed
Runs with PyMuPDF only."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import pdf_extract as P
res = []

def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit"), "bo": pymupdf.Font("tibo")}
doc = pymupdf.open()
W, H = 470, 684
BS, NS, CS = 9.0, 7.0, 6.0          # body, notes, captions
LEAD = 12
MEAS = 298                           # measure; recto margin 72, verso 100
WORDS = ("die alte Straße lief an der Mühle vorbei und über das Feld und wir alle gingen mit ihr Tag für Tag "
         "durch den Ort bis an den Rhein hinunter " * 20).split()
_w = [0]

def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    return pg

def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)

def words_to(width, fs=BS):
    """next words from WORDS, as many as fit in `width`"""
    out = []
    while True:
        w = WORDS[_w[0] % len(WORDS)]
        if FB["rg"].text_length(" ".join(out + [w]), fontsize=fs) > width:
            return " ".join(out)
        out.append(w); _w[0] += 1

RAG = [0.97, 0.9, 0.99, 0.91, 0.95, 0.89, 0.98, 0.92]   # ragged line lengths (share of the measure)

def para(pg, x, y, n, meas=MEAS, last=None, first_ind=0.0):
    """n ragged lines at x; the last one short (or `last` text appended to a full-ish line); returns next y"""
    for i in range(n):
        xi = x + (first_ind if i == 0 else 0)
        if i == n - 1 and last is not None:
            txt = words_to(RAG[i % 8] * (meas - (xi - x)) - FB["rg"].text_length(" " + last, fontsize=BS))
            put(pg, xi, y, txt + " " + last)
        elif i == n - 1:
            put(pg, xi, y, words_to(0.35 * meas) + ".")
        else:
            put(pg, xi, y, words_to(RAG[i % 8] * (meas - (xi - x))))
        y += LEAD
    return y

def marker(pg, x, y, n, space=True):
    if space:
        x = put(pg, x, y - 3.4, " ", fs=5.2)
    return put(pg, x, y - 3.4, str(n), fs=5.2)

# ---- page 1 (recto): author, title with marker 1, heading, paragraph (marker 2), quotation over the page end
p1 = page()
put(p1, 44, 64, "Anna Beispiel", fs=12)
x = put(p1, 72, 82, "Fahrende im Reichshof", fs=12)
put(p1, x, 82 - 4.5, "1", fs=7)
put(p1, 72, 142, "Das Klischee", "bo")
put(p1, 72, 142, "\x07", "bo")               # an unmapped glyph printed over the "D" (overprint): dropped
y = 166
for _ in range(3):
    put(p1, 72, y, words_to(0.95 * MEAS)); y += LEAD
put(p1, 72, y, words_to(0.93 * MEAS - 40) + " Abstam\u00ad"); y += LEAD           # soft hyphen at a line end
put(p1, 72, y, "mung ist " + words_to(0.9 * MEAS - 70) + " Diebs-"); y += LEAD     # suspended hyphen
put(p1, 72, y, "und Räuberbanden bei Irsigler/Lassotta und bei den Autoren Kiessling/"); y += LEAD
x = put(p1, 72, y, "Dietmar und ein\u00adfach so weiter gilt")
marker(p1, x, y, 2); y += LEAD
y += LEAD                                                                          # space: next paragraph
QX = 82.0                                                                          # quotation: ~1 em in
x = put(p1, QX, y, "„" + words_to(0.85 * (MEAS - 10))); y += LEAD           # hanging first line
for _ in range(2):
    put(p1, QX + 3.6, y, words_to(0.93 * (MEAS - 14))); y += LEAD
put(p1, QX + 3.6, y, words_to(0.4 * MEAS) + "."); y += LEAD                     # inner paragraph end (short)
put(p1, QX + 13, y, words_to(0.97 * (MEAS - 23))); y += LEAD   # inner paragraph: tab, indent
put(p1, QX, y, words_to(0.94 * (MEAS - 10))); y += LEAD
x = put(p1, QX, y, words_to(0.3 * MEAS) + " ")
put(p1, x, y, "scharffer Ruthen/ und Betretten/ mit der Zigeuner-Stöcke/", "it"); y += LEAD
x = put(p1, QX, y, "worauff die Straffe", "it"); put(p1, x, y, " " + words_to(0.8 * MEAS)); y += LEAD

# ---- page 2 (verso): the quotation goes on (margin 100, quotation at 113.8), ends with marker 3; paragraph ending
# in a very short line at the page end (marker 4)
p2 = page()
y = 132
put(p2, 113.8, y, words_to(0.93 * (MEAS - 14))); y += LEAD
x = put(p2, 113.8, y, words_to(0.5 * MEAS) + " vorhanden sein.“"); marker(p2, x, y, 3); y += LEAD
y += LEAD
y = para(p2, 100, y, 5)
for _ in range(30):
    y2 = y
    if y2 > 600:
        break
    y = para(p2, 100, y + LEAD, 4)
x = put(p2, 100, y + LEAD, "des Alten Reiches gilt"); marker(p2, x, y + LEAD, 4); put(p2, x + 5, y + LEAD, ".")

# ---- page 3 (recto): new paragraph at the top; its last line (page end) full, no sentence end: "durchaus ernst"
p3 = page()
y = para(p3, 72, 132, 6)
y += LEAD
y = para(p3, 72, y, 30, last="Lustenau durchaus ernst")

# ---- page 4 (verso): a figure and its caption beside it, no "Abb."
p4 = page()
p4.draw_rect(pymupdf.Rect(103, 121, 400, 651), color=(0, 0, 0))
pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 8, 8), False)
pix.clear_with(200)
p4.insert_image(pymupdf.Rect(103, 121, 400, 651), pixmap=pix)
for i, ln in enumerate(["Steckbrief aus", "dem Jahr 1749.", "Quelle: Vorarlberger", "Landesarchiv"]):
    wdt = FB["rg"].text_length(ln, fontsize=CS)
    put(p4, 90.6 - wdt, 370 + 8 * i, ln, fs=CS)                   # set flush right against the image

# ---- page 5 (recto): the interrupted paragraph goes on in lower case; a quoted numbered list; a paragraph whose
# last line (page end) is full and ends a sentence
p5 = page()
y = para(p5, 72, 132, 3)
y += LEAD
put(p5, 72, y, "Aus dem Bereich nennt die Liste folgende Receptatores:"); y += 2 * LEAD
put(p5, 82.7, y, "5. "); put(p5, 95.7, y, "Zu Aesch bey dem Bauren/ welcher der Bucklete Melck genannt wird/ auch"); y += LEAD
put(p5, 95.7, y, "bey dem oberen Würth geben Unterschlauff. […]"); y += LEAD
put(p5, 82.7, y, "7. ", "it"); put(p5, 95.7, y, "Zu Hochenembs in dem Würths-Haus zum Bock genannt/ kennet alle", "it"); y += LEAD
put(p5, 95.7, y, "Dieb/ und behalt die gestolene Waaren auff.", "it"); y += LEAD
x = put(p5, 82.7, y, "20. Der Wildenmannwirth zu Dorenbüren […].", "it"); marker(p5, x, y, 5, space=False); y += LEAD
y += LEAD
y = para(p5, 72, y, 30, last="bezahlt einer Frau bassgeigen.")

# ---- page 6 (verso): continuation after the sentence end (listed); the text's last paragraph, then a stray "1"
p6 = page()
y = para(p6, 100, 132, 3)
y += LEAD
x = put(p6, 100, y, words_to(0.9 * MEAS)); y += LEAD
x = put(p6, 100, y, "und der eigentümliche Dialekt bilden.")
put(p6, x, y - 3.4, "1", fs=5.2)

# ---- page 7 (recto): endnotes, no heading, number on the baseline + tab; note 4 runs over to page 8
p7 = page()
y = 132
notes = [("1", "Der vorliegende Aufsatz geht auf einen Vortrag zurück."),
         ("2", "Achim Landwehr, Norm. Konstanz 2001, S.56; Etienne François/Hagen Schulze; Mark Häberlein/Martin Zürn."),
         ("3", None),
         ("4", "Wolfgang Scheffknecht, Die Reichsgrafschaft Hohenems und der Reichshof Lustenau im Spiegel der")]
for n, txt in notes:
    put(p7, 72, y, n + " ", fs=NS)
    if txt is None:            # raised edition number inside the note
        x = put(p7, 82, y, "Ernst Schubert, Arme Leute. Neustadt an der Aisch ", fs=NS)
        x = put(p7, x, y - 2.5, "2", fs=4.2)
        put(p7, x, y, "1990, S.268.", fs=NS)
    else:
        put(p7, 82, y, txt, fs=NS)
    y += 9
for _ in range(45):
    put(p7, 72, y, "Nachweise und Hinweise zu den Quellen stehen in der Anmerkung weiter unten fort und fort", fs=NS)
    y += 9
    if y > 600:
        break

# ---- page 8 (verso): the top line continues note 4 (opens with a tab), then note 5
p8 = page()
put(p8, 106, 132, "Hohenems und Lustenau. In: Blumenegg. Bludenz 2004, S.110-144.", fs=NS)
put(p8, 100, 141, "5 ", fs=NS); put(p8, 110, 141, "VLA, HoA 103,25: Jauner- und Diebs-Lista.", fs=NS)
for yy in range(150, 600, 9):
    put(p8, 100, yy, "Weitere Zeilen der Anmerkung fünf mit Nachweisen aus dem Archiv in einer Reihe", fs=NS)

tmp = tempfile.mkdtemp()
pdf = os.path.join(tmp, "de.pdf")
doc.save(pdf)
out = os.path.join(tmp, "de.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
md = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
rep = open(os.path.join(tmp, "de_extract.md"), encoding="utf-8").read() if md else r.stderr
front = open(os.path.join(tmp, "de_front.md"), encoding="utf-8").read() if os.path.exists(os.path.join(tmp, "de_front.md")) else ""
D = md[:3000]
body = [b for b in md.split("\n\n") if b.strip() and not b.startswith("[^")]
defs = dict(re.findall(r"^\[\^(\d+)\]: (.*)$", md, re.M))

t("layout recognised: ragged right, paragraphs marked by space", "ragged right, paragraphs marked by space" in rep, rep[:1500])
t("marker in the title -> ::: przypis-tytulowy with note 1; numbered notes 2–5; marker out of the front matter",
  md.startswith("::: przypis-tytulowy\nDer vorliegende Aufsatz") and sorted(defs) == ["2", "3", "4", "5"]
  and "[^1]" not in front and "Fahrende im Reichshof" in front, (md[:300], sorted(defs), front))
t("the title-note number raised again at the end: issue, comment in its place (not silently dropped)",
  "calls the note on the title" in rep and re.search(r"bilden\.<!-- DO SPRAWDZENIA: [^>]*1[^>]*-->", md) is not None
  and "EXTRACT CHECK 1" in r.stdout, (r.stdout, md[-600:]))
p_a = next((b for b in body if "Abstammung" in b), "")
t("ragged paragraph kept whole (no break at lines short of the measure)",
  p_a.startswith("die alte Straße") and p_a.rstrip().endswith("gilt[^2]"), p_a)
t("soft hyphen at a line end joined; soft hyphen inside a line removed", "Abstammung ist" in md and "einfach so" in md
  and "\u00ad" not in md, p_a)
t("suspended hyphen before 'und' kept with its space: 'Diebs- und'", "Diebs- und Räuberbanden" in md, p_a)
t("roman slash: closed as in the document (Kiessling/Dietmar)", "Kiessling/Dietmar" in md, p_a)
t("italic slash: spaced as the document spaces its virgules (Stöcke/ worauff)", "Stöcke/ worauff" in md, D)
t("space in the marker's size before a marker dropped: 'gilt[^2]'", "gilt[^2]" in md and " [^" not in md, D)
q = [b for b in body if b.startswith("> ")]
t("quotation indented ~1 em: two inner paragraphs, the second running from the recto onto the verso",
  len(q) >= 2 and q[0].startswith("> „") and "Stöcke/ worauff" in q[1] and q[1].rstrip().endswith("vorhanden sein.“[^3]"),
  q[:3])
t("control characters: indent-to-here removed, tab a space, a line opening with either is a typed indent",
  P.clean_text("\t \x07\t Eine") == ("    Eine", True) and P.clean_text("„\x07Die") == ("„Die", False)
  and P.clean_text("5.\t") == ("5. ", False), [P.clean_text("\t \x07\t Eine"), P.clean_text("„\x07Die")])
t("a very short last line at a page end ends the paragraph: the next page starts a new one",
  any(b.rstrip().endswith("gilt[^4].") for b in body), [b[-40:] for b in body])
cap = re.search(r"::: podpis\n(.*?)\n:::", md)
t("caption beside an image, no 'Abb.' -> ::: podpis, one paragraph", cap is not None
  and cap.group(1) == "Steckbrief aus dem Jahr 1749. Quelle: Vorarlberger Landesarchiv", cap and cap.group(0))
t("paragraph interrupted by the figure page, going on in lower case: rejoined, caption after it",
  re.search(r"durchaus ernst [a-zäöü]", md) is not None and md.index("durchaus ernst") < md.index("::: podpis"),
  [b[:60] for b in body])
t("quoted numbered list: one quotation paragraph per item, hanging lines joined, no Markdown list",
  "> 5\\. Zu Aesch bey dem Bauren/ welcher der Bucklete Melck genannt wird/ auch bey dem oberen Würth" in md
  and "> *7. Zu Hochenembs in dem Würths-Haus zum Bock genannt/ kennet alle Dieb/ und behalt" in md
  and re.search(r"^> \*20\. Der Wildenmannwirth", md, re.M) is not None, [b for b in body if "Aesch" in b or "20." in b])
t("full line with a sentence end at a page end: taken as continuing, listed for checking",
  re.search(r"bassgeigen\. [a-zäöü]", md) is not None and "paragraph taken as continuing over the page break" in rep, rep[-2500:])
t("endnotes without a heading parsed; note continued at the top of the next notes page",
  defs.get("4", "").endswith("fort und fort Hohenems und Lustenau. In: Blumenegg. Bludenz 2004, S.110-144.")
  and defs.get("5", "").startswith("VLA, HoA 103,25"), defs)
t("raised edition number inside a note -> superscript digit, not a marker: 'Neustadt an der Aisch ²1990'",
  defs.get("3", "").endswith("Neustadt an der Aisch ²1990, S.268."), defs.get("3"))
t("unmapped glyph printed over mapped text (overprint) dropped and listed", "# Das Klischee" in md
  and "\ufffd" not in md and "(overprint) dropped" in rep, (md[:200], rep[-800:]))
d2 = pymupdf.open(); q2 = d2.new_page(width=W, height=H)
q2.insert_font(fontname="rg", fontbuffer=FB["rg"].buffer)
for i in range(6):
    q2.insert_text((72, 132 + 12 * i), "Zeile mit Text " + ("\x07 und mehr" if i == 2 else "und mehr"), fontname="rg", fontsize=BS)
d2.save(os.path.join(tmp, "u.pdf"))
r2 = subprocess.run([sys.executable, EX, os.path.join(tmp, "u.pdf"), "-o", os.path.join(tmp, "u.md")], capture_output=True, text=True)
rep2 = open(os.path.join(tmp, "u_extract.md"), encoding="utf-8").read()
t("an unmapped glyph not over other text: kept in the text, an issue", "EXTRACT CHECK" in r2.stdout
  and "without a Unicode mapping (U+FFFD)" in rep2 and "\ufffd" in open(os.path.join(tmp, "u.md"), encoding="utf-8").read(), rep2)
n = len(res); ok = sum(res)
print(f"PDF-DE ALL PASS {n}/{n}" if ok == n else f"PDF-DE FAILED {n - ok}/{n}")
