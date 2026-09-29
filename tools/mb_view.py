#!/usr/bin/env python3
r"""mb_view.py: render SROM working notes (Markdown) for MB, in the look of the Claude desktop app.

  mb_view.py <file.md> [<file.md> ...]   one page per file
  mb_view.py --text PAH                  one page per text: its open questions (MB-decisions.md) followed by
                                         both notes sheets (stage 1 srom-typeset, stage 2 srom-tlumacz)
  mb_view.py --all                       MB-decisions.md
  options: --docx (also a Word file)  --open (open the result)  --out <dir> (default: <root>/_widok)

Output: self-contained HTML (Anthropic Serif/Mono from the installed Claude app, embedded; Georgia if the app is
missing), light and dark like the app. Files MB must open, written `🔴 \`path\`` in the Markdown, become red links
(#ea3d39) to the file. Question IDs (PAH-3, GEN-1, ...) become links to their heading. Local files only: the
embedded fonts are the app's and must not be published.
Needs pandoc; --docx also python-docx (use ~/.venvs/srom/bin/python).
"""
import argparse, base64, colorsys, datetime, glob, html, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # "SROM edit and trans"
HANDOFFS = ROOT / "_handoffs"
LEDGER = HANDOFFS / "MB-decisions.md"
APP = Path("/Applications/Claude.app/Contents/Resources")
RED = "#ea3d39"
ID_RE = r"(?:[A-Z][A-Z0-9]{2})-\d+"


# ---------------------------------------------------------------- text codes (README table is the only list)
def text_codes():
    """{'PAH': ('Pahulich, ...', 'pahulich'), ...} from the table in _handoffs/README.md."""
    codes = {}
    for line in (HANDOFFS / "README.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`?([A-Z][A-Z0-9]{2})`?\s*\|\s*([^|]+?)\s*\|\s*`?([a-z0-9_-]+|—)`?\s*\|", line)
        if m:
            codes[m.group(1)] = (m.group(2), m.group(3))
    return codes


def code_re():
    codes = text_codes()
    return re.compile(r"\b(?:%s)-\d+\b" % "|".join(sorted(codes))) if codes else re.compile(r"\b" + ID_RE + r"\b")


# ---------------------------------------------------------------- Markdown preparation
def resolve(path, base):
    p = path.strip()
    for cand in (ROOT / p, base / p, ROOT / "srom-typeset" / p, ROOT / "srom-tlumacz" / p, HANDOFFS / p):
        if cand.exists():
            return cand.resolve()
    return None


def page_of(p):
    """The rendered page that shows file p, and whether its IDs sit there as detail anchors."""
    if p == LEDGER.resolve():
        return "MB-decisions.html", False
    folders = {f: c for c, (_, f) in text_codes().items() if f != "—"}
    if p.name.endswith("_uwagi.md") and p.parent.name in folders and p.parent.parent.name == "work":
        return f"{folders[p.parent.name]}_{p.parent.name}.html", True
    return None, False


def mark_files(md, base, mode="html", here=None):
    r"""`🔴 \`path\`` (optionally followed by "→ ID") and `🔴 [text](path)` -> red links; a stray 🔴 is dropped.
    HTML: a ledger or notes-sheet path links to its rendered page (at the ID); anything else to the file itself."""
    def target(path, qid):
        p = resolve(path, base)
        if not p:
            return None
        page, detail = page_of(p) if mode == "html" else (None, False)
        if page and page != here:
            return page + (f"#{qid}-detail" if qid and detail else f"#{qid}" if qid else "")
        if page and qid:
            return f"#{qid}-detail" if detail else f"#{qid}"
        return p.as_uri()

    def code(m):
        text = m.group(1) + (f" → {m.group(2)}" if m.group(2) else "")
        t = target(m.group(1), m.group(2))
        return f"[{text}]({t}){{.mbfile}}" if t else f"[{text}]{{.mbfile .missing}}"

    def link(m):
        t = m.group(2) if re.match(r"[a-z]+:", m.group(2)) else (target(m.group(2), None) or m.group(2))
        return f"[{m.group(1)}]({t}){{.mbfile}}"
    md = re.sub(r"🔴\s*`([^`]+)`(?:\s*→\s*(%s))?" % ID_RE, code, md)
    md = re.sub(r"🔴\s*\[([^\]]+)\]\(([^)]+)\)", link, md)
    return md.replace("🔴", "")


