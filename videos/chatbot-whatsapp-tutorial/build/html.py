# Generates index.html for the WhatsApp AI chatbot tutorial (16:9), plus build/events.json for SFX.
import json, os, re, math, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open(os.path.join(ROOT, "build", "plan.json")))
segs = json.load(open(os.path.join(ROOT, "audio", "segmentos.json")))
SEG = {s["id"]: s for s in segs}
S, T = plan["S"], plan["T"]
def p(i, k=0, off=0.0):
    s = SEG[i]; iv = s["speech"]; k = min(k, len(iv) - 1)
    return round(s["start"] + iv[k][0] + off, 3)
def end(i): return round(SEG[i]["start"] + SEG[i]["dur"], 3)
EV = []
def ev(kind, t): EV.append([kind, round(t, 3)])

# ---------------------------------------------------------------- captions
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
        n = min(len(words), max(1, math.ceil(chars(words) / 34)))
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

# ---------------------------------------------------------------- small builders
def kicker(n, title, sid):
    return (f'<div class="abs kick" id="{sid}k" style="left:100px;top:150px">PASO {n} DE 5</div>'
            f'<div class="abs ttl" id="{sid}t" style="left:100px;top:200px;width:560px">{title}</div>')
def bullets(sid, items, top=420):
    out = []
    for i, txt in enumerate(items):
        out.append(f'<div class="abs bul {sid}b" id="{sid}b{i}" style="left:100px;top:{top + i * 92}px;width:560px"><i></i><span>{txt}</span></div>')
    return "".join(out)
def node(id_, x, y, icon, label, cls="", w=120, h=120, trig=False):
    rad = "60px 18px 18px 60px" if trig else "18px"
    jc = "justify-content:flex-start;padding-left:26px;" if w > 200 else ""
    return (f'<div class="abs node {cls}" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{rad};{jc}">{icon}</div>'
            f'<div class="abs nlabel {cls}" id="{id_}L" style="left:{x - 40}px;top:{y + h + 10}px;width:{w + 80}px">{label}</div>')
ICON = {
    "wa": '<svg width="64" height="64" viewBox="0 0 64 64" aria-label="Chat"><path d="M32 6 C17 6 6 16 6 29 C6 36 9 41 14 45 L11 58 L24 51 C26 52 29 52 32 52 C47 52 58 42 58 29 C58 16 47 6 32 6 Z" fill="#25a95a"/><path d="M22 24 L42 24 M22 33 L36 33" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>',
    "bolt": '<svg class="abs" style="left:-18px;top:44px" width="30" height="34" viewBox="0 0 30 34" aria-label="Disparador"><path d="M17 0 L2 20 L13 20 L10 34 L28 12 L16 12 Z" fill="#ff6d5a"/></svg>',
    "agent": '<svg width="70" height="64" viewBox="0 0 70 64" aria-label="Agente"><rect x="8" y="14" width="54" height="42" rx="12" fill="#041b3d"/><circle cx="25" cy="34" r="6" fill="#47d4d4"/><circle cx="45" cy="34" r="6" fill="#47d4d4"/><rect x="31" y="2" width="8" height="12" rx="4" fill="#041b3d"/></svg>',
    "claude": '<svg width="60" height="60" viewBox="0 0 60 60" aria-label="Modelo"><g stroke="#d97757" stroke-width="7" stroke-linecap="round"><path d="M30 6 L30 54"/><path d="M6 30 L54 30"/><path d="M13 13 L47 47"/><path d="M47 13 L13 47"/></g></svg>',
    "mem": '<svg width="56" height="60" viewBox="0 0 56 60" aria-label="Memoria"><ellipse cx="28" cy="12" rx="22" ry="8" fill="#007b83"/><path d="M6 12 L6 48 C6 53 16 56 28 56 C40 56 50 53 50 48 L50 12" fill="#47d4d4"/><ellipse cx="28" cy="12" rx="22" ry="8" fill="#007b83"/></svg>',
    "send": '<svg width="64" height="64" viewBox="0 0 64 64" aria-label="Enviar"><path d="M6 30 L58 8 L44 58 L30 38 Z" fill="#25a95a"/><path d="M30 38 L58 8" stroke="#fff" stroke-width="4"/></svg>',
    "if": '<svg width="64" height="64" viewBox="0 0 64 64" aria-label="Filtro"><path d="M8 10 L56 10 L38 34 L38 54 L26 48 L26 34 Z" fill="#8b5cf6"/></svg>',
}
def panel(id_, x, y, w, title, rows, cls=""):
    inner = f'<div class="ptitle">{title}</div>' + "".join(
        f'<div class="prow {cls}r" id="{id_}r{i}"><div class="plabel">{lab}</div><div class="pval{" expr" if ex else ""}">{val}</div></div>' for i, (lab, val, ex) in enumerate(rows))
    return f'<div class="abs panel" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px">{inner}</div>'
