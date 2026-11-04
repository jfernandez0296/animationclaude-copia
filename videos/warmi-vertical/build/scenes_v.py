from common import build, LOGO_SVG
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'compositions')
def w(name, s): open(os.path.join(OUT, name), 'w').write(s)
def logo(i): return LOGO_SVG.replace('WG', 'WG' + i)
CHIP_CSS = '''
          .tchip { display: flex; align-items: center; gap: 14px; padding: 14px 30px 14px 20px; border-radius: 999px; background: #ffffff; box-shadow: 0 22px 46px rgba(60, 20, 120, 0.18), 0 6px 14px rgba(60, 20, 120, 0.1); font-size: 40px; font-weight: 700; white-space: nowrap; color: #170b2e; }
          .tchip i { display: block; width: 28px; height: 28px; border-radius: 50%; flex: 0 0 28px; }
'''
TOOLS = [('ChatGPT', '#7c3aed'), ('Gemini', '#4a76d6'), ('Perplexity', '#2e9b63'), ('NotebookLM', '#d9a21b'),
         ('Lovable', '#d74ac5'), ('v0', '#170b2e'), ('Make', '#7c3aed'), ('n8n', '#d64545'), ('Claude', '#d97a4a')]
def chip(name, color, extra=''): return '<div class="tchip" %s><i style="background:%s"></i>%s</div>' % (extra, color, name)

# 1 caos
pos = [(40, 110), (560, 70), (300, 310), (30, 1330), (640, 1390), (180, 1560), (560, 1660), (40, 1770), (620, 1250)]
chips1 = ''.join(chip(n, c, 'data-layout-allow-overlap="true" style="position:absolute;left:%dpx;top:%dpx"' % p) for (n, c), p in zip(TOOLS, pos))
w('scene-caos.html', build('scene-caos', 'V1 caos', 5.7, CHIP_CSS + '''
          .c-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 40px; }
          .c-title { font-size: 136px; text-align: center; white-space: nowrap; }
          .c-q { font-family: var(--font-display, system-ui, sans-serif); font-size: 124px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.04; text-align: center; white-space: nowrap; }
''', '<div class="c-chips">' + chips1 + '''</div>
          <div class="content c-center">
            <h1 class="disp c-title">Hay mil<br />herramientas<br />de <span class="grad">IA.</span></h1>
            <div class="c-q grad">¿Por dónde<br />empiezas?</div>
          </div>
''', '''
            var cs = q(".tchip"); var r = rng(77);
            for (var i = 0; i < cs.length; i++) {
              var a = r() * Math.PI * 2;
              tl.fromTo(cs[i], { x: Math.cos(a) * 1500, y: Math.sin(a) * 1500, rotation: (r() - 0.5) * 180, scale: 0.4 }, { x: 0, y: 0, rotation: (r() - 0.5) * 16, scale: 1, duration: 0.9, ease: "back.out(1.3)" }, 0.1 + i * 0.1);
              tl.to(cs[i], { x: (r() - 0.5) * 80, y: (r() - 0.5) * 80, rotation: (r() - 0.5) * 22, duration: 1.2 + r(), ease: "sine.inOut", yoyo: true, repeat: 3 }, 1.2 + i * 0.05);
            }
            var ls = splitLetters(el(".c-title"), "c-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: 120, rotation: (r() - 0.5) * 30 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.6, ease: "power4.out" }, 0.3 + i * 0.035); });
            tl.fromTo(el(".c-q"), { autoAlpha: 0, scale: 2.6, rotation: -6 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 2.4);
            tl.to(cs, { x: "+=14", duration: 0.06, yoyo: true, repeat: 5, ease: "none" }, 2.5);
            tl.fromTo(el(".c-center"), { scale: 1 }, { scale: 1.05, duration: 5.7, ease: "none" }, 0);
'''))

# 2 orden
cols = [('APRENDE', TOOLS[0:4]), ('CONSTRUYE', TOOLS[4:6]), ('AUTOMATIZA', TOOLS[6:9] + [('Webhooks', '#2e9b63')]), ('PRESENTA', [])]
rows = ''
for k, (lab, items) in enumerate(cols):
    inner = ''.join(chip(n, c) for n, c in items) if items else '<div class="tchip fin"><i style="background:#d74ac5"></i>Tu proyecto final</div>'
    rows += '<div class="o-row"><div class="o-num">%d</div><div class="o-body"><div class="o-lab">%s</div><div class="o-chips">%s</div></div></div>' % (k + 1, lab, inner)
