from common import build, LOGO_SVG
import os, math
OUT = os.path.join(os.path.dirname(__file__), '..', 'compositions')
def w(name, s): open(os.path.join(OUT, name), 'w').write(s)
def logo(i): return LOGO_SVG.replace('WG', 'WG' + i)

CHIP_CSS = '''
          .tchip { display: flex; align-items: center; gap: 14px; padding: 14px 32px 14px 20px; border-radius: 999px; background: #ffffff; box-shadow: 0 22px 46px rgba(60, 20, 120, 0.18), 0 6px 14px rgba(60, 20, 120, 0.1); font-size: 40px; font-weight: 700; white-space: nowrap; color: #170b2e; }
          .tchip i { display: block; width: 28px; height: 28px; border-radius: 50%; flex: 0 0 28px; }
'''
TOOLS = [('ChatGPT', '#7c3aed'), ('Gemini', '#4a76d6'), ('Perplexity', '#2e9b63'), ('NotebookLM', '#d9a21b'),
         ('Lovable', '#d74ac5'), ('v0', '#170b2e'), ('Make', '#7c3aed'), ('n8n', '#d64545'), ('Claude', '#d97a4a')]
def chip(name, color, extra=''):
    return '<div class="tchip" %s><i style="background:%s"></i>%s</div>' % (extra, color, name)

# ---------- 1 · caos ----------
pos = [(90, 120), (1330, 90), (660, 40), (60, 470), (1460, 420), (180, 840), (1280, 830), (700, 900), (1480, 640)]
chips1 = ''.join(chip(n, c, 'data-layout-allow-overlap="true" style="position:absolute;left:%dpx;top:%dpx"' % p) for (n, c), p in zip(TOOLS, pos))
w('scene-caos.html', build('scene-caos', 'Escena 1: caos', 5.7, CHIP_CSS + '''
          .c-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; }
          .c-title { font-size: 150px; text-align: center; white-space: nowrap; }
          .c-q { font-family: var(--font-display, system-ui, sans-serif); font-size: 110px; font-weight: 700; letter-spacing: -0.03em; white-space: nowrap; }
          .c-chips { position: absolute; inset: 0; }
''', '''
          <div class="c-chips">''' + chips1 + '''</div>
          <div class="content c-center">
            <h1 class="disp c-title">Hay mil herramientas<br />de <span class="grad">IA.</span></h1>
            <div class="c-q grad">¿Por dónde empiezas?</div>
          </div>
''', '''
            var cs = q(".tchip");
            var r = rng(77);
            for (var i = 0; i < cs.length; i++) {
              var a = r() * Math.PI * 2;
              tl.fromTo(cs[i], { x: Math.cos(a) * 1500, y: Math.sin(a) * 900, rotation: (r() - 0.5) * 180, scale: 0.4 }, { x: 0, y: 0, rotation: (r() - 0.5) * 16, scale: 1, duration: 0.9, ease: "back.out(1.3)" }, 0.1 + i * 0.1);
              tl.to(cs[i], { x: (r() - 0.5) * 90, y: (r() - 0.5) * 90, rotation: (r() - 0.5) * 22, duration: 1.2 + r(), ease: "sine.inOut", yoyo: true, repeat: 3 }, 1.2 + i * 0.05);
            }
            var ls = splitLetters(el(".c-title"), "c-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: 120, rotation: (r() - 0.5) * 30 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.6, ease: "power4.out" }, 0.3 + i * 0.03); });
            tl.fromTo(el(".c-q"), { autoAlpha: 0, scale: 2.6, rotation: -6 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 2.4);
            // everything shakes when the question lands
            tl.to(cs, { x: "+=14", duration: 0.06, yoyo: true, repeat: 5, ease: "none" }, 2.5);
            tl.fromTo(el(".c-center"), { scale: 1 }, { scale: 1.05, duration: 5.7, ease: "none" }, 0);
'''))

# ---------- 2 · orden ----------
cols = [('APRENDE', [TOOLS[0], TOOLS[1], TOOLS[2], TOOLS[3]]), ('CONSTRUYE', [TOOLS[4], TOOLS[5]]),
        ('AUTOMATIZA', [TOOLS[6], TOOLS[7], TOOLS[8], ('Webhooks', '#2e9b63')]), ('PRESENTA', [])]
