#!/usr/bin/env python3
"""
docx_in.py — author's Word file -> SROM-MD (then run normalize.py).

    python3 docx_in.py article.docx -o article.md

- tracked changes ACCEPTED, comments dropped (both counted in the report — check nothing was pending)
- italics -> *…*, small caps -> [..]{.smallcaps}, Word headings -> # / ##, real footnotes -> [^n]
- footnote definitions moved directly under the paragraph that cites them (safe chunking for translation)
- one paragraph per line; empty paragraphs removed
- flagged in <out>_import.md: bold-only paragraphs (manual headings?), superscript digits typed by hand
  (fake footnote numbers), other superscripts, images (replaced by a ::: podpis placeholder), tables,
  numbered lists, hyperlinks, manual line breaks
- --typed-notes (E9): notes typed as text, laid out like the PDF the file came from (superscript digits in the body,
  each page's notes as numbered paragraphs after its text, paragraphs split at page breaks) -> real notes labelled
  with the source numbers; split paragraphs joined; every repair and every gap listed (see typed_notes)
Last line: IMPORT OK / IMPORT CHECK n
"""
import argparse, html, json, os, re, subprocess, sys, zipfile
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WRITE = ("markdown-smart-raw_html-raw_attribute-native_divs-link_attributes-simple_tables"
         "-multiline_tables-grid_tables-fenced_code_attributes-header_attributes-auto_identifiers")

LUA_IN = r'''
local function note(kind, s) io.stderr:write("IMPORT-MSG:" .. kind .. "\t" .. s .. "\n") end
local stringify = pandoc.utils.stringify
return {{
  Superscript = function(el)
    local s = stringify(el)
    if s:match("^%d+$") then note("FAKE-NOTE", "superscript digits typed by hand: " .. s .. " (a footnote not made with Insert Footnote?)")
    else note("SUPERSCRIPT", "superscript kept as plain text: " .. s) end
    return el.content
  end,
  Subscript = function(el) note("SUBSCRIPT", "subscript kept as plain text: " .. stringify(el)); return el.content end,
  Link = function(el) note("LINK", "link kept as text: " .. stringify(el) .. " -> " .. el.target); return el.content end,
  LineBreak = function(el) note("LINEBREAK", "manual line break kept (verse in a block quote keeps it; elsewhere the build turns it into a space)") end,
  Image = function(el) note("IMAGE", "image replaced by placeholder: " .. el.src); return pandoc.Str("[RYCINA: " .. el.src .. "]") end,
  Figure = function(el)
    local cap = stringify(el.caption.long)
    note("FIGURE", "figure -> ::: podpis placeholder: " .. cap)
    return pandoc.Div({pandoc.Para({pandoc.Str("[RYCINA]"), pandoc.Space(), table.unpack(pandoc.utils.blocks_to_inlines(el.caption.long))})}, pandoc.Attr("", {"podpis"}))
  end,
  Table = function(el) note("TABLE", "table kept — finish in InDesign"); return el end,
  Para = function(el)
    if #el.content == 1 and el.content[1].t == "Strong" then note("BOLDPARA", "bold-only paragraph (manual heading?): " .. stringify(el)) end
    if #el.content == 0 then return {} end
  end,
}}
'''


def move_defs(md):
    """move every footnote definition directly under the paragraph containing its marker"""
    blocks = [b.rstrip() for b in re.split(r"\n\s*\n", md) if b.strip()]
    defs, order, body, last = {}, [], [], None
    for b in blocks:
        m = re.match(r"^\[\^([^\]\s]+)\]:", b)
        if m:
            last = m.group(1)
            defs[last] = [b]
            order.append(last)
        elif b.startswith("    ") and last is not None:
            defs[last].append(b)            # continuation paragraph of a multi-paragraph note
        else:
            last = None
            body.append(b)
    out = []
    for b in body:
        out.append(b)
        for lab in re.findall(r"\[\^([^\]\s]+)\](?!:)", b):
            if lab in defs:
                out.extend(defs.pop(lab))
    for lab in order:
        if lab in defs:
            out.extend(defs.pop(lab))
    return "\n\n".join(out) + "\n"


