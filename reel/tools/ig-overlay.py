"""Paint an approximation of Instagram's Reels interface over frames of the rendered reel
(top bar, right action column, bottom caption area) to check what a phone hides.
Usage: python3 tools/ig-overlay.py <mp4> <out.png> <frame> [<frame> ...]"""
import subprocess, sys
from PIL import Image, ImageDraw

mp4, out, frames = sys.argv[1], sys.argv[2], [int(f) for f in sys.argv[3:]]
tiles = []
for f in frames:
    png = f'/tmp/ig-{f}.png'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(f / 30), '-i', mp4, '-frames:v', '1', png], check=True)
    im = Image.open(png).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, 1080, 250], fill=(255, 0, 0, 40))            # status bar + Reels title
    for y in (1080, 1230, 1380, 1530, 1680):                            # like, comment, share, more, audio
        d.ellipse([960, y, 1040, y + 80], fill=(255, 255, 255, 110))
    d.rectangle([0, 1520, 1080, 1920], fill=(255, 0, 0, 40))           # username, caption, audio, progress
    d.rectangle([40, 1600, 420, 1640], fill=(255, 255, 255, 150))
    d.rectangle([40, 1670, 760, 1705], fill=(255, 255, 255, 110))
    d.rectangle([40, 1725, 620, 1755], fill=(255, 255, 255, 110))
    d.rectangle([40, 1800, 520, 1830], fill=(255, 255, 255, 90))
    tiles.append(Image.alpha_composite(im, ov).convert('RGB').resize((324, 576)))
strip = Image.new('RGB', (324 * len(tiles), 576), 'black')
for i, t in enumerate(tiles):
    strip.paste(t, (324 * i, 0))
strip.save(out)
print(out, strip.size)
