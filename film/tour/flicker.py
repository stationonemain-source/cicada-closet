# frame-to-frame change, at the same 720px scale for both. An upscaler that shimmers moves MORE between
# frames than the source it came from; a clean one moves about the same.
import subprocess, numpy as np
def frames(p, flags):
    raw = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss','20','-t','4','-i',p,'-vf',
        f'scale=720:1280:flags={flags},format=gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720).astype(np.float32)
for name, p, f in [('original', 'remux.mp4', 'bicubic'), ('upscale', 'bd1080.mp4', 'area')]:
    a = frames(p, f); d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    print(f'{name:9s} frames={len(a)} mean frame-to-frame change={d.mean():.2f} p95={np.percentile(d,95):.2f}')