def line(id_, d, cls="wire"):
    return f'<path class="{cls}" id="{id_}" d="{d}" fill="none" stroke="#9aa1b1" stroke-width="5" stroke-linecap="round"/>'
CANVAS = '<div class="abs canvas" style="left:700px;top:150px;width:1120px;height:730px"></div>'
ILLU = '<div class="abs illu">Recreación ilustrativa de las pantallas</div>'
def phone(id_, x, y, msgs):
    b = "".join(f'<div class="abs bubble {"me" if who == "me" else "bot"}" id="{id_}m{i}" style="top:{top}px">{txt}</div>' for i, (who, txt, top) in enumerate(msgs))
    return (f'<div class="abs phone" id="{id_}" style="left:{x}px;top:{y}px"><div class="abs pscreen"></div>'
            f'<div class="abs phead"><div class="abs pav"></div><div class="abs pname">Mi negocio</div><div class="abs pstat">en línea</div></div>{b}'
            f'<div class="abs typing" id="{id_}ty" style="top:430px"><i></i><i></i><i></i></div></div>')

# ---------------------------------------------------------------- scene markup
STEPS = ["Meta", "Disparador", "Agente IA", "Responder", "Probar"]
stepbar = "".join(f'<div class="abs step" id="st{i}" style="left:{600 + i * 248}px;top:38px"><b>{i + 1}</b>{n}</div>' for i, n in enumerate(STEPS))

A = f'''
      <div class="sc" id="sA" style="background:#041b3d">
        <div class="abs" id="aK" style="left:120px;top:190px;font-size:34px;font-weight:800;letter-spacing:4px;color:#47d4d4">TUTORIAL</div>
        <div class="abs h" id="aT" style="left:120px;top:250px;width:1000px;font-size:104px;color:#fff">Tu chatbot de IA en <span style="color:#47d4d4">WhatsApp</span></div>
        <div class="abs" id="aR" style="left:120px;top:540px;width:190px;height:190px;border-radius:95px;border:14px solid #1d4a86"></div>
        <svg class="abs" id="aRing" style="left:120px;top:540px" width="190" height="190" viewBox="0 0 190 190" aria-label="Temporizador"><circle id="aArc" cx="95" cy="95" r="88" fill="none" stroke="#f5b94d" stroke-width="14" stroke-linecap="round" transform="rotate(-90 95 95)" stroke-dasharray="553" stroke-dashoffset="553"/></svg>
        <div class="abs h" id="aMin" style="left:120px;top:603px;width:190px;font-size:54px;color:#fff;text-align:center">3:00</div>
        <div class="abs h" id="aSub" style="left:350px;top:600px;width:700px;font-size:60px;color:#fff">en <span style="color:#f5b94d">3 minutos</span>, paso a paso</div>
        {phone("aP", 1340, 120, [("me", "Hola, ¿atienden hoy?", 190), ("bot", "¡Hola! Sí, hasta las 8 p. m. ¿En qué te ayudo?", 300)])}
        <div class="abs piece pc" id="pc0" style="left:120px;top:420px"><div class="pt">API de WhatsApp</div><div class="ps">de Meta</div></div>
        <div class="abs plus pc" style="left:500px;top:470px">+</div>
        <div class="abs piece pc" id="pc1" style="left:580px;top:420px"><div class="pt">n8n</div><div class="ps">automatización</div></div>
        <div class="abs plus pc" style="left:960px;top:470px">+</div>
        <div class="abs piece pc" id="pc2" style="left:1040px;top:420px"><div class="pt">Modelo de IA</div><div class="ps">por ejemplo, Claude</div></div>
        <div class="abs h pc" id="pcEq" style="left:120px;top:700px;width:1300px;font-size:64px;color:#47d4d4">= tu chatbot con IA en WhatsApp</div>
      </div>'''

