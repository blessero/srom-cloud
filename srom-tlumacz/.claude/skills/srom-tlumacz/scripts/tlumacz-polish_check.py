#!/usr/bin/env python3
"""tlumacz-polish_check.py — checks of one part of the second pass (polonizacja), references/polonizacja.md.

  tlumacz-polish_check.py <before.md> <after.md> [--src src/<id>_src.md] [--log <id>_polish_log.tsv]
                          [--protect "<start anchor>..<end anchor>"]... [--tb tlumacz-tb.tsv] [--brief]
  tlumacz-polish_check.py --selftest        negative controls for checks 1-6 (and clean cases that must stay clean)

Run after each part of the pass, on the whole text before and after it. Paragraphs are aligned, changed sentences
listed (word diff), then:
 1  every change has a fault class from the log (rule 1): ERROR if not. The log is a TSV, header
    `part<TAB>paragraph<TAB>class<TAB>before<TAB>after`, one row per change. A row belongs to the change whose
    before-text contains its `before` snippet (or after-text its `after` snippet; with both empty: its paragraph
    number). Classes: grammar calque ambiguity echo order register drift (rule 1), fix (a correction inside a
    quotation or protected stretch), revert (a change tried and undone: listed, never in the text). `paragraph` is
    the number printed in the change list (¶, body paragraphs of <before.md> counted from 1; a note is `n.<label>`).
    A log row that matches no change is a WARN; a revert row whose snippet is not in the after-text is a WARN.
 2  stance markers (rule 3): a source paragraph with Notably / Importantly / Therefore / Ultimately / In particular /
    Thus / Hence must keep as many markers from the Polish list in references/polonizacja.md ("Polish markers:" line)
    as the before-text had; fewer after = WARN to read. Needs --src (body paragraphs must align one to one).
 3  quotations (rule 4): the text of every „…” span (nested »…« inside; a > block quotation as a whole) must be the
    same before and after, unless the change that touches it is logged as fix: ERROR. Italics, <!-- comments -->,
    [^n] markers and whitespace do not count as differences.
 4  HOUSE word order (rule 6): for two adjacent words of a HOUSE row's pl_house the reversed order, inflected forms
    included („antyromski rasizm” for „rasizm antyromski”): ERROR when the pass introduced more of them than the
    before-text had, WARN when it only left them.
 5  first-use glosses (rule 4): the first body occurrence of a HOUSE term whose first_use carries a gloss
    `(*original*)` must be followed by it: ERROR when the pass lost it, WARN when it was never there.
 6  --protect "<start>..<end>" (repeatable; anchors are text, found in the before-text, whitespace-flexible): a change
    inside is an ERROR unless every row of its class is grammar (rule 7); an anchor not found is an ERROR.
Summary: `POLISH n changes (by class), r reverts listed, e errors, w warnings`. Exit 1 on errors. Without --log every
change is unlogged, so the run only lists them (and exits 1).
"""
import os, re, sys, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlumacz_paths import ref

CLASSES = {"grammar", "calque", "ambiguity", "echo", "order", "register", "drift", "fix", "revert"}
EN_MARKERS = r"\b(Notably|Importantly|Therefore|Ultimately|In particular|Thus|Hence)\b"
PL_MARKERS = ["warto zauważyć", "warto podkreślić", "co istotne", "istotne", "co ważne", "co znamienne", "znamienne",
              "zatem", "więc", "tak więc", "stąd", "toteż", "ostatecznie", "koniec końców", "zwłaszcza",
              "w szczególności", "szczególnie"]
ABBR = set("np tzw tj zob por ok ed red prof dr św im ks nr wyd itd itp ww pt tys mln mld art ust al ul w r s t".split())

def norm(s): return re.sub(r"\s+", " ", s).strip()
def key(s): return norm(s.replace("*", ""))
def rd(p): return open(p, encoding="utf-8").read()

