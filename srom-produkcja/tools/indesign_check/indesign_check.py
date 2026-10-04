#!/usr/bin/env python3
"""
indesign_check.py — live check of srom_style_setup.jsx in InDesign (the editor's Mac; InDesign must be running).
Not part of run_all.py: it drives InDesign through AppleScript, in hidden windows, on copies in a temp folder —
the documents open in InDesign are never touched.

    ~/.venvs/srom/bin/python tools/indesign_check/indesign_check.py [--specimen out.pdf] [--keep DIR]

For each vol. 18 template in dump/ (03_Ellis, 09_Konferencja):
  before   the IDML as it is → PDF
  control  the setup script with the deliberate changes undone (vol. 18 GREP rule only, the document's own
           Cytat blokowy values, no keep-with-next on headings) → PDF; must equal `before` line for line (text,
           position, size, font): proves that the new styles, the purge and the mapping move nothing
  keeps    control + the headings' keep-with-next → PDF; lists the headings that closed a column in vol. 18
           (Kanon § 3.6) and now move on
  real     the shipped setup script → PDF; same page count; lines re-broken are reported (Kanon § 3.3 no-break rules,
           the unified Cytat)
  final    the final pass (srom_final_pass.jsx) after the real setup, report-only and fix: the fix run may not leave more
           problems than the report run, nor add overset or pages
and once on a blank document. Every run must end RESULT: OK. --template OUT.idml also builds the clean template
(make_template.jsx, from 03_Ellis) and checks it by opening it again. Last line: INDESIGN CHECK ALL PASS n/n.
"""
import argparse, copy, difflib, json, os, shutil, subprocess, sys, tempfile
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
FULL_PAGES = {"03_Ellis": 14, "09_Konferencja": 12}   # pages of the vol. 18 files in dump/
REPO = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(REPO, ".claude", "skills", "srom-produkcja")
DUMP = os.path.join(REPO, "dump")
# the vol. 18 values of Cytat blokowy (read in InDesign, 29.09.2026) — the control run puts them back
OLD_CYTAT = {
    "03_Ellis": {"pointSize": 9, "leading": 12, "tracking": -10, "composer": "Adobe Paragraph Composer", "hyphenateAfterFirst": 2,
                 "hyphenateBeforeLast": 2, "hyphenateLadderLimit": 3, "hyphenateWordsLongerThan": 5, "hyphenationZone": 36,
                 "hyphenateLastWord": False, "minimumWordSpacing": 80, "maximumWordSpacing": 133, "desiredLetterSpacing": 0,
                 "minimumLetterSpacing": 0, "maximumLetterSpacing": 0, "minimumGlyphScaling": 100, "maximumGlyphScaling": 100},
    "09_Konferencja": {"pointSize": 9.5, "leading": 12},
}


