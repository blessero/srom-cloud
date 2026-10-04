"""every word and every number on the PDF's pages is in the extraction (text + front matter + dropped running heads),
and nothing is in the extraction that the PDF does not have. The PDF side is read independently of the extractor's
line assembly (plain get_text), with the private-use figures/small capitals decoded by the same public table
(Adobe/Linotype PUA). Line-end hyphens are joined on both sides, so a word split over two lines counts once."""
import re, sys, unicodedata, pymupdf
from collections import Counter
sys.path.insert(0, sys.argv[1])
from pdf_extract import PUA
pdf, md_files = sys.argv[2], sys.argv[3:]
d = pymupdf.open(pdf)
tr = {k: v for k, v in PUA.items()}
src = "\n".join(d[i].get_text() for i in range(d.page_count)).translate(tr)
src = re.sub(r"(?m)^.*(Downloaded from|use, available at).*$", "", src)      # Cambridge Core download stamp
src = unicodedata.normalize("NFKC", src.replace("´c", "ć").replace("¼", "="))    # ligatures ﬁ -> fi
def toks(t):
    t = re.sub(r"(?<=[a-z])-\s*\n\s*(?=[a-z])", "", t)
    return Counter(w.lower() for w in re.findall(r"[^\W\d_]+|\d+", t))
out = ""
for f in md_files:
    out += open(f, encoding="utf-8").read() + "\n"
out = re.sub(r"(?m)^.*(Downloaded from|use, available at).*$", "", out)
out = re.sub(r"\[\^(\d+)\]:?", r" \1 ", out)            # markers and note labels are the PDF's numbers
out = re.sub(r"<!--.*?-->|:::[ \t]*[\w-]*", " ", out)
W1, W2 = toks(src), toks(out)
lost, extra = W1 - W2, W2 - W1
print("lost:", sorted(lost.items())[:80])
print("extra:", sorted(extra.items())[:80])
print(f"TOKENS {sum(W1.values())} in PDF · lost {sum(lost.values())} · extra {sum(extra.values())}")
