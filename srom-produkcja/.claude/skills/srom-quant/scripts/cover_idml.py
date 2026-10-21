#!/usr/bin/env python3
"""
cover_idml.py — the online cover page (design B, MB 21.10.2026) as an InDesign template, for one article:

    python3 cover_idml.py <master.csv> <article_id> <out.idml> [--template SROM_okladka_szablon_MB2.idml]

Takes template 2's document (page, swatches, bars, logo, Open Access mark) and writes named styles (group
"Okladka web") and one frame per block, at the positions and first baselines cover_page.py gives that article, so the
InDesign export matches the PDF line for line (checked in InDesign 2026 on vol. 18 no. 2, 21.10.2026: 42/42 lines,
baselines within 0.1 pt). Fonts in InDesign: Epilogue, Fraunces Italic and IBM Plex Mono Medium from Adobe Fonts;
"Fraunces 9pt Regular" installed from assets/cover/fonts (InDesign 2026 imports Adobe's variable Fraunces Regular at 12 pt
as Thin). Links are not written (the PDF gets them from cover_page.py).
"""
import argparse, csv, os, re, shutil, sys, tempfile, zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cover_page as cp  # noqa: E402
from cover_page import authors, translators, keywords, licence, date_pl, nbsp, placeholder, title_words  # noqa: E402

web = cp
CX, CY = cp.W / 2, cp.H / 2                     # spread origin = page centre
ASSET_LOGO = "file:" + os.path.join(cp.ASSETS, "sr_logo.pdf").replace(" ", "%20")
TEMPLATE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "SROM_okladka_szablon_MB2.idml"))

# ---------------------------------------------------------------- styles
G = "Okladka web"
INK, RED = "Color/SROM ink", "Color/SROM red"
PSTYLES = {   # name: font, style, size, leading, colour, extra attributes
    "Info":           ("IBM Plex Mono", "Medium", 7.5, 10.5, INK, ""),
    "Tytul PL":       ("Epilogue", "SemiBold", 15, 17.5, RED, ""),
    "Tytul EN":       ("Fraunces 9pt", "Regular", 12, 15, INK, ' AppliedLanguage="$ID/English: UK"'),
    "Autor":          ("Epilogue", "Regular", 7.5, 15, INK, ""),
    "Autor e-mail":   ("Epilogue", "Regular", 7.5, 10.5, INK, ""),
    "Afiliacja":      ("Epilogue", "Regular", 8, 10.5, INK, ' SpaceBefore="1.3"'),
    "Tlumaczenie":    ("Epilogue", "Regular", 8, 10.5, INK, ""),
    "Cytowanie":      ("Epilogue", "Regular", 8, 10.5, INK, ""),
    "Etykieta":       ("IBM Plex Mono", "Medium", 7, 9.6, RED, ' Capitalization="AllCaps" Tracking="140"'),
    "Abstrakt":       ("Epilogue", "Regular", 6.8, 9.6, INK, ' Justification="LeftJustified"'),
    "Abstrakt EN":    ("Epilogue", "Regular", 6.8, 9.6, INK, ' Justification="LeftJustified" AppliedLanguage="$ID/English: UK"'),
    "Slowa kluczowe": ("Epilogue", "Regular", 6.8, 9.6, INK, ' SpaceBefore="4"'),
    "Keywords":       ("Epilogue", "Regular", 6.8, 9.6, INK, ' SpaceBefore="4" AppliedLanguage="$ID/English: UK"'),
    "Stopka":         ("Epilogue", "Regular", 6, 8.5, INK, ""),
}
CSTYLES = {   # name: attributes, font
    "Etykieta":        (f'FontStyle="Medium" PointSize="6" FillColor="{RED}" Capitalization="AllCaps" Tracking="140"', "IBM Plex Mono"),
    "Etykieta szara":  (f'FontStyle="Medium" PointSize="6" FillColor="{INK}" Capitalization="AllCaps" Tracking="140"', "IBM Plex Mono"),
    "Autor nazwisko":  (f'FontStyle="SemiBold" PointSize="11.5" FillColor="{RED}"', "Epilogue"),
    "Tytul dziela":    ('FontStyle="Italic" PointSize="8.4"', "Fraunces"),
    "Bez podzialu":    ('NoBreak="true"', None),
}
ps = lambda n: f"ParagraphStyle/{G}%3a{n}"
cs = lambda n: f"CharacterStyle/{G}%3a{n}" if n else "CharacterStyle/$ID/[No character style]"


