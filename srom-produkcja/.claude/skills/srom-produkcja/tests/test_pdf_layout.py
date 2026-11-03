"""Journal-layout PDF (the first real stage-1 test, 27.09.2026: an English humanities journal set by a
typesetting system, not by Word). A hand-set 3-page PDF reproduces what broke the extractor there:
- italic font known only by an obfuscated name with a style suffix (AdvOTa14f9db0.I+20)
- a note's number and first words on a raised baseline, the rest of its first line lower ("2 Smith, 35" / "–69.")
- a note whose whole first line, number included, sits on one baseline (number only smaller)
- a superscript ("XVIIᵉ") inside a note line
- section headings in capitals *smaller* than the body; a two-line one
- opening words in small capitals; title, author and abstract on page 1; an unnumbered title note
- verse quoted line by line; a figure caption interrupting a paragraph; a reference list at note size
- line-end hyphens after "prefixes" that are not prefixes there (pro-|duction), closed em dash at a line end
Runs with PyMuPDF only (no LibreOffice)."""
import os, re, sys, subprocess, tempfile
import pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "scripts", "pdf_extract.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import pdf_extract as P
res = []

def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

# ---- font names
t("italic by style suffix: AdvOTa14f9db0.I+20", P.is_italic({"font": "AdvOTa14f9db0.I+20", "flags": 4}))
t("italic by style suffix: AdvOTa14f9db0.I", P.is_italic({"font": "AdvOTa14f9db0.I", "flags": 4}))
t("roman obfuscated name not italic: AdvOT635f2c37+20", not P.is_italic({"font": "AdvOT635f2c37+20", "flags": 4}))
t("bold by style suffix: AdvOTx.B, not italic", P.is_bold({"font": "AdvOTx.B", "flags": 4}) and not P.is_italic({"font": "AdvOTx.B", "flags": 4}))
t("italic suffix is not bold", not P.is_bold({"font": "AdvOTa14f9db0.I", "flags": 4}))

# ---- the PDF
FB = {"rg": pymupdf.Font("tiro"), "it": pymupdf.Font("tiit")}
doc = pymupdf.open()
W, H = 432, 666
LM, RM = 48, 372          # text block
BS, NS = 10.8, 9.0        # body, notes

def page():
    pg = doc.new_page(width=W, height=H)
    for k, f in FB.items():
        pg.insert_font(fontname=k, fontbuffer=f.buffer)
    return pg

def put(pg, x, y, txt, fn="rg", fs=BS):
    pg.insert_text((x, y), txt, fontname=fn, fontsize=fs)
    return x + FB[fn].text_length(txt, fontsize=fs)

def fill(words, width, fs=BS):
    """greedy lines of short words, each within a few points of the measure (so none looks 'short')"""
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if FB["rg"].text_length(cand, fontsize=fs) > width:
            lines.append(cur); cur = w
        else:
            cur = cand
    return lines, cur

def line_to(end, width=RM - LM, fs=BS):
    """a full-measure line that ends with `end`"""
    words = []
    for w in WORDS:
        if FB["rg"].text_length(" ".join(words + [w, end]), fontsize=fs) > width:
            break
        words.append(w)
    return " ".join(words + [end])

WORDS = ("the old road ran on past the mill and the field and all of us went on with it day by day " * 12).split()

# page 1: title, author, abstract, caps heading, small-caps opener, marker 1, title note, note 1 (raised start)
p1 = page()
put(p1, 70, 80, "A Test Title for Stage One", fs=16)
x = put(p1, 110, 110, "ANNA NOWAK", fs=8); put(p1, x, 110, ", University of Nowhere", "it", NS)
put(p1, LM, 140, "This abstract is set in italics at the note size", "it", NS)
put(p1, LM, 152, "and it runs on to a second line of its own.", "it", NS)
put(p1, 170, 190, "INTRODUCTION", fs=10.5)
x = put(p1, LM, 210, "THIS ESSAY BEGINS", fs=9)
body, rest = fill(WORDS[:60], RM - x - 4)
put(p1, x, 210, " " + body[0])
y = 223
more, rest = fill(WORDS[len(body[0].split()):80], RM - LM)
for ln in more:
    put(p1, LM, y, ln); y += 13
