"""Lift Jenna's ink off the skin, from her own photographs (no redrawing).

For each tattoo:  ink alpha = local contrast against a blurred skin estimate (dark ink + colour ink)
                  x limb/subject mask from Higgsfield's background remover (eroded)
                  x a density mask that drops isolated freckles far from the design.
Writes, per piece:   assets/<name>-ink.png   colour cutout (RGBA), what the plate "fills in" with
                     assets/<name>-line.png  sepia line layer (RGBA) derived from the same alpha
Also makes the studio plate's line layer from edges of the shop photo.
"""
import pathlib, sys
import numpy as np
from PIL import Image, ImageFilter

here = pathlib.Path(__file__).resolve().parent
root = here.parent
posts = root / 'ref' / 'posts'
out = here / 'assets'; out.mkdir(exist_ok=True)
SEPIA = np.array([58, 42, 30], np.float32)
CLEAR = {'stag-beetle-seraphim': [(0, 0, .35, .12), (.55, 0, 1, .07)]}  # stray marks outside the design, as fractions
MAX = 1000


def load_rgb(p):
    im = Image.open(p).convert('RGB'); im.thumbnail((MAX, MAX), Image.LANCZOS); return im


def trim(rgba, pad=24):
    bb = rgba.getbbox()
    if not bb: return rgba
    x0, y0, x1, y1 = bb
    return rgba.crop((max(0, x0 - pad), max(0, y0 - pad), min(rgba.width, x1 + pad), min(rgba.height, y1 + pad)))


def tattoo(name, erode=21, dark_off=14, chroma_off=30, density=0.10, line_off=18):
    im = load_rgb(posts / f'{name}.jpg')
    a = np.asarray(im).astype(np.float32)
    bg = np.asarray(im.filter(ImageFilter.GaussianBlur(26))).astype(np.float32)
    lum, bgl = a @ [.299, .587, .114], bg @ [.299, .587, .114]
    dark = np.clip((bgl - lum - dark_off) / 55.0, 0, 1)
    chroma = np.clip((np.linalg.norm(a - bg, axis=2) - chroma_off) / 50.0, 0, 1)
    alpha = np.maximum(dark, chroma)
    outline = np.clip((bgl - lum - line_off) / 42.0, 0, 1)
    # subject mask from Higgsfield background remover
    lp = here / 'work' / f'{name}-limb.png'
    limb = Image.open(lp).convert('RGBA').split()[3].resize(im.size, Image.LANCZOS) if lp.exists() else Image.new('L', im.size, 255)
    if erode >= 3:
        limb = limb.filter(ImageFilter.MinFilter(erode)).filter(ImageFilter.GaussianBlur(6))
    m = np.asarray(limb).astype(np.float32) / 255.0
    alpha *= m
    outline *= m
    # density: keep strokes that belong to the design, drop lone freckles
    A = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))
    alpha = np.asarray(A).astype(np.float32) / 255.0
    dens = np.asarray(A.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255.0
    keep = np.clip((dens - density) / 0.10, 0, 1)
    alpha *= keep
    outline *= keep
    alpha = np.clip(alpha * 1.15, 0, 1)
    O = Image.fromarray((outline * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))
    for box in CLEAR.get(name, []):
        x0, y0, x1, y1 = (int(box[0] * im.width), int(box[1] * im.height), int(box[2] * im.width), int(box[3] * im.height))
        O.paste(0, (x0, y0, x1, y1))
    line_a = np.clip(np.asarray(O).astype(np.float32) / 255.0 * 1.2, 0, 1)
    line = Image.fromarray(np.dstack([np.broadcast_to(SEPIA, a.shape), line_a * 235]).astype(np.uint8), 'RGBA')
    # full frame, pixel-aligned with the photo so the drawing can turn into it in place
    line.save(out / f'{name}-line.png', optimize=True)
    im.save(out / f'{name}.jpg', quality=86, optimize=True, progressive=True)
    return im.size


def studio_lines():
    im = Image.open(root / 'tier1' / 'assets' / 'shop-gallery.jpg').convert('RGB')
    im = im.crop((0, int(im.height * .285), int(im.width * .62), int(im.height * .60)))  # the sharp room only: no blurred ceiling, ornament or lower graphic
    im.thumbnail((MAX, MAX), Image.LANCZOS)
    g = im.convert('L').filter(ImageFilter.GaussianBlur(1.2))
    e = np.asarray(g.filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    a = np.clip((e - 10) / 40.0, 0, 1)
    line = Image.fromarray(np.dstack([np.broadcast_to(SEPIA, (im.height, im.width, 3)), a * 225]).astype(np.uint8), 'RGBA')
    line.save(out / 'studio-line.png', optimize=True)
    im.save(out / 'studio.jpg', quality=84, optimize=True, progressive=True)
    return im.size


if __name__ == '__main__':
    TUNE = {'bluebird': dict(erode=3, density=0.06), 'luna-moth': dict(erode=61, density=0.10),
            'stag-beetle-seraphim': dict(erode=41), 'pink-skies': dict(erode=41, chroma_off=34),
            'salamander': dict(erode=1, density=0.04, line_off=22)}
    names = sys.argv[1:] or list(TUNE)
    for n in names:
        print(n, tattoo(n, **TUNE.get(n, {})))
    print('studio', studio_lines())
