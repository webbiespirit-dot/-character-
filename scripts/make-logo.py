"""Generate the webbiespirit W-signature mark for Instagram.

The mark: a spun-gold sun disc with the W written through it as one signature stroke.
Outside the disc the pen is a bundle of gold light-trail threads on white paper; where it
crosses the rim it flips to a solid white knockout, and it flips back to gold on the way
out. Everything is computed here (deterministic, fixed seeds) and written as SVG:

    python3 scripts/make-logo.py [outdir]      (default: social/logo)

    w-signature.svg   the master mark, 1000x1000 units, white background
    reveal.html       the mark writing itself: the page scripts/render-logo.mjs turns into video

Rasters (profile PNG, size ladder, Reel MP4) come from scripts/render-logo.mjs, which needs
Chromium through Playwright and ffmpeg.
"""
import math
import sys
from pathlib import Path

import numpy as np

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "social" / "logo"
OUT.mkdir(parents=True, exist_ok=True)

CX, CY, R = 500.0, 500.0, 316.0          # the sun disc
SAFE = 458.0                              # Instagram's circle crop, minus a margin

# ---------- the signature centerline -------------------------------------------------
# One stroke, left to right: (x, y, tangent angle in degrees (screen coords), handle in, handle out).
# Tangents are shared at every knot, so the joins are G1 and the pen never jerks.
KNOTS = [
    (122, 716, -60, 0, 64),      # pen touches down outside the disc, lower left
    (236, 548, -66, 76, 96),     # climbs through the rim
    (330, 300, 0, 22, 22),       # apex 1, inside the sun
    (396, 744, 0, 30, 30),       # valley 1
    (507, 418, 0, 20, 20),       # the middle peak sits lower, as a hand writes it
    (616, 744, 0, 30, 30),       # valley 2
    (716, 318, -64, 130, 72),    # the final upstroke leaves the sun
    (776, 190, -126, 72, 66),    # and turns over the top
    (640, 108, 180, 80, 84),     # the swash arcs over the sun
    (404, 144, 196, 92, 0),      # and fades out above its left shoulder
]
# pen pressure, as half-width keys at (knot, fraction of the way to the next knot)
PRESSURE = [
    (0, 0.0, 1.2), (0, 0.5, 5.5), (1, 0.0, 8.0), (1, 0.5, 8.5), (2, 0.0, 5.0),
    (2, 0.25, 30), (2, 0.42, 42), (2, 0.72, 38), (3, 0.0, 7.5),
    (3, 0.5, 5.5), (4, 0.0, 4.5),
    (4, 0.25, 30), (4, 0.42, 42), (4, 0.72, 38), (5, 0.0, 7.5),
    (5, 0.5, 6.0), (6, 0.0, 6.5), (6, 0.5, 10), (7, 0.0, 12), (7, 0.5, 14), (8, 0.0, 14),
    (8, 0.4, 11), (8, 0.75, 5), (9, 0.0, 0.0),
]


def sample_centerline(knots, per_seg=600):
    pts = []
    for i in range(len(knots) - 1):
        x0, y0, a0, _, ho = knots[i]
        x1, y1, a1, hi, _ = knots[i + 1]
        p0 = np.array([x0, y0], float)
        p3 = np.array([x1, y1], float)
        c1 = p0 + ho * np.array([math.cos(math.radians(a0)), math.sin(math.radians(a0))])
        c2 = p3 - hi * np.array([math.cos(math.radians(a1)), math.sin(math.radians(a1))])
        t = np.linspace(0, 1, per_seg, endpoint=(i == len(knots) - 2))[:, None]
        q = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p3
        pts.append(q)
    raw = np.vstack(pts)
    seg = np.linalg.norm(np.diff(raw, axis=0), axis=1)
    s_raw = np.concatenate([[0], np.cumsum(seg)])
    s = np.arange(0, s_raw[-1], 1.0)
    C = np.stack([np.interp(s, s_raw, raw[:, 0]), np.interp(s, s_raw, raw[:, 1])], 1)
    # arc length at each knot
    knot_s = [s_raw[min(i * (per_seg - 1), len(s_raw) - 1)] for i in range(len(knots))]
    knot_s = [s_raw[i * per_seg - (1 if i else 0)] if i < len(knots) - 1 else s_raw[-1] for i in range(len(knots))]
    return s, C, knot_s


def gsmooth(v, sigma):
    k = int(3 * sigma)
    g = np.exp(-0.5 * (np.arange(-k, k + 1) / sigma) ** 2)
    g /= g.sum()
    return np.convolve(np.pad(v, k, mode="edge"), g, mode="valid")


s, C, knot_s = sample_centerline(KNOTS)
L = s[-1]
T = np.gradient(C, axis=0)
T /= np.linalg.norm(T, axis=1)[:, None]
N = np.stack([-T[:, 1], T[:, 0]], 1)

