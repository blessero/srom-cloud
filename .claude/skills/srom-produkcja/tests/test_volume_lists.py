"""volume_lists.py noty: 'Noty o autorach' from a master CSV and the authors register — order (Polish alphabet by the
register's key), bold name, dash, the note's own opening dropped, Kontakt after a line break, italics, [BRAK NOTY],
reports (joint note, register doubts, capital after the dash), template style names."""
import os, subprocess, sys, tempfile
from docx import Document
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
res = []
def t(name, ok, detail=""):
    ok = bool(ok); res.append(ok); print(("PASS " if ok else "FAIL ") + name + ("" if ok else "\n   " + str(detail)[:1500]))

d = tempfile.mkdtemp()
csv_p, reg_p, out = (os.path.join(d, f) for f in ("master.csv", "autorzy.tsv", "noty.docx"))
open(csv_p, "w", encoding="utf-8").write(
    "article_id,authors_struct,authors_display\n"
    "A1,Anna|Żak|X|,Anna Żak\n"
    "A2,Jan|Łoś|Y| ;; Ewa|Lis|Z|,\"Jan Łoś, Ewa Lis\"\n"
    "A3,,Piotr Nowy\n"
    "A4,Anna|Żak|X|,Anna Żak\n")
open(reg_p, "w", encoding="utf-8").write(
    "sortuj\tosoba\torcid\tafiliacja\tnota\tkontakt\tzrodlo\tuwagi\n"
    "Żak\tDr hab. Anna Żak\t\t\tDr hab. Anna Żak, etnolożka, autorka książki *Tabor*.\tanna@x.pl\ttest\t\n"
    "Łoś\tJan Łoś\t\t\tJan Łoś i Ewa Lis są autorami prac o Romach.\t\ttest\tnota wspólna\n"
    "Lis\tEwa Lis\t\t\tBadaczka z Wrocławia.\t\ttest\t\n")
r = subprocess.run([sys.executable, os.path.join(S, "volume_lists.py"), "noty", csv_p, "--authors", reg_p, "-o", out],
                   capture_output=True, text=True)
t("runs and ends with a verdict", r.returncode == 0 and "NOTY CHECK 4" in r.stdout, r.stdout + r.stderr)
ps = Document(out).paragraphs
t("one paragraph per person, each person once", len(ps) == 4, [p.text for p in ps])
t("Polish alphabetical order by the register key (Lis, Łoś, Nowy, Żak)",
  [p.runs[0].text.split(" i ")[0] for p in ps] == ["Ewa Lis", "Jan Łoś", "Piotr Nowy", "Dr hab. Anna Żak"], [p.text for p in ps])
zak = ps[3]
t("name as printed, in the bold character style", zak.runs[0].text == "Dr hab. Anna Żak" and zak.runs[0].style.name == "Pogrubienie",
  [(x.text, x.style.name) for x in zak.runs])
t("the note's own opening and comma dropped after the dash", zak.text.startswith("Dr hab. Anna Żak – etnolożka, autorka"), zak.text)
t("*…* -> italic character style", any(x.text == "Tabor" and x.style.name == "Kursywa" for x in zak.runs),
  [(x.text, x.style.name) for x in zak.runs])
t("Kontakt after a line break", "<w:br/>" in zak._p.xml and zak.text.endswith("Kontakt: anna@x.pl"), zak.text)
t("paragraph style = the template's author-note style", all(p.style.name == "Tekst BEZ WCIĘCIA" for p in ps), [p.style.name for p in ps])
t("missing person -> [BRAK NOTY] and reported", ps[2].text == "Piotr Nowy – [BRAK NOTY]" and "Piotr Nowy: not in the register" in r.stdout,
  ps[2].text + r.stdout)
t("joint note printed as written, its opening in bold, reported",
  ps[1].runs[0].text == "Jan Łoś" and ps[1].text.startswith("Jan Łoś i Ewa Lis są") and "joint note" in r.stdout and "register flags: nota wspólna" in r.stdout,
  ps[1].text + r.stdout)
t("capital after the dash reported, text kept", ps[0].text == "Ewa Lis – Badaczka z Wrocławia." and "capital after the dash (Badaczka)" in r.stdout,
  ps[0].text + r.stdout)
print(f"VOLUME_LISTS ALL PASS {sum(res)}/{len(res)}" if all(res) else f"VOLUME_LISTS FAILED {res.count(False)}/{len(res)}")
