"""Post 5, "Meet the two founders": a 2-slide night-sky carousel.

Slide 1: the two founders as a sun and a planet sharing one gold orbit.
Slide 2: Cyprus drawn as a glowing island, Larnaca lit up, comet paths out to the rest of the island, and the CTA.

Run:  cd social/posts && python3 p5_founders.py
Out:  out/en/5-meet-the-founders-<n>.png and out/el/5-meet-the-founders-<n>.png
"""
import math
import os
from pathlib import Path

# The full Chromium in new-headless mode paints only part of the 1350px viewport (the carousel dots and
# @handle come out blank). The headless shell honours --window-size exactly; kit reads CHROME at import time.
_SHELL = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
if 'CHROME' not in os.environ and os.path.exists(_SHELL):
    os.environ['CHROME'] = _SHELL

from kit import (Slide, render, sun_avatar, planet_avatar, sparkle, E,  # noqa: E402
                 GOLD, GOLD_2, VIOLET, ROSE, TEAL, SKYBLUE, CREAM)

HERE = Path(__file__).resolve().parent
N = 2
SLUG = '5-meet-the-founders'

COPY = {
    'en': {
        'h1': 'Two founders.',
        'h2': 'Every site <span class="nw">hand-finished.</span>',
        'h_size': 100,
        'role_label': 'Co-founder',
        'founders': [
            ('Apollonas', 'Bisaku', 'Design and build'),
            ('Giorgos', 'Paliogiannis', 'Clients and growth'),
        ],
        'amp': '&amp;',
        'eyebrow': 'From the Larnaca seafront',
        's2_h': 'Working with businesses <span class="g glow nw">all over Cyprus.</span>',
        's2_size': 84,
        'towns': {'Nicosia': 'Nicosia', 'Limassol': 'Limassol', 'Paphos': 'Paphos', 'Ayia Napa': 'Ayia Napa', 'Larnaca': 'Larnaca'},
        'talk': 'You talk to the people who <span class="g">build your site.</span>',
        'cta': 'DM us PREVIEW',
        'cta_or': 'or visit <b>webbiespirit.com</b>',
    },
    'el': {
        'h1': 'Δύο ιδρυτές.',
        'h2': 'Κάθε ιστοσελίδα <span class="nw">δουλεμένη στο χέρι.</span>',
        'h_size': 96,
        'role_label': 'ΣΥΝΙΔΡΥΤΗΣ',
        'founders': [
            ('Απόλλωνας', 'Μπισάκου', 'Σχεδιασμός και κατασκευή'),
            ('Γιώργος', 'Παλιογιάννης', 'Πελάτες και ανάπτυξη'),
        ],
        'amp': '&amp;',
        'eyebrow': 'Από την παραλία της Λάρνακας',
        's2_h': 'Δουλεύουμε με επιχειρήσεις σε <span class="g glow nw">όλη την Κύπρο.</span>',
        's2_size': 76,
        'towns': {'Nicosia': 'Λευκωσία', 'Limassol': 'Λεμεσός', 'Paphos': 'Πάφος', 'Ayia Napa': 'Αγία Νάπα', 'Larnaca': 'Λάρνακα'},
        'talk': 'Μιλάτε απευθείας με τους ανθρώπους που <span class="g">φτιάχνουν την ιστοσελίδα σας.</span>',
        'cta': 'Στείλτε μας «PREVIEW»',
        'cta_or': 'ή μπείτε στο <b>webbiespirit.com</b>',
    },
}

# Flying through the sky: each slide gets its own clouds.
NEBULA = {
    1: [(-260, -160, 700, 620, VIOLET, .58), (620, 120, 640, 560, ROSE, .42), (300, 560, 560, 420, GOLD, .22),
        (-240, 900, 680, 560, TEAL, .44), (680, 980, 560, 480, VIOLET, .40)],
    2: [(560, -220, 700, 600, TEAL, .40), (-280, 180, 640, 560, ROSE, .40), (360, 520, 640, 520, VIOLET, .46),
        (-200, 980, 640, 520, VIOLET, .40), (700, 1000, 560, 460, GOLD, .26)],
}

# Star-field seeds chosen so no bright star lands inside the small text and reads as punctuation.
SEED = {1: 57, 2: 77}

