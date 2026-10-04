"""every word and every number on the PDF's pages is in the extraction (text + front matter + dropped running heads),
and nothing is in the extraction that the PDF does not have. The PDF side is read independently of the extractor's
line assembly (plain get_text). Line-end hyphens are joined on both sides, so a word split over two lines counts once.
(From work/tittel/wordcheck.py; Manchester UP Sabon text layer, soft hyphens at line ends.)"""
import re, sys, unicodedata, pymupdf
from collections import Counter
pdf, md_files = sys.argv[1], sys.argv[2:]
d = pymupdf.open(pdf)
src = unicodedata.normalize("NFKC", "\n".join(d[i].get_text() for i in range(d.page_count)))
def toks(t):
    t = re.sub(r"(?<=[a-zäöüß])[-\u00ad]\s*\n\s*(?=[a-zäöüß])", "", t)
    t = t.replace("\u00ad", "")
    return Counter(w.lower() for w in re.findall(r"[^\W\d_]+|\d+", t))
out = ""
for f in md_files:
    t = open(f, encoding="utf-8").read()
    if f.endswith("_extract.md"):    # the report: only its list of dropped running heads and page stamps
        t = "\n".join(re.sub(r"^- p\d+: ", "", l) for l in t.splitlines() if re.match(r"^- p\d+: ", l))
    out += t + "\n"
out = re.sub(r"\[\^(\d+)\]:?", r" \1 ", out)            # markers and note labels are the PDF's numbers
out = re.sub(r"<!--.*?-->|:::[ \t]*[\w-]*", " ", out, flags=re.S)
W1, W2 = toks(src), toks(unicodedata.normalize("NFKC", out))
lost, extra = W1 - W2, W2 - W1
print("lost:", sorted(lost.items())[:80])
print("extra:", sorted(extra.items())[:80])
print(f"TOKENS {sum(W1.values())} in PDF · lost {sum(lost.values())} · extra {sum(extra.values())}")