colhtml = ''
for k, (lab, items) in enumerate(cols):
    inner = ''.join(chip(n, c) for n, c in items)
    if lab == 'PRESENTA':
        inner = '<div class="tchip fin"><i style="background:#d74ac5"></i>Tu proyecto final</div>'
    colhtml += '<div class="o-col" style="left:%dpx"><div class="o-num">%d</div><div class="o-lab">%s</div>%s</div>' % (110 + k * 440, k + 1, lab, inner)
w('scene-orden.html', build('scene-orden', 'Escena 2: orden', 6.6, CHIP_CSS + '''
          .o-bg { position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, #ffffff 0%, #faf7ff 60%, #efe7fb 100%); }
          .o-title { position: absolute; left: 0; right: 0; top: 80px; text-align: center; font-size: 118px; white-space: nowrap; }
          .o-line { position: absolute; left: 310px; top: 392px; width: 1300px; height: 10px; border-radius: 5px; background: #e1d4f7; }
          .o-fill { position: absolute; inset: 0; border-radius: 5px; background: linear-gradient(90deg, #5421a6, #7c3aed, #b5249f); }
          .o-col { position: absolute; top: 330px; width: 400px; display: flex; flex-direction: column; align-items: center; gap: 22px; }
          .o-num { width: 124px; height: 124px; border-radius: 50%; background: #ffffff; border: 8px solid #7c3aed; color: #5421a6; font-family: var(--font-display, system-ui, sans-serif); font-size: 72px; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(60, 20, 120, 0.2); }
          .o-lab { font-family: var(--font-display, system-ui, sans-serif); font-size: 50px; font-weight: 700; letter-spacing: 0.02em; color: #170b2e; margin: 4px 0 14px; }
          .fin { background: linear-gradient(135deg, #5421a6, #b5249f); color: #ffffff; }
''', '''
          <div class="o-bg"></div>
          <h2 class="disp o-title">Y ahora, <span class="grad">en orden.</span></h2>
          <div class="o-line"><div class="o-fill"></div></div>
          <div class="content">''' + colhtml + '''</div>
''', '''
            tl.to(el(".o-bg"), { autoAlpha: 0, duration: 0.6 }, 0.9);
            var ls = splitLetters(el(".o-title"), "o-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: -90, rotation: (i % 2 ? 1 : -1) * 18 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.6, ease: "bounce.out" }, 0.15 + i * 0.04); });
            tl.set(el(".o-fill"), { scaleX: 0, transformOrigin: "0% 50%" }, 0);
            tl.fromTo(el(".o-line"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 0.7);
            tl.to(el(".o-fill"), { scaleX: 1, duration: 3.2, ease: "power1.inOut" }, 1.1);
            var cols = q(".o-col");
            for (var k = 0; k < cols.length; k++) {
              var t0 = 0.9 + k * 0.85;
              tl.fromTo(cols[k].querySelector(".o-num"), { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2.2)" }, t0);
              tl.fromTo(cols[k].querySelector(".o-lab"), { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.4 }, t0 + 0.15);
              var chs = cols[k].querySelectorAll(".tchip");
              tl.fromTo(chs, { y: -700, autoAlpha: 0, rotation: function (i) { return (i % 2 ? 1 : -1) * 14; } }, { y: 0, autoAlpha: 1, rotation: 0, duration: 0.7, stagger: 0.14, ease: "bounce.out" }, t0 + 0.35);
            }
            tl.fromTo(el(".fin"), { scale: 1 }, { scale: 1.08, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }, 4.6);
            tl.fromTo(el(".content"), { scale: 1 }, { scale: 1.03, duration: 6.6, ease: "none" }, 0);
'''))

