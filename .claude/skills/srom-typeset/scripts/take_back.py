#!/usr/bin/env python3
"""take_back.py — take a delivered translation into srom-typeset (handoff.md, "Back"; scenario C).

    python3 take_back.py <delivery_dir> <id> --src-dir work/<id> [--out work/<id>/pl]
                         [--expect <file>=<sha256 | first8…last7>] …

<delivery_dir> is srom-tlumacz's `work/<id>/`, read only. The delivery item (E-item) names the files with their
sha256. Required files: `<id>_robocza.docx` (the editor's Word file, the master), `<id>_pl.md` (its import),
`<id>_front_pl.md`. Optional files: `<id>_refs_tlum.json` and `<id>_pytania_tlum.csv`, taken when present.
Steps:
  1. every file present, and each --expect value matches (full hex, or the abbreviated form used in the
     handoff items, "3b060a87…1f3d5366"); with --expect, every file taken needs one
  2. copied to --out (default <src-dir>/pl); SHA256SUMS written there (shasum -a 256 -c format)
  3. the Word master is imported again (docx_in.py) and must equal the delivered `<id>_pl.md` byte for byte, so
     that what is built is what the editor approved
  4. check.py --pair <src-dir>/<id>_src.md against the copy, with <src-dir>/refs.json (+ the refs_tlum copy)
Then build from the copy (the command is printed). The copies are never edited. A correction goes into the
master, and a new delivery item follows.
Last line: TAKE-BACK OK <id> (n files) / TAKE-BACK FAILED <id>: n problem(s)
"""
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ("{id}_robocza.docx", "{id}_pl.md", "{id}_front_pl.md")
OPTIONAL = ("{id}_refs_tlum.json", "{id}_pytania_tlum.csv")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def short(h):
    return f"{h[:8]}…{h[-7:]}"


def matches(h, want):
    want = want.strip().lower()
    m = re.fullmatch(r"([0-9a-f]+)(?:…|\.\.\.)([0-9a-f]+)", want)
    if m:
        return h.startswith(m.group(1)) and h.endswith(m.group(2))
    return re.fullmatch(r"[0-9a-f]{64}", want) is not None and h == want


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("delivery_dir")
    ap.add_argument("id")
    ap.add_argument("--src-dir", required=True, help="srom-typeset's work/<id> (holds <id>_src.md and refs.json)")
    ap.add_argument("--out", help="where the copies go (default: <src-dir>/pl)")
    ap.add_argument("--expect", action="append", default=[], metavar="FILE=SHA256")
    a = ap.parse_args()
    i, dl, src = a.id, os.path.abspath(a.delivery_dir), os.path.abspath(a.src_dir)
    out = os.path.abspath(a.out or os.path.join(src, "pl"))
    probs = []
    if out == dl or out.startswith(dl + os.sep):
        sys.exit("take_back: --out must not be inside the delivery folder (it is the other module's)")
    names = [n.format(id=i) for n in REQUIRED]
    for n in names:
        if not os.path.isfile(os.path.join(dl, n)):
            probs.append(f"missing in the delivery: {n}")
    names += [n.format(id=i) for n in OPTIONAL if os.path.isfile(os.path.join(dl, n.format(id=i)))]
    names = [n for n in names if os.path.isfile(os.path.join(dl, n))]
    for n in ("{id}_src.md", "refs.json"):
        if not os.path.isfile(os.path.join(src, n.format(id=i))):
            probs.append(f"missing in --src-dir: {n.format(id=i)}")
    expect = {}
    for e in a.expect:
        f, _, h = e.partition("=")
        expect[f.strip()] = h
    hashes = {n: sha(os.path.join(dl, n)) for n in names}
    for n, h in hashes.items():
        if n in expect:
            if not matches(h, expect[n]):
                probs.append(f"sha256 differs from the delivery item: {n} is {short(h)}, item says {expect[n]}")
        elif expect:
            probs.append(f"no --expect for {n} (the delivery item must list every file)")
    for f in expect:
        if f not in hashes:
            probs.append(f"--expect names a file that is not delivered: {f}")
    for n, h in hashes.items():
        print(f"  {n:34} {short(h)}" + ("  (compared)" if n in expect and matches(h, expect[n]) else ""))
    if not expect:
        print("  note: no --expect given, sha256 not compared with a delivery item")
    if probs:
        return finish(i, probs, 0)
    os.makedirs(out, exist_ok=True)
    for n in names:
        shutil.copy2(os.path.join(dl, n), os.path.join(out, n))
        if sha(os.path.join(out, n)) != hashes[n]:
            probs.append(f"copy differs from the delivered file: {n}")
    with open(os.path.join(out, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        fh.writelines(f"{hashes[n]}  {n}\n" for n in names)
    # 3. the Word master, imported again, must be the delivered SROM-MD
    tmp = tempfile.mkdtemp()
    re_md = os.path.join(tmp, f"{i}_pl.md")
    r = subprocess.run([sys.executable, os.path.join(HERE, "docx_in.py"), os.path.join(out, f"{i}_robocza.docx"),
                        "-o", re_md], capture_output=True, text=True)
    if r.returncode or not os.path.isfile(re_md):
        probs.append("the Word master does not import: " + (r.stderr.strip().splitlines() or ["?"])[-1][:200])
    else:
        got, want = open(re_md, encoding="utf-8").read(), open(os.path.join(out, f"{i}_pl.md"), encoding="utf-8").read()
        if got != want:
            gl, wl = got.splitlines(), want.splitlines()
            k = next((j for j in range(min(len(gl), len(wl))) if gl[j] != wl[j]), min(len(gl), len(wl)))
            probs.append(f"{i}_pl.md is not the import of {i}_robocza.docx (first difference at line {k + 1}: "
                         f"delivered {wl[k][:80] if k < len(wl) else '<end>'!r}, Word {gl[k][:80] if k < len(gl) else '<end>'!r}) "
                         "— the md was edited after the import, or the Word file after the md was made")
    # 4. handoff check against the frozen source
    cmd = [sys.executable, os.path.join(HERE, "check.py"), "--pair", os.path.join(src, f"{i}_src.md"),
           os.path.join(out, f"{i}_pl.md"), "--refs", os.path.join(src, "refs.json")]
    if f"{i}_refs_tlum.json" in hashes:
        cmd += ["--refs", os.path.join(out, f"{i}_refs_tlum.json")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["?"])[-1]
    print(f"  check.py --pair: {last}")
    if r.returncode or "CHECK OK" not in last:
        probs.append("check.py --pair fails:\n" + r.stdout[-1500:])
    if not probs:
        q = f" --queries {out}/{i}_pytania_tlum.csv" if f"{i}_pytania_tlum.csv" in hashes else ""
        rt = f" --refs {out}/{i}_refs_tlum.json" if f"{i}_refs_tlum.json" in hashes else ""
        print(f"  build: python3 {HERE}/build.py {out}/{i}_pl.md --refs {src}/refs.json{rt} "
              f"--pair-src {src}/{i}_src.md{q} --out {src}/build/")
    return finish(i, probs, len(names))


def finish(i, probs, n):
    for p in probs:
        print("  PROBLEM " + p)
    print(f"TAKE-BACK OK {i} ({n} files)" if not probs else f"TAKE-BACK FAILED {i}: {len(probs)} problem(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
