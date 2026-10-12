#!/usr/bin/env python3
"""Render the webbiespirit Instagram posts (1080x1350) in English and Greek.

    python3 social/posts/photograms.py   # once, draws the sun-print photograms
    python3 social/posts/make_posts.py

The posts are printed in the site's own world (see DESIGN.md): brushed Prussian-cobalt
emulsion coats on cool cotton paper, type exposed in white, sunlight only on the action,
and photograms of real objects. Each slide is an HTML page screenshotted with headless
Chromium into social/posts/<lang>/. Set CHROME if the browser lives elsewhere.
"""
import html
import os
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
W, H = 1080, 1350
E = html.escape

T = {
    'en': {
        'cover': 'See your new website before you pay anything.',
        'steps': [
            ('Tell us about your business.', 'A few lines is enough: what you do, who your customers are, what you want them to do.'),
            ('We design your preview. Free.', 'A concept of your new website, designed around your business.'),
            ('You see it. Then you decide.', 'Love it? We build it. Not for you? You owe nothing.'),
        ],
        'strip': ['Tell us', 'We design', 'You decide'],
        'cta_h': 'Want your free preview?', 'cta_b': 'Send us “PREVIEW” in a message.',
        'pk_h': 'Simple packages.', 'pk_f': 'Preview first. Pay only if you love it.',
        'pk': [('Start', '350 €', '', '2 rounds of changes'),
               ('Pro', '499 €', '699 €', '3 rounds of changes + 30 days of small changes'),
               ('Ultra', '947 €', '', 'Unlimited changes for 60 days, online shop, customer accounts')],
        'most': 'Most picked',
        'g_h': 'Instagram is where people see you. Google is where they find you.',
        'g_b': 'When someone searches “barber Larnaca”, websites are what show up. Let’s make yours.',
        'l_h': 'Websites for Larnaca businesses.',
        'l_list': ['Tattoo studios', 'Barbers & beauty', 'Restaurants & cafés'],
        'l_more': 'and more. Based in Larnaca, working with businesses anywhere.',
    },
    'el': {
        'cover': 'Δες τη νέα σου ιστοσελίδα πριν πληρώσεις οτιδήποτε.',
        'steps': [
            ('Πες μας για την επιχείρησή σου.', 'Λίγες γραμμές αρκούν: τι κάνεις, ποιοι είναι οι πελάτες σου, τι θέλεις να κάνουν.'),
            ('Σχεδιάζουμε τη μακέτα σου. Δωρεάν.', 'Μια πρόταση για τη νέα σου ιστοσελίδα, σχεδιασμένη γύρω από την επιχείρησή σου.'),
            ('Τη βλέπεις. Μετά αποφασίζεις.', 'Σου αρέσει; Τη φτιάχνουμε. Δεν είναι για σένα; Δεν χρωστάς τίποτα.'),
        ],
        'strip': ['Μας λες', 'Σχεδιάζουμε', 'Αποφασίζεις'],
        'cta_h': 'Θέλεις τη δωρεάν μακέτα σου;', 'cta_b': 'Στείλε μας «PREVIEW» σε μήνυμα.',
        'pk_h': 'Απλά πακέτα.', 'pk_f': 'Πρώτα η μακέτα. Πληρώνεις μόνο αν σε ενθουσιάσει.',
        'pk': [('Start', '350 €', '', '2 γύροι αλλαγών'),
               ('Pro', '499 €', '699 €', '3 γύροι αλλαγών + 30 μέρες μικρές αλλαγές'),
               ('Ultra', '947 €', '', 'Απεριόριστες αλλαγές για 60 μέρες, e‑shop, λογαριασμοί πελατών')],
        'most': 'Η πιο δημοφιλής',
        'g_h': 'Στο Instagram σε βλέπουν. Στο Google σε βρίσκουν.',
        'g_b': 'Όταν κάποιος ψάχνει «κουρείο Λάρνακα», εμφανίζονται ιστοσελίδες. Ας φτιάξουμε τη δική σου.',
        'l_h': 'Ιστοσελίδες για επιχειρήσεις της Λάρνακας.',
        'l_list': ['Στούντιο τατουάζ', 'Κουρεία & ομορφιά', 'Εστιατόρια & καφέ'],
        'l_more': 'και πολλά ακόμα. Με έδρα τη Λάρνακα, για επιχειρήσεις όπου κι αν βρίσκονται.',
    },
}