def styles_xml(src):
    pst = "".join(
        f'\t\t\t<ParagraphStyle Self="{ps(n)}" Name="{G}:{n}" Imported="false" NextStyle="{ps(n)}" SplitDocument="false" '
        f'EmitCss="true" IncludeClass="true" EmptyNestedStyles="true" EmptyLineStyles="true" EmptyGrepStyles="true" '
        f'Composer="HL Single" MinimumWordSpacing="100" Ligatures="false" FontStyle="{st}" PointSize="{sz}" FillColor="{col}"{"" if "AppliedLanguage" in ex else " AppliedLanguage=" + chr(34) + "$ID/Polish" + chr(34)} Hyphenation="false"{ex}>\n'
        f'\t\t\t\t<Properties><BasedOn type="string">$ID/[No paragraph style]</BasedOn>'
        f'<Leading type="unit">{ld}</Leading><AppliedFont type="string">{fn}</AppliedFont></Properties>\n'
        f'\t\t\t</ParagraphStyle>\n'
        for n, (fn, st, sz, ld, col, ex) in PSTYLES.items())
    cst = "".join(
        f'\t\t\t<CharacterStyle Self="{cs(n)}" Name="{G}:{n}" Imported="false" SplitDocument="false" EmitCss="true" '
        f'IncludeClass="true" {at}>\n\t\t\t\t<Properties><BasedOn type="string">$ID/[No character style]</BasedOn>'
        + (f'<AppliedFont type="string">{fn}</AppliedFont>' if fn else "") + '</Properties>\n\t\t\t</CharacterStyle>\n'
        for n, (at, fn) in CSTYLES.items())
    # drop template 2's groups and loose styles (IBM Plex Sans), keep the defaults
    src = re.sub(r'\t\t<ParagraphStyleGroup Self="ParagraphStyleGroup/\$ID/Okladka online".*?</ParagraphStyleGroup>\n', "", src, flags=re.S)
    src = re.sub(r'\t\t<CharacterStyle Self="CharacterStyle/(czerwony|kursywa)".*?</CharacterStyle>\n', "", src, flags=re.S)
    src = src.replace("\t</RootParagraphStyleGroup>",
                      f'\t\t<ParagraphStyleGroup Self="ParagraphStyleGroup/$ID/{G}" Name="$ID/{G}">\n{pst}\t\t</ParagraphStyleGroup>\n\t</RootParagraphStyleGroup>')
    return src.replace("\t</RootCharacterStyleGroup>",
                       f'\t\t<CharacterStyleGroup Self="CharacterStyleGroup/$ID/{G}" Name="$ID/{G}">\n{cst}\t\t</CharacterStyleGroup>\n\t</RootCharacterStyleGroup>')


def fonts_xml(src):
    fams = {"Epilogue": [("Regular", "Epilogue-Regular"), ("SemiBold", "Epilogue-SemiBold")],
            "Fraunces 9pt": [("Regular", "Fraunces9pt-Regular")], "Fraunces": [("Italic", "Fraunces-Italic")],
            "IBM Plex Mono": [("Medium", "IBMPlexMono-Medium")]}
    out = ""
    for i, (fam, sts) in enumerate(fams.items()):
        out += f'\t<FontFamily Self="diweb{i}" Name="{fam}">\n' + "".join(
            f'\t\t<Font Self="diweb{i}Fontn{fam} {st}" FontFamily="{fam}" Name="{fam} {st}" PostScriptName="{psn}" '
            f'Status="Installed" FontStyleName="{st}" FontType="TrueType" WritingScript="0" FullName="{fam} {st}" '
            f'FullNameNative="{fam} {st}" FontStyleNameNative="{st}" PlatformName="$ID/" Version="$ID/" TypekitID="$ID/" />\n'
            for st, psn in sts) + "\t</FontFamily>\n"
    src = re.sub(r'\t<FontFamily Self="[^"]*" Name="IBM Plex Sans">.*?</FontFamily>\n', "", src, flags=re.S)
    return src.replace("</idPkg:Fonts>", out + "</idPkg:Fonts>")


# ---------------------------------------------------------------- content (same data rules as the renderer)
def para(style, runs):
    return (style, runs)


def r(text, cstyle=None):
    return (cstyle, text)


def too_long(name, orcid, mail):
    """cover_page.header()'s test: name | ORCID | e-mail does not fit on one line."""
    pen = cp.Pen(cp.pymupdf.open().new_page(width=cp.W, height=cp.H), web.font_dir())
    ids = "".join(cp.SEP + cp.a(h, cp.esc(t)) for h, t in ((orcid, orcid), (f"mailto:{mail}", mail)))
    body = cp.p(*cp.AUTHOR, f'<span class="n red">{cp.esc(name)}</span><span style="font-size:7.5pt">{ids}</span>')
    return pen.height(cp.TX, cp.RX, body) > cp.AUTHOR[1] + 1


