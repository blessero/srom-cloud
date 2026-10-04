"""Writes workspace/STATUS.md: src/STATUS_head.md + the hand-off log carried from Code, one row per text from the
sha256 files that record each hand-off (srom-tlumacz/work/<id>/src/manifest.sha256: RIP → TRANS; srom-produkcja
work/<id>/pl/SHA256SUMS: a take-back). The row's time is the sha256 file's mtime; the verdict is re-measured here."""
import glob, hashlib, os, time

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(M, "build/srom-cowork/workspace")
AUTHOR = {"ndiaye": "Ndiaye", "ostendorf": "Ostendorf", "pahulich": "Pahulich", "tittel": "Tittel",
          "westohueri": "West Ohueri", "scheffknecht": "Scheffknecht"}


NOW = time.strftime("%d.%m.%Y %H:%M")


def short(h): return f"{h[:8]}…{h[-7:]}"


def row(sumfile, what):
    d = os.path.dirname(sumfile)
    t = sumfile.split("/work/")[1].split("/")[0]
    pairs = [l.split(None, 1) for l in open(sumfile, encoding="utf-8").read().splitlines() if l.strip()]
    ok = all(hashlib.sha256(open(os.path.join(d, f.strip()), "rb").read()).hexdigest() == h for h, f in pairs)
    files = ", ".join(f"`{f.strip()}` {short(h)}" for h, f in pairs)
    when = time.strftime("%d.%m.%Y %H:%M", time.localtime(os.path.getmtime(sumfile)))
    rel = os.path.relpath(sumfile, W)
    return (when, f"| {when} | [{AUTHOR[t]}] | {what} (`{rel}`) | {files} | "
                  f"sha256 {'OK' if ok else 'MISMATCH'} on {NOW} (carried from Code) |")


rows = [row(f, "RIP → TRANS") for f in glob.glob(f"{W}/srom-tlumacz/work/*/src/manifest.sha256")]
rows += [row(f, "TRANS → INJECT trial, draft before MB's edit (not a delivery)")
         for f in glob.glob(f"{W}/srom-produkcja/work/*/pl/SHA256SUMS")]
rows.sort(key=lambda r: time.strptime(r[0], "%d.%m.%Y %H:%M"))
head = open(os.path.join(M, "src/STATUS_head.md"), encoding="utf-8").read()
log = ("\n| when | text | what | files and sha256 (`first8…last7`) | verdicts |\n|---|---|---|---|---|\n"
       + "\n".join(r for _, r in rows) + "\n")
open(os.path.join(W, "STATUS.md"), "w", encoding="utf-8").write(head + log)
print(f"STATUS WRITTEN {len(rows)} log rows")
