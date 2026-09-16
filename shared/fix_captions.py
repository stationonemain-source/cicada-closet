"""Swap in Instagram originals and correct plate names to Jenna's own captions; re-sync tier2 pieces."""
import pathlib, re, shutil
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent
posts = root / 'ref' / 'posts'

# originals -> web jpgs (real pixels beat upscales)
for name in ['luna-moth', 'stag-beetle-seraphim', 'bluebird', 'pink-skies', 'salamander', 'murals', 'jenna']:
    im = Image.open(posts / f'{name}.jpg').convert('RGB'); im.thumbnail((1600, 1600), Image.LANCZOS)
    for d in ('tier1', 'tier2'):
        im.save(root / d / 'assets' / f'{name}.jpg', quality=86, optimize=True, progressive=True)
for d in ('tier1', 'tier2'):
    for old in ['moth-of-eyes', 'sparrow', 'sunset-mirror', 'cicada-paintings']:
        p = root / d / 'assets' / f'{old}.jpg'
        if p.exists(): p.unlink()

PLATES = [
    ('luna-moth', 'Luna moth', 'colour', 'Chappell-inspired luna moth · colour tattoo, July 2026',
     'Colour tattoo of a teal luna moth with a gold crescent moon and green sprigs'),
    ('stag-beetle-seraphim', 'Stag beetle seraphim', 'black &amp; grey', 'Stag beetle seraphim · tattoo, July 2025',
     'Black and grey tattoo of a stag beetle with six wings patterned with eyes'),
    ('bluebird', 'Bluebird', 'black &amp; grey', 'Bluebird · tattoo, September 2026',
     'Black and grey tattoo of a bluebird in flight on an upper arm'),
    ('pink-skies', 'Pink skies', 'colour', 'Pink skies · colour tattoo, July 2026',
     'Colour tattoo of a pink sunset over a river, framed in an ornate gilt mirror'),
    ('salamander', 'Salamander', 'on paper', 'Salamander · watercolour and Micron pen on paper, July 2026',
     'Watercolour and ink drawing of a black salamander with yellow spots curled on a dry oak leaf'),
    ('murals', 'Murals for Mira', 'paint', 'Murals painted for Mira’s room · July 2026',
     'Two painted murals on a rust ground: cicadas, morning glories, strawberries and hearts'),
]


def plates_html():
    out = []
    for f, title, kind, cap, alt in PLATES:
        out.append(f'      <button class="plate tall reveal" data-full="assets/{f}.jpg" data-cap="{cap}"><figure><div class="img">'
                   f'<img src="assets/{f}.jpg" alt="{alt}" loading="lazy"></div><figcaption><b>{title}</b><span>{kind}</span></figcaption></figure></button>')
    return '\n'.join(out)


t1 = root / 'tier1' / 'index.html'
s = t1.read_text(encoding='utf-8')
s, n = re.subn(r'(<div class="plates">\n).*?(\n\s*</div>\n\s*<p style="margin-top:34px)', lambda m: m.group(1) + plates_html() + m.group(2), s, flags=re.S)
assert n == 1, 'plates block not found'
s = s.replace('luna moths, sparrows, salamanders, morning glories, marigolds and, fittingly, cicadas.',
              'luna moths, bluebirds, stag beetles, salamanders, morning glories and, fittingly, cicadas.')
s = s.replace('whose work leans toward moths, birds and botanicals, in fine line and in colour.',
              'whose work leans toward moths, birds, beetles and botanicals, in black and grey and in colour.')
t1.write_text(s, encoding='utf-8')

style = s.split('<style>')[1].split('</style>')[0]
body = s.split('<main id="top">')[1].split('</main>')[0]
t2 = root / 'tier2'
(t2 / '_style.css').write_text(style, encoding='utf-8')
(t2 / '_after.html').write_text(body.split('</section>', 1)[1], encoding='utf-8')
(t2 / '_footer.html').write_text('<footer>' + s.split('<footer>')[1].split('</footer>')[0] + '</footer>', encoding='utf-8')
(t2 / '_dialog.html').write_text('<dialog id="lb">' + s.split('<dialog id="lb">')[1].split('</dialog>')[0] + '</dialog>', encoding='utf-8')
e = t2 / '_engine.html'
es = e.read_text(encoding='utf-8')
es = es.replace('<p>Luna moths, marigolds, sparrows, salamanders.</p>', '<p>Luna moths, bluebirds, stag beetles, salamanders.</p>')
es = es.replace('<h2>Moths, birds and botanicals.</h2><p>Fine-line and colour work by Jenna Feezel, BFA.</p>',
                '<h2>Moths, birds and botanicals.</h2><p>Black and grey and colour work by Jenna Feezel, BFA.</p>')
e.write_text(es, encoding='utf-8')
for bad in ['Moth of eyes', 'Sparrow', 'sunset-mirror', 'Cicada studies', 'sparrows']:
    assert bad not in s and bad not in es, bad
print('captions fixed')