# pressure: cosine interpolation between keys along arc length, then a light smoothing
keys = sorted((knot_s[k] + f * (knot_s[k + 1] - knot_s[k]) if k + 1 < len(knot_s) else knot_s[k], hw) for k, f, hw in PRESSURE)
hw = np.zeros_like(s)
for (sa, ha), (sb, hb) in zip(keys[:-1], keys[1:]):
    m = (s >= sa) & (s <= sb)
    u = (s[m] - sa) / max(sb - sa, 1e-6)
    hw[m] = ha + (hb - ha) * (1 - np.cos(math.pi * u)) / 2
hw = gsmooth(hw, 5)
hw[-1] = 0

# where the stroke crosses the rim (entering, then leaving)
rad = np.hypot(C[:, 0] - CX, C[:, 1] - CY)
inside = rad < R
crossings = np.where(inside[:-1] != inside[1:])[0]
s_in, s_out = s[crossings[0]], s[crossings[-1]]
reach = (rad + hw).max()
print(f"length {L:.0f}  rim in at {s_in:.0f}  out at {s_out:.0f}  farthest ink {reach:.0f} at {C[(rad + hw).argmax()].round()} (safe {SAFE:.0f})", file=sys.stderr)
assert reach <= SAFE, "the mark leaves Instagram's circle crop"


def discs(sel, scale=1.0, floor=0.6):
    """A round nib's trace as a union of discs: exact pressure stroke, no folds at the apexes."""
    parts = []
    idx = np.where(sel)[0]
    i = 0
    while i < len(idx):
        j = idx[i]
        r = max(hw[j] * scale, floor)
        parts.append("M%.1f,%.1fa%.1f,%.1f 0 1,0 %.1f,0a%.1f,%.1f 0 1,0 %.1f,0z" % (C[j, 0] - r, C[j, 1], r, r, 2 * r, r, r, -2 * r))
        i += max(1, int(round(max(0.8, 0.12 * r))))
    return "".join(parts)


def polyline(sel, step=3):
    P = C[sel][::step]
    return "M" + " ".join("%.1f,%.1f" % (x, y) for x, y in P)


# ---------- gold ---------------------------------------------------------------------
def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def ramp(stops):
    def col(t):
        t = t % 1.0
        for (a, ca), (b, cb) in zip(stops[:-1], stops[1:]):
            if a <= t <= b:
                f = (t - a) / (b - a)
                c = hex2rgb(ca) * (1 - f) + hex2rgb(cb) * f
                return "#%02X%02X%02X" % tuple(int(round(v)) for v in c)
        return stops[-1][1]
    return col


OUTER = ramp([(0.00, "#D8A63A"), (0.12, "#F0D27E"), (0.22, "#FCF1CC"), (0.30, "#EFCF78"), (0.40, "#C08B2C"),
              (0.48, "#8F5E14"), (0.58, "#D1A13A"), (0.68, "#FAE9B4"), (0.76, "#E6BE57"), (0.86, "#A8761C"),
              (0.93, "#7B4F10"), (1.00, "#D8A63A")])
CORE = ramp([(0.00, "#C68F22"), (0.12, "#DDAF46"), (0.22, "#E8C266"), (0.30, "#CC9A30"), (0.40, "#8E5B12"),
             (0.48, "#5E3908"), (0.58, "#A6711A"), (0.68, "#E2B954"), (0.76, "#C68F22"), (0.86, "#7A4B0E"),
             (0.93, "#583406"), (1.00, "#C68F22")])
GLINT = ramp([(0.00, "#FFFBEC"), (0.5, "#FBF0C6"), (1.0, "#FFFBEC")])
NG = 6


def grad(idname, colfn, k, base_ang=70, radius=360):
    ang = math.radians(base_ang + (k - (NG - 1) / 2) * 2.4)
    dx, dy = math.cos(ang), math.sin(ang)
    phase = (k - (NG - 1) / 2) * 0.014
    stops = "".join('<stop offset="%.3f" stop-color="%s"/>' % (j / 24, colfn(j / 24 + phase)) for j in range(25))
    return ('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f">%s</linearGradient>'
            % (idname, CX - radius * dx, CY - radius * dy, CX + radius * dx, CY + radius * dy, stops))


rng = np.random.default_rng(7)


