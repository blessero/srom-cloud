"""Every third-party module imported by a script in the plugin is named in requirements.txt."""
import ast, os, sys
B = "build/srom-cowork"
req = open(os.path.join(B, "plugin/srom/requirements.txt")).read().lower()
dist = {"docx": "python-docx", "fitz": "pymupdf", "pymupdf": "pymupdf", "lxml": "lxml"}
local, found = set(), {}
for root, _, files in os.walk(os.path.join(B, "plugin")):
    local |= {f[:-3] for f in files if f.endswith(".py")}
for root, _, files in os.walk(os.path.join(B, "plugin")):
    for f in files:
        if not f.endswith(".py"):
            continue
        p = os.path.join(root, f)
        for n in ast.walk(ast.parse(open(p, encoding="utf-8").read())):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module] if isinstance(n, ast.ImportFrom) and n.module and not n.level else []
            for m in names:
                top = m.split(".")[0]
                if top in sys.stdlib_module_names or top in local:
                    continue
                found.setdefault(top, set()).add(p.split("skills/")[-1])
miss = {m: sorted(v) for m, v in found.items() if dist.get(m, m).lower() not in req}
print("third-party:", sorted(found))
print("IMPORTS COVERED" if not miss else f"IMPORTS MISSING {miss}")