# ---------- 3 · ocho semanas + MVP ----------
nodes = ''.join('<div class="w-node" style="left:%dpx"><i></i><span>S%d</span></div>' % (130 + k * 237, k + 1) for k in range(8))
w('scene-semanas.html', build('scene-semanas', 'Escena 3: ocho semanas', 7.0, '''
          .w-big { position: absolute; left: 110px; top: 70px; font-size: 230px; line-height: 1; }
          .w-big small { font-size: 100px; letter-spacing: -0.03em; margin-left: 24px; }
          .w-pill { position: absolute; right: 110px; top: 130px; padding: 14px 40px; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #b5249f); color: #ffffff; font-family: var(--font-display, system-ui, sans-serif); font-size: 64px; font-weight: 700; box-shadow: 0 24px 50px rgba(84, 33, 166, 0.4); }
          .w-track { position: absolute; left: 130px; top: 470px; width: 1660px; height: 10px; border-radius: 5px; background: #e1d4f7; }
          .w-fill { position: absolute; inset: 0; border-radius: 5px; background: linear-gradient(90deg, #5421a6, #b5249f); }
          .w-node { position: absolute; top: 442px; width: 66px; margin-left: -33px; display: flex; flex-direction: column; align-items: center; }
          .w-node i { display: block; width: 66px; height: 66px; border-radius: 50%; background: #ffffff; border: 8px solid #cdb9f1; box-sizing: border-box; }
          .w-node span { margin-top: 10px; font-size: 38px; font-weight: 700; color: #4b4560; }
          .w-app { position: absolute; left: 510px; top: 600px; width: 900px; height: 400px; border-radius: 34px; background: #ffffff; box-shadow: 0 50px 100px rgba(60, 20, 120, 0.28); overflow: hidden; }
          .w-bar { position: absolute; left: 0; top: 0; width: 900px; height: 66px; background: linear-gradient(90deg, #5421a6, #b5249f); }
          .w-blk { position: absolute; border-radius: 20px; }
          .w-tile { background: #efe3ff; } .w-chart { background: #f6f1ff; } .w-cta { background: linear-gradient(90deg, #5421a6, #b5249f); }
          .w-stamp { position: absolute; right: 80px; top: 640px; padding: 14px 36px; border: 8px solid #2e9b63; border-radius: 22px; color: #2e9b63; font-family: var(--font-display, system-ui, sans-serif); font-size: 64px; font-weight: 700; background: rgba(255, 255, 255, 0.92); transform: rotate(-9deg); opacity: 0; }
          .w-conf { position: absolute; width: 20px; height: 20px; border-radius: 50%; opacity: 0; }
''', '''
          <h2 class="disp w-big">8<small>semanas</small></h2>
          <div class="w-pill">sin programar</div>
          <div class="w-track"><div class="w-fill"></div></div>
          ''' + nodes + '''
          <div class="w-app">
            <div class="w-bar"></div>
            <div class="w-blk w-tile" style="left:36px;top:96px;width:260px;height:110px"></div>
            <div class="w-blk w-tile" style="left:320px;top:96px;width:260px;height:110px"></div>
            <div class="w-blk w-tile" style="left:604px;top:96px;width:260px;height:110px"></div>
            <div class="w-blk w-chart" style="left:36px;top:230px;width:540px;height:140px"></div>
            <div class="w-blk w-cta" style="left:604px;top:230px;width:260px;height:140px"></div>
          </div>
          <div class="w-stamp">PUBLICADO ✓</div>
''', '''
            var r = rng(3);
            ls = splitLetters(el(".w-big"), "w-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, scale: 0.2, y: 60 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.7, ease: "back.out(2)" }, 0.1 + i * 0.07); });
            tl.fromTo(el(".w-pill"), { autoAlpha: 0, x: 200, rotation: 8 }, { autoAlpha: 1, x: 0, rotation: 0, duration: 0.8, ease: "back.out(1.6)" }, 0.9);
            tl.set(el(".w-fill"), { scaleX: 0, transformOrigin: "0% 50%" }, 0);
            tl.fromTo(el(".w-track"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 1.2);
            var nodes = q(".w-node");
            tl.to(el(".w-fill"), { scaleX: 1, duration: 2.8, ease: "none" }, 1.5);
            for (var k = 0; k < nodes.length; k++) {
              var t = 1.5 + (k / 7) * 2.8;
              tl.fromTo(nodes[k], { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: "power3.out" }, 1.3 + k * 0.08);
              tl.to(nodes[k].querySelector("i"), { backgroundColor: "#7c3aed", borderColor: "#5421a6", scale: 1.25, duration: 0.3, ease: "back.out(2.4)" }, t);
              tl.to(nodes[k].querySelector("i"), { scale: 1, duration: 0.25 }, t + 0.3);
            }
            // the MVP assembles block by block
            tl.fromTo(el(".w-app"), { autoAlpha: 0, y: 220, scale: 0.8 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.4)" }, 3.2);
            var blks = q(".w-blk, .w-bar");
            for (var b = 0; b < blks.length; b++) {
              var side = b % 2 ? 1 : -1;
              tl.fromTo(blks[b], { x: side * 700, autoAlpha: 0, rotation: side * 12 }, { x: 0, autoAlpha: 1, rotation: 0, duration: 0.55, ease: "back.out(1.5)" }, 3.6 + b * 0.22);
            }
            tl.fromTo(el(".w-stamp"), { autoAlpha: 0, scale: 3, rotation: -25 }, { autoAlpha: 1, scale: 1, rotation: -9, duration: 0.5, ease: "back.out(1.7)" }, 5.4);
            tl.to(el(".w-app"), { y: -12, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 5.4);
            var root2 = el(".w-app").parentNode;
            for (var c = 0; c < 22; c++) {
              var d = document.createElement("div"); d.className = "w-conf";
              d.style.left = "1250px"; d.style.top = "700px";
              d.style.background = ["#7c3aed", "#d74ac5", "#7ff0d3", "#ffffff"][c % 4];
              root2.appendChild(d);
              var a = (c / 22) * Math.PI * 2, dist = 160 + r() * 260;
              tl.set(d, { autoAlpha: 0 }, 0);
              tl.fromTo(d, { x: 0, y: 0, autoAlpha: 1, scale: 1 }, { x: Math.cos(a) * dist, y: Math.sin(a) * dist * 0.7, autoAlpha: 0, scale: 0.3, duration: 0.9, ease: "power3.out", immediateRender: false }, 5.5);
            }
'''.replace('ls = splitLetters', 'var ls = splitLetters')))

