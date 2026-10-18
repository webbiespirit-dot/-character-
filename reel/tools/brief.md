# webbiespirit reel: creative brief (for storyboard proposals)

## Deliverable
Instagram Reel, 9:16, 1080x1920, 30 fps, 28.0 s = 840 frames. Rendered in Remotion.
Music: original track, 120 BPM = 15 frames per beat, 60 frames per bar. Beat k starts at frame 15*k.
Sections of the music (fixed, do not move):
- Beats 0-3 (frames 0-59, 0-2 s): intro: an impact at 0.0 s, four building kicks on each beat, snare roll in beat 3, riser into the drop.
- Beat 4 (frame 60, 2.0 s): the DROP. Groove with 4-on-the-floor kick, claps on 2 and 4, chord stabs on each bar's downbeat (every 4 beats from beat 4).
- Beats 12+: open hats enter. Beats 20+: a 16th-note arpeggio enters (more energy).
- Beats 30-31 (frames 450-479, 15.0-16.0 s): RHYTHM BREAK: kick and bass drop out, a filter riser and reverse cymbal. Beat 32 (frame 480, 16.0 s) slams back in.
- Beats 48-49 (frames 720-749, 24.0-25.0 s): snare roll + riser.
- Beat 50 (frame 750, 25.0 s): OUTRO HIT: big impact, a pad sustains, no more kicks. A soft 3-note chime at 26.5 s (frame 795). Fade to silence by 28.5 s.

## Fixed structure from the client
- Hook, frames 0-59 (0-2 s): bold kinetic text "We built N websites this week" (N = number of demos shown). Must stop the scroll in the first second.
- Body, frames 60-749 (2-25 s, 46 beats): fast cuts, 1.5-3 s per shot, cuts ON beats. A different treatment each demo: phone mockup (3D tilt), full-bleed scroll-through, split-screen before/after (before = the same page with its CSS stripped, i.e. raw unstyled HTML; after = the finished site), zoom-punch on the CTA tap, quick glitch or whip-pan transitions. Vary the pacing; break the rhythm once or twice on purpose (the music break at 15-16 s is one natural place).
- Each demo gets a label: business type + "built in 1 day" (e.g. "Nail studio, built in 1 day"). NEVER a business name.
- Captions: big, high-contrast, word-by-word animated. Text must stay inside the safe area: y between 250 px and 1520 px (top 250 px and bottom 400 px are clear).
- Ending, frames 750-839 (25-28 s): the name "webbiespirit", "Websites for small businesses", CTA "DM us 'WEBSITE'".

## Footage available (phone captures, 390x844 CSS px at 3x = 1170x2532, 30 fps)
Per demo: (a) a smooth eased full-page scroll (about 4-6 s raw), (b) a CTA tap: pointer eases to the main CTA, presses (site shows its :active scale), (c) a hero hold / close-up (static with the site's own load animation playing), (d) an unstyled "before" screenshot of the same page.

## The demos (5 confirmed, 2 optional extras if they look good)
1. Nail & lash studio: oxblood #4A0D18 and blush #FBF6F4 palette, Italiana serif display + Pinyon Script wordmark, a 3D nail you paint by tapping colour chips in the hero, a scroll-driven "coat by coat" section, a 3D photo ring, price tabs. Primary CTA: a light pill button "Call to book" in the hero. Dark hero, light sections.
2. Coffee chain (fictional brand, React app): cream #F3EEE6 world, big video scenes (coffee pour, exploded briki pot), product grid of drinks, warm palette. Scroll-heavy, cinematic.
3. Barbershop: slate-blue wall #33414a, black letter panels with mustard #edb12a felt letters lit by track lights, a 3D bow tie you spin, a scroll "walk in through the glass door" sequence, a chalk price board on white brick, a 3D photo ring on a star-tile floor. Primary CTA: mustard button "Call". Dark, moody, rounded buttons.
4. Old-town barber: near-black leather #1B1512, honey #E0A95F accents, Fira Sans Extra Condensed 900 Greek headline in two lines, a real WebGL spinning barber pole, scroll walk-in "Walk in. Sit down. Leave sharp.", 3D photo ring, then/now flip card. Primary CTA: honey button "Call".
5. The agency's own page (webbiespirit): cyanotype look, Prussian blue coats on cotton paper, Piazzolla serif, a presenter video in a 9:16 print, one sunlight-yellow CTA "Say hello". (Use this one lightly or as a bridge into the ending; it is the brand itself.)
Optional extras on the server (only if they look impressive): a hair salon demo, a holiday villas demo, a tattoo studio demo.

## Brand (from DESIGN.md): "The Daylight Sun-Print"
Colors: deep Prussian #0B2559, cobalt field #163F94, mid #2F63C7, pale #8FB0E6, sunlight #E0E46A (ONLY on the primary action), cotton paper #F3F6F9, soft exposure #D3DFF5. Fonts: Piazzolla (serif, statements; variable weight 100-900) and Sofia Sans (sans, instructions/controls; variable weight up to 1000). Square corners, no drop shadows, hard tonal steps (no gradients), paper-grain and emulsion-mottle textures available, brushed emulsion edge mask available. Motion: "development" from latent to exposed on an exponential ease-out cubic-bezier(.16,1,.3,1), 120 ms press scale .97.
The reel must feel luxury and scroll-stopping, NOT like a polished corporate promo. Avoid: generic dark gradient blobs, stock "whoosh" transitions used everywhere, centered everything, emoji, em-dashes in on-screen text.

## Truth constraints for on-screen text
Allowed claims: free concept preview ("you see it before you pay" / "free preview first"), "built in 1 day" labels (client's wording), websites for small businesses, DM 'WEBSITE'. No testimonials, no client names, no results, no prices.
