# Vertical (1080x1920) version of the WhatsApp AI chatbot tutorial, with brand logos and icons.
import json, os, re, math, itertools
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

# ---------------------------------------------------------------- logos (Simple Icons, CC0) and icons (Lucide, ISC)
BRAND = {"whatsapp": "#25D366", "meta": "#0467DF", "n8n": "#EA4B71", "anthropic": "#191919", "claude": "#D97757"}
def logo(name, size, color=None, label=None):
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(IMG, f"logo-{name}.svg")).read()).group(1)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-label="{label or name}"><path d="{d}" fill="{color or BRAND[name]}"/></svg>'
def icon(name, size, color="#041b3d", sw=2):
    src = open(os.path.join(IMG, f"icon-{name}.svg")).read()
    inner = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-label="{name}">{inner}</svg>')
def badge(name, sid, x, y, s=150):
    return f'<div class="abs lbadge" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px">{logo(name, int(s * 0.62))}</div>'

# ---------------------------------------------------------------- captions (same alignment as the 16:9 cut, narrower lines)
HL = {"whatsapp", "meta", "n8n", "ia", "claude", "token", "client", "secret", "mensajes", "webhook", "agente", "memoria", "sistema",
      "filtro", "producción", "scaly", "app", "api", "id", "disparador", "anthropic", "permanente", "prueba"}
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
    if s["id"] == "c17": continue
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

# ---------------------------------------------------------------- builders
def header(n, title, sid, brand):
    return (f'<div class="abs kick" id="{sid}k" style="left:70px;top:190px">PASO {n} DE 5</div>'
            f'<div class="abs ttl" id="{sid}t" style="left:70px;top:236px;width:760px">{title}</div>'
            + badge(brand, f"{sid}lg", 860, 180))
def node(id_, x, y, inner, label, w=130, h=130, trig=False, cls=""):
    rad = f"{h // 2}px 20px 20px {h // 2}px" if trig else "20px"
    jc = "justify-content:flex-start;padding-left:24px;gap:16px;" if w > 200 else ""
    return (f'<div class="abs node {cls}" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{rad};{jc}">{inner}</div>'
            f'<div class="abs nlabel {cls}" id="{id_}L" style="left:{x - 40}px;top:{y + h + 10}px;width:{w + 80}px">{label}</div>')
BOLT = '<svg class="abs" style="left:-20px;top:48px" width="30" height="34" viewBox="0 0 30 34" aria-label="Disparador"><path d="M17 0 L2 20 L13 20 L10 34 L28 12 L16 12 Z" fill="#ff6d5a"/></svg>'
def panel(id_, x, y, w, title, rows, ttl_logo=""):
    inner = f'<div class="ptitle">{ttl_logo}<span>{title}</span></div>' + "".join(
        f'<div class="prow" id="{id_}r{i}"><div class="plabel">{lab}</div><div class="pval{" expr" if ex else ""}">{val}</div></div>' for i, (lab, val, ex) in enumerate(rows))
    return f'<div class="abs panel" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px">{inner}</div>'
def wire(id_, d, dash=False):
    extra = ' stroke-dasharray="12 12"' if dash else ""
    return f'<path id="{id_}" d="{d}" fill="none" stroke="#9aa1b1" stroke-width="5" stroke-linecap="round"{extra}/>'
CANVAS = '<div class="abs canvas" style="left:60px;top:420px;width:960px;height:880px"></div>'
ILLU = '<div class="abs illu">Recreación ilustrativa · logos de sus respectivas marcas</div>'
def phone(id_, x, y, msgs):
    b = "".join(f'<div class="abs bubble {who}" id="{id_}m{i}" style="top:{top}px">{txt}</div>' for i, (who, txt, top) in enumerate(msgs))
    return (f'<div class="abs phone" id="{id_}" style="left:{x}px;top:{y}px"><div class="abs pscreen"></div>'
            f'<div class="abs phead"><div class="abs pav">{logo("whatsapp", 34, "#ffffff")}</div><div class="abs pname">Mi negocio</div><div class="abs pstat">en línea · bot con IA</div></div>{b}'
            f'<div class="abs typing" id="{id_}ty" style="top:440px"><i></i><i></i><i></i></div></div>')
def person(id_, x, y, skin, hair, shirt, scale=1.0):
    return f'''<svg class="abs" id="{id_}" style="left:{x}px;top:{y}px" width="{int(140 * scale)}" height="{int(170 * scale)}" viewBox="0 0 140 170" aria-label="Cliente ilustrativo">
          <path d="M8 170 C8 122 38 100 70 100 C102 100 132 122 132 170 Z" fill="{shirt}"/><circle cx="70" cy="62" r="40" fill="{skin}"/>
          <path d="M30 60 C30 16 110 16 110 60 C96 38 44 38 30 60 Z" fill="{hair}"/><circle cx="56" cy="66" r="4.5" fill="#2a1a14"/><circle cx="84" cy="66" r="4.5" fill="#2a1a14"/>
          <path d="M58 82 Q70 92 82 82" fill="none" stroke="#2a1a14" stroke-width="4" stroke-linecap="round"/></svg>'''
