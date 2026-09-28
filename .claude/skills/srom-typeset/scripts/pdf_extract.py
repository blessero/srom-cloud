#!/usr/bin/env python3
"""
pdf_extract.py — born-digital article PDF -> SROM-MD source for translation (no OCR).

    python3 pdf_extract.py article.pdf -o article_src.md [--pages 3-24]

What it recovers, and how:
  italics            font name (Italic/Oblique/-It, or a style suffix .I/.BI on obfuscated names) or flag -> *…*
  note markers       small raised digits in the text (or superscript flag), also bracketed "[12]" -> [^n]
  footnotes          bottom-of-page zone in the note font size (the size under the separator rule if one is
                     drawn, else the commonest small size low on the page), each note starting with its number
                     (raised, or just set smaller);
                     a zone that starts without a number continues the previous note -> [^n]: … after its paragraph
  raised line parts  a note number with the first words on a raised baseline, a superscript (XVIIᵉ): merged into
                     their line when nothing overlaps horizontally (else "35" | "–69" would split)
  title note         page 1: an unnumbered block at the foot, clear of the body   -> ::: przypis-tytulowy (listed)
  front matter       page 1 above the first text line (title in larger type, author, abstract) -> <out>_front.md,
                     not the text (SROM-MD has no header; Kanon § 13.3); with an "Abstract"/"Keywords" heading in
                     the first pages, everything up to the next heading (title/bio page, keywords box in a column)
  paragraphs         first-line indent, short last line, vertical gap; a paragraph interrupted by a figure
                     caption is rejoined, the caption placed after it
  headings           larger font, bold, or in capitals after a gap (also when smaller than the body) -> # / ##
  opening small caps "THIS ESSAY BEGINS in …" -> "This essay begins in …" (listed: check proper names)
  block quotes       smaller font, indented both sides, or every line at one left indent, outside the note zone -> >
  verse              >= 3 one-line quotation paragraphs at the same indent        -> one > quotation, line breaks kept
  captions           "Figure 1." / "Rycina 1." … -> ::: podpis; "Table 1." … -> ::: tabela-tytul
  reference list     after a heading "Bibliography"/"References"/… (any size): hanging indent -> one entry per
                     line in <out>_bib.txt; taken out of the text (decision 19); a repeated-author dash (typed, or
                     drawn as a rule) takes the author of the entry above (listed)
  headers/footers    page numbers and lines repeating across pages             -> dropped (listed)
  line-end hyphens   joined ("Ro-/mani" -> "Romani"); the document decides where it can (the joined or the
                     hyphenated word found inside a line elsewhere), else kept after prefixes such as
                     self-/non-/post- and flagged; before a capital (anti-|Roma) kept; a slash at a line end joined
                     without a space; a URL broken inside a token joined when a link target has it whole;
                     every join listed for proofreading
Report: <out>_extract.md with note/marker contiguity, joins, dropped lines, warnings.
Last line: EXTRACT OK / EXTRACT CHECK n issue(s)   (issues = broken note sequence, unmatched
markers/notes, multi-column pages, non-digit superscripts — fix before translating).
Limits: single-column text flow; scanned PDFs need OCR first; tables/figures are not rebuilt.
"""
import argparse, re, sys, unicodedata
from collections import Counter, defaultdict

import pymupdf

NOTES_RX = re.compile(r"(?i)^(notes|endnotes|przypisy|anmerkungen|notes and references)$")
FRONT_RX = re.compile(r"(?i)^(abstract|summary|keywords|key words|streszczenie|słowa kluczowe|résumé|mots[- ]clés|zusammenfassung|schlagwörter|schlüsselwörter)$")
BIB_RX = re.compile(r"(?i)^(\d+\.\s*)?(references|bibliography|works cited|literature|literatura|bibliografia|sources|źródła|literaturverzeichnis)$")
KEEP_HYPHEN_PREFIXES = {"self", "non", "anti", "post", "pre", "co", "well", "cross", "semi", "quasi", "neo", "pan",
                        "pro", "ex", "inter", "intra", "multi", "trans", "ultra", "counter", "mid", "socio",
                        "post", "euro", "afro", "indo", "anglo", "franco", "polish", "roma", "sinti"}