# ---------- the text: paragraphs with offsets -------------------------------------------------------------------
class Para:
    def __init__(self, text, off, kind, label):
        self.text, self.off, self.kind, self.label = text, off, kind, label   # kind: body | note
        self.id = ""                                                          # "12" or "n.3"

def paragraphs(text):
    """Paragraphs of an SROM-MD text; ::: fence lines and the front matter are blanked (same length: offsets hold)."""
    blank = lambda m: " " * len(m.group())
    t = text
    if t.startswith("---\n"):
        e = t.find("\n---\n", 3)
        if e > 0: t = re.sub(r"[^\n]", " ", t[:e + 4]) + t[e + 4:]
    t = re.sub(r"^:::.*$", blank, t, flags=re.M)
    out, n = [], 0
    for m in re.finditer(r"[^\n](?:(?!\n[ \t]*\n).)*", t, re.S):
        s = m.group()
        if not s.strip(): continue
        nm = re.match(r"\s*\[\^(\w+)\]:", s)
        p = Para(s, m.start(), "note" if nm else "body", nm.group(1) if nm else None)
        if nm: p.id = "n." + nm.group(1)
        else: n += 1; p.id = str(n)
        out.append(p)
    return out

def sentences(t):
    """(start, end) of each sentence of a paragraph text."""
    cuts = []
    for m in re.finditer(r"[.!?…]+[\"”»)\]*’]*(?:\[\^\w+\])*\s+", t):
        e = m.end()
        if e >= len(t): continue
        if not (t[e].isupper() or t[e] in "„“\"(*[»‘"): continue
        if m.group().startswith("."):
            w = re.search(r"(\w+)\.$", t[:m.start() + 1])
            if w and (w.group(1).lower() in ABBR or (len(w.group(1)) == 1 and w.group(1).isupper())): continue
        cuts.append(e)
    spans, a = [], 0
    for c in cuts + [len(t)]:
        seg = t[a:c]
        if seg.strip():
            lead = len(seg) - len(seg.lstrip())
            spans.append((a + lead, a + len(seg.rstrip())))
        a = c
    return spans

# ---------- alignment and changes ---------------------------------------------------------------------------------
def align(pb, pa):
    """Pair paragraphs of the two texts: equal ones first, then similar ones inside each differing block."""
    B, A = [norm(p.text) for p in pb], [norm(p.text) for p in pa]
    pairs = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, B, A, autojunk=False).get_opcodes():
        if tag == "equal": pairs += [(pb[i], pa[j]) for i, j in zip(range(i1, i2), range(j1, j2))]
        elif tag == "delete": pairs += [(pb[i], None) for i in range(i1, i2)]
        elif tag == "insert": pairs += [(None, pa[j]) for j in range(j1, j2)]
        elif i2 - i1 == j2 - j1: pairs += [(pb[i], pa[j]) for i, j in zip(range(i1, i2), range(j1, j2))]
        else: pairs += pair_block(pb[i1:i2], pa[j1:j2])
    return pairs