w('scene-orden.html', build('scene-orden', 'V2 orden', 6.6, CHIP_CSS + '''
          .o-bg { position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, #ffffff 0%, #faf7ff 60%, #efe7fb 100%); }
          .o-title { position: absolute; left: 0; right: 0; top: 130px; text-align: center; font-size: 128px; white-space: nowrap; }
          .o-list { position: absolute; left: 70px; top: 520px; width: 940px; display: flex; flex-direction: column; gap: 44px; }
          .o-line { position: absolute; left: 60px; top: 60px; width: 10px; height: 880px; border-radius: 5px; background: #e1d4f7; }
          .o-fill { position: absolute; inset: 0; border-radius: 5px; background: linear-gradient(180deg, #5421a6, #b5249f); }
          .o-row { position: relative; display: flex; align-items: flex-start; gap: 36px; }
          .o-num { flex: 0 0 120px; width: 120px; height: 120px; border-radius: 50%; background: #ffffff; border: 8px solid #7c3aed; color: #5421a6; font-family: var(--font-display, system-ui, sans-serif); font-size: 70px; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(60, 20, 120, 0.2); }
          .o-body { display: flex; flex-direction: column; gap: 14px; }
          .o-lab { font-family: var(--font-display, system-ui, sans-serif); font-size: 58px; font-weight: 700; letter-spacing: 0.02em; color: #170b2e; line-height: 1.1; }
          .o-chips { display: flex; flex-wrap: wrap; gap: 16px; width: 780px; }
          .fin { background: linear-gradient(135deg, #5421a6, #b5249f); color: #ffffff; }
''', '''
          <div class="o-bg"></div>
          <h2 class="disp o-title">Y ahora,<br /><span class="grad">en orden.</span></h2>
          <div class="content"><div class="o-list"><div class="o-line"><div class="o-fill"></div></div>''' + rows + '''</div></div>
''', '''
            tl.to(el(".o-bg"), { autoAlpha: 0, duration: 0.6 }, 0.9);
            var ls = splitLetters(el(".o-title"), "o-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: -90, rotation: (i % 2 ? 1 : -1) * 18 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.6, ease: "bounce.out" }, 0.15 + i * 0.045); });
            tl.set(el(".o-fill"), { scaleY: 0, transformOrigin: "50% 0%" }, 0);
            tl.to(el(".o-fill"), { scaleY: 1, duration: 3.4, ease: "power1.inOut" }, 1.0);
            var rows = q(".o-row");
            for (var k = 0; k < rows.length; k++) {
              var t0 = 0.9 + k * 0.9;
              tl.fromTo(rows[k].querySelector(".o-num"), { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2.2)" }, t0);
              tl.fromTo(rows[k].querySelector(".o-lab"), { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.45 }, t0 + 0.15);
              tl.fromTo(rows[k].querySelectorAll(".tchip"), { x: 900, autoAlpha: 0, rotation: function (i) { return (i % 2 ? 1 : -1) * 10; } }, { x: 0, autoAlpha: 1, rotation: 0, duration: 0.6, stagger: 0.12, ease: "back.out(1.4)" }, t0 + 0.35);
            }
            tl.fromTo(el(".fin"), { scale: 1 }, { scale: 1.08, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }, 4.8);
            tl.fromTo(el(".content"), { scale: 1 }, { scale: 1.025, duration: 6.6, ease: "none" }, 0);
'''))

