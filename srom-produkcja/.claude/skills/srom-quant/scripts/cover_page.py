#!/usr/bin/env python3
"""
cover_page.py — the online edition's metadata page, put in front of the article's PDF (MB, 03.10.2026).

    python3 cover_page.py volumes/<vol>/srom_master_v3.csv <article_id> <article.pdf> --out <dir> [--proof]
        → <dir>/<pdf_file>   cover page + the article, ready to upload
    python3 cover_page.py volumes/<vol>/srom_master_v3.csv <article_id> --out <dir> [--proof]
        → <dir>/<article_id>_okladka.pdf   the cover page alone, to look at

One source: the master CSV row (master_schema.md). No InDesign: PyMuPDF draws the page at the journal's trim size
(165 × 235 mm) after MB's template (SROM_okladka_szablon_MB2.idml, 07.10.2026: IBM Plex Sans, SROM red, all other
type 88 % black = RGB 66 66 65), so it reads as a digital add-on, not a printed page. The final PDF also gets links (DOI, ORCID, licence,
the original's DOI, the journal's site), page labels (cover i; the article keeps its printed page numbers) and the
metadata of pdf_metadata.py (Info dictionary + XMP with PRISM).

Before the cover goes in, the article PDF's text layer is repaired (fix_actualtext.py, pikepdf: InDesign's accent glyphs
read as U+FFFD; the pages render as before, tags kept), and /Lang (the CSV's `language`, else pl) and
ViewerPreferences/DisplayDocTitle are set where the export lacks them (Cowork C6, 06.10.2026). After saving, a
self-check line reads the written file back: U+FFFD left, pages, tagged, /Lang, DisplayDocTitle, DOI in XMP.

Two blocks with fixed edges (MB, 07.10.2026). Header: Polish title at TITLE_Y, citation ending at CITE_BOTTOM; the gaps
between title, English title, authors, translator + original and citation stretch (up to 2×) or shrink (down to ½) so
texts with and without translator lines fill the same block. Authors' e-mails come from volumes/autorzy.tsv (`kontakt`),
matched by ORCID, else by name.
One page, strictly (MB, 04.10.2026): the two abstract blocks (Polish, then English, each with its keywords) are not
frames of a fixed height. The Polish one starts at ABSTRACT_TOP, the English one follows it at the template's gap,
and the English one may grow down to ABSTRACT_BOTTOM (218 mm from the top; the footer starts below it). The keywords stand 14 pt (baseline to baseline) under the last line. The type is
7.2 pt in both; only if the text still does not fit, both go down to 7 pt (never below, never one without the other).
If it does not fit at 7 pt, the run stops and names the overflow. The header, footer and leading never change.
Texts without abstracts (reviews, chronicles) get the header alone.

A printed field holding a placeholder (10.XXXXX, todo…, TODO) or left empty stops the run, so a page with a fake DOI
is never written; --proof prints it as it stands, marks the page PODGLĄD and names the file *_proof.pdf.
"""
import argparse, csv, html, io, os, re, sys
from datetime import datetime, timezone

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_metadata import build as metadata, licence_name, placeholder  # noqa: E402

MM = 72 / 25.4
W, H = 165 * MM, 235 * MM                      # SROM trim size (InDesign template: 467.72 × 666.14 pt)
# geometry in pt, from MB's template (frames' top-left corners; text frames grow downwards)
LX, TX, RX = 17.0, 70.9, 433.7                 # label column · text column · right edge
LOGO = (320.4, 17.7, 433.7, 63.9)              # x0 y0 x1 y1
INFO_Y, TITLE_Y, CITE_BOTTOM, ABSTRACT_TOP = 18.9, 83.8, 269.7, 283.3
FOOT_DATES, FOOT_LIC, OA = 629.3, 640.5, (17.0, 639.8, 62.2, 656.1)
BAR = 4.25                                     # red bars at both edges, full height
GAP = {"title_en": 14, "author": 8.3, "author2": 6, "translator": 9, "cite": 10.1,
       "abstract": 13.6, "abstract_en": 13.4}  # least gap, frame to frame; header gaps stretch up to 2×
