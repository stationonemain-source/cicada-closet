"""Build planB/index.html (Plan B · The Field Guide, tier 1)."""
import pathlib, sys
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / 'shared'))
import build_nav as N

IG = 'https://www.instagram.com/p/{}/'
PLATES = [
    dict(n='I', file='luna-moth', name='Luna Moth', latin='Actias luna', medium='Tattoo, colour', posted='July 2026', post='DayYFUZDw_O',
         alt='Colour tattoo of a teal luna moth beneath a gold crescent moon, with green sprigs',
         note='The luna moth is a North American silk moth, pale green, with long trailing tails on its hindwings. Adults have no working mouthparts and live about a week. The artist posted this one as a luna moth &ldquo;Chappell inspired.&rdquo;'),
    dict(n='II', file='stag-beetle-seraphim', name='Stag Beetle Seraphim', latin='Family Lucanidae', medium='Tattoo, black and grey', posted='July 2025', post='DMV0eDuxfaQ',
         alt='Black and grey tattoo of a stag beetle with six wings, each wing patterned with an eye',
         note='Stag beetles are named for the males&rsquo; oversized jaws, which branch like antlers. In the old descriptions a seraph has six wings. This beetle has six, and an eye on each.'),
    dict(n='III', file='bluebird', name='Bluebird', latin='Genus Sialia', medium='Tattoo, black and grey', posted='September 2026', post='DdCi5jkj81B',
         alt='Black and grey tattoo of a bluebird in flight on an upper arm',
         note='Bluebirds are small thrushes. The eastern bluebird lives in Oklahoma all year and is often seen perched on fences and wires around open fields. Here the bird is drawn in flight, with both wings fully open.'),
    dict(n='IV', file='pink-skies', name='Pink Skies', latin='A sunset, in a gilt frame', medium='Tattoo, colour', posted='July 2026', post='Da6BiSKHLMZ',
         alt='Colour tattoo of a pink sunset over a river between dark pines, framed in an ornate gilt mirror',
         note='A river runs toward a pink sky between dark pines, and an ornate gilt mirror frames the whole scene. The artist posted it as a piece made in honour of someone.'),
    dict(n='V', file='salamander', name='Salamander', latin='Order Caudata', medium='Watercolour and Micron pen on paper', posted='July 2026', post='DbdtExQnH7c',
         alt='Watercolour and ink drawing of a black salamander with yellow spots curled across a dry oak leaf',
         note='Salamanders are amphibians of the order Caudata, with long tails and soft skin, and they favour damp leaf litter. This one curls across a fallen oak leaf. The artist described it as a quick little watercolour, finished in Micron pen.'),
    dict(n='VI', file='murals', name='Murals for Mira', latin='Cicadas, morning glories &amp; strawberries', medium='Paint, a pair of murals', posted='July 2026', post='DbYjhahnIus', wide=True,
         alt='Two symmetrical painted murals on a rust ground showing cicadas, morning glories, strawberries and small hearts',
         note='A pair of symmetrical murals on a rust ground, painted for Mira&rsquo;s room. Cicadas sit among morning glories, strawberries and small hearts. It is the same insect that gives the studio its name.'),
]


def spread(i, p):
    flip = ' flip' if i % 2 else ''
    wide = ' wide' if p.get('wide') else ''
    return f'''    <article class="spread{flip}" id="plate-{i + 1}" aria-labelledby="pl{i + 1}">
      <div class="page plate-page">
        <span class="plate-no">Plate {p['n']}</span>
        <button class="mount{wide}" data-full="assets/{p['file']}.jpg" data-cap="Plate {p['n']}. {p['name']}."><i></i><img src="assets/{p['file']}.jpg" alt="{p['alt']}" loading="lazy"></button>
        <span class="plate-cap">From the artist&rsquo;s photograph.</span>
      </div>
      <div class="page text-page">
        <span class="num" aria-hidden="true">{p['n']}</span>
        <h3 id="pl{i + 1}">{p['name']}</h3>
        <p class="latin">{p['latin']}</p>
        <dl><dt>Medium</dt><dd>{p['medium']}</dd><dt>Posted</dt><dd>{p['posted']}</dd></dl>
        <p class="note">{p['note']}</p>
        <a class="src" href="{IG.format(p['post'])}" target="_blank" rel="noopener">See the post on Instagram</a>
      </div>
    </article>'''


def toc(i, p):
    kind = p['medium'].split(',')[0].lower() if p['medium'].startswith('Tattoo') else p['medium'].split(',')[0].lower()
    kind = p['medium'].lower()
    return f'      <li><a href="#plate-{i + 1}"><b>Pl. {p["n"]}</b><span class="t">{p["name"]} <span class="lead"></span></span><i>{kind}</i></a></li>'


LINKS = [('#studio', 'Studio', 'Preface'), ('#work', 'Plates', 'I to VI'), ('#artist', 'Artist', 'Colophon'),
         ('#book', 'Booking', 'Appendix A'), ('#care', 'Aftercare', 'Appendix B')]
OVERRIDES = '''
/* nav tuned for the field guide faces */
.nav-links a{font-size:16px;letter-spacing:.06em;text-transform:none}
.nav-book{font-size:15px;letter-spacing:.06em;text-transform:none}
.nav-toggle{font-size:15px;letter-spacing:.06em;text-transform:none}
.nav-mark span{font-size:21px}
.nav-sheet nav a small{font-size:14px;letter-spacing:.06em;text-transform:none}
'''
tpl = (here / '_template.html').read_text(encoding='utf-8')
out = (tpl.replace('{{NAV_CSS}}', N.css() + OVERRIDES)
          .replace('{{NAV}}', N.render(LINKS).strip())
          .replace('{{NAV_JS}}', N.js())
          .replace('{{TOC}}', '\n'.join(toc(i, p) for i, p in enumerate(PLATES)))
          .replace('{{PLATES}}', '\n'.join(spread(i, p) for i, p in enumerate(PLATES))))
assert '{{' not in out
(here / 'index.html').write_text(out, encoding='utf-8')
print('planB built', len(out))
