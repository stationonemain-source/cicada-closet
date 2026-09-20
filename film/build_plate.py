"""Build the hero plate: film frame 1, untouched, with its OWN borders extruded outward
so the hero is full-bleed and flush.

Nothing is redrawn -- her lettering is the original pixels, bit for bit, pasted back on
top at the end. That is also why the handoff to the film is seamless: at the handoff
scale the plate IS frame 1.

Every invented pixel comes from her own photo:
  - left / right : the photo's own wood margins, mirror-tiled outward (grain scale kept)
  - above / below: the nearest row whose paper carries NO ink, repeated with noise, then
                   eased into shadow so the sheet leaves the light pool instead of ending
                   at an invented cut edge.

Usage: python film/build_plate.py
"""
import json
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "frame1_src.png")

PLATE_W, PLATE_H = 2600, 3800   # covers a 0.42-aspect phone with the sheet at ~88% width
FALLOFF = 900.0                 # rows over which the extension sinks into shadow
KEEP = 0.42                     # brightness left at the far edge of the plate


def blank_row(a, bright, from_top):
    """Nearest row whose paper interior carries no ink -- the texture we extrude."""
    h = a.shape[0]
    for y in (range(h) if from_top else range(h - 1, -1, -1)):
        idx = np.where(bright[y])[0]
        if len(idx) < 200:
            continue
        lo, hi = idx.min() + 60, idx.max() - 60
        if hi - lo < 200:
            continue
        if (a[y, lo:hi].sum(1) < 260).mean() < 0.004:
            return y
    return 0 if from_top else h - 1


def blank_patch(a, bright, ph=220, pw=260):
    """Largest-scoring ink-free patch of paper: the texture the kraft field is built from."""
    h, w, _ = a.shape
    ink = (a.sum(2) < 265) & bright
    best, best_score = None, -1.0
    for y in range(0, h - ph, 20):
        for x in range(0, w - pw, 20):
            blk = bright[y:y + ph, x:x + pw]
            if blk.mean() < 0.999:
                continue
            if ink[y:y + ph, x:x + pw].mean() > 0.0005:
                continue
            score = a[y:y + ph, x:x + pw].std()      # prefer real grain, not a flat blur
            if score > best_score:
                best, best_score = a[y:y + ph, x:x + pw].copy(), score
    if best is None:                                  # fall back to the brightest paper block
        y, x = h // 2, w // 2
        best = a[y:y + ph, x:x + pw].copy()
    return np.concatenate([best, best[::-1]])         # mirrored vertically, so it tiles


def mirror_tile(strip, width):
    """Repeat `strip` outward with mirroring, preserving grain scale."""
    if width <= 0:
        return np.zeros((0, 3))
    parts, n = [], len(strip)
    for i in range(width // n + 2):
        parts.append(strip if i % 2 == 0 else strip[::-1])
    return np.concatenate(parts)[:width]


def build(mode):
    src = Image.open(SRC).convert("RGB")
    a = np.asarray(src).astype(float)
    h, w, _ = a.shape
    bright = a.sum(2) > 300
    yt, yb = blank_row(a, bright, True), blank_row(a, bright, False)
    kraft = mode == "kraft"

    ox, oy = (PLATE_W - w) // 2, (PLATE_H - h) // 2
    left_pad, right_pad = ox, PLATE_W - w - ox
    plate = np.zeros((PLATE_H, PLATE_W, 3))
    rng = np.random.default_rng(7)

    # kraft mode fills from a blank PATCH of her paper (no ink anywhere in it), so the
    # field is real paper grain and never repeats a fragment of the lettering
    kraft_patch = blank_patch(a, bright)

    BAND = 200

    def band_row(y):
        """Rows outside the frame reflect a 200-row band, so the extension keeps real
        2-D texture instead of the vertical streaks a single repeated row produces."""
        if y < 0:
            t = (-y - 1) % (2 * BAND)
            return a[BAND - 1 - t] if t < BAND else a[t - BAND]
        t = (y - h) % (2 * BAND)
        return a[h - 1 - t] if t < BAND else a[h - 2 * BAND + t]

    for py in range(PLATE_H):
        y = py - oy
        inside = 0 <= y < h
        base = a[y] if inside else band_row(y)

        if kraft:
            row = mirror_tile(kraft_patch[py % len(kraft_patch)], PLATE_W)
        else:
            row = np.empty((PLATE_W, 3))
            row[left_pad:left_pad + w] = base
            # wood continues outward from each margin, mirrored so the grain keeps its scale
            row[:left_pad] = mirror_tile(base[:100][::-1], left_pad)[::-1]
            row[left_pad + w:] = mirror_tile(base[w - 60:], right_pad)

        if not inside:                      # ease into shadow, never a fake cut edge
            d = min(1.0, (abs(y) if y < 0 else y - h + 1) / FALLOFF)
            row = row * (1.0 - (1.0 - KEEP) * (d * d * (3 - 2 * d)))
        plate[py] = row

    plate += rng.normal(0, 3.0, plate.shape)
    img = Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8))

    # defocus outward: the sheet leaves the focal plane, which also hides the joins
    blurred = img.filter(ImageFilter.GaussianBlur(11))
    yy = np.arange(PLATE_H)[:, None].astype(float)
    dist = np.clip((np.abs(yy - (oy + h / 2)) - h * 0.60) / 700.0, 0, 1)
    mask = Image.fromarray((dist * 255).astype(np.uint8).repeat(PLATE_W, 1))
    img = Image.composite(blurred, img, mask)

    if kraft:
        # keep her paper and lettering, leave the photo's wood margins out
        m = np.zeros((h, w), np.uint8)
        for y in range(h):
            idx = np.where(bright[y])[0]
            if len(idx) > 200:
                m[y, idx.min() + 26:idx.max() - 26] = 255
        img.paste(src, (ox, oy), Image.fromarray(m).filter(ImageFilter.GaussianBlur(18)))
    else:
        img.paste(src, (ox, oy))            # her frame, untouched, straight back on top

    out = f"hero-plate-{mode}.jpg"
    for d in ("tier1/assets", "tier2/assets"):
        img.save(os.path.join(ROOT, d, out), quality=80, optimize=True)
    kb = os.path.getsize(os.path.join(ROOT, "tier2/assets", out)) // 1024
    print(f"{out}  {PLATE_W}x{PLATE_H}  {kb} KB   frame1 at ({ox},{oy})  blank rows {yt}/{yb}")
    return {"w": PLATE_W, "h": PLATE_H, "ox": ox, "oy": oy, "fw": w, "fh": h}


if __name__ == "__main__":
    geo = build("wood")
    build("kraft")
    print(json.dumps(geo))