# ---------- 4 · para ti ----------
ICON = lambda p: '<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % p
rows = [('Emprendedoras.', '#5421a6', ICON('<path d="M5 19l3-1 8-8a3 3 0 00-4-4l-8 8-1 3zM14 6l4 4M15 13l5 5"/>')),
        ('Profesionales.', '#b5249f', ICON('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')),
        ('Consultoras.', '#170b2e', ICON('<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c1-4 3-6 7-6s6 2 7 6M16 14c3 0 5 2 6 5"/>'))]
rh = ''.join('<div class="p-row"><span class="p-ico">%s</span><span class="p-w" style="color:%s">%s</span></div>' % (ic, c, t) for t, c, ic in rows)
w('scene-parati.html', build('scene-parati', 'Escena 4: para ti', 6.5, '''
          .p-wrap { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; gap: 12px; padding-left: 220px; }
          .p-row { display: flex; align-items: center; gap: 36px; }
          .p-w { font-family: var(--font-display, system-ui, sans-serif); font-size: 190px; font-weight: 700; letter-spacing: -0.04em; line-height: 1.02; white-space: nowrap; }
          .p-ico { width: 150px; height: 150px; border-radius: 46px; background: linear-gradient(135deg, #5421a6, #d74ac5); display: flex; align-items: center; justify-content: center; box-shadow: 0 26px 54px rgba(84, 33, 166, 0.35); }
          .p-ico svg { display: block; width: 84px; height: 84px; }
          .p-pill { margin-top: 28px; padding: 18px 56px; border-radius: 999px; background: #ffffff; box-shadow: 0 24px 54px rgba(60, 20, 120, 0.2); font-size: 58px; font-weight: 700; margin-left: 186px; }
          .p-pill b { color: #5421a6; }
''', '''
          <div class="content p-wrap">
            ''' + rh + '''
            <div class="p-pill"><b>Sin experiencia técnica.</b> 100% no code</div>
          </div>
''', '''
            var rows = q(".p-row");
            for (var i = 0; i < rows.length; i++) {
              var side = i % 2 ? 1 : -1;
              tl.fromTo(rows[i], { x: side * 1400, autoAlpha: 0, skewX: side * -18 }, { x: 0, autoAlpha: 1, skewX: 0, duration: 0.9, ease: "power4.out" }, 0.2 + i * 0.7);
              tl.fromTo(rows[i].querySelector(".p-ico"), { scale: 0, rotation: -120 }, { scale: 1, rotation: 0, duration: 0.7, ease: "back.out(2)" }, 0.6 + i * 0.7);
              tl.to(rows[i], { x: 18, duration: 1.4 + i * 0.2, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.6 + i * 0.1);
            }
            tl.fromTo(el(".p-pill"), { autoAlpha: 0, y: 70, scale: 0.7 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 2.7);
            tl.fromTo(el(".p-wrap"), { scale: 1 }, { scale: 1.035, duration: 6.5, ease: "none" }, 0);
'''))