B = f'''
      <div class="sc light" id="sB">
        {kicker(1, "Crea la app en Meta", "B")}
        {bullets("B", ["Entra a developers.facebook.com", "Crea una app y agrega WhatsApp", "Número de prueba y token", "Tu número como destinatario"])}
        <div class="abs warn" id="Bw" style="left:100px;top:790px;width:560px"><b>Ojo:</b> el token temporal dura menos de un día. En producción, usa un token permanente.</div>
        <div class="abs mock" id="Bm" style="left:700px;top:150px;width:1120px;height:730px">
          <div class="abs mbar"><i></i><i></i><i></i><div class="abs url">developers.facebook.com/apps</div></div>
          <div class="abs side"><div class="si">Panel</div><div class="si" id="Bsw">WhatsApp</div><div class="si sub" id="Bsa">Configuración de la API</div><div class="si">Configuración de la app</div></div>
          <div class="abs h" id="Bh1" style="left:330px;top:110px;width:700px;font-size:40px">Mis apps</div>
          <div class="abs btn" id="Bcreate" style="left:330px;top:180px">Crear app</div>
          <div class="abs appc" id="Bapp" style="left:330px;top:290px"><div class="h" style="font-size:36px">Mi chatbot</div><div class="abs" style="left:30px;top:80px;font-size:28px;color:#4a5566">Productos:</div><div class="abs okp" id="Bwa" style="left:180px;top:72px">WhatsApp ✓</div></div>
          <div class="abs apis" id="Bapi" style="left:300px;top:90px">
            <div class="h" style="font-size:38px">Configuración de la API</div>
            <div class="abs flab" style="left:0;top:80px">Token de acceso temporal</div>
            <div class="abs fbox mono" id="Btok" style="left:0;top:122px;width:500px">EAAG••••••••••••••</div>
            <div class="abs btn sm" id="Bgen" style="left:530px;top:118px">Generar token</div>
            <div class="abs flab" style="left:0;top:220px">De</div>
            <div class="abs fbox" id="Bfrom" style="left:0;top:262px;width:500px">Número de prueba · +1 555 ••• ••••</div>
            <div class="abs flab" style="left:0;top:360px">Para</div>
            <div class="abs fbox" id="Bto" style="left:0;top:402px;width:500px">+51 9•• ••• •••</div>
            <div class="abs okp" id="Btook" style="left:530px;top:404px">Verificado ✓</div>
          </div>
        </div>
        <div class="abs datos" id="Bd" style="left:1020px;top:230px;width:740px">
          <div class="h" style="font-size:38px;margin-bottom:18px">Anota 4 datos</div>
          {"".join(f'<div class="drow Bdr" id="Bd{i}"><div class="dl">{l}</div><div class="dv mono">{v}</div><div class="dw">{w}</div></div>' for i, (l, v, w) in enumerate([("ID de la app", "1234 •••• ••••", "App › Configuración básica"), ("Clave secreta de la app", "•••• •••• ••••", "App › Configuración básica"), ("ID del número de teléfono", "1098 •••• ••••", "WhatsApp › Configuración de la API"), ("ID de la cuenta de WhatsApp Business", "2087 •••• ••••", "WhatsApp › Configuración de la API")]))}
        </div>
        {ILLU}
      </div>'''

C = f'''
      <div class="sc light" id="sC">
        {kicker(2, "El disparador de WhatsApp en n8n", "C")}
        {bullets("C", ["Flujo nuevo + WhatsApp Trigger", "Client ID = ID de la app", "Client Secret = clave secreta", "Updates: messages", "Activa: el webhook se registra solo"])}
        {CANVAS}
        <div class="abs plusn" id="Cplus" style="left:1200px;top:430px">+</div>
        {node("Cn", 820, 380, ICON["wa"] + ICON["bolt"], "WhatsApp Trigger", trig=True)}
        <div class="abs modal" id="Cmod" style="left:1060px;top:200px;width:720px">
          <div class="ptitle">Credencial · WhatsApp OAuth account</div>
          <div class="prow" id="Cm0"><div class="plabel">Client ID</div><div class="pval mono">1234 •••• ••••</div><div class="tagm">= ID de la app</div></div>
          <div class="prow" id="Cm1"><div class="plabel">Client Secret</div><div class="pval mono">•••• •••• ••••</div><div class="tagm">= clave secreta de la app</div></div>
        </div>
        {panel("Cpar", 1060, 200, 720, "WhatsApp Trigger · Parámetros", [("Trigger On", "Updates", False), ("Updates", "messages", True)])}
        <div class="abs toggle" id="Ctog" style="left:1580px;top:180px"><div class="abs knob" id="Cknob"></div></div><div class="abs tlab" id="Ctl" style="left:1430px;top:186px">Active</div>
        <div class="abs okb" id="Cwh" style="left:1060px;top:560px">Webhook registrado en Meta ✓</div>
        <div class="abs note2" id="Cpub" style="left:1060px;top:660px;width:720px">Requiere una URL pública: n8n Cloud ya la tiene; si lo alojas tú, usa tu dominio.</div>
        {ILLU}
      </div>'''