def idrun(jsx, *args):
    al = ", ".join(json.dumps(a) for a in args)
    r = subprocess.run(["osascript", "-e", "with timeout of 900 seconds",
                        "-e", f'tell application id "com.adobe.InDesign" to do script (POSIX file {json.dumps(jsx)}) language javascript with arguments {{{al}}}',
                        "-e", "end timeout"], capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def lines(pdf):
    out = []
    for pn, page in enumerate(pymupdf.open(pdf)):
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                tx = "".join(s["text"] for s in l["spans"]).strip()
                if tx:
                    out.append((pn + 1, round(l["bbox"][0], 1), round(l["bbox"][3], 1), round(l["spans"][0]["size"], 1), l["spans"][0]["font"], tx))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specimen", help="also build a style specimen PDF here")
    ap.add_argument("--keep", help="work in this folder and keep it (default: a temp folder, deleted)")
    ap.add_argument("--template", help="also build the clean SROM template IDML here (+ a PDF preview next to it)")
    ap.add_argument("--no-final", action="store_true", help="skip the final-pass runs (they take a few minutes)")
    a = ap.parse_args()
    w = a.keep or tempfile.mkdtemp(prefix="srom_idcheck_")
    os.makedirs(w, exist_ok=True)
    for f in ("runner.jsx", "dumplib.jsxinc", "specimen.jsx", "finalrun.jsx", "make_template.jsx"):
        shutil.copy(os.path.join(HERE, f), w)
    spec = json.load(open(os.path.join(SKILL, "indesign", "style_spec.json"), encoding="utf-8"))
    tpl = open(os.path.join(SKILL, "indesign", "srom_style_setup.jsx.tpl"), encoding="utf-8").read()
    setup = os.path.join(w, "setup.jsx")
    shutil.copy(os.path.join(SKILL, "indesign", "srom_style_setup.jsx"), setup)
    runner = os.path.join(w, "runner.jsx")
    final = os.path.join(w, "final.jsx")
    shutil.copy(os.path.join(SKILL, "indesign", "srom_final_pass.jsx"), final)
    res = []

    def t(name, ok, detail=""):
        res.append(ok)
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

    for stem in ("03_Ellis", "09_Konferencja"):
        idml = os.path.join(w, stem + ".idml")
        shutil.copy(os.path.join(DUMP, stem + ".idml"), idml)
        sp = copy.deepcopy(spec)
        sp["document"]["footnotes"]["separatorText"] = ".\u2002"        # vol. 18: "." + en space (MB 02.10.2026: no dot)
        for p in sp["paragraph"]:
            if p["name"] == "Tekst":
                p["grep"] = p["grep"][:1]
            if p["name"] == "Cytat":
                p["props"].update(OLD_CYTAT[stem])
            for k in ("spaceBefore", "spaceAfter"):                      # vol. 18 typed empty paragraphs (MB 02.10.2026: style gaps)
                if k in p["props"]:
                    p["props"][k] = 0
        keeps = os.path.join(w, f"keeps_{stem}.jsx")
        open(keeps, "w", encoding="utf-8").write(tpl.replace("/*SPEC*/", json.dumps(sp, ensure_ascii=True)))
        for p in sp["paragraph"]:
            if "keepWithNext" in p["props"]:
                p["props"]["keepWithNext"] = 0
        control = os.path.join(w, f"control_{stem}.jsx")
        open(control, "w", encoding="utf-8").write(tpl.replace("/*SPEC*/", json.dumps(sp, ensure_ascii=True)))
        P = {k: os.path.join(w, f"{stem}_{k}") for k in ("before", "control", "keeps", "real")}
        idrun(runner, "open", idml, "", P["before"] + ".txt", P["before"] + ".json", P["before"] + ".pdf")
        rc = idrun(runner, "open", idml, control, P["control"] + ".txt", P["control"] + ".json", P["control"] + ".pdf")
        rk = idrun(runner, "open", idml, keeps, P["keeps"] + ".txt", P["keeps"] + ".json", P["keeps"] + ".pdf")
        rr = idrun(runner, "open", idml, setup, P["real"] + ".txt", P["real"] + ".json", P["real"] + ".pdf")
        t(f"{stem}: control run RESULT: OK", rc == "RESULT: OK", rc)
        t(f"{stem}: keeps run RESULT: OK", rk == "RESULT: OK", rk)
        t(f"{stem}: real run RESULT: OK", rr == "RESULT: OK", open(P["real"] + ".txt", encoding="utf-8").read().replace("\r", "\n")[-1500:] if os.path.exists(P["real"] + ".txt") else rr)
        b, c, r = lines(P["before"] + ".pdf"), lines(P["control"] + ".pdf"), lines(P["real"] + ".pdf")
        np_ = pymupdf.open(P["before"] + ".pdf").page_count
        t(f"{stem}: whole document exported ({np_} pages; InDesign reuses the last export's page range otherwise)", np_ == FULL_PAGES[stem], np_)
        same = sum(1 for x, y in zip(b, c) if x == y)
        t(f"{stem}: control = vol. 18 line for line ({same}/{len(b)} lines: text, position, size, font)", same == len(b) == len(c),
          [(x, y) for x, y in zip(b, c) if x != y][:5])
        k = lines(P["keeps"] + ".pdf")
        first = next((i for i, (x, y) in enumerate(zip(b, k)) if x != y), None)
        if first is not None:
            x = b[first]
            print(f"     info: keep-with-next moves the text from p. {x[0]} on: in vol. 18 a heading closed a column there "
                  f"(Kanon § 3.6): {[y[5][:40] for y in b[max(0, first - 2):first + 1] if y[0] == x[0]]}")
        pk = pymupdf.open(P["keeps"] + ".pdf").page_count
        pb, pr = pymupdf.open(P["before"] + ".pdf").page_count, pymupdf.open(P["real"] + ".pdf").page_count
        t(f"{stem}: keeps run keeps the page count ({pb} → {pk})", pb == pk)
        # the real run adds the heading and quotation gaps (02.10.2026) on top of vol. 18's typed empty paragraphs
        t(f"{stem}: real run adds at most one page ({pb} → {pr})", pb <= pr <= pb + 1, (pb, pr))
        sm = difflib.SequenceMatcher(None, [x[5] for x in b], [x[5] for x in r], autojunk=False)
        moved = sum(i2 - i1 for op, i1, i2, _, _ in sm.get_opcodes() if op in ("replace", "delete"))
        print(f"     info: {moved}/{len(b)} lines re-broken in the real run (no-break rules of Kanon § 3.3, unified Cytat)")
        if not a.no_final:
            fr = os.path.join(w, "finalrun.jsx")
            out = {}
            for mode in ("report", "fix"):
                rep_ = os.path.join(w, f"{stem}_final_{mode}.txt")
                res_ = idrun(fr, idml, setup, final, mode, rep_, os.path.join(w, f"{stem}_final_{mode}.pdf") if mode == "fix" else "")
                txt = open(rep_, encoding="utf-8").read().replace("\r", "\n") if os.path.exists(rep_) else ""
                out[mode] = (res_, txt, sum(1 for l in txt.splitlines() if l.startswith("   !")), sum(1 for l in txt.splitlines() if "OVERSET" in l))
                t(f"{stem}: final pass ({mode}) ran to a RESULT line", "RESULT:" in txt and "ERROR" not in res_, res_ + "\n" + txt[-800:])
            fixed = sum(1 for l in out["fix"][1].splitlines() if l.startswith("   fixed"))
            t(f"{stem}: final pass fix mode: {out['report'][2]} problems → {out['fix'][2]} ({fixed} fixed), no new overset",
              out["fix"][2] <= out["report"][2] and out["fix"][3] <= out["report"][3], (out["report"][1], out["fix"][1]))
            pf = os.path.join(w, f"{stem}_final_fix.pdf")
            if os.path.exists(pf):
                t(f"{stem}: final pass fix mode keeps the page count", pymupdf.open(pf).page_count == pb, pymupdf.open(pf).page_count)
            print("     final pass report:\n" + "\n".join("       " + l for l in out["fix"][1].splitlines() if l.startswith("   ")))
    rb = idrun(runner, "new", "x", setup, os.path.join(w, "blank.txt"), os.path.join(w, "blank.json"), "")
    t("blank document: RESULT: OK", rb == "RESULT: OK", rb)
    try:
        order = json.loads(open(os.path.join(w, "blank.json"), encoding="utf-8").read(), strict=False)["DOC|order"]
        want = [p["name"] for p in spec["paragraph"] if p["group"] == ""]
        got = [x[2:] for x in order if x.startswith("P:") and not x.startswith("P:[")]
        t("panel order at the root = spec order", got == want, (got, want))
    except (OSError, ValueError, KeyError) as e:
        t("panel order readable", False, e)
    if a.template:
        tpl_out = os.path.abspath(a.template)
        for old in (tpl_out, tpl_out[:-5] + "_podglad.pdf"):
            if os.path.exists(old):
                os.remove(old)                        # the re-open check must read the new file
        rt = idrun(os.path.join(w, "make_template.jsx"), os.path.join(DUMP, "03_Ellis.idml"), setup, tpl_out,
                   tpl_out[:-5] + "_podglad.pdf", os.path.join(w, "template.txt"))
        print("     " + open(os.path.join(w, "template.txt"), encoding="utf-8").read().replace("\n", "\n     ") if os.path.exists(os.path.join(w, "template.txt")) else rt)
        t("template built (RESULT: OK)", rt == "RESULT: OK", rt)
        idrun(runner, "open", tpl_out, "", os.path.join(w, "tpl.txt"), os.path.join(w, "tpl.json"), "")
        try:
            dj = json.loads(open(os.path.join(w, "tpl.json"), encoding="utf-8").read(), strict=False)
            pn = [k for k in dj if k.startswith("P|") and not k.split("|")[2].startswith("[")]
            cn = [k for k in dj if k.startswith("C|") and not k.split("|")[2].startswith("[")]
            g = dj["DOC|grid"]; fo = dj["DOC|fn"]
            t(f"template re-opened: {len(pn)} paragraph + {len(cn)} character styles, grid 13.2945 from 62.362, footnotes in Przypis",
              len(pn) == len(spec["paragraph"]) and len(cn) == len(spec["character"]) and abs(g["baselineDivision"] - 13.2944881889764) < 1e-6
              and abs(g["baselineStart"] - 62.3622047244095) < 1e-6 and fo["footnoteTextStyle"].endswith(":Przypis") and fo["noSplitting"] is False,
              (len(pn), len(cn), g, fo.get("footnoteTextStyle")))
        except (OSError, ValueError, KeyError) as e:
            t("template re-opened and read", False, e)
    if a.specimen:
        rs = idrun(os.path.join(w, "specimen.jsx"), setup, os.path.abspath(a.specimen))
        t(f"specimen written ({a.specimen})", rs.startswith("RESULT: OK") and "overset false" in rs, rs)
    if not a.keep:
        shutil.rmtree(w, ignore_errors=True)
    n, ok = len(res), sum(res)
    print(f"INDESIGN CHECK ALL PASS {n}/{n}" if ok == n else f"INDESIGN CHECK FAILED {n - ok}/{n}")
    sys.exit(0 if ok == n else 1)


if __name__ == "__main__":
    main()
