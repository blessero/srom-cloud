#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from normalize import Normalizer

# (input, expected output, expected flag rule or None)
CASES = [
    # quotes
    ('Mówił "tak" i "nie".', "Mówił „tak” i „nie”.", None),
    ("Mówił “tak” i ‘gloss’.", "Mówił „tak” i ‘gloss’.", None),
    ('Tytuł "Rom "wędrowny" i osiadły".', "Tytuł „Rom »wędrowny« i osiadły”.", None),
    ("Cytat „zewnętrzny «wewnętrzny» koniec”.", "Cytat „zewnętrzny »wewnętrzny« koniec”.", None),
    ('Otwarty "cytat bez końca.', 'Otwarty "cytat bez końca.', "QUOTE-UNBALANCED"),
    ('Tytuł *"Rom"* w tekście.', "Tytuł *„Rom”* w tekście.", None),
    # dashes and ranges
    ("W latach 1939-1945 i s. 15 - 20.", "W latach 1939–1945 i s. 15–20.", None),
    ("To prawda - powiedział — i odszedł.", "To prawda – powiedział – i odszedł.", None),
    ("Okres 1918 – 1939 oraz 5-6 osób.", "Okres 1918–1939 oraz 5–6 osób.", None),
    ("w 1918 – 20 lat później", "w 1918 – 20 lat później", None),
    ("polsko-romski słownik", "polsko-romski słownik", None),
    ("Adres: 33-100 Tarnów.", "Adres: 33-100 Tarnów.", "POSTCODE-OR-RANGE"),
    ("Zob. https://x.pl/2019-2020/a-b oraz DOI 10.1234/ab-12-34.", "Zob. https://x.pl/2019-2020/a-b oraz DOI 10.1234/ab-12-34.", None),
    ("ISBN 978-83-08-01234-5 i data 2019-05-03.", "ISBN 978-83-08-01234-5 i data 2019-05-03.", None),
    ("Sygnatura RG-25.004M bez zmian.", "Sygnatura RG-25.004M bez zmian.", None),
    ("- punkt listy - z pauzą", "- punkt listy – z pauzą", None),
    # spaces, ellipsis, omissions
    ("Tekst  z   wieloma\u00a0spacjami , i ( nawiasem ) .", "Tekst z wieloma spacjami, i (nawiasem).", None),
    ("Opuszczenie (...) i [...] oraz wielokropek...", "Opuszczenie […] i […] oraz wielokropek…", None),
    ("Znak\u00admiękki\u200b usunięty.", "Znakmiękki usunięty.", None),
    # note markers
    ("Zdanie kończy się.[^1] Następne,[^2] i dalej", "Zdanie kończy się[^1]. Następne[^2], i dalej", None),
    ("W 1943 r.[^3] zmarł.", "W 1943 r.[^3] zmarł.", None),
    ("Cytat „słowa[^4]” koniec.", "Cytat „słowa”[^4] koniec.", None),
    ("Cytat „słowa”.[^5]", "Cytat „słowa”[^5].", None),
    ("Tekst.[@ficowski1985, s. 15-20]", "Tekst[@ficowski1985, s. 15–20].", None),
    ("Tekst. [@ficowski1985, s. 15]", "Tekst. [@ficowski1985, s. 15]", "CITE-AFTER-PUNCT"),
    # "; [@b]" and the definition head "[^1]: [@a]" are normal in notes — must NOT be flagged ("!" = no flag)
    ("[^1]: [@ficowski1985, s. 15]; zob. też [@hancock2007].", "[^1]: [@ficowski1985, s. 15]; zob. też [@hancock2007].", "!CITE-AFTER-PUNCT"),
    # fenced interlinear example: verbatim (alignment spaces, straight quotes untouched)
    ("::: przyklad\n```\n(1)  Me   dikhav \"x\"\n     1SG  widzieć\n```\n:::", "::: przyklad\n```\n(1)  Me   dikhav \"x\"\n     1SG  widzieć\n```\n:::", None),
    # verse: forced line break (trailing backslash) survives
    ("> pierwszy wers,\\\n> drugi wers.", "> pierwszy wers,\\\n> drugi wers.", None),
    # initials, apostrophe
    ("Według R. L. Turnera i J. P. Kleiwega.", "Według R.L. Turnera i J.P. Kleiwega.", None),
    ("Pisał O'Brien.", "Pisał O’Brien.", None),
    # apparatus labels in notes only
    ("[^1]: J. Nowak, *Tytuł*, przeł. A. B, [w:] *Tom*, str. 5, ss. 7-9; ibid., s. 3.",
     "[^1]: J. Nowak, *Tytuł*, tłum. A. B, w: *Tom*, s. 5, s. 7–9; *Ibidem*, s. 3.", None),
    ("W tekście cytat „str. 5 przeł. X” zostaje.", "W tekście cytat „str. 5 przeł. X” zostaje.", None),
    ("[^2]: Zob. op. cit., s. 5.", "[^2]: Zob. op. cit., s. 5.", "BACKREF-FORBIDDEN"),
    ("[^3]: Ukraïns'kyi zhurnal, s. 5.", "[^3]: Ukraïns'kyi zhurnal, s. 5.", "APOSTROPHE-OR-SOFTSIGN"),
    # structure untouched
    ("::: {custom-style=\"Tekst\"}", "::: {custom-style=\"Tekst\"}", None),
    ("[*Tytuł*]{custom-style=\"Kursywa\"} i [Mróz]{.smallcaps}", "[*Tytuł*]{custom-style=\"Kursywa\"} i [Mróz]{.smallcaps}", None),
]


def main():
    ok = 0
    for i, (src, exp, fl) in enumerate(CASES, 1):
        nz = Normalizer()
        got = nz.run(src)
        rules = [f[1] for f in nz.flags]
        if fl and fl.startswith("!"):
            good = got == exp and fl[1:] not in rules
        else:
            good = got == exp and (fl is None or fl in rules)
        # idempotence
        nz2 = Normalizer()
        again = nz2.run(got)
        if again != got or nz2.log:
            good = False
            print(f"  not idempotent: {nz2.log}")
        if good:
            ok += 1
        else:
            print(f"FAIL {i}: {src!r}\n   got {got!r}\n   exp {exp!r}\n   flags {rules}")
    total = len(CASES)
    print(f"NORMALIZE ALL PASS {ok}/{total}" if ok == total else f"NORMALIZE FAILED {ok}/{total}")


if __name__ == "__main__":
    main()