D = f'''
      <div class="sc light" id="sD">
        {kicker(3, "El agente de IA", "D")}
        {bullets("D", ["Mensaje: el texto de WhatsApp", "Modelo: Claude (Anthropic)", "Memoria por número de cliente", "Mensaje del sistema: tu negocio"])}
        {CANVAS}
        <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080" aria-label="Conexiones">
          {line("Dw1", "M860 320 C900 320 900 320 930 320")}
          <path class="dash" id="Dw2" d="M955 400 L935 520" fill="none" stroke="#9aa1b1" stroke-width="4" stroke-dasharray="10 10"/>
          <path class="dash" id="Dw3" d="M1075 400 L1145 520" fill="none" stroke="#9aa1b1" stroke-width="4" stroke-dasharray="10 10"/>
        </svg>
        {node("Dn0", 740, 260, ICON["wa"] + ICON["bolt"], "WhatsApp Trigger", trig=True)}
        {node("Dag", 930, 250, ICON["agent"] + '<div class="abs h" style="left:110px;top:44px;font-size:32px">AI Agent</div>', "", w=260, h=150)}
        <div class="abs slot" id="Ds0" style="left:900px;top:404px">Chat Model</div><div class="abs slot" id="Ds1" style="left:1020px;top:404px">Memory</div><div class="abs slot" id="Ds2" style="left:1140px;top:404px">Tool</div>
        {node("Dm", 880, 520, ICON["claude"], "Anthropic Chat Model", w=110, h=110)}
        {node("Dmem", 1090, 520, ICON["mem"], "Simple Memory", w=110, h=110)}
        {panel("Dp0", 1360, 170, 440, "AI Agent · Prompt", [("Fuente", "Define below", False), ("Mensaje del usuario", "{{ $json.messages[0].text.body }}", True)])}
        {panel("Dp1", 1360, 470, 440, "Anthropic Chat Model", [("Credencial", "Anthropic API key ••••", False), ("Modelo", "Claude", False)])}
        {panel("Dp2", 1360, 170, 440, "Simple Memory", [("Session ID", "Define below", False), ("Key", "{{ $('WhatsApp Trigger').item.json.messages[0].from }}", True), ("Context Window Length", "5", False)])}
        <div class="abs sysm" id="Dsys" style="left:1360px;top:170px;width:440px">
          <div class="ptitle">AI Agent · System Message</div>
          <div class="mono sl" id="Dl0">Eres el asistente de [Tu negocio].</div>
          <div class="mono sl" id="Dl1">Horario: lun–sáb, 9:00 a 20:00.</div>
          <div class="mono sl" id="Dl2">Precios: [tu lista de precios].</div>
          <div class="mono sl" id="Dl3">Si no sabes algo, ofrece hablar con una persona.</div>
        </div>
        {ILLU}
      </div>'''

E = f'''
      <div class="sc light" id="sE">
        {kicker(4, "Responde por WhatsApp", "E")}
        {bullets("E", ["Nodo: WhatsApp Business Cloud", "Operación: Send Message", "Para: el número del cliente", "Texto: la respuesta del agente"])}
        {CANVAS}
        <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080" aria-label="Conexiones">
          {line("Ew1", "M860 260 L930 260")}
          {line("Ew2", "M1190 260 L1240 260")}
        </svg>
        {node("En0", 740, 200, ICON["wa"] + ICON["bolt"], "WhatsApp Trigger", trig=True)}
        {node("Eag", 930, 185, ICON["agent"] + '<div class="abs h" style="left:110px;top:44px;font-size:32px">AI Agent</div>', "", w=260, h=150)}
        {node("Esd", 1240, 200, ICON["send"], "WhatsApp Business Cloud")}
        {panel("Ep", 1060, 395, 740, "WhatsApp Business Cloud · Send Message", [("Operación", "Send Message", False), ("Sender Phone Number (ID)", "ID del número de teléfono", False), ("Recipient's Phone Number", "{{ $('WhatsApp Trigger').item.json.messages[0].from }}", True), ("Text Body", "{{ $json.output }}", True)], "E")}
        <div class="abs note2" id="Ecr" style="left:720px;top:430px;width:320px">Credencial: token de acceso + ID de la cuenta de WhatsApp Business</div>
        {ILLU}
      </div>'''

