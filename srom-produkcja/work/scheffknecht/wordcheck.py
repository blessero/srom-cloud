"""every word on the PDF's article pages is in the extraction (text + front matter + dropped running heads), and
nothing is in the extraction that the PDF does not have. Line-end hyphens and soft hyphens are joined on both
sides, so a word split over two lines counts once."""
import re, sys, pymupdf
from collections import Counter
pdf, md_files, pages = sys.argv[1], sys.argv[2:-1], sys.argv[-1]
a, b = [int(x) for x in pages.split("-")]
d = pymupdf.open(pdf)
src = "\n".join(d[i].get_text() for i in range(a - 1, b))
def words(t):
    t = t.replace("­\n", "").replace("­", "")
    t = re.sub(r"-\s*\n\s*(?=[a-zäöüß])", "", t)
    return Counter(w.lower() for w in re.findall(r"[^\W\d_]+", t))
out = ""
for f in md_files:
    out += open(f, encoding="utf-8").read() + "\n"
out = re.sub(r"\[\^\d+\]:?|<!--.*?-->|:::[ \t]*[\w-]*", " ", out)
W1, W2 = words(src), words(out)
lost, extra = W1 - W2, W2 - W1
print("lost:", sorted(lost.items())[:80])
print("extra:", sorted(extra.items())[:80])
print(f"WORDS {sum(W1.values())} in PDF · lost {sum(lost.values())} · extra {sum(extra.values())}")
