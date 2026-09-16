#!/usr/bin/env bash
# chain.sh <clip-name> <start-image> <prompt-file> [prev-last-png] [resolution] [extra higgsfield args...]
# Bash port of scroll-film-studio/scripts/chain-step.sh. Mechanical, no model.
set -e -o pipefail
DIR="$(cd "$(dirname "$0")" && pwd)/clips"
NAME=$1; START=$2; PFILE=$3; PREV=$4; RES=${5:-480p}; shift 5 2>/dev/null || shift $#
PROMPT=$(cat "$PFILE"); case "$START" in *.png) python3 -c "from PIL import Image;Image.open('$START').convert('RGB').save('${START%.png}.jpg',quality=95)"; START="${START%.png}.jpg";; esac
MODE=std; [[ "$RES" == "480p" || "$RES" == "720p" ]] && MODE=fast
mkdir -p "$DIR"
echo "[$NAME] create ($RES/$MODE, audio off)"
CREATE=$(higgsfield generate create seedance_2_0 --prompt "$PROMPT" --start-image "$START" \
  --duration 5 --resolution "$RES" --generate-audio false --aspect_ratio 16:9 "$@" --json 2>&1)
ID=$(echo "$CREATE" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
[[ -n "$ID" ]] || { echo "[$NAME] FAILED create:"; echo "$CREATE" | tail -5; exit 1; }
echo "[$NAME] job $ID"; echo "$ID" > "$DIR/$NAME.job"
WAIT=$(higgsfield generate wait "$ID" --timeout 15m --interval 5s --json 2>&1 || true)
URL=$(echo "$WAIT" | grep -oE 'https://[^" ]+\.mp4[^" ]*' | tail -1)
[[ -n "$URL" ]] || { echo "[$NAME] FAILED no mp4 (unbilled, retry):"; echo "$WAIT" | tail -3; exit 1; }
curl -fsSL -o "$DIR/$NAME.mp4" "$URL"
ffmpeg -y -v error -i "$DIR/$NAME.mp4" -vf "select=eq(n\,0)" -frames:v 1 -update 1 -q:v 1 "$DIR/$NAME-first.png"
ffmpeg -y -v error -sseof -0.05 -i "$DIR/$NAME.mp4" -update 1 -q:v 1 "$DIR/$NAME-last.png"
echo "[$NAME] got $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$DIR/$NAME.mp4")"
if [[ -n "$PREV" ]]; then
  SSIM=$( (ffmpeg -i "$PREV" -i "$DIR/$NAME-first.png" -lavfi ssim -f null - 2>&1 || true) | grep -o 'All:[0-9.]*' | cut -d: -f2)
  ffmpeg -y -v error -i "$PREV" -i "$DIR/$NAME-first.png" -filter_complex "[0][1]hstack" "$DIR/$NAME-junction.jpg" || true
  echo "[$NAME] JUNCTION SSIM vs $(basename "$PREV"): ${SSIM:-n/a}"
fi
# filmstrip of 8 frames for review
ffmpeg -y -v error -i "$DIR/$NAME.mp4" -vf "select='not(mod(n\,15))',scale=320:-2,tile=8x1" -frames:v 1 "$DIR/$NAME-strip.jpg" || true
echo "[$NAME] DONE"
