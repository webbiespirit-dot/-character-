"""webbiespirit post kit: the site's own cosmic brand, for 1080x1350 Instagram slides.

Taken from webbiespirit.com: a living sky (nebula + sparkles), night #0d0b1a or ivory #f6f3ec,
gold as the only action colour, Syne for display, Instrument Sans for text (Manrope covers Greek),
and the logo, a gold W tracing a comet path through orbit rings around a globe.

Use:  from kit import Slide, render
      html = Slide(lang='en', sky='night', seed=3).page(body_html)
      render(html, 'social/posts/out/en/name.png')
"""
import glob
import html as _html
import os
import random
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE / 'fonts'
# The full Chromium in new-headless mode paints only a 1080x1263 viewport inside the 1350 screenshot
# (the bottom 87px, with the carousel dots and @handle, come out blank). The headless shell honours
# --window-size exactly, so prefer it when present.
_SHELLS = sorted(glob.glob('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell'))
CHROME = os.environ.get('CHROME') or (_SHELLS[-1] if _SHELLS else '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
W, H = 1080, 1350
E = _html.escape

# Brand colours. Gold is the action colour; the nebula colours only ever live in the sky.
NIGHT = '#0d0b1a'
NIGHT_2 = '#15122a'
NIGHT_3 = '#1d1936'
IVORY = '#f6f3ec'
INK = '#17132a'
CREAM = '#f5efe2'
GOLD = '#e8bc4c'
GOLD_2 = '#f8df8e'
GOLD_DEEP = '#a67d26'
GOLD_TEXT = '#946f1b'      # gold that reads on ivory
VIOLET = '#8452d2'         # the logo aura's second colour
ROSE = '#ff6fae'
TEAL = '#38d6c4'
SKYBLUE = '#5b8cff'


def css(sky):
    f = FONTS.as_uri()
    night = sky == 'night'
    fg, muted, line = (CREAM, '#b9b1c9', 'rgba(245,239,226,.14)') if night else (INK, '#5e5876', 'rgba(23,19,42,.12)')
    card = 'rgba(255,255,255,.06)' if night else 'rgba(255,255,255,.78)'
    return f"""
@font-face {{ font-family: Syne; src: url({f}/syne-latin-wght-normal.woff2) format('woff2'); font-weight: 400 800; }}
@font-face {{ font-family: Syne; src: url({f}/syne-latin-ext-wght-normal.woff2) format('woff2'); font-weight: 400 800; unicode-range: U+0100-024F, U+20AC; }}
@font-face {{ font-family: Syne; src: url({f}/syne-greek-wght-normal.woff2) format('woff2'); font-weight: 400 800; unicode-range: U+0370-03FF, U+1F00-1FFF; }}
@font-face {{ font-family: Body; src: url({f}/instrument-sans-latin-wght-normal.woff2) format('woff2'); font-weight: 400 700; }}
@font-face {{ font-family: Body; src: url({f}/instrument-sans-latin-ext-wght-normal.woff2) format('woff2'); font-weight: 400 700; unicode-range: U+0100-024F, U+20AC; }}
""" + ''.join(f"@font-face {{ font-family: Body; src: url({f}/manrope-greek-{w}-normal.woff2) format('woff2'); font-weight: {w}; unicode-range: U+0370-03FF, U+1F00-1FFF; }}\n" for w in (400, 500, 600, 700, 800)) + f"""
:root {{ --bg: {NIGHT if night else IVORY}; --fg: {fg}; --muted: {muted}; --line: {line}; --card: {card};
  --gold: {GOLD}; --gold-2: {GOLD_2}; --gold-deep: {GOLD_DEEP}; --gold-text: {GOLD if night else GOLD_TEXT};
  --violet: {VIOLET}; --rose: {ROSE}; --teal: {TEAL}; --skyblue: {SKYBLUE}; --ink: {INK}; --cream: {CREAM}; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}px; height: {H}px; overflow: hidden; }}
body {{ background: var(--bg); color: var(--fg); font-family: Body, 'Helvetica Neue', Arial, sans-serif; position: relative;
  -webkit-font-smoothing: antialiased; }}
.sky {{ position: absolute; inset: 0; overflow: hidden; z-index: 0; }}
.sky .neb {{ position: absolute; border-radius: 50%; filter: blur(70px); }}
.sky svg.stars {{ position: absolute; inset: 0; }}
.layer {{ position: absolute; inset: 0; z-index: 2; }}
h1, h2, h3, .display {{ font-family: Syne, 'Avenir Next', sans-serif; font-weight: 800; letter-spacing: -.035em; line-height: 1.02; text-wrap: balance; }}
.gold {{ color: var(--gold-text); }}
.muted {{ color: var(--muted); }}
.lead {{ font-size: 40px; line-height: 1.4; color: var(--muted); text-wrap: pretty; }}
.btn {{ display: inline-flex; align-items: center; gap: 14px; background: linear-gradient(180deg, {GOLD_2}, {GOLD} 55%, #d9a93a); color: #15100a;
  font-weight: 700; font-size: 36px; padding: 24px 40px; border-radius: 999px; white-space: nowrap;
  box-shadow: 0 1px 0 rgba(255,255,255,.5) inset, 0 18px 40px -16px rgba(166,125,38,.8); }}
.chip {{ display: inline-flex; align-items: center; gap: 10px; font-weight: 700; font-size: 26px; padding: 10px 22px; border-radius: 999px;
  border: 2px solid var(--line); background: var(--card); color: var(--fg); }}
.card {{ background: var(--card); border: 1.5px solid var(--line); border-radius: 34px; }}
.brand {{ position: absolute; left: 72px; top: 64px; display: flex; align-items: center; gap: 16px; z-index: 5;
  font-family: Syne, sans-serif; font-weight: 700; font-size: 38px; letter-spacing: -.02em; color: var(--fg); }}
.brand svg {{ width: 64px; height: 64px; overflow: visible; filter: drop-shadow(0 0 10px rgba(232,188,76,.55)); }}
.handle {{ position: absolute; right: 72px; bottom: 56px; z-index: 5; font-size: 28px; font-weight: 600; color: var(--muted); }}
.dots {{ position: absolute; left: 72px; bottom: 64px; z-index: 5; display: flex; gap: 12px; }}
.dots i {{ width: 14px; height: 14px; border-radius: 50%; background: var(--fg); opacity: .25; }}
.dots i.on {{ opacity: 1; background: var(--gold); width: 40px; border-radius: 8px; }}
.fit {{ overflow: hidden; }}
"""


DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="goldStroke" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GOLD_2}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_DEEP}"/></linearGradient>
<radialGradient id="core" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6d6"/><stop offset=".35" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_DEEP}" stop-opacity="0"/></radialGradient>
<radialGradient id="planet" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="#fff6d6"/><stop offset=".45" stop-color="{GOLD}"/><stop offset="1" stop-color="#8a6420"/></radialGradient>
</defs></svg>"""


def logo(size=200, sky='night', orbit_angle=0):
    """The webbiespirit mark, fully drawn: gold W comet path, orbit rings, globe with meridians."""
    o = 'rgba(245,239,226,.45)' if sky == 'night' else 'rgba(23,19,42,.4)'
    return f"""<svg viewBox="0 0 200 200" width="{size}" height="{size}" style="overflow:visible" aria-hidden="true">
