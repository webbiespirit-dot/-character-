# webbiespirit Instagram Reel

A 28 s, 9:16 Reel (1080x1920, 30 fps) that shows seven demo websites built by the studio, cut to a 120 BPM track, in the live site's night-and-gold brand.

## Files

| File | What it is |
| --- | --- |
| `webbiespirit-reel.mp4` | The Reel. H.264 + AAC, 28.0 s, about 21 MB. |
| `cover.png` | Cover frame (the hook card). |
| `caption.txt` | Three caption options and 15 hashtags. |
| `audio/track.wav` | The music, generated in `tools/make_track.py`; `audio/beats.json` is the detected beat grid. |
| `raw/<demo>/` | Captures per demo: `hero.mp4`, `cta.mp4`, `scroll.mp4`, `before.png`, `meta.json` (clips are not committed). |
| `src/` | The Remotion composition (`Reel.tsx`, `data/storyboard.ts`, components and treatments). |
| `tools/` | Capture, music, manifest, render and QA scripts. |

## The demos

Four from the brief and three more from the studio's demo folder, for variety:

nail & lash studio (`hoa`), coffee chain (`briki`), barbershop (`bowtie`), old-town barber (`adams`), hair salon (`moxie-hair`), café-bar (`kafenio11`), fitness studio (`k2fit`).

Business names are swapped out before each capture (`tools/sites.mjs`), in the page text, in split-letter headings, and in names painted onto canvases, so the footage shows the work and not the businesses. The coffee chain is fictional and keeps its name.

## Re-render

```sh
cd reel
npm install
node tools/capture.mjs tools/sites.mjs          # captures, about 5 min per demo
python3 tools/make_track.py && python3 tools/detect_beats.py
COVER_FRAME=40 tools/render.sh                  # mp4, cover, five verification frames in out/verify
tools/qa-frames.sh                              # frames and strips in out/qa for a visual pass
```

Capture needs the machine to itself: the demos with WebGL scenes fall back to flat CSS when the browser is starved for CPU, and the café-bar capture now waits for its WebGL record before shooting.

## Structure

Hook 0 to 2 s (kinetic text, the numeral in gold), fourteen shots of 1.5 to 3 s across five treatments (phone mockup, full-bleed scroll, split before/after, zoom-punch on the tap, slow hold as the rhythm break at 15 s), word-by-word captions inside Instagram's safe zones, and a 3 s ending with the mark, the name, "Websites for small businesses" and the DM call to action. Cuts and the tap sounds sit on beats.

## Follow-ups

- The track is synthesised in-house so it is royalty-free; a licensed track can be swapped in by replacing `audio/track.wav` and re-running `tools/detect_beats.py` (the storyboard is written in beats, so timing holds at 120 BPM).
- The caption "built in 1 day" is the studio's own claim; change it in `src/data/storyboard.ts` if the wording should differ.
- A Greek version needs only `data/storyboard.ts` (hook, captions, ending) and `caption.txt`.
