#!/usr/bin/env bash
# Genera la voz en off con Gemini TTS. Requiere GEMINI_API_KEY en el entorno.
# Uso: ./generar-voz.sh [voz] [salida.wav]   (voz por defecto: Kore)
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:-Kore}"
OUT="${2:-voz.wav}"
: "${GEMINI_API_KEY:?Falta GEMINI_API_KEY}"
TEXT="Lee en español neutro latinoamericano, tono cercano y seguro, ritmo pausado y claro: $(tr '\n' ' ' < guion-voz.txt)"
BODY=$(jq -n --arg t "$TEXT" --arg v "$VOICE" '{contents:[{parts:[{text:$t}]}],generationConfig:{responseModalities:["AUDIO"],speechConfig:{voiceConfig:{prebuiltVoiceConfig:{voiceName:$v}}}}}')
curl -sS -m 180 -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent" -d "$BODY" \
  | jq -r '.candidates[0].content.parts[0].inlineData.data' | base64 -d > voz.pcm
ffmpeg -y -loglevel error -f s16le -ar 24000 -ac 1 -i voz.pcm "$OUT"
rm -f voz.pcm
ffprobe -v error -show_entries format=duration -of default=nw=1 "$OUT"
