#!/usr/bin/env bash
# assemble.sh <clip1> <clip2> ...  → clips/master.mp4, frames/f_XXXX.jpg, seam colour
set -e -o pipefail
cd "$(dirname "$0")"; A=clips; F=frames; mkdir -p $F
INPUTS=(); FILTER=""; N=0
for CLIP in "$@"; do
  INPUTS+=(-i "$A/$CLIP.mp4")
  if (( N == 0 )); then FILTER+="[${N}:v]setpts=PTS-STARTPTS[v${N}];"
  else FILTER+="[${N}:v]select='gte(n\,1)',setpts=PTS-STARTPTS[v${N}];"; fi
  N=$((N+1))
done
CONCAT=""; for ((i=0;i<N;i++)); do CONCAT+="[v${i}]"; done
FILTER+="${CONCAT}concat=n=${N}:v=1:a=0[out]"
ffmpeg -y -v error "${INPUTS[@]}" -filter_complex "$FILTER" -map "[out]" -fps_mode vfr -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p "$A/master.mp4"
echo "master: $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$A/master.mp4")"
rm -f $F/f_*.jpg
ffmpeg -v error -i "$A/master.mp4" -vf "select='not(mod(n\,2))',scale=1280:-2" -fps_mode vfr -q:v 4 "$F/f_%04d.jpg"
COUNT=$(ls $F/f_*.jpg | wc -l); echo "frames: $COUNT  $(du -sh $F | cut -f1)"
LAST=$(ls $F/f_*.jpg | tail -1)
SEAM=$(ffmpeg -v error -i "$LAST" -vf "crop=iw:ih*0.12:0:ih*0.88,scale=1:1" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | cut -c1-6)
echo "seam: #$SEAM"
