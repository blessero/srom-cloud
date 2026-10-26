"""Build a record's contact sheet from its rows file (SKILL.md step 5), so nothing on the sheet is kept by hand.

    kontaktowka_build.py <record dir> [--commons-info] [--outputs <dir> | --no-mirror]
    kontaktowka_build.py <record dir> --from-html [--force]

`<record dir>` is `work/<id>/ikonografia/`. The rows file `kontaktowka.json` there has the shape of the sheet's DATA:
    {"text": "...", "note": "...", "slots": {"S1": "idea", ...},
     "items": [{"id": "S1-a", "slot": "S1", "src": "commons:File name.jpg", "title": ..., "date": ..., "creator": ...,
                "holder": ..., "cls": "A", "size": ..., "page": ..., "full": ..., "why": ..., "metryka": ...,
                "alt": [{"label", "url", "why"}], "also": ""}, ...]}
Each build takes the renderer from the skill's current template, writes `kontaktowka.html`, embeds every
`miniatury/*.jpg` (so a rebuild can never drop them) and refreshes MB's copy in `Claude outputs/` (pobierz.py).
`src` fills `thumb`, `full`, `page` and `size` where the row leaves them empty (a field given in the row always wins):
    commons:<file name>       Special:FilePath thumbnail (960), the File: page; `--commons-info` adds full URL and size
    loc:<coll>-<number>       tile.loc.gov `v.jpg` (ppmsca, cwpb, ds …: folder = number rounded down to 100)
    si:<ids id>               ids.si.edu, 900 px
    ia:<id>/n<k>              Internet Archive page image, 700 px, and its BookReader page
    iiif:<image service base> `!700,700` thumbnail, `full/max` file
    getty:<uuid>              media.getty.edu IIIF, `!700,700`
    mini:<url>                downloaded once to miniatury/<id>.jpg (browser User-Agent: some servers send curl a
                              placeholder), 800 px, embedded; from Cowork use a `miniatura` row in pobierz.tsv instead
Checks: duplicate ids, a slot not in `slots`, an unknown class or `src` kind stop the build (exit 1); rows without a
thumbnail, holder or metryka are listed. The metryka stays hand-written (Kanon § 10.3 needs technique and Polish date
forms the fields do not carry); the build only reports where it is missing.
`--from-html` writes `kontaktowka.json` from an existing sheet's DATA block (once per old sheet; needs node).
"""
import json, pathlib, re, shutil, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import pobierz  # embed(), mirror(), WORK, OUTPUTS: one place for both

TEMPLATE = HERE.parents[1] / "assets" / "template" / "kontaktowka.html"
UA = pobierz.UA
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
CLASSES = set("ABCDEF")
FIELDS = ("id", "slot", "thumb", "title", "date", "creator", "holder", "cls", "size", "page", "full", "why", "metryka",
          "alt", "also")
START, END = "const DATA = ", "\n/* ---- rendering"


def q(name):
    return urllib.parse.quote(name.replace(" ", "_"), safe="(),!'*~$:@&=+;")


