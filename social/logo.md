# The W signature

The studio's mark for Instagram: a spun-gold sun with the W written through it as one signature stroke. Only gold and white.

The pen starts on the white paper at the lower left as a bundle of gold threads, a light trail. Where it crosses the rim of the sun it flips to a solid white stroke and writes the W with real pressure: hairline joins, two heavy downstrokes, the middle peak lower than the outer two, as a hand writes it. On the way out it flips back to gold and the swash arcs over the top of the sun before it fades. The sun is engraved with fine concentric rings and a brushed light sweep, so from a distance it is solid gold and up close it is spun metal. Inside the sun the same threads run white-hot as faint silk lines in the white stroke.

Nothing in it is drawn by hand or by an image model. `scripts/make-logo.py` computes the stroke (a Bézier centerline, a pressure profile along its length, and the trace of a round nib as a union of discs), lays the threads and the rings, and writes the SVG and the animated page. `scripts/render-logo.mjs` renders the rasters with Chromium and ffmpeg. Both are deterministic.

## Files

| File | What it is | Where it goes |
| --- | --- | --- |
| `logo/w-signature.svg` | The master mark, 1000 × 1000 units on a white square. Everything important sits inside the circle Instagram crops to, with an 8% margin. | Keep as the source. Any size can be rendered from it. |
| `logo/profile-1080.png` | The mark at 1080 × 1080. | **The profile picture.** Instagram shows it as a circle, about 110 px wide on a phone, and the file is composed for that crop. |
| `logo/preview-sizes.png` | The mark as the circles a phone shows: 320, 150, 110, 64, 40 and 28 px. | A check, not for posting. |
| `logo/reveal.html` | The mark writing itself: the sun appears, the pen enters from the lower left, writes the W, leaves over the top, then a light sweeps the gold. | The source of the videos. Open it in a browser to watch it. |
| `logo/reveal-1080x1920.mp4` | The reveal, 9:16, 6 s, 30 fps, no sound. | A Reel or a story. |
| `logo/reveal-1080x1080.mp4` | The same, square. | A feed post. |

## Setting the profile picture

1. In the Instagram app, open the profile, tap **Edit profile**, then **Edit picture or avatar** and **New profile picture**.
2. Choose `profile-1080.png`. Do not zoom or move it: the file is already composed for the circle.
3. Check it against `preview-sizes.png`. At 110 px the W, the sun and the swash all read.

## Posting the reveal

Upload `reveal-1080x1920.mp4` as a Reel or a story, or `reveal-1080x1080.mp4` to the feed. The video is silent; Instagram's own music can go over it. The captions in `instagram-reels.md` fit it.

## The gold

The disc is a brushed sweep from champagne (#F7E6B4) through yellow gold (#DDB048) to bronze (#B98424) and back to pale gold, under concentric engraving rings in #FFF6D8 and #7A5212 at 5–16% opacity, with a darker rim. The threads run a ramp of #FCF1CC, #F0D27E, #D8A63A, #C08B2C and #8F5E14, and the spine that holds them together at small sizes is #9C6B1B. The W is #FFFFFF. There is no other colour.

## Regenerating

```sh
python3 scripts/make-logo.py            # writes logo/w-signature.svg and logo/reveal.html
npm i playwright && npx playwright install chromium
node scripts/render-logo.mjs            # writes the PNGs and the MP4s (needs ffmpeg)
```

Change the stroke in `KNOTS` and the pressure in `PRESSURE` at the top of `scripts/make-logo.py`. The script refuses to write a mark that leaves Instagram's circle crop.
