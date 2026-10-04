"""Checks of the Cowork workspace (gates L6). Modes:
--tree    volume data, every live text folder of both modules, the module folders, the three Cowork files
--red     every red path (🔴 `path`) in the ledger, STATUS.md and the notes sheets resolves in the workspace or, failing
          that, in the plugin (skills/<path>, or the plugin root for SROM_knowledge_base.md)
--same    every copied file is byte-identical to its live original, and no live file under the copied roots is missing
--status  STATUS.md: a section per live text folder; every sha256 in the hand-off log matches the file now
--rules   the workspace CLAUDE.md carries the standing rules
Optional second argument: the bundle root (default build/srom-cowork)."""
import glob, hashlib, os, re, sys

R = "/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans"
B = sys.argv[2] if len(sys.argv) > 2 else "build/srom-cowork"
W, PL = os.path.join(B, "workspace"), os.path.join(B, "plugin/srom")
COWORK = {"MB-decisions.md", "STATUS.md", "CLAUDE.md"}
# copied roots and what make_workspace.sh leaves out of each, as its rsync lines say: (dir names anywhere, file names
# anywhere, "<id>/build" = a build/ folder right under a text folder, "/name" = a top-level file)
ROOTS = {"srom-produkcja/volumes": [], "srom-produkcja/work": ["build_inject", "wordcheck.py", "source_imprints.py"],
         "srom-tlumacz/work": ["<id>/build"], "srom-tlumacz/sources": ["/SROM_knowledge_base.md"],
         "srom-tlumacz/training": [], "srom-tlumacz/tlumacz-1.3.2": []}
JUNK = ("__pycache__", ".DS_Store", ".pyc")
mode = sys.argv[1]


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def live_files(root, excl):
    base = os.path.join(R, root)
    for dp, dn, fn in os.walk(base):
        rel = os.path.relpath(dp, base)
        parts = [] if rel == "." else rel.split(os.sep)
        if any(x in parts for x in JUNK) or any(x in parts for x in excl):
            continue
        if "<id>/build" in excl and len(parts) >= 2 and parts[1] == "build":
            continue
        for f in fn:
            if f.endswith(JUNK) or f in excl or (not parts and "/" + f in excl):
                continue
            yield os.path.join(root, *parts, f)


if mode == "--tree":
    need = ["srom-produkcja/volumes/18/srom_master_v3.csv", "srom-produkcja/volumes/autorzy.tsv",
            "srom-produkcja/volumes/ror.tsv", "srom-tlumacz/sources/vol18-md", "srom-tlumacz/sources/vol18-en",
            "srom-tlumacz/sources/prng", "srom-tlumacz/training/sources.tsv", "srom-tlumacz/tlumacz-1.3.2/vol19_terms.py"]
    need += sorted(COWORK)
    for m in ("srom-produkcja", "srom-tlumacz"):
        need += [os.path.relpath(d, R) for d in glob.glob(f"{R}/{m}/work/*/")]
    miss = [n for n in need if not os.path.exists(os.path.join(W, n.rstrip("/")))]
    for n in miss: print("missing", n)
    print(f"checked {len(need)}:", "TREE OK" if not miss else f"TREE FAILED {len(miss)}")

elif mode == "--red":
    srcs = [os.path.join(W, f) for f in ("MB-decisions.md", "STATUS.md")] + glob.glob(f"{W}/*/work/*/*_uwagi.md")
    paths, bad = set(), []
    for f in srcs:
        for p in re.findall(r"🔴 `([^`]+)`", open(f, encoding="utf-8").read()):
            paths.add(p)
    for p in sorted(paths):
        if not any(os.path.exists(os.path.join(x, p)) for x in (W, os.path.join(PL, "skills"), PL)):
            bad.append(p); print("missing", p)
    n = len(paths)
    print(f"RED PATHS OK {n}/{n}" if not bad else f"RED PATHS FAILED {n - len(bad)}/{n}")

elif mode == "--same":
    copied = [os.path.relpath(p, W) for p in glob.glob(f"{W}/**/*", recursive=True) if os.path.isfile(p)]
    copied = [c for c in copied if c not in COWORK]
    diff = [c for c in copied if not os.path.isfile(os.path.join(R, c)) or sha(os.path.join(R, c)) != sha(os.path.join(W, c))]
    for c in diff[:10]: print("differs or not live:", c)
    live = set(f for r, e in ROOTS.items() for f in live_files(r, e))
    missing = sorted(live - set(copied))
    for c in missing[:10]: print("live file not copied:", c)
    ok = len(copied) - len(diff)
    print(f"SAME {ok}/{len(copied)}" if not missing else f"SAME FAILED {ok}/{len(copied)}, not copied {len(missing)}")

elif mode == "--status":
    t = open(os.path.join(W, "STATUS.md"), encoding="utf-8").read()
    secs = re.split(r"\n### ", t.split("## Hand-off log")[0])[1:]
    ids = [os.path.basename(d.rstrip("/")) for m in ("srom-produkcja", "srom-tlumacz") for d in glob.glob(f"{R}/{m}/work/*/")]
    nosec = [i for i in sorted(set(ids)) if not any(f"work/{i}/" in s for s in secs)]
    for i in nosec: print("no section names", f"work/{i}/")
    good = total = 0
    for row in t.split("## Hand-off log")[1].splitlines():
        m = re.search(r"\(`([^`]+)`\)", row)
        if not row.startswith("| ") or not m: continue
        d = os.path.dirname(os.path.join(W, m.group(1)))
        for f, a, b in re.findall(r"`([^`]+)` ([0-9a-f]{8})…([0-9a-f]{7})", row):
            total += 1; h = sha(os.path.join(d, f)) if os.path.exists(os.path.join(d, f)) else ""
            if h[:8] == a and h[-7:] == b: good += 1
            else: print("hash differs:", m.group(1), f)
    print(f"STATUS OK {len(secs)} texts, hashes {good}/{total}" if not nosec and total and good == total
          else f"STATUS FAILED sections {len(secs)}, missing {nosec}, hashes {good}/{total}")

elif mode == "--rules":
    c = open(os.path.join(W, "CLAUDE.md"), encoding="utf-8").read()
    rules = {"dates": r"date '\+%d\.%m\.%Y %H:%M'", "doubts": r"never silently dropped or corrected",
             "fabricate": r"Never invent bibliographic", "ledger": r"Next free.*[\s\S]*\*Trail\*",
             "word master": r"the Word file .* is the master", "files to open": r"Files to open:",
             "lean": r"Keep it lean"}
    ok = 0
    for k, r in rules.items():
        hit = bool(re.search(r, c)); ok += hit; print(("ok   " if hit else "MISS ") + k)
    print(f"RULES OK {ok}/{len(rules)}" if ok == len(rules) else f"RULES FAILED {ok}/{len(rules)}")
