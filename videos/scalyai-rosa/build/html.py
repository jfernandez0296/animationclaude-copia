# Generates index.html from build/plan.json and audio/segmentos.json.
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
V, S, T = plan["V"], plan["S"], plan["T"]

# ------------------------------------------------------------------ captions
HL = {"once", "noche", "esperando", "scaly", "ai", "erp", "medida", "falta", "crm", "cliente", "chatbot", "ia", "whatsapp", "descansa", "hora"}
def phrases(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[,.:;?!…]$", w) or w.endswith("..."):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def chars(ws): return sum(len(w) + 1 for w in ws)
caps = []
for s in segs[:6]:
    ph, iv = phrases(s["text"]), [list(x) for x in s["speech"]]
    while len(ph) > len(iv):          # merge the shortest adjacent pair of phrases
        k = min(range(len(ph) - 1), key=lambda i: chars(ph[i]) + chars(ph[i + 1]))
        ph[k:k + 2] = [ph[k] + ph[k + 1]]
    while len(iv) > len(ph):          # merge intervals across the smallest gap
        k = min(range(len(iv) - 1), key=lambda i: iv[i + 1][0] - iv[i][1])
        iv[k:k + 2] = [[iv[k][0], iv[k + 1][1]]]
    for words, (a, b) in zip(ph, iv):
        import itertools, math
        n = max(1, math.ceil(chars(words) / 22))
        n = min(n, len(words))
        best = None
        for cut in itertools.combinations(range(1, len(words)), n - 1):
            gs = [words[i:j] for i, j in zip((0,) + cut, cut + (len(words),))]
            score = max(chars(x) for x in gs) + (6 if any(len(x) == 1 and len(x[0]) < 6 for x in gs) else 0)
            if best is None or score < best[0]:
                best = (score, gs)
        groups = best[1]
        tot, t0 = sum(chars(x) for x in groups), a
        for x in groups:
            d = (b - a) * chars(x) / tot
            caps.append([s["start"] + t0, s["start"] + t0 + d, x])
            t0 += d
for i in range(len(caps)):             # each chunk stays until the next one (or 0.3 s after its phrase)
    nxt = caps[i + 1][0] if i + 1 < len(caps) else caps[i][1] + 0.4
    caps[i][1] = min(nxt, caps[i][1] + 0.3) if nxt - caps[i][1] > 0.6 else nxt
def capword(w):
    k = re.sub(r"[^\wáéíóúñ]", "", w.lower())
    return f"<b>{w}</b>" if k in HL else w
cap_html = "\n".join(f'      <div class="cap" id="cap{i}" data-layout-allow-overlap="true"><span>{" ".join(capword(w) for w in c[2])}</span></div>' for i, c in enumerate(caps))
cap_js = "\n".join(f'      capShow("#cap{i}", {c[0]:.3f}, {c[1]:.3f});' for i, c in enumerate(caps))

# ------------------------------------------------------------------ illustrations
def rosa(id_, expr, style):
    eyes = {
        "worried": '<circle cx="168" cy="200" r="8" fill="#2a1a14"/><circle cx="232" cy="200" r="8" fill="#2a1a14"/>'
                   '<path d="M148 178 L186 170" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/><path d="M252 178 L214 170" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/>'
                   '<path d="M180 250 Q200 238 220 250" fill="none" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/>',
        "happy": '<path d="M156 202 Q168 186 180 202" fill="none" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/><path d="M220 202 Q232 186 244 202" fill="none" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/>'
                 '<path d="M172 236 Q200 276 228 236 Z" fill="#8a3b2e"/>',
        "sleep": '<path d="M156 200 Q168 210 180 200" fill="none" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/><path d="M220 200 Q232 210 244 200" fill="none" stroke="#2a1a14" stroke-width="7" stroke-linecap="round"/>'
                 '<ellipse cx="200" cy="246" rx="8" ry="6" fill="#8a3b2e"/>',
    }[expr]
    return f'''<svg class="abs" id="{id_}" style="{style}" width="400" height="520" viewBox="0 0 400 520" aria-label="Rosa, personaje ilustrativo">
          <circle cx="200" cy="58" r="40" fill="#3b2a24"/>
          <ellipse cx="200" cy="178" rx="104" ry="112" fill="#3b2a24"/>
          <path d="M60 520 C60 400 110 330 200 330 C290 330 340 400 340 520 Z" fill="#f5b94d"/>
          <path d="M135 352 L265 352 L292 520 L108 520 Z" fill="#007b83"/>
          <rect x="166" y="420" width="68" height="46" rx="12" fill="#0a6b72"/>
          <rect x="178" y="268" width="44" height="66" rx="18" fill="#e3a171"/>
          <circle cx="120" cy="202" r="17" fill="#e8a97c"/><circle cx="280" cy="202" r="17" fill="#e8a97c"/>
          <circle cx="120" cy="226" r="7" fill="#f5b94d"/><circle cx="280" cy="226" r="7" fill="#f5b94d"/>
          <ellipse cx="200" cy="192" rx="80" ry="88" fill="#f2bb90"/>
          <path d="M118 178 C118 112 160 94 200 94 C240 94 282 112 282 178 C262 142 236 130 200 130 C170 130 140 144 118 178 Z" fill="#3b2a24"/>
          <circle cx="150" cy="226" r="14" fill="#ef9a86" opacity="0.55"/><circle cx="250" cy="226" r="14" fill="#ef9a86" opacity="0.55"/>
          {eyes}
        </svg>'''
def person(id_, cls, skin, hair, shirt, style):
    return f'''<svg class="abs {cls}" id="{id_}" style="{style}" width="140" height="170" viewBox="0 0 140 170" aria-label="Cliente ilustrativo">
          <path d="M8 170 C8 122 38 100 70 100 C102 100 132 122 132 170 Z" fill="{shirt}"/>
          <circle cx="70" cy="62" r="40" fill="{skin}"/>
          <path d="M30 60 C30 16 110 16 110 60 C96 38 44 38 30 60 Z" fill="{hair}"/>
          <circle cx="56" cy="66" r="4.5" fill="#2a1a14"/><circle cx="84" cy="66" r="4.5" fill="#2a1a14"/>
          <path d="M60 84 L80 84" stroke="#2a1a14" stroke-width="4" stroke-linecap="round"/>
        </svg>'''
STARS = [(40, 60), (120, 30), (300, 50), (330, 150), (250, 250), (60, 200), (180, 300), (330, 300)]
def night(p):
    stars = "".join(f'<div class="abs star {p}st" style="left:{x}px;top:{y}px"></div>' for x, y in STARS)
    jars = "".join(f'<div class="abs jar" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c}"></div>'
                   for x, y, w, h, c in ((80, 610, 70, 90, "#f5b94d"), (165, 630, 60, 70, "#47d4d4"), (240, 600, 80, 100, "#ef9a86"), (80, 820, 90, 60, "#47d4d4"), (185, 790, 70, 90, "#f5b94d")))
    return f'''<div class="abs win" id="{p}win" style="left:600px;top:170px;width:390px;height:390px">{stars}<div class="abs moon" style="left:200px;top:60px"></div></div>
        <div class="abs" style="left:540px;top:0;width:4px;height:120px;background:#c98b4a"></div>
        <div class="abs shade" id="{p}shade" style="left:480px;top:118px"></div>
        <div class="abs" style="left:60px;top:700px;width:300px;height:18px;border-radius:9px;background:#c98b4a"></div>
        <div class="abs" style="left:60px;top:880px;width:300px;height:18px;border-radius:9px;background:#c98b4a"></div>
        {jars}
        <div class="abs wclock" id="{p}clock" style="left:110px;top:200px"><div class="abs hand hh" style="transform:rotate(-30deg)"></div><div class="abs hand mh"></div><div class="abs" style="left:68px;top:68px;width:24px;height:24px;border-radius:12px;background:#041b3d"></div></div>
        <div class="abs h" style="left:90px;top:400px;width:300px;font-size:56px;color:#47d4d4">23:00</div>'''
COUNTER = '<div class="abs counter"></div><div class="abs counter-top"></div><div class="abs" style="left:0;top:1250px;width:1080px;height:8px;background:#6a4122"></div><div class="abs" style="left:0;top:1640px;width:1080px;height:8px;background:#6a4122"></div>'
CURSOR = '<svg class="abs" id="cur" style="left:640px;top:1060px" width="70" height="90" viewBox="0 0 70 90" aria-label="Cursor"><path d="M6 4 L6 70 L24 54 L38 86 L52 80 L38 50 L62 48 Z" fill="#ffffff" stroke="#041b3d" stroke-width="5" stroke-linejoin="round"/></svg>'
HEART = '<svg class="abs" id="heart" style="left:300px;top:700px" width="90" height="80" viewBox="0 0 90 80" aria-label="Corazón"><path d="M45 76 C10 52 2 34 2 22 C2 10 12 2 24 2 C34 2 41 8 45 15 C49 8 56 2 66 2 C78 2 88 10 88 22 C88 34 80 52 45 76 Z" fill="#ef6f5a"/></svg>'
LOGO_X = [340, 260, 340]; LOGO_W = [400, 560, 400]; LOGO_Y = [560, 630, 700]
ROWS = [("Café", 0.85, "Hay stock", "ok"), ("Pan", 0.6, "Hay stock", "ok"), ("Galletas", 0.1, "Falta", "low")]
ROW_Y = [470, 640, 810]; TRACK_X = 130; TRACK_W = 560
bars, rows = [], []
for i, (name, v, st, kind) in enumerate(ROWS):
    y = ROW_Y[i]
    rows.append(f'<div class="abs h rl" style="left:{TRACK_X}px;top:{y}px;width:500px;font-size:48px;color:#041b3d">{name}</div>'
                f'<div class="abs rl" style="left:{TRACK_X}px;top:{y + 74}px;width:{TRACK_W}px;height:44px;border-radius:22px;background:#eef1f4"></div>'
                f'<div class="pill rl {"stlow" if kind == "low" else "stok"}" id="pill{i}" style="left:740px;top:{y + 64}px">{st}</div>')
    bars.append(f'<div class="abs lbar" id="lb{i}" style="left:{TRACK_X}px;top:{y + 74}px;width:{LOGO_W[i]}px;height:44px;border-radius:22px;background:{["#47d4d4", "#007b83", "#47d4d4"][i]}"></div>')
morph = [dict(dx=LOGO_X[i] - TRACK_X, dy=LOGO_Y[i] - (ROW_Y[i] + 74), sx=round(ROWS[i][1] * TRACK_W / LOGO_W[i], 4)) for i in range(3)]

html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>ScalyAI Rosa</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-500-latin.woff2") format("woff2"); font-weight: 400 600; }}
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-700-latin.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-800-latin.woff2") format("woff2"); font-weight: 800 900; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #041b3d; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #041b3d; font-family: "Manrope", system-ui, sans-serif; color: #041b3d; }}
      .abs {{ position: absolute; }}
      .sc {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      .h {{ font-weight: 800; letter-spacing: -0.03em; line-height: 1.06; }}
      .pill {{ position: absolute; padding: 12px 28px; border-radius: 999px; font-size: 34px; font-weight: 800; white-space: nowrap; }}
      .chip {{ position: absolute; left: 90px; top: 140px; padding: 14px 32px; border-radius: 999px; font-size: 40px; font-weight: 800; white-space: nowrap; }}
      .win {{ border: 14px solid #c98b4a; border-radius: 24px; background: #0a2550; overflow: hidden; }}
      .star {{ width: 10px; height: 10px; border-radius: 5px; background: #f5e6b8; }}
      .moon {{ width: 110px; height: 110px; border-radius: 55px; background: #f5e6b8; box-shadow: 0 0 60px rgba(245,230,184,0.5); }}
      .shade {{ width: 120px; height: 72px; background: #f5b94d; clip-path: polygon(22% 0, 78% 0, 100% 100%, 0 100%); }}
      .glow {{ width: 640px; height: 640px; border-radius: 320px; background: radial-gradient(circle, rgba(245,185,77,0.38) 0%, rgba(245,185,77,0) 70%); }}
      .jar {{ border-radius: 14px 14px 18px 18px; border: 5px solid #041b3d; }}
      .wclock {{ width: 160px; height: 160px; border-radius: 80px; background: #fbf1e0; border: 10px solid #c98b4a; }}
      .hand {{ left: 76px; width: 8px; border-radius: 4px; background: #041b3d; transform-origin: 50% 100%; }}
      .hh {{ top: 36px; height: 44px; }}
      .mh {{ top: 18px; height: 62px; }}
      .counter {{ left: 0; top: 1060px; width: 1080px; height: 860px; background: #7a4c2a; }}
      .counter-top {{ left: 0; top: 1040px; width: 1080px; height: 36px; background: #c98b4a; }}
      .phone {{ width: 160px; height: 280px; border-radius: 30px; background: #0b2c5c; border: 8px solid #10284f; overflow: hidden; }}
      .screen {{ left: 10px; top: 16px; width: 124px; height: 232px; border-radius: 18px; background: #47d4d4; }}
      .badge {{ width: 72px; height: 72px; border-radius: 36px; background: #c8442c; color: #fff; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center; border: 5px solid #041b3d; }}
      .notif {{ padding: 16px 26px; border-radius: 22px; background: #fff; font-size: 32px; font-weight: 700; color: #041b3d; white-space: nowrap; box-shadow: 0 12px 30px rgba(0,0,0,0.25); }}
      .notif i {{ display: inline-block; width: 18px; height: 18px; border-radius: 9px; background: #ef6f5a; margin-right: 12px; }}
      .card {{ background: #fff; border-radius: 34px; border: 6px solid #041b3d; overflow: hidden; }}
      .cell {{ border-right: 3px solid #e3e6ea; border-bottom: 3px solid #e3e6ea; }}
      .mrow {{ height: 86px; border-bottom: 3px solid #eef0f2; }}
      .unread {{ width: 52px; height: 52px; border-radius: 26px; background: #c8442c; color: #fff; font-size: 30px; font-weight: 800; display: flex; align-items: center; justify-content: center; }}
      .wait {{ padding: 10px 26px; border-radius: 26px; background: #fff; border: 5px solid #041b3d; font-size: 44px; font-weight: 800; color: #041b3d; line-height: 1; }}
      .stok {{ background: #d6f3f0; color: #00585e; }}
      .stlow {{ background: #ffd3c9; color: #9a2a14; }}
      .stway {{ background: #fde8bd; color: #7a4b00; }}
      .note {{ font-size: 40px; font-weight: 700; color: #041b3d; }}
      .bub {{ padding: 24px 32px; border-radius: 32px; font-size: 38px; font-weight: 600; line-height: 1.25; }}
      .z {{ font-size: 64px; font-weight: 800; color: #f5e6b8; }}
      .cap {{ position: absolute; left: 60px; width: 960px; top: 1300px; text-align: center; }}
      .cap span {{ display: inline-block; background: #041b3d; color: #ffffff; font-size: 62px; font-weight: 800; letter-spacing: -0.01em; padding: 16px 34px; border-radius: 26px; line-height: 1.15; box-shadow: 0 12px 34px rgba(0,0,0,0.28); }}
      .cap b {{ color: #f5b94d; font-weight: 800; }}
      .bar {{ position: absolute; height: 44px; border-radius: 22px; }}
      #s2, #s3, #s4, #s5, #s6, #s7, .cap {{ visibility: hidden; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1080" data-height="1920">

      <!-- S1 · 23:00, Rosa still answering messages -->
      <div class="sc" id="s1" style="background:#041b3d">
        <div class="abs glow" id="glow1" data-layout-allow-overflow="true" style="left:220px;top:-60px"></div>
        {night("a")}
        {rosa("rosa1", "worried", "left:300px;top:560px")}
        {COUNTER}
        <div class="abs phone" id="ph1" style="left:720px;top:820px"><div class="abs screen" id="scr1"></div></div>
        <div class="abs badge" id="bdg1" style="left:840px;top:790px"><span id="bdgn">1</span></div>
        <div class="abs notif nt1" style="left:500px;top:690px"><i></i>Nuevo mensaje</div>
        <div class="abs notif nt1" style="left:560px;top:590px"><i></i>Nuevo mensaje</div>
        <div class="abs notif nt1" style="left:480px;top:490px"><i></i>Nuevo mensaje</div>
        <div class="abs" id="disc" style="left:90px;top:1500px;width:900px;font-size:30px;font-weight:600;color:#e7c9a0">Historia ilustrativa · Rosa es un personaje ficticio</div>
      </div>

      <!-- S2 · notebook, Excel, WhatsApp and customers waiting -->
      <div class="sc" id="s2" style="background:#fbf1e0">
        <div class="abs card c2" id="nbk" style="left:80px;top:170px;width:430px;height:400px;background:#fff7d6;transform:rotate(-6deg)">
          <div class="abs h" style="left:34px;top:26px;width:300px;font-size:44px">Ventas</div>
          <div class="abs" style="left:34px;top:120px;width:340px;height:6px;background:#d9c58a"></div>
          <div class="abs" style="left:34px;top:190px;width:280px;height:6px;background:#d9c58a"></div>
          <div class="abs" style="left:34px;top:260px;width:320px;height:6px;background:#d9c58a"></div>
          <div class="abs" style="left:34px;top:330px;width:200px;height:6px;background:#d9c58a"></div>
          <div class="abs" style="left:290px;top:220px;width:110px;height:110px;border-radius:55px;border:8px solid rgba(160,100,40,0.35)"></div>
        </div>
        <div class="abs card c2" id="xls" style="left:470px;top:300px;width:540px;height:420px;transform:rotate(4deg)">
          <div class="abs" style="left:0;top:0;width:540px;height:84px;background:#1f7a4c"></div>
          <div class="abs h" style="left:30px;top:20px;width:400px;font-size:38px;color:#fff">stock.xlsx</div>
          {"".join(f'<div class="abs cell" style="left:{c * 108}px;top:{84 + r * 67}px;width:108px;height:67px"></div>' for r in range(5) for c in range(5))}
          <div class="abs h" id="q" style="left:226px;top:232px;width:96px;height:56px;background:#ffd3c9;color:#9a2a14;font-size:44px;text-align:center">?</div>
        </div>
        <div class="abs card c2" id="wsp" style="left:90px;top:640px;width:520px;height:470px;transform:rotate(-2deg)">
          <div class="abs" style="left:0;top:0;width:520px;height:84px;background:#007b83"></div>
          <div class="abs h" style="left:30px;top:20px;width:400px;font-size:38px;color:#fff">Mensajes</div>
          {"".join(f'<div class="abs mrow" style="left:0;top:{100 + r * 90}px;width:520px"></div><div class="abs" style="left:30px;top:{112 + r * 90}px;width:60px;height:60px;border-radius:30px;background:{c}"></div><div class="abs" style="left:110px;top:{132 + r * 90}px;width:{w}px;height:18px;border-radius:9px;background:#e3e6ea"></div><div class="abs unread ur" style="left:430px;top:{116 + r * 90}px">{n}</div>' for r, (c, w, n) in enumerate((("#f5b94d", 220, 3), ("#47d4d4", 260, 1), ("#ef9a86", 200, 5), ("#9fb4d1", 240, 2))))}
        </div>
        {person("p1", "cust", "#e8b48f", "#2b2b2b", "#47d4d4", "left:880px;top:760px")}
        {person("p2", "cust", "#c98f63", "#6b3f22", "#f5b94d", "left:880px;top:930px")}
        {person("p3", "cust", "#f2c9a6", "#9a6b3a", "#ef9a86", "left:700px;top:1050px")}
        <div class="abs wait w2" style="left:720px;top:790px">…</div>
        <div class="abs wait w2" style="left:720px;top:960px">…</div>
        <div class="abs wait w2" style="left:860px;top:1100px">…</div>
      </div>

      <!-- S3 · Scaly AI: the logo bars become the inventory -->
      <div class="sc" id="s3" style="background:#041b3d">
        <div class="abs card" id="erp" style="left:70px;top:250px;width:940px;height:960px;border:none;border-radius:44px"></div>
        <div class="abs rl" style="left:130px;top:300px;width:600px;font-size:34px;font-weight:700;color:#5b6a7a">Tienda de Rosa · Inventario</div>
        <div class="pill rl" style="left:130px;top:360px;background:#041b3d;color:#47d4d4">ERP a su medida</div>
        {"".join(rows)}
        <div class="pill stway" id="pill2b" style="left:740px;top:{ROW_Y[2] + 64}px">En camino</div>
        <div class="abs h rl" id="btn" style="left:130px;top:1010px;width:820px;height:120px;border-radius:26px;background:#007b83;color:#fff;font-size:46px;display:flex;align-items:center;justify-content:center">Pedir galletas</div>
        {"".join(bars)}
        <div class="abs h" id="wm" style="left:0;top:800px;width:1080px;font-size:170px;color:#fff;text-align:center">ScalyAI</div>
        {CURSOR}
      </div>

      <!-- S4 · CRM: Don Luis -->
      <div class="sc" id="s4" style="background:#f3e7d0">
        <div class="chip" id="chip4" style="background:#041b3d;color:#47d4d4">CRM · cada cliente, por su nombre</div>
        <div class="abs card c4" id="k1" style="left:430px;top:290px;width:520px;height:300px;transform:rotate(-9deg);background:#fde8bd"></div>
        <div class="abs card c4" id="k2" style="left:470px;top:300px;width:520px;height:300px;transform:rotate(7deg);background:#d6f3f0"></div>
        <div class="abs card c4" id="k3" style="left:380px;top:330px;width:620px;height:690px">
          {person("pl", "", "#c98f63", "#d9d9d9", "#007b83", "left:36px;top:30px")}
          <div class="abs h" style="left:200px;top:52px;width:400px;font-size:56px">Don Luis</div>
          <div class="pill" style="left:200px;top:130px;background:#fde8bd;color:#7a4b00;font-size:30px;padding:8px 22px">Cliente frecuente</div>
          <div class="abs nl" style="left:40px;top:270px;width:36px;height:36px;border-radius:18px;background:#007b83"></div><div class="abs note nl" style="left:96px;top:262px;width:500px">Café de los lunes</div>
          <div class="abs nl" style="left:40px;top:380px;width:36px;height:36px;border-radius:18px;background:#007b83"></div><div class="abs note nl" style="left:96px;top:372px;width:500px">Pide galletas de avena</div>
          <div class="abs nl" style="left:40px;top:490px;width:36px;height:36px;border-radius:18px;background:#f5b94d"></div><div class="abs note nl" style="left:96px;top:482px;width:500px">Cumpleaños: viernes</div>
        </div>
        {rosa("rosa4", "happy", "left:-10px;top:620px;transform:scale(0.82);transform-origin:0 0")}
        {HEART}
        <div class="abs" style="left:0;top:1060px;width:1080px;height:860px;background:#e7d3ae"></div>
      </div>

      <!-- S5 · night again: Rosa rests, the chatbot answers -->
      <div class="sc" id="s5" style="background:#041b3d">
        {night("b")}
        <div class="chip" id="chip5" style="top:60px;background:#47d4d4;color:#041b3d">Chatbot con IA</div>
        {rosa("rosa5", "sleep", "left:120px;top:560px")}
        <div class="abs z zz" style="left:300px;top:520px">z</div><div class="abs z zz" style="left:340px;top:470px">z</div><div class="abs z zz" style="left:380px;top:420px">Z</div>
        {COUNTER}
        <div class="abs phone" id="ph5" style="left:780px;top:820px"><div class="abs screen"></div></div>
        <div class="abs bub" id="q5" style="left:400px;top:590px;width:600px;background:#fff;color:#041b3d;border-bottom-left-radius:8px">¿Tienen galletas para mañana?</div>
        <div class="abs bub" id="a5" style="left:470px;top:720px;width:530px;background:#47d4d4;color:#041b3d;border-bottom-right-radius:8px">¡Sí! Te separo un paquete.</div>
      </div>

      <!-- S6 · 6 p. m., the sign flips to "Cerrado" -->
      <div class="sc" id="s6" style="background:linear-gradient(180deg,#ffd9a8 0%,#fbf1e0 60%)">
        <div class="abs" id="sun6" style="left:640px;top:170px;width:360px;height:360px;border-radius:180px;background:#f5b94d"></div>
        <div class="abs h" id="time6" style="left:90px;top:170px;width:500px;font-size:84px;color:#a86400">6:00 p. m.</div>
        <div class="abs" id="door" style="left:580px;top:360px;width:400px;height:820px;border-radius:24px 24px 0 0;background:#fff;border:14px solid #041b3d"></div>
        <div class="abs" style="left:620px;top:400px;width:320px;height:300px;border-radius:12px;background:#cdeee9"></div>
        <div class="abs" style="left:900px;top:820px;width:22px;height:70px;border-radius:11px;background:#041b3d"></div>
        <div class="abs" style="left:700px;top:450px;width:6px;height:90px;background:#041b3d;transform:rotate(30deg);transform-origin:50% 0"></div>
        <div class="abs" style="left:856px;top:450px;width:6px;height:90px;background:#041b3d;transform:rotate(-30deg);transform-origin:50% 0"></div>
        <div class="abs h" id="sgo" style="left:640px;top:520px;width:280px;height:120px;border-radius:20px;background:#007b83;color:#fff;font-size:52px;display:flex;align-items:center;justify-content:center">Abierto</div>
        <div class="abs h" id="sgc" style="left:640px;top:520px;width:280px;height:120px;border-radius:20px;background:#ef6f5a;color:#fff;font-size:52px;display:flex;align-items:center;justify-content:center">Cerrado</div>
        {rosa("rosa6", "happy", "left:110px;top:640px")}
        <div class="abs" style="left:0;top:1170px;width:1080px;height:750px;background:#e7d3ae"></div>
      </div>

      <!-- S7 · CTA -->
      <div class="sc" id="s7" style="background:#041b3d">
        <div class="bar" id="x0" style="left:90px;top:560px;width:400px;background:linear-gradient(90deg,#007b83,#47d4d4)"></div>
        <div class="bar" id="x1" style="left:90px;top:630px;width:560px;background:#007b83"></div>
        <div class="bar" id="x2" style="left:90px;top:700px;width:400px;background:#47d4d4"></div>
        <div class="abs h" id="xw" style="left:84px;top:800px;width:920px;font-size:190px;color:#fff">ScalyAI</div>
        <div class="abs h" id="xt" style="left:90px;top:1080px;width:900px;font-size:100px;color:#fff">¿Y tu <span style="color:#47d4d4">negocio</span>?</div>
        <div class="abs" id="xb" style="left:90px;top:1220px;width:900px;font-size:46px;font-weight:600;color:#d7e3f3">ERP, CRM y chatbots con IA.</div>
        <div class="abs h" id="xc" style="left:90px;top:1360px;width:900px;padding:38px 40px;border-radius:999px;background:#47d4d4;color:#041b3d;font-size:56px;text-align:center">Cuéntanos tu historia</div>
      </div>

      <!-- captions (synced to the narration) -->
{cap_html}

{"".join(f'      <audio id="v{i + 1}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for i, s in enumerate(segs))}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.85"></audio>
      <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.5"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const S = {json.dumps(S)}, V = {json.dumps(V)};
      const pop = (sel, t, d) => tl.fromTo(sel, {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: d || 0.45, ease: "power3.out" }}, t);
      const reveal = (id, t, x, y) => {{
        tl.set(id, {{ autoAlpha: 1 }}, t);
        tl.fromTo(id, {{ clipPath: "circle(0% at " + x + " " + y + ")" }}, {{ clipPath: "circle(150% at " + x + " " + y + ")", duration: 0.7, ease: "power2.inOut" }}, t);
      }};
      const capShow = (sel, a, b) => {{
        tl.fromTo(sel, {{ autoAlpha: 0, y: 14, scale: 0.94 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.16, ease: "back.out(2)" }}, a - 0.04);
        tl.set(sel, {{ autoAlpha: 0 }}, b);
      }};
      tl.set(["#s2", "#s3", "#s4", "#s5", "#s6", "#s7", ".cap"], {{ autoAlpha: 0 }}, 0);

      // S1 · night
      tl.fromTo("#s1", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.4 }}, 0);
      tl.fromTo("#glow1", {{ opacity: 0.55 }}, {{ opacity: 1, duration: 0.18, yoyo: true, repeat: 15, ease: "sine.inOut" }}, 0.2);
      tl.fromTo(".ast", {{ opacity: 0.3 }}, {{ opacity: 1, duration: 0.6, yoyo: true, repeat: 7, stagger: 0.12, ease: "sine.inOut" }}, 0);
      tl.fromTo("#rosa1", {{ y: 30 }}, {{ y: 0, duration: 0.8, ease: "power2.out" }}, 0.1);
      tl.fromTo("#ph1", {{ y: 60, autoAlpha: 0 }}, {{ y: 0, autoAlpha: 1, duration: 0.5, ease: "back.out(1.6)" }}, 0.4);
      [0.6, 1.9, 3.2].forEach((d, k) => {{
        tl.to("#ph1", {{ x: 8, duration: 0.05, yoyo: true, repeat: 5 }}, V[0] + d);
        tl.to("#scr1", {{ opacity: 0.55, duration: 0.15, yoyo: true, repeat: 1 }}, V[0] + d);
      }});
      tl.fromTo(".nt1", {{ autoAlpha: 0, y: 60, scale: 0.8 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.4, stagger: 1.3, ease: "back.out(1.7)" }}, V[0] + 0.65);
      tl.fromTo("#bdg1", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, V[0] + 0.6);
      const nb = {{ v: 1 }};
      tl.to(nb, {{ v: 12, duration: 4.0, ease: "none", onUpdate: () => {{ document.getElementById("bdgn").textContent = Math.round(nb.v); }} }}, V[0] + 0.7);
      tl.fromTo("#disc", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.4 }}, 0.5);

      // S2 · scattered work, customers waiting
      reveal("#s2", S[1], "540px", "185px");
      tl.fromTo(".c2", {{ autoAlpha: 0, y: -200, rotate: "-=12" }}, {{ autoAlpha: 1, y: 0, rotate: "+=12", duration: 0.55, stagger: 0.3, ease: "back.out(1.4)" }}, S[1] + 0.35);
      tl.fromTo(".ur", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, stagger: 0.12, ease: "back.out(2.4)" }}, S[1] + 1.5);
      tl.fromTo("#q", {{ scale: 0.6 }}, {{ scale: 1.15, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, V[1] + 2.4);
      tl.fromTo(".cust", {{ autoAlpha: 0, y: 60 }}, {{ autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.18, ease: "back.out(1.5)" }}, V[1] + 4.1);
      tl.fromTo(".w2", {{ autoAlpha: 0, scale: 0.6 }}, {{ autoAlpha: 1, scale: 1, duration: 0.3, stagger: 0.18, ease: "back.out(2)" }}, V[1] + 4.4);
      tl.to(".w2", {{ opacity: 0.45, duration: 0.35, yoyo: true, repeat: 3, stagger: 0.12, ease: "sine.inOut" }}, V[1] + 5.0);
      tl.set("#s1", {{ autoAlpha: 0 }}, S[1] + 0.75);

      // S3 · the turn: Scaly AI logo bars morph into Rosa's inventory
      reveal("#s3", S[2], "540px", "960px");
      tl.set(["#erp", ".rl"], {{ autoAlpha: 0 }}, 0);
      {"".join(f'tl.set("#lb{i}", {{ x: {m["dx"]}, y: {m["dy"]}, scaleX: 1, transformOrigin: "0% 50%", autoAlpha: 0 }}, 0);' for i, m in enumerate(morph))}
      tl.fromTo(["#lb0", "#lb1", "#lb2"], {{ autoAlpha: 0, scaleX: 0 }}, {{ autoAlpha: 1, scaleX: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" }}, S[2] + 0.35);
      pop("#wm", S[2] + 0.75, 0.5);
      tl.to("#wm", {{ autoAlpha: 0, y: -40, duration: 0.35, ease: "power2.in" }}, V[2] + 2.3);
      tl.fromTo("#erp", {{ autoAlpha: 0, scale: 0.9 }}, {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, V[2] + 2.45);
      {"".join(f'tl.to("#lb{i}", {{ x: 0, y: 0, scaleX: {m["sx"]}, duration: 0.8, ease: "power3.inOut" }}, V[2] + 2.45 + {i * 0.08});' for i, m in enumerate(morph))}
      tl.to("#lb2", {{ backgroundColor: "#ef6f5a", duration: 0.4 }}, V[2] + 3.1);
      tl.fromTo(".rl", {{ autoAlpha: 0, y: 16 }}, {{ autoAlpha: 1, y: 0, duration: 0.35, stagger: 0.04 }}, V[2] + 3.0);
      tl.set("#pill2b", {{ autoAlpha: 0 }}, 0);
      tl.fromTo("#cur", {{ autoAlpha: 0, x: 240, y: 200 }}, {{ autoAlpha: 1, x: 0, y: 0, duration: 0.7, ease: "power2.out" }}, V[2] + 5.4);
      tl.to("#pill2", {{ scale: 1.15, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, V[2] + 6.75);
      tl.to("#btn", {{ scale: 0.96, duration: 0.1, yoyo: true, repeat: 1 }}, V[2] + 6.95);
      tl.to("#lb2", {{ scaleX: {round(0.7 * TRACK_W / LOGO_W[2], 4)}, backgroundColor: "#f5b94d", duration: 0.6, ease: "power2.out" }}, V[2] + 7.05);
      tl.to("#pill2", {{ autoAlpha: 0, duration: 0.15 }}, V[2] + 7.2);
      tl.fromTo("#pill2b", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, V[2] + 7.25);
      tl.set("#s2", {{ autoAlpha: 0 }}, S[2] + 0.75);

      // S4 · CRM
      tl.set("#s4", {{ autoAlpha: 1 }}, S[3]);
      tl.fromTo("#s4", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.inOut" }}, S[3]);
      pop("#chip4", S[3] + 0.4);
      tl.fromTo(".c4", {{ autoAlpha: 0, y: 160 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, stagger: 0.2, ease: "back.out(1.3)" }}, S[3] + 0.5);
      tl.fromTo(".nl", {{ autoAlpha: 0, x: -24 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.12 }}, S[3] + 1.4);
      tl.fromTo("#rosa4", {{ autoAlpha: 0, y: 80 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "back.out(1.4)" }}, S[3] + 0.8);
      tl.fromTo("#heart", {{ autoAlpha: 0, scale: 0.3, y: 30 }}, {{ autoAlpha: 1, scale: 1, y: 0, duration: 0.45, ease: "back.out(2.2)" }}, V[3] + 3.5);
      tl.to("#heart", {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, V[3] + 4.0);
      tl.set("#s3", {{ autoAlpha: 0 }}, S[3] + 0.65);

      // S5 · night again, chatbot answers
      reveal("#s5", S[4], "795px", "365px");
      pop("#chip5", S[4] + 0.5);
      tl.fromTo("#rosa5", {{ rotate: 0, transformOrigin: "50% 100%" }}, {{ rotate: -6, duration: 1.2, ease: "sine.inOut" }}, S[4] + 0.3);
      tl.fromTo(".zz", {{ autoAlpha: 0, y: 30 }}, {{ autoAlpha: 1, y: -30, duration: 0.9, stagger: 0.35, repeat: 1, ease: "sine.out" }}, S[4] + 0.6);
      tl.fromTo(".bst", {{ opacity: 0.3 }}, {{ opacity: 1, duration: 0.6, yoyo: true, repeat: 5, stagger: 0.1 }}, S[4]);
      tl.fromTo("#q5", {{ autoAlpha: 0, y: 40, scale: 0.92 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }}, S[4] + 1.3);
      tl.fromTo("#a5", {{ autoAlpha: 0, y: 40, scale: 0.92 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }}, S[4] + 2.5);
      tl.set("#s4", {{ autoAlpha: 0 }}, S[4] + 0.75);

      // S6 · 6 p. m., closing on time
      reveal("#s6", S[5], "820px", "350px");
      tl.fromTo("#sun6", {{ y: -40 }}, {{ y: 40, duration: 2.6, ease: "none" }}, S[5]);
      pop("#time6", S[5] + 0.35);
      tl.fromTo("#rosa6", {{ autoAlpha: 0, y: 80 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "back.out(1.4)" }}, S[5] + 0.45);
      tl.set("#sgc", {{ scaleX: 0 }}, 0);
      tl.to("#sgo", {{ scaleX: 0, duration: 0.18, ease: "power2.in" }}, S[5] + 1.1);
      tl.to("#sgc", {{ scaleX: 1, duration: 0.22, ease: "back.out(2)" }}, S[5] + 1.28);
      tl.to("#rosa6", {{ y: -18, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.out" }}, S[5] + 1.5);
      tl.set("#s5", {{ autoAlpha: 0 }}, S[5] + 0.75);

      // S7 · CTA
      reveal("#s7", S[6], "540px", "960px");
      tl.fromTo(["#x0", "#x1", "#x2"], {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out", stagger: 0.1 }}, S[6] + 0.4);
      pop("#xw", S[6] + 0.7);
      pop("#xt", S[6] + 1.2);
      pop("#xb", S[6] + 1.9);
      tl.fromTo("#xc", {{ autoAlpha: 0, scale: 0.85 }}, {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, S[6] + 2.4);
      tl.to("#xc", {{ scale: 1.04, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, S[6] + 3.0);
      tl.set("#s6", {{ autoAlpha: 0 }}, S[6] + 0.75);

      // captions
{cap_js}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("captions", len(caps)); [print(f"{a:6.2f}-{b:6.2f}", " ".join(w)) for a, b, w in caps]