def resolve(item, d, info):
    """Fill thumb/full/page/size from src; return an error string or ''."""
    src = item.get("src", "")
    if not src:
        return ""
    kind, _, key = src.partition(":")
    key = key.strip()
    fill = {}
    if kind == "commons":
        fill = {"thumb": "https://commons.wikimedia.org/wiki/Special:FilePath/"
                         + urllib.parse.quote(key.replace(" ", "_")) + "?width=960",
                "page": f"https://commons.wikimedia.org/wiki/File:{q(key)}"}
        v = info.get(key)
        if v:
            fill["full"] = v["url"]
            if v.get("w"):
                fill["size"] = f"{v['w']} × {v['h']} px (Commons file)"
    elif kind == "loc":
        m = re.fullmatch(r"([a-z]+)-(\d{5})", key)
        if not m:
            return f"loc:{key}: expected <collection>-<5 digits> (e.g. ppmsca-80097); give `thumb` for other folders"
        u = (f"https://tile.loc.gov/storage-services/service/pnp/{m[1]}/{int(m[2]) // 100 * 100:05d}/{m[2]}v.jpg")
        fill = {"thumb": u, "full": u, "size": "LoC 'v' (about 1000 px)"}
    elif kind == "si":
        u = f"https://ids.si.edu/ids/deliveryService?max_w=900&id={key}"
        fill = {"thumb": u, "full": u}
    elif kind == "ia":
        m = re.fullmatch(r"([^/]+)/n(\d+)", key)
        if not m:
            return f"ia:{key}: expected <identifier>/n<leaf>"
        fill = {"thumb": f"https://archive.org/download/{m[1]}/page/n{m[2]}_w700.jpg",
                "full": f"https://archive.org/download/{m[1]}/page/n{m[2]}.jpg",
                "page": f"https://archive.org/details/{m[1]}/page/n{m[2]}/mode/1up"}
    elif kind == "iiif":
        base = key.rstrip("/")
        fill = {"thumb": base + "/full/!700,700/0/default.jpg", "full": base + "/full/max/0/default.jpg"}
    elif kind == "getty":
        fill = {"thumb": f"https://media.getty.edu/iiif/image/{key}/full/!700,700/0/default.jpg",
                "full": f"https://media.getty.edu/iiif/image/{key}/full/max/0/default.jpg"}
    elif kind == "mini":
        out = d / "miniatury" / f"{item['id']}.jpg"
        if not out.exists():
            err = fetch_mini(key, out)
            if err:
                return f"mini {item['id']}: {err}"
        fill = {"thumb": f"miniatury/{item['id']}.jpg"}
        if not item.get("full"):
            fill["full"] = key
    else:
        return f"{item.get('id')}: unknown src kind {kind!r}"
    for k, v in fill.items():
        if not item.get(k):
            item[k] = v
    return ""


def fetch_mini(url, out):
    out.parent.mkdir(exist_ok=True)
    tmp = out.with_suffix(".src")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
        tmp.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    except Exception as e:  # noqa: BLE001 - any failure is reported on the row
        return f"download failed: {str(e)[:120]}"
    try:
        if tmp.stat().st_size < 1000:
            return "empty or tiny file"
        if shutil.which("sips"):
            r = subprocess.run(["sips", "-Z", "800", "-s", "format", "jpeg", "-s", "formatOptions", "70", str(tmp),
                                "--out", str(out)], capture_output=True, text=True)
            return "" if r.returncode == 0 and out.exists() else "sips could not read it (not an image?)"
        try:
            from PIL import Image
        except ImportError:
            return "no sips and no Pillow to make the thumbnail"
        im = Image.open(tmp).convert("RGB")
        im.thumbnail((800, 800))
        im.save(out, quality=70)
        return ""
    finally:
        if tmp.exists():
            tmp.unlink()


def commons_info(names, cache_path):
    """Full URL and size of Commons files, 25 a call, cached next to the rows file (Commons 429s bursts)."""
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    todo = [n for n in names if n not in cache]
    for i in range(0, len(todo), 25):
        chunk = todo[i:i + 25]
        url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "titles": "|".join("File:" + n for n in chunk), "prop": "imageinfo",
             "iiprop": "url|size", "format": "json", "formatversion": "2"})
        for k in range(4):
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90)
                data = json.loads(r.read())
                break
            except urllib.error.HTTPError as e:
                time.sleep(int(e.headers.get("retry-after") or 10) if e.code == 429 else 10 * (k + 1))
            except Exception:  # noqa: BLE001
                time.sleep(10 * (k + 1))
        else:
            print("commons-info: no answer after 4 tries; the rest stay without size", file=sys.stderr)
            break
        norm = {x["to"]: x["from"] for x in data.get("query", {}).get("normalized", [])}
        for p in data.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("url"):
                name = norm.get(p["title"], p["title"]).split(":", 1)[1]
                cache[name] = cache[name.replace("_", " ")] = {"url": ii["url"], "w": ii.get("width"), "h": ii.get("height")}
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
        time.sleep(3)
    return cache


def data_js(rows):
    """DATA as JSON, one item per line; `</` escaped so no string can close the script element."""
    head = {k: rows[k] for k in ("text", "note", "slots")}
    lines = [json.dumps({k: i.get(k, [] if k == "alt" else "") for k in FIELDS}, ensure_ascii=False) for i in rows["items"]]
    s = json.dumps(head, ensure_ascii=False, indent=1)[:-2] + ',\n "items": [\n  ' + ",\n  ".join(lines) + "\n ]\n}"
    return s.replace("</", "<\\/")


