# West Ohueri, "Peripheral whiteness and racial belonging and non-belonging" (Off White, MUP 2024, ch. 6):
#   westohueri_pdf.md (the extraction) -> westohueri_pre.md (prep: Kanon § 4.1 block quotations, stray italic stops,
#   comments for the editor; logged) -> westohueri_src.md (citations keyed). Every change is logged to key_log.md;
#   check.py --keyed pre src proves no page, note or work was lost. Re-run after any re-extraction or change to refs.py.
#  1. Prep (not keying): the three fieldwork statements are set in italics in the original — Kanon § 4.1: block
#     quotations without italics, the Albanian words in them italic (MB 29.09.2026); "*.*" (an italic full stop, invisible)
#     -> "."; DO SPRAWDZENIA comments at the unsourced quotation (Tosk, queries D1) and note 49 (the forthcoming book, D2).
#     Note labels = printed numbers 1–68 (no title note; nothing renumbered).
#  2. Chicago full citations and short forms -> [@key, s. N] (srom-md.md; refs.py). A note that is only citations is
#     replaced whole (WHOLE: the note's text is logged); notes with prose keep it and only the citation is replaced
#     (PAIRS). A citation inside the author's sentence goes in brackets. "Ibid." -> the key (the build decides Ibidem).
#     Lead-ins: See -> Zob., see -> zob., See also -> Zob. też, see also -> zob. też (handoff.md).
#  3. Literal: prose notes 33 and 49 (a book in progress, not a published work). Note 29 "Baker, this volume" is keyed to
#     her chapter in the same book (MB 29.09.2026).
import re, sys
src = open("westohueri_pdf.md", encoding="utf-8").read()
log = ["# key.py log — westohueri", ""]


def sub(text, old, new, why, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"key.py: expected {count}× {old!r}, found {n}")
    log.append(f"prep: {old!r} -> {new!r}: {why}")
    return text.replace(old, new)


# ---- 1. prep
pre = src
for q in re.findall(r"^> \*(.+)\*$", pre, re.M):
    pre = sub(pre, f"> *{q}*", f"> {q}", "fieldwork statement: block quotation without italics (Kanon § 4.1; queries A7)")
pre = sub(pre, "*White Enclosures*, 5*.*", "*White Enclosures*, 5.", "an italic full stop (invisible in print)")
pre = sub(pre, "‘dorë e zezë’*.*", "‘dorë e zezë’.", "an italic full stop (invisible in print)")
pre = sub(pre, "‘reinforced a *Tosk* [southerner][^53] sense of power and later superiority which still permeates Albanian "
          "society today’.", "‘reinforced a *Tosk* [southerner][^53] sense of power and later superiority which still permeates "
          "Albanian society today’. <!-- DO SPRAWDZENIA (pytania D1): cytat bez wskazania źródła; zapewne Blumi, "
          "„Politics” (przyp. 52), strona nieznana – pytanie do autorki -->",
          "comment: a quotation without a source (queries D1)")
# Albanian words inside the (now roman) fieldwork blocks: italic as foreign words, *jevgjit* also as a foreign exonym
# (Kanon § 3.4; MB 29.09.2026: a block is roman except what the Kanon sets in italics)
pre = sub(pre, "you know, the Jevgjit.", "you know, the *Jevgjit*.", "Albanian exonym in a block: italic (Kanon § 3.4)")
pre = sub(pre, "‘je bere si jevg’ (‘you have become like the jevgjit’)", "‘*je bere si jevg*’ (‘you have become like the *jevgjit*’)",
          "Albanian words in a block: italic (Kanon § 3.4)")
pre = sub(pre, "we have become the jevgjit because", "we have become the *jevgjit* because", "Albanian exonym in a block: italic")
pre = sub(pre, "where those jevgjit live.", "where those *jevgjit* live.", "Albanian exonym in a block: italic")
pre = sub(pre, "[^49]: See my forthcoming work, *Albania in Red, Black, and White* (manuscript in progress).",
          "[^49]: See my forthcoming work, *Albania in Red, Black, and White* (manuscript in progress). <!-- DO SPRAWDZENIA "
          "(pytania D2): w 2025 r. ukazała się książka autorki *Encountering Race in Albania* (Cornell UP) – czy to ta praca? -->",
          "comment: the forthcoming book may have appeared (queries D2)")
open("westohueri_pre.md", "w", encoding="utf-8").write(pre)
labels = re.findall(r"^\[\^(\d+)\]:", pre, re.M)
assert labels == [str(i) for i in range(1, 69)], "labels not 1…68"
log.append("labels: 1–68 = printed note numbers")
log.append("")

