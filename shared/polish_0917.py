"""09-17 polish pass: heading spacing, aftercare, studio collage, artist, footer (tier1 = source),
synced into the film site; plus the film handoff seam and the phone gap (tier2 engine)."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
t1 = root / 'tier1' / 'index.html'
s = t1.read_text(encoding='utf-8')


def rep(src, a, b):
    assert a in src, 'NOT FOUND: ' + a[:90]
    return src.replace(a, b)


# (2) heading spacing + calmer section rhythm (also shortens the aftercare gap)
s = rep(s, "section{padding:clamp(72px,10vw,140px) var(--gutter)}",
        "section{padding:clamp(64px,8vw,112px) var(--gutter)}\nsection h2{margin-bottom:18px}")

# (3) aftercare: readable and intentional
s = rep(s, ".care{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:26px;margin-top:30px}\n"
           ".care div{border-top:2px solid var(--ink);padding-top:12px}\n"
           ".care b{display:block;font-family:var(--display);font-size:18px;margin-bottom:6px}\n"
           ".care p{font-size:15.5px;color:var(--ink-2);margin:0}",
        ".care{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:34px}\n"
        ".care div{background:rgba(239,227,204,.6);border-top:3px solid var(--ink);padding:20px 22px 22px}\n"
        ".care b{display:block;font-family:var(--display);font-weight:400;font-size:21px;line-height:1.15;margin-bottom:10px}\n"
        ".care p{font-size:16.5px;line-height:1.6;color:var(--ink);margin:0}\n"
        "#care > p{font-size:18px;color:var(--ink-2)}")

# (4) studio collage: the clean room, a gallery-wall detail, the real grand-opening poster
s = rep(s, ".studio .photos img:first-child{grid-column:span 2;aspect-ratio:16/10}",
        ".studio .photos img:first-child{grid-column:span 2;aspect-ratio:16/9}\n"
        ".studio .photos img.poster{object-fit:contain;background:#98a0a6}")
a = s.index('<div class="photos">')
b = s.index('</div>', a) + len('</div>')
s = s[:a] + ('<div class="photos">\n'
             '      <img src="assets/studio-room.jpg" alt="Inside The Cicada Closet: deep green walls hung with framed work by local artists, and the front counter" loading="lazy">\n'
             '      <img src="assets/studio-wall.jpg" alt="Close view of the gallery wall: framed paintings and drawings by local artists" loading="lazy">\n'
             '      <img class="poster" src="assets/studio-opening.jpg" alt="Poster for Grillin&rsquo; and Chillin&rsquo;, the grand opening and art show at The Cicada Closet on Saturday, July 11" loading="lazy">\n'
             '    </div>') + s[b:]

# (5) artist: presence
s = rep(s, ".artist p{color:var(--cream);opacity:.9}",
        ".artist h2{font-size:clamp(40px,5.4vw,68px);margin-bottom:10px}\n"
        ".artist p.lede{font-family:var(--display);font-size:clamp(20px,2vw,26px);line-height:1.25;color:#cdb98a;opacity:1;margin-bottom:22px;max-width:30ch}\n"
        ".artist p{color:var(--cream);opacity:.92;font-size:18.5px;line-height:1.65}")
s = rep(s, ".artist .creds span{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;border:1px solid rgba(239,227,204,.4);padding:7px 12px}",
        ".artist .creds span{font-family:var(--mono);font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;border:1px solid rgba(239,227,204,.45);padding:10px 15px}")
s = rep(s, "<h2>Jenna Feezel</h2>\n      <p>Jenna holds",
        "<h2>Jenna Feezel</h2>\n      <p class=\"lede\">Painter, licensed tattoo artist, and the owner behind the keyhole.</p>\n      <p>Jenna holds")

# (7) footer: finished, on ink
a = s.index('/* footer */')
b = s.index('/* lightbox */')
FOOT_CSS = """/* footer */
footer{background:var(--ink);color:var(--cream);padding:clamp(48px,6vw,72px) var(--gutter) 28px;display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:34px 40px;font-family:var(--body)}
@media (max-width:760px){footer{grid-template-columns:1fr}}
footer a{color:var(--cream);text-decoration-thickness:1px;text-underline-offset:3px}
.foot-brand{display:flex;gap:16px;align-items:flex-start}
.foot-brand i{flex:none;width:64px;height:26px;margin-top:4px;background:var(--kraft);-webkit-mask:url(assets/cicada-mark.png) center/contain no-repeat;mask:url(assets/cicada-mark.png) center/contain no-repeat}
.foot-brand b{display:block;font-family:var(--display);font-weight:400;font-size:24px;line-height:1.1}
.foot-brand span{display:block;margin-top:6px;color:#cdb98a;font-size:16px}
.foot-col{display:grid;gap:6px;align-content:start;font-size:16.5px;line-height:1.5}
.foot-col .k{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--berry);margin-bottom:4px}
.foot-col .ig{display:inline-flex;align-items:center;gap:8px}
footer svg{width:17px;height:17px;fill:currentColor}
.foot-base{grid-column:1/-1;border-top:1px solid rgba(239,227,204,.16);padding-top:20px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;color:#a99a7e}

"""
s = s[:a] + FOOT_CSS + s[b:]
i0 = s.index('<svg viewBox="0 0 24 24">')
IG = s[i0:s.index('</svg>', i0) + 6]
a = s.index('<footer>')
b = s.index('</footer>') + len('</footer>')
MAPS = 'https://www.google.com/maps/dir/?api=1&amp;destination=755+S+Jenkins+Ave,+Norman,+OK+73069'
FOOT = ('<footer>\n'
        '  <div class="foot-brand"><i aria-hidden="true"></i><div><b>The Cicada Closet</b><span>Female-owned tattoo studio in Norman, Oklahoma.</span></div></div>\n'
        f'  <div class="foot-col"><span class="k">Visit</span><span>755 S Jenkins Ave<br>Norman, OK 73069</span><a href="{MAPS}" target="_blank" rel="noopener">Get directions</a></div>\n'
        f'  <div class="foot-col"><span class="k">Book &amp; follow</span><a class="ig" href="https://www.instagram.com/jens.art/" target="_blank" rel="noopener">{IG}Message @jens.art</a>'
        f'<a class="ig" href="https://www.instagram.com/thecicadacloset/" target="_blank" rel="noopener">{IG}@thecicadacloset</a></div>\n'
        '  <div class="foot-base"><span>&copy; 2026 The Cicada Closet</span><a href="#top">Back to top</a></div>\n'
        '</footer>')
s = s[:a] + FOOT + s[b:]
t1.write_text(s, encoding='utf-8')

# sync shared pieces into the film site
t2 = root / 'tier2'
(t2 / '_style.css').write_text(s.split('<style>')[1].split('</style>')[0], encoding='utf-8')
body = s.split('<main id="top">')[1].split('</main>')[0]
(t2 / '_after.html').write_text(body.split('</section>', 1)[1], encoding='utf-8')
(t2 / '_footer.html').write_text(s[s.index('<footer>'):s.index('</footer>') + len('</footer>')], encoding='utf-8')
for n in ('studio-room', 'studio-wall', 'studio-opening'):
    (t2 / 'assets' / f'{n}.jpg').write_bytes((root / 'tier1' / 'assets' / f'{n}.jpg').read_bytes())

# (1) seamless film handoff and (6) shorter gap on phones
e = t2 / '_engine.html'
es = e.read_text(encoding='utf-8')
es = rep(es, ".landing::before{inset:52vh 0 0 0}",
         ".landing::before{-webkit-mask-image:linear-gradient(180deg,transparent 0,transparent 36vh,#000 64vh);mask-image:linear-gradient(180deg,transparent 0,transparent 36vh,#000 64vh)}\n"
         "@media (max-width:760px){.landing{margin-top:-46vh;background:linear-gradient(180deg,rgba(172,118,70,0) 0,var(--seam) 12vh,var(--kraft) 30vh)}"
         ".landing > section:first-of-type{padding-top:calc(30vh + 8px)}"
         ".landing::before{-webkit-mask-image:linear-gradient(180deg,transparent 0,transparent 20vh,#000 40vh);mask-image:linear-gradient(180deg,transparent 0,transparent 20vh,#000 40vh)}}")
es = rep(es, "onKraft = lt + innerHeight * 0.46 <= 70;", "onKraft = lt + innerHeight * (innerWidth <= 760 ? 0.28 : 0.46) <= 70;")
e.write_text(es, encoding='utf-8')
print('all seven applied')