CAPTION_RX = re.compile(r"^\**(?:(Figure|Fig\.|Plate|Illustration|Rycina|Ryc\.|Ilustracja|Fot\.|Abb\.|Abbildung)|(Table|Tabela|Tab\.|Tabelle))\**\s*\d+[.:]")
LINKS = set()       # URI targets of the PDF's link annotations: what a click opens, the authority for URL text
VOCAB = set()       # words (lowercase, hyphenated ones too) that occur inside lines of the document being read
TEXT_FLAGS = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP  # ligatures expanded


def is_italic(sp):
    f = sp["font"].lower()
    return bool(sp["flags"] & 2) or "italic" in f or "oblique" in f or re.search(r"[-,](it|ital|bi|boldit)\b", f) is not None \
        or re.search(r"\.b?i(\+\w+)?$", f) is not None     # obfuscated names with a style suffix: AdvOTa14f9db0.I(+20)


def is_bold(sp):
    f = sp["font"].lower()
    return bool(sp["flags"] & 16) or "bold" in f or "black" in f or "semibold" in f or re.search(r"\.bi?(\+\w+)?$", f) is not None


class Line:
    def __init__(self, spans, page):
        self.spans = spans              # dicts with text, size, font, flags, x0, x1, y (baseline), sup
        self.page = page
        base = [s for s in spans if not s["sup"]] or spans
        self.size = Counter(round(s["size"], 1) for s in base for _ in s["text"]).most_common(1)[0][0]
        main = [s for s in base if abs(round(s["size"], 1) - self.size) < 0.5]
        self.y = max(s["y"] for s in main) if main else min(s["y"] for s in base)   # baseline, not a raised part
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
        if re.fullmatch(r"[\d*†‡,\s\[\]]+", txt) and final:
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
        if res and re.fullmatch(r"[\d*†‡,\s\[\]]+", "".join(s["text"] for s in res[-1]).strip()):
            prev = res[-1]
            ps = prev[0]["size"]
            cs = max(s["size"] for s in ln)
            if 0 < ln[0]["y"] - prev[0]["y"] < 0.7 * cs and ps < 0.8 * cs:
                res[-1] = prev + ln
                continue
        res.append(ln)
    res = merge_raised(res)
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


def note_number(L):
    """the line opens with a note number set small: raised, or just smaller than the line (some typesetters put the
    number and the whole first line on one baseline). A full-size number opening a line ("12 marca 1937") is not one."""
    s = L.spans[0]
    return bool(re.fullmatch(r"\s*\d{1,3}\s*", s["text"])) and (s["sup"] or s["size"] < 0.8 * L.size)


def caps_line(L, B):
    """a line set in capitals (letters, no lowercase) at about body size, not ending like a sentence part:
    a section heading in journals that set headings in caps or small caps at or below the body size"""
    t = L.text.strip()
    letters = [c for c in t if c.isalpha()]
    return len(letters) >= 3 and not any(c.islower() for c in letters) and L.size >= 0.9 * B and len(t) < 120 \
        and not re.search(r"[.,;]\**$", t)


def merge_raised(lines):
    """A cluster sitting less than 0.6 of the next line's size above it, with no span overlapping that line's
    spans horizontally, is a raised part of that line, not a line of its own: a note number set with the first
    words of the note on a raised baseline ("40 Vallée, 45:" above "“Il se noircit…"), a superscript ("XVIIᵉ").
    Real lines are a full leading apart and overlap horizontally; a line of another column is far to the side."""
    lines = sorted(lines, key=lambda ln: min(s["y"] for s in ln))
    out = []
    for i, ln in enumerate(lines):
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            dy = min(s["y"] for s in nxt) - max(s["y"] for s in ln)
            ink = lambda l: [s for s in l if s["text"].strip()]
            overlap = any(a["x0"] < b["x1"] - 0.5 and b["x0"] < a["x1"] - 0.5 for a in ink(ln) for b in ink(nxt))
            # and it sits next to that line's text, not a column away (a keywords box beside an abstract)
            sz = max(s["size"] for s in nxt)
            near = any(max(b["x0"] - a["x1"], a["x0"] - b["x1"]) < 1.5 * sz for a in ink(ln) for b in ink(nxt))
            if 0 < dy < 0.6 * sz and not overlap and near:
                nxt[:0] = ln
                continue
        out.append(ln)
    return out