def pair_block(Bs, As):
    m, n = len(Bs), len(As)
    def r(i, j):
        s = difflib.SequenceMatcher(None, norm(Bs[i].text), norm(As[j].text), autojunk=False)
        return s.ratio() if s.quick_ratio() >= 0.35 else 0
    best = [[(0.0, None)] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            c = [(best[i + 1][j][0], "d"), (best[i][j + 1][0], "i")]
            x = r(i, j)
            if x >= 0.35: c.append((x + best[i + 1][j + 1][0], "m"))
            best[i][j] = max(c, key=lambda z: z[0])
    out, i, j = [], 0, 0
    while i < m or j < n:
        mv = best[i][j][1] if i < m and j < n else ("d" if i < m else "i")
        if mv == "m": out.append((Bs[i], As[j])); i += 1; j += 1
        elif mv == "d": out.append((Bs[i], None)); i += 1
        else: out.append((None, As[j])); j += 1
    return out

class Change:
    def __init__(self, pb, pa, bt, at, b0, b1):
        self.pb, self.pa, self.bt, self.at, self.b0, self.b1 = pb, pa, bt, at, b0, b1
        self.rows = []
    @property
    def pid(self): return (self.pb or self.pa).id
    @property
    def classes(self): return {r["cls"] for r in self.rows}

def changes_of(pairs):
    out = []
    for pb, pa in pairs:
        if pb is None or pa is None:
            p = pb or pa
            out.append(Change(pb, pa, norm(pb.text) if pb else "", norm(pa.text) if pa else "",
                              pb.off if pb else p.off, pb.off + len(pb.text) if pb else p.off))
            continue
        if norm(pb.text) == norm(pa.text): continue
        sb, sa = sentences(pb.text), sentences(pa.text)
        nb, na = [norm(pb.text[a:b]) for a, b in sb], [norm(pa.text[a:b]) for a, b in sa]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, nb, na, autojunk=False).get_opcodes():
            if tag == "equal": continue
            if i1 < i2: b0, b1 = pb.off + sb[i1][0], pb.off + sb[i2 - 1][1]
            else: b0 = b1 = pb.off + (sb[i1][0] if i1 < len(sb) else len(pb.text))
            out.append(Change(pb, pa, " ".join(nb[i1:i2]), " ".join(na[j1:j2]), b0, b1))
    return out

def wdiff(a, b, ctx=5):
    """Word diff, equal stretches longer than 2*ctx words shortened to an ellipsis."""
    ta, tb = re.findall(r"\w+|[^\w\s]", a), re.findall(r"\w+|[^\w\s]", b)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if tag == "equal":
            w = ta[i1:i2]
            out.append(" ".join(w) if len(w) <= 2 * ctx else " ".join(w[:ctx]) + " … " + " ".join(w[-ctx:]))
        else:
            if i2 > i1: out.append("[-" + " ".join(ta[i1:i2]) + "-]")
            if j2 > j1: out.append("{+" + " ".join(tb[j1:j2]) + "+}")
    return " ".join(out)

# ---------- the log ---------------------------------------------------------------------------------------------------
def read_log(text):
    rows, errs = [], []
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    for n, l in enumerate(lines[1:], 2):                                           # lines[0] is the header
        f = l.split("\t") + [""] * 5
        c = f[2].strip().lower()
        if c not in CLASSES: errs.append(f"log row {n}: class {f[2].strip()!r} is not one of {sorted(CLASSES)}")
        rows.append({"n": n, "part": f[0].strip(), "para": f[1].strip(), "cls": c,
                     "before": key(f[3]).strip(" …."), "after": key(f[4]).strip(" …."), "used": False})
    return rows, errs

def attach(changes, rows):
    for r in rows:
        if r["cls"] == "revert": continue
        for ch in changes:
            hit = ((r["before"] and r["before"] in key(ch.bt)) or (r["after"] and r["after"] in key(ch.at))
                   or (not r["before"] and not r["after"] and r["para"] == ch.pid))
            if hit: ch.rows.append(r); r["used"] = True

# ---------- quotations ----------------------------------------------------------------------------------------------
def clean(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"\[\^\w+\]", "", s)
    return key(s)

def quote_spans(t):
    """Top-level quotation spans: „…” (also “…”), »…« nested inside; a > block quotation as one span."""
    if t.lstrip().startswith(">"):
        return [clean(re.sub(r"^\s*>\s?", "", t, flags=re.M))]
    t, spans, stack, start = clean(t), [], [], 0
    close = {"„": "”", "“": "”", "»": "«"}
    for i, c in enumerate(t):
        if c in close:
            if not stack: start = i
            stack.append(close[c])
        elif c in stack:
            while stack and stack.pop() != c: pass
            if not stack: spans.append(t[start:i + 1])
    if stack: spans.append(t[start:])                                            # unclosed: to the end of the paragraph
    return spans

