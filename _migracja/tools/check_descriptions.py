"""Each SROM SKILL.md: frontmatter name = folder, description <= 1024 chars, a 'Not for' clause naming a sibling skill."""
import os, re, glob
SK = "build/srom-cowork/plugin/srom/skills"
sib = {"srom-kanon", "srom-produkcja", "srom-tlumacz", "srom-quant"}
ok = 0
for f in sorted(glob.glob(f"{SK}/srom-*/SKILL.md")):
    name = os.path.basename(os.path.dirname(f)); t = open(f, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", t, re.S).group(1)
    n = re.search(r"^name: (.*)$", fm, re.M).group(1).strip(); d = re.search(r"^description: (.*)$", fm, re.M).group(1).strip()
    nf = d[d.find("Not for"):] if "Not for" in d else ""
    named = {s for s in sib - {name} if s in nf}
    good = n == name and len(d) <= 1024 and named
    print(f"{'ok  ' if good else 'FAIL'} {name}: {len(d)} chars, not-for names {sorted(named)}")
    ok += bool(good)
print(f"DESCRIPTIONS OK {ok}/4" if ok == 4 else f"DESCRIPTIONS FAILED {4-ok}/4")
