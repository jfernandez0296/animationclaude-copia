#!/usr/bin/env bash
# Genera una voz por escena (ElevenLabs, voz George) y la ajusta a su hueco con atempo. La clave la añade el proxy.
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:-JBFqnCBsd6RMkjVDRZzb}"
SOLO="${2:-}"   # opcional: ids separados por coma (ej. v9,v10); vacío = todos
mkdir -p seg
n=$(jq length segmentos.json)
for i in $(seq 0 $((n-1))); do
  id=$(jq -r ".[$i].id" segmentos.json); if [ -n "$SOLO" ] && [[ ",$SOLO," != *",$id,"* ]]; then continue; fi; text=$(jq -r ".[$i].text" segmentos.json); max=$(jq -r ".[$i].max" segmentos.json)
  prev=$([ $i -gt 0 ] && jq -r ".[$((i-1))].text" segmentos.json || echo "")
  next=$([ $i -lt $((n-1)) ] && jq -r ".[$((i+1))].text" segmentos.json || echo "")
  body=$(jq -n --arg t "$text" --arg p "$prev" --arg n "$next" '{text:$t,model_id:"eleven_multilingual_v2",language_code:"es",voice_settings:{stability:0.5,similarity_boost:0.75,style:0.2,use_speaker_boost:true}} + (if $p!="" then {previous_text:$p} else {} end) + (if $n!="" then {next_text:$n} else {} end)')
  curl -sS -m 120 -X POST -H "Content-Type: application/json" -o "seg/$id.mp3" "https://api.elevenlabs.io/v1/text-to-speech/${VOICE}?output_format=mp3_44100_128" -d "$body"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "seg/$id.mp3")
  tempo=$(python3 -c "d=$dur;m=$max;print(round(min(1.3,max(1.0,d/m)),3))")
  ffmpeg -y -loglevel error -i "seg/$id.mp3" -filter:a "atempo=$tempo" -ar 44100 -ac 1 "seg/$id.wav"
  fin=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "seg/$id.wav")
  echo "$id dur=$dur tempo=$tempo final=$fin max=$max"
done