x = put(p1, LM, y, line_to("so it all"))
put(p1, x + 0.5, y - 3.3, "1", fs=7.6)
last_body_y = y
put(p1, LM, last_body_y + 32, "I owe many thanks to my colleagues for their help, and to the", fs=NS)
put(p1, LM, last_body_y + 44, "reviewers for their generous reading.", fs=NS)
x = put(p1, 60, last_body_y + 58, "1", fs=6.4)
x = put(p1, x, last_body_y + 58, " Smith, 35", fs=NS)
put(p1, x, last_body_y + 62, "–69; the pro-", fs=NS)
put(p1, LM, last_body_y + 74, "duction of the text was slow, see https://www.example.org/", fs=NS)
put(p1, LM, last_body_y + 86, "2018/feb/old-road-and-the-mill-", fs=NS)
put(p1, LM, last_body_y + 98, "and-the-field.", fs=NS)
for yy in (74, 86, 98):
    p1.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.example.org/2018/feb/old-road-and-the-mill-and-the-field",
                    "from": pymupdf.Rect(LM, last_body_y + yy - 9, RM, last_body_y + yy + 2)})
put(p1, LM, last_body_y + 140, "Test Journal 12 (2020): 1–30 © The Author(s), 2020. doi: 10.1234/tj.2020.1", fs=NS)

# page 2: running head, paragraph continued from page 1, two-line caps heading, verse with marker 2,
# notes 2 (whole first line on one baseline) and 3 (raised start + superscript e)
p2 = page()
put(p2, 150, 54, "TEST JOURNAL", fs=8)
y = 78
cont, _ = fill(WORDS[80:130], RM - LM)
for ln in cont[:3]:
    put(p2, LM, y, ln); y += 13
put(p2, LM, y, line_to("of intrigue—")); y += 13
put(p2, LM, y, "and more production here, and the end."); y += 13
y += 20
put(p2, 90, y, "SECOND PART: A LONG HEADING", fs=10.5); y += 13
put(p2, 150, y, "IN CAPITALS", fs=10.5); y += 20
for ln in fill(WORDS[130:170], RM - LM - 16)[0][:2]:
    put(p2, LM, y, ln); y += 13
put(p2, LM, y, "and so the old song says of it:"); y += 19
verse = ["Dark goddess whose splendor", "Burns with the force of suns:", "Snow cannot rival her", "And ebony triumphs over ivory."]
for i, v in enumerate(verse):
    x = put(p2, 72, y, v, fs=10)
    if i == len(verse) - 1:
        put(p2, x + 0.5, y - 3.3, "2", fs=7.6)
    y += 13
y += 6
put(p2, 60, y, "And the text goes on after the verse to the end of the page.")
ny = 540
put(p2, 60, ny, "2", fs=6.4)
put(p2, 64, ny, " Whole first line on one baseline, number only smaller,", fs=NS)
put(p2, LM, ny + 12, "and a second line of the same note.", fs=NS)
x = put(p2, 60, ny + 20, "3", fs=6.4)
x = put(p2, x, ny + 20, " Asséo,", fs=NS)
x2 = put(p2, x, ny + 24, " 1974: “Le XVII", fs=NS)
x2 = put(p2, x2, ny + 24, " ", fs=3)          # kerning space in the small size, on the baseline
x3 = put(p2, x2, ny + 20, "e", fs=6.4)
put(p2, x3, ny + 24, " siècle”.", fs=NS)

# page 3: marker 3 in a paragraph interrupted by a figure caption, then BIBLIOGRAPHY at note size
p3 = page()
put(p3, 150, 54, "TEST JOURNAL", fs=8)
y = 78
para, _ = fill(WORDS[170:250], RM - LM)
put(p3, 60, y, para[0]); y += 13
for ln in para[1:3]:
    put(p3, LM, y, ln); y += 13
x = put(p3, LM, y, para[3]); put(p3, x + 0.5, y - 3.3, "3", fs=7.6)
y += 30
put(p3, LM, y, "Figure 1. A drawing of the old road, 1631. Private collection.", fs=NS)
y += 30
put(p3, LM, y, "after the figure the same sentence goes on and ends here."); y += 30
put(p3, 175, y, "BIBLIOGRAPHY", fs=10.5); y += 18
put(p3, LM, y, "Acton, Thomas. Gypsy Politics and Social Change. London: Routledge", fs=NS); y += 12
put(p3, 60, y, "and Kegan Paul, 1974.", fs=NS); y += 12
put(p3, LM, y, "Fraser, Angus. The Gypsies. Oxford: Blackwell, 1992. https://www.gyp-", fs=NS); y += 12
put(p3, 60, y, "sylore.org/fraser.html.", fs=NS); y += 12
for yy in (y - 24, y - 12):
    p3.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.gypsylore.org/fraser.html", "from": pymupdf.Rect(LM, yy - 9, RM, yy + 2)})
