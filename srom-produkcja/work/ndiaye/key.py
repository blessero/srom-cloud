# Keying Ndiaye, "Black Roma": literal short-form notes (ndiaye_pdf.md) -> [@key, s. N] tokens (ndiaye_src.md).
# Rules: srom-typeset/references/srom-md.md "Keying short-form notes". Every change is logged to key_log.md.
import re, sys, json
sys.path.insert(0, "../../.claude/skills/srom-typeset/scripts")
from cite_map import expand_ranges

# author form in the notes -> key, or {year: key}
AUTH = {
    "Admant": "admant2015", "Andrews": "andrews1993", "Asséo": {"1974": "asseo1974", "2009": "asseo2009"},
    "Boulanger": "boulanger2000", "Brome": "brome", "Brooks": "brooks2012", "Browne": "browne1672", "Camus": "camus1640",
    "Carlell": "carlell1657", "Cathelin": "cathelin2004", "Chang and Rucker-Chang": "chang2020", "Chevreau": "chevreau1656",
    "Cressy": "cressy2016", "Crooks": "crooks1931", "Damon": "damon1997", "Dauge-Roth": "daugeroth2019", "Davity": "davity1660",
    "Dodoens and Lyte": "dodoens1578", "Filhol": {"2010": "filhol2010", "2013": "filhol2013"}, "Fleay": "fleay1891",
    "Forestier": "forestier1988", "Fra-Molinero": "framolinero1995", "Galland": "galland2017", "Goldberg": "goldberg2019",
    "Harbage": "harbage1940", "Head": "head1688", "Hendricks and Parker": "hendricks1994", "Hitchcock": "hitchcock2016",
    "Hornback": "hornback2018", "Hutner": "hutner2001", "Jaffe-Berg": "jaffeberg2015", "Katritzky": "katritzky2006",
    "King": "king2019", "Kóczé": "kocze2020", "Krantz": "krantz1520", "Lawrence": "lawrence1912", "Levin": "levin1967",
    "Lowe": "lowe2015", "Lucassen and Willems": "lucassen2003", "M. W., M. A.": "mw1662", "M.W.": "mw1662",
    "Matache and West": "matache2018", "Matras": "matras2014", "Mayall": "mayall2004", "McKee": "mckee2008",
    "Mejia-LaPerle": "mejialaperle2017", "Ménestrier": "menestrier1682", "Mills": "mills1997",
    "Molière": {y: f"moliere{y}" for y in ("1663", "1668", "1671", "1673", "1674", "1827")}, "Montluc": "montluc1654",
    "Ndiaye": {"2021": "ndiaye2021", "2022": "ndiaye2022"}, "Netzloff": "netzloff2003", "Newman": "newman2015",
    "Nicoll": "nicoll1963", "Nocentelli": "nocentelli2013", "Park Hong": "parkhong2021", "Pasquier": "pasquier1621",
    "Patterson": "patterson1982", "Phillips": "phillips2008", "Plésiat": "plesiat2010",
    "Ravenscroft": {"1672": "ravenscroft1672", "1677": "ravenscroft1677", "1678": "ravenscroft1678"},
    "Reynolds": "reynolds2002", "Robinson": "robinson1983", "Ruggle": "ruggle1662", "Sallebray": "sallebray1642",
    "Scudéry": "scudery1649", "Sentaurens": "sentaurens1984", "Taylor": "taylor2014", "Thompson": "thompson2008",
    "Touam Bona": "touambona2016", "Vallée": "vallee1657", "Van Lannep": "vanlennep1965",
    "Wagner and Andrzejewski": "wagner2019", "Zysberg": "zysberg1987",
}
NAMES = "|".join(re.escape(n) for n in sorted(AUTH, key=len, reverse=True))
PAGES = r"\d+[a-z]?(?:–\d+)?(?:, \d+(?:–\d+)?)*(?!\.\d)"
SPECIAL = r"\d+\.\d+\.\d+(?:–\d+)?|[A-Z]\d+[ʳᵛ]|lines \d+(?:–\d+)?|n\.p\."
# one citation: Name[, year][, locator]; the year only when it is one of the author's years
CIT = re.compile(rf"(?<![\w’])(?P<name>{NAMES})(?:,\s(?P<year>1[5-9]\d\d|20\d\d)(?=[,.;\s]))?(?:,\s(?P<loc>{SPECIAL}|{PAGES}))?")
LEAD = [("See also ", "Zob. też "), ("see also ", "zob. też "), ("See ", "Zob. "), ("see ", "zob. "), ("cf. ", "por. "),
        ("Quoted in ", "Cyt. za "), ("quoted in ", "cyt. za ")]

log = []


def key_of(name, year, note):
    k = AUTH[name]
    if isinstance(k, dict):
        if year not in k:
            raise SystemExit(f"note {note}: {name} without a known year ({year})")
        return k[year]
    if year:
        raise SystemExit(f"note {note}: {name} has one work but a year {year} follows")
    return k