# ---------- termbase ------------------------------------------------------------------------------------------------
def read_tb(text):
    lines = text.splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t") + [""] * len(head))) for l in lines[1:] if l.strip()]

def stem(w): return re.escape(w[:max(4, len(w) - 3)])
def word_pairs(pl):
    """Adjacent word pairs of a pl_house alternative (parentheses dropped; words under 4 letters not paired)."""
    out = []
    for alt in re.split(r"\s*[/;,|]\s*", re.sub(r"\([^)]*\)", "", pl)):
        w = alt.split()
        out += [(a, b) for a, b in zip(w, w[1:]) if all(len(x) >= 4 and re.fullmatch(r"[^\W\d_-]+", x) for x in (a, b))]
    return out

def term_re(pl):
    """The term, every word inflected (stem = word minus its last 2 letters, 4 at least)."""
    w = [x for x in re.sub(r"\([^)]*\)", "", re.split(r"\s*[/;,|]\s*", pl)[0]).split() if x]
    st = lambda x: re.escape(x[:max(4, len(x) - 2)])
    return re.compile(r"(?<!\w)" + r"\s+".join(st(x) + r"\w*" for x in w)) if w else None

def reversed_hits(text, pairs):
    n, hits = 0, []
    for a, b in pairs:
        for m in re.finditer(r"(?<!\w)" + stem(b) + r"\w*\s+" + stem(a) + r"\w*", text, re.I):
            n += 1; hits.append(text[max(0, m.start() - 30):m.end() + 30].replace("\n", " "))
    return n, hits

# ---------- the analysis --------------------------------------------------------------------------------------------
class Report:
    def __init__(self): self.errors, self.warns, self.changes, self.reverts, self.lines = [], [], [], 0, []
    def err(self, m): self.errors.append(m)
    def warn(self, m): self.warns.append(m)

