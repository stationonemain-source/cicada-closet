"""Lay her logo on the desk as a real card: perspective, one light, contact shadow, depth.

The round-2 card was her artwork square-on to the camera with a shadow under it, which is
why it read flat, and why the join with the wood showed as a tonal step. Here the artwork is
warped onto the table plane, lit by the same light as the wood photo (upper-left), given a
contact shadow that follows its own silhouette, a lit near edge for paper thickness, and a
touch of defocus toward the far edge. Nothing is redrawn: her file is warped, never repainted.

Output: assets/logo-card.webp (transparent) + the keyhole's position inside it, which the
page's engine scales about.

Usage: python film/build_card3d.py
"""
import os

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "logo_new.webp")

BOTTOM_W = 2000          # near edge of the card, in card-asset pixels
TOP_SHRINK = 0.845       # far edge is shorter -- this is the whole perspective
HEIGHT_F = 0.74          # foreshortening of a square lying on the table
TILT_DEG = 2.4           # a little off-square, so it reads as placed, not pasted
MARGIN = 330             # room for the cast shadow


def find_coeffs(dst, src):
    """Homography coefficients mapping dst -> src (the direction PIL wants)."""
    m = []
    for (dx, dy), (sx, sy) in zip(dst, src):
        m.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy])
        m.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy])
    A = np.array(m, dtype=float)
    B = np.array(src, dtype=float).reshape(8)
    return np.linalg.solve(A.T @ A, A.T @ B)


def apply_h(h, x, y):
    d = h[6] * x + h[7] * y + 1.0
    return ((h[0] * x + h[1] * y + h[2]) / d, (h[3] * x + h[4] * y + h[5]) / d)


def keyhole_box(img):
    from collections import deque
    a = np.asarray(img.convert("RGB")).astype(int)
    h, w, _ = a.shape
    dark = a.sum(2) < 70
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
    logo = Image.open(SRC).convert("RGBA")
    LW, LH = logo.size
    kx0, ky0, kx1, ky1 = keyhole_box(logo)

    card_h = BOTTOM_W * HEIGHT_F
    top_w = BOTTOM_W * TOP_SHRINK
    inset = (BOTTOM_W - top_w) / 2.0
    quad = [(inset, 0.0), (inset + top_w, 0.0), (BOTTOM_W, card_h), (0.0, card_h)]

    # a small tilt, about the card's centre
    cx, cy = BOTTOM_W / 2, card_h / 2
    t = np.radians(TILT_DEG)
    quad = [((x - cx) * np.cos(t) - (y - cy) * np.sin(t) + cx,
             (x - cx) * np.sin(t) + (y - cy) * np.cos(t) + cy) for x, y in quad]

    xs = [p[0] for p in quad]
    ys = [p[1] for p in quad]
    ox, oy = MARGIN - min(xs), MARGIN - min(ys)
    quad = [(x + ox, y + oy) for x, y in quad]
    OW = int(max(p[0] for p in quad) + MARGIN)
    OH = int(max(p[1] for p in quad) + MARGIN)

    src_corners = [(0, 0), (LW, 0), (LW, LH), (0, LH)]
    coeffs = find_coeffs(quad, src_corners)
    warped = logo.transform((OW, OH), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    # ---- one light, from the upper left, same as the wood plate
    a = np.asarray(warped).astype(float)
    rgb, alpha = a[..., :3], a[..., 3:4]
    yy, xx = np.mgrid[0:OH, 0:OW]
    lit = 1.10 - 0.13 * (xx / OW) - 0.08 * (yy / OH)          # brighter near the light
    rgb = np.clip(rgb * lit[..., None], 0, 255)
    warped = Image.fromarray(np.concatenate([rgb, alpha], 2).astype(np.uint8))

    # ---- defocus toward the far edge, so the card has depth like the table does
    soft = warped.filter(ImageFilter.GaussianBlur(2.1))
    top_y = min(p[1] for p in quad)
    fade = np.clip(1.0 - (yy - top_y) / (card_h * 0.30), 0, 1) ** 2.0
    warped = Image.composite(soft, warped, Image.fromarray((fade * 255).astype(np.uint8)))

    # ---- shadow: the card's own silhouette, thrown down and right, twice
    sil = warped.split()[3]
    shadow = Image.new("RGBA", (OW, OH), (0, 0, 0, 0))
    for off, blur, al in (((10, 16), 15, 150), ((34, 54), 62, 112)):
        lay = Image.new("RGBA", (OW, OH), (0, 0, 0, 0))
        m = ImageChops.offset(sil, *off).filter(ImageFilter.GaussianBlur(blur))
        lay.paste((9, 6, 4, al), (0, 0), m)
        shadow = Image.alpha_composite(shadow, lay)

    out = Image.alpha_composite(shadow, warped)

    # ---- paper thickness: the near edge catches the light, and darkens where it meets wood
    d = ImageDraw.Draw(out)
    bl, br = quad[3], quad[2]
    d.line([bl, br], fill=(247, 236, 214, 190), width=4)
    d.line([(bl[0], bl[1] + 4), (br[0], br[1] + 4)], fill=(38, 25, 16, 140), width=3)

    for folder in ("tier1/assets", "tier2/assets"):
        out.save(os.path.join(ROOT, folder, "logo-card.webp"), quality=88, method=6)

    # ---- where the keyhole landed
    h_fwd = find_coeffs(src_corners, quad)
    kcx, kcy = apply_h(h_fwd, (kx0 + kx1) / 2, (ky0 + ky1) / 2)
    kl, _ = apply_h(h_fwd, kx0, (ky0 + ky1) / 2)
    kr, _ = apply_h(h_fwd, kx1, (ky0 + ky1) / 2)
    kb = os.path.getsize(os.path.join(ROOT, "tier2/assets/logo-card.webp")) // 1024
    print(f"logo-card.webp  {OW}x{OH}  {kb} KB")
    print(f"  KX={kcx / OW:.4f}  KY={kcy / OH:.4f}  KW={(kr - kl) / OW:.4f}")
    print(f"  AW={BOTTOM_W / OW:.4f}  AH={card_h / OH:.4f}   (card extent inside the asset)")


if __name__ == "__main__":
    main()