def css():
    f = (ROOT / 'assets/fonts').as_uri()
    i = (ROOT / 'assets/img').as_uri()
    return f"""
@font-face {{ font-family: P; src: url({f}/piazzolla-latin-standard-normal.woff2) format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: P; src: url({f}/piazzolla-greek-standard-normal.woff2) format('woff2'); font-weight: 100 900; unicode-range: U+0370-03FF, U+1F00-1FFF; }}
@font-face {{ font-family: S; src: url({f}/sofia-sans-latin-wght-normal.woff2) format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: S; src: url({f}/sofia-sans-greek-wght-normal.woff2) format('woff2'); font-weight: 100 900; unicode-range: U+0370-03FF, U+1F00-1FFF; }}
:root {{ --deep:#0B2559; --field:#163F94; --mid:#2F63C7; --light:#8FB0E6; --sun:#E0E46A; --sens:#DAD69C;
        --paper:#F3F6F9; --ink:#0B2559; --soft:#3A5486; --onsoft:#D3DFF5; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}px; height: {H}px; overflow: hidden; }}
body {{ background: var(--paper); color: var(--ink); font-family: S, sans-serif; position: relative; }}
body::after {{ content: ''; position: absolute; inset: 0; background: url({i}/paper-grain.png); background-size: 160px; mix-blend-mode: multiply; opacity: .55; pointer-events: none; z-index: 9; }}
.coat {{ position: absolute; overflow: hidden; background-color: var(--field); background-image: url({i}/emulsion-mottle-soft.png); background-size: 900px 900px;
        color: #fff; -webkit-mask-box-image: url({i}/emulsion-edge.png) 64 fill / 44px stretch; }}
.coat.deep {{ background-color: var(--deep); }}
.gram {{ position: absolute; display: block; }}
.mark {{ position: absolute; display: flex; align-items: center; gap: 14px; font-family: P; font-size: 40px; font-weight: 520; letter-spacing: -.01em; z-index: 5; }}
.mark i {{ width: 26px; height: 26px; border-radius: 50%; background: var(--sun); box-shadow: 0 0 0 6px rgba(224,228,106,.18); }}
.mark b {{ font-weight: 520; color: var(--mid); }} .coat .mark b {{ color: var(--onsoft); }}
.handle {{ position: absolute; font-size: 28px; letter-spacing: .02em; color: var(--soft); z-index: 5; }}
.coat .handle {{ color: var(--onsoft); }}
h1 {{ font-family: P; font-weight: 560; letter-spacing: -.022em; line-height: .98; text-wrap: balance; }}
.lead {{ font-size: 40px; line-height: 1.38; color: var(--soft); text-wrap: pretty; }}
.coat .lead {{ color: var(--onsoft); }}
.pill {{ display: inline-block; background: var(--sun); color: var(--deep); font-weight: 700; font-size: 38px; padding: 24px 40px; border-radius: 999px; white-space: nowrap; }}
.fit {{ overflow: hidden; }}
.strip {{ position: absolute; display: grid; -webkit-mask-box-image: url({i}/emulsion-edge.png) 64 fill / 40px stretch; }}
.band {{ position: relative; background-image: url({i}/emulsion-mottle-soft.png); background-size: 700px 700px; padding: 34px 30px; overflow: hidden; }}
.band.latent {{ background-color: var(--sens); color: var(--deep); }}
.band.b1 {{ background-color: var(--light); color: var(--deep); }}
.band.b2 {{ background-color: var(--mid); color: #fff; }}
.band.b3 {{ background-color: var(--deep); color: #fff; }}
.band .n {{ font-family: P; font-weight: 300; font-size: 150px; line-height: .8; opacity: .92; }}
.band .lbl {{ font-family: P; font-weight: 460; font-size: 38px; line-height: 1.1; margin-top: 18px; }}
.band.latent .n, .band.latent .lbl {{ opacity: .38; }}
"""


