"""Build planB2/index.html (Plan B · The Living Plates, tier 2)."""
import pathlib, sys, html
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / 'shared'))
import build_nav as N

ns = {'__file__': str(here.parent / 'planB' / 'build.py')}
exec((here.parent / 'planB' / 'build.py').read_text(encoding='utf-8').split('\ndef spread')[0], ns)
IG, PLATES = ns['IG'], ns['PLATES']
ITEMS = [dict(p, rows=[('Medium', p['medium']), ('Posted', p['posted'])], link=(IG.format(p['post']), 'See the post on Instagram')) for p in PLATES]
ITEMS.append(dict(n='VII', file='studio', name='The Studio', latin='755 South Jenkins Avenue, Norman',
                  alt='Inside The Cicada Closet: deep green walls hung with framed work by local artists',
                  rows=[('Opened', 'July 2026'), ('Gallery', 'Open to local artists')],
                  note='The studio opened with Grillin&rsquo; &amp; Chillin&rsquo;, a grand opening and art show, on Saturday the eleventh of July, 2026. Its small gallery wall is open to local artists, who keep all of their sales, with no commissions and no fees.',
                  link=('https://www.instagram.com/thecicadacloset/', 'The studio on Instagram')))


def panel(i, p):
    line = here / 'assets' / f"{p['file']}-line.png"
    line_img = f'<img class="line" src="assets/{p["file"]}-line.png" alt="" aria-hidden="true">' if line.exists() else ''
    rows = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in p['rows'])
    from PIL import Image
    w, h = Image.open(here / 'assets' / f"{p['file']}.jpg").size
    wide = ' wide' if w > h else ''
    return f'''      <div class="panel plate" id="plate-{i + 1}">
        <article class="spread" aria-labelledby="pl{i + 1}">
          <div class="plate-page">
            <span class="plate-no">Plate {p['n']}</span>
            <div class="stack{wide}">
              <img class="ghost" src="assets/{p['file']}.jpg" alt="" aria-hidden="true">
              {line_img}
              <img class="photo" src="assets/{p['file']}.jpg" alt="{p['alt']}" decoding="async">
              <svg aria-hidden="true"><rect x="0.5%" y="0.5%" width="99%" height="99%" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><rect class="inner" x="2.5%" y="2%" width="95%" height="96%" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
            </div>
            <span class="plate-cap">From the artist&rsquo;s photograph.</span>
          </div>
          <div class="text-page">
            <span class="num" aria-hidden="true">{p['n']}</span>
            <h3 id="pl{i + 1}">{p['name']}</h3>
            <p class="latin">{p['latin']}</p>
            <dl>{rows}</dl>
            <p class="nt">{p['note']}</p>
            <a class="src" href="{p['link'][0]}" target="_blank" rel="noopener">{p['link'][1]}</a>
          </div>
        </article>
      </div>'''


LINKS = [('#work', 'Plates', 'I to VII'), ('#artist', 'Artist', 'Colophon'), ('#book', 'Booking', 'Appendix A'), ('#care', 'Aftercare', 'Appendix B')]
OVERRIDES = '''
.nav[data-mode="solid"]{-webkit-backdrop-filter:none;backdrop-filter:none;background:rgba(232,226,209,.97)}
.nav-links a{font-size:16px;letter-spacing:.06em;text-transform:none}
.nav-book,.nav-toggle{font-size:15px;letter-spacing:.06em;text-transform:none}
.nav-mark span{font-size:21px}
.nav-sheet nav a small{font-size:14px;letter-spacing:.06em;text-transform:none}
'''
tpl = (here / '_template.html').read_text(encoding='utf-8')
out = (tpl.replace('{{NAV_CSS}}', N.css() + OVERRIDES).replace('{{NAV}}', N.render(LINKS).strip())
          .replace('{{NAV_JS}}', N.js()).replace('{{PLATES}}', '\n'.join(panel(i, p) for i, p in enumerate(ITEMS))))
assert '{{' not in out
(here / 'index.html').write_text(out, encoding='utf-8')
print('planB2 built', len(out), 'plates', len(ITEMS))
