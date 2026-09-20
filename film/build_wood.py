"""Even out the desk so the whole hero background is one tone, one texture.

The generated plate is lit from the upper left, so it reads lighter in one corner and darker
in the other -- that unevenness is what showed as a two-tone background behind the card. Here
the low-frequency illumination is measured and divided out, which flattens the tone while
leaving every bit of the grain intact, then the result is graded to a single walnut.

Only the card's own shadow varies the tone after this, which is what makes the logo sit.

Usage: python film/build_wood.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT_W = 2400
TONE = (63, 50, 42)      # the single walnut the whole background settles on
GRAIN = 1.10             # grain kept slightly above flat, or it looks like paint


def main():
    src = Image.open(os.path.join(HERE, "wood_raw.png")).convert("RGB")
    src = src.resize((OUT_W, int(OUT_W * src.height / src.width)), Image.LANCZOS)
    a = np.asarray(src).astype(float)
    H, W, _ = a.shape

    # low-frequency illumination, measured then removed
    field = np.asarray(
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(OUT_W / 7.0))).astype(float)
    field = np.maximum(field.mean(2, keepdims=True), 12.0)
    flat = a / field                       # 1.0 = average surface, grain rides either side
    flat = 1.0 + (flat - 1.0) * GRAIN

    tone = np.array(TONE, dtype=float)
    out = np.clip(flat * tone, 0, 255)

    # the faintest centre lift, so it reads as a surface under a room light, not wallpaper
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    out *= (1.0 - 0.055 * np.clip(r, 0, 1.4))[..., None]

    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        img.save(os.path.join(ROOT, folder, "hero-wood.jpg"), quality=84, optimize=True)

    chk = np.asarray(img).astype(float).mean(2)
    q = [chk[:H // 2, :W // 2].mean(), chk[:H // 2, W // 2:].mean(),
         chk[H // 2:, :W // 2].mean(), chk[H // 2:, W // 2:].mean()]
    kb = os.path.getsize(os.path.join(ROOT, "tier2/assets/hero-wood.jpg")) // 1024
    print(f"hero-wood.jpg  {img.size[0]}x{img.size[1]}  {kb} KB")
    print("  quadrant means: " + "  ".join(f"{v:.1f}" for v in q) +
          f"   spread {max(q) - min(q):.1f}  (was ~19 before flattening)")


if __name__ == "__main__":
    main()
