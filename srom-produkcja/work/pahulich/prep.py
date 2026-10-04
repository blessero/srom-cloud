# Pahulich: pahulich_pdf.md (extraction) -> pahulich_pre.md (input to cite_map scan). Re-run after any re-extraction.
# Every change is listed here and in pahulich_queries.md; nothing else is touched.
import re, sys
md = open("pahulich_pdf.md", encoding="utf-8").read()
log = []

def sub(old, new, why, count=1):
    global md
    n = md.count(old)
    if n != count:
        sys.exit(f"prep: expected {count}× {old!r}, found {n}")
    md = md.replace(old, new)
    log.append(f"{old!r} -> {new!r}: {why}")

# line-end hyphen joins the extractor could not decide (listed in pahulich_pdf_extract.md)
sub("religiopolitical", "religio-political", "PDF 'religio-|political' at a line end; hyphen kept (check against Wynter 2003, 309 — query)")
sub("statedefined", "state-defined", "PDF 'state-|defined' at a line end; 'statedefined' is no word")
# italic run swallowing the comma after "Ibid." / a year (PDF kerning): the comma is roman
n = len(re.findall(r"\*Ibid\.,\*", md))
md = md.replace("*Ibid.,*", "*Ibid.*,")
log.append(f"'*Ibid.,*' -> '*Ibid.*,' ×{n}: comma set roman")
sub("Mróz 2015*,* 17, 58", "Mróz 2015, 17, 58", "comma in italics (PDF)")
sub("[Dissertation on the Gipseys]*,*", "[Dissertation on the Gipseys],", "comma in italics (PDF)")
# author-date parentheses cite_map cannot read as they stand (its report, pahulich_pre_citemap.md)
def add_note(old, new, label, note, why):
    """replace in a body paragraph and put a note (in the source's words; cite_map keys it) after that paragraph"""
    global md
    lines = md.split("\n")
    i = [j for j, l in enumerate(lines) if old in l]
    if len(i) != 1:
        sys.exit(f"prep: expected one paragraph with {old!r}, found {len(i)}")
    lines[i[0]] = lines[i[0]].replace(old, new)
    j = i[0] + 1
    while j < len(lines) and (not lines[j].strip() or lines[j].startswith("[^")):
        j += 1
    lines[j:j] = [f"[^{label}]: {note}", ""]
    md = "\n".join(lines)
    log.append(f"{old!r} -> {new!r} + [^{label}]: {note!r}: {why}")

add_note(" (for similar inquiry, see Parvulescu and Boatcă 2022)", "[^m1]", "m1",
         "For similar inquiry, see Parvulescu and Boatcă 2022.", "prose inside the parenthesis: the whole of it becomes the note (Kanon § 7.1)")
add_note("Ella Shohat and Robert Stam (2012)", "Ella Shohat and Robert Stam[^m2]", "m2", "Shohat and Stam 2012.",
         "narrative citation with first names: marker after the names (§ 7.1)")
add_note(" (see also Thomas 2018 on Soviet politics of sedentarization of nomads in Central Asia)", "[^m3]", "m3",
         "[Zob. też @thomas2018] on Soviet politics of sedentarization of nomads in Central Asia.",
         "prose inside the parenthesis: the whole of it becomes the note; keyed by hand (the lead-in is followed by prose)")
sub("the creation of other racial states” (*Ibid.*, 155)", "the creation of other racial states” (Shohat and Stam 2012, 155)",
    "Ibid. = Shohat and Stam (2012), named just before it (a hand-made note, which the scan does not track)")
sub("(*Ibid.*; Mróz 2015)", "(Červinski 2008; Mróz 2015)", "Ibid. = the work cited just before it in the paragraph, (Červinski 2008)")
sub("dainty” (viii)", "dainty” (1807, viii)", "page only: the work cited in the same sentence, Grellmann (1807)")
sub("nationality” (74)", "nationality” (1931, 74)", "page only: the work cited in the same sentence, Barannikov (1931)")
sub("internal affairs (1992, 81; Crowe 2007, 109).", "internal affairs (1992, 81); Crowe 2007, 109. "
    "<!-- DO SPRAWDZENIA: „1992, 81” – rok i strona bez nazwiska autora; zapewne Fraser 1992 (pytanie do autora, pahulich_queries.md) -->",
    "note 2: '1992, 81' has no author in the source — left as written, flagged; Crowe keyed")
sub("Jenkins and Leroy (2021)", "Jenkins and Leroy (2021)<!-- DO SPRAWDZENIA: Jenkins, Leroy 2021 – brak w bibliografii autora (pytanie do autora) -->",
    "work not in the author's list — left as written, flagged")

# acknowledgements: the author's note on the title (Kanon § 7.1: one title note; in a translation it follows the
# translation note as a further paragraph of the same block — srom-tlumacz adds the translation note)
m = re.search(r"\n## Acknowledgments\n\n(.+)\n$", md)
if not m:
    sys.exit("prep: Acknowledgments section not found at the end")
ack = m.group(1)
md = md[:m.start()] + "\n"
md = "::: przypis-tytulowy\n" + ack + "\n:::\n\n" + md
log.append("'## Acknowledgments' section (end) -> ::: przypis-tytulowy at the top (Kanon § 7.1)")
open("pahulich_pre.md", "w", encoding="utf-8").write(md)
open("prep_log.md", "w", encoding="utf-8").write("# prep.py — changes to the extraction\n\n" + "\n".join(f"- {x}" for x in log) + "\n")
print("\n".join(log))
