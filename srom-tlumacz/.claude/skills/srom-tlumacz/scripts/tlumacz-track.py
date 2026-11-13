#!/usr/bin/env python3
"""tlumacz-track.py — tracked-change replacements in a Word copy (the tool of the 12.11.2026 Pahulich v2).

  tlumacz-track.py <in.docx | unpacked dir> <edits.json> [-o out.docx] [--author NAME]
  tlumacz-track.py --selftest

edits.json: a list of [part, anchor, old, new]. part = document.xml or footnotes.xml; anchor = text identifying the one
paragraph (unique in that part); old = the exact text to replace, once in that paragraph, not spanning a non-text run
(footnote reference etc.); new = the replacement, *…* marks italics, {FN:<text>} inserts a tracked footnote reference
whose footnote reads <text>. Every edit becomes w:del + w:ins (author "Claude" unless --author, date = now, UTC);
nothing is changed silently. A docx input needs -o (the input is never overwritten: it is MB's master); a directory is
edited in place. Check the result with the docx skill's validator and re-import it (outputs.md § Back, `_v2` copy).
"""
import copy, glob, os, re, shutil, sys, json, tempfile, time, zipfile
from lxml import etree

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
def q(t): return "{%s}%s" % (W, t)

AUTHOR, DATE = "Claude", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
_id = [9000]
def nid():
    _id[0] += 1
    return str(_id[0])

def run_text(r):
    """text of a plain text run, or None if the run holds anything but rPr/t"""
    kids = [k for k in r if k.tag not in (q("rPr"), q("lastRenderedPageBreak"))]
    if not kids: return ""
    if all(k.tag == q("t") for k in kids):
        return "".join(k.text or "" for k in kids)
    return None

def para_text(p):
    return "".join((run_text(r) or "") for r in p if r.tag == q("r"))

def normalise(r):
    t = run_text(r)
    if t is None: return
    for k in r.findall(q("lastRenderedPageBreak")): r.remove(k)
    for k in [k for k in r if k.tag == q("t")]: r.remove(k)
    e = etree.SubElement(r, q("t")); e.text = t
    e.set("{%s}space" % XML, "preserve")

def split_run(r, at):
    """split plain run r at char offset at; returns (left, right) both in the tree"""
    t = run_text(r)
    right = copy.deepcopy(r)
    r.find(q("t")).text = t[:at]
    right.find(q("t")).text = t[at:]
    r.addnext(right)
    return r, right

def mk_run(rpr, text, italic=False):
    r = etree.Element(q("r"))
    if rpr is not None:
        rp = copy.deepcopy(rpr)
        r.append(rp)
    else:
        rp = None
    if italic:
        if rp is None:
            rp = etree.SubElement(r, q("rPr"))
        if rp.find(q("i")) is None:
            # i must follow rStyle/rFonts/b/bCs; insert after those if present
            i = etree.Element(q("i"))
            pos = 0
            for idx, k in enumerate(rp):
                if k.tag in (q("rStyle"), q("rFonts"), q("b"), q("bCs")): pos = idx + 1
            rp.insert(pos, i)
    t = etree.SubElement(r, q("t")); t.text = text
    t.set("{%s}space" % XML, "preserve")
    return r

def segs(new):
    out = []
    for i, part in enumerate(re.split(r"\*", new)):
        if part: out.append((part, i % 2 == 1))
    return out

