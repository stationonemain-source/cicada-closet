#!/usr/bin/env bash
# resume.sh <clip-name> <job-id> [prev-last-png] — wait on an existing Seedance job, then download + gate like chain.sh
DIR="$(cd "$(dirname "$0")" && pwd)/clips"; NAME=$1; ID=$2; PREV=$3
for attempt in 1 2 3 4 5 6; do
  WAIT=$(higgsfield generate wait "$ID" --timeout 15m --interval 10s --json 2>&1 </dev/null)
  URL=$(echo "$WAIT" | grep -oE 'https://[^" ]+\.mp4[^" ]*' | tail -1)
  [[ -n "$URL" ]] && break
  if echo "$WAIT" | grep -qiE '"failed"|status "failed"|ended with status'; then echo "[$NAME] job FAILED server-side (unbilled): $(echo "$WAIT" | tail -1)"; exit 3; fi
  echo "[$NAME] still waiting (attempt $attempt): $(echo "$WAIT" | tail -1)"
done
[[ -n "$URL" ]] || { echo "[$NAME] gave up waiting"; exit 1; }
curl -fsSL -o "$DIR/$NAME.mp4" "$URL"
ffmpeg -y -v error -i "$DIR/$NAME.mp4" -vf "select=eq(n\,0)" -frames:v 1 -update 1 -q:v 1 "$DIR/$NAME-first.png"
ffmpeg -y -v error -sseof -0.05 -i "$DIR/$NAME.mp4" -update 1 -q:v 1 "$DIR/$NAME-last.png"
echo "[$NAME] got $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$DIR/$NAME.mp4")"
if [[ -n "$PREV" ]]; then
  SSIM=$( (ffmpeg -i "$PREV" -i "$DIR/$NAME-first.png" -lavfi ssim -f null - 2>&1 || true) | grep -o 'All:[0-9.]*' | cut -d: -f2)
  echo "[$NAME] JUNCTION SSIM vs $(basename "$PREV"): ${SSIM:-n/a}"
fi
ffmpeg -y -v error -i "$DIR/$NAME.mp4" -vf "select='not(mod(n\,15))',scale=320:-2,tile=8x1" -frames:v 1 "$DIR/$NAME-strip.jpg" || true
echo "[$NAME] DONE"
