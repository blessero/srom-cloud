#!/usr/bin/env python3
"""
export_work.py — SROM-MD -> working Word file for the editor (round-trips through docx_in.py).

    python3 export_work.py art.md -o art_robocza.docx

The working copy is for reading and editing in Word, not for typesetting:
- real Word footnotes, italics, small caps, headings, quotes (verse line breaks kept), lists, tables
- citations stay as short editable tokens: [@ficowski1985, s. 15] (fix a page in place; keep the brackets and @key)
- comments <!-- … --> (e.g. srom-tlumacz's open items) become ordinary Word comments; the editor handles
  them in Word — they are dropped on import and never block anything
- special blocks carry Word paragraph styles "SROM podpis", "SROM nota", "SROM bibliografia" … —
  keep them on those paragraphs; the importer rebuilds the blocks from them
The rendered proof with the full Polish apparatus comes from build.py --proof.
Import back:  python3 docx_in.py art_robocza.docx -o art.md   (recognised automatically)
"""
import argparse, os, re, subprocess, sys, tempfile, zipfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROM = ("markdown-smart-superscript-subscript-strikeout-raw_html-raw_tex-tex_math_dollars"
        "-implicit_figures-fancy_lists-example_lists-task_lists-auto_identifiers")
MARK = "SROM-robocza"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

LUA_OUT = r'''
return {{
  Div = function(d)
    if d.identifier == "bibliografia" then d.attributes["custom-style"] = "SROM bibliografia"; return d end
    if #d.classes > 0 then d.attributes["custom-style"] = "SROM " .. d.classes[1]; return d end
  end,
}}
'''


def comments_to_word(text):
    """<!-- X --> -> a real Word comment anchored at that spot (dropped again on import; never blocks)"""
    n = [0]
    def rep(m):
        n[0] += 1
        body = re.sub(r"\s+", " ", m.group(1)).strip().replace("]", "\\]").replace("[", "\\[")
        return (f'[{body}]{{.comment-start id="{n[0]}" author="SROM" date="2026-01-01T00:00:00Z"}}'
                f'[]{{.comment-end id="{n[0]}"}}')
    return re.sub(r"<!--(.*?)-->", rep, text, flags=re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    text = comments_to_word(open(a.md, encoding="utf-8").read())
    work = tempfile.mkdtemp()
    src = os.path.join(work, "in.md")
    open(src, "w", encoding="utf-8").write(text)
    lua = os.path.join(work, "out.lua")
    open(lua, "w", encoding="utf-8").write(LUA_OUT)
    r = subprocess.run(["pandoc", src, "-f", FROM, "-L", lua, "-M", f"subject={MARK}",
                        "-M", "title-meta=" + os.path.basename(a.md), "-o", a.out], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    shutil.rmtree(work)
    print(f"written {a.out} (working copy — import back with docx_in.py)")


if __name__ == "__main__":
    main()
