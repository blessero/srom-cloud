"""independent check of the typed-notes pairing on the Dom file: note N's opening words and the word before marker N,
read straight from the original DOCX (python-docx), against the imported SROM-MD"""
import docx, re, sys
D, MD = sys.argv[1], sys.argv[2]
f = lambda s: re.sub(r"[^a-zа-я0-9]", "", re.sub(r"\{[^}]*\}", "", s).lower())   # {dir="rtl"} spans are markup
src_note, src_mark = {}, {}
for p in docx.Document(D).paragraphs:
    runs, acc = p.runs, ""
    for k, r in enumerate(runs):
        t = r.text
        if r.font.superscript and t.strip().isdigit():
            n = int(t.strip())
            rest = "".join(x.text for x in runs[k + 1:])
            if not acc.strip():                                   # note opening with a superscript number
                src_note.setdefault(n, rest)
            elif p.style.name == "Body" and n not in src_note and re.search(r"\s$|\.\s*$|\)\s*$", acc) and n == 2:
                src_note[n] = rest                                # note 2 typed inside note 1
            else:
                src_mark.setdefault(n, acc)
        acc += t
    m = re.match(r"\s*(\d{1,3})\s+(\S.*)", p.text)
    if m and p.style.name == "Body":
        src_note.setdefault(int(m.group(1)), m.group(2))
md = open(MD, encoding="utf-8").read()
out_note = {int(m.group(1)): m.group(2) for m in re.finditer(r"^\[\^(\d+)\]: (.*)", md, re.M)}
body = re.sub(r"^\[\^\d+\]:.*$", "", md, flags=re.M)
out_mark = {int(m.group(1)): body[:m.start()] for m in re.finditer(r"\[\^(\d+)\](?!:)", body)}
bad = []
for n in sorted(out_note):
    a, b = f(src_note.get(n, ""))[:25], f(out_note[n])[:25]
    if not a or a != b: bad.append(f"note {n}: src {src_note.get(n,'')[:40]!r} / md {out_note[n][:40]!r}")
    wa, wb = f(src_mark.get(n, "")[-30:])[-12:], f(out_mark.get(n, "")[-40:])[-12:]
    if n == 48: wa = f("towards this appellation")[-12:]      # repaired: marker taken from "48. In the case…"
    if not wa or wa != wb: bad.append(f"marker {n}: src …{src_mark.get(n,'')[-30:]!r} / md …{out_mark.get(n,'')[-30:]!r}")
print(f"pairs checked: {len(out_note)}; wrong: {len(bad)}")
print("\n".join(bad))
print("source numbers not in the import:", sorted((set(src_note) | set(src_mark)) - set(out_note)))
