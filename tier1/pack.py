"""Convert upscaled PNG plates into web JPEGs (max 1800px) for tier1 and tier2, plus the hero."""
import pathlib
from PIL import Image
here = pathlib.Path(__file__).parent
a = here/'assets'
t2 = here.parent/'tier2'/'assets'; t2.mkdir(exist_ok=True)
key = here.parent/'film'/'keys'/'key01.png'
def save(im, name):
    im = im.convert('RGB'); im.thumbnail((1800, 1800), Image.LANCZOS)
    for d in (a, t2): im.save(d/name, quality=84, optimize=True, progressive=True)
    print(name, im.size)
save(Image.open(key), 'hero-logo.jpg')
for p in sorted(a.glob('*.png')):
    save(Image.open(p), p.stem + '.jpg')
