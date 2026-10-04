"""--shape: four example folders with README, non-empty input/ and expected/.
--run <bundle>: copy each example, delete the produced files, run the README command, compare (text files normalised)."""
import os, re, shutil, subprocess, sys, tempfile, glob
SKS = ["srom-kanon", "srom-produkcja", "srom-quant", "srom-tlumacz"]
B = sys.argv[2] if len(sys.argv) > 2 else "build/srom-cowork"
SK = os.path.join(B, "plugin/srom/skills")
def norm(s, root=None):
    for r in (sorted({root, os.path.realpath(root)}, key=len, reverse=True) if root else ()): s = s.replace(r + "/", "<skills>/")
    return re.sub(r"pandoc \d+(\.\d+)*", "pandoc <v>", s)
ok = 0
for s in SKS:
    d = os.path.join(SK, s, "assets/example")
    if sys.argv[1] == "--shape":
        good = os.path.isfile(f"{d}/README.md") and os.listdir(f"{d}/input") and os.listdir(f"{d}/expected")
    else:
        rd = open(f"{d}/README.md", encoding="utf-8").read()
        cmd = re.search(r"^`(.+)`$", rd.split("Command")[1], re.M).group(1)
        prod = [p.strip() for p in rd.split("Produced by the command:")[1].strip().split(",")]
        T = tempfile.mkdtemp(); e = os.path.join(T, "skills", s, "assets/example")
        shutil.copytree(SK, os.path.join(T, "skills"))
        for p in prod: os.remove(os.path.join(e, p))
        subprocess.run(["sh", "-c", cmd], cwd=e)
        bad = []
        for p in prod:
            a, b = os.path.join(d, p), os.path.join(e, p)
            if not os.path.exists(b): bad.append(p + " missing"); continue
            if p.endswith(".docx"): continue
            x, y = norm(open(a, encoding="utf-8").read()), norm(open(b, encoding="utf-8").read(), os.path.join(T, "skills"))
            if x != y:
                dl = next(((i, l, m) for i, (l, m) in enumerate(zip(x.split("\n"), y.split("\n"))) if l != m), None)
                bad.append(f"{p} differs, line {dl}" if dl else f"{p} differs in length")
        good = not bad
        if bad: print("  ", s, bad)
    print(("ok   " if good else "FAIL ") + s); ok += bool(good)
print(f"EXAMPLE SHAPE {ok}/4" if sys.argv[1] == "--shape" else f"EXAMPLES REPRODUCED {ok}/4")
