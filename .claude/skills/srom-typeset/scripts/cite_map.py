#!/usr/bin/env python3
"""
cite_map.py — author-date (Harvard/APA/Chicago-AD) references -> SROM footnote citations.

    python3 cite_map.py scan  article.md --refs refs.json [--apply out.md [--renumber]] [--report map.md]
    python3 cite_map.py audit --refs refs.json --bib original_bibliography.txt

scan   finds every author-date reference, resolves it to a refs.json key by surname(s) + year
       (+ letter suffix via the ref's "citation-label", e.g. "Kowalski 2012a"), and proposes:
         body text  "tekst (Ficowski 1985: 15)."        -> "tekst[^c1]."      [^c1]: [@ficowski1985, s. 15].
                    "(zob. Mróz 2011; Hancock 2007)"     -> one note          [^c2]: [Zob. @mroz2011; @hancock2007].
         narrative  "Ficowski (1985: 15) twierdzi"       -> "Ficowski[^c3] twierdzi"
         in a note  "Szerzej: Mróz (2011: 90)." / "Zob. Mróz 2011: 90." -> "Szerzej: [@mroz2011, s. 90]."
       Status per hit: OK · INFLECTED (Polish case form matched by stem — verify) · TRIMMED (narrative "Likewise,
       Grellmann (1807)": matched on the name after the last comma — verify) · YEAR-ONLY ("… Law and Kovats state
       … (2018, 78)": the one work of that year by authors named earlier in the paragraph, else the work cited directly
       before it if its year matches — verify) · YEAR-UNIQUE (neither: the author's only work of that year — check) ·
       YEAR-ONLY? (no such work: left unchanged, listed — a date, or convert by hand) · IN-NOTE (verify
       grammar) · NOT-CITED? (narrative "Name (year)" whose name is not a ref author, e.g. "w Warszawie
       (1920)" — left unchanged, listed) · PAGE-ONLY ("(s. 21)": converted as a citation of the work
       cited just before it, listed) · PAGE-ONLY? (no earlier citation) · AMBIGUOUS · UNKNOWN · UNPARSED.
       --apply refuses to write while any AMBIGUOUS/UNKNOWN/UNPARSED/PAGE-ONLY? hit remains; after
       checking them, --allow-unknown / --allow-unparsed release UNKNOWN / UNPARSED (those parentheses
       are then left in the text as they are). Never guesses a work (kanon §0).
audit  cross-checks refs.json (typed by hand or by Claude) against the article's ORIGINAL
       bibliography: every original entry must map to exactly one ref, and every number
       (year, volume, issue, pages, ISBN/DOI digits) and every capitalised word of the original
       must survive in the SROM rendering. Catches transcription errors in refs.json.
Last line: CITEMAP OK / CITEMAP FAIL n
"""
import argparse, json, os, re, subprocess, sys, tempfile, unicodedata
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSL = os.path.join(ROOT, "csl", "srom.csl")

UP = "A-ZŁŚŻŹĆŃÓĘĄÄÖÜÉÈÁÍÚČŠŽŘŐŰÇÑ"
NAME = rf"(?:\b(?:de|van|von|der|den|di|da|le|la|du|del|ten|ter)\s)*[{UP}][\w’'\-]+"
NAMES = rf"{NAME}(?:(?:,\s|\s(?:i|and|&|und|et)\s){NAME})*(?:\s(?:i\sin\.|et\sal\.|i\sinni|u\.\sa\.))?(?:\s\((?:red|eds?|Hrsg|oprac)\.\))?"
YEAR = r"(?:1[5-9]\d\d|20\d\d)(?:/(?:1[5-9]\d\d|20\d\d))?[a-z]?|b\.\s?d\.|n\.\s?d\.|w\sdruku|in\spress"
LOC = r"(?:[:,]\s?(?:s\.|str\.|pp?\.|S\.)?\s?[^;()\[\]]+?)?"
PREFIX = r"(?:(?i:zob\.|por\.|np\.|see|cf\.|e\.g\.|vgl\.|zob\.\steż|see\salso|cyt\.\sza|quoted\sin|cited\sin)\s)?"
ITEM = re.compile(rf"^\s*(?P<pre>{PREFIX})(?P<names>{NAMES}),?\s(?P<year>{YEAR})(?P<loc>{LOC})\s*$")
_ED = r"\((?:red|eds?|Hrsg|oprac)\.\)"
PAREN = re.compile(rf"(?<!\])\s?\(((?:[^()\[\]]|{_ED})*?(?:1[5-9]\d\d|20\d\d|b\.\s?d\.|n\.\s?d\.)(?:[^()\[\]]|{_ED})*?)\)")
NARR = re.compile(rf"(?P<names>{NAMES})\s\((?P<year>{YEAR})(?P<loc>{LOC})\)")
BARE = re.compile(rf"(?P<pre>{PREFIX})(?P<names>{NAME}(?:\s(?:i|and|&)\s{NAME})?(?:\s(?:i\sin\.|et\sal\.))?),?\s(?P<year>{YEAR})(?P<loc>(?::\s?|,\s(?=\d))[\d–\-, ]*\d(?:\s(?:i\sn\.|passim))?)?(?=[;.,)]|$)")
PREFIX_MAP = {"see": "zob.", "see also": "zob. też", "cf.": "por.", "e.g.": "np.", "vgl.": "por.",
              "quoted in": "cyt. za", "cited in": "cyt. za"}
