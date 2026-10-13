#!/usr/bin/env python3
"""Post 2: "Does your website pass the 11pm test?" A 6-slide quiz carousel on the day (ivory) sky.

    cd social/posts && python3 p2_eleven_pm_test.py

Writes out/en/2-the-11pm-test-<n>.png and out/el/2-the-11pm-test-<n>.png.
"""
from pathlib import Path

from kit import (E, GOLD, GOLD_2, GOLD_DEEP, INK, IVORY, ROSE, SKYBLUE, TEAL, VIOLET, Slide, render, sparkle)

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
        'phone_btn': 'Book now', 'phone_time': '11:00 pm',
        'steps': ['Service', 'Time', 'Done!'], 'sec': 'seconds',
        'query': 'barber Larnaca',
        'cta_h': 'Missing one? <span class="hl">We’ll design your free preview.</span>',
        'cta_btn': 'DM us “PREVIEW”',
        'cta_line': 'You pay nothing until you love it.',
    },
    'el': {
        'quiz': 'Μικρό κουίζ',
        'cover_h': 'Περνάει η ιστοσελίδα σας <span class="hl">το τεστ των 11 το βράδυ</span>;',
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
             'Όταν κάποιος ψάχνει «κουρείο Λάρνακα», <b>αυτό που εμφανίζεται είναι ιστοσελίδες.</b>'),
        ],
        'phone_btn': 'Κράτηση', 'phone_time': '23:00',
        'steps': ['Υπηρεσία', 'Ώρα', 'Έγινε!'], 'sec': 'δευτερόλεπτα',
        'query': 'κουρείο Λάρνακα',
        'cta_h': 'Σας λείπει κάποιο; <span class="hl">Θα σχεδιάσουμε δωρεάν την προεπισκόπησή σας.</span>',
        'cta_btn': 'Στείλτε μας «PREVIEW»',
        'cta_line': 'Δεν πληρώνετε τίποτα μέχρι να σας ενθουσιάσει.',
    },
}

ACCENTS = [VIOLET, ROSE, TEAL, SKYBLUE]

EXTRA = f"""
.hl {{ background: linear-gradient(180deg, transparent 56%, rgba(232,188,76,.62) 56%, rgba(232,188,76,.62) 90%, transparent 90%);
  -webkit-box-decoration-break: clone; box-decoration-break: clone; padding: 0 .04em; }}
.abs {{ position: absolute; }}
.chip.acc {{ border: none; color: #fff; font-size: 30px; padding: 12px 26px; letter-spacing: .01em;
  box-shadow: 0 12px 26px -14px rgba(23,19,42,.55); }}
.chip.acc .n {{ display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; background: rgba(255,255,255,.28);
  font-family: Syne, sans-serif; font-weight: 800; font-size: 22px; }}
.tick {{ position: absolute; width: 168px; height: 168px; border-radius: 42px; display: grid; place-items: center;
  background: linear-gradient(160deg, {GOLD_2}, {GOLD} 55%, #d9a93a); transform: rotate(-9deg);
  box-shadow: 0 2px 0 rgba(255,255,255,.6) inset, 0 26px 44px -18px rgba(166,125,38,.9), 0 0 0 8px rgba(255,255,255,.75); z-index: 4; }}
.tick svg {{ width: 104px; height: 104px; }}
.stage {{ position: absolute; left: 72px; top: 262px; width: 936px; height: 520px; border-radius: 48px;
  background: rgba(255,255,255,.62); border: 2px solid rgba(255,255,255,.9);
  box-shadow: 0 30px 60px -36px rgba(23,19,42,.35); overflow: hidden; }}
.stage svg {{ position: absolute; inset: 0; }}
.head {{ position: absolute; left: 72px; width: 936px; font-size: 100px; color: var(--ink); }}
.body {{ position: absolute; left: 72px; width: 936px; font-size: 40px; line-height: 1.38; color: var(--muted); text-wrap: pretty; }}
.body b {{ color: var(--ink); font-weight: 700; }}
"""