ABSTRACT_BOTTOM = 218 * MM                     # the English abstract may grow down to here (MB, 04.10.2026)
ABSTRACT_LEAD, KEYWORDS_GAP = 10, 4           # pt: leading of the abstracts; extra space above the keywords line
ABSTRACT_SIZES = (7.2, 7.0)                    # pt, both abstracts; 7.0 only when 7.2 does not fit
RED = (227 / 255, 0, 11 / 255)                 # "SROM red", RGB 227 0 11
INK = "#424241"                                # 88 % black (CMYK 0 0 0 88 → RGB 66 66 65, InDesign's conversion)
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cover")
FONT_DIRS = [d for d in (os.environ.get("SROM_FONT_DIR"),                       # any folder holding the two .ttf files
                         os.path.expanduser("~/Library/Fonts/FontBase"), os.path.expanduser("~/Library/Fonts"), "/Library/Fonts",
                         os.path.expanduser("~/.local/share/fonts"), os.path.expanduser("~/.fonts"),   # Linux (Cowork's VM)
                         "/usr/share/fonts/truetype/ibm-plex", "/usr/share/fonts/truetype") if d]
FONTS = {"normal": "IBMPlexSans-Regular.ttf", "italic": "IBMPlexSans-Italic.ttf"}
SITE = "https://studiaromologica.pl"
SEP = "\u00a0\u00a0\u00a0|\u00a0\u00a0 "          # "   |   " as in the template; breaks only after the bar
EMAILS = {}                                    # ORCID or name → e-mail, from volumes/autorzy.tsv (main() loads it)

# Polish names of the CC 4.0 licences (official Polish translation).
CC_PL = {"by": "Uznanie autorstwa", "by-sa": "Uznanie autorstwa – Na tych samych warunkach",
         "by-nd": "Uznanie autorstwa – Bez utworów zależnych", "by-nc": "Uznanie autorstwa – Użycie niekomercyjne",
         "by-nc-sa": "Uznanie autorstwa – Użycie niekomercyjne – Na tych samych warunkach",
         "by-nc-nd": "Uznanie autorstwa – Użycie niekomercyjne – Bez utworów zależnych"}

CSS = """
@font-face {font-family: plex; src: url(%(normal)s);}
@font-face {font-family: plex; font-style: italic; src: url(%(italic)s);}
* {font-family: plex; margin: 0; padding: 0; color: #424241;}
p {margin: 0;}
.red {color: #e3000b;}
"""


def esc(s):
    return html.escape(s or "", quote=True)


def nbsp(s):
    """Kanon § 3.3: no line break after one-letter words, s. t. z. nr r. w. sygn. k. and initials, nor before %
    (InDesign does it by GREP style; the cover is not set in InDesign)."""
    s = re.sub(r"(?<![\w.])([aiouwzAIOUWZ]|[stzrwk]\.|nr|sygn\.|[A-ZĄĆĘŁŃÓŚŹŻ]\.) ", "\\1\u00a0", s or "")
    s = re.sub(r"(?<![\w.])([aiouwzAIOUWZ]|[A-ZĄĆĘŁŃÓŚŹŻ]\.) ", "\\1\u00a0", s)        # a second one-letter word in a row
    return s.replace(" %", "\u00a0%")


def pl(s):
    return esc(nbsp(s))


def font_dir():
    for d in FONT_DIRS:
        if all(os.path.exists(os.path.join(d, f)) for f in FONTS.values()):
            return d
    sys.exit(f"ABORT: IBM Plex Sans ({', '.join(FONTS.values())}) not found in {', '.join(FONT_DIRS)}.")