def tag_detail(body, rx, seen):
    """First mention of each ID in a notes sheet becomes its detail anchor (heading: {#ID-detail}; text: a span)."""
    out, fence = [], False
    for line in body.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence:
            if re.match(r"#{1,6} ", line):
                m = rx.search(line)
                if m and m.group(0) not in seen and not line.rstrip().endswith("}"):
                    seen.add(m.group(0))
                    line = line.rstrip() + " {#%s-detail}" % m.group(0)
            else:
                parts = re.split(r"(`[^`]*`)", line)
                for j in range(0, len(parts), 2):
                    def one(m):
                        if m.group(0) in seen:
                            return m.group(0)
                        seen.add(m.group(0))
                        return "[%s]{#%s-detail .qid}" % (m.group(0), m.group(0))
                    parts[j] = rx.sub(one, parts[j])
                line = "".join(parts)
        out.append(line)
    return "\n".join(out)


def shift_headings(md, by):
    out, fence = [], False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"#{1,6} ", line):
            n = min(6, max(1, len(line) - len(line.lstrip("#")) + by))
            line = "#" * n + line.lstrip("#")
        out.append(line)
    return "\n".join(out)


def anchor_ids(md, rx, external=None):
    """Heading with an ID gets {#ID} (first time) or {#ID-detail} (the notes sheet); IDs in text link there."""
    used, lines, fence = set(), md.splitlines(), False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
        if fence or not re.match(r"#{1,6} ", line) or line.rstrip().endswith("}"):
            continue
        m = rx.search(line)
        if m:
            a = m.group(0) if m.group(0) not in used else m.group(0) + "-detail"
            if a not in used:
                used.add(a)
                lines[i] = line.rstrip() + " {#%s}" % a

    def link_ids(seg):
        def one(m):
            pre, i = m.group(1) or "", m.group(2)
            if pre and (i + "-detail") in used:
                return f"{pre}[{i}](#{i}-detail)"
            if i in used:
                return f"{pre}[{i}](#{i})"
            return f"{pre}[{i}]({external}#{i})" if external else m.group(0)
        return re.sub(r"(→\s*)?\b(%s)\b" % rx.pattern.replace(r"\b", ""), one, seg)
    fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
        if fence or re.match(r"#{1,6} ", line):
            continue
        # outside code spans and outside existing link text/targets
        parts = re.split(r"(`[^`]*`|\[[^\]]*\]\([^)]*\)(?:\{[^}]*\})?|\[[^\]]*\]\{[^}]*\})", line)
        lines[i] = "".join(p if j % 2 else link_ids(p) for j, p in enumerate(parts))
    return "\n".join(lines)


def combined(code, mode="html"):
    codes = text_codes()
    if code not in codes:
        sys.exit(f"mb_view: unknown text code {code} (table in _handoffs/README.md: {', '.join(codes)})")
    title, folder = codes[code]
    stem = f"{code}_{folder if folder != '—' else 'questions'}"
    here = stem + ".html"
    led = LEDGER.read_text(encoding="utf-8")
    sec = re.search(r"^## [^\n]*\(%s\)[^\n]*\n(.*?)(?=^## |\Z)" % code, led, re.S | re.M)
    parts = [f"# {title}", "", f"Everything open for this text. Questions first; the notes sheets below hold the "
             "detail (click a red link or an ID to jump). All questions: [MB-decisions](MB-decisions.html).", ""]
    parts += ["## Open questions", "", mark_files(sec.group(1).strip(), HANDOFFS, mode, here) if sec
              else "_None in MB-decisions.md._", ""]
    rx, seen = code_re(), set()
    for stage, mod in (("Stage 1 notes (source, srom-typeset)", "srom-typeset"),
                       ("Stage 2 notes (translation, srom-tlumacz)", "srom-tlumacz")):
        f = ROOT / mod / "work" / folder / f"{folder}_uwagi.md"
        if folder != "—" and f.exists():
            body = f.read_text(encoding="utf-8")
            first = re.match(r"# (.*)\n", body)
            body = body[first.end():] if first else body
            head = f"[{f.relative_to(ROOT)}]({f.resolve().as_uri()}){{.mbfile}}" + (f" — {first.group(1)}" if first else "")
            parts += [f"## {stage}", "", head, "",
                      tag_detail(mark_files(shift_headings(body, 1), f.parent, mode, here), rx, seen), ""]
    return "\n".join(parts), stem


# ---------------------------------------------------------------- look
def now():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")


def font_face(family, path, style="normal", fmt="truetype"):
    try:
        data = base64.b64encode(Path(path).read_bytes()).decode()
    except OSError:
        return ""
    return (f"@font-face{{font-family:{family};src:url(data:font/{'ttf' if fmt == 'truetype' else 'woff2'};base64,{data})"
            f" format('{fmt}');font-weight:300 800;font-style:{style};font-display:swap}}\n")


