"""Markdown -> HTML fragment, no dependencies (the Mac's Python has no `markdown` package).

    md_html.py <file.md>            prints the fragment
    from md_html import render      render(text) -> (html, toc)  toc = [(level, id, title), ...] for ## and ###

Covers what the workspace's records use: headings, paragraphs, nested - * 1. lists, pipe tables, ``` fences,
> quotes, ---, and inline `code`, **bold**, *italic*, [text](url), bare http(s) URLs. Raw HTML in the source is escaped.
Used by kontaktowka_build.py (the sheet's „Zapis” panel: ikonografia.md, MB 21.11.2026).
"""
import html, re, sys

_U = r"(?:[^\s<>()]|\([^\s<>()]*\))+"
_INL = re.compile(r"(`[^`]+`)|\[([^\]]+)\]\((" + _U + r")\)|(https?://(?:[^\s<>()\]]|\([^\s<>()]*\))+(?<![.,;:!?'\"”]))")


def inline(s):
    out, pos = [], 0
    for m in _INL.finditer(s):
        out.append(_emph(html.escape(s[pos:m.start()], quote=False)))
        if m[1]:
            out.append("<code>" + html.escape(m[1][1:-1], quote=False) + "</code>")
        elif m[2]:
            u = m[3]
            if u.startswith("http"):
                out.append(f'<a href="{html.escape(u)}" target="_blank" rel="noopener noreferrer">{_emph(html.escape(m[2], quote=False))}</a>')
            elif u.startswith("#"):  # a heading in the same file (MB 25.11.2026: a reference opens its fuller entry)
                out.append(f'<a href="{html.escape(u)}">{_emph(html.escape(m[2], quote=False))}</a>')
            else:  # a local path: show it, no link (a sandboxed page cannot open it)
                out.append(f'{_emph(html.escape(m[2], quote=False))} <code>{html.escape(u, quote=False)}</code>')
        else:
            u = m[4]
            out.append(f'<a href="{html.escape(u)}" target="_blank" rel="noopener noreferrer">{html.escape(u, quote=False)}</a>')
        pos = m.end()
    out.append(_emph(html.escape(s[pos:], quote=False)))
    return "".join(out)


def _emph(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)([^_]+?)(?<!\s)_(?![\w_])", r"<i>\1</i>", s)
    return s


def _slug(t, seen):
    b = re.sub(r"[^\w]+", "-", t.lower()).strip("-")[:40] or "s"
    s, k = b, 2
    while s in seen:
        s, k = f"{b}-{k}", k + 1
    seen.add(s)
    return s


def _cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


LIST = re.compile(r"^(\s*)([-*+]|\d{1,2}[.)])\s+(.*)$")  # 1–2 digits: a wrapped line starting „1525.” is no list


def render(text):
    lines = text.replace("\r\n", "\n").split("\n")
    out, toc, seen, i, n = [], [], set(), 0, len(lines)
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(x.strip() for x in para)) + "</p>")
            para.clear()

    while i < n:
        ln = lines[i]
        if not ln.strip():
            flush(); i += 1; continue
        if ln.lstrip().startswith("```"):
            flush(); j = i + 1
            while j < n and not lines[j].lstrip().startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j]), quote=False) + "</code></pre>")
            i = j + 1; continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
        if m:
            flush(); lv = len(m[1]); sid = _slug(m[2], seen)
            if lv in (2, 3):
                toc.append((lv, sid, m[2]))
            out.append(f'<h{lv} id="{sid}">{inline(m[2])}</h{lv}>'); i += 1; continue
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", ln):
            flush(); out.append("<hr>"); i += 1; continue
        if ln.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush(); head = _cells(ln); i += 2; rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(_cells(lines[i])); i += 1
            t = ["<div class=\"tw\"><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>"); continue
        if ln.lstrip().startswith(">"):
            flush(); q = []
            while i < n and lines[i].lstrip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>" + render("\n".join(q))[0] + "</blockquote>"); continue
        if LIST.match(ln):
            flush(); i = _list(lines, i, out); continue
        para.append(ln); i += 1
    flush()
    return "\n".join(out), toc


def _list(lines, i, out):
    """A list and its nested lists; continuation lines join their item."""
    n = len(lines)
    m = LIST.match(lines[i]); base = len(m[1].expandtabs(4)); tag = "ol" if m[2][0].isdigit() else "ul"
    out.append(f"<{tag}>")
    item = None
    while i < n:
        ln = lines[i]
        if not ln.strip():
            # a blank line ends the list unless the next line is still a list item or indented continuation
            if i + 1 < n and (LIST.match(lines[i + 1]) or lines[i + 1].startswith("  ")):
                i += 1; continue
            break
        m = LIST.match(ln)
        ind = len(ln) - len(ln.lstrip()) if not m else len(m[1].expandtabs(4))
        if m and ind == base:
            if item is not None:
                out.append("<li>" + inline(" ".join(item)) + "</li>")
            item = [m[3]]; i += 1; continue
        if m and ind > base:
            sub = []
            i = _list(lines, i, sub)
            item = item or [""]
            out.append("<li>" + inline(" ".join(item)) + "".join(sub) + "</li>"); item = None
            continue
        if m and ind < base:
            break
        if ind > 0 or not m:
            if re.match(r"^(#{1,6})\s", ln) or ln.lstrip().startswith("|"):
                break
            (item if item is not None else []).append(ln.strip()); i += 1; continue
    if item is not None:
        out.append("<li>" + inline(" ".join(item)) + "</li>")
    out.append(f"</{tag}>")
    return i


if __name__ == "__main__":
    h, t = render(open(sys.argv[1], encoding="utf-8").read())
    print(h)
