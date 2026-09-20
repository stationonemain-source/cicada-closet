# Placeholder aftercare sheet until Jenna's official sheet arrives.
# Drop her real files in as assets/aftercare/cicada-closet-aftercare.pdf
# (+ a preview jpg of page 1 as aftercare-sheet.jpg) and delete this script's output.
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1275, 1650  # US letter @150dpi
KRAFT = (201, 164, 114)
CREAM = (239, 227, 204)
INK = (27, 23, 19)
RUST = (164, 70, 28)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def font(size, name="georgiai.ttf"):
    for cand in (name, "georgia.ttf", "times.ttf"):
        try:
            return ImageFont.truetype(cand, size)
        except OSError:
            continue
    return ImageFont.load_default()


serif = lambda s: font(s, "georgia.ttf")
ital = lambda s: font(s, "georgiai.ttf")

# border
d.rectangle([40, 40, W - 40, H - 40], outline=INK, width=3)
d.rectangle([52, 52, W - 52, H - 52], outline=INK, width=1)

# cicada mark
mark_path = os.path.join(os.path.dirname(__file__), "..", "tier1", "assets", "cicada-mark.png")
y = 130
try:
    mark = Image.open(mark_path).convert("RGBA")
    mw = 260
    mh = int(mark.height * mw / mark.width)
    mark = mark.resize((mw, mh))
    ink_mark = Image.new("RGBA", mark.size, INK + (255,))
    img.paste(ink_mark, ((W - mw) // 2, y), mark)
    y += mh + 40
except Exception:
    y += 40

def center(text, f, fill=INK, dy=0):
    global y
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((W - (bb[2] - bb[0])) / 2, y + dy), text, font=f, fill=fill)
    y += (bb[3] - bb[1]) + 18 + dy

center("THE CICADA CLOSET", serif(64))
center("Official Tattoo Aftercare", ital(44), RUST)
y += 30
d.line([W * 0.28, y, W * 0.72, y], fill=INK, width=2)
y += 70

center("Your artist's full aftercare sheet", ital(36))
center("will live on this page.", ital(36))
y += 40
center("Until then, follow the instructions", serif(30))
center("you were given at your appointment,", serif(30))
center("and message the studio with any questions.", serif(30))
y += 60
center("@thecicadacloset  ·  755 S Jenkins Ave, Norman, OK", serif(26), RUST)

out = os.path.join(os.path.dirname(__file__), "..", "tier1", "assets", "aftercare")
os.makedirs(out, exist_ok=True)
img.save(os.path.join(out, "aftercare-sheet.jpg"), quality=88)
img.save(os.path.join(out, "cicada-closet-aftercare.pdf"), "PDF", resolution=150)
print("wrote", out)
