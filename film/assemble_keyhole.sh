#!/usr/bin/env bash
# assemble_keyhole.sh — client cut 2026-09-20: chapter 1 only (full logo -> zoom into the keyhole -> black).
# No wings. The site fades in from the darkness inside the keyhole.
set -e -o pipefail
cd "$(dirname "$0")"; OUT=../tier2/frames
rm -rf "$OUT"; mkdir -p "$OUT/hd" "$OUT/sd"
ffmpeg -v error -i clips/h1.mp4 -vf "scale=1600:-2:flags=lanczos" -fps_mode vfr -q:v 4 "$OUT/hd/f_%04d.jpg"
ffmpeg -v error -i clips/h1.mp4 -vf "scale=960:-2:flags=lanczos" -fps_mode vfr -q:v 5 "$OUT/sd/f_%04d.jpg"
echo "frames hd: $(ls $OUT/hd | wc -l) $(du -sh $OUT/hd | cut -f1)   sd: $(ls $OUT/sd | wc -l) $(du -sh $OUT/sd | cut -f1)"
