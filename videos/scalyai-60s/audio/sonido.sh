#!/usr/bin/env bash
# Sintetiza la música de fondo y los efectos con ffmpeg (sin archivos externos, sin derechos de terceros).
set -euo pipefail
cd "$(dirname "$0")"
SR=44100
# --- Música: pad ambiental en cuatro acordes (Am9, Fmaj7, C, G) de 15 s + pulso suave a 90 bpm ---
chord() { # $1 = frecuencias separadas por espacio
  local expr="0"; for f in $1; do expr="$expr+0.11*sin(2*PI*$f*t)+0.05*sin(2*PI*$f*2.003*t)"; done
  echo "($expr)*(0.75+0.25*sin(2*PI*0.18*t))"
}
mk() { ffmpeg -y -loglevel error -f lavfi -i "aevalsrc='$(chord "$1")':s=$SR:d=17:c=stereo" -af "lowpass=f=1800,afade=t=in:d=2.5,afade=t=out:st=14.5:d=2.5" "$2"; }
mk "110 164.81 220 261.63 329.63" c1.wav
mk "87.31 130.81 174.61 220 261.63" c2.wav
mk "130.81 196 261.63 329.63 392" c3.wav
mk "98 146.83 196 246.94 293.66" c4.wav
ffmpeg -y -loglevel error -i c1.wav -i c2.wav -i c3.wav -i c4.wav -filter_complex \
 "[0:a][1:a]acrossfade=d=2[a];[a][2:a]acrossfade=d=2[b];[b][3:a]acrossfade=d=2[pad]" -map "[pad]" pad.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc='0.55*sin(2*PI*58*t)*exp(-7*mod(t,0.6667))':s=$SR:d=62:c=stereo" -af "lowpass=f=140,volume=0.7" pulse.wav
ffmpeg -y -loglevel error -i pad.wav -i pulse.wav -filter_complex \
 "[0:a]volume=1.0[p];[1:a]volume=0.45,afade=t=in:st=0:d=8[k];[p][k]amix=inputs=2:duration=longest:normalize=0,atrim=0:60,afade=t=in:d=3,afade=t=out:st=55:d=5,loudnorm=I=-26:TP=-3:LRA=7" -ar $SR musica.wav
# --- Efectos ---
whoosh() { # $1 duración, $2 archivo
  ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=d=$1:c=pink:r=$SR:a=0.8" -af "bandpass=f=900:w=1.4,afade=t=in:d=$(python3 -c "print($1*0.45)"),afade=t=out:st=$(python3 -c "print($1*0.45)"):d=$(python3 -c "print($1*0.55)"),volume=0.9" -ac 2 "$2"
}
whoosh 0.6 wh.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc='0.4*sin(2*PI*(500*t+900*t*t))*sin(PI*t/0.9)':s=$SR:d=0.9:c=stereo" riser.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc='0.35*(sin(2*PI*880*t)+0.6*sin(2*PI*1318.5*t)+0.3*sin(2*PI*1760*t))*exp(-3.2*t)':s=$SR:d=1.8:c=stereo" chime.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=d=1.1:c=pink:r=$SR:a=0.9" -af "bandpass=f=700:w=1.2,afade=t=in:d=0.45,afade=t=out:st=0.45:d=0.65" -ac 2 wh_long.wav
# --- Mezcla de efectos en una sola pista de 60 s ---
ins=(); fc=""; i=0
add() { ins+=(-i "$1"); fc="$fc[$i:a]adelay=$(python3 -c "print(int($2*1000))")|$(python3 -c "print(int($2*1000))")[x$i];"; i=$((i+1)); }
add riser.wav 4.15
for t in 9.95 17.45 21.95 31.35 39.45 41.85; do add wh.wav $t; done
add riser.wav 26.95
add wh_long.wav 48.7
add chime.wav 50.2
labels=""; for k in $(seq 0 $((i-1))); do labels="$labels[x$k]"; done
ffmpeg -y -loglevel error "${ins[@]}" -filter_complex "${fc}${labels}amix=inputs=$i:duration=longest:normalize=0,apad=whole_dur=60,atrim=0:60" -ar $SR efectos.wav
rm -f c?.wav pad.wav pulse.wav wh.wav riser.wav chime.wav wh_long.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 musica.wav efectos.wav
