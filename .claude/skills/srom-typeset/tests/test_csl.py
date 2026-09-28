#!/usr/bin/env python3
"""Kanon examples (§ 7, § 9) as a test suite for csl/srom.csl (raw citeproc output, before srom_post.lua)."""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CSL = os.path.join(HERE, "..", "csl", "srom.csl")
REFS = os.path.join(HERE, "fixtures", "kanon_refs.json")


def ser(x):
    if isinstance(x, list):
        return "".join(ser(i) for i in x)
    t, c = x["t"], x.get("c")
    if t == "Str": return c
    if t in ("Space", "SoftBreak"): return " "
    if t == "Emph": return "*" + ser(c) + "*"
    if t == "SmallCaps": return "[" + ser(c) + "]{.sc}"
    if t == "Quoted": return ("„" + ser(c[1]) + "”") if c[0]["t"] == "DoubleQuote" else ("»" + ser(c[1]) + "«")
    if t == "Span": return ser(c[1])
    if t == "Link": return ser(c[1])
    if t == "Cite": return ser(c[1])
    if t == "Note": return ""
    if t in ("Para", "Plain"): return ser(c)
    raise ValueError(t)


def notes_of(blocks):
    out = []
    def walk(x):
        if isinstance(x, list):
            for i in x: walk(i)
        elif isinstance(x, dict):
            if x.get("t") == "Note":
                out.append(" ".join(ser(b) for b in x["c"]))
                walk(x["c"])  # nested cites inside notes are inline, not new notes
            elif "c" in x:
                walk(x["c"])
    walk(blocks)
    return out


def render(md, extra=()):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("---\nlang: pl-PL\nnotes-after-punctuation: false\n---\n" + md)
    r = subprocess.run(["pandoc", f.name, "-f", "markdown-smart", "--citeproc", "--csl", CSL,
                        "--bibliography", REFS, "-t", "json", *extra], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr)
    return json.loads(r.stdout)


NOTES = [
    ("ficowski1985", "s. 15", "J. Ficowski, *Cyganie na polskich drogach*, Wydawnictwo Literackie, Kraków 1985, s. 15."),
    ("mroz1998", "s. 40-42", "L. Mróz, A. Bartosz, *Tytuł pracy*, Wydawnictwo, Warszawa 1998, s. 40–42."),
    ("fialkowska2020", "s. 12", "K. Fiałkowska i in., *Tytuł pracy*, Wydawnictwo, Warszawa 2020, s. 12."),
    ("kowalski2011", "s. 88", "A. Kowalski (red.), *Tytuł tomu*, Wydawnictwo, Kraków 2011, s. 88."),
    ("mroz2011", "s. 88-104", "L. Mróz, *Tytuł rozdziału*, w: *Tytuł tomu*, red. A. Kowalski, Wydawnictwo, Kraków 2011, s. 88–104."),
    ("kolaczek2012", "s. 217", "M. Kołaczek, *Tytuł artykułu*, „Studia Romologica”, 2012, nr 5, s. 217."),
    ("ploski1947", "s. 310", "S. Płoski, *Relacja von dem Bacha o powstaniu warszawskim*, „Dzieje Najnowsze”, 1947, t. 1, z. 2, s. 310."),
    ("turner1926", "s. 145", "R.L. Turner, *The position of Romani*, „Journal of the Gypsy Lore Society”, 1926, t. 5, nr 4, s. 145."),
    ("hancock2007", "s. 33", "I. Hancock, *Tytuł*, tłum. J. Nowak, Wydawnictwo, Warszawa 2007, s. 33."),
    ("bartosz2019", "s. 51", "A. Bartosz, *Tytuł*, wyd. 3 popr., Wydawnictwo, Tarnów 2019, s. 51."),
    ("kowalski2015", "s. 77", "A. Kowalski, *Tytuł*, t. 2: *Tytuł tomu*, Wydawnictwo, Kraków 2015, s. 77."),
    ("nowak2010", "s. 221", "A. Nowak, *Romani chib*, w: *Tytuł encyklopedii*, t. 4, Wydawnictwo, Warszawa 2010, s. 221."),
    ("marsh2008", "s. 21", "A. Marsh, *Ethnicity and Identity*, w: *We are Here*, red. E. Uzpeder, EDROM, Istanbul 2008, s. 21."),
    ("kopanska2018", "s. 60", "J. Kopańska, *Tytuł*, Uniwersytet Jagielloński, Kraków 2018, s. 60 (maszynopis pracy doktorskiej, egzemplarz przechowywany w Bibliotece Jagiellońskiej)."),
    ("demeter2018", "s. 5", "N. Demeter, *Istoriia tsygan* [Historia Cyganów], Nauka, Moskva 2018, s. 5."),
    ("nowak1963", "s. 3", "J. Nowak, *Tytuł artykułu*, „Gazeta Krakowska”, 1963, nr 145, s. 3."),
    ("nsp2021", "{tabl. 14}", "*Narodowy Spis Powszechny Ludności i Mieszkań 2021. Wyniki wstępne*, GUS, Warszawa 2022, tabl. 14."),
    ("kowalskiweb", None, "A. Kowalski, *Tytuł tekstu*, w: *Nazwa serwisu*, https://przyklad.pl/tekst [dostęp: 18.03.2025]."),
    ("papusza", "00:42:15", "*Papusza*, reż. J. Kos-Krauze, K. Krauze, Polska 2013, 00:42:15."),
    ("czas1928", "s. 2", "„Czas”, 03.05.1928, s. 2."),
]