STEPS = [("Meta", "meta"), ("Disparador", "n8n"), ("Agente IA", "claude"), ("Responder", "whatsapp"), ("Probar", None)]
stepbar = "".join(f'<div class="abs step" id="st{i}" style="left:{50 + i * 198}px;top:70px"><b>{i + 1}</b>{n}</div>' for i, (n, _) in enumerate(STEPS))

# ---------------------------------------------------------------- scenes
A = f'''
      <div class="sc" id="sA" style="background:#041b3d">
        <div class="abs" id="aK" style="left:70px;top:150px;font-size:34px;font-weight:800;letter-spacing:4px;color:#47d4d4">TUTORIAL</div>
        <div class="abs h" id="aT" style="left:70px;top:210px;width:940px;font-size:96px;color:#fff">Tu chatbot de IA en <span style="color:#47d4d4">WhatsApp</span></div>
        <svg class="abs" id="aRing" style="left:70px;top:470px" width="150" height="150" viewBox="0 0 150 150" aria-label="Temporizador"><circle cx="75" cy="75" r="66" fill="none" stroke="#1d4a86" stroke-width="12"/><circle id="aArc" cx="75" cy="75" r="66" fill="none" stroke="#f5b94d" stroke-width="12" stroke-linecap="round" transform="rotate(-90 75 75)" stroke-dasharray="415" stroke-dashoffset="415"/></svg>
        <div class="abs h" id="aMin" style="left:70px;top:520px;width:150px;font-size:44px;color:#fff;text-align:center">3:00</div>
        <div class="abs h" id="aSub" style="left:250px;top:515px;width:780px;font-size:56px;color:#fff">en <span style="color:#f5b94d">3 minutos</span>, paso a paso</div>
        {phone("aP", 340, 680, [("me", "Hola, ¿atienden hoy?", 190), ("bot", "¡Hola! Sí, hasta las 8 p. m. ¿En qué te ayudo?", 300)])}
        <div class="abs fl" id="aL0" style="left:110px;top:760px">{logo("whatsapp", 120)}</div>
        <div class="abs fl lbadge" id="aL1" style="left:800px;top:820px;width:170px;height:170px">{logo("n8n", 110)}</div>
        <div class="abs fl lbadge" id="aL2" style="left:90px;top:1100px;width:170px;height:170px">{logo("claude", 110)}</div>
        <div class="abs fl lbadge" id="aL3" style="left:810px;top:1180px;width:170px;height:170px">{logo("meta", 110)}</div>
        <div class="abs card3 pc" id="pc0" style="left:60px;top:430px"><div class="abs lbadge" style="left:34px;top:35px;width:160px;height:160px">{logo("whatsapp", 100)}</div><div class="abs pt" style="left:230px;top:58px">API de WhatsApp</div><div class="abs ps" style="left:230px;top:126px">{logo("meta", 34, "#9fc3ff")}<span>de Meta</span></div></div>
        <div class="abs plus pc" style="left:500px;top:668px">+</div>
        <div class="abs card3 pc" id="pc1" style="left:60px;top:730px"><div class="abs lbadge" style="left:34px;top:35px;width:160px;height:160px">{logo("n8n", 100)}</div><div class="abs pt" style="left:230px;top:58px">n8n</div><div class="abs ps" style="left:230px;top:126px">{icon("zap", 34, "#9fc3ff")}<span>automatización</span></div></div>
        <div class="abs plus pc" style="left:500px;top:968px">+</div>
        <div class="abs card3 pc" id="pc2" style="left:60px;top:1030px"><div class="abs lbadge" style="left:34px;top:35px;width:160px;height:160px">{logo("claude", 100)}</div><div class="abs pt" style="left:230px;top:58px">Modelo de IA</div><div class="abs ps" style="left:230px;top:126px">{logo("anthropic", 30, "#9fc3ff")}<span>por ejemplo, Claude</span></div></div>
        <div class="abs h pc" id="pcEq" style="left:60px;top:1300px;width:960px;font-size:54px;color:#47d4d4;text-align:center">= tu chatbot con IA</div>
      </div>'''

datos = [("hash", "ID de la app", "1234 •••• ••••", "App › Configuración básica"), ("key-round", "Clave secreta de la app", "•••• •••• ••••", "App › Configuración básica"),
         ("smartphone", "ID del número de teléfono", "1098 •••• ••••", "WhatsApp › Configuración de la API"), ("badge-check", "ID de la cuenta de WhatsApp Business", "2087 •••• ••••", "WhatsApp › Configuración de la API")]
