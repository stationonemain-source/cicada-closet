"""Hero assets for the code-driven keyhole zoom (2026-09-20, client round 2).

Two pieces, nothing synthesised around her artwork:
  assets/hero-wood.jpg  -- the wooden desk, stationary, fills the screen
  assets/logo-card.webp -- her new logo as a card with a soft contact shadow baked in,
                           on transparency, so it reads as resting ON the wood

The film no longer plays video frames. The card is the only thing that moves: it scales
about the keyhole until the keyhole swallows the screen. Prints the keyhole's position in
the finished card, which is what the page's engine scales about.

Usage: python film/build_hero.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CARD = 2200          # her artwork, upscaled so the resting state is crisp on retina
PAD = 300            # room for the shadow
OUT = CARD + PAD * 2


def keyhole(img):
    """Locate the keyhole: the dark blob nearest the thorax."""
    a = np.asarray(img.convert("RGB")).astype(int)
    h, w, _ = a.shape
    dark = a.sum(2) < 70
    from collections import deque
    seen = np.zeros_like(dark)
    best = None
    for sy in range(0, h, 4):
        for sx in range(0, w, 4):
            if not dark[sy, sx] or seen[sy, sx]:
                continue
            q, pts = deque([(sy, sx)]), []
            seen[sy, sx] = 1
            while q:
                y, x = q.popleft()
                pts.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and dark[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = 1
                        q.append((ny, nx))
            if len(pts) < 400:
                continue
            p = np.array(pts)
            d = ((p[:, 0].mean() - h * 0.36) ** 2 + (p[:, 1].mean() - w * 0.5) ** 2) ** 0.5
            if best is None or d < best[0]:
                best = (d, p)
    p = best[1]
    return p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max()


def main():
    # ---- wood: stationary background
    wood = Image.open(os.path.join(HERE, "wood_raw.png")).convert("RGB")
    wood = wood.resize((2400, int(2400 * wood.height / wood.width)), Image.LANCZOS)
    w = np.asarray(wood).astype(float) * 0.88          # a touch deeper, so the card carries the eye
    wood = Image.fromarray(np.clip(w, 0, 255).astype(np.uint8))
    for d in ("tier1/assets", "tier2/assets"):
        wood.save(os.path.join(ROOT, d, "hero-wood.jpg"), quality=82, optimize=True)

    # ---- card: her logo + a baked contact shadow, on transparency
    src = Image.open(os.path.join(HERE, "logo_new.webp")).convert("RGBA")
    x0, y0, x1, y1 = keyhole(src)
    sw, sh = src.size
    logo = src.resize((CARD, CARD), Image.LANCZOS)

    canvas = Image.new("RGBA", (OUT, OUT), (0, 0, 0, 0))
    # two shadows: a tight contact line and a broad ambient one -- that is what makes
    # a flat rectangle read as an object lying on a surface rather than pasted onto it
    for blur, off, alpha, grow in ((16, 10, 130, 0), (70, 46, 105, 8)):
        sh_img = Image.new("RGBA", (OUT, OUT), (0, 0, 0, 0))
        box = (PAD - grow, PAD - grow + off, PAD + CARD + grow, PAD + CARD + grow + off)
        sh_img.paste((12, 8, 5, alpha), box)
        canvas = Image.alpha_composite(canvas, sh_img.filter(ImageFilter.GaussianBlur(blur)))

    canvas.paste(logo, (PAD, PAD), logo)
    for d in ("tier1/assets", "tier2/assets"):
        canvas.save(os.path.join(ROOT, d, "logo-card.webp"), quality=86, method=6)

    kb = os.path.getsize(os.path.join(ROOT, "tier2/assets", "logo-card.webp")) // 1024
    wkb = os.path.getsize(os.path.join(ROOT, "tier2/assets", "hero-wood.jpg")) // 1024
    kx = (PAD + (x0 + x1) / 2 * CARD / sw) / OUT
    ky = (PAD + (y0 + y1) / 2 * CARD / sh) / OUT
    kw = (x1 - x0) * CARD / sw / OUT
    print(f"hero-wood.jpg  {wood.size[0]}x{wood.size[1]}  {wkb} KB")
    print(f"logo-card.webp {OUT}x{OUT}  {kb} KB")
    print(f"KEYHOLE in card:  KX={kx:.4f}  KY={ky:.4f}  KW={kw:.4f}")


if __name__ == "__main__":
    main()