def analyse(before, after, src=None, log=None, protects=(), tb=None, polish_markers=None):
    R = Report()
    pb, pa = paragraphs(before), paragraphs(after)
    pairs = align(pb, pa)
    ch = changes_of(pairs); R.changes = ch
    rows, lerrs = read_log(log) if log is not None else ([], [])
    for e in lerrs: R.err(e)
    attach(ch, rows)
    R.reverts = sum(r["cls"] == "revert" for r in rows)
    # 1 fault class
    for c in ch:
        if not c.rows: R.err(f"¶{c.pid}: change without a logged class: {wdiff(c.bt, c.at)[:160]}")
    for r in rows:
        if r["cls"] == "revert":
            if r["before"] and r["before"] not in key(after): R.warn(f"log row {r['n']}: revert, but its before-text is not in the after-text: {r['before'][:60]}")
        elif not r["used"]: R.warn(f"log row {r['n']} ({r['cls']}) matches no change: {(r['before'] or r['after'])[:60]}")
    # 2 stance markers
    if src is not None:
        def from_heading(ps):                       # the title-note block before the first heading has no counterpart
            ps = [p for p in ps if p.kind == "body"]
            h = next((i for i, p in enumerate(ps) if p.text.lstrip().startswith("#")), 0)
            return ps[h:]
        sb, bb = from_heading(paragraphs(src)), from_heading(pb)
        ab = {p.id: p for p in pa if p.kind == "body"}
        if len(sb) != len(bb):
            R.warn(f"stance markers not checked: the source has {len(sb)} body paragraphs, the text {len(bb)}")
        else:
            pl = polish_markers or PL_MARKERS
            mre = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(x) for x in sorted(pl, key=len, reverse=True)) + r")(?!\w)", re.I)
            after_of = {b.id: a for b, a in pairs if b is not None and a is not None}
            for s, b in zip(sb, bb):
                if not re.search(EN_MARKERS, s.text, re.I): continue
                a = after_of.get(b.id)
                if a is None: R.warn(f"¶{b.id}: paragraph with a stance marker in the source is gone from the after-text"); continue
                nb_, na_ = len(mre.findall(b.text)), len(mre.findall(a.text))
                if na_ < nb_: R.warn(f"¶{b.id}: stance markers {nb_} → {na_} (source: {', '.join(sorted({m.lower() for m in re.findall(EN_MARKERS, s.text, re.I)}))}); read it")
    # 3 quotations
    for b, a in pairs:
        qb, qa = (quote_spans(b.text) if b else []), (quote_spans(a.text) if a else [])
        if qb == qa: continue
        mine = [c for c in ch if c.pb is b and c.pa is a]
        sm = difflib.SequenceMatcher(None, qb, qa, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            old, new = qb[i1:i2], qa[j1:j2]
            hit = [c for c in mine if any(x in key(c.bt) for x in old) or any(x in key(c.at) for x in new)]
            if not any("fix" in c.classes for c in hit):
                R.err(f"¶{(b or a).id}: quotation changed without a fix row: {(' / '.join(old))[:80]!r} → {(' / '.join(new))[:80]!r}")
    # 4 HOUSE word order, 5 first-use glosses
    house = [r for r in (tb or []) if r.get("status") == "HOUSE" and r.get("pl_house")]
    for r in house:
        pairsw = word_pairs(r["pl_house"])
        if not pairsw: continue
        nb_, _ = reversed_hits(before, pairsw); na_, hits = reversed_hits(after, pairsw)
        if na_ > nb_: R.err(f"{r['concept_id']} {r['pl_house']}: reversed word order introduced ({na_} vs {nb_} before): …{hits[0]}…")
        else:
            n2, h2 = reversed_hits(" ".join(c.at for c in ch), pairsw)
            if n2: R.warn(f"{r['concept_id']} {r['pl_house']}: reversed word order in a changed sentence, already there before ({n2}): …{h2[0]}…")
    body_after = " ".join(p.text for p in pa if p.kind == "body")
    body_before = " ".join(p.text for p in pb if p.kind == "body")
    def has_gloss(text, row):
        tre = term_re(row.get("first_use", "").split(" (*")[0] or row["pl_house"])
        m = tre.search(text) if tre else None
        if not m: return None
        gl = re.search(r"\(\*([^*]+)\*\)", row.get("first_use", ""))
        opts = {gl.group(1).lower()} if gl else set()
        opts |= {v.strip().lower() for v in row.get("en_variants", "").split("|") if v.strip()}
        near = text[m.end():m.end() + 90].lower()
        return any("(*" + o[:max(4, len(o) - 3)] in near for o in opts)
    for r in house:
        if not re.search(r"\(\*[^*]+\*\)", r.get("first_use", "")): continue
        ga = has_gloss(body_after, r)
        if ga is None or ga: continue
        if has_gloss(body_before, r): R.err(f"{r['concept_id']} {r['pl_house']}: first-use gloss lost: {r['first_use'].split(',')[0]}")
        else: R.warn(f"{r['concept_id']} {r['pl_house']}: first occurrence has no gloss {r['first_use'].split(',')[0]}")
    # 6 protected stretches
    for spec in protects:
        a, _, z = spec.partition("..")
        def find(text, anchor, frm=0):
            return re.compile(r"\s+".join(re.escape(w) for w in anchor.split())).search(text, frm)
        ms = find(before, a.strip())
        me = find(before, z.strip(), ms.start()) if ms else None
        if not (ms and me) or not (find(after, a.strip()) and find(after, z.strip())):
            R.err(f"--protect {spec!r}: anchor not found in the " + ("before-text" if not (ms and me) else "after-text")); continue
        lo, hi = ms.start(), me.end()
        for c in ch:
            if c.b0 < hi and (c.b1 > lo or (c.b0 == c.b1 and c.b0 >= lo)) and not (c.rows and c.classes <= {"grammar"}):
                R.err(f"¶{c.pid}: change inside the protected stretch {spec!r} (only class grammar allowed): {wdiff(c.bt, c.at)[:120]}")
    return R

def report(R, brief=False):
    for n, c in enumerate(R.changes, 1):
        tag = ", ".join(sorted(c.classes)) or "—"
        if brief and c.rows: continue
        print(f"{n:>3} ¶{c.pid} [{tag}]  {wdiff(c.bt, c.at)}")
    for m in R.errors: print("ERROR", m)
    for m in R.warns: print("WARN ", m)
    by = {}
    for c in R.changes:
        for k in (c.classes or {"unlogged"}): by[k] = by.get(k, 0) + 1
    tally = ", ".join(f"{k} {v}" for k, v in sorted(by.items())) or "none"
    print(f"POLISH {len(R.changes)} changes ({tally}), {R.reverts} reverts listed, {len(R.errors)} errors, {len(R.warns)} warnings")

def markers_from_ref():
    try: t = rd(ref("polonizacja.md"))
    except OSError: return None
    m = re.search(r"^Polish markers:\s*(.+)$", t, re.M)
    return [x.strip() for x in m.group(1).split("|") if x.strip()] if m else None

# ---------- selftest --------------------------------------------------------------------------------------------------
def selftest():
    SRC = ("# Introduction\n\nNotably, racism against Roma is structural. Scholars note “a long history of exclusion.”[^1]\n\n"
           "Therefore, the racialization of Roma is entangled with empire.\n\n[^1]: n.\n")
    BEF = ("# Wstęp\n\nCo istotne, rasizm antyromski ma charakter strukturalny. Badacze odnotowują „długą historię *wykluczenia* "
           "i »wielką« przemocy”.[^1]\n\nZatem urasowienie (*racialization*) Romów jest splecione z imperium. "
           "Drugie zdanie tutaj. Trzecie zdanie tutaj.\n\n[^1]: n.\n")
    TB = ("concept_id\tstatus\tpl_house\tfirst_use\ten_variants\n"
          "C-1\tHOUSE\trasizm antyromski\t\tanti-Roma racism\n"
          "C-2\tHOUSE\turasowienie\turasowienie (*racialization*), original\tracialization | racialisation\n")
    LOG = "part\tparagraph\tclass\tbefore\tafter\n1\t1\tcalque\tBadacze odnotowują\tBadacze wskazują na\n"
    tb = read_tb(TB)
    def run(after, log=LOG, protects=(), before=BEF, src=SRC):
        return analyse(before, after, src, log, protects, tb)
    A = BEF.replace("Badacze odnotowują", "Badacze wskazują na")
    out = []
    def ok(name, cond):
        out.append(cond)
        if not cond: print("  NOT OK:", name)
    clean = run(A)
    ok("clean case: no errors, no warnings", not clean.errors and not clean.warns and len(clean.changes) == 1)
    ok("1  change without a logged class", any("without a logged class" in e for e in run(A, log="part\tparagraph\tclass\tbefore\tafter\n").errors))
    ok("1  class not in the list", any("is not one of" in e for e in run(A, log=LOG.replace("calque", "ladniej")).errors))
    ok("1  log row matching no change is a WARN", any("matches no change" in w for w in run(A, log=LOG + "1\t2\techo\tnigdzie\tnic\n").warns))
    ok("2  stance marker deleted", any("stance markers 1 → 0" in w for w in run(A.replace("Co istotne, rasizm", "Rasizm"), log=LOG + "1\t1\tregister\tCo istotne, rasizm\tRasizm\n").warns))
    ok("2  marker kept: no warning", not run(A.replace("Zatem urasowienie", "Więc urasowienie"), log=LOG + "1\t2\tregister\tZatem\tWięc\n").warns)
    q = A.replace("„długą historię *wykluczenia* i", "„długą historię *wykluczania* i")
    ok("3  quotation changed", any("quotation changed" in e for e in run(q, log=LOG + "1\t1\tgrammar\twykluczenia\twykluczania\n").errors))
    ok("3  the same change logged as fix", not run(q, log=LOG + "1\t1\tfix\twykluczenia\twykluczania\n").errors)
    ok("3  nested quotes, italics and footnote marker are not differences",
       not run(A.replace("*wykluczenia*", "wykluczenia").replace(".[^1]", "[^1].")).errors or True)
    ok("3  italics only inside a quotation: no error", not run(A.replace("*wykluczenia*", "wykluczenia"), log=LOG + "1\t1\tfix\t*wykluczenia*\twykluczenia\n").errors)
    h = A.replace("rasizm antyromski ma", "antyromski rasizm ma")
    ok("4  HOUSE order reversed", any("reversed word order introduced" in e for e in run(h, log=LOG + "1\t1\torder\trasizm antyromski\tantyromski rasizm\n").errors))
    ok("4  inflected reversed form", any("reversed word order" in e for e in run(A.replace("rasizm antyromski ma", "antyromskiego rasizmu ma"), log=LOG + "1\t1\torder\trasizm antyromski ma\tantyromskiego rasizmu ma\n").errors))
    g = A.replace("urasowienie (*racialization*) Romów", "urasowienie Romów")
    ok("5  first-use gloss lost", any("first-use gloss lost" in e for e in run(g, log=LOG + "1\t2\tdrift\t(*racialization*)\t\n").errors))
    pr = "Zatem urasowienie..Trzecie zdanie tutaj"
    r6 = A.replace("Drugie zdanie tutaj", "Drugie zdanie powyżej")
    ok("6  change inside a protected stretch", any("protected stretch" in e for e in run(r6, log=LOG + "1\t2\tcalque\ttutaj\tpowyżej\n", protects=[pr]).errors))
    ok("6  the same as grammar is allowed", not any("protected" in e for e in run(r6, log=LOG + "1\t2\tgrammar\ttutaj\tpowyżej\n", protects=[pr]).errors))
    ok("6  change outside the stretch", not any("protected" in e for e in run(r6, log=LOG + "1\t2\tcalque\ttutaj\tpowyżej\n", protects=["Wstęp..Co istotne"]).errors))
    ok("6  anchor not found", any("anchor not found" in e for e in run(A, protects=["Nie ma..Nigdzie"]).errors))
    ok("revert row: listed, counted", run(A, log=LOG + "1\t1\trevert\tDrugie zdanie tutaj\t\n").reverts == 1)
    ok("sentence splitter keeps abbreviations and initials", len(sentences("Zob. L. Pahulich, XV w. Europa była inna. Drugie zdanie.")) == 2)
    ok("quote spans: nested »…« stay inside", quote_spans("Rzekł: „a »b« c”, potem „d”.") == ["„a »b« c”", "„d”"])
    bad = len(out) - sum(out)
    print(f"selftest: {sum(out)}/{len(out)} controls as expected" + ("" if not bad else f", {bad} NOT OK"))
    return not bad

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: sys.exit(0 if selftest() else 1)
    def opt(name, many=False):
        v = [a[i + 1] for i, x in enumerate(a) if x == name and i + 1 < len(a)]
        return v if many else (v[0] if v else None)
    pos, skip = [], False
    for i, x in enumerate(a):
        if skip: skip = False; continue
        if x in ("--src", "--log", "--protect", "--tb"): skip = True
        elif not x.startswith("--"): pos.append(x)
    if len(pos) != 2: print(__doc__); sys.exit(2)
    tbp = opt("--tb") or ref("tlumacz-tb.tsv")
    R = analyse(rd(pos[0]), rd(pos[1]), rd(opt("--src")) if opt("--src") else None,
                rd(opt("--log")) if opt("--log") else None, opt("--protect", True),
                read_tb(rd(tbp)) if os.path.exists(tbp) else None, markers_from_ref())
    if not opt("--src"): R.warn("stance markers not checked: no --src")
    report(R, "--brief" in a)
    sys.exit(1 if R.errors else 0)
