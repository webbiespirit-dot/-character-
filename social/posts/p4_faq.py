"""Post 4, "3 questions shop owners ask us": a 4-slide carousel on the ivory day sky, told as a bright group chat.

Run:  cd social/posts && python3 p4_faq.py
Out:  out/en/4-questions-<n>.png and out/el/4-questions-<n>.png
"""
import glob
import os
from pathlib import Path

# The full Chromium in new-headless mode paints only part of the 1350px viewport (the carousel dots and
# @handle come out blank). The headless shell honours --window-size exactly; kit reads CHROME at import time.
if 'CHROME' not in os.environ:
    _shell = sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell'))
    if _shell:
        os.environ['CHROME'] = _shell[-1]

from kit import (Slide, render, brand_mark, sparkle, E,  # noqa: E402
                 GOLD, GOLD_2, GOLD_DEEP, VIOLET, ROSE, TEAL, SKYBLUE, INK, NIGHT)

HERE = Path(__file__).resolve().parent
N = 4

COPY = {
    'en': {
        'q': ['Do I own my website?', 'What do I need to send you?', 'Can I see it before I pay?'],
        'q_size': [88, 88, 88],
        'cover_n': '3',
        'cover_w': 'questions',
        'cover_h': 'shop owners ask us.',
        'swipe': 'Swipe for the answers',
        'kicker': 'Question {n} of 3',
        'a1_open': 'Yes.',
        'a1': 'The domain is registered in your name and the site is yours.',
        'a1_url': 'yourshop.com',
        'a1_tag': 'In your name',
        'a2_items': ['Your Instagram or Facebook page', 'Your price list', 'Opening hours', 'Your logo, if you have one'],
        'a2_end': "That's enough for the <span class=\"hi\">free preview.</span>",
        'a3_open': 'Always.',
        'a3': 'We build the preview first, you look at it on your own phone, and you pay only if you want it live.',
        'cta': 'DM us PREVIEW',
        'cta_or': 'or visit <b>webbiespirit.com</b>',
    },
    'el': {
        'q': ['Η ιστοσελίδα θα είναι δική μου;', 'Τι πρέπει να σας στείλω;', 'Μπορώ να τη δω πριν πληρώσω;'],
        # Greek words run longer in Syne, so the questions sit a size down to stay at three lines.
        'q_size': [72, 76, 72],
        'cover_n': '3',
        'cover_w': 'ερωτήσεις',
        'cover_h': 'που μας κάνουν οι ιδιοκτήτες μαγαζιών.',
        'swipe': 'Σύρετε για τις απαντήσεις',
        'kicker': 'Ερώτηση {n} από 3',
        'a1_open': 'Ναι.',
        'a1': 'Το domain κατοχυρώνεται στο όνομά σας και η ιστοσελίδα είναι δική σας.',
        'a1_url': 'tomagazisas.com',
        'a1_tag': 'Στο όνομά σας',
        'a2_items': ['Τη σελίδα σας στο Instagram ή στο Facebook', 'Τον τιμοκατάλογό σας', 'Το ωράριο λειτουργίας', 'Το λογότυπό σας, αν έχετε'],
        'a2_end': 'Αυτά αρκούν για τη <span class="hi">δωρεάν μακέτα.</span>',
        'a3_open': 'Πάντα.',
        'a3': 'Φτιάχνουμε πρώτα τη μακέτα, τη βλέπετε στο δικό σας κινητό και πληρώνετε μόνο αν θέλετε να βγει στον αέρα.',
        'cta': 'Στείλτε μας «PREVIEW»',
        'cta_or': 'ή μπείτε στο <b>webbiespirit.com</b>',
    },
}

# Each question gets its own bubble colour, and the cover previews all three: (top, bottom, text colour).
BUBBLE = [
    ('#a06cf0', '#6b3cc6', '#ffffff'),   # violet, white text
    ('#7ef0df', '#2fc4b2', INK),         # teal, ink text
    ('#ffa3cb', '#ff6fae', INK),         # rose, ink text
]

# A flight through the daytime sky: every slide gets its own clouds.
NEBULA = {
    1: [(-220, 60, 720, 560, VIOLET, .36), (560, 260, 680, 600, TEAL, .40), (-200, 860, 720, 560, ROSE, .40), (600, 980, 620, 480, GOLD, .42)],
    2: [(560, -200, 720, 580, VIOLET, .36), (-280, 520, 660, 620, SKYBLUE, .32), (600, 880, 660, 560, ROSE, .36), (-120, -160, 420, 360, GOLD, .34)],
    3: [(-240, -140, 720, 560, TEAL, .40), (580, 420, 680, 620, GOLD, .36), (-220, 920, 720, 540, VIOLET, .34), (760, -100, 420, 380, ROSE, .30)],
    4: [(600, -180, 660, 560, ROSE, .40), (-280, 380, 700, 640, TEAL, .34), (480, 900, 720, 560, VIOLET, .36), (-140, 1080, 520, 400, GOLD, .38)],
}