def load_emails(path):
    """volumes/autorzy.tsv → {ORCID: e-mail, name as printed: e-mail}; {} if the file is missing."""
    out = {}
    if os.path.exists(path):
        for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter="\t"):
            m = re.search(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", r.get("kontakt") or "")
            if m:
                for k in (r.get("orcid"), r.get("osoba")):
                    if k and k.strip():
                        out[k.strip()] = m.group(0)
    return out


def email(name, orcid):
    if orcid in EMAILS:
        return EMAILS[orcid]
    return next((v for k, v in EMAILS.items() if not k.startswith("http") and (k == name or k.endswith(" " + name))), "")


def authors(row):
    """[(name, affiliation, orcid, e-mail)] from authors_struct; falls back to the display columns."""
    out = []
    for a in (row.get("authors_struct") or "").split(";;"):
        f = [x.strip() for x in a.split("|")] + ["", "", "", ""]
        if f[0] or f[1]:
            name = f"{f[0]} {f[1]}".strip()
            out.append((name, f[2], f[3], email(name, f[3])))
    return out or [(row.get("authors_display", ""), row.get("affiliation_display", ""), row.get("orcid_display", ""), "")]


def translators(row):
    return [f"{f[0]} {f[1]}".strip() for f in ([x.strip() for x in t.split("|")] + ["", ""]
            for t in (row.get("translators_struct") or "").split(";;")) if f[0] or f[1]]


def date_pl(iso):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", iso or "")
    return f"{m.group(3)}.{m.group(2)}.{m.group(1)}" if m else (iso or "")      # Kanon § 3.5: dd.mm.rrrr


def keywords(s):
    return "; ".join(k.strip() for k in re.split(r"[;,]", s or "") if k.strip())   # Kanon § 1 pt 9: semicolon


def licence(row):
    """(short name, full Polish name, deed URL) from license_url; ("", "", "") if it is not a CC licence URL."""
    url = row.get("license_url", "")
    m = re.search(r"licenses/([a-z-]+)/(\d\.\d)", url)
    if not m:
        return "", "", ""
    code, ver = m.group(1), m.group(2)
    short = licence_name(url, row.get("license", ""))
    return (short, f"Creative Commons {CC_PL.get(code, code.upper())} {ver} ({short})",
            f"https://creativecommons.org/licenses/{code}/{ver}/deed.pl")


def check(row):
    """What the page prints; a placeholder or a gap is a problem (fatal unless --proof)."""
    probs = []
    for k in ("title_pl", "title_en", "authors_display", "volume", "year", "pages"):
        if not row.get(k) or placeholder(row.get(k)):
            probs.append(f"{k} empty")
    if placeholder(row.get("doi")):
        probs.append(f"doi is a placeholder: {row.get('doi') or 'empty'}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("pub_date_print", "")):
        probs.append(f"pub_date_print not YYYY-MM-DD: {row.get('pub_date_print') or 'empty'}")
    if not row.get("editorial_period") or placeholder(row.get("editorial_period")):
        probs.append("editorial_period empty")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("pub_date_online", "")):
        probs.append(f"pub_date_online not YYYY-MM-DD: {row.get('pub_date_online') or 'empty'}")
    if not licence(row)[0]:
        probs.append(f"license_url not a CC licence: {row.get('license_url') or 'empty'}")
    have = [k for k in ("abstract_pl", "abstract_en", "keywords_pl", "keywords_en") if row.get(k)]
    if have and len(have) < 4:
        probs.append("missing: " + ", ".join(sorted({"abstract_pl", "abstract_en", "keywords_pl", "keywords_en"} - set(have))))
    if row.get("is_translation") == "TAK" and not translators(row):
        probs.append("translation without translators_struct (Kanon § 12.2.3)")
    return probs


class Pen:
    """Writes HTML blocks on one page; put() returns the y below the block and fails rather than shrink the type."""

    def __init__(self, page, fdir):
        self.page, self.fdir = page, fdir
        self.arch = pymupdf.Archive(fdir)
        self.css = CSS % FONTS
        self.scratch = pymupdf.open().new_page(width=W, height=H)

    def put(self, x0, y, x1, body, bottom=None, page=None):
        r = pymupdf.Rect(x0, y, x1, bottom or H)
        spare, _ = (page or self.page).insert_htmlbox(r, body, css=self.css, archive=self.arch, scale_low=1)
        if spare < 0:
            raise ValueError("does not fit")
        return r.y1 - spare - 2.0               # PyMuPDF's block is 2 pt taller than InDesign's frame (measured on MB's template)

    def height(self, x0, x1, body):
        return self.put(x0, 0, x1, body, page=self.scratch)


def a(href, text):
    return f'<a href="{esc(href)}" style="color:#424241; text-decoration:none">{text}</a>'


def p(size, lead, body, cls="", extra=""):
    return f'<p{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} style="font-size:{size}pt; line-height:{lead}pt{extra}">{body}</p>'


def band(pen, row):
    """Red bars, the info block at the left and the logo at the right."""
    for x in (0, W - BAR):
        pen.page.draw_rect(pymupdf.Rect(x, 0, x + BAR, H), color=None, fill=RED)
    box = pymupdf.Rect(*LOGO)
    pen.page.show_pdf_page(box, pymupdf.open(os.path.join(ASSETS, "sr_logo.pdf")), 0)
    pen.page.insert_link({"kind": pymupdf.LINK_URI, "from": box, "uri": SITE})
    doi_url = f"https://doi.org/{row.get('doi', '')}"
    land = row.get("landing_url", "")      # the text stays the DOI URL (Crossref display rule); the link goes to our stable page
    info = [f'{esc(row.get("journal_title") or "Studia Romologica")} {esc(row.get("volume"))}/{esc(row.get("year"))}',
            f'ISSN: {esc(row.get("issn") or "1689-4758")}',
            f'Strony: {esc(row.get("pages"))}' if row.get("pages") else "",
            a(land if land.startswith("http") and not placeholder(land) else doi_url, esc(doi_url))]
    pen.put(TX, INFO_Y, LOGO[0] - 6, "".join(p(8, 10.5, s) for s in info if s))


def header(pen, row):
    """Titles, authors, translator + original, citation between TITLE_Y and CITE_BOTTOM; returns the y below."""
    au = authors(row)
    blocks = [(0, p(15, 18, pl(row.get("title_pl")), "red")), (GAP["title_en"], p(12, 16, esc(row.get("title_en"))))]
    for i, (name, aff, orcid, mail) in enumerate(au):
        ids = [x for x in (a(orcid, esc(orcid)) if orcid else "", a(f"mailto:{mail}", esc(mail)) if mail else "") if x]
        line = lambda ids: p(12, 15, f'<span class="red">{esc(name)}</span><span style="font-size:8pt">{"".join(SEP + x for x in ids)}</span>')
        body = line(ids)
        if len(ids) == 2 and pen.height(TX, RX, body) > 16:      # too long for one line: the e-mail goes under it
            body = line(ids[:1]) + p(8, 10.5, ids[1])
        if aff:
            body += p(8, 10.5, pl(aff))
        blocks.append((GAP["author"] if i == 0 else GAP["author2"], body))
    extra = ""
    tr = translators(row)
    if tr:
        extra += p(8, 10.5, f"Tłumaczenie: {esc(', '.join(tr))}")
    if row.get("is_translation") == "TAK" and (row.get("original_title") or row.get("original_source")):
        od = row.get("original_doi", "")
        od = f"https://doi.org/{od}" if od and not placeholder(od) else ""
        orig = ", ".join(x for x in (f'<i>{esc(row.get("original_title"))}</i>' if row.get("original_title") else "",
                                     esc(row.get("original_source")), a(od, esc(od)) if od else "") if x)
        extra += p(8, 10.5, f"Pierwodruk: {orig}")
    if extra:
        blocks.append((GAP["translator"], extra))
    cite = (f'<span class="red">Jak cytować:</span> {esc(", ".join(a[0] for a in au))}, <i>{pl(row.get("title_pl"))}</i>, '
            f'„{esc(row.get("journal_title") or "Studia Romologica")}”, {esc(row.get("year"))}, t.\u00a0{esc(row.get("volume"))}'
            + (f", s.\u00a0{esc(row.get('pages'))}" if row.get("pages") else "") + ".")
    blocks.append((GAP["cite"], p(8, 10.5, cite)))
    gaps = [g for g, _ in blocks]
    slack = CITE_BOTTOM - TITLE_Y - sum(pen.height(TX, RX, b) for _, b in blocks) - sum(gaps)
    k = max(0.5, min(2, 1 + slack / sum(gaps)))     # stretch to fill the block, up to 2×; shrink to ½, then run over
    y = TITLE_Y
    for g, b in blocks:
        y = pen.put(TX, y + g * k, RX, b)
    return y


def abstract(pen, row, key, y, size):
    """Label in the left column, abstract and keywords in the text column; the block is as tall as its text
    (down to ABSTRACT_BOTTOM at most); returns the y below."""
    label, kw = {"pl": ("Abstrakt", "Słowa kluczowe:"), "en": ("Abstract", "Keywords:")}[key]
    text = pl if key == "pl" else esc
    lead = ABSTRACT_LEAD
    pen.put(LX, y, TX - 4, p(9.5, 11.5, label, "red"))
    body = (p(size, lead, text(row.get("abstract_" + key)), extra="; text-align:justify")
            + p(size, lead, f'<span class="red">{kw}</span> {text(keywords(row.get("keywords_" + key)))}',
                extra=f"; text-align:justify; margin-top:{KEYWORDS_GAP}pt"))
    return pen.put(TX, y, RX, body, bottom=ABSTRACT_BOTTOM)


def footer(pen, row):
    pen.page.show_pdf_page(pymupdf.Rect(*OA), pymupdf.open(os.path.join(ASSETS, "open_access.pdf")), 0)
    dates = [f"Data publikacji: {date_pl(row.get('pub_date_print'))}",
             f"Data publikacji online: {date_pl(row.get('pub_date_online'))}",
             f"Okres redakcji: {nbsp(row.get('editorial_period'))}"]
    pen.put(TX, FOOT_DATES, RX, p(6, 8.5, esc(SEP.join(d for d in dates if d)), extra="; letter-spacing:-0.01em"))
    short, name, deed = licence(row)
    body = f'© {esc(row.get("year"))} {esc(", ".join(a[0] for a in authors(row)))}.'
    if short:
        body += f" Artykuł w\u00a0otwartym dostępie na licencji {a(deed, esc(name))}"
    pen.put(TX, FOOT_LIC, RX, p(6, 8.5, body, extra="; letter-spacing:-0.01em"))


def page(row, size, fdir):
    doc = pymupdf.open()
    pen = Pen(doc.new_page(width=W, height=H), fdir)
    band(pen, row)
    y = header(pen, row)
    for i, k in enumerate(k for k in ("pl", "en") if row.get("abstract_" + k)):
        y = abstract(pen, row, k, max(ABSTRACT_TOP, y + GAP["abstract"]) if i == 0 else y + GAP["abstract_en"], size)
    footer(pen, row)
    return doc


def cover(row, proof=False):
    """The cover as a one-page PyMuPDF document; the abstracts take 7.2 pt, then 7 pt, then the run stops."""
    fdir = font_dir()
    for size in ABSTRACT_SIZES:
        try:
            doc = page(row, size, fdir)
            break
        except ValueError:
            pass
    else:
        sys.exit(f"ABORT: {row.get('article_id')}: the cover does not fit on one page even at {ABSTRACT_SIZES[-1]} pt "
                 f"(abstracts {len(row.get('abstract_pl', ''))} + {len(row.get('abstract_en', ''))} characters, "
                 f"the English one may end at {ABSTRACT_BOTTOM / MM:.0f} mm). Shorten an abstract.")
    if proof:
        doc[0].insert_text((LX, 120), "PODGLĄD", fontsize=10, color=RED,
                           fontname="plex", fontfile=os.path.join(fdir, FONTS["normal"]))
    return doc, size


def xmp(meta, row):
    """XMP packet: Dublin Core, rights, and the PDF/PRISM fields of pdf_metadata.build()."""
    e = lambda s: html.escape(s or "", quote=False)
    props = "".join(f"<{k}>{e(v)}</{k}>" for _, k, v in meta["props"] if k != "dc:identifier")
    ident = next((v for _, k, v in meta["props"] if k == "dc:identifier"), "")
    creators = "".join(f"<rdf:li>{e(a[0])}</rdf:li>" for a in authors(row))
    subjects = "".join(f"<rdf:li>{e(k)}</rdf:li>" for k in meta["keywords"])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
 xmlns:pdf="http://ns.adobe.com/pdf/1.3/" xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/" xmlns:xmp="http://ns.adobe.com/xap/1.0/">
<dc:format>application/pdf</dc:format>
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["title"])}</rdf:li></rdf:Alt></dc:title>
<dc:creator><rdf:Seq>{creators}</rdf:Seq></dc:creator>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["subject"])}</rdf:li></rdf:Alt></dc:description>
<dc:subject><rdf:Bag>{subjects}</rdf:Bag></dc:subject>
<dc:language><rdf:Bag><rdf:li>{e(row.get("language") or "pl")}</rdf:li></rdf:Bag></dc:language>
<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{e(meta["notice"])}</rdf:li></rdf:Alt></dc:rights>
{f"<dc:identifier>{e(ident)}</dc:identifier>" if ident else ""}
<xmpRights:Marked>True</xmpRights:Marked><xmpRights:WebStatement>{e(meta["licenceUrl"])}</xmpRights:WebStatement>
<xmp:MetadataDate>{now}</xmp:MetadataDate>
{props}
</rdf:Description></rdf:RDF></x:xmpmeta>
<?xpacket end="w"?>"""


def prepare(path, row):
    """The article PDF with its text layer repaired and /Lang, DisplayDocTitle set where missing;
    returns (PyMuPDF document, report line, warnings)."""
    try:
        import pikepdf
        from fix_actualtext import repair
    except ImportError:
        sys.exit("ABORT: pikepdf missing (the text-layer repair needs it): ~/.venvs/srom/bin/pip install pikepdf")
    pdf, warn = pikepdf.open(path), []
    spans, maps = repair(pdf)
    lang = (row.get("language") or "pl").strip()
    if "/Lang" not in pdf.Root:
        pdf.Root.Lang = pikepdf.String(lang)
    elif str(pdf.Root.Lang).split("-")[0].lower() != lang.split("-")[0].lower():
        warn.append(f"the PDF's /Lang is {pdf.Root.Lang}, the CSV's language is {lang}")
    vp = pdf.Root.get("/ViewerPreferences")
    if vp is None:
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
    elif "/DisplayDocTitle" not in vp:
        vp.DisplayDocTitle = True
    buf = io.BytesIO()
    pdf.save(buf)
    return (pymupdf.open("pdf", buf.getvalue()),
            f"text layer: {spans} accent glyph(s) moved into their ActualText span, {maps} accent code(s) mapped", warn)


def selfcheck(path, doi):
    """One line read back from the written file. U+FFFD as pdftotext counts it: MuPDF without its default
    TEXT_CID_FOR_UNKNOWN_UNICODE, which would hide the replacement character."""
    d = pymupdf.open(path)
    cat = d.pdf_catalog()
    key = lambda k: d.xref_get_key(cat, k)[1]
    fffd = sum(pg.get_text(flags=pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP).count("\ufffd") for pg in d)
    tagged = key("MarkInfo/Marked") == "true" and key("StructTreeRoot") != "null"
    return (f"self-check: U+FFFD {fffd} · pages {len(d)} · tagged {'yes' if tagged else 'no'} · /Lang {key('Lang')}"
            f" · DisplayDocTitle {key('ViewerPreferences/DisplayDocTitle')}"
            f" · DOI in XMP {'yes' if doi and f'<prism:doi>{doi}</prism:doi>' in d.get_xml_metadata() else 'no'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("article_id"); ap.add_argument("article_pdf", nargs="?")
    ap.add_argument("--out", default="."); ap.add_argument("--proof", action="store_true")
    a = ap.parse_args()
    rows = [{k.lstrip("\ufeff"): v for k, v in r.items()} for r in csv.DictReader(open(a.master, encoding="utf-8"))]
    row = next((r for r in rows if r["article_id"] == a.article_id), None)
    if row is None:
        sys.exit(f"ABORT: {a.article_id}: no such row in {a.master}")
    EMAILS.update(load_emails(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(a.master))), "autorzy.tsv")))
    probs = check(row)
    if probs and not a.proof:
        sys.exit(f"ABORT: {a.article_id}: " + "; ".join(probs) + ". Fill the master CSV (or run with --proof).")
    doc, size = cover(row, a.proof)
    n = len(doc)
    os.makedirs(a.out, exist_ok=True)
    tag = "_proof" if a.proof else ""
    if not a.article_pdf:
        path = os.path.join(a.out, f"{a.article_id}_okladka{tag}.pdf")
        doc.save(path, garbage=4, deflate=True)
    else:
        art, fixed, warn = prepare(a.article_pdf, row)
        probs += warn
        r0 = art[0].rect
        if abs(r0.width - W) > 1 or abs(r0.height - H) > 1:
            probs.append(f"article page is {r0.width / MM:.1f} × {r0.height / MM:.1f} mm, not 165 × 235 "
                         "(export without bleed and marks)")
        span = [int(x) for x in (row.get("pages_from"), row.get("pages_to")) if (x or "").isdigit()]
        if len(span) == 2 and len(art) != span[1] - span[0] + 1:
            probs.append(f"article PDF has {len(art)} pages, the CSV says {span[0]}–{span[1]} ({span[1] - span[0] + 1})")
        art.insert_pdf(doc, start_at=0)                    # the article's bookmarks and links keep their pages
        first = int(row["pages_from"]) if (row.get("pages_from") or "").isdigit() else 1
        art.set_page_labels([{"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1},
                             {"startpage": n, "prefix": "", "style": "D", "firstpagenum": first}])
        meta, warn = metadata(row)
        art.set_metadata({"title": meta["title"], "author": meta["author"], "subject": meta["subject"],
                          "keywords": "; ".join(meta["keywords"]), "creator": "Studia Romologica (srom-quant cover_page.py)",
                          "producer": f"PyMuPDF {pymupdf.VersionBind}"})
        art.set_xml_metadata(xmp(meta, row))
        path = os.path.join(a.out, re.sub(r"\.pdf$", "", row.get("pdf_file") or a.article_id) + tag + ".pdf")
        art.save(path, garbage=3, deflate=True)
        print(fixed)
        print(selfcheck(path, row.get("doi", "")))
    print(f"written {path}"
          + "".join(f"\n!! {x}" for x in probs))
    print("RESULT: PROOF — not for upload" if a.proof else
          f"RESULT: CHECK — {len(probs)} warning(s) above before upload" if probs else "RESULT: OK")


if __name__ == "__main__":
    main()