<g transform="rotate({orbit_angle} 100 100)"><ellipse cx="100" cy="100" rx="92" ry="36" transform="rotate(-22 100 100)" fill="none" stroke="{o}" stroke-width=".9"/></g>
<ellipse cx="100" cy="100" rx="78" ry="30" transform="rotate(28 100 100)" fill="none" stroke="{o}" stroke-width=".9" stroke-dasharray="2 5"/>
<circle cx="100" cy="100" r="60" fill="none" stroke="rgba(232,188,76,.75)" stroke-width="1.1"/>
<circle cx="100" cy="100" r="42" fill="url(#core)" opacity=".5"/>
<g fill="none" stroke="rgba(232,188,76,.75)" stroke-width="1.1" stroke-opacity=".55"><ellipse cx="100" cy="100" rx="60" ry="14"/>
<ellipse cx="100" cy="100" rx="20" ry="60"/><ellipse cx="100" cy="100" rx="42" ry="60"/></g>
<path d="M44 68 C52 92 58 118 66 136 C78 118 88 100 100 84 C112 100 122 118 134 136 C142 118 148 92 156 68" fill="none" stroke="url(#goldStroke)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="156" cy="68" r="5" fill="{GOLD_2}"/><circle cx="44" cy="68" r="3.2" fill="{GOLD}"/><circle cx="100" cy="84" r="2.2" fill="#fff6d6"/>
<circle cx="192" cy="88" r="1.8" fill="{GOLD_2}"/></svg>"""


def brand_mark():
    """Small nav-style mark, as in the site's top bar."""
    return f"""<svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="62" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="5"/>
<ellipse cx="100" cy="100" rx="88" ry="34" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="5" transform="rotate(-22 100 100)"/>
<path d="M40 70 L62 136 L100 82 L138 136 L160 70" fill="none" stroke="url(#goldStroke)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="160" cy="70" r="9" fill="{GOLD_2}"/></svg>"""


