from common import build, LOGO_SVG
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'compositions')
def w(name, s): open(os.path.join(OUT, name), 'w').write(s)
def logo(i): return LOGO_SVG.replace('WG', 'WG' + i)

LOGO_CSS = '''
          .wl { display: flex; align-items: center; gap: 18px; }
          .wl-badge { display: block; width: 76px; height: 76px; flex: 0 0 76px; }
          .wl-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 52px; font-weight: 700; letter-spacing: -0.02em; line-height: 1; }
          .wl-by { font-size: 28px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #4b4560; margin-left: 4px; }
'''

# ---------- S1 · gancho ----------
w('scene-gancho.html', build('scene-gancho', 'Escena 1: gancho', 5.3, '''
          .g-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 36px; }
          .g-title { font-size: 128px; text-align: center; white-space: nowrap; }
          .g-q { font-family: var(--font-display, system-ui, sans-serif); font-size: 68px; font-weight: 500; letter-spacing: -0.02em; color: #4b4560; white-space: nowrap; display: flex; gap: 18px; }
          .g-q b { font-weight: 700; color: #5421a6; }
          .g-w { display: inline-block; }
          .chip { position: absolute; display: flex; align-items: center; gap: 16px; padding: 16px 32px 16px 22px; border-radius: 999px; background: #ffffff; box-shadow: 0 24px 50px rgba(60, 20, 120, 0.16), 0 6px 14px rgba(60, 20, 120, 0.08); font-size: 36px; font-weight: 700; color: #170b2e; white-space: nowrap; }
          .chip i { display: block; width: 40px; height: 40px; border-radius: 50%; border: 5px solid #7c3aed; flex: 0 0 40px; }
''', '''
          <div class="content g-content">
            <h1 class="disp g-title">Tu semana está llena de<br /><span class="grad">tareas repetitivas.</span></h1>
            <p class="g-q"><b>¿Y si</b> <span>la IA las hiciera por ti?</span></p>
          </div>
          <div class="chip c1" style="left: 130px; top: 190px"><i></i>Responder correos</div>
          <div class="chip c2" style="left: 1330px; top: 160px"><i></i>Pasar datos a Excel</div>
          <div class="chip c3" style="left: 90px; top: 790px"><i></i>Armar reportes</div>
          <div class="chip c4" style="left: 1400px; top: 800px"><i></i>Copiar y pegar</div>
''', '''
            tl.fromTo(el(".g-content"), { scale: 1 }, { scale: 1.04, duration: 5, ease: "none" }, 0);
            var ls = splitLetters(el(".g-title"), "g-ch");
            var r = rng(5);
            ls.forEach(function (c, i) {
              tl.fromTo(c, { autoAlpha: 0, y: 110, rotation: (r() - 0.5) * 24 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.6, ease: "power4.out" }, 0.15 + i * 0.03);
            });
            var qw = el(".g-q"); var qs = [];
            Array.prototype.slice.call(qw.querySelectorAll("b, span")).forEach(function (n) { n.classList.add("g-w"); qs.push(n); });
            tl.fromTo(qs, { autoAlpha: 0, y: 40, filter: "blur(12px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.7, stagger: 0.3, ease: "power2.out" }, 2.0);
            var chips = q(".chip");
            for (var i = 0; i < chips.length; i++) {
              tl.fromTo(chips[i], { autoAlpha: 0, scale: 0.6, y: 50, rotation: i % 2 ? 6 : -6 }, { autoAlpha: 1, scale: 1, y: 0, rotation: 0, duration: 0.6, ease: "back.out(1.8)" }, 0.5 + i * 0.22);
              tl.to(chips[i], { y: -14, duration: 1.3 + i * 0.15, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.4 + i * 0.1);
            }
'''))