BIB = {
    "ficowski1985": "[Ficowski]{.sc}, Jerzy. *Cyganie na polskich drogach*, Wydawnictwo Literackie, Kraków 1985.",
    "mroz1998": "[Mróz]{.sc}, Lech, [Bartosz]{.sc}, Adam. *Tytuł pracy*, Wydawnictwo, Warszawa 1998.",
    "fialkowska2020": "[Fiałkowska]{.sc}, Kamila, [Garapich]{.sc}, Michał P., [Mirga-Wójtowicz]{.sc}, Elżbieta, [Kowalski]{.sc}, Jan. *Tytuł pracy*, Wydawnictwo, Warszawa 2020.",
    "kowalski2011": "[Kowalski]{.sc}, Andrzej (red.). *Tytuł tomu*, Wydawnictwo, Kraków 2011.",
    "mroz2011": "[Mróz]{.sc}, Lech. *Tytuł rozdziału*, w: *Tytuł tomu*, red. A. Kowalski, Wydawnictwo, Kraków 2011, s. 88–104.",
    "kolaczek2012": "[Kołaczek]{.sc}, Małgorzata. *Tytuł artykułu*, „Studia Romologica”, 2012, nr 5, s. 211–228. DOI: 10.1234/srom.2012.5.11.",
    "turner1926": "[Turner]{.sc}, Ralph L. *The position of Romani*, „Journal of the Gypsy Lore Society”, 1926, t. 5, nr 4, s. 145–189.",
    "hancock2007": "[Hancock]{.sc}, Ian. *Tytuł*, tłum. J. Nowak, Wydawnictwo, Warszawa 2007.",
    "demeter2018": "[Demeter]{.sc}, Nadezhda. *Istoriia tsygan* [Historia Cyganów], Nauka, Moskva 2018.",
    "kopanska2018": "[Kopańska]{.sc}, Joanna. *Tytuł*, Uniwersytet Jagielloński, Kraków 2018 (maszynopis pracy doktorskiej, egzemplarz przechowywany w Bibliotece Jagiellońskiej).",
    "kowalskiweb": "[Kowalski]{.sc}, Andrzej. *Tytuł tekstu*, w: *Nazwa serwisu*, https://przyklad.pl/tekst [dostęp: 18.03.2025].",
}

