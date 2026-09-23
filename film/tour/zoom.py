# zoom.py — the wall art at 3x, original vs upscale, same frame. Where a model would invent detail.
import subprocess, os
from io import BytesIO
from PIL import Image, ImageDraw
def fr(p, t, w, h):
    o = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',p,'-frames:v','1',
        '-vf',f'scale={w}:{h}:flags=bicubic','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True).stdout
    return Image.open(BytesIO(o)).convert('RGB')
jobs = [(14, (350, 396, 640, 586)), (30, (250, 446, 480, 646)), (3, (80, 516, 300, 746)), (3, (520, 400, 640, 580))]
rows = []
for t, (x0, y0, x1, y1) in jobs:
    a = fr('remux.mp4', t, 720, 1280).crop((x0, y0, x1, y1))
    b = fr('bd1080.mp4', t, 720, 1280).crop((x0, y0, x1, y1))
    s = 2
    a = a.resize((a.width*s, a.height*s), Image.BICUBIC); b = b.resize((b.width*s, b.height*s), Image.BICUBIC)
    r = Image.new('RGB', (a.width*2+10, a.height), (20,20,20)); r.paste(a,(0,0)); r.paste(b,(a.width+10,0)); rows.append(r)
W = max(r.width for r in rows); H = sum(r.height for r in rows) + 10*len(rows)
sh = Image.new('RGB', (W, H), (20,20,20)); y = 0
for r in rows: sh.paste(r, (0, y)); y += r.height + 10
sh.save('zoom_art.jpg', quality=92); print('zoom_art.jpg', sh.size)
