"""Post 3, "Packages": one night-sky slide. Three planets of growing size ride one orbit,
each carrying its package's price: small teal Start, glowing gold Pro (most picked), big ringed Ultra.

Run:  cd social/posts && python3 p3_packages.py
Out:  out/en/3-packages-1.png and out/el/3-packages-1.png
"""
from pathlib import Path

from kit import (Slide, render, sparkle, E,
                 GOLD, GOLD_2, VIOLET, ROSE, TEAL, SKYBLUE, CREAM)

HERE = Path(__file__).resolve().parent

COPY = {
    'en': {
        'kicker': 'Our packages',
        'title': 'Pick your <span class="g">orbit.</span>',
        # '|' forces a line break, so each card reads as tidy rows instead of wrapping wherever the width runs out.
        'start': ['One page', 'Request form', '|', 'Map', 'QR code'],
        'pro': ['Online booking', '|', 'A shop for your products', '|', 'Google done properly'],
        'ultra': ['Chatbot', 'Live visitors', '|', 'Customer accounts', '|', 'Premium branding'],
        'badge': 'Most picked',
        'plus': 'Everything in Pro +',
        'care': ('Care from €30/month:', 'hosting, domain and small edits.'),
        'cta': '<b>Free preview first.</b> Pay only if you love it.',
    },
    'el': {
        'kicker': 'ΤΑ ΠΑΚΕΤΑ ΜΑΣ',
        'title': 'Διαλέξτε <span class="g">τροχιά.</span>',
        'start': ['Μία σελίδα', 'Φόρμα αιτήματος', '|', 'Χάρτης', 'QR code'],
        'pro': ['Online κρατήσεις', '|', 'Κατάστημα για τα προϊόντα σας', '|', 'Σωστή παρουσία στο Google'],
        'ultra': ['Chatbot', 'Live επισκέπτες', '|', 'Λογαριασμοί πελατών', '|', 'Premium branding'],
        'badge': 'Η πιο δημοφιλής επιλογή',
        'plus': 'Όλα όσα έχει το Pro +',
        'care': ('Συντήρηση από €30/μήνα:', 'hosting, domain και μικρές αλλαγές.'),
        # Too long for one line at a readable size, so the Greek CTA stacks its two sentences.
        'cta': '<b>Πρώτα η δωρεάν μακέτα.</b><br>Πληρώνετε μόνο αν σας ενθουσιάσει.',
    },
}

# Gold sits behind Pro so the highlighted card glows; the other clouds frame the orbit.
NEBULA = [(-260, 80, 720, 560, VIOLET, .55), (640, 300, 600, 620, ROSE, .38), (520, 470, 460, 380, GOLD, .22),
          (-280, 820, 700, 560, TEAL, .36), (560, 960, 680, 520, SKYBLUE, .44)]

# The kit scatters sparkles at random, which land on text: they are hidden and placed here by hand.
W_ = '#ffffff'
SPARKS = [(1022, 222, 13, GOLD_2, .9), (600, 150, 9, W_, .75), (40, 330, 9, W_, .7), (1050, 556, 10, GOLD_2, .85),
          (40, 800, 9, W_, .65), (1050, 1110, 12, GOLD_2, .85)]

# Rows: key, card top, card height, planet (cx, r), text right edge. The orbit is drawn through the planets.
ROWS = [
    ('start', 318, 190, (932, 64), 850),
    ('pro', 524, 232, (896, 88), 776),
    ('ultra', 772, 232, (904, 102), 750),
]
CARE_TOP, CTA_TOP = 1028, 1128

