"""Inline photos/<name>.webp references as data URIs.

Usage: python3 -I inline.py <site-dir> <in.html> <out-standalone.html> <out-artifact.html>
The standalone file is a full HTML document for Hostinger; the artifact file drops the
document skeleton tags because the Artifact publisher adds its own.
"""
import base64, pathlib, re, sys

site, src, out_full, out_artifact = map(pathlib.Path, sys.argv[1:5])
html = (site / src).read_text(encoding="utf-8")

def data_uri(match):
    path = site / match.group(0)
    return "data:image/webp;base64," + base64.b64encode(path.read_bytes()).decode()

html, n = re.subn(r"photos/[a-z0-9-]+\.webp", data_uri, html)
missing = re.findall(r"photos/[^\"')\s]+", html)
if missing:
    sys.exit(f"unresolved photo refs: {missing}")
out_full.parent.mkdir(parents=True, exist_ok=True)
out_full.write_text(html, encoding="utf-8")

art = re.sub(r"(?is)<!doctype html>\s*", "", html)
art = re.sub(r"(?is)</?html[^>]*>|</?head[^>]*>|</?body[^>]*>", "", art)
art = re.sub(r'(?i)<meta\s+charset=[^>]*>|<meta\s+name="viewport"[^>]*>', "", art)
# the <title> must be within the first 8KB for the artifact gallery
title = re.search(r"(?is)<title>.*?</title>", art)
if title:
    art = title.group(0) + "\n" + art.replace(title.group(0), "", 1)
out_artifact.write_text(art.strip() + "\n", encoding="utf-8")
print(f"inlined {n} photo refs; standalone {out_full.stat().st_size:,} B; artifact {out_artifact.stat().st_size:,} B")