F = f'''
      <div class="sc light" id="sF">
        {kicker(5, "Activa y prueba", "F")}
        {bullets("F", ["Activa el flujo", "Escribe al número de prueba", "Tip: filtra los avisos de estado"])}
        <div class="abs canvas" style="left:700px;top:150px;width:560px;height:730px"></div>
        <div class="abs toggle on" id="Ftog" style="left:1080px;top:180px"><div class="abs knob" id="Fknob"></div></div><div class="abs tlab" id="Ftl" style="left:930px;top:186px">Active</div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080" aria-label="Conexiones">
          {line("Fw0", "M840 390 L840 610")}{line("Fw1", "M840 390 L840 440")}{line("Fw2", "M840 540 L840 610")}{line("Fw3", "M840 710 L840 770")}
        </svg>
        <div class="abs fnode" id="Fn0" style="left:740px;top:290px">{ICON["wa"].replace('width="64" height="64"', 'width="40" height="40"')}<span>WhatsApp Trigger</span></div>
        <div class="abs fnode" id="Fif" style="left:740px;top:440px">{ICON["if"].replace('width="64" height="64"', 'width="40" height="40"')}<span>If · ¿es mensaje de texto?</span></div>
        <div class="abs fnode" id="Fag" style="left:740px;top:610px">{ICON["agent"].replace('width="70" height="64"', 'width="44" height="40"')}<span>AI Agent</span></div>
        <div class="abs fnode" id="Fsd" style="left:740px;top:770px">{ICON["send"].replace('width="64" height="64"', 'width="40" height="40"')}<span>Send Message</span></div>
        <div class="abs stat" id="Fst0" style="left:1112px;top:296px">entregado</div><div class="abs stat" id="Fst1" style="left:1112px;top:346px">leído</div>
        {phone("Fp", 1360, 120, [("me", "Hola, ¿atienden los sábados?", 190), ("bot", "¡Hola! Sí, de 9:00 a 13:00. ¿Te ayudo a reservar?", 300)])}
        {ILLU}
      </div>'''

G = f'''
      <div class="sc light" id="sG">
        <div class="abs ttl" id="Gt" style="left:100px;top:150px;width:900px">Listo: tu chatbot con IA</div>
        {"".join(f'<div class="abs bul Gb" style="left:100px;top:{290 + i * 92}px;width:760px"><i class="ok"></i><span>{x}</span></div>' for i, x in enumerate(["App en Meta + número de prueba", "Disparador de WhatsApp en n8n", "Agente de IA con memoria", "Respuesta por WhatsApp", "Activado y probado"]))}
        <div class="abs prod" id="Gp" style="left:980px;top:270px;width:820px">
          <div class="h" style="font-size:44px;color:#fff;margin-bottom:20px">Para producción</div>
          <div class="pl Gpl">Conecta tu número real</div>
          <div class="pl Gpl">Verifica tu negocio en Meta</div>
          <div class="pl Gpl">Usa un token permanente</div>
        </div>
      </div>
      <div class="sc" id="sH" style="background:#041b3d">
        <div class="bar" id="x0" style="left:660px;top:250px;width:400px;background:linear-gradient(90deg,#007b83,#47d4d4)"></div>
        <div class="bar" id="x1" style="left:580px;top:320px;width:560px;background:#007b83"></div>
        <div class="bar" id="x2" style="left:660px;top:390px;width:400px;background:#47d4d4"></div>
        <div class="abs h" id="xw" style="left:0;top:480px;width:1920px;font-size:150px;color:#fff;text-align:center">ScalyAI</div>
        <div class="abs h" id="xt" style="left:0;top:680px;width:1920px;font-size:64px;color:#47d4d4;text-align:center">¿Lo armamos contigo? Escríbenos.</div>
      </div>'''

# ---------------------------------------------------------------- timeline
J = []
def js(s): J.append("      " + s)
def show(sel, t, d=0.45, y=30): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, y: {y} }}, {{ autoAlpha: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.3f});')
def popin(sel, t, d=0.4): js(f'tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.8 }}, {{ autoAlpha: 1, scale: 1, duration: {d}, ease: "back.out(1.7)" }}, {t:.3f});'); ev("pop", t)
def hide(sel, t, d=0.3): js(f'tl.to("{sel}", {{ autoAlpha: 0, duration: {d} }}, {t:.3f});')
def draw(sel, t, d=0.5): js(f'tl.fromTo("{sel}", {{ strokeDasharray: 400, strokeDashoffset: 400 }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power2.out" }}, {t:.3f});')
def tap(sel, t): js(f'tl.to("{sel}", {{ scale: 0.94, duration: 0.09, yoyo: true, repeat: 1 }}, {t:.3f});'); ev("click", t)
def reveal(sel, t, x="50%", y="50%"):
    js(f'tl.set("{sel}", {{ autoAlpha: 1 }}, {t:.3f});')
    js(f'tl.fromTo("{sel}", {{ clipPath: "circle(0% at {x} {y})" }}, {{ clipPath: "circle(150% at {x} {y})", duration: 0.7, ease: "power2.inOut" }}, {t:.3f});')
def stepstate(i, t):
    for k in range(5):
        cls = "step cur" if k == i else ("step done" if k < i else "step")
        js(f'tl.set("#st{k}", {{ attr: {{ class: "abs {cls}" }} }}, {t:.3f});')

