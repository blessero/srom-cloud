"""MB's view of a record: what he needs from ikonografia.md, nothing of the run log (MB 21.11.2026).

    ikonografia_view.py <record dir> [--out file.html]     prints (or writes) the HTML fragment
    from ikonografia_view import render_view                render_view(record_dir) -> (html, toc)

`ikonografia.md` stays the full record (the log: run notes, search terms, the candidate list of § 2, states). The view
shows, in this order:
  § 0 Na start         the proposal („Propozycja wyboru”) and the few things MB should know first; written by hand
  Sloty i kandydaci    built from kontaktowka.json (slots, rows, `rec`) joined with the § 1 brief table (passage,
                       type as an icon, angle): one place instead of the brief plus the § 2 list
  § 6, § 4, § 3        doubts, permissions, the register (§ 3 only once it has rows: the images going to print)
  § 7, § 8 …           footnote or literature leads, any later section
  § 5                  searches that found nothing, last
The header above § 1, the prose of § 1 and § 2 stay in the md only. Section numbers are kept, so „§ 6” on the sheet and
in Biurko still points at the right place. Used by kontaktowka_build.py (the sheet's „Zapis” panel) and by Biurko's
Czytnik (desk_sync.py) for `*/ikonografia/ikonografia.md`.
"""
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import md_html

PL = {"0": "Na start", "1": "Brief", "2": "Kandydaci", "3": "Rejestr: obrazy do druku (plik, metryka, zgoda)",
      "4": "Zgody", "5": "Wyszukiwania bez wyniku", "6": "Wątpliwości", "7": "Tropy z przypisów i literatury"}
TYPES = [  # (keyword in the brief's type cell, icon, Polish label)
    ("cited source", "📜", "źródło cytowane"), ("source", "📜", "źródło cytowane"),
    ("map", "🗺️", "miejsce / mapa"), ("place", "🗺️", "miejsce / mapa"), ("building", "🏛️", "budynek"),
    ("person", "👤", "osoba"), ("portrait", "👤", "osoba"), ("event", "📅", "wydarzenie"),
    ("archive", "🗄️", "dokument / archiwum"), ("document", "🗄️", "dokument / archiwum"),
    ("ethnographic", "👁️", "obraz etnograficzny"), ("photograph", "📷", "fotografia"),
    ("comparative", "⚖️", "porównanie"), ("extension", "➕", "rozszerzenie"), ("art", "🎨", "sztuka"),
]
ANGLES = {"documentary": "dokumentalny", "immersive": "immersyjny", "argument": "argument", "extension": "rozszerzenie"}


