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
Last line: IMPORT OK / IMPORT CHECK n
"""
import argparse, json, os, re, subprocess, sys, zipfile
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
return {pass1, pass2, pass3}
"""
WRITE_RT = WRITE.replace("-fenced_code_attributes", "")


def _unescape(s):
    return re.sub(r"\\([^\w\s])", r"\1", s)


def restore_tokens(md):
    """citation tokens came back from Word as escaped text: \\[@key, s. 15\\] -> [@key, s. 15];
    highlighted markers ⟦X⟧ -> <!-- X -->"""
    def tok(m):
        inner = _unescape(m.group(1))
        return "[" + inner + "]" if "@" in inner else m.group(0)
    md = re.sub(r"\\\[((?:[^\]\\]|\\.)*?)\\\]", tok, md)
    md = re.sub(r"⟦(.*?)⟧", lambda m: "<!-- " + _unescape(m.group(1)).strip() + " -->", md, flags=re.S)
    return md


def roundtrip(docx, out, lua_path):
    open(lua_path, "w", encoding="utf-8").write(LUA_RT)
    r = subprocess.run(["pandoc", docx, "-f", "docx+styles", "--track-changes=accept", "--lua-filter", lua_path,
                        "-t", WRITE_RT, "--wrap=none", "--markdown-headings=atx"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    md = restore_tokens(move_defs(r.stdout))
    open(out, "w", encoding="utf-8").write(md)
    return md


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("-o", "--out", required=True)
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
    open(lua, "w", encoding="utf-8").write(LUA_IN)
    r = subprocess.run(["pandoc", a.docx, "-f", "docx", "--track-changes=accept", "--lua-filter", lua, "-t", "json"],
                       capture_output=True, text=True)
    if r.returncode:
        os.remove(lua)
        sys.exit(r.stderr)
    ast = json.loads(r.stdout)
    msgs = [ln[11:] for ln in r.stderr.splitlines() if ln.startswith("IMPORT-MSG:")]
    # pandoc turns Word tabs into spaces: find tab-aligned paragraphs in the XML itself
    from lxml import etree
    Wn = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for par in etree.fromstring(z.read("word/document.xml")).iter(Wn + "p"):
        if any(r_.find(Wn + "tab") is not None for r_ in par.iter(Wn + "r")):
            txt = "".join(t.text or "" for t in par.iter(Wn + "t"))
            msgs.append("TABS\ttab-aligned paragraph — interlinear example (retype as ::: przyklad) or a table? " + txt[:60])
    r2 = subprocess.run(["pandoc", "-f", "json", "-t", WRITE, "--wrap=none", "--markdown-headings=atx"],
                        input=json.dumps(ast), capture_output=True, text=True)
    md = move_defs(r2.stdout)
    md, bib = split_bibliography(md)
    open(a.out, "w", encoding="utf-8").write(md)
    base = a.out.rsplit(".", 1)[0]
    extra = []
    if bib:
        open(base + "_bib.txt", "w", encoding="utf-8").write("\n".join(bib) + "\n")
        extra.append(f"- author's reference list: {len(bib)} entries moved to `{os.path.basename(base)}_bib.txt` (input for refs.json and "
                     "`cite_map.py audit`). Archival / fieldwork sections (kanon §9 I–III) go back into the text as a `::: {#bibliografia}` block.")
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
    n = len(issues) + (1 if (ins or dele or comments) else 0)
    print(f"written {a.out} · report {rp}")
    print("IMPORT OK" if not n else f"IMPORT CHECK {n}")


if __name__ == "__main__":
    main()
