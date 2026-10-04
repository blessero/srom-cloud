"""G10: render the per-article InDesign script templates (Ibidem, post-import, asterisk series) with realistic data (incl. Polish diacritics,
quotes, asterisks) and check they are valid ES3 for ExtendScript."""
import os, sys, json, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build
cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
out = tempfile.mkdtemp()
rows = [(2, "*Ibidem*, s. 17.", "Ficowski, *Cyganie na polskich drogach…*, s. 17."),
        (12, "*Ibidem*, s. 5; „Studia”", "Mróz, *Tytuł \"x\"*, s. 5; „Studia”")]
build.write_jsx(rows, 40, cfg, out, "t", ["* Pierwodruk: „Tytuł” \"x\" żółć", "* Uwaga – przyp. tłum."], True)
files = [os.path.join(out, f) for f in sorted(os.listdir(out))] + [os.path.join(ROOT, "indesign", "srom_zakladki.jsx")]
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), *files], capture_output=True, text=True)
print(r.stdout + r.stderr)

# ---- house-style setup script v3 (style_spec.json -> srom_style_setup.jsx, style-sheet.md)
import re, zipfile
from lxml import etree
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:800]))
spec = json.load(open(os.path.join(ROOT, "indesign", "style_spec.json"), encoding="utf-8"))
sd = tempfile.mkdtemp()
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "make_style_setup.py"), "--out-dir", sd], capture_output=True, text=True)
t("spec renders, is consistent, and config names only spec styles", r.returncode == 0 and "SPEC OK" in r.stdout, r.stdout)
t("shipped setup script is current (regenerated == shipped)", open(os.path.join(sd, "srom_style_setup.jsx"), encoding="utf-8").read() == open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx"), encoding="utf-8").read())
t("shipped style sheet is current (regenerated == shipped)", open(os.path.join(sd, "style-sheet.md"), encoding="utf-8").read() == open(os.path.join(ROOT, "references", "style-sheet.md"), encoding="utf-8").read())
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), os.path.join(sd, "srom_style_setup.jsx")], capture_output=True, text=True)
t("srom_style_setup.jsx is valid ES3", "JSX-DONE" in r.stdout, r.stdout)
jsx = open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx"), encoding="utf-8").read()
t("batch mode never touches the active document (tests pass SROM_TARGET_DOC)", "batch ? SROM_TARGET_DOC : app.activeDocument" in jsx)
t("no localised built-in style names in the script ([None], [No Paragraph Style] by index)", not re.search(r'itemByName\("\[', jsx))
P = {p["name"]: p for p in spec["paragraph"]}
C = {c["name"]: c for c in spec["character"]}
def depth(n, seen=()):
    if n in seen: return 99
    b = P[n]["basedOn"]
    return 0 if not b else 1 + depth(b, seen + (n,))
t("no 'based on' cycles, hierarchy at most 4 deep", all(depth(n) <= 4 for n in P), {n: depth(n) for n in P})
root = [p["name"] for p in spec["paragraph"] if p["group"] == ""]
docx_styles = set(json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))["paragraph"].values())
t("every style the DOCX uses is at the root (InDesign's Word import matches names at the root only), Tekst / Tekst BEZ WCIĘCIA / Przypis first",
  docx_styles <= set(root) and root[:3] == ["Tekst", "Tekst BEZ WCIĘCIA", "Przypis"], sorted(docx_styles - set(root)))
t("at most 30 paragraph and 8 character styles in all", len(P) <= 30 and len(C) <= 8, (len(P), len(C)))
t("names short enough for a narrow panel (≤ 20 characters)", all(len(n) <= 20 for n in list(P) + list(C)), [n for n in list(P) + list(C) if len(n) > 20])
# every style of the vol. 18 templates goes somewhere on purpose
tn = json.load(open(os.path.join(ROOT, "tests", "fixtures", "template_style_names.json"), encoding="utf-8"))
olds = {o for p in spec["paragraph"] for o in p.get("old", []) + list(p.get("old_if", {}))}
t("every paragraph style of the two vol. 18 templates is mapped explicitly", not [n for n in tn["paragraph"] if not n.startswith("$ID/") and n not in olds],
  [n for n in tn["paragraph"] if not n.startswith("$ID/") and n not in olds])
