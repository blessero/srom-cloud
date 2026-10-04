#!/usr/bin/env python3
"""cloud.py: carry the SROM Code system to a cloud mirror (one GitHub repository) and back. Runs on MB's Mac.

The local folder stays the home. The mirror is a second git repository, a sibling folder (`../srom-cloud`), whose
working tree is a copy of this whole folder: the three module repositories with their history (git subtree), the
data their .gitignore keeps out of git (texts, PDFs, Word copies), and the root files. Cloud sessions clone the
mirror from GitHub; what they commit comes back here as ordinary commits in each module repository.

  python3 _cloud/cloud.py init   [--mirror DIR] [--remote URL]  create the mirror (once), with history; no push
  python3 _cloud/cloud.py export [--mirror DIR] [--no-push]      local -> mirror, commit, push
  python3 _cloud/cloud.py import [--mirror DIR] [--no-pull]      pull, mirror -> local, commit in each module repo
  python3 _cloud/cloud.py sync   [--mirror DIR]                  import, then export (the usual call during a cloud phase)
  python3 _cloud/cloud.py status [--mirror DIR]                  what changed on each side since the last sync

Rules it keeps:
- Never overwrites local work. Export refuses while a module repository has uncommitted changes; import refuses
  while anything here changed since the last sync (it lists the files) or the mirror has local, unpushed edits.
- Export refuses while GitHub has cloud commits not yet imported (import them first).
- Not carried: .git, caches, `_widok/` (MB's rendered views embed the Claude app's fonts: this Mac only),
  `_migracja/build/` and its zip (Cowork has them), `srom-produkcja/dist/` (derived .skill files), `_cloud/state/`.
- A module's `.gitignore` is stored in the mirror as `.gitignore.module`, so the mirror commits the data the
  module keeps out of git; it is renamed back on import.
- Cowork's channel (`_handoffs/cowork-to-code.md`, `_handoffs/cowork/`) is written by Cowork on this Mac, also
  during a cloud phase: it always goes out with export and is never overwritten by import.
State of the last sync: `_cloud/state/last-sync.json` (local heads, mirror head, sha256 of every carried file).
"""
import argparse, datetime, filecmp, hashlib, json, os, shutil, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MODULES = ("srom-produkcja", "srom-tlumacz", "_handoffs")
SKIP_NAMES = {".git", ".DS_Store", "__pycache__", ".venv", "node_modules", ".pytest_cache"}
SKIP_PATHS = ("_widok", "_migracja/build", "srom-produkcja/dist", "_cloud/state")
COWORK_OWNED = ("_handoffs/cowork-to-code.md", "_handoffs/cowork")
COWORK_IN_HANDOFFS = tuple(p.split("/", 1)[1] for p in COWORK_OWNED)
MIRROR_ONLY = (".git", ".gitignore")          # at the mirror's root
MIRROR_GITIGNORE = """# mirror of "SROM edit and trans" (_cloud/cloud.py): junk only; data is committed on purpose
.DS_Store
__pycache__/
*.pyc
.venv/
node_modules/
~$*
_widok/
_cloud/state/
"""
STATE = os.path.join(ROOT, "_cloud", "state", "last-sync.json")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def skipped(rel, name):
    if name in SKIP_NAMES or name.endswith(".pyc") or name.startswith("~$") or name.startswith(".~lock."):
        return True
    if rel.endswith(".zip") and rel.startswith("_migracja/") and rel.count("/") == 1:
        return True
    return any(rel == p or rel.startswith(p + "/") for p in SKIP_PATHS)


def to_mirror(rel):
    return rel + ".module" if os.path.basename(rel) == ".gitignore" and "/" in rel else rel


def to_local(rel):
    return rel[:-len(".module")] if rel.endswith("/.gitignore.module") else rel


def cowork_owned(rel):
    return any(rel == p or rel.startswith(p + "/") for p in COWORK_OWNED)