# The kit scatters seven random sparkles that can land on text; they are hidden and placed by hand instead.
SPARKS = {
    1: [(960, 190, 20, GOLD, .95), (1010, 440, 11, VIOLET, .7), (1030, 560, 12, ROSE, .8), (42, 520, 12, GOLD, .85),
        (1030, 1066, 14, GOLD, .9), (300, 1220, 10, TEAL, .8)],
    2: [(1020, 1000, 16, GOLD, .9), (60, 1120, 12, ROSE, .8), (330, 1215, 10, VIOLET, .7)],
    3: [(1030, 260, 12, GOLD, .9), (40, 1160, 14, GOLD, .85), (620, 1215, 9, TEAL, .8)],
    4: [(1028, 300, 12, GOLD, .9), (46, 930, 14, GOLD, .9), (1032, 1040, 10, ROSE, .8)],
}

EXTRA_CSS = f"""
.sky svg.stars path {{ display: none; }}
.abs {{ position: absolute; }}
.chat {{ position: absolute; left: 72px; right: 72px; top: 178px; bottom: 112px; display: flex; flex-direction: column;
  justify-content: center; gap: 34px; }}
.row {{ display: flex; align-items: flex-end; gap: 22px; }}
.row.me {{ justify-content: flex-end; }}
.av {{ width: 96px; height: 96px; border-radius: 50%; flex: none; display: grid; place-items: center; }}
.av.shop {{ background: linear-gradient(145deg, {GOLD_2}, {GOLD} 55%, #e0a43a); box-shadow: 0 12px 26px -12px rgba(166,125,38,.9); }}
.av.shop svg {{ width: 58px; height: 58px; }}
.av.ws {{ background: radial-gradient(circle at 50% 35%, #2b2353, {NIGHT} 75%); box-shadow: 0 12px 26px -12px rgba(23,19,42,.8); }}
.av.ws svg {{ width: 66px; height: 66px; overflow: visible; }}
.av.ghost {{ visibility: hidden; }}
.bw {{ position: relative; filter: drop-shadow(0 22px 26px rgba(70,40,120,.22)); }}
.bubble {{ position: relative; border-radius: 48px; padding: 38px 48px 42px; }}
.bubble.them {{ border-bottom-left-radius: 14px; }}
.bubble.mine {{ border-bottom-right-radius: 14px; background: #ffffff; color: {INK}; }}
.tail {{ position: absolute; bottom: 0; width: 46px; height: 44px; }}
.tail.l {{ left: -24px; }}
.tail.r {{ right: -24px; }}
.qtext {{ font-family: Syne, sans-serif; font-weight: 800; letter-spacing: -.03em; line-height: 1.04; text-wrap: balance; }}
.atext {{ font-size: 42px; line-height: 1.36; font-weight: 500; text-wrap: pretty; }}
.open {{ display: block; font-family: Syne, sans-serif; font-weight: 800; font-size: 76px; letter-spacing: -.03em; line-height: 1; margin-bottom: 18px; }}
.hi {{ --a: 58%; --b: 88%; background: linear-gradient(transparent var(--a), rgba(232,188,76,.62) var(--a), rgba(232,188,76,.62) var(--b), transparent var(--b));
  padding: 0 .06em; border-radius: 6px; white-space: nowrap; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
.open .hi {{ --a: 48%; --b: 82%; }}
.kick {{ position: absolute; right: 72px; top: 70px; display: inline-flex; align-items: center; gap: 14px; height: 60px;
  padding: 0 26px 0 8px; border-radius: 999px; background: rgba(255,255,255,.86); font-weight: 700; font-size: 27px; color: {INK};
  box-shadow: 0 10px 24px -14px rgba(70,40,120,.5); }}
.kick b {{ width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; font-size: 26px;
  background: linear-gradient(145deg, {GOLD_2}, {GOLD}); color: #15100a; }}
.swipe {{ display: inline-flex; align-items: center; gap: 16px; font-weight: 700; font-size: 32px; color: {INK};
  padding: 18px 30px; border-radius: 999px; background: rgba(255,255,255,.86); box-shadow: 0 12px 30px -16px rgba(70,40,120,.55); }}
.swipe b {{ color: {GOLD_DEEP}; font-size: 38px; line-height: 1; }}
.items {{ display: flex; flex-direction: column; gap: 18px; }}
.it {{ display: flex; align-items: center; gap: 24px; font-size: 38px; font-weight: 600; line-height: 1.2; }}
.it span:last-child {{ text-wrap: balance; }}
.ico {{ width: 74px; height: 74px; border-radius: 22px; flex: none; display: grid; place-items: center;
  background: linear-gradient(145deg, var(--c), var(--c2)); box-shadow: 0 10px 22px -12px var(--c2); }}
.ico svg {{ width: 44px; height: 44px; }}
.rule {{ height: 2px; background: rgba(23,19,42,.1); margin: 30px 0 26px; }}
.end {{ font-size: 40px; font-weight: 700; line-height: 1.3; }}
.url {{ display: flex; align-items: center; gap: 18px; padding: 20px 28px; border-radius: 999px; background: #f2edfb;
  font-size: 38px; font-weight: 700; color: {INK}; }}
.url svg {{ width: 38px; height: 38px; flex: none; }}
.tag {{ display: inline-flex; align-items: center; gap: 12px; margin-top: 22px; padding: 14px 26px; border-radius: 999px;
  background: linear-gradient(180deg, {GOLD_2}, {GOLD}); color: #15100a; font-weight: 700; font-size: 32px; }}
.tag svg {{ width: 34px; height: 34px; }}
.ctarow {{ display: flex; flex-direction: column; align-items: center; gap: 22px; margin-top: 8px; }}
.btn.big {{ font-size: 44px; padding: 30px 58px; }}
.ctaor {{ font-size: 32px; color: var(--muted); font-weight: 500; }}
.ctaor b {{ color: {INK}; font-weight: 700; }}
.coverq {{ display: flex; align-items: center; gap: 22px; padding: 26px 40px 28px 26px; white-space: nowrap; }}
.coverq .n {{ width: 64px; height: 64px; border-radius: 50%; flex: none; display: grid; place-items: center; font-weight: 700;
  font-size: 34px; background: linear-gradient(145deg, {GOLD_2}, {GOLD}); color: #15100a; box-shadow: 0 6px 14px -6px rgba(0,0,0,.35); }}
.coverq .t {{ font-weight: 700; font-size: 40px; line-height: 1.1; }}
.coverh {{ font-family: Syne, sans-serif; font-weight: 800; font-size: 112px; letter-spacing: -.04em; line-height: 1.0; color: {INK};
  text-wrap: balance; }}
.coverh .g {{ background: linear-gradient(180deg, #e2ad3c, #946f1b); -webkit-background-clip: text; background-clip: text; color: transparent;
  white-space: nowrap; }}
"""


