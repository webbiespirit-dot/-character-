#!/usr/bin/env python3
"""Post 2: "Does your website pass the 11pm test?" A 6-slide quiz carousel on the day (ivory) sky.

    cd social/posts && python3 p2_eleven_pm_test.py

Writes out/en/2-the-11pm-test-<n>.png and out/el/2-the-11pm-test-<n>.png.
"""
import glob
import os
from pathlib import Path

# kit.render with the full Chrome binary screenshots a 1080x1263 viewport (the bottom 87px, with the
# carousel dots and @webbiespirit, come out blank). The headless shell renders the true 1080x1350 viewport.
if 'CHROME' not in os.environ:
    _shell = sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell'))
    if _shell:
        os.environ['CHROME'] = _shell[-1]

from kit import E, GOLD, GOLD_2, INK, ROSE, SKYBLUE, TEAL, VIOLET, Slide, render, sparkle  # noqa: E402

HERE = Path(__file__).resolve().parent
NAME = '2-the-11pm-test'
N = 6

COPY = {
    'en': {
        'quiz': 'Quick quiz',
        'cover_h': 'Does your website pass the <span class="hl">11pm test</span>?',
        'cover_lead': '4 things your customers expect',
        'swipe': 'Swipe',
        'clock': '11:00', 'clock_suffix': 'pm',
        'check': 'Check {i} of 4',
        'items': [
            ('Made for the phone.',
             'Your customers check prices and book from bed at 11pm. <b>Every page should be designed for a phone first.</b>'),
            ('Booking in 30 seconds.',
             'Pick a service, pick a time, done. <b>No missed DM, no notebook by the till.</b>'),
            ('Greek and English.',
             '<b>Tourists and expats book too.</b> Your website should speak both.'),
            ('Found on Google.',
             'When someone searches “barber Larnaca”, <b>websites are what show up.</b>'),
        ],
        'phone_btn': 'Book now', 'phone_time': '11:00 pm', 'time_w': 400,
        'steps': ['Service', 'Time', 'Done!'], 'sec': 'seconds',
        'query': 'barber Larnaca',
        'cta_q': 'Missing one?', 'cta_h': '<span class="hl">We’ll design your free preview.</span>',
        'cta_btn': 'DM us “PREVIEW”', 'cta_btn_fs': 46,
        'cta_line': 'You pay nothing until you love it.',
    },
    'el': {
        'quiz': 'Μικρό κουίζ',
        'cover_h': '<span class="nw">Περνάει η</span><br><span class="nw">ιστοσελίδα σας</span><br>'
                   '<span class="hl nw">το τεστ των</span><br><span class="nw"><span class="hl">11 το βράδυ</span>;</span>',
        'cover_lead': '4 πράγματα που περιμένουν οι πελάτες σας',
        'swipe': 'Σύρετε',
        'clock': '23:00', 'clock_suffix': '',
        'check': 'Έλεγχος {i} από 4',
        'items': [
            ('Φτιαγμένη για το κινητό.',
             'Οι πελάτες σας βλέπουν τιμές και κάνουν κράτηση από το κρεβάτι, στις 11 το βράδυ. '
             '<b>Κάθε σελίδα πρέπει να σχεδιάζεται πρώτα για το κινητό.</b>'),
            ('Κράτηση σε 30 δευτερόλεπτα.',
             'Διαλέξτε υπηρεσία, διαλέξτε ώρα, έγινε. <b>Κανένα χαμένο μήνυμα, κανένα τετράδιο δίπλα στο ταμείο.</b>'),
            ('Ελληνικά και Αγγλικά.',
             '<b>Κάνουν κράτηση και τουρίστες και ξένοι που ζουν στην Κύπρο.</b> Η ιστοσελίδα σας πρέπει να μιλά και τις δύο γλώσσες.'),
            ('Σας βρίσκουν στο Google.',
             'Όταν κάποιος ψάχνει «κουρείο Λάρνακα», <b>αυτά που εμφανίζονται είναι ιστοσελίδες.</b>'),
        ],
        'phone_btn': 'Κράτηση', 'phone_time': '23:00', 'time_w': 312,
        'steps': ['Υπηρεσία', 'Ώρα', 'Έγινε!'], 'sec': 'δευτερόλεπτα',
        'query': 'κουρείο Λάρνακα',
        # Syne Greek is very wide: short lines keep the headline above 80px.
        'cta_q': 'Σας λείπει κάποιο;', 'cta_h': '<span class="hl">Σχεδιάζουμε<br>δωρεάν τη<br>μακέτα σας.</span>',
        'cta_btn': 'Στείλτε μας «PREVIEW»', 'cta_btn_fs': 40,
        'cta_line': 'Δεν πληρώνετε τίποτα μέχρι να σας ενθουσιάσει.',
    },
}

