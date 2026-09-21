"""Jenna's 09-21 edits (Instagram DMs): bio, black & grey line, booking size, aftercare wording + her real
sheet, address without the "S", and a deeper keyhole push before the black.

Run from the repo root:  python shared/jenna_edits_0921.py
Idempotent: each replacement asserts it found its old text OR already sees the new text.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SHEET_SRC = Path(r'C:\Users\Circl\AppData\Local\Temp\claude\C--Users-Circl--claude'
                 r'\03898714-dca8-47d7-94d0-0cccbf68580e\images\2.webp')

TEXT = [
    # 1. bio: the first line is already the sub-header, so the paragraph starts with the degree
    ('<p>Jenna Feezel is a tattoo artist, painter, and the founder of The Cicada Closet. She earned her Bachelor of Fine Arts in Studio Art before beginning her career in tattooing.</p>',
     '<p>Jenna Feezel earned her Bachelor of Fine Arts in Studio Art before beginning her career in tattooing.</p>'),
    # 2. black & grey line, her exact words
    ('her paintings explore color and organic form, while her tattoo work lives primarily in black and grey&mdash;illustrative, intentional, and deeply personal.</p>',
     'her paintings explore color and organic form. Her tattoo work commonly lives in black and grey, but she is working towards implementing the same colorful aesthetic into her tattooing process.</p>'),
    # 3. booking step
    ('Where you would like the tattoo placed and approximately how large you want it.',
     'Where you would like the tattoo placed and approximately what size.'),
    # 4. aftercare: "and" -> "or"
    ('open it, download it, and come back to it any time while you heal.',
     'open it, download it, or come back to it any time while you heal.'),
]

# 5. address as she writes it (and as her own aftercare sheet prints it). Visible text only:
#    schema streetAddress and the Google Maps query keep "S" so maps and search still resolve.
ADDRESS_VISIBLE = [
    ('studio and local art gallery at 755 S Jenkins Ave, Norman', 'studio and local art gallery at 755 Jenkins Ave, Norman'),
    ('<span>755 S Jenkins Ave, Norman, OK 73069<br>', '<span>755 Jenkins Ave, Norman, OK 73069<br>'),
    ('Norman, Oklahoma · 755 S Jenkins Ave</p>', 'Norman, Oklahoma · 755 Jenkins Ave</p>'),
    ('<dd>755 S Jenkins Ave<br>Norman, OK 73069</dd>', '<dd>755 Jenkins Ave<br>Norman, OK 73069</dd>'),
    ('<span>755 S Jenkins Ave<br>Norman, OK 73069</span>', '<span>755 Jenkins Ave<br>Norman, OK 73069</span>'),
]

# 6. keyhole (tier2 only): black used to land at p .50-.70 with the camera still ~0.5 units off the
#    sheet. Now it lands at .77-.82, as the keyhole swallows the frame (canvas 100% dark by .81); the camera meets the
#    sheet at p~.825 (wide) and would see the kraft field behind the well past p~.838, so black is
#    complete before that on every aspect. The landing rises 10vh later on desktop so its dark edge
#    only appears once the screen is already black (phones' -46vh already clears).
KEYHOLE = [
    ("const f = Math.max(0, Math.min(1, (p - 0.50) / 0.20));   // black lands before the camera meets the relief's face",
     "const f = Math.max(0, Math.min(1, (p - 0.77) / 0.05));   // travel INTO the keyhole first; black completes (p .82) before the camera passes the sheet (p .84 at 16:10, later on narrower screens)"),
    ('.landing{margin-top:-70vh;', '.landing{margin-top:-60vh;'),
]


def patch(path, pairs, required=True):
    s = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif new in s:
            pass
        elif required:
            raise SystemExit(f'{path.name}: could not find -> {old[:70]}')
    path.write_text(s, encoding='utf-8')
    print('patched', path.relative_to(ROOT))


for tier in ('tier1', 'tier2'):
    patch(ROOT / tier / 'index.html', TEXT + ADDRESS_VISIBLE)
patch(ROOT / 'tier2' / 'index.html', KEYHOLE)
patch(ROOT / 'shared' / 'nav.html', ADDRESS_VISIBLE, required=False)

# her real aftercare sheet replaces the branded placeholder (same filenames, so no markup change)
im = Image.open(SHEET_SRC).convert('RGB')
for tier in ('tier1', 'tier2'):
    d = ROOT / tier / 'assets' / 'aftercare'
    im.save(d / 'aftercare-sheet.jpg', quality=92, optimize=True, progressive=True)
    # 1103 px wide at 130 dpi prints at about 8.5 in, a letter-size page
    im.save(d / 'cicada-closet-aftercare.pdf', 'PDF', resolution=130.0)
    print('sheet ->', d.relative_to(ROOT), im.size)