cold = {o for c in spec["character"] for o in c.get("old", [])} | set(spec["char_retire"])
t("every character style of the two templates is mapped or retired", not [n for n in tn["character"] if not n.startswith("$ID/") and n.split(":")[-1] not in cold],
  [n for n in tn["character"] if not n.startswith("$ID/") and n.split(":")[-1] not in cold])
# the sacred values (MB 29.09.2026): body 10.5/13 on the 13.2945 grid, notes 9/10.8 off the grid, Cambria, quote 9 pt / 1 cm
def eff(n):
    out = {}
    chain = []
    while n:
        chain.append(n); n = P[n]["basedOn"]
    for n in reversed(chain):
        out.update(P[n]["props"])
    return out
fpj = open(os.path.join(ROOT, "indesign", "srom_final_pass.jsx"), encoding="utf-8").read()
t("final pass: shipped script is current (regenerated == shipped)", open(os.path.join(sd, "srom_final_pass.jsx"), encoding="utf-8").read() == fpj)
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), os.path.join(sd, "srom_final_pass.jsx")], capture_output=True, text=True)
t("final pass: valid ES3", "JSX-DONE" in r.stdout, r.stdout)
t("final pass: one undo step, batch mode never on the active document",
  "UndoModes.ENTIRE_SCRIPT" in fpj and "batch ? SROM_TARGET_DOC : app.activeDocument" in fpj)
fp = spec["final_pass"]
t("final pass: Kanon § 3.6 checks present (szewc, bękart, wdowa, heading, one-letter word, URL, overset)",
  all(k in fpj for k in ('"SZEWC"', '"BĘKART"', '"WDOWA"', '"ŚRÓDTYTUŁ"', '"SIEROTKA"', '"URL"', "OVERSET")))
t("final pass: tracking remedies stay within ±10 (vol. 18 practice)", max(abs(x) for x in fp["tracking_steps"]) <= fp["max_tracking"] <= 10, fp)
t("final pass: every heading style keeps with next (Kanon § 3.6), except the title block", all(eff(n).get("keepWithNext", 0) >= 1 for n in fp["headings"] if n not in ("Tytuł", "Autor")),
  {n: eff(n).get("keepWithNext") for n in fp["headings"]})
tk, pz, cy = eff("Tekst"), eff("Przypis"), eff("Cytat")
t("Tekst = Cambria 10.5/13, grid, tracking 0, H&J 85/100/115 · −3/−1/+1 · 98/100/102", (tk["appliedFont"], tk["pointSize"], tk["leading"], tk["gridAlignment"], tk["tracking"],
  tk["minimumWordSpacing"], tk["maximumWordSpacing"], tk["minimumLetterSpacing"], tk["desiredLetterSpacing"], tk["maximumLetterSpacing"], tk["minimumGlyphScaling"], tk["maximumGlyphScaling"])
  == ("Cambria", 10.5, 13, "ALIGN_BASELINE", 0, 85, 115, -3, -1, 1, 98, 102), tk)
