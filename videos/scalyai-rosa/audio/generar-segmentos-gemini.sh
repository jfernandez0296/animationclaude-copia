#!/usr/bin/env bash
# One Gemini TTS take per scene (voice Leda, natural/conversational style), light tempo fit, loudness-matched.
# The API key is added by the credential proxy. Usage: ./generar-segmentos-gemini.sh [voz] [ids]
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:-Leda}"; SOLO="${2:-}"
STYLE="Lee en voz alta, con tono cálido y cercano, como quien cuenta una historia: "
mkdir -p seg
n=$(jq length segmentos.json)
for i in $(seq 0 $((n-1))); do
  id=$(jq -r ".[$i].id" segmentos.json); text=$(jq -r ".[$i].text" segmentos.json); max=$(jq -r ".[$i].max" segmentos.json)
  if [ -n "$SOLO" ] && [[ ",$SOLO," != *",$id,"* ]]; then continue; fi
  body=$(jq -n --arg t "$STYLE$text" --arg v "$VOICE" '{contents:[{parts:[{text:$t}]}],generationConfig:{responseModalities:["AUDIO"],speechConfig:{voiceConfig:{prebuiltVoiceConfig:{voiceName:$v}}}}}')
  for try in 1 2 3 4 5; do
    resp=$(curl -sS -m 120 -H "Content-Type: application/json" "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent" -d "$body")
    data=$(echo "$resp" | jq -r '.candidates[0].content.parts[0].inlineData.data // empty')
    [ -n "$data" ] && break
    echo "$id: sin audio (límite del plan gratuito: 3 por minuto); espero 35 s"; sleep 35
  done
  echo "$data" | base64 -d > "seg/$id.pcm"
  sleep 21   # plan gratuito: 3 solicitudes por minuto
  ffmpeg -y -loglevel error -f s16le -ar 24000 -ac 1 -i "seg/$id.pcm" "seg/$id.raw.wav"
  # trim leading/trailing silence
  ffmpeg -y -loglevel error -i "seg/$id.raw.wav" -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse" "seg/$id.trim.wav"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "seg/$id.trim.wav")
  tempo=$(python3 -c "d=$dur;m=$max;print(round(min(1.3,max(1.0,d/m)),3))")
  ffmpeg -y -loglevel error -i "seg/$id.trim.wav" -filter:a "atempo=$tempo,loudnorm=I=-19:TP=-2:LRA=7" -ar 44100 -ac 1 "seg/$id.wav"
  rm -f "seg/$id.pcm" "seg/$id.raw.wav" "seg/$id.trim.wav"
  echo "$id dur=$dur tempo=$tempo final=$(ffprobe -v error -show_entries format=duration -of csv=p=0 seg/$id.wav) max=$max"
done
