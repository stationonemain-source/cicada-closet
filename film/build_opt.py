"""Optimised hero assets.

The first 3D build shipped a 3840x2160 kraft plate (1.4 MB) for what is, visually, paper
grain -- and paper grain repeats perfectly. So the field becomes a small SEAMLESS tile
instead. Seamless matters: an ordinary Gaussian blur is not periodic and leaves a visible
grid, so the grain is filtered in the frequency domain, which wraps by construction.

Her logo textures are recompressed: the 4K carries the detail that keeps the keyhole sharp
at the end of the push, so it stays 4096, just at a sane quality.

Usage: python film/build_opt.py
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TILE = 1024
SEED = 11


def periodic_grain(n, sigma, rng):
    """Gaussian-filtered noise that tiles: filtering in frequency space wraps by construction."""
    w = rng.normal(0, 1, (n, n))
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.fftfreq(n)[None, :]
    k = np.exp(-2.0 * (np.pi * sigma) ** 2 * (fx ** 2 + fy ** 2))
    g = np.real(np.fft.ifft2(np.fft.fft2(w) * k))
    return (g - g.mean()) / (g.std() + 1e-9)


def main():
    lg = np.asarray(Image.open(os.path.join(HERE, "logo_new.webp")).convert("RGB")).astype(float)
    lh, lw, _ = lg.shape
    corners = np.concatenate([lg[0:90, 0:90].reshape(-1, 3), lg[0:90, lw - 90:].reshape(-1, 3),
                              lg[lh - 90:, 0:90].reshape(-1, 3), lg[lh - 90:, lw - 90:].reshape(-1, 3)])
    tone, spread = corners.mean(0), corners.std(0).mean()

    rng = np.random.default_rng(SEED)
    field = 1.0 + (periodic_grain(TILE, 0.7, rng) * 0.72
                   + periodic_grain(TILE, 4.0, rng) * 0.38) * (spread / 255.0) * 1.35
    tile = Image.fromarray(np.clip(field[..., None] * tone, 0, 255).astype(np.uint8))
    for folder in ("tier1/assets", "tier2/assets"):
        tile.save(os.path.join(ROOT, folder, "kraft-tile.jpg"), quality=86, optimize=True)

    # seam check: the right edge against the left, and the bottom against the top
    a = np.asarray(tile).astype(int)
    seam_x = np.abs(a[:, -1] - a[:, 0]).mean()
    seam_y = np.abs(a[-1, :] - a[0, :]).mean()
    interior = np.abs(a[:, 1:] - a[:, :-1]).mean()

    src = Image.open(os.path.join(ROOT, "tier2/assets/logo-3d-4k.webp")).convert("RGBA")
    for name, size, q in (("logo-3d-4k.webp", 4096, 80), ("logo-3d-2k.webp", 2048, 80)):
        im = src if src.size[0] == size else src.resize((size, size), Image.LANCZOS)
        for folder in ("tier1/assets", "tier2/assets"):
            im.save(os.path.join(ROOT, folder, name), quality=q, method=6)

    def kb(f):
        return os.path.getsize(os.path.join(ROOT, "tier2/assets", f)) // 1024

    print(f"kraft-tile.jpg   {TILE}x{TILE}  {kb('kraft-tile.jpg')} KB   (was hero-kraft.jpg 1398 KB)")
    print(f"  seam: edge diff x {seam_x:.2f} y {seam_y:.2f} vs interior {interior:.2f}  (<= interior = invisible)")
    print(f"logo-3d-4k.webp  {kb('logo-3d-4k.webp')} KB     logo-3d-2k.webp  {kb('logo-3d-2k.webp')} KB")


if __name__ == "__main__":
    main()