POSITION_MD = (
    "A [@ficowski1985, s. 15]. B [@ficowski1985, s. 17]. C [@ficowski1985, s. 17].^[Archiwum X.] "
    "D [@ficowski1985, s. 20]. E [@mroz1998, s. 40; @ficowski1985, s. 21]. F [@ficowski1985, s. 21]. "
    "G [@kolaczek2012]. H [@kolaczek2012, s. 212]."
)
POSITION_EXP = [
    "J. Ficowski, *Cyganie na polskich drogach*, Wydawnictwo Literackie, Kraków 1985, s. 15.",
    "*Ibidem*, s. 17.",
    "*Ibidem*.",
    "Archiwum X.",
    "Ficowski, *Cyganie na polskich drogach…*, s. 20.",
    "L. Mróz, A. Bartosz, *Tytuł pracy*, Wydawnictwo, Warszawa 1998, s. 40; Ficowski, *Cyganie na polskich drogach…*, s. 21.",
    "Ficowski, *Cyganie na polskich drogach…*, s. 21.",
    "M. Kołaczek, *Tytuł artykułu*, „Studia Romologica”, 2012, nr 5, [BRAK STRONY].",
    "*Ibidem*, s. 212.",
]


def check(label, pairs):
    ok = 0
    for name, got, exp in pairs:
        if got == exp:
            ok += 1
        else:
            print(f"FAIL {label} {name}\n   got {got}\n   exp {exp}")
    print(f"{label} ALL PASS {ok}/{len(pairs)}" if ok == len(pairs) else f"{label} FAILED {ok}/{len(pairs)}")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("notes", "all"):
        md = " ".join(f"X{i} [@{k}{', ' + loc if loc else ''}]." for i, (k, loc, _) in enumerate(NOTES))
        notes = notes_of(render(md)["blocks"])
        pairs = [(k, notes[i] if i < len(notes) else "<missing>", exp) for i, (k, _, exp) in enumerate(NOTES)]
        # short form (§7.3)
        n2 = notes_of(render("A [@ficowski1985, s. 15]. B [@mroz1998, s. 1]. C [@ficowski1985, s. 51].")["blocks"])
        pairs.append(("short-form", n2[2], "Ficowski, *Cyganie na polskich drogach…*, s. 51."))
        check("NOTES", pairs)
    if what in ("bib", "all"):
        keys = ", ".join("@" + k for k in BIB)
        doc = render(f"---\nnocite: '{keys}'\n---\n\nX\n")
        entries = {}
        for b in doc["blocks"]:
            if b["t"] == "Div" and b["c"][0][0] == "refs":
                for e in b["c"][1]:
                    entries[e["c"][0][0].replace("ref-", "")] = " ".join(ser(x) for x in e["c"][1])
        check("BIB", [(k, entries.get(k, "<missing>"), v) for k, v in BIB.items()])
    if what in ("position", "all"):
        notes = notes_of(render(POSITION_MD)["blocks"])
        pairs = [(f"n{i + 1}", notes[i] if i < len(notes) else "<missing>", e) for i, e in enumerate(POSITION_EXP)]
        # Polish collation (§9.5)
        refs = [{"id": f"p{i}", "type": "book", "author": [{"family": fam, "given": "A"}], "title": "T",
                 "publisher": "W", "publisher-place": "M", "issued": {"date-parts": [[2000]]}}
                for i, fam in enumerate(["Żak", "Zieliński", "Źrebiec", "Łodziński", "Lewandowski", "Ćwiek", "Czarnecki", "Śliwa", "Sowa"])]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(refs, f)
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as g:
            g.write("---\nlang: pl-PL\nnocite: '@*'\n---\n\nX\n")
        r = subprocess.run(["pandoc", g.name, "-f", "markdown-smart", "--citeproc", "--csl", CSL, "--bibliography", f.name, "-t", "plain"],
                           capture_output=True, text=True)
        order = [ln.split(",")[0] for ln in r.stdout.splitlines() if ln.strip() and ln.strip() != "X"]
        exp = ["CZARNECKI", "ĆWIEK", "LEWANDOWSKI", "ŁODZIŃSKI", "SOWA", "ŚLIWA", "ZIELIŃSKI", "ŹREBIEC", "ŻAK"]
        pairs.append(("collation", " ".join(order), " ".join(exp)))
        check("POSITION", pairs)


if __name__ == "__main__":
    main()
