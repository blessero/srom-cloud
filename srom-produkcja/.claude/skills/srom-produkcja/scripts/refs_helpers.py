#!/usr/bin/env python3
"""Shared by every text's refs.py (new rips import this instead of pasting P, Y, book, chap, art) and by build.py,
check.py and cite_map.py (the lint). A helper never puts a null (None) into a record: pandoc stops on one with
"expected String or Number, but encountered Null" and no key.

    sys.path.insert(0, "<...>/srom-produkcja/scripts"); from refs_helpers import P, Y, book, chap, art, short, written
    book("wolfe2016", [P("Wolfe", "Patrick")], "Traces of History", "Verso", "London", 2016)
    short("kaps", [P("Kaps")], "Differences", type="article-journal")      # short form only -> [BRAK …] placeholders
    written(book(...), editor="Van Lannep")                                  # srom-as-written next to the corrected field

    python3 refs_helpers.py refs.json [more.json]     # the lint alone: `refs.json: <id>.<field> is null`, exit 1 on any
"""
import json, os, sys


def clean(d):
    """the record without its None values"""
    return {k: v for k, v in d.items() if v is not None}


def P(family, given=None, **kw):
    return clean({"family": family, "given": given, **kw})


def Y(*a):
    """CSL date; None parts are dropped. With no part left it raises (a null date would stop pandoc with no key):
    guard an unknown year with `if year`, as book(), chap() and art() do"""
    parts = [x for x in a if x is not None]
    if not parts:
        raise ValueError("Y() needs at least one date part")
    return {"date-parts": [parts]}


def book(id, au, title, pub, place, year, ed=None, **kw):
    return clean({"id": id, "type": "book", "title": title, "issued": Y(year) if year else None, "author": au or None,
                  "editor": ed or None, "publisher": pub or None, "publisher-place": place or None, **kw})


def chap(id, au, title, cont, eds, pub, place, year, page=None, **kw):
    return clean({"id": id, "type": "chapter", "title": title, "container-title": cont, "issued": Y(year) if year else None,
                  "page": page or None, "author": au or None, "editor": eds or None, "publisher": pub or None,
                  "publisher-place": place or None, **kw})


def art(id, au, title, journal, vol, year, page=None, issue=None, **kw):
    return clean({"id": id, "type": "article-journal", "title": title, "container-title": journal or None,
                  "issued": Y(year) if year else None, "author": au or None, "volume": vol or None, "issue": issue or None,
                  "page": page or None, **kw})


def short(id, au, title, type="book", **kw):
    """a work the author cites by a short form only (no place, publisher, year given): the record carries the author,
    the title and `title-short` and leaves those fields out, so the build prints [BRAK MIEJSCA], [BRAK WYDAWCY] and
    [BRAK ROKU] and puts the work into the query sheet. Nothing is guessed. type "article-journal" for a journal item."""
    kw.setdefault("title-short", title)
    return clean({"id": id, "type": type, "title": title, "author": au or None, **kw})


def written(rec, **forms):
    """the form the author's note used for a field that refs.json corrects, kept next to the corrected field:
    written(book(...), author="Wolf", title="Traces")  ->  rec["srom-as-written"] == {"author": "Wolf", "title": "Traces"}.
    author / editor hold family names only, several separated by ';' (srom-md.md). None and empty forms are dropped;
    an existing srom-as-written is extended, not replaced. Returns rec."""
    aw = dict(rec.get("srom-as-written") or {})
    aw.update({k: v for k, v in forms.items() if v})
    if aw:
        rec["srom-as-written"] = aw
    return rec


def lint_refs(items, name="refs.json"):
    """every null anywhere in a CSL-JSON list, one message each: `refs.json: <id>.<field> is null`
    (a nested one as `<id>.author[0].given`, `<id>.issued.date-parts[0][0]`)"""
    out = []

    def walk(x, path, rid):
        if x is None:
            out.append(f"{name}: {rid}.{path} is null")
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}" if path else k, rid)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]", rid)

    for n, r in enumerate(items):
        rid = r.get("id") if isinstance(r, dict) and r.get("id") else f"#{n + 1}"
        if isinstance(r, dict):
            for k, v in r.items():
                walk(v, k, rid)
        else:
            out.append(f"{name}: {rid} is not a record")
    return out


def lint_files(paths):
    """lint_refs over one or more files"""
    out = []
    for p in paths or []:
        out += lint_refs(json.load(open(p, encoding="utf-8")), os.path.basename(p))
    return out


if __name__ == "__main__":
    probs = lint_files(sys.argv[1:])
    for p in probs:
        print("ERROR " + p)
    print("REFS OK" if not probs else f"REFS FAIL {len(probs)}")
    sys.exit(1 if probs else 0)