B = f'''
      <div class="sc light" id="sB">
        {header(1, "Crea la app en Meta", "B", "meta")}
        <div class="abs mock" id="Bm" style="left:60px;top:420px;width:960px;height:880px">
          <div class="abs mbar"><i></i><i></i><i></i><div class="abs url"><span class="ul">{logo("meta", 26)}</span>developers.facebook.com/apps</div></div>
          <div class="abs side"><div class="si">Panel</div><div class="si" id="Bsw"><span class="sl2">{logo("whatsapp", 26)}</span>WhatsApp</div><div class="si sub" id="Bsa">Configuración de la API</div><div class="si">Configuración</div></div>
          <div class="abs h" id="Bh1" style="left:270px;top:110px;width:600px;font-size:40px">Mis apps</div>
          <div class="abs btn" id="Bcreate" style="left:270px;top:180px">Crear app</div>
          <div class="abs appc" id="Bapp" style="left:270px;top:300px"><div class="h" style="font-size:36px">Mi chatbot</div><div class="abs" style="left:30px;top:84px;font-size:26px;color:#4a5566">Productos:</div><div class="abs okp" id="Bwa" style="left:180px;top:74px"><span class="ok2">{logo("whatsapp", 26)}</span>WhatsApp ✓</div></div>
          <div class="abs apis" id="Bapi" style="left:262px;top:96px">
            <div class="h" style="font-size:36px">Configuración de la API</div>
            <div class="abs flab" style="left:0;top:70px">Token de acceso temporal</div>
            <div class="abs fbox mono" id="Btok" style="left:0;top:110px;width:640px">EAAG••••••••••••••</div>
            <div class="abs btn sm" id="Bgen" style="left:0;top:190px">Generar token</div>
            <div class="abs flab" style="left:0;top:300px">De</div>
            <div class="abs fbox" id="Bfrom" style="left:0;top:340px;width:640px">Número de prueba · +1 555 ••• ••••</div>
            <div class="abs flab" style="left:0;top:440px">Para</div>
            <div class="abs fbox" id="Bto" style="left:0;top:480px;width:420px">+51 9•• ••• •••</div>
            <div class="abs okp" id="Btook" style="left:440px;top:484px">Verificado ✓</div>
          </div>
        </div>
        <div class="abs datos" id="Bd" style="left:90px;top:520px;width:900px">
          <div class="h" style="font-size:40px;margin-bottom:14px">Anota 4 datos</div>
          {"".join(f'<div class="drow" id="Bd{i}"><div class="dic">{icon(ic, 40, "#007b83")}</div><div><div class="dl">{l}</div><div class="dw">{w}</div></div><div class="dv mono">{v}</div></div>' for i, (ic, l, v, w) in enumerate(datos))}
        </div>
        <div class="abs warn" id="Bw" style="left:60px;top:1316px;width:960px"><span class="wi">{icon("clock", 44, "#a86400")}</span><span><b>Ojo:</b> el token temporal dura menos de un día. En producción, usa un token permanente.</span></div>
        {ILLU}
      </div>'''

C = f'''
      <div class="sc light" id="sC">
        {header(2, "El disparador de WhatsApp en n8n", "C", "n8n")}
        {CANVAS}
        <div class="abs plusn" id="Cplus" style="left:470px;top:500px">+</div>
        {node("Cn", 130, 490, logo("whatsapp", 74) + BOLT, "WhatsApp Trigger", w=150, h=150, trig=True)}
        <div class="abs toggle" id="Ctog" style="left:860px;top:460px"><div class="abs knob" id="Cknob"></div></div><div class="abs tlab" id="Ctl" style="left:700px;top:466px">Active</div>
        <div class="abs modal" id="Cmod" style="left:100px;top:760px;width:880px">
          <div class="ptitle"><span class="tl2">{icon("lock", 30, "#041b3d")}</span><span>Credencial · WhatsApp OAuth account</span></div>
          <div class="prow" id="Cm0"><div class="plabel">Client ID</div><div class="pval mono">1234 •••• ••••</div><div class="tagm">{logo("meta", 22, "#6b4300")} = ID de la app</div></div>
          <div class="prow" id="Cm1"><div class="plabel">Client Secret</div><div class="pval mono">•••• •••• ••••</div><div class="tagm">{logo("meta", 22, "#6b4300")} = clave secreta de la app</div></div>
        </div>
        {panel("Cpar", 100, 760, 880, "WhatsApp Trigger · Parámetros", [("Trigger On", "Updates", False), ("Updates", "messages", True)], '<span class="tl2">' + logo("whatsapp", 30) + '</span>')}
        <div class="abs okb" id="Cwh" style="left:100px;top:1170px"><span class="tl2">{icon("webhook", 34, "#ffffff")}</span>Webhook registrado en {logo("meta", 34, "#ffffff")} Meta ✓</div>
        <div class="abs note2" id="Cpub" style="left:60px;top:1316px;width:960px"><span class="wi">{icon("globe", 40, "#1d3a6e")}</span><span>Requiere una URL pública: n8n Cloud ya la tiene; si lo alojas tú, usa tu dominio.</span></div>
        {ILLU}
      </div>'''