NONPAGE = [(r"^(?:tab\.|tabl\.|table)\s?", "tabl. "), (r"^(?:fig\.|rys\.|ryc\.)\s?", "rys. "), (r"^(?:k\.|fol\.|ff?\.\s?(?=\d))\s?", "k. "),
           (r"^(?:rozdz\.|ch\.|chap\.|Kap\.)\s?", "rozdz. "), (r"^(?:przyp\.|n\.|fn\.)\s?", "przyp. ")]
CASE_SUFFIXES = sorted(["iego", "ego", "emu", "owie", "owi", "ami", "ach", "ów", "om", "em", "ej", "ie", "ą", "ę",
                        "a", "u", "y", "i", "e", "o"], key=len, reverse=True)


def fold(s):
    s = s.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").casefold()


def stem(name):
    f = fold(name)
    for suf in CASE_SUFFIXES:
        if f.endswith(suf) and len(f) - len(suf) >= 3:
            return f[:-len(suf)]
    return f


# ---------------------------------------------------------------- refs index
def primary_names(ref):
    people = ref.get("author") or ref.get("editor") or []
    out = []
    for p in people:
        fam = p.get("family") or p.get("literal") or ""
        part = p.get("non-dropping-particle", "")
        out.append((part + " " + fam).strip() if part else fam)
    return out


def as_written_names(ref):
    """the author's own form of a corrected or transliterated name (refs.json "srom-as-written": {"editor": "Van Lannep"};
    several family names in order: {"author": "Kirey; Serdyuk"}): the entry still matches the author's list and text"""
    aw = ref.get("srom-as-written") or {}
    return [n.strip() for k, v in aw.items() if k in ("author", "editor") and v for n in v.split(";") if n.strip()]


def as_written_primary(ref):
    """the author's spelling of the names a citation is made with: the authors, else the editors (as primary_names)"""
    aw = ref.get("srom-as-written") or {}
    key = "author" if ref.get("author") else "editor"
    return [n.strip() for n in (aw.get(key) or "").split(";") if n.strip()]


def ref_years(ref):
    ys = set()
    for fld in ("issued", "original-date"):
        dp = (ref.get(fld) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]:
            ys.add(str(dp[0][0]))
    return ys


def split_names(s):
    s = re.sub(r"\s\((?:red|eds?|Hrsg|oprac)\.\)$", "", s.strip())
    etal = bool(re.search(r"\s(?:i\sin\.|et\sal\.|i\sinni|u\.\sa\.)$", s))
    s = re.sub(r"\s(?:i\sin\.|et\sal\.|i\sinni|u\.\sa\.)$", "", s)
    parts = [re.sub(r"[’']s$", "", p) for p in re.split(r",\s|\s(?:i|and|&|und|et)\s", s) if p]   # Robinson’s (2000)
    return parts, etal


def resolve_narr(names_s, year_s, refs):
    """narrative "Name (year)": as resolve; if unknown, the name after the last comma alone ("Likewise, Grellmann
    (1807)", "Claiming …, Grellmann (1807)") -> TRIMMED (listed; the words before the comma are not names)"""
    st, keys = resolve(names_s, year_s, refs)
    if st == "UNKNOWN" and ", " in names_s:
        tail = names_s.rsplit(", ", 1)[1]
        st2, keys2 = resolve(tail, year_s, refs)
        if st2 in ("OK", "INFLECTED"):
            return "TRIMMED", keys2
    return st, keys


