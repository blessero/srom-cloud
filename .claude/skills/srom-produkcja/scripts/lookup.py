#!/usr/bin/env python3
"""
lookup.py — find data the author did not give; proposes, never writes refs.json (Kanon § 0: the editor confirms).

    python3 lookup.py missing "Jenkins and Leroy" 2021 [--hint "racial capitalism"] [--csv q.csv] [--json cand.json]
        a work cited in the text but missing from the author's bibliography (cite_map: NOT-CITED? / UNKNOWN that is
        a citation): Crossref search by the names (+ hint words from the sentence) and the year; candidates whose
        year matches and whose authors/editors include every name. --csv: a query row for build.py --queries
        (to the author: confirm the work); --json: the candidates as CSL-JSON drafts ("srom-candidate": true) —
        copied into refs.json only after confirmation.
    python3 lookup.py webdate URL
        publication date of a web text (Kanon § 8.6) from the page itself: meta article:published_time,
        itemprop/JSON-LD datePublished, <time datetime>; the URL it redirects to.
    python3 lookup.py webdates refs.json [--csv q.csv]
        webdate for every webpage/post in refs.json without a full publication date and not marked "srom-undated".
    python3 lookup.py dois refs.json [--csv q.csv] [--tsv doi_check.tsv]
        Kanon § 9.7: every DOI checked against its registry (year, volume, issue, first page, title, first author:
        differences listed); for articles, chapters and books without a DOI, a Crossref DOI proposed only when year,
        first author, title (and an article's volume and first page) agree. Query rows to the editor (GEN-10).
    python3 lookup.py imprints refs.json [--csv q.csv] [--tsv imprints.tsv]
        missing place/publisher of books and chapters from the Library of Congress, DNB and BN catalogues (MARC):
        title words + year (+ what refs.json already has) must agree; one value proposed, several = CONFLICT, none = ?.
        Query rows to the editor, for approval item by item (GEN-4). Replaces work/ostendorf/source_imprints.py.
Tests: --from-file FILE (missing, webdate) or --canned FILE (dois, imprints) replaces the network.
Last line: LOOKUP OK n / LOOKUP NONE
"""
import argparse, csv, json, re, sys, unicodedata, urllib.parse, urllib.request

UA = {"User-Agent": "SROM-typeset/1.0 (Studia Romologica; mailto:michalbartosz@hotmail.com)"}


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.replace("ł", "l")) if unicodedata.category(c) != "Mn").casefold()


def get(url, from_file=None):
    if from_file:
        return open(from_file, encoding="utf-8").read(), url
    req = urllib.request.Request(url, headers=dict(UA, **{"User-Agent": "Mozilla/5.0 " + UA["User-Agent"]}))
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", errors="replace"), r.geturl()


# ------------------------------------------------------------------ missing work
def names_of(s):
    s = re.sub(r"\s(?:et al\.|i in\.)$", "", s.strip())
    return [p.strip() for p in re.split(r",\s|\s(?:and|i|&)\s", s) if p.strip()]


def csl_from_crossref(w):
    typ = {"journal-article": "article-journal", "book-chapter": "chapter", "edited-book": "book", "monograph": "book",
           "book": "book", "reference-entry": "entry-encyclopedia", "report": "report"}.get(w.get("type"), w.get("type"))
    d = {"id": "", "type": typ, "title": (w.get("title") or [""])[0], "srom-candidate": True,
         "srom-source": "https://doi.org/" + w["DOI"] if w.get("DOI") else "Crossref"}
    for role in ("author", "editor"):
        if w.get(role):
            d[role] = [{"family": a.get("family", ""), "given": a.get("given", "")} for a in w[role] if a.get("family")]
    if w.get("container-title"):
        d["container-title"] = w["container-title"][0]
    dp = (w.get("issued") or w.get("published") or {}).get("date-parts") or [[None]]
    if dp[0][0]:
        d["issued"] = {"date-parts": [[dp[0][0]]]}
    for k in ("volume", "issue", "page", "publisher", "DOI"):
        if w.get(k):
            d[k] = w[k]
    first = (d.get("author") or d.get("editor") or [{"family": "x"}])[0]["family"]
    d["id"] = re.sub(r"[^a-z]", "", fold(first)) + str(dp[0][0] or "")
    return d