def walk(top, mirror_side):
    """{nfc relative path in LOCAL naming: (absolute path, 'f'|'l'|'d')} of everything carried."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(top):
        reld = nfc(os.path.relpath(dirpath, top)).replace(os.sep, "/")
        reld = "" if reld == "." else reld
        keep = []
        for d in sorted(dirnames):
            rel = f"{reld}/{nfc(d)}" if reld else nfc(d)
            full = os.path.join(dirpath, d)
            if mirror_side and not reld and d in MIRROR_ONLY:
                continue
            if skipped(rel, nfc(d)):
                continue
            if os.path.islink(full):
                out[rel] = (full, "l")
            else:
                out[rel] = (full, "d"); keep.append(d)
        dirnames[:] = keep
        for f in sorted(filenames):
            rel = f"{reld}/{nfc(f)}" if reld else nfc(f)
            if mirror_side and (not reld and f in MIRROR_ONLY or reld and f == ".gitignore"):
                continue
            if skipped(rel, nfc(f)):
                continue
            full = os.path.join(dirpath, f)
            out[to_local(rel) if mirror_side else rel] = (full, "l" if os.path.islink(full) else "f")
    return out


def digest(path, kind):
    if kind == "l":
        return "link:" + os.readlink(path)
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(tree):
    return {rel: digest(p, k) for rel, (p, k) in tree.items() if k != "d"}


def same(a, ka, b, kb):
    if ka != kb:
        return False
    if ka == "l":
        return os.readlink(a) == os.readlink(b)
    return os.path.getsize(a) == os.path.getsize(b) and filecmp.cmp(a, b, shallow=False)


def place(src, kind, dst):
    if os.path.lexists(dst) and (os.path.islink(dst) or not os.path.isdir(dst)):
        os.remove(dst)
    elif os.path.isdir(dst) and kind != "d":
        shutil.rmtree(dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if kind == "l":
        os.symlink(os.readlink(src), dst)
    else:
        shutil.copy2(src, dst)


def sync(src_top, src_is_mirror, dst_top, keep=lambda rel: False):
    """Make dst like src (carried paths only). keep(rel): never touch that path on dst. Returns (copied, removed)."""
    src, dst = walk(src_top, src_is_mirror), walk(dst_top, not src_is_mirror)
    name = (lambda rel: to_mirror(rel)) if not src_is_mirror else (lambda rel: rel)
    copied, removed = [], []
    for rel, (p, k) in src.items():
        if keep(rel):
            continue
        target = os.path.join(dst_top, name(rel))
        if k == "d":
            if rel in dst and dst[rel][1] == "d":
                continue
            if os.path.lexists(target):
                os.remove(target)
            os.makedirs(target, exist_ok=True)
            continue
        have = dst.get(rel)
        if have and have[1] != "d" and same(p, k, have[0], have[1]):
            continue
        place(p, k, have[0] if have else target)
        copied.append(rel)
    for rel in sorted(set(dst) - set(src), key=len, reverse=True):
        if keep(rel) or any(rel.startswith(k + "/") for k in src if src[k][1] == "l"):
            continue
        p, k = dst[rel]
        if k == "d":
            if not os.listdir(p):
                os.rmdir(p)
            continue
        os.remove(p); removed.append(rel)
    return copied, removed


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} in {repo}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.rstrip()   # rstrip: porcelain lines start with a meaningful space


def dirty(repo, ignore=()):
    lines = git(repo, "status", "--porcelain", "--untracked-files=all").splitlines()
    return [l for l in lines if not any(nfc(l[3:].strip('"')).startswith(i) for i in ignore)]


def heads():
    return {m: git(os.path.join(ROOT, m), "rev-parse", "HEAD") for m in MODULES}


def now():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")


def load_state():
    if not os.path.isfile(STATE):
        return None
    with open(STATE, encoding="utf-8") as fh:
        return json.load(fh)


def save_state(mirror):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    st = {"time": now(), "mirror": os.path.realpath(mirror), "mirror_head": git(mirror, "rev-parse", "HEAD"),
          "local_heads": heads(), "manifest": manifest(walk(ROOT, False))}
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=0, sort_keys=True)


def remote(mirror):
    return git(mirror, "remote") != ""


def local_changes(st):
    """Carried files changed here since the last sync, Cowork's channel excepted."""
    cur, old = manifest(walk(ROOT, False)), st["manifest"]
    diff = sorted(r for r in set(cur) | set(old) if cur.get(r) != old.get(r) and not cowork_owned(r))
    moved = [m for m in MODULES if git(os.path.join(ROOT, m), "rev-parse", "HEAD") != st["local_heads"][m]]
    return diff, moved


