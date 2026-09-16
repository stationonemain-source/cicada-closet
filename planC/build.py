"""Build planC/index.html (Plan C · Healed, tier 1)."""
import json, pathlib, sys
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / 'shared'))
import build_nav as N

IG = 'https://www.instagram.com/p/{}/'
WORK = [  # newest first, dates are Instagram post dates
    ('bluebird', 'Bluebird', 'tattoo', '2026-09-08', 'Sep 2026', 'DdCi5jkj81B', 'Black and grey tattoo of a bluebird in flight on an upper arm'),
    ('salamander', 'Salamander', 'watercolour', '2026-07-31', 'Jul 2026', 'DbdtExQnH7c', 'Watercolour and ink drawing of a black salamander with yellow spots on an oak leaf'),
    ('murals', 'Murals for Mira', 'murals', '2026-07-29', 'Jul 2026', 'DbYjhahnIus', 'Two symmetrical painted murals on a rust ground with cicadas, morning glories and strawberries'),
    ('pink-skies', 'Pink skies', 'tattoo', '2026-07-17', 'Jul 2026', 'Da6BiSKHLMZ', 'Colour tattoo of a pink sunset over a river, framed in an ornate gilt mirror'),
    ('luna-moth', 'Luna moth', 'tattoo', '2026-07-14', 'Jul 2026', 'DayYFUZDw_O', 'Colour tattoo of a teal luna moth beneath a gold crescent moon'),
    ('stag-beetle-seraphim', 'Stag beetle seraphim', 'tattoo', '2025-07-20', 'Jul 2025', 'DMV0eDuxfaQ', 'Black and grey tattoo of a six-winged stag beetle with an eye on each wing'),
]
STAGES = [
    dict(**{'from': 0}, tick='Day 0', range='Day 0', name='Fresh',
         see='Your tattoo leaves the studio covered. The skin is tender, warm and pink at the edges, a lot like a mild sunburn.',
         todo=['Keep the covering on for as long as Jenna tells you.', 'Wash your hands before you touch it.',
               'When the covering comes off, wash gently with lukewarm water and unscented soap, then pat dry.']),
    dict(**{'from': 1}, tick='1–3', range='Days 1–3', name='Tender',
         see='It may weep a little clear fluid and excess ink, and it can feel swollen and warm. Both ease over these first days.',
         todo=['Wash gently two or three times a day and pat dry with a clean paper towel.',
               'Apply a thin layer of the product Jenna recommends.', 'Sleep on clean sheets and wear loose clothing over it.']),
    dict(**{'from': 4}, tick='4–7', range='Days 4–7', name='Flaking',
         see='The surface starts to flake and peel like a healing sunburn, and it usually starts to itch.',
         todo=['Let flakes fall away on their own. No picking or peeling.', 'Tap or pat an itch instead of scratching it.',
               'Keep moisturising, thinly.']),
    dict(**{'from': 8}, tick='8–14', range='Days 8–14', name='Settling',
         see='Most of the flaking finishes. Under the new layer of skin the tattoo can look dull or slightly cloudy for a while.',
         todo=['Keep it clean and lightly moisturised.', 'Still no baths, pools, lakes or hot tubs.',
               'Keep it covered or out of direct sun.']),
    dict(**{'from': 15}, tick='Wk 2–4', range='Weeks 2–4', name='Cloudy',
         see='The surface looks healed, but the skin underneath is still repairing. A milky or shiny look is normal, and it fades.',
         todo=['Keep moisturising if the skin feels dry.', 'Wait until any shine and flaking are fully gone before swimming or sunbathing.',
               'Hold off judging colour and line until it has settled.']),
    dict(**{'from': 29}, tick='Wk 5+', range='Week 5 on', name='Healed',
         see='The surface has usually settled by now, and what you see is close to how it will look. Deeper skin can take a few more months to finish.',
         todo=['Put sunscreen on it whenever it is out in the sun. Sun exposure is one of the main causes of fading.',
               'If anything looks patchy once it has settled, message Jenna and ask.']),
]


def piece(f, title, kind, iso, label, post, alt):
    return (f'        <figure class="piece"><a href="{IG.format(post)}" target="_blank" rel="noopener" aria-label="{title}, open the post on Instagram">'
            f'<img src="assets/{f}.jpg" alt="{alt}" loading="lazy"></a>'
            f'<figcaption><b>{title}</b><span>{kind} · <time datetime="{iso}">{label}</time></span></figcaption></figure>')


LINKS = [('#work', 'Work', 'Recent pieces'), ('#care', 'Healing', 'Day by day'), ('#studio', 'Studio', 'Gallery wall'),
         ('#artist', 'Artist', 'Jenna Feezel'), ('#book', 'Booking', 'By message')]
OVERRIDES = '''
/* nav tuned for the green-wall palette */
.nav[data-mode="dark"]{background:rgba(31,45,37,.96)}
.nav-mark span{font-size:19px;letter-spacing:0}
'''
tpl = (here / '_template.html').read_text(encoding='utf-8')
tpl = tpl.replace('<section class="clock" id="care">', '<section class="clock" id="care" data-nav-dark>')
out = (tpl.replace('{{NAV_CSS}}', N.css() + OVERRIDES)
          .replace('{{NAV}}', N.render(LINKS).strip())
          .replace('{{NAV_JS}}', N.js())
          .replace('{{WORK}}', '\n'.join(piece(*w) for w in WORK))
          .replace('{{STAGES}}', json.dumps(STAGES, ensure_ascii=False)))
assert '{{' not in out
(here / 'index.html').write_text(out, encoding='utf-8')
print('planC built', len(out))
