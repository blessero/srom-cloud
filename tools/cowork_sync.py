#!/usr/bin/env python3
"""cowork_sync.py: how far Claude Code's SROM and Cowork's copy of it have drifted apart. Read-only; works on temp
copies. Runs on MB's Mac (a Code session, or MB in Terminal), or in Cowork's shell once the Code folder is connected.

  python3 _handoffs/tools/cowork_sync.py [--code DIR] [--cowork DIR]

Defaults: --code = the folder holding _handoffs/ (this script's grandparent), --cowork = $SROM_COWORK, else
$HOME/mnt/srom-cowork (Cowork's shell), else /Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork.

1. Skill patches from Cowork (workspace/skill-changes/ and _handoffs/cowork/): is each one in Code, in Cowork's
   plugin folder, ticked in Cowork's STATUS.md? Tested newest first by reverse-applying on temp copies, so stacked
   patches are judged right. "in Code, not in Cowork" means Cowork lost a change; a patch not in Code is also
   tried forward on Code ("applies cleanly", or "does not apply": often a Cowork-only fix of the bundle's own edits).
2. Skill files that differ between Code and Cowork's plugin folder (until SYS-10 is settled, many are the bundle's
   deliberate edits: listed, not judged).
3. Question IDs: the same ID open in both ledgers under different headings, an ID open in one ledger only, an ID
   Cowork has used (in its STATUS.md) that Code's ledger uses for an open question, "Next free" numbers that would
   hand out one ID twice.
4. Text data: files in work/ and volumes/ that differ between Code's modules and Cowork's workspace.
Exit 1 when section 1 or 3 needs action, else 0. The last line is SYNC OK or SYNC: n item(s) need action.
"""
import argparse, glob, os, re, shutil, subprocess, sys, tempfile, filecmp

HERE = os.path.dirname(os.path.realpath(__file__))
CODE_SKILLS = {"srom-produkcja": "srom-produkcja/.claude/skills/srom-produkcja",
               "srom-kanon": "srom-produkcja/.claude/skills/srom-kanon",
               "srom-quant": "srom-produkcja/.claude/skills/srom-quant",
               "srom-zizek": "srom-produkcja/.claude/skills/srom-zizek",
               "srom-tlumacz": "srom-tlumacz/.claude/skills/srom-tlumacz"}
JUNK = {"__pycache__", ".DS_Store"}
ID = r"(?:GEN|V19|PAH|OST|TIT|NDI|WOH|SCH|SYS)-\d+"


def default_cowork():
    for c in (os.environ.get("SROM_COWORK"), os.path.expanduser("~/mnt/srom-cowork"),
              "/Users/michalbartosz/ARBEIT/Bima/SROM/Cowork/srom-cowork"):
        if c and os.path.isdir(os.path.join(c, "workspace")):
            return c
    return None


def copy_tree(src, dst):
    shutil.copytree(src, dst, symlinks=False, ignore=shutil.ignore_patterns(*JUNK, "*.pyc"))


def patch(d, p, reverse, dry=False):
    args = ["patch", "-p0", "-s", "-f", "--dry-run", "-d", d, "-i", p] + (["-R"] if reverse else [])
    if subprocess.run(args, capture_output=True, stdin=subprocess.DEVNULL).returncode:
        return False
    if dry:
        return True
    subprocess.run(args[:4] + args[5:], capture_output=True, stdin=subprocess.DEVNULL)   # the same, for real
    return True


def present(patches, tree):
    """{patch: True/False/None}: newest first, each found one is reversed on the temp tree (None: target missing)."""
    out = {}
    for p in sorted(patches, key=os.path.basename, reverse=True):
        if tree is None:
            out[p] = None
            continue
        out[p] = patch(tree, p, reverse=True)
    return out


def ledger(path):
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    heads = {m.group(1): m.group(2).strip() for m in re.finditer(rf"^### ({ID}) · (.+)$", text, re.M)}
    nxt = {m.group(1): int(m.group(2)) for m in re.finditer(r"Next free: ([A-Z0-9]+)-(\d+)", text)}
    return heads, nxt