class Doc:
    def __init__(self, d):
        self.d = d
        self.trees = {}
        for f in glob.glob(f"{d}/word/*.xml"):                 # new revision ids start above every id already used
            for e in etree.parse(f).iter():
                v = e.get(q("id"))
                if v and v.isdigit(): _id[0] = max(_id[0], int(v))
    def tree(self, part):
        if part not in self.trees:
            self.trees[part] = etree.parse(f"{self.d}/word/{part}")
        return self.trees[part]
    def save(self):
        for part, t in self.trees.items():
            t.write(f"{self.d}/word/{part}", xml_declaration=True, encoding="UTF-8", standalone=True)

    def find_para(self, part, anchor):
        ps = [p for p in self.tree(part).iter(q("p")) if anchor in para_text(p)]
        if len(ps) != 1: raise SystemExit(f"anchor {anchor!r} in {part}: {len(ps)} paragraphs")
        return ps[0]

    def new_footnote(self, text):
        ft = self.tree("footnotes.xml").getroot()
        ids = [int(f.get(q("id"))) for f in ft.findall(q("footnote"))]
        fid = str(max(ids) + 1)
        # model: an existing normal footnote (id >= 1) — copy its paragraph props and the footnoteRef run
        model = [f for f in ft.findall(q("footnote")) if int(f.get(q("id"))) >= 1][0]
        mp = model.find(q("p"))
        fn = etree.SubElement(ft, q("footnote")); fn.set(q("id"), fid)
        p = etree.SubElement(fn, q("p"))
        if mp.find(q("pPr")) is not None: p.append(copy.deepcopy(mp.find(q("pPr"))))
        refrun = [r for r in mp.findall(q("r")) if r.find(q("footnoteRef")) is not None][0]
        textrun = [r for r in mp.findall(q("r")) if run_text(r)]
        trpr = textrun[0].find(q("rPr")) if textrun else None
        ins = etree.SubElement(p, q("ins")); ins.set(q("id"), nid()); ins.set(q("author"), AUTHOR); ins.set(q("date"), DATE)
        ins.append(copy.deepcopy(refrun))
        # plain rPr for text: drop italics from the model's
        base = copy.deepcopy(trpr) if trpr is not None else None
        if base is not None:
            for k in base.findall(q("i")) + base.findall(q("iCs")): base.remove(k)
        ins.append(mk_run(base, " "))
        for s, it in segs(text): ins.append(mk_run(base, s, it))
        return fid

    def replace(self, part, anchor, old, new):
        p = self.find_para(part, anchor)
        for r in p.findall(q("r")): normalise(r)
        txt = para_text(p)
        n = txt.count(old)
        if n != 1: raise SystemExit(f"old {old!r}: {n} occurrences in paragraph {anchor!r}")
        start = txt.index(old); end = start + len(old)
        # walk runs, split at start/end
        pos = 0; affected = []; runs = [r for r in p if r.tag == q("r")]
        i = 0
        while i < len(runs):
            r = runs[i]; t = run_text(r)
            L = len(t) if t is not None else 0
            if t is None:
                if start < pos < end or (start < pos and pos < end): raise SystemExit(f"old {old!r} spans a non-text run")
                i += 1; continue
            a, b = pos, pos + L
            if b <= start or a >= end or L == 0:
                pos = b; i += 1; continue
            if a < start:
                left, right = split_run(r, start - a)
                runs[i:i+1] = [left, right]; continue
            if b > end:
                left, right = split_run(r, end - a)
                runs[i:i+1] = [left, right]; continue
            affected.append(r); pos = b; i += 1
        rpr = affected[0].find(q("rPr")) if affected else None
        last = None
        for r in affected:
            d = etree.Element(q("del")); d.set(q("id"), nid()); d.set(q("author"), AUTHOR); d.set(q("date"), DATE)
            r.addprevious(d); d.append(r)
            t = r.find(q("t")); t.tag = q("delText")
            last = d
        if not affected:
            raise SystemExit("pure insertion not supported: give some context in old")
        # build insertion
        pieces = re.split(r"(\{FN:.*?\})", new)
        ins = etree.Element(q("ins")); ins.set(q("id"), nid()); ins.set(q("author"), AUTHOR); ins.set(q("date"), DATE)
        for piece in pieces:
            m = re.fullmatch(r"\{FN:(.*)\}", piece)
            if m:
                fid = self.new_footnote(m.group(1))
                # reference run: copy rPr of an existing footnoteReference run in the document
                refr = next(r for r in self.tree("document.xml").iter(q("r")) if r.find(q("footnoteReference")) is not None)
                rr = etree.Element(q("r"))
                if refr.find(q("rPr")) is not None: rr.append(copy.deepcopy(refr.find(q("rPr"))))
                fr = etree.SubElement(rr, q("footnoteReference")); fr.set(q("id"), fid)
                ins.append(rr)
            else:
                for s, it in segs(piece): ins.append(mk_run(rpr, s, it))
        if len(ins): last.addnext(ins)

def unpack(path):
    d = tempfile.mkdtemp(); zipfile.ZipFile(path).extractall(d); return d

def pack(d, out):
    names = [os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs]
    names.sort(key=lambda n: (n != "[Content_Types].xml", n))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names: z.write(os.path.join(d, n), n)

def apply(d, edits, say=print):
    doc = Doc(d)
    for e in edits:
        doc.replace(*e); say("ok: " + e[2][:60])
    doc.save()

# ---------- selftest: a minimal docx, edits applied, negative controls --------------------------------------------
NS = 'xmlns:w="%s"' % W
DOC = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
       '<w:p><w:r><w:t xml:space="preserve">Pierwszy akapit z błędem w słowie i drugim zdaniem.</w:t></w:r></w:p>'
       '<w:p><w:r><w:t xml:space="preserve">Drugi akapit</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr>'
       '<w:footnoteReference w:id="1"/></w:r><w:r><w:t xml:space="preserve"> ma przypis i dalszy tekst.</w:t></w:r></w:p>'
       '</w:body></w:document>')
