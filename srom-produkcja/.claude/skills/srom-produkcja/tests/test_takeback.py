"""Hand-back of a translation (handoff.md "Back", review 29.09.2026 row 3): take_back.py copies a delivery from
srom-tlumacz's folder, compares sha256 with the delivery line, requires the delivered SROM-MD to be the import of
the editor's Word master, and runs the handoff check; handoff.md and SKILL.md describe that path."""
import hashlib, json, os, re, shlex, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, FX = os.path.join(ROOT, "scripts"), os.path.join(ROOT, "tests", "fixtures")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
def py(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
def ab(h):
    return f"{h[:8]}…{h[-7:]}"

d = tempfile.mkdtemp()
typ = os.path.join(d, "typeset", "work", "art")                 # srom-produkcja's article folder
os.makedirs(typ)
shutil.copy(os.path.join(FX, "sample_article.md"), os.path.join(typ, "art_src.md"))
shutil.copy(os.path.join(FX, "kanon_refs.json"), os.path.join(typ, "refs.json"))

def delivery(name, md_edit=None, docx_edit=None, refs_tlum=False, queries=False, front=True):
    """a delivery folder as srom-tlumacz leaves it: Word master exported from the translation, md = its import"""
    dl = os.path.join(d, "tlumacz", name)
    os.makedirs(dl)
    src = open(os.path.join(typ, "art_src.md"), encoding="utf-8").read()
    pl = os.path.join(dl, "draft.md")
    open(pl, "w", encoding="utf-8").write(docx_edit(src) if docx_edit else src)
    py(os.path.join(S, "export_work.py"), pl, "-o", os.path.join(dl, "art_robocza.docx"))
    os.remove(pl)
    py(os.path.join(S, "docx_in.py"), os.path.join(dl, "art_robocza.docx"), "-o", os.path.join(dl, "art_pl.md"))
    for f in os.listdir(dl):                                       # the import report is not part of a delivery
        if f.endswith("_import.md"):
            os.remove(os.path.join(dl, f))
    if md_edit:
        p = os.path.join(dl, "art_pl.md")
        open(p, "w", encoding="utf-8").write(md_edit(open(p, encoding="utf-8").read()))
    if front:
        open(os.path.join(dl, "art_front_pl.md"), "w", encoding="utf-8").write("# Tytuł\nTytuł\n")
    if refs_tlum:
        json.dump([{"id": "dodane2001", "type": "book", "title": "Dodane", "issued": {"date-parts": [[2001]]},
                    "srom-added": "tlum", "srom-source": "https://example.org/isbn"}],
                  open(os.path.join(dl, "art_refs_tlum.json"), "w", encoding="utf-8"))
    if queries:
        open(os.path.join(dl, "art_pytania_tlum.csv"), "w", encoding="utf-8").write("adresat;rodzaj;przypis;dzieło;szczegóły\n")
    return dl

def take(dl, *extra, out=None):
    out = out or os.path.join(d, "out_" + os.path.basename(dl))
    r = py(os.path.join(S, "take_back.py"), dl, "art", "--src-dir", typ, "--out", out, *extra)
    return r, out

# 1. a clean delivery
dl = delivery("good", refs_tlum=True, queries=True)
before = {f: sha(os.path.join(dl, f)) for f in os.listdir(dl)}
exp = [f"--expect={f}={ab(h)}" for f, h in before.items()]
r, out = take(dl, *exp)
t("clean delivery: TAKE-BACK OK with all five files", r.returncode == 0 and "TAKE-BACK OK art (5 files)" in r.stdout, r.stdout + r.stderr)
t("clean delivery: copies identical to the delivered files", all(sha(os.path.join(out, f)) == h for f, h in before.items()))
sums = open(os.path.join(out, "SHA256SUMS"), encoding="utf-8").read() if os.path.isfile(os.path.join(out, "SHA256SUMS")) else ""
t("SHA256SUMS written in shasum -c format", all(f"{h}  {f}\n" in sums for f, h in before.items()), sums)
t("the delivery folder is left untouched (read only)", {f: sha(os.path.join(dl, f)) for f in os.listdir(dl)} == before)
t("the pair check ran with the translation's refs (added citation accepted)", "check.py --pair: CHECK OK" in r.stdout, r.stdout)
t("the build command is printed with both --refs, --pair-src and --queries",
  re.search(r"build\.py'? .*build/art_pl\.md --refs .*refs\.json --refs .*art_refs_tlum\.json --pair-src .*art_src\.md --queries .*art_pytania_tlum\.csv", r.stdout),
  r.stdout)
r2, _ = take(dl, *[f"--expect={f}={h}" for f, h in before.items()], out=os.path.join(d, "out_full"))
t("full sha256 values are accepted too", r2.returncode == 0, r2.stdout)

# 2. sha256 does not match the delivery line / line incomplete
bad = [e if "art_pl.md" not in e else "--expect=art_pl.md=00000000…0000000" for e in exp]
r, _ = take(dl, *bad, out=os.path.join(d, "out_badsha"))
t("a sha256 that differs from the delivery line fails", r.returncode == 1 and "sha256 differs from the delivery line: art_pl.md" in r.stdout, r.stdout)
r, _ = take(dl, *exp[:-1], out=os.path.join(d, "out_partial"))
t("with --expect, a file the item does not list fails", r.returncode == 1 and "no --expect for" in r.stdout, r.stdout)
t("nothing is copied when the sha256 check fails", not os.path.exists(os.path.join(d, "out_badsha")))

# 3. the md is not the import of the Word master
dl = delivery("mdedited", md_edit=lambda s: s.replace("\n\n", "\n\nZdanie dopisane po imporcie.\n\n", 1))
r, _ = take(dl)
t("an md edited after the import fails (the Word file is the master)",
  r.returncode == 1 and "is not the import of art_robocza.docx" in r.stdout, r.stdout)

# 4. required file missing
dl = delivery("nofront", front=False)
r, _ = take(dl)
t("a delivery without <id>_front_pl.md fails", r.returncode == 1 and "missing in the delivery: art_front_pl.md" in r.stdout, r.stdout)

# 5. the Word master breaks the pair (a note lost in Word): md and docx agree, the handoff check fails
src_txt = open(os.path.join(typ, "art_src.md"), encoding="utf-8").read()
m = re.search(r"\[\^(\d+)\]", src_txt)
lab = m.group(1)
def drop_note(s):
    s = s.replace(f"[^{lab}]", "", 1)
    return re.sub(rf"\n\[\^{lab}\]:[^\n]*\n", "\n", s, count=1)
dl = delivery("lostnote", docx_edit=drop_note)
r, _ = take(dl)
t("a note lost in the Word master fails the handoff check", r.returncode == 1 and "check.py --pair fails" in r.stdout, r.stdout)

# 6. --out inside the other module's folder is refused
dl = delivery("inside")
r, _ = take(dl, out=os.path.join(dl, "copy"))
t("--out inside the delivery folder is refused", r.returncode != 0 and "must not be inside the delivery folder" in (r.stdout + r.stderr))

# 6b. INJECT normalises outside pl/ (review 07.10.2026 F3): a Word master that lost a note's full stop is taken back,
# the printed normalise command writes to build/, the printed build passes without --draft, pl/ still verifies
nostop = lambda s: re.sub(r"(\n\[\^2\]:[^\n]*)\.\n", r"\1\n", s, count=1)
dl = delivery("nostop", docx_edit=nostop)
r, out = take(dl)
t("6b: a delivery that needs NOTE-FULLSTOP is taken back", r.returncode == 0, r.stdout)
cmds = {k: shlex.split(v) for k, v in re.findall(r"^  (normalise|build): python3 (.+)$", r.stdout, re.M)}
t("6b: the normalise command reads pl/ and writes into <src-dir>/build/",
  cmds.get("normalise", [])[:4] == [os.path.join(S, "normalize.py"), f"{out}/art_pl.md", "-o", f"{typ}/build/art_pl.md"], r.stdout)
plain = py(os.path.join(S, "build.py"), os.path.join(out, "art_pl.md"), "--refs", os.path.join(typ, "refs.json"),
           "--pair-src", os.path.join(typ, "art_src.md"), "--out", os.path.join(d, "b_plain"))
t("6b control: building the copy itself fails on normalisation and names build/ as the output",
  plain.returncode != 0 and "not normalised" in open(os.path.join(d, "b_plain", "art_pl_report.md"), encoding="utf-8").read()
  and "write the output to build/" in open(os.path.join(d, "b_plain", "art_pl_report.md"), encoding="utf-8").read(), plain.stdout)
rn = subprocess.run([sys.executable, *cmds.get("normalise", ["x"])], capture_output=True, text=True)
rb = subprocess.run([sys.executable, *cmds.get("build", ["x"])], capture_output=True, text=True)
t("6b: normalise (1 change, 0 flags) then build without --draft → PASS",
  "1 changes, 0 flags" in rn.stdout and rb.returncode == 0 and "PASS" in rb.stdout, rn.stdout + rb.stdout + rb.stderr)
sc = subprocess.run(["shasum", "-a", "256", "-c", "SHA256SUMS"], cwd=out, capture_output=True, text=True)
t("6b: pl/ is untouched (SHA256SUMS verifies)", sc.returncode == 0, sc.stdout + sc.stderr)

# 7. contract text: handoff.md and SKILL.md describe the hand-back as implemented
HO = open(os.path.join(ROOT, "references", "handoff.md"), encoding="utf-8").read()
back = HO.split("## Back", 1)[1] if "## Back" in HO else ""
t("handoff.md 'Back': the editor's Word file in srom-tlumacz's work/<id>/ is the master",
  "master" in back and "work/<id>/" in back and "<id>_robocza.docx" in back, back[:600])
t("handoff.md 'Back': srom-tlumacz imports; a delivery line in the hand-off log lists the files with sha256",
  "delivery line" in back and "sha256" in back and all(f"`<id>_{x}`" in back for x in ("pl.md", "front_pl.md", "refs_tlum.json", "pytania_tlum.csv", "robocza.docx")), back[:1500])
t("handoff.md 'Back': srom-produkcja takes it with take_back.py into work/<id>/pl/ and builds from there",
  "take_back.py" in back and "work/<id>/pl/" in back and "build.py" in back, back[:1500])
t("handoff.md 'Back': normalize.py writes the copy into work/<id>/build/, never in place, and build.py builds that file",
  "normalize.py" in back and "work/<id>/build/<id>_pl.md" in back and "never in place" in back
  and "build.py srom-produkcja/work/<id>/build/<id>_pl.md" in back, back[:2500])
t("handoff.md 'Back': never re-export over the master", re.search(r"(?i)never .{0,60}(re-?export|overwrite)", back), back[:1500])
SK = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
scen = SK.split("**C. Translated article**", 1)[1].split("\n\n", 1)[0] if "**C. Translated article**" in SK else ""
t("SKILL.md scenario C: take_back.py, and srom-tlumacz does the import", "take_back.py" in scen and "srom-tlumacz" in scen and "delivery" in scen, scen)

n, ok = len(res), sum(res)
print(f"TAKEBACK ALL PASS {n}/{n}" if ok == n else f"TAKEBACK FAILED {n - ok}/{n}")
sys.exit(0 if ok == n else 1)