# 3 semanas
nodes = ''.join('<div class="w-node" style="left:%dpx"><i></i><span>S%d</span></div>' % (95 + k * 127, k + 1) for k in range(8))
w('scene-semanas.html', build('scene-semanas', 'V3 ocho semanas', 7.0, '''
          .w-big { position: absolute; left: 70px; top: 150px; font-size: 330px; line-height: 1; white-space: nowrap; }
          .w-big small { font-size: 130px; letter-spacing: -0.03em; margin-left: 24px; }
          .w-pill { position: absolute; left: 70px; top: 540px; padding: 16px 52px; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #b5249f); color: #ffffff; font-family: var(--font-display, system-ui, sans-serif); font-size: 80px; font-weight: 700; box-shadow: 0 24px 50px rgba(84, 33, 166, 0.4); }
          .w-track { position: absolute; left: 95px; top: 852px; width: 889px; height: 10px; border-radius: 5px; background: #e1d4f7; }
          .w-fill { position: absolute; inset: 0; border-radius: 5px; background: linear-gradient(90deg, #5421a6, #b5249f); }
          .w-node { position: absolute; top: 824px; width: 60px; margin-left: -30px; display: flex; flex-direction: column; align-items: center; }
          .w-node i { display: block; width: 60px; height: 60px; border-radius: 50%; background: #ffffff; border: 8px solid #cdb9f1; box-sizing: border-box; }
          .w-node span { margin-top: 10px; font-size: 34px; font-weight: 700; color: #4b4560; }
          .w-app { position: absolute; left: 70px; top: 980px; width: 940px; height: 700px; border-radius: 34px; background: #ffffff; box-shadow: 0 50px 100px rgba(60, 20, 120, 0.28); overflow: hidden; }
          .w-bar { position: absolute; left: 0; top: 0; width: 940px; height: 78px; background: linear-gradient(90deg, #5421a6, #b5249f); color: #ffffff; font-size: 40px; font-weight: 700; line-height: 78px; padding-left: 36px; }
          .w-blk { position: absolute; border-radius: 22px; display: flex; flex-direction: column; justify-content: center; padding: 0 36px; font-weight: 700; }
          .w-hero { left: 36px; top: 110px; width: 868px; height: 230px; background: #f1e8ff; font-size: 70px; line-height: 1.05; color: #170b2e; font-family: var(--font-display, system-ui, sans-serif); }
          .w-hero small { font-family: var(--font-body, system-ui, sans-serif); font-size: 38px; font-weight: 500; color: #4b4560; margin-top: 10px; }
          .w-cta { left: 36px; top: 364px; width: 868px; height: 130px; background: linear-gradient(90deg, #5421a6, #b5249f); color: #ffffff; font-size: 56px; align-items: center; text-align: center; }
          .w-tile { top: 520px; width: 270px; height: 130px; background: #efe3ff; color: #5421a6; font-size: 40px; align-items: center; padding: 0; }
          .w-stamp { position: absolute; right: 20px; top: 12px; height: 54px; padding: 0 26px; border-radius: 27px; background: #2e9b63; color: #ffffff; font-family: var(--font-display, system-ui, sans-serif); font-size: 32px; font-weight: 700; line-height: 54px; opacity: 0; }
          .w-conf { position: absolute; width: 20px; height: 20px; border-radius: 50%; opacity: 0; }
''', '''
          <h2 class="disp w-big">8<small>semanas</small></h2>
          <div class="w-pill">sin programar</div>
          <div class="w-track"><div class="w-fill"></div></div>
          ''' + nodes + '''
          <div class="w-app">
            <div class="w-bar">Mi negocio</div>
            <div class="w-stamp">PUBLICADO ✓</div>
            <div class="w-blk w-hero">Reserva en 1 minuto<small>Tu cliente elige y listo</small></div>
            <div class="w-blk w-cta">Reservar →</div>
            <div class="w-blk w-tile" style="left:36px">Servicios</div>
            <div class="w-blk w-tile" style="left:335px">Horarios</div>
            <div class="w-blk w-tile" style="left:634px">Pagos</div>
          </div>
''', '''
            var r = rng(3);
            var ls = splitLetters(el(".w-big"), "w-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, scale: 0.2, y: 60 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.7, ease: "back.out(2)" }, 0.1 + i * 0.07); });
            tl.fromTo(el(".w-pill"), { autoAlpha: 0, x: 300, rotation: 8 }, { autoAlpha: 1, x: 0, rotation: 0, duration: 0.8, ease: "back.out(1.6)" }, 0.9);
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
            tl.fromTo(el(".w-app"), { autoAlpha: 0, y: 260, scale: 0.8 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.4)" }, 3.2);
            var blks = q(".w-blk, .w-bar");
            for (var b = 0; b < blks.length; b++) {
              var side = b % 2 ? 1 : -1;
              tl.fromTo(blks[b], { x: side * 600, autoAlpha: 0, rotation: side * 12 }, { x: 0, autoAlpha: 1, rotation: 0, duration: 0.55, ease: "back.out(1.5)" }, 3.6 + b * 0.22);
            }
            tl.fromTo(el(".w-stamp"), { autoAlpha: 0, scale: 0.2 }, { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(2.4)" }, 5.4);
            tl.to(el(".w-app"), { y: -12, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 5.4);
            var host = el(".w-app").parentNode;
            for (var c = 0; c < 22; c++) {
              var d = document.createElement("div"); d.className = "w-conf";
              d.style.left = "540px"; d.style.top = "1300px";
              d.style.background = ["#7c3aed", "#d74ac5", "#7ff0d3", "#ffffff"][c % 4];
              host.appendChild(d);
              var a = (c / 22) * Math.PI * 2, dist = 160 + r() * 300;
              tl.set(d, { autoAlpha: 0 }, 0);
              tl.fromTo(d, { x: 0, y: 0, autoAlpha: 1, scale: 1 }, { x: Math.cos(a) * dist, y: Math.sin(a) * dist * 0.8, autoAlpha: 0, scale: 0.3, duration: 0.9, ease: "power3.out", immediateRender: false }, 5.5);
            }
'''))

