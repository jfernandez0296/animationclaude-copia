# Builds the timing plan, tempo-fits the narration, and synthesizes music + SFX with numpy.
# Usage: python3 build/audio.py   (run from the project folder)
import json, os, re, subprocess, wave
import numpy as np

SR = 44100
TEMPO = 1.10
GAPS = [0.35, 0.40, 0.75, 0.45, 0.50, 0.65, 0.45]   # silence before r1..r7
TAIL = 2.6
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "audio")

def sh(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True)

def dur(p):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout)

def speech(p, d):
    """speech intervals = complement of silences >= 0.2 s"""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silencedetect=n=-35dB:d=0.2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    out, cur = [], 0.0
    for a, b in zip(ss, se + [d] * (len(ss) - len(se))):
        if a - cur > 0.05:
            out.append([round(cur, 3), round(a, 3)])
        cur = b
    if d - cur > 0.05:
        out.append([round(cur, 3), round(d, 3)])
    return out

segs = json.load(open(os.path.join(A, "segmentos.json")))
os.makedirs(os.path.join(A, "seg", "orig"), exist_ok=True)
t = 0.0
for i, s in enumerate(segs):
    src = os.path.join(A, "seg", "orig", s["id"] + ".wav")
    dst = os.path.join(A, "seg", s["id"] + ".wav")
    if not os.path.exists(src):
        os.replace(dst, src)
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter:a", f"atempo={TEMPO}", "-ar", "44100", "-ac", "1", dst)
    d = dur(dst)
    t += GAPS[i]
    s["start"], s["dur"], s["speech"] = round(t, 3), round(d, 3), speech(dst, d)
    t += d
TOTAL = round(t + TAIL, 2)
json.dump(segs, open(os.path.join(A, "segmentos.json"), "w"), ensure_ascii=False, indent=1)

V = [s["start"] for s in segs]
S = [0.0] + [round(v - 0.45, 3) for v in V[1:]]
plan = {"V": V, "S": S, "D": [s["dur"] for s in segs], "T": TOTAL}
json.dump(plan, open(os.path.join(ROOT, "build", "plan.json"), "w"), indent=1)
print("plan", plan)

# ---------------------------------------------------------------- synthesis helpers
N = int(TOTAL * SR)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    buf[i:i + len(x)] += g * x
def pluck(f, d=1.1, bright=1.0):
    x = tt(d)
    env = np.exp(-x * 4.2) * (1 - np.exp(-x * 300))
    return env * (np.sin(2 * np.pi * f * x) + 0.35 * bright * np.sin(4 * np.pi * f * x) + 0.12 * bright * np.sin(6 * np.pi * f * x))
def pad(freqs, d, amp=0.05):
    x = tt(d)
    y = sum(np.sin(2 * np.pi * f * x) + 0.6 * np.sin(2 * np.pi * f * 1.003 * x) for f in freqs)
    env = np.minimum(1, x / 0.6) * np.minimum(1, (d - x) / 0.6)
    return amp * y * env * (0.85 + 0.15 * np.sin(2 * np.pi * 0.25 * x))
