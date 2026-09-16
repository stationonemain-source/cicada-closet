"""One-off: put the shared nav on tier1 + tier2 and replace copy that asserted unverified facts."""
import pathlib, re, shutil, sys
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / 'shared'))
import build_nav as N


def sub(s, old, new, count=1, regex=False):
    if regex:
        s2, n = re.subn(old, new, s, count=count, flags=re.S)
    else:
        n = s.count(old); s2 = s.replace(old, new, count)
    if n == 0:
        raise SystemExit(f'NOT FOUND: {old[:90]!r}')
    return s2


LINKS = [('#work', 'Work', 'Selected pieces'), ('#studio', 'Studio', 'Gallery wall'),
         ('#artist', 'Artist', 'Jenna Feezel'), ('#book', 'Booking', 'By message'),
         ('#care', 'Aftercare', 'The basics')]

COPY = [
    ('<p class="sub">Fine-line, illustrative and botanical work by Jenna Feezel. Nine five-star reviews and a gallery wall where local artists keep every dollar.</p>',
     '<p class="sub">Fine-line, illustrative and botanical work by Jenna Feezel, BFA. Rated 5.0 on Google, with a gallery wall where local artists keep every dollar.</p>'),
    ('<p class="big">A small shop with green walls, a keyhole on its sign, and one artist who draws everything she tattoos.</p>',
     '<p class="big">A small studio with green walls, a keyhole in its logo, and an owner who is a fine artist as well as a tattooer.</p>'),
    ('whose work leans toward moths, birds, botanicals and the kind of linework that still reads clean years later.</p>',
     'whose work leans toward moths, birds and botanicals, in fine line and in colour.</p>'),
    ('<p>Every piece starts as a drawing. Every client gets a conversation before a needle. The chair is private, the room is calm, and the walls are hung with work by Norman artists who sell here for free.</p>',
     '<p>The walls double as a small gallery. Local artists can hang work there and keep 100% of what sells, with no commission and no fees.</p>'),
    ('<h2>One chair. Green walls. A gallery that pays its artists in full.</h2>',
     '<h2>Green walls, and a gallery that pays its artists in full.</h2>'),
    ("<b>Local artist call.</b> The studio's small gallery wall is open to Norman artists. Artists keep 100% of sales. No commissions, no fees. Just community.",
     '<b>Local artist call.</b> A small gallery wall, open to local artists. Artists keep 100% of sales. No commissions, no fees. Just community.'),
    ('<p>The shop hosts openings and art shows through the year. The first one, in July 2026, filled the wall and the sidewalk out front. If you make things and want them seen, message the shop.</p>',
     '<p>The studio opened with Grillin&rsquo; &amp; Chillin&rsquo;, a grand opening and art show on Saturday, July 11, 2026. If you make art and want it on the wall, message the shop.</p>'),
    ('<p>Jenna trained as a painter before she trained as a tattooer, and it shows in the work: composition first, then line, then colour used sparingly and on purpose. Her subjects come from the field and the garden. Moths, sparrows, salamanders, morning glories, cicadas.</p>',
     '<p>Jenna holds a Bachelor of Fine Arts and paints as well as tattoos. Her BFA exhibition and her paintings sit alongside the tattoo work on her Instagram.</p>'),
    ('<p>She draws every design herself, sends it before the appointment, and tattoos with the intention that it still looks like the drawing in ten years.</p>',
     '<p>Her subjects come from the field and the garden: luna moths, sparrows, salamanders, morning glories, marigolds and, fittingly, cicadas.</p>'),
    ('<h2>Booking is by message.</h2>', '<h2>Book with a message.</h2>'),
    ('<p>There is no form and no phone line yet. Send Jenna a direct message on Instagram with the three things below and she will reply with availability and a deposit note.</p>',
     '<p>Send Jenna a message on Instagram at @jens.art. Including the three things below saves a round of questions. Her Booking highlight on Instagram has her current details.</p>'),
    ('<li><span>Days and times that work for you. The studio opens at 10am.</span></li>',
     '<li><span>Days and times that work for you.</span></li>'),
    ('<dt>Hours</dt><dd>By appointment, from 10am<small>Message for the current week.</small></dd>',
     '<dt>Hours</dt><dd>Opens at 10am<small>As listed on Google. Message to confirm a day.</small></dd>'),
    ('<h2>Two weeks of care for a lifetime of ink.</h2>', '<h2>The first weeks matter most.</h2>'),
    ('<p>Jenna goes over aftercare with you in the chair and her instructions come first. The basics below are what most of it comes down to.</p>',
     '<p>Follow the aftercare instructions Jenna gives you. Her Aftercare highlight on Instagram has her version. These are the general basics most artists agree on.</p>'),
]