ACCENTS = [VIOLET, ROSE, TEAL, SKYBLUE]

# The kit scatters seven random sparkles over the sky; they land on headlines. Hide those and place our own.
EXTRA = f"""
.sky svg.stars path {{ display: none; }}
/* The pale-gold mark washes out on the ivory sky: a thin deep-gold edge keeps it crisp. */
.brand svg {{ filter: drop-shadow(0 0 .8px rgba(120,85,20,.85)) drop-shadow(0 0 8px rgba(232,188,76,.45)); }}
.hl {{ background: linear-gradient(180deg, transparent 56%, rgba(232,188,76,.62) 56%, rgba(232,188,76,.62) 90%, transparent 90%);
  -webkit-box-decoration-break: clone; box-decoration-break: clone; padding: 0 .04em; }}
.abs {{ position: absolute; }}
.nw {{ white-space: nowrap; }}
.chip.acc {{ border: none; color: #fff; font-size: 30px; padding: 12px 26px; letter-spacing: .01em;
  box-shadow: 0 12px 26px -14px rgba(23,19,42,.55); }}
.tick {{ position: absolute; width: 168px; height: 168px; border-radius: 42px; display: grid; place-items: center;
  background: linear-gradient(160deg, {GOLD_2}, {GOLD} 55%, #d9a93a); transform: rotate(-9deg);
  box-shadow: 0 2px 0 rgba(255,255,255,.6) inset, 0 26px 44px -18px rgba(166,125,38,.9), 0 0 0 8px rgba(255,255,255,.75); z-index: 4; }}
.tick svg {{ width: 104px; height: 104px; }}
.stage {{ position: absolute; left: 72px; top: 262px; width: 936px; height: 520px; border-radius: 48px;
  background: rgba(255,255,255,.62); border: 2px solid rgba(255,255,255,.9);
  box-shadow: 0 30px 60px -36px rgba(23,19,42,.35); overflow: hidden; }}
.stage > svg {{ position: absolute; inset: 0; }}
.head {{ position: absolute; left: 72px; width: 936px; font-size: 100px; color: var(--ink); }}
.body {{ position: absolute; left: 72px; width: 936px; font-size: 40px; line-height: 1.38; color: var(--muted); text-wrap: pretty; }}
.body b {{ color: var(--ink); font-weight: 700; }}
.ov {{ position: absolute; display: flex; align-items: center; justify-content: center; color: var(--ink); font-weight: 700; white-space: nowrap; }}
"""


def sparkles(spots):
    """Our own sparkles, placed in the gaps: (x, y, size, colour, opacity)."""
    return ('<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">'
            + ''.join(sparkle(x, y, s, c, o) for x, y, s, c, o in spots) + '</svg>')