BIB_RX = re.compile(r"(?i)^(?:#+\s*|\*\*)?(?:\d+\.\s*)?(bibliografia|literatura|literatura przedmiotu|źródła i literatura|references|bibliography|works cited|literature|sources|literaturverzeichnis)(?:\*\*)?\s*$")
PAGE_LABELS = {"page": "s.", "pages": "s.", "p.": "s.", "pp.": "s.", "folio": "k.", "chapter": "rozdz.", "table": "tabl.",
               "figure": "rys.", "volume": "t.", "line": "w.", "note": "przyp.", "column": "szp.", "section": "§", "paragraph": "ust."}


def split_bibliography(md):
    """author's own reference list -> _bib.txt lines (input for cite_map audit); removed from the text,
    because SROM prints the bibliography generated from refs.json"""
    blocks = md.split("\n\n")
    out, bib, in_bib = [], [], False
    for b in blocks:
        first = b.strip().split("\n")[0]
        if BIB_RX.match(first.strip()):
            in_bib = True
            continue
        if in_bib and b.lstrip().startswith("#"):
            in_bib = False
        if in_bib:
            t = re.sub(r"\[([^\]]*)\]\{\.smallcaps\}", r"\1", b)
            t = re.sub(r"[*_]", "", re.sub(r"\s+", " ", t)).strip()
            if t:
                bib.append(t)
        else:
            out.append(b)
    return "\n\n".join(out), bib


