"""Post 1, "How the free preview works": a 5-slide night-sky carousel that plays like a launch countdown.

Run:  cd social/posts && python3 p1_how_it_works.py
Out:  out/en/1-how-it-works-<n>.png and out/el/1-how-it-works-<n>.png
"""
import os
from pathlib import Path

# The full Chromium in new-headless mode paints only a 1080x1263 viewport inside the 1350 screenshot
# (the bottom 87px, with the carousel dots and @handle, come out blank). The headless shell honours
# --window-size exactly, so prefer it when present. kit reads CHROME at import time.
_SHELL = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
if 'CHROME' not in os.environ and os.path.exists(_SHELL):
    os.environ['CHROME'] = _SHELL

from kit import (Slide, render, logo, sparkle, E,  # noqa: E402
                 GOLD, GOLD_2, VIOLET, ROSE, TEAL, SKYBLUE, CREAM, NIGHT)

HERE = Path(__file__).resolve().parent
N = 5

COPY = {
    'en': {
        'cover_kicker': 'The free preview',
        'cover_h1': 'Your new website.',
        'cover_h2': 'Before you pay a cent.',
        'cover_more': 'How it works',
        'step': 'Step {n} of 3',
        's1_h': 'Send us your Instagram.',
        's1_lead': 'What to send:',
        's1_items': ['Instagram or Facebook page', 'Price list', 'Opening hours', 'Logo, if you have one'],
        's2_h': 'We build your free preview',
        's2_gold': 'in two days.',
        's2_stamp': 'Free',
        's3_h': 'You see it on your phone.',
        's3_love_q': 'Love it?',
        's3_love_a': 'Live within a week.',
        's3_no_q': 'Not for you?',
        's3_no_a': 'You owe nothing.',
        'cta_h': 'Ready for launch?',
        'cta_lead': ['Free preview first.', 'You pay nothing until you love it.'],
        'cta_btn': 'DM us PREVIEW',
        'cta_or': 'or visit',
    },
    'el': {
        'cover_kicker': 'Η δωρεάν μακέτα',
        'cover_h1': 'Η νέα σας ιστοσελίδα.',
        # "Πριν πληρώσετε" is too wide for one line in Syne Greek, which orphaned "Πριν"; this reads as
        # naturally ("before you give a single euro") and sets as two balanced lines.
        'cover_h2': 'Πριν δώσετε ούτε ένα ευρώ.',
        'cover_more': 'Πώς λειτουργεί',
        'step': 'Βήμα {n} από 3',
        's1_h': 'Στείλτε μας το Instagram σας.',
        's1_lead': 'Τι να μας στείλετε:',
        's1_items': ['Σελίδα Instagram ή Facebook', 'Τιμοκατάλογο', 'Ωράριο λειτουργίας', 'Λογότυπο, αν έχετε'],
        's2_h': 'Φτιάχνουμε τη δωρεάν μακέτα σας',
        's2_gold': 'σε δύο μέρες.',
        's2_stamp': 'Δωρεάν',
        's3_h': 'Τη βλέπετε στο κινητό σας.',
        's3_love_q': 'Σας αρέσει;',
        's3_love_a': 'Online μέσα σε μία εβδομάδα.',
        's3_no_q': 'Δεν σας κάνει;',
        's3_no_a': 'Δεν χρωστάτε τίποτα.',
        # "Έτοιμοι" would open on a capital with tonos, which Syne sets as a loose mark in the margin.
        'cta_h': 'Πάμε για εκτόξευση;',
        'cta_lead': ['Πρώτα η δωρεάν μακέτα.', 'Πληρώνετε μόνο αν σας ενθουσιάσει.'],
        'cta_btn': 'Στείλτε μας «PREVIEW»',
        'cta_or': 'ή στο',
    },
}