def span_md(spans, for_note=False):
    """spans -> text with *italics* and [^n] markers; returns (text, markers, oddsups)"""
    parts, markers, odd = [], [], []
    for s in spans:
        t = s["text"]
        if s["sup"]:
            st = t.strip()
            mm = re.fullmatch(r"(\d{1,3})|\[(\d{1,3})\]", st)      # 12, or bracketed [12] (Critical Romani Studies)
            if mm:
                n = mm.group(1) or mm.group(2)
                parts.append(("m", n))
                markers.append(int(n))
                continue
            if st:
                odd.append(st)
                if len(parts) >= 2 and parts[-1][0] == "r" and not parts[-1][1].strip():
                    parts.pop()        # kerning space before a raised letter: "XVII" " " "e" -> XVIIe
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
        if re.search(r"(?:https?://|www\.)\S*$", out) and re.search(r"[-/._=?&#~]\**$", out):
            if out.endswith("-"):      # the URL's own hyphen, or the typesetter's (laviedesi-|dees)? the link decides
                head = re.search(r"(?:https?://|www\.)\S*$", out).group(0)
                tail = re.match(r"\S*", t).group(0).rstrip(".,;:)”’")
                if any(u.startswith(head[:-1] + tail) for u in LINKS):
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen removed (link target)")
                    out = out[:-1]
                elif any(u.startswith(head + tail) for u in LINKS):
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen kept (link target)")
                else:
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen kept, no link in the PDF — check the address")
            out = out + t              # a URL broken at the line end: no space inside it (Kanon § 8.6)
            continue
        um = re.search(r"(?:https?://|www\.)\S*$", out)
        if um and t and any(u.startswith(um.group(0) + re.match(r"\S*", t).group(0).rstrip(".,;:)”’")) for u in LINKS):
            joins.append(f"URL {um.group(0)[-25:]}|{t[:25]} -> joined (link target)")   # broken inside a token, no hyphen
            out = out + t
            continue
        m = re.search(r"([\w’']+)[-\u00ad](\**)$", out)
        nxt = re.match(r"(\**)([a-ząćęłńóśźżäöüéèáíúčšž][\w’']*)", t)
        if m and nxt:
            frag = m.group(1)
            whole, hyph = (frag + nxt.group(2)).lower(), (frag + "-" + nxt.group(2)).lower()
            # evidence from the document itself (words inside lines) beats the prefix list
            keep = hyph in VOCAB if (whole in VOCAB) != (hyph in VOCAB) else frag.lower() in KEEP_HYPHEN_PREFIXES
            why = "found in the text" if (whole in VOCAB) != (hyph in VOCAB) else \
                "prefix, not found in the text — check" if keep else ""
            if keep:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}-{nxt.group(2)} (hyphen kept: {why})")
                out = out + t
            else:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}{nxt.group(2)}"
                             + (f" (prefix, but {why})" if frag.lower() in KEEP_HYPHEN_PREFIXES else ""))
                out = out[:m.start(0)] + frag + m.group(2) + t
            continue
        if re.search(r"[^\W\d_]-\**$", out) and re.match(r"[\*“‘\"(]*[A-ZÀ-ÞĄĆĘŁŃÓŚŹŻČŠŽ]", t):   # anti-|Roma, Polish-|Lithuanian
            joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> hyphen kept (capital follows)")
            out = out + t
            continue
        if re.search(r"[^\W\d_”’]/\**$", out) and re.match(r"\**[^\W\d_]", t):   # police/|carceral: no space after a slash at a line end
            joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> joined at the slash")
            out = out + t
            continue
        if re.search(r"\d–\**$", out) and re.match(r"\**\d", t):   # 1939–|1945
            out = out + t
            continue
        if re.search(r"—\**$", out) or re.match(r"\**—", t):          # closed em dash at a line end: intrigue”—|and
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

    for pg in pages:
        LINKS.update(l["uri"] for l in pg.get_links() if l.get("uri"))
    for L in (l for ls in all_lines.values() for l in ls):
        VOCAB.update(w.lower() for w in re.findall(r"[^\W\d_][\w’']*(?:-[^\W\d_][\w’']*)*", re.sub(r"\S+-\s*$", "", L.text)))

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

    # short horizontal rules: a note separator, or a drawn repeated-author rule opening a reference-list line
    # ("———. 2008." set as a line, not as glyphs): the rule ends where the line's text begins, on its baseline
    rules_at = {}
    for pno, ls in all_lines.items():
        page = doc[pno - 1]
        rules_at[pno] = []
        try:
            drs = page.get_drawings()
        except Exception:
            drs = []
        for dr in drs:
            r = dr.get("rect")
            if not (r and r.height < 2.5 and 8 < r.width < 0.6 * page.rect.width):
                continue
            host = next((L for L in ls if abs(L.x0 - r.x1) < 3 and 0 <= L.y - r.y1 < 0.6 * L.size), None)
            if host is not None and r.width < 12 * host.size:
                host.spans.insert(0, dict(host.spans[0], text="———", font="rule", x0=r.x0, x1=r.x1, sup=False, flags=0))
                host.x0, host.text = r.x0, "———" + host.text
                warns.append(f"page {pno}: drawn rule before {host.text[3:30]!r} -> ——— (repeated author)")
            elif r.width >= 20:
                rules_at[pno].append(r.y0)

    # note font size: the size of the lines right under a note separator; else the most common size below
    # the body size among bottom-of-page lines (a reference list set between the two must not win)
    under = Counter()
    for pno, ls in all_lines.items():
        for y in rules_at[pno]:
            L = next((L for L in ls if L.y - L.size > y), None)
            if L is not None and L.size < 0.95 * B and L.y - y < 3 * B:
                under[L.size] += 1
    small = Counter()
    for pno, ls in all_lines.items():
        H = doc[pno - 1].rect.height
        for L in ls:
            if L.size < 0.95 * B and L.y > 0.4 * H:
                small[L.size] += len(L.text)
    N = under.most_common(1)[0][0] if under else small.most_common(1)[0][0] if small else None

    # footnote zones
    for pno, ls in all_lines.items():
        if N is None or not ls:
            continue
        rules = rules_at[pno]
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
                    and not note_number(suffix[top]):
                top += 1
            # first page: an unnumbered block in the note zone, well clear of the body above it, is the author's
            # note on the title (acknowledgements) -> ::: przypis-tytulowy (Kanon § 7.1)
            if top and pno == p0 and i > 0 and suffix[0].y - ls[i - 1].y > 1.9 * 1.25 * B:
                for L in suffix[:top]:
                    L.zone = "title"
            if top == len(suffix):
                continue
        zone = suffix[top:]
        for j, L in enumerate(zone):
            L.zone = "note"
            # a block set well apart below the notes (licence, DOI, copyright line) is not part of the last note
            if j and L.y - zone[j - 1].y > 2.2 * 1.25 * N:
                for F in zone[j:]:
                    F.zone = "foot"
                break

    # column sanity (reported once the front matter is known: columns there are read in column order)
    col_pages = []
    for pno, ls in all_lines.items():
        body = [L for L in ls if L.zone == "body" and abs(L.size - B) < 0.35]
        if len(body) > 8:
            xs = sorted(L.x0 for L in body)
            W = doc[pno - 1].rect.width
            if xs[-1] - xs[0] > 0.35 * W and sum(1 for x in xs if x > xs[0] + 0.35 * W) > 3:
                col_pages.append(pno)

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
            if note_number(L):
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
            m_sup = note_number(L)
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

    foot = [L for pno in all_lines for L in all_lines[pno] if L.zone == "foot"]
    for L in foot:
        dropped.append(f"p{L.page}: {L.text.strip()[:60]} (set apart below the notes)")

    # ---------- body paragraphs
    body_lines = [L for pno in all_lines for L in all_lines[pno] if L.zone == "body"]
    title_note = [L for pno in all_lines for L in all_lines[pno] if L.zone == "title"]
    lefts = defaultdict(Counter)
    rights = defaultdict(Counter)
    for L in body_lines:
        if abs(L.size - B) < 0.35:
            lefts[L.page][round(L.x0)] += 1
            rights[L.page][round(L.x1)] += 1

    # headings: larger than the body, bold, or in capitals after a gap (or under another line in capitals)
    prev = None
    for L in body_lines:
        gap = L.y - prev.y if prev is not None and L.page == prev.page else None
        L.caps_head = caps_line(L, B) and (gap is None or gap > 1.5 * 1.25 * B or prev.caps_head)
        L.head = L.size > B * 1.1 or (L.bold and len(L.text) < 120) or L.caps_head
        prev = L

    # front matter: first-page lines above the first body-size text line, when a title (larger type) is among
    # them; a heading right above the text stays. Not part of SROM-MD (title, author, abstract come from the CSV).
    front = []
    first = [L for L in body_lines if L.page == p0]
    k = next((j for j, L in enumerate(first) if abs(L.size - B) < 0.35 and not L.head), None)
    if k:
        cand = first[:k]
        tsize = max(L.size for L in cand)
        if tsize > B * 1.1:
            while cand and cand[-1].head and cand[-1].size < tsize - 0.1:
                cand.pop()
            front = cand
    # an "Abstract"/"Keywords" heading near the start: everything up to the first other heading on that page
    # or the next is front matter too (journals that give pages to title, bio, abstract and keywords before the text)
    fi = next((j for j, L in enumerate(body_lines) if L.head and FRONT_RX.match(L.text.strip()) and L.page < p0 + 3), None)
    if fi is not None:
        last = max(L.page for L in body_lines[fi:] if L.head and FRONT_RX.match(L.text.strip()) and L.page < p0 + 3)
        fe = next((j for j in range(fi + 1, len(body_lines)) if body_lines[j].head
                   and not FRONT_RX.match(body_lines[j].text.strip())), None)
        if fe is not None and body_lines[fe].page <= last + 1:
            front = body_lines[:fe]
            warns.append(f"front matter: pages {p0}–{body_lines[fe - 1].page} up to the heading "
                         f"{body_lines[fe].text.strip()[:40]!r} (abstract/keywords section)")
        else:
            warns.append("an abstract/keywords heading, but no text heading right after it: front matter left in the text — check")
    body_lines = [L for L in body_lines if L not in front]
    for pno in col_pages:
        if any(L.page == pno for L in body_lines):
            issues.append(f"page {pno}: text starts at very different x positions — two columns? reading order must be verified")
        else:
            warns.append(f"page {pno}: two columns in the front matter, read column by column — check the order")
    # reading order in the front matter: a column far right (a keywords box beside the abstract) after the rest of its page
    front.sort(key=lambda L: (L.page, L.x0 > 0.6 * doc[L.page - 1].rect.width, L.y))
    front_md = []
    for j, L in enumerate(front):
        pv = front[j - 1] if j else None
        if pv is None or abs(L.size - pv.size) > 0.35 or L.y - pv.y > 1.6 * 1.25 * L.size or L.page != pv.page \
                or abs(L.x0 - pv.x0) > 0.2 * doc[L.page - 1].rect.width or re.match(r"\s*[•▪■◦·]", L.text):
            front_md.append([])
        front_md[-1].append(re.sub(r"^(\s*[•▪■◦·])\s*", r"\1 ", span_md(L.spans)[0].replace("\t", " ")))
    front_md = [join_lines(x, joins) for x in front_md]
    if front_md and any(L.page == p0 for L in foot):     # page-1 foot block: journal, licence, DOI -> with the front matter
        front_md.append(join_lines([span_md(L.spans)[0] for L in foot if L.page == p0], joins))

    head_sizes = sorted({L.size for L in body_lines if L.size > B * 1.1}, reverse=True)
    any_caps = any(L.caps_head for L in body_lines)
    bib = False
    for L in body_lines:
        if L.head:
            bib = bool(BIB_RX.match(L.text.strip()))
        L.bib = bib and not L.head
    bib_left = {}
    for L in body_lines:
        if L.bib:
            bib_left[L.page] = min(bib_left.get(L.page, L.x0), L.x0)

    paras = []
    prev = None
    for L in body_lines:
        Lm = left_margin(lefts[L.page]) if lefts[L.page] else L.x0
        Rm = max(rights[L.page]) if rights[L.page] else L.x1
        if L.head:
            if L.size > B * 1.1:
                # largest heading size -> level 1; any other larger size -> level 2 (verify)
                kind = "h1" if L.size >= head_sizes[0] - 0.1 else "h2"
            else:
                # bold or capitals at body size: level 2 under larger headings (or under caps headings, if bold);
                # the only kind of heading -> level 1
                kind = "h2" if head_sizes or (any_caps and not L.caps_head) else "h1"
        elif L.size < B * 0.95 and not L.bib:
            kind = "q"
        else:
            kind = "p"
        new, big_gap = True, False
        if prev is not None and paras:
            pk = paras[-1]["kind"]
            gap = L.y - prev.y if L.page == prev.page else None
            lead = 1.25 * max(L.size, prev.size)
            big_gap = gap is not None and gap > 1.6 * lead
            if kind == pk and kind.startswith("h"):
                new = gap is None or gap > 1.9 * lead
            elif kind == pk and L.bib and prev.bib:
                # reference list with hanging indent: a line at the list's left edge starts a new entry
                new = L.x0 <= bib_left[L.page] + 0.3 * L.size or big_gap
            elif kind == pk:
                prev_short = prev.x1 < Rm - 2.5 * prev.size
                indented = L.x0 > Lm + 0.6 * L.size if kind == "p" else L.x0 > paras[-1]["x0"] + 0.6 * L.size
                if indented and abs(L.x0 - prev.x0) < 2 and prev.x0 > Lm + 2.2 * L.size:
                    indented = prev_short = False   # block indented >= 2 em (same-size quotation): continuation
                new = indented or prev_short or big_gap
        spans = L.spans
        if new and kind == "p" and not L.bib:
            # opening words in capitals set smaller than the line (small caps: "THIS ESSAY ORIGINATES in …")
            j = 0
            while j < len(spans) and (not spans[j]["text"].strip() or (spans[j]["size"] < 0.95 * L.size
                                      and not any(c.islower() for c in spans[j]["text"]))):
                j += 1
            lead_txt = "".join(s["text"] for s in spans[:j])
            if 0 < j < len(spans) and sum(c.isupper() for c in lead_txt) >= 2:
                low = lead_txt.lower()
                m = re.search(r"[^\W\d_]", low)
                new_txt = low[:m.start()] + low[m.start()].upper() + low[m.start() + 1:] if m else low
                warns.append(f"page {L.page}: opening words in small capitals retyped: {lead_txt.strip()!r} -> "
                             f"{new_txt.strip()!r} (check proper names)")
                spans = [dict(spans[0], text=new_txt, size=L.size)] + spans[j:]
        if new:
            paras.append({"kind": kind, "texts": [], "mks": [], "x0": L.x0, "ind": L.x0 - Lm, "bib": L.bib, "geo": [],
                          "gap": big_gap, "bibhead": L.head and bool(BIB_RX.match(L.text.strip()))})
        txt, mk, odd = span_md(spans)
        if odd:
            warns.append(f"page {L.page}: superscript text kept as plain: {odd}")
        paras[-1]["texts"].append(txt)
        paras[-1]["mks"].extend(mk)
        paras[-1]["geo"].append((L.x0, L.x1, Lm, Rm, L.size))
        prev = L
    for P in paras:
        geo = P["geo"]
        # same-size quotations: >= 2 lines, all indented left, all but the last short of the right margin
        # (or indented left only, every line at one indent: a block quotation set full out to the right margin)
        if P["kind"] == "p" and not P["bib"] and len(geo) >= 2 and all(x0 > lm + 2.2 * sz for x0, x1, lm, rm, sz in geo) \
                and (all(x1 < rm - 0.8 * sz for x0, x1, lm, rm, sz in geo[:-1])
                     or max(g[0] for g in geo) - min(g[0] for g in geo) < 1.5):
            P["kind"] = "q"
        m = CAPTION_RX.match(P["texts"][0].strip())
        if m and P["kind"] in ("p", "q") and not P["bib"]:
            P["kind"] = "podpis" if m.group(1) else "tabela-tytul"
    # a paragraph interrupted by a figure/table caption (text flowing around a figure) is one paragraph:
    # last line before the caption full, first line after it not indented -> rejoin, caption after the paragraph
    j = 0
    while j + 2 < len(paras):
        A, C, D = paras[j], paras[j + 1], paras[j + 2]
        if A["kind"] == "p" == D["kind"] and C["kind"] in ("podpis", "tabela-tytul") and not A["bib"] and not D["bib"]:
            ax0, ax1, alm, arm, asz = A["geo"][-1]
            dx0, dx1, dlm, drm, dsz = D["geo"][0]
            if ax1 >= arm - 2.5 * asz and dx0 <= dlm + 0.6 * dsz:
                A["texts"] += D["texts"]; A["mks"] += D["mks"]; A["geo"] += D["geo"]
                warns.append(f"paragraph continued across a caption: “…{A['texts'][-len(D['texts']) - 1][-30:]}” | "
                             f"“{D['texts'][0][:30]}…” (caption placed after the paragraph)")
                del paras[j + 2]
                continue
        j += 1
    # verse: >= 3 one-line quotation paragraphs in a row, same indent from the page's margin, no gap between -> one quotation, line breaks kept
    merged, j, n_verse = [], 0, 0
    while j < len(paras):
        P, run = paras[j], [paras[j]]
        if P["kind"] == "q" and len(P["texts"]) == 1:
            while j + len(run) < len(paras):
                R = paras[j + len(run)]
                if R["kind"] != "q" or len(R["texts"]) != 1 or abs(R["ind"] - P["ind"]) > 1.5 or R["gap"]:
                    break
                run.append(R)
        if len(run) >= 3:
            merged.append(dict(P, kind="verse", texts=[R["texts"][0] for R in run], mks=[n for R in run for n in R["mks"]]))
            n_verse += 1
        else:
            merged += run[:1]
        j += len(run) if len(run) >= 3 else 1
    paras = merged

    # ---------- assemble
    out, seen_markers = [], []
    bib_entries = []
    if title_note:
        out += ["::: przypis-tytulowy", join_lines([span_md(L.spans)[0] for L in title_note], joins), ":::", ""]
        warns.append(f"page {p0}: unnumbered note at the foot of the first page -> ::: przypis-tytulowy "
                     "(the author's note on the title, Kanon § 7.1; check)")
    for P in paras:
        kind, texts, mks = P["kind"], P["texts"], P["mks"]
        if P["bib"] or P["bibhead"]:
            # the author's reference list leaves the text (decision 19): SROM prints the one generated from refs.json
            if P["bib"]:
                bib_entries.append(join_lines(texts, joins).replace("*", ""))
            continue
        if kind == "verse":
            out.append("> " + "\\\n> ".join(join_lines([x], joins) for x in texts))
        else:
            t = join_lines(texts, joins)
            if kind == "h1":
                out.append("# " + t)
            elif kind == "h2":
                out.append("## " + t)
            elif kind == "q":
                out.append("> " + t)
            elif kind in ("podpis", "tabela-tytul"):
                out += [f"::: {kind}", t, ":::"]
            else:
                out.append(t)
        out.append("")
        for n in mks:
            seen_markers.append(n)
            if n in notes:
                out += [f"[^{n}]: " + join_lines(notes[n], joins), ""]
    md = "\n".join(out).rstrip() + "\n"

    def link_fix(text):
        """URL text that differs from its link target in a character or two (a glyph mapped wrongly:
        "?id¼1859" for "?id=1859") takes the target; listed"""
        def f(m):
            u = m.group(0).rstrip(".,;:)”’")
            if u in LINKS:
                return m.group(0)
            near = [x for x in LINKS if len(x) == len(u) and sum(a != b for a, b in zip(x, u)) <= 2]
            if len(near) == 1:
                warns.append(f"URL text {u!r} differs from its link target -> {near[0]!r} (the link used)")
                return near[0] + m.group(0)[len(u):]
            return m.group(0)
        return re.sub(r"(?:https?://|www\.)\S+", f, text)
    md = link_fix(md)
    bib_entries = [link_fix(x) for x in bib_entries]
    # "———. 2008. …" (repeated author, typed or drawn): the author of the entry above, so that each line of
    # <out>_bib.txt stands alone for the audit; listed
    for j, e in enumerate(bib_entries):
        m = re.match(r"^\s*(?:[—–]{2,}|-{3,}|_{3,})\s*([.,])\s*", e)
        if not m:
            continue
        au = re.match(r"^(.+?)\.\s+(?:\(?\[?\d{4}|n\.\s?d\.|forthcoming|in press)", bib_entries[j - 1]) if j else None
        if au is None:
            issues.append(f"reference list: repeated-author dash with no author above to take: {e[:60]!r}")
            continue
        bib_entries[j] = au.group(1) + "." + (" " + e[m.end():] if m.group(1) == "." else ", " + e[m.end():])
        warns.append(f"reference list: ——— -> {au.group(1)!r} (repeated author): {bib_entries[j][:70]!r}")
    front_md = [link_fix(x) for x in front_md]
    img_pages = [pno for pno in all_lines if doc[pno - 1].get_images()]
    if img_pages:
        warns.append(f"images on pages {img_pages}: not extracted (figures are placed by hand); captions -> ::: podpis")
    if n_verse:
        warns.append(f"{n_verse} verse quotation(s): line breaks kept (> …\\) — check where each begins and ends")

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

    # the text layer may give accented letters decomposed ("a" + combining acute): written composed (NFC), which
    # the kanon linter, the name matching in cite_map and InDesign all expect
    nfd = sum(1 for x in [md] + bib_entries + front_md for w in x.split() if unicodedata.normalize("NFC", w) != w)
    md = unicodedata.normalize("NFC", md)
    bib_entries = [unicodedata.normalize("NFC", x) for x in bib_entries]
    front_md = [unicodedata.normalize("NFC", x) for x in front_md]
    if nfd:
        warns.append(f"{nfd} word(s) with decomposed accents (a + combining mark) composed (NFC)")
    open(a.out, "w", encoding="utf-8").write(md)
    if bib_entries:
        bp = a.out.rsplit(".", 1)[0] + "_bib.txt"
        open(bp, "w", encoding="utf-8").write("\n".join(bib_entries) + "\n")
        warns.append(f"reference list: {len(bib_entries)} entries written to {bp} (input for refs.json + cite_map audit)")
    ital = len(re.findall(r"\*[^*]+\*", md))
    repp = a.out.rsplit(".", 1)[0] + "_extract.md"
    rep = [f"# PDF extraction — {a.pdf} (pages {p0}–{p1})", "",
           f"- body size {B} pt · note size {N} pt · paragraphs {sum(1 for p in paras if p['kind'] in ('p', 'q', 'verse'))} · headings {sum(1 for p in paras if p['kind'].startswith('h'))}",
           f"- footnotes {len(notes)} · markers {len(seen_markers)} · italic runs {ital}", "",
           "## Issues (fix before translating)"] + ([f"- {x}" for x in issues] or ["- none"])
    if front_md:
        fp = a.out.rsplit(".", 1)[0] + "_front.md"
        open(fp, "w", encoding="utf-8").write("\n\n".join(front_md) + "\n")
        rep += ["", f"## Front matter (not in the text: title, author, abstract go to the master CSV, Kanon § 13.3) -> {fp}"] \
            + [f"- {x[:200]}" for x in front_md]
    rep += ["", "## Warnings"] + ([f"- {x}" for x in warns] or ["- none"])
    rep += ["", "## Line-end hyphen joins (proofread)"] + ([f"- {x}" for x in joins] or ["- none"])
    rep += ["", "## Dropped running heads / page numbers"] + ([f"- {x}" for x in dropped] or ["- none"])
    open(repp, "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print(f"notes {len(notes)} · markers {len(seen_markers)} · italics {ital} · joins {len(joins)} · report {repp}")
    print("EXTRACT OK" if not issues else f"EXTRACT CHECK {len(issues)} issue(s)")
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