# ---------------- tier 1 ----------------
t1 = root / 'tier1' / 'index.html'
s = t1.read_text(encoding='utf-8')
s = sub(s, 'main,header,footer{position:relative;z-index:1}', 'main,footer{position:relative;z-index:1}')
s = sub(s, r'/\* header \*/.*?(?=/\* hero \*/)', '', regex=True)
s = sub(s, '</style>', N.css() + '\n</style>')
s = sub(s, r'<header>.*?</header>', N.render(LINKS).strip(), regex=True)
s = sub(s, '<section class="hero" style="padding:0">', '<section class="hero" data-nav-over style="padding:0">')
s = sub(s, '<section class="artist" id="artist">', '<section class="artist" id="artist" data-nav-dark>')
s = sub(s, r"\n\s*document\.querySelectorAll\('a\[href\^=\"#\"\]'\)\.forEach\(a => a\.addEventListener\('click', e => \{\n.*?\}\)\);\n", '\n', regex=True)
s = sub(s, "gsap.ticker.lagSmoothing(0);", "gsap.ticker.lagSmoothing(0);\n    window.__lenis = lenis;")
s = sub(s, r"  // header flips over the dark artist band\n.*?flip\(\);\n", '', regex=True)
for old, new in COPY:
    s = sub(s, old, new)
s = sub(s, '</body>', '<script>\n' + N.js() + '</script>\n</body>')
t1.write_text(s, encoding='utf-8')
print('tier1 ok')

# re-extract shared pieces for tier2
style = s.split('<style>')[1].split('</style>')[0]
body = s.split('<main id="top">')[1].split('</main>')[0]
after = body.split('</section>', 1)[1]
footer = '<footer>' + s.split('<footer>')[1].split('</footer>')[0] + '</footer>'
dialog = '<dialog id="lb">' + s.split('<dialog id="lb">')[1].split('</dialog>')[0] + '</dialog>'
t2 = root / 'tier2'
(t2 / '_style.css').write_text(style, encoding='utf-8')
(t2 / '_after.html').write_text(after, encoding='utf-8')
(t2 / '_footer.html').write_text(footer, encoding='utf-8')
(t2 / '_dialog.html').write_text(dialog, encoding='utf-8')
shutil.copy(root / 'tier1' / 'assets' / 'cicada-mark.png', t2 / 'assets' / 'cicada-mark.png')

# ---------------- tier 2 engine ----------------
e = t2 / '_engine.html'
s = e.read_text(encoding='utf-8')
s = sub(s, 'header{color:var(--cream);mix-blend-mode:normal;transition:color .3s}\nheader.on-light{color:var(--ink)}\n', '')
s = sub(s, r'<header id="hdr">.*?</header>', N.render(LINKS).strip(), regex=True)
s = sub(s, '<div class="film" id="film">', '<div class="film" id="film" data-nav-over>')
s = sub(s, "const film = document.getElementById('film'), hdr = document.getElementById('hdr');", "const film = document.getElementById('film');")
s = sub(s, r"  // ---- adaptive header\n.*?(?=  // ---- beats)", '', regex=True)
s = sub(s, ' sampleHeader(now);', '')
s = sub(s, r"\n    document\.querySelectorAll\('a\[href\^=\"#\"\]'\)\.forEach\(.*?\}\)\); \}", ' window.__lenis = lenis; }', regex=True)
BEATS = [
    ('<h2>Every piece starts as a drawing.</h2><p>Moths, birds, botanicals. Composition first, then line.</p>',
     '<h2>Moths, birds and botanicals.</h2><p>Fine-line and colour work by Jenna Feezel, BFA.</p>'),
    ('<h2>Colour used sparingly, on purpose.</h2><p>Teal, ochre, marigold. Never more than the drawing needs.</p>',
     '<h2>From the field and the garden.</h2><p>Luna moths, marigolds, sparrows, salamanders.</p>'),
    ('<h2>Made to look like the drawing in ten years.</h2><p>Clean line on healed skin is the whole point.</p>',
     '<h2>Drawn for skin.</h2><p>755 South Jenkins Avenue, Norman.</p>'),
    ('<p class="eyebrow">One chair · green walls · a gallery that pays its artists in full</p>',
     '<p class="eyebrow">Green walls · a gallery that pays its artists in full</p>'),
]
for old, new in BEATS:
    s = sub(s, old, new)
s = sub(s, '</body>', '<script>\n' + N.js() + '</script>\n</body>')
e.write_text(s, encoding='utf-8')
print('tier2 engine ok')
