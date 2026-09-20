"""Assemble site/ (what GitHub Pages serves) from tier1, tier2, planB, planC. noindex on every page."""
import pathlib, shutil
root = pathlib.Path(__file__).resolve().parent.parent
site = root / 'site'
if site.exists():
    shutil.rmtree(site)
site.mkdir()
NOINDEX = '<meta name="robots" content="noindex,nofollow">'


def page(src, dst, subdir):
    s = src.read_text(encoding='utf-8')
    if NOINDEX not in s:
        s = s.replace('<meta name="viewport" content="width=device-width,initial-scale=1">',
                      '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + NOINDEX, 1)
    if subdir:
        s = s.replace('"assets/', '"../assets/').replace('url(assets/', 'url(../assets/')
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(s, encoding='utf-8')


page(root / 'tier1' / 'index.html', site / 'index.html', False)
shutil.copytree(root / 'tier1' / 'assets', site / 'assets', ignore=shutil.ignore_patterns('*.png', '!cicada-mark.png'))
shutil.copy(root / 'tier1' / 'assets' / 'cicada-mark.png', site / 'assets' / 'cicada-mark.png')
shutil.copy(root / 'tier1' / 'works.json', site / 'works.json')
page(root / 'tier2' / 'index.html', site / 'film' / 'index.html', True)
shutil.copytree(root / 'tier2' / 'frames', site / 'film' / 'frames')
(site / 'film' / 'works.json').write_text(
    (root / 'tier2' / 'works.json').read_text(encoding='utf-8').replace('"assets/', '"../assets/'),
    encoding='utf-8')
for name, folder in (('field-guide', 'planB'), ('living-plates', 'planB2'), ('healed', 'planC')):
    page(root / folder / 'index.html', site / name / 'index.html', False)
    shutil.copytree(root / folder / 'assets', site / name / 'assets', ignore=shutil.ignore_patterns('logo.jpg', 'hero-logo.jpg', 'shop-chair.jpg'))
(site / '.nojekyll').touch()
missing = []
import re
for html in site.rglob('index.html'):
    for ref in re.findall(r'(?:src|href|data-full)="((?:\.\./)?(?:assets|sheets)/[^"]+)"', html.read_text(encoding='utf-8')):
        if not (html.parent / ref).resolve().exists():
            missing.append(f'{html.relative_to(site)} -> {ref}')
print('\n'.join(missing) if missing else 'all local references resolve')