# One flight through the sky: each slide gets its own nebula so swiping feels like moving.
NEBULA = {
    1: [(-260, 120, 760, 620, VIOLET, .62), (560, -220, 700, 560, ROSE, .42), (620, 820, 640, 560, TEAL, .40), (180, 300, 620, 420, GOLD, .22)],
    2: [(520, -160, 720, 600, ROSE, .50), (-300, 520, 700, 640, SKYBLUE, .46), (560, 900, 620, 520, VIOLET, .50)],
    3: [(-220, -120, 700, 560, TEAL, .40), (520, 380, 720, 640, VIOLET, .56), (-160, 940, 640, 480, GOLD, .28), (700, -140, 480, 420, ROSE, .30)],
    4: [(560, -200, 680, 560, SKYBLUE, .48), (-280, 300, 640, 640, ROSE, .42), (480, 860, 720, 560, TEAL, .40)],
    5: [(-220, 760, 820, 660, ROSE, .52), (480, 560, 760, 640, VIOLET, .62), (520, -200, 640, 520, GOLD, .30), (-280, -120, 560, 460, TEAL, .34)],
}

# The kit scatters seven sparkles at random, which land on text. Those are hidden (see EXTRA_CSS)
# and each slide gets its own, placed by hand in open sky: (x, y, size, colour, opacity).
W_ = '#ffffff'
SPARKS = {
    1: [(250, 250, 22, GOLD_2, .95), (850, 520, 16, GOLD_2, .9), (800, 210, 10, W_, .8), (210, 560, 12, W_, .75),
        (965, 330, 12, GOLD_2, .85), (120, 420, 9, W_, .7), (985, 1170, 14, GOLD_2, .85), (1010, 700, 9, W_, .7)],
    2: [(960, 165, 14, GOLD_2, .9), (640, 172, 9, W_, .75), (905, 716, 16, GOLD_2, .9), (1046, 980, 9, W_, .7), (36, 560, 10, W_, .7)],
    3: [(975, 168, 14, GOLD_2, .9), (650, 168, 9, W_, .75), (1046, 600, 9, W_, .7)],
    4: [(960, 165, 14, GOLD_2, .9), (640, 172, 9, W_, .75), (1046, 676, 10, GOLD_2, .8), (40, 640, 9, W_, .7)],
    5: [(130, 190, 10, W_, .75), (420, 560, 13, GOLD_2, .9), (1010, 960, 14, GOLD_2, .85), (930, 1180, 10, W_, .7)],
}


def sparks(n):
    return ('<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350" viewBox="0 0 1080 1350">'
            + ''.join(sparkle(x, y, sz, col, op) for x, y, sz, col, op in SPARKS[n]) + '</svg>')


EXTRA_CSS = """
.sky svg.stars path { display: none; }
.abs { position: absolute; }
.kicker { font-family: Body, sans-serif; font-weight: 700; font-size: 30px; letter-spacing: .16em; text-transform: uppercase; color: var(--gold); }
.hl { font-family: Syne, sans-serif; font-weight: 800; letter-spacing: -.035em; line-height: 1.04; color: var(--cream); text-wrap: balance; }
.hl .g { color: var(--gold); }
.glow { text-shadow: 0 0 34px rgba(232,188,76,.45); }
.num { font-family: Body, sans-serif; font-weight: 700; letter-spacing: -.04em; line-height: 1; font-variant-numeric: lining-nums; }
.tint { border-radius: 30px; border: 2px solid var(--c); position: absolute; overflow: hidden;
  background: linear-gradient(135deg, color-mix(in srgb, var(--c) 30%, transparent), rgba(255,255,255,.04) 70%);
  box-shadow: 0 24px 60px -30px color-mix(in srgb, var(--c) 80%, transparent); }
.ico { width: 96px; height: 96px; border-radius: 28px; flex: none; display: grid; place-items: center;
  background: linear-gradient(145deg, var(--c), var(--c2)); box-shadow: 0 10px 30px -10px var(--c); }
.ico svg { width: 56px; height: 56px; }
.more { display: inline-flex; align-items: center; gap: 16px; font-weight: 700; font-size: 36px; color: var(--cream);
  padding: 18px 34px; border-radius: 999px; border: 2px solid rgba(245,239,226,.35); background: rgba(13,11,26,.35); }
.more b { color: var(--gold); font-size: 40px; line-height: 1; }
.btn.big { font-size: 42px; padding: 30px 54px; }
"""

