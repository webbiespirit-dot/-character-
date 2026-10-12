#!/usr/bin/env python3
"""Draw the cyanotype photograms used on the posts (deterministic).

A photogram is an object laid on sensitised paper: where it blocks the sun the paper
stays pale, where light passes through glass it only half-exposes, and the edges halate.
Each image is a white RGBA layer whose alpha is "how much light was blocked".
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent / 'grams'
SS = 2  # supersample


def finish(mask, halation=18, contact=1.6, inner=None):
    """mask: L image, 255 = fully blocked (pressed flat on the paper, so sharp).
    inner: optional L image of things lifted off the paper (under glass), which print soft.
    Returns white RGBA with halation, uneven exposure and paper fibre."""
    contact_img = mask.filter(ImageFilter.GaussianBlur(contact * SS))
    halo = mask.filter(ImageFilter.GaussianBlur(halation * SS))
    a = np.maximum(np.asarray(contact_img, np.float32), np.asarray(halo, np.float32) * 0.42)
    if inner is not None:
        a = np.maximum(a, np.asarray(inner.filter(ImageFilter.GaussianBlur(5 * SS)), np.float32))
    h, w = a.shape
    rng = np.random.default_rng(7)
    # uneven exposure: soft, mostly horizontal variation, like a brushed coat
    low = Image.fromarray((rng.random((max(h // 90, 2), max(w // 30, 2))) * 255).astype(np.uint8))
    low = np.asarray(low.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(20 * SS)), np.float32) / 255
    a *= 0.88 + 0.14 * low
    a *= 0.93 + 0.07 * rng.random(a.shape)          # paper fibre unevenness
    a = np.clip(a, 0, 255).astype(np.uint8)
    w, h = mask.size
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    img.putalpha(Image.fromarray(a))
    return img.resize((w // SS, h // SS), Image.LANCZOS)


def phone(kind='site'):
    W, H = 760 * SS, 1440 * SS
    m = Image.new('L', (W, H), 0)
    body = ImageDraw.Draw(m)
    r = 96 * SS
    # glass body: light passes partly through, a little more towards one corner
    grad = Image.linear_gradient('L').resize((W, H)).point(lambda v: 95 + v * 0.22)
    shape = Image.new('L', (W, H), 0)
    ImageDraw.Draw(shape).rounded_rectangle((0, 0, W - 1, H - 1), r, fill=255)
    m.paste(grad, (0, 0), shape)
    body.rounded_rectangle((0, 0, W - 1, H - 1), r, outline=255, width=14 * SS)
    body.rounded_rectangle((W // 2 - 70 * SS, 34 * SS, W // 2 + 70 * SS, 64 * SS), 15 * SS, fill=255)
    inner = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(inner)
    x0, x1 = 70 * SS, W - 70 * SS
    if kind == 'site':
        y = 130 * SS
        d.rectangle((x0, y, x0 + 220 * SS, y + 34 * SS), fill=235)                # logo
        for k in range(3):
            d.rectangle((x1 - (3 - k) * 70 * SS, y + 8 * SS, x1 - (3 - k) * 70 * SS + 46 * SS, y + 22 * SS), fill=200)
        y += 90 * SS
        d.rounded_rectangle((x0, y, x1, y + 470 * SS), 26 * SS, fill=250)          # hero image
        for k in range(5):                                                       # sun rays inside hero
            d.line((x0 + 60 * SS + k * 110 * SS, y + 470 * SS, x0 + 250 * SS + k * 70 * SS, y + 60 * SS), fill=170, width=10 * SS)
        y += 520 * SS
        d.rectangle((x0, y, x1 - 60 * SS, y + 52 * SS), fill=245)                  # headline
        d.rectangle((x0, y + 72 * SS, x1 - 200 * SS, y + 124 * SS), fill=245)
        y += 170 * SS
        for wv in (1.0, .92, .97, .7):                                           # body text
            d.rectangle((x0, y, x0 + int((x1 - x0) * wv), y + 16 * SS), fill=190)
            y += 36 * SS
        y += 30 * SS
        d.rounded_rectangle((x0, y, x0 + 300 * SS, y + 86 * SS), 43 * SS, fill=255)  # button
        y += 140 * SS
        d.rounded_rectangle((x0, y, x0 + (x1 - x0) // 2 - 16 * SS, y + 220 * SS), 20 * SS, fill=215)
        d.rounded_rectangle((x0 + (x1 - x0) // 2 + 16 * SS, y, x1, y + 220 * SS), 20 * SS, fill=215)
    else:  # search results
        y = 150 * SS
        d.rounded_rectangle((x0, y, x1, y + 96 * SS), 48 * SS, fill=245)           # search bar
        cx, cy, rr = x0 + 52 * SS, y + 48 * SS, 18 * SS
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=120, width=6 * SS)
        d.line((cx + 13 * SS, cy + 13 * SS, cx + 30 * SS, cy + 30 * SS), fill=120, width=7 * SS)
        d.rectangle((x0 + 100 * SS, cy - 9 * SS, x0 + 420 * SS, cy + 9 * SS), fill=150)
        y += 170 * SS
        for k in range(4):
            hit = k == 0
            d.rectangle((x0, y, x0 + 260 * SS, y + 14 * SS), fill=170)
            d.rectangle((x0, y + 34 * SS, x1 - (40 if hit else 140) * SS, y + 74 * SS), fill=255 if hit else 225)
            for j, wv in enumerate((1.0, .86)):
                d.rectangle((x0, y + 100 * SS + j * 32 * SS, x0 + int((x1 - x0) * wv), y + 114 * SS + j * 32 * SS), fill=175)
            if hit:
                d.rounded_rectangle((x0 - 24 * SS, y - 26 * SS, x1 + 24 * SS, y + 196 * SS), 26 * SS, outline=255, width=8 * SS)
            y += 260 * SS
    return finish(m, inner=inner)


def olive_branch(seed=3):
    rnd = random.Random(seed)
    W, H = 1500 * SS, 1100 * SS
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    # main stem: gentle curve
    pts = [(int((60 + t * 1380) * SS), int((900 - 520 * t + 160 * math.sin(t * 3.1)) * SS)) for t in [i / 60 for i in range(61)]]
    d.line(pts, fill=255, width=11 * SS, joint='curve')
    for i in range(4, 58, 3):
        bx, by = pts[i]
        nx, ny = pts[i + 1]
        ang = math.atan2(ny - by, nx - bx)
        side = 1 if (i // 3) % 2 else -1
        a = ang + side * math.radians(rnd.uniform(38, 62))
        L = rnd.uniform(210, 300) * SS * (0.75 + 0.25 * math.sin(i / 58 * math.pi))
        wid = L * rnd.uniform(0.13, 0.17)
        leaf = Image.new('L', (int(L * 2.2), int(L * 2.2)), 0)
        ld = ImageDraw.Draw(leaf)
        c = leaf.size[0] // 2
        poly = []
        for k in range(41):
            t = k / 40
            poly.append((c + t * L, c - math.sin(math.pi * t) ** 0.9 * wid))
        for k in range(40, -1, -1):
            t = k / 40
            poly.append((c + t * L, c + math.sin(math.pi * t) ** 0.9 * wid))
        ld.polygon(poly, fill=250)
        ld.line((c, c, c + L * .92, c), fill=205, width=3 * SS)                  # midrib
        leaf = leaf.rotate(-math.degrees(a), resample=Image.BICUBIC, center=(c, c))
        m.paste(255, (bx - c, by - c), leaf)
        if i in (13, 31, 46):                                                  # olives hang below the stem
            ox, oy = bx + 14 * SS, by + 150 * SS
            d.line((bx, by, ox, oy - 34 * SS), fill=255, width=5 * SS)
            d.ellipse((ox - 30 * SS, oy - 40 * SS, ox + 30 * SS, oy + 40 * SS), fill=255)
    return finish(m, halation=14)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    phone('site').save(OUT / 'phone-site.png')
    phone('search').save(OUT / 'phone-search.png')
    olive_branch().save(OUT / 'olive.png')
    print('ok')
