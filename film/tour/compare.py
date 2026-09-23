# python compare.py cand1.mp4 [cand2.mp4 ...]  -> compare_t<sec>.jpg
# Every candidate is shown against the ORIGINAL as a viewer would see it: the original is scaled to
# 720x1280 with plain bilinear, which is what the browser does to a 360x640 video on a retina
# screen. Same frame, same crop, side by side. Judge faithfulness here, not in the model's preview.
import subprocess, sys, os
from PIL import Image, ImageDraw

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, 'remux.mp4')
cands = sys.argv[1:]
times = [3, 14, 30, 45]
W, H = 720, 1280

def frame(path, t, flags):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(t), '-i', path,
                          '-frames:v', '1', '-vf', f'scale={W}:{H}:flags={flags}', '-f', 'image2pipe',
                          '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    from io import BytesIO
    return Image.open(BytesIO(out)).convert('RGB')

for t in times:
    tiles = [('original (as browser shows it)', frame(src, t, 'bilinear'))]
    for c in cands:
        tiles.append((os.path.basename(c), frame(os.path.join(here, c), t, 'lanczos')))
    # the middle of the frame, at 1:1 device pixels — where the framed work hangs
    box = (80, 300, 640, 980)
    cw, ch = box[2] - box[0], box[3] - box[1]
    sheet = Image.new('RGB', (cw * len(tiles), ch + 34), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(tiles):
        sheet.paste(im.crop(box), (i * cw, 34))
        d.text((i * cw + 10, 10), name, fill=(240, 240, 240))
    p = os.path.join(here, f'compare_t{t}.jpg')
    sheet.save(p, quality=92)
    print(p)
