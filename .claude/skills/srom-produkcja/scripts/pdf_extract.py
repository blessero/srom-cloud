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
                     a zone that starts without a number continues the previous note -> [^n]: … after its paragraph;
                     with no rule drawn, unnumbered lines atop the zone continue the previous page's note only when that
                     note ends mid-sentence and they sit at the notes' left edges (else: a quotation at note size; listed)
  raised line parts  a note number with the first words on a raised baseline, a superscript (XVIIᵉ): merged into
                     their line when nothing overlaps horizontally (else "35" | "–69" would split)
  title note         page 1: an unnumbered block at the foot, clear of the body   -> ::: przypis-tytulowy (listed);
                     or the note called from the title (numbered notes then start at 2); that number raised again in
                     the text is an issue, left as a DO SPRAWDZENIA comment
  raised digits      in a note: text, not a marker (an edition, "Neustadt ²1990") -> superscript digits (listed);
                     a space set in the marker's size before a marker is dropped
  endnotes           no heading needed: pages set wholly at the note size are notes; their top line continues a note
  control chars      U+0007 (InDesign indent-to-here) and other C0 codes removed, tabs -> spaces; soft hyphens removed
  unmapped glyphs    U+FFFD printed exactly over mapped text (overprint) dropped, listed; any other -> issue
  misread glyphs     private-use old-style figures / small capitals (Adobe legacy PUA, Linotype LT Std U+F643–F64C)
                     -> digits / capitals; a spacing accent printed over a letter composed with it ("Savi´c" -> "Savić");
                     "¼" from a TeX math font -> "="; word spaces set as gaps with no space glyph (letterspaced small
                     caps, one text object per word) inserted; all counted in the report; unknown private-use -> issue
  front matter       page 1 above the first text line (title in larger type, author, abstract; a chapter numeral set
                     larger above a book chapter's title does not count as the title) -> <out>_front.md,
                     not the text (SROM-MD has no header; Kanon § 13.3); with an "Abstract"/"Keywords" heading in
                     the first pages, everything up to the next text heading after the last of them (title/bio page,
                     keywords box in a column; On_Culture: metadata page, then title and abstract)
  paragraphs         first-line indent, short last line, vertical gap; a paragraph interrupted by a figure
                     caption is rejoined (full last line, no sentence end, or lower case after it), the caption
                     placed after it. The layout is measured first: RAGGED right (a line is short only below the
                     widths paragraphs run on from) and BLOCK paragraphs (space, no indent: an indented run is a
                     quotation, even at ~1 em); margins pooled per side (recto/verso); page breaks after a sentence
                     end on a full line are listed
  numbered items     "5. Zu Aesch …" with a hanging indent: one paragraph per item, escaped "5\\." (no Markdown list)
  headings           larger font, bold, or in capitals after a gap (also when smaller than the body) -> # / ##;
                     the journal's decoration taken off: "1_Introduction" -> "1. Introduction", "_Endnotes" (listed)
  opening small caps "THIS ESSAY BEGINS in …" -> "This essay begins in …" (listed: check proper names)
  block quotes       smaller font, indented both sides, or every line at one left indent, outside the note zone -> >;
                     a quotation justified to its own right edge (most lines end at one x) is measured against that edge
  verse              >= 3 one-line quotation paragraphs at the same indent        -> one > quotation, line breaks kept
  captions           "Figure 1." / "Rycina 1." … -> ::: podpis; "Table 1." … -> ::: tabela-tytul; short text set
                     smaller than the body beside, above or below an image -> ::: podpis (listed)
  reference list     after a heading "Bibliography"/"References"/… (any size): hanging indent -> one entry per
                     line in <out>_bib.txt; taken out of the text (decision 19); a repeated-author dash (typed, or
                     drawn as a rule) takes the author of the entry above (listed)
  headers/footers    page numbers and lines repeating across pages             -> dropped (listed)
  line-end hyphens   joined ("Ro-/mani" -> "Romani"); the document decides where it can (the joined or the
                     hyphenated word found inside a line elsewhere), else kept after prefixes such as
                     self-/non-/post- and flagged, or when the text has another compound on the same second element
                     (light-|brown beside "dark-brown"; flagged); before a capital (anti-|Roma) kept; before a conjunction
                     (Diebs-|und) kept with its space; a soft hyphen always joined; a slash at a line end joined
                     without a space, unless the document spaces its slashes in text of that style (virgules); a URL broken inside a token joined when a link target has it whole;
                     a URL hyphen at a line end: the link target decides, else the same address written whole inside a
                     line elsewhere, else kept and flagged; a URL closed by ">" ends there; before an opening quotation
                     mark (anti-|“gypsy”) the hyphen stays, no space
                     every join listed for proofreading
Report: <out>_extract.md with note/marker contiguity, joins, dropped lines, warnings.
Last line: EXTRACT OK / EXTRACT CHECK n issue(s)   (issues = broken note sequence, unmatched
markers/notes, multi-column pages, non-digit superscripts — fix before translating).
Limits: single-column text flow; scanned PDFs need OCR first; tables/figures are not rebuilt.
"""
import argparse, re, sys, unicodedata
from collections import Counter, defaultdict

import pymupdf

# a heading may carry the journal's decoration: a leading underscore ("_Abstract", "_Endnotes", "1_Introduction" in
# On_Culture) — matched here, and taken off the text's headings ("1_Introduction" -> "1. Introduction", listed)
NOTES_RX = re.compile(r"(?i)^_?(notes|endnotes|przypisy|anmerkungen|notes and references)$")
FRONT_RX = re.compile(r"(?i)^_?(abstract|summary|keywords|key words|streszczenie|słowa kluczowe|résumé|mots[- ]clés|zusammenfassung|schlagwörter|schlüsselwörter)$")
BIB_RX = re.compile(r"(?i)^_?(\d+[._]\s*)?(references|bibliography|works cited|literature|literatura|bibliografia|sources|źródła|literaturverzeichnis)$")
KEEP_HYPHEN_PREFIXES = {"self", "non", "anti", "post", "pre", "co", "well", "cross", "semi", "quasi", "neo", "pan",
                        "pro", "ex", "inter", "intra", "multi", "trans", "ultra", "counter", "mid", "socio",
                        "post", "euro", "afro", "indo", "anglo", "franco", "polish", "roma", "sinti"}
CAPTION_RX = re.compile(r"^\**(?:(Figure|Fig\.|Plate|Illustration|Rycina|Ryc\.|Ilustracja|Fot\.|Abb\.|Abbildung)|(Table|Tabela|Tab\.|Tabelle))\**\s*\d+[.:]")
LINKS = set()       # URI targets of the PDF's link annotations: what a click opens, the authority for URL text
VOCAB = set()       # words (lowercase, hyphenated ones too) that occur inside lines of the document being read
URLDOC = set()      # URLs written whole inside a line of the document (not running to a line end): evidence for breaks
UNMAPPED = []       # (page, overprinted glyphs dropped, unmapped glyphs kept, span text)
SLASH = {True: Counter(), False: Counter()}   # italic?/roman -> in-line "word/ word" (spaced) vs "word/word" (closed)
# a hyphen at a line end before one of these is a suspended hyphen (Diebs- und Räuberbanden, pre- and post-war): kept, with the space
CONJ_RX = re.compile(r"(?i)(und|oder|bzw\.?|sowie|bis|noch|als|wie|and|or|nor|to|i|lub|albo|oraz|czy|ani|et|ou)\b")
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
        self.size = (Counter(round(s["size"], 1) for s in base for c in s["text"] if not c.isspace())
                     or Counter(round(s["size"], 1) for s in base for _ in s["text"])).most_common(1)[0][0]
        main = [s for s in base if abs(round(s["size"], 1) - self.size) < 0.5]
        self.y = max(s["y"] for s in main) if main else min(s["y"] for s in base)   # baseline, not a raised part
        ink = [s for s in spans if s["text"].strip()] or spans
        self.x0 = min(s["x0"] for s in ink)             # where the ink starts (leading tabs/spaces are invisible)
        self.x1 = max(s["x1"] for s in spans)
        self.text = "".join(s["text"] for s in spans)
        self.tab = min(spans, key=lambda s: s["x0"]).get("tab", False)   # the line's text opens with a tab
        self.bold = all(is_bold(s) for s in spans if s["text"].strip())
        self.zone = "body"

    def __repr__(self):
        return f"<p{self.page} y{self.y:.0f} {self.size} {self.zone} {self.text[:40]!r}>"


def clean_text(text):
    """InDesign control characters (U+0007 "indent to here", other C0 codes) are layout, not text; a tab is a space
    in running text. Returns (text, opens with a tab or control character: a typed indent)"""
    return re.sub(r"[\x00-\x08\x0b-\x1f]", "", text).replace("\t", " "), text[:1] < " "


# Private-use code points that some fonts' ToUnicode maps give instead of the character (the text layer then loses
# them): Adobe's legacy PUA (Adobe Glyph List: zerooldstyle … nineoldstyle, Asmall … Zsmall, Agravesmall …) and the
# old-style figures of Linotype LT Std fonts (Sabon LT Std, Cambridge UP books: U+F643 = 0 … U+F64C = 9; checked
# against a CRS reference's volume, year, pages and DOI). Small capitals are read as capitals (what the reader sees),
# also those of a separate small-capitals font (SC_FONT below).
PUA = {**{0xF643 + i: str(i) for i in range(10)}, **{0xF730 + i: str(i) for i in range(10)},
       **{0xF761 + i: chr(0x41 + i) for i in range(26)},
       **{0xF7E0 + i: chr(0xC0 + i) for i in range(31) if 0xC0 + i != 0xD7}}
SPACING_ACCENT = {"´": "́", "`": "̀", "ˆ": "̂", "˜": "̃", "¨": "̈", "¸": "̧",
                  "ˇ": "̌", "˘": "̆", "˙": "̇", "˚": "̊", "˝": "̋", "¯": "̄", "˛": "̨"}
GLYPHS = Counter()  # repairs made in the text layer, for the report
PUA_LEFT = []       # (page, code points, span text): private-use glyphs no table explains


# A small-capitals font (a separate SC face: "Sabon-RomanSC", "MinionPro-RegularSC", "…-SmallCaps") maps its glyphs
# to lower-case letters: "1000 bce" in the text layer where the page prints BCE (Manchester UP, West Ohueri 2024).
SC_FONT = re.compile(r"(?:SC|SmCp|SmallCaps)$")


def repair_glyphs(chars, font, size, pno):
    """Glyphs the text layer misreads: private-use code points (PUA table), lower case from a small-capitals font,
    a spacing accent printed over a letter (TeX-style "Savi´c" -> "Savić"), "¼" from a TeX math font ("=" in Cambridge
    PDFs: "id¼6" -> "id=6")."""
    out = []
    parts = font.split("+")                       # "KALMLA+SabonLTStd-Roman+f6": subset prefix, name, suffix
    sc = bool(SC_FONT.search(parts[1] if len(parts) > 1 and len(parts[0]) == 6 else parts[0]))
    for c in chars:
        o = ord(c["c"])
        if sc and c["c"].islower():
            c = dict(c, c=c["c"].upper())
            GLYPHS["lower case from a small-capitals font read as capitals"] += 1
        elif o in PUA:
            c = dict(c, c=PUA[o])
            GLYPHS["private-use " + ("figure" if PUA[o].isdigit() else "small capital") + " glyphs read as "
                   + ("digits" if PUA[o].isdigit() else "capitals")] += 1
        elif c["c"] == "¼" and re.search(r"(?i)math|^(\w+\+)?cm(sy|mi|ex)|texcm", font):
            c = dict(c, c="=")
            GLYPHS["'¼' from a TeX math font read as '='"] += 1
        out.append(c)
    for k, c in enumerate(out):
        if c["c"] in SPACING_ACCENT:
            mid = (c["bbox"][0] + c["bbox"][2]) / 2
            for j in (k + 1, k - 1):
                if 0 <= j < len(out) and out[j]["c"].isalpha() and out[j]["bbox"][0] <= mid <= out[j]["bbox"][2]:
                    out[j] = dict(out[j], c=unicodedata.normalize("NFC", out[j]["c"] + SPACING_ACCENT[c["c"]]))
                    out[k] = None
                    GLYPHS["spacing accent printed over a letter composed with it (´c -> ć)"] += 1
                    break
    out = [c for c in out if c is not None]
    # a word space set as a gap, with no space glyph (letterspaced small capitals: "IBERIAN ATLANTIC")
    sp = []
    for k, c in enumerate(out):
        if k and c["c"].strip() and out[k - 1]["c"].strip() and c["bbox"][0] - out[k - 1]["bbox"][2] > 0.25 * size:
            sp.append(dict(c, c=" ", bbox=(out[k - 1]["bbox"][2], c["bbox"][1], c["bbox"][0], c["bbox"][3])))
            GLYPHS["word space set as a gap (no space glyph) inserted"] += 1
        sp.append(c)
    out = sp
    left =[c["c"] for c in out if 0xE000 <= ord(c["c"]) <= 0xF8FF]
    if left:
        full = "".join(c["c"] for c in out)
        PUA_LEFT.append((pno, " ".join(f"U+{ord(x):04X}" for x in sorted(set(left))), full[:60]))
    return out


def page_lines(page, W):
    raw = []
    d = page.get_text("rawdict", flags=TEXT_FLAGS)
    # a glyph without a Unicode mapping (U+FFFD) printed exactly over a mapped one is an overprint (a word set twice,
    # e.g. for a bolder look): dropped. Any other U+FFFD stays in the text and is an issue (UNMAPPED)
    mapped = {(round(c["bbox"][0]), round(c["origin"][1])) for b in d["blocks"] for l in b.get("lines", [])
              for sp in l["spans"] for c in sp.get("chars", []) if c["c"] != "\ufffd" and c["c"].strip()}
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                chars = repair_glyphs(sp.get("chars", []), sp["font"], sp["size"], page.number + 1)
                bad = [c for c in chars if c["c"] == "\ufffd"]
                if bad:
                    over = [c for c in bad if (round(c["bbox"][0]), round(c["origin"][1])) in mapped]
                    chars = [c for c in chars if c not in over]
                    full = "".join(c["c"] for c in sp.get("chars", []))
                    k = full.index("\ufffd")
                    UNMAPPED.append((page.number + 1, len(over), len(bad) - len(over), full[max(0, k - 30):k + 30]))
                clean, tab = clean_text("".join(c["c"] for c in chars))
                if not clean:
                    continue
                # x0 is where the ink starts: a leading tab or space is invisible
                vis = [c for c in chars if c["c"].strip() and ord(c["c"]) >= 32]
                raw.append({"text": clean, "size": sp["size"], "font": sp["font"], "flags": sp["flags"],
                            "x0": vis[0]["bbox"][0] if vis else sp["bbox"][0], "x1": sp["bbox"][2], "y": sp["origin"][1],
                            "top": sp["bbox"][1], "sup": False, "tab": tab})
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
        if not any(s["text"].strip() for s in ln):
            continue            # a line of tabs/spaces only (text from Word): no ink, no line
        ln.sort(key=lambda s: s["x0"])
        # words set as separate text objects with no space glyph between them (loosely justified lines, a number
        # after a figure font change: "In Spain, this veil", "1501 letters"): the gap is the space
        for a, b in zip(ln, ln[1:]):
            if b["x0"] - a["x1"] > 0.15 * max(a["size"], b["size"]) and a["text"][-1:].strip() and b["text"][:1].strip() \
                    and abs(a["y"] - b["y"]) < 0.5 * max(a["size"], b["size"]):
                b["text"] = " " + b["text"]
                GLYPHS["word space set as a gap between text objects (no space glyph) inserted"] += 1
        mx =(Counter(round(s["size"], 1) for s in ln for c in s["text"] if not c.isspace())
              or Counter(round(s["size"], 1) for s in ln for _ in s["text"])).most_common(1)[0][0]  # ink, not tabs
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
    last_size = None
    for s in spans:
        t = s["text"]
        prev_size, last_size = last_size, s["size"]
        if s["sup"]:
            st = t.strip()
            mm = re.fullmatch(r"(\d{1,3})|\[(\d{1,3})\]", st)      # 12, or bracketed [12] (Critical Romani Studies)
            if mm and for_note:
                # no note is called from inside a note: raised digits there are text (an edition: "Neustadt ²1990")
                sup = st.translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
                odd.append(f"{st} -> {sup}")
                parts.append(("r", sup))
                continue
            if mm:
                n = mm.group(1) or mm.group(2)
                if parts and parts[-1][0] == "r" and not parts[-1][1].strip() and parts[-1][1] and prev_size is not None \
                        and abs(prev_size - s["size"]) < 0.3:
                    parts.pop()        # a space set in the marker's size is the marker's spacing, not the text's
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


def url_evidence(head, tail):
    """a URL broken after a hyphen, no link target: the same address written whole inside a line elsewhere in the
    document decides (compared up to the first "/" after the break: host or path segment). True = the hyphen is the
    address's own, False = the typesetter's, None = no evidence"""
    def seg(u):
        cut = u.find("/", len(head) - 1)
        return u[:cut] if cut > 0 else u
    joined, kept = seg(head[:-1] + tail), seg(head + tail)
    a, b = any(u.startswith(joined) for u in URLDOC), any(u.startswith(kept) for u in URLDOC)
    return None if a == b else b


def join_lines(texts, joins):
    """join line texts of one paragraph; line-end hyphenation removed and logged"""
    out = ""
    for t in texts:
        t = t.strip()
        if not out:
            out = t
            continue
        # a URL at the line end is open (broken) unless closed by ">" or a quotation mark: "<http://…-6>." ends it
        um0 = re.search(r"(?:https?://|www\.)\S*$", out)
        open_url = um0 is not None and not re.search(r"[>”\"]", um0.group(0))
        if open_url and re.search(r"[-/._=?&#~]\**$", out):
            if out.endswith("-"):      # the URL's own hyphen, or the typesetter's (laviedesi-|dees)? the link decides
                head = re.search(r"(?:https?://|www\.)\S*$", out).group(0)
                tail = re.match(r"\S*", t).group(0).rstrip(".,;:)”’")
                if any(u.startswith(head[:-1] + tail) for u in LINKS):
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen removed (link target)")
                    out = out[:-1]
                elif any(u.startswith(head + tail) for u in LINKS):
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen kept (link target)")
                elif (ev := url_evidence(head, tail)) is not None:
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen {'kept' if ev else 'removed'} (the same address "
                                 f"elsewhere in the document)")
                    if not ev:
                        out = out[:-1]
                else:
                    joins.append(f"URL {head[-25:]}|{tail[:25]} -> hyphen kept, no link in the PDF — check the address")
            out = out + t              # a URL broken at the line end: no space inside it (Kanon § 8.6)
            continue
        um = um0 if open_url else None
        if um and t and any(u.startswith(um.group(0) + re.match(r"\S*", t).group(0).rstrip(".,;:)”’")) for u in LINKS):
            joins.append(f"URL {um.group(0)[-25:]}|{t[:25]} -> joined (link target)")   # broken inside a token, no hyphen
            out = out + t
            continue
        out = re.sub(r"-\u00ad(\**)$", r"-\1", out)       # a hard hyphen with a soft one after it is a hard hyphen
        m = re.search(r"([\w’']+)\u00ad-?(\**)$", out)
        if m and re.match(r"\**[^\W\d_]", t):    # a discretionary (soft) hyphen: the typesetter's, always joined
            w2 = t.split()[0].strip("*")[:20]
            joins.append(f"{m.group(1)}~|{w2} -> {m.group(1)}{w2} (soft hyphen, joined)")
            out = out[:m.start(0)] + m.group(1) + m.group(2) + t
            continue
        if re.search(r"[^\W\d_]-\**$", out) and CONJ_RX.match(t.lstrip("*")):
            joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> hyphen and space kept (suspended hyphen)")
            out = out + " " + t
            continue
        m = re.search(r"([\w’']+)-(\**)$", out)
        nxt = re.match(r"(\**)([a-ząćęłńóśźżäöüéèáíúčšž][\w’']*)", t)
        if m and nxt:
            frag = m.group(1)
            whole, hyph = (frag + nxt.group(2)).lower(), (frag + "-" + nxt.group(2)).lower()
            # evidence from the document itself (words inside lines) beats the prefix list
            keep = hyph in VOCAB if (whole in VOCAB) != (hyph in VOCAB) else frag.lower() in KEEP_HYPHEN_PREFIXES
            why = "found in the text" if (whole in VOCAB) != (hyph in VOCAB) else \
                "prefix, not found in the text — check" if keep else ""
            # neither form inside a line, no prefix: a hyphenated compound in the text with the same second element
            # ("dark-brown" for light-|brown, "Gitano-like" for mulatto-|like) is the document's evidence
            twin = None if (whole in VOCAB) != (hyph in VOCAB) or keep or len(nxt.group(2)) < 3 else \
                next((w for w in sorted(VOCAB) if w.endswith("-" + nxt.group(2).lower()) and w != hyph), None)
            if twin:
                keep, why = True, f"compound like '{twin}' in the text — check"
            if keep:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}-{nxt.group(2)} (hyphen kept: {why})")
                out = out + t
            else:
                joins.append(f"{frag}-|{nxt.group(2)} -> {frag}{nxt.group(2)}"
                             + (f" (prefix, but {why})" if frag.lower() in KEEP_HYPHEN_PREFIXES else ""))
                out = out[:m.start(0)] + frag + m.group(2) + t
            continue
        if re.search(r"[^\W\d_]-\**$", out) and re.match(r"\**[“‘„«»\"]", t):   # anti-|“gypsy”: a compound on a quoted word
            joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> hyphen kept, no space (quotation mark follows)")
            out = out + t
            continue
        if re.search(r"[^\W\d_]-\**$", out) and re.match(r"[\*“‘\"(]*[A-ZÀ-ÞĄĆĘŁŃÓŚŹŻČŠŽ]", t):   # anti-|Roma, Polish-|Lithuanian
            joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> hyphen kept (capital follows)")
            out = out + t
            continue
        if re.search(r"[^\W\d_”’]/\**$", out) and re.match(r"\**[^\W\d_]", t):   # police/|carceral: no space after a slash at a line end
            # unless the document spaces its slashes in text of that style (early-modern virgules: "Betretten/ mit")
            c = SLASH[out.endswith("*")]
            if c["spaced"] > c["closed"]:
                joins.append(f"{out[-12:].split()[-1]}|{t.split()[0][:20]} -> slash, space kept (the document spaces slashes here)")
                out = out + " " + t
            else:
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
    return out.replace("\u00ad", "")      # soft hyphens left inside lines (discretionary breaks not taken)


def wordcheck(pages, outputs):
    """Word tokens of the PDF pages (plain get_text, private-use glyphs decoded) vs the extraction's outputs.
    A hyphen between letters is dropped on both sides ("Anglo-\nAtlantic" = "Anglo-Atlantic", "anti-\nsocial" =
    "antisocial"); note labels count as the PDF's numbers; a download stamp ("Downloaded from … use, available at …",
    Cambridge Core) is not text. (Promoted from the per-article
    work/<id>/wordcheck.py of Ostendorf, Scheffknecht, Tittel, West Ohueri, 30.09.2026.)"""
    def toks(t):
        t = re.sub(r"(?<=[^\W\d_])[-­‐‑]\s*(?:\n\s*)?(?=[^\W\d_])", "", unicodedata.normalize("NFKC", t))
        return Counter(w.lower() for w in re.findall(r"[^\W\d_]+|\d+", t.replace("­", "")))
    src = "\n".join(pg.get_text() for pg in pages).translate(PUA)
    stamp = r"(?m)^.*(?:Downloaded from|use, available at).*$"      # a publisher's download stamp: not text
    src = re.sub(stamp, "", src)
    out = re.sub(stamp, "", "\n".join(outputs))
    out = re.sub(r"(?m)^p\d+: | \(set apart below the notes\)", "", out)
    out = re.sub(r"\[\^(\d+)\]:?", r" \1 ", out)
    out = re.sub(r"<!--.*?-->|:::[ \t]*[\w-]*", " ", out, flags=re.S)
    w1, w2 = toks(src), toks(out)
    return w1 - w2, w2 - w1


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
        for sp in L.spans:
            SLASH[is_italic(sp)]["spaced"] += len(re.findall(r"[^\W\d_]/ [^\W\d_]", sp["text"]))
            SLASH[is_italic(sp)]["closed"] += len(re.findall(r"[^\W\d_]/[^\W\d_]", sp["text"]))
        URLDOC.update(m.group(0) for m in re.finditer(r"(?:https?://|www\.)[^\s<>”\"]+", L.text)
                      if L.text[m.end():].strip())
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
    open_note = None    # the last note line of the previous page, when it ends mid-sentence (the note runs on)
    for pno, ls in all_lines.items():
        if N is None or not ls:
            continue
        was_open, open_note = open_note, None
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
            # (not on an endnote page: set wholly at the note size, notes starting on it; its top line continues a note)
            starts = lambda X: re.match(r"^\s*\d{1,3}(?:[.)]?\s|\s?[A-ZŁŚŻŹĆ„\"(*])", X.text) or note_number(X)
            endnote_page = i == 0 and any(starts(X) for X in suffix)
            # no rule to mark the zone: unnumbered lines atop it continue the previous page's note when that note
            # ends mid-sentence, and start at the notes' left edge (a note-size quotation above the notes is indented)
            # (the notes' left edges: where a note starts, where its second line runs, where the text after a hanging
            # number begins, and where the open note's own lines ran on the page before)
            edges = [X.x0 for X in suffix if starts(X)] + [Y.x0 for X, Y in zip(suffix, suffix[1:]) if starts(X) and not starts(Y)] \
                + [X.spans[1]["x0"] for X in suffix if note_number(X) and len(X.spans) > 1] \
                + ([was_open.x0] if was_open is not None and not starts(was_open) else [])
            runs_on = was_open is not None and not starts(suffix[0]) and any(abs(suffix[0].x0 - e) < 0.5 * N for e in edges)
            if runs_on:
                warns.append(f"page {pno}: note zone opens without a number after a note ending mid-sentence "
                             f"({was_open.text.strip()[-30:]!r}) -> continues that note: {suffix[0].text.strip()[:40]!r}")
            while not endnote_page and not runs_on and top < len(suffix) and not re.match(r"^\s*\d{1,3}(?:[.)]?\s|\s?[A-ZŁŚŻŹĆ„\"(*])", suffix[top].text) \
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
        last = [L for L in zone if L.zone == "note"]
        if last and not re.search(r"[.!?][”\"’)\]]*\s*$", last[-1].text):
            open_note = last[-1]

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
                warns.append(f"page {pno}: superscript text in a note (raised digits as superscript characters, "
                             f"letters kept as plain): {odd}")
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
    # a page full of an indented quotation has no margin of its own to show: the margin is pooled over the pages
    # of the same side (recto/verso), where the text block sits at the same x
    # (when that margin occurs on the page at all: a first page or a figure page may be set differently)
    side = defaultdict(Counter)
    for pno, c in lefts.items():
        side[pno % 2].update(c)
    margin = {}
    for pno in lefts:
        own, pooled = left_margin(lefts[pno]), left_margin(side[pno % 2])
        seen = any(abs(x - pooled) <= 1 for x in lefts[pno])
        margin[pno] = pooled if pooled < own - 0.3 * B and seen else own

    # layout class, from the body lines themselves: RAGGED right (a short line is followed, at normal leading, by a
    # line at the margin: line ends say nothing about paragraph ends) and BLOCK paragraphs (marked by space, never
    # by a first-line indent: an indented run of body-size lines is then a quotation, even at ~1 em)
    sl = [L for L in body_lines if abs(L.size - B) < 0.35 and not (L.bold and len(L.text) < 120)]
    ragged_cont = indent_start = gap_start = 0
    mid = []            # widths (share of the measure) of lines that a paragraph goes on from, at the margin
    for Pv, L in zip(sl, sl[1:]):
        if L.page != Pv.page or not lefts[L.page]:
            continue
        lm, rm = margin[L.page], max(rights[L.page])
        at_margin = abs(L.x0 - lm) < 0.3 * B
        if L.y - Pv.y > 1.6 * 1.25 * B:
            gap_start += at_margin
        elif abs(Pv.x0 - lm) < 0.3 * B and Pv.x1 < rm - 2.5 * B:
            ragged_cont += at_margin
            indent_start += lm + 0.6 * B < L.x0 < lm + 3 * B
        if abs(Pv.x0 - lm) < 0.3 * B and at_margin and L.y - Pv.y <= 1.6 * 1.25 * B and rm > lm:
            mid.append((Pv.x1 - lm) / (rm - lm))
    ragged = ragged_cont >= max(5, 0.03 * len(sl))
    # ragged right: a line is "short" (a paragraph's last line) when shorter than the lines paragraphs run on from
    # (their 5th percentile, less 5 %), not than the measure less 2.5 em
    ragged_cut = 0.95 * sorted(mid)[len(mid) // 20] if ragged and mid else None
    block = gap_start >= 3 and indent_start <= max(1, 0.1 * gap_start)
    if ragged or block:
        warns.append(f"layout: {'ragged right' if ragged else 'justified'}, paragraphs marked by "
                     f"{'space (indented runs = quotations)' if block else 'indent'}"
                     f"{f', a line under {ragged_cut:.0%} of the measure ends a paragraph' if ragged_cut else ''} "
                     f"[short line then margin line {ragged_cont}, indented starts {indent_start}, starts after a gap {gap_start}]")

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
        # the title's size, not a chapter number's (a lone numeral set larger above a book chapter's title)
        tsize = max((L.size for L in cand if any(c.isalpha() for c in L.text)), default=max(L.size for L in cand))
        again = lambda H: any(M.page > p0 and M.head and abs(M.size - H.size) < 0.15 and M.caps_head == H.caps_head
                              for M in body_lines)
        # no title when the largest lines are a heading style the text uses again on later pages (an extract
        # starting with its first section heading, e.g. a chapter read with --pages without its title page)
        tlines = [L for L in cand if abs(L.size - tsize) < 0.15 and any(c.isalpha() for c in L.text)]
        if tsize > B * 1.1 and not (tlines and all(L.head and again(L) for L in tlines)):
            # a heading right above the text stays in it; with a text heading of that style (size, capitals) later
            # on, only headings of a style the text uses again (the author's name, set large, is front matter)
            styled = any(again(H) for H in cand if H.head and H.size < tsize - 0.1)
            while cand and cand[-1].head and cand[-1].size < tsize - 0.1 and (again(cand[-1]) or not styled):
                cand.pop()
            front = cand
    # an "Abstract"/"Keywords" heading near the start: everything up to the first other heading after the last of
    # them (on that page or the next) is front matter too (journals that give pages to title, bio, abstract and
    # keywords before the text; On_Culture: keywords, publication date, how to cite on page 1, title and abstract on 2)
    fi = next((j for j, L in enumerate(body_lines) if L.head and FRONT_RX.match(L.text.strip()) and L.page < p0 + 3), None)
    if fi is not None:
        fl = max(j for j, L in enumerate(body_lines) if L.head and FRONT_RX.match(L.text.strip()) and L.page < p0 + 3)
        last = body_lines[fl].page
        fe = next((j for j in range(fl + 1, len(body_lines)) if body_lines[j].head
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
    # a note called from the title (or the author's name): the author's note on the title, Kanon § 7.1 -> not a
    # numbered note; the marker leaves the front matter
    title_n = None
    for L in front:
        for n in span_md(L.spans)[1]:
            if n in notes and title_n is None:
                title_n = n
                warns.append(f"note {n} is called from the title/front matter -> ::: przypis-tytulowy (Kanon § 7.1; "
                             f"the numbered notes start at {n + 1})")
    title_md = join_lines(notes.pop(title_n), joins) if title_n is not None else None
    if title_n is not None:
        order.remove(title_n)
        front_md = [x.replace(f"[^{title_n}]", "") for x in front_md]
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

    # a block quotation set justified to its own right edge, inside the text's (both sides indented): its lines end
    # well short of the text's right margin, and would each be read as a paragraph (then a "verse"). A run of lines at
    # one indent and size where most lines (all but the last) end at the same x is justified: that x is its margin
    run = []
    for L in body_lines + [None]:
        cand = L is not None and not L.head and (L.size < 0.95 * B or L.x0 > margin.get(L.page, L.x0) + 0.6 * L.size)
        if run and not (cand and L.page == run[-1].page and abs(L.x0 - run[-1].x0) <= 1.5
                        and abs(L.size - run[-1].size) <= 0.3 and 0 < L.y - run[-1].y < 1.6 * 1.25 * L.size):
            edge = max(R.x1 for R in run)
            if len(run) >= 3 and sum(1 for R in run[:-1] if edge - R.x1 < 3) >= max(2, 0.6 * (len(run) - 1)):
                for R in run:
                    R.qedge = edge
            run = []
        if cand:
            run.append(L)

    paras = []
    prev = None
    for L in body_lines:
        Lm = margin.get(L.page, L.x0)
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
        elif block and not L.bib and L.x0 > Lm + 0.6 * L.size:
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
            elif kind == pk and re.match(r"\**\d{1,3}[.)] ", paras[-1]["texts"][0]):
                # numbered item with a hanging indent: the next item starts back at the item's own left edge
                new = L.x0 - Lm <= paras[-1]["ind"] + 0.3 * L.size or big_gap
            elif kind == pk:
                pRm = max(rights[prev.page]) if rights[prev.page] else prev.x1
                pLm0 = margin.get(prev.page, prev.x0)
                short = (prev.x1 - pLm0) < ragged_cut * (pRm - pLm0) if ragged_cut else prev.x1 < Rm - 2.5 * prev.size
                if kind == "q" and getattr(prev, "qedge", None) and getattr(L, "qedge", None):
                    short = prev.x1 < prev.qedge - 2.5 * prev.size     # justified quotation: its own right edge
                prev_short = short and (not ragged or ragged_cut is not None)
                # positions relative to each line's own page margin (a quotation running on from a recto to a verso)
                pLm = margin.get(prev.page, prev.x0)
                indented = L.x0 > Lm + 0.6 * L.size if kind == "p" else L.x0 - Lm > paras[-1]["ind"] + 0.6 * L.size
                if indented and abs((L.x0 - Lm) - (prev.x0 - pLm)) < 2 and prev.x0 - pLm > 2.2 * L.size:
                    indented = prev_short = False   # block indented >= 2 em (same-size quotation): continuation
                # a line opening with a typed tab after a short line starts a paragraph (text from Word: tab indents)
                new = indented or prev_short or big_gap or (L.tab and short)
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
        if not new and prev is not None and L.page != prev.page and block and kind == "p" \
                and re.search(r"[.!?:…][”“»«’)\]*]*$", paras[-1]["texts"][-1].strip()):
            # space-marked paragraphs: a page break hides the space; a sentence end there may be a paragraph end
            warns.append(f"page {L.page}: paragraph taken as continuing over the page break after a sentence end "
                         f"(“…{paras[-1]['texts'][-1].strip()[-30:]}” | “{L.text.strip()[:30]}…”) — check")
        if new:
            paras.append({"kind": kind, "texts": [], "mks": [], "x0": L.x0, "ind": L.x0 - Lm, "bib": L.bib, "geo": [],
                          "page": L.page, "ys": [],
                          "gap": big_gap, "bibhead": L.head and bool(BIB_RX.match(L.text.strip()))})
        txt, mk, odd = span_md(spans)
        if odd:
            warns.append(f"page {L.page}: superscript text kept as plain: {odd}")
        paras[-1]["texts"].append(txt)
        paras[-1]["mks"].extend(mk)
        paras[-1]["geo"].append((L.x0, L.x1, Lm, Rm, L.size))
        paras[-1]["ys"].append((L.page, L.y - L.size, L.y))
        prev = L
    # images: a short text set smaller than the body beside, above or below a picture is its caption, whatever it
    # opens with ("Steckbrief aus dem Jahr 1749. Quelle: …"); lines of one caption (set ragged) are one paragraph
    img_rects = {pno: [pymupdf.Rect(i["bbox"]) for i in doc[pno - 1].get_image_info()] for pno in all_lines}
    for P in paras:
        pgs = {y[0] for y in P["ys"]}
        if P["kind"] not in ("p", "q") or P["bib"] or len(pgs) != 1 or len(P["texts"]) > 8 \
                or any(sz >= 0.95 * B for *_, sz in P["geo"]):
            continue
        x0, x1 = min(g[0] for g in P["geo"]), max(g[1] for g in P["geo"])
        y0, y1 = min(y[1] for y in P["ys"]), max(y[2] for y in P["ys"])
        for R in img_rects[P["page"]]:
            lead = 1.25 * B
            beside = (x1 <= R.x0 + 2 or x0 >= R.x1 - 2) and y1 > R.y0 - 2 * lead and y0 < R.y1 + 2 * lead
            under = x1 > R.x0 and x0 < R.x1 and (0 <= y0 - R.y1 < 3 * lead or 0 <= R.y0 - y1 < 3 * lead)
            if beside or under:
                P["kind"] = "podpis"
                P["img"] = True
                break
    j = 0
    while j + 1 < len(paras):
        A, C = paras[j], paras[j + 1]
        if A.get("img") and C.get("img") and A["page"] == C["page"] and C["ys"][0][1] - A["ys"][-1][2] < 1.25 * B:
            A["texts"] += C["texts"]; A["mks"] += C["mks"]; A["geo"] += C["geo"]; A["ys"] += C["ys"]
            del paras[j + 1]
            continue
        j += 1
    for P in paras:
        if P.get("img") and not CAPTION_RX.match(P["texts"][0].strip()):
            warns.append(f"page {P['page']}: text next to an image -> ::: podpis: {join_lines(P['texts'], [])[:70]!r} (check)")
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
            # full last line (meaningless when the text is set ragged), no sentence end, or the text after the
            # caption going on in lower case
            a_end, d_start = A["texts"][-1].strip(), D["texts"][0].lstrip("*„“‚‘»«\"' ")
            cont = (ax1 >= arm - 2.5 * asz and not ragged) or not re.search(r"[.!?:…][”“»«’)\]*]*$", a_end) \
                or d_start[:1].islower()
            if cont and dx0 <= dlm + 0.6 * dsz:
                A["texts"] += D["texts"]; A["mks"] += D["mks"]; A["geo"] += D["geo"]; A["ys"] += D["ys"]
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
    if title_md is not None:
        out += ["::: przypis-tytulowy", title_md, ":::", ""]
    elif title_note:
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
        if title_n in mks:
            # the title note's number called again in the text: nothing in SROM-MD can point there -> out of the
            # text, a comment in its place, an issue for the editor (the source is not corrected silently)
            issues.append(f"marker {title_n} in the text (page {P['page']}) calls the note on the title: stray? "
                          f"removed, comment left in its place")
            mks = [n for n in mks if n != title_n]
            texts = [x.replace(f"[^{title_n}]", f"<!-- DO SPRAWDZENIA: w źródle tu odsyłacz {title_n} "
                                                  f"(numer przypisu do tytułu) -->") for x in texts]
        if kind == "verse":
            out.append("> " + "\\\n> ".join(join_lines([x], joins) for x in texts))
        else:
            t = join_lines(texts, joins)
            if kind in ("p", "q"):
                t = re.sub(r"^(\d{1,3})([.)])(\s)", r"\1\\\2\3", t)     # "5. Zu Aesch …" is not a Markdown list
            if kind.startswith("h") and re.match(r"(\d+)?_(?=\S)", t):
                # the journal's decoration: "1_Introduction" -> "1. Introduction", "_Conclusion" -> "Conclusion"
                t0, t = t, re.sub(r"^(\d+)?_(?=\S)", lambda m: f"{m.group(1)}. " if m.group(1) else "", t)
                warns.append(f"heading decoration: {t0[:40]!r} -> {t[:40]!r}")
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

    for pno, over, kept, ctx in UNMAPPED:
        if over:
            warns.append(f"page {pno}: {over} glyph(s) without a Unicode mapping printed over the same text "
                         f"(overprint) dropped: {ctx!r}")
        if kept:
            issues.append(f"page {pno}: {kept} glyph(s) without a Unicode mapping (U+FFFD) in {ctx!r} — "
                          "read the PDF there and type the text")

    for what, n in sorted(GLYPHS.items()):
        warns.append(f"{n} {what} — spot-check numbers and names against the PDF")
    for pno, cps, ctx in PUA_LEFT:
        issues.append(f"page {pno}: private-use glyph(s) {cps} with no known meaning in {ctx!r} — read the PDF there")

    # ---------- integrity
    start = title_n + 1 if title_n == 1 else 1
    exp = list(range(start, start + len(order)))
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
    lost, extra = wordcheck(pages, [md] + bib_entries + front_md + dropped)
    rep += ["", f"## Word check: lost {sum(lost.values())} · extra {sum(extra.values())} (every word and number of the PDF "
            "pages, read independently of the line assembly, against text + bibliography + front matter + dropped lines; "
            "read every lost word against the PDF)",
            "- lost: " + (", ".join(f"{w}×{n}" if n > 1 else w for w, n in sorted(lost.items())[:80]) or "none"),
            "- extra: " + (", ".join(f"{w}×{n}" if n > 1 else w for w, n in sorted(extra.items())[:80]) or "none")]
    open(repp, "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print(f"notes {len(notes)} · markers {len(seen_markers)} · italics {ital} · joins {len(joins)} · "
          f"wordcheck lost {sum(lost.values())} extra {sum(extra.values())} · report {repp}")
    print("EXTRACT OK" if not issues else f"EXTRACT CHECK {len(issues)} issue(s)")
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
