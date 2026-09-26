"""srom-typeset ↔ srom-kanon: the kanon skill is required and found; its two texts (Polish Kanon = normative,
RULES.md = English digest) carry one version and one section numbering; every § this skill cites exists in
the Kanon; without srom-kanon the build fails and says why."""
import os, re, sys, glob, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import kanon_path
FX = os.path.join(ROOT, "tests", "fixtures")
res = []
def t(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

K = kanon_path.find_kanon()
t("srom-kanon skill found", bool(K), kanon_path.MISSING)
if not K:
    print("KANON FAILED 1/1"); sys.exit(1)
kan = open(os.path.join(K, "references", "kanon-redakcyjny.md"), encoding="utf-8").read()
rules = open(os.path.join(K, "RULES.md"), encoding="utf-8").read()
kv = kanon_path.kanon_version(K)
rv = re.search(r"\(v(\d+\.\d+)\)", rules.splitlines()[0])
t("RULES.md version = Kanon version", kv and rv and rv.group(1) == kv, (kv, rules.splitlines()[0]))
reg = re.findall(r"^\| (\d+\.\d+) \|", kan.split("## 17.")[-1], re.M)
t("Kanon § 17 register ends with the current version", reg and reg[-1] == kv, (reg, kv))
skill = open(os.path.join(K, "SKILL.md"), encoding="utf-8").read()
t("srom-kanon SKILL.md names the current version", f"Kanon v{kv}" in skill)

heads = {m.group(1) for m in re.finditer(r"^#{2,4} (\d+(?:\.\d+)*)\.? ", kan, re.M)}
rheads = {m.group(1) for m in re.finditer(r"^#{2,3} (\d+(?:\.\d+)*)\. ", rules, re.M)}
t("every numbered RULES.md section exists in the Kanon", rheads and rheads <= heads, sorted(rheads - heads))
t("RULES.md § references exist in the Kanon",
  all(n in heads for n in re.findall(r"§ ?(\d+(?:\.\d+)*)", rules)),
  [n for n in re.findall(r"§ ?(\d+(?:\.\d+)*)", rules) if n not in heads])

bad, drafts = [], []
for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
    if os.path.isdir(f) or "__pycache__" in f or f.endswith((".pyc", ".docx")):
        continue
    try:
        txt = open(f, encoding="utf-8").read()
    except UnicodeDecodeError:
        continue
    rel = os.path.relpath(f, ROOT)
    for m in re.finditer(r"§ ?(\d+(?:\.\d+)*)", txt):
        if m.group(1) not in heads:
            bad.append(f"{rel}:{txt[:m.start()].count(chr(10)) + 1} §{m.group(1)}")
    if re.search(r"draft § ?12|kanon v1\.[0-5]|§ ?9 I", txt) and rel != os.path.join("tests", "test_kanon.py"):
        drafts.append(rel)
t("every § cited by srom-typeset exists in the Kanon", not bad, bad)
t("no stale wording (draft § 12…, kanon v1.x, roman-numbered bibliography sections)", not drafts, drafts)

out = tempfile.mkdtemp()
env = dict(os.environ, SROM_KANON=os.path.join(out, "nowhere"))
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), os.path.join(FX, "sample_article.md"),
                    "--refs", os.path.join(FX, "kanon_refs.json"), "--out", out], capture_output=True, text=True, env=env)
rep = open(os.path.join(out, "sample_article_report.md"), encoding="utf-8").read()
t("without srom-kanon the build FAILS and names the missing skill", r.returncode == 1 and "srom-kanon skill not found" in rep, r.stdout)
out2 = tempfile.mkdtemp()
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py"), os.path.join(FX, "sample_article.md"),
                    "--refs", os.path.join(FX, "kanon_refs.json"), "--out", out2], capture_output=True, text=True)
rep = open(os.path.join(out2, "sample_article_report.md"), encoding="utf-8").read()
t("with srom-kanon the build PASSES and the report names the Kanon version", r.returncode == 0 and f"Kanon v{kv}" in rep, rep[:600])
t("srom-typeset bundles no linter of its own", not os.path.exists(os.path.join(ROOT, "scripts", "lint_srom.py")))

n, ok = len(res), sum(res)
print(f"KANON ALL PASS {n}/{n}" if ok == n else f"KANON FAILED {n - ok}/{n}")