EXTRA_CSS = """
.sky svg.stars path { display: none; }
.abs { position: absolute; }
.kicker { font-family: Body, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); }
.title { font-family: Syne, sans-serif; font-weight: 800; letter-spacing: -.035em; line-height: 1.05; color: var(--cream);
  white-space: nowrap; font-size: 86px; }
.title .g { color: var(--gold); text-shadow: 0 0 34px rgba(232,188,76,.45); }
.pk { position: absolute; left: 72px; width: 936px; border-radius: 34px; border: 2px solid var(--c);
  background: linear-gradient(120deg, color-mix(in srgb, var(--c) 30%, rgba(13,11,26,.55)), rgba(13,11,26,.45) 62%, color-mix(in srgb, var(--c) 18%, rgba(13,11,26,.5)));
  backdrop-filter: blur(6px); box-shadow: 0 26px 60px -34px color-mix(in srgb, var(--c) 90%, transparent); }
.pk.hot { border-width: 3px; box-shadow: 0 0 0 7px rgba(232,188,76,.14), 0 0 70px -10px rgba(232,188,76,.55); }
.pk .in { position: absolute; left: 40px; top: 22px; bottom: 18px; display: flex; flex-direction: column; gap: 10px; }
.pk .head { display: flex; align-items: center; gap: 20px; height: 54px; flex: none; }
.pk .name { font-family: Syne, sans-serif; font-weight: 800; font-size: 56px; letter-spacing: -.03em; line-height: 1; color: var(--cream); }
.pk.hot .name { color: var(--gold); }
.pk .feat { flex: 1; min-height: 0; font-size: 34px; line-height: 1.2; color: #ece6f4; font-weight: 500; }
.pk .feat span { white-space: nowrap; display: inline-block; vertical-align: top; margin-right: 24px; }
.pk .feat span:last-child { margin-right: 0; }
.pk .feat.grid2 { display: grid; grid-template-columns: max-content max-content; column-gap: 40px; align-content: start; }
.pk .feat.grid2 span { margin-right: 0; }
.pk .feat span svg { width: .65em; height: .65em; margin-right: 10px; vertical-align: -.02em; }
.badge { display: inline-flex; align-items: center; gap: 10px; font-weight: 700; font-size: 26px; padding: 10px 22px 10px 16px; border-radius: 999px;
  white-space: nowrap; }
.badge.gold { background: linear-gradient(180deg, var(--gold-2), var(--gold) 60%, #d9a93a); color: #15100a; box-shadow: 0 10px 26px -10px rgba(232,188,76,.9); }
.badge.line { border: 2px solid var(--rose); color: var(--cream); background: rgba(255,111,174,.16); padding: 8px 22px; }
.badge svg { width: 26px; height: 26px; }
.planet { position: absolute; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.planet::after { content: ''; position: absolute; inset: 0; border-radius: 50%;
  background: radial-gradient(circle at 74% 78%, rgba(13,11,26,.38), rgba(13,11,26,0) 58%); }
.planet .p { position: relative; z-index: 2; font-family: Body, sans-serif; font-weight: 700; letter-spacing: -.04em; line-height: 1; font-variant-numeric: lining-nums; }
.planet .was { position: relative; z-index: 2; font-size: 34px; font-weight: 700; letter-spacing: -.02em; margin-bottom: 4px; color: #3a2808;
  text-decoration: line-through; text-decoration-color: #c2185b; text-decoration-thickness: 4px; }
.care { display: flex; align-items: center; gap: 24px; }
.care .t { width: 820px; height: 82px; font-size: 34px; line-height: 1.2; white-space: nowrap; color: #d3cbe0; }
.care .t b { display: block; color: var(--cream); font-weight: 700; }
.cta { position: absolute; left: 72px; width: 936px; height: 104px; border-radius: 52px; display: flex; align-items: center; justify-content: center; gap: 22px;
  background: linear-gradient(180deg, var(--gold-2), var(--gold) 55%, #d9a93a); color: #15100a;
  box-shadow: 0 1px 0 rgba(255,255,255,.5) inset, 0 18px 40px -16px rgba(166,125,38,.8); }
.cta .t { max-width: 760px; text-align: center; white-space: nowrap; font-size: 40px; line-height: 1.15; font-weight: 500; letter-spacing: -.005em; }
.cta .t b { font-weight: 700; }
html[lang=el] .cta { height: 116px; border-radius: 58px; margin-top: -4px; }
html[lang=el] .cta .t { font-size: 35px; line-height: 1.2; }
.cta svg { width: 40px; height: 40px; flex: none; }
"""


def spark_icon(color):
    return f'<svg viewBox="0 0 22 22">{sparkle(11, 11, 10, color, 1)}</svg>'


def orbit_svg(points):
    """A dashed orbit through the planet centres, entering and leaving at the right edge (Catmull-Rom spline)."""
    pts = [(1110, 150)] + points + [(1110, 1210)]
    pts = [pts[0]] + pts + [pts[-1]]
    d = f'M{pts[1][0]:.1f} {pts[1][1]:.1f}'
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">
<path d="{d}" fill="none" stroke="rgba(245,239,226,.45)" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round"/>
</svg>"""


def comet():
    """A comet streaking across the top-right sky, head down-left."""
    return f"""<svg class="abs" style="left:640px;top:70px" width="400" height="110" viewBox="0 0 400 110" aria-hidden="true">