def content(row):
    au = authors(row)
    doi_url = f"https://doi.org/{row.get('doi', '')}"
    st = {}
    st["info"] = [para("Info", [r(f'{row.get("journal_title") or "Studia Romologica"} {row["volume"]}/{row["year"]}')]),
                  para("Info", [r(f'ISSN {row.get("issn") or "1689-4758"}')]),
                  para("Info", [r(f'Strony {row["pages"]}')]), para("Info", [r(doi_url)])]
    st["tytul_pl"] = [para("Tytul PL", [r(title_words(nbsp(row["title_pl"])))])]
    st["tytul_en"] = [para("Tytul EN", [r(title_words(row["title_en"]))])]
    for i, (name, aff, orcid, mail) in enumerate(au):        # one frame per author, as cover_page.py puts one block each
        ids = [x for x in (orcid, mail) if x]
        a = [para("Autor", [r(name, "Autor nazwisko")] + [r(web.SEP + x) for x in ids])]
        if orcid and mail and too_long(name, orcid, mail):      # as cover_page.header(): the e-mail goes under the line
            a = [para("Autor", [r(name, "Autor nazwisko"), r(web.SEP + orcid)]), para("Autor e-mail", [r(mail)])]
        if aff:
            a.append(para("Afiliacja", [r(nbsp(aff))]))
        st["autor" if i == 0 else f"autor_{i + 1}"] = a
    t = []
    tr = translators(row)
    if tr:
        t.append(para("Tlumaczenie", [r("Tłumaczenie", "Etykieta szara"), r("  " + ", ".join(tr))]))
    if row.get("is_translation") == "TAK" and (row.get("original_title") or row.get("original_source")):
        od = row.get("original_doi", "")
        runs = [r("Pierwodruk", "Etykieta szara"), r("  ")]
        if row.get("original_title"):
            runs.append(r(row["original_title"], "Tytul dziela"))
        rest = ", ".join(x for x in (nbsp(row.get("original_source")), f"https://doi.org/{od}" if od and not placeholder(od) else "") if x)
        if rest:
            runs.append(r(", " + rest if row.get("original_title") else rest))
        t.append(para("Tlumaczenie", runs))
    if t:
        st["tlumaczenie"] = t
    st["cytowanie"] = [para("Cytowanie", [
        r("Jak cytować", "Etykieta"), r("  " + ", ".join(x[0] for x in au) + ", "), r(nbsp(row["title_pl"]), "Tytul dziela"),
        r(f', „{row.get("journal_title") or "Studia Romologica"}”, {row["year"]}, t. {row["volume"]}, '),
        r(f's. {row["pages"]}.', "Bez podzialu")])]
    for k, lab, kw, ps_, ks in (x for x in (("pl", "Abstrakt", "Słowa kluczowe", "Abstrakt", "Slowa kluczowe"),
                                ("en", "Abstract", "Keywords", "Abstrakt EN", "Keywords")) if row.get("abstract_" + x[0])):
        f = nbsp if k == "pl" else (lambda s: s)
        st[f"etykieta_{k}"] = [para("Etykieta", [r(lab)])]
        st[f"abstrakt_{k}"] = [para(ps_, [r(f(row["abstract_" + k]))]),
                               para(ks, [r(kw, "Etykieta"), r("  " + f(keywords(row["keywords_" + k])))])]
    dates = [f"Data publikacji: {date_pl(row['pub_date_print'])}", f"Data publikacji online: {date_pl(row['pub_date_online'])}",
             f"Okres redakcji: {nbsp(row['editorial_period'])}" if (row.get("editorial_period") or "").strip() else ""]
    st["stopka_daty"] = [para("Stopka", [r(web.SEP.join(d for d in dates if d))])]
    short, name, _ = licence(row)
    who = (row.get("copyright_holder") or "").strip()
    who = "" if who == "None" else who
    who = who or ", ".join(x[0] for x in au)
    st["stopka_licencja"] = [para("Stopka", [r(f"© {row['year']} {who}. Artykuł w otwartym dostępie na licencji {name}")])]
    return st