# ---------- drawings ----------

def tail(side, color):
    """Chat-bubble tail at the bottom corner, curving out of the bubble's side."""
    if side == 'l':
        d = 'M24 0 C24 22 15 36 0 44 L46 44 L46 0 Z'
    else:
        d = 'M22 0 C22 22 31 36 46 44 L0 44 L0 0 Z'
    return f'<svg class="tail {side}" viewBox="0 0 46 44" aria-hidden="true"><path d="{d}" fill="{color}"/></svg>'


SHOP = ('<svg viewBox="0 0 56 56" fill="none" stroke="#15100a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M8 22 L12 10 H44 L48 22"/><path d="M8 22 a5 5 0 0 0 10 0 a5 5 0 0 0 10 0 a5 5 0 0 0 10 0 a5 5 0 0 0 10 0"/>'
        '<path d="M11 28 V47 H45 V28"/><path d="M23 47 V36 H33 V47"/></svg>')


def av_shop():
    return f'<div class="av shop">{SHOP}</div>'


def av_ws(ghost=False):
    return f'<div class="av ws{" ghost" if ghost else ""}">{brand_mark()}</div>'


def grad(k):
    top, bot, _ = BUBBLE[k]
    return f'linear-gradient(180deg,{top},{bot} calc(100% - 46px),{bot})'


def q_bubble(k, text, size=84, width=None):
    top, bot, fg = BUBBLE[k]
    w = f'width:{width}px;' if width else ''
    return (f'<div class="bw" style="flex:1;min-width:0;{w}"><div class="bubble them" style="background:{grad(k)};color:{fg}">'
            f'<div class="qtext" style="font-size:{size}px">{E(text)}</div></div>{tail("l", bot)}</div>')


