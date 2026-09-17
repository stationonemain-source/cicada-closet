#!/usr/bin/env bash
# assemble_wings.sh — short film: chapter 1 + chapter 2 (logo -> keyhole -> blue wings -> golden light), every frame.
set -e -o pipefail
cd "$(dirname "$0")"; OUT=../tier2/frames
ffmpeg -y -v error -i clips/h1.mp4 -i clips/h2.mp4 -filter_complex "[0:v]setpts=PTS-STARTPTS[a];[1:v]select='gte(n\,1)',setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[out]" -map "[out]" -fps_mode vfr -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p clips/master_wings.mp4
rm -rf "$OUT"; mkdir -p "$OUT/hd" "$OUT/sd"
ffmpeg -v error -i clips/master_wings.mp4 -vf "scale=1600:-2:flags=lanczos" -fps_mode vfr -q:v 4 "$OUT/hd/f_%04d.jpg"
ffmpeg -v error -i clips/master_wings.mp4 -vf "scale=960:-2:flags=lanczos" -fps_mode vfr -q:v 5 "$OUT/sd/f_%04d.jpg"
echo "frames hd: $(ls $OUT/hd | wc -l) $(du -sh $OUT/hd | cut -f1)   sd: $(ls $OUT/sd | wc -l) $(du -sh $OUT/sd | cut -f1)"
LAST=$(ls $OUT/hd/f_*.jpg | tail -1)
SEAM=$(ffmpeg -v error -i "$LAST" -vf "crop=iw*0.3:ih*0.5:iw*0.35:ih*0.4,scale=1:1" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | cut -c1-6)
echo "seam (golden light, centre of last frame): #$SEAM"
