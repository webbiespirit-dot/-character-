# Brief: Rockabilly Barber Shop sample website (webbiespirit)

webbiespirit is a small web design studio in Cyprus, run by Apollonas. It is building a **free sample website** for Rockabilly Barber Shop in Larnaca to win the owner as a paying client. **The shop has no website at all, so this would be its first.** Never mention or compare against an "old" or "current" site. The page will be hosted at webbiespirit.com/preview/rockabilly/ and sent to the owner on WhatsApp, so he will open it **on his phone first**. It has to make him say "that's my shop" and look hand-crafted. A generic template look loses the deal.

Working directory for all files: `/tmp/claude-0/-home-user--character-/6135ff0e-c52c-5606-accc-6ebc8f36dc3f/scratchpad/site/`

## 1. Facts (use ONLY these, verbatim where possible)

| | |
|---|---|
| Name | **Rockabilly Barber Shop** (on Facebook just "Rockabilly") |
| Slogan | **"Keep the culture alive!"** (always in English, in both languages) |
| Style | **Classic · Old school · Hot shave** (the owner's own words) |
| Since | 2019, Larnaca |
| Address | **Kimonos 3, 6015 Larnaca** (Greek: Κίμωνος 3, 6015 Λάρνακα), town centre, near Michalakis Paridis Square (Greek: κοντά στην πλατεία Μιχαλάκη Παρίδη) |
| Phone | **+357 24 102169** → `tel:+35724102169`, displayed as "24 102169" |
| Email | rockabilly.2019cy@gmail.com |
| Book online | **https://rockabilly.setmore.com/** |
| Facebook | **https://www.facebook.com/barbershoprockabilly/** |
| Instagram | **@barbershop_rockabilly** → **https://www.instagram.com/barbershop_rockabilly/** (confirmed by the owner's contact; MUST be on the page) |
| Products (Wolt) | https://wolt.com/en/cyp/larnaca/venue/rockabilly-barber-shop |
| Directions | https://www.google.com/maps/search/?api=1&query=Rockabilly+Barber+Shop+Kimonos+3+Larnaca |

**Do NOT include:** any reviews, star ratings or review counts, staff names, the owner's name, awards, "best in Larnaca" claims, a WhatsApp number, prices or services not listed below, or any year other than 2019.

### Opening hours (Cyprus time, Asia/Nicosia)

| Day | Hours |
|---|---|
| Monday | Closed |
| Tuesday | 09:30–19:00 |
| Wednesday | 09:30–19:00 |
| Thursday | 09:30–19:00 |
| Friday | 09:30–19:00 |
| Saturday | 09:00–16:00 |
| Sunday | Closed |

### Services and prices

**Barbering**

| Service | Time | Price |
|---|---|---|
| Haircut | 45 min | €15 |
| Haircut & beard | 1 hr | €18 |
| Haircut & hot shave | 1 hr 10 min | €20 |
| Kids haircut (under 12) | 45 min | €12 |
| Hot shave | 25 min | €8 |
| Beard | 15 min | €5 |

**Waxing, men:** underarms €20 · half back €35 · half legs €40 · back €65 · full legs €70 · full body €150

**Waxing, women:** underarms €20 · full face (chin, lip, neck) €30 · full legs €60 · full body €120

**Products on Wolt (Proraso):** shave cream €10 · shave ball €10 · after-shave cream €16 · shave brush €18 · pre-shave €24

## 2. Photos (real, from the shop; 3 of them)

Reference them with exactly these relative paths (they get inlined as data URIs at the end, so do not change the paths and do not reference any other image file or URL):

- `photos/barber-comb.webp` (520×765, portrait). A smiling, tattooed barber in a black tee combs a customer's slick, glossy side-part. Behind: a round Reuzel pomade tin sign, a guitar on the wall, sage-green walls, a window, a plant. **The best photo: use it as the hero.** Subject's faces are in the top 2/3; don't crop off the barber's face.
- `photos/beard-trim.webp` (587×737, portrait). Close-up: tattooed hands run a clipper along a man's grey-flecked beard. Sage-green wall behind. Good for the beard / hot-shave area or the gallery.
- `photos/mirror.webp` (522×677, portrait). Shot through an ornate dark-mahogany scalloped mirror frame: a young barber styles a customer's curly top. The background has sage-green walls, framed straight-razor artwork, a red-and-white barber pole on the right and pomade tins on the counter. Good for the gallery or the visit section.

Never caption the people with names or roles you can't know. Write neutral, true captions and alt texts, e.g. "Slick side part, finished with a comb", "Beard trim", "In the mirror at Kimonos 3".

**The real shop's colours:** sage/olive-green walls (about #6b7350 to #8a8a62), dark mahogany wood (#4a2a1f), black tees, chrome, a red-and-white barber pole. The brief says: "If the photos show different shop colours, match the real shop." So the palette is **near-black, cream and cherry red with small worn-gold details, plus the shop's sage green** as the supporting colour.

## 3. Sections, in this order

1. **Thin top ribbon:** EN "Concept preview by webbiespirit · not the official site" / EL "Δείγμα σχεδίου από το webbiespirit · όχι η επίσημη σελίδα", with an **EN / ΕΛ** language toggle. It must fit at 375 px (wrapping to 2 short lines is OK, overflowing is not).
2. **Hero:** ROCKABILLY wordmark, "Barber Shop · Larnaca · Since 2019", the slogan "Keep the culture alive!", "Classic · Old school · Hot shave", a **live status badge** (see Tech), and two buttons: "Book online" (https://rockabilly.setmore.com/) and "Call 24 102169" (tel:+35724102169). Use `photos/barber-comb.webp`.
3. **Services & prices** as a vintage diner-menu card with **dotted leaders** between name and price, with the duration shown. Barbering is open; Waxing (Men / Women) is collapsible (`<details>`). Each group has a "Book online" link.
4. **"The hot shave"** feature: "Hot towel. Straight razor. Old-school finish." and "€8, or €20 with a haircut." with a Book link.
5. **"Take it home":** the 5 Proraso products with prices and an "Order on Wolt" button. There are no product photos. Use typographic price tags or simple SVG line drawings (tube, tin, brush, bottle), never a Proraso logo.
6. **Gallery** of the photos (3 now; build it so more can be added later). A tap-to-enlarge lightbox is welcome but optional. End the gallery with a clear "More on Instagram · @barbershop_rockabilly" / "Περισσότερα στο Instagram · @barbershop_rockabilly" link to https://www.instagram.com/barbershop_rockabilly/.
7. **Visit:** address, "near Michalakis Paridis Square", an hours table with **today highlighted**, and buttons for Directions (the Google Maps link), Call, Email, Instagram and Facebook. No map iframes or embeds; a stylised CSS/SVG street-sign or address card is welcome.
8. **Footer:** an Instagram link (@barbershop_rockabilly) next to Facebook, plus EN "Website concept by webbiespirit.com" / EL "Σχέδιο ιστοσελίδας από το webbiespirit.com", linking to https://webbiespirit.com.
9. **On phones (≤ 760 px), a sticky bottom bar:** Book · Call · Directions, with `padding-bottom: calc(… + env(safe-area-inset-bottom, 0px))`. Pad the page bottom so the bar never covers the footer.

## 4. Language: English and Greek

- The toggle switches **every** piece of visible text, including button labels, the status badge, day names, captions, `alt` texts, `aria-label`s and `<title>`, and sets `<html lang>`.
- Default to EN unless `navigator.language` starts with `el`. Remember the choice in `localStorage`, with every read and write wrapped in try/catch.
- In Greek, address customers informally (εσύ): Κλείσε ραντεβού, Κάλεσε, Οδηγίες.
- The slogan "Keep the culture alive!", the "Rockabilly" wordmark and the brand name stay in English in both languages.
- Greek glossary (use these terms):
  - Barber Shop · Larnaca · Since 2019 → Κουρείο · Λάρνακα · Από το 2019
  - Classic · Old school · Hot shave → Κλασικό · Old school · Ζεστό ξύρισμα
  - Book online → Κλείσε ραντεβού · Call 24 102169 → Κάλεσε 24 102169 · Directions → Οδηγίες · Email → Email · Facebook → Facebook
  - Services & prices → Υπηρεσίες & τιμές · Barbering → Κουρείο · Waxing → Αποτρίχωση με κερί · Men → Άνδρες · Women → Γυναίκες
  - Haircut → Κούρεμα · Haircut & beard → Κούρεμα & γένια · Haircut & hot shave → Κούρεμα & ζεστό ξύρισμα · Kids haircut (under 12) → Παιδικό κούρεμα (έως 12 ετών) · Hot shave → Ζεστό ξύρισμα · Beard → Γένια
  - 45 min → 45 λεπτά · 1 hr → 1 ώρα · 1 hr 10 min → 1 ώρα 10 λεπτά · 25 min → 25 λεπτά · 15 min → 15 λεπτά
  - underarms → Μασχάλες · half back → Μισή πλάτη · half legs → Μισά πόδια · back → Πλάτη · full legs → Ολόκληρα πόδια · full body → Ολόκληρο σώμα · full face (chin, lip, neck) → Ολόκληρο πρόσωπο (πηγούνι, πάνω χείλος, λαιμός)
  - The hot shave → Το ζεστό ξύρισμα · "Hot towel. Straight razor. Old-school finish." → "Ζεστή πετσέτα. Ξυράφι. Φινίρισμα παλιάς σχολής." · "€8, or €20 with a haircut." → "€8, ή €20 μαζί με κούρεμα."
  - Take it home → Πάρ' το σπίτι · Order on Wolt → Παράγγειλε στο Wolt · Products: Shave cream → Κρέμα ξυρίσματος · Shave ball → Shave ball (σαπούνι ξυρίσματος) · After-shave cream → Κρέμα after shave · Shave brush → Πινέλο ξυρίσματος · Pre-shave → Pre-shave
  - Visit → Πού θα μας βρεις · Opening hours → Ωράριο · Closed → Κλειστά · Today → Σήμερα
  - Days: Δευτέρα, Τρίτη, Τετάρτη, Πέμπτη, Παρασκευή, Σάββατο, Κυριακή
- Copy style: plain, short and direct. No em-dash asides, no "not X but Y" lines, no marketing filler, no invented claims.

## 5. Design

- **A classic 1950s rockabilly barbershop.** Near-black, cream and cherry red with small worn-gold details, plus the shop's real sage green.
- **Fonts (Google Fonts only):**
  - Wordmark: **Yellowtail** sign-painter script. It's Latin only, so use it only for "Rockabilly" and other English-only words like the slogan.
  - Headings: **Roboto Slab 800–900**, which has Greek.
  - Body: **Commissioner**, which has Greek. Use 400/500/600/700.
  - Give every face a real fallback stack.
- **Signature details to include:**
  - barber-pole stripe dividers in red and cream; an animated pole is welcome, but respect `prefers-reduced-motion`
  - an "EST. 2019 · LARNACA" circular stamp badge (SVG `textPath` is a good way)
  - a black-and-cream checkerboard strip
  - simple straight-razor, comb and scissors line icons drawn in inline SVG
- **It must look hand-crafted and special.** No generic AI look:
  - no blue-and-white, no purple gradients, no glassmorphism or glassy blurred cards
  - no emoji icons, no "01/02/03" numbering, not everything centred
  - no `rounded-lg`-everywhere cards, no Inter or Space Grotesk
- Deliberately a single dark look. Set `color-scheme: dark` on `:root` and give `body` an explicit background. Define all colours as CSS custom properties in `:root` at the top of the `<style>`, with a one-line layout-concept comment above them.

## 6. Tech

- **A single self-contained HTML document** (`<!doctype html>`, `<html lang="en">`, `<head>` with `<meta charset="utf-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`):
  - CSS and JS inline
  - the only external resource is the Google Fonts stylesheet (with `preconnect`); no other external scripts, images, iframes or embeds
  - `<meta name="robots" content="noindex">`, a `<meta name="description">`, and `<title>` = "Rockabilly Barber Shop · Larnaca"
  - schema.org `BarberShop` JSON-LD: name, slogan, address (streetAddress "Kimonos 3", postalCode "6015", addressLocality "Larnaca", addressCountry "CY"), telephone "+35724102169", email, `openingHoursSpecification` for the hours above, `priceRange` "€5–€150", `sameAs` [Facebook URL, Instagram URL], and `url` "https://webbiespirit.com/preview/rockabilly/"
- **Mobile first at 375 px:**
  - no horizontal scrolling at any width from 320 to 1440
  - side gutter ≥ 16 px
  - tap targets ≥ 44 px
  - give text-bearing flex/grid children `min-width: 0`
  - use `overflow-x: clip` on the body as a last resort only, not as a way to hide a real overflow bug
  - looks great on desktop too
- **Live status badge in the hero**, computed in Asia/Nicosia time with `Intl.DateTimeFormat` (not the device's local time), refreshed every minute:
  - during opening hours: EN "Open now · until 19:00" / EL "Ανοιχτά τώρα · έως 19:00" (use today's real closing time), with a lit dot
  - on an open day before opening: "Open today 09:30–19:00" / "Ανοιχτά σήμερα 09:30–19:00"
  - after closing, or on a closed day: "Closed now · opens Tuesday 09:30" / "Κλειστά τώρα · ανοίγει Τρίτη 09:30" (next open day; say "tomorrow" / "αύριο" when it's the next day)
- Highlight today's row in the hours table with the same Cyprus-time logic.
- External links use `target="_blank" rel="noopener"`. `tel:` and `mailto:` links are fine.
- Respect `prefers-reduced-motion`, give keyboard focus a visible state, and use `-webkit-tap-highlight-color: transparent` with proper `:active` states.
- Images: `loading="lazy"` except the hero, plus `width`/`height` attributes and `object-fit: cover` with a sensible `object-position`.
- One orchestrated motion moment beats scattered effects. Keep motion tasteful.

## 7. Checking your work

The screenshot helper is `node /tmp/claude-0/-home-user--character-/6135ff0e-c52c-5606-accc-6ebc8f36dc3f/scratchpad/tools/shoot.js <html> <out-prefix> [el]`. Run it from the `site/` directory. It:
- takes full-page screenshots at 375×812 (phone) and 1280×900 (desktop), as `<out-prefix>-phone.png` and `<out-prefix>-desktop.png`
- reports horizontal overflow, the overflowing elements and console errors
- uses Greek browser locale when you pass `el`

View the PNGs with the Read tool. Google Fonts do load in this environment.