def a_bubble(inner, width=None, tailed=True):
    w = f'width:{width}px;' if width else ''
    return f'<div class="bw" style="{w}"><div class="bubble mine">{inner}</div>{tail("r", "#ffffff") if tailed else ""}</div>'


def sparks(n):
    return ('<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350" viewBox="0 0 1080 1350">'
            + ''.join(sparkle(x, y, sz, col, op) for x, y, sz, col, op in SPARKS[n]) + '</svg>')


def planet(cx, cy, r, ring, tilt=-18, moon=None):
    """A little gold planet with a coloured ring (back half behind, front half in front), like the site's avatars."""
    rx, ry = r * 1.85, r * .52
    arc = lambda sweep, op, w: (f'<path d="M{cx - rx} {cy} A{rx} {ry} 0 0 {sweep} {cx + rx} {cy}" fill="none" stroke="{ring}" '
                                f'stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>')
    m = ''
    if moon:
        mx, my, mr, mc = moon
        m = f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="{mc}"/>'
    return (f'<g transform="rotate({tilt} {cx} {cy})">{arc(1, .55, r * .14)}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#planet)"/>'
            f'<path d="M{cx} {cy - r}a{r} {r} 0 0 0 0 {2 * r} {r} {r} 0 0 1 0 {-2 * r}z" fill="{NIGHT}" opacity=".16"/>'
            f'{arc(0, 1, r * .16)}</g>{m}')


# Slides 2 to 4: a dotted gold orbit sweeps behind the chat (the cover's comet trail carried on), with a planet in a free corner.
ORBITS = {
    2: dict(orbit=(560, 1010, 620, 200, -12), planet=(214, 1078, 44, VIOLET, -16, (330, 1010, 9, TEAL))),
    3: dict(orbit=(540, 900, 600, 200, 8), planet=(985, 822, 30, ROSE, -20, (940, 724, 7, VIOLET))),
    4: dict(orbit=(540, 1090, 680, 140, -5), planet=(122, 1066, 30, TEAL, -18, (214, 1152, 7, ROSE))),
}


def orbit_bg(n):
    ox, oy, orx, ory, rot = ORBITS[n]['orbit']
    return (f'<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
            f'<ellipse cx="{ox}" cy="{oy}" rx="{orx}" ry="{ory}" transform="rotate({rot} {ox} {oy})" fill="none" stroke="{GOLD}" '
            f'stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round" opacity=".75"/></svg>')


def planet_fg(n):
    cx, cy, r, ring, tilt, moon = ORBITS[n]['planet']
    return (f'<svg class="abs" style="left:0;top:0;pointer-events:none" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
            f'{planet(cx, cy, r, ring, tilt, moon)}</svg>')


ICONS = {
    'social': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"><rect x="8" y="8" width="40" height="40" rx="12"/><circle cx="28" cy="28" r="9"/><circle cx="39.5" cy="16.5" r="1.8" fill="#fff" stroke="none"/></svg>',
    'price': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"><path d="M30 7 H47 a2 2 0 0 1 2 2 V26 L27 48 a3 3 0 0 1 -4 0 L8 33 a3 3 0 0 1 0 -4 Z"/><circle cx="39" cy="17" r="3.5" fill="#fff" stroke="none"/></svg>',
    'clock': '<svg viewBox="0 0 56 56" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="28" cy="28" r="20"/><path d="M28 16 V28 L36 33"/></svg>',
    'logo': f'<svg viewBox="0 0 56 56">{sparkle(28, 28, 22, "#fff", 1)}{sparkle(46, 10, 6, "#fff", .9)}</svg>',
}
ICON_COL = [('social', ROSE, VIOLET), ('price', TEAL, '#1fa596'), ('clock', SKYBLUE, VIOLET), ('logo', VIOLET, ROSE)]

LOCK = (f'<svg viewBox="0 0 40 40" fill="none" stroke="{VIOLET}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="7" y="17" width="26" height="18" rx="5"/><path d="M13 17 V12 a7 7 0 0 1 14 0 V17"/></svg>')
KEY = ('<svg viewBox="0 0 40 40" fill="none" stroke="#15100a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
       '<circle cx="13" cy="20" r="7"/><path d="M20 20 H35 M30 20 V26 M35 20 V25"/></svg>')


def kicker(c, n):
    return f'<div class="kick"><b>?</b>{E(c["kicker"].format(n=n))}</div>'


# ---------- slides ----------

