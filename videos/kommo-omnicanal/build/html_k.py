# Vertical tutorial: Kommo + WhatsApp coexistence + Instagram + TikTok.
import json, os, re, math, itertools, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
SEG = {s["id"]: s for s in segs}
S, T = plan["S"], plan["T"]
def p(i, k=0, off=0.0):
    s = SEG[i]; iv = s["speech"]; k = min(k, len(iv) - 1)
    return round(s["start"] + iv[k][0] + off, 3)
EV = []
def ev(kind, t): EV.append([kind, round(t, 3)])
BRAND = {"whatsapp": "#25D366", "meta": "#0467DF", "instagram": "#FF0069", "tiktok": "#000000"}
def logo(name, size, color=None):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, f"logo-{name}.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-label="{name}"><path d="{d}" fill="{color or BRAND[name]}"/></svg>'
def icon(name, size, color="#041b3d", sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>')
def kommo(size, color="#041b3d"):   # plain wordmark (not the official logo)
    return f'<span class="kw" style="font-size:{size}px;color:{color}">kommo</span>'
def badge(inner, sid, x, y, s=150):
    return f'<div class="abs lbadge" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px">{inner}</div>'

# ---------------------------------------------------------------- captions
HL = {"whatsapp", "instagram", "tiktok", "kommo", "coexistencia", "bandeja", "instalar", "meta", "qr", "historial", "treinta", "integraciones",
      "empresa", "business", "lead", "embudo", "scaly", "ojo", "versión"}
def phrases(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[,.:;?!]$", w): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def chars(ws): return sum(len(w) + 1 for w in ws)
caps = []
for s in segs:
    ph, iv = phrases(s["text"]), [list(x) for x in s["speech"]]
    while len(ph) > len(iv):
        k = min(range(len(ph) - 1), key=lambda i: chars(ph[i]) + chars(ph[i + 1])); ph[k:k + 2] = [ph[k] + ph[k + 1]]
    while len(iv) > len(ph):
        k = min(range(len(iv) - 1), key=lambda i: iv[i + 1][0] - iv[i][1]); iv[k:k + 2] = [[iv[k][0], iv[k + 1][1]]]
    for words, (a, b) in zip(ph, iv):
        if s["id"] == "k8" and s["start"] + a > 86.3: continue
        n = min(len(words), max(1, math.ceil(chars(words) / 24)))
        best = None
        for cut in itertools.combinations(range(1, len(words)), n - 1):
            gs = [words[i:j] for i, j in zip((0,) + cut, cut + (len(words),))]
            sc = max(chars(x) for x in gs) + (8 if any(len(x) == 1 and len(x[0]) < 6 for x in gs) else 0)
            if best is None or sc < best[0]: best = (sc, gs)
        tot, t0 = sum(chars(x) for x in best[1]), a
        for x in best[1]:
            d = (b - a) * chars(x) / tot; caps.append([s["start"] + t0, s["start"] + t0 + d, x]); t0 += d
for i in range(len(caps)):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else caps[i][1] + 0.4
    caps[i][1] = min(nxt, caps[i][1] + 0.35) if nxt - caps[i][1] > 0.7 else nxt
def cw(w):
    k = re.sub(r"[^\wáéíóúñ]", "", w.lower())
    return f"<b>{w}</b>" if k in HL else w
CAPS = "\n".join(f'      <div class="cap" id="cap{i}" data-layout-allow-overlap="true"><span>{" ".join(cw(w) for w in c[2])}</span></div>' for i, c in enumerate(caps))
CAPJS = "\n".join(f'      capShow("#cap{i}", {c[0]:.3f}, {c[1]:.3f});' for i, c in enumerate(caps))

# ---------------------------------------------------------------- pieces
def header(n, title, sid, badge_inner):
    return (f'<div class="abs kick" id="{sid}k" style="left:70px;top:190px">PASO {n} DE 3</div>'
            f'<div class="abs ttl" id="{sid}t" style="left:70px;top:236px;width:760px">{title}</div>' + badge(badge_inner, f"{sid}lg", 860, 180))
ILLU = '<div class="abs illu">Recreación ilustrativa · logos de sus respectivas marcas</div>'
STEPS = [("WhatsApp", "whatsapp"), ("Instagram", "instagram"), ("TikTok", "tiktok"), ("Bandeja", None)]
stepbar = "".join(f'<div class="abs step" id="st{i}" style="left:{40 + i * 252}px;top:70px"><b>{logo(l, 24) if l else icon("inbox", 24)}</b>{n}</div>' for i, (n, l) in enumerate(STEPS))
def kmock(id_, inner, y=420, h=880):
    side = "".join(f'<div class="ki">{icon(n, 34, "#9fb4d1")}</div>' for n in ("layout-dashboard", "kanban", "messages-square", "users", "settings"))
    return (f'<div class="abs kmock" id="{id_}" style="left:60px;top:{y}px;width:960px;height:{h}px">'
            f'<div class="abs kside">{kommo(30, "#ffffff")}<div style="height:30px"></div>{side}</div>{inner}</div>')
random.seed(4)
def qr(size=300):
    n = 21; c = size / n; cells = []
    def finder(x0, y0):
        return [(x0 + i, y0 + j) for i in range(7) for j in range(7) if i in (0, 6) or j in (0, 6) or (2 <= i <= 4 and 2 <= j <= 4)]
    on = set(finder(0, 0) + finder(14, 0) + finder(0, 14))
    for i in range(n):
        for j in range(n):
            infinder = (i < 8 and j < 8) or (i > 12 and j < 8) or (i < 8 and j > 12)
            if not infinder and random.random() < 0.48: on.add((i, j))
    rects = "".join(f'<rect x="{i * c:.1f}" y="{j * c:.1f}" width="{c + 0.4:.1f}" height="{c + 0.4:.1f}"/>' for i, j in sorted(on))
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-label="Código QR ilustrativo"><g fill="#111b21">{rects}</g></svg>'
def phone(id_, x, y, inner, title="WhatsApp Business", w=400, h=700):
    return (f'<div class="abs phone" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="abs pscreen" style="width:{w - 28}px;height:{h - 28}px"></div>'
            f'<div class="abs phead" style="width:{w - 28}px"><div class="abs pav">{logo("whatsapp", 32, "#ffffff")}</div><div class="abs pname">{title}</div></div>{inner}</div>')

# ---------------------------------------------------------------- scenes
apps = [("whatsapp", 120, 560, 5), ("instagram", 440, 720, 3), ("tiktok", 760, 560, 7)]
A = f'''
      <div class="sc" id="sA" style="background:#041b3d">
        <div class="abs" id="aK" style="left:70px;top:150px;font-size:34px;font-weight:800;letter-spacing:4px;color:#47d4d4">TUTORIAL</div>
        <div class="abs h" id="aT" style="left:70px;top:205px;width:940px;font-size:84px;color:#fff">WhatsApp, Instagram y TikTok en una sola bandeja</div>
        {"".join(f'<div class="abs app aap" id="ap{i}" style="left:{x}px;top:{y}px">{logo(n, 120, "#ffffff" if n == "tiktok" else None)}<div class="abs nb">{c}</div></div>' for i, (n, x, y, c) in enumerate(apps))}
        <div class="abs inbox" id="aIn" style="left:190px;top:900px;width:700px">
          <div class="ibh">{kommo(44, "#041b3d")}<span class="ibt">Bandeja de entrada</span></div>
          {"".join(f'<div class="ibr" id="aR{i}"><span class="ibl">{logo(n, 40, "#111111" if n == "tiktok" else None)}</span><span class="ibn">{nm}</span><span class="ibm">{m}</span></div>' for i, (n, nm, m) in enumerate([("whatsapp", "Lucía", "¿Tienen envío hoy?"), ("instagram", "@mateo.pe", "Precio del modelo azul"), ("tiktok", "@ana_rv", "Vi tu video, ¿hay stock?")]))}
        </div>
        <div class="abs h" id="aSub" style="left:70px;top:1330px;width:940px;font-size:46px;color:#f5b94d;text-align:center">Kommo + coexistencia de WhatsApp</div>
      </div>'''

B = f'''
      <div class="sc light" id="sB">
        {header(1, "WhatsApp con coexistencia", "B", logo("whatsapp", 92))}
        <div class="abs grp" id="Bdia">
          {phone("Bph", 70, 430, '<div class="abs bubble me" id="Bb1" style="top:170px">Hola, ¿tienen envío hoy?</div><div class="abs bubble bot" id="Bb2" style="top:290px">¡Sí! Te lo enviamos esta tarde.</div>', "Mi negocio", 380, 640)}
          <div class="abs h" style="left:70px;top:1090px;width:380px;font-size:28px;text-align:center;color:#2b3444">Tu celular · app Business</div>
          <div class="abs kwin" id="Bkw" style="left:520px;top:470px;width:490px;height:560px">
            <div class="ibh">{kommo(34, "#041b3d")}<span class="ibt">Chats</span></div>
            <div class="abs bubble me" id="Bk1" style="top:150px;right:20px">Hola, ¿tienen envío hoy?</div>
            <div class="abs bubble bot" id="Bk2" style="top:280px;left:20px">¡Sí! Te lo enviamos esta tarde.</div>
          </div>
          <div class="abs h" style="left:520px;top:1090px;width:490px;font-size:28px;text-align:center;color:#2b3444">Kommo · en la computadora</div>
          <div class="abs sync" id="Bsy" style="left:445px;top:680px">{icon("history", 70, "#007b83", 2.2)}</div>
          <div class="abs synct" id="Bst" style="left:420px;top:770px">mismo número</div>
        </div>
        {kmock("Bkm", f"""
          <div class="abs kh" style="left:200px;top:40px">Integraciones</div>
          <div class="abs icard" id="Bic" style="left:200px;top:120px"><div class="icl">{logo("whatsapp", 70)}</div><div><div class="ict">WhatsApp Business</div><div class="ics">App + API en el mismo número</div></div><div class="abs kbtn" id="Binst" style="right:24px;top:40px">Instalar</div></div>
          <div class="abs mdlg" id="Bmeta" style="left:200px;top:330px"><div class="mt">{logo("meta", 40)}<span>Iniciar sesión con Meta</span></div>
            <div class="mrow" id="Bm1"><div class="ml">Portafolio comercial</div><div class="mv">Mi negocio ▾</div></div>
            <div class="mrow" id="Bm2"><div class="ml">Número de WhatsApp</div><div class="mv">+51 9•• ••• •••</div></div></div>
        """)}
        {phone("Bqr", 300, 430, f'<div class="abs qrmsg" style="left:24px;top:140px">Escanea el código QR para vincular con Kommo</div><div class="abs qrbox" id="Bqrc" style="left:52px;top:270px">{qr(300)}<div class="abs scanl" id="Bscan"></div></div><div class="abs hdlg" id="Bhist" style="left:24px;top:390px"><div class="h" style="font-size:28px">¿Compartir historial de chats?</div><div class="hb"><span class="hbn">Ahora no</span><span class="hby">Compartir</span></div></div>', "WhatsApp Business", 480, 820)}
        <div class="abs chip30" id="B30" style="left:120px;top:1270px">{icon("history", 36, "#00585e")}<span>Se importan chats activos de los últimos 30 días</span></div>
        <div class="abs reqs" id="Breq" style="left:70px;top:430px;width:940px">
          <div class="h" style="font-size:44px;margin-bottom:12px">Antes de conectar</div>
          <div class="rq" id="Brq0">{icon("smartphone", 46, "#007b83")}<span>App WhatsApp Business versión <b>2.24.17</b> o superior</span></div>
          <div class="rq" id="Brq1">{icon("clock", 46, "#007b83")}<span>Una cuenta con algo de antigüedad y buena calidad de mensajes</span></div>
          <div class="rq warnq" id="Brq2">{icon("badge-check", 46, "#a86400")}<span>Las cuentas nuevas no califican de inmediato</span></div>
          <div class="rq" id="Brq3">{logo("meta", 46)}<span>Portafolio comercial de Meta (o créalo al configurar)</span></div>
        </div>
        {ILLU}
      </div>'''

C = f'''
      <div class="sc light" id="sC">
        {header(2, "Conecta Instagram", "C", logo("instagram", 92))}
        {kmock("Ckm", f"""
          <div class="abs crumbs" style="left:200px;top:40px"><span class="cr" id="Cc0">{icon("settings", 28, "#041b3d")} Ajustes</span><span class="cr" id="Cc1">› Integraciones</span><span class="cr" id="Cc2">› Instagram</span></div>
          <div class="abs icard" id="Cic" style="left:200px;top:130px"><div class="icl">{logo("instagram", 70)}</div><div><div class="ict">Instagram</div><div class="ics">Mensajes directos, comentarios y menciones</div></div></div>
          <div class="abs igbtn" id="Cbtn" style="left:200px;top:330px">{logo("instagram", 36, "#ffffff")}<span>Continuar con Instagram</span></div>
          <div class="abs okb" id="Cok" style="left:200px;top:470px">{icon("circle-check", 36, "#ffffff")}<span>Instagram conectado</span></div>
          <div class="abs dm" id="Cdm" style="left:200px;top:590px"><span class="ibl">{logo("instagram", 40)}</span><span><b>@mateo.pe</b> · ¿Precio del modelo azul?</span></div>
        """)}
        <div class="abs note2" id="Creq" style="left:60px;top:1316px;width:960px">{logo("meta", 40)}<span>Necesitas una cuenta de empresa de Instagram vinculada a tu portafolio de Meta.</span></div>
        {ILLU}
      </div>'''

D = f'''
      <div class="sc light" id="sD">
        {header(3, "Conecta TikTok", "D", logo("tiktok", 88))}
        {kmock("Dkm", f"""
          <div class="abs kh" style="left:200px;top:40px">Integraciones</div>
          <div class="abs srch" style="left:200px;top:120px">{icon("search", 32, "#5a6270")}<span id="Dq">TikTok</span><i class="caret" id="Dcar"></i></div>
          <div class="abs icard" id="Dic" style="left:200px;top:240px"><div class="icl">{logo("tiktok", 66)}</div><div><div class="ict">TikTok</div><div class="ics">Mensajes de TikTok Business</div></div><div class="abs kbtn" id="Dinst" style="right:24px;top:40px">Instalar</div></div>
          <div class="abs mdlg" id="Dauth" style="left:200px;top:450px"><div class="mt">{logo("tiktok", 40)}<span>Continuar con TikTok</span></div>
            <div class="mrow"><div class="ml">Cuenta</div><div class="mv">TikTok Business · @minegocio</div></div>
            <div class="abs kbtn" id="Dok" style="left:30px;top:250px">Autorizar</div></div>
          <div class="abs okb" id="Ddone" style="left:200px;top:470px">{icon("circle-check", 36, "#ffffff")}<span>TikTok conectado</span></div>
        """)}
        {ILLU}
      </div>'''

lead = lambda n, t: f'<div class="lcd"><span class="ibl">{logo(n, 30, "#111111" if n == "tiktok" else None)}</span>{t}</div>'
E = f'''
      <div class="sc light" id="sE">
        <div class="abs ttl" id="Et" style="left:70px;top:200px;width:940px">Una sola bandeja</div>
        <div class="abs inbox" id="Ein" style="left:60px;top:340px;width:960px">
          <div class="ibh">{kommo(44, "#041b3d")}<span class="ibt">Bandeja de entrada</span></div>
          {"".join(f'<div class="ibr Er" id="Er{i}"><span class="ibl">{logo(n, 44, "#111111" if n == "tiktok" else None)}</span><span class="ibn">{nm}</span><span class="ibm">{m}</span></div>' for i, (n, nm, m) in enumerate([("whatsapp", "Lucía", "¿Tienen envío hoy?"), ("instagram", "@mateo.pe", "Precio del modelo azul"), ("tiktok", "@ana_rv", "Vi tu video, ¿hay stock?")]))}
        </div>
        <div class="abs pipe" id="Epipe" style="left:60px;top:840px;width:960px">
          <div class="pcol"><div class="pch">Leads entrantes</div>{lead("tiktok", "@ana_rv")}{lead("instagram", "@mateo.pe")}</div>
          <div class="pcol"><div class="pch">Contactado</div>{lead("whatsapp", "Lucía")}</div>
          <div class="pcol"><div class="pch">Venta</div><div class="lcd ghost">—</div></div>
        </div>
      </div>
      <div class="sc" id="sH" style="background:#041b3d">
        <div class="bar" id="x0" style="left:340px;top:520px;width:400px;background:linear-gradient(90deg,#007b83,#47d4d4)"></div>
        <div class="bar" id="x1" style="left:260px;top:590px;width:560px;background:#007b83"></div>
        <div class="bar" id="x2" style="left:340px;top:660px;width:400px;background:#47d4d4"></div>
        <div class="abs h" id="xw" style="left:0;top:760px;width:1080px;font-size:170px;color:#fff;text-align:center">ScalyAI</div>
        <div class="abs h" id="xt" style="left:60px;top:990px;width:960px;font-size:62px;color:#47d4d4;text-align:center">¿Lo configuramos contigo? Escríbenos.</div>
        <div class="abs" id="xr" style="left:0;top:1250px;width:1080px;display:flex;justify-content:center;gap:36px">{"".join(f'<div class="lbadge mini">{logo(b, 64)}</div>' for b in ("whatsapp", "instagram", "tiktok", "meta"))}<div class="lbadge mini">{kommo(30)}</div></div>
      </div>'''

# ---------------------------------------------------------------- timeline
J = []
def js(s): J.append("      " + s)
def show(sel, t, d=0.45, y=30): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y} }}, {{ autoAlpha: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.3f});')
def popin(sel, t, d=0.4): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: {d}, ease: "back.out(1.8)" }}, {t:.3f});'); ev("pop", t)
def hide(sel, t, d=0.3): js(f'tl.to("{sel}", {{ autoAlpha: 0, duration: {d} }}, {t:.3f});')
def tap(sel, t): js(f'tl.to("{sel}", {{ scale: 0.92, duration: 0.09, yoyo: true, repeat: 1 }}, {t:.3f});'); ev("click", t)
def reveal(sel, t, x="50%", y="50%"):
    js(f'tl.set("{sel}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{sel}", {{ clipPath: "circle(0% at {x} {y})" }}, {{ clipPath: "circle(150% at {x} {y})", duration: 0.7, ease: "power2.inOut" }}, {t:.3f});')