def story_xml(sid, paras):
    body = ""
    for i, (style, runs) in enumerate(paras):
        last = i == len(paras) - 1
        crs = "".join(f'<CharacterStyleRange AppliedCharacterStyle="{cs(c)}"><Content>{escape(tx)}</Content></CharacterStyleRange>'
                      for c, tx in runs)
        if not last:
            crs += '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]"><Br /></CharacterStyleRange>'
        body += f'\t\t<ParagraphStyleRange AppliedParagraphStyle="{ps(style)}">{crs}</ParagraphStyleRange>\n'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<idPkg:Story xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging" DOMVersion="21.5">\n'
            f'\t<Story Self="{sid}" UserText="true" IsEndnoteStory="false" AppliedTOCStyle="n" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">\n'
            f'\t\t<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" FrameType="TextFrameType" StoryOrientation="Horizontal" StoryDirection="LeftToRightDirection" />\n'
            f'{body}\t</Story>\n</idPkg:Story>\n')


# ---------------------------------------------------------------- geometry from the renderer
def geometry(row):
    calls = []
    put0 = cp.Pen.put

    def put(self, x0, y, x1, body, bottom=None, page=None):
        y1 = put0(self, x0, y, x1, body, bottom, page)
        if page is None:
            calls.append([x0, y, x1, y1])
        return y1
    cp.Pen.put = put
    for size in cp.ABSTRACT_SIZES:
        calls.clear()
        try:
            doc = cp.page(row, size, web.font_dir()); break
        except ValueError:
            pass
    cp.Pen.put = put0
    orig = row.get("is_translation") == "TAK" and (row.get("original_title") or row.get("original_source"))
    names = ["info", "tytul_pl", "tytul_en"] + ["autor" if i == 0 else f"autor_{i + 1}" for i in range(len(authors(row)))] + (["tlumaczenie"] if translators(row) or orig else []) + ["cytowanie"] \
        + [f"{n}_{k}" for k in ("pl", "en") if row.get("abstract_" + k) for n in ("etykieta", "abstrakt")] + ["stopka_daty", "stopka_licencja"]
    assert len(names) == len(calls), (names, calls)
    lines = [(l["bbox"], l["spans"][0]["origin"][1]) for b in doc[0].get_text("dict")["blocks"] if b["type"] == 0 for l in b["lines"]]
    geo = {}
    for n, (x0, y, x1, y1) in zip(names, calls):
        base = min(o for bb, o in lines if bb[0] >= x0 - 1 and bb[2] <= x1 + 1 and y - 1 <= bb[1] and bb[3] <= y1 + 4)
        geo[n] = (x0, y, x1, max(y1, y + 10), base - y)
    return geo, size


