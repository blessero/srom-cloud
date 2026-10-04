"""excerpt.py <src.md> <out.md> <para-block indices...>: front matter + title note + the given paragraph blocks, each
followed by the definitions of the notes it marks (SROM-MD keeps notes under their paragraphs). Prints the keys cited."""
import re, sys
nohead = "--no-head" in sys.argv
argv = [a for a in sys.argv if a != "--no-head"]
src, out, idx = argv[1], argv[2], [int(i) for i in argv[3:]]
B = open(src, encoding="utf-8").read().split("\n\n")
defs = {re.match(r"\[\^([^\]]+)\]:", b).group(1): b for b in B if re.match(r"\[\^[^\]]+\]:", b)}
head = [] if nohead else [b for b in B[:3] if b.startswith("---") or b.startswith("::: przypis-tytulowy")]
body = []
for i in idx:
    body.append(B[i])
    for m in re.findall(r"\[\^([^\]]+)\](?!:)", B[i]):
        body.append(defs[m])
x = "\n\n".join(head + body) + "\n"
open(out, "w", encoding="utf-8").write(x)
print(" ".join(sorted(set(re.findall(r"@([\w:.#$%&+?<>~/-]*\w)", x)))))