def stepstate(i, t):
    for k in range(4):
        cls = "step cur" if k == i else ("step done" if k < i else "step")
        js(f'tl.set("#st{k}", {{ attr: {{ class: "abs {cls}" }} }}, {t:.3f});')
def logopop(sid, t): js(f'tl.fromTo("{sid}", {{ autoAlpha: 0, scale: 0.4, rotate: -20 }}, {{ autoAlpha: 1, scale: 1, rotate: 0, duration: 0.55, ease: "back.out(2)" }}, {t:.3f});'); ev("pop", t)

js('tl.set(["#sB", "#sC", "#sD", "#sE", "#sH", "#stepbar", ".cap"], { autoAlpha: 0 }, 0);')
# A
show("#aK", 0.2); show("#aT", 0.35, 0.6)
for i in range(3): logopop(f"#ap{i}", 1.0 + i * 0.45)
js(f'tl.fromTo(".nb", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, stagger: 0.4, ease: "back.out(2.5)" }}, 2.6);')
js(f'tl.to(".aap", {{ rotate: 6, duration: 0.12, yoyo: true, repeat: 9, stagger: 0.1, ease: "sine.inOut" }}, 3.4);')
js('tl.set(["#aIn", "#aR0", "#aR1", "#aR2", "#aSub"], { autoAlpha: 0 }, 0);')
show("#aIn", p("k1", 2), 0.5, 60)
for i in range(3):
    js(f'tl.to("#ap{i}", {{ x: {[260, -60, -380][i]}, y: {[440, 300, 440][i]}, scale: 0.3, autoAlpha: 0, duration: 0.55, ease: "power2.in" }}, {p("k1", 2, 0.3 + i * 0.25):.3f});')
    popin(f"#aR{i}", p("k1", 2, 0.75 + i * 0.25))
