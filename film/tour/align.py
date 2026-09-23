# Is the upscale frame-aligned with the original, and where does it differ most?
import subprocess, numpy as np
def frames(p):
    raw = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',p,'-vf','scale=180:320:flags=area,format=gray',
        '-f','rawvideo','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 320, 180).astype(np.float32)
a, b = frames('remux.mp4'), frames('bd1080.mp4')
print('frames', len(a), len(b))
for off in (-2, -1, 0, 1, 2):
    n = min(len(a), len(b)) - 4
    ia = np.arange(2, n); ib = ia + off
    mse = ((a[ia] - b[ib]) ** 2).mean(axis=(1, 2))
    psnr = 10 * np.log10(255**2 / np.maximum(mse, 1e-6))
    print(f'offset {off:+d}: mean PSNR {psnr.mean():.1f}  min {psnr.min():.1f} at t={ia[psnr.argmin()]/30:.1f}s')
