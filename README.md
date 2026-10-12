# webbiespirit · sponsor page

A one-page, phone-first sponsor site for **webbiespirit**. A presenter stands by a pool and welcomes visitors in English or Greek. She explains the studio's offer, a free concept preview of a new website, and asks visitors to say hello by email.

The page is static HTML, CSS and JavaScript, with no build step.

## Run it

```sh
python3 -m http.server 8080
# open http://localhost:8080
```

- To force a language, add `?lang=en` or `?lang=el` to the URL. The visitor's choice is remembered.
- Without that parameter, phones set to Greek get Greek automatically.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` | The page. English is the default markup, so it reads without JavaScript. |
| `assets/css/site.css` | The cyanotype "sun-print" world: brushed emulsion fields, paper grain, the exposure strip, and the mobile layout. |
| `assets/js/site.js` | EN/EL copy, the presenter player with captions drawn by the page, the scroll "develop" reveals, the thumb dock, and copy-email. |
| `assets/js/media.js` | URLs of every video and photo, per language. |
| `assets/captions/{en,el}.vtt` | Captions, timed to each video's speech. |
| `assets/fonts/` | Piazzolla (display) and Sofia Sans (text), self-hosted Latin + Greek subsets, SIL OFL 1.1. |
| `assets/img/` | Brushed emulsion edge mask, the emulsion mottle inside every coat (strong and soft), paper grain, favicon and touch icon. |
| `scripts/make-textures.py` | Regenerates the emulsion edge mask, emulsion mottle, paper grain and touch icon (deterministic). |
| `scripts/fetch-media.sh` | Downloads all media into `assets/media/` and points the page at the local copies. |

## Hosting the media yourself

Videos and photos are currently served from the studio's Higgsfield media CDN. To ship everything from this repository instead (for example on Hostinger), run:

```sh
bash scripts/fetch-media.sh
```

## Deploying

This is a standalone campaign page, not the studio's homepage. webbiespirit.com already runs the studio's main site, so never upload this page over the root of that domain.

To publish it, give it its own address (for example a folder such as `webbiespirit.com/test-the-water/`) and upload `index.html` with the `assets/` folder into that folder. Then add a `<link rel="canonical">` and an `og:url` with that address to the page head. Everything else here (this README, `PRODUCT.md`, `.impeccable/`, `scripts/`) is for development and does not belong on the live site.

## The presenter

She is a fictional character made for this page. She presents the studio. She never poses as a client, and the page shows no reviews or endorsements in her name.

## Provenance of the media

| Asset | How it was made |
| --- | --- |
| Presenter photograph | Higgsfield Soul 2.0, text-to-image, 9:16, job `080ec7f0-2d78-47a9-be8f-89c0b0302f81` |
| English voice | Seed Audio 1.0, preset voice "Sienna" (`41023a48-71ab-478a-bea7-c7b5a78f6b36`). Pauses tightened and sped up 1.08× with pitch preserved. |
| English video | Seedance 2.5 omni-reference: the photo as first frame plus the English voice as audio reference. Drafted at 480p (job `9715dc90-…`), finalized at 1080p (job `d9c70251-…`), then encoded to 720p/1080p H.264. |
| Greek voice | ElevenLabs engine via Higgsfield Text-to-Speech V2, same "Sienna" preset, script reviewed by a Greek copy editor. Pauses re-paced by punctuation (sentence, comma, other) and sped up 1.05× with pitch preserved. Checked word by word with Whisper. |
| Greek video | A real-time intro made with Kling 3.0 (job `c36c5e86-…`), from the photograph to the English performance's first frame, joined to that performance at 1080p. Sync Lipsync 3 (job `fc94ee06-12da-47a2-ab03-89096ac2ab24`) then re-timed her lips to the exact Greek voice track. Served at 720p H.264. |
| Sun-print of the presenter | Derived from the photograph: Prussian-blue cyanotype toning plus a hand-coated brush-edge alpha (Pillow/NumPy). |
| Olive photogram | GPT Image 2.5, job `48a1d821-31c6-4ef5-9641-c338d1f5092d` |
| Olive loop | Seedance 2.5, the photogram as both first and last frame (seamless loop), job `845f1ad7-56c1-48aa-bc13-15294f372906` |
| Emulsion edge and mottle, paper grain, icons | `scripts/make-textures.py` and hand-written SVG |