D = f'''
      <div class="sc light" id="sD">
        {header(3, "El agente de IA", "D", "claude")}
        {CANVAS}
        <svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-label="Conexiones">
          {wire("Dw1", "M230 545 L300 545")}{wire("Dw2", "M365 625 L340 700", True)}{wire("Dw3", "M485 625 L560 700", True)}
        </svg>
        {node("Dn0", 100, 480, logo("whatsapp", 64) + BOLT, "WhatsApp Trigger", trig=True)}
        {node("Dag", 300, 465, icon("bot", 64, "#041b3d") + '<div class="h" style="font-size:38px">AI Agent</div>', "", w=420, h=160)}
        <div class="abs slot" id="Ds0" style="left:310px;top:630px">Chat Model</div><div class="abs slot" id="Ds1" style="left:440px;top:630px">Memory</div><div class="abs slot" id="Ds2" style="left:570px;top:630px">Tool</div>
        {node("Dm", 280, 700, logo("claude", 66), "Anthropic Chat Model", w=120, h=120)}
        {node("Dmem", 500, 700, icon("database", 60, "#007b83"), "Simple Memory", w=120, h=120)}
        <div class="abs fl2" id="Dbrain" style="left:780px;top:520px">{icon("brain", 150, "#47d4d4", 1.6)}</div>
        {panel("Dp0", 90, 900, 900, "AI Agent · Prompt", [("Fuente", "Define below", False), ("Mensaje del usuario", "{{ $json.messages[0].text.body }}", True)], '<span class="tl2">' + icon("message-circle", 30, "#041b3d") + '</span>')}
        {panel("Dp1", 90, 900, 900, "Anthropic Chat Model", [("Credencial", "Anthropic API key ••••", False), ("Modelo", "Claude", False)], '<span class="tl2">' + logo("anthropic", 30) + '</span>')}
        {panel("Dp2", 90, 900, 900, "Simple Memory", [("Session ID", "Define below", False), ("Key", "{{ $('WhatsApp Trigger').item.json.messages[0].from }}", True), ("Context Window Length", "5", False)], '<span class="tl2">' + icon("database", 30, "#007b83") + '</span>')}
        <div class="abs panel" id="Dsys" style="left:90px;top:900px;width:900px">
          <div class="ptitle"><span class="tl2">{icon("sparkles", 30, "#a86400")}</span><span>AI Agent · System Message</span></div>
          <div class="mono sl" id="Dl0">Eres el asistente de [Tu negocio].</div>
          <div class="mono sl" id="Dl1">Horario: lun–sáb, 9:00 a 20:00.</div>
          <div class="mono sl" id="Dl2">Precios: [tu lista de precios].</div>
          <div class="mono sl" id="Dl3">Si no sabes algo, ofrece hablar con una persona.</div>
        </div>
        {ILLU}
      </div>'''

E = f'''
      <div class="sc light" id="sE">
        {header(4, "Responde por WhatsApp", "E", "whatsapp")}
        {CANVAS}
        <svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-label="Conexiones">
          {wire("Ew1", "M220 545 L270 545")}{wire("Ew2", "M630 545 L690 545")}
        </svg>
        {node("En0", 90, 480, logo("whatsapp", 64) + BOLT, "WhatsApp Trigger", trig=True)}
        {node("Eag", 270, 465, icon("bot", 60, "#041b3d") + '<div class="h" style="font-size:34px">AI Agent</div>', "", w=360, h=160)}
        {node("Esd", 690, 480, logo("whatsapp", 64), "WhatsApp Business Cloud")}
        <div class="abs fl2" id="Esend" style="left:860px;top:500px">{icon("send", 90, "#25a95a", 1.8)}</div>
        <div class="abs note2" id="Ecr" style="left:90px;top:700px;width:900px"><span class="wi">{icon("key-round", 36, "#1d3a6e")}</span><span>Credencial: token de acceso + ID de la cuenta de WhatsApp Business</span></div>
        {panel("Ep", 90, 830, 900, "WhatsApp Business Cloud · Send Message", [("Operación", "Send Message", False), ("Sender Phone Number (ID)", "ID del número de teléfono", False), ("Recipient's Phone Number", "{{ $('WhatsApp Trigger').item.json.messages[0].from }}", True), ("Text Body", "{{ $json.output }}", True)], '<span class="tl2">' + logo("whatsapp", 30) + '</span>')}
        {ILLU}
      </div>'''

