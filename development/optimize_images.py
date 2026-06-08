"""
Web-optimize every image referenced by the live page code blocks, into a flat
upload-ready folder for Squarespace Custom Files. Originals are untouched.

  - JPEGs: downscale to <=2000px long edge, q82 progressive, EXIF stripped
  - Transparent PNGs (logos): keep PNG, optimize
  - Opaque PNGs (cricket): convert to JPEG (smaller); rename noted in manifest

Writes development/squarespace_upload/<files> + upload_manifest.tsv (the
filename -> paste-your-SS-URL sheet that drives the later path swap).
"""
import os
import re
import glob
import numpy as np
from PIL import Image, ImageOps

ROOT = "c:/Users/Jennifer Minnich/Github/TSF-1"
PAGES = glob.glob(os.path.join(ROOT, "development/page_code_blocks/*.html"))
OUT = os.path.join(ROOT, "development/squarespace_upload")
MAX_EDGE, QUALITY = 2000, 82

os.makedirs(OUT, exist_ok=True)

# collect unique ../../ image refs across all pages
refs = set()
for pg in PAGES:
    txt = open(pg, encoding="utf-8").read()
    refs.update(re.findall(r"\.\./\.\.[^'\")]*\.(?:png|jpg|jpeg)", txt))
refs = sorted(refs)


def downscale(im):
    w, h = im.size
    if max(w, h) > MAX_EDGE:
        s = MAX_EDGE / max(w, h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    return im


rows = []
for ref in refs:
    src = os.path.join(ROOT, ref.replace("../../", ""))
    base = os.path.basename(src)
    im = ImageOps.exif_transpose(Image.open(src))
    im = downscale(im)
    ext = base.lower().rsplit(".", 1)[1]
    in_kb = os.path.getsize(src) // 1024

    if ext == "png":
        rgba = im.convert("RGBA")
        has_alpha = bool((np.asarray(rgba)[..., 3] < 250).any())
        if has_alpha:
            out_name = base
            rgba.save(os.path.join(OUT, out_name), optimize=True)
        else:
            out_name = base.rsplit(".", 1)[0] + ".jpg"
            im.convert("RGB").save(os.path.join(OUT, out_name), "JPEG",
                                   quality=QUALITY, optimize=True, progressive=True)
    else:
        out_name = base
        im.convert("RGB").save(os.path.join(OUT, out_name), "JPEG",
                               quality=QUALITY, optimize=True, progressive=True)

    out_kb = os.path.getsize(os.path.join(OUT, out_name)) // 1024
    rows.append((out_name, ref, in_kb, out_kb))
    rename = "" if out_name == base else "  (renamed)"
    print(f"{in_kb:6d}K -> {out_kb:5d}K  {out_name}{rename}")

# manifest: the sheet the user fills with SS URLs, then we swap
man = os.path.join(OUT, "upload_manifest.tsv")
with open(man, "w", encoding="utf-8") as f:
    f.write("output_file\toriginal_ref_in_code\tPASTE_SQUARESPACE_URL_HERE\n")
    for out_name, ref, _i, _o in rows:
        f.write(f"{out_name}\t{ref}\t\n")

tot_in = sum(r[2] for r in rows)
tot_out = sum(r[3] for r in rows)
print(f"\n{len(rows)} images  {tot_in/1024:.1f}MB -> {tot_out/1024:.1f}MB")
print("manifest:", man)