def describe(d):
    who = d.get("author") or d.get("editor") or []
    names = ", ".join(f"{a.get('given', '')} {a['family']}".strip() for a in who) + (" (red.)" if not d.get("author") and who else "")
    parts = [names, d.get("title", "")]
    if d.get("container-title"):
        parts.append("w: " + d["container-title"])
    parts += [d.get("publisher", ""), str((d.get("issued") or {}).get("date-parts", [[""]])[0][0])]
    if d.get("DOI"):
        parts.append("DOI: " + d["DOI"])
    return ", ".join(p for p in parts if p)


def missing(a):
    names = names_of(a.names)
    q = urllib.parse.urlencode({"query.bibliographic": " ".join(names + [a.year] + ([a.hint] if a.hint else [])), "rows": 20})
    txt, _ = get("https://api.crossref.org/works?" + q, a.from_file)
    items = json.loads(txt, strict=False)["message"]["items"]
    cands = []
    for w in items:
        fams = {fold(p.get("family", "")) for r in ("author", "editor") for p in w.get(r, [])}
        dp = (w.get("issued") or w.get("published") or {}).get("date-parts") or [[None]]
        if str(dp[0][0]) == a.year and all(fold(n) in fams for n in names):
            cands.append(csl_from_crossref(w))
    # a book and its chapters: the book (or edited book) first, chapters after
    cands.sort(key=lambda d: (d["type"] == "chapter", d.get("title", "")))
    for i, d in enumerate(cands, 1):
        print(f"CANDIDATE {i}: {describe(d)}")
    if a.json and cands:
        json.dump(cands, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.csv:
        det = ("; ".join(f"({i}) {describe(d)}" for i, d in enumerate(cands[:3], 1)) if cands
               else "nie znaleziono w Crossref — prosimy o opis")
        write_rows(a.csv, [("autor", "praca przywołana w tekście, brak w bibliografii — proszę potwierdzić opis", a.note or "",
                            f"{a.names} {a.year}", det)])
    print(f"LOOKUP OK {len(cands)}" if cands else "LOOKUP NONE")
    return 0


# ------------------------------------------------------------------ web dates
DATE_RX = [
    ("article:published_time", r'<meta[^>]+(?:property|name)=["\']article:published_time["\'][^>]+content=["\']([^"\']+)'),
    ("article:published_time", r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']article:published_time'),
    ("datePublished", r'itemprop=["\']datePublished["\'][^>]+content=["\']([^"\']+)'),
    ("datePublished", r'"datePublished"\s*:\s*"([^"]+)"'),
    ("<time datetime>", r'<time[^>]+datetime=["\']([^"\']+)'),
]


def webdate_of(url, from_file=None):
    html, final = get(url, from_file)
    for src, rx in DATE_RX:
        m = re.search(rx, html, re.I)
        if m:
            dm = re.match(r"(\d{4})-(\d{2})-(\d{2})", m.group(1))
            if dm:
                return [int(x) for x in dm.groups()], src, final
    return None, None, final


def webdate(a):
    d, src, final = webdate_of(a.url, a.from_file)
    if final != a.url and not a.from_file:
        print(f"REDIRECT {a.url} -> {final}")
    if d:
        print(f"WEBDATE {d[2]:02d}.{d[1]:02d}.{d[0]} ({src})")
        print("LOOKUP OK 1")
    else:
        print("no publication date on the page — an undated page: \"srom-undated\": true")
        print("LOOKUP NONE")
    return 0


def webdates(a):
    refs = json.load(open(a.refs, encoding="utf-8"))
    rows, n = [], 0
    for r in refs:
        dp = ((r.get("issued") or {}).get("date-parts") or [[]])[0]
        if r.get("type") not in ("webpage", "post", "post-weblog") or len(dp) >= 3 or r.get("srom-undated") or not r.get("URL"):
            continue
        try:
            d, src, final = webdate_of(r["URL"], a.from_file)
        except Exception as e:
            print(f"{r['id']}: page not read ({e})")
            continue
        given = ".".join(str(x) for x in reversed(dp)) or "brak"
        if d:
            n += 1
            ok = dp == d[:len(dp)]
            print(f"{r['id']}: page {d[2]:02d}.{d[1]:02d}.{d[0]} ({src}); the author: {given}{'' if ok else ' — DIFFERS'}"
                  + (f"; URL now {final}" if final != r["URL"] and not a.from_file else ""))
            rows.append(("redakcja", "data publikacji ze strony — uzupełnić (§ 8.6)" + ("" if ok else "; różni się od autora"),
                         "", r["id"], f"{d[2]:02d}.{d[1]:02d}.{d[0]} ({src}); autor: {given}"))
        else:
            print(f"{r['id']}: no date on the page — mark \"srom-undated\": true")
    if a.csv and rows:
        write_rows(a.csv, rows)
    print(f"LOOKUP OK {n}" if n else "LOOKUP NONE")
    return 0


# ------------------------------------------------------------------ canned responses (tests)
def fetch(url, canned=None):
    """the network, or in tests a JSON map {url substring: response body}"""
    if canned is not None:
        for k, v in canned.items():
            if k in url:
                return v
        raise RuntimeError("no canned response for " + url)
    return get(url)[0]


def doi_meta(doi, canned=None):
    """Crossref's record (most DOIs here); otherwise the registry's CSL-JSON by content negotiation (DataCite, mEDRA)"""
    try:
        return json.loads(fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi), canned), strict=False)["message"]
    except Exception:
        if canned is not None:
            return json.loads(fetch("https://doi.org/" + doi, canned))
        req = urllib.request.Request("https://doi.org/" + doi, headers=dict(UA, Accept="application/vnd.citationstyles.csl+json"))
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode("utf-8"))