# ---------- 5 · facilitador ----------
w('scene-jaime.html', build('scene-jaime', 'Escena 5: facilitador', 6.5, '''
          .j-ring { position: absolute; left: 150px; top: 250px; width: 560px; height: 560px; border-radius: 50%; border: 4px dashed rgba(124, 58, 237, 0.4); }
          .j-ring2 { left: 90px; top: 190px; width: 680px; height: 680px; border-color: rgba(215, 74, 197, 0.35); }
          .j-photo { position: absolute; left: 190px; top: 290px; width: 480px; height: 480px; border-radius: 50%; padding: 14px; background: linear-gradient(135deg, #7ff0d3, #7c3aed 55%, #d74ac5); box-shadow: 0 50px 90px rgba(60, 20, 120, 0.3); }
          .j-photo img { display: block; width: 452px; height: 452px; border-radius: 50%; object-fit: cover; }
          .j-text { position: absolute; left: 840px; top: 250px; width: 980px; display: flex; flex-direction: column; gap: 14px; }
          .j-name { font-size: 96px; }
          .j-role { font-size: 60px; font-weight: 700; color: #5421a6; }
          .j-live { display: flex; align-items: center; gap: 30px; margin-top: 26px; }
          .j-num { font-family: var(--font-display, system-ui, sans-serif); font-size: 280px; font-weight: 700; letter-spacing: -0.05em; line-height: 0.95; color: #170b2e; }
          .j-lbl { display: flex; flex-direction: column; gap: 12px; align-items: flex-start; }
          .j-lbl b { font-family: var(--font-display, system-ui, sans-serif); font-size: 70px; line-height: 1.05; }
          .j-dot { display: inline-flex; align-items: center; gap: 14px; padding: 8px 26px; border-radius: 999px; background: #fdecec; color: #c0262d; font-size: 38px; font-weight: 700; }
          .j-dot i { display: block; width: 20px; height: 20px; border-radius: 50%; background: #e0343d; }
''', '''
          <div class="j-ring j-ring2" data-layout-allow-overflow="true"></div>
          <div class="j-ring" data-layout-allow-overflow="true"></div>
          <div class="j-photo"><img src="assets/img/jaime.png" alt="Jaime Fernández Chávez" /></div>
          <div class="j-text">
            <h2 class="disp j-name">Jaime Fernández <span class="grad">Chávez</span></h2>
            <div class="j-role">Director de Scaly AI</div>
            <div class="j-live"><div class="j-num">16</div><div class="j-lbl"><b>sesiones<br />en vivo</b><span class="j-dot"><i></i>EN VIVO</span></div></div>
          </div>
''', '''
            tl.fromTo(q(".j-ring"), { scale: 0.6, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 1.0, stagger: 0.2, ease: "power3.out" }, 0);
            tl.to(q(".j-ring"), { rotation: 360, duration: 12, ease: "none" }, 0);
            tl.fromTo(el(".j-photo"), { autoAlpha: 0, scale: 0.4, rotation: -30 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.9, ease: "back.out(1.6)" }, 0.2);
            tl.to(el(".j-photo"), { y: -16, duration: 1.8, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.2);
            var ls = splitLetters(el(".j-name"), "j-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, x: 80, filter: "blur(10px)" }, { autoAlpha: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 0.6 + i * 0.035); });
            tl.fromTo(el(".j-role"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 1.6);
            var num = el(".j-num"); var o = { v: 0 };
            tl.fromTo(el(".j-live"), { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 2.3);
            tl.to(o, { v: 16, duration: 1.4, ease: "power2.out", onUpdate: function () { num.textContent = String(Math.round(o.v)); } }, 2.4);
            tl.fromTo(el(".j-dot i"), { scale: 1 }, { scale: 1.6, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5 }, 3.0);
'''))

