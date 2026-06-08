"""
Produce Squarespace-ready page code blocks by swapping every local image path
for its hosted Squarespace URL.

Reads harvested URLs from development/squarespace_upload/harvested_urls.txt
(paste the Custom Files URLs there, any order, one per line or blob). Each URL
ends in its filename, so we map by FILE STEM (name without extension) -> this
also auto-handles cricket.png -> cricket.jpg.

Rewrites all 4 pages into development/squarespace_ready/, leaving the
local-rendering originals in page_code_blocks/ untouched. Reports any image
still missing a URL so we know exactly what's left to upload.
"""
import os
import re
import glob

ROOT = "c:/Users/Jennifer Minnich/Github/TSF-1"
URLS = os.path.join(ROOT, "development/squarespace_upload/harvested_urls.txt")
SRC_DIR = os.path.join(ROOT, "development/page_code_blocks")
OUT_DIR = os.path.join(ROOT, "development/squarespace_ready")

# stem (filename without extension) -> SS URL
url_by_stem = {}
blob = open(URLS, encoding="utf-8").read()
for u in re.findall(r"https://static1\.squarespace\.com/\S+?\.(?:png|jpg|jpeg)", blob):
    stem = os.path.splitext(os.path.basename(u))[0]
    url_by_stem[stem] = u
print(f"{len(url_by_stem)} URLs loaded:", ", ".join(sorted(url_by_stem)))

# every local image ref across the 4 pages, keyed by stem
refs = set()
for pg in glob.glob(os.path.join(SRC_DIR, "*.html")):
    refs.update(re.findall(r"\.\./\.\.[^'\")]*\.(?:png|jpg|jpeg)", open(pg, encoding="utf-8").read()))
ref_stems = {os.path.splitext(os.path.basename(r))[0] for r in refs}

missing = sorted(ref_stems - set(url_by_stem))
if missing:
    print(f"\n*** STILL NEED {len(missing)} URLs (upload + harvest these): ***")
    for m in missing:
        print("   ", m)

os.makedirs(OUT_DIR, exist_ok=True)
for pg in glob.glob(os.path.join(SRC_DIR, "*.html")):
    txt = open(pg, encoding="utf-8").read()
    n = 0
    for ref in sorted(refs, key=len, reverse=True):
        stem = os.path.splitext(os.path.basename(ref))[0]
        if stem in url_by_stem and ref in txt:
            txt = txt.replace(ref, url_by_stem[stem])
            n += 1
    out = os.path.join(OUT_DIR, os.path.basename(pg))
    open(out, "w", encoding="utf-8").write(txt)
    left = txt.count("../../")
    print(f"{os.path.basename(pg):14s} swapped {n} paths, {left} local paths remaining -> {out}")
