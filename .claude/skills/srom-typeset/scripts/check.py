#!/usr/bin/env python3
"""
check.py — integrity checks on SROM-MD before building / after translating.

    python3 check.py article.md [--refs refs.json]          single-file integrity
    python3 check.py --pair source.md target.md [--refs …]  translation invariance

Single file (ERROR = must fix):
  - every [^n] reference has exactly one definition, every definition is referenced, labels unique
  - every @key resolves in refs.json (if given); malformed citations left as literal text
  - literal * or _ surviving the parse (broken italics), leftover author-date "(Nowak 2010: 15)"
Pair (source vs translation):
  - same number of headings / paragraphs / block quotes / list items           ERROR if different
  - per paragraph: same number of note markers                                 ERROR
  - per note: same citation keys in the same order                             ERROR
  - per paragraph and note: same numbers (years, pages, dates …)               WARN (formats change legitimately)
Exit 1 if any ERROR. Last line: CHECK OK / CHECK FAIL n error(s).
"""
import argparse, json, os, re, subprocess, sys, tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cite_map import expand_ranges      # 210–13 -> 210–213

FROM = ("markdown-smart-superscript-subscript-strikeout-raw_html-raw_tex-tex_math_dollars"
        "-implicit_figures-fancy_lists-example_lists-task_lists-auto_identifiers")
AUTHOR_DATE = re.compile(
    r"\((?:zob\.\s|por\.\s|see\s|cf\.\s)?[A-ZŁŚŻŹĆ][\w’'\-]+(?:\s(?:i|and|&|et)\s[A-ZŁŚŻŹĆ][\w’'\-]+|\set\sal\.|\si\sin\.)?(?:\s\((?:red|eds?|Hrsg|oprac)\.\))?,?\s(?:1[5-9]|20)\d\d[a-z]?(?:[:,]\s?[\d–\-]+)?[^()]{0,40}\)")