NUM_FONT = 'font-family="Body, sans-serif" font-weight="700"'


# ---------- drawings ----------

def rocket(w=150, uid='r'):
    """A playful rocket pointing up, drawn in a 120x240 box."""
    h = w * 2
    return f"""<svg viewBox="0 0 120 240" width="{w}" height="{h}" style="overflow:visible" aria-hidden="true">
<defs>
 <linearGradient id="body{uid}" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{CREAM}"/><stop offset="1" stop-color="#cbc1df"/></linearGradient>
 <linearGradient id="flame{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD_2}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></linearGradient>
 <radialGradient id="win{uid}" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#bff6ee"/><stop offset=".6" stop-color="{TEAL}"/><stop offset="1" stop-color="#1d6f86"/></radialGradient>
 <clipPath id="clip{uid}"><path d="M60 10 C90 42 94 112 82 180 L38 180 C26 112 30 42 60 10 Z"/></clipPath>
</defs>
<path d="M42 182 Q60 268 78 182 Z" fill="url(#flame{uid})"/>
<path d="M50 182 Q60 228 70 182 Z" fill="#fff6d6"/>
<path d="M40 128 L10 192 Q24 186 44 178 Z" fill="{ROSE}"/>
<path d="M80 128 L110 192 Q96 186 76 178 Z" fill="{ROSE}"/>
<path d="M60 10 C90 42 94 112 82 180 L38 180 C26 112 30 42 60 10 Z" fill="url(#body{uid})"/>
<g clip-path="url(#clip{uid})"><rect x="0" y="0" width="120" height="56" fill="{VIOLET}"/><rect x="0" y="56" width="120" height="6" fill="{GOLD}"/></g>
<circle cx="60" cy="98" r="17" fill="url(#win{uid})" stroke="{GOLD}" stroke-width="5"/>
<circle cx="54" cy="92" r="4" fill="#ffffff" opacity=".8"/>
<rect x="55" y="140" width="10" height="44" rx="5" fill="{ROSE}"/>
<rect x="42" y="176" width="36" height="10" rx="4" fill="#8d84a8"/>
</svg>"""


def badge(n):
    """Step numeral as a glowing gold planet with an orbit ring."""
    return f"""<svg viewBox="0 0 240 240" width="240" height="240" style="overflow:visible" aria-hidden="true">
<circle cx="120" cy="120" r="100" fill="{GOLD}" opacity=".18" style="filter:blur(18px)"/>
<path d="M6 128 A116 34 -18 0 1 232 92" fill="none" stroke="rgba(245,239,226,.5)" stroke-width="2.5"/>
<circle cx="120" cy="120" r="80" fill="url(#planet)"/>
<path d="M120 40a80 80 0 0 0 0 160 80 80 0 0 1 0-160z" fill="{NIGHT}" opacity=".16"/>
<text x="120" y="122" text-anchor="middle" dominant-baseline="central" {NUM_FONT} font-size="112" letter-spacing="-3" fill="#1b1430">{n}</text>
<path d="M232 92 A116 34 -18 0 1 6 128" fill="none" stroke="url(#goldStroke)" stroke-width="5" stroke-linecap="round"/>
<circle cx="226" cy="98" r="7" fill="{GOLD_2}"/>
{sparkle(34, 40, 14, GOLD_2, .9)}
</svg>"""


