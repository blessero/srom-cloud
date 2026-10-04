#!/usr/bin/env python3
"""tlumacz-draft_check.py — checks of a translation draft in work/<id>/ (leaf 1.4.2a; replaces the per-article copies).

  tlumacz-draft_check.py <id> [--leftover] [--marks] [--quotes]   (no flag = all three)
  tlumacz-draft_check.py --all          every work/<id>/ that has <id>_pl.md
  tlumacz-draft_check.py --selftest     negative controls on temporary copies

--leftover  English function words left in the Polish text: body paragraphs and the title-note block (::: …),
            notes excluded (they keep the author's originals). Italics, <!-- comments -->, [@citation] tokens and
            capitalised multi-word names (institutions, projects, journals: kept in the original) are removed first.
            16 words, case-insensitive (the strictest of the old copies).
--marks     "DO SPRAWDZENIA: S<n>" in <id>_pl.md = "- S<n>" lines in <id>_uwagi.md (the notes sheet is the only
            lasting record: comments leave the text after the Word round trip).
--quotes    <id>_quotes.tsv, if present (PLAN OUT-QUOTES): classes valid; every quotation of 4+ words in the source
            (“…” span not in title case, assigned to the next note marker;
            block quotation: its own marker, else the next paragraph's first) has a row naming its note ("n. <label>");
            every row whose status is open names an S-item, e.g. "open (S2)", that exists in the text and the sheet.
Output per article: "DRAFT <id>: leftover n, marks a=b, quotes x/y (c bad class, o open rows unmatched)" or "quotes –".
Exit 1 if any check fails. The draft is read, never written.
"""
import os, re, sys, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlumacz_paths import MODULE   # the module folder that holds work/<id>/
WORDS = r"(?i)\b(the|and|of|with|which|that|this|from|were|was|is|for|not|but|have|had)\b"
# a capitalised word followed by more capitalised words or connectors: "Detroit Institute of Arts",
# "Rivals of the Past, Children of the Future", "The Author(s)" — institution, project and journal names stay in the original
NAME = r"\b[A-Z][\w’'().:-]*(?:,?\s+(?:of|and|the|for|on|in|[A-Z][\w’'().:-]*))+"
CLASSES = {"PL-EDITION", "PL-ORIGINAL", "THIRD-LANG", "EN-NO-PL", "VERSE"}

def rd(p): return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def leftover(pl):
    body = pl.split("\n---\n", 1)[1] if pl.startswith("---") else pl
    body = re.sub(r"^:::\s*\S.*$|^:::\s*$", "", body, flags=re.M)          # keep the title-note text, drop fences
    paras = [p for p in body.split("\n\n") if p.strip() and not p.lstrip().startswith("[^")]
    hits = []
    for p in paras:
        t = re.sub(r"<!--.*?-->", " ", p, flags=re.S)
        t = re.sub(r"\[@[^\]]*\]", " ", t)
        t = re.sub(r"\*[^*]+\*", " ", t)
        t = re.sub(NAME, " ", t)                                             # names and titles kept in the original
        hits += [t[max(0, m.start() - 40):m.end() + 40].replace("\n", " ") for m in re.finditer(WORDS, t)]
    return hits

def marks(pl, uw):
    a = set(re.findall(r"DO SPRAWDZENIA: (S\d+)", pl))
    b = set(re.findall(r"^- (S\d+)\b", uw or "", re.M))
    return a, b

def is_title(q):
    """A quoted span in title case (most words capitalised) is a title, not a quotation to re-source."""
    w = [x for x in re.findall(r"[^\W\d_][\w’'-]*", q) if x.lower() not in ("of", "the", "and", "in", "on", "a", "an", "for", "to", "–")]
    return bool(w) and sum(x[0].isupper() for x in w) / len(w) >= 0.6

def quoted_notes(src):
    labels, block = set(), []
    for para in [p for p in src.split("\n\n") if p.strip()] + [""]:
        m = re.match(r"\[\^(\w+)\]:", para)
        if m:
            if any(len(q.split()) >= 4 and not is_title(q) for q in re.findall(r"“([^”]*)”", para)):
                labels.add(m.group(1))
            continue
        if para.startswith(">"): block.append(para); continue
        if block:                                  # a block quotation: its own marker, else the next paragraph's first
            nm = re.search(r"\[\^(\w+)\]", " ".join(block)) or re.search(r"\[\^(\w+)\]", para)
            if nm: labels.add(nm.group(1))
            block = []
        for q in re.finditer(r"“([^”]*)”", para):
            if len(q.group(1).split()) >= 4 and not is_title(q.group(1)):
                nm = re.search(r"\[\^(\w+)\]", para[q.end():])
                if nm: labels.add(nm.group(1))
    return labels

