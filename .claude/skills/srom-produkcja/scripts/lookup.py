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
Tests: --from-file FILE replaces the network (Crossref JSON or page HTML).
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
    a = ap.parse_args()
    sys.exit({"missing": missing, "webdate": webdate, "webdates": webdates}[a.cmd](a))


if __name__ == "__main__":
    main()
