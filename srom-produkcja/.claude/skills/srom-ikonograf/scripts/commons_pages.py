#!/usr/bin/env python3
"""Download thumbnails of many Commons files for triage by eye (learnt 25.10.2026; the Missouri Historical Society albums).

    commons_pages.py <out-dir> --prefix "<file-name prefix without File:>" [--filter <regex>] [--width 500]
    commons_pages.py <out-dir> --category "Category:<name>" [--filter <regex>] [--width 500]

Lists the files (allpages prefix, or category members), keeps those whose name matches --filter, and saves each as
<out-dir>/<key>.jpg where <key> is `a<album>_p<page>` when the name has "Album <n> … (page <k>)", else a slug.
Existing files are skipped, so a stopped run resumes. Run it in the background with nohup for hundreds of files:
about 1.3 s a file (Commons 429s a bare User-Agent; this one is named, no journal domain: sources.md § Wikimedia).
Then `montage.py --grid <out-dir> a10_` (20 pages per image)."""
import sys, re, os, json, time, argparse, urllib.request, urllib.parse

UA = "SROM-ikonograf/0.2 (Studia Romologica, non-commercial journal research; https://github.com/blessero)"
def get(url, tries=4):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90).read()
        except Exception:
            time.sleep(10 * (k + 1))
    return None
def api(**p):
    p["format"] = "json"
    return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--prefix"); ap.add_argument("--category")
ap.add_argument("--filter", default=""); ap.add_argument("--width", type=int, default=500)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)

titles, cont = [], {}
while True:
    if a.prefix: d = api(action="query", list="allpages", apnamespace=6, apprefix=a.prefix, aplimit=500, **cont); k = "allpages"
    else: d = api(action="query", list="categorymembers", cmtitle=a.category, cmtype="file", cmlimit=500, **cont); k = "categorymembers"
    titles += [x["title"] for x in d["query"][k]]
    if "continue" in d: cont = d["continue"]; time.sleep(2)
    else: break
if a.prefix: titles = ["File:" + t.split(":", 1)[1] if not t.startswith("File:") else t for t in titles]
titles = [t for t in titles if re.search(a.filter, t)]
print(len(titles), "files")
def key(t):
    m = re.search(r"Album (\d+) .*?\(page (\d+)\)", t)
    return "a%s_p%03d" % (m.group(1), int(m.group(2))) if m else re.sub(r"[^A-Za-z0-9]+", "_", t[5:])[:60]
for i in range(0, len(titles), 30):
    chunk = titles[i:i + 30]
    d = api(action="query", titles="|".join(chunk), prop="imageinfo", iiprop="url", iiurlwidth=a.width)
    for pg in d["query"]["pages"].values():
        th = (pg.get("imageinfo") or [{}])[0].get("thumburl"); fn = os.path.join(a.out, key(pg["title"]) + ".jpg")
        if th and not os.path.exists(fn):
            b = get(th)
            if b: open(fn, "wb").write(b)
            time.sleep(1.3)
print("done:", len(os.listdir(a.out)), "files in", a.out)