<defs><linearGradient id="tail" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ROSE}" stop-opacity="0"/>
<stop offset=".6" stop-color="{GOLD}" stop-opacity=".55"/><stop offset="1" stop-color="{GOLD_2}" stop-opacity="1"/></linearGradient>
<radialGradient id="cometGlow"><stop offset="0" stop-color="{GOLD_2}" stop-opacity=".9"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>
<path d="M392 6 L60 86 L66 96 Z" fill="url(#tail)"/>
<path d="M360 30 L80 92" stroke="{TEAL}" stroke-opacity=".35" stroke-width="2"/>
<circle cx="62" cy="91" r="24" fill="url(#cometGlow)"/><circle cx="62" cy="91" r="9" fill="#fff6d6"/>
</svg>"""


def ring(cx, cy, r, front):
    """Ultra's ring, split into a back half (under the planet) and a front half (over it)."""
    rx, ry, rot = r * 1.4, r * .36, -10
    w, h = rx * 2 + 20, ry * 2 + 80
    d = f'M10 {h / 2} A{rx} {ry} 0 0 {0 if front else 1} {w - 10} {h / 2}'
    return (f'<svg class="abs" style="left:{cx - w / 2}px;top:{cy - h / 2}px;overflow:visible;z-index:{4 if front else 2}" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" aria-hidden="true"><g transform="rotate({rot} {w / 2} {h / 2})">'
            f'<path d="{d}" fill="none" stroke="url(#goldStroke)" stroke-width="{9 if front else 7}" stroke-linecap="round" opacity="{1 if front else .6}"/>'
            f'</g></svg>')


def planet(key, cx, cy, r):
    left, top, size = cx - r, cy - r, 2 * r
    under = extra = ''
    if key == 'start':
        bg = f'radial-gradient(circle at 34% 28%, #e3fffa, {TEAL} 46%, #16707a 100%)'
        glow = 'rgba(56,214,196,.55)'
        inner = '<div class="p" style="font-size:40px;color:#06262b">€350</div>'
        extra = (f'<div class="abs" style="left:{cx + r * .62}px;top:{cy - r * 1.12}px;width:18px;height:18px;border-radius:50%;'
                 f'background:radial-gradient(circle at 35% 30%,#fff,{SKYBLUE});box-shadow:0 0 14px {SKYBLUE};z-index:3"></div>')
    elif key == 'pro':
        bg = f'radial-gradient(circle at 36% 28%, #fff6d6, {GOLD} 46%, #8a6420 100%)'
        glow = 'rgba(232,188,76,.75)'
        inner = ('<div class="was">€699</div>'
                 '<div class="p" style="font-size:58px;color:#1b1430">€499</div>')
        mr = r + 20
        under = (f'<div class="abs" style="left:{cx - mr}px;top:{cy - mr}px;width:{2 * mr}px;height:{2 * mr}px;border-radius:50%;'
                 f'border:2.5px dashed rgba(248,223,142,.6);z-index:2"></div>')
        extra = (f'<div class="abs" style="left:{cx - mr * .72 - 11}px;top:{cy - mr * .69 - 11}px;width:22px;height:22px;border-radius:50%;'
                 f'background:radial-gradient(circle at 35% 30%,#fff,{ROSE});box-shadow:0 0 16px {ROSE};z-index:4"></div>')
    else:
        bg = f'radial-gradient(circle at 34% 26%, #ffd9ec, {ROSE} 34%, {VIOLET} 72%, #2e1960 100%)'
        glow = 'rgba(255,111,174,.5)'
        inner = ('<div class="p" style="font-size:60px;color:#fffaf0;text-shadow:0 2px 12px rgba(46,25,96,.6);'
                 'transform:translateY(-16px)">€947</div>')
        under = ring(cx, cy, r, front=False)
        extra = ring(cx, cy, r, front=True)
    halo = (f'<div class="abs" style="left:{cx - r * 1.5}px;top:{cy - r * 1.5}px;width:{r * 3}px;height:{r * 3}px;border-radius:50%;'
            f'background:radial-gradient(circle,{glow},transparent 62%);z-index:1"></div>')
    body = (f'<div class="planet" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;background:{bg};z-index:3;'
            f'box-shadow:0 0 0 1px rgba(255,255,255,.18) inset">{inner}</div>')
    return halo + under + body + extra