# ---------- 6 · precio ----------
rays = ''.join('<div class="e-ray" style="transform:rotate(%ddeg)"></div>' % (k * 15) for k in range(24))
w('scene-precio.html', build('scene-precio', 'Escena 6: precio', 6.0, '''
          .e-rays { position: absolute; left: 960px; top: 540px; width: 0; height: 0; }
          .e-ray { position: absolute; left: -10px; top: -1400px; width: 20px; height: 1400px; transform-origin: 10px 1400px; background: linear-gradient(180deg, rgba(196, 166, 255, 0), rgba(196, 166, 255, 0.35)); }
          .e-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; }
          .e-tag { font-size: 44px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #5421a6; }
          .e-old { font-size: 50px; font-weight: 500; color: #4b4560; text-decoration: line-through; text-decoration-thickness: 5px; }
          .e-price { font-family: var(--font-display, system-ui, sans-serif); font-size: 380px; font-weight: 700; letter-spacing: -0.05em; line-height: 1; white-space: nowrap; color: #5421a6; }
          .e-badge { margin-top: 10px; padding: 16px 56px; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #b5249f); color: #ffffff; font-size: 62px; font-weight: 700; box-shadow: 0 26px 54px rgba(84, 33, 166, 0.4); white-space: nowrap; }
          .e-usd { font-size: 46px; font-weight: 700; color: #170b2e; }
          .coin { position: absolute; width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff1b8, #f5b82e 60%, #c98a0c); border: 4px solid #e8a720; opacity: 0; }
''', '''
          <div class="e-rays" data-layout-allow-overflow="true">''' + rays + '''</div>
          <div class="content e-content">
            <div class="e-tag">Pack completo · 8 semanas</div>
            <div class="e-old">Por separado: S/ 598</div>
            <div class="e-price"><span class="e-cur">S/ </span><span class="e-num">499</span></div>
            <div class="e-usd">USD 135 · pago único</div>
            <div class="e-badge">Ahorras S/ 99</div>
          </div>
''', '''
            var r = rng(41);
            tl.fromTo(el(".e-rays"), { rotation: 0, autoAlpha: 0 }, { rotation: 40, autoAlpha: 1, duration: 6, ease: "none" }, 0);
            tl.fromTo(el(".e-tag"), { autoAlpha: 0, y: -40 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.2);
            tl.fromTo(el(".e-old"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 0.5);
            var obj = { v: 0 }; var num = el(".e-num");
            tl.fromTo(el(".e-price"), { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.8, ease: "back.out(1.7)" }, 0.6);
            tl.to(obj, { v: 499, duration: 1.6, ease: "power3.out", onUpdate: function () { num.textContent = String(Math.round(obj.v)); } }, 0.7);
            tl.fromTo(el(".e-usd"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 2.1);
            tl.fromTo(el(".e-badge"), { autoAlpha: 0, scale: 0.3, rotation: -10 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.9, ease: "elastic.out(1, 0.5)" }, 2.3);
            tl.to(el(".e-badge"), { scale: 1.06, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 3 }, 3.3);
            var host = el(".e-content");
            for (var c = 0; c < 18; c++) {
              var d = document.createElement("div"); d.className = "coin";
              d.style.left = (900 + r() * 120) + "px"; d.style.top = "380px";
              host.appendChild(d);
              var a = -Math.PI / 2 + (r() - 0.5) * 2.2, dist = 260 + r() * 340;
              tl.set(d, { autoAlpha: 0 }, 0);
              tl.fromTo(d, { x: 0, y: 0, autoAlpha: 1, rotation: 0 }, { x: Math.cos(a) * dist, y: Math.sin(a) * dist + 420, autoAlpha: 0, rotation: 360 * (r() > 0.5 ? 1 : -1), duration: 1.5, ease: "power2.out", immediateRender: false }, 2.4 + r() * 0.3);
            }
            tl.fromTo(el(".e-content"), { scale: 1 }, { scale: 1.04, duration: 6, ease: "none" }, 0);
'''))