def tracker(cur):
    """Mission path: steps 1, 2, 3, then the launch. cur = current step (1..3)."""
    xs = [36, 236, 436]
    end = 640
    y = 46
    parts = [
        f'<line x1="{xs[0]}" y1="{y}" x2="{end}" y2="{y}" stroke="rgba(245,239,226,.35)" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>',
        f'<line x1="{xs[0]}" y1="{y}" x2="{xs[cur - 1]}" y2="{y}" stroke="url(#goldStroke)" stroke-width="7" stroke-linecap="round"/>',
    ]
    for k, x in enumerate(xs, start=1):
        if k < cur:
            parts.append(f'<circle cx="{x}" cy="{y}" r="26" fill="{GOLD}"/>'
                         f'<path d="M{x - 11} {y} l8 8 l15 -16" fill="none" stroke="#1b1430" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
        elif k == cur:
            parts.append(f'<circle cx="{x}" cy="{y}" r="44" fill="{GOLD}" opacity=".25"/>'
                         f'<circle cx="{x}" cy="{y}" r="32" fill="url(#planet)" stroke="{GOLD_2}" stroke-width="3"/>'
                         f'<text x="{x}" y="{y + 1}" text-anchor="middle" dominant-baseline="central" {NUM_FONT} font-size="36" fill="#1b1430">{k}</text>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="26" fill="{NIGHT}" stroke="rgba(245,239,226,.5)" stroke-width="3"/>'
                         f'<text x="{x}" y="{y + 1}" text-anchor="middle" dominant-baseline="central" {NUM_FONT} font-size="28" fill="rgba(245,239,226,.8)">{k}</text>')
    svg = f'<svg viewBox="0 0 690 92" width="690" height="92" style="overflow:visible" aria-hidden="true">{"".join(parts)}</svg>'
    # the rocket waits at the launch point
    rk = f'<div class="abs" style="left:{end - 6}px;top:-30px;transform:rotate(40deg)">{rocket(54, "t")}</div>'
    return f'<div class="abs" style="left:0;top:0;width:690px;height:92px">{svg}{rk}</div>'


def step_header(c, n):
    return f"""
<div class="abs" style="left:46px;top:166px">{badge(n)}</div>
<div class="abs kicker" style="left:330px;top:208px">{E(c['step'].format(n=n))}</div>
<div class="abs" style="left:318px;top:268px;width:690px;height:92px">{tracker(n)}</div>
"""


ICONS = {
    'social': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"><rect x="8" y="8" width="40" height="40" rx="12"/><circle cx="28" cy="28" r="9"/><circle cx="39.5" cy="16.5" r="1.8" fill="#fff" stroke="none"/></svg>',
    'price': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"><path d="M30 7 H47 a2 2 0 0 1 2 2 V26 L27 48 a3 3 0 0 1 -4 0 L8 33 a3 3 0 0 1 0 -4 Z"/><circle cx="39" cy="17" r="3.5" fill="#fff" stroke="none"/></svg>',
    'clock': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="28" cy="28" r="20"/><path d="M28 16 V28 L36 33"/></svg>',
    'logo': f'<svg viewBox="0 0 56 56">{sparkle(28, 28, 22, "#fff", 1)}{sparkle(46, 10, 6, "#fff", .9)}</svg>',
}


# ---------- slides ----------

def slide1(c, lang):
    el = lang == 'el'
    return f"""
<div class="abs" style="left:190px;top:130px;width:700px;height:560px;border-radius:50%;
  background:radial-gradient(closest-side, rgba(248,223,142,.55), rgba(232,188,76,.22) 45%, rgba(132,82,210,0) 100%);filter:blur(10px)"></div>
<div class="abs" style="left:325px;top:190px;filter:drop-shadow(0 0 26px rgba(232,188,76,.65))">{logo(430, 'night', orbit_angle=-6)}</div>
<div class="abs kicker" style="left:72px;top:664px">{E(c['cover_kicker'])}</div>
<div class="abs hl fit" data-fit style="left:36px;top:678px;width:1008px;height:calc(400px + 72px);padding:36px;font-size:{84 if el else 96}px">
  {E(c['cover_h1'])}<br><span class="g glow">{E(c['cover_h2'])}</span>
</div>
<div class="abs" style="left:72px;top:1142px"><span class="more">{E(c['cover_more'])} <b>&rarr;</b></span></div>
"""


def slide2(c, lang):
    el = lang == 'el'
    colours = [(ROSE, VIOLET, 'social'), (TEAL, '#1f8f9e', 'price'), (SKYBLUE, VIOLET, 'clock'), (VIOLET, ROSE, 'logo')]
    cards = ''
    for k, (item, (c1, c2, ic)) in enumerate(zip(c['s1_items'], colours)):
        x = 72 + (k % 2) * 484
        y = 770 + (k // 2) * 236
        cards += f"""<div class="tint" style="--c:{c1};left:{x}px;top:{y}px;width:452px;height:212px;display:flex;align-items:center;gap:26px;padding:0 30px">
  <div class="ico" style="--c:{c1};--c2:{c2}">{ICONS[ic]}</div>
  <div class="fit" data-fit style="width:270px;height:150px;display:flex;align-items:center;font-weight:700;font-size:{36 if el else 38}px;line-height:1.18;color:var(--cream)"><span>{E(item)}</span></div>
</div>"""
    return f"""{step_header(c, 1)}
<div class="abs hl fit" data-fit style="left:36px;top:384px;width:1008px;height:calc(240px + 72px);padding:36px;font-size:{84 if el else 100}px">{E(c['s1_h'])}</div>
<div class="abs" style="left:72px;top:690px;font-size:40px;font-weight:600;color:var(--cream);opacity:.85">{E(c['s1_lead'])}</div>
{cards}
"""


def browser_mock(stamp, top):
    tiles = ''
    for col in (TEAL, SKYBLUE, ROSE):
        tiles += f"""<div style="flex:1;min-height:0;border-radius:18px;background:linear-gradient(160deg, color-mix(in srgb, {col} 55%, transparent), color-mix(in srgb, {col} 18%, transparent));
  border:1.5px solid color-mix(in srgb, {col} 70%, transparent);padding:0 18px;display:flex;align-items:center;gap:16px">
  <div style="width:48px;height:48px;flex:none;border-radius:50%;background:{col}"></div>
  <div style="flex:1;display:flex;flex-direction:column;gap:10px"><div style="height:12px;width:90%;border-radius:6px;background:rgba(255,255,255,.75)"></div>
  <div style="height:12px;width:60%;border-radius:6px;background:rgba(255,255,255,.45)"></div></div></div>"""
    h = 1212 - top
    return f"""
<div class="abs" style="left:96px;top:{top}px;width:888px;height:{h}px;transform:rotate(-2deg);border-radius:30px;overflow:hidden;
  background:#16122b;border:2px solid rgba(245,239,226,.22);box-shadow:0 40px 90px -30px rgba(132,82,210,.9)">
  <div style="height:56px;display:flex;align-items:center;gap:12px;padding:0 24px;background:rgba(255,255,255,.07)">
    <i style="width:16px;height:16px;border-radius:50%;background:{ROSE}"></i><i style="width:16px;height:16px;border-radius:50%;background:{GOLD}"></i><i style="width:16px;height:16px;border-radius:50%;background:{TEAL}"></i>
    <div style="margin-left:18px;height:28px;width:420px;border-radius:14px;background:rgba(255,255,255,.12)"></div>
  </div>
  <div style="padding:20px 24px 24px;display:flex;flex-direction:column;gap:18px;height:{h - 60}px">
    <div style="flex:1.5;min-height:0;border-radius:20px;padding:26px 30px;background:linear-gradient(120deg, {VIOLET}, {ROSE} 70%, #ffb38a);display:flex;flex-direction:column;gap:14px">
      <div style="height:22px;width:58%;border-radius:11px;background:rgba(255,255,255,.95)"></div>
      <div style="height:16px;width:40%;border-radius:8px;background:rgba(255,255,255,.65)"></div>
      <div style="margin-top:6px;height:36px;width:160px;border-radius:18px;background:linear-gradient(180deg,{GOLD_2},{GOLD})"></div>
    </div>
    <div style="display:flex;gap:18px;flex:1;min-height:0">{tiles}</div>
  </div>
</div>
<div class="abs" style="right:84px;top:{top - 44}px;transform:rotate(8deg)"><span class="btn" style="font-family:Syne,sans-serif;font-weight:800;font-size:34px;padding:16px 30px">&#10022; {E(stamp)}</span></div>
<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">{sparkle(76, top - 30, 20, GOLD_2, .95)}{sparkle(1012, 1196, 14, GOLD_2, .85)}</svg>
"""


def slide3(c, lang):
    el = lang == 'el'
    return f"""{step_header(c, 2)}
<div class="abs hl fit" data-fit style="left:36px;top:384px;width:1008px;height:calc({360 if el else 320}px + 72px);padding:36px;font-size:{76 if el else 96}px">
  {E(c['s2_h'])}<br><span class="g glow" style="font-size:1.12em">{E(c['s2_gold'])}</span>
</div>
{browser_mock(c['s2_stamp'], 868 if el else 830)}
"""


def phone_mock():
    return f"""
<div class="abs" style="left:96px;top:690px;width:300px;height:540px;transform:rotate(-7deg);border-radius:48px;padding:14px;
  background:linear-gradient(160deg,#2a2448,#120f22);border:2px solid rgba(245,239,226,.3);box-shadow:0 40px 80px -30px rgba(91,140,255,.9)">
  <div style="width:100%;height:100%;border-radius:36px;overflow:hidden;background:#17132c;position:relative">
    <div style="position:absolute;left:50%;top:12px;transform:translateX(-50%);width:90px;height:24px;border-radius:12px;background:#0b0916"></div>
    <div style="height:230px;padding:60px 22px 0;background:linear-gradient(150deg,{SKYBLUE},{VIOLET} 60%,{ROSE});display:flex;flex-direction:column;gap:12px">
      <div style="height:18px;width:80%;border-radius:9px;background:rgba(255,255,255,.95)"></div>
      <div style="height:18px;width:60%;border-radius:9px;background:rgba(255,255,255,.95)"></div>
      <div style="height:12px;width:70%;border-radius:6px;background:rgba(255,255,255,.6)"></div>
      <div style="margin-top:8px;height:38px;width:130px;border-radius:19px;background:linear-gradient(180deg,{GOLD_2},{GOLD})"></div>
    </div>
    <div style="padding:18px;display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div style="height:96px;border-radius:16px;background:color-mix(in srgb,{TEAL} 45%,transparent)"></div>
      <div style="height:96px;border-radius:16px;background:color-mix(in srgb,{ROSE} 45%,transparent)"></div>
      <div style="height:96px;border-radius:16px;background:color-mix(in srgb,{GOLD} 40%,transparent)"></div>
      <div style="height:96px;border-radius:16px;background:color-mix(in srgb,{SKYBLUE} 45%,transparent)"></div>
    </div>
  </div>
</div>
<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">{sparkle(410, 690, 18, GOLD_2, .95)}{sparkle(70, 1010, 12, '#ffffff', .8)}</svg>
"""


def answer_card(q, a, colour, qcolour, top, lang, extra=''):
    el = lang == 'el'
    qs, as_ = (40, 44) if el else (44, 50)
    return f"""<div class="tint" style="--c:{colour};left:450px;top:{top}px;width:558px;height:250px;padding:0 36px;display:flex;flex-direction:column;justify-content:center;gap:12px">
  <div class="fit" data-fit style="width:400px;height:{int(qs * 1.25)}px;font-family:Syne,sans-serif;font-weight:800;font-size:{qs}px;line-height:1.2;color:{qcolour};letter-spacing:-.02em;white-space:nowrap">{E(q)}</div>
  <div class="fit" data-fit style="width:486px;max-height:{int(as_ * 1.18 * 2) + 4}px;font-weight:700;font-size:{as_}px;line-height:1.18;color:var(--cream)">{E(a)}</div>
  {extra}
</div>"""


def slide4(c, lang):
    el = lang == 'el'
    rk = f'<div class="abs" style="right:30px;top:24px;transform:rotate(30deg)">{rocket(40, "c")}</div>'
    return f"""{step_header(c, 3)}
<div class="abs hl fit" data-fit style="left:36px;top:384px;width:1008px;height:calc(240px + 72px);padding:36px;font-size:{84 if el else 100}px">{E(c['s3_h'])}</div>
{phone_mock()}
{answer_card(c['s3_love_q'], c['s3_love_a'], GOLD, GOLD, 700, lang, rk)}
{answer_card(c['s3_no_q'], c['s3_no_a'], TEAL, TEAL, 974, lang)}
"""


def slide5(c, lang):
    el = lang == 'el'
    count = f"""
<div class="abs num" style="left:72px;top:220px;display:flex;align-items:baseline;gap:40px">
  <span style="font-size:130px;color:{TEAL}">3</span>
  <span style="font-size:180px;color:{ROSE}">2</span>
  <span class="glow" style="font-size:250px;color:var(--gold)">1</span>
</div>"""
    smoke = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="{o}"/>' for x, y, r, col, o in [
        (640, 610, 70, ROSE, .55), (760, 630, 86, VIOLET, .6), (880, 600, 66, TEAL, .5), (560, 625, 46, GOLD, .45), (960, 630, 50, SKYBLUE, .5)])
    trail = f"""<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs><linearGradient id="trail" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{ROSE}" stop-opacity="0"/><stop offset=".5" stop-color="{ROSE}" stop-opacity=".7"/><stop offset="1" stop-color="{GOLD_2}"/></linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="14"/></filter></defs>
  <g filter="url(#soft)">{smoke}</g>
  <path d="M760 610 C760 530 770 450 790 390" stroke="url(#trail)" stroke-width="40" stroke-linecap="round" fill="none" opacity=".85"/>
  {sparkle(980, 230, 18, GOLD_2, .95)}{sparkle(560, 190, 12, '#ffffff', .8)}{sparkle(1010, 490, 10, GOLD_2, .8)}
</svg>"""
    rk = f'<div class="abs" style="left:722px;top:120px;transform:rotate(12deg);filter:drop-shadow(0 0 30px rgba(232,188,76,.5))">{rocket(150, "big")}</div>'
    return f"""{trail}{count}{rk}
<div class="abs hl fit" data-fit style="left:36px;top:594px;width:1008px;height:calc(250px + 72px);padding:36px;font-size:{104 if el else 118}px">{E(c['cta_h'])}</div>
<div class="abs fit" data-fit style="left:72px;top:896px;width:936px;height:112px;font-size:{36 if el else 38}px;font-weight:500;line-height:1.38;color:var(--cream);text-shadow:0 2px 14px rgba(13,11,26,.6)">{'<br>'.join(E(s) for s in c['cta_lead'])}</div>
<div class="abs" style="left:72px;top:1040px"><span class="btn big">{E(c['cta_btn'])} <span style="font-size:1.05em">&rarr;</span></span></div>
<div class="abs" style="left:76px;top:1170px;font-size:34px;font-weight:600;color:var(--cream)"><span style="opacity:.75">{E(c['cta_or'])}</span> <b style="color:var(--gold)">webbiespirit.com</b></div>
"""


SLIDES = [slide1, slide2, slide3, slide4, slide5]


def build(lang):
    c = COPY[lang]
    outs = []
    for i, fn in enumerate(SLIDES):
        n = i + 1
        page = Slide(lang=lang, sky='night', nebula=NEBULA[n], seed=100 + n, dots=(i, N), extra_css=EXTRA_CSS).page(fn(c, lang) + sparks(n))
        outs.append(render(page, HERE / 'out' / lang / f'1-how-it-works-{n}.png'))
    return outs


if __name__ == '__main__':
    for lang in ('en', 'el'):
        for p in build(lang):
            print(p)