# The kit scatters random sparkles that can land on text; they are hidden and placed by hand here.
SPARKS = {
    1: [(1012, 470, 18, GOLD_2, .95), (946, 560, 11, ROSE, .85), (118, 600, 13, GOLD_2, .9), (1034, 1196, 14, GOLD_2, .9),
        (40, 1080, 10, TEAL, .85), (560, 1222, 9, GOLD_2, .7)],
    2: [(1000, 214, 16, GOLD_2, .95), (60, 560, 11, ROSE, .8), (1020, 900, 12, TEAL, .85), (54, 940, 10, GOLD_2, .8),
        (1030, 1086, 12, GOLD_2, .9)],
}

EXTRA_CSS = f"""
.sky svg.stars path {{ display: none; }}
.abs {{ position: absolute; }}
.kicker {{ font-family: Body, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .16em; text-transform: uppercase; color: var(--gold); }}
.glow {{ text-shadow: 0 0 34px rgba(232,188,76,.45); }}
.g {{ color: var(--gold); }}
.nw {{ white-space: nowrap; }}
.hl {{ font-family: Syne, sans-serif; font-weight: 800; letter-spacing: -.035em; line-height: 1.02; text-wrap: balance; color: var(--fg); }}
.hl .two {{ display: block; font-size: .8em; margin-top: .22em; color: var(--gold); text-shadow: 0 0 34px rgba(232,188,76,.45); }}
.av {{ position: absolute; border-radius: 50%; }}
.av svg {{ display: block; border-radius: 50%; }}
.av::before {{ content: ''; position: absolute; inset: -46px; border-radius: 50%; z-index: -1; filter: blur(30px); opacity: .75;
  background: radial-gradient(circle, var(--halo) 0%, transparent 68%); }}
.av .rim {{ position: absolute; inset: -5px; border-radius: 50%; border: 4px solid rgba(232,188,76,.9);
  box-shadow: 0 0 28px rgba(232,188,76,.45), inset 0 0 18px rgba(232,188,76,.25); }}
.amp {{ font-family: Body, sans-serif; font-weight: 700; font-size: 128px; line-height: 1; color: var(--gold);
  text-shadow: 0 0 40px rgba(232,188,76,.6); }}
.fd {{ position: absolute; width: 460px; text-align: center; }}
.fd .lab {{ font-weight: 700; font-size: 26px; letter-spacing: .18em; text-transform: uppercase; color: var(--c); }}
.fd .nm {{ font-family: Syne, sans-serif; font-weight: 800; font-size: 56px; letter-spacing: -.03em; line-height: 1.04; color: var(--fg);
  white-space: nowrap; height: 124px; width: 440px; margin: 12px auto 0; }}
.fd .role {{ font-size: 36px; line-height: 1.3; font-weight: 600; color: #ddd5ea; width: 460px; height: 50px; margin-top: 14px;
  white-space: nowrap; }}
.fd .bar {{ width: 64px; height: 6px; border-radius: 6px; margin: 16px auto 0; background: var(--c); box-shadow: 0 0 16px var(--c); }}
.town {{ position: absolute; font-weight: 700; font-size: 29px; color: {CREAM}; white-space: nowrap;
  text-shadow: 0 2px 10px rgba(13,11,26,.9), 0 0 2px rgba(13,11,26,.9); }}
.here {{ position: absolute; display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px 10px 14px; border-radius: 999px;
  background: linear-gradient(180deg, {GOLD_2}, {GOLD} 60%, #d9a93a); color: #15100a; font-weight: 700; font-size: 28px; white-space: nowrap;
  box-shadow: 0 12px 30px -12px rgba(232,188,76,.8); }}
.here svg {{ width: 30px; height: 30px; }}
.talk {{ position: absolute; display: flex; align-items: center; gap: 30px; }}
.minis {{ position: relative; flex: none; width: 168px; height: 104px; }}
.minis .m {{ position: absolute; top: 0; width: 104px; height: 104px; border-radius: 50%; box-shadow: 0 0 0 4px #15122a, 0 0 0 7px rgba(232,188,76,.85); }}
.minis .m svg {{ display: block; }}
.talk .tx {{ font-size: 40px; line-height: 1.28; font-weight: 600; color: var(--fg); width: 736px; height: 108px; text-wrap: balance; }}
.btn.big {{ font-size: 40px; padding: 28px 50px; }}
.btn svg {{ width: 40px; height: 40px; }}
.ctaor {{ font-size: 30px; line-height: 1.25; color: var(--muted); font-weight: 500; white-space: nowrap; }}
.ctaor b {{ display: block; font-size: 34px; color: var(--gold); font-weight: 700; }}
"""