# ---------- 7 · cierre ----------
w('scene-final.html', build('scene-final', 'Escena 7: cierre', 4.7, '''
          .z-bg { position: absolute; inset: 0; background: radial-gradient(circle at 20% 15%, #7c3aed 0%, transparent 52%), radial-gradient(circle at 85% 90%, #d74ac5 0%, transparent 50%), linear-gradient(160deg, #1d0a45 0%, #3b1285 100%); }
          .z-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 36px; color: #ffffff; }
          .z-title { font-size: 150px; text-align: center; color: #ffffff; white-space: nowrap; }
          .z-title .z-acc { color: #ffa8ec; }
          .z-pill { height: 112px; padding: 0 64px; display: flex; align-items: center; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #c42fa8); border: 3px solid rgba(255, 255, 255, 0.4); font-size: 56px; font-weight: 700; box-shadow: 0 26px 60px rgba(215, 74, 197, 0.45); white-space: nowrap; }
          .z-info { font-size: 40px; font-weight: 500; color: #ece2ff; text-align: center; line-height: 1.4; }
          .z-logo { position: absolute; left: 0; right: 0; top: 70px; display: flex; align-items: center; justify-content: center; gap: 18px; }
          .wl-badge { display: block; width: 76px; height: 76px; }
          .wl-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 54px; font-weight: 700; letter-spacing: -0.02em; }
          .z-ring { position: absolute; left: 810px; top: 300px; width: 300px; height: 300px; border-radius: 50%; border: 5px solid #ffa8ec; opacity: 0; }
''', '''
          <div class="z-bg"></div>
          <div class="z-ring zr0" data-layout-allow-overflow="true"></div>
          <div class="z-ring zr1" data-layout-allow-overflow="true"></div>
          <div class="z-logo" style="color:#ffffff">''' + logo('7') + '''<span class="wl-name">Warmi Academy</span></div>
          <div class="content z-content">
            <h1 class="disp z-title">De usar IA a<br /><span class="z-acc">construir con ella.</span></h1>
            <div class="z-pill">Empieza el 7 de octubre</div>
            <div class="z-info">6:30 p. m. Perú, Colombia, Ecuador · 2.ª edición<br />warmi.ventures@gmail.com</div>
          </div>
''', '''
            tl.fromTo(el(".z-bg"), { scale: 1.15 }, { scale: 1, duration: 3, ease: "power2.out" }, 0);
            tl.fromTo(el(".z-logo"), { y: -50 }, { y: 0, duration: 0.7, ease: "power3.out" }, 0.4);
            var ls = splitLetters(el(".z-title"), "z-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { y: 110, scale: 0.7 }, { y: 0, scale: 1, duration: 0.6, ease: "back.out(1.7)" }, 0.5 + i * 0.03); });
            tl.fromTo(el(".z-pill"), { y: 70, scale: 0.6 }, { y: 0, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 1.9);
            tl.fromTo(el(".z-info"), { y: 30 }, { y: 0, duration: 0.6, ease: "power2.out" }, 2.4);
            var rings = q(".z-ring");
            for (var i = 0; i < rings.length; i++) tl.fromTo(rings[i], { scale: 0.3, autoAlpha: 0.8 }, { scale: 4.2, autoAlpha: 0, duration: 1.3, ease: "power2.out" }, 1.9 + i * 0.25);
            tl.to(el(".z-pill"), { scale: 1.05, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 2 }, 2.8);
            tl.fromTo(el(".z-content"), { scale: 1 }, { scale: 1.03, duration: 4.7, ease: "none" }, 0);
'''))
print('ok')