F = f'''
      <div class="sc light" id="sF">
        {header(5, "Activa y prueba", "F", "whatsapp")}
        <div class="abs canvas" style="left:60px;top:420px;width:960px;height:250px"></div>
        <svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-label="Conexiones">
          {wire("Fw0", "M220 520 L630 520")}{wire("Fw1", "M220 520 L300 520")}{wire("Fw2", "M410 520 L520 520")}{wire("Fw3", "M630 520 L740 520")}
        </svg>
        <div class="abs fn" id="Fn0" style="left:110px;top:465px">{logo("whatsapp", 60)}</div>
        <div class="abs fn" id="Fif" style="left:300px;top:465px">{icon("filter", 54, "#8b5cf6")}</div>
        <div class="abs fn" id="Fag" style="left:520px;top:465px">{icon("bot", 56, "#041b3d")}</div>
        <div class="abs fn" id="Fsd" style="left:740px;top:465px">{icon("send", 52, "#25a95a")}</div>
        <div class="abs fnl" style="left:80px;top:585px">Trigger</div><div class="abs fnl" id="FifL" style="left:270px;top:585px">If · texto</div><div class="abs fnl" style="left:490px;top:585px">AI Agent</div><div class="abs fnl" style="left:710px;top:585px">Enviar</div>
        <div class="abs toggle" id="Ftog" style="left:880px;top:440px;width:100px;height:50px"><div class="abs knob" id="Fknob" style="width:38px;height:38px"></div></div>
        <div class="abs stat" id="Fst0" style="left:110px;top:700px">✓✓ entregado</div><div class="abs stat" id="Fst1" style="left:330px;top:700px">✓✓ leído</div>
        {person("Fper", 40, 1120, "#e8b48f", "#2b2b2b", "#47d4d4", 1.5)}
        {phone("Fp", 330, 770, [("me", "Hola, ¿atienden los sábados?", 190), ("bot", "¡Hola! Sí, de 9:00 a 13:00. ¿Te ayudo a reservar?", 310)])}
        {ILLU}
      </div>'''

recap = [("meta", "App en Meta + número de prueba"), ("n8n", "Disparador de WhatsApp en n8n"), ("claude", "Agente de IA con memoria"), ("whatsapp", "Respuesta por WhatsApp"), (None, "Activado y probado")]
G = f'''
      <div class="sc light" id="sG">
        <div class="abs ttl" id="Gt" style="left:70px;top:200px;width:940px">Listo: tu chatbot con IA</div>
        {"".join(f'<div class="abs rec Gb" style="left:70px;top:{380 + i * 112}px"><div class="rl">{logo(b, 52) if b else icon("circle-check", 52, "#22a06b")}</div><span>{x}</span><div class="rk">{icon("circle-check", 40, "#22a06b")}</div></div>' for i, (b, x) in enumerate(recap))}
        <div class="abs prod" id="Gp" style="left:70px;top:980px;width:940px">
          <div class="h" style="font-size:46px;color:#fff;margin-bottom:16px"><span class="tl2">{icon("rocket", 44, "#f5b94d")}</span>Para producción</div>
          <div class="pl Gpl"><span class="tl2">{icon("smartphone", 36, "#47d4d4")}</span>Conecta tu número real</div>
          <div class="pl Gpl"><span class="tl2">{icon("badge-check", 36, "#47d4d4")}</span>Verifica tu negocio en Meta</div>
          <div class="pl Gpl"><span class="tl2">{icon("key-round", 36, "#47d4d4")}</span>Usa un token permanente</div>
        </div>
      </div>
      <div class="sc" id="sH" style="background:#041b3d">
        <div class="bar" id="x0" style="left:340px;top:520px;width:400px;background:linear-gradient(90deg,#007b83,#47d4d4)"></div>
        <div class="bar" id="x1" style="left:260px;top:590px;width:560px;background:#007b83"></div>
        <div class="bar" id="x2" style="left:340px;top:660px;width:400px;background:#47d4d4"></div>
        <div class="abs h" id="xw" style="left:0;top:760px;width:1080px;font-size:170px;color:#fff;text-align:center">ScalyAI</div>
        <div class="abs h" id="xt" style="left:60px;top:990px;width:960px;font-size:64px;color:#47d4d4;text-align:center">¿Lo armamos contigo? Escríbenos.</div>
        <div class="abs" id="xr" style="left:0;top:1250px;width:1080px;display:flex;justify-content:center;gap:36px">{"".join(f'<div class="lbadge mini">{logo(b, 64)}</div>' for b in ("whatsapp", "meta", "n8n", "claude"))}</div>
      </div>'''

