#!/usr/bin/env python3
"""Contact montages for triage by eye: many page thumbnails in one image (learnt 25.10.2026, q-stlouis1904).

    montage.py <out.jpg> <img> <img> ...            one montage, 3 columns, 400 px cells (a few large images)
    montage.py --grid <dir> <prefix>                 every <dir>/<prefix>*.jpg, 20 per sheet, 5 columns, 300 px cells,
                                                     written as <dir>/../mont_<prefix>_<n>.jpg
The file name is printed in red above each cell: that is how a page is named afterwards. Needs Pillow (python3 -I is fine).
Read the result with the Read tool: 20 album pages cost about one image."""
import sys, glob, os
from PIL import Image, ImageDraw

def sheet(files, out, cols, w, h):
    rows = (len(files) + cols - 1) // cols
    img = Image.new("RGB", (cols * w, rows * h), "white"); d = ImageDraw.Draw(img)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB"); im.thumbnail((w - 4, h - 18))
        x, y = (i % cols) * w, (i // cols) * h
        img.paste(im, (x + 2, y + 16)); d.text((x + 3, y + 2), os.path.splitext(os.path.basename(f))[0][:40], fill="red")
    img.save(out, quality=80)

if sys.argv[1] == "--grid":
    d, prefix = sys.argv[2], sys.argv[3]
    files = sorted(glob.glob(os.path.join(d, prefix + "*.jpg")))
    for n in range(0, len(files), 20):
        out = os.path.join(d, "..", f"mont_{prefix}_{n // 20}.jpg"); sheet(files[n:n + 20], out, 5, 300, 330); print(out)
else:
    sheet(sys.argv[2:], sys.argv[1], 3, 400, 416); print(sys.argv[1])
