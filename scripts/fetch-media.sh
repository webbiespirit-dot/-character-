#!/usr/bin/env bash
# Self-host the page's media: download every file listed in assets/js/media.js
# (and the absolute media URLs in index.html) into assets/media/, then point the
# page at the local copies. Safe to re-run.
#
#   bash scripts/fetch-media.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/media
urls=$(grep -ohE 'https://d2ol7oe51mr4n9\.cloudfront\.net/[^"'"'"' )]+' assets/js/media.js index.html | sort -u)
for u in $urls; do
  f="assets/media/$(basename "$u")"
  if [ ! -s "$f" ]; then
    echo "fetch $u"
    curl -fsSL --retry 3 -o "$f.part" "$u" && mv "$f.part" "$f"
  fi
done
# Rewrite absolute media URLs to the local copies.
sed -i -E 's#https://d2ol7oe51mr4n9\.cloudfront\.net/[^"/]+/#assets/media/#g' assets/js/media.js index.html
echo "Media is now served from assets/media/."
