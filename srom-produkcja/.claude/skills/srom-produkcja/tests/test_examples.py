"""assets/example/ of srom-produkcja, srom-kanon and srom-quant: each README names one command and the files it
produces; the example is copied, the produced files deleted, the command run, the output compared with expected/
(text files only; a .docx must exist). Needs the skills side by side (build.py finds srom-kanon next to itself)."""
import os, re, shutil, subprocess, sys, tempfile

SKILLS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMES = ["srom-produkcja", "srom-kanon", "srom-quant"]


def norm(s, roots):
    for r in sorted(roots, key=len, reverse=True):
        s = s.replace(r + "/", "<skills>/")
    return re.sub(r"pandoc \d+(\.\d+)*", "pandoc <v>", s)


ok = 0
with tempfile.TemporaryDirectory() as T:
    sk = os.path.join(T, "skills")
    shutil.copytree(SKILLS, sk, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", "tests"))
    for name in NAMES:
        d = os.path.join(SKILLS, name, "assets", "example")
        e = os.path.join(sk, name, "assets", "example")
        rd = open(os.path.join(d, "README.md"), encoding="utf-8").read()
        cmd = re.search(r"^`(.+)`$", rd.split("Command")[1], re.M).group(1)
        produced = [p.strip() for p in rd.split("Produced by the command:")[1].strip().split(",")]
        for p in produced:
            os.remove(os.path.join(e, p))
        subprocess.run(["sh", "-c", cmd.replace("python3", sys.executable, 1)], cwd=e, capture_output=True)
        bad = []
        for p in produced:
            a, b = os.path.join(d, p), os.path.join(e, p)
            if not os.path.exists(b):
                bad.append(p + " missing")
            elif not p.endswith(".docx"):
                x = norm(open(a, encoding="utf-8").read(), {sk})
                y = norm(open(b, encoding="utf-8").read(), {sk, os.path.realpath(sk)})
                if x != y:
                    n = next((i + 1 for i, (l, m) in enumerate(zip(x.split("\n"), y.split("\n"))) if l != m), None)
                    bad.append(f"{p} differs" + (f" at line {n}" if n else " in length"))
        print(("ok   " if not bad else "FAIL ") + name + (": " + "; ".join(bad) if bad else ""))
        ok += not bad
print(f"EXAMPLES ALL PASS {ok}/{len(NAMES)}" if ok == len(NAMES) else f"EXAMPLES FAILED {len(NAMES) - ok}/{len(NAMES)}")
sys.exit(0 if ok == len(NAMES) else 1)