js('tl.set(["#sB", "#sC", "#sD", "#sE", "#sF", "#sG", "#sH", "#stepbar", ".cap"], { autoAlpha: 0 }, 0);')
# A
show("#aK", 0.2); show("#aT", 0.4, 0.6)
popin("#aP", 1.0, 0.5); show("#aPm0", p("c01", 0, 1.0)); js(f'tl.fromTo("#aPty", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.2 }}, {p("c01", 1):.3f});'); hide("#aPty", p("c01", 1, 1.0), 0.1); show("#aPm1", p("c01", 1, 1.1)); ev("pop", p("c01", 1, 1.1))
show(["#aR", "#aRing", "#aMin"] and "#aR", p("c01", 2)); show("#aRing", p("c01", 2)); show("#aMin", p("c01", 2)); show("#aSub", p("c01", 2, 0.3))
js(f'tl.to("#aArc", {{ strokeDashoffset: 0, duration: 3.2, ease: "none" }}, {p("c01", 2, 0.3):.3f});')
for sel in ("#aK", "#aT", "#aR", "#aRing", "#aMin", "#aSub", "#aP"): hide(sel, p("c02", 0, -0.3))
js(f'tl.set(".pc", {{ autoAlpha: 0 }}, 0);')
popin("#pc0", p("c02", 1)); js(f'tl.fromTo(".plus", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3, stagger: 2.2 }}, {p("c02", 1, 0.6):.3f});')
popin("#pc1", p("c02", 2)); popin("#pc2", p("c02", 3)); show("#pcEq", p("c02", 4, -0.1))
# B
reveal("#sB", S[1]); js(f'tl.set("#sA", {{ autoAlpha: 0 }}, {S[1] + 0.75:.3f});'); show("#stepbar", S[1] + 0.4, 0.4, -20); stepstate(0, S[1] + 0.4)
show("#Bk", S[1] + 0.6); show("#Bt", S[1] + 0.75)
js('tl.set(["#Bapi", "#Bd", "#Bapp", "#Bw", "#Btook", ".Bb", ".Bdr"], { autoAlpha: 0 }, 0);')
show("#Bm", p("c03", 1), 0.5, 40); show("#Bb0", p("c03", 1, 0.3))
tap("#Bcreate", p("c03", 2)); popin("#Bapp", p("c03", 2, 0.25)); show("#Bb1", p("c03", 2, 0.3))
popin("#Bwa", p("c03", 3, 1.0))
hide("#Bh1", p("c04", 0)); hide("#Bcreate", p("c04", 0)); hide("#Bapp", p("c04", 0))
js(f'tl.to("#Bsa", {{ backgroundColor: "#d6f3f0", duration: 0.3 }}, {p("c04", 0):.3f});')
show("#Bapi", p("c04", 0, 0.2)); js(f'tl.set("#Bfrom", {{ autoAlpha: 0 }}, 0);'); popin("#Bfrom", p("c04", 1)); show("#Bb2", p("c04", 1))
js(f'tl.set("#Btok", {{ autoAlpha: 0 }}, 0);'); tap("#Bgen", p("c04", 2, 0.3)); popin("#Btok", p("c04", 2, 0.5))
js(f'tl.set("#Bto", {{ autoAlpha: 0 }}, 0);'); popin("#Bto", p("c04", 3)); popin("#Btook", p("c04", 3, 1.2)); show("#Bb3", p("c04", 3, 0.2))
hide("#Bapi", p("c05", 0, -0.2)); show("#Bd", p("c05", 0), 0.5, 40)
for k in range(4): popin(f"#Bd{k}", p("c05", k + 1))
popin("#Bw", p("c06", 1))
js(f'tl.to("#Bw", {{ scale: 1.03, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {p("c06", 3):.3f});')
# C
reveal("#sC", S[2], "20%", "50%"); stepstate(1, S[2] + 0.3); js(f'tl.set("#sB", {{ autoAlpha: 0 }}, {S[2] + 0.75:.3f});')
show("#Ck", S[2] + 0.5); show("#Ct", S[2] + 0.65)
js('tl.set(["#Cn", "#CnL", "#Cmod", "#Cpar", "#Ctog", "#Ctl", "#Cwh", "#Cpub", ".Cb", "#Cplus"], { autoAlpha: 0 }, 0);')
popin("#Cplus", p("c07", 2)); js(f'tl.to("#Cplus", {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 3 }}, {p("c07", 2, 0.4):.3f});'); hide("#Cplus", p("c07", 2, 2.2))
popin("#Cn", p("c07", 2, 2.0)); show("#CnL", p("c07", 2, 2.2)); show("#Cb0", p("c07", 2, 2.0))
show("#Cmod", p("c07", 3), 0.4, 30); js('tl.set(["#Cm0", "#Cm1"], { autoAlpha: 0 }, 0);')
popin("#Cm0", p("c07", 4)); show("#Cb1", p("c07", 4)); popin("#Cm1", p("c07", 5)); show("#Cb2", p("c07", 5))
hide("#Cmod", p("c08", 0, -0.2)); show("#Cpar", p("c08", 0)); js('tl.set(["#Cparr0", "#Cparr1"], { autoAlpha: 0 }, 0);')
popin("#Cparr0", p("c08", 0, 0.2)); popin("#Cparr1", p("c08", 1)); show("#Cb3", p("c08", 1))
show("#Ctog", p("c08", 2)); show("#Ctl", p("c08", 2)); tap("#Ctog", p("c08", 2, 0.4))
js(f'tl.to("#Cknob", {{ x: 56, duration: 0.25, ease: "power2.out" }}, {p("c08", 2, 0.5):.3f});')
js(f'tl.to("#Ctog", {{ backgroundColor: "#22a06b", duration: 0.25 }}, {p("c08", 2, 0.5):.3f});')
popin("#Cwh", p("c08", 3)); show("#Cb4", p("c08", 3)); show("#Cpub", p("c08", 4))
# D
reveal("#sD", S[3], "80%", "40%"); stepstate(2, S[3] + 0.3); js(f'tl.set("#sC", {{ autoAlpha: 0 }}, {S[3] + 0.75:.3f});')
show("#Dk", S[3] + 0.5); show("#Dt", S[3] + 0.65)
js('tl.set(["#Dag", "#DagL", "#Ds0", "#Ds1", "#Ds2", "#Dm", "#DmL", "#Dmem", "#DmemL", "#Dp0", "#Dp1", "#Dp2", "#Dsys", ".sl", ".Db", "#Dw1", "#Dw2", "#Dw3"], { autoAlpha: 0 }, 0);')
show("#Dn0", S[3] + 0.7); show("#Dn0L", S[3] + 0.8)
js(f'tl.set("#Dw1", {{ autoAlpha: 1 }}, {p("c09", 1):.3f});'); draw("#Dw1", p("c09", 1)); popin("#Dag", p("c09", 1, 0.3)); show("#DagL", p("c09", 1, 0.4))
for k, sl in enumerate(("#Ds0", "#Ds1", "#Ds2")): show(sl, p("c09", 1, 0.6 + k * 0.1), 0.3, 10)
show("#Dp0", p("c09", 2)); show("#Db0", p("c09", 2))
js(f'tl.set("#Dw2", {{ autoAlpha: 1 }}, {p("c10", 0, 0.5):.3f});'); popin("#Dm", p("c10", 1)); show("#DmL", p("c10", 1)); show("#Dp1", p("c10", 1, 0.2)); show("#Db1", p("c10", 1))
hide("#Dp0", p("c11", 0, -0.2)); hide("#Dp1", p("c11", 0, -0.2))
js(f'tl.set("#Dw3", {{ autoAlpha: 1 }}, {p("c11", 0, 0.3):.3f});'); popin("#Dmem", p("c11", 0, 0.4)); show("#DmemL", p("c11", 0, 0.5)); show("#Dp2", p("c11", 0, 1.6)); show("#Db2", p("c11", 0, 0.5))
hide("#Dp2", p("c12", 0, -0.2)); show("#Dsys", p("c12", 0)); show("#Db3", p("c12", 0))
for k in range(4): show(f"#Dl{k}", p("c12", k, 0.1), 0.35, 12)
# E
reveal("#sE", S[4], "50%", "20%"); stepstate(3, S[4] + 0.3); js(f'tl.set("#sD", {{ autoAlpha: 0 }}, {S[4] + 0.75:.3f});')
show("#Ek", S[4] + 0.5); show("#Et", S[4] + 0.65)
js('tl.set(["#Esd", "#EsdL", "#Ep", "#Ecr", ".Eb", ".Er", "#Ew2"], { autoAlpha: 0 }, 0);')
js(f'tl.set("#Ew2", {{ autoAlpha: 1 }}, {p("c13", 1):.3f});'); draw("#Ew2", p("c13", 1), 0.4); popin("#Esd", p("c13", 1, 0.3)); show("#EsdL", p("c13", 1, 0.4)); show("#Eb0", p("c13", 1))
show("#Ep", p("c13", 2), 0.4, 30); show("#Epr0", p("c13", 2, 0.2)); show("#Eb1", p("c13", 2)); show("#Ecr", p("c13", 2, 1.0))
show("#Epr1", p("c13", 3)); show("#Epr2", p("c13", 4, 0.3)); show("#Eb2", p("c13", 4, 0.3)); show("#Epr3", p("c13", 4, 2.6)); show("#Eb3", p("c13", 4, 2.6))
# F
reveal("#sF", S[5], "75%", "50%"); stepstate(4, S[5] + 0.3); js(f'tl.set("#sE", {{ autoAlpha: 0 }}, {S[5] + 0.75:.3f});')
show("#Fk", S[5] + 0.5); show("#Ft", S[5] + 0.65)
js('tl.set(["#Fif", "#Fw1", "#Fw2", "#Fst0", "#Fst1", ".Fb", "#Fpm0", "#Fpm1", "#Fpty"], { autoAlpha: 0 }, 0);')
js(f'tl.set("#Fw1", {{ autoAlpha: 0 }}, 0);')
tap("#Ftog", p("c14", 1)); js(f'tl.fromTo("#Fknob", {{ x: 0 }}, {{ x: 56, duration: 0.25 }}, {p("c14", 1, 0.1):.3f});'); js(f'tl.fromTo("#Ftog", {{ backgroundColor: "#b9bfcc" }}, {{ backgroundColor: "#22a06b", duration: 0.25 }}, {p("c14", 1, 0.1):.3f});'); show("#Fb0", p("c14", 1))
show("#Fpm0", p("c14", 1, 1.6)); ev("pop", p("c14", 1, 1.6)); show("#Fb1", p("c14", 1, 1.6))
js(f'tl.fromTo("#Fpty", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.2 }}, {p("c14", 2):.3f});'); hide("#Fpty", p("c14", 3, 0.1), 0.1)
show("#Fpm1", p("c14", 3, 0.15)); ev("pop", p("c14", 3, 0.15))
popin("#Fst0", p("c15", 1, 2.0)); popin("#Fst1", p("c15", 1, 2.4))
js(f'tl.to(["#Fst0", "#Fst1"], {{ textDecoration: "line-through", opacity: 0.45, duration: 0.2 }}, {p("c15", 2, 0.6):.3f});')
js(f'tl.to("#Fag", {{ y: 0, duration: 0 }}, 0);')
popin("#Fif", p("c15", 2)); js(f'tl.set(["#Fw1", "#Fw2"], {{ autoAlpha: 1 }}, {p("c15", 2):.3f});'); js(f'tl.set("#Fw0", {{ autoAlpha: 0 }}, {p("c15", 2):.3f});'); show("#Fb2", p("c15", 2))
# G + CTA
reveal("#sG", S[6]); stepstate(5, S[6] + 0.3); js(f'tl.set("#sF", {{ autoAlpha: 0 }}, {S[6] + 0.75:.3f});')
show("#Gt", p("c16", 0)); js(f'tl.fromTo(".Gb", {{ autoAlpha: 0, x: -30 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.25 }}, {p("c16", 0, 0.4):.3f});')
show("#Gp", p("c16", 2)); js(f'tl.fromTo(".Gpl", {{ autoAlpha: 0, x: 30 }}, {{ autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.9 }}, {p("c16", 3):.3f});')
reveal("#sH", p("c17", 0, -0.4)); js(f'tl.set(["#sG", "#stepbar"], {{ autoAlpha: 0 }}, {p("c17", 0, 0.4):.3f});')
js(f'tl.fromTo(["#x0", "#x1", "#x2"], {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" }}, {p("c17", 0, 0.1):.3f});')
show("#xw", p("c17", 0, 0.4)); show("#xt", p("c17", 1)); ev("chime", p("c17", 0, 0.2))
for t in [S[1], S[2], S[3], S[4], S[5]]: ev("chime2", t + 0.45)
json.dump(EV, open(os.path.join(ROOT, "build", "events.json"), "w"))

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Chatbot IA WhatsApp</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-fps="30" data-width="1920" data-height="1080">
{A}
{B}
{C}
{D}
{E}
{F}
{G}
      <div class="abs" id="stepbar" style="left:0;top:0;width:1920px;height:120px">{stepbar}</div>
{CAPS}
{"".join(f'      <audio id="v_{s["id"]}" src="audio/seg/{s["id"]}.wav" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="12" data-volume="1"></audio>{chr(10)}' for s in segs)}      <audio id="musica-fondo" src="audio/musica-duck.wav" data-start="0" data-duration="{T}" data-track-index="13" data-volume="0.8"></audio>
      <audio id="efectos-sonido" src="audio/efectos.wav" data-start="0" data-duration="{T}" data-track-index="14" data-volume="0.45"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const capShow = (sel, a, b) => {{
        tl.fromTo(sel, {{ autoAlpha: 0, y: 12 }}, {{ autoAlpha: 1, y: 0, duration: 0.15, ease: "power2.out" }}, a - 0.04);
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
