"""Assemble site/ (what GitHub Pages serves).

LIVE since 2026-09-24 on Jenna's own domain (Station Care Plan): the film IS the homepage at
https://thecicadacloset.com/, indexable, with canonical/og pointing at the domain. /film/ forwards to /.
The spec alternates (classic, field-guide, living-plates, healed) are no longer deployed -- their
sources stay in this workspace. /handover/ (her plan guide) stays deployed, noindex."""
import pathlib, shutil
root = pathlib.Path(__file__).resolve().parent.parent
site = root / 'site'
if site.exists():
    shutil.rmtree(site)
site.mkdir()
NOINDEX = '<meta name="robots" content="noindex,nofollow">'
DOMAIN = 'thecicadacloset.com'
ORIGIN = 'https://' + DOMAIN + '/'


def page(src, dst, subdir):
    s = src.read_text(encoding='utf-8')
    if NOINDEX not in s:
        s = s.replace('<meta name="viewport" content="width=device-width,initial-scale=1">',
                      '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + NOINDEX, 1)
    if subdir:
        s = s.replace('"assets/', '"../assets/').replace('url(assets/', 'url(../assets/')
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(s, encoding='utf-8')


# The film is THE site (client, 2026-09-20) and lives at the root of her domain (2026-09-24).
# tier2 is authored for the root, so no path rewriting is needed here.
film = (root / 'tier2' / 'index.html').read_text(encoding='utf-8')
for a, b in (
    ('<meta property="og:image" content="assets/hero-logo.jpg">',
     '<link rel="canonical" href="' + ORIGIN + '">\n'
     '<meta property="og:type" content="website">\n'
     '<meta property="og:url" content="' + ORIGIN + '">\n'
     '<meta property="og:image" content="' + ORIGIN + 'assets/hero-logo.jpg">'),
    ('"image":"assets/hero-logo.jpg"}', '"image":"' + ORIGIN + 'assets/hero-logo.jpg","url":"' + ORIGIN + '"}'),
):
    assert a in film, a
    film = film.replace(a, b, 1)
assert NOINDEX not in film
(site / 'index.html').write_text(film, encoding='utf-8')
shutil.copy(root / 'tier2' / 'hero3d.js', site / 'hero3d.js')
shutil.copy(root / 'tier2' / 'works.json', site / 'works.json')
shutil.copytree(root / 'tier1' / 'assets', site / 'assets', ignore=shutil.ignore_patterns('*.png', '!cicada-mark.png'))
shutil.copy(root / 'tier1' / 'assets' / 'cicada-mark.png', site / 'assets' / 'cicada-mark.png')
# old links (the preview we sent, /film/) keep working
(site / 'film').mkdir()
(site / 'film' / 'index.html').write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">\n'
    + NOINDEX + '\n<link rel="canonical" href="' + ORIGIN + '">\n'
    '<meta http-equiv="refresh" content="0; url=../">\n'
    '<script>location.replace("../" + location.hash)</script>\n'
    '<title>The Cicada Closet</title></head>\n'
    '<body><p><a href="../">Enter The Cicada Closet</a></p></body></html>\n',
    encoding='utf-8')
(site / 'CNAME').write_text(DOMAIN + '\n', encoding='utf-8')
(site / 'robots.txt').write_text(
    'User-agent: *\nDisallow: /handover/\n\nSitemap: ' + ORIGIN + 'sitemap.xml\n', encoding='utf-8')
(site / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url><loc>' + ORIGIN + '</loc></url>\n</urlset>\n', encoding='utf-8')
# Jenna's handover guide (09-23). Source is an artifact body (no <head>), so give it a full document here.
guide = (root / 'shared' / 'handover-guide.html').read_text(encoding='utf-8')
(site / 'handover').mkdir(parents=True, exist_ok=True)
(site / 'handover' / 'index.html').write_text(
    '<!doctype html>\n<html lang="en"><head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    + NOINDEX + '\n' + guide.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body></html>\n',
    encoding='utf-8')
(site / '.nojekyll').touch()
missing = []
import re
for html in site.rglob('index.html'):
    for ref in re.findall(r'(?:src|href|data-full)="((?:\.\./)?(?:assets|sheets)/[^"]+)"', html.read_text(encoding='utf-8')):
        if not (html.parent / ref).resolve().exists():
            missing.append(f'{html.relative_to(site)} -> {ref}')
print('\n'.join(missing) if missing else 'all local references resolve')