# ---------- S2 · programa ----------
w('scene-programa.html', build('scene-programa', 'Escena 2: el programa', 7.0, LOGO_CSS + '''
          .p-bg { position: absolute; inset: 0; background: radial-gradient(circle at 12% 8%, rgba(196,166,255,0.55), transparent 48%), radial-gradient(circle at 92% 92%, rgba(127,240,211,0.45), transparent 46%), radial-gradient(ellipse at 50% 40%, #ffffff 0%, #faf7ff 55%, #efe7fb 100%); }
          .p-left { position: absolute; left: 110px; top: 130px; width: 900px; display: flex; flex-direction: column; gap: 34px; align-items: flex-start; }
          .p-title { font-size: 104px; }
          .p-checks { display: flex; flex-direction: column; gap: 16px; }
          .p-check { display: flex; align-items: center; gap: 18px; font-size: 40px; font-weight: 700; }
          .p-check i { display: block; width: 44px; height: 44px; border-radius: 50%; background: #7c3aed; flex: 0 0 44px; position: relative; }
          .p-check i::after { content: ""; position: absolute; left: 14px; top: 8px; width: 11px; height: 20px; border: solid #fff; border-width: 0 5px 5px 0; transform: rotate(45deg); }
          .p-shot { position: absolute; left: 1060px; top: 150px; width: 760px; border-radius: 34px; background: #ffffff; padding: 0; overflow: hidden; }
          .p-bar { display: flex; gap: 12px; padding: 18px 24px; background: #f1ebfb; }
          .p-bar span { display: block; width: 18px; height: 18px; border-radius: 50%; background: #c9b6ee; }
          .p-shot img { display: block; width: 760px; height: 690px; object-fit: cover; object-position: 0 0; }
''', '''
          <div class="p-bg"></div>
          <div class="content">
            <div class="p-left">
              <div class="wl">''' + logo('2') + '''<span class="wl-name">Warmi <span class="grad">Academy</span></span><span class="wl-by">by Warmi Ventures</span></div>
              <h1 class="disp p-title">Aprende a usar la IA y <span class="grad">automatiza tu trabajo en 8 semanas</span></h1>
              <div class="p-checks"><div class="p-check"><i></i>100% sin código</div><div class="p-check"><i></i>Clases en vivo y grabaciones</div></div>
            </div>
            <div class="card p-shot"><div class="p-bar"><span></span><span></span><span></span></div><img src="assets/img/hero.png" alt="" /></div>
          </div>
''', '''
            tl.to(el(".p-bg"), { autoAlpha: 0, duration: 0.6 }, 0.9);
            tl.fromTo(el(".content"), { scale: 1 }, { scale: 1.035, duration: 7, ease: "none" }, 0);
            tl.fromTo(el(".wl"), { autoAlpha: 0, x: -60 }, { autoAlpha: 1, x: 0, duration: 0.7, ease: "power3.out" }, 0.3);
            var ls = splitLetters(el(".p-title"), "p-ch");
            ls.forEach(function (c, i) {
              tl.fromTo(c, { autoAlpha: 0, y: 70, filter: "blur(10px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out" }, 0.5 + i * 0.022);
            });
            tl.fromTo(q(".p-check"), { autoAlpha: 0, x: -50 }, { autoAlpha: 1, x: 0, duration: 0.6, stagger: 0.25, ease: "back.out(1.6)" }, 2.6);
            tl.fromTo(el(".p-shot"), { autoAlpha: 0, x: 220, rotationY: -35, transformPerspective: 1400, transformOrigin: "0% 50%" }, { autoAlpha: 1, x: 0, rotationY: 0, duration: 1.0, ease: "power3.out" }, 0.9);
            tl.to(el(".p-shot"), { y: -14, duration: 1.8, ease: "sine.inOut", yoyo: true, repeat: 2 }, 2.4);
            tl.fromTo(el(".p-shot img"), { objectPosition: "0px 0px" }, { objectPosition: "0px -40px", duration: 5, ease: "none" }, 1.5);
'''))