def resolve(names_s, year_s, refs):
    """-> (status, [keys])"""
    names, etal = split_names(names_s)
    yr = year_s.strip()
    letter = ""
    m = re.match(r"^(\d{4})(?:/(\d{4}))?([a-z])?$", yr)
    years = set()
    if m:
        years = {m.group(1)} | ({m.group(2)} if m.group(2) else set())
        letter = m.group(3) or ""
    nodate = not m
    exact, inflected = [], []
    for r in refs:
        pn = primary_names(r)
        if not pn:
            continue
        ry = ref_years(r)
        if nodate:
            if ry:
                continue
        elif not (ry & years):
            continue
        if etal:
            if len(pn) < 2:
                continue
            cmp_names = pn[:1]
        else:
            if len(pn) != len(names):
                continue
            cmp_names = pn
        want = names[:len(cmp_names)]
        if [fold(x) for x in cmp_names] == [fold(x) for x in want]:
            exact.append(r)
        elif [stem(x) for x in cmp_names] == [stem(x) for x in want]:
            inflected.append(r)
    if not exact and not inflected:
        # the author's spelling of a name the refs give in another form (ALA-LC "Bielikov" for the author's "Byelikov")
        for r in refs:
            aw = as_written_primary(r)
            if not aw or not (ref_years(r) & years if not nodate else not ref_years(r)):
                continue
            cmp_names = aw[:1] if etal else aw
            if (etal or len(aw) == len(names)) and [fold(x) for x in cmp_names] == [fold(x) for x in names[:len(cmp_names)]]:
                exact.append(r)
    for pool, tag in ((exact, "OK"), (inflected, "INFLECTED")):
        if letter and len(pool) > 1:
            lab = [r for r in pool if (r.get("citation-label") or "").strip().endswith(yr)]
            pool = lab if lab else pool
        if len(pool) == 1:
            return tag, [pool[0]["id"]]
        if len(pool) > 1:
            return "AMBIGUOUS", [r["id"] for r in pool]
    return "UNKNOWN", []


YEARONLY = re.compile(rf"^\s*(?P<year>{YEAR})(?P<loc>{LOC})\s*$")


WHY = {"YEAR-ONLY": "author named before it, or the work cited directly before it",
       "YEAR-UNIQUE": "the author's only work of that year; the work cited before it is another — check"}


def resolve_context(before, year_s, refs, prev_key=None, has_loc=False):
    """"(2018, 78)" with no name (Kanon § 7.1), in this order:
    1. the work of that year whose author(s) are named earlier in the same paragraph or note ("Ian Law and Martin
       Kovats state that … (2018, 78)"): all the ref's family names (the first, for four or more) occur there; of
       several, the one named last -> YEAR-ONLY
    2. the work cited directly before it (prev_key), if its year is that year -> YEAR-ONLY
    3. the author's only work of that year in refs.json -> YEAR-UNIQUE (listed: the work cited before it is
       another, or there is none)
    4. none -> YEAR-ONLY? (left in the text, listed)                                   -> (status, [keys])
    Steps 2-3 only with a locator ("(1992, 81)"): a bare "(1991)" is a date unless step 1 finds its author."""
    m = re.match(r"^(\d{4})", year_s.strip())
    if not m:
        return "YEAR-ONLY?", []
    st, keys = _named_before(before, m.group(1), refs)
    if st != "YEAR-ONLY?":
        return st, keys
    if not has_loc:                 # a bare "(1991)" in running text is a date unless its author is named (step 1)
        return "YEAR-ONLY?", []
    byid = {r["id"]: r for r in refs}
    if prev_key in byid and m.group(1) in ref_years(byid[prev_key]):
        return "YEAR-ONLY", [prev_key]
    same = [r["id"] for r in refs if m.group(1) in ref_years(r) and not r.get("srom-added")]
    if len(same) == 1:
        return "YEAR-UNIQUE", same
    return "YEAR-ONLY?", []


def _named_before(before, year, refs):
    words = [(w.start(), fold(re.sub(r"[’']s$", "", w.group(0)))) for w in re.finditer(r"[^\W\d_][\w’'\-]*", before)]
    cands = []
    for r in refs:
        if year not in ref_years(r):
            continue
        for names in (primary_names(r), as_written_primary(r)):
            need = [fold(n) for n in (names[:1] if len(names) >= 4 else names)]
            if not need:
                continue
            pos = [max((p for p, w in words if w == n), default=-1) for n in need]
            if min(pos) >= 0:
                cands.append((max(pos), r["id"]))
                break
    if not cands:
        return "YEAR-ONLY?", []
    cands.sort(reverse=True)
    if len(cands) > 1 and cands[0][0] == cands[1][0]:
        return "AMBIGUOUS", [k for _, k in cands]
    return "YEAR-ONLY", [cands[0][1]]


