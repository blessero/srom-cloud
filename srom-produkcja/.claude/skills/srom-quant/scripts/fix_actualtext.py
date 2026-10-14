#!/usr/bin/env python3
"""
fix_actualtext.py — repair the text layer of an InDesign PDF; the page renders exactly as before (Cowork C6, 06.10.2026;
prototype measured on the whole vol. 18 PDF). cover_page.py runs it on the article PDF before the cover goes in.

InDesign (vol. 18, Cambria) draws many accented letters (ó ś ż ń ć ź, also á é í …) as two glyphs: the base letter
inside a marked-content span /Span <</ActualText (ó)>> BDC … EMC, and a zero-width accent glyph right after the EMC,
outside the span, which its ToUnicode maps to U+FFFD. Search, copy and indexing then see "Romó� w".

Two repairs, both invisible:
 1. the accent glyph is moved inside the span (drawing order and positions unchanged), so ActualText-aware readers
    (MuPDF, PDFium/Chrome, Acrobat) read the span as one letter; poppler/xpdf still put a word gap after
    some of these letters (their spacing heuristic; measured, not fixed);
 2. the accent glyph's ToUnicode entry U+FFFD becomes the combining mark that the spans' ActualText implies
    (ó → o + U+0301), so readers that ignore ActualText (pdf.js) read a decomposed "ó" instead of "o�".

A third repair (C15 addendum, 14.10.2026) covers a case that is not a span at all: a precomposed letter (ć) drawn as one glyph,
followed in the same text-show operator by a zero-width accent glyph that InDesign adds for the diacritic. After repair 2
that accent code reads as U+0301, so MuPDF, poppler, PDFium and Acrobat read "ć" and then another acute ("Choć́"). Such a
glyph is wrapped in an empty marked-content span, /Span <</ActualText ()>> BDC … EMC, so ActualText-aware readers read
nothing for it; drawing order and positions are unchanged (a split of the TJ array leaves the text matrix as it was).
 3. an accent glyph whose mark the preceding letter in the same show already carries is wrapped in an empty ActualText span.

Known leftovers, not repaired (Cowork, vol. 18 of 13.05.2026: 12,005 → 60 U+FFFD): the show operator after the EMC is
not the next one (it starts in a new text object, after a font change or any operator other than Td), so the accent
glyph stays outside its span, and its U+FFFD stays unless another span in the same font taught its code a mark.
cover_page.py counts what is left after saving and prints it; nothing hides it.

    python3 fix_actualtext.py in.pdf out.pdf
"""
import re, sys, unicodedata
from decimal import Decimal
import pikepdf
from pikepdf import Operator, String, Name, ContentStreamInstruction as CSI

TD, TJ1, TJN, BDC, EMC, TF = (Operator(x) for x in ("Td", "Tj", "TJ", "BDC", "EMC", "Tf"))