# ---------- S3 · resultados ----------
cards3 = [
  ("IA aplicada a tu trabajo o negocio", "ChatGPT · Gemini · Perplexity · NotebookLM", '<path d="M9 3a3 3 0 00-3 3v1a3 3 0 00-2 5 3 3 0 002 5 3 3 0 003 3h1V3zM15 3a3 3 0 013 3v1a3 3 0 012 5 3 3 0 01-2 5 3 3 0 01-3 3h-1V3z"/>'),
  ("Tu MVP publicado", "Lovable · v0", '<path d="M5 19l3-1 8-8a3 3 0 00-4-4l-8 8-1 3zM14 6l4 4M15 13l5 5"/>'),
  ("Automatizaciones funcionando", "Make · Webhooks", '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/><path d="M10 6.5h4a3 3 0 013 3V14"/>'),
  ("IA dentro de tus automatizaciones", "n8n · Claude · APIs", '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5V12M12 12l-6 5M12 12l6 5"/>'),
]
c3 = ''.join(f'<div class="card r-card"><div class="r-ico"><svg viewBox="0 0 24 24">{ic}</svg></div><div class="r-t">{t}</div><div class="r-tools">{tools}</div></div>' for t, tools, ic in cards3)
w('scene-resultados.html', build('scene-resultados', 'Escena 3: resultados', 7.5, '''
          .r-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 50px; }
          .r-title { font-size: 100px; text-align: center; white-space: nowrap; }
          .r-grid { display: grid; grid-template-columns: 820px 820px; gap: 40px; }
          .r-card { padding: 36px 44px 38px; border-radius: 36px; display: flex; flex-direction: column; gap: 16px; }
          .r-ico { width: 84px; height: 84px; border-radius: 26px; background: #efe3ff; display: flex; align-items: center; justify-content: center; color: #5421a6; }
          .r-ico svg { display: block; width: 46px; height: 46px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
          .r-t { font-family: var(--font-display, system-ui, sans-serif); font-size: 48px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.1; }
          .r-tools { align-self: flex-start; padding: 8px 22px; border-radius: 999px; background: #f4eeff; color: #5421a6; font-size: 30px; font-weight: 700; }
''', f'''
          <div class="content r-content">
            <h2 class="disp r-title">En 8 semanas vas a <span class="grad">lograr esto</span></h2>
            <div class="r-grid">{c3}</div>
          </div>
''', '''
            tl.fromTo(el(".r-content"), { scale: 1 }, { scale: 1.03, duration: 7.5, ease: "none" }, 0);
            var ls = splitLetters(el(".r-title"), "r-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, scale: 0.2, y: 40 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2.2)" }, 0.2 + i * 0.03); });
            var cs = q(".r-card");
            for (var i = 0; i < cs.length; i++) {
              tl.fromTo(cs[i], { autoAlpha: 0, y: 130, rotationX: -50, transformPerspective: 1200, transformOrigin: "50% 100%" }, { autoAlpha: 1, y: 0, rotationX: 0, duration: 0.8, ease: "back.out(1.4)" }, 0.9 + i * 0.5);
              tl.to(cs[i], { y: -10, duration: 1.5 + i * 0.2, ease: "sine.inOut", yoyo: true, repeat: 2 }, 2.6 + i * 0.1);
              tl.fromTo(cs[i].querySelector(".r-tools"), { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.5, ease: "power3.out" }, 1.5 + i * 0.5);
            }
'''))