FNS = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes {NS}>'
       '<w:footnote w:id="1"><w:p><w:r><w:footnoteRef/></w:r><w:r><w:t xml:space="preserve"> Treść przypisu.</w:t></w:r></w:p></w:footnote>'
       '</w:footnotes>')

def selftest():
    t = tempfile.mkdtemp(); out = []
    def ok(name, cond):
        out.append(bool(cond))
        if not cond: print("  NOT OK:", name)
    def build():
        d = tempfile.mkdtemp(); os.makedirs(d + "/word")
        open(d + "/[Content_Types].xml", "w").write("<Types/>")
        open(d + "/word/document.xml", "w", encoding="utf-8").write(DOC)
        open(d + "/word/footnotes.xml", "w", encoding="utf-8").write(FNS)
        p = os.path.join(t, "in.docx"); pack(d, p); return p
    def fails(edit):
        d = unpack(build())
        try: apply(d, [edit], say=lambda s: None); return False
        except SystemExit: return True
    p = build()
    d = unpack(p)
    apply(d, [["document.xml", "Pierwszy akapit", "błędem w słowie", "*poprawką* w słowie"],
              ["document.xml", "Drugi akapit", "dalszy tekst", "dalszym tekstem{FN:Nowy *przypis*.}"]], say=lambda s: None)
    pack(d, os.path.join(t, "out.docx"))
    z = zipfile.ZipFile(os.path.join(t, "out.docx"))
    doc, fn = etree.fromstring(z.read("word/document.xml")), etree.fromstring(z.read("word/footnotes.xml"))
    dels, ins = doc.findall(".//" + q("del")), doc.findall(".//" + q("ins"))
    ok("two w:del and two w:ins in the document", len(dels) == 2 and len(ins) == 2)
    ok("author and date on every revision", all(e.get(q("author")) == "Claude" and e.get(q("date")) for e in dels + ins))
    ok("deleted text is w:delText, inside the w:del", all(e.find(".//" + q("delText")) is not None for e in dels))
    ok("revision ids are unique", len({e.get(q("id")) for e in doc.iter() if e.tag in (q("ins"), q("del"))}) == 4)
    ok("italic run in the insertion", any(r.find(q("rPr") + "/" + q("i")) is not None for r in ins[0].findall(q("r"))))
    ok("new tracked footnote id 2 with its reference", fn.findall(q("footnote"))[-1].get(q("id")) == "2"
       and doc.find(".//" + q("ins") + "//" + q("footnoteReference")).get(q("id")) == "2")
    accepted = "".join(x.text or "" for x in doc.iter(q("t")))
    ok("accepting everything gives the new text", "poprawką w słowie" in accepted and "dalszym tekstem" in accepted)
    ok("the input docx is untouched", b"delText" not in zipfile.ZipFile(p).read("word/document.xml"))
    ok("anchor in no paragraph", fails(["document.xml", "Nie ma takiego", "x", "y"]))
    ok("anchor in two paragraphs", fails(["document.xml", "akapit", "x", "y"]))
    ok("old not in the paragraph", fails(["document.xml", "Pierwszy akapit", "brak", "y"]))
    ok("old twice in the paragraph", fails(["document.xml", "Pierwszy akapit", "w", "y"]))
    ok("old spanning the footnote reference", fails(["document.xml", "Drugi akapit", "akapit ma", "x"]))
    shutil.rmtree(t, ignore_errors=True)
    print(f"selftest: {sum(out)}/{len(out)} controls as expected" + ("" if all(out) else f", {len(out) - sum(out)} NOT OK"))
    return all(out)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: sys.exit(0 if selftest() else 1)
    if "--author" in a: AUTHOR = a[a.index("--author") + 1]
    outp = a[a.index("-o") + 1] if "-o" in a else None
    pos = [x for i, x in enumerate(a) if not x.startswith("-") and (i == 0 or a[i - 1] not in ("-o", "--author"))]
    if len(pos) != 2: print(__doc__); sys.exit(2)
    src, edits = pos[0], json.load(open(pos[1], encoding="utf-8"))
    if os.path.isdir(src): apply(src, edits)
    else:
        if not outp or os.path.abspath(outp) == os.path.abspath(src): sys.exit("a docx input needs -o <other file>")
        d = unpack(src); apply(d, edits); pack(d, outp); shutil.rmtree(d, ignore_errors=True)
        print("written:", outp)