def cmd_export(a, quiet=False):
    m = a.mirror
    if not os.path.isdir(os.path.join(m, ".git")):
        sys.exit(f"no mirror at {m}: run init first")
    bad = {mod: dirty(os.path.join(ROOT, mod), COWORK_IN_HANDOFFS if mod == "_handoffs" else ()) for mod in MODULES}
    bad = {k: v for k, v in bad.items() if v}
    if bad:
        sys.exit("EXPORT REFUSED: uncommitted changes (commit them in that module first):\n" +
                 "\n".join(f"  {k}: {l}" for k, v in bad.items() for l in v[:10]))
    if dirty(m):
        sys.exit(f"EXPORT REFUSED: the mirror {m} has uncommitted edits; look at them (git -C … status) first")
    if remote(m) and not a.no_push:
        git(m, "fetch", "origin")
        ahead = git(m, "rev-list", "--count", "HEAD..origin/main", check=False)
        if ahead not in ("", "0"):
            sys.exit(f"EXPORT REFUSED: GitHub has {ahead} cloud commit(s) not imported yet: run import first")
    st = load_state()
    copied, removed = sync(ROOT, False, m)
    for dirpath, dirnames, filenames in os.walk(m):      # a module's own .gitignore would hide its data in the mirror
        dirnames[:] = [d for d in dirnames if d != ".git"]
        if dirpath != m and ".gitignore" in filenames:
            os.remove(os.path.join(dirpath, ".gitignore"))
    git(m, "add", "-A")
    if git(m, "status", "--porcelain"):
        h = heads()
        body = []
        for mod in MODULES:
            if st and st["local_heads"].get(mod) and st["local_heads"][mod] != h[mod]:
                log = git(os.path.join(ROOT, mod), "log", "--format=  %h %s", f"{st['local_heads'][mod]}..{h[mod]}",
                          check=False)
                if log:
                    body.append(f"{mod}:\n{log}")
        msg = f"export {now()}: " + " · ".join(f"{k} {v[:7]}" for k, v in h.items())
        git(m, "commit", "-q", "-m", msg + ("\n\n" + "\n".join(body) if body else ""))
        print(f"exported: {len(copied)} file(s) copied, {len(removed)} removed; mirror {git(m, 'rev-parse', '--short', 'HEAD')}")
    else:
        print("export: nothing changed since the last sync")
    if remote(m) and not a.no_push:
        git(m, "push", "-q", "origin", "main")
        print("pushed to", git(m, "remote", "get-url", "origin"))
    save_state(m)