ARROW = ('<svg viewBox="0 0 40 40" fill="none" stroke="#15100a" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M8 20 H31 M22 11 L31 20 L22 29"/></svg>')
PIN = ('<svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="13" fill="#15100a"/>'
       + sparkle(15, 15, 9, GOLD_2, 1) + '</svg>')


# ---------- geometry helpers ----------

def ell_pt(cx, cy, rx, ry, rot, t):
    """Point at parameter angle t (degrees) on an ellipse rotated by rot degrees (screen coords, y down)."""
    a, r = math.radians(t), math.radians(rot)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)


def half_arc(cx, cy, rx, ry, rot, front):
    """Back (upper) or front (lower) half of a rotated ellipse, as an SVG arc path."""
    x1, y1 = ell_pt(cx, cy, rx, ry, rot, 180 if not front else 0)
    x2, y2 = ell_pt(cx, cy, rx, ry, rot, 0 if not front else 180)
    return f'M{x1:.1f} {y1:.1f} A{rx} {ry} {rot} 0 1 {x2:.1f} {y2:.1f}'


def sparks(n):
    return ('<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350" viewBox="0 0 1080 1350">'
            + ''.join(sparkle(x, y, s, col, op) for x, y, s, col, op in SPARKS[n]) + '</svg>')


# ---------- slide 1: the founders ----------

AV = 280            # avatar diameter
AY = 752            # avatar centre line
AX = (297, 783)     # avatar centres, over each founder's column
RING = dict(cx=540, cy=AY, rx=430, ry=112, rot=-7)
HEAD = 84           # where the comet rides on the front of the orbit (degrees)

# After kit's fit pass, give both founders' names (and both roles) the same size, the smaller of the two.
EQUALISE = """<script>document.fonts.ready.then(()=>setTimeout(()=>{for(const sel of ['.nm','.role']){
const els=[...document.querySelectorAll(sel)];const m=Math.min(...els.map(e=>parseFloat(getComputedStyle(e).fontSize)));
els.forEach(e=>e.style.fontSize=m+'px');}},0));</script>"""


def founders(lang, c):
    size = c['h_size']
    # Headline boxes carry 40px of left/bottom padding so the gold glow is not clipped by the fit box's overflow;
    # no right padding, so the fit pass still catches a line running past the 1008px margin.
    head = (f'<div class="abs hl fit" data-fit style="left:32px;top:184px;width:976px;height:370px;padding:0 0 40px 40px;font-size:{size}px">'
            f'<span class="nw">{E(c["h1"])}</span><span class="two">{c["h2"]}</span></div>')

    r = RING
    # a wider, dashed orbit far behind, for depth
    back = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">
