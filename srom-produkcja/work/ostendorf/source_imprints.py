# Missing places/publishers (queries A2, MB 28.09.2026: "source them") from the Library of Congress catalogue (SRU,
# MARC 264/260). A record is accepted only when its title matches the work's main title, its date is the work's year,
# and (where refs.json has one) its publisher matches ours; place = the first place of the imprint, brackets removed
# (Kanon § 7.2: place as on the title page, not polonised). Several matching records that disagree -> not resolved.
# Output: imprints.tsv (key, field, value, evidence = LCCN + raw imprint) — the evidence for every value refs.py takes.
import json, re, sys, time, unicodedata, urllib.parse, urllib.request
from xml.etree import ElementTree as ET

M = "{http://www.loc.gov/MARC21/slim}"
SRU = "http://lx2.loc.gov:210/LCDB?operation=searchRetrieve&version=1.1&maximumRecords=25&recordSchema=marcxml&query="


def fold(s):
    s = unicodedata.normalize("NFD", s or "")
    return re.sub(r"[^a-z0-9 ]", " ", "".join(c for c in s if unicodedata.category(c) != "Mn").lower())


def words(s):
    return [w for w in fold(s).split() if w not in ("the", "a", "an", "of", "and", "in", "de", "la", "da", "y", "e", "der", "die", "und")]


def sru(q):
    for i in range(4):
        try:
            with urllib.request.urlopen(SRU + urllib.parse.quote(q), timeout=90) as r:
                root = ET.fromstring(r.read())
            if root.find("{http://www.loc.gov/zing/srw/}numberOfRecords") is None:
                raise ValueError("diagnostic: " + ET.tostring(root, encoding="unicode")[-300:])
            return root
        except Exception as e:
            err = e
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"SRU failed for {q!r}: {err}")


def subs(df, code):
    return [s.text or "" for s in df.findall(M + "subfield") if s.get("code") == code]


def records(root):
    for rec in (root.iter(M + "record") if root is not None else []):
        f = {}
        for cf in rec.findall(M + "controlfield"):
            f[cf.get("tag")] = cf.text or ""
        dfs = {}
        for df in rec.findall(M + "datafield"):
            dfs.setdefault(df.get("tag"), []).append(df)
        imp = [d for d in dfs.get("264", []) if d.get("ind2") == "1"] or dfs.get("260", [])
        if not imp:
            continue
        d = imp[0]
        title = " ".join(subs(dfs.get("245", [None])[0], "a") + subs(dfs.get("245", [None])[0], "b")) if dfs.get("245") else ""
        lccn = (subs(dfs["010"][0], "a") or [""])[0].strip() if dfs.get("010") else f.get("001", "")
        yield {"title": title, "places": subs(d, "a"), "pubs": subs(d, "b"), "date": " ".join(subs(d, "c")),
               "y008": f.get("008", "")[7:11], "lccn": lccn,
               "raw": " ".join(f"{s.get('code')}={s.text}" for s in d.findall(M + "subfield"))}


def clean_place(p):
    """the city as on the title page: "Oxford, United Kingdom" -> Oxford, "Basingstoke [England]" -> Basingstoke"""
    p = re.sub(r"\[[^\]]*\]", "", p).strip(" :;,.")
    p = re.sub(r"\s*\(.*?\)\s*", " ", p).strip()
    return p.split(",")[0].strip()


def clean_pub(p):
    return re.sub(r"\s*\.\.\.$", "", re.sub(r"[\[\]]", "", p)).strip(" :;,.")