def build(d, commons=False, outputs=None, quiet=False):
    """Write d/kontaktowka.html from d/kontaktowka.json; return the list of errors (empty = built)."""
    d = pathlib.Path(d)
    rows = json.loads((d / "kontaktowka.json").read_text(encoding="utf-8"))
    items, slots = rows.get("items", []), rows.get("slots", {})
    errs, seen = [], set()
    for i in items:
        if i.get("id") in seen:
            errs.append(f"duplicate id {i.get('id')}")
        seen.add(i.get("id"))
        if i.get("slot") not in slots:
            errs.append(f"{i.get('id')}: slot {i.get('slot')!r} not in slots")
        if i.get("cls") not in CLASSES:
            errs.append(f"{i.get('id')}: class {i.get('cls')!r} is not one of A–F")
    info = {}
    if commons:
        names = [i["src"].split(":", 1)[1].strip() for i in items if i.get("src", "").startswith("commons:")]
        info = commons_info(names, d / "kontaktowka.commons.json")
    for i in items:
        e = resolve(i, d, info)
        if e:
            errs.append(e)
    if errs:
        for e in errs:
            print("ERROR", e, file=sys.stderr)
        return errs
    t = TEMPLATE.read_text(encoding="utf-8")
    a, b = t.index(START), t.index(END)
    (d / "kontaktowka.html").write_text(t[:a] + START + data_js(rows) + ";" + t[b:], encoding="utf-8")
    pobierz.embed(d)
    if outputs:
        pobierz.mirror(d.parent.parent, outputs)
    if not quiet:
        miss = lambda k: [i["id"] for i in items if not i.get(k)]
        print(f"built {d / 'kontaktowka.html'}: {len(items)} rows in {len(slots)} slots; "
              f"{len(list((d / 'miniatury').glob('*.jpg'))) if (d / 'miniatury').is_dir() else 0} local thumbnails embedded")
        for k, what in (("thumb", "no thumbnail"), ("holder", "no holder"), ("metryka", "no metryka draft"), ("full", "no full-resolution URL")):
            m = miss(k)
            if m:
                print(f"  {what} ({len(m)}): {' '.join(m[:30])}{' …' if len(m) > 30 else ''}")
    return []


EXTRACT = r"""
const fs = require("fs"), vm = require("vm");
const s = fs.readFileSync(process.argv[1], "utf8"), i = s.indexOf("const DATA = ");
if (i < 0) { console.error("no DATA block"); process.exit(2); }
let j = i + 13, depth = 0, q = null, esc = false;
for (; j < s.length; j++) { const c = s[j];
  if (q) { if (esc) esc = false; else if (c === "\\") esc = true; else if (c === q) q = null; continue; }
  if (c === '"' || c === "'" || c === "`") q = c;
  else if (c === "{" || c === "[") depth++;
  else if (c === "}" || c === "]") { depth--; if (!depth) { j++; break; } } }
process.stdout.write(JSON.stringify(vm.runInNewContext("(" + s.slice(i + 13, j) + ")", {}, { timeout: 2000 })));
"""


def from_html(d, force=False):
    d = pathlib.Path(d)
    out = d / "kontaktowka.json"
    if out.exists() and not force:
        print(f"{out} exists: edit it, or pass --force to replace it from the sheet", file=sys.stderr)
        return 1
    node = shutil.which("node")
    if not node:
        print("--from-html needs node (the old sheets' DATA is JavaScript, not JSON)", file=sys.stderr)
        return 1
    r = subprocess.run([node, "-e", EXTRACT, str(d / "kontaktowka.html")], capture_output=True, text=True)
    if r.returncode:
        print(r.stderr.strip(), file=sys.stderr)
        return 1
    rows = json.loads(r.stdout)
    rows["items"] = [{**{k: [] if k == "alt" else "" for k in FIELDS}, **i} for i in rows["items"]]  # extra keys kept
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out}: {len(rows['items'])} rows in {len(rows['slots'])} slots")
    return 0


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    d = pathlib.Path(argv[0]).resolve()
    if "--from-html" in argv:
        return from_html(d, "--force" in argv)
    if "--outputs" in argv:
        outputs = pathlib.Path(argv[argv.index("--outputs") + 1])
    elif "--no-mirror" in argv:
        outputs = None
    else:  # a record in the workspace refreshes MB's copy; anything else (a test) only with --outputs
        outputs = pobierz.OUTPUTS if pobierz.WORK.resolve() in d.parents else None
    return 1 if build(d, "--commons-info" in argv, outputs) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