# ---- 2. keying
WHOLE = {
 1: "[@westohueri2021].", 2: "[@blumi2018, s. 40].", 4: "[@essed2008].", 5: "[@cornell2007; @pierre2012; @yuvaldavis2006].",
 6: "[@robinson2000].", 7: "[@melamed2015].", 8: "[@bhattacharyya2018].", 9: "[@card2020].", 10: "[@goldberg2006].",
 11: "[@said1979; @todorova2009].", 12: "[@todorova2009].", 13: "[@bjelic2022].", 14: "[@zakharov2017].",
 16: "[@rexhepi2023].", 17: "[@kalmar2022].", 18: "[@frankenberg1993].", 19: "[@wekker2016].", 20: "[@bjelic2022].",
 21: "[@maghbouleh2017].", 22: "[@durham1909].", 23: "[@jezernik2004].", 24: "[@linne1964].", 25: "[@jezernik2004].",
 28: "[@malcolm2002].", 30: "[@misha2002].", 31: "[@fishta1997].", 32: "[@tochka2015].", 34: "[@tochka2015].",
 36: "[@tochka2015].", 37: "[@tochka2015].", 38: "[@golemi2020].", 40: "[@golemi2020].", 42: "[@nishku2020].",
 43: "[@galaty2018; @mehilli2017].", 44: "[@peshkopia2021].", 45: "[@misha2002].", 46: "[@hysa2010].", 47: "[@blumi2018].",
 48: "[@turda2007; @turda2010; @bucur2010].", 50: "[@blumi1997, s. 379].", 51: "[@mehilli2017].", 52: "[@blumi1997].",
 54: "[@blumi2018].", 55: "[@nixon2010; @kuus2004].", 56: "[@kajsiu2011].", 57: "[@rexhepi2023, s. 5].", 58: "[@garner2007].",
 59: "[@rexhepi2023].", 60: "[@frankenberg1993; @essed2008].", 62: "[@qesku2004].", 64: "[@kettler2020].",
 65: "[@golemi2020].", 67: "[@erebara2020].", 68: "[@vargas2018].",
}
PAIRS = {
 3: [("See Sevati Trubeta, ‘Balkan Egyptians and Gypsy/Roma Discourse’, *Nationalities Papers*, 33:1 (2005), 71–95.",
      "Zob. [@trubeta2005].")],
 15: [("Chelsi West Ohueri, ‘Mapping Race and Belonging in the Margins of Europe: Albanian, Romani, and Egyptian Sentiments’ "
       "(PhD dissertation, The University of Texas at Austin, 2016); see also West Ohueri, ‘Zor’.",
       "[@westohueri2016]; zob. też [@westohueri2021].")],
 26: [("Wekker (*White Innocence*)", "Wekker ([@wekker2016])"),
      ("Frankenburg (*White Women, Race Matters*)", "Frankenburg ([@frankenberg1993])")],
 27: [("Noel Malcolm, ‘Myths of Albanian National Identity: Some Key Elements, as Expressed in the Works of Albanian Writers in "
       "America in the Early Twentieth Century’, in Stephanie Schwandner-Sievers and Bernd Jürgen Fischer (eds), *Albanian "
       "Identities: Myth and History* (Bloomington, IN: Indiana University Press, 2002).", "[@malcolm2002].")],
 35: [("Federal Writers’ Project, *The Albanian Struggle in the Old World and New* (Boston, MA: The Writer, 1939). See also "
       "Tochka, ‘“Enlighten and Beautify”’.", "[@fwp1939]. Zob. też [@tochka2015].")],
 39: [("(see Patrick C. Hogan, ‘“Othello”, Racism, and Despair’, *CLA Journal*, 41:4 (1998), 431–51)", "(zob. [@hogan1998])")],
 41: [("Isa Blumi, ‘The Commodification of Otherness and the Ethnic Unit in the Balkans: How to Think About Albanians’, *East "
       "European Politics and Society*, 12:3 (1998), 527–69. See also Michael Galaty, *Memory and Nation Building: From "
       "Ancient Times to the Islamic State* (Lanham, MD: Rowman and Littlefield, 2018).",
       "[@blumi1998]. Zob. też [@galaty2018].")],
 53: [("See Blumi, ‘Politics’, for more", "Zob. [@blumi1997], for more")],
 61: [("(West Ohueri, ‘Mapping Race’)", "([@westohueri2016])")],
 63: [("See West Ohueri, ‘Mapping Race’; West Ohueri, ‘Zor’.", "Zob. [@westohueri2016; @westohueri2021].")],
 29: [("see also Baker, this volume.", "zob. też [@baker2024].")],
 66: [("See Stuart Hall and Sut Jhally, *Race the Floating Signifier: Stuart Hall in Lecture* (Northampton, MA: Media "
       "Education Foundation, 2002).", "Zob. [@hall2002].")],
}
LITERAL = {33: "prose",
           49: "prose: a book in progress, not a published work (queries D2)"}
PARTLY = {3: "prose about the Balkan Egyptians", 29: "prose (mythologies of warfare)", 26: "prose", 27: "prose after the citation", 39: "prose",
          53: "prose (Tosk and Gheg)", 61: "prose"}
assert not set(WHOLE) & set(PAIRS)
out = pre
for n in range(1, 69):
    m = re.search(rf"^\[\^{n}\]: (.*)$", out, re.M)
    body = m.group(1)
    if n in WHOLE:
        assert "[@" not in body and not re.search(r"\b(See|see|also|Here|It is)\b", body), f"note {n}: prose in a WHOLE note"
        log.append(f"note {n}: {body} -> {WHOLE[n]}")
        body = WHOLE[n]
    elif n in PAIRS:
        for lit, keyed in PAIRS[n]:
            assert body.count(lit) == 1, f"note {n}: literal not found once: {lit[:70]!r}"
            body = body.replace(lit, keyed)
            log.append(f"note {n}: {lit} -> {keyed}")
        if n in PARTLY:
            log.append(f"note {n}: partly literal — {PARTLY[n]}")
    else:
        assert n in LITERAL, f"note {n}: neither keyed nor listed as literal"
        log.append(f"note {n}: literal — {LITERAL[n]}")
    out = out[:m.start(1)] + body + out[m.end(1):]
open("westohueri_src.md", "w", encoding="utf-8").write(out)
open("key_log.md", "w", encoding="utf-8").write("\n".join(log) + "\n")
print(f"keyed {len(WHOLE) + len(PAIRS)} notes ({len(PARTLY)} partly literal), literal {len(LITERAL)}; log key_log.md")