def words(s):
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", fold(re.sub(r"<[^>]+>", " ", s or ""))).split()
            if w not in ("the", "a", "an", "of", "and", "in", "de", "la", "da", "y", "e", "der", "die", "das", "und", "i", "w", "z", "na")]


def year_of(d):
    return str(((d.get("issued") or {}).get("date-parts") or [[None]])[0][0] or "")


# ------------------------------------------------------------------ DOIs (Kanon § 9.7)
def dois(a):
    """every DOI in refs.json checked against its registry (doi.org, CSL-JSON: Crossref, DataCite, mEDRA); for articles,
    chapters and books without one, a Crossref candidate is proposed only when year, first author and title agree (and,
    for an article, volume and first page where both have them). Proposals and differences are for the editor, never
    written into refs.json (MB-decisions GEN-10)."""
    canned = json.load(open(a.canned, encoding="utf-8")) if a.canned else None
    refs = json.load(open(a.refs, encoding="utf-8"))
    rows, lines, n = [], [], 0
    for r in refs:
        who = (r.get("author") or r.get("editor") or [{}])[0].get("family", "")
        if r.get("DOI"):
            try:
                reg = doi_meta(r["DOI"], canned)
            except Exception as e:
                lines.append(f"{r['id']}\tNOT RESOLVED\t{r['DOI']}\t{str(e)[:80]}")
                rows.append(("redakcja", "DOI nie rozwiązuje się w rejestrze — do sprawdzenia", "", r["id"], r["DOI"]))
                continue
            diff = []
            ry = {year_of(reg)} | {str(((reg.get(k) or {}).get("date-parts") or [[None]])[0][0]) for k in ("published-print", "published-online")}
            if year_of(r) and year_of(r) not in ry:
                diff.append(f"rok {year_of(r)} (rejestr {'/'.join(sorted(y for y in ry if y != 'None'))})")
            for k, lab in (("volume", "tom"), ("issue", "numer")):
                if r.get(k) and reg.get(k) and str(r[k]) != str(reg[k]):
                    diff.append(f"{lab} {r[k]} (rejestr {reg[k]})")
            if r.get("page") and reg.get("page") and re.split(r"[-–]", str(r["page"]))[0] != re.split(r"[-–]", str(reg["page"]))[0]:
                diff.append(f"strony {r['page']} (rejestr {reg['page']})")
            flat = lambda v: " ".join(v) if isinstance(v, list) else (v or "")
            rw, gw = set(words(r.get("title"))), set(words(flat(reg.get("title")) + " " + flat(reg.get("subtitle"))))
            if rw and len(rw & gw) < 0.8 * len(rw):
                diff.append(f"tytuł (rejestr: {str(reg.get('title'))[:80]})")
            rfam = [fold(p.get("family", "")) for p in (reg.get("author") or reg.get("editor") or [])]
            if who and rfam and not any(fold(who) in f.split() or fold(who) == f for f in rfam):   # "West Ohueri", "Theo Goldberg"
                diff.append(f"autor {who} (rejestr: {', '.join(p.get('family', '') for p in (reg.get('author') or reg.get('editor')))})")
            lines.append(f"{r['id']}\t{'DIFFERS' if diff else 'OK'}\t{r['DOI']}\t{'; '.join(diff)}")
            if diff:
                rows.append(("redakcja", "dane autora różnią się od rejestru DOI — do decyzji", "", r["id"], f"DOI {r['DOI']}: " + "; ".join(diff)))
            continue
        if r.get("type") not in ("article-journal", "chapter", "book", "paper-conference", "report") or not who or not year_of(r):
            continue
        tw = words(r.get("title"))[:6]
        q = urllib.parse.urlencode({"query.bibliographic": " ".join([r.get("title", ""), r.get("container-title", ""), who, year_of(r)]),
                                    "rows": 5})
        try:
            items = json.loads(fetch("https://api.crossref.org/works?" + q, canned), strict=False)["message"]["items"]
        except Exception as e:
            lines.append(f"{r['id']}\tERROR\t\t{str(e)[:80]}")
            continue
        hit = None
        for w in items:
            wy = {str(((w.get(k) or {}).get("date-parts") or [[None]])[0][0]) for k in ("issued", "published-print", "published-online")}
            fams = [fold(p.get("family", "")) for p in (w.get("author") or w.get("editor") or [])]
            ttl = set(words(" ".join(w.get("title") or [])))
            if year_of(r) not in wy or not fams or fold(who) != fams[0] or not tw or not all(x in ttl for x in tw):
                continue
            if r["type"] == "article-journal" and any(r.get(k) and w.get(k) and re.split(r"[-–]", str(r[k]))[0] != re.split(r"[-–]", str(w[k]))[0]
                                                      for k in ("volume", "page")):
                continue
            hit = w
            break
        if hit:
            n += 1
            ev = f"{hit.get('container-title', [''])[0] if hit.get('container-title') else ''} {hit.get('volume', '')} {hit.get('page', '')}".strip()
            lines.append(f"{r['id']}\tPROPOSED\t{hit['DOI']}\tCrossref: {' '.join(hit.get('title') or [])[:70]} | {ev}")
            rows.append(("redakcja", "DOI z Crossref — do dodania (Kanon § 9.7)", "", r["id"], f"DOI: {hit['DOI']} ({ev})"))
        else:
            lines.append(f"{r['id']}\tNONE\t\t")
        if canned is None:
            import time; time.sleep(0.5)
    print("\n".join(lines))
    if a.tsv:
        open(a.tsv, "w", encoding="utf-8").write("key\tstatus\tDOI\tdetails\n" + "\n".join(lines) + "\n")
    if a.csv and rows:
        write_rows(a.csv, rows)
    bad = sum(1 for l in lines if "\tDIFFERS\t" in l or "\tNOT RESOLVED\t" in l)
    print(f"LOOKUP OK {n} proposed · {bad} to check" if n or bad else "LOOKUP NONE")
    return 0


