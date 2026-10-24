# Kinetic-typography version of the Rosa story.
# Generates index.html (word-synced type) and audio/efectos.wav from build/plan.json and audio/segmentos.json.
import json, os, re, math, itertools
import numpy as np, wave
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
V, S, T = plan["V"], plan["S"], plan["T"]

# per story beat: background, text colour, keyword colour
BEAT = [("#041b3d", "#fbf1e0", "#f5b94d"),   # r1 night
        ("#fbf1e0", "#041b3d", "#c8442c"),   # r2 chaos
        ("#00646b", "#ffffff", "#f5b94d"),   # r3 Scaly AI + ERP
        ("#fbf1e0", "#041b3d", "#00646b"),   # r4 CRM
        ("#041b3d", "#fbf1e0", "#47d4d4"),   # r5 chatbot
        ("#f5b94d", "#041b3d", "#7a2e12"),   # r6 closes on time
        ("#041b3d", "#fbf1e0", "#f5b94d")]   # r7 CTA
HL = {"once", "noche", "cuaderno", "excel", "esperando", "scaly", "ai.", "erp", "medida:", "falta.", "crm", "cliente,", "chatbot", "ia", "whatsapp", "descansa.", "hora.", "negocio?", "historia."}
EFFECTS = ["rise", "pop", "mask", "slide"]