# ---------------------------------------------------------------- timeline
J = []
def js(s): J.append("      " + s)
def show(sel, t, d=0.45, y=30): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y} }}, {{ autoAlpha: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.3f});')
def popin(sel, t, d=0.4): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.7 }}, {{ autoAlpha: 1, scale: 1, duration: {d}, ease: "back.out(1.8)" }}, {t:.3f});'); ev("pop", t)
def hide(sel, t, d=0.3): js(f'tl.to("{sel}", {{ autoAlpha: 0, duration: {d} }}, {t:.3f});')
def draw(sel, t, d=0.5): js(f'tl.fromTo("{sel}", {{ strokeDasharray: 500, strokeDashoffset: 500 }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power2.out" }}, {t:.3f});')
def tap(sel, t): js(f'tl.to("{sel}", {{ scale: 0.93, duration: 0.09, yoyo: true, repeat: 1 }}, {t:.3f});'); ev("click", t)
def reveal(sel, t, x="50%", y="50%"):
    js(f'tl.set("{sel}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{sel}", {{ clipPath: "circle(0% at {x} {y})" }}, {{ clipPath: "circle(150% at {x} {y})", duration: 0.7, ease: "power2.inOut" }}, {t:.3f});')
def stepstate(i, t):
    for k in range(5):
        cls = "step cur" if k == i else ("step done" if k < i else "step")
        js(f'tl.set("#st{k}", {{ attr: {{ class: "abs {cls}" }} }}, {t:.3f});')
def logopop(sid, t): js(f'tl.fromTo("{sid}", {{ autoAlpha: 0, scale: 0.4, rotate: -20 }}, {{ autoAlpha: 1, scale: 1, rotate: 0, duration: 0.55, ease: "back.out(2)" }}, {t:.3f});'); ev("pop", t)