def app_fonts():
    css = font_face("mb-serif", APP / "fonts/AnthropicSerif-Romans-Variable-25x258.ttf")
    css += font_face("mb-serif", APP / "fonts/AnthropicSerif-Italics-Variable-25x258.ttf", "italic")
    css += font_face("mb-sans", APP / "fonts/AnthropicSans-Romans-Variable-25x258.ttf")
    for f in glob.glob(str(APP / "ion-dist/assets/v1/*.css")):
        m = re.search(r"font-family:anthropic-mono;src:url\(/assets/v1/([^)]+\.woff2)\)[^}]*font-style:normal",
                      Path(f).read_text(encoding="utf-8", errors="ignore"))
        if m:
            css += font_face("mb-mono", APP / "ion-dist/assets/v1" / m.group(1), fmt="woff2")
            break
    return css


# Claude desktop palette (app CSS, design-system greys: --cds-hsl-gray-*), light and dark
CSS = """
:root{--bg:60 14.29% 97.25%;--bg2:60 11.11% 94.71%;--bg3:45 11.76% 93.33%;--t1:0 0% 7.45%;--t2:60 2.75% 21.37%;
--t4:42.86 2.93% 46.86%;--bd:60 1.69% 11.57%;--code:0 57.78% 35.29%;--link:213.6 72.25% 33.92%;--clay:14.77 63.11% 59.61%}
@media (prefers-color-scheme:dark){:root{--bg:0 0% 8.24%;--bg2:60 1.59% 12.35%;--bg3:60 1.96% 10%;--t1:60 14.29% 97.25%;
--t2:55 9.09% 74.12%;--t4:48 4.59% 57.25%;--bd:52.5 11.76% 86.67%;--code:0 76.84% 81.37%;--link:212.79 79.63% 78.82%}}
*{box-sizing:border-box}
html{background:hsl(var(--bg));-webkit-text-size-adjust:100%}
body{margin:0;padding:40px 16px 80px;color:hsl(var(--t1));font-family:mb-serif,"Anthropic Serif",Georgia,serif;
font-size:16.5px;line-height:1.65;font-weight:400}
main{max-width:46rem;margin:0 auto}
.meta{font-family:mb-sans,"Anthropic Sans",system-ui,sans-serif;font-size:13px;color:hsl(var(--t4));margin-bottom:28px}
h1,h2,h3,h4,h5{font-weight:600;line-height:1.3;color:hsl(var(--t1));margin:1.6em 0 .5em}
h1{font-size:1.6rem;margin-top:0}h2{font-size:1.3rem;padding-top:.6em;border-top:.5px solid hsl(var(--bd)/.15)}
h3{font-size:1.1rem}h4,h5{font-size:1rem}
p{margin:.5em 0 .85em}ul,ol{padding-left:1.6rem;margin:.4em 0 .9em}li{margin:.3em 0}li>p{margin:.2em 0}
strong{font-weight:600}em{font-style:italic}
a{color:hsl(var(--link));text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px}
a.mbfile,.mbfile{color:%RED%;font-weight:600;text-decoration-color:%RED%}
.mbfile.missing{text-decoration:line-through dotted}
code{font-family:mb-mono,ui-monospace,Menlo,monospace;font-size:.86em;color:hsl(var(--code));background:hsl(var(--bg3));
border:.5px solid hsl(var(--bd)/.15);border-radius:.35rem;padding:.08em .32em}
a.mbfile code,.mbfile code{color:inherit;background:none;border:0;padding:0}
.qid{font-weight:600}
pre{background:hsl(var(--bg2));border:.5px solid hsl(var(--bd)/.15);border-radius:.6rem;padding:12px 14px;overflow-x:auto}
pre code{color:hsl(var(--t1));background:none;border:0;padding:0}
blockquote{margin:.8em 0;padding:.1em 0 .1em 1em;border-left:3px solid hsl(var(--bd)/.2);color:hsl(var(--t2))}
table{border-collapse:collapse;margin:1em 0;font-size:.94rem;display:block;overflow-x:auto;max-width:100%}
th,td{border:.5px solid hsl(var(--bd)/.2);padding:6px 10px;text-align:left;vertical-align:top}
th{background:hsl(var(--bg2));font-weight:600}
hr{border:0;border-top:.5px solid hsl(var(--bd)/.2);margin:2em 0}
h3[id]{scroll-margin-top:16px}:target{background:hsl(var(--clay)/.12);border-radius:.3rem}
""".replace("%RED%", RED)