# ---------- S4 · para quién ----------
cards4 = [("Emprendedoras", "Que quieren construir sin depender de terceros", '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 4-7 8-7s7 2 8 7"/>'),
          ("Profesionales", "Que buscan automatizar tareas de su día a día", '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
          ("Freelancers y consultoras", "Que quieren ofrecer más valor con IA", '<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c1-4 3-6 7-6s6 2 7 6M16 14c3 0 5 2 6 5"/>'),
          ("Sin experiencia técnica", "Todo el programa es 100% no code", '<path d="M8 8l-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>')]
c4 = ''.join(f'<div class="card a-card"><div class="a-ico"><svg viewBox="0 0 24 24">{ic}</svg></div><div class="a-t">{t}</div><div class="a-d">{d}</div></div>' for t, d, ic in cards4)
w('scene-paraquien.html', build('scene-paraquien', 'Escena 4: para quién', 6.5, '''
          .a-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 70px; }
          .a-title { font-size: 112px; text-align: center; white-space: nowrap; }
          .a-row { display: flex; gap: 36px; }
          .a-card { width: 410px; height: 470px; padding: 40px 38px; display: flex; flex-direction: column; gap: 22px; border-radius: 40px; }
          .a-ico { width: 96px; height: 96px; border-radius: 30px; background: linear-gradient(135deg, #5421a6, #d74ac5); display: flex; align-items: center; justify-content: center; color: #fff; }
          .a-ico svg { display: block; width: 52px; height: 52px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
          .a-t { font-family: var(--font-display, system-ui, sans-serif); font-size: 44px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.08; }
          .a-d { font-size: 36px; font-weight: 500; line-height: 1.3; color: #4b4560; }
''', f'''
          <div class="content a-content">
            <h2 class="disp a-title">¿Para quién <span class="grad">es?</span></h2>
            <div class="a-row">{c4}</div>
          </div>
''', '''
            tl.fromTo(el(".a-content"), { scale: 1 }, { scale: 1.03, duration: 6.5, ease: "none" }, 0);
            var ls = splitLetters(el(".a-title"), "a-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, rotationX: -90, y: 30, transformPerspective: 800 }, { autoAlpha: 1, rotationX: 0, y: 0, duration: 0.6, ease: "back.out(1.7)" }, 0.15 + i * 0.045); });
            var cs = q(".a-card");
            for (var i = 0; i < cs.length; i++) {
              tl.fromTo(cs[i], { autoAlpha: 0, rotationY: 80, x: 60, transformPerspective: 1200, transformOrigin: "0% 50%" }, { autoAlpha: 1, rotationY: 0, x: 0, duration: 0.8, ease: "back.out(1.3)" }, 0.8 + i * 0.35);
              tl.to(cs[i], { y: -12, duration: 1.4 + i * 0.15, ease: "sine.inOut", yoyo: true, repeat: 2 }, 2.4 + i * 0.1);
            }
'''))

# ---------- S5 · cómo ----------
w('scene-programa-detalle.html', build('scene-programa-detalle', 'Escena 5: módulos y sesiones', 6.5, '''
          .m-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 46px; }
          .m-title { font-size: 104px; white-space: nowrap; }
          .m-row { display: flex; gap: 44px; }
          .m-card { width: 830px; padding: 40px 48px 44px; border-radius: 40px; display: flex; flex-direction: column; gap: 14px; }
          .m-tag { align-self: flex-start; padding: 8px 24px; border-radius: 999px; background: #efe3ff; color: #5421a6; font-size: 32px; font-weight: 700; }
          .m-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 62px; font-weight: 700; letter-spacing: -0.025em; line-height: 1.05; }
          .m-when { font-size: 38px; font-weight: 500; color: #4b4560; }
          .m-big { display: flex; align-items: center; gap: 26px; }
          .m-num { font-family: var(--font-display, system-ui, sans-serif); font-size: 150px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
          .m-lbl { font-size: 46px; font-weight: 700; line-height: 1.15; }
          .m-pills { display: flex; gap: 16px; }
          .m-pill { padding: 14px 30px; border-radius: 999px; background: #ffffff; box-shadow: 0 16px 34px rgba(60, 20, 120, 0.14); font-size: 36px; font-weight: 700; white-space: nowrap; }
''', '''
          <div class="content m-content">
            <h2 class="disp m-title">Dos módulos, <span class="grad">16 sesiones en vivo</span></h2>
            <div class="m-row">
              <div class="card m-card"><span class="m-tag">Módulo 1</span><div class="m-name">IA para No Técnicos</div><div class="m-when">Inicia el 7 de octubre · 4 semanas</div></div>
              <div class="card m-card"><span class="m-tag">Módulo 2</span><div class="m-name">Automatización No Code</div><div class="m-when">Inicia el 4 de noviembre · 4 semanas</div></div>
            </div>
            <div class="m-pills"><span class="m-pill">Miércoles y viernes · 6:30 p. m.</span><span class="m-pill">Grabaciones</span><span class="m-pill">Comunidad</span><span class="m-pill">Certificado digital</span></div>
          </div>
''', '''
            tl.fromTo(el(".m-content"), { scale: 1 }, { scale: 1.03, duration: 6.5, ease: "none" }, 0);
            var ls = splitLetters(el(".m-title"), "m-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: -80, rotation: (i % 2 ? 1 : -1) * 14 }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.55, ease: "bounce.out" }, 0.1 + i * 0.03); });
            var cs = q(".m-card");
            tl.fromTo(cs[0], { autoAlpha: 0, x: -260, rotationY: 30, transformPerspective: 1200 }, { autoAlpha: 1, x: 0, rotationY: 0, duration: 0.9, ease: "power3.out" }, 0.8);
            tl.fromTo(cs[1], { autoAlpha: 0, x: 260, rotationY: -30, transformPerspective: 1200 }, { autoAlpha: 1, x: 0, rotationY: 0, duration: 0.9, ease: "power3.out" }, 1.2);
            tl.fromTo(q(".m-pill"), { autoAlpha: 0, y: 40, scale: 0.8 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.55, stagger: 0.3, ease: "back.out(1.8)" }, 2.4);
            tl.to(cs, { y: -10, duration: 1.5, ease: "sine.inOut", yoyo: true, repeat: 2, stagger: 0.2 }, 2.8);
'''))

# ---------- S6 · facilitador ----------
w('scene-facilitador.html', build('scene-facilitador', 'Escena 6: facilitador', 6.5, '''
          .f-photo { position: absolute; left: 190px; top: 250px; width: 540px; height: 540px; border-radius: 64px; padding: 14px; background: linear-gradient(135deg, #7ff0d3, #7c3aed 55%, #d74ac5); box-shadow: 0 50px 90px rgba(60, 20, 120, 0.3); }
          .f-photo img { display: block; width: 512px; height: 512px; border-radius: 52px; object-fit: cover; }
          .f-text { position: absolute; left: 830px; top: 230px; width: 900px; display: flex; flex-direction: column; gap: 28px; }
          .f-title { font-size: 70px; }
          .f-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 88px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.02; }
          .f-role { font-size: 40px; font-weight: 500; line-height: 1.3; color: #4b4560; }
          .f-line { display: flex; align-items: center; gap: 20px; padding: 24px 34px; border-radius: 30px; background: #ffffff; box-shadow: 0 26px 54px rgba(60, 20, 120, 0.16); font-size: 44px; font-weight: 700; line-height: 1.2; }
          .f-line i { display: block; width: 18px; align-self: stretch; border-radius: 9px; background: linear-gradient(180deg, #5421a6, #d74ac5); flex: 0 0 18px; }
          .f-orb { position: absolute; left: 80px; top: 120px; width: 760px; height: 760px; border-radius: 50%; background: radial-gradient(circle, rgba(196,166,255,0.5), transparent 66%); }
''', '''
          <div class="f-orb" data-layout-allow-overflow="true"></div>
          <div class="f-photo"><img src="assets/img/jaime.png" alt="Jaime Fernández Chávez" /></div>
          <div class="f-text">
            <h2 class="disp f-title">Aprende de alguien que <span class="grad">lo aplica cada día</span></h2>
            <div class="f-name">Jaime Fernández Chávez</div>
            <div class="f-role">Ingeniero por la UNI · Lovable Ambassador · Cofundador de Warmi Ventures</div>
            <div class="f-line"><i></i>Enseña con proyectos reales, no con teoría.</div>
          </div>
''', '''
            tl.fromTo(el(".f-orb"), { scale: 0.7, autoAlpha: 0 }, { scale: 1.1, autoAlpha: 1, duration: 3, ease: "power2.out" }, 0);
            tl.fromTo(el(".f-photo"), { autoAlpha: 0, scale: 0.7, rotationY: 50, transformPerspective: 1200 }, { autoAlpha: 1, scale: 1, rotationY: 0, duration: 1.0, ease: "back.out(1.4)" }, 0.2);
            tl.to(el(".f-photo"), { y: -16, rotation: 1.2, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 2 }, 1.4);
            var ls = splitLetters(el(".f-title"), "f-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: "power3.out" }, 0.5 + i * 0.022); });
            tl.fromTo(el(".f-name"), { autoAlpha: 0, y: 40, filter: "blur(14px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.8, ease: "power3.out" }, 1.5);
            tl.fromTo(el(".f-role"), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out" }, 2.2);
            tl.fromTo(el(".f-line"), { autoAlpha: 0, x: 80 }, { autoAlpha: 1, x: 0, duration: 0.8, ease: "back.out(1.5)" }, 3.0);
'''))

# ---------- S7 · precio ----------
w('scene-precio.html', build('scene-precio', 'Escena 7: precio', 5.7, '''
          .e-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; }
          .e-tag { font-size: 38px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #5421a6; }
          .e-old { font-size: 44px; font-weight: 500; color: #4b4560; text-decoration: line-through; text-decoration-thickness: 4px; }
          .e-price { font-family: var(--font-display, system-ui, sans-serif); font-size: 330px; font-weight: 700; letter-spacing: -0.05em; line-height: 1; white-space: nowrap; color: #5421a6; }
          .e-usd { font-size: 46px; font-weight: 700; }
          .e-badge { margin-top: 18px; padding: 16px 48px; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #d74ac5); color: #ffffff; font-size: 54px; font-weight: 700; letter-spacing: 0.02em; box-shadow: 0 26px 54px rgba(84, 33, 166, 0.35); white-space: nowrap; }
          .e-pct { font-size: 40px; font-weight: 700; color: #4b4560; }
''', '''
          <div class="content e-content">
            <div class="e-tag">Pack completo · 8 semanas</div>
            <div class="e-old">Por separado: S/ 598</div>
            <div class="e-price"><span class="e-cur">S/ </span><span class="e-num">499</span></div>
            <div class="e-usd">USD 135 · pago único</div>
            <div class="e-badge">AHORRA S/ 99</div>
            <div class="e-pct">17 % menos que comprar los módulos por separado</div>
          </div>
''', '''
            tl.fromTo(el(".e-content"), { scale: 1 }, { scale: 1.04, duration: 5.5, ease: "none" }, 0);
            tl.fromTo(el(".e-tag"), { autoAlpha: 0, y: -30 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.2);
            tl.fromTo(el(".e-old"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 0.5);
            var obj = { v: 0 }; var num = el(".e-num");
            tl.fromTo(el(".e-price"), { autoAlpha: 0, scale: 0.6 }, { autoAlpha: 1, scale: 1, duration: 0.7, ease: "back.out(1.6)" }, 0.6);
            tl.to(obj, { v: 499, duration: 1.4, ease: "power3.out", onUpdate: function () { num.textContent = String(Math.round(obj.v)); } }, 0.7);
            tl.fromTo(el(".e-usd"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 1.9);
            tl.fromTo(el(".e-badge"), { autoAlpha: 0, scale: 0.3, rotation: -8 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.8, ease: "elastic.out(1, 0.5)" }, 2.1);
            tl.fromTo(el(".e-pct"), { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.6 }, 2.8);
            tl.to(el(".e-badge"), { scale: 1.06, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 3 }, 3.2);
'''))

# ---------- S8 · cierre ----------
w('scene-cierre.html', build('scene-cierre', 'Escena 8: cierre', 9.0, LOGO_CSS + '''
          .z-bg { position: absolute; inset: 0; background: radial-gradient(circle at 20% 15%, #7c3aed 0%, transparent 52%), radial-gradient(circle at 85% 90%, #d74ac5 0%, transparent 50%), linear-gradient(160deg, #1d0a45 0%, #3b1285 100%); }
          .z-content { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 44px; color: #ffffff; }
          .z-title { font-size: 112px; text-align: center; color: #ffffff; }
          .z-title .z-acc { color: #ffa8ec; }
          .z-btns { display: flex; gap: 28px; align-items: center; }
          .z-btn { display: flex; align-items: center; justify-content: center; height: 108px; padding: 0 56px; border-radius: 999px; font-size: 44px; font-weight: 700; white-space: nowrap; }
          .z-b1 { background: linear-gradient(90deg, #5421a6, #c42fa8); color: #ffffff; box-shadow: 0 26px 60px rgba(215, 74, 197, 0.45); border: 3px solid rgba(255,255,255,0.35); }
          .z-b2 { background: rgba(255, 255, 255, 0.14); color: #ffffff; border: 3px solid rgba(255, 255, 255, 0.55); }
          .z-info { font-size: 38px; font-weight: 500; color: #ece2ff; text-align: center; line-height: 1.35; }
          .z-info b { color: #ffffff; }
          .z-logo { position: absolute; left: 0; right: 0; top: 70px; justify-content: center; color: #ffffff; }
          .z-logo .wl-by { color: #d9c8ff; }
          .z-ring { position: absolute; left: 810px; top: 300px; width: 300px; height: 300px; border-radius: 50%; border: 5px solid #ffa8ec; opacity: 0; }
''', '''
          <div class="z-bg"></div>
          <div class="z-ring zr0" data-layout-allow-overflow="true"></div>
          <div class="z-ring zr1" data-layout-allow-overflow="true"></div>
          <div class="wl z-logo">''' + logo('8') + '''<span class="wl-name">Warmi Academy</span><span class="wl-by">by Warmi Ventures</span></div>
          <div class="content z-content">
            <h1 class="disp z-title">¿Listo para pasar de usar IA a <span class="z-acc">construir con ella?</span></h1>
            <div class="z-btns"><div class="z-btn z-b1">Ver opciones e inscribirme →</div><div class="z-btn z-b2">Hablar por WhatsApp</div></div>
            <div class="z-info"><b>2.ª edición · Inicio: 7 de octubre de 2026</b><br />6:30 p. m. Perú, Colombia, Ecuador</div>
          </div>
''', '''
            tl.fromTo(el(".z-content"), { scale: 1 }, { scale: 1.03, duration: 9, ease: "none" }, 0);
            tl.fromTo(el(".z-bg"), { scale: 1.15 }, { scale: 1, duration: 3, ease: "power2.out" }, 0);
            tl.fromTo(el(".z-logo"), { autoAlpha: 0, y: -40 }, { autoAlpha: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.3);
            var ls = splitLetters(el(".z-title"), "z-ch");
            ls.forEach(function (c, i) { tl.fromTo(c, { autoAlpha: 0, y: 90, filter: "blur(12px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out" }, 0.4 + i * 0.025); });
            tl.fromTo(q(".z-btn"), { autoAlpha: 0, y: 70, scale: 0.7 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, stagger: 0.2, ease: "elastic.out(1, 0.55)" }, 2.6);
            tl.fromTo(el(".z-info"), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out" }, 3.5);
            var rings = q(".z-ring");
            for (var i = 0; i < rings.length; i++) tl.fromTo(rings[i], { scale: 0.3, autoAlpha: 0.8 }, { scale: 4.2, autoAlpha: 0, duration: 1.3, ease: "power2.out" }, 2.6 + i * 0.25);
            tl.to(el(".z-b1"), { scale: 1.045, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: 3 }, 4.0);
'''))
print("scenes ok")
