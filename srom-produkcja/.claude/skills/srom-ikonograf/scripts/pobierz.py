"""Downloads for ikonograf runs in Cowork, whose VM reaches no repositories (SKILL.md § Where it runs).

Cowork writes `work/<id>/ikonografia/pobierz.tsv`, one request a line (tab-separated; `#` lines are comments):
    plik       <file name>   <url>    -> pliki/<file name>, as served (a chosen image, step 6)
    miniatura  <slot id>     <url>    -> miniatury/<slot id>.jpg, 800 px JPEG, embedded in kontaktowka.html (step 5)
This script (run on the Mac every few minutes by launchd, or by hand) does each request once and logs it in
`pobierz.log` next to the list: `dd.mm.yyyy HH:MM <tab> ok|FAIL <tab> name <tab> detail <tab> url`. A row is done when
the log has `ok` for the same name and URL; a FAIL is retried on the next run, up to three times.
Never the journal's own site: the live-site hook does not see this script, so it refuses those hosts itself.
Usage: pobierz.py [--root <workspace work dir>] [--allow-file]
"""
import base64, datetime, os, pathlib, re, subprocess, sys, tempfile, time

HERE = pathlib.Path(__file__).resolve()
WORK = HERE.parents[6] / "workspace" / "srom-produkcja" / "work"
UA = "SROM-ikonograf/0.2 (Studia Romologica, non-commercial journal research; https://github.com/blessero)"
REFUSED = ("studiaromologica", "seohost")
MAX_PER_RUN, PAUSE, TRIES = 40, 3, 3


def now():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")


def embed(d):
    """Write every miniatury/*.jpg into the sheet's MINI block (replaces the old lines)."""
    p = d / "kontaktowka.html"
    if not p.exists():
        return
    s = re.sub(r'<script>MINI\[.*?</script>\n', '', p.read_text(encoding="utf-8"))
    add = "".join(f'<script>MINI["miniatury/{f.name}"]="data:image/jpeg;base64,{base64.b64encode(f.read_bytes()).decode()}";</script>\n'
                  for f in sorted((d / "miniatury").glob("*.jpg")))
    p.write_text(s.replace("</body>", add + "</body>", 1), encoding="utf-8")


def fetch(url, out):
    r = subprocess.run(["curl", "-sSL", "--fail", "--max-time", "300", "-A", UA, "-o", str(out), url],
                       capture_output=True, text=True)
    if r.returncode:
        return r.stderr.strip()[-160:] or f"curl {r.returncode}"
    if not out.exists() or out.stat().st_size < 1000:
        return "empty or tiny file"
    return ""


def main(argv):
    work = pathlib.Path(argv[argv.index("--root") + 1]) if "--root" in argv else WORK
    schemes = ("http://", "https://", "file://") if "--allow-file" in argv else ("http://", "https://")
    done_n = 0
    for lst in sorted(work.glob("*/ikonografia/pobierz.tsv")):
        d, log = lst.parent, lst.parent / "pobierz.log"
        logged = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
        ok = {(l.split("\t")[2], l.split("\t")[4]) for l in logged if l.count("\t") >= 4 and l.split("\t")[1] == "ok"}
        fails = {}
        for l in logged:
            f = l.split("\t")
            if len(f) >= 5 and f[1] == "FAIL":
                fails[(f[2], f[4])] = fails.get((f[2], f[4]), 0) + 1
        new_thumb = False
        for line in lst.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            f = [x.strip() for x in line.split("\t")]
            if len(f) < 3:
                continue
            kind, name, url = f[0], f[1], f[2]
            key = (name, url)
            if key in ok or fails.get(key, 0) >= TRIES or done_n >= MAX_PER_RUN:
                continue
            res = ""
            if kind not in ("plik", "miniatura") or not name or "/" in name or name.startswith("."):
                res = "bad row (kind plik|miniatura, a plain file name)"
            elif not url.startswith(schemes) or any(h in url.lower() for h in REFUSED):
                res = "refused URL (not http(s), or the journal's own site)"
            if not res:
                done_n += 1
                with tempfile.TemporaryDirectory() as t:
                    tmp = pathlib.Path(t) / "src"
                    res = fetch(url, tmp)
                    if not res and kind == "plik":
                        (d / "pliki").mkdir(exist_ok=True)
                        os.replace(tmp, d / "pliki" / name)
                        detail = f"pliki/{name} {(d / 'pliki' / name).stat().st_size} B"
                    elif not res:
                        (d / "miniatury").mkdir(exist_ok=True)
                        out = d / "miniatury" / f"{name}.jpg"
                        r = subprocess.run(["sips", "-Z", "800", "-s", "format", "jpeg", "-s", "formatOptions", "70",
                                            str(tmp), "--out", str(out)], capture_output=True, text=True)
                        res = "" if r.returncode == 0 and out.exists() else "sips could not read it (not an image?)"
                        detail = f"miniatury/{name}.jpg {out.stat().st_size} B" if not res else ""
                        new_thumb = new_thumb or not res
                time.sleep(PAUSE)
            with log.open("a", encoding="utf-8") as fh:
                fh.write("\t".join([now(), "FAIL" if res else "ok", name, res or detail, url]) + "\n")
        if new_thumb:
            embed(d)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
