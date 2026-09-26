#!/usr/bin/env python3
"""
pdf_extract.py — born-digital article PDF -> SROM-MD source for translation (no OCR).

    python3 pdf_extract.py article.pdf -o article_src.md [--pages 3-24]

What it recovers, and how:
  italics            font name (Italic/Oblique/-It) or italic flag            -> *…*
  note markers       small raised digits in the text (or superscript flag)     -> [^n]
  footnotes          bottom-of-page zone in the note font size (separator rule
                     if drawn), each note starting with its number; a zone that
                     starts without a number continues the previous note        -> [^n]: … after its paragraph
  paragraphs         first-line indent, short last line, vertical gap
  headings           bold or larger font, standalone line(s)                   -> # / ##  (verify levels)
  block quotes       smaller font or indented both sides, outside the note zone -> >
  headers/footers    page numbers and lines repeating across pages             -> dropped (listed)
  line-end hyphens   joined ("Ro-/mani" -> "Romani"); kept after prefixes such as
                     self-/non-/post-; every join listed for proofreading
Report: <out>_extract.md with note/marker contiguity, joins, dropped lines, warnings.
Last line: EXTRACT OK / EXTRACT CHECK n issue(s)   (issues = broken note sequence, unmatched
markers/notes, multi-column pages, non-digit superscripts — fix before translating).
Limits: single-column text flow; scanned PDFs need OCR first; tables/figures are not rebuilt.
"""
import argparse, re, sys
from collections import Counter, defaultdict

import pymupdf

NOTES_RX = re.compile(r"(?i)^(notes|endnotes|przypisy|anmerkungen|notes and references)$")
BIB_RX = re.compile(r"(?i)^(\d+\.\s*)?(references|bibliography|works cited|literature|literatura|bibliografia|sources|źródła|literaturverzeichnis)$")
KEEP_HYPHEN_PREFIXES = {"self", "non", "anti", "post", "pre", "co", "well", "cross", "semi", "quasi", "neo", "pan",
                        "pro", "ex", "inter", "intra", "multi", "trans", "ultra", "counter", "mid", "socio",
                        "post", "euro", "afro", "indo", "anglo", "franco", "polish", "roma", "sinti"}
TEXT_FLAGS = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP  # ligatures expanded


def is_italic(sp):
    f = sp["font"].lower()
    return bool(sp["flags"] & 2) or "italic" in f or "oblique" in f or re.search(r"[-,](it|ital|bi|boldit)\b", f) is not None


def is_bold(sp):
    f = sp["font"].lower()
    return bool(sp["flags"] & 16) or "bold" in f or "black" in f or "semibold" in f


class Line:
    def __init__(self, spans, page):
        self.spans = spans              # dicts with text, size, font, flags, x0, x1, y (baseline), sup
        self.page = page
        base = [s for s in spans if not s["sup"]] or spans
        self.size = Counter(round(s["size"], 1) for s in base for _ in s["text"]).most_common(1)[0][0]
        self.y = min(s["y"] for s in base)
        self.x0 = min(s["x0"] for s in spans)
        self.x1 = max(s["x1"] for s in spans)
        self.text = "".join(s["text"] for s in spans)
        self.bold = all(is_bold(s) for s in spans if s["text"].strip())
        self.zone = "body"

    def __repr__(self):
        return f"<p{self.page} y{self.y:.0f} {self.size} {self.zone} {self.text[:40]!r}>"