def archive_org(title, year):
    """second source for old books: the catalogue record of a digitised copy (archive.org, publisher = "Place : Name")"""
    q = f'title:({" ".join(words(title)[:6])}) AND year:{year}'
    u = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": q, "fl[]": ["identifier", "title", "publisher", "date"], "rows": 10, "output": "json"}, doseq=True)
    try:
        with urllib.request.urlopen(u, timeout=60) as r:
            docs = json.load(r)["response"]["docs"]
    except Exception:
        return []
    out = []
    for d in docs:
        pub = d.get("publisher")
        pub = pub[0] if isinstance(pub, list) else pub
        if pub and ":" in pub and all(w in words(d.get("title", "")) for w in words(title)[:4]):
            pl, _, pb = pub.partition(":")
            out.append({"places": [pl], "pubs": [pb], "lccn": "archive.org " + d["identifier"], "raw": pub, "title": d.get("title", ""),
                        "date": str(d.get("date", "")), "y008": ""})
    return out


refs = {r["id"]: r for r in json.load(open("refs.json", encoding="utf-8"))}
todo = [k for k, r in refs.items() if (not r.get("publisher-place") or (not r.get("publisher")
        and (r.get("issued", {}).get("date-parts", [[9999]])[0][0] > 1800))) and r["type"] not in ("article-journal", "article-newspaper")]
out = [("key", "field", "value", "evidence")]
for k in todo:
    r = refs[k]
    yr = str(r["issued"]["date-parts"][0][0])
    chap = r["type"] == "chapter" and r.get("container-title")
    main = re.split(r"[:;]", r["container-title"] if chap else r["title"])[0]
    main = re.sub(r"<[^>]+>", "", main)
    tw = words(main)[:6]
    au = ((r.get("editor") if chap else None) or r.get("author") or r.get("editor") or [{}])[0].get("family", "")
    q = " and ".join(f'bath.title="{w}"' for w in tw[:5])
    if au:
        q += f' and bath.author="{fold(au).split()[0] if fold(au).split() else au}"'
    got = []
    try:
        found = list(records(sru(q)))
        if not found and au:
            time.sleep(2)
            found = list(records(sru(" and ".join(f'bath.title="{w}"' for w in tw[:5]))))     # without the name
    except RuntimeError as e:
        out.append((k, "publisher-place" if not r.get("publisher-place") else "publisher", "ERROR", str(e)[:200]))
        print(k, "-> ERROR", file=sys.stderr); continue
    for rec in found:
        if not all(w in words(rec["title"]) for w in tw[:5]):
            continue
        if yr not in rec["date"] and rec["y008"] != yr:
            continue
        if r.get("publisher") and r["type"] != "thesis":
            ours = set(words(r["publisher"])) - {"press", "university", "publishers", "books"}
            theirs = set(words(" ".join(rec["pubs"])))
            if ours and not ours & theirs:
                continue
        if r.get("publisher-place") and rec["places"] and fold(clean_place(rec["places"][0])) != fold(r["publisher-place"]):
            continue                     # another edition (Philadelphia vs London)
        got.append(rec)
    if not got and int(yr) < 1930:
        got = [g for g in archive_org(main, yr)
               if not r.get("publisher-place") or fold(clean_place(g["places"][0])) == fold(r["publisher-place"])]
    places = {clean_place(g["places"][0]) for g in got if g["places"]}
    pubs = {clean_pub(g["pubs"][0]) for g in got if g["pubs"]}
    ev = " || ".join(f"LCCN {g['lccn']}: {g['raw']}" for g in got[:3])
    if not r.get("publisher-place"):
        out.append((k, "publisher-place", places.pop() if len(places) == 1 else ("?" if not places else "CONFLICT: " + " / ".join(sorted(places))), ev or "no matching LoC record"))
    if not r.get("publisher") and int(yr) > 1800:
        out.append((k, "publisher", pubs.pop() if len(pubs) == 1 else ("?" if not pubs else "CONFLICT: " + " / ".join(sorted(pubs))), ev or "no matching LoC record"))
    print(k, "->", out[-1][2][:60], file=sys.stderr)
    time.sleep(2)
open("imprints.tsv", "w", encoding="utf-8").write("\n".join("\t".join(x) for x in out) + "\n")
print(f"{len(out) - 1} fields; resolved {sum(1 for x in out[1:] if x[2] not in ('?', 'ERROR') and not x[2].startswith('CONFLICT'))}")