def to_html(md, title, src_label):
    r = subprocess.run(["pandoc", "-f", "commonmark_x-fancy_lists", "-t", "html5", "--wrap=none"], input=md,
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("mb_view: pandoc failed: " + r.stderr)
    return (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{html.escape(title)}</title>"
            f"<style>{app_fonts()}{CSS}</style></head><body><main>"
            f"<div class=\"meta\">{html.escape(src_label)} · rendered {now()}</div>{r.stdout}</main></body></html>")


# ---------------------------------------------------------------- Word
def hexcol(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def reference_docx(path):
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.oxml.ns import qn
    subprocess.run(["pandoc", "-o", str(path), "--print-default-data-file", "reference.docx"], check=True)
    d = Document(str(path))
    t1, t2 = RGBColor.from_string(hexcol(0, 0, 7.45)), RGBColor.from_string(hexcol(60, 2.75, 21.37))

    def font(st, name, size=None, color=t1, bold=None):
        st.font.name = name
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(k), name)
        for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            rf.attrib.pop(qn(k), None)
        if size:
            st.font.size = Pt(size)
        if color is not None:
            st.font.color.rgb = color
        if bold is not None:
            st.font.bold = bold
    names = {s.name: s for s in d.styles}
    for n in ("Normal", "Body Text", "First Paragraph", "Compact", "Footnote Text", "Table", "Definition", "Abstract"):
        if n in names:
            font(names[n], "Anthropic Serif", 11 if n != "Footnote Text" else 9)
    for n, size in (("Title", 20), ("Subtitle", 14), ("Heading 1", 18), ("Heading 2", 15), ("Heading 3", 13),
                    ("Heading 4", 11.5), ("Heading 5", 11)):
        if n in names:
            font(names[n], "Anthropic Serif", size, t1, True)
            names[n].font.italic = False
    if "Block Text" in names:
        font(names["Block Text"], "Anthropic Serif", 11, t2)
    if "Verbatim Char" in names:
        font(names["Verbatim Char"], "Anthropic Mono", 9.5, RGBColor.from_string(hexcol(0, 57.78, 35.29)))
    if "Hyperlink" in names:
        names["Hyperlink"].font.color.rgb = RGBColor.from_string(RED[1:].upper())
    d.save(str(path))


def page_background(docx_path):
    """Ivory page like the app (Word: Design > Page Color); Word shows it on screen, prints white."""
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    d = Document(str(docx_path))
    bg = OxmlElement("w:background")
    bg.set(qn("w:color"), hexcol(60, 14.29, 97.25))
    d.element.insert(0, bg)
    st = d.settings.element
    if st.find(qn("w:displayBackgroundShape")) is None:
        st.insert(0, OxmlElement("w:displayBackgroundShape"))
    d.save(str(docx_path))


def to_docx(md, out, outdir):
    ref = outdir / ".reference.docx"
    if not ref.exists():
        reference_docx(ref)
    subprocess.run(["pandoc", "-f", "commonmark_x-fancy_lists", "-t", "docx", "--reference-doc", str(ref), "-o", str(out)],
                   input=md, text=True, check=True)
    page_background(out)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--text", action="append", default=[], help="text code from _handoffs/README.md, e.g. PAH")
    ap.add_argument("--all", action="store_true", help="MB-decisions.md")
    ap.add_argument("--docx", action="store_true")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "_widok"))
    a = ap.parse_args()
    if not shutil.which("pandoc"):
        sys.exit("mb_view: pandoc not found")
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = []                          # (md_for(mode), stem, label)
    if a.all:
        a.files.append(str(LEDGER))
        a.text += [c for c, (_, f) in text_codes().items() if f != "—"]
    for f in a.files:
        p = Path(f).resolve()
        label = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
        stem = p.stem
        jobs.append((lambda mode, p=p, stem=stem: mark_files(p.read_text(encoding="utf-8"), p.parent, mode,
                                                           stem + ".html"), stem, label))
    for c in dict.fromkeys(x.upper() for x in a.text):
        jobs.append((lambda mode, c=c: combined(c, mode)[0], combined(c)[1], f"{c}: MB-decisions.md + notes sheets"))
    if not jobs:
        ap.error("give a file, --text CODE or --all")
    rx = code_re()
    for md_for, stem, label in jobs:
        ext = None if stem == LEDGER.stem else "MB-decisions.html"
        md = anchor_ids(md_for("html"), rx, ext)
        title = (re.search(r"^# (.+)$", md, re.M) or [None, stem])[1]
        title = re.sub(r"\s*\{[^}]*\}$", "", title)
        out = outdir / f"{stem}.html"
        out.write_text(to_html(md, title, label), encoding="utf-8")
        print(out)
        if a.docx:
            dx = outdir / f"{stem}.docx"
            to_docx(anchor_ids(md_for("docx"), rx), dx, outdir)
            print(dx)
    if a.open and jobs:
        subprocess.run(["open", str(outdir / f"{jobs[0][1]}.html")])


if __name__ == "__main__":
    main()