<defs><linearGradient id="ringG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ROSE}"/><stop offset=".5" stop-color="{GOLD_2}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
<filter id="soft" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>
<ellipse cx="540" cy="{AY}" rx="502" ry="150" transform="rotate(4 540 {AY})" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-width="2" stroke-dasharray="3 12" stroke-linecap="round"/>
<path d="{half_arc(**r, front=False)}" fill="none" stroke="url(#ringG)" stroke-width="10" opacity=".45" filter="url(#soft)"/>
<path d="{half_arc(**r, front=False)}" fill="none" stroke="url(#ringG)" stroke-width="4" stroke-linecap="round" opacity=".8"/>
</svg>"""

    # the two founders, sun and planet, each with its own coloured halo
    avs = ''
    for (x, halo, art) in ((AX[0], ROSE, sun_avatar(AV)), (AX[1], TEAL, planet_avatar(AV))):
        avs += (f'<div class="av" style="left:{x - AV // 2}px;top:{AY - AV // 2}px;width:{AV}px;height:{AV}px;--halo:{halo}">'
                f'{art}<span class="rim"></span></div>')

    # front half of the shared orbit passes in front of both, with a comet riding it
    trail = ''
    for k in range(13):
        t = HEAD + 4 + k * 3
        px, py = ell_pt(**r, t=t)
        trail += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{max(1.4, 8 - k * .45):.1f}" fill="{GOLD_2}" opacity="{max(.06, .95 - k * .06):.2f}"/>'
    hx, hy = ell_pt(**r, t=HEAD)
    front = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">
<path d="{half_arc(**r, front=True)}" fill="none" stroke="url(#ringG)" stroke-width="10" opacity=".45" filter="url(#soft)"/>
<path d="{half_arc(**r, front=True)}" fill="none" stroke="url(#ringG)" stroke-width="4.5" stroke-linecap="round"/>
{trail}<circle cx="{hx:.1f}" cy="{hy:.1f}" r="11" fill="#fff6d6"/>{sparkle(round(hx, 1), round(hy, 1), 30, GOLD_2, .95)}
</svg>"""

    amp = f'<div class="abs amp" style="left:0;width:1080px;top:{AY - 64}px;text-align:center">{c["amp"]}</div>'

    cols = ''
    for k, (first, last, role) in enumerate(c['founders']):
        col = ROSE if k == 0 else TEAL
        left = AX[k] - 230
        cols += (f'<div class="fd" style="left:{left}px;top:{AY + AV // 2 + 44}px;--c:{col}">'
                 f'<div class="lab">{E(c["role_label"])}</div>'
                 f'<div class="nm fit" data-fit>{E(first)}<br>{E(last)}</div>'
                 f'<div class="role fit" data-fit>{E(role)}</div></div>')
    return head + back + avs + front + amp + cols + sparks(1) + EQUALISE


# ---------- slide 2: Larnaca to all of Cyprus ----------

# Cyprus coastline, clockwise from Cape Arnauti (lon, lat). Rough on purpose: it is drawn as a glowing island.
COAST = [
    (32.27, 35.10), (32.34, 35.06), (32.41, 35.04), (32.46, 35.05), (32.52, 35.12), (32.58, 35.17), (32.70, 35.18),
    (32.81, 35.15), (32.88, 35.18), (32.92, 35.26), (32.93, 35.39), (33.05, 35.36), (33.20, 35.35), (33.32, 35.34),
    (33.50, 35.34), (33.70, 35.38), (33.90, 35.43), (34.10, 35.50), (34.30, 35.58), (34.45, 35.64), (34.59, 35.70),
    (34.50, 35.63), (34.30, 35.51), (34.10, 35.40), (33.96, 35.30), (33.93, 35.20), (33.95, 35.12), (34.00, 35.04),
    (34.08, 34.97), (33.98, 34.97), (33.85, 34.96), (33.70, 34.94), (33.63, 34.91), (33.61, 34.82), (33.45, 34.75),
    (33.33, 34.71), (33.15, 34.70), (33.04, 34.67), (32.99, 34.60), (32.95, 34.56), (32.90, 34.62), (32.80, 34.64),
    (32.70, 34.65), (32.60, 34.68), (32.47, 34.73), (32.40, 34.76), (32.33, 34.85), (32.32, 34.95), (32.29, 35.03),
]
TOWNS = {  # lon, lat, label offset (dx, dy) from the star, anchor
    'Nicosia': (33.37, 35.17, (0, -34), 'c'),
    'Limassol': (33.04, 34.69, (22, 34), 'l'),
    'Paphos': (32.43, 34.78, (-6, 44), 'c'),
    'Ayia Napa': (33.99, 34.99, (18, 38), 'l'),
}
LARNACA = (33.63, 34.92)
K = 310                 # px per degree of longitude
KY = K * 1.22           # px per degree of latitude (cos 35 deg)
MAP_CX, MAP_TOP = 540, 510


def proj(lon, lat):
    return MAP_CX + (lon - 33.43) * K, MAP_TOP + (35.70 - lat) * KY


def smooth_closed(pts):
    """Closed Catmull-Rom spline through pts, as cubic Beziers."""
    n = len(pts)
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + 'Z'