def bundle(sel, n, dist_pow, scale, amp_rng, lam_rng, sw_fn, op_fn, gid, start_fade, end_fade, step=4):
    """n filaments riding the same centerline, each at its own radius inside the pen width,
    slowly rotating about the axis so they cross; the bundle's width is the pen pressure."""
    lin = np.linspace(-1, 1, n)
    base = np.clip(np.sign(lin) * np.abs(lin) ** dist_pow * scale + rng.uniform(-0.03, 0.03, n), -0.99, 0.99)
    amp = rng.uniform(*amp_rng, n)
    lam = rng.uniform(*lam_rng, n)
    ph = rng.uniform(0, 2 * math.pi, n)
    out = []
    idx = np.where(sel)[0]
    for i in np.argsort(-np.abs(base)):
        m = idx
        uu = np.clip(abs(base[i]) * np.cos(2 * math.pi * s[m] / lam[i] + ph[i])
                     + amp[i] * np.sin(2 * math.pi * s[m] / (lam[i] * 0.37) + ph[i] * 1.7), -1, 1)
        pts = (C[m] + N[m] * (uu * hw[m])[:, None])[::step]
        d = "M" + " ".join("%.1f,%.1f" % (px, py) for px, py in pts)
        out.append('<path d="%s" stroke="url(#%s%d)" stroke-width="%.2f" opacity="%.2f"/>'
                   % (d, gid, i % NG, sw_fn(base[i]), op_fn(base[i])))
    return "".join(out)


# the thread bundle lives outside the sun: lead-in and flourish, with a little overlap under the disc
lead = s <= s_in + 30
exit_ = s >= s_out - 30
threads = ""
for sel in (lead, exit_):
    threads += bundle(sel, 16, 1.3, 0.98, (0.03, 0.10), (900, 1700),
                      lambda b: 1.6 + 1.5 * (1 - abs(b)) ** 1.5 + rng.uniform(0, 0.4),
                      lambda b: min(0.95, 0.5 + 0.35 * (1 - abs(b)) ** 0.8 + rng.uniform(0, 0.1)), "o", 0, 0)
    threads += bundle(sel, 7, 1.0, 0.36, (0.03, 0.08), (800, 1500),
                      lambda b: 3.0 + 1.8 * (1 - abs(b) / 0.36) + rng.uniform(0, 0.4),
                      lambda b: min(0.95, 0.82 + 0.12 * (1 - abs(b) / 0.36)), "c", 0, 0)
    threads += bundle(sel, 3, 1.0, 0.55, (0.02, 0.05), (1000, 1800),
                      lambda b: 1.0 + rng.uniform(0, 0.4), lambda b: 0.9, "g", 0, 0)
# inside the sun the same bundle runs white-hot: pale threads over the white knockout
inner = (s >= s_in - 30) & (s <= s_out + 30)
PALE = ramp([(0.0, "#FFFFFF"), (0.3, "#FDF7E6"), (0.5, "#F9EDCB"), (0.7, "#FDF7E6"), (1.0, "#FFFFFF")])
inner_threads = bundle(inner, 8, 1.3, 0.86, (0.03, 0.10), (900, 1700),
                       lambda b: 0.8 + 0.6 * (1 - abs(b)) ** 1.5, lambda b: 0.38, "p", 0, 0)

core_solid = discs(lead | exit_, scale=0.58, floor=0.5)    # the bronze spine that survives 110px
white_solid = discs(inner, scale=1.0, floor=0.6)            # the knockout
mask_line = polyline(np.ones_like(s, bool), step=3)

# ---------- the spun sun ---------------------------------------------------------------
rng2 = np.random.default_rng(3)
rings = []
rr = 10.0
while rr < R - 2:
    op = rng2.uniform(0.05, 0.16) * min(1.0, (rr - 6) / 80.0)
    col = "#FFF6D8" if rng2.random() < 0.5 else "#7A5212"
    rings.append('<circle cx="%g" cy="%g" r="%.1f" stroke="%s" stroke-opacity="%.3f" stroke-width="%.2f"/>'
                 % (CX, CY, rr, col, op, rng2.uniform(0.8, 1.5)))
    rr += rng2.uniform(1.7, 2.6)


def sector(a0, a1, radius):
    a0, a1 = math.radians(a0), math.radians(a1)
    return "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (CX, CY, CX + radius * math.cos(a0), CY + radius * math.sin(a0),
                                                  CX + radius * math.cos(a1), CY + radius * math.sin(a1))


grads = "".join(grad("o%d" % k, OUTER, k) + grad("c%d" % k, CORE, k, base_ang=68) + grad("g%d" % k, GLINT, k)
                + grad("p%d" % k, PALE, k) for k in range(NG))