def files(top):
    out = {}
    for dp, dns, fns in os.walk(top):
        dns[:] = [d for d in dns if d not in JUNK and d != "build" and not d.startswith("build_")]
        for f in fns:
            if f not in JUNK and not f.endswith(".pyc"):
                full = os.path.join(dp, f)
                out[os.path.relpath(full, top)] = full
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--cowork", default=default_cowork())
    a = ap.parse_args()
    code, cw = a.code, a.cowork
    if not cw or not os.path.isdir(cw):
        sys.exit("Cowork folder not found: pass --cowork or set SROM_COWORK")
    W, PLUG = os.path.join(cw, "workspace"), os.path.join(cw, "plugin", "srom")
    action = []
    tmp = tempfile.mkdtemp(prefix="cowork-sync-")
    try:
        # 1. patches
        print("1. Skill patches from Cowork")
        patches = sorted(glob.glob(os.path.join(W, "skill-changes", "*.patch")) +
                         glob.glob(os.path.join(code, "_handoffs", "cowork", "*.patch")), key=os.path.basename)
        ct, cf, kt, kk = (os.path.join(tmp, n) for n in ("code", "code-fresh", "cowork", "cowork-kb"))
        for t in (ct, cf):
            os.makedirs(t)
            for name, rel in CODE_SKILLS.items():
                if os.path.isdir(os.path.join(code, rel)):
                    copy_tree(os.path.join(code, rel), os.path.join(t, name))
        copy_tree(os.path.join(PLUG, "skills"), kt)
        os.makedirs(kk)
        if os.path.isfile(os.path.join(PLUG, "SROM_knowledge_base.md")):
            shutil.copy(os.path.join(PLUG, "SROM_knowledge_base.md"), kk)
        kb = [p for p in patches if p.endswith("_knowledge-base.patch")]
        sk = [p for p in patches if p not in kb]
        in_code = {**present(sk, ct), **present(kb, None)}          # Code has no knowledge-base file (SYS-10)
        fits_code = {p: patch(cf, p, reverse=False, dry=True) for p in sk if in_code[p] is False}   # each alone, on Code as it is
        in_cw = {**present(sk, kt), **present(kb, kk)}
        status = open(os.path.join(W, "STATUS.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(W, "STATUS.md")) else ""
        for p in patches:
            b = os.path.basename(p)
            ticked = any(l.lower().startswith("x]") for l in status.split("\n- [") if b in l)
            c, k = in_code[p], in_cw[p]
            verdict = ("in Code, in Cowork" if c and k else
                       "in Code, not in Cowork: Cowork lost it" if c and not k else
                       "not in Code: Code to apply (applies cleanly)" if k and c is False and fits_code.get(p) else
                       "not in Code, does not apply to Code: look at it (a Cowork-only fix?)" if k and c is False else
                       "Code has no such file (knowledge base)" if c is None and k else
                       "in neither: lost or superseded")
            need = (c and not k) or (c is False and k) or (c is False and not k) or (c and k and not ticked)
            if c and k and not ticked:
                verdict += "; not ticked in Cowork's STATUS.md"
            print(f"  {'!!' if need else 'ok'} {b}: {verdict}")
            if need:
                action.append(b)
        if not patches:
            print("  none")

        # 2. skill files
        print("2. Skill files that differ, Code vs Cowork's plugin folder")
        for name, rel in CODE_SKILLS.items():
            A, B = files(os.path.join(code, rel)), files(os.path.join(PLUG, "skills", name))
            diff = sorted(r for r in set(A) & set(B) if not filecmp.cmp(A[r], B[r], shallow=False))
            only_code, only_cw = sorted(set(A) - set(B)), sorted(set(B) - set(A))
            print(f"  {name}: {len(diff)} differ, {len(only_code)} only in Code, {len(only_cw)} only in Cowork"
                  + (": " + ", ".join((diff + [f'+{x}' for x in only_code])[:8]) if diff or only_code else ""))

        # 3. ledgers
        print("3. Question IDs")
        ch, cn = ledger(os.path.join(code, "_handoffs", "MB-decisions.md"))
        kh, kn = ledger(os.path.join(W, "MB-decisions.md"))
        for i in sorted(set(ch) & set(kh), key=lambda x: (x.split("-")[0], int(x.split("-")[1]))):
            if ch[i] != kh[i]:
                print(f"  ~~ {i} open in both, headings differ: Code \"{ch[i][:60]}\" / Cowork \"{kh[i][:60]}\"")
        used_cw = set(re.findall(ID, status)) - set(kh)
        for i in sorted(set(ch) - set(kh), key=lambda x: (x.split("-")[0], int(x.split("-")[1]))):
            clash = i in used_cw
            ctx = next((l.strip()[:90] for l in status.splitlines() if re.search(rf"\b{i}\b", l)), "")
            print(f"  {'!!' if clash else '..'} {i} open in Code only (\"{ch[i][:50]}\")"
                  + (f"; Cowork used {i} for something else: \"{ctx}\"" if clash else ""))
            if clash:
                action.append(i)
        for i in sorted(set(kh) - set(ch)):
            print(f"  .. {i} open in Cowork only (\"{kh[i][:60]}\")")
        for code_ in sorted(set(cn) | set(kn)):
            hi_c = max([int(x.split("-")[1]) for x in ch if x.startswith(code_ + "-")] + [cn.get(code_, 1) - 1])
            hi_k = max([int(x.split("-")[1]) for x in kh if x.startswith(code_ + "-")] + [kn.get(code_, 1) - 1])
            if code_ in kn and kn[code_] <= hi_c and kn[code_] < 100:
                print(f"  !! {code_}: Cowork's next free {code_}-{kn[code_]} is already taken in Code (up to {code_}-{hi_c})")
                action.append(f"{code_}-{kn[code_]}")
            if code_ in cn and cn[code_] <= hi_k:
                print(f"  !! {code_}: Code's next free {code_}-{cn[code_]} is already taken in Cowork (up to {code_}-{hi_k})")
                action.append(f"{code_}-{cn[code_]}")

        # 4. text data
        print("4. Text data, Code modules vs Cowork workspace (build folders left out)")
        for rel in ("srom-produkcja/work", "srom-produkcja/volumes", "srom-tlumacz/work"):
            A, B = files(os.path.join(code, rel)), files(os.path.join(W, rel))
            diff = sorted(r for r in set(A) & set(B) if not filecmp.cmp(A[r], B[r], shallow=False))
            print(f"  {rel}: {len(diff)} differ, {len(set(A) - set(B))} only in Code, {len(set(B) - set(A))} only in Cowork"
                  + (": " + ", ".join(diff[:6]) if diff else ""))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SYNC: {len(action)} item(s) need action" if action else "SYNC OK")
    return 1 if action else 0


if __name__ == "__main__":
    sys.exit(main())
