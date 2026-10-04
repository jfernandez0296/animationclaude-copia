#!/usr/bin/env bash
# Genera la voz en off con ElevenLabs. La clave (encabezado xi-api-key) la añade el proxy de credenciales.
# Uso: ./generar-voz-elevenlabs.sh [voice_id] [salida.mp3]
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:-JBFqnCBsd6RMkjVDRZzb}"   # George (premade)
OUT="${2:-voz-eleven.mp3}"
TEXT=$(tr '\n' ' ' < guion-voz.txt)
BODY=$(jq -n --arg t "$TEXT" '{text:$t,model_id:"eleven_multilingual_v2",language_code:"es",voice_settings:{stability:0.5,similarity_boost:0.75,style:0.2,use_speaker_boost:true}}')
curl -sS -m 180 -X POST -H "Content-Type: application/json" -o "$OUT" -w "HTTP %{http_code}\n" \
  "https://api.elevenlabs.io/v1/text-to-speech/${VOICE}?output_format=mp3_44100_128" -d "$BODY"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$OUT" || { cat "$OUT"; exit 1; }
