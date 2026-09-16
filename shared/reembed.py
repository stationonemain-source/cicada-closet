"""Re-embed the current shared nav css/js into tier1 index + add favicon; tier2 re-syncs from tier1."""
import pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / 'shared')); import build_nav as N
t1 = root / 'tier1' / 'index.html'; s = t1.read_text(encoding='utf-8')
s, a = re.subn(r'/\* ---- nav \(shared.*?(?=</style>)', lambda m: N.css() + '\n', s, flags=re.S)
s, b = re.subn(r"<script>\n\(function\(\)\{\n  var nav = document\.getElementById\('nav'\).*?</script>", lambda m: '<script>\n' + N.js() + '</script>', s, flags=re.S)
if '<link rel="icon"' not in s:
    s = s.replace('<link rel="preconnect"', '<link rel="icon" type="image/png" href="assets/cicada-mark.png">\n<link rel="preconnect"', 1)
assert a == 1 and b == 1, (a, b)
t1.write_text(s, encoding='utf-8')
t2 = root / 'tier2'
(t2 / '_style.css').write_text(s.split('<style>')[1].split('</style>')[0], encoding='utf-8')
e = t2 / '_engine.html'; es = e.read_text(encoding='utf-8')
es, c = re.subn(r"<script>\n\(function\(\)\{\n  var nav = document\.getElementById\('nav'\).*?</script>", lambda m: '<script>\n' + N.js() + '</script>', es, flags=re.S)
if '<link rel="icon"' not in es:
    es = es.replace('<link rel="preconnect"', '<link rel="icon" type="image/png" href="assets/cicada-mark.png">\n<link rel="preconnect"', 1)
assert c == 1, c
e.write_text(es, encoding='utf-8'); print('re-embedded')
