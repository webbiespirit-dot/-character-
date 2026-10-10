"""Generate the brushed-emulsion edge mask and the paper grain tile.

Both are deterministic (fixed seeds), so re-running this script reproduces
the committed PNGs byte for byte on the same Pillow/NumPy versions.

    python3 scripts/make-textures.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def smooth_noise(n, scale, rng):
    """1-D value noise of length n with features roughly `scale` px long."""
    pts = rng.random(n // scale + 3)
    x = np.arange(n) / scale
    i = x.astype(int)
    f = x - i
    f = f * f * (3 - 2 * f)
    return pts[i] * (1 - f) + pts[i + 1] * f


def row_noise(n, scale, rng, sharp=1.0):
    v = smooth_noise(n, scale, rng)
    return v ** sharp


def emulsion_mask(size=480, seed=11):
    """Alpha mask of a cyanotype coat laid with horizontal brush strokes.

    Left and right edges end in bristle streaks of uneven length (stroke
    starts and stops). Top and bottom edges wander, with dry-brush gaps that
    run along the stroke direction.
    """
    rng = np.random.default_rng(seed)
    h = w = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rows, cols = np.arange(h), np.arange(w)

    def side_reach(n):
        # Low-frequency wander plus per-bristle jitter (2-4 px features).
        return (
            26
            + 16 * row_noise(n, 120, rng)
            + 10 * row_noise(n, 3, rng, 1.8)
            + 5 * row_noise(n, 11, rng)
        )

    def cap_reach(n):
        return 24 + 15 * row_noise(n, 140, rng) + 6 * row_noise(n, 37, rng)

    left, right = side_reach(h), side_reach(h)
    top, bottom = cap_reach(w), cap_reach(w)
    d = np.minimum.reduce([
        xx - left[:, None],
        (w - 1 - xx) - right[:, None],
        yy - top[None, :],
        (h - 1 - yy) - bottom[None, :],
    ])
    alpha = np.clip(d / 2.2 + 0.5, 0, 1)

    # Dry-brush streaks: long along x, thin along y.
    streak = np.asarray(
        Image.fromarray((rng.random((h // 2, w // 40)) * 255).astype(np.uint8))
        .resize((w, h), Image.BICUBIC),
        dtype=np.float32,
    ) / 255.0
    near = np.clip(1 - np.maximum(d, 0) / 16.0, 0, 1)
    alpha = alpha * (1 - near * np.clip((0.55 - streak) * 1.6, 0, 0.85))

    # A few stray bristle hairs that overshoot the side edges.
    for side in (0, 1):
        for _ in range(26):
            y = int(rng.integers(30, h - 30))
            length = float(rng.uniform(6, 22))
            reach = (left if side == 0 else right)[y]
            x0 = reach - length
            x1 = reach + 2
            xs = np.arange(max(0, int(x0)), int(x1))
            fade = np.clip((xs - x0) / length, 0, 1) * rng.uniform(0.35, 0.8)
            col = xs if side == 0 else (w - 1 - xs)
            alpha[y, col] = np.maximum(alpha[y, col], fade)
    alpha = np.asarray(
        Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.45)),
        dtype=np.float32,
    ) / 255.0
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = (alpha.clip(0, 1) * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / "emulsion-edge.png", optimize=True)


def paper_grain(size=160, seed=5):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (size, size)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    # Tileable: blend with a half-shifted copy across the seams.
    shifted = np.roll(np.roll(g, size // 2, 0), size // 2, 1)
    w = np.minimum(np.arange(size), size - 1 - np.arange(size)) / (size / 2)
    m = np.minimum.outer(w, w)
    g = g * m + shifted * (1 - m)
    a = (np.abs(g - 0.5) * 2) ** 1.6 * 34  # sparse, faint fibres
    rgba = np.zeros((size, size, 4), np.uint8)
    rgba[..., :3] = np.where(g[..., None] > 0.5, 255, 11)
    rgba[..., 3] = a.clip(0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / "paper-grain.png", optimize=True)


if __name__ == "__main__":
    emulsion_mask()
    paper_grain()
    print("wrote", OUT / "emulsion-edge.png", OUT / "paper-grain.png")