DEFS = f'''<defs>
  {grads}
  <linearGradient id="spun" gradientUnits="userSpaceOnUse" x1="{CX - 240:.0f}" y1="{CY - 240:.0f}" x2="{CX + 240:.0f}" y2="{CY + 240:.0f}">
    <stop offset="0" stop-color="#F7E6B4"/><stop offset="0.16" stop-color="#F3D784"/><stop offset="0.38" stop-color="#DDB048"/>
    <stop offset="0.58" stop-color="#B98424"/><stop offset="0.78" stop-color="#CFA03A"/><stop offset="1" stop-color="#E9C96E"/>
  </linearGradient>
  <radialGradient id="rim" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="{R}">
    <stop offset="0.86" stop-color="#7A4B10" stop-opacity="0"/><stop offset="1" stop-color="#6E430E" stop-opacity="0.32"/>
  </radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="30"/></filter>
  <clipPath id="sun"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>
  <path id="spine" pathLength="1" d="{mask_line}"/>
</defs>'''

ART = f'''<rect width="1000" height="1000" fill="#FFFFFF"/>
<g class="sign" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="{core_solid}" fill="#9C6B1B" stroke="none" opacity="0.92"/>
  {threads}
</g>
<g class="sun">
  <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#spun)"/>
  <g clip-path="url(#sun)" fill="none">
    {''.join(rings)}
    <path d="{sector(-135 - 26, -135 + 26, 440)}" fill="#FFF8E0" opacity="0.5" filter="url(#soft)"/>
    <path d="{sector(45 - 22, 45 + 22, 440)}" fill="#FFF3CC" opacity="0.26" filter="url(#soft)"/>
  </g>
  <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#rim)"/>
</g>
<g class="sign" clip-path="url(#sun)" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="{white_solid}" fill="#FFFFFF" stroke="none"/>
  {inner_threads}
</g>'''

SVG_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1000 1000" width="1000" height="1000">'
svg = f'''{SVG_OPEN}
<title>webbiespirit</title>
{DEFS}
{ART}
</svg>
'''
(OUT / "w-signature.svg").write_text(svg)

# ---------- the reveal: the signature writes itself, then light sweeps the gold ------------
MASK_W = 2 * hw.max() + 24
reveal = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>webbiespirit</title>
<style>
html,body{{margin:0;height:100%;background:#fff;overflow:hidden}}
body{{display:grid;place-items:center}}
svg{{display:block;width:min(86vw,86vh);height:min(86vw,86vh)}}
.sun{{transform-box:fill-box;transform-origin:center;animation:rise 700ms cubic-bezier(.23,1,.32,1) both}}
#pen{{stroke-dasharray:1;stroke-dashoffset:1;animation:write 2800ms cubic-bezier(.45,.05,.55,.95) 500ms both}}
.sheen{{animation:sweep 2000ms cubic-bezier(.45,.05,.55,.95) 3300ms both}}
@keyframes rise{{from{{opacity:0;transform:scale(.94)}}to{{opacity:1;transform:none}}}}
@keyframes write{{to{{stroke-dashoffset:0}}}}
@keyframes sweep{{from{{transform:translate(-760px,-760px)}}to{{transform:translate(760px,760px)}}}}
</style></head><body>
{SVG_OPEN}
{DEFS}
<defs>
  <mask id="write" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="1000">
    <use id="pen" href="#spine" fill="none" stroke="#fff" stroke-width="{MASK_W:.0f}" stroke-linecap="round" stroke-linejoin="round"/>
  </mask>
  <mask id="gold" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="1000">
    <circle cx="{CX}" cy="{CY}" r="{R}" fill="#fff"/>
    <path d="{core_solid}" fill="#fff"/>
  </mask>
  <linearGradient id="sheenGrad" gradientUnits="userSpaceOnUse" x1="380" y1="380" x2="620" y2="620">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.62"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="1000" height="1000" fill="#FFFFFF"/>
<g class="sun">
  <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#spun)"/>
  <g clip-path="url(#sun)" fill="none">
    {''.join(rings)}
    <path d="{sector(-135 - 26, -135 + 26, 440)}" fill="#FFF8E0" opacity="0.5" filter="url(#soft)"/>
    <path d="{sector(45 - 22, 45 + 22, 440)}" fill="#FFF3CC" opacity="0.26" filter="url(#soft)"/>
  </g>
  <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#rim)"/>
</g>
<g mask="url(#write)">
  <g class="sign" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="{core_solid}" fill="#9C6B1B" stroke="none" opacity="0.92"/>
    {threads}
  </g>
  <g class="sign" clip-path="url(#sun)" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="{white_solid}" fill="#FFFFFF" stroke="none"/>
    {inner_threads}
  </g>
</g>
<g mask="url(#gold)"><g class="sheen"><rect x="-900" y="-900" width="2800" height="2800" fill="url(#sheenGrad)"/></g></g>
</svg>
</body></html>
'''
(OUT / "reveal.html").write_text(reveal)
print("wrote", OUT / "w-signature.svg", f"({len(svg) // 1024} KB)", "and", OUT / "reveal.html", file=sys.stderr)