show("#aSub", p("k1", 3))
# B (coexistence)
reveal("#sB", S[1]); js(f'tl.set("#sA", {{ autoAlpha: 0 }}, {S[1] + 0.75:.3f});')
show("#stepbar", S[1] + 0.4, 0.4, -20); stepstate(0, S[1] + 0.4)
show("#Bk", S[1] + 0.6); show("#Bt", S[1] + 0.75); logopop("#Blg", S[1] + 0.9)
js('tl.set(["#Bb1", "#Bb2", "#Bk1", "#Bk2", "#Bkw", "#Bsy", "#Bst", "#Bkm", "#Bmeta", "#Bm1", "#Bm2", "#Bqr", "#Bhist", "#B30", "#Breq", "#Brq0", "#Brq1", "#Brq2", "#Brq3"], { autoAlpha: 0 }, 0);')
show("#Bph", p("k2", 3), 0.5, 50); show("#Bb1", p("k2", 3, 0.6)); show("#Bb2", p("k2", 3, 1.6))
show("#Bkw", p("k2", 4), 0.5, 50); popin("#Bsy", p("k2", 4, 0.1)); show("#Bst", p("k2", 4, 0.3))
js(f'tl.to("#Bsy", {{ rotate: 360, duration: 1.6, ease: "power1.inOut" }}, {p("k2", 4, 0.3):.3f});')
show("#Bk1", p("k2", 4, 0.6)); show("#Bk2", p("k2", 4, 1.0))
hide("#Bdia", p("k3", 0, -0.3)); show("#Bkm", p("k3", 0), 0.45, 40)
tap("#Binst", p("k3", 1, 1.6)); show("#Bmeta", p("k3", 2), 0.4, 30); popin("#Bm1", p("k3", 3)); popin("#Bm2", p("k3", 4))
hide("#Bkm", p("k4", 0, -0.3)); show("#Bqr", p("k4", 0), 0.5, 50)
js(f'tl.fromTo("#Bscan", {{ y: 0 }}, {{ y: 290, duration: 0.8, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("k4", 1):.3f});'); ev("click", p("k4", 1))
hide("#Bqrc", p("k4", 2, -0.1)); popin("#Bhist", p("k4", 2)); tap("#Bhist .hby", p("k4", 2, 1.4))
popin("#B30", p("k4", 3))
hide("#Bqr", p("k5", 0, -0.2)); hide("#B30", p("k5", 0, -0.2)); show("#Breq", p("k5", 0), 0.4, 30)
popin("#Brq0", p("k5", 1)); popin("#Brq1", p("k5", 2)); popin("#Brq2", p("k5", 3)); popin("#Brq3", p("k5", 3, 1.2))
# C (Instagram)
reveal("#sC", S[2], "80%", "20%"); stepstate(1, S[2] + 0.3); js(f'tl.set("#sB", {{ autoAlpha: 0 }}, {S[2] + 0.75:.3f});')
show("#Ck", S[2] + 0.5); show("#Ct", S[2] + 0.65); logopop("#Clg", S[2] + 0.8)
js('tl.set(["#Cc0", "#Cc1", "#Cc2", "#Cic", "#Cbtn", "#Cok", "#Cdm", "#Creq"], { autoAlpha: 0 }, 0);')
show("#Ckm", S[2] + 0.9, 0.45, 40)
popin("#Cc0", p("k6", 2)); popin("#Cc1", p("k6", 3)); popin("#Cc2", p("k6", 4)); show("#Cic", p("k6", 4, 0.2))
show("#Cbtn", p("k6", 5)); tap("#Cbtn", p("k6", 6, 0.6)); popin("#Cok", p("k6", 6, 1.0))
show("#Creq", p("k6", 7)); show("#Cdm", p("k6", 7, 1.5)); ev("pop", p("k6", 7, 1.5))
# D (TikTok)
reveal("#sD", S[3], "20%", "20%"); stepstate(2, S[3] + 0.3); js(f'tl.set("#sC", {{ autoAlpha: 0 }}, {S[3] + 0.75:.3f});')
show("#Dk", S[3] + 0.5); show("#Dt", S[3] + 0.65); logopop("#Dlg", S[3] + 0.8)
js('tl.set(["#Dic", "#Dauth", "#Ddone"], { autoAlpha: 0 }, 0);')
show("#Dkm", S[3] + 0.9, 0.45, 40)
js(f'tl.fromTo("#Dq", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "steps(6)" }}, {p("k7", 2):.3f});')
show("#Dic", p("k7", 2, 0.6)); tap("#Dinst", p("k7", 3, 0.3)); show("#Dauth", p("k7", 4), 0.4, 30); tap("#Dok", p("k7", 5, 0.8)); hide("#Dauth", p("k7", 5, 1.0), 0.2); popin("#Ddone", p("k7", 5, 1.15))
# E (inbox + pipeline) and CTA
reveal("#sE", S[4]); stepstate(3, S[4] + 0.3); js(f'tl.set("#sD", {{ autoAlpha: 0 }}, {S[4] + 0.75:.3f});')
show("#Et", p("k8", 0)); show("#Ein", p("k8", 0, 0.2), 0.45, 40); js('tl.set(".Er", { autoAlpha: 0 }, 0);')
popin("#Er0", p("k8", 1)); popin("#Er1", p("k8", 2)); popin("#Er2", p("k8", 3))
show("#Epipe", p("k8", 4), 0.5, 40); js(f'tl.fromTo(".lcd", {{ autoAlpha: 0, y: 20 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.2 }}, {p("k8", 4, 0.3):.3f});')
reveal("#sH", p("k8", 5, -0.3)); js(f'tl.set(["#sE", "#stepbar"], {{ autoAlpha: 0 }}, {p("k8", 5, 0.5):.3f});')
js(f'tl.fromTo(["#x0", "#x1", "#x2"], {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" }}, {p("k8", 5, 0.2):.3f});')
show("#xw", p("k8", 5, 0.5)); show("#xt", p("k8", 5, 0.9)); show("#xr", p("k8", 7)); ev("chime", p("k8", 5, 0.3))
for t in S[1:]: ev("chime2", t + 0.45)
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style_v.css")).read() + open(os.path.join(ROOT, "build", "style_k.css")).read()
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Kommo Omnicanal</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1080" data-height="1920">
{A}
{B}
{C}
{D}
{E}
      <div class="abs" id="stepbar" style="left:0;top:0;width:1080px;height:150px">{stepbar}</div>
{CAPS}
{"".join(f'      <audio id="v_{s["id"]}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for s in segs)}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.8"></audio>
      <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.45"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const capShow = (sel, a, b) => {{
        tl.fromTo(sel, {{ autoAlpha: 0, y: 12, scale: 0.96 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.15, ease: "back.out(2)" }}, a - 0.04);
        tl.set(sel, {{ autoAlpha: 0 }}, b);
      }};
{chr(10).join(J)}
{CAPJS}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("captions", len(caps), "events", len(EV))
