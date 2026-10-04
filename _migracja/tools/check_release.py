"""Release checks (gates L7). Modes:
--readme    README.md has the six sections: install, environment, local apps, first session, what changed, untested
--manifest  MANIFEST.md has a row for every shipped skill, with its role and its dependencies
--refs      every concrete file path named in backticks in a SKILL.md or a skill's references/*.md exists in the bundle
Optional second argument: the bundle root (default build/srom-cowork)."""
import glob, os, re, sys

B = sys.argv[2] if len(sys.argv) > 2 else "build/srom-cowork"
PL = os.path.join(B, "plugin/srom")
SK = os.path.join(PL, "skills")
mode = sys.argv[1]

if mode == "--readme":
    t = open(os.path.join(B, "README.md"), encoding="utf-8").read()
    want = ["Install", "Environment", "Local apps", "First session", "What changed", "Untested"]
    heads = re.findall(r"^## \d+\. (.+)$", t, re.M)
    ok = 0
    for w in want:
        hit = any(h.startswith(w) for h in heads); ok += hit; print(("ok   " if hit else "MISS ") + w)
    print(f"README OK {ok}/6" if ok == 6 else f"README FAILED {ok}/6")

elif mode == "--manifest":
    t = open(os.path.join(B, "MANIFEST.md"), encoding="utf-8").read()
    skills = sorted(os.listdir(SK))
    ok = 0
    for s in skills:
        row = next((l for l in t.splitlines() if l.startswith(f"| **{s}** |")), "")
        cells = [c.strip() for c in row.strip("|").split("|")] if row else []
        hit = len(cells) >= 5 and all(cells[1:4])
        ok += hit; print(("ok   " if hit else "MISS ") + s)
    print(f"MANIFEST OK {ok}/{len(skills)}" if ok == len(skills) else f"MANIFEST FAILED {ok}/{len(skills)}")

elif mode == "--refs":
    # a path with "/" must resolve (in the skill, the plugin, or the workspace); a bare name must exist somewhere in the
    # plugin when it is code; bare data names (refs.json, art.md) are made per article and are not bundle files
    texts = glob.glob(f"{SK}/*/SKILL.md") + glob.glob(f"{SK}/*/references/*.md")
    ext = r"\.(py|md|json|tsv|csv|csl|lua|jsx|tpl|idml|pdf|php|sh|mjs|txt|xsd)$"
    code = r"\.(py|jsx|lua|csl|mjs|sh|tpl|idml|xsd|php)$"
    # files on the live WordPress server that srom-quant names (not part of any repository or bundle)
    EXTERNAL = {"wp-content/mu-plugins/srom-loops.php", "srom-loops.php", "functions.php", "object-cache.php",
                "advanced-cache.php"}
    seen, bad, ext_hits = set(), [], set()
    for f in texts:
        sk = f.split("/skills/")[1].split("/")[0]
        for tok in re.findall(r"`([^`\s]+)`", open(f, encoding="utf-8").read()):
            tok = tok.rstrip(".,;:)")
            if not re.search(ext, tok) or re.search(r"[<>*{}$|\[\]]", tok) or tok.startswith(("http", "~", "/")):
                continue
            if "/" not in tok and not re.search(code, tok) or tok.startswith(("_", ".", "-")):
                continue  # a per-article data name or a file-name suffix (_ibidem.jsx), not a bundle file
            if sk.startswith("wp-") and not tok.startswith(("references/", "scripts/", "assets/")):
                continue  # the general-purpose WordPress skills name site and core files (wp-load.php, functions.php)
            if tok in EXTERNAL:
                ext_hits.add(tok); continue
            if (sk, tok) in seen: continue
            seen.add((sk, tok))
            if "/" in tok:
                cands = [os.path.normpath(os.path.join(SK, sk, tok)), os.path.join(SK, tok), os.path.join(PL, tok),
                         os.path.join(SK, sk, "references", tok), os.path.join(B, "workspace", tok), os.path.join(B, tok)]
                cands += glob.glob(f"{SK}/*/{tok}")  # a sibling skill's file (srom-kanon references/kartoteka.tsv)
                cands += [os.path.join(B, "workspace", m, tok) for m in ("srom-produkcja", "srom-tlumacz")]  # module-relative
            else:
                cands = glob.glob(f"{PL}/**/{tok}", recursive=True) + glob.glob(f"{B}/workspace/**/{tok}", recursive=True)
            if not any(os.path.exists(c) for c in cands):
                bad.append((sk, tok)); print("missing", sk, tok, "in", os.path.relpath(f, SK))
    print("external (site files, not checked):", ", ".join(sorted(ext_hits)))
    n = len(seen)
    print(f"REFS OK {n}/{n}" if not bad else f"REFS FAILED {n - len(bad)}/{n}")