def tick_svg(color=INK):
    return (f'<svg viewBox="0 0 100 100"><path d="M22 53 L42 72 L79 30" fill="none" stroke="{color}" stroke-width="13" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def moon(cx, cy, r, mask_id):
    """A gold crescent moon with a soft halo."""
    return f"""<defs><mask id="{mask_id}"><rect x="{cx - r - 5}" y="{cy - r - 5}" width="{2 * r + 10}" height="{2 * r + 10}" fill="#fff"/>
<circle cx="{cx + r * .42}" cy="{cy - r * .3}" r="{r * .86}" fill="#000"/></mask>
<radialGradient id="{mask_id}g" cx=".3" cy=".65" r=".9"><stop offset="0" stop-color="#fff6d6"/><stop offset=".45" stop-color="{GOLD_2}"/><stop offset="1" stop-color="{GOLD}"/></radialGradient></defs>
<circle cx="{cx}" cy="{cy}" r="{r * 1.35}" fill="{GOLD_2}" opacity=".18"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{mask_id}g)" mask="url(#{mask_id})"/>"""


# ---------------------------------------------------------------- slide 1: cover
def cover(lang, c):
    s = Slide(lang, sky='day', seed=21, dots=(0, N), extra_css=EXTRA + """
.clock { position:absolute; left:72px; top:270px; font-family:Syne,sans-serif; font-weight:800; font-size:140px; letter-spacing:-.05em; line-height:1;
  background: linear-gradient(100deg, #8452d2 0%, #ff6fae 60%, #e8bc4c 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
  padding-bottom: 10px; }
.clock small { font-size: 56px; letter-spacing: -.02em; margin-left: 8px; }
.boxes { position:absolute; left:72px; top:1104px; display:flex; gap:22px; align-items:center; }
.boxes i { width:84px; height:84px; border-radius:22px; border:7px solid; background:rgba(255,255,255,.8); display:grid; place-items:center;
  font-style:normal; font-family:Syne,sans-serif; font-weight:800; font-size:36px; }
.swipe { position:absolute; right:72px; top:1115px; display:flex; align-items:center; gap:14px; font-weight:700; font-size:32px; color:var(--ink); }
.swipe span.arr { width:62px; height:62px; border-radius:50%; background:var(--ink); color:#f8df8e; display:grid; place-items:center; font-size:34px; }
""", nebula=[(-180, 120, 620, 520, VIOLET, .34), (640, -160, 600, 560, ROSE, .30), (560, 820, 640, 520, TEAL, .32),
             (-160, 900, 560, 480, SKYBLUE, .30), (380, 420, 380, 300, GOLD, .26)])
    suffix = f'<small>{E(c["clock_suffix"])}</small>' if c['clock_suffix'] else ''
    art = f"""<svg class="abs" style="left:660px;top:130px" width="400" height="400" viewBox="0 0 400 400">
<ellipse cx="210" cy="195" rx="172" ry="58" transform="rotate(-18 210 195)" fill="none" stroke="{INK}" stroke-opacity=".28" stroke-width="2.5" stroke-dasharray="3 10" stroke-linecap="round"/>
{moon(210, 190, 116, 'm1')}
<ellipse cx="210" cy="195" rx="172" ry="58" transform="rotate(-18 210 195)" fill="none" stroke="url(#goldStroke)" stroke-width="4" stroke-dasharray="190 1200" stroke-linecap="round"/>
<circle cx="372" cy="143" r="9" fill="{ROSE}"/>
</svg>"""
    spots = [(700, 120, 22, GOLD, .95), (1030, 470, 18, VIOLET, .8), (640, 470, 12, TEAL, .9), (1010, 160, 11, GOLD, .9),
             (520, 210, 14, ROSE, .8), (560, 1150, 18, GOLD, .9), (1015, 875, 14, TEAL, .85), (40, 760, 12, VIOLET, .7)]
    boxes = ''.join(f'<i style="border-color:{a};color:{a}">{k + 1}</i>' for k, a in enumerate(ACCENTS))
    body = f"""{sparkles(spots)}
<div class="chip acc abs" style="left:72px;top:184px;background:{INK};color:{GOLD_2}">{E(c['quiz'])}</div>
<div class="clock">{E(c['clock'])}{suffix}</div>
{art}
<h1 class="head fit" data-fit style="top:510px;height:460px;font-size:112px;display:flex;flex-direction:column;justify-content:center"><span>{c['cover_h']}</span></h1>
<p class="body fit" data-fit style="top:992px;height:70px;font-size:44px;color:var(--ink);font-weight:600;line-height:1.3">{E(c['cover_lead'])}</p>
<div class="boxes">{boxes}</div>
<div class="swipe">{E(c['swipe'])}<span class="arr">→</span></div>
"""
    return s.page(body)


# ---------------------------------------------------------------- slides 2-5 illustrations (936 x 520 stage)
def art_phone(c):
    tw = c['time_w']
    svg = f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><linearGradient id="hdr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter></defs>
<ellipse cx="610" cy="280" rx="210" ry="210" fill="{VIOLET}" opacity=".28" filter="url(#soft)"/>
{moon(175, 170, 92, 'm2')}
<text x="292" y="120" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="34" opacity=".7">z</text>
<text x="322" y="88" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="46" opacity=".85">z</text>
<text x="362" y="52" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="60">Z</text>
<g transform="translate(40 352)">
  <rect width="{tw}" height="104" rx="52" fill="{INK}"/>
  <circle cx="54" cy="52" r="24" fill="none" stroke="{GOLD_2}" stroke-width="5"/><path d="M54 38 V52 L64 60" stroke="{GOLD_2}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <text x="96" y="67" font-family="Syne" font-weight="800" font-size="42" fill="{GOLD_2}">{E(c['phone_time'])}</text>
</g>
<g transform="translate(470 34) rotate(7 135 230)">
  <rect width="270" height="470" rx="46" fill="{INK}"/>
  <rect x="13" y="13" width="244" height="444" rx="35" fill="#fffdf8"/>
  <rect x="100" y="24" width="70" height="18" rx="9" fill="{INK}"/>
  <rect x="30" y="58" width="210" height="112" rx="22" fill="url(#hdr)"/>
  <path d="M58 92 L70 134 L94 102 L118 134 L130 92" fill="none" stroke="{GOLD_2}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="150" y="96" width="70" height="12" rx="6" fill="#fff" opacity=".85"/><rect x="150" y="118" width="48" height="12" rx="6" fill="#fff" opacity=".6"/>
  <circle cx="48" cy="208" r="12" fill="{ROSE}"/><rect x="70" y="200" width="96" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="194" width="58" height="28" rx="14" fill="{GOLD}"/>
  <circle cx="48" cy="262" r="12" fill="{TEAL}"/><rect x="70" y="254" width="80" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="248" width="58" height="28" rx="14" fill="{GOLD}"/>
  <circle cx="48" cy="316" r="12" fill="{SKYBLUE}"/><rect x="70" y="308" width="104" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="302" width="58" height="28" rx="14" fill="{GOLD}"/>
  <rect x="30" y="364" width="210" height="64" rx="32" fill="{GOLD}"/>
</g>
{sparkle(892, 230, 20, GOLD, .95)}{sparkle(420, 300, 14, ROSE, .9)}{sparkle(884, 450, 15, TEAL, .9)}{sparkle(60, 60, 12, VIOLET, .8)}
</svg>"""
    # HTML label on the phone's button (Greek text in SVG falls back to a serif face), same rotation as the phone.
    ov = (f'<div class="abs" style="left:470px;top:34px;width:270px;height:470px;transform-origin:135px 230px;transform:rotate(7deg)">'
          f'<div class="ov" style="left:30px;top:364px;width:210px;height:64px;font-size:27px">{E(c["phone_btn"])}</div></div>')
    return svg + ov


def art_booking(c):
    cols = [ROSE, VIOLET, GOLD]
    rows = ''
    for k, (label, col) in enumerate(zip(c['steps'], cols)):
        # Rows start low enough to clear the tick stamp on the stage's top-right corner.
        y = 96 + k * 128
        done = k == 2
        fs = min(44, int(300 / (len(label) * .95)))
        mark = (f'<path d="M800 {y + 54} l12 12 l24 -26" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
                if done else '')
        rows += f"""<rect x="400" y="{y}" width="470" height="104" rx="52" fill="{GOLD if done else '#ffffff'}" stroke="{col}" stroke-width="4"/>
<circle cx="458" cy="{y + 52}" r="34" fill="{INK if done else col}"/>
<text x="458" y="{y + 65}" text-anchor="middle" font-family="Syne" font-weight="800" font-size="36" fill="{GOLD_2 if done else '#fff'}">{k + 1}</text>
<text x="514" y="{y + 52 + fs * .34:.0f}" font-family="Syne" font-weight="800" font-size="{fs}" fill="{INK}">{E(label)}</text>{mark}"""
    svg = f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><filter id="soft3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter></defs>
<circle cx="200" cy="270" r="190" fill="{ROSE}" opacity=".25" filter="url(#soft3)"/>
<path d="M458 206 V218 M458 334 V346" stroke="{INK}" stroke-opacity=".35" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>
<rect x="182" y="48" width="36" height="34" rx="10" fill="{INK}"/><rect x="172" y="36" width="56" height="20" rx="10" fill="{ROSE}"/>
<path d="M300 102 l22 -22" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
<circle cx="200" cy="270" r="178" fill="#fff" stroke="{INK}" stroke-width="12"/>
<circle cx="200" cy="270" r="146" fill="none" stroke="{ROSE}" stroke-opacity=".22" stroke-width="26"/>
<path d="M200 124 A146 146 0 0 1 200 416" fill="none" stroke="{ROSE}" stroke-width="26" stroke-linecap="round"/>
<circle cx="200" cy="416" r="18" fill="{GOLD}" stroke="#fff" stroke-width="5"/>
<text x="200" y="300" text-anchor="middle" font-family="Syne" font-weight="800" font-size="112" fill="{INK}" letter-spacing="-4">30</text>
{rows}
{sparkle(905, 470, 18, GOLD, .95)}{sparkle(40, 470, 14, VIOLET, .8)}{sparkle(370, 480, 12, ROSE, .9)}{sparkle(640, 470, 12, TEAL, .9)}
</svg>"""
    ov = f'<div class="ov" style="left:80px;top:318px;width:240px;height:40px;font-size:26px;color:#5e5876">{E(c["sec"])}</div>'
    return svg + ov


def art_lang(c, lang):
    knob_x = 0 if lang == 'el' else 124
    return f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><filter id="soft4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter></defs>
<circle cx="468" cy="300" r="200" fill="{TEAL}" opacity=".28" filter="url(#soft4)"/>
<g transform="translate(468 300)">
  <ellipse rx="230" ry="62" transform="rotate(-16)" fill="none" stroke="{INK}" stroke-opacity=".25" stroke-width="3" stroke-dasharray="3 10" stroke-linecap="round"/>
  <circle r="118" fill="#fff" stroke="{INK}" stroke-width="8"/>
  <g fill="none" stroke="{TEAL}" stroke-width="6"><ellipse rx="118" ry="30"/><ellipse rx="44" ry="118"/><ellipse rx="86" ry="118"/><path d="M-118 0 H118"/></g>
  <circle r="118" fill="none" stroke="{INK}" stroke-width="8"/>
  <path d="M-230 0 A230 62 0 0 0 230 0" transform="rotate(-16)" fill="none" stroke="url(#goldStroke)" stroke-width="5" stroke-linecap="round" stroke-dasharray="260 900"/>
</g>
<g transform="translate(24 50) rotate(-5)">
  <rect width="444" height="132" rx="44" fill="{TEAL}"/>
  <path d="M280 128 L330 186 L330 128 Z" fill="{TEAL}"/>
  <text x="222" y="86" text-anchor="middle" font-family="Syne" font-weight="800" font-size="52" fill="{INK}">Γεια σας!</text>
</g>
<g transform="translate(560 88) rotate(5)">
  <rect width="320" height="132" rx="44" fill="{VIOLET}"/>
  <path d="M72 128 L40 186 L120 128 Z" fill="{VIOLET}"/>
  <text x="160" y="88" text-anchor="middle" font-family="Syne" font-weight="800" font-size="56" fill="#fff">Hello!</text>
</g>
<g transform="translate(344 434)">
  <rect width="248" height="72" rx="36" fill="{INK}"/>
  <rect x="{6 + knob_x}" y="6" width="112" height="60" rx="30" fill="{GOLD}"/>
  <text x="62" y="48" text-anchor="middle" font-family="Syne" font-weight="800" font-size="30" fill="{INK if lang == 'el' else '#f5efe2'}">EL</text>
  <text x="186" y="48" text-anchor="middle" font-family="Syne" font-weight="800" font-size="30" fill="{INK if lang == 'en' else '#f5efe2'}">EN</text>
</g>
{sparkle(880, 300, 20, GOLD, .95)}{sparkle(70, 330, 16, ROSE, .9)}{sparkle(800, 470, 12, VIOLET, .8)}{sparkle(130, 470, 12, GOLD, .9)}
</svg>"""


def art_search(c):
    res = ''
    favs = [GOLD, ROSE, TEAL]
    titles = [VIOLET, ROSE, TEAL]
    for k in range(3):
        # The bar and results sit below the tick stamp on the stage's top-right corner.
        y = 210 + k * 100
        first = k == 0
        res += f"""<rect x="56" y="{y}" width="824" height="86" rx="26" fill="#fff" stroke="{GOLD if first else '#e4e0ec'}" stroke-width="{5 if first else 2}"/>
<circle cx="110" cy="{y + 43}" r="25" fill="{favs[k]}"/>
<g fill="none" stroke="#fff" stroke-width="3.5" opacity=".9"><ellipse cx="110" cy="{y + 43}" rx="25" ry="8"/><ellipse cx="110" cy="{y + 43}" rx="10" ry="25"/></g>
<rect x="160" y="{y + 21}" width="{330 - k * 40}" height="18" rx="9" fill="{titles[k]}"/>
<rect x="160" y="{y + 52}" width="{560 - k * 60}" height="13" rx="6.5" fill="#d9d4e4"/>"""
    svg = f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><filter id="soft5" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="sh5" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="{INK}" flood-opacity=".18"/></filter>
<linearGradient id="bar5" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SKYBLUE}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient></defs>
<ellipse cx="300" cy="300" rx="300" ry="190" fill="{SKYBLUE}" opacity=".2" filter="url(#soft5)"/>
<ellipse cx="700" cy="330" rx="260" ry="170" fill="{ROSE}" opacity=".16" filter="url(#soft5)"/>
<g filter="url(#sh5)"><rect x="40" y="84" width="840" height="104" rx="52" fill="#fff" stroke="url(#bar5)" stroke-width="6"/></g>
<circle cx="110" cy="132" r="22" fill="none" stroke="{VIOLET}" stroke-width="8"/><path d="M126 148 L144 166" stroke="{VIOLET}" stroke-width="9" stroke-linecap="round"/>
{res}
{sparkle(862, 252, 22, GOLD, 1)}{sparkle(904, 500, 13, ROSE, .9)}{sparkle(30, 500, 11, TEAL, .9)}
</svg>"""
    ov = (f'<div class="ov" style="left:172px;top:84px;height:104px;justify-content:flex-start;font-size:46px;font-weight:600">'
          f'{E(c["query"])}<span style="display:inline-block;width:5px;height:56px;border-radius:3px;background:{GOLD};margin-left:8px"></span></div>')
    return svg + ov


ITEM_SPARKS = [  # kept clear of the chip, the tick stamp (top right) and the headline/body block
    [(560, 215, 16, GOLD, .9), (800, 150, 20, ROSE, .85), (690, 96, 12, VIOLET, .8), (1046, 1000, 16, GOLD, .9), (1046, 620, 11, TEAL, .9), (34, 900, 11, ROSE, .8)],
    [(600, 215, 14, TEAL, .9), (790, 160, 20, GOLD, .9), (700, 96, 11, ROSE, .8), (1046, 980, 16, VIOLET, .85), (1046, 560, 12, GOLD, .9), (34, 820, 11, TEAL, .8)],
    [(600, 200, 18, VIOLET, .85), (800, 150, 16, GOLD, .9), (700, 100, 12, TEAL, .8), (1046, 990, 16, ROSE, .85), (1046, 600, 12, GOLD, .9), (34, 880, 11, VIOLET, .8)],
    [(600, 210, 15, ROSE, .85), (790, 160, 20, GOLD, .9), (700, 92, 12, SKYBLUE, .85), (1046, 975, 15, TEAL, .9), (1046, 580, 11, VIOLET, .85), (34, 860, 11, GOLD, .85)],
]

ITEM_NEBULA = [
    [(-200, 160, 640, 560, VIOLET, .36), (620, -120, 560, 480, GOLD, .30), (560, 880, 640, 520, ROSE, .30), (-160, 980, 520, 420, TEAL, .26)],
    [(560, 120, 640, 560, ROSE, .34), (-220, -120, 600, 480, TEAL, .28), (-180, 860, 620, 520, VIOLET, .30), (640, 980, 520, 420, GOLD, .30)],
    [(-200, 200, 620, 560, TEAL, .36), (620, -140, 560, 480, VIOLET, .28), (600, 860, 600, 520, SKYBLUE, .30), (-200, 1000, 540, 420, ROSE, .28)],
    [(600, 200, 620, 560, SKYBLUE, .30), (-220, -100, 600, 520, ROSE, .32), (-180, 880, 620, 520, GOLD, .30), (640, 1000, 520, 420, TEAL, .30)],
]


def item_slide(lang, c, k):
    head, text = c['items'][k]
    acc = ACCENTS[k]
    art = [art_phone, art_booking, lambda cc: art_lang(cc, lang), art_search][k](c)
    s = Slide(lang, sky='day', seed=32 + 11 * k, nebula=ITEM_NEBULA[k], dots=(k + 1, N), extra_css=EXTRA)
    body = f"""{sparkles(ITEM_SPARKS[k])}
<div class="chip acc abs" style="left:72px;top:176px;background:{acc};color:{'#fff' if acc == VIOLET else INK}">{E(c['check'].format(i=k + 1))}</div>
<div class="stage">{art}</div>
<div class="tick" style="right:44px;top:148px">{tick_svg()}</div>
<h2 class="head fit" data-fit style="top:814px;height:216px;font-size:106px">{E(head)}</h2>
<p class="body fit" data-fit style="top:1050px;height:184px">{text}</p>
"""
    return s.page(body)


# ---------------------------------------------------------------- slide 6: CTA
def cta(lang, c):
    s = Slide(lang, sky='day', seed=77, dots=(5, N), extra_css=EXTRA + """
.row { position:absolute; left:0; right:0; top:206px; display:flex; justify-content:center; gap:30px; }
.row i { width:150px; height:150px; border-radius:40px; display:grid; place-items:center; font-style:normal;
  box-shadow: 0 22px 40px -22px rgba(23,19,42,.6); }
.row i svg { width:96px; height:96px; }
.row i.q { background: rgba(255,255,255,.85); border: 7px dashed #e8bc4c; font-family:Syne,sans-serif; font-weight:800; font-size:92px; color:#a67d26; }
.ctaq { position:absolute; left:72px; width:936px; top:410px; height:94px; font-size:74px; color:var(--violet); text-align:center; }
.ctah { position:absolute; left:72px; width:936px; top:506px; height:334px; font-size:100px; color:var(--ink); text-align:center;
  display:flex; align-items:center; justify-content:center; }
.ctah > span.in { display:block; }
.btnwrap { position:absolute; left:0; right:0; top:860px; display:flex; justify-content:center; }
.btn.big { padding:30px 58px; font-family:Syne,sans-serif; font-weight:800; letter-spacing:-.01em; }
.line { position:absolute; left:72px; width:936px; top:1022px; height:64px; font-size:40px; font-weight:600; color:var(--ink); text-align:center; }
.url { position:absolute; left:0; right:0; top:1112px; display:flex; justify-content:center; }
""", nebula=[(-220, -120, 640, 560, ROSE, .32), (600, 80, 620, 560, VIOLET, .32), (-200, 760, 620, 560, TEAL, .32),
             (580, 900, 620, 480, GOLD, .34), (300, 520, 420, 320, SKYBLUE, .24)])
    boxes = ''.join(f'<i style="background:{a};transform:rotate({r}deg)">{tick_svg("#fff" if a == VIOLET else INK)}</i>'
                    for a, r in zip(ACCENTS[:3], (-7, 4, -3)))
    boxes += '<i class="q" style="transform:rotate(6deg)">?</i>'
    spots = [(80, 300, 22, GOLD, .95), (1000, 220, 18, ROSE, .9), (1010, 400, 14, TEAL, .9), (52, 700, 12, VIOLET, .85),
             (672, 104, 18, GOLD, .9), (930, 260, 10, GOLD, .9), (120, 1000, 14, ROSE, .8), (960, 1140, 18, GOLD, .9), (900, 960, 11, VIOLET, .8)]
    body = f"""{sparkles(spots)}
<div class="row">{boxes}</div>
<p class="ctaq display fit" data-fit>{E(c['cta_q'])}</p>
<h2 class="ctah fit" data-fit><span class="in">{c['cta_h']}</span></h2>
<div class="btnwrap"><div class="btn big" style="font-size:{c['cta_btn_fs']}px">{E(c['cta_btn'])}</div></div>
<p class="line fit" data-fit>{E(c['cta_line'])}</p>
<div class="url"><span class="chip" style="font-size:30px">webbiespirit.com</span></div>
"""
    return s.page(body)


def main():
    for lang, c in COPY.items():
        pages = [cover(lang, c)] + [item_slide(lang, c, k) for k in range(4)] + [cta(lang, c)]
        for n, doc in enumerate(pages, 1):
            print(render(doc, HERE / 'out' / lang / f'{NAME}-{n}.png'))


if __name__ == '__main__':
    main()