# ------------------------------------------------------------------ imprints (Kanon § 0; MB-decisions GEN-4)
MARC = "{http://www.loc.gov/MARC21/slim}"
CATALOGUES = [   # all three answer MARC XML; name, URL builder(title words, author, year)
    ("LoC", lambda tw, au, yr: "http://lx2.loc.gov:210/LCDB?operation=searchRetrieve&version=1.1&maximumRecords=25&recordSchema=marcxml&query="
     + urllib.parse.quote(" and ".join([f'bath.title="{w}"' for w in tw[:5]] + ([f'bath.author="{au}"'] if au else [])))),
    ("DNB", lambda tw, au, yr: "https://services.dnb.de/sru/dnb?version=1.1&operation=searchRetrieve&recordSchema=MARC21-xml&maximumRecords=25&query="
     + urllib.parse.quote(" and ".join([f"tit={w}" for w in tw[:5]] + ([f"per={au}"] if au else [])))),
    ("BN", lambda tw, au, yr: "https://data.bn.org.pl/api/institutions/bibs.marcxml?limit=25&"
     + urllib.parse.urlencode({"title": " ".join(tw[:5]), **({"author": au} if au else {})})),
]


def marc_records(xml):
    from xml.etree import ElementTree as ET
    try:
        root = ET.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml)
    except ET.ParseError:
        return
    sub = lambda df, c: [s.text or "" for s in df.findall(MARC + "subfield") if s.get("code") == c]
    for rec in root.iter(MARC + "record"):
        dfs = {}
        for df in rec.findall(MARC + "datafield"):
            dfs.setdefault(df.get("tag"), []).append(df)
        imp = [d for d in dfs.get("264", []) if d.get("ind2") == "1"] or dfs.get("260", [])
        if not imp:
            continue
        f008 = next((c.text or "" for c in rec.findall(MARC + "controlfield") if c.get("tag") == "008"), "")
        f001 = next((c.text or "" for c in rec.findall(MARC + "controlfield") if c.get("tag") == "001"), "")
        t245 = dfs.get("245", [None])[0]
        yield {"title": " ".join(sub(t245, "a") + sub(t245, "b")) if t245 is not None else "", "places": sub(imp[0], "a"),
               "pubs": sub(imp[0], "b"), "date": " ".join(sub(imp[0], "c")), "y008": f008[7:11], "id": f001,
               "raw": " ".join(f"{s.get('code')}={s.text}" for s in imp[0].findall(MARC + "subfield"))}