FIT_JS = """<script>
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(el=>{
  let s=parseFloat(getComputedStyle(el).fontSize); const min=s*0.6;
  while((el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1)&&s>min){s-=2;el.style.fontSize=s+'px';}
});});
</script>"""

MARK = '<div class="mark" style="{pos}"><i></i><span>webbie<b>spirit</b></span></div>'


def gram(name):
    return (HERE / 'grams' / f'{name}.png').as_uri()


def page(lang, body):
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{css()}</style></head>'
            f'<body>{body}{FIT_JS}</body></html>')


def cover(t, lang):
    return page(lang, f"""
<div class="coat" style="left:34px;top:34px;width:1012px;height:820px">
  {MARK.format(pos='left:60px;top:58px')}
  <img class="gram" src="{gram('phone-site')}" style="width:520px;left:420px;top:120px;transform:rotate(-9deg)">
</div>
<h1 class="fit" data-fit style="position:absolute;left:70px;top:900px;width:940px;height:330px;font-size:98px">{E(t['cover'])}</h1>
<div class="handle" style="left:70px;bottom:52px">@webbiespirit</div>""")


def step(t, lang, k):
    title, body = t['steps'][k]
    bands = ''
    for j in range(3):
        cls = f'b{j + 1}' if j <= k else 'latent'
        g = ''
        if j == 1 and j <= k:
            g = f'<img class="gram" src="{gram("phone-site")}" style="width:210px;left:60px;top:220px;transform:rotate(6deg)">'
        bands += f'<div class="band {cls}"><div class="n">{j + 1}</div><div class="lbl">{E(t["strip"][j])}</div>{g}</div>'
    return page(lang, f"""
{MARK.format(pos='left:70px;top:64px')}
<h1 class="fit" data-fit style="position:absolute;left:70px;top:170px;width:940px;height:250px;font-size:92px">{E(title)}</h1>
<p class="lead fit" data-fit style="position:absolute;left:70px;top:440px;width:900px;height:170px">{E(body)}</p>
<div class="strip" style="left:34px;top:650px;width:1012px;height:600px;grid-template-columns:1fr 1fr 1fr">{bands}</div>
<div class="handle" style="right:70px;bottom:40px">@webbiespirit</div>""")


def cta(t, lang):
    return page(lang, f"""
<div class="coat deep" style="left:34px;top:34px;width:1012px;height:1282px">
  {MARK.format(pos='left:60px;top:58px')}
  <img class="gram" src="{gram('olive')}" style="width:1500px;left:-240px;top:330px;transform:rotate(-10deg)">
  <h1 class="fit" data-fit style="position:absolute;left:60px;top:190px;width:880px;height:300px;font-size:104px">{E(t['cta_h'])}</h1>
  <p class="lead fit" data-fit style="position:absolute;left:60px;top:510px;width:880px;height:120px;color:#fff">{E(t['cta_b'])}</p>
  <div style="position:absolute;left:60px;bottom:70px"><span class="pill">webbiespirit.com</span></div>
</div>""")