def check(aid, root=MODULE, want=("leftover", "marks", "quotes"), quiet=False):
    d = os.path.join(root, "work", aid)
    pl, uw = rd(os.path.join(d, f"{aid}_pl.md")), rd(os.path.join(d, f"{aid}_uwagi.md"))
    ok, parts = True, []
    if "leftover" in want:
        h = leftover(pl); ok &= not h; parts.append(f"leftover {len(h)}")
        if not quiet: [print("  …" + x + "…") for x in h]
    a, b = marks(pl, uw)
    if "marks" in want:
        ok &= a == b; parts.append(f"marks {len(a)}={len(b)}" if a == b else f"marks {len(a)}≠{len(b)}")
        if a != b and not quiet: print("  only in text:", sorted(a - b), "only in notes sheet:", sorted(b - a))
    if "quotes" in want:
        qs, src = rd(os.path.join(d, f"{aid}_quotes.tsv")), rd(os.path.join(d, "src", f"{aid}_src.md"))
        if qs is None: parts.append("quotes –")
        else:
            rows = [l.split("\t") for l in qs.splitlines()[1:] if l.strip()]
            sheet = set()
            for r in rows:                                   # "n. 12", "n. 71, 75", "n. 83–84"
                for part in re.findall(r"n\. ([\d,–\- ]+)", r[1]):
                    for x in re.findall(r"\d+(?:[–-]\d+)?", part):
                        a1, _, b1 = x.replace("–", "-").partition("-")
                        sheet |= {str(n) for n in range(int(a1), int(b1 or a1) + 1)}
            found = quoted_notes(src or "")
            bad = [r[0] for r in rows if r[3] not in CLASSES]
            opn = [r for r in rows if r[5].startswith("open")]
            unmatched = [r[0] for r in opn if not (set(re.findall(r"S\d+", r[5])) and set(re.findall(r"S\d+", r[5])) <= (a & b))]
            miss = found - sheet
            ok &= not (miss or bad or unmatched)
            parts.append(f"quotes {len(found & sheet)}/{len(found)} ({len(bad)} bad class, {len(unmatched)} open rows unmatched)")
            if not quiet:
                if miss: print("  quotation notes missing from the sheet:", sorted(miss, key=lambda x: (len(x), x)))
                if bad: print("  bad class:", bad)
                if unmatched: print("  open rows without a matching S-item:", unmatched)
    print(f"DRAFT {aid}: " + ", ".join(parts))
    return ok

def ids(root=MODULE):
    w = os.path.join(root, "work")
    return sorted(x for x in os.listdir(w) if os.path.exists(os.path.join(w, x, f"{x}_pl.md")))

def selftest():
    def planted(aid, fn, change):
        tmp = tempfile.mkdtemp(); d = os.path.join(tmp, "work", aid)
        shutil.copytree(os.path.join(MODULE, "work", aid), d, ignore=shutil.ignore_patterns("build", "research", "*.docx"))
        p = os.path.join(d, fn); open(p, "w", encoding="utf-8").write(change(open(p, encoding="utf-8").read()))
        with open(os.devnull, "w") as nul:
            so = sys.stdout; sys.stdout = nul
            try: r = check(aid, tmp, quiet=True)
            finally: sys.stdout = so
        shutil.rmtree(tmp); return not r
    def body_para(s, add): return s.rstrip("\n") + "\n\n" + add + "\n"
    cases = [
        ("English sentence in the body", "ostendorf", "ostendorf_pl.md", lambda s: body_para(s, "This was left in the text and not translated.")),
        ("English in the title-note block", "pahulich", "pahulich_pl.md", lambda s: s.replace("::: przypis-tytulowy\n", "::: przypis-tytulowy\nThe acknowledgements of the author.\n", 1)),
        ("S-mark missing from the notes sheet", "tittel", "tittel_pl.md", lambda s: s + "\n<!-- DO SPRAWDZENIA: S99 -->\n"),
        ("quotes row removed", "ostendorf", "ostendorf_quotes.tsv", lambda s: "\n".join(l for l in s.split("\n") if not l.startswith("Q02\t"))),
        ("bad class", "tittel", "tittel_quotes.tsv", lambda s: s.replace("\tEN-NO-PL\t", "\tENGLISH\t", 1)),
        ("open row naming a missing S-item", "tittel", "tittel_quotes.tsv", lambda s: s.replace("open (S2)", "open (S98)", 1)),
    ]
    caught = 0
    for name, aid, fn, ch in cases:
        c = planted(aid, fn, ch); caught += c
        if not c: print("  NOT CAUGHT:", name)
    print(f"selftest: {caught}/{len(cases)} negative controls caught")
    return caught == len(cases)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a[2:] for a in sys.argv[1:] if a.startswith("--")}
    if "selftest" in flags: sys.exit(0 if selftest() else 1)
    want = tuple(f for f in ("leftover", "marks", "quotes") if f in flags) or ("leftover", "marks", "quotes")
    todo = ids() if "all" in flags else args
    if not todo: print(__doc__); sys.exit(2)
    sys.exit(0 if all([check(a, want=want) for a in todo]) else 1)