# 4 para ti
ICON = lambda p: '<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % p
rws = [('Emprendedoras.', '#5421a6', ICON('<path d="M5 19l3-1 8-8a3 3 0 00-4-4l-8 8-1 3zM14 6l4 4M15 13l5 5"/>')),
       ('Profesionales.', '#b5249f', ICON('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')),
       ('Consultoras.', '#170b2e', ICON('<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c1-4 3-6 7-6s6 2 7 6M16 14c3 0 5 2 6 5"/>'))]
rh = ''.join('<div class="p-row"><span class="p-ico">%s</span><span class="p-w" style="color:%s">%s</span></div>' % (ic, c, t) for t, c, ic in rws)
w('scene-parati.html', build('scene-parati', 'V4 para ti', 6.5, '''
          .p-wrap { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; gap: 56px; padding-left: 50px; }
          .p-row { display: flex; align-items: center; gap: 24px; }
          .p-w { font-family: var(--font-display, system-ui, sans-serif); font-size: 112px; font-weight: 700; letter-spacing: -0.04em; line-height: 1.02; white-space: nowrap; }
          .p-ico { flex: 0 0 96px; width: 96px; height: 96px; border-radius: 30px; background: linear-gradient(135deg, #5421a6, #d74ac5); display: flex; align-items: center; justify-content: center; box-shadow: 0 26px 54px rgba(84, 33, 166, 0.35); }
          .p-ico svg { display: block; width: 56px; height: 56px; }
          .p-pill { margin-top: 30px; padding: 24px 56px; border-radius: 40px; background: #ffffff; box-shadow: 0 24px 54px rgba(60, 20, 120, 0.2); font-size: 58px; font-weight: 700; line-height: 1.2; align-self: center; text-align: center; }
          .p-pill b { color: #5421a6; }
''', '''
          <div class="content p-wrap">
            ''' + rh + '''
            <div class="p-pill"><b>Sin experiencia técnica.</b><br />100% no code</div>
          </div>
''', '''
            var rows = q(".p-row");
            for (var i = 0; i < rows.length; i++) {
              var side = i % 2 ? 1 : -1;
              tl.fromTo(rows[i], { x: side * 1200, autoAlpha: 0, skewX: side * -18 }, { x: 0, autoAlpha: 1, skewX: 0, duration: 0.9, ease: "power4.out" }, 0.2 + i * 0.7);
              tl.fromTo(rows[i].querySelector(".p-ico"), { scale: 0, rotation: -120 }, { scale: 1, rotation: 0, duration: 0.7, ease: "back.out(2)" }, 0.6 + i * 0.7);
              tl.to(rows[i], { x: 14, duration: 1.4 + i * 0.2, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.6 + i * 0.1);
            }
            tl.fromTo(el(".p-pill"), { autoAlpha: 0, y: 70, scale: 0.7 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 2.7);
            tl.fromTo(el(".p-wrap"), { scale: 1 }, { scale: 1.035, duration: 6.5, ease: "none" }, 0);
'''))

