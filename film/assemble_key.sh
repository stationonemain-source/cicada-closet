#!/usr/bin/env bash
# assemble_key.sh — the short film: chapter 1 only (logo -> through the keyhole), EVERY frame, two sizes.
set -e -o pipefail
cd "$(dirname "$0")"; OUT=../tier2/frames
rm -rf "$OUT"; mkdir -p "$OUT/hd" "$OUT/sd"
ffmpeg -v error -i clips/h1.mp4 -vf "scale=1600:-2:flags=lanczos" -fps_mode vfr -q:v 3 "$OUT/hd/f_%04d.jpg"
ffmpeg -v error -i clips/h1.mp4 -vf "scale=960:-2:flags=lanczos" -fps_mode vfr -q:v 4 "$OUT/sd/f_%04d.jpg"
echo "frames hd: $(ls $OUT/hd | wc -l) $(du -sh $OUT/hd | cut -f1)   sd: $(ls $OUT/sd | wc -l) $(du -sh $OUT/sd | cut -f1)"