def cmd_import(a):
    m = a.mirror
    st = load_state()
    if not st:
        sys.exit("IMPORT REFUSED: no sync recorded here (export first)")
    if dirty(m):
        sys.exit(f"IMPORT REFUSED: the mirror {m} has uncommitted edits; look at them first")
    if remote(m) and not a.no_pull:
        git(m, "pull", "-q", "--ff-only", "origin", "main")
    changed, moved = local_changes(st)
    bad = {mod: dirty(os.path.join(ROOT, mod), COWORK_IN_HANDOFFS if mod == "_handoffs" else ()) for mod in MODULES}
    bad = {k: v for k, v in bad.items() if v}
    if changed or moved or bad:
        lines = [f"  changed here: {r}" for r in changed[:20]] + [f"  new commits here: {x}" for x in moved] + \
                [f"  uncommitted in {k}: {l}" for k, v in bad.items() for l in v[:5]]
        sys.exit("IMPORT REFUSED: this folder changed since the last sync (work was done locally during the cloud "
                 "phase). Nothing was touched. Merge by hand or ask a session to:\n" + "\n".join(lines))
    base, head = st["mirror_head"], git(m, "rev-parse", "HEAD")
    if base == head:
        print("import: the mirror has nothing new"); return
    copied, removed = sync(m, True, ROOT, keep=cowork_owned)
    hs = os.path.join(ROOT, "_handoffs")
    if dirty(hs):                       # Cowork wrote its channel during the cloud phase: its own commit first
        git(hs, "add", "-A", "--", *[p for p in COWORK_IN_HANDOFFS if os.path.lexists(os.path.join(hs, p))])
        if git(hs, "diff", "--cached", "--name-only"):
            git(hs, "commit", "-q", "-m", "cowork: channel files written by Cowork during the cloud phase [general]")
    done = []
    for mod in MODULES:
        r = os.path.join(ROOT, mod)
        git(r, "add", "-A")
        if not git(r, "diff", "--cached", "--name-only"):
            continue
        log = git(m, "log", "--reverse", "--format=  %h %s", f"{base}..{head}", "--", f"{mod}/", check=False)
        git(r, "commit", "-q", "-m", f"cloud import {now()}: mirror {base[:7]}..{head[:7]}\n\n{log}".rstrip())
        done.append(f"{mod} {git(r, 'rev-parse', '--short', 'HEAD')}")
    print(f"imported mirror {base[:7]}..{head[:7]}: {len(copied)} file(s) copied, {len(removed)} removed; "
          f"commits: {', '.join(done) or 'none (root files only)'}")
    save_state(m)


def cmd_status(a):
    st = load_state()
    if not st:
        print("no sync recorded"); return
    changed, moved = local_changes(st)
    print(f"last sync {st['time']} (mirror {st['mirror_head'][:7]})")
    print(f"here since: {len(changed)} file(s) changed, new commits in: {', '.join(moved) or 'none'}")
    for r in changed[:20]:
        print("  ", r)
    if os.path.isdir(a.mirror):
        if remote(a.mirror):
            git(a.mirror, "fetch", "-q", "origin", check=False)
            n = git(a.mirror, "rev-list", "--count", f"{st['mirror_head']}..origin/main", check=False)
            print(f"cloud since: {n or '?'} commit(s) on GitHub not imported")
        n = git(a.mirror, "rev-list", "--count", f"{st['mirror_head']}..HEAD", check=False)
        print(f"mirror folder since: {n} commit(s) not imported")


def cmd_sync(a):
    cmd_import(a)
    cmd_export(a)


def cmd_init(a):
    m = a.mirror
    if os.path.exists(m):
        sys.exit(f"INIT REFUSED: {m} exists")
    os.makedirs(m)
    git(m, "init", "-q", "-b", "main")
    with open(os.path.join(m, ".gitignore"), "w") as fh:
        fh.write(MIRROR_GITIGNORE)
    git(m, "add", ".gitignore")
    git(m, "commit", "-q", "-m", 'mirror of "SROM edit and trans" for cloud sessions (_cloud/cloud.py)')
    for mod in MODULES:
        git(m, "subtree", "add", "-q", f"--prefix={mod}", os.path.join(ROOT, mod), "main")
    if a.remote:
        git(m, "remote", "add", "origin", a.remote)
    a.no_push = True
    cmd_export(a)
    print(f"mirror ready: {m} ({git(m, 'rev-list', '--count', 'HEAD')} commits); push with: "
          f"git -C '{m}' push -u origin main" if a.remote else f"mirror ready: {m}; no remote yet")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("cmd", choices=["init", "export", "import", "sync", "status"])
    p.add_argument("--mirror", default=os.path.join(os.path.dirname(ROOT), "srom-cloud"))
    p.add_argument("--remote")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--no-pull", action="store_true")
    a = p.parse_args()
    a.mirror = os.path.abspath(a.mirror)
    {"init": cmd_init, "export": cmd_export, "import": cmd_import, "sync": cmd_sync, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