t("Przypis = 9/10.8, off the grid (a grid-aligned note would get 13.29 pt lines)", (pz["pointSize"], pz["leading"], pz["gridAlignment"]) == (9, 10.8, "NONE"), pz)
t("Cytat = 9/10.8 on the grid, indent 1 cm", (cy["pointSize"], cy["leading"], cy["gridAlignment"], round(cy["leftIndent"] / 72 * 2.54, 3)) == (9, 10.8, "ALIGN_BASELINE", 1.0), cy)
g = spec["document"]["grid"]
t("baseline grid 13.2945 pt from 62.362 pt (kept from 18 volumes)", (round(g["baselineDivision"], 4), round(g["baselineStart"], 3)) == (13.2945, 62.362), g)
# fidelity: the vol. 18 IDMLs in dump/ — the styles the spec keeps must resolve to the same values
DUMP = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ROOT))), "dump")
IDML = {"PointSize": "pointSize", "Leading": "leading", "Tracking": "tracking", "FirstLineIndent": "firstLineIndent", "LeftIndent": "leftIndent",
        "SpaceBefore": "spaceBefore", "SpaceAfter": "spaceAfter", "Justification": "justification", "GridAlignment": "gridAlignment",
        "Capitalization": "capitalization", "Hyphenation": "hyphenation", "FontStyle": "fontStyle", "MinimumWordSpacing": "minimumWordSpacing",
        "MaximumWordSpacing": "maximumWordSpacing", "MinimumLetterSpacing": "minimumLetterSpacing", "DesiredLetterSpacing": "desiredLetterSpacing",
        "MaximumLetterSpacing": "maximumLetterSpacing", "MinimumGlyphScaling": "minimumGlyphScaling", "MaximumGlyphScaling": "maximumGlyphScaling",
        "HyphenateAfterFirst": "hyphenateAfterFirst", "HyphenateBeforeLast": "hyphenateBeforeLast", "HyphenationZone": "hyphenationZone",
        "HyphenateWordsLongerThan": "hyphenateWordsLongerThan", "DropCapLines": "dropCapLines", "DropCapCharacters": "dropCapCharacters",
        "RuleAbove": "ruleAbove", "RuleAboveOffset": "ruleAboveOffset", "KeepRuleAboveInFrame": "keepRuleAboveInFrame", "RuleBelow": "ruleBelow", "RuleBelowOffset": "ruleBelowOffset"}
def enum(v):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", v).upper()
def idml_eff(path):
    z = zipfile.ZipFile(path)
    st = etree.fromstring(z.read("Resources/Styles.xml"))
    d = {}
    for e in st.iter("ParagraphStyle"):
        b = e.find("Properties/BasedOn")
        a = dict(e.attrib)
        for x in (e.find("Properties") if e.find("Properties") is not None else []):
            if x.tag in ("Leading",) and x.text: a["Leading"] = x.text
        d[e.get("Name")] = (b.text.replace("ParagraphStyle/", "") if b is not None and b.text else None, a)
    def resolve(n):
        if n not in d: return {}
        b, a = d[n]
        r = dict(resolve(b)) if b and b != n else {}
        r.update(a); return r
    return resolve
def conv(k, v):
    if k == "FontStyle": return v
    if v in ("true", "false"): return v == "true"
    try: return round(float(v), 3)
    except ValueError: return {"AlignBaseline": "ALIGN_BASELINE", "None": "NONE", "AllCaps": "ALL_CAPS", "Normal": "NORMAL"}.get(v, enum(v))
KEEP = [("Tekst", "09_Konferencja", "Tekst"), ("Tekst BEZ WCIĘCIA", "09_Konferencja", "Bez wciecia"), ("Przypis", "03_Ellis", "Przypis"), ("Przypis", "09_Konferencja", "Przypis"),
        ("Śródtytuł", "09_Konferencja", "Podrozdzial"), ("Bibliografia", "03_Ellis", "Literatura"), ("Autor", "09_Konferencja", "Autor"), ("Afiliacja", "09_Konferencja", "Uni"),
        ("Podpis LINIA", "03_Ellis", "Podpisy"), ("Tekst INICJAŁ", "09_Konferencja", "Inicjal")]
if os.path.isdir(DUMP):
    bad, compared = {}, 0
    for new, f, old in KEEP:
        o = idml_eff(os.path.join(DUMP, f + ".idml"))(old); n = eff(new)
        for ik, sk in IDML.items():
            if ik in o and sk in n:
                compared += 1
            if ik in o and sk in n and conv(ik, o[ik]) != (round(n[sk], 3) if isinstance(n[sk], float) else n[sk]):
                if not (sk == "justification" and new == "Autor") and not (sk == "hyphenation" and new == "Autor") \
                        and not (sk == "spaceBefore" and new == "Śródtytuł"):   # deliberate: Autor one-line name; heading gap (MB 02.10.2026)
                    bad.setdefault(new, []).append((sk, o[ik], n[sk]))
    t(f"kept styles resolve to the vol. 18 values (dump/*.idml; {compared} values compared)", not bad and compared > 150, (compared, bad))
else:
    t("kept styles resolve to the vol. 18 values (dump/ missing: skipped)", True)
n, ok = len(res), sum(res)
print(f"STYLES ALL PASS {n}/{n}" if ok == n else f"STYLES FAILED {n - ok}/{n}")