def kick():
    x = tt(0.35)
    return np.sin(2 * np.pi * (48 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 9)
rng = np.random.default_rng(7)
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def smooth(x, k): return np.convolve(x, np.ones(k) / k, mode="same")

# ---------------------------------------------------------------- music
mus = np.zeros(N)
Tt = S[2]                          # the turn: "Entonces conoció a Scaly AI"
beat = 60 / 84
# part A: night, A minor, a ticking wall clock and sparse plucks
A_end = Tt + 0.6
a = pad([110, 164.81, 220, 261.63, 246.94], A_end, 0.035)
fade = np.ones(len(a)); fl = int(0.8 * SR); fade[-fl:] = np.linspace(1, 0, fl)
add(mus, a * fade, 0)
for k in range(int(A_end / beat)):
    tk = k * beat
    add(mus, np.sin(2 * np.pi * 2400 * tt(0.03)) * np.exp(-tt(0.03) * 160), tk, 0.05)
    if k % 2 == 0:
        add(mus, pluck([329.63, 261.63, 293.66, 246.94][(k // 2) % 4], 1.4, 0.6), tk + 0.02, 0.10)
# part B: warm, F - C - G - Am, arpeggio plucks, soft kick + shaker
prog = [[174.61, 220, 261.63, 349.23], [130.81, 196, 261.63, 329.63], [98, 146.83, 196, 246.94], [110, 164.81, 220, 261.63]]
bar = 4 * beat
nb = int((TOTAL - Tt) / bar) + 1
for b in range(nb):
    t0 = Tt + b * bar
    last = t0 + bar >= TOTAL - TAIL
    ch = prog[b % 4] if not last else [130.81, 196, 261.63, 329.63]
    add(mus, pad(ch, bar + 0.7 if not last else TOTAL - t0, 0.04), t0)
    if last:
        add(mus, pluck(523.25, 2.5), t0, 0.12)
        break
    for e in range(8):
        f = ch[[0, 1, 2, 3, 2, 1, 2, 3][e]] * 2
        add(mus, pluck(f, 0.9), t0 + e * beat / 2, 0.075 if e % 2 else 0.095)
    for q in (0, 2):
        add(mus, kick(), t0 + q * beat, 0.22)
    for q in range(4):
        add(mus, smooth(noise(0.05), 3) * np.exp(-tt(0.05) * 60), t0 + q * beat + beat / 2, 0.05)
swell = noise(1.2) * np.linspace(0, 1, int(1.2 * SR)) ** 2
add(mus, smooth(swell, 40), Tt - 1.2, 0.08)
fo = int(2.4 * SR); mus[-fo:] *= np.linspace(1, 0, fo)

# ---------------------------------------------------------------- sfx
fx = np.zeros(N)
def whoosh(d=0.7):
    x = tt(d); env = np.sin(np.pi * x / d) ** 2
    return smooth(noise(d), 18) * env * 2.2
def pop(f0=520, f1=880):
    x = tt(0.09); return np.sin(2 * np.pi * (f0 + (f1 - f0) * x / 0.09) * x) * np.exp(-x * 40)
def buzz():
    x = tt(0.32); return np.sign(np.sin(2 * np.pi * 150 * x)) * 0.5 * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * x)) * np.minimum(1, (0.32 - x) / 0.05)
def chime(base=784):
    x = tt(2.2); return sum(a * np.sin(2 * np.pi * base * m * x) for a, m in ((1, 1), (0.5, 1.5), (0.3, 2), (0.15, 3))) * np.exp(-x * 2.4)
def tick():
    x = tt(0.04); return np.sin(2 * np.pi * 1900 * x) * np.exp(-x * 120)
def riser(d=1.0):
    x = tt(d); return np.sin(2 * np.pi * (300 * x + 500 * x * x / d) ) * (x / d) ** 2 * 0.6
def swish():
    x = tt(0.35); return smooth(noise(0.35), 6) * np.sin(np.pi * x / 0.35) ** 2 * 1.6

V1, V2, V3, V4, V5, V6, V7 = V
S1, S2, S3, S4, S5, S6, S7 = S
for k, d in enumerate((0.6, 1.9, 3.2)):
    add(fx, buzz(), V1 + d, 0.35); add(fx, pop(500, 760), V1 + d + 0.05, 0.3)
add(fx, whoosh(), S2 - 0.25, 0.5)
for d in (0.35, 0.65, 0.95):
    add(fx, pop(380, 560), S2 + d, 0.35)
add(fx, riser(1.0), S3 - 1.0, 0.5); add(fx, chime(784), S3 + 0.3, 0.35)
add(fx, whoosh(0.6), S3 + 2.35, 0.35)
add(fx, tick(), V3 + 6.95, 0.6); add(fx, pop(600, 1000), V3 + 7.25, 0.35)
add(fx, whoosh(), S4 - 0.2, 0.45)
for d in (0.5, 0.75, 1.0, 2.6):
    add(fx, pop(520, 820), S4 + d, 0.3)
add(fx, whoosh(), S5 - 0.2, 0.45)
for d in (1.3, 2.5):
    add(fx, pop(700, 980), S5 + d, 0.3)
add(fx, whoosh(), S6 - 0.2, 0.45); add(fx, swish(), S6 + 1.1, 0.5); add(fx, chime(659.25), S6 + 1.35, 0.25)
add(fx, whoosh(), S7 - 0.2, 0.45); add(fx, chime(1046.5), S7 + 1.0, 0.25)

def save(path, x, peak=0.7):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

save(os.path.join(A, "musica-raw.wav"), mus, 0.6)
sh("ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(A, "musica-raw.wav"), "-af", "loudnorm=I=-23:TP=-3:LRA=9", "-ar", "44100", os.path.join(A, "musica.wav"))
os.remove(os.path.join(A, "musica-raw.wav"))
save(os.path.join(A, "efectos.wav"), fx, 0.7)
sh("python3", os.path.join(A, "ducking.py"), os.path.join(A, "musica.wav"), os.path.join(A, "musica-duck.wav"), os.path.join(A, "segmentos.json"), os.path.join(A, "seg"))
print("audio ok", TOTAL)