js('tl.set(["#sB", "#sC", "#sD", "#sE", "#sF", "#sG", "#sH", "#stepbar", ".cap", ".pc"], { autoAlpha: 0 }, 0);')
# A
show("#aK", 0.2); show("#aT", 0.4, 0.6)
popin("#aP", 1.0, 0.5); show("#aPm0", p("c01", 0, 1.0))
js(f'tl.fromTo("#aPty", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.2 }}, {p("c01", 1):.3f});'); hide("#aPty", p("c01", 1, 1.0), 0.1); show("#aPm1", p("c01", 1, 1.1)); ev("pop", p("c01", 1, 1.1))
for k, t in enumerate((1.6, 2.2, 2.8, 3.4)): logopop(f"#aL{k}", t)
js(f'tl.to(".fl", {{ y: -14, duration: 1.1, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: 0.3 }}, 4.0);')
show("#aRing", p("c01", 2)); show("#aMin", p("c01", 2)); show("#aSub", p("c01", 2, 0.3))
js(f'tl.to("#aArc", {{ strokeDashoffset: 0, duration: 3.2, ease: "none" }}, {p("c01", 2, 0.3):.3f});')
for sel in ("#aK", "#aT", "#aRing", "#aMin", "#aSub", "#aP", ".fl"): hide(sel, p("c02", 0, -0.3))
popin("#pc0", p("c02", 1)); js(f'tl.fromTo(".plus", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3, stagger: 2.2 }}, {p("c02", 1, 0.6):.3f});')
popin("#pc1", p("c02", 2)); popin("#pc2", p("c02", 3)); show("#pcEq", p("c02", 4, -0.1))
# B
reveal("#sB", S[1]); js(f'tl.set("#sA", {{ autoAlpha: 0 }}, {S[1] + 0.75:.3f});')
show("#stepbar", S[1] + 0.4, 0.4, -20); stepstate(0, S[1] + 0.4)
show("#Bk", S[1] + 0.6); show("#Bt", S[1] + 0.75); logopop("#Blg", S[1] + 0.9)
js('tl.set(["#Bapi", "#Bd", "#Bapp", "#Bw", "#Btook", "#Bd0", "#Bd1", "#Bd2", "#Bd3", "#Bfrom", "#Btok", "#Bto"], { autoAlpha: 0 }, 0);')
show("#Bm", p("c03", 1), 0.5, 40)
tap("#Bcreate", p("c03", 2)); popin("#Bapp", p("c03", 2, 0.25)); popin("#Bwa", p("c03", 3, 1.0))
hide("#Bh1", p("c04", 0)); hide("#Bcreate", p("c04", 0)); hide("#Bapp", p("c04", 0))
js(f'tl.to("#Bsa", {{ backgroundColor: "#d6f3f0", duration: 0.3 }}, {p("c04", 0):.3f});')
show("#Bapi", p("c04", 0, 0.2)); popin("#Bfrom", p("c04", 1)); tap("#Bgen", p("c04", 2, 0.3)); popin("#Btok", p("c04", 2, 0.5))
popin("#Bto", p("c04", 3)); popin("#Btook", p("c04", 3, 1.2))
hide("#Bm", p("c05", 0, -0.2)); show("#Bd", p("c05", 0), 0.5, 40)
for k in range(4): popin(f"#Bd{k}", p("c05", k + 1))
popin("#Bw", p("c06", 1)); js(f'tl.to("#Bw", {{ scale: 1.03, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("c06", 3):.3f});')
# C
reveal("#sC", S[2], "20%", "30%"); stepstate(1, S[2] + 0.3); js(f'tl.set("#sB", {{ autoAlpha: 0 }}, {S[2] + 0.75:.3f});')
show("#Ck", S[2] + 0.5); show("#Ct", S[2] + 0.65); logopop("#Clg", S[2] + 0.8)
js('tl.set(["#Cn", "#CnL", "#Cmod", "#Cpar", "#Ctog", "#Ctl", "#Cwh", "#Cpub", "#Cplus", "#Cm0", "#Cm1", "#Cparr0", "#Cparr1"], { autoAlpha: 0 }, 0);')
popin("#Cplus", p("c07", 2)); js(f'tl.to("#Cplus", {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 3 }}, {p("c07", 2, 0.4):.3f});'); hide("#Cplus", p("c07", 2, 2.2))
popin("#Cn", p("c07", 2, 2.0)); show("#CnL", p("c07", 2, 2.2))
show("#Cmod", p("c07", 3), 0.4, 30); popin("#Cm0", p("c07", 4)); popin("#Cm1", p("c07", 5))
hide("#Cmod", p("c08", 0, -0.2)); show("#Cpar", p("c08", 0)); popin("#Cparr0", p("c08", 0, 0.2)); popin("#Cparr1", p("c08", 1))
show("#Ctog", p("c08", 2)); show("#Ctl", p("c08", 2)); tap("#Ctog", p("c08", 2, 0.4))
js(f'tl.to("#Cknob", {{ x: 56, duration: 0.25, ease: "power2.out" }}, {p("c08", 2, 0.5):.3f});')
js(f'tl.to("#Ctog", {{ backgroundColor: "#22a06b", duration: 0.25 }}, {p("c08", 2, 0.5):.3f});')
popin("#Cwh", p("c08", 3)); show("#Cpub", p("c08", 4))
# D
reveal("#sD", S[3], "80%", "30%"); stepstate(2, S[3] + 0.3); js(f'tl.set("#sC", {{ autoAlpha: 0 }}, {S[3] + 0.75:.3f});')
show("#Dk", S[3] + 0.5); show("#Dt", S[3] + 0.65); logopop("#Dlg", S[3] + 0.8)
js('tl.set(["#Dag", "#DagL", "#Ds0", "#Ds1", "#Ds2", "#Dm", "#DmL", "#Dmem", "#DmemL", "#Dp0", "#Dp1", "#Dp2", "#Dsys", ".sl", "#Dw1", "#Dw2", "#Dw3", "#Dbrain"], { autoAlpha: 0 }, 0);')
show("#Dn0", S[3] + 0.7); show("#Dn0L", S[3] + 0.8)
js(f'tl.set("#Dw1", {{ autoAlpha: 1 }}, {p("c09", 1):.3f});'); draw("#Dw1", p("c09", 1)); popin("#Dag", p("c09", 1, 0.3))
for k, sl in enumerate(("#Ds0", "#Ds1", "#Ds2")): show(sl, p("c09", 1, 0.6 + k * 0.1), 0.3, 10)
popin("#Dbrain", p("c09", 1, 0.9)); js(f'tl.to("#Dbrain", {{ scale: 1.08, duration: 0.8, yoyo: true, repeat: 9, ease: "sine.inOut" }}, {p("c09", 1, 1.5):.3f});')
show("#Dp0", p("c09", 2))
js(f'tl.set("#Dw2", {{ autoAlpha: 1 }}, {p("c10", 0, 0.5):.3f});'); popin("#Dm", p("c10", 1)); show("#DmL", p("c10", 1))
hide("#Dp0", p("c10", 1, -0.1)); show("#Dp1", p("c10", 1, 0.2))
hide("#Dp1", p("c11", 0, -0.2))
js(f'tl.set("#Dw3", {{ autoAlpha: 1 }}, {p("c11", 0, 0.3):.3f});'); popin("#Dmem", p("c11", 0, 0.4)); show("#DmemL", p("c11", 0, 0.5)); show("#Dp2", p("c11", 0, 1.4))
hide("#Dp2", p("c12", 0, -0.2)); show("#Dsys", p("c12", 0))
for k in range(4): show(f"#Dl{k}", p("c12", k, 0.1), 0.35, 12)
# E
reveal("#sE", S[4], "50%", "20%"); stepstate(3, S[4] + 0.3); js(f'tl.set("#sD", {{ autoAlpha: 0 }}, {S[4] + 0.75:.3f});')
show("#Ek", S[4] + 0.5); show("#Et", S[4] + 0.65); logopop("#Elg", S[4] + 0.8)
js('tl.set(["#Esd", "#EsdL", "#Ep", "#Ecr", "#Ew2", "#Esend", "#Epr0", "#Epr1", "#Epr2", "#Epr3"], { autoAlpha: 0 }, 0);')
js(f'tl.set("#Ew2", {{ autoAlpha: 1 }}, {p("c13", 1):.3f});'); draw("#Ew2", p("c13", 1), 0.4); popin("#Esd", p("c13", 1, 0.3)); show("#EsdL", p("c13", 1, 0.4))
popin("#Esend", p("c13", 1, 0.6)); js(f'tl.to("#Esend", {{ x: 30, y: -20, duration: 0.6, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {p("c13", 1, 1.2):.3f});')
show("#Ep", p("c13", 2), 0.4, 30); show("#Epr0", p("c13", 2, 0.2)); show("#Ecr", p("c13", 2, 1.0))
show("#Epr1", p("c13", 3)); show("#Epr2", p("c13", 4, 0.3)); show("#Epr3", p("c13", 4, 2.6))
# F
reveal("#sF", S[5], "75%", "60%"); stepstate(4, S[5] + 0.3); js(f'tl.set("#sE", {{ autoAlpha: 0 }}, {S[5] + 0.75:.3f});')
show("#Fk", S[5] + 0.5); show("#Ft", S[5] + 0.65); logopop("#Flg", S[5] + 0.8)
js('tl.set(["#Fif", "#FifL", "#Fw1", "#Fw2", "#Fst0", "#Fst1", "#Fpm0", "#Fpm1", "#Fpty", "#Fper"], { autoAlpha: 0 }, 0);')
tap("#Ftog", p("c14", 1)); js(f'tl.fromTo("#Fknob", {{ x: 0 }}, {{ x: 50, duration: 0.25 }}, {p("c14", 1, 0.1):.3f});'); js(f'tl.fromTo("#Ftog", {{ backgroundColor: "#b9bfcc" }}, {{ backgroundColor: "#22a06b", duration: 0.25 }}, {p("c14", 1, 0.1):.3f});')
show("#Fper", p("c14", 1, 0.8), 0.5, 60)
show("#Fpm0", p("c14", 1, 1.6)); ev("pop", p("c14", 1, 1.6))
js(f'tl.fromTo("#Fpty", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.2 }}, {p("c14", 2):.3f});'); hide("#Fpty", p("c14", 3, 0.1), 0.1)
show("#Fpm1", p("c14", 3, 0.15)); ev("pop", p("c14", 3, 0.15))
popin("#Fst0", p("c15", 1, 2.0)); popin("#Fst1", p("c15", 1, 2.4))
js(f'tl.to(["#Fst0", "#Fst1"], {{ textDecoration: "line-through", opacity: 0.45, duration: 0.2 }}, {p("c15", 2, 0.6):.3f});')
popin("#Fif", p("c15", 2)); show("#FifL", p("c15", 2)); js(f'tl.set(["#Fw1", "#Fw2"], {{ autoAlpha: 1 }}, {p("c15", 2):.3f});'); js(f'tl.set("#Fw0", {{ autoAlpha: 0 }}, {p("c15", 2):.3f});')
# G + CTA
reveal("#sG", S[6]); stepstate(5, S[6] + 0.3); js(f'tl.set("#sF", {{ autoAlpha: 0 }}, {S[6] + 0.75:.3f});')
show("#Gt", p("c16", 0)); js(f'tl.fromTo(".Gb", {{ autoAlpha: 0, x: -30 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.25 }}, {p("c16", 0, 0.4):.3f});')
show("#Gp", p("c16", 2)); js(f'tl.fromTo(".Gpl", {{ autoAlpha: 0, x: 30 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.9 }}, {p("c16", 3):.3f});')
reveal("#sH", p("c17", 0, -0.4)); js(f'tl.set(["#sG", "#stepbar"], {{ autoAlpha: 0 }}, {p("c17", 0, 0.4):.3f});')
js(f'tl.fromTo(["#x0", "#x1", "#x2"], {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" }}, {p("c17", 0, 0.1):.3f});')
show("#xw", p("c17", 0, 0.4)); show("#xt", p("c17", 1)); show("#xr", p("c17", 2)); ev("chime", p("c17", 0, 0.2))
for t in [S[1], S[2], S[3], S[4], S[5]]: ev("chime2", t + 0.45)
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style_v.css")).read()
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Chatbot IA WhatsApp Vertical</title>
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
