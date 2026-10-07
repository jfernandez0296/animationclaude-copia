#!/usr/bin/env bash
# Retimes the screen recording to exactly 40 s: freeze on each key section, fast scroll in between.
set -euo pipefail
SRC="$1"; OUT="$2"; TMP="$(mktemp -d)"
stops=(0.0 4.0 6.6 7.1 9.0 12.9 16.5)
holds=(4.6 5.0 4.5 4.5 5.0 5.5 6.1)
n=${#stops[@]}; list="$TMP/list.txt"; : > "$list"
for i in $(seq 0 $((n-1))); do
  ffmpeg -y -loglevel error -ss "${stops[$i]}" -i "$SRC" -frames:v 1 "$TMP/f$i.png"
  ffmpeg -y -loglevel error -loop 1 -framerate 30 -i "$TMP/f$i.png" -t "${holds[$i]}" -vf "format=yuv420p" -c:v libx264 -crf 14 -an "$TMP/h$i.mp4"
  echo "file '$TMP/h$i.mp4'" >> "$list"
  if [ $i -lt $((n-1)) ]; then
    a="${stops[$i]}"; b="${stops[$((i+1))]}"; d=$(python3 -c "print($b-$a)")
    ffmpeg -y -loglevel error -ss "$a" -t "$d" -i "$SRC" -vf "setpts=PTS*(0.8/$d),fps=30,format=yuv420p" -t 0.8 -c:v libx264 -crf 14 -an "$TMP/m$i.mp4"
    echo "file '$TMP/m$i.mp4'" >> "$list"
  fi
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" -c:v libx264 -crf 17 -pix_fmt yuv420p -r 30 -an -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