def clean_place(p):
    """the city as on the title page: "Oxford, United Kingdom" -> Oxford, "[London]" -> London, "Kraków ;" -> Kraków"""
    p = re.sub(r"\[([^\]]*)\]", lambda m: m.group(1) if not re.search(r"\s", m.group(1)) else "", p).strip(" :;,.")
    return re.sub(r"\s*\(.*?\)\s*", " ", p).strip().split(",")[0].strip()


def clean_pub(p):
    return re.sub(r"\s*\.\.\.$", "", re.sub(r"[\[\]]", "", p)).strip(" :;,.")


def imprints(a):
    """missing place / publisher of books and chapters (not journals) from library catalogues. A record counts only
    when its title contains the work's main title words, its date is the work's year, and it agrees with any
    publisher or place refs.json already has. One value from all matching records -> proposed; several -> CONFLICT;
    none -> ?. Proposals are for the editor's approval item by item, never written into refs.json."""
    canned = json.load(open(a.canned, encoding="utf-8")) if a.canned else None
    refs = json.load(open(a.refs, encoding="utf-8"))
    out, rows = [], []
    for r in refs:
        yr = year_of(r)
        if r.get("type") in ("article-journal", "article-newspaper", "article-magazine", "webpage", "post", "post-weblog") or not yr:
            continue
        need = [f for f in ("publisher-place", "publisher") if not r.get(f) and not (f == "publisher" and int(yr) <= 1800)]
        if not need:
            continue
        chap = r.get("type") == "chapter" and r.get("container-title")
        main = re.split(r"[:;.?]", re.sub(r"<[^>]+>", "", r["container-title"] if chap else r.get("title", "")))[0]
        tw = words(main)[:6]
        au = fold(((r.get("editor") if chap else None) or r.get("author") or r.get("editor") or [{}])[0].get("family", "")).split()
        au = au[0] if au else ""
        got, ev = [], []
        for name, url in CATALOGUES:
            try:
                recs = list(marc_records(fetch(url(tw, au, yr), canned)))
            except Exception as e:
                ev.append(f"{name}: not read ({str(e)[:40]})")
                continue
            for rec in recs:
                if not all(w in words(rec["title"]) for w in tw[:5]) or (yr not in rec["date"] and rec["y008"] != yr):
                    continue
                if r.get("publisher") and r.get("type") != "thesis":
                    ours = set(words(r["publisher"])) - {"press", "university", "publishers", "books", "verlag", "wydawnictwo"}
                    if ours and not ours & set(words(" ".join(rec["pubs"]))):
                        continue
                if r.get("publisher-place") and rec["places"] and fold(clean_place(rec["places"][0])) != fold(r["publisher-place"]):
                    continue                 # another edition
                got.append((name, rec))
            if canned is None:
                import time; time.sleep(1)
        evid = " || ".join(f"{n} {g['id']}: {g['raw']}" for n, g in got[:3]) or "; ".join(ev) or "no matching record (LoC, DNB, BN)"
        for f in need:
            vals = {(clean_place(g["places"][0]) if f == "publisher-place" else clean_pub(g["pubs"][0]))
                    for _, g in got if (g["places"] if f == "publisher-place" else g["pubs"])}
            v = vals.pop() if len(vals) == 1 else ("?" if not vals else "CONFLICT: " + " / ".join(sorted(vals)))
            out.append((r["id"], f, v, evid))
            if v != "?":
                rows.append(("redakcja", ("miejsce wydania" if f == "publisher-place" else "wydawca") + " z katalogu — do zatwierdzenia",
                             "", r["id"], f"{v} ({evid[:200]})"))
    print("\n".join("\t".join(x) for x in out))
    if a.tsv:
        open(a.tsv, "w", encoding="utf-8").write("key\tfield\tvalue\tevidence\n" + "\n".join("\t".join(x) for x in out) + "\n")
    if a.csv and rows:
        write_rows(a.csv, rows)
    ok = sum(1 for x in out if x[2] != "?" and not x[2].startswith("CONFLICT"))
    print(f"LOOKUP OK {ok} of {len(out)}" if ok else "LOOKUP NONE")
    return 0


def write_rows(path, rows):
    import os
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8-sig" if new else "utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        if new:
            w.writerow(["adresat", "rodzaj", "przypis", "dzieło", "szczegóły"])
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("missing"); m.add_argument("names"); m.add_argument("year"); m.add_argument("--hint")
    m.add_argument("--note", help="source note label, for the query row"); m.add_argument("--csv"); m.add_argument("--json")
    w = sub.add_parser("webdate"); w.add_argument("url")
    ws = sub.add_parser("webdates"); ws.add_argument("refs"); ws.add_argument("--csv")
    for p in (m, w, ws):
        p.add_argument("--from-file", help="tests: read this file instead of the network")
    for name in ("dois", "imprints"):
        p = sub.add_parser(name); p.add_argument("refs"); p.add_argument("--csv"); p.add_argument("--tsv", help="evidence file")
        p.add_argument("--canned", help="tests: JSON {url substring: response} instead of the network")
    a = ap.parse_args()
    sys.exit({"missing": missing, "webdate": webdate, "webdates": webdates, "dois": dois, "imprints": imprints}[a.cmd](a))


if __name__ == "__main__":
    main()
