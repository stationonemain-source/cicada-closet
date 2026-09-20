"""Render exactly what the hero canvas draws, offline.

Mirrors the engine's maths in tier2/index.html (same KX/KY/KW, same easing, same fade), so
it is a faithful preview of the keyhole push without needing a browser. Writes a contact
sheet per device.

Usage: python film/preview_hero.py
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

KX, KY, KW, AW, AH = 0.4991, 0.3664, 0.0473, 1.0, 1.0          # keep in step with the engine
STEPS = (0.0, 0.18, 0.36, 0.55, 0.72, 0.88)


def render(W, H, label):
    wood = Image.open(os.path.join(ROOT, "tier2/assets/hero-kraft.jpg")).convert("RGB")
    card = Image.open(os.path.join(ROOT, "tier2/assets/logo-flush.webp")).convert("RGBA")
    IW, IH = card.size

    # background-size: cover
    sc = max(W / wood.width, H / wood.height)
    bw, bh = int(wood.width * sc + 1), int(wood.height * sc + 1)
    bg0 = wood.resize((bw, bh), Image.LANCZOS).crop(
        ((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H))

    wide = W >= 700
    s0 = min(W * (0.54 if wide else 0.92) / (AW * IW), H * 0.70 / (AH * IH))
    s1 = 1.35 * max(W, H) / (KW * IW)

    shots = []
    for p in STEPS:
        e = p ** 0.85
        s = s0 * (s1 / s0) ** e
        rest_cy = H * (0.54 if wide else 0.52)
        cy = rest_cy + (H / 2 - rest_cy) * min(1, p * 2)
        dw, dh = max(1, int(IW * s)), max(1, int(IH * s))
        dx, dy = W / 2 - KX * IW * s, cy - KY * IH * s

        frame = bg0.copy()
        # only the visible slice, exactly as the canvas does
        sx0, sy0 = max(0, -dx / s), max(0, -dy / s)
        sx1, sy1 = min(IW, (W - dx) / s), min(IH, (H - dy) / s)
        if sx1 > sx0 and sy1 > sy0:
            sub = card.crop((int(sx0), int(sy0), max(int(sx0) + 1, int(sx1)), max(int(sy0) + 1, int(sy1))))
            tw, th = max(1, int((sx1 - sx0) * s)), max(1, int((sy1 - sy0) * s))
            sub = sub.resize((tw, th), Image.LANCZOS)
            frame.paste(sub, (int(dx + sx0 * s), int(dy + sy0 * s)), sub)

        f = max(0.0, min(1.0, (p - 0.62) / 0.30))
        if f > 0:
            frame = Image.blend(frame, Image.new("RGB", (W, H), (0, 0, 0)), f)
        shots.append(frame)

    gap = 14
    sheet = Image.new("RGB", (len(shots) * W + (len(shots) - 1) * gap, H), (24, 20, 16))
    for i, im in enumerate(shots):
        sheet.paste(im, (i * (W + gap), 0))
    out = os.path.join(HERE, f"hero_preview_{label}.jpg")
    sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(out, quality=86)
    print(out, "steps", STEPS)


if __name__ == "__main__":
    render(390, 844, "phone")
    render(1440, 900, "desktop")