# 5 jaime
w('scene-jaime.html', build('scene-jaime', 'V5 facilitador', 6.5, '''
          .j-ring { position: absolute; left: 190px; top: 180px; width: 700px; height: 700px; border-radius: 50%; border: 4px dashed rgba(124, 58, 237, 0.4); }
          .j-ring2 { left: 120px; top: 110px; width: 840px; height: 840px; border-color: rgba(215, 74, 197, 0.35); }
          .j-photo { position: absolute; left: 270px; top: 260px; width: 540px; height: 540px; border-radius: 50%; padding: 14px; background: linear-gradient(135deg, #7ff0d3, #7c3aed 55%, #d74ac5); box-shadow: 0 50px 90px rgba(60, 20, 120, 0.3); }
          .j-photo img { display: block; width: 512px; height: 512px; border-radius: 50%; object-fit: cover; }
          .j-text { position: absolute; left: 0; right: 0; top: 1020px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; }
          .j-name { font-size: 104px; }
          .j-role { font-size: 64px; font-weight: 700; color: #5421a6; }
          .j-live { display: flex; align-items: center; justify-content: center; gap: 34px; margin-top: 56px; }
          .j-num { font-family: var(--font-display, system-ui, sans-serif); font-size: 300px; font-weight: 700; letter-spacing: -0.05em; line-height: 0.95; color: #170b2e; }
          .j-lbl { display: flex; flex-direction: column; gap: 14px; align-items: flex-start; text-align: left; }
          .j-lbl b { font-family: var(--font-display, system-ui, sans-serif); font-size: 76px; line-height: 1.05; }
          .j-dot { display: inline-flex; align-items: center; gap: 14px; padding: 8px 26px; border-radius: 999px; background: #fdecec; color: #c0262d; font-size: 40px; font-weight: 700; }
          .j-dot i { display: block; width: 20px; height: 20px; border-radius: 50%; background: #e0343d; }
''', '''
          <div class="j-ring j-ring2" data-layout-allow-overflow="true"></div>
          <div class="j-ring" data-layout-allow-overflow="true"></div>
          <div class="j-photo"><img src="assets/img/jaime.png" alt="Jaime Fernández Chávez" /></div>
          <div class="j-text">
            <h2 class="disp j-name">Jaime Fernández<br /><span class="grad">Chávez</span></h2>
            <div class="j-role">Director de Scaly AI</div>
            <div class="j-live"><div class="j-num">16</div><div class="j-lbl"><b>sesiones<br />en vivo</b><span class="j-dot"><i></i>EN VIVO</span></div></div>
          </div>
''', '''
            tl.fromTo(q(".j-ring"), { scale: 0.6, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 1.0, stagger: 0.2, ease: "power3.out" }, 0);
            tl.to(q(".j-ring"), { rotation: 360, duration: 12, ease: "none" }, 0);
            tl.fromTo(el(".j-photo"), { autoAlpha: 0, scale: 0.4, rotation: -30 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.9, ease: "back.out(1.6)" }, 0.2);
            tl.to(el(".j-photo"), { y: -16, duration: 1.8, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.2);
            var ls = splitLetters(el(".j-name"), "j-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: 60, filter: "blur(10px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 0.6 + i * 0.035); });
            tl.fromTo(el(".j-role"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 1.6);
            var num = el(".j-num"); var o = { v: 0 };
            tl.fromTo(el(".j-live"), { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 2.3);
            tl.to(o, { v: 16, duration: 1.4, ease: "power2.out", onUpdate: function () { num.textContent = String(Math.round(o.v)); } }, 2.4);
            tl.fromTo(el(".j-dot i"), { scale: 1 }, { scale: 1.6, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5 }, 3.0);
'''))

# 6 final
w('scene-final.html', build('scene-final', 'V6 cierre', 10.2, '''
          .z-bg { position: absolute; inset: 0; background: radial-gradient(circle at 20% 15%, #7c3aed 0%, transparent 52%), radial-gradient(circle at 85% 90%, #d74ac5 0%, transparent 50%), linear-gradient(160deg, #1d0a45 0%, #3b1285 100%); }
          .z-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 56px; color: #ffffff; }
          .z-title { font-size: 150px; text-align: center; color: #ffffff; white-space: nowrap; }
          .z-title .z-acc { color: #ffa8ec; }
          .z-pill { padding: 30px 64px; display: flex; align-items: center; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #c42fa8); border: 3px solid rgba(255, 255, 255, 0.4); font-size: 60px; font-weight: 700; box-shadow: 0 26px 60px rgba(215, 74, 197, 0.45); white-space: nowrap; }
          .z-info { font-size: 42px; font-weight: 500; color: #ece2ff; text-align: center; line-height: 1.45; }
          .z-logo { position: absolute; left: 0; right: 0; top: 150px; display: flex; align-items: center; justify-content: center; gap: 18px; }
          .wl-badge { display: block; width: 84px; height: 84px; }
          .wl-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 60px; font-weight: 700; letter-spacing: -0.02em; }
          .z-ring { position: absolute; left: 390px; top: 800px; width: 300px; height: 300px; border-radius: 50%; border: 5px solid #ffa8ec; opacity: 0; }
''', '''
          <div class="z-bg"></div>
          <div class="z-ring zr0" data-layout-allow-overflow="true"></div>
          <div class="z-ring zr1" data-layout-allow-overflow="true"></div>
          <div class="z-logo" style="color:#ffffff">''' + logo('7') + '''<span class="wl-name">Warmi Academy</span></div>
          <div class="content z-content">
            <h1 class="disp z-title">De usar IA a<br /><span class="z-acc">construir<br />con ella.</span></h1>
            <div class="z-pill">Empieza el 7 de octubre</div>
            <div class="z-info">6:30 p. m. Perú, Colombia, Ecuador<br />2.ª edición<br />warmi.ventures@gmail.com</div>
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
            tl.to(el(".z-pill"), { scale: 1.05, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 9 }, 2.8);
            tl.fromTo(el(".z-content"), { scale: 1 }, { scale: 1.03, duration: 10.2, ease: "none" }, 0);
'''))
print('ok')
