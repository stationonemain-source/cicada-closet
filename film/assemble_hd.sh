#!/usr/bin/env bash
# assemble_hd.sh h1 h2 h3 h4 h5 -> clips/master_hd.mp4, ../tier2/frames/{hd,sd}/f_XXXX.jpg, seam colour
set -e -o pipefail
cd "$(dirname "$0")"; A=clips; OUT=../tier2/frames
INPUTS=(); FILTER=""; N=0
for CLIP in "$@"; do
  INPUTS+=(-i "$A/$CLIP.mp4")
  if (( N == 0 )); then FILTER+="[${N}:v]setpts=PTS-STARTPTS[v${N}];"
  else
    # optional per-clip grade match at a seam: GRADE_<clip>="eq filter args"
    G="GRADE_${CLIP}"; EXTRA=""; [[ -n "${!G}" ]] && EXTRA=",${!G}"
    FILTER+="[${N}:v]select='gte(n\,1)',setpts=PTS-STARTPTS${EXTRA}[v${N}];"; fi
  N=$((N+1))
done
CONCAT=""; for ((i=0;i<N;i++)); do CONCAT+="[v${i}]"; done
FILTER+="${CONCAT}concat=n=${N}:v=1:a=0[out]"
ffmpeg -y -v error "${INPUTS[@]}" -filter_complex "$FILTER" -map "[out]" -fps_mode vfr -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p "$A/master_hd.mp4"
echo "master: $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$A/master_hd.mp4")"
rm -rf "$OUT"; mkdir -p "$OUT/hd" "$OUT/sd"
ffmpeg -v error -i "$A/master_hd.mp4" -vf "select='not(mod(n\,2))',scale=1600:-2:flags=lanczos" -fps_mode vfr -q:v 3 "$OUT/hd/f_%04d.jpg"
ffmpeg -v error -i "$A/master_hd.mp4" -vf "select='not(mod(n\,2))',scale=960:-2:flags=lanczos" -fps_mode vfr -q:v 4 "$OUT/sd/f_%04d.jpg"
echo "frames hd: $(ls $OUT/hd | wc -l)  $(du -sh $OUT/hd | cut -f1)   sd: $(ls $OUT/sd | wc -l)  $(du -sh $OUT/sd | cut -f1)"
LAST=$(ls $OUT/hd/f_*.jpg | tail -1)
SEAM=$(ffmpeg -v error -i "$LAST" -vf "crop=iw:ih*0.12:0:ih*0.88,scale=1:1" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | cut -c1-6)
echo "seam: #$SEAM"