def sections(text):
    """{num: (title, body)} for "## n. Title" sections; the H1 line."""
    h1 = re.search(r"^# (.+)$", text, re.M)
    out = {}
    for m in re.finditer(r"^## (\d+)\.[ \t]*([^\n]*)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        out[m[1]] = (m[2].strip(), m[3].strip())
    return (h1[1].strip() if h1 else ""), out


def brief_rows(body):
    """The § 1 table as {slot key: {passage, type, idea, angle}} (column names from its header row)."""
    lines = [l for l in body.split("\n") if l.lstrip().startswith("|")]
    if len(lines) < 3:
        return {}
    head = [c.lower() for c in md_html._cells(lines[0])]
    col = lambda *names: next((k for k, h in enumerate(head) if any(h.startswith(n) for n in names)), None)
    ks, kp, kt, ki, ka = col("slot"), col("passage"), col("type"), col("idea"), col("angle")
    out = {}
    for l in lines[2:]:
        c = md_html._cells(l)
        get = lambda k: c[k] if k is not None and k < len(c) else ""
        if ks is not None and get(ks):
            out[norm(get(ks))] = {"passage": get(kp), "type": get(kt), "idea": get(ki), "angle": get(ka)}
    return out


def norm(slot):
    return re.sub(r"[\s*`]", "", slot).replace("^2", "²")


def icons(t):
    t, seen, out = t.lower(), set(), []
    for kw, ic, lab in TYPES:
        if kw in t and lab not in seen:
            seen.add(lab)
            out.append(f'<span class="ty" title="{lab}">{ic}</span>')
    return "".join(out)


def angle(a):
    a = a.lower()
    words = [pl for en, pl in ANGLES.items() if en in a]
    return f'<span class="an">{" · ".join(words)}</span>' if words else ""


def short(s, n=110):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def slots_html(rows, brief):
    """One block per slot: idea, type icons, angle, passage; then its candidates, one short line each."""
    out = ['<p class="lg">Typ: ' + " ".join(f'{ic} {lab}' for lab, ic in
           dict((lab, ic) for _, ic, lab in TYPES).items()) +
           ' · <span class="dot p1"></span> główne, <span class="dot p2"></span> dodatkowe (propozycja) · ² slot drugorzędny</p>']
    items = rows.get("items", [])
    for slot, idea in rows.get("slots", {}).items():
        b = brief.get(norm(slot), {})
        meta = " ".join(x for x in (icons(b.get("type", "")), angle(b.get("angle", ""))) if x)
        out.append(f'<h3 id="slot-{html.escape(slot)}">{html.escape(slot)} · {md_html.inline(idea)}</h3>')
        if meta or b.get("passage"):
            out.append(f'<p class="sm">{meta}{" " if meta and b.get("passage") else ""}'
                       f'{"<span class=psg>" + md_html.inline(b["passage"]) + "</span>" if b.get("passage") else ""}</p>')
        li = []
        for i in (x for x in items if x.get("slot") == slot):
            dot = f'<span class="dot p{i["rec"]}"></span>' if i.get("rec") in ("1", "2") else '<span class="dot"></span>'
            t = html.escape(short(i.get("title", "")))
            if i.get("page"):
                t = f'<a href="{html.escape(i["page"])}" target="_blank" rel="noopener noreferrer">{t}</a>'
            d = html.escape(short(i.get("date", ""), 40))
            li.append(f'<li>{dot}<b>{html.escape(i["id"])}</b> · {t}{" · " + d if d else ""}</li>')
        out.append('<ul class="cand">' + "".join(li) + "</ul>" if li else '<p class="sm">— brak kandydatów</p>')
    return "\n".join(out)


def has_rows(body):
    """A section's table has at least one data row with content (an empty register shows only its header)."""
    lines = [l for l in body.split("\n") if l.lstrip().startswith("|")]
    return any("".join(md_html._cells(l)).strip(" -:") for l in lines[2:])


def render_view(d):
    d = pathlib.Path(d)
    text = (d / "ikonografia.md").read_text(encoding="utf-8")
    rp = d / "kontaktowka.json"
    rows = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    h1, sec = sections(text)
    parts, toc, seen = [f"<h1>{md_html.inline(h1)}</h1>"], [], set()

    def add(num, title, body_html):
        sid = f"sec-{num}"
        parts.append(f'<h2 id="{sid}">{num + ". " if num.isdigit() else ""}{html.escape(title)}</h2>\n{body_html}')
        toc.append((2, sid, title))

    def md(body):
        h, _ = md_html.render(re.sub(r"^#{1,3} ", "#### ", body, flags=re.M))  # sub-headings stay below h3
        return h

    if "0" in sec:
        add("0", PL["0"], md(sec["0"][1]))
    if rows.get("slots"):
        add("S", "Sloty i kandydaci", slots_html(rows, brief_rows(sec.get("1", ("", ""))[1])))
    for n in ("6", "4", "3"):
        if n in sec and (n != "3" or has_rows(sec[n][1])):
            add(n, PL[n], md(sec[n][1]))
    for n in sorted((k for k in sec if k not in ("0", "1", "2", "3", "4", "5", "6")), key=int):
        add(n, PL.get(n) or sec[n][0], md(sec[n][1]))
    if "5" in sec:
        add("5", PL["5"], md(sec["5"][1]))
    return "\n".join(parts), toc


if __name__ == "__main__":
    h, _ = render_view(sys.argv[1])
    if "--out" in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index("--out") + 1]).write_text(h, encoding="utf-8")
    else:
        print(h)
