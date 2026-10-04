"""stages.md: the four stages in order, each with Input, Output, Pass (and Fail); the hand-off log format."""
import re
t = open("build/srom-cowork/plugin/srom/skills/srom-produkcja/references/stages.md", encoding="utf-8").read()
want = ["## 1. RIP", "## 2. TRANS", "## 3. INJECT", "## 4. InDesign import"]
pos = [t.find(w) for w in want]
ok = 0
if all(p >= 0 for p in pos) and pos == sorted(pos):
    secs = [t[p:(pos[i + 1] if i + 1 < len(pos) else len(t))] for i, p in enumerate(pos)]
    for w, s in zip(want, secs):
        good = all(k in s for k in ("**Input:**", "**Output", "**Pass", "**Fail:**"))
        print(("ok   " if good else "FAIL ") + w)
        ok += good
else:
    print("FAIL order/presence", pos)
log = "## The hand-off log" in t
print("hand-off log format:", "ok" if log else "missing")
print(f"STAGES OK {ok}/4" if ok == 4 and log else f"STAGES FAILED {ok}/4")