def card(c, key, top, h, text_right):
    colour = {'start': TEAL, 'pro': GOLD, 'ultra': ROSE}[key]
    bullet = {'start': TEAL, 'pro': GOLD_2, 'ultra': ROSE}[key]
    name = {'start': 'Start', 'pro': 'Pro', 'ultra': 'Ultra'}[key]
    width = text_right - 72 - 40
    head = f'<div class="name">{name}</div>'
    if key == 'pro':
        head += f'<div class="badge gold"><svg viewBox="0 0 26 26">{sparkle(13, 13, 12, "#15100a", 1)}</svg>{E(c["badge"])}</div>'
    if key == 'ultra':
        head += f'<div class="badge line">{E(c["plus"])}</div>'
    s = spark_icon(bullet)
    grid = key == 'start'  # Start's four short items sit in two aligned columns
    body = ''.join(('' if grid else '<br>') if t == '|' else f'<span>{s}{E(t)}</span>' for t in c[key])
    return (f'<div class="pk{" hot" if key == "pro" else ""}" style="top:{top}px;height:{h}px;--c:{colour}">'
            f'<div class="in" style="width:{width}px"><div class="head">{head}</div>'
            f'<div class="feat fit{" grid2" if grid else ""}" data-fit style="width:{width}px">{body}</div></div></div>')


def satellite():
    """The care plan: a little satellite looking after your site in orbit."""
    return f"""<svg viewBox="0 0 64 64" width="72" height="72" aria-hidden="true" style="flex:none;overflow:visible">
<g transform="rotate(-30 32 32)">
<rect x="2" y="25" width="17" height="14" rx="2" fill="{SKYBLUE}" stroke="{CREAM}" stroke-width="2"/>
<rect x="45" y="25" width="17" height="14" rx="2" fill="{SKYBLUE}" stroke="{CREAM}" stroke-width="2"/>
<path d="M10.5 25v14M53.5 25v14" stroke="{CREAM}" stroke-width="1.5"/>
<rect x="21" y="22" width="22" height="20" rx="5" fill="{GOLD}"/>
<path d="M19 32h2M43 32h2" stroke="{CREAM}" stroke-width="3"/>
<path d="M32 22v-8" stroke="{CREAM}" stroke-width="2.5"/><circle cx="32" cy="12" r="4" fill="{ROSE}"/>
</g>{sparkle(58, 8, 6, GOLD_2, .95)}</svg>"""


def slide(c):
    centres = [(cx, top + h / 2) for _, top, h, (cx, _r), _t in ROWS]
    parts = [
        orbit_svg(centres),
        comet(),
        f'<div class="abs kicker" style="left:74px;top:170px">{E(c["kicker"])}</div>',
        f'<div class="abs title fit" data-fit style="left:72px;top:206px;width:936px;height:96px">{c["title"]}</div>',
    ]
    for key, top, h, _p, text_right in ROWS:
        parts.append(card(c, key, top, h, text_right))
    for key, top, h, (cx, r), _t in ROWS:
        parts.append(planet(key, cx, top + h / 2, r))
    care_b, care_t = c['care']
    parts.append(f'<div class="abs care" style="left:76px;top:{CARE_TOP}px">{satellite()}'
                 f'<div class="t fit" data-fit><b>{E(care_b)}</b>{E(care_t)}</div></div>')
    star = f'<svg viewBox="0 0 40 40">{sparkle(20, 20, 18, "#15100a", 1)}</svg>'
    parts.append(f'<div class="cta" style="top:{CTA_TOP}px">{star}<div class="t">{c["cta"]}</div>{star}</div>')
    parts.append('<svg class="abs" style="left:0;top:0;pointer-events:none;z-index:6" width="1080" height="1350" viewBox="0 0 1080 1350">'
                 + ''.join(sparkle(x, y, s, col, op) for x, y, s, col, op in SPARKS) + '</svg>')
    return ''.join(parts)


def build(lang):
    page = Slide(lang=lang, sky='night', seed=303, nebula=NEBULA, extra_css=EXTRA_CSS).page(slide(COPY[lang]))
    return [render(page, HERE / 'out' / lang / '3-packages-1.png')]


if __name__ == '__main__':
    for lang in ('en', 'el'):
        for p in build(lang):
            print(p)