def strip_comments(text):
    """editor comments <!-- … --> are not text: removed before any parse (pandoc would print them)"""
    comments = re.findall(r"<!--(.*?)-->", text, flags=re.S)
    text = re.sub(r"[ \t]*<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, [c.strip() for c in comments]


def load_refs(paths, errs=None):
    """one or more CSL-JSON files (e.g. refs.json + srom-tlumacz's <id>_refs_tlum.json) -> {id: item}"""
    out = {}
    for p in paths or []:
        for r in json.load(open(p, encoding="utf-8")):
            if r["id"] in out and errs is not None:
                errs.append(f"duplicate ref id @{r['id']} ({os.path.basename(p)})")
            out[r["id"]] = r
    return out


def ast(path):
    src, _ = strip_comments(open(path, encoding="utf-8").read())
    r = subprocess.run(["pandoc", "-f", FROM, "-t", "json"], input=src, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    return json.loads(r.stdout)


def ser(x):
    if isinstance(x, list):
        return "".join(ser(i) for i in x)
    t, c = x["t"], x.get("c")
    if t == "Str": return c
    if t in ("Space", "SoftBreak", "LineBreak"): return " "
    if t in ("Emph", "Strong", "SmallCaps", "Underline", "Strikeout", "Superscript", "Subscript"): return ser(c)
    if t == "Quoted": return "„" + ser(c[1]) + "”"
    if t in ("Span", "Link"): return ser(c[1])
    if t == "Cite": return " ".join(ser(ci["citationPrefix"]) + " @" + ci["citationId"] + ser(ci["citationSuffix"]) for ci in c[0])
    if t == "Note": return "⁽ⁿ⁾"
    return ""


def leaves(blocks, kind="p"):
    """flatten to leaf paragraphs with their structural kind (h1/h2/p/q/li)"""
    out = []
    for b in blocks:
        t = b["t"]
        if t == "Header":
            out.append(("h%d" % b["c"][0], b["c"][2]))
        elif t in ("Para", "Plain"):
            out.append((kind, b["c"]))
        elif t == "BlockQuote":
            out += leaves(b["c"], "q")
        elif t == "BulletList" or t == "OrderedList":
            items = b["c"] if t == "BulletList" else b["c"][1]
            for it in items:
                out += leaves(it, "li")
        elif t == "Div":
            if b["c"][0][0] in ("refs",) or "przypis-tytulowy" in b["c"][0][1]:
                continue          # the translation note on the title (kanon § 12.2.3) has no source counterpart
            out += leaves(b["c"][1], kind)
    return out


def notes_in(inls):
    res = []
    def walk(x):
        if isinstance(x, list):
            for i in x: walk(i)
        elif isinstance(x, dict):
            if x.get("t") == "Note":
                res.append(x["c"])
                return
            if "c" in x: walk(x["c"])
    walk(inls)
    return res


def cites_in(x):
    res = []
    def walk(y):
        if isinstance(y, list):
            for i in y: walk(i)
        elif isinstance(y, dict):
            if y.get("t") == "Cite":
                res.extend(c["citationId"] for c in y["c"][0])
            if "c" in y: walk(y["c"])
    walk(x)
    return res


MONTHS = {}
for _i, _names in enumerate([
        "january|januar|janvier|enero|gennaio|stycznia|styczeń|styczen",
        "february|februar|février|fevrier|febrero|febbraio|lutego|luty",
        "march|märz|marz|mars|marzo|marca|marzec",
        "april|avril|abril|aprile|kwietnia|kwiecień|kwiecien",
        "may|mai|mayo|maggio|maja|maj",
        "june|juni|juin|junio|giugno|czerwca|czerwiec",
        "july|juli|juillet|julio|luglio|lipca|lipiec",
        "august|août|aout|agosto|sierpnia|sierpień|sierpien",
        "september|septembre|septiembre|settembre|września|wrzesnia|wrzesień|wrzesien",
        "october|oktober|octobre|octubre|ottobre|października|pazdziernika|październik",
        "november|novembre|noviembre|listopada|listopad",
        "december|dezember|décembre|decembre|diciembre|dicembre|grudnia|grudzień|grudzien"], 1):
    for _n in _names.split("|"):
        MONTHS[_n] = _i
_M = "|".join(sorted(MONTHS, key=len, reverse=True))
MONTH_RX = re.compile(r"(?:(?<=\d )|(?<=\d\. ))\b(" + _M + r")\b|\b(" + _M + r")\b(?=,? \d)", re.I)  # only next to a digit


def ser_num(x, skip=()):
    """serialisation for number comparison: citation keys never counted; added citations skipped whole"""
    if isinstance(x, list):
        return "".join(ser_num(i, skip) for i in x)
    if isinstance(x, dict) and x.get("t") == "Cite":
        return " ".join(ser(ci["citationPrefix"]) + " " + ser(ci["citationSuffix"]) for ci in x["c"][0] if ci["citationId"] not in skip)
    if isinstance(x, dict) and x.get("t") in ("Emph", "Strong", "SmallCaps", "Underline", "Strikeout", "Superscript", "Subscript"):
        return ser_num(x["c"], skip)
    if isinstance(x, dict) and x.get("t") == "Quoted":
        return "„" + ser_num(x["c"][1], skip) + "”"
    if isinstance(x, dict) and x.get("t") in ("Span", "Link"):
        return ser_num(x["c"][1], skip)
    if isinstance(x, dict) and x.get("t") == "Note":
        return " "
    return ser(x) if isinstance(x, dict) else ""


def numbers(text):
    text = MONTH_RX.sub(lambda m: " %d " % MONTHS[(m.group(1) or m.group(2)).lower()], text)   # 4 March 1937 == 04.03.1937
    text = re.sub(r"(?<=\d)[,\u00a0 \u202f](?=\d{3}\b)", "", text)   # thousands separators
    return Counter(int(n) for n in re.findall(r"\d+", text))


def strip_notes(inls):
    return [i for i in inls if not (isinstance(i, dict) and i.get("t") == "Note")]


# ---------------------------------------------------------------- single file
NARRATIVE = re.compile(r"([A-ZŁŚŻŹĆ][\w’'\-]+)\s\((?:1[5-9]|20)\d\d[a-z]?(?:[:,]\s?[^()]{1,30})?\)")


def check_single(path, refs, errs, warns):
    """refs: dict id -> CSL item (names known: author-date leftovers are judged against them),
    a set of ids (names unknown: every leftover is an error), or None (keys not checked)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    global cm
    import cite_map as cm
    author_stems = None
    if isinstance(refs, dict):
        author_stems = {cm.stem(n) for r in refs.values() for n in cm.primary_names(r) if n}
    raw = open(path, encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    defs = re.findall(r"^\[\^([^\]\s]+)\]:", body, re.M)
    refs_ = re.findall(r"\[\^([^\]\s]+)\]", re.sub(r"^\[\^[^\]\s]+\]:", "", body, flags=re.M))
    for k, v in Counter(defs).items():
        if v > 1: errs.append(f"note label [^{k}] defined {v}×")
    for k in sorted(set(refs_) - set(defs), key=str):
        errs.append(f"note marker [^{k}] has no definition")
    for k in sorted(set(defs) - set(refs_), key=str):
        errs.append(f"note definition [^{k}] is never referenced (orphan)")
    for k, v in Counter(refs_).items():
        if v > 1: errs.append(f"note marker [^{k}] used {v}× (each note needs its own label)")
    for lab, txt in note_defs(body).items():
        errs += label_errors(lab, txt)

    doc = ast(path)
    keys = cites_in(doc["blocks"])
    def modes(x):
        if isinstance(x, list):
            for i in x: modes(i)
        elif isinstance(x, dict):
            if x.get("t") == "Cite":
                for c in x["c"][0]:
                    if c["citationMode"]["t"] == "AuthorInText":
                        errs.append(f"@{c['citationId']} without brackets (author-in-text) — write the name in prose and cite [@{c['citationId']}, s. …]")
                    elif c["citationMode"]["t"] == "SuppressAuthor":
                        errs.append(f"[-@{c['citationId']}] suppresses the author — use [@{c['citationId']}]")
            if "c" in x: modes(x["c"])
    modes(doc["blocks"])
    if refs is not None:
        for k in sorted(set(keys) - set(refs)):
            errs.append(f"citation key @{k} not in refs.json")
    flat = []
    for kind, inls in leaves(doc["blocks"]):
        flat.append(ser(inls))
        for n in notes_in(inls):
            flat.append(" ".join(ser(b["c"]) for b in n if b["t"] in ("Para", "Plain")))
    for s in flat:
        for m in re.finditer(r"(?<![\w\\])[*_]{1,2}\S|\S[*_]{1,2}(?!\w)", s):
            errs.append(f"literal * or _ after parsing (broken italics?): …{s[max(0, m.start()-30):m.end()+30]}…")
            break
        for m in re.finditer(r"\[@|@[\w:-]+\]", s):
            errs.append(f"malformed citation left as text: …{s[max(0, m.start()-30):m.end()+30]}…")
            break
        for m in AUTHOR_DATE.finditer(s):
            nm = re.match(r"\((?:zob\.\s|por\.\s|see\s|cf\.\s)?([^\s,(]+)", m.group(0)).group(1)
            if author_stems is None or cm.stem(nm) in author_stems:
                errs.append(f"author-date reference not converted: {m.group(0)}")
            else:
                warns.append(f"parenthesis with a name and a year — a citation? (name not in refs): {m.group(0)}")
        for m in NARRATIVE.finditer(s):
            if author_stems is not None and cm.stem(m.group(1)) in author_stems:
                errs.append(f"narrative author-date reference not converted: {m.group(0)}")
        if "⁽ⁿ⁾" in s and re.search(r"\[\^", s):
            errs.append(f"unparsed note marker: …{s[:60]}…")
    return len(defs), keys


# ---------------------------------------------------------------- pair
# non-author notes (kanon § 7.1): translator's "… – przyp. tłum.", editorial "… – przyp. red." — the formula must END
# the note; "[… – przyp. tłum.]" at the end is a translator's addition inside an AUTHOR's note (§ 12.2.7) and stays one
NA_FORMULA = re.compile(r"[–-]\s*przyp\.\s*(tłum|red)\.\s*$")
NA_LABEL = re.compile(r"([tr])\d+")


def na_kind(text):
    """"tłum" / "red" if the note text ends with the non-author formula, else None"""
    m = NA_FORMULA.search((text or "").strip())
    return m.group(1) if m else None


def label_kind(lab):
    """label t<n> -> "tłum", r<n> -> "red", else None"""
    m = NA_LABEL.fullmatch(lab or "")
    return {"t": "tłum", "r": "red"}[m.group(1)] if m else None


def _meta_text(x):
    if isinstance(x, list):
        return "".join(_meta_text(i) for i in x)
    if not isinstance(x, dict):
        return ""
    t, c = x.get("t"), x.get("c")
    if t in ("Str", "MetaString"):
        return c
    if t in ("Space", "SoftBreak", "LineBreak"):
        return " "
    return _meta_text(c) if isinstance(c, list) else ""


def translators(meta):
    """Kanon § 12.2.3 (E10): the translator name(s) from the front-matter field `tlumaczenie` (string or list).
    None = field absent; a list, possibly with empty names, otherwise."""
    v = (meta or {}).get("tlumaczenie")
    if v is None:
        return None
    items = v["c"] if v.get("t") == "MetaList" else [v]
    return [re.sub(r"\s+", " ", _meta_text(i)).strip() for i in items]


def translators_struct(names):
    """master-CSV format (curator C1): Given|Surname|Affiliation|ORCID ;; … — split at the last space"""
    out = []
    for n in names:
        given, _, surname = n.rpartition(" ")
        out.append(f"{given}|{surname}||")
    return " ;; ".join(out)


def label_errors(lab, text):
    k = label_kind(lab)
    if k and na_kind(text) != k:
        return [f"note [^{lab}] must end with the formula \"– przyp. {k}.\" (kanon § 7.1)"]
    return []
DODANO = re.compile(r"<!--\s*DODANO:\s*(.*?)-->", re.S)


def note_defs(raw):
    """label -> raw definition text (incl. indented continuation paragraphs and comments)"""
    body = re.sub(r"^(`{3,}|~{3,}).*?^\1\s*$", "", raw, flags=re.S | re.M)
    defs, cur = {}, None
    for blk in re.split(r"\n\s*\n", body):
        m = re.match(r"^\[\^([^\]\s]+)\]:(.*)", blk, re.S)
        if m:
            cur = m.group(1)
            defs[cur] = m.group(2)
        elif blk.startswith("    ") and cur:
            defs[cur] += "\n" + blk
        else:
            cur = None
    return defs


def marker_labels(raw):
    """note labels in reading order (= pandoc's note numbering)"""
    body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    body = re.sub(r"^\[\^[^\]\s]+\]:", "", body, flags=re.M)
    return re.findall(r"\[\^([^\]\s]+)\]", body)


def examples(doc):
    """interlinear examples (fenced blocks) in reading order -> list of examples, each a list of lines"""
    out = []
    def walk(x):
        if isinstance(x, list):
            for i in x: walk(i)
        elif isinstance(x, dict):
            if x.get("t") == "CodeBlock":
                for ex in re.split(r"\n\s*\n", x["c"][1].strip("\n")):
                    out.append([l.rstrip() for l in ex.split("\n") if l.strip()])
            elif "c" in x:
                walk(x["c"])
    walk(doc["blocks"])
    return out


def check_pair(src, tgt, errs, warns, refs=None):
    """source vs translation. Translator and editorial notes (label t<n>/r<n>, or text ending "– przyp. tłum."/
    "– przyp. red.") and the
    title note (::: przypis-tytulowy) have no source counterpart and are left out of the comparison
    (IF-TYPESET R1). A citation added in a note (e.g. the Polish edition, § 12.2.4 a–b) passes
    only when declared inside that note: <!-- DODANO: @key --> (R2)."""
    SA, TA = ast(src), ast(tgt)
    A, B = leaves(SA["blocks"]), leaves(TA["blocks"])
    # E1 — interlinear examples: same examples, same number of lines, line 1 (the form) unchanged;
    # line 2 (Polish glosses) and line 3 (translation) are the translator's
    xs, xt = examples(SA), examples(TA)
    if len(xs) != len(xt):
        errs.append(f"interlinear examples: {len(xs)} in source, {len(xt)} in target")
    for i, (e1, e2) in enumerate(zip(xs, xt), 1):
        if len(e1) != len(e2):
            errs.append(f"example {i}: {len(e1)} line(s) in source, {len(e2)} in target")
        elif e1 and re.sub(r"\s+", " ", e1[0]) != re.sub(r"\s+", " ", e2[0]):
            errs.append(f"example {i}: form line changed — source «{e1[0].strip()}» / target «{e2[0].strip()}»")
    ka, kb = Counter(k for k, _ in A), Counter(k for k, _ in B)
    if ka != kb:
        errs.append(f"block structure differs: source {dict(ka)} / target {dict(kb)}")
    raw_t = open(tgt, encoding="utf-8").read()
    labels, defs = marker_labels(raw_t), note_defs(raw_t)
    na_all = [n for _, i in A for n in notes_in(i)]
    nb_raw = [n for _, i in B for n in notes_in(i)]
    tn_flags = []
    for j, n in enumerate(nb_raw):
        lab = labels[j] if j < len(labels) else ""
        text = " ".join(ser(b["c"]) for b in n if b["t"] in ("Para", "Plain"))
        is_tn = bool(label_kind(lab) or na_kind(text))
        errs += label_errors(lab, text)
        tn_flags.append(is_tn)
    if any(tn_flags):
        warns.append(f"{sum(tn_flags)} translator/editorial note(s) left out of the comparison: " +
                     ", ".join(str(j + 1) for j, f in enumerate(tn_flags) if f) + " (target numbering)")
    nb_all = [n for n, f in zip(nb_raw, tn_flags) if not f]
    nb_labels = [labels[j] if j < len(labels) else "" for j, f in enumerate(tn_flags) if not f]
    if len(na_all) != len(nb_all):
        errs.append(f"note count differs: source {len(na_all)} / target {len(nb_all)} (translator/editorial notes excluded)")
    for i, (x, y) in enumerate(zip(na_all, nb_all), 1):
        ks, kt = cites_in(x), cites_in(y)
        declared = []
        for d in DODANO.findall(defs.get(nb_labels[i - 1], "")):
            declared += re.findall(r"@([\w:.#$%&+?<>~/-]+)", d)
        # additions: declared in the note (<!-- DODANO: @key -->) or marked "srom-added" in the refs
        # (srom-tlumacz's <id>_refs_tlum.json — survives the Word round trip, where comments do not)
        tl_added = [k for k in kt if k not in ks and refs and refs.get(k, {}).get("srom-added")]
        for k in declared:
            if k not in kt:
                warns.append(f"note {i}: DODANO declares @{k}, which the note does not cite")
        allowed = set(declared) | set(tl_added)
        rest = [k for k in kt if not (k in allowed and k not in ks)]
        for k in [k for k in kt if k in allowed and k not in ks]:
            warns.append(f"note {i}: added citation @{k} (translator's addition) — check it belongs here")
        if rest != ks:
            added = [k for k in kt if k not in ks and k not in allowed]
            msg = f"note {i}: citation keys differ: source {ks} / target {kt}"
            if added:
                msg += (f" — undeclared addition {added}: mark it \"srom-added\" in the translator's refs file "
                        f"or declare <!-- DODANO: @{added[0]} --> in that note")
            errs.append(msg)
        skip = allowed - set(ks)
        nx = numbers(" ".join(ser_num(b["c"]) for b in x if b["t"] in ("Para", "Plain")))
        ny = numbers(" ".join(ser_num(b["c"], skip) for b in y if b["t"] in ("Para", "Plain")))
        if nx != ny:
            warns.append(f"note {i}: numbers differ — only in source {dict(nx - ny)}, only in target {dict(ny - nx)}")
    if len(A) == len(B):
        ptr = 0
        for i, ((k1, x), (k2, y)) in enumerate(zip(A, B), 1):
            if k1 != k2:
                errs.append(f"block {i}: kind {k1} vs {k2} — structure drift starts here: {ser(y)[:60]}")
                break
            ny_notes = notes_in(y)
            n_tn = sum(tn_flags[ptr:ptr + len(ny_notes)])
            ptr += len(ny_notes)
            if len(notes_in(x)) != len(ny_notes) - n_tn:
                errs.append(f"block {i} ({k1}): {len(notes_in(x))} note marker(s) in source, {len(ny_notes) - n_tn} in target: {ser(y)[:70]}…")
            nx, ny = numbers(ser_num(strip_notes(x))), numbers(ser_num(strip_notes(y)))
            if nx != ny:
                warns.append(f"block {i} ({k1}): numbers differ — only in source {dict(nx - ny)}, only in target {dict(ny - nx)}: {ser(y)[:50]}…")
    else:
        errs.append(f"leaf block count differs ({len(A)} / {len(B)}) — per-paragraph marker check skipped; realign paragraphs 1:1")


def printed_numbers(src, tgt):
    """{source note label: printed footnote number in the target} — the alignment --pair uses. Printed
    numbering counts the author's notes in reading order, incl. notes made from citations typed in the main
    text; translator/editorial notes are the asterisk series (kanon § 7.1) and take no number."""
    s_labels = marker_labels(open(src, encoding="utf-8").read())
    raw_t = open(tgt, encoding="utf-8").read()
    TA = ast(tgt)
    pos, n = [], [0]
    def walk(x, in_note):
        if isinstance(x, list):
            for i in x: walk(i, in_note)
        elif isinstance(x, dict):
            t = x.get("t")
            if t == "Note" and not in_note:
                pos.append(x["c"]); return
            if t == "Cite" and not in_note:
                pos.append(None); return
            if "c" in x: walk(x["c"], in_note)
    walk(TA["blocks"], False)
    t_labels = marker_labels(raw_t)
    keep, j = [], 0
    for content in pos:
        if content is None:          # a citation in the main text: citeproc makes it a numbered note
            n[0] += 1
            continue
        lab = t_labels[j] if j < len(t_labels) else ""
        j += 1
        text = " ".join(ser(b["c"]) for b in content if b["t"] in ("Para", "Plain"))
        if not (label_kind(lab) or na_kind(text)):
            n[0] += 1
            keep.append(n[0])
    return {lab: keep[i] for i, lab in enumerate(s_labels) if i < len(keep)}


# ---------------------------------------------------------------- keyed (literal notes -> [@key] citations)
LOCATOR_NUM = re.compile(r"\b(?:s|k|l|ark|tabl|p|pp|str|S)\.\s?(\d+[a-z]?(?:\s?[–-]\s?\d+[a-z]?)?(?:,\s?\d+[a-z]?(?:[–-]\d+)?)*)")
IBID = re.compile(r"(?i)^\W*(ibidem|ibid\.?|tamże|tamze|tenże|taż|idem|eadem)\b")


def locator_numbers(text):
    c = Counter()
    for m in LOCATOR_NUM.finditer(text.replace("\u00a0", " ")):
        for n in re.findall(r"\d+", m.group(1)):
            c[int(n)] += 1
    return c


SHORT_LOC = r"(?:,\s?(?:1[5-9]\d\d|20\d\d)[a-z]?)?,\s?(\d+[a-z]?(?:\s?[–-]\s?\d+[a-z]?)?(?:,\s?\d+[a-z]?(?:\s?[–-]\s?\d+[a-z]?)?)*)(?![\d.]\d)"


def squeeze(s):
    """folded, without spaces: "M.W." == "M. W." """
    return re.sub(r"\s+", "", fold_txt(s))


def name_forms(ref):
    """how an original note may name the work's author: family name, a literal author, or its first part
    ("M. W." for "M. W., M. A.")"""
    out = []
    for p in (ref.get("author") or ref.get("editor") or []):
        n = p.get("family") or p.get("literal") or ""
        if n:
            out.append(n)
            if p.get("literal") and "," in n:
                out.append(n.split(",")[0])
    aw = ref.get("srom-as-written") or {}          # an approved correction: the author's form still counts
    out += [v for k, v in aw.items() if k in ("author", "editor") and v]
    return out


def shortform_numbers(text, refs, keys):
    """pages in short-form notes without a label, as most English and French journals write them:
    "Hornback, 35–69", "Ndiaye, 2022, 214–31", "M. W., M. A., 45" -> the numbers after the author (and year)
    of a work the keyed note cites. Abbreviated ranges count in full (210–13 = 210–213)."""
    t, found = squeeze(expand_ranges(text)), {}
    years = {str(y[0]) for key in keys for f in ("issued", "original-date")
             for y in ((refs.get(key) or {}).get(f) or {}).get("date-parts", []) if y}
    for n in {squeeze(x) for key in keys for x in name_forms(refs.get(key) or {})}:   # one author, two works: once
        for m in re.finditer(re.escape(n) + SHORT_LOC.replace("\\s?", ""), t):
            if m.group(1) in years:
                continue                 # "Ndiaye, 2021." — the year of a work cited whole, not a page
            found[m.start(1)] = m.group(1)   # by position: "Chang" inside "Rucker-Chang, 24" is the same locator
    return Counter(int(x) for loc in found.values() for x in re.findall(r"\d+", loc))


def check_keyed(orig, keyed, refs_path, errs, warns):
    """Renders the keyed file exactly as build.py will and compares it note by note with the author's
    original notes: every page/folio number must survive (labelled "s. 15", "p. 15", or bare after the author
    in short-form notes, "Hornback, 35–69"; abbreviated ranges counted in full), every cited key's author must be named in
    the original note (or the original note is an ibid./tamże pointing at the same work)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build
    cfg = os.path.join(build.ROOT, "config", "styles.json")
    meta = ["-M", "lang=pl-PL", "-M", "notes-after-punctuation=false", "-M", "suppress-bibliography=true",
            "-M", f"srom-config={cfg}"]
    ro, _ = build.pandoc_json(orig)
    rk, _ = build.pandoc_json(keyed, ["--citeproc", "--csl", build.CSL, "--bibliography", refs_path,
                                      "--lua-filter", build.LUA, *meta])
    raw_k, _ = build.pandoc_json(keyed)
    refs = {r["id"]: r for r in json.load(open(refs_path, encoding="utf-8"))}
    on, kn = build.notes_text(ro), build.notes_text(rk)
    kraw = [n for _, i in leaves(raw_k["blocks"]) for n in notes_in(i)]
    kkeys = [cites_in(n) for n in kraw]
    if len(on) != len(kn):
        errs.append(f"note count differs: original {len(on)} / keyed {len(kn)} — keying must not add or drop notes")
    prev_keys, prev_loc = [], Counter()
    for i, (o, k) in enumerate(zip(on, kn), 1):
        keys = kkeys[i - 1] if i - 1 < len(kkeys) else []
        o_loc = locator_numbers(expand_ranges(o)) | shortform_numbers(o, refs, keys)
        lost = o_loc - locator_numbers(expand_ranges(k))
        if lost and IBID.match(k) and keys == prev_keys and not (lost - prev_loc):
            lost = Counter()             # same work, same page as the note before: a bare Ibidem is right
        if lost:
            errs.append(f"note {i}: page/folio numbers lost in keying {dict(lost)}\n        original: {o[:160]}\n        rendered: {k[:160]}")
        years = Counter(int(y[0]) for key in keys for f in ("issued", "original-date")
                        for y in ((refs.get(key) or {}).get(f) or {}).get("date-parts", []) if y)
        other = numbers(expand_ranges(o)) - numbers(expand_ranges(k)) - o_loc - Counter({y: 99 for y in years})
        if other:
            warns.append(f"note {i}: other numbers not in rendering {dict(other)}: {o[:100]}")
        if not keys:
            if norm_ws(o) != norm_ws(k):
                warns.append(f"note {i}: literal note differs after rendering: {o[:80]} | {k[:80]}")
        elif IBID.match(o):
            if keys != prev_keys[-1:] and keys != prev_keys:
                errs.append(f"note {i}: original is ibid./tamże but keyed {keys} ≠ previous note {prev_keys}")
        else:
            fo, so = fold_txt(o), squeeze(o)
            for key in keys:
                r = refs.get(key)
                if not r:
                    continue
                names = name_forms(r)
                if names and not any(fold_txt(n) in fo or fold_txt(n)[:max(4, len(n) - 3)] in fo or squeeze(n) in so
                                     for n in names if n):
                    ttl = fold_txt((r.get("title-short") or r.get("title") or "")[:18].rstrip("…"))
                    if not (len(ttl) >= 8 and ttl in fo):
                        errs.append(f"note {i}: @{key} ({', '.join(names)}) — neither author nor title found in the original note: {o[:120]}")
        prev_keys = keys or prev_keys
        prev_loc = o_loc if keys else prev_loc


def fold_txt(s):
    import unicodedata
    s = s.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").casefold()


def norm_ws(s):
    return re.sub(r"\s+", " ", s.replace("*", "")).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md", nargs="?")
    ap.add_argument("--pair", nargs=2, metavar=("SOURCE", "TARGET"))
    ap.add_argument("--keyed", nargs=2, metavar=("ORIGINAL", "KEYED"),
                    help="author's literal notes vs the same text with notes turned into [@key] citations")
    ap.add_argument("--refs", action="append", help="CSL-JSON; repeat for srom-tlumacz's <id>_refs_tlum.json")
    a = ap.parse_args()
    errs, warns = [], []
    refs = load_refs(a.refs, errs) if a.refs else None
    if a.keyed:
        if not a.refs:
            ap.error("--keyed needs --refs")
        e = []
        check_single(a.keyed[1], refs, e, warns)
        errs += [f"[keyed] {x}" for x in e]
        merged = os.path.join(tempfile.mkdtemp(), "refs.json")
        json.dump(list(refs.values()), open(merged, "w", encoding="utf-8"), ensure_ascii=False)
        check_keyed(a.keyed[0], a.keyed[1], merged, errs, warns)
    elif a.pair:
        for p in a.pair:
            e = []
            check_single(p, refs, e, warns)
            errs += [f"[{p}] {x}" for x in e]
        check_pair(a.pair[0], a.pair[1], errs, warns, refs)
    elif a.md:
        n, keys = check_single(a.md, refs, errs, warns)
        print(f"notes: {n} · citations: {len(keys)} ({len(set(keys))} distinct keys)")
    else:
        ap.error("give a file or --pair")
    for w in warns: print("WARN  " + w)
    for e in errs: print("ERROR " + e)
    print("CHECK OK" if not errs else f"CHECK FAIL {len(errs)} error(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