def page_lines(page, W):
    raw = []
    d = page.get_text("dict", flags=TEXT_FLAGS)
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                if not sp["text"]:
                    continue
                raw.append({"text": sp["text"], "size": sp["size"], "font": sp["font"], "flags": sp["flags"],
                            "x0": sp["bbox"][0], "x1": sp["bbox"][2], "y": sp["origin"][1], "top": sp["bbox"][1], "sup": False})
    if not raw:
        return []
    # cluster by baseline; then attach small raised spans (markers) to the line they sit on
    raw.sort(key=lambda s: (round(s["y"], 1), s["x0"]))
    lines = []
    for s in sorted(raw, key=lambda s: s["y"]):
        for ln in lines[-4:]:
            if abs(ln[0]["y"] - s["y"]) < 1.2:
                ln.append(s)
                break
        else:
            lines.append([s])
    out = lines
    # attach lines consisting solely of small digits to the following/preceding line with baseline within 0.6 size
    final = []
    for ln in out:
        txt = "".join(s["text"] for s in ln).strip()
        if re.fullmatch(r"[\d*†‡,\s]+", txt) and final:
            host = None
            for cand in reversed(final[-3:]):
                cs = max(s["size"] for s in cand)
                if 0 < cand[0]["y"] - ln[0]["y"] < 0.7 * cs and ln[0]["size"] < 0.8 * cs:
                    host = cand
                    break
            if host is None:
                # marker line may come before its host line in baseline order (raised = smaller y)
                final.append(ln)
                continue
            host.extend(ln)
            continue
        final.append(ln)
    # second chance for marker lines that preceded their host
    res = []
    for ln in final:
        txt = "".join(s["text"] for s in ln).strip()
        if res and re.fullmatch(r"[\d*†‡,\s]+", "".join(s["text"] for s in res[-1]).strip()):
            prev = res[-1]
            ps = prev[0]["size"]
            cs = max(s["size"] for s in ln)
            if 0 < ln[0]["y"] - prev[0]["y"] < 0.7 * cs and ps < 0.8 * cs:
                res[-1] = prev + ln
                continue
        res.append(ln)
    lines_obj = []
    for ln in res:
        ln.sort(key=lambda s: s["x0"])
        mx = Counter(round(s["size"], 1) for s in ln for _ in s["text"]).most_common(1)[0][0]
        base_y = max(s["y"] for s in ln if abs(s["size"] - mx) < 0.5) if any(abs(s["size"] - mx) < 0.5 for s in ln) else ln[0]["y"]
        for s in ln:
            s["sup"] = bool(s["flags"] & 1) or (s["size"] < 0.8 * mx and s["y"] < base_y - 0.12 * mx)
        lines_obj.append(Line(ln, page.number + 1))
    lines_obj.sort(key=lambda L: (L.y, L.x0))
    return lines_obj


