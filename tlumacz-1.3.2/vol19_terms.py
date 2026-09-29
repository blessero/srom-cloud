#!/usr/bin/env python3
"""Vol. 19 terminology concordance (leaf 1.3.2).

For each probe in probes.tsv: occurrences of the English regex in every vol. 19 source, and of each Polish
alternative in every draft. Verdict per probe, over the drafts whose source has the English term:
  consistent  - every such draft's most frequent alternative is the same
  divergent   - the most frequent alternatives differ between drafts (to be reviewed; may be a sense difference)
  single      - only one draft has the term;  pending - no draft yet (source only);  none - no source has it
  missing     - a draft whose source has the term uses none of the alternatives (unlisted rendering: review)
Writes vol19-concordance.tsv next to this file. Last line: "concordance: n probes, c consistent, d divergent,
m missing, s single, p pending".
--selftest  plants a divergence (włóczęg → tułacz in a temporary copy of one draft) and a missing rendering, and
            confirms both are reported.
Drafts are read, never written. West Ohueri's source is read from srom-typeset's work folder (read-only).
"""
import csv, os, re, sys, tempfile, shutil
H = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(H)
TEXTS = ["ndiaye", "ostendorf", "pahulich", "tittel", "westohueri"]
def src(t):
    p = os.path.join(M, "work", t, "src", f"{t}_src.md")
    return p if os.path.exists(p) else os.path.join(M, "..", "srom-typeset", "work", t, f"{t}_src.md")
def draft(t, root=M): return os.path.join(root, "work", t, f"{t}_pl.md")
def rd(p): return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def run(root=M, quiet=False):
    probes = list(csv.DictReader(open(os.path.join(H, "probes.tsv"), encoding="utf-8"), delimiter="\t"))
    S = {t: rd(src(t)) for t in TEXTS}; D = {t: rd(draft(t, root)) for t in TEXTS}
    out, tally = [], {}
    for p in probes:
        alts = [a.split("=", 1) for a in p["alternatives (label=regex; …)"].split("; ")]
        en = {t: len(re.findall(p["en_regex"], S[t])) if S[t] else 0 for t in TEXTS}
        pl = {t: {lab: len(re.findall(rx, D[t])) for lab, rx in alts} if D[t] else None for t in TEXTS}
        live = [t for t in TEXTS if en[t] and pl[t] is not None]
        tops = {t: max(pl[t], key=pl[t].get) for t in live if any(pl[t].values())}
        miss = [t for t in live if not any(pl[t].values())]
        if not any(en.values()): v = "none"
        elif miss: v = "missing"
        elif not live: v = "pending"
        elif len(live) == 1: v = "single"
        else: v = "consistent" if len(set(tops.values())) == 1 else "divergent"
        tally[v] = tally.get(v, 0) + 1
        cells = []
        for t in TEXTS:
            s = f"EN {en[t]}"
            if pl[t] is not None: s += " | " + ", ".join(f"{k} {n}" for k, n in pl[t].items() if n) or " | –"
            cells.append(s)
        out.append([p["id"], p["concept"], v] + cells + [", ".join(miss)])
        if not quiet and v in ("divergent", "missing"):
            print(f"  {p['id']} {p['concept']}: {v}", {t: tops.get(t, "–") for t in live})
    if root == M:
        with open(os.path.join(H, "vol19-concordance.tsv"), "w", encoding="utf-8") as f:
            f.write("\t".join(["id", "concept", "verdict"] + TEXTS + ["no listed rendering in"]) + "\n")
            for r in out: f.write("\t".join(r) + "\n")
    g = lambda k: tally.get(k, 0)
    print(f"concordance: {len(probes)} probes, {g('consistent')} consistent, {g('divergent')} divergent, "
          f"{g('missing')} missing, {g('single')} single, {g('pending')} pending")
    return tally

if "--selftest" in sys.argv:
    tmp = tempfile.mkdtemp()
    for t in TEXTS:
        if os.path.exists(draft(t)):
            os.makedirs(os.path.join(tmp, "work", t)); shutil.copy(draft(t), draft(t, tmp))
    p = draft("tittel", tmp); s = open(p, encoding="utf-8").read()
    s = s.replace("włóczęg", "tułacz").replace("Egipcjan", "Xgipcjan")
    open(p, "w", encoding="utf-8").write(s)
    base = run(quiet=True); planted = run(tmp, quiet=True); shutil.rmtree(tmp)
    ok1 = planted.get("divergent", 0) > base.get("divergent", 0)
    ok2 = planted.get("missing", 0) > base.get("missing", 0)
    print(f"selftest: planted divergence {'caught' if ok1 else 'NOT caught'}, planted missing rendering {'caught' if ok2 else 'NOT caught'}")
    sys.exit(0 if ok1 and ok2 else 1)
run()