def island(c):
    pts = [proj(lo, la) for lo, la in COAST]
    shape = smooth_closed(pts)
    lx, ly = proj(*LARNACA)
    paths, stars, labels = '', '', ''
    for name, (lo, la, (dx, dy), anchor) in TOWNS.items():
        tx, ty = proj(lo, la)
        # a comet path arching from Larnaca out to the town
        mx, my = (lx + tx) / 2, (ly + ty) / 2 - 70 - abs(tx - lx) * .12
        paths += (f'<path d="M{lx:.1f} {ly:.1f} Q{mx:.1f} {my:.1f} {tx:.1f} {ty:.1f}" fill="none" stroke="{GOLD}" stroke-width="3.5" '
                  f'stroke-dasharray="1 11" stroke-linecap="round" opacity=".95"/>')
        stars += (f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="14" fill="{CREAM}" opacity=".18"/>'
                  f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="6.5" fill="{CREAM}"/>')
        lab = E(c['towns'][name])
        if anchor == 'c':
            labels += f'<div class="town" style="left:{tx + dx - 200:.0f}px;width:400px;text-align:center;top:{ty + dy - 18:.0f}px">{lab}</div>'
        else:
            labels += f'<div class="town" style="left:{tx + dx:.0f}px;top:{ty + dy - 18:.0f}px">{lab}</div>'
    pulse = ''.join(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{rr}" fill="none" stroke="{GOLD}" stroke-width="2.5" opacity="{op}"/>'
                    for rr, op in ((30, .8), (50, .45), (72, .2)))
    svg = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">
<defs><linearGradient id="isl" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{ROSE}"/><stop offset=".45" stop-color="{VIOLET}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
<linearGradient id="islS" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{ROSE}"/><stop offset=".5" stop-color="{GOLD_2}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
<filter id="isGlow" x="-20%" y="-30%" width="140%" height="160%"><feGaussianBlur stdDeviation="16"/></filter></defs>
<path d="{shape}" fill="url(#isl)" opacity=".55" filter="url(#isGlow)"/>
<path d="{shape}" fill="url(#isl)" opacity=".42"/>
<path d="{shape}" fill="none" stroke="url(#islS)" stroke-width="3" stroke-linejoin="round" opacity=".9"/>
{paths}{stars}{pulse}
<circle cx="{lx:.1f}" cy="{ly:.1f}" r="16" fill="#fff6d6"/>{sparkle(round(lx, 1), round(ly, 1), 34, GOLD_2, 1)}
</svg>"""
    here = f'<div class="here" style="left:{lx + 6:.0f}px;top:{ly + 52:.0f}px">{PIN}{E(c["towns"]["Larnaca"])}</div>'
    return svg + labels + here


def reach(lang, c):
    head = (f'<div class="abs kicker" style="left:72px;top:184px">{E(c["eyebrow"])}</div>'
            f'<div class="abs hl fit" data-fit style="left:32px;top:232px;width:976px;height:302px;padding:0 0 40px 40px;font-size:{c["s2_size"]}px">'
            f'{c["s2_h"]}</div>')
    talk = (f'<div class="talk" style="left:72px;top:966px">'
            f'<div class="minis"><span class="m" style="left:0">{sun_avatar(104)}</span>'
            f'<span class="m" style="left:64px">{planet_avatar(104)}</span></div>'
            f'<div class="tx fit" data-fit>{c["talk"]}</div></div>')
    cta = (f'<div class="abs" style="left:72px;top:1120px;display:flex;align-items:center;gap:30px">'
           f'<span class="btn big">{E(c["cta"])}{ARROW}</span><span class="ctaor">{c["cta_or"]}</span></div>')
    return island(c) + head + talk + cta + sparks(2)


# ---------- build ----------

def build(lang):
    c = COPY[lang]
    out = []
    for i in range(1, N + 1):
        s = Slide(lang=lang, sky='night', seed=SEED[i], nebula=NEBULA[i], dots=(i - 1, N), extra_css=EXTRA_CSS)
        body = founders(lang, c) if i == 1 else reach(lang, c)
        png = HERE / 'out' / lang / f'{SLUG}-{i}.png'
        render(s.page(body), png)
        out.append(png)
    return out


def main():
    for lang in ('en', 'el'):
        for p in build(lang):
            print(p)


if __name__ == '__main__':
    main()
