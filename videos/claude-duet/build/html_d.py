# Vertical explainer: what Claude Duet is, what it does, its limits and who can use it.
import json, os, re, math, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
SEG = {s["id"]: s for s in segs}
S, T = plan["S"], plan["T"]
INK, CREAM, CLAY, CLAYD, SAND, SAGE, AMBER = "#1f1e1d", "#f4efe6", "#c15f3c", "#a4482a", "#e8dfd0", "#4f7a63", "#f0b36a"
def p(i, k=0, off=0.0):
    s = SEG[i]; iv = s["speech"]; k = min(k, len(iv) - 1)
    return round(s["start"] + iv[k][0] + off, 3)
EV = []
def ev(kind, t): EV.append([kind, round(t, 3)])
def logo(name, size, color):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, f"logo-{name}.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-label="{name}"><path d="{d}" fill="{color}"/></svg>'
def icon(name, size, color=INK, sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>')

# ---------------------------------------------------------------- captions
HL = {"duet", "claude", "correo", "calendario", "resumen", "aprobación", "apruebes", "nube", "facturas", "planilla", "contratos", "dashboard",
      "límites", "urgente", "pro", "max", "espera", "ios", "android", "primero", "delicado", "solo", "semana", "sígueme", "apagar"}
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
def head(sid, kick, title, dark, w=940):
    kc = AMBER if dark else CLAYD
    tc = CREAM if dark else INK
    return (f'<div class="abs kick" id="{sid}k" style="left:70px;top:200px;color:{kc}">{kick}</div>'
            f'<div class="abs ttl" id="{sid}t" style="left:70px;top:250px;width:{w}px;color:{tc}">{title}</div>')
def row(sid, ic, text, x, y, w=940, bg="#ffffff", fg=INK, icbg=SAND, icc=INK, extra=""):
    return (f'<div class="abs row" id="{sid}" style="left:{x}px;top:{y}px;width:{w}px;background:{bg};color:{fg}">'
            f'<div class="ric" style="background:{icbg}">{icon(ic, 52, icc)}</div><div class="rtx">{text}</div>{extra}</div>')
ILLU = '<div class="abs illu" style="color:{c}">Recreación ilustrativa · Claude es una marca de Anthropic</div>'
duet_mark = lambda s, c=CLAY: f'<div class="dmark" style="width:{s}px;height:{s}px;border-radius:{s * 0.28:.0f}px">{logo("claude", int(s * 0.62), c)}</div>'

A = f'''      <div class="sc" id="sA" style="background:{INK}">
        <div class="abs kick" id="aK" style="left:70px;top:200px;color:{AMBER}">NUEVO · VISTA PREVIA</div>
        <div class="abs" id="aLg" style="left:70px;top:262px">{duet_mark(150)}</div>
        <div class="abs ttl" id="aT" style="left:250px;top:268px;font-size:118px;color:{CREAM}">Claude Duet</div>
        <div class="abs sub" id="aS" style="left:254px;top:410px;color:#c9c2b6">El agente que te escribe primero</div>
        <div class="abs phone" id="aPh" style="left:290px;top:560px">
          <div class="abs pscr" id="aScr"></div>
          <div class="abs ptime" id="aTm">7:30</div>
          <div class="abs notif" id="aN"><div class="nhd">{duet_mark(44)}<span>Claude Duet</span><i>ahora</i></div>
            <div class="nbd">Buenos días. Hay 3 cosas que necesitan tu atención.</div></div>
          <div class="abs notif sm" id="aN2"><div class="nbd">Dejé listo un borrador. ¿Lo reviso contigo?</div></div>
        </div>
        <div class="abs moon" id="aMoon" style="left:820px;top:640px">{icon("moon", 110, AMBER, 1.8)}</div>
        <div class="abs zz" id="aZ" style="left:900px;top:580px;color:{AMBER}">z z z</div>
        {ILLU.format(c="#8d877c")}
      </div>'''

hub_nodes = [("mail", "Correo", 110, 820), ("calendar", "Calendario", 400, 1120), ("layout-dashboard", "Tus apps", 690, 820)]
B = f'''      <div class="sc light" id="sB">
        {head("B", "QUÉ ES", "Una app aparte que vigila lo importante", False)}
        <div class="abs chip" id="Bch" style="left:70px;top:430px">Vista previa de investigación</div>
        <svg class="abs" id="Bw" width="1080" height="1400" viewBox="0 0 1080 1400" style="left:0;top:0" aria-hidden="true">
          {"".join(f'<line id="Bl{i}" x1="540" y1="760" x2="{x + 140}" y2="{y + 110}" stroke="{CLAY}" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"/>' for i, (_, _, x, y) in enumerate(hub_nodes))}
        </svg>
        <div class="abs" id="Bhub" style="left:430px;top:650px">{duet_mark(220)}</div>
        {"".join(f'<div class="abs node" id="Bn{i}" style="left:{x}px;top:{y}px">{icon(ic, 84, INK)}<div>{t}</div></div>' for i, (ic, t, x, y) in enumerate(hub_nodes))}
        <div class="abs pill" id="Bclk" style="left:240px;top:560px;background:{INK};color:{CREAM}"><span id="Bclki">{icon("clock", 44, AMBER)}</span> Revisa cada pocas horas</div>
      </div>'''

C = f'''      <div class="sc light" id="sC" style="background:#efe5d4">
        {head("C", "CADA MAÑANA", "Tu resumen, sin que lo pidas", False)}
        <div class="abs card" id="Cc" style="left:70px;top:470px;width:940px;height:880px">
          <div class="abs chd"><span id="Csun">{icon("sunrise", 64, CLAY)}</span><div><b>Resumen de la mañana</b><i>Martes · 7:30</i></div></div>
          {row("Cr0", "mail", "Correos que importan", 40, 190, 860, "#faf7f1", INK, "#f6dccd", CLAYD, '<div class="cnt">2</div>')}
          {row("Cr1", "calendar", "Reuniones de hoy", 40, 340, 860, "#faf7f1", INK, "#dfe9e2", SAGE, '<div class="cnt sage">3</div>')}
          {row("Cr2", "send", "Borrador de respuesta listo", 40, 490, 860, "#faf7f1", INK, SAND, INK)}
          <div class="abs btn" id="Cap" style="left:40px;top:680px">Aprobar</div>
          <div class="abs btn ghost" id="Ced" style="left:300px;top:680px">Editar</div>
          <div class="abs okp" id="Cok" style="left:560px;top:692px">{icon("circle-check", 34, SAGE)} Aprobado</div>
        </div>
      </div>'''

D = f'''      <div class="sc" id="sD" style="background:{INK}">
        {head("D", "EN SEGUNDO PLANO", "Trabaja en su propia computadora en la nube", True)}
        <div class="abs" id="Dcl" style="left:250px;top:520px">{icon("cloud", 580, "#3a3836", 1.2)}</div>
        <div class="abs vm" id="Dvm" style="left:340px;top:700px">
          <div class="vmt">tarea en curso</div>
          <div class="vbar"><div id="Dbar"></div></div>
          <div class="vmp" id="Dpct">trabajando…</div>
        </div>
        <div class="abs phone sm" id="Dph" style="left:110px;top:1040px"><div class="abs pscr lit" id="Dscr"></div><div class="abs poff" id="Doff">{icon("moon", 70, "#8d877c", 1.8)}</div></div>
        <div class="abs dtx" id="Dt2" style="left:400px;top:1110px;color:{CREAM}">Apagas el celular…<br><b style="color:{AMBER}">y Duet sigue avanzando.</b></div>
      </div>'''

ex = [("receipt", "Facturas sin pagar", "redacta los recordatorios"), ("users", "Planilla", "lista para que la revises"),
      ("file-signature", "Contratos", "listos para enviar"), ("presentation", "Informe, presentación o dashboard", "armados por Duet")]
E = f'''      <div class="sc light" id="sE">
        {head("E", "EJEMPLOS PARA TU NEGOCIO", "Lo que puede preparar por ti", False)}
        {"".join(row(f"Er{i}", ic, f"<b>{t}</b><i>{d}</i>", 70, 480 + i * 225, 940, "#ffffff", INK, ["#f6dccd", "#dfe9e2", SAND, "#f6e3c4"][i], [CLAYD, SAGE, INK, "#8a5a00"][i]) for i, (ic, t, d) in enumerate(ex))}
      </div>'''

acts = [("send", "Enviar"), ("credit-card", "Pagar"), ("file-signature", "Firmar"), ("trash-2", "Borrar")]
F = f'''      <div class="sc" id="sF" style="background:{INK}">
        {head("F", "TÚ DECIDES", "En lo delicado, espera tu aprobación", True)}
        {"".join(f'<div class="abs act" id="Fa{i}" style="left:{70 + i * 240}px;top:500px">{icon(ic, 64, CREAM)}<div>{t}</div><span class="lk">{icon("hand", 30, INK)}</span></div>' for i, (ic, t) in enumerate(acts))}
        <div class="abs card dk" id="Fc" style="left:70px;top:820px;width:940px;height:520px">
          <div class="abs chd"><span>{duet_mark(64)}</span><div><b style="color:{CREAM}">Antes de enviar</b><i>Esto es lo que voy a hacer</i></div></div>
          <div class="abs fmsg" id="Fm">Enviar recordatorio de pago a 3 clientes</div>
          <div class="abs btn" id="Fap" style="left:40px;top:380px">Aprobar</div>
          <div class="abs btn ghost dk" id="Fno" style="left:300px;top:380px">Ahora no</div>
          <div class="abs okp" id="Fok" style="left:560px;top:392px">{icon("circle-check", 34, SAGE)} Enviado</div>
        </div>
      </div>'''

lims = [("folder-lock", "No ve los archivos de tu computadora"), ("wallet", "No mueve dinero entre cuentas"), ("triangle-alert", "Puede calcular mal qué es urgente")]
G = f'''      <div class="sc light" id="sG">
        {head("G", "OJO", "Sus límites, hoy", False)}
        {"".join(row(f"Gr{i}", ic, t, 70, 520 + i * 250, 940, "#ffffff", INK, "#f6dccd", CLAYD, f'<span class="ban" id="Gb{i}">{icon("ban", 58, CLAYD)}</span>' if i < 2 else "") for i, (ic, t) in enumerate(lims))}
        <div class="abs src" id="Gsrc" style="left:70px;top:1290px;color:#6b655c">Anthropic dice que es una versión temprana</div>
      </div>'''

H = f'''      <div class="sc" id="sH" style="background:{INK}">
        {head("H", "ACCESO", "¿Quién puede usarlo?", True)}
        {"".join(f'<div class="abs pill big" id="Hp{i}" style="left:70px;top:{470 + i * 140}px">{t}</div>' for i, t in enumerate(["Suscriptores Pro y Max", "En Estados Unidos", "Con lista de espera"]))}
        {"".join(f'<div class="abs plat" id="Hq{i}" style="left:{70 + i * 320}px;top:930px">{icon(ic, 60, CREAM)}<div>{t}</div></div>' for i, (ic, t) in enumerate([("smartphone", "iOS"), ("smartphone", "Android"), ("globe", "claude.ai")]))}
        <div class="abs note" id="Hn" style="left:70px;top:1180px">{icon("clock", 44, AMBER)} Usa los mismos límites de tu plan</div>
      </div>'''

I = f'''      <div class="sc" id="sI" style="background:{CLAYD}">
        {head("I", "CONSEJO", "Si te llega el acceso", True)}
        <div class="abs tip" id="Ip0" style="left:70px;top:470px"><div class="num">1</div><div>Empieza solo con <b>correo y calendario</b></div></div>
        <div class="abs tip" id="Ip1" style="left:70px;top:680px"><div class="num">2</div><div>Aprueba cada acción la <b>primera semana</b></div></div>
        <div class="abs endw" id="Iw" style="left:0;top:960px;width:1080px">Guarda este video</div>
        <div class="abs ends" id="Is" style="left:0;top:1140px;width:1080px">y sígueme para más herramientas de IA</div>
        <div class="abs illu" id="Isrc" style="left:70px;top:1330px;color:#f3d9cc">Fuente: anuncio de Anthropic, 21 oct 2026 · recreación ilustrativa</div>
      </div>'''

# ---------------------------------------------------------------- timeline
J = []
def js(s): J.append("      " + s)
def show(sel, t, d=0.45, y=30): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y} }}, {{ autoAlpha: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.3f});')
def popin(sel, t, d=0.4): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: {d}, ease: "back.out(1.8)" }}, {t:.3f});'); ev("pop", t)
def slide(sel, t, x=-80): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, x: {x} }}, {{ autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {t:.3f});'); ev("pop", t)
def hide(sel, t, d=0.3): js(f'tl.to("{sel}", {{ autoAlpha: 0, duration: {d} }}, {t:.3f});')
def tap(sel, t): js(f'tl.to("{sel}", {{ scale: 0.92, duration: 0.09, yoyo: true, repeat: 1 }}, {t:.3f});'); ev("click", t)
def reveal(sel, prev, t, x="50%", y="50%"):
    js(f'tl.set("{sel}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{sel}", {{ clipPath: "circle(0% at {x} {y})" }}, {{ clipPath: "circle(150% at {x} {y})", duration: 0.7, ease: "power2.inOut" }}, {t:.3f});')
    js(f'tl.set("{prev}", {{ autoAlpha: 0 }}, {t + 0.75:.3f});')

def heading(sid, t):
    show(f"#{sid}k", t + 0.3, 0.4, 20); show(f"#{sid}t", t + 0.45, 0.5, 40)

# A
js('tl.set(["#aN", "#aN2", "#aMoon", "#aZ"], { autoAlpha: 0 }, 0);')
show("#aK", 0.15, 0.4, 20); show("#aPh", 0.3, 0.6, 80)
js(f'tl.fromTo("#aN", {{ autoAlpha: 0, y: -60, scale: 0.92 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {p("d1", 0, 1.1):.3f});'); ev("chime", p("d1", 0, 1.1))
js(f'tl.to("#aPh", {{ rotation: 2, duration: 0.07, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {p("d1", 0, 1.2):.3f});')
popin("#aLg", p("d1", 1, 0.9)); show("#aT", p("d1", 1, 1.05), 0.5, 40); show("#aS", p("d1", 1, 1.4))
show("#aMoon", p("d1", 2), 0.5, 30); show("#aZ", p("d1", 2, 0.4), 0.5, 30)
js(f'tl.to("#aScr", {{ backgroundColor: "#141312", duration: 0.6 }}, {p("d1", 2):.3f});')
js(f'tl.to("#aZ", {{ y: -40, duration: 1.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {p("d1", 2, 0.9):.3f});')
js(f'tl.fromTo("#aN2", {{ autoAlpha: 0, y: -40 }}, {{ autoAlpha: 1, y: 0, duration: 0.45, ease: "back.out(1.6)" }}, {p("d1", 2, 1.1):.3f});'); ev("pop", p("d1", 2, 1.1))
# B
reveal("#sB", "#sA", S[1]); heading("B", S[1])
show("#Bch", p("d2", 1), 0.4, 20); popin("#Bhub", p("d2", 2, -0.2), 0.5)
for i in range(3):
    js(f'tl.fromTo("#Bl{i}", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3 }}, {p("d2", 2, 0.25 + i * 0.7):.3f});')
    popin(f"#Bn{i}", p("d2", 2, 0.3 + i * 0.7))
js(f'tl.to("#Bw line", {{ strokeDashoffset: -104, duration: 2.6, ease: "none" }}, {p("d2", 3):.3f});')
popin("#Bclk", p("d2", 3, 0.2)); js(f'tl.to("#Bclki", {{ rotation: 360, duration: 1.6, ease: "power1.inOut" }}, {p("d2", 3, 0.6):.3f});')
js(f'tl.to("#Bhub", {{ scale: 1.07, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("d2", 3, 0.8):.3f});')
# C
reveal("#sC", "#sB", S[2], "50%", "30%"); heading("C", S[2])
js('tl.set(["#Cr0", "#Cr1", "#Cr2", "#Cap", "#Ced", "#Cok"], { autoAlpha: 0 }, 0);')
show("#Cc", p("d3", 1, -0.4), 0.5, 60); js(f'tl.fromTo("#Csun", {{ rotation: -30, y: 20 }}, {{ rotation: 0, y: 0, duration: 0.8, ease: "power2.out" }}, {p("d3", 1, -0.3):.3f});')
tC = SEG["d3"]["start"]; a, b = SEG["d3"]["speech"][1]
slide("#Cr0", tC + a + 0.1); slide("#Cr1", tC + a + (b - a) * 0.3); slide("#Cr2", tC + a + (b - a) * 0.6)
show("#Cap", tC + a + (b - a) * 0.75, 0.35, 20); show("#Ced", tC + a + (b - a) * 0.78, 0.35, 20)
tap("#Cap", tC + b + 0.15); popin("#Cok", tC + b + 0.3)
# D
reveal("#sD", "#sC", S[3]); heading("D", S[3])
js('tl.set(["#Doff", "#Dt2"], { autoAlpha: 0 }, 0);')
show("#Dcl", p("d4", 0, 0.6), 0.6, 40); popin("#Dvm", p("d4", 0, 1.1))
js(f'tl.fromTo("#Dbar", {{ scaleX: 0.05 }}, {{ scaleX: 1, transformOrigin: "0% 50%", duration: {SEG["d4"]["dur"] - 1.2:.2f}, ease: "none" }}, {p("d4", 0, 1.3):.3f});')
show("#Dph", p("d4", 1, -0.2), 0.4, 30); js(f'tl.to("#Dscr", {{ backgroundColor: "#0e0d0c", duration: 0.4 }}, {p("d4", 1, 0.4):.3f});'); ev("click", p("d4", 1, 0.4))
show("#Doff", p("d4", 1, 0.6), 0.4, 10); show("#Dt2", p("d4", 1, 0.2))
# E
reveal("#sE", "#sD", S[4], "50%", "20%"); heading("E", S[4])
for i in range(4): slide(f"#Er{i}", p("d5", i + 1, -0.1), 120)
js(f'tl.to("#Er3", {{ scale: 1.03, duration: 0.3, yoyo: true, repeat: 1 }}, {p("d5", 4, 1.2):.3f});')
# F
reveal("#sF", "#sE", S[5]); heading("F", S[5])
js('tl.set([".lk", "#Fc", "#Fok"], { autoAlpha: 0 }, 0);')
for i in range(4):
    popin(f"#Fa{i}", p("d6", 2 + i // 2, (i % 2) * 0.9))
    js(f'tl.fromTo("#Fa{i} .lk", {{ autoAlpha: 0, scale: 0.3 }}, {{ autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {p("d6", 2 + i // 2, (i % 2) * 0.9 + 0.3):.3f});')
show("#Fc", p("d6", 4, -0.1), 0.5, 60)
js(f'tl.to("#Fap", {{ scale: 1.06, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("d6", 5):.3f});')
tap("#Fap", p("d6", 5, 1.3)); popin("#Fok", p("d6", 5, 1.45))
# G
reveal("#sG", "#sF", S[6], "50%", "30%"); heading("G", S[6])
js('tl.set([".ban"], { autoAlpha: 0 }, 0);')
for i in range(3): slide(f"#Gr{i}", p("d7", i + 1, -0.1))
for i in range(2): popin(f"#Gb{i}", p("d7", i + 1, 0.6))
js(f'tl.to("#Gr2 .ric", {{ rotation: 8, duration: 0.1, yoyo: true, repeat: 5 }}, {p("d7", 3, 0.6):.3f});')
show("#Gsrc", p("d7", 3, 1.6), 0.4, 10)
# H
reveal("#sH", "#sG", S[7]); heading("H", S[7])
a, b = SEG["d8"]["speech"][1]
for i in range(3): slide(f"#Hp{i}", SEG["d8"]["start"] + a + (b - a) * i / 3)
a, b = SEG["d8"]["speech"][2]
for i in range(3): popin(f"#Hq{i}", SEG["d8"]["start"] + a + (b - a) * i / 3)
show("#Hn", p("d8", 3))
# I
reveal("#sI", "#sH", S[8]); heading("I", S[8])
slide("#Ip0", p("d9", 1)); slide("#Ip1", p("d9", 2))
popin("#Iw", p("d9", 3, -0.05), 0.5); show("#Is", p("d9", 4)); show("#Isrc", p("d9", 4, 1.0), 0.4, 10); ev("chime", p("d9", 3))
js(f'tl.to("#Iw", {{ scale: 1.05, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("d9", 4, 0.6):.3f});')
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style_d.css")).read()
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Claude Duet</title>
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
{F}
{G}
{H}
{I}
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