def tick_svg(color=INK):
    return (f'<svg viewBox="0 0 100 100"><path d="M22 53 L42 72 L79 30" fill="none" stroke="{color}" stroke-width="13" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def moon(cx, cy, r, mask_id):
    """A gold crescent moon."""
    return f"""<defs><mask id="{mask_id}"><rect x="{cx - r - 5}" y="{cy - r - 5}" width="{2 * r + 10}" height="{2 * r + 10}" fill="#fff"/>
<circle cx="{cx + r * .42}" cy="{cy - r * .3}" r="{r * .86}" fill="#000"/></mask>
<radialGradient id="{mask_id}g" cx=".3" cy=".65" r=".9"><stop offset="0" stop-color="#fff6d6"/><stop offset=".45" stop-color="{GOLD_2}"/><stop offset="1" stop-color="{GOLD}"/></radialGradient></defs>
<circle cx="{cx}" cy="{cy}" r="{r * 1.35}" fill="{GOLD_2}" opacity=".18"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{mask_id}g)" mask="url(#{mask_id})"/>"""


# ---------------------------------------------------------------- slide 1: cover
def cover(lang, c):
    s = Slide(lang, sky='day', seed=21, dots=(0, N), extra_css=EXTRA + """
.clock { position:absolute; left:72px; top:262px; font-family:Syne,sans-serif; font-weight:800; font-size:188px; letter-spacing:-.05em; line-height:1;
  background: linear-gradient(100deg, #8452d2 0%, #ff6fae 55%, #e8bc4c 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }
.clock small { font-size: 74px; letter-spacing: -.02em; margin-left: 10px; }
.boxes { position:absolute; left:72px; top:1110px; display:flex; gap:22px; align-items:center; }
.boxes i { width:84px; height:84px; border-radius:22px; border:7px solid; background:rgba(255,255,255,.8); display:grid; place-items:center;
  font-style:normal; font-family:Syne,sans-serif; font-weight:800; font-size:36px; }
.swipe { position:absolute; right:72px; top:1122px; display:flex; align-items:center; gap:14px; font-weight:700; font-size:32px; color:var(--ink); }
.swipe span.arr { width:62px; height:62px; border-radius:50%; background:var(--ink); color:#f8df8e; display:grid; place-items:center; font-size:34px; }
""", nebula=[(-180, 120, 620, 520, VIOLET, .34), (640, -160, 600, 560, ROSE, .30), (560, 820, 640, 520, TEAL, .32),
             (-160, 900, 560, 480, SKYBLUE, .30), (380, 420, 380, 300, GOLD, .26)])
    suffix = f'<small>{E(c["clock_suffix"])}</small>' if c['clock_suffix'] else ''
    art = f"""<svg class="abs" style="left:600px;top:150px" width="440" height="420" viewBox="0 0 440 420">
<ellipse cx="230" cy="210" rx="205" ry="70" transform="rotate(-18 230 210)" fill="none" stroke="{INK}" stroke-opacity=".28" stroke-width="2.5" stroke-dasharray="3 10" stroke-linecap="round"/>
{moon(230, 205, 128, 'm1')}
<ellipse cx="230" cy="210" rx="205" ry="70" transform="rotate(-18 230 210)" fill="none" stroke="url(#goldStroke)" stroke-width="4" stroke-dasharray="210 1200" stroke-linecap="round"/>
<circle cx="416" cy="152" r="10" fill="{ROSE}"/>
{sparkle(70, 70, 26, GOLD, .95)}{sparkle(395, 330, 18, VIOLET, .8)}{sparkle(120, 360, 13, TEAL, .9)}{sparkle(352, 40, 11, GOLD, .9)}
</svg>"""
    boxes = ''.join(f'<i style="border-color:{a};color:{a}">{k + 1}</i>' for k, a in enumerate(ACCENTS))
    body = f"""
<div class="chip acc abs" style="left:72px;top:184px;background:{INK};color:{GOLD_2}">{E(c['quiz'])}</div>
<div class="clock">{E(c['clock'])}{suffix}</div>
{art}
<h1 class="head fit" data-fit style="top:520px;height:440px;font-size:112px">{c['cover_h']}</h1>
<p class="body fit" data-fit style="top:990px;height:70px;font-size:44px;color:var(--ink);font-weight:600;line-height:1.3">{E(c['cover_lead'])}</p>
<div class="boxes">{boxes}</div>
<div class="swipe">{E(c['swipe'])}<span class="arr">→</span></div>
"""
    return s.page(body)


# ---------------------------------------------------------------- slides 2-5 illustrations
def art_phone(c):
    return f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><linearGradient id="hdr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter></defs>
<ellipse cx="610" cy="280" rx="210" ry="210" fill="{VIOLET}" opacity=".28" filter="url(#soft)"/>
{moon(175, 170, 92, 'm2')}
<text x="292" y="120" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="34" opacity=".7">z</text>
<text x="322" y="88" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="46" opacity=".85">z</text>
<text x="362" y="52" font-family="Syne" font-weight="800" fill="{VIOLET}" font-size="60">Z</text>
<g transform="translate(70 352)">
  <rect width="290" height="104" rx="52" fill="{INK}"/>
  <circle cx="54" cy="52" r="24" fill="none" stroke="{GOLD_2}" stroke-width="5"/><path d="M54 38 V52 L64 60" stroke="{GOLD_2}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <text x="95" y="68" font-family="Syne" font-weight="800" font-size="44" fill="{GOLD_2}">{E(c['phone_time'])}</text>
</g>
<g transform="translate(482 34) rotate(7 135 230)">
  <rect width="270" height="470" rx="46" fill="{INK}"/>
  <rect x="13" y="13" width="244" height="444" rx="35" fill="#fffdf8"/>
  <rect x="100" y="24" width="70" height="18" rx="9" fill="{INK}"/>
  <rect x="30" y="58" width="210" height="112" rx="22" fill="url(#hdr)"/>
  <path d="M58 92 L70 134 L94 102 L118 134 L130 92" fill="none" stroke="{GOLD_2}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="150" y="96" width="70" height="12" rx="6" fill="#fff" opacity=".85"/><rect x="150" y="118" width="48" height="12" rx="6" fill="#fff" opacity=".6"/>
  <g>
    <circle cx="48" cy="208" r="12" fill="{ROSE}"/><rect x="70" y="200" width="96" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="194" width="58" height="28" rx="14" fill="{GOLD}"/>
    <circle cx="48" cy="262" r="12" fill="{TEAL}"/><rect x="70" y="254" width="80" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="248" width="58" height="28" rx="14" fill="{GOLD}"/>
    <circle cx="48" cy="316" r="12" fill="{SKYBLUE}"/><rect x="70" y="308" width="104" height="16" rx="8" fill="#d9d4e4"/><rect x="182" y="302" width="58" height="28" rx="14" fill="{GOLD}"/>
  </g>
  <rect x="30" y="364" width="210" height="64" rx="32" fill="{GOLD}"/>
  <text x="135" y="406" text-anchor="middle" font-family="Body" font-weight="700" font-size="26" fill="{INK}">{E(c['phone_btn'])}</text>
</g>
{sparkle(860, 90, 22, GOLD, .95)}{sparkle(420, 300, 14, ROSE, .9)}{sparkle(880, 420, 16, TEAL, .9)}{sparkle(60, 60, 12, VIOLET, .8)}
</svg>"""


def art_booking(c):
    steps = c['steps']
    cols = [ROSE, VIOLET, GOLD]
    rows = ''
    for k, (label, col) in enumerate(zip(steps, cols)):
        y = 44 + k * 150
        done = k == 2
        fill = GOLD if done else '#ffffff'
        num_fill = INK if done else col
        num_txt = GOLD_2 if done else '#fff'
        mark = (f'<path d="M{24} {y + 60} l12 12 l24 -26" transform="translate({800 - 24} 0)" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
                if done else '')
        rows += f"""<rect x="400" y="{y}" width="470" height="120" rx="60" fill="{fill}" stroke="{col if not done else GOLD}" stroke-width="4"/>
<circle cx="460" cy="{y + 60}" r="38" fill="{num_fill}"/>
<text x="460" y="{y + 75}" text-anchor="middle" font-family="Syne" font-weight="800" font-size="40" fill="{num_txt}">{k + 1}</text>
<text x="518" y="{y + 75}" font-family="Syne" font-weight="800" font-size="44" fill="{INK}">{E(label)}</text>{mark}"""
    return f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><filter id="soft3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter></defs>
<circle cx="200" cy="280" r="190" fill="{ROSE}" opacity=".25" filter="url(#soft3)"/>
<path d="M460 120 V194 M460 270 V344" stroke="{INK}" stroke-opacity=".35" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>
<rect x="182" y="58" width="36" height="34" rx="10" fill="{INK}"/><rect x="172" y="46" width="56" height="20" rx="10" fill="{ROSE}"/>
<path d="M300 112 l22 -22" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
<circle cx="200" cy="280" r="178" fill="#fff" stroke="{INK}" stroke-width="12"/>
<circle cx="200" cy="280" r="146" fill="none" stroke="{ROSE}" stroke-opacity=".22" stroke-width="26"/>
<path d="M200 134 A146 146 0 0 1 200 426" fill="none" stroke="{ROSE}" stroke-width="26" stroke-linecap="round"/>
<circle cx="200" cy="426" r="18" fill="{GOLD}" stroke="#fff" stroke-width="5"/>
<text x="200" y="312" text-anchor="middle" font-family="Syne" font-weight="800" font-size="112" fill="{INK}" letter-spacing="-4">30</text>
<text x="200" y="358" text-anchor="middle" font-family="Body" font-weight="700" font-size="26" fill="#5e5876">{E(c['sec'])}</text>
{rows}
{sparkle(905, 40, 18, GOLD, .95)}{sparkle(40, 470, 14, VIOLET, .8)}{sparkle(370, 470, 12, ROSE, .9)}
</svg>"""


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
<g transform="translate(40 42) rotate(-5)">
  <rect width="372" height="132" rx="44" fill="{TEAL}"/>
  <path d="M250 128 L300 186 L300 128 Z" fill="{TEAL}"/>
  <text x="186" y="88" text-anchor="middle" font-family="Syne" font-weight="800" font-size="56" fill="{INK}">Γεια σας!</text>
</g>
<g transform="translate(560 64) rotate(5)">
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
    for k in range(3):
        y = 188 + k * 108
        first = k == 0
        res += f"""<rect x="56" y="{y}" width="824" height="92" rx="26" fill="#fff" stroke="{GOLD if first else '#e4e0ec'}" stroke-width="{5 if first else 2}"/>
<circle cx="110" cy="{y + 46}" r="26" fill="{favs[k]}"/>
<g fill="none" stroke="#fff" stroke-width="3.5" opacity=".9"><ellipse cx="110" cy="{y + 46}" rx="26" ry="8"/><ellipse cx="110" cy="{y + 46}" rx="10" ry="26"/></g>
<rect x="160" y="{y + 22}" width="{330 - k * 40}" height="18" rx="9" fill="{SKYBLUE}"/>
<rect x="160" y="{y + 54}" width="{560 - k * 60}" height="13" rx="6.5" fill="#d9d4e4"/>"""
    return f"""<svg viewBox="0 0 936 520" width="936" height="520">
<defs><filter id="soft5" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="sh5" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="{INK}" flood-opacity=".18"/></filter></defs>
<ellipse cx="468" cy="300" rx="380" ry="200" fill="{SKYBLUE}" opacity=".22" filter="url(#soft5)"/>
<g filter="url(#sh5)"><rect x="40" y="40" width="856" height="112" rx="56" fill="#fff" stroke="{SKYBLUE}" stroke-width="5"/></g>
<circle cx="112" cy="92" r="22" fill="none" stroke="{SKYBLUE}" stroke-width="8"/><path d="M128 108 L146 126" stroke="{SKYBLUE}" stroke-width="9" stroke-linecap="round"/>
<text x="176" y="112" font-family="Body" font-weight="600" font-size="48" fill="{INK}">{E(c['query'])}</text>
<rect x="{176 + 0}" y="66" width="5" height="56" rx="2.5" fill="{GOLD}" id="caret"/>
{res}
{sparkle(860, 232, 22, GOLD, 1)}{sparkle(900, 470, 14, ROSE, .9)}{sparkle(30, 470, 12, TEAL, .9)}
</svg>"""


def item_slide(lang, c, k):
    head, text = c['items'][k]
    acc = ACCENTS[k]
    arts = [art_phone(c), art_booking(c), art_lang(c, lang), art_search(c)]
    seeds = [32, 43, 54, 65]
    nebs = [
        [(-200, 160, 640, 560, VIOLET, .36), (620, -120, 560, 480, GOLD, .30), (560, 880, 640, 520, ROSE, .30), (-160, 980, 520, 420, TEAL, .26)],
        [(560, 120, 640, 560, ROSE, .34), (-220, -120, 600, 480, TEAL, .28), (-180, 860, 620, 520, VIOLET, .30), (640, 980, 520, 420, GOLD, .30)],
        [(-200, 200, 620, 560, TEAL, .36), (620, -140, 560, 480, VIOLET, .28), (600, 860, 600, 520, SKYBLUE, .30), (-200, 1000, 540, 420, ROSE, .28)],
        [(600, 200, 620, 560, SKYBLUE, .36), (-220, -100, 560, 480, ROSE, .28), (-180, 880, 620, 520, GOLD, .30), (640, 1000, 520, 420, TEAL, .30)],
    ]
    s = Slide(lang, sky='day', seed=seeds[k], nebula=nebs[k], dots=(k + 1, N), extra_css=EXTRA)
    chip = c['check'].format(i=k + 1)
    body = f"""
<div class="chip acc abs" style="left:72px;top:176px;background:{acc}">{E(chip)}</div>
<div class="stage">{arts[k]}</div>
<div class="tick" style="right:44px;top:704px">{tick_svg()}</div>
<h2 class="head fit" data-fit style="top:822px;height:212px;width:800px">{E(head)}</h2>
<p class="body fit" data-fit style="top:1048px;height:184px">{text}</p>
"""
    return s.page(body)


# ---------------------------------------------------------------- slide 6: CTA
def cta(lang, c):
    s = Slide(lang, sky='day', seed=77, dots=(5, N), extra_css=EXTRA + """
.row { position:absolute; left:0; right:0; top:206px; display:flex; justify-content:center; gap:30px; }
.row i { width:150px; height:150px; border-radius:40px; display:grid; place-items:center; font-style:normal;
  box-shadow: 0 22px 40px -22px rgba(23,19,42,.6); }
.row i svg { width:96px; height:96px; }
.row i.q { background: rgba(255,255,255,.85); border: 7px dashed #e8bc4c; font-family:Syne,sans-serif; font-weight:800; font-size:92px; color:#a67d26; transform: rotate(6deg); }
.center { text-align:center; }
.ctah { position:absolute; left:72px; width:936px; top:440px; height:380px; font-size:104px; color:var(--ink); text-align:center;
  display:flex; align-items:center; justify-content:center; }
.ctah > span.in { display:block; }
.btnwrap { position:absolute; left:0; right:0; top:860px; display:flex; justify-content:center; }
.btn.big { font-size:46px; padding:30px 58px; font-family:Syne,sans-serif; font-weight:800; letter-spacing:-.01em; }
.line { position:absolute; left:72px; width:936px; top:1020px; height:64px; font-size:40px; font-weight:600; color:var(--ink); text-align:center; }
.url { position:absolute; left:0; right:0; top:1110px; display:flex; justify-content:center; }
""", nebula=[(-220, -120, 640, 560, ROSE, .32), (600, 80, 620, 560, VIOLET, .32), (-200, 760, 620, 560, TEAL, .32),
             (580, 900, 620, 480, GOLD, .34), (300, 520, 420, 320, SKYBLUE, .24)])
    boxes = ''.join(f'<i style="background:{a};transform:rotate({r}deg)">{tick_svg("#fff" if a == VIOLET else INK)}</i>'
                    for a, r in zip(ACCENTS[:3], (-7, 4, -3)))
    boxes += '<i class="q">?</i>'
    art = f"""<svg class="abs" style="left:0;top:150px" width="1080" height="300" viewBox="0 0 1080 300">
{sparkle(80, 120, 22, GOLD, .95)}{sparkle(1000, 70, 18, ROSE, .9)}{sparkle(1010, 250, 14, TEAL, .9)}{sparkle(60, 270, 12, VIOLET, .85)}</svg>"""
    body = f"""
{art}
<div class="row">{boxes}</div>
<h2 class="ctah fit" data-fit><span class="in">{c['cta_h']}</span></h2>
<div class="btnwrap"><div class="btn big">{E(c['cta_btn'])}</div></div>
<p class="line fit" data-fit>{E(c['cta_line'])}</p>
<div class="url"><span class="chip" style="font-size:30px">webbiespirit.com</span></div>
"""
    return s.page(body)


def main():
    for lang, c in COPY.items():
        pages = [cover(lang, c)] + [item_slide(lang, c, k) for k in range(4)] + [cta(lang, c)]
        for n, doc in enumerate(pages, 1):
            out = render(doc, HERE / 'out' / lang / f'{NAME}-{n}.png')
            print(out)


if __name__ == '__main__':
    main()