def locator(loc):
    loc = (loc or "").strip()
    loc = re.sub(r"^[:,]\s?", "", loc)
    if not loc:
        return ""
    for rx, lab in NONPAGE:
        if re.match(rx, loc):
            return "{" + re.sub(rx, lab, loc).strip() + "}"
    loc = re.sub(r"^(?:s\.|str\.|pp?\.|S\.)\s?", "", loc)
    loc = re.sub(r"\s?ff?\.$", " i n.", loc)
    loc = re.sub(r"(?<=\d)-(?=\d)", "–", loc)
    return "s. " + loc


def cite_body(items, capitalise):
    parts = []
    for n, (pre, key, loc) in enumerate(items):
        pre = PREFIX_MAP.get(pre.strip().lower(), pre.strip()) if pre else ""   # "See also" at a note start
        if n == 0 and capitalise and pre:
            pre = pre[0].upper() + pre[1:]
        parts.append(((pre + " ") if pre else "") + "@" + key + ((", " + loc) if loc else ""))
    return "[" + "; ".join(parts) + "]"


# ---------------------------------------------------------------- scan
class Hit:
    def __init__(self, where, orig, status, keys, repl, detail=""):
        self.where, self.orig, self.status, self.keys, self.repl, self.detail = where, orig, status, keys, repl, detail


def parse_items(content, refs):
    items, statuses, cands = [], [], []
    for raw in re.split(r";\s?", content):
        m = ITEM.match(raw)
        if not m:
            return None, ["UNPARSED"], [raw]
        st, keys = resolve(m.group("names"), m.group("year"), refs)
        statuses.append(st)
        cands.append(keys)
        items.append((m.group("pre"), keys[0] if len(keys) == 1 else "?", locator(m.group("loc"))))
    return items, statuses, cands


def worst(statuses):
    for s in ("UNPARSED", "UNKNOWN", "AMBIGUOUS", "INFLECTED", "TRIMMED", "YEAR-UNIQUE", "YEAR-ONLY", "OK"):
        if s in statuses:
            return s
    return "OK"


