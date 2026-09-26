"""G10: render both InDesign script templates with realistic data (incl. Polish diacritics,
quotes, asterisks) and check they are valid ES3 for ExtendScript."""
import os, sys, json, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build
cfg = json.load(open(os.path.join(ROOT, "config", "styles.json"), encoding="utf-8"))
out = tempfile.mkdtemp()
rows = [(2, "*Ibidem*, s. 17.", "Ficowski, *Cyganie na polskich drogach…*, s. 17."),
        (12, "*Ibidem*, s. 5; „Studia”", "Mróz, *Tytuł \"x\"*, s. 5; „Studia”")]
build.write_jsx(rows, 40, cfg, out, "t")
files = [os.path.join(out, f) for f in sorted(os.listdir(out))]
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), *files], capture_output=True, text=True)
print(r.stdout + r.stderr)

# ---- house-style setup script (style_spec.json -> srom_style_setup.jsx)
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:800]))
spec = json.load(open(os.path.join(ROOT, "indesign", "style_spec.json"), encoding="utf-8"))
sd = tempfile.mkdtemp()
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "make_style_setup.py"), "--out-dir", sd], capture_output=True, text=True)
t("spec renders and config names only spec styles", r.returncode == 0 and "SPEC OK" in r.stdout, r.stdout)
t("shipped setup script is current (regenerated == shipped)", open(os.path.join(sd, "srom_style_setup.jsx"), encoding="utf-8").read() == open(os.path.join(ROOT, "indesign", "srom_style_setup.jsx"), encoding="utf-8").read())
r = subprocess.run(["node", os.path.join(ROOT, "tests", "es3check.mjs"), os.path.join(sd, "srom_style_setup.jsx")], capture_output=True, text=True)
t("srom_style_setup.jsx is valid ES3", "JSX-DONE" in r.stdout, r.stdout)
para = {spec["base"]["name"]: None}
for g in spec["groups"]:
    for s in g["styles"]:
        para[s["name"]] = s.get("basedOn")
t("every 'based on' exists", all(b in para for b in para.values() if b), [b for b in para.values() if b and b not in para])
def depth(n, seen=()):
    if n in seen: return 99
    b = para.get(n)
    return 0 if not b else 1 + depth(b, seen + (n,))
t("no 'based on' cycles, hierarchy at most 4 deep", all(depth(n) <= 4 for n in para), {n: depth(n) for n in para})
tn = json.load(open(os.path.join(ROOT, "tests", "fixtures", "template_style_names.json"), encoding="utf-8"))
olds = {o for g in spec["groups"] for s in g["styles"] for o in s.get("old", [])} | set(para) | set(spec["leftovers"]["names"])
unmapped = [n for n in tn["paragraph"] if not n.startswith("$ID/") and n not in olds]
t("every paragraph style of the two templates is mapped, kept or retired", not unmapped, unmapped)
cold = {o for c in spec["character"] for o in c.get("old", [])} | {c["name"] for c in spec["character"]} | set(spec["char_leftovers"]) | set(spec["char_keep"])
cun = [n for n in tn["character"] if not n.startswith("$ID/") and n not in cold]
t("every character style of the two templates is mapped, kept or retired", not cun, cun)
t("no name used for both a paragraph and a character style (Word forbids it)", not (set(para) & {c["name"] for c in spec["character"]}), set(para) & {c["name"] for c in spec["character"]})
n, ok = len(res), sum(res)
print(f"STYLES ALL PASS {n}/{n}" if ok == n else f"STYLES FAILED {n - ok}/{n}")
