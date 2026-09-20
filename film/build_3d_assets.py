"""4K assets for the 3D hero.

Her logo, upscaled to 4096 by Higgsfield's upscaler (verified against the original: mean
abs diff 7.3, so the linework is hers), gets the keyhole punched OUT to transparency. In the
3D scene that hole is a real opening -- there is a dark volume behind the paper, so as the
camera pushes in you see INTO the keyhole with parallax rather than at a black shape painted
on a flat picture. That parallax is the whole difference between 3D and a zoom.

Also regenerates the kraft surface at 4K, at the exact tone of her paper.

Outputs (tier1/assets + tier2/assets):
  logo-3d-4k.webp / logo-3d-2k.webp  — her logo, keyhole punched, edges feathered
  hero-kraft.jpg                      — 3840x2160 paper at her tone

Usage: python film/build_3d_assets.py
"""
import os
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PLATE = (3840, 2160)
FEATHER = 0.075
SEED = 11


def punch_keyhole(img):
    """Flood the keyhole's black region and return it as an alpha hole (feathered 3px)."""
    a = np.asarray(img.convert("RGB")).astype(int)
    h, w, _ = a.shape
    dark = a.sum(2) < 90
    # start at the thorax, where the keyhole is
    sy, sx = int(h * 0.366), int(w * 0.499)
    if not dark[sy, sx]:
        found = None
        for r in range(1, 240):
            for dy in (-r, r):
                if dark[sy + dy, sx]:
                    found = (sy + dy, sx)
                    break
            if found:
                break
        sy, sx = found
    seen = np.zeros_like(dark)
    q = deque([(sy, sx)])
    seen[sy, sx] = 1
    pts = []
    while q:
        y, x = q.popleft()
        pts.append((y, x))
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and dark[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1
                q.append((ny, nx))
    p = np.array(pts)
    mask = np.zeros((h, w), np.uint8)
    mask[p[:, 0], p[:, 1]] = 255
    box = (p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max())
    return Image.fromarray(mask).filter(ImageFilter.GaussianBlur(2.5)), box, len(pts)


def main():
    src = Image.open(os.path.join(HERE, "logo_4k.png")).convert("RGBA")
    W, H = src.size
    hole, box, n = punch_keyhole(src)

    a = np.asarray(src).astype(float)
    hm = np.asarray(hole).astype(float) / 255.0
    a[..., 3] = a[..., 3] * (1.0 - hm)                     # the keyhole becomes an opening

    f = int(W * FEATHER)                                    # blank margin only, never the art
    ramp = np.ones((H, W))
    edge = np.linspace(0, 1, f) ** 1.4
    ramp[:, :f] *= edge
    ramp[:, -f:] *= edge[::-1]
    ramp[:f, :] *= edge[:, None]
    ramp[-f:, :] *= edge[::-1][:, None]
    a[..., 3] *= ramp

    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        out.save(os.path.join(ROOT, folder, "logo-3d-4k.webp"), quality=90, method=6)
        out.resize((2048, 2048), Image.LANCZOS).save(
            os.path.join(ROOT, folder, "logo-3d-2k.webp"), quality=90, method=6)

    # ---- 4K paper, at the tone of her own kraft
    lg = np.asarray(Image.open(os.path.join(HERE, "logo_new.webp")).convert("RGB")).astype(float)
    lh, lw, _ = lg.shape
    corners = np.concatenate([lg[0:90, 0:90].reshape(-1, 3), lg[0:90, lw - 90:].reshape(-1, 3),
                              lg[lh - 90:, 0:90].reshape(-1, 3), lg[lh - 90:, lw - 90:].reshape(-1, 3)])
    tone, spread = corners.mean(0), corners.std(0).mean()
    rng = np.random.default_rng(SEED)
    PW, PH = PLATE

    def grain(sigma):
        n = rng.normal(0, 1, (PH, PW))
        n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(sigma))).astype(float)
        return (n - n.mean()) / (n.std() + 1e-6)

    field = 1.0 + (grain(1.4) * 0.72 + grain(11.0) * 0.42) * (spread / 255.0) * 1.35
    plate = Image.fromarray(np.clip(field[..., None] * tone, 0, 255).astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        plate.save(os.path.join(ROOT, folder, "hero-kraft.jpg"), quality=86, optimize=True)

    kb4 = os.path.getsize(os.path.join(ROOT, "tier2/assets/logo-3d-4k.webp")) // 1024
    kb2 = os.path.getsize(os.path.join(ROOT, "tier2/assets/logo-3d-2k.webp")) // 1024
    kbp = os.path.getsize(os.path.join(ROOT, "tier2/assets/hero-kraft.jpg")) // 1024
    print(f"logo-3d-4k.webp  {W}x{H}  {kb4} KB     logo-3d-2k.webp 2048x2048  {kb2} KB")
    print(f"hero-kraft.jpg   {PW}x{PH}  {kbp} KB   tone {tone.round(1)}")
    print(f"keyhole punched: {n} px, bbox {box}")
    print(f"  KX={((box[0] + box[2]) / 2) / W:.4f}  KY={((box[1] + box[3]) / 2) / H:.4f}"
          f"  KW={(box[2] - box[0]) / W:.4f}  KH={(box[3] - box[1]) / H:.4f}")


if __name__ == "__main__":
    main()