def fold_key(s):
    import unicodedata
    s = s.replace("ł", "l").replace("Ł", "L")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def harvest(docx, lua, out_md, report_lines):
    """Zotero / Mendeley citation fields -> SROM citations + refs.json (the author's own library data)"""
    r = subprocess.run(["pandoc", docx, "-f", "docx+citations", "--track-changes=accept", "--lua-filter", lua, "-t", "json"],
                       capture_output=True, text=True)
    rj = subprocess.run(["pandoc", docx, "-f", "docx+citations", "-t", "csljson"], capture_output=True, text=True)
    if r.returncode or rj.returncode:
        report_lines.append("- citation harvest FAILED: " + (r.stderr or rj.stderr)[:200])
        return
    ast = json.loads(r.stdout)
    refs = json.loads(rj.stdout or "[]")
    newkey, used = {}, Counter()
    for ref in refs:
        people = ref.get("author") or ref.get("editor") or []
        who = (people[0].get("family") or people[0].get("literal") or "") if people else (ref.get("title") or "anon").split()[0]
        yr = ((ref.get("issued") or {}).get("date-parts") or [[""]])[0][0]
        base = fold_key(who.split()[0] if who else "anon") + str(yr or "")
        used[base] += 1
        newkey[str(ref["id"])] = base if used[base] == 1 else base + "abcdefghij"[used[base] - 1]
        ref["id"] = newkey[str(ref["id"])]
    unknown_labels = set()

    def fix(x):
        if isinstance(x, list):
            for i in x: fix(i)
        elif isinstance(x, dict):
            if x.get("t") == "Cite":
                for c in x["c"][0]:
                    c["citationId"] = newkey.get(c["citationId"], c["citationId"])
                    suf = c["citationSuffix"]
                    words = [e for e in suf if e.get("t") == "Str"]
                    if len(words) >= 2 and words[0]["c"] == ",":
                        lab = words[1]["c"]
                        if lab in PAGE_LABELS:
                            words[1]["c"] = PAGE_LABELS[lab]
                        elif not re.match(r"^\d", lab):
                            unknown_labels.add(lab)
                    while suf and suf[-1].get("t") == "Space":
                        suf.pop()
            if "c" in x: fix(x["c"])
    fix(ast["blocks"])
    r2 = subprocess.run(["pandoc", "-f", "json", "-t", WRITE, "--wrap=none", "--markdown-headings=atx"],
                        input=json.dumps(ast), capture_output=True, text=True)
    md, _ = split_bibliography(move_defs(r2.stdout))
    base = out_md.rsplit(".", 1)[0]
    open(base + "_cited.md", "w", encoding="utf-8").write(md)
    json.dump(sorted(refs, key=lambda r: r["id"]), open(base + "_refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report_lines += [f"- **{len(refs)} works harvested from citation fields** → `{os.path.basename(base)}_cited.md` (citations keyed) + "
                     f"`{os.path.basename(base)}_refs.json`. Complete each ref per the refs.json conventions (the build flags missing data), "
                     "then continue with the _cited file."]
    if unknown_labels:
        report_lines.append(f"- locator labels not mapped to Polish, fix by hand: {sorted(unknown_labels)}")


# ------------------------------------------------------------------ working copy (export_work.py) round trip
LUA_RT = r"""
local function cs(el) return el.attributes and el.attributes["custom-style"] end
local stringify = pandoc.utils.stringify
-- pandoc 3.8 (docx+styles) wraps the caption inside the table in a "Table Caption" Div: unwrap it there,
-- before pass1 drops the standalone "Table Caption" paragraph that older pandoc left next to the table
local pass0 = {
  Table = function(t)
    t.caption.long = t.caption.long:walk({
      Div = function(d) if cs(d) == "Table Caption" then return d.content end end,
    })
    t.attributes["custom-style"] = nil                -- also added to the table itself by pandoc >= 3.8
    return t
  end,
}
local pass1 = {
  Span = function(s) if cs(s) then return s.content end end,
  CodeBlock = function(c)
    return pandoc.Div({pandoc.CodeBlock(c.text, pandoc.Attr("", {"przyklad"}))}, pandoc.Attr("", {"przyklad"}))
  end,
  Div = function(d)
    local c = cs(d)
    if not c then return nil end
    if c:sub(1, 5) == "SROM " then
      local cls = c:sub(6)
      if cls == "przyklad" then return d.content end   -- rebuilt around the code block
      if cls == "mowca" then d = d:walk({LineBreak = function() return pandoc.SoftBreak() end}) end  -- export_work.py
      return pandoc.Div(d.content, pandoc.Attr("", {cls}))
    end
    if c == "Table Caption" then return {} end        -- the reader already attached it to the table
    return d.content
  end,
}
local pass2 = {
  Note = function(n)
    local b = n.content[1]
    if b and (b.t == "Para" or b.t == "Plain") then
      while #b.content > 0 and (b.content[1].t == "Space" or b.content[1].t == "SoftBreak") do b.content:remove(1) end
    end
    return n
  end,
}
local function is_bibdiv(b) return b.t == "Div" and b.classes[1] == "bibliografia" end
local pass3 = {
  Pandoc = function(doc)
    local out, i, blocks = pandoc.List(), 1, doc.blocks
    while i <= #blocks do
      local b = blocks[i]
      local starts = (b.t == "Header" and b.level == 1 and stringify(b):lower() == "bibliografia") or is_bibdiv(b)
      if starts then
        local inner = pandoc.List()
        while i <= #blocks and ((blocks[i].t == "Header" and (blocks[i].level > 1 or #inner == 0)) or is_bibdiv(blocks[i])) do
          local x = blocks[i]
          if is_bibdiv(x) then inner:extend(x.content) else inner:insert(x) end
          i = i + 1
        end
        out:insert(pandoc.Div(inner, pandoc.Attr("bibliografia")))
      else
        out:insert(b)
        i = i + 1
      end
    end
    doc.blocks = out
    return doc
  end,
}
-- Word styles are per paragraph, so a block of several paragraphs comes back as one Div per paragraph (E16):
-- re-join consecutive Divs of a class whose paragraphs form one unit. Not podpis / tabela-* (one caption each),
-- przyklad (one example per code block) or mowca (the first line of each block is a speaker).
local JOIN = {["przypis-tytulowy"] = true, nota = true, motto = true, ["motto-zrodlo"] = true, dialog = true,
              ["bez-wciecia"] = true}
local function join_class(b) return b.t == "Div" and #b.classes == 1 and JOIN[b.classes[1]] and b.classes[1] end
local pass4 = {
  Pandoc = function(doc)
    local out = pandoc.List()
    for _, b in ipairs(doc.blocks) do
      local c, prev = join_class(b), out[#out]
      if c and prev and join_class(prev) == c then prev.content:extend(b.content) else out:insert(b) end
    end
    doc.blocks = out
    return doc
  end,
}
return {pass0, pass1, pass2, pass3, pass4}
"""
WRITE_RT = WRITE.replace("-fenced_code_attributes", "")


def _unescape(s):
    return re.sub(r"\\([^\w\s])", r"\1", s)


def restore_tokens(md):
    """citation tokens came back from Word as escaped text: \\[@key, s. 15\\] -> [@key, s. 15];
    highlighted markers ⟦X⟧ -> <!-- X -->"""
    def tok(m):
        inner = _unescape(m.group(1))
        if "@" in inner:
            return "[" + inner + "]"
        # editorial brackets in the text ("[Central and South Eastern Europe]", "[…]"): pandoc escapes them on the
        # way back; plain brackets read the same unless something after them would make a link/span/footnote
        return "[" + m.group(1) + "]" if not re.match(r"[(\[{:]", md[m.end():m.end() + 1]) and "^" not in inner else m.group(0)
    md = re.sub(r"\\\[((?:[^\]\\]|\\.)*?)\\\]", tok, md)
    md = re.sub(r"⟦(.*?)⟧", lambda m: "<!-- " + _unescape(m.group(1)).strip() + " -->", md, flags=re.S)
    # "[@key] <!-- X -->;" exported before 28.09.2026 left the space when Word dropped the comment
    md = re.sub(r"(\[[^\]\n]*@[^\]\n]*\])[ \t]+(?=[.,;:])", r"\1", md)
    return md


def roundtrip(docx, out, lua_path):
    open(lua_path, "w", encoding="utf-8").write(LUA_RT)
    r = subprocess.run(["pandoc", docx, "-f", "docx+styles", "--track-changes=accept", "--lua-filter", lua_path,
                        # preserve: the reader makes no soft breaks of its own, only the ::: mowca line break above
                        "-t", WRITE_RT, "--wrap=preserve", "--markdown-headings=atx"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    md = restore_tokens(move_defs(r.stdout))
    # front matter `tlumaczenie` (E10) comes back from the custom property export_work.py wrote
    tl = custom_property(docx, "srom-tlumaczenie")
    if tl:
        names = [n.strip() for n in tl.split(" ;; ") if n.strip()]
        md = "---\ntlumaczenie:\n" + "".join(f"  - {json.dumps(n, ensure_ascii=False)}\n" for n in names) + "---\n\n" + md
    open(out, "w", encoding="utf-8").write(md)
    return md


def custom_property(docx, name):
    """value of a Word custom document property, or None"""
    with zipfile.ZipFile(docx) as z:
        if "docProps/custom.xml" not in z.namelist():
            return None
        x = z.read("docProps/custom.xml").decode("utf-8")
    m = re.search(r'<property[^>]*\bname="' + re.escape(name) + r'"[^>]*>\s*<vt:lpwstr>(.*?)</vt:lpwstr>', x, re.S)
    return html.unescape(m.group(1)) if m else None


# ------------------------------------------------------------------ typed notes (E9): --typed-notes
FN_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
FN_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"
TERMINAL = tuple('.!?…:;”"’)»')


def typed_notes(src, dst):
    """A DOCX laid out like the PDF it came from (E9): superscript digits typed in the body, each page's notes typed
    as paragraphs after that page's text, paragraphs split at page breaks. Rewritten into real Word footnotes in
    `dst`, pairing marker N with note N in sequence. Never guesses: every repair and every gap is listed.
    Returns (report lines, number of problems, the note numbers in order)."""
    from lxml import etree
    Wn = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    z = zipfile.ZipFile(src)
    doc = etree.fromstring(z.read("word/document.xml"))
    body = doc.find(Wn + "body")
    sup_styles = set()
    if "word/styles.xml" in z.namelist():
        for st in etree.fromstring(z.read("word/styles.xml")).iter(Wn + "style"):
            va = st.find(f"{Wn}rPr/{Wn}vertAlign")
            if va is not None and va.get(Wn + "val") == "superscript":
                sup_styles.add(st.get(Wn + "styleId"))
    fn_xml = z.read("word/footnotes.xml") if "word/footnotes.xml" in z.namelist() else None
    if fn_xml is not None and any(f.get(Wn + "type") is None for f in etree.fromstring(fn_xml).iter(Wn + "footnote")):
        sys.exit("--typed-notes: the file already has real Word footnotes — not converted (mixed notes: do it by hand)")

    def is_sup(r):
        rpr = r.find(Wn + "rPr")
        if rpr is None:
            return False
        va, rs = rpr.find(Wn + "vertAlign"), rpr.find(Wn + "rStyle")
        return (va is not None and va.get(Wn + "val") == "superscript") or (rs is not None and rs.get(Wn + "val") in sup_styles)

    def rtext(r):
        return "".join(t.text or "" for t in r.iter(Wn + "t"))

    def text(p):
        return "".join(t.text or "" for t in p.iter(Wn + "t"))

    def plain(p):
        """text without the superscript note numbers (for "does the paragraph end a sentence?")"""
        return "".join(rtext(r) for r in p.iter(Wn + "r") if sup_digits(r) is None)

    def style(p):
        s = p.find(f"{Wn}pPr/{Wn}pStyle")
        return s.get(Wn + "val") if s is not None else ""

    def sup_digits(r):
        s = rtext(r).strip()
        return int(s) if is_sup(r) and s.isdigit() and len(s) <= 3 else None

    def lead(p):
        """(N, superscript?) when the paragraph opens with a note number"""
        for r in p.iter(Wn + "r"):
            s = rtext(r)
            if not s.strip():
                continue
            if sup_digits(r) is not None:
                return sup_digits(r), True
            break
        m = re.match(r"\s*(\d{1,3})[.)]?\s+\S", text(p))
        return (int(m.group(1)), False) if m else (None, False)

    def strip_lead(p, rx):
        """remove the leading match of rx from the paragraph's text, across runs"""
        m = re.match(rx, text(p))
        n = len(m.group(0)) if m else 0
        for t in p.iter(Wn + "t"):
            if n <= 0:
                break
            s = t.text or ""
            t.text, n = s[n:], n - len(s)
        for r in list(p.iter(Wn + "r")):                          # an emptied superscript run would stay superscript
            if not rtext(r) and r.find(Wn + "t") is not None and r.getparent() is not None:
                r.getparent().remove(r)

    def content(p):
        return [c for c in p if c.tag != Wn + "pPr"]

    def space_run():
        r = etree.Element(Wn + "r")
        t = etree.SubElement(r, Wn + "t")
        t.text = " "
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        return r

    paras = [c for c in body if c.tag == Wn + "p"]
    heading = lambda p: re.match(r"(?i)(heading|nagłówek|title|tytuł)", style(p) or "")
    # styles: the style of paragraphs that open with a superscript number vs of paragraphs carrying markers inside
    from collections import Counter as _C
    ns = _C(style(p) for p in paras if lead(p)[1])
    bs = _C(style(p) for p in paras if not lead(p)[1] and any(sup_digits(r) is not None for r in p.iter(Wn + "r")))
    note_style = ns.most_common(1)[0][0] if ns else None
    body_style = bs.most_common(1)[0][0] if bs else None
    styled = note_style is not None and note_style != body_style

    # pass 1: classify, in document order
    items, nxt, cur, markers, notes = [], 1, None, {}, {}
    gap_since_body, notes_since_body, last_body, repeated, last_marker, last_tail = False, False, None, set(), 0, ""
    rep, problems = [], 0
    for i, p in enumerate(paras):
        tx = text(p)
        if not tx.strip():
            continue
        if re.fullmatch(r"\s*\d{8,}\s*", tx):
            items.append(("drop", p, None)); rep.append(f"- page-ID string dropped: {tx.strip()}")
            continue
        if re.match(r"\s*\d{10,}", tx):
            rep.append(f"- GARBLED: paragraph opens with a long digit string (page ID glued to text?) — left as is: {tx[:60]}")
            problems += 1
        n, sup = lead(p)
        is_note = n is not None and not heading(p) and (
            (sup and n >= nxt) or (not sup and n == nxt and (n in markers or (styled and style(p) == note_style)))
            or (not sup and n > nxt and styled and style(p) == note_style))
        if is_note:
            if n > nxt:
                gap_since_body = True
                rep.append(f"- GAP: notes {nxt}–{n - 1} not found before note {n}" if n - 1 > nxt else f"- GAP: note {nxt} not found before note {n}")
                problems += 1
            splits, k = [], n + 1
            for c in content(p)[1:]:
                if c.tag == Wn + "r" and sup_digits(c) == k:       # the next note typed inside this one (E9: note 2)
                    splits.append((c, k)); k += 1
            items.append(("note", p, (n, splits)))
            for m_ in [n] + [s[1] for s in splits]:
                if m_ in notes:
                    repeated.add(m_)
                notes[m_] = i
            nxt, cur, notes_since_body = k, n, True
            continue
        if cur is not None and styled and style(p) == note_style:
            items.append(("notecont", p, None))
            continue
        # body
        cur = None
        join = repair = None
        first = next((sup_digits(r) for r in p.iter(Wn + "r") if sup_digits(r) is not None), None)
        if last_body is not None and not heading(p):
            # a paragraph never ends mid-sentence: split by a page break. Next starting in lower case: always;
            # in upper case only with evidence of the break (notes in between, or a comma/dash before it)
            prev = last_tail                                       # end of the text so far (after any join)
            if prev and not prev.endswith(TERMINAL) and (
                    tx.lstrip()[:1].islower() or (tx.lstrip()[:1].isupper() and (notes_since_body or prev.endswith((",", "–", "-"))))):
                # a page is missing when notes were skipped, or when this paragraph's first marker skips numbers
                if gap_since_body or (first is not None and first > last_marker + 1):
                    rep.append(f"- LOST TEXT? note/marker numbers skip here, paragraphs not joined: „…{prev[-40:]}” / „{plain(p).strip()[:40]}…”")
                    problems += 1
                else:
                    join = True
        if last_body is not None and not notes_since_body and not heading(p):
            m = re.match(r"\s*(\d{1,3})(?=[.,;:)]?\s)", tx)
            if m and not last_tail.endswith(TERMINAL):
                repair = int(m.group(1))                          # "…appellation" / "48. In the case": checked below
        for r in p.iter(Wn + "r"):
            if sup_digits(r) is not None:
                n_ = sup_digits(r)
                if n_ in markers:
                    repeated.add(n_)
                markers[n_] = i
                last_marker = max(last_marker, n_)
        items.append(("body", p, (join, repair)))
        if not join:
            last_body = p if not heading(p) else None
        last_tail = plain(p).rstrip() if not heading(p) else ""
        notes_since_body = gap_since_body = False

    # a repair only where note N exists and no marker N does
    fixed = {}
    for kind, p, x in items:
        if kind == "body" and x[1] is not None and x[1] in notes and x[1] not in markers:
            fixed[id(p)] = x[1]; markers[x[1]] = -1
            rep.append(f"- REPAIRED: marker {x[1]} typed at the start of a paragraph („{text(p).strip()[:30]}…”) → marker "
                       f"at the end of the previous paragraph, paragraphs joined — verify against the PDF"); problems += 1
    for n_ in sorted(repeated):
        rep.append(f"- REPEATED: number {n_} occurs more than once (marker or note) — not paired"); problems += 1
    no_note = sorted(n_ for n_ in markers if n_ not in notes)
    no_marker = sorted(n_ for n_ in notes if n_ not in markers)
    late = sorted(n_ for n_ in markers if n_ in notes and markers[n_] > notes[n_])
    if no_note:
        rep.append(f"- MARKER WITHOUT NOTE: {no_note} — left as superscript text"); problems += 1
    if no_marker:
        rep.append(f"- NOTE WITHOUT MARKER: {no_marker} — left in the text as a paragraph"); problems += 1
    if late:
        rep.append(f"- NOTE BEFORE ITS MARKER: {late} — not paired"); problems += 1
    pair = {n_ for n_ in markers if n_ in notes and n_ not in repeated and n_ not in late}

    # pass 2: rewrite
    fnotes, prev_body, cur_p = {}, None, None
    for kind, p, x in items:
        if kind == "drop":
            body.remove(p)
        elif kind == "note":
            n, splits = x
            if n not in pair and not any(s[1] in pair for s in splits):
                cur_p = None
                continue
            body.remove(p)
            strip_lead(p, r"\s*\d{1,3}[.)]?\s*")
            pp = p.find(Wn + "pPr")
            if pp is not None:
                p.remove(pp)
            fnotes[n], cur_p = [p], p
            for c, k in splits:
                p2 = etree.Element(Wn + "p")
                kids = content(cur_p)
                for e in kids[kids.index(c) + 1:]:
                    p2.append(e)
                cur_p.remove(c)
                strip_lead(p2, r"\s*")
                fnotes[k], cur_p = [p2], p2
        elif kind == "notecont":
            if cur_p is None:
                continue
            body.remove(p)
            cur_p.append(space_run())
            for e in content(p):
                cur_p.append(e)
        else:
            cur_p = None
            join, _ = x
            n_fix = fixed.get(id(p))
            if n_fix is not None and prev_body is not None:
                strip_lead(p, r"\s*\d{1,3}")
                r = etree.SubElement(prev_body, Wn + "r")
                rpr = etree.SubElement(r, Wn + "rPr")
                etree.SubElement(rpr, Wn + "vertAlign").set(Wn + "val", "superscript")
                etree.SubElement(r, Wn + "t").text = str(n_fix)
                for e in content(p):
                    prev_body.append(e)
                body.remove(p)
                continue
            if join and prev_body is not None:
                rep.append(f"- joined across a page: „…{plain(prev_body).rstrip()[-30:]}” + „{text(p).strip()[:30]}…”")
                prev_body.append(space_run())
                for e in content(p):
                    prev_body.append(e)
                body.remove(p)
                continue
            prev_body = p if not heading(p) else None
    # markers -> footnote references
    used = set()
    for p in body.iter(Wn + "p"):
        for r in list(p.iter(Wn + "r")):
            n_ = sup_digits(r)
            if n_ in pair and n_ in fnotes and n_ not in used:
                used.add(n_)
                for c in [c for c in r if c.tag != Wn + "rPr"]:
                    r.remove(c)
                etree.SubElement(r, Wn + "footnoteReference").set(Wn + "id", str(n_))
    root = etree.fromstring(fn_xml) if fn_xml is not None else etree.Element(Wn + "footnotes", nsmap={"w": Wn[1:-1]})
    for n_ in sorted(used):
        f = etree.SubElement(root, Wn + "footnote")
        f.set(Wn + "id", str(n_))
        for p in fnotes[n_]:
            f.append(p)
    files = {n: z.read(n) for n in z.namelist()}
    files["word/document.xml"] = etree.tostring(doc, xml_declaration=True, encoding="UTF-8", standalone=True)
    files["word/footnotes.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    rels = files["word/_rels/document.xml.rels"].decode("utf-8")
    if FN_REL not in rels:
        rels = rels.replace("</Relationships>", f'<Relationship Id="rIdSromTypedNotes" Type="{FN_REL}" Target="footnotes.xml"/></Relationships>')
        files["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    ct = files["[Content_Types].xml"].decode("utf-8")
    if "/word/footnotes.xml" not in ct:
        ct = ct.replace("</Types>", f'<Override PartName="/word/footnotes.xml" ContentType="{FN_CT}"/></Types>')
        files["[Content_Types].xml"] = ct.encode("utf-8")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
        for n, b in files.items():
            out.writestr(n, b)
    head = [f"- **typed notes (--typed-notes)**: {len(used)} markers paired with their notes"
            + (f"; note style „{note_style}”, body style „{body_style}”" if styled else "; no separate note style — continuation lines of notes not recognised")]
    return head + rep, problems, sorted(used)


def relabel(md, numbers):
    """pandoc numbers notes 1…n in order; give them back the source's numbers (note labels = source numbers)"""
    m = {str(i): str(n) for i, n in enumerate(numbers, 1)}
    return re.sub(r"\[\^(\d+)\]", lambda x: "[^" + m.get(x.group(1), x.group(1)) + "]", md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--typed-notes", action="store_true",
                    help="notes typed as text (superscript digits + numbered note paragraphs, page by page): make them real notes (E9)")
    a = ap.parse_args()
    z = zipfile.ZipFile(a.docx)
    doc_xml = z.read("word/document.xml").decode("utf-8", "replace")
    parts = doc_xml + "".join(z.read(n).decode("utf-8", "replace") for n in ("word/footnotes.xml", "word/endnotes.xml") if n in z.namelist())
    ins, dele = parts.count("<w:ins "), parts.count("<w:del ")
    comments = z.read("word/comments.xml").decode("utf-8", "replace").count("<w:comment ") if "word/comments.xml" in z.namelist() else 0
    fields = {"Zotero": parts.count("ZOTERO_ITEM"), "Mendeley": parts.count("ADDIN CSL_CITATION"), "EndNote": parts.count("ADDIN EN.CITE")}
    lua = os.path.join(os.path.dirname(os.path.abspath(a.out)) or ".", ".docx_in.lua")
    core = z.read("docProps/core.xml").decode("utf-8", "replace") if "docProps/core.xml" in z.namelist() else ""
    if "SROM-robocza" in core:
        md = roundtrip(a.docx, a.out, lua)
        os.remove(lua)
        n_notes = len(re.findall(r"^\[\^[^\]]+\]:", md, re.M))
        n_tok = len(re.findall(r"\[[^\]]*@", md))
        n_open = md.count("<!--")
        ctexts = []
        if "word/comments.xml" in z.namelist():
            from lxml import etree as _et
            Wn = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            for cm in _et.fromstring(z.read("word/comments.xml")).iter(Wn + "comment"):
                ctexts.append("".join(t.text or "" for t in cm.iter(Wn + "t")).strip())
        rep = [f"# DOCX import (working copy) — {a.docx}", "",
               f"- tracked changes accepted: {ins} insertions, {dele} deletions · Word comments dropped: {comments}",
               f"- footnotes: {n_notes} · citation tokens: {n_tok} · open markers: {n_open}",
               "", "## Word comments still in the file (not imported, for your attention)"] + \
              ([f"- {c}" for c in ctexts] or ["- none"]) + \
              ["", "Next: check.py (integrity; --pair against the source for a translation), then build.py"]
        open(a.out.rsplit(".", 1)[0] + "_import.md", "w", encoding="utf-8").write("\n".join(rep) + "\n")
        print(f"written {a.out} (working copy round trip)")
        print("IMPORT OK")
        return
    src, tn_rep, tn_n, tn_nums = a.docx, [], 0, None
    if a.typed_notes:
        src = a.out.rsplit(".", 1)[0] + "_typed-notes.docx"
        tn_rep, tn_n, tn_nums = typed_notes(a.docx, src)
    open(lua, "w", encoding="utf-8").write(LUA_IN)
    r = subprocess.run(["pandoc", src, "-f", "docx", "--track-changes=accept", "--lua-filter", lua, "-t", "json"],
                       capture_output=True, text=True)
    if r.returncode:
        os.remove(lua)
        sys.exit(r.stderr)
    ast = json.loads(r.stdout)
    msgs = [ln[11:] for ln in r.stderr.splitlines() if ln.startswith("IMPORT-MSG:")]
    # pandoc turns Word tabs into spaces: find tab-aligned paragraphs in the XML itself
    from lxml import etree
    Wn = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for par in etree.fromstring(zipfile.ZipFile(src).read("word/document.xml")).iter(Wn + "p"):
        if any(r_.find(Wn + "tab") is not None for r_ in par.iter(Wn + "r")):
            txt = "".join(t.text or "" for t in par.iter(Wn + "t"))
            msgs.append("TABS\ttab-aligned paragraph — interlinear example (retype as ::: przyklad) or a table? " + txt[:60])
    r2 = subprocess.run(["pandoc", "-f", "json", "-t", WRITE, "--wrap=none", "--markdown-headings=atx"],
                        input=json.dumps(ast), capture_output=True, text=True)
    md = move_defs(r2.stdout if tn_nums is None else relabel(r2.stdout, tn_nums))
    md, bib = split_bibliography(md)
    open(a.out, "w", encoding="utf-8").write(md)
    base = a.out.rsplit(".", 1)[0]
    extra = list(tn_rep)
    if tn_rep:
        extra.append(f"- the converted file (real notes) is `{os.path.basename(src)}` — open it in Word to compare")
    if bib:
        open(base + "_bib.txt", "w", encoding="utf-8").write("\n".join(bib) + "\n")
        extra.append(f"- author's reference list: {len(bib)} entries moved to `{os.path.basename(base)}_bib.txt` (input for refs.json and "
                     "`cite_map.py audit`). Abbreviation, archival and fieldwork sections (kanon §9.2) go back into the text as a `::: {#bibliografia}` block.")
    if fields["Zotero"] or fields["Mendeley"]:
        harvest(a.docx, lua, a.out, extra)
    if fields["EndNote"]:
        extra.append(f"- {fields['EndNote']} EndNote citation fields: not harvested — their displayed text was imported; key by hand")
    os.remove(lua)
    issues = [m for m in msgs if m.split("\t")[0] in ("FAKE-NOTE", "FIGURE", "IMAGE", "BOLDPARA", "TABS")]
    rep = [f"# DOCX import — {a.docx}", "",
           f"- tracked changes accepted: {ins} insertions, {dele} deletions · comments dropped: {comments}"
           + ("  **← confirm nothing was pending**" if ins or dele or comments else ""),
           f"- footnotes: {len(re.findall(r'^\[\^[^\]]+\]:', md, re.M))} · citation fields: "
           + ", ".join(f"{k} {v}" for k, v in fields.items() if v) if any(fields.values()) else
           f"- footnotes: {len(re.findall(r'^\[\^[^\]]+\]:', md, re.M))}"] + extra + ["", "## To check"]
    rep += [f"- {m.replace(chr(9), ': ', 1)}" for m in msgs] or ["- nothing"]
    rep += ["", "Next: python3 normalize.py " + a.out]
    rp = base + "_import.md"
    open(rp, "w", encoding="utf-8").write("\n".join(rep) + "\n")
    n = len(issues) + tn_n + (1 if (ins or dele or comments) else 0)
    print(f"written {a.out} · report {rp}")
    print("IMPORT OK" if not n else f"IMPORT CHECK {n}")


if __name__ == "__main__":
    main()