def packages(t, lang):
    rows = ''
    for k, (name, price, was, what) in enumerate(t['pk']):
        tag = (f'<span class="pill" style="font-size:26px;padding:10px 22px;position:absolute;right:30px;top:26px">{E(t["most"])}</span>'
               if name == 'Pro' else '')
        was_h = (f'<span style="font-size:32px;text-decoration:line-through;opacity:.7;margin-left:14px;font-weight:400">{E(was)}</span>'
                 if was else '')
        rows += f"""<div class="band b{k + 1}" style="display:grid;grid-template-columns:300px 1fr;align-items:center;padding:30px 40px">
  {tag}<div style="font-family:P;font-size:84px;font-weight:460;line-height:1">{name}</div>
  <div><div style="font-size:58px;font-weight:800;line-height:1.05">{E(price)}{was_h}</div>
  <div class="fit" data-fit style="font-size:31px;line-height:1.3;margin-top:10px;max-height:84px;opacity:.95">{E(what)}</div></div></div>"""
    return page(lang, f"""
{MARK.format(pos='left:70px;top:64px')}
<h1 style="position:absolute;left:70px;top:160px;font-size:104px">{E(t['pk_h'])}</h1>
<div class="strip" style="left:34px;top:330px;width:1012px;height:820px;grid-template-rows:1fr 1fr 1fr">{rows}</div>
<p class="lead fit" data-fit style="position:absolute;left:70px;top:1180px;width:940px;height:120px;color:var(--ink)">{E(t['pk_f'])}</p>""")


def google(t, lang):
    return page(lang, f"""
<div class="coat" style="left:34px;top:34px;width:1012px;height:1282px">
  {MARK.format(pos='left:60px;top:58px')}
  <img class="gram" src="{gram('phone-search')}" style="width:500px;left:560px;top:600px;transform:rotate(8deg)">
  <h1 class="fit" data-fit style="position:absolute;left:60px;top:170px;width:890px;height:400px;font-size:94px">{E(t['g_h'])}</h1>
  <p class="lead fit" data-fit style="position:absolute;left:60px;top:640px;width:470px;height:330px">{E(t['g_b'])}</p>
  <div style="position:absolute;left:60px;bottom:70px"><span class="pill">webbiespirit.com</span></div>
</div>""")


def larnaca(t, lang):
    items = ''.join(f'<div style="font-family:P;font-weight:460;font-size:66px;line-height:1.12;padding:10px 0">{E(x)}</div>'
                    for x in t['l_list'])
    return page(lang, f"""
{MARK.format(pos='left:70px;top:64px')}
<h1 class="fit" data-fit style="position:absolute;left:70px;top:160px;width:940px;height:230px;font-size:96px">{E(t['l_h'])}</h1>
<div class="coat deep" style="left:34px;top:430px;width:1012px;height:886px">
  <img class="gram" src="{gram('olive')}" style="width:760px;left:300px;top:-150px;transform:rotate(-6deg)">
  <div style="position:absolute;left:60px;top:380px">{items}</div>
  <p class="lead fit" data-fit style="position:absolute;left:60px;top:672px;width:880px;height:120px">{E(t['l_more'])}</p>
  <div class="handle" style="right:60px;bottom:52px">@webbiespirit</div>
</div>""")


def slides(lang):
    t = T[lang]
    yield '1-how-it-works-1', cover(t, lang)
    for k in range(3):
        yield f'1-how-it-works-{k + 2}', step(t, lang, k)
    yield '1-how-it-works-5', cta(t, lang)
    yield '2-packages', packages(t, lang)
    yield '3-found-on-google', google(t, lang)
    yield '4-made-for-larnaca', larnaca(t, lang)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for lang in T:
            (HERE / lang).mkdir(exist_ok=True)
            for name, doc in slides(lang):
                src = Path(tmp) / f'{lang}-{name}.html'
                src.write_text(doc, encoding='utf-8')
                subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                                '--force-device-scale-factor=1', f'--window-size={W},{H}', '--virtual-time-budget=3000',
                                '--allow-file-access-from-files', f'--screenshot={HERE / lang / (name + ".png")}', src.as_uri()],
                               check=True, capture_output=True)
                print(lang, name)


if __name__ == '__main__':
    main()