def sun_avatar(size=220):
    """Apollo's avatar on the site: a gold sun with rays in a starry disc."""
    rays = 'M69.5 50.0L79.5 50.0M68.0 57.5L73.6 59.8M63.8 63.8L70.9 70.9M57.5 68.0L59.8 73.6M50.0 69.5L50.0 79.5M42.5 68.0L40.2 73.6M36.2 63.8L29.1 70.9M32.0 57.5L26.4 59.8M30.5 50.0L20.5 50.0M32.0 42.5L26.4 40.2M36.2 36.2L29.1 29.1M42.5 32.0L40.2 26.4M50.0 30.5L50.0 20.5M57.5 32.0L59.8 26.4M63.8 36.2L70.9 29.1M68.0 42.5L73.6 40.2'
    return f"""<svg viewBox="0 0 100 100" width="{size}" height="{size}"><defs><radialGradient id="avA" cx=".5" cy=".35" r=".75"><stop offset="0" stop-color="#2b2353"/><stop offset=".6" stop-color="#171233"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient></defs>
<circle cx="50" cy="50" r="50" fill="url(#avA)"/>{_disc_stars(11)}<path d="{rays}" stroke="url(#goldStroke)" stroke-width="2.6" stroke-linecap="round" fill="none"/>
<circle cx="50" cy="50" r="22" fill="url(#core)" opacity=".85"/><circle cx="50" cy="50" r="12.5" fill="{GOLD_2}"/><circle cx="50" cy="50" r="12.5" fill="none" stroke="#fff6d6" stroke-width="1" opacity=".7"/></svg>"""


def planet_avatar(size=220):
    """Palios's avatar on the site: a gold ringed planet in a starry disc."""
    return f"""<svg viewBox="0 0 100 100" width="{size}" height="{size}"><defs><radialGradient id="avP" cx=".5" cy=".35" r=".75"><stop offset="0" stop-color="#1e2a52"/><stop offset=".6" stop-color="#141935"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient></defs>
<circle cx="50" cy="50" r="50" fill="url(#avP)"/>{_disc_stars(23)}
<path d="M8 50A42 13.5 0 0 1 92 50" fill="none" stroke="url(#goldStroke)" stroke-width="2.4" opacity=".55" stroke-linecap="round"/>
<circle cx="50" cy="48" r="21" fill="url(#planet)"/><path d="M50 27a21 21 0 0 0 0 42 21 21 0 0 1 0-42z" fill="{NIGHT}" opacity=".22"/>
<path d="M8 50A42 13.5 0 0 0 92 50" fill="none" stroke="url(#goldStroke)" stroke-width="2.8" stroke-linecap="round"/>
<circle cx="84" cy="30" r="2.6" fill="{GOLD_2}"/><circle cx="19" cy="70" r="1.9" fill="{GOLD}"/></svg>"""