def scan(md_text, refs):
    lines = md_text.split("\n")
    labels = set(re.findall(r"\[\^([^\]\s]+)\]", md_text))
    counter = [0]

    def new_label():
        while True:
            counter[0] += 1
            lab = f"c{counter[0]}"
            if lab not in labels:
                labels.add(lab)
                return lab

    hits, out = [], []
    last_key = [None]          # last work cited in the main text so far (page-only "(s. 21)" refers to it)
    in_bib = False
    prev_para = [""]            # a block quotation's source is named in the paragraph that leads into it
    before_marker = {}          # note label -> the work cited in the text just before its marker
    for ln_no, line in enumerate(lines, 1):
        if line.strip() and not line.startswith(("[^", ":::", "#", ">")):
            prev_para[0] = line
        if line.startswith("::: {#bibliografia}"):
            in_bib = True
        if in_bib:
            out.append(line)
            if line.strip() == ":::":
                in_bib = False
            continue
        mnote = re.match(r"^(\[\^[^\]\s]+\]:\s?)(.*)$", line)
        if line.startswith("#") or not line.strip():
            out.append(line)
            continue
        new_defs = []
        if mnote:
            head, text = mnote.group(1), mnote.group(2)
            where = f"line {ln_no} (note {head.strip()[2:-2]})"

            def note_paren(m):
                content = m.group(1)
                items, sts, cands = parse_items(content, refs)
                y = YEARONLY.match(content) if items is None else None
                if y:
                    st, keys = resolve_context(text[:m.start()], y.group("year"), refs, before_marker.get(head.strip()[2:-2]),
                                              bool(y.group("loc")))
                    if st not in ("YEAR-ONLY", "YEAR-UNIQUE"):
                        hits.append(Hit(where, m.group(0).strip(), st, keys, None,
                                        "year without a name: no single work of that year by an author named earlier in the note — left unchanged"))
                        return m.group(0)
                    rep = " " + cite_body([("", keys[0], locator(y.group("loc")))], False)
                    hits.append(Hit(where, m.group(0).strip(), st, keys, rep.strip(), WHY[st]))
                    return rep
                if items is None:
                    if ITEM_HINT.search(content):
                        hits.append(Hit(where, m.group(0).strip(), "UNPARSED", [], None))
                    return m.group(0)
                if "UNKNOWN" in sts or "AMBIGUOUS" in sts:
                    hits.append(Hit(where, m.group(0).strip(), worst(sts), [k for c in cands for k in c], None, "left unchanged"))
                    return m.group(0)
                st = worst(sts + ["IN-NOTE"]) if worst(sts) == "OK" else worst(sts)
                rep = " " + cite_body(items, False)
                hits.append(Hit(where, m.group(0).strip(), st, [k for c in cands for k in c], rep.strip()))
                return rep

            def note_narr(m):
                st, keys = resolve_narr(m.group("names"), m.group("year"), refs)
                if st == "UNKNOWN":
                    hits.append(Hit(where, m.group(0), "NOT-CITED?", [], None, "name not in refs.json — left unchanged"))
                    return m.group(0)
                rep = cite_body([("", keys[0] if len(keys) == 1 else "?", locator(m.group("loc")))], False)
                hits.append(Hit(where, m.group(0), "IN-NOTE" if st == "OK" else st, keys, rep))
                return rep

            def note_bare(m):
                st, keys = resolve(m.group("names"), m.group("year"), refs)
                if st == "UNKNOWN":
                    return m.group(0)          # not an author-date cite (e.g. "Kraków 1985" in a full citation)
                at_start = m.start() == 0 or re.search(r"[.!?]\s*$", m.string[:m.start()]) is not None   # sentence start
                rep = cite_body([(m.group("pre"), keys[0] if len(keys) == 1 else "?", locator(m.group("loc")))], at_start)
                hits.append(Hit(where, m.group(0), "IN-NOTE" if st == "OK" else st, keys, rep))
                return rep

            text = NARR.sub(note_narr, text)
            text = PAREN.sub(note_paren, text)
            text = BARE.sub(note_bare, text)
            text = re.sub(r"\]\s?\.\s?\.$", "].", text)
            out.append(head + text)
            continue

        where = f"line {ln_no}"

        def body_narr(m):
            st, keys = resolve_narr(m.group("names"), m.group("year"), refs)
            if st == "UNKNOWN":
                # "w Warszawie (1920)", "Konferencja w Genewie (1971)": not a citation unless the name is a ref author
                hits.append(Hit(where, m.group(0), "NOT-CITED?", [], None, "name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json"))
                return m.group(0)
            lab = new_label()
            body = cite_body([("", keys[0] if len(keys) == 1 else "?", locator(m.group("loc")))], True)
            hits.append(Hit(where, m.group(0), st, keys, f"{m.group('names')}[^{lab}]", f"[^{lab}]: {body}."))
            new_defs.append(f"[^{lab}]: {body}.")
            return f"{m.group('names')}[^{lab}]"

        def body_paren(m):
            content = m.group(1)
            items, sts, cands = parse_items(content, refs)
            y = YEARONLY.match(content) if items is None else None
            if y:
                ctx = (prev_para[0] + "\n" if line.startswith(">") else "") + line[:m.start()]
                st, keys = resolve_context(ctx, y.group("year"), refs, last_key[0], bool(y.group("loc")))
                if st not in ("YEAR-ONLY", "YEAR-UNIQUE"):
                    hits.append(Hit(where, m.group(0).strip(), st, keys, None,
                                    "year without a name: no single work of that year by an author named earlier in the paragraph — left unchanged"))
                    return m.group(0)
                lab = new_label()
                body = cite_body([("", keys[0], locator(y.group("loc")))], True)
                hits.append(Hit(where, m.group(0).strip(), st, keys, f"[^{lab}]", f"[^{lab}]: {body}. ({WHY[st]})"))
                new_defs.append(f"[^{lab}]: {body}.")
                return f"[^{lab}]"
            if items is None:
                if ITEM_HINT.search(content):
                    hits.append(Hit(where, m.group(0).strip(), "UNPARSED", [], None))
                return m.group(0)
            if "UNKNOWN" in sts or "AMBIGUOUS" in sts:
                hits.append(Hit(where, m.group(0).strip(), worst(sts), [k for c in cands for k in c], None,
                                "left unchanged — add the work to refs.json (or --allow-unknown if it is not a citation)"))
                return m.group(0)
            lab = new_label()
            body = cite_body(items, True)
            hits.append(Hit(where, m.group(0).strip(), worst(sts), [k for c in cands for k in c], f"[^{lab}]", f"[^{lab}]: {body}."))
            new_defs.append(f"[^{lab}]: {body}.")
            return f"[^{lab}]"


        def body_paren_tracked(m):
            r = body_paren(m)
            if hits and hits[-1].where == where and hits[-1].keys and hits[-1].status in ("OK", "INFLECTED", "TRIMMED", "YEAR-ONLY", "YEAR-UNIQUE"):
                last_key[0] = hits[-1].keys[-1]
            return r

        def body_pageonly(m):
            loc = locator((m.group("loc") or m.group("loc2") or "").strip())
            if not last_key[0]:
                hits.append(Hit(where, m.group(0).strip(), "PAGE-ONLY?", [], None, "no earlier citation to refer to — resolve by hand"))
                return m.group(0)
            lab = new_label()
            body = cite_body([("", last_key[0], loc)], True)
            hits.append(Hit(where, m.group(0).strip(), "PAGE-ONLY", [last_key[0]], f"[^{lab}]",
                            f"[^{lab}]: {body}. (the work cited just before it)"))
            new_defs.append(f"[^{lab}]: {body}.")
            return f"[^{lab}]"

        def body_narr_tracked(m):
            r = body_narr(m)
            if hits[-1].keys and hits[-1].status in ("OK", "INFLECTED", "TRIMMED"):
                last_key[0] = hits[-1].keys[-1]
            return r

        # one pass in reading order, so labels c1, c2 … and "page-only follows last work" follow the text
        pieces, pos = [], 0
        handlers = ((NARR, body_narr_tracked), (PAREN, body_paren_tracked), (PAGEONLY, body_pageonly))
        while True:
            best = None
            for rx, fn in handlers:
                m = rx.search(line, pos)
                if m and (best is None or m.start() < best[0].start()):
                    best = (m, fn)
            if not best:
                break
            m, fn = best
            for lab in re.findall(r"\[\^([^\]\s]+)\]", line[pos:m.start()]):
                before_marker[lab] = last_key[0]
            pieces.append(line[pos:m.start()])
            pieces.append(fn(m))
            pos = m.end()
        for lab in re.findall(r"\[\^([^\]\s]+)\]", line[pos:]):
            before_marker[lab] = last_key[0]
        pieces.append(line[pos:])
        new = "".join(pieces)
        new = re.sub(r"(?<=\.)(\[\^c\d+\])\.", r"\1", new)      # "XV w. (A 1985)." -> "XV w.[^c1]"
        # safety sweep: any parenthesis still holding Name + year is an unconverted reference
        for seg in paren_segments(new):
            if ITEM_HINT.search(seg) and not any(h.where == where and h.orig == seg.strip() for h in hits):
                hits.append(Hit(where, seg, "UNPARSED", [], None, "left in text — convert by hand or confirm it is not a reference"))
        out.append(new)
        for d in new_defs:
            out += ["", d]
    return hits, "\n".join(out)