def phrases(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[,.:;?!…]$", w):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def chars(ws): return sum(len(w) + 1 for w in ws)

# ------------------------------------------------------------------ word timings → screens
screens = []   # dict(seg, t, words=[(word, t)])
for si, s in enumerate(segs):
    ph, iv = phrases(s["text"]), [list(x) for x in s["speech"]]
    while len(ph) > len(iv):
        k = min(range(len(ph) - 1), key=lambda i: chars(ph[i]) + chars(ph[i + 1]))
        ph[k:k + 2] = [ph[k] + ph[k + 1]]
    while len(iv) > len(ph):
        k = min(range(len(iv) - 1), key=lambda i: iv[i + 1][0] - iv[i][1])
        iv[k:k + 2] = [[iv[k][0], iv[k + 1][1]]]
    for words, (a, b) in zip(ph, iv):
        tot, acc, timed = chars(words), 0, []
        for w in words:
            timed.append((w, s["start"] + a + (b - a) * acc / tot))
            acc += len(w) + 1
        # split the phrase into screens of ≤4 words / ≤17 chars, most balanced split
        n = max(math.ceil(chars(words) / 17), math.ceil(len(words) / 4))
        n = min(n, len(words))
        best = None
        for cut in itertools.combinations(range(1, len(words)), n - 1):
            gs = [timed[i:j] for i, j in zip((0,) + cut, cut + (len(words),))]
            score = max(chars([x[0] for x in g]) for g in gs) + 8 * sum(len(g) == 1 and len(g[0][0]) < 4 for g in gs) + 30 * sum(len(g[-1][0]) <= 3 and g[-1][0][-1].isalpha() for g in gs[:-1])
            if best is None or score < best[0]: best = (score, gs)
        for g in best[1]:
            screens.append(dict(seg=si, t=g[0][1], words=g))

def layout(words):
    """largest font size whose greedy line wrap fits 940 px in ≤3 lines"""
    for fs in (230, 200, 176, 154, 136, 120):
        cap = 940 / (0.60 * fs)
        lines, cur = [], ""
        for w in words:
            if len(w) > cap: break
            if cur and len(cur) + 1 + len(w) > cap: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            if len(lines) <= 3: return fs
    return 110

def key(w): return w.lower().strip("¿¡")
scr_html, scr_js, events = [], [], []
for i, sc in enumerate(screens):
    bg, fg, kc = BEAT[sc["seg"]]
    fx = EFFECTS[i % len(EFFECTS)]
    fs = layout([w for w, _ in sc["words"]])
    spans = []
    for j, (w, t) in enumerate(sc["words"]):
        hl = key(w) in HL
        bar = f'<em style="background:{kc}"></em>' if hl else ""
        spans.append(f'<span class="w{" m" if fx == "mask" else ""}" id="w{i}_{j}"><span class="i" style="color:{kc if hl else fg}">{w}</span>{bar}</span>')
        scr_js.append(f'      word("#w{i}_{j}", "{fx}", {t:.3f}, {str(hl).lower()});')
        events.append(("key" if hl else "tick", t))
    scr_html.append(f'      <div class="scr" id="scr{i}" style="font-size:{fs}px">{" ".join(spans)}</div>')
    end = screens[i + 1]["t"] if i + 1 < len(screens) else T - 2.55
    scr_js.append(f'      tl.set("#scr{i}", {{ autoAlpha: 1 }}, {sc["t"] - 0.05:.3f});')
    scr_js.append(f'      tl.to("#scr{i}", {{ autoAlpha: 0, y: -70, duration: 0.12, ease: "power2.in" }}, {end - 0.13:.3f});')
bg_js = "\n".join(f'      tl.to("#bg", {{ backgroundColor: "{BEAT[k][0]}", duration: 0.35, ease: "power1.inOut" }}, {V[k] - 0.3:.3f});' for k in range(1, len(segs)))
for k in range(1, len(segs)): events.append(("whoosh", V[k] - 0.3))
scaly_t = next(t for sc in screens for w, t in sc["words"] if w.startswith("Scaly"))
CTA = T - 2.55
events += [("chime", scaly_t), ("chime", CTA)]

html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>ScalyAI Rosa Kinetic</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-500-latin.woff2") format("woff2"); font-weight: 400 600; }}
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-700-latin.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-800-latin.woff2") format("woff2"); font-weight: 800 900; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #041b3d; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Manrope", system-ui, sans-serif; }}
      #bg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: {BEAT[0][0]}; }}
      .abs {{ position: absolute; }}
      .scr {{ position: absolute; left: 70px; top: 520px; width: 940px; height: 760px; display: flex; flex-wrap: wrap; align-content: center; justify-content: center; column-gap: 0.22em;
              font-weight: 800; letter-spacing: -0.045em; line-height: 0.98; text-align: center; visibility: hidden; opacity: 0; }}
      .w {{ position: relative; display: inline-block; padding: 0 0.02em 0.12em; }}
      .w.m {{ overflow: hidden; }}
      .i {{ display: inline-block; }}
      .w em {{ position: absolute; left: 0.04em; right: 0.04em; bottom: 0.02em; height: 0.09em; border-radius: 0.05em; transform-origin: 0 50%; transform: scaleX(0); }}
      .ghost {{ left: -40px; top: 1330px; width: 1160px; text-align: center; font-size: 420px; font-weight: 800; letter-spacing: -0.06em; color: rgba(251,241,224,0.07); line-height: 1; }}
      .tag {{ left: 70px; top: 130px; font-size: 30px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; }}
      .bars {{ left: 340px; top: 330px; width: 400px; height: 160px; }}
      .bars div {{ position: absolute; height: 34px; border-radius: 17px; transform-origin: 50% 50%; }}
      #cta {{ left: 0; top: 0; width: 1080px; height: 1920px; visibility: hidden; opacity: 0; }}
      .wm {{ left: 0; top: 820px; width: 1080px; text-align: center; font-size: 150px; font-weight: 800; letter-spacing: -0.05em; color: #fbf1e0; }}
      .wa {{ left: 190px; top: 1100px; width: 700px; padding: 30px 0; border-radius: 999px; background: #47d4d4; color: #041b3d; text-align: center; font-size: 56px; font-weight: 800; }}
      .sub {{ left: 0; top: 1250px; width: 1080px; text-align: center; font-size: 40px; font-weight: 700; color: #fbf1e0; }}
      #ghost1, #tag1, #bars1 {{ visibility: hidden; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg"></div>
      <div class="abs ghost" id="ghost1" data-layout-allow-overflow="true" data-layout-allow-overlap="true">23:00</div>
      <div class="abs tag" id="tag1" style="color:#47d4d4">Historia ilustrativa</div>
      <div class="abs bars" id="bars1"><div style="left:0;top:0;width:280px;background:#47d4d4"></div><div style="left:0;top:62px;width:400px;background:#fbf1e0"></div><div style="left:0;top:124px;width:280px;background:#47d4d4"></div></div>

{chr(10).join(scr_html)}

      <div class="abs" id="cta">
        <div class="abs bars" id="bars2" style="top:560px"><div style="left:60px;top:0;width:280px;background:#47d4d4"></div><div style="left:0;top:62px;width:400px;background:#007b83"></div><div style="left:60px;top:124px;width:280px;background:#47d4d4"></div></div>
        <div class="abs wm" id="wm">ScalyAI</div>
        <div class="abs wa" id="wa">WhatsApp 902 342 731</div>
        <div class="abs sub" id="sub">Cuéntanos tu historia</div>
      </div>

{"".join(f'      <audio id="v{i + 1}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for i, s in enumerate(segs))}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.85"></audio>
      <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.5"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const FROM = {{
        rise:  [{{ y: 150, autoAlpha: 0, rotation: 4 }}, {{ y: 0, autoAlpha: 1, rotation: 0, duration: 0.32, ease: "power4.out" }}],
        pop:   [{{ scale: 0.2, autoAlpha: 0 }}, {{ scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(2.4)" }}],
        mask:  [{{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.3, ease: "power4.out" }}],
        slide: [{{ x: -180, autoAlpha: 0, skewX: -12 }}, {{ x: 0, autoAlpha: 1, skewX: 0, duration: 0.3, ease: "expo.out" }}],
      }};
      const word = (sel, fx, t, hl) => {{
        const [a, b] = FROM[fx];
        tl.fromTo(sel + " .i", a, b, t - 0.06);
        if (hl) {{
          tl.to(sel + " em", {{ scaleX: 1, duration: 0.28, ease: "power3.out" }}, t + 0.22);
          tl.to(sel + " .i", {{ scale: 1.08, duration: 0.14, yoyo: true, repeat: 1, ease: "sine.inOut" }}, t + 0.14);
        }}
      }};

      // beat 1 decor
      tl.fromTo("#ghost1", {{ autoAlpha: 0, scale: 1.15 }}, {{ autoAlpha: 1, scale: 1, duration: 1.2, ease: "power2.out" }}, 0.1);
      tl.to("#ghost1", {{ autoAlpha: 0, duration: 0.3 }}, {V[1] - 0.35:.3f});
      tl.fromTo("#tag1", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.4 }}, 0.2);
      tl.to("#tag1", {{ autoAlpha: 0, duration: 0.3 }}, {V[1] - 0.35:.3f});

      // background colour per story beat
{bg_js}

      // Scaly bars draw on "Scaly AI"
      tl.set("#bars1", {{ autoAlpha: 1 }}, {scaly_t - 0.1:.3f});
      tl.fromTo("#bars1 div", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, stagger: 0.08, ease: "expo.out" }}, {scaly_t - 0.1:.3f});
      tl.to("#bars1", {{ autoAlpha: 0, duration: 0.25 }}, {V[3] - 0.35:.3f});

      // word-synced type
{chr(10).join(scr_js)}

      // end lockup
      tl.set("#cta", {{ autoAlpha: 1 }}, {CTA:.3f});
      tl.fromTo("#bars2 div", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, stagger: 0.08, ease: "expo.out" }}, {CTA:.3f});
      tl.fromTo("#wm", {{ autoAlpha: 0, y: 60 }}, {{ autoAlpha: 1, y: 0, duration: 0.45, ease: "power4.out" }}, {CTA + 0.25:.3f});
      tl.fromTo("#wa", {{ autoAlpha: 0, scale: 0.8 }}, {{ autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {CTA + 0.6:.3f});
      tl.fromTo("#sub", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.4 }}, {CTA + 0.9:.3f});
      tl.to("#wa", {{ scale: 1.04, duration: 0.35, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {CTA + 1.3:.3f});

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)

# ------------------------------------------------------------------ SFX
SR = 48000
buf = np.zeros(int(T * SR) + SR)
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d * SR)) / SR
def add(x, at, g):
    i = int(at * SR); buf[i:i + len(x)] += g * x[: len(buf) - i]
def whoosh():
    d = 0.45; n = rng.uniform(-1, 1, int(d * SR)); n = np.convolve(n, np.ones(40) / 40, "same")
    e = np.sin(np.pi * tt(d) / d) ** 2; return n * e
def tick():
    d = 0.05; return np.sin(2 * np.pi * 1800 * tt(d)) * np.exp(-tt(d) * 90)
def key_hit():
    d = 0.18; return np.sin(2 * np.pi * 220 * tt(d) * (1 + 0.6 * np.exp(-tt(d) * 30))) * np.exp(-tt(d) * 22)
def chime():
    d = 1.6; x = tt(d); return sum(np.sin(2 * np.pi * f * x) * np.exp(-x * (3 + k)) / (k + 1) for k, f in enumerate((880, 1318.5, 1760)))
for kind, t in events:
    if kind == "tick": add(tick(), t, 0.10)
    elif kind == "key": add(key_hit(), t, 0.45)
    elif kind == "whoosh": add(whoosh(), max(0, t - 0.15), 0.5)
    else: add(chime(), t, 0.35)
buf = buf[: int(T * SR)]
buf = buf / max(1e-6, np.abs(buf).max()) * 0.6
pcm = (np.stack([buf, buf], 1) * 32767).astype("<i2")
with wave.open(os.path.join(ROOT, "audio", "efectos.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(len(screens), "screens; scaly at", round(scaly_t, 2), "CTA at", round(CTA, 2))
for sc in screens: print(f'{sc["t"]:6.2f}', " ".join(w for w, _ in sc["words"]))
