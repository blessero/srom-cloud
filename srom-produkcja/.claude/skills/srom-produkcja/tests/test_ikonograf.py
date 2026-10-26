"""srom-ikonograf files: the contact-sheet template renders in the side panel (no lazy images, local thumbnails
embedded, render after the MINI block), carries alt/also; the record template has the footnote-leads section and the image register; queries have their folder; no
User-Agent or command in the skill names the journal's domain (the live-site hook would block it)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IK = os.path.join(ROOT, "srom-ikonograf")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))
def rd(*p):
    return open(os.path.join(IK, *p), encoding="utf-8").read()

html = rd("assets", "template", "kontaktowka.html")
t("template: no lazy <img> (the side panel never loads lazy images)", not re.search(r"<img[^>]*loading=", html))
t("template: local thumbnails come from the MINI block, rendered after it loads",
  "var MINI = {}" in html and "MINI" in html.split("var MINI")[0] and 'addEventListener("DOMContentLoaded", render)' in html
  and html.index("var MINI = {}") > html.index("DOMContentLoaded"))
t("template: better copy (alt) and also-in fields rendered", "Lepsza kopia:" in html and "Też w:" in html)
t("template: size toggle and enlarged view", '"duże"' in html and 'id="lb"' in html)
t("record template: § 7 footnote leads and the zgody.md pointer",
  "## 7. Footnote leads" in rd("assets", "template", "ikonografia.md") and "zgody.md" in rd("assets", "template", "ikonografia.md"))
rec = rd("assets", "template", "ikonografia.md")
t("record template: § 3 is the register of every image (origin, metryka per Kanon § 10.3)",
  "## 3. Register" in rec and "| Il. | origin |" in rec and "Kanon § 10.3" in rec)
t("template: draft metryka field rendered, labelled as a draft", 'metryka:""' in html and "Metryka (szkic):" in html)
sk = rd("SKILL.md")
t("skill: queries kept in work/q-<slug>/ikonografia/ (seen by pobierz.py and Biurko like any record)",
  "## Queries" in sk and "work/q-<slug>/ikonografia/" in sk)
t("skill description within the 1024-character limit", len(re.search(r"^description: (.*)$", sk, re.M)[1]) <= 1024)
bad = [(f, m) for f in ("SKILL.md", "references/sources.md", "references/rights.md")
       for m in re.findall(r"-A\s+\"[^\"]*studiaromologica[^\"]*\"", rd(*f.split("/")))]
t("no User-Agent naming the journal's domain", not bad, bad)

# pobierz.py: Cowork's download list, done on the Mac (file:// URLs, no network)
import random, shutil, struct, subprocess, sys, tempfile, zlib
if shutil.which("sips") is None:  # pobierz.py makes thumbnails with macOS sips
    print("SKIP pobierz: 4 tests (sips not found; macOS only)")
else:
    def png(path, w=120, h=90):
        raw = b"".join(b"\0" + bytes(random.randrange(256) for _ in range(w * 3)) for _ in range(h))
        ch = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                               + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))
    w = tempfile.mkdtemp(); d = os.path.join(w, "x", "ikonografia"); os.makedirs(d)
    shutil.copy(os.path.join(IK, "assets", "template", "kontaktowka.html"), d)
    src = os.path.join(w, "src.png"); png(src)
    journal = "https://" + "studiaromologica" + ".pl/x.jpg"
    open(os.path.join(d, "pobierz.tsv"), "w").write(
        f"# kind\tname\turl\nplik\tx_il01_test.png\tfile://{src}\nminiatura\tS1-a\tfile://{src}\nplik\tbad.jpg\t{journal}\n")
    run = lambda: subprocess.run([sys.executable, os.path.join(IK, "scripts", "pobierz.py"), "--root", w, "--allow-file"],
                                 capture_output=True, text=True)
    r = run(); log = open(os.path.join(d, "pobierz.log")).read().splitlines()
    t("pobierz: plik saved to pliki/ as served", r.returncode == 0 and open(os.path.join(d, "pliki", "x_il01_test.png"), "rb").read() == open(src, "rb").read(), r.stderr + "\n".join(log))
    t("pobierz: miniatura made as JPEG and embedded in the sheet",
      os.path.exists(os.path.join(d, "miniatury", "S1-a.jpg")) and 'MINI["miniatury/S1-a.jpg"]="data:image/jpeg;base64,' in open(os.path.join(d, "kontaktowka.html")).read(), log)
    t("pobierz: the journal's own site refused, logged as FAIL", any("\tFAIL\tbad.jpg\trefused" in l for l in log), log)
    run(); log2 = open(os.path.join(d, "pobierz.log")).read().splitlines()
    t("pobierz: done rows are not fetched again (only the refused row is retried)",
      sum("\tok\t" in l for l in log2) == 2 and sum("\tFAIL\t" in l for l in log2) == 2, log2)
# pobierz.py: MB's copies of the sheets in Claude outputs (no network, no sips)
w2 = tempfile.mkdtemp(); out = os.path.join(w2, "outputs"); work2 = os.path.join(w2, "work")
for rid in ("pahulich", "q-test1"):
    os.makedirs(os.path.join(work2, rid, "ikonografia"))
    open(os.path.join(work2, rid, "ikonografia", "kontaktowka.html"), "w").write(f"<html>{rid}</html>")
mir = lambda *a: subprocess.run([sys.executable, os.path.join(IK, "scripts", "pobierz.py"), "--root", work2, *a],
                                capture_output=True, text=True)
r = mir("--outputs", out, "--mirror")
cp = lambda n: os.path.join(out, f"Kontaktowka - {n}.html")
t("pobierz: sheet mirrored to Claude outputs as Kontaktowka - <Name>.html (text, query)",
  r.returncode == 0 and sorted(os.listdir(out)) == ["Kontaktowka - Pahulich.html", "Kontaktowka - Zapytanie test1.html"]
  and open(cp("Pahulich")).read() == "<html>pahulich</html>", (r.stderr, os.listdir(out) if os.path.isdir(out) else None))
ino = os.stat(cp("Pahulich")).st_ino; mir("--outputs", out, "--mirror"); same = os.stat(cp("Pahulich")).st_ino == ino
srcp = os.path.join(work2, "pahulich", "ikonografia", "kontaktowka.html")
open(srcp, "w").write("<html>rebuilt</html>"); os.utime(srcp, (os.stat(srcp).st_atime, os.stat(srcp).st_mtime + 10))
mir("--outputs", out)  # a normal run (no list to do) mirrors too
t("pobierz: sheet copy left alone when unchanged, refreshed after a rebuild",
  same and open(cp("Pahulich")).read() == "<html>rebuilt</html>" and not [f for f in os.listdir(out) if f.startswith(".")])
mir("--mirror")
t("pobierz: sheet copies never written from a test root without --outputs",
  not os.path.exists(os.path.join(w2, "Claude outputs")) and sorted(os.listdir(w2)) == ["outputs", "work"])
# the triage scripts (known-item search): all compile; montage.py offline, if Pillow is there
import py_compile
bad = []
for f in sorted(os.listdir(os.path.join(IK, "scripts"))):
    if f.endswith(".py"):
        try: py_compile.compile(os.path.join(IK, "scripts", f), cfile=os.path.join(tempfile.mkdtemp(), "x.pyc"), doraise=True)
        except py_compile.PyCompileError as e: bad.append((f, str(e)[:200]))
t("scripts: every srom-ikonograf script compiles under this interpreter", not bad, bad)
try:
    from PIL import Image
except ImportError:
    print("SKIP montage: 2 tests (no Pillow)")
else:
    m = tempfile.mkdtemp(); g = os.path.join(m, "pages"); os.makedirs(g)
    for k in range(23):
        Image.new("RGB", (60 + k, 90), (k * 10, 80, 160)).save(os.path.join(g, f"a10_p{k:03d}.jpg"))
    mt = lambda *a: subprocess.run([sys.executable, os.path.join(IK, "scripts", "montage.py"), *a], capture_output=True, text=True)
    r = mt("--grid", g, "a10_")
    outs = sorted(f for f in os.listdir(m) if f.startswith("mont_"))
    t("montage: --grid makes 20 pages a sheet (23 pages = 2 sheets, 5 columns of 300 px)",
      r.returncode == 0 and outs == ["mont_a10__0.jpg", "mont_a10__1.jpg"]
      and Image.open(os.path.join(m, outs[0])).size == (1500, 1320), (r.stderr[-300:], outs))
    one = os.path.join(m, "one.jpg"); r = mt(one, *[os.path.join(g, f"a10_p{k:03d}.jpg") for k in range(4)])
    t("montage: a list of images makes one sheet, 3 columns of 400 px",
      r.returncode == 0 and Image.open(one).size == (1200, 832), r.stderr[-300:])
print(f"IKONOGRAF ALL PASS {sum(res)}/{len(res)}" if all(res) else f"IKONOGRAF FAILED {res.count(False)}/{len(res)}")