PAGEONLY = re.compile(r"\s?\((?:(?:s\.|str\.|pp?\.)\s?(?P<loc>[\d–\-, ]+(?:\s?ff?\.)?)|\*?(?i:ibid\.?|ibidem|tamże|tamze)\*?\.?\*?(?:[,:]\s?(?:s\.|pp?\.)?\s?(?P<loc2>[\d–\-, ]+))?)\)")   # (*Ibid.*, 2, 21)
ITEM_HINT = re.compile(rf"[{UP}][\w’'\-]+,?\s(?:\([^()]*\)\s)?(?:1[5-9]\d\d|20\d\d)")




def paren_segments(text):
    """top-level (…) segments, one level of nesting allowed; skips [^…] markers and [@…] cites"""
    segs, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
            if depth == 0:
                segs.append(text[start:i + 1])
    return segs


def write_report(hits, path):
    rows = ["# cite_map report", "", "| # | where | original | status | key(s) | becomes |", "|---|---|---|---|---|---|"]
    for i, h in enumerate(hits, 1):
        rows.append(f"| {i} | {h.where} | `{h.orig}` | **{h.status}** | {', '.join(h.keys) or '—'} | "
                    f"`{h.repl or 'unchanged'}`{(' + `' + h.detail + '`') if h.detail else ''} |")
    c = Counter(h.status for h in hits)
    rows += ["", "Totals: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items()))]
    open(path, "w", encoding="utf-8").write("\n".join(rows) + "\n")


# ---------------------------------------------------------------- audit
def render_bib(refs_path, keys):
    d = tempfile.mkdtemp()
    md = os.path.join(d, "b.md")
    open(md, "w", encoding="utf-8").write("---\nlang: pl-PL\nnocite: '" + ", ".join("@" + k for k in keys) + "'\n---\n\nX\n")
    r = subprocess.run(["pandoc", md, "--citeproc", "--csl", CSL, "--bibliography", refs_path, "-t", "plain", "--wrap=none"],
                       capture_output=True, text=True)
    return r.stdout


STOP = {"In", "W", "Red", "Eds", "Ed", "Hrsg", "Vol", "No", "Nr", "Pp", "S", "The", "A", "An", "And", "Of", "Und",
        "Der", "Die", "Das", "La", "Le", "Les", "Et", "Trans", "Transl", "Translated", "Tłum", "Edited", "By", "Accessed", "Retrieved",
        "Available", "Dostęp", "Online", "Doi", "Isbn", "Http", "Https", "Www", "Press",
        "Tome", "Tomo", "Tom", "Volume", "Band", "Bd", "Teil"}           # volume labels: rendered as "t."
MONTHS = {fold(m) for m in ("January February March April May June July August September October November December "
                            "janvier février mars avril mai juin juillet août septembre octobre novembre décembre "
                            "Januar Februar März Juni Juli Oktober Dezember").split()}


def expand_ranges(s):
    """abbreviated page ranges as English sources write them: 110–24 -> 110–124, for comparing numbers
    (Kanon § 3.2: ranges in full)"""
    def f(m):
        a, b = m.group(1), m.group(2)
        if len(b) < len(a):
            full = a[:len(a) - len(b)] + b
            if int(full) > int(a):
                return f"{a}–{full}"
        return m.group(0)
    return re.sub(r"(?<!\d)(?<!\d\.)(\d{2,5})[-–](\d{1,4})(?!\d|\.\d)", f, s)


def tokens(s):
    s = unicodedata.normalize("NFC", s)          # a PDF text layer may give "á" as a + combining accent
    s = re.sub(r"https?://\S+", " ", s)
    nums = Counter(int(n) for n in re.findall(r"\d+", re.sub(r"(?<=\d)[-–](?=\d)", " ", expand_ranges(s))))
    words = {fold(w) for w in re.findall(rf"[{UP}][\w’'\-]{{2,}}", s) if w.split("-")[0].capitalize() not in STOP}
    return nums, words


def audit(refs_paths, bib_path):
    refs = []
    for rp in refs_paths:
        refs += json.load(open(rp, encoding="utf-8"))
    refs_path = os.path.join(tempfile.mkdtemp(), "refs.json")
    json.dump(refs, open(refs_path, "w", encoding="utf-8"), ensure_ascii=False)
    lines = [l.strip() for l in open(bib_path, encoding="utf-8") if l.strip()]
    problems, used = [], Counter()
    for ln in lines:
        m = re.match(rf"^(?:[-–•*]\s)?({NAME})", ln)
        ym = re.search(rf"\b({YEAR})\b", ln)
        cand = []
        if m:
            nm = fold(m.group(1).rstrip(","))
            cand = [r for r in refs if not r.get("srom-added") and primary_names(r) and fold(primary_names(r)[0]) == nm]
        if not cand:
            # family names of more than one word (Touam Bona, Park Hong), a capitalised particle (Van Lannep),
            # a literal author (M. W., M. A.): the entry starts with the whole name
            fl = fold(re.sub(r"^[-–•*]\s", "", ln))
            cand = [r for r in refs if not r.get("srom-added") and any(
                    re.match(re.escape(fold(n)) + r"[,.\s]", fl) for n in primary_names(r)[:1] + as_written_names(r))]
        if cand:
            if ym and len(cand) > 1:
                y = ym.group(1)[:4]
                cand = [r for r in cand if y in ref_years(r)] or cand
            if len(cand) > 1:
                t = fold(ln)
                cand = [r for r in cand if fold(r.get("title", ""))[:25] in t] or cand
        if len(cand) != 1:
            problems.append(f"original entry not mapped to exactly one ref ({len(cand)}): {ln[:90]}")
            continue
        r = cand[0]
        used[r["id"]] += 1
        rendered = render_bib(refs_path, [r["id"]])
        on, ow = tokens(ln)
        rn, rw = tokens(rendered + " " + json.dumps(r, ensure_ascii=False))
        miss_n = on - rn
        miss_w = sorted(ow - rw)
        dp = ((r.get("issued") or {}).get("date-parts") or [[]])[0]
        if len(dp) >= 2:                   # the month is in the date; its name is rendered in Polish
            miss_w = [w for w in miss_w if w not in MONTHS]
        if miss_n or miss_w:
            problems.append(f"{r['id']}: in original but not in ref/rendering — numbers {dict(miss_n) or '—'}, words {miss_w or '—'}\n"
                            f"      original: {ln}\n      SROM:     {rendered.strip()}")
    for r in refs:
        if r.get("srom-added"):
            if not str(r.get("srom-source", "")).strip():
                problems.append(f"{r['id']}: added by the translation (srom-added) but has no srom-source (catalogue URL or verified ISBN)")
            continue
        if used[r["id"]] == 0:
            problems.append(f"{r['id']}: in refs.json but no matching original entry (added? or entry missing from bibliography)")
        elif used[r["id"]] > 1:
            problems.append(f"{r['id']}: matched by {used[r['id']]} original entries")
    return problems


def renumber(md):
    """author's notes and converted ones (1, c1, c2, m1 …) -> 1…N in the order of their markers in the text; the
    definitions after each paragraph in that order. Translator/editorial labels (t…, r…) are left alone.
    -> (text, {old: new})"""
    NOTE_DEF = re.compile(r"^\[\^([^\]\s]+)\]:")
    lines = md.split("\n")
    order = []
    for ln in lines:
        body = ln if not NOTE_DEF.match(ln) else ln[NOTE_DEF.match(ln).end():]
        for lab in re.findall(r"\[\^([^\]\s]+)\]", body):
            if not re.match(r"^[tr]\d", lab) and lab not in order:
                order.append(lab)
    mp = {old: str(i) for i, old in enumerate(order, 1)}
    tok = lambda m: f"[^\x00{mp[m.group(1)]}]" if m.group(1) in mp else m.group(0)
    out = [re.sub(r"\[\^([^\]\s]+)\]", tok, ln).replace("\x00", "") for ln in lines]
    # definitions after a paragraph: blocks of "[^n]: …" (+ indented continuation lines) separated by blank lines
    res, i = [], 0
    while i < len(out):
        if NOTE_DEF.match(out[i]):
            blocks = []
            while i < len(out) and (NOTE_DEF.match(out[i]) or (not out[i].strip() and i + 1 < len(out)
                                    and (NOTE_DEF.match(out[i + 1]) or out[i + 1].startswith("    ")))
                                    or out[i].startswith("    ")):
                if NOTE_DEF.match(out[i]):
                    blocks.append([out[i]])
                elif out[i].strip():
                    blocks[-1].append(out[i])
                i += 1
            key = lambda b: int(NOTE_DEF.match(b[0]).group(1)) if NOTE_DEF.match(b[0]).group(1).isdigit() else 10 ** 6
            for j, b in enumerate(sorted(blocks, key=key)):
                if j:
                    res.append("")
                res.extend(b)
            continue
        res.append(out[i])
        i += 1
    return "\n".join(res), mp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "audit"])
    ap.add_argument("md", nargs="?")
    ap.add_argument("--refs", required=True, action="append", help="repeat for srom-tlumacz's <id>_refs_tlum.json")
    ap.add_argument("--apply")
    ap.add_argument("--report")
    ap.add_argument("--bib")
    ap.add_argument("--allow-unknown", action="store_true",
                    help="apply even with UNKNOWN parentheses (left unchanged) after confirming they are not citations")
    ap.add_argument("--allow-unparsed", action="store_true",
                    help="apply even with UNPARSED hits (after checking each one in the report)")
    ap.add_argument("--renumber", action="store_true",
                    help="with --apply: notes labelled 1…N in the order of their markers (a frozen source's labels = the printed numbers)")
    a = ap.parse_args()
    if a.cmd == "audit":
        probs = audit(a.refs, a.bib)
        for p in probs:
            print("PROBLEM " + p)
        print("CITEMAP OK" if not probs else f"CITEMAP FAIL {len(probs)}")
        sys.exit(1 if probs else 0)
    refs = [r for rp in a.refs for r in json.load(open(rp, encoding="utf-8"))]
    hits, new = scan(open(a.md, encoding="utf-8").read(), refs)
    rep = a.report or os.path.splitext(a.md)[0] + "_citemap.md"
    write_report(hits, rep)
    c = Counter(h.status for h in hits)
    for h in hits:
        if h.status not in ("OK",):
            print(f"{h.status:9} {h.where}: {h.orig}  ->  {h.repl or 'unchanged'}  {h.keys}")
    blocking = c["AMBIGUOUS"] + (0 if a.allow_unknown else c["UNKNOWN"]) + (0 if a.allow_unparsed else c["UNPARSED"]) + c["PAGE-ONLY?"]
    print(f"hits: {len(hits)} · " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) + f" · report: {rep}")
    if a.apply:
        if blocking:
            print(f"CITEMAP FAIL {blocking} — not applied (resolve AMBIGUOUS/UNKNOWN/UNPARSED/PAGE-ONLY? first)")
            sys.exit(1)
        if a.renumber:
            new, mp = renumber(new)
            print(f"renumbered: {len(mp)} notes, 1–{len(mp)} in marker order"
                  + (f" (author's notes: {', '.join(f'{k}→{v}' for k, v in mp.items() if k.isdigit())})" if mp else ""))
        open(a.apply, "w", encoding="utf-8").write(new)
        print(f"written {a.apply}")
    print("CITEMAP OK" if not blocking else f"CITEMAP FAIL {blocking}")
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
