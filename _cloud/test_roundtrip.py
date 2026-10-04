#!/usr/bin/env python3
"""test_roundtrip.py: cloud.py on scratch copies, never on the real folders. A copy of this root plays "here", a
bare repository plays GitHub, a clone plays the cloud session. Prints ROUNDTRIP OK n/n (exit 0) or the failures.
Takes about half a minute (copies the root once, about 100 MB)."""
import os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
results = []


def check(name, ok, info=""):
    results.append(bool(ok))
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"\n     {str(info)[:600]}"))


def run(*cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout + r.stderr


def git(repo, *a):
    return run("git", "-C", repo, *a)[1].strip()


def append(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    tmp = tempfile.mkdtemp(prefix="srom-cloud-test-")
    here, mirror, bare, cloud = (os.path.join(tmp, n) for n in ("here", "srom-cloud", "remote.git", "cloud"))
    shutil.copytree(ROOT, here, symlinks=True, ignore=lambda d, names: [
        n for n in names if (d == ROOT and n == "_widok") or n == "state" and d.endswith("_cloud")
        or (d.endswith("_migracja") and (n == "build" or n.endswith(".zip")))])
    tool = [sys.executable, os.path.join(here, "_cloud", "cloud.py")]
    T = lambda *a: run(*tool, *a, "--mirror", mirror)
    # a tracked file the cloud will delete, committed before init
    append(os.path.join(here, "srom-tlumacz", "zz_cloud_test_delete.txt"), "delete me in the cloud\n")
    run("git", "-C", os.path.join(here, "srom-tlumacz"), "add", "zz_cloud_test_delete.txt")
    run("git", "-C", os.path.join(here, "srom-tlumacz"), "commit", "-qm", "test: file to delete")
    append(os.path.join(here, "_widok", "local_only.html"), "<p>stays on this Mac</p>\n")
    before = {m: git(os.path.join(here, m), "rev-list", "--count", "HEAD") for m in ("srom-produkcja", "srom-tlumacz", "_handoffs")}

    run("git", "init", "-q", "--bare", "-b", "main", bare)
    code, out = T("init", "--remote", bare)
    check("init: mirror created", code == 0 and "mirror ready" in out, out)
    code, out = run("git", "-C", mirror, "push", "-q", "-u", "origin", "main")
    check("init: pushed to the stand-in for GitHub", code == 0, out)
    sha = git(os.path.join(here, "srom-produkcja"), "rev-parse", "HEAD")
    n = int(git(mirror, "rev-list", "--count", sha) or 0)
    check(f"mirror keeps srom-produkcja's history ({n} commits = {before['srom-produkcja']})", n == int(before["srom-produkcja"]))
    check("module commit hashes survive in the mirror (cited hashes still resolve)",
          git(mirror, "cat-file", "-t", sha) == "commit", sha)
    ignored = git(os.path.join(here, "srom-produkcja"), "ls-files", "--others", "--ignored", "--exclude-standard", "work").splitlines()
    data = next((p for p in ignored if p.endswith((".pdf", ".docx", ".json"))), None)
    check(f"data the module keeps out of git is committed in the mirror ({data})",
          data and git(mirror, "ls-files", f"srom-produkcja/{data}") == f"srom-produkcja/{data}", data)
    check(".gitignore stored as .gitignore.module; _widok not carried; mirror clean",
          os.path.isfile(os.path.join(mirror, "srom-produkcja", ".gitignore.module"))
          and not os.path.exists(os.path.join(mirror, "srom-produkcja", ".gitignore"))
          and not os.path.exists(os.path.join(mirror, "_widok")) and git(mirror, "status", "--porcelain") == "")

    # the cloud session
    run("git", "clone", "-q", bare, cloud)
    for k, v in (("user.name", "cloud"), ("user.email", "cloud@example.invalid")):
        run("git", "-C", cloud, "config", k, v)
    append(os.path.join(cloud, "srom-produkcja", "CLAUDE.md"), "\nCLOUD-EDIT-1\n")
    append(os.path.join(cloud, "srom-produkcja", "work", "ndiaye", "cloud_note.txt"), "data made in the cloud\n")
    os.remove(os.path.join(cloud, "srom-tlumacz", "zz_cloud_test_delete.txt"))
    append(os.path.join(cloud, "srom-tlumacz", ".gitignore.module"), "cloud-ignored/\n")
    run("git", "-C", cloud, "add", "-A"); run("git", "-C", cloud, "commit", "-qm", "cloud: produkcja edit, data, delete")
    append(os.path.join(cloud, "CLAUDE.md"), "\nCLOUD-ROOT-EDIT\n")
    append(os.path.join(cloud, "_handoffs", "code-to-cowork.md"), "\n## K99 — [general] test item (04.10.2026 00:00)\n")
    append(os.path.join(cloud, "_handoffs", "cowork-to-code.md"), "\nCLOUD MUST NOT WRITE THIS\n")
    run("git", "-C", cloud, "add", "-A"); run("git", "-C", cloud, "commit", "-qm", "cloud: root and handoff")
    code, out = run("git", "-C", cloud, "push", "-q", "origin", "main")
    check("cloud: two commits pushed", code == 0, out)

    # guards
    code, out = T("export")
    check("export refused while GitHub has cloud work not imported", code != 0 and "not imported" in out, out)
    stray = os.path.join(here, "srom-produkcja", "work", "ndiaye", "local_stray.txt")
    append(stray, "made here during the cloud phase\n")
    code, out = T("import")
    check("import refused when this folder changed since the sync, naming the file",
          code != 0 and "IMPORT REFUSED" in out and "local_stray.txt" in out, out)
    os.remove(stray)
    append(os.path.join(here, "_handoffs", "cowork-to-code.md"), "## C100 — [general] written by Cowork here\n")

    # import
    code, out = T("import")
    check("import runs (Cowork's channel file is no obstacle)", code == 0 and "imported" in out, out)
    P = lambda *p: os.path.join(here, *p)
    log = git(P("srom-produkcja"), "log", "-1", "--format=%s%n%b")
    check("srom-produkcja: one 'cloud import' commit listing the cloud commit",
          log.startswith("cloud import") and "cloud: produkcja edit, data, delete" in log, log)
    check("tracked edit arrived and is committed", "CLOUD-EDIT-1" in read(P("srom-produkcja", "CLAUDE.md"))
          and git(P("srom-produkcja"), "status", "--porcelain") == "")
    check("data file arrived and stays out of git (module rule kept)",
          os.path.isfile(P("srom-produkcja", "work", "ndiaye", "cloud_note.txt"))
          and git(P("srom-produkcja"), "ls-files", "work/ndiaye/cloud_note.txt") == "")
    check("deletion arrived and is committed", not os.path.exists(P("srom-tlumacz", "zz_cloud_test_delete.txt"))
          and git(P("srom-tlumacz"), "status", "--porcelain") == "")
    gi = read(P("srom-tlumacz", ".gitignore"))
    check(".gitignore.module came back as .gitignore", "cloud-ignored/" in gi
          and not os.path.exists(P("srom-tlumacz", ".gitignore.module")))
    check("root CLAUDE.md edit arrived", "CLOUD-ROOT-EDIT" in read(P("CLAUDE.md")))
    hs = read(P("_handoffs", "code-to-cowork.md")) if os.path.exists(P("_handoffs", "code-to-cowork.md")) else ""
    check("Code→Cowork item arrived in _handoffs and is committed", "K99" in hs and git(P("_handoffs"), "status", "--porcelain") == "")
    cw = read(P("_handoffs", "cowork-to-code.md"))
    check("Cowork's file kept as Cowork wrote it (the cloud's write ignored) and committed under 'cowork:'",
          "C100" in cw and "CLOUD MUST NOT" not in cw
          and "cowork:" in git(P("_handoffs"), "log", "--format=%s", "-3"), cw)
    check("_widok untouched", os.path.isfile(P("_widok", "local_only.html")))
    code, out = T("status")
    check("status after import: nothing changed here", "0 file(s) changed" in out, out)

    # back out again: a dirty module refuses, Cowork's new line travels
    append(P("srom-produkcja", "CLAUDE.md"), "uncommitted\n")
    code, out = T("export")
    check("export refused with uncommitted changes in a module", code != 0 and "uncommitted" in out, out)
    run("git", "-C", P("srom-produkcja"), "checkout", "--", "CLAUDE.md")
    append(P("_handoffs", "cowork-to-code.md"), "## C101 — [general] second Cowork item\n")
    code, out = T("sync")
    check("sync (import, then export) pushes Cowork's new item", code == 0 and "pushed" in out, out)
    run("git", "-C", cloud, "pull", "-q", "origin", "main")
    check("the cloud sees Cowork's new item after a pull", "C101" in read(os.path.join(cloud, "_handoffs", "cowork-to-code.md")))

    # everything else byte-identical: the mirror's tree equals this folder's carried files
    sys.path.insert(0, os.path.join(here, "_cloud"))
    import cloud as C
    C.ROOT = here
    a, b = C.manifest(C.walk(here, False)), C.manifest(C.walk(mirror, True))
    diff = sorted(r for r in set(a) | set(b) if a.get(r) != b.get(r))
    check(f"after the round trip, here and the mirror are identical ({len(a)} files)", not diff, diff[:10])
    n, ok = len(results), sum(results)
    print(f"ROUNDTRIP OK {n}/{n}" if ok == n else f"ROUNDTRIP FAILED {n - ok}/{n} (scratch kept: {tmp})")
    if ok == n:
        shutil.rmtree(tmp)
    return 0 if ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
