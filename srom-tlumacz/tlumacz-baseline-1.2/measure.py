#!/usr/bin/env python3
"""measure.py — runnable checks for tlumacz-gates-1.2.md (run from the srom-tlumacz folder or this one).

  words      each <art>_src.md has 1,300–2,000 body words (note blocks excluded)
  structure  each <art>_blind.md has the source's paragraph count and note labels, in order
  marks      Polish drafts, body text: no em dash, no straight double quote, „ present (kanon § 3.1–3.2)
  house      per paragraph, the HOUSE Polish stem occurs at least as often as its source term
  queries    each <art>_pytania_tlum.csv has the srom-typeset header and >= 1 row
  inventory  counts from divergences.tsv: verdicts, and classes of my errors (verdict MB or BOTH)
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARTS = ["takacs", "ostendorf", "fotta", "dom"]
HOUSE = [  # (source pattern, Polish stem pattern) — the four HOUSE rows of tlumacz-tb.tsv
    (r"\bracializ|\bracialis", r"urasow|urasaw"),
    (r"\binterlocking matri", r"splecion\w* matryc"),
    (r"absence-ing", r"u-nieobecnia"),
    (r"\bsubaltern", r"subaltern"),
]
HEADER = ["adresat", "rodzaj", "przypis", "dzieło", "szczegóły"]


def blocks(path):
    """Split into (paragraphs, notes): paragraphs = non-note blocks; notes = [(label, text)]."""
    text = open(path, encoding="utf-8").read()
    paras, notes = [], []
    for b in re.split(r"\n\s*\n", text.strip()):
        m = re.match(r"\[\^(\w+)\]:\s*(.*)", b, re.S)
        if m:
            notes.append((m.group(1), m.group(2)))
        elif b.startswith("    ") and notes:  # indented continuation of a multi-paragraph note
            notes[-1] = (notes[-1][0], notes[-1][1] + "\n" + b)
        else:
            paras.append(b)
    return paras, notes


def p(a, kind): return os.path.join(HERE, f"{a}_{kind}")


def words():
    ok = 0
    for a in ARTS:
        paras, _ = blocks(p(a, "src.md"))
        n = len(re.sub(r"\[\^\w+\]", "", " ".join(x for x in paras if not x.startswith("#"))).split())
        good = 1300 <= n <= 2000; ok += good
        print(f"  {a}: {n} body words {'ok' if good else 'OUT OF RANGE'}")
    print(f"words: {ok}/{len(ARTS)} in range")


def structure():
    ok = 0
    for a in ARTS:
        if not os.path.exists(p(a, "blind.md")):
            print(f"  {a}: no draft"); continue
        sp, sn = blocks(p(a, "src.md")); tp, tn = blocks(p(a, "blind.md"))
        sm = [re.findall(r"\[\^(\w+)\](?!:)", x) for x in sp]; tm = [re.findall(r"\[\^(\w+)\](?!:)", x) for x in tp]
        probs = []
        if len(sp) != len(tp): probs.append(f"paragraphs {len(sp)}→{len(tp)}")
        if [l for l, _ in sn] != [l for l, _ in tn]: probs.append(f"notes {[l for l,_ in sn]}→{[l for l,_ in tn]}")
        if sm != tm: probs.append("marker placement per paragraph differs")
        ok += not probs
        print(f"  {a}: {len(sp)} paragraphs, {len(sn)} notes " + ("ok" if not probs else "; ".join(probs)))
    print(f"structure: {ok}/{len(ARTS)} match")


def marks():
    ok = 0
    for a in ARTS:
        if not os.path.exists(p(a, "blind.md")):
            print(f"  {a}: no draft"); continue
        t = "\n\n".join(blocks(p(a, "blind.md"))[0])  # body only: notes hold citation strings frozen as the author wrote them
        probs = [f"{t.count(c)}×{n}" for c, n in (("—", "em dash"), ('"', "straight quote")) if t.count(c)]
        if "„" not in t: probs.append("no „")
        ok += not probs
        print(f"  {a}: " + ("clean" if not probs else ", ".join(probs)))
    print(f"marks: {ok}/{len(ARTS)} clean")


def house():
    total = miss = 0
    for a in ARTS:
        if not os.path.exists(p(a, "blind.md")):
            print(f"  {a}: no draft"); miss += 1; continue
        sp, sn = blocks(p(a, "src.md")); tp, tn = blocks(p(a, "blind.md"))
        pairs = list(zip(sp, tp)) + list(zip([x for _, x in sn], [x for _, x in tn]))
        for s, t in pairs:
            for sp_pat, pl_pat in HOUSE:
                ns, nt = len(re.findall(sp_pat, s, re.I)), len(re.findall(pl_pat, t, re.I))
                total += ns
                if nt < ns:
                    miss += ns - nt; print(f"  {a}: '{sp_pat}' {ns}× in source, HOUSE form {nt}× in: {t[:70]}…")
    print(f"house: all {total} occurrences rendered" if not miss else f"house: {miss} of {total} missing")


def queries():
    ok = 0
    for a in ARTS:
        f = p(a, "pytania_tlum.csv")
        if not os.path.exists(f):
            print(f"  {a}: missing"); continue
        rows = list(csv.reader(open(f, encoding="utf-8-sig"), delimiter=";"))
        good = rows and rows[0] == HEADER and len(rows) > 1 and all(len(r) == 5 for r in rows)
        ok += bool(good)
        print(f"  {a}: {len(rows) - 1} rows " + ("ok" if good else "BAD (header, width or empty)"))
    print(f"queries: {ok}/{len(ARTS)} valid")


def inventory():
    rows = list(csv.DictReader(open(os.path.join(HERE, "divergences.tsv"), encoding="utf-8"), delimiter="\t"))
    from collections import Counter
    ok = all(r["verdict"] in {"MB", "ME", "EQ", "SV", "BOTH"} for r in rows) and all(r["art"] in ARTS for r in rows)
    print("rows:", len(rows), "| per article:", dict(Counter(r["art"] for r in rows)))
    print("verdicts:", dict(Counter(r["verdict"] for r in rows)))
    mine = [r for r in rows if r["verdict"] in ("MB", "BOTH")]
    print("my errors by class:", dict(Counter(r["class"] for r in mine)))
    print("MB-side issues by class:", dict(Counter(r["class"] for r in rows if r["verdict"] in ("ME", "BOTH"))))
    print(f"inventory: {'valid' if ok else 'INVALID codes'}, {len(mine)} errors of mine in {len(rows)} divergences")


if __name__ == "__main__":
    {"words": words, "structure": structure, "marks": marks, "house": house, "queries": queries, "inventory": inventory}[sys.argv[1]]()