def loc_of(loc):
    if not loc:
        return ""
    if loc == "n.p.":
        return None                      # no page: whole work
    if loc.startswith("lines "):
        return ", {w. " + expand_ranges(loc[6:]) + "}"
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+(?:–\d+)?)", loc)
    if m:                                # act.scene.line — written out until MB decides the form (queries Q)
        log.append(f"act.scene.line {loc} -> akt {m.group(1)}, sc. {m.group(2)}, w. {m.group(3)}")
        return ", {akt " + m.group(1) + ", sc. " + m.group(2) + ", w. " + m.group(3) + "}"
    if re.fullmatch(r"[A-Z]\d+[ʳᵛ]", loc):   # printer's signature: k. S2r (Kanon § 7.2)
        sig = "k. " + loc[:-1] + {"ʳ": "r", "ᵛ": "v"}[loc[-1]]
        log.append(f"signature {loc} -> {sig}")
        return ", {" + sig + "}"
    full = expand_ranges(loc)
    if full != loc:
        log.append(f"range in full: {loc} -> {full}")
    return ", s. " + full


def cite(m, note):
    name, year, loc = m.group("name"), m.group("year"), m.group("loc")
    k = key_of(name, year, note)
    l = loc_of(loc)
    return "@" + k + (l or "")


# citations that stand as a reference without a locator (a bare name keyed only where it is a reference, not prose)
BARE = {9: ["Fra-Molinero"], 13: ["Wagner and Andrzejewski"], 60: ["Cressy"], 62: ["Lucassen and Willems"],
        89: ["Thompson"], 120: ["Hutner", "Hendricks and Parker", "Nocentelli"], 125: ["Wagner and Andrzejewski"],
        127: ["Matache and West"], 129: ["Cathelin"]}
# must stay prose (a name, not a reference): checked below
PROSE_OK = {"Brooks is", "Mills defines", "Ménestrier closely", "Asséo counts", "Dauge-Roth underlines", "Asséo points",
            "Robinson briefly", "Robinson to", "Fleay writes", "Hornback’s", "Ruggle’s", "Ravenscroft also",
            "Ravenscroft, whose", "Matras, take", "Newman’s", "Crooks’s", "Cervantes"}


def key_note(n, text):
    out, pos = [], 0
    spans = []
    for m in CIT.finditer(text):
        is_ref = m.group("year") or m.group("loc")
        if not is_ref and m.group("name") in BARE.get(n, []) and re.match(r"[.;,]", text[m.end():m.end() + 1] or "."):
            is_ref = True
        if not is_ref:
            continue
        if m.group("name") == "Ravenscroft" and not m.group("year"):
            continue                     # "Ravenscroft, whose career …" (prose)
        spans.append(m)
    # group citations joined by "; " into one bracket
    groups, cur = [], []
    for m in spans:
        if cur and text[cur[-1].end():m.start()] == "; ":
            cur.append(m)
        else:
            if cur:
                groups.append(cur)
            cur = [m]
    if cur:
        groups.append(cur)
    for g in groups:
        s, e = g[0].start(), g[-1].end()
        pre = text[pos:s]
        lead = ""
        for en, pl in LEAD:
            if pre.endswith(en):
                pre, lead = pre[:-len(en)], pl
                log.append(f"note {n}: lead-in '{en.strip()}' -> '{pl.strip()}'")
                break
        items = []
        for m in g:
            if m.group("loc") == "n.p.":
                log.append(f"note {n}: {m.group(0)} -> whole work (n.p. = no page)")
            items.append(cite(m, n))
        out.append(pre + lead + "[" + "; ".join(items) + "]")
        pos = e
    out.append(text[pos:])
    res = "".join(out)
    # "n.p. (book 11, chapter 2)": no page; the book and chapter are the locator (Polish labels, srom-md.md)
    def bc(m):
        log.append(f"note {n}: n.p. (book {m.group(2)}, chapter {m.group(3)}) -> {{ks. {m.group(2)}, rozdz. {m.group(3)}}}")
        return f"[@{m.group(1)}, {{ks. {m.group(2)}, rozdz. {m.group(3)}}}]"
    return re.sub(r"\[@(\w+)\] \(book (\d+), chapter (\d+)\)", bc, res)


src = open("ndiaye_pdf.md", encoding="utf-8").read()
res, keyed_notes = [], 0
for line in src.split("\n"):
    m = re.match(r"^\[\^(\d+)\]: (.*)$", line)
    if m:
        n, t = int(m.group(1)), m.group(2)
        k = key_note(n, t)
        if k != t:
            keyed_notes += 1
        if n == 59:                       # a web reference given as a bare URL: lead-in only, stays literal
            k = k.replace("See https://", "Zob. https://")
            log.append("note 59: lead-in 'See' -> 'Zob.' (URL stays literal)")
        res.append(f"[^{n}]: {k}")
    else:
        res.append(line)
out = "\n".join(res)
open("ndiaye_src.md", "w", encoding="utf-8").write(out)
open("key_log.md", "w", encoding="utf-8").write("# Keying log\n\n" + "\n".join(f"- {x}" for x in log) + "\n")

# report every note left without a citation, and every author name left outside a token, for review
for line in out.split("\n"):
    m = re.match(r"^\[\^(\d+)\]: (.*)$", line)
    if not m:
        continue
    n, t = int(m.group(1)), m.group(2)
    bare = re.sub(r"\[[^\]]*@[^\]]*\]", "", t)
    left = [x.group(0) for x in re.finditer(rf"(?<![\w’])(?:{NAMES})\S*\s?\S*", bare)]
    left = [x for x in left if not any(x.startswith(p) for p in PROSE_OK)]
    if "@" not in t or left:
        print(f"[{n}] {'NO CITATION ' if '@' not in t else ''}{left or ''}  {t[:110]}")
print(f"keyed notes: {keyed_notes}")
