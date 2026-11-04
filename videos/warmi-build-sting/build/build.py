# Warmi Build product sting (9:16, ~9.5 s): the app builds itself, the benefit lands, the logo closes.
import os, re, wave, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = 9.5
def icon(name, size, color, sw=2.2):
    src = open(os.path.join(ROOT, "assets", "img", f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>'
LOGO = '''<svg id="lg" width="300" height="300" viewBox="0 0 48 48" aria-label="Warmi"><defs><linearGradient id="WG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5421a6"/><stop offset="1" stop-color="#d74ac5"/></linearGradient></defs>
  <circle id="lgc" cx="24" cy="24" r="24" fill="url(#WG)"/><path id="lgs1" d="M24 11l2.6 8.4L35 22l-8.4 2.6L24 33l-2.6-8.4L13 22l8.4-2.6z" fill="#fff"/><path id="lgs2" d="M35 29l1.1 3.4 3.4 1.1-3.4 1.1L35 38l-1.1-3.4-3.4-1.1 3.4-1.1z" fill="#fff"/></svg>'''
ICONS = [("message-circle", 230, "WhatsApp"), ("calendar", 540, "Agenda"), ("mail", 850, "Correo")]
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Warmi Build Sting</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-500-normal.woff2") format("woff2"); font-weight: 400 600; }}
      @font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700 900; }}
      @font-face {{ font-family: "DM Sans"; src: url("assets/fonts/dm-sans-latin-500-normal.woff2") format("woff2"); font-weight: 400 600; }}
      @font-face {{ font-family: "DM Sans"; src: url("assets/fonts/dm-sans-latin-700-normal.woff2") format("woff2"); font-weight: 700 900; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #faf7ff; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: linear-gradient(180deg, #faf7ff 0%, #f3e9ff 60%, #fde9f6 100%); font-family: "DM Sans", sans-serif; color: #170b2e; }}
      .abs {{ position: absolute; }}
      .h {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; letter-spacing: -0.035em; line-height: 1.02; }}
      .blob {{ border-radius: 50%; filter: blur(60px); opacity: 0.55; }}
      .card {{ left: 290px; top: 560px; width: 500px; height: 800px; border-radius: 64px; background: #ffffff; box-shadow: 0 40px 90px rgba(84,33,166,0.22); overflow: hidden; transform-origin: 50% 50%; }}
      .bar {{ border-radius: 18px; background: #efe6fb; }}
      .chip {{ padding: 14px 34px; border-radius: 999px; background: #d74ac5; color: #fff; font-size: 44px; font-weight: 800; white-space: nowrap; }}
      .ic {{ width: 150px; height: 150px; border-radius: 44px; background: #ffffff; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 50px rgba(84,33,166,0.18); }}
      .icl {{ width: 220px; font-size: 32px; font-weight: 700; color: #4b4560; text-align: center; }}
      .pub {{ padding: 12px 24px; border-radius: 999px; background: #1f9d68; color: #fff; font-size: 30px; font-weight: 800; white-space: nowrap; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1080" data-height="1920">
      <div class="abs blob" id="b1" style="left:-120px;top:240px;width:520px;height:520px;background:#c9a7ff"></div>
      <div class="abs blob" id="b2" style="left:640px;top:1180px;width:560px;height:560px;background:#f7a8e3"></div>

      <div class="abs h" id="t1" style="left:80px;top:200px;width:920px;font-size:96px;text-align:center">De tu idea</div>
      <div class="abs h" id="t2" style="left:80px;top:310px;width:920px;font-size:96px;text-align:center;color:#5421a6">a tu app <span style="color:#b5249f">con IA</span></div>
      <div class="abs" id="t3w" style="left:0;top:445px;width:1080px;display:flex;justify-content:center"><div class="chip" id="t3">sin programar</div></div>
      <div class="abs h" id="t4" style="left:80px;top:230px;width:920px;font-size:88px;text-align:center">y automatiza<br /><span style="color:#5421a6">tu trabajo</span></div>

      <svg class="abs" id="links" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-label="Conexiones">
        <path class="ln" d="M440 1240 C400 1330 260 1340 240 1440" fill="none" stroke="#b59ae6" stroke-width="6" stroke-linecap="round"/>
        <path class="ln" d="M540 1260 L540 1440" fill="none" stroke="#b59ae6" stroke-width="6" stroke-linecap="round"/>
        <path class="ln" d="M640 1240 C680 1330 820 1340 840 1440" fill="none" stroke="#b59ae6" stroke-width="6" stroke-linecap="round"/>
      </svg>

      <div class="abs" id="spark" style="left:520px;top:940px;width:40px;height:40px;border-radius:20px;background:#d74ac5;box-shadow:0 0 60px 20px rgba(215,74,197,0.45)"></div>
      <svg class="abs" id="outline" style="left:286px;top:556px" width="508" height="808" viewBox="0 0 508 808" aria-label="Contorno"><rect x="4" y="4" width="500" height="800" rx="64" fill="none" stroke="#5421a6" stroke-width="6" stroke-dasharray="2400" stroke-dashoffset="2400" id="orect"/></svg>
      <div class="abs card" id="card">
        <div class="abs" id="hdr" style="left:0;top:0;width:500px;height:150px;background:linear-gradient(90deg,#5421a6,#7c3aed)"></div>
        <div class="abs h" id="hdt" style="left:44px;top:46px;width:420px;font-size:46px;color:#fff">Mi negocio</div>
        <div class="abs" id="hero" style="left:40px;top:190px;width:420px;height:250px;border-radius:30px;background:linear-gradient(135deg,#f7a8e3,#c9a7ff)"></div>
        <div class="abs bar" id="l1" style="left:40px;top:480px;width:360px;height:34px"></div>
        <div class="abs bar" id="l2" style="left:40px;top:540px;width:280px;height:34px"></div>
        <div class="abs h" id="btn" style="left:40px;top:640px;width:420px;height:104px;border-radius:30px;background:#d74ac5;color:#fff;font-size:42px;display:flex;align-items:center;justify-content:center">Reservar</div>
      </div>
      <div class="abs pub" id="pub" style="left:640px;top:520px">Publicado ✓</div>

      {"".join(f'<div class="abs ic icx" id="ic{i}" style="left:{x - 75}px;top:1440px">{icon(n, 76, "#5421a6")}</div><div class="abs icl icx" id="icl{i}" style="left:{x - 110}px;top:1606px">{lab}</div>' for i, (n, x, lab) in enumerate(ICONS))}

      <div class="abs" id="logo" style="left:390px;top:610px;width:300px;height:300px">{LOGO}</div>
      <div class="abs h" id="wm" style="left:0;top:960px;width:1080px;font-size:132px;text-align:center">Warmi <span style="color:#5421a6">Build</span></div>
      <div class="abs" id="tag" style="left:90px;top:1120px;width:900px;font-size:44px;font-weight:700;color:#4b4560;text-align:center">Programa de IA y automatización</div>
      <div class="abs" id="by" style="left:90px;top:1200px;width:900px;font-size:34px;font-weight:600;color:#7a6f92;text-align:center">por Warmi Ventures</div>
      <audio id="musica" src="audio/musica.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.9"></audio>
      <audio id="efectos" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.6"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const ease = "power3.out";
      tl.set(["#card", "#hdr", "#hdt", "#hero", "#l1", "#l2", "#btn", "#pub", ".icx", ".ln", "#t1", "#t2", "#t3", "#t4", "#logo", "#wm", "#tag", "#by"], {{ autoAlpha: 0 }}, 0);
      // ambient blobs drift the whole time
      tl.fromTo("#b1", {{ x: 0, y: 0 }}, {{ x: 120, y: 80, duration: {T}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#b2", {{ x: 0, y: 0 }}, {{ x: -140, y: -100, duration: {T}, ease: "sine.inOut" }}, 0);
      // 0.0 - 1.9: a spark of light becomes the app, piece by piece
      tl.fromTo("#spark", {{ scale: 0, autoAlpha: 0 }}, {{ scale: 1, autoAlpha: 1, duration: 0.35, ease: "back.out(2)" }}, 0.1);
      tl.to("#spark", {{ scale: 3, autoAlpha: 0, duration: 0.4, ease: "power2.in" }}, 0.45);
      tl.to("#orect", {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut" }}, 0.5);
      tl.fromTo("#card", {{ autoAlpha: 0, scale: 0.96 }}, {{ autoAlpha: 1, scale: 1, duration: 0.4, ease }}, 0.95);
      tl.to("#outline", {{ autoAlpha: 0, duration: 0.3 }}, 1.2);
      tl.fromTo("#hdr", {{ autoAlpha: 0, scaleY: 0, transformOrigin: "50% 0%" }}, {{ autoAlpha: 1, scaleY: 1, duration: 0.35, ease }}, 1.1);
      tl.fromTo("#hdt", {{ autoAlpha: 0, x: -20 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, ease }}, 1.3);
      tl.fromTo("#hero", {{ autoAlpha: 0, scale: 0.85 }}, {{ autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, 1.35);
      tl.fromTo(["#l1", "#l2"], {{ autoAlpha: 0, scaleX: 0, transformOrigin: "0% 50%" }}, {{ autoAlpha: 1, scaleX: 1, duration: 0.3, stagger: 0.1, ease }}, 1.55);
      tl.fromTo("#btn", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 1.8);
      // 1.7 - 3.6: the benefit
      tl.fromTo("#t1", {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease }}, 1.7);
      tl.fromTo("#t2", {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease }}, 2.0);
      tl.fromTo("#t3", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, 2.45);
      tl.to("#btn", {{ scale: 0.94, duration: 0.12, yoyo: true, repeat: 1 }}, 3.0);
      tl.fromTo("#pub", {{ autoAlpha: 0, scale: 0.5, rotate: -8 }}, {{ autoAlpha: 1, scale: 1, rotate: 0, duration: 0.45, ease: "back.out(2.2)" }}, 3.2);
      tl.to(["#t1", "#t2", "#t3"], {{ autoAlpha: 0, y: -30, duration: 0.35, stagger: 0.05, ease: "power2.in" }}, 3.75);
      // 4.0 - 6.2: it also automates the work around it
      tl.to(["#card", "#pub"], {{ y: -80, duration: 0.6, ease: "power2.inOut" }}, 3.9);
      tl.fromTo("#t4", {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease }}, 4.15);
      tl.set(".ln", {{ autoAlpha: 1 }}, 4.35);
      tl.fromTo(".ln", {{ strokeDasharray: 400, strokeDashoffset: 400 }}, {{ strokeDashoffset: 0, duration: 0.5, stagger: 0.12, ease: "power2.out" }}, 4.35);
      tl.fromTo(".ic", {{ autoAlpha: 0, scale: 0.5 }}, {{ autoAlpha: 1, scale: 1, duration: 0.4, stagger: 0.15, ease: "back.out(2)" }}, 4.7);
      tl.fromTo(".icl", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.15, ease }}, 4.85);
      tl.to(".ic", {{ y: -10, duration: 0.4, yoyo: true, repeat: 1, stagger: 0.12, ease: "sine.inOut" }}, 5.4);
      // 6.2 - 9.5: everything gathers into the logo
      tl.to(["#t4", ".icx", ".ln", "#pub"], {{ autoAlpha: 0, duration: 0.35, ease: "power2.in" }}, 6.2);
      tl.to("#card", {{ scale: 0.3, autoAlpha: 0, y: 40, duration: 0.55, ease: "power3.in" }}, 6.25);
      tl.fromTo("#logo", {{ autoAlpha: 0, scale: 0.3, rotate: -30 }}, {{ autoAlpha: 1, scale: 1, rotate: 0, duration: 0.7, ease: "back.out(1.7)" }}, 6.65);
      tl.fromTo("#lgs1", {{ scale: 0, transformOrigin: "24px 22px" }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.5)" }}, 6.95);
      tl.fromTo("#lgs2", {{ scale: 0, transformOrigin: "35px 33.5px" }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, 7.15);
      tl.fromTo("#wm", {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.55, ease }}, 7.2);
      tl.fromTo("#tag", {{ autoAlpha: 0, y: 24 }}, {{ autoAlpha: 1, y: 0, duration: 0.45, ease }}, 7.6);
      tl.fromTo("#by", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.45 }}, 7.95);
      tl.to("#logo", {{ scale: 1.04, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 8.2);
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)

# ---------------------------------------------------------------- audio (numpy): warm pluck bed + soft SFX
SR = 44100; N = int(T * SR); rng = np.random.default_rng(11)
def tt(d): return np.arange(int(d * SR)) / SR
def add(b, x, at, g=1.0):
    i = int(at * SR); x = x[: max(0, len(b) - i)]; b[i:i + len(x)] += g * x
def pluck(f, d=0.9):
    x = tt(d); return np.exp(-x * 5) * (1 - np.exp(-x * 300)) * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x))
def pad(fs, d, a):
    x = tt(d); return a * sum(np.sin(2 * np.pi * f * x) + 0.5 * np.sin(2 * np.pi * f * 1.004 * x) for f in fs) * np.minimum(1, x / 0.4) * np.minimum(1, (d - x) / 0.4)
mus = np.zeros(N); beat = 60 / 112
prog = [[130.81, 196, 261.63, 329.63], [110, 164.81, 220, 261.63], [87.31, 130.81, 174.61, 220], [98, 146.83, 196, 246.94]]
for b in range(4):
    t0 = b * 4 * beat; ch = prog[b % 4] if b < 3 else [130.81, 196, 261.63, 329.63]
    add(mus, pad(ch, 4 * beat + (2 if b == 3 else 0.4), 0.035), t0)
    for e in range(8):
        add(mus, pluck(ch[[0, 2, 1, 3, 2, 3, 1, 2][e]] * 4), t0 + e * beat / 2, 0.06)
    for q in (0, 2):
        x = tt(0.3); add(mus, np.sin(2 * np.pi * (45 + 55 * np.exp(-x * 30)) * x) * np.exp(-x * 10), t0 + q * beat, 0.18)
mus[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
fx = np.zeros(N)
def sm(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
def whoosh(d=0.6):
    x = tt(d); return sm(rng.uniform(-1, 1, len(x)), 14) * np.sin(np.pi * x / d) ** 2 * 2
def pop(f0=600, f1=950):
    x = tt(0.08); return np.sin(2 * np.pi * (f0 + (f1 - f0) * x / 0.08) * x) * np.exp(-x * 45)
def chime(b=880):
    x = tt(2.0); return sum(a * np.sin(2 * np.pi * b * m * x) for a, m in ((1, 1), (0.5, 1.5), (0.25, 2))) * np.exp(-x * 2.5)
def shimmer():
    x = tt(0.6); return sum(np.sin(2 * np.pi * f * x) for f in (1568, 2093, 2637)) * np.exp(-x * 6) * 0.4
add(fx, shimmer(), 0.1, 0.5)
for t in (1.1, 1.35, 1.55, 1.8, 2.45, 3.2, 4.7, 4.85, 5.0): add(fx, pop(), t, 0.3)
add(fx, pop(500, 300), 3.0, 0.4)
add(fx, whoosh(), 3.7, 0.45); add(fx, whoosh(0.7), 6.15, 0.5)
add(fx, chime(), 6.75, 0.35); add(fx, shimmer(), 6.95, 0.4)
def save(path, x, peak):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
save(os.path.join(ROOT, "audio", "raw.wav"), mus, 0.6)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "audio", "raw.wav"), "-af", "loudnorm=I=-18:TP=-2:LRA=7", "-ar", "44100", os.path.join(ROOT, "audio", "musica.wav")], check=True)
os.remove(os.path.join(ROOT, "audio", "raw.wav"))
save(os.path.join(ROOT, "audio", "efectos.wav"), fx, 0.7)
print("ok")