def span_md(spans, for_note=False):
    """spans -> text with *italics* and [^n] markers; returns (text, markers, oddsups)"""
    parts, markers, odd = [], [], []
    for s in spans:
        t = s["text"]
        if s["sup"]:
            st = t.strip()
            if re.fullmatch(r"\d{1,3}", st):
                parts.append(("m", st))
                markers.append(int(st))
                continue
            odd.append(st)
        parts.append(("i" if is_italic(s) and t.strip() else "r", t))
    out = []
    for kind, t in parts:
        if kind == "m":
            out.append(f"[^{t}]")
        elif kind == "i":
            lead = t[:len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            out.append(f"{lead}*{t.strip()}*{trail}")
        else:
            out.append(t)
    txt = "".join(out)
    txt = re.sub(r"\*(\s*)\*", r"\1", txt)          # adjacent italic runs
    return txt, markers, odd


def left_margin(counter):
    """leftmost x where lines start repeatedly (first-line indents and quotations start further right)"""
    n = sum(counter.values())
    common = [x for x, c in counter.items() if c >= max(2, 0.15 * n)]
    return min(common) if common else min(counter)


def join_lines(texts, joins):
    """join line texts of one paragraph; line-end hyphenation removed and logged"""
    out = ""
    for t in texts:
        t = t.strip()
        if not out:
            out = t
            continue
        m = re.search(r"([\w’']+)[-\u00ad](\**)$", out)
        nxt = re.match(r"(\**)([a-ząćęłńóśźżäöüéèáíúčšž][\w’']*)", t)
        if m and nxt:
            frag = m.group(1)
            if frag.lower() in KEEP_HYPHEN_PREFIXES:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}-{nxt.group(2)} (hyphen kept after prefix)")
                out = out + t
            else:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}{nxt.group(2)}")
                out = out[:m.start(0)] + frag + m.group(2) + t
            continue
        if re.search(r"\d–\**$", out) and re.match(r"\**\d", t):   # 1939–|1945
            out = out + t
            continue
        out = out + " " + t
    out = re.sub(r"\*(\s*)\*", r"\1", out)
    out = re.sub(r"[ \u00a0]{2,}", " ", out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--pages", help="e.g. 3-24 (1-based, inclusive)")
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    p0, p1 = 1, doc.page_count
    if a.pages:
        p0, p1 = [int(x) for x in a.pages.split("-")]
    pages = [doc[i] for i in range(p0 - 1, p1)]
    issues, warns, dropped, joins = [], [], [], []

    all_lines = {}
    for pg in pages:
        all_lines[pg.number + 1] = page_lines(pg, pg.rect.width)
    if not any(all_lines.values()):
        sys.exit("no text layer — scanned PDF? run OCR first")
    chars = Counter()
    for L in (l for ls in all_lines.values() for l in ls):
        chars[L.size] += len(L.text)
    B = chars.most_common(1)[0][0]

    # headers / footers
    rep = Counter()
    for pno, ls in all_lines.items():
        H = doc[pno - 1].rect.height
        for L in ls:
            if L.y < 0.09 * H or L.y > 0.92 * H:
                rep[re.sub(r"\d+", "#", L.text.strip())] += 1
    n_pages = len(all_lines)
    for pno, ls in all_lines.items():
        H = doc[pno - 1].rect.height
        keep = []
        for L in ls:
            key = re.sub(r"\d+", "#", L.text.strip())
            edge = L.y < 0.09 * H or L.y > 0.92 * H
            if edge and (re.fullmatch(r"[#\s–-]*", key) or (n_pages > 2 and rep[key] >= max(2, 0.4 * n_pages))):
                dropped.append(f"p{pno}: {L.text.strip()[:60]}")
                continue
            keep.append(L)
        all_lines[pno] = keep

    # note font size: most common size below body size among bottom-of-page lines
    small = Counter()
    for pno, ls in all_lines.items():
        H = doc[pno - 1].rect.height
        for L in ls:
            if L.size < 0.95 * B and L.y > 0.4 * H:
                small[L.size] += len(L.text)
    N = small.most_common(1)[0][0] if small else None

    # footnote zones
    for pno, ls in all_lines.items():
        if N is None or not ls:
            continue
        page = doc[pno - 1]
        rules = []
        try:
            for dr in page.get_drawings():
                r = dr.get("rect")
                if r and r.height < 2.5 and 20 < r.width < 0.6 * page.rect.width:
                    rules.append(r.y0)
        except Exception:
            pass
        i = len(ls)
        while i > 0 and abs(ls[i - 1].size - N) < 0.35:
            i -= 1
        suffix = ls[i:]
        if not suffix:
            continue
        below_rule = [r for r in rules if r < suffix[0].y + 1 and (i == 0 or r > ls[i - 1].y - 1)]
        top = 0
        if not below_rule:
            # trim from the top until a line that starts a note (or the zone continues a note from the previous page)
            while top < len(suffix) and not re.match(r"^\s*\d{1,3}(?:[.)]?\s|\s?[A-ZŁŚŻŹĆ„\"(*])", suffix[top].text) \
                    and not suffix[top].spans[0]["sup"]:
                top += 1
            if top == len(suffix):
                continue
        for L in suffix[top:]:
            L.zone = "note"

    # column sanity
    for pno, ls in all_lines.items():
        body = [L for L in ls if L.zone == "body" and abs(L.size - B) < 0.35]
        if len(body) > 8:
            xs = sorted(L.x0 for L in body)
            W = doc[pno - 1].rect.width
            if xs[-1] - xs[0] > 0.35 * W and sum(1 for x in xs if x > xs[0] + 0.35 * W) > 3:
                issues.append(f"page {pno}: text starts at very different x positions — two columns? reading order must be verified")

    # endnotes: a heading "Notes"/"Endnotes"/"Przypisy" turns the following lines (to the next heading) into the note zone
    endnote_mode = False
    for pno, ls in all_lines.items():
        for L in ls:
            if L.zone != "body":
                continue
            heading = L.size > B * 1.1 or (L.bold and len(L.text) < 120)
            if heading and NOTES_RX.match(L.text.strip()):
                endnote_mode = True
                L.zone = "drop"
                warns.append(f"endnotes section found on page {pno} — parsed as notes")
                continue
            if heading and endnote_mode:
                endnote_mode = False
            if endnote_mode:
                L.zone = "note"

    # ---------- notes
    # How are note numbers set in this PDF: raised (superscript) or on the baseline ("12. …")?
    # Decide once for the whole document, so that a continuation line beginning with a number
    # ("12 marca 1937 …") is never taken for the start of note 12.
    sup_starts = txt_starts = 0
    for ls in all_lines.values():
        for L in ls:
            if L.zone != "note":
                continue
            if L.spans[0]["sup"] and re.fullmatch(r"\s*\d{1,3}\s*", L.spans[0]["text"]):
                sup_starts += 1
            elif re.match(r"^\s*\d{1,3}[.)]?\s", L.text):
                txt_starts += 1
    raised_numbers = sup_starts > 0 and sup_starts >= txt_starts
    notes = {}
    order, cur = [], None
    for pno, ls in all_lines.items():
        first_in_zone = True
        for L in (x for x in ls if x.zone == "note"):
            spans = list(L.spans)
            m_sup = spans[0]["sup"] and re.fullmatch(r"\s*\d{1,3}\s*", spans[0]["text"])
            m_txt = re.match(r"^\s*(\d{1,3})(?:[.)]?\s+)", L.text)
            num = None
            if m_sup:
                num = int(spans[0]["text"])
                spans = spans[1:]
            elif m_txt and not raised_numbers and (not cur or int(m_txt.group(1)) == (cur + 1)):
                num = int(m_txt.group(1))
                cut = len(m_txt.group(0))
                ns = []
                for s in spans:
                    if cut >= len(s["text"]):
                        cut -= len(s["text"])
                        continue
                    s = dict(s, text=s["text"][cut:])
                    cut = 0
                    ns.append(s)
                spans = ns
            txt, mk, odd = span_md(spans, True)
            if odd:
                warns.append(f"page {pno}: superscript text in a note kept as plain: {odd}")
            if num is not None:
                if num in notes:
                    issues.append(f"note {num} starts twice (page {pno})")
                cur = num
                notes[num] = [txt]
                order.append(num)
            elif cur is None:
                issues.append(f"page {pno}: note-zone text before any numbered note: {L.text[:50]!r}")
            else:
                if first_in_zone:
                    warns.append(f"note {cur} continues on page {pno}")
                notes[cur].append(txt)
            first_in_zone = False

    # ---------- body paragraphs
    body_lines = [L for pno in all_lines for L in all_lines[pno] if L.zone == "body"]
    lefts = defaultdict(Counter)
    rights = defaultdict(Counter)
    for L in body_lines:
        if abs(L.size - B) < 0.35:
            lefts[L.page][round(L.x0)] += 1
            rights[L.page][round(L.x1)] += 1
    head_sizes = sorted({L.size for L in body_lines if L.size > B * 1.1}, reverse=True)
    paras = []          # [kind, [texts], markers, x0]
    prev = None
    bib_mode = False
    for L in body_lines:
        Lm = left_margin(lefts[L.page]) if lefts[L.page] else L.x0
        Rm = max(rights[L.page]) if rights[L.page] else L.x1
        if L.size > B * 1.1 or (L.bold and len(L.text) < 120):
            # largest heading size -> level 1; any other larger size or bold body-size line -> level 2 (verify)
            kind = "h1" if head_sizes and L.size >= head_sizes[0] - 0.1 else "h2"
            bib_mode = bool(BIB_RX.match(L.text.strip()))
        elif L.size < B * 0.95 and not bib_mode:
            kind = "q"
        else:
            kind = "p"
        new = True
        if prev is not None and paras:
            pk = paras[-1][0]
            gap = L.y - prev.y if L.page == prev.page else None
            lead = 1.25 * max(L.size, prev.size)
            if kind == pk and kind.startswith("h"):
                new = gap is None or gap > 1.9 * lead
            elif kind == pk and bib_mode:
                # reference list with hanging indent: a flush-left line starts a new entry
                new = L.x0 <= Lm + 0.3 * L.size or (gap is not None and gap > 1.6 * lead)
            elif kind == pk:
                prev_short = prev.x1 < Rm - 2.5 * prev.size
                indented = L.x0 > Lm + 0.6 * L.size if kind == "p" else L.x0 > paras[-1][3] + 0.6 * L.size
                if indented and abs(L.x0 - prev.x0) < 2 and prev.x0 > Lm + 2.2 * L.size:
                    indented = prev_short = False   # block indented >= 2 em (same-size quotation): continuation
                big_gap = gap is not None and gap > 1.6 * lead
                new = indented or prev_short or big_gap
        if new:
            paras.append([kind, [], [], L.x0, bib_mode and kind == "p"])
        txt, mk, odd = span_md(L.spans)
        if odd:
            warns.append(f"page {L.page}: superscript text kept as plain: {odd}")
        paras[-1][1].append(txt)
        paras[-1][2].extend(mk)
        paras[-1].append((L.x0, L.x1, Lm, Rm, L.size))
        prev = L
    # same-size quotations: >= 2 lines, all indented left, all but the last short of the right margin
    for P in paras:
        geo = P[5:]
        if P[0] == "p" and not P[4] and len(geo) >= 2 and all(x0 > lm + 2.2 * sz for x0, x1, lm, rm, sz in geo) \
                and all(x1 < rm - 0.8 * sz for x0, x1, lm, rm, sz in geo[:-1]):
            P[0] = "q"

    # ---------- assemble
    out, seen_markers = [], []
    bib_entries = []
    for kind, texts, mks, _, is_bib, *geo in paras:
        if is_bib:
            bib_entries.append(join_lines(texts, joins).replace("*", ""))
        t = join_lines(texts, joins)
        if kind == "h1":
            out.append("# " + t)
        elif kind == "h2":
            out.append("## " + t)
        elif kind == "q":
            out.append("> " + t)
        else:
            out.append(t)
        out.append("")
        for n in mks:
            seen_markers.append(n)
            if n in notes:
                out += [f"[^{n}]: " + join_lines(notes[n], joins), ""]
    md = "\n".join(out).rstrip() + "\n"

    # ---------- integrity
    exp = list(range(1, len(order) + 1))
    if order != exp and order:
        issues.append(f"note numbers not contiguous from 1: {order}")
    if seen_markers != sorted(seen_markers) or len(set(seen_markers)) != len(seen_markers):
        issues.append(f"marker sequence out of order / duplicated: {seen_markers}")
    miss_def = sorted(set(seen_markers) - set(notes))
    miss_mark = sorted(set(notes) - set(seen_markers))
    if miss_def:
        issues.append(f"markers without a footnote: {miss_def}")
    if miss_mark:
        issues.append(f"footnotes without a marker in the text: {miss_mark}")
        for n in miss_mark:
            md += f"\n[^{n}]: " + join_lines(notes[n], joins) + "\n"

    open(a.out, "w", encoding="utf-8").write(md)
    if bib_entries:
        bp = a.out.rsplit(".", 1)[0] + "_bib.txt"
        open(bp, "w", encoding="utf-8").write("\n".join(bib_entries) + "\n")
        warns.append(f"reference list: {len(bib_entries)} entries written to {bp} (input for refs.json + cite_map audit)")
    ital = len(re.findall(r"\*[^*]+\*", md))
    repp = a.out.rsplit(".", 1)[0] + "_extract.md"
    rep = [f"# PDF extraction — {a.pdf} (pages {p0}–{p1})", "",
           f"- body size {B} pt · note size {N} pt · paragraphs {sum(1 for p in paras if p[0] in ('p', 'q'))} · headings {sum(1 for p in paras if p[0].startswith('h'))}",
           f"- footnotes {len(notes)} · markers {len(seen_markers)} · italic runs {ital}", "",
           "## Issues (fix before translating)"] + ([f"- {x}" for x in issues] or ["- none"])
    rep += ["", "## Warnings"] + ([f"- {x}" for x in warns] or ["- none"])
    rep += ["", "## Line-end hyphen joins (proofread)"] + ([f"- {x}" for x in joins] or ["- none"])
    rep += ["", "## Dropped running heads / page numbers"] + ([f"- {x}" for x in dropped] or ["- none"])
    open(repp, "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print(f"notes {len(notes)} · markers {len(seen_markers)} · italics {ital} · joins {len(joins)} · report {repp}")
    print("EXTRACT OK" if not issues else f"EXTRACT CHECK {len(issues)} issue(s)")
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