put(p3, LM, y, "Galland, Nora. Name-Calling. Shakespeare en devenir 12 (2017): https://www.ex.org/i.php?id¼12.", fs=NS)
p3.insert_link({"kind": pymupdf.LINK_URI, "uri": "https://www.ex.org/i.php?id=12", "from": pymupdf.Rect(LM, y - 9, RM, y + 2)}); y += 12

d = tempfile.mkdtemp()
pdf = os.path.join(d, "journal.pdf"); doc.save(pdf)
out = os.path.join(d, "j.md")
r = subprocess.run([sys.executable, EX, pdf, "-o", out], capture_output=True, text=True)
md = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
rep = open(os.path.join(d, "j_extract.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "j_extract.md")) else ""
front = open(os.path.join(d, "j_front.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "j_front.md")) else ""
bib = open(os.path.join(d, "j_bib.txt"), encoding="utf-8").read().splitlines() if os.path.exists(os.path.join(d, "j_bib.txt")) else []
D = md + "\n---REPORT---\n" + rep + r.stdout + r.stderr

notes = {m.group(1): m.group(2) for m in re.finditer(r"^\[\^(\d+)\]:\s*(.+)$", md, re.M)}
t("EXTRACT OK, 3 notes, 3 markers in order", "EXTRACT OK" in r.stdout and sorted(notes) == ["1", "2", "3"]
  and re.findall(r"\[\^(\d+)\](?!:)", md) == ["1", "2", "3"], D)
t("URL broken after a slash: no space; after a hyphen: hyphen kept and listed",
  "https://www.example.org/2018/feb/old-road-and-the-mill-and-the-field." in notes.get("1", "")
  and "URL" in rep and "hyphen kept (link target)" in rep, D)
t("block set apart below the notes (journal, licence, DOI) not in the last note; page 1: with the front matter",
  "doi" not in notes.get("1", "") and "Test Journal 12 (2020)" in front and "set apart below the notes" in rep, D + front)
t("raised note start joined without a space: 'Smith, 35–69'", notes.get("1", "").startswith("Smith, 35–69;"), notes)
t("note line joined with evidence: pro-|duction -> production (word found in the text)",
  "the production of the text was slow" in notes.get("1", "") and "(prefix, but found in the text)" in rep, D)
t("note number on the line's own baseline, smaller -> note 2",
  notes.get("2") == "Whole first line on one baseline, number only smaller, and a second line of the same note.", notes)
t("superscript inside a note line kept in place: 'XVIIe siècle' (listed)",
  notes.get("3") == "Asséo, 1974: “Le XVIIe siècle”." and "['e']" in rep, notes)
t("front matter out of the text into _front.md (title, author, abstract)",
  "A Test Title" not in md and "abstract is set" not in md and "A Test Title for Stage One" in front
  and "*This abstract is set in italics at the note size and it runs on to a second line of its own.*" in front, D + front)
t("caps heading smaller than the body -> # heading, kept though it sits just above the text",
  re.search(r"^# INTRODUCTION$", md, re.M) is not None, D)
t("two-line caps heading -> one heading", re.search(r"^# SECOND PART: A LONG HEADING IN CAPITALS$", md, re.M) is not None, D)
t("small-caps opening words retyped and listed", re.search(r"^This essay begins the old road", md, re.M) is not None
  and "opening words in small capitals retyped" in rep, D)
t("unnumbered note at the foot of page 1 -> ::: przypis-tytulowy at the top",
  md.startswith("::: przypis-tytulowy\nI owe many thanks to my colleagues for their help, and to the reviewers for their generous reading.\n:::"), D)
t("paragraph running over the page (running head between) stays one paragraph",
  re.search(r"so it all\[\^1\] " + re.escape(cont[0].split()[0]) + " ", md) is not None, D)
t("closed em dash at a line end joined without a space: intrigue—and", "intrigue—and more" in md, D)
t("verse -> one quotation, forced line breaks, marker on the last line",
  "> Dark goddess whose splendor\\\n> Burns with the force of suns:\\\n> Snow cannot rival her\\\n> And ebony triumphs over ivory.[^2]" in md, D)
t("caption -> ::: podpis, placed after the paragraph it interrupted; paragraph rejoined",
  re.search(r"\[\^3\] after the figure the same sentence goes on and ends here\.\n\n\[\^3\]: .*\n\n::: podpis\nFigure 1\. A drawing", md) is not None, D)
t("reference list at note size -> _bib.txt, one entry per item; out of the text with its heading",
  bib[:1] == ["Acton, Thomas. Gypsy Politics and Social Change. London: Routledge and Kegan Paul, 1974."] and len(bib) == 3 and "BIBLIOGRAPHY" not in md and "Acton" not in md, (bib, D))
t("URL hyphen at a line break decided by the link target: typesetter's removed, the address's own kept",
  bib[1:2] == ["Fraser, Angus. The Gypsies. Oxford: Blackwell, 1992. https://www.gypsylore.org/fraser.html."]
  and "hyphen removed (link target)" in rep and "hyphen kept (link target)" in rep, (bib, D))
t("URL text with a wrong glyph (id¼12) replaced by its link target, listed",
  bib[2:] == ["Galland, Nora. Name-Calling. Shakespeare en devenir 12 (2017): https://www.ex.org/i.php?id=12."]
  and "differs from its link target" in rep, (bib, D))
t("running head dropped", "TEST JOURNAL" not in md, D)
# word check (promoted from the per-article wordcheck.py): in the report; a word dropped from the text is caught
wc = re.search(r"^## Word check: lost (\d+) · extra (\d+)", rep, re.M)
pg = list(pymupdf.open(pdf))
lost, _ = P.wordcheck(pg, [md.replace("mill", "", 1), front] + bib)
lost0, _ = P.wordcheck(pg, [md, front] + bib)
t("word check in the report; a word removed from the text shows up as lost",
  wc is not None and lost.get("mill", 0) == lost0.get("mill", 0) + 1, (wc and wc.group(0), lost))

# ---- C39 (Davis RIP, 03.11.2026): the publisher's page-foot block, tables as stubs
# page 1: a paragraph running to the page's last line; at the foot the publisher's block (CONTACT, ©, licence; 8 and 7 pt);
# page 2 goes on in lower case, a prose paragraph full of numbers (no table), then "Table 1." with its cells (8 pt, rows
# of figures; a note marker raised in the caption) and the paragraph resumes; page 3 is a table set sideways (rotated);
# text with marker 2 follows on page 4 (the table's note 1 comes first in the numbering)
d3 = pymupdf.open()
def pg3():
    q = d3.new_page(width=W, height=H)
    for k, f in FB.items():
        q.insert_font(fontname=k, fontbuffer=f.buffer)
    return q
def para(q, y, words, n_lines):
    """n_lines full lines of the measure from words (cycled); returns the next baseline"""
    i = 0
    for ln in range(n_lines):
        cur = ""
        while True:
            w = words[i % len(words)]
            cand = (cur + " " + w).strip()
            if FB["rg"].text_length(cand, fontsize=BS) > RM - LM:
                break
            cur = cand; i += 1
        q.insert_text((LM, y), cur, fontname="rg", fontsize=BS)
        y += 13
    return y
filler = "the removal of children from their families was justified by officials as a form of rescue and reform".split()
q1 = pg3()
y = para(q1, 80, filler, 39)          # the last line of the page is a full one: the paragraph goes on overleaf
q1.insert_text((LM, 600), "CONTACT  Sacha Davis sacha@example.edu School of Humanities, University of Newcastle,", fontname="rg", fontsize=8)
q1.insert_text((LM, 609), "Callaghan, NSW 2308, Australia", fontname="rg", fontsize=8)
q1.insert_text((LM, 626), "© 2026 The Author(s). Published by Informa UK Limited, trading as Taylor & Francis Group", fontname="rg", fontsize=7)
q1.insert_text((LM, 634), "This is an Open Access article distributed under the terms of the Creative Commons Attribution License", fontname="rg", fontsize=7)
q2 = pg3()
y = para(q2, 80, "children into useful members of society while the census counted 9861 houses and 1073 huts in 1780 and 11649 in 1781".split(), 12)
q2.insert_text((LM, y), "and the paragraph was cut by the table so that it", fontname="rg", fontsize=BS)
y += 30
q2.insert_text((LM, y), "Table 1. Counts by year.", fontname="rg", fontsize=9.5)
q2.insert_text((LM + FB["rg"].text_length("Table 1. Counts by year.", fontsize=9.5) + 1, y - 4), "1", fontname="rg", fontsize=6)
for k, row in enumerate(["Year Boys Girls Total Children", "1780 2249 2067 4316 22,560", "1781 2816 2777 5593 25,964",
                         "1782 3151 3058 6209 29,996", "1783 2105 2174 4279 22,050"]):
    q2.insert_text((LM, y + 14 + 10 * k), row, fontname="rg", fontsize=8)
y += 14 + 50 + 24
y = para(q2, y, filler, 4)
q2.insert_text((LM, 575), "1 Source: the census, vol. 3.", fontname="rg", fontsize=NS)
q2.draw_line((LM, 565), (LM + 80, 565))
q3 = pg3()
q3.insert_text((LM, 60), "Table 2. Sideways table.", fontname="rg", fontsize=9.5)
for k, col in enumerate(["Remaining at home boys 4856 4126 301", "Attending school boys 6782 6453 631", "Taken from parents girls 3784 2783 480",
                         "Servants male maidservants 2254 2391 2351", "Total removed 8388 6059 5053 3515"]):
    q3.insert_text((100 + 14 * k, 300 + 20 * k), col, fontname="rg", fontsize=8, rotate=90)
q4 = pg3()
y = para(q4, 80, filler, 6)
q4.insert_text((LM, y), "the last sentence of the text", fontname="rg", fontsize=BS)
x = LM + FB["rg"].text_length("the last sentence of the text", fontsize=BS) + 2
q4.insert_text((x, y - 4), "2", fontname="rg", fontsize=6.5)
q4.insert_text((LM, 575), "2 Last note.", fontname="rg", fontsize=NS)
q4.draw_line((LM, 565), (LM + 80, 565))
pdf3 = os.path.join(tempfile.mkdtemp(), "tbl.pdf")
d3.save(pdf3)
out3 = pdf3[:-4] + ".md"
r3 = subprocess.run([sys.executable, EX, pdf3, "-o", out3], capture_output=True, text=True)
md3 = open(out3, encoding="utf-8").read()
rep3 = open(out3[:-3] + "_extract.md", encoding="utf-8").read()
t("publisher's page-foot block (CONTACT, ©, licence) cut out; the paragraph runs on over the page break",
  "CONTACT" not in md3 and "Open Access" not in md3 and "children into useful members" in md3 and "\n\nchildren into" not in md3
  and "publisher's page-foot block" in rep3, md3[:300] + rep3)
t("a table (caption + rows of figures) becomes one <!-- TABLE p. 2 --> stub after its caption; no cell survives",
  md3.count("<!-- TABLE p. 2 -->") == 1 and "2249" not in md3 and "Year Boys" not in md3
  and bool(re.search(r"::: tabela-tytul\nTable 1\. Counts by year\.\[\^1\]\n:::\n\n\[\^1\]: Source: the census[^\n]*\n\n<!-- TABLE p. 2 -->", md3)), md3)
t("a sideways table page becomes a <!-- TABLE p. 3 --> stub", md3.count("<!-- TABLE p. 3 -->") == 1 and "4856" not in md3, md3)
t("prose with numbers (a census paragraph with years and counts) is not a table", md3.count("<!-- TABLE") == 2
  and "counted 9861 houses and 1073 huts" in md3, md3)
t("the paragraph the table interrupted is one paragraph; the table's note stays out of the marker-order check",
  "the paragraph was cut by the table so that it the removal of children" in md3 and r3.returncode == 0
  and "EXTRACT OK" in r3.stdout and "marker sequence" not in rep3 and "without a marker" not in rep3, r3.stdout + rep3)

n, ok = len(res), sum(res)
print(f"PDF-LAYOUT ALL PASS {n}/{n}" if ok == n else f"PDF-LAYOUT FAILED {n - ok}/{n}")
