# The W signature

The studio's mark for Instagram: a spun-gold sun with the W written through it as one signature stroke. Only gold and white.

The profile picture is the full-bleed version: the sun is the whole square, so it fills Instagram's circle edge to edge with no white margin, and the signature is white from first touch to last. The same mark also exists framed on white, as a sun inside a white square, with its gold threads outside the sun; the reveal videos use that one.

The pen starts on the white paper at the lower left as a bundle of gold threads, a light trail. Where it crosses the rim of the sun it flips to a solid white stroke and writes the W with real pressure: thin joins, two heavy downstrokes with the swell on their trailing edge as a nib leaves it, the middle peak lower than the outer two, as a hand writes it. On the way out it flips back to gold and the swash arcs over the top of the sun and lifts off, fading to nothing. The thin strokes never drop below 15 units of the 1000-unit square, so the W keeps its joins at 110 px. The sun is engraved with fine concentric rings and a brushed light sweep, so from a distance it is solid gold and up close it is spun metal. Inside the sun the same threads run white-hot as faint silk lines in the white stroke.

Nothing in it is drawn by hand or by an image model. `scripts/make-logo.py` computes the stroke (a Bézier centerline, a pressure profile along its length, and the trace of a round nib as a union of discs), lays the threads and the rings, and writes the SVG and the animated page. `scripts/render-logo.mjs` renders the rasters with Chromium and ffmpeg. Both are deterministic.

## Files

| File | What it is | Where it goes |
| --- | --- | --- |
| `logo/w-signature-full.svg` | The full-bleed master, 1000 × 1000 units. The gold fills the whole square and the signature stays inside the circle Instagram crops to, with an 8% margin. | Keep as the source of the profile picture. |
| `logo/profile-1080.png` | The full-bleed mark at 1080 × 1080. | **The profile picture.** It fills the whole circle, about 110 px wide on a phone. Because the gold runs to the corners it also survives any other crop, such as a rounded square. |
| `logo/preview-sizes.png` | The profile picture as the circles a phone shows: 320, 150, 110, 64, 40 and 28 px. | A check, not for posting. |
| `logo/w-signature.svg` | The framed master: the sun on a white square, gold threads outside it. | Keep as the source for the reveal and for places that want a white ground. |
| `logo/profile-framed-1080.png` | The framed mark at 1080 × 1080. | Where a white square works better than a gold one, such as a website or a document. |
| `logo/reveal.html` | The mark writing itself: the sun appears, the pen enters from the lower left, writes the W one stroke at a time, braking into each turn, leaves over the top, then a light catches the gold. | The source of the videos. Open it in a browser to watch it. |
| `logo/reveal-1080x1920.mp4` | The reveal, 9:16, 6 s, 30 fps, no sound. | A Reel or a story. |
| `logo/reveal-1080x1080.mp4` | The same, square. | A feed post. |

## Setting the profile picture

1. In the Instagram app, open the profile, tap **Edit profile**, then **Edit picture or avatar** and **New profile picture**.
2. Choose `profile-1080.png`. Do not zoom or move it: the file is already composed for the circle, and the gold already fills it.
3. Check it against `preview-sizes.png`. At 110 px the W and the swash both read.

## Posting the reveal

Upload `reveal-1080x1920.mp4` as a Reel or a story, or `reveal-1080x1080.mp4` to the feed. The video is silent; Instagram's own music can go over it. The captions in `instagram-reels.md` fit it.

## The gold

The disc is a brushed sweep from pale gold (#EDD08A) through yellow gold (#DDB048) to bronze (#B98424) and back, under concentric engraving rings in #FFF6D8 and #7A5212 at 5–16% opacity that fade out at the centre, with a darker rim. The threads run a ramp of #FCF1CC, #F0D27E, #D8A63A, #C08B2C and #9A6A1A, nothing darker than bronze #80520F, and the spine that holds them together at small sizes is #9C6B1B. The W is #FFFFFF with a faint engraved edge (#C9973A at half opacity) so it keeps its outline where the light falls. There is no other colour.

## Regenerating

```sh
python3 scripts/make-logo.py            # writes logo/w-signature.svg and logo/reveal.html
python3 scripts/make-logo.py --full     # writes logo/w-signature-full.svg, the profile picture
npm i playwright && npx playwright install chromium
node scripts/render-logo.mjs            # writes the PNGs and the MP4s (needs ffmpeg)
```

Change the stroke in `KNOTS_CROP` (framed) or `KNOTS_FULL` (full-bleed) and the pressure in `PRESSURE` at the top of `scripts/make-logo.py`. The script refuses to write a mark that leaves Instagram's circle crop.
