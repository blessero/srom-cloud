#!/usr/bin/env python3
"""
doi_check.py — live check of an article's <stem>_doi.jsx (SYS-5) in InDesign (the editor's Mac; InDesign must be running).
Not part of run_all.py (test_doi.py checks what the build writes). Hidden windows, copies in a temp folder: the
documents open in InDesign are never touched.

    ~/.venvs/srom/bin/python tools/indesign_check/doi_check.py <build dir> [--keep DIR]

Places <stem>.docx into the clean template, runs <stem>_doi.jsx twice (report → apply; the second run must replace,
not double, the links), exports the PDF with hyperlinks and reads it back: every expected text lies under a link to
its own https://doi.org/… URL, the links are invisible (border 0), and nothing else is linked.
Last line: INDESIGN DOI CHECK ALL PASS n/n.
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TEMPLATE = os.path.join(REPO, ".claude", "skills", "srom-produkcja", "indesign", "SROM_szablon_v3.idml")


def idrun(jsx, *args):
    al = ", ".join(json.dumps(a) for a in args)
    r = subprocess.run(["osascript", "-e", "with timeout of 900 seconds",
                        "-e", f'tell application id "com.adobe.InDesign" to do script (POSIX file {json.dumps(jsx)}) language javascript with arguments {{{al}}}',
                        "-e", "end timeout"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return (r.stdout + r.stderr).strip()


def expected(jsx_path):
    src = open(jsx_path, encoding="utf-8").read()

    def arr(name):
        m = re.search(r"var %s = (?:\{|\[)\n(.*?)\n(?:\}|\]);" % name, src, re.S)
        return m.group(1) if m else ""
    notes = json.loads("{" + arr("NOTES") + "}")
    return [x for v in notes.values() for x in v] + json.loads("[" + arr("AST") + "]") + json.loads("[" + arr("BIB") + "]")


def key(s):
    s = unicodedata.normalize("NFC", s).replace("ƴ", "")       # PyMuPDF reads Cambria's ó as "óƴ"
    return re.sub(r"[\s­ -​]+", "", s)


def pdf_links(pdf):
    """[(uri, text under the rectangle)] in page order (a hyperlink over several lines has one rectangle per line);
    the border widths seen"""
    d = pymupdf.open(pdf)
    rects, borders = [], set()
    for page in d:
        chars = [(c["origin"][0] + (c["bbox"][2] - c["bbox"][0]) / 2, c["origin"][1], c["c"])
                 for b in page.get_text("rawdict")["blocks"] for l in b.get("lines", []) for s in l["spans"] for c in s["chars"]]
        for l in page.get_links():
            if l.get("kind") != pymupdf.LINK_URI:
                continue
            borders.add(d.xref_get_key(l["xref"], "Border")[1])
            r = l["from"]
            rects.append((l["uri"], "".join(c for x, y, c in chars if r.x0 <= x <= r.x1 and r.y0 <= y <= r.y1 + 0.5)))
    return rects, borders


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build")
    ap.add_argument("--keep")
    a = ap.parse_args()
    js = glob.glob(os.path.join(a.build, "*_doi.jsx"))
    if len(js) != 1:
        sys.exit(f"{a.build}: needs exactly one *_doi.jsx (found {len(js)})")
    stem = os.path.basename(js[0])[:-len("_doi.jsx")]
    w = a.keep or tempfile.mkdtemp(prefix="srom_doicheck_")
    os.makedirs(w, exist_ok=True)
    for f in (TEMPLATE, os.path.join(a.build, stem + ".docx"), js[0], os.path.join(HERE, "doi_live.jsx")):
        shutil.copy(f, w)
    pdf, rep = os.path.join(w, stem + ".pdf"), os.path.join(w, "doi_live.txt")
    idrun(os.path.join(w, "doi_live.jsx"), os.path.join(w, os.path.basename(TEMPLATE)), os.path.join(w, stem + ".docx"),
          os.path.join(w, stem + "_doi.jsx"), pdf, rep)
    log = open(rep, encoding="utf-8").read().replace("\r", "\n") if os.path.exists(rep) else "no report"
    res = []

    def t(name, ok, detail=""):
        res.append(bool(ok))
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
    exp = expected(js[0])
    run1 = log.split("RUN1 ")[-1].split("RUN2 ")[0]
    run2 = log.split("RUN2 ")[-1].split("COUNTS")[0]
    m = re.search(r"COUNTS hyperlinks (\d+) sources (\d+) destinations (\d+)", log)
    t("placed without overset", "overset false" in log, log[:600])
    t(f"run 1: RESULT: OK, {len(exp)} links made", "RESULT: OK" in run1 and f"APPLIED: {len(exp)} link(s) made" in run1, run1[-1200:])
    t("run 2 replaces the links of run 1 (none doubled)", f"({len(exp)} old ones replaced)" in run2 and m
      and m.groups() == (str(len(exp)),) * 3, (run2[-600:], m and m.groups()))
    rects, borders = pdf_links(pdf) if os.path.exists(pdf) else ([], set())
    under = {}
    for u, x in rects:
        under[u] = under.get(u, "") + key(x)
    miss = [f"{k}: {text[:70]}" for text, url, k in exp if key(text) not in under.get(url, "")]
    t(f"PDF: every expected text under a link to its own DOI ({len(exp) - len(miss)}/{len(exp)})", not miss, miss)
    stray = [(u, x) for u, x in rects if not key(x) or not any(key(x) in key(text) for text, url, _ in exp if url == u)]
    t(f"PDF: nothing else linked ({len(rects)} link rectangles, each over part of an expected text)", rects and not stray, stray[:5])
    t("PDF: links invisible (border 0)", borders == {"[0 0 0]"}, borders)
    t("PDF: every URL encoded (no raw < > ; ( ) # ? or space)", rects and not any(re.search(r"[<>;()#? ]", u.split("doi.org/", 1)[1]) for u, _ in rects))
    if not a.keep:
        shutil.rmtree(w, ignore_errors=True)
    n, ok = len(res), sum(res)
    print(f"INDESIGN DOI CHECK ALL PASS {n}/{n}" if ok == n else f"INDESIGN DOI CHECK FAILED {n - ok}/{n}")
    sys.exit(0 if ok == n else 1)


if __name__ == "__main__":
    main()
