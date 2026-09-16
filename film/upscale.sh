#!/usr/bin/env bash
cd "$(dirname "$0")/.."
: > film/upscale.jobs
for pair in jens_2:moth-of-eyes jens_4:sparrow jens_6:salamander jens_7:cicada-paintings jens_8:sunset-mirror jens_1:marigold jens_3:jenna ig_2:shop-gallery ig_6:logo ig_5:shop-chair; do
  k=${pair%%:*}; n=${pair##*:}; f=ref/$k.jpg; out=tier1/assets/$n.png
  [[ -f $out ]] && continue
  DIMS=$(python3 -c "from PIL import Image;w,h=Image.open('$f').size;s=2560/max(w,h);print(int(w*s)//2*2,int(h*s)//2*2)")
  W=${DIMS% *}; H=${DIMS#* }
  ID=$(higgsfield generate create topaz_image --image "$f" --output_width $W --output_height $H --variant "Standard V2" --json 2>&1 | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
  echo "$k -> $n ${W}x${H} job ${ID:-FAILED}"
  [[ -n $ID ]] && echo "$ID $out" >> film/upscale.jobs
done
while read ID OUT; do
  URL=$(higgsfield generate wait $ID --timeout 8m --interval 6s --json 2>&1 | grep -oE 'https://[^" ]+\.png' | tail -1)
  if [[ -n "$URL" ]]; then curl -fsSL -o "$OUT" "$URL" && echo "saved $OUT"; else echo "FAILED $OUT ($ID)"; fi
done < film/upscale.jobs
higgsfield account status