def cover(lang, c):
    pos = [  # side, top, rotation
        ('left:72px', 566, -3),
        ('right:72px', 748, 2.5),
        ('left:96px', 930, -2),
    ]
    bubbles = ''
    for k, (side, top, rot) in enumerate(pos):
        bg_top, bg_bot, fg = BUBBLE[k]
        tl = 'l' if 'left' in side else 'r'
        radius = 'border-bottom-left-radius:14px' if tl == 'l' else 'border-bottom-right-radius:14px'
        bubbles += (f'<div class="abs" style="{side};top:{top}px;transform:rotate({rot}deg)"><div class="bw">'
                    f'<div class="bubble coverq" style="background:{grad(k)};color:{fg};{radius}">'
                    f'<span class="n">{k + 1}</span><span class="t">{E(c["q"][k])}</span></div>{tail(tl, bg_bot)}</div></div>')
    # a dotted comet path weaving behind the three bubbles, ending in a little comet
    comet = f"""<svg class="abs" style="left:0;top:500px" width="1080" height="700" viewBox="0 0 1080 700" aria-hidden="true">
<path d="M40 40 C300 -10 700 20 980 120 C1110 170 980 240 700 300 C420 360 60 330 90 470 C110 580 220 664 396 665" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round" opacity=".85"/>
<circle cx="410" cy="665" r="10" fill="{GOLD}"/>{sparkle(410, 665, 24, GOLD_2, .95)}
</svg>"""
    head = (f'<div class="abs fit coverh" data-fit style="left:72px;top:184px;width:936px;height:340px">'
            f'<span class="g">{E(c["cover_n"])}&nbsp;{E(c["cover_w"])}</span> {E(c["cover_h"])}</div>'
            f'<div class="abs" style="right:72px;top:1128px"><span class="swipe">{E(c["swipe"])} <b>&rarr;</b></span></div>')
    return comet + bubbles + head + sparks(1)


def q_slide(lang, c, n):
    """n = 1..3 (question number); slide index = n + 1."""
    k = n - 1
    q = c['q'][k]
    if n == 1:
        ans = (f'<span class="open"><span class="hi">{E(c["a1_open"])}</span></span>'
               f'<div class="atext">{E(c["a1"])}</div>')
        card = (f'<div class="url">{LOCK}<span>{E(c["a1_url"])}</span></div>'
                f'<span class="tag">{KEY}{E(c["a1_tag"])}</span>')
        extra = f'<div class="row me">{a_bubble(card)}{av_ws()}</div>'
        body = (f'<div class="row">{av_shop()}{q_bubble(k, q, c['q_size'][k])}</div>'
                f'<div class="row me">{a_bubble(ans, 740, tailed=False)}{av_ws(ghost=True)}</div>'
                + extra)
    elif n == 2:
        items = ''.join(f'<div class="it"><span class="ico" style="--c:{c1};--c2:{c2}">{ICONS[ic]}</span><span>{E(t)}</span></div>'
                        for (ic, c1, c2), t in zip(ICON_COL, c['a2_items']))
        ans = f'<div class="items">{items}</div><div class="rule"></div><div class="end">{c["a2_end"]}</div>'
        body = (f'<div class="row">{av_shop()}{q_bubble(k, q, c['q_size'][k])}</div>'
                f'<div class="row me">{a_bubble(ans, 790)}{av_ws()}</div>')
    else:
        ans = (f'<span class="open"><span class="hi">{E(c["a3_open"])}</span></span>'
               f'<div class="atext">{E(c["a3"])}</div>')
        body = (f'<div class="row">{av_shop()}{q_bubble(k, q, c['q_size'][k])}</div>'
                f'<div class="row me">{a_bubble(ans, 790)}{av_ws()}</div>'
                f'<div class="ctarow"><span class="btn big">{E(c["cta"])}</span><span class="ctaor">{c["cta_or"]}</span></div>')
    return orbit_bg(n + 1) + kicker(c, n) + f'<div class="chat">{body}</div>' + planet_fg(n + 1) + sparks(n + 1)


def build(lang):
    c = COPY[lang]
    out = []
    for i in range(1, N + 1):
        s = Slide(lang=lang, sky='day', seed=40 + i, nebula=NEBULA[i], dots=(i - 1, N), extra_css=EXTRA_CSS)
        body = cover(lang, c) if i == 1 else q_slide(lang, c, i - 1)
        png = HERE / 'out' / lang / f'4-questions-{i}.png'
        render(s.page(body), png)
        out.append(png)
    return out


def main():
    for lang in ('en', 'el'):
        for p in build(lang):
            print(p)


if __name__ == '__main__':
    main()
