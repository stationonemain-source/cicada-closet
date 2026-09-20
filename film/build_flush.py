"""Flush hero: one sheet of kraft paper, her logo printed straight onto it.

No card, no shadow, no edges. The background is kraft and the logo's own background is kraft,
so the only way this works is if the two are the same paper -- otherwise the logo's square
shows. So:

  * the background is generated (not tiled) to the exact tone of HER file's kraft, measured
    from the blank corners of logo_new.webp, with grain matched to the swatch's statistics.
    Generated rather than repeated because a 61x72 swatch tiled across a screen shows a grid.
  * her logo gets a feathered alpha border. Only the blank margin is touched -- the feather
    never reaches the artwork -- so the square dissolves into the background instead of ending.

Outputs assets/hero-kraft.jpg and assets/logo-flush.webp, and prints the engine's constants.

Usage: python film/build_flush.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PLATE = (2400, 1500)
FEATHER = 0.075          # fraction of the logo's width faded out at the border
SEED = 11


def kraft_tone():
    """The paper her artwork actually sits on, from its blank corners."""
    a = np.asarray(Image.open(os.path.join(HERE, "logo_new.webp")).convert("RGB")).astype(float)
    h, w, _ = a.shape
    p = np.concatenate([a[0:90, 0:90].reshape(-1, 3), a[0:90, w - 90:].reshape(-1, 3),
                        a[h - 90:, 0:90].reshape(-1, 3), a[h - 90:, w - 90:].reshape(-1, 3)])
    return p.mean(0), p.std(0).mean()


def grain(shape, sigma, rng):
    n = rng.normal(0, 1, shape)
    n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(sigma))).astype(float)
    n = (n - n.mean()) / (n.std() + 1e-6)
    return n


def main():
    tone, spread = kraft_tone()
    rng = np.random.default_rng(SEED)
    W, H = PLATE

    fine = grain((H, W), 0.9, rng)          # fibre
    soft = grain((H, W), 7.0, rng)          # the faint mottle real paper has
    field = 1.0 + (fine * 0.72 + soft * 0.42) * (spread / 255.0) * 1.35

    plate = np.clip(field[..., None] * tone, 0, 255)
    img = Image.fromarray(plate.astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        img.save(os.path.join(ROOT, folder, "hero-kraft.jpg"), quality=88, optimize=True)

    # ---- her logo, with only its blank margin feathered so the square dissolves
    logo = Image.open(os.path.join(HERE, "logo_new.webp")).convert("RGBA")
    LW, LH = logo.size
    f = int(LW * FEATHER)
    ramp = np.ones((LH, LW))
    edge = np.linspace(0, 1, f) ** 1.4
    ramp[:, :f] *= edge
    ramp[:, -f:] *= edge[::-1]
    ramp[:f, :] *= edge[:, None]
    ramp[-f:, :] *= edge[::-1][:, None]
    a = np.asarray(logo).astype(float)
    a[..., 3] = a[..., 3] * ramp
    flush = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        flush.save(os.path.join(ROOT, folder, "logo-flush.webp"), quality=92, method=6)

    chk = np.asarray(img).astype(float)
    q = [chk[:H // 2, :W // 2].mean(), chk[:H // 2, W // 2:].mean(),
         chk[H // 2:, :W // 2].mean(), chk[H // 2:, W // 2:].mean()]
    kb = os.path.getsize(os.path.join(ROOT, "tier2/assets/hero-kraft.jpg")) // 1024
    lb = os.path.getsize(os.path.join(ROOT, "tier2/assets/logo-flush.webp")) // 1024
    print(f"hero-kraft.jpg  {W}x{H}  {kb} KB   tone {tone.round(1)}  spread {max(q) - min(q):.2f}")
    print(f"logo-flush.webp {LW}x{LH}  {lb} KB   feather {f}px of blank margin only")
    print(f"  page background colour: #{int(tone[0]):02x}{int(tone[1]):02x}{int(tone[2]):02x}")


if __name__ == "__main__":
    main()