def tounicode(font):
    """{code bytes: destination hex} of the font's ToUnicode (bfchar and simple bfrange)."""
    tu = font.get("/ToUnicode")
    if tu is None:
        return {}
    data = tu.read_bytes().decode("latin-1")
    m = {}
    for block in re.findall(r"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            m[bytes.fromhex(src)] = dst.upper()
    for block in re.findall(r"beginbfrange(.*?)endbfrange", data, re.S):
        for a, b, d in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            n = len(a) // 2
            for k, v in enumerate(range(int(a, 16), int(b, 16) + 1)):
                m[v.to_bytes(n, "big")] = "%0*X" % (len(d), int(d, 16) + k)
    return m


def widths(font):
    """advance width (1/1000 em) of a code, for Type0 /W and simple /Widths."""
    if font.get("/Subtype") == "/Type0":
        df = font.DescendantFonts[0]
        dw = float(df.get("/DW", 1000))
        W = list(df.get("/W", []))
        def w(code):
            cid = int.from_bytes(code, "big"); i = 0
            while i < len(W):
                a = int(W[i])
                if isinstance(W[i + 1], pikepdf.Array):
                    arr = W[i + 1]
                    if a <= cid < a + len(arr):
                        return float(arr[cid - a])
                    i += 2
                else:
                    if a <= cid <= int(W[i + 1]):
                        return float(W[i + 2])
                    i += 3
            return dw
        return w
    fc, ws = int(font.get("/FirstChar", 0)), list(font.get("/Widths", []))
    return lambda code: float(ws[code[0] - fc]) if 0 <= code[0] - fc < len(ws) else 0.0


class Font:
    def __init__(self, obj):
        self.obj, self.cl = obj, (2 if obj.get("/Subtype") == "/Type0" else 1)
        self.tu, self.width = tounicode(obj), widths(obj)
        self.marks = {}                                  # code -> set of combining chars seen
        self.mapped = {}                                 # code -> combining char patch_tounicode gave it

    def is_bad(self, code):
        return self.tu.get(code, "") in ("", "FFFD", "0000")


def first_string(instr):
    if instr.operator == TJ1:
        return bytes(instr.operands[0]), None
    arr = list(instr.operands[0])
    if arr and isinstance(arr[0], pikepdf.String):
        return bytes(arr[0]), arr[1:]
    return b"", None


def rebuild_show(instr, tail, rest):
    if instr.operator == TJ1:
        return [CSI([String(tail)], TJ1)] if tail else []
    items = ([String(tail)] if tail else []) + list(rest)
    return [CSI([pikepdf.Array(items)], TJN)] if items else []


def fix_stream(instrs, fonts):
    out, i, n, cur, fixed = [], 0, len(instrs), None, 0
    while i < n:
        ins = instrs[i]
        if ins.operator == TF:
            cur = fonts.get(str(ins.operands[0]))
        if not (ins.operator == BDC and len(ins.operands) == 2 and ins.operands[0] == Name("/Span")
                and isinstance(ins.operands[1], pikepdf.Dictionary) and "/ActualText" in ins.operands[1]):
            out.append(ins); i += 1; continue
        j = i + 1
        while j < n and instrs[j].operator != EMC:
            j += 1
        body = instrs[i + 1:j]
        if j >= n or any(b.operator in (BDC, Operator("BMC"), TF) for b in body) or cur is None:
            out.append(ins); i += 1; continue
        k, td_b = j + 1, None
        if k < n and instrs[k].operator == TD:
            td_b, k = instrs[k], k + 1
        if not (k < n and instrs[k].operator in (TJ1, TJN)):
            out.append(ins); i += 1; continue
        s, rest = first_string(instrs[k])
        mark, tail = s[:cur.cl], s[cur.cl:]
        if len(mark) < cur.cl or not cur.is_bad(mark):
            out.append(ins); i += 1; continue
        actual = str(ins.operands[1].ActualText).lstrip("﻿")
        nfd = unicodedata.normalize("NFD", actual)
        if len(nfd) == 2 and unicodedata.combining(nfd[1]):
            cur.marks.setdefault(mark, set()).add(nfd[1])
        out.append(ins)                                   # drawing order and positions unchanged
        out += body + ([td_b] if td_b is not None else []) + [CSI([String(mark)], TJ1), instrs[j]]
        out += rebuild_show(instrs[k], tail, rest or [])
        fixed += 1
        i = k + 1
    return out, fixed


def fonts_of(res, cache):
    out = {}
    f = res.get("/Font") if res is not None else None
    for name, obj in (f.items() if f is not None else []):
        key = obj.objgen
        if key not in cache:
            cache[key] = Font(obj)
        out[name] = cache[key]
    return out


def patch_tounicode(pdf, font):
    """U+FFFD → the combining mark the spans imply, when every span agrees on it."""
    ok = {c: next(iter(s)) for c, s in font.marks.items() if len(s) == 1}
    font.mapped = {}
    if not ok or font.obj.get("/ToUnicode") is None:
        return 0
    data = font.obj.ToUnicode.read_bytes().decode("latin-1")
    n = 0
    for code, ch in ok.items():
        h = code.hex().upper()
        new, k = re.subn(r"<%s>(\s*)<FFFD>" % h, "<%s>\\1<%04X>" % (h, ord(ch)), data, flags=re.I)
        data, n = new, n + k
        if k:
            font.mapped[code] = ch
    font.obj.ToUnicode = pdf.make_stream(data.encode("latin-1"))
    return n


def code_text(font, code):
    """What the (patched) ToUnicode says a code is, as a str; '' when unmapped."""
    d = font.tu.get(code, "")
    if d in ("", "FFFD", "0000") or len(d) % 4:
        return ""
    return bytes.fromhex(d).decode("utf-16-be", "replace")


EMPTY_SPAN = lambda: CSI([Name("/Span"), pikepdf.Dictionary(ActualText=String(b"\xfe\xff"))], BDC)


def wrap_doubled(instrs, fonts):
    """Repair 3: in a show operator, an accent glyph (a code repair 2 mapped to a combining mark) that follows a letter of the
    same operator already carrying that mark is wrapped in an empty ActualText span. Returns (instructions, wrapped)."""
    out, wrapped, cur = [], 0, None
    for ins in instrs:
        if ins.operator == TF:
            cur = fonts.get(str(ins.operands[0]))
        if ins.operator not in (TJ1, TJN) or cur is None or not cur.mapped:
            out.append(ins); continue
        cl, prev = cur.cl, ""
        items = [ins.operands[0]] if ins.operator == TJ1 else list(ins.operands[0])
        buf, cuts = [], False
        def flush():
            if ins.operator == TJN:
                if any(isinstance(x, pikepdf.String) for x in buf):
                    out.append(CSI([pikepdf.Array(buf)], TJN))
            else:
                out.extend(CSI([x], TJ1) for x in buf)
            buf.clear()
        for it in items:
            if not isinstance(it, pikepdf.String):
                buf.append(it); continue
            b, run = bytes(it), b""
            for k in range(0, len(b) - cl + 1, cl):
                code = b[k:k + cl]
                mk = cur.mapped.get(code)
                if mk and mk in unicodedata.normalize("NFD", prev):
                    if run:
                        buf.append(String(run)); run = b""
                    flush()
                    out += [EMPTY_SPAN(), CSI([String(code)], TJ1), CSI([], EMC)]
                    wrapped += 1; cuts = True
                else:
                    run += code
                prev = code_text(cur, code) or prev
            if run:
                buf.append(String(run))
        if not cuts:
            out.append(ins); continue
        flush()
    return out, wrapped


def repair(pdf):
    """Repairs an open pikepdf.Pdf in place; returns (spans fixed, accent glyphs given a Unicode mapping, doubled accents wrapped)."""
    cache = {}
    def holders():
        seen = set()
        for page in pdf.pages:
            res = page.obj.get("/Resources")
            yield page, res
            xo = res.get("/XObject") if res is not None else None
            for _, x in (xo.items() if xo is not None else []):
                if x.get("/Subtype") == "/Form" and x.objgen not in seen:
                    seen.add(x.objgen)
                    yield x, x.get("/Resources") if x.get("/Resources") is not None else res
    def run(holder, res, fn):
        new, n = fn(list(pikepdf.parse_content_stream(holder)), fonts_of(res, cache))
        if n:
            data = pikepdf.unparse_content_stream(new)
            if isinstance(holder, pikepdf.Page):
                holder.obj.Contents = pdf.make_stream(data)
            else:
                holder.write(data)
        return n
    total = sum(run(h, r, fix_stream) for h, r in holders())
    maps = sum(patch_tounicode(pdf, f) for f in cache.values())
    wrapped = sum(run(h, r, wrap_doubled) for h, r in holders()) if maps else 0
    return total, maps, wrapped


def main(src, dst):
    pdf = pikepdf.open(src)
    total, maps, wrapped = repair(pdf)
    pdf.save(dst)
    print(f"spans fixed: {total}; accent glyphs given a Unicode mapping: {maps}; doubled accents wrapped: {wrapped}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