def _disc_stars(seed):
    r = random.Random(seed)
    out = ''
    for _ in range(20):
        a, d = r.uniform(0, 6.283), r.uniform(28, 46)
        import math
        out += f'<circle cx="{50 + d * math.cos(a):.1f}" cy="{50 + d * math.sin(a):.1f}" r="{r.uniform(.5, 1.3):.2f}" fill="{CREAM}" opacity="{r.uniform(.3, .8):.2f}"/>'
    return out


def sparkle(x, y, s, color=GOLD_2, op=1.0):
    """A four-point sparkle, the site's 2D sky effect."""
    return (f'<path d="M{x} {y - s} Q{x + s * .14} {y - s * .14} {x + s} {y} Q{x + s * .14} {y + s * .14} {x} {y + s} '
            f'Q{x - s * .14} {y + s * .14} {x - s} {y} Q{x - s * .14} {y - s * .14} {x} {y - s}Z" fill="{color}" opacity="{op}"/>')


def sky_html(sky='night', seed=1, nebula=None):
    """Nebula clouds + stars + a few sparkles. nebula: list of (x, y, w, h, color, opacity) or None for a seeded mix."""
    r = random.Random(seed)
    night = sky == 'night'
    if nebula is None:
        palette = [VIOLET, ROSE, TEAL, GOLD, SKYBLUE]
        r.shuffle(palette)
        nebula = []
        for k, c in enumerate(palette[:4]):
            nebula.append((r.randint(-200, 800), r.randint(-200, 1150), r.randint(420, 720), r.randint(380, 640), c,
                           (r.uniform(.42, .62) if night else r.uniform(.30, .45))))
    blobs = ''.join(f'<div class="neb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};opacity:{o}"></div>'
                    for x, y, w, h, c, o in nebula)
    star_c = CREAM if night else INK
    stars = ''.join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.uniform(.8, 2.4):.1f}" fill="{star_c}" opacity="{r.uniform(.25, .85) if night else r.uniform(.10, .3):.2f}"/>'
                    for _ in range(150 if night else 70))
    sparks = ''.join(sparkle(r.uniform(60, W - 60), r.uniform(60, H - 60), r.uniform(9, 20), GOLD_2 if night else GOLD, r.uniform(.55, .95))
                     for _ in range(7))
    return f'<div class="sky">{blobs}<svg class="stars" viewBox="0 0 {W} {H}">{stars}{sparks}</svg></div>'


FIT_JS = """<script>
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(el=>{
  let s=parseFloat(getComputedStyle(el).fontSize); const min=s*0.55;
  while((el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1)&&s>min){s-=2;el.style.fontSize=s+'px';}
});});
</script>"""


class Slide:
    def __init__(self, lang='en', sky='night', seed=1, nebula=None, brand=True, handle=True, dots=None, extra_css=''):
        self.lang, self.sky, self.seed, self.nebula = lang, sky, seed, nebula
        self.brand, self.handle, self.dots, self.extra_css = brand, handle, dots, extra_css

    def page(self, body):
        top = f'<div class="brand">{brand_mark()}<span>webbiespirit</span></div>' if self.brand else ''
        hnd = '<div class="handle">@webbiespirit</div>' if self.handle else ''
        dts = ''
        if self.dots:
            i, n = self.dots
            dts = '<div class="dots">' + ''.join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(n)) + '</div>'
        return (f'<!doctype html><html lang="{self.lang}"><head><meta charset="utf-8"><style>{css(self.sky)}{self.extra_css}</style></head>'
                f'<body>{DEFS}{sky_html(self.sky, self.seed, self.nebula)}{top}<div class="layer">{body}</div>{dts}{hnd}{FIT_JS}</body></html>')


def render(html_doc, out_png):
    out = Path(out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / 'slide.html'
        src.write_text(html_doc, encoding='utf-8')
        subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        f'--window-size={W},{H}', '--virtual-time-budget=3000', '--allow-file-access-from-files',
                        f'--screenshot={out}', src.as_uri()], check=True, capture_output=True)
    return out