def frame_xml(tpl, uid, sid, name, x0, y0, x1, y1, base):
    X0, Y0, X1, Y1 = x0 - CX, y0 - CY, x1 - CX, y1 - CY
    pts = "".join(f'<PathPointType Anchor="{x} {y}" LeftDirection="{x} {y}" RightDirection="{x} {y}" />'
                  for x, y in ((X0, Y0), (X0, Y1), (X1, Y1), (X1, Y0)))
    s = re.sub(r'Self="u135"', f'Self="{uid}"', tpl)
    s = re.sub(r'ParentStory="u123"', f'ParentStory="{sid}"', s)
    s = re.sub(r'Name="tytul_pl"', f'Name="{name}"', s)
    s = re.sub(r'ItemTransform="[^"]*"', 'ItemTransform="1 0 0 1 0 0"', s, count=1)
    s = re.sub(r"<PathPointArray>.*?</PathPointArray>", f"<PathPointArray>{pts}</PathPointArray>", s, flags=re.S)
    s = re.sub(r'TextColumnFixedWidth="[^"]*"', f'TextColumnFixedWidth="{x1 - x0}"', s)
    # MuPDF breaks a line ~2 pt before the box edge (measured: 2.01–2.13 pt at 6.8–15 pt) and justifies to that width;
    # a 2.3 pt right inset (InDesign measures to the outline, not the advance) makes it break the same lines
    s = re.sub(r'(<InsetSpacing type="list">(?:\s*<ListItem type="unit">[^<]*</ListItem>){3}\s*<ListItem type="unit">)[^<]*',
               r"\g<1>2.3", s, count=1)
    return s.replace('FirstBaselineOffset="LeadingOffset"', f'FirstBaselineOffset="FixedHeight" MinimumFirstBaselineOffset="{base:.3f}"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("article_id"); ap.add_argument("out"); ap.add_argument("--template", default=TEMPLATE)
    args = ap.parse_args()
    MASTER, AID, OUT, MB2 = args.master, args.article_id, args.out, args.template
    rows = [{k.lstrip("﻿"): v for k, v in x.items()} for x in csv.DictReader(open(MASTER, encoding="utf-8"))]
    row = next(x for x in rows if x["article_id"] == AID)
    cp.EMAILS.update(cp.load_emails(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(MASTER))), "autorzy.tsv")))
    geo, size = geometry(row)
    st = content(row)
    tmp = tempfile.mkdtemp()
    zipfile.ZipFile(MB2).extractall(tmp)
    j = lambda *p: os.path.join(tmp, *p)
    for f in os.listdir(j("Stories")):
        os.remove(j("Stories", f))
    spread = open(j("Spreads", "Spread_uf9.xml"), encoding="utf-8").read()
    tpl = re.search(r'\t\t<TextFrame Self="u135".*?</TextFrame>\n', spread, re.S).group(0)
    spread = re.sub(r'\t\t<TextFrame Self=.*?</TextFrame>\n', "", spread, flags=re.S)
    spread = re.sub(r'LinkResourceURI="[^"]*sr_logo\.pdf"', f'LinkResourceURI="{ASSET_LOGO}"', spread)
    frames, ids = "", []
    for i, (name, (x0, y0, x1, y1, base)) in enumerate(geo.items()):
        sid, uid = f"uw{i:02d}", f"uwf{i:02d}"
        ids.append(sid)
        open(j("Stories", f"Story_{sid}.xml"), "w", encoding="utf-8").write(story_xml(sid, st[name]))
        frames += frame_xml(tpl, uid, sid, name, x0, y0, x1, y1, base)
    spread = spread.replace("\t</Spread>", frames + "\t</Spread>")
    open(j("Spreads", "Spread_uf9.xml"), "w", encoding="utf-8").write(spread)
    dm = open(j("designmap.xml"), encoding="utf-8").read()
    dm = re.sub(r'\t<idPkg:Story src="Stories/[^"]*" />\n', "", dm)
    dm = dm.replace("\t<idPkg:BackingStory", "".join(f'\t<idPkg:Story src="Stories/Story_{s}.xml" />\n' for s in ids) + "\t<idPkg:BackingStory")
    dm = re.sub(r'StoryList="[^"]*"', f'StoryList="{" ".join(ids)} u99"', dm)
    dm = dm.replace('Name="SROM_okladka_szablon_MB2.indd"', 'Name="SROM_okladka_szablon_MB3.indd"')
    open(j("designmap.xml"), "w", encoding="utf-8").write(dm)
    for f, fn in (("Styles.xml", styles_xml), ("Fonts.xml", fonts_xml)):
        p = j("Resources", f)
        new = fn(open(p, encoding="utf-8").read())
        open(p, "w", encoding="utf-8").write(new)
    # Adobe Fonts' variable Fraunces: InDesign 2026 imports "Regular" at 12 pt as a custom instance "9pt-12.000" with
    # the weight lost (Thin), whatever this setting; hence the static "Fraunces 9pt" for the title. Off, so that
    # resizing the variable italic never moves it off the opsz 9 instance the PDF uses.
    p = j("Resources", "Preferences.xml")
    pref = open(p, encoding="utf-8").read()
    assert 'UseOpticalSize="true"' in pref
    open(p, "w", encoding="utf-8").write(pref.replace('UseOpticalSize="true"', 'UseOpticalSize="false"'))
    g = j("Resources", "Graphic.xml")
    gx = open(g, encoding="utf-8").read()
    red0 = re.search(r'\t<Color Self="Color/SROM red".*?/>\n', gx).group(0)
    red = red0.replace('ColorValue="227 0 11"', 'ColorValue="223 38 30"')      # the website's red #DF261E (MB 21.10.2026)
    gx = gx.replace(red0, red)
    ink = (red.replace("SROM red", "SROM ink").replace('Space="RGB" ColorValue="223 38 30"', 'Space="CMYK" ColorValue="0 0 0 88"')
           .replace("u12ColorGroupSwatcha", "u12ColorGroupSwatchweb"))
    open(g, "w", encoding="utf-8").write(gx.replace(red, red + ink))
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w") as z:
        z.write(j("mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, _, files in os.walk(tmp):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, tmp)
                if rel != "mimetype":
                    z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
    shutil.rmtree(tmp)
    print(f"written {OUT} ({len(ids)} stories, abstracts {size} pt)")
    for n, v in geo.items():
        print(f"  {n:16s} x {v[0]:.1f}–{v[2]:.1f}  top {v[1]:.1f}  first baseline +{v[4]:.2f}")


if __name__ == "__main__":
    main()
