import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'compositions', 'tour.html')
K = 0.9; WL = 240; WT = 90
# hold start times (output timeline) and durations
STOPS = {'A': 0.0, 'B': 5.4, 'C': 11.2, 'D': 16.5, 'E': 21.8, 'F': 27.6, 'G': 33.9}
HOLD_END = {'A': 4.6, 'B': 10.4, 'C': 15.7, 'D': 21.0, 'E': 26.8, 'F': 33.1, 'G': 37.0}
# spotlights: (stop, offset, duration, (x0,y0,x1,y1) in source px, badge text or None, tag text or None)
SPOTS = [
 ('A', 0.7, 1.7, (205, 128, 842, 335), None, 'automatiza tu trabajo'),
 ('A', 2.5, 1.9, (205, 436, 750, 534), '✓', None),
 ('B', 0.5, 1.0, (288, 239, 868, 487), '1', None),
 ('B', 1.5, 1.0, (883, 239, 1463, 487), '2', None),
 ('B', 2.5, 1.0, (288, 503, 868, 751), '3', None),
 ('B', 3.5, 1.4, (883, 503, 1463, 751), '4', None),
 ('C', 0.3, 0.9, (288, 386, 570, 618), '1', None),
 ('C', 1.2, 0.9, (585, 386, 868, 618), '2', None),
 ('C', 2.1, 0.9, (883, 386, 1165, 618), '3', None),
 ('C', 3.0, 1.5, (1181, 386, 1463, 618), '4', None),
 ('D', 0.5, 3.6, (366, 378, 1386, 700), None, None),
 ('E', 0.5, 1.9, (212, 140, 864, 492), '1', None),
 ('E', 2.5, 2.3, (887, 140, 1539, 610), '2', None),
 ('F', 0.4, 2.0, (640, 196, 1072, 470), None, None),
 ('F', 2.6, 2.2, (604, 514, 1146, 842), None, None),
 ('G', 0.4, 2.2, (442, 82, 1310, 398), None, None),
]
CAPS = {
 'A': 'Programa integral de IA + automatización no code',
 'B': '4 resultados concretos en 8 semanas',
 'C': 'Para emprendedoras, profesionales y consultoras',
 'D': 'Aprende de quien lo aplica cada día',
 'E': 'Dos módulos · 16 sesiones en vivo',
 'F': 'Pack completo · pago único · ahorra S/ 99',
 'G': '2.ª edición · inicia el 7 de octubre',
}
def spot_html(i, s):
    stop, off, dur, (x0, y0, x1, y1), badge, tag = s
    h = '<div class="spot sp%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (i, x0, y0, x1 - x0, y1 - y0)
    if badge:
        h += '<div class="badge bd%d" style="left:%dpx;top:%dpx">%s</div>' % (i, x0 - 26, y0 - 26, badge)
    return h
spots = '\n            '.join(spot_html(i, s) for i, s in enumerate(SPOTS))
caps = ''.join('<div class="cap cp%s">%s</div>' % (k, v) for k, v in CAPS.items())
data = {'K': K, 'WL': WL, 'WT': WT, 'stops': STOPS, 'holdEnd': HOLD_END, 'spots': [dict(stop=s[0], off=s[1], dur=s[2], r=list(s[3])) for s in SPOTS]}
html = '''<!doctype html>
<html lang="es">
  <head><meta charset="UTF-8" /><title>Recorrido con motion graphics</title></head>
  <body>
    <template>
      <div id="root" data-composition-id="tour" data-width="1920" data-height="1080" data-duration="40" data-fps="30">
        <style>
          #root { position: absolute; inset: 0; overflow: hidden; font-family: var(--font-body, system-ui, sans-serif); color: #170b2e; }
          #tour-clip { position: absolute; inset: 0; }
          .cam { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; }
          .win { position: absolute; left: 240px; top: 90px; width: 1440px; height: 860px; border-radius: 30px; overflow: hidden; background: #ffffff; box-shadow: 0 60px 120px rgba(60, 20, 120, 0.32), 0 14px 30px rgba(60, 20, 120, 0.14); }
          .stage { position: absolute; left: 0; top: 0; width: 1600px; height: 956px; transform-origin: 0 0; transform: scale(0.9); }
          .stage video { position: absolute; left: 0; top: 0; width: 1600px; height: 956px; display: block; }
          .spot { position: absolute; border-radius: 26px; border: 6px solid #d74ac5; box-shadow: 0 0 0 3000px rgba(23, 11, 46, 0.55), 0 0 40px rgba(215, 74, 197, 0.6); opacity: 0; }
          .rolefix { position: absolute; left: 612px; top: 457px; width: 700px; height: 36px; background: #ffffff; color: #4b4560; font-size: 22px; font-weight: 500; line-height: 36px; padding-left: 4px; opacity: 0; }
          .badge { position: absolute; width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #5421a6, #d74ac5); color: #ffffff; font-family: var(--font-display, system-ui, sans-serif); font-size: 42px; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 24px rgba(84, 33, 166, 0.5); opacity: 0; }
          .brand { position: absolute; left: 60px; top: 14px; display: flex; align-items: center; gap: 14px; padding: 6px 28px 6px 10px; border-radius: 999px; background: #ffffff; box-shadow: 0 10px 28px rgba(60, 20, 120, 0.2); }
          .wl-badge { display: block; width: 58px; height: 58px; }
          .wl-name { font-family: var(--font-display, system-ui, sans-serif); font-size: 40px; font-weight: 700; letter-spacing: -0.02em; }
          .tag2 { position: absolute; right: 60px; top: 20px; box-shadow: 0 10px 28px rgba(60, 20, 120, 0.2); padding: 10px 26px; border-radius: 999px; background: #efe3ff; color: #5421a6; font-size: 30px; font-weight: 700; }
          .caps { position: absolute; left: 0; right: 0; top: 968px; height: 90px; }
          .cap { position: absolute; left: 50%; top: 0; transform: translateX(-50%); padding: 14px 44px; border-radius: 999px; background: #1d0a45; color: #ffffff; font-family: var(--font-display, system-ui, sans-serif); font-size: 44px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; box-shadow: 0 20px 44px rgba(29, 10, 69, 0.4); opacity: 0; }
          .lt { position: absolute; left: 90px; top: 790px; padding: 26px 40px; border-radius: 28px; background: #ffffff; box-shadow: 0 30px 70px rgba(60, 20, 120, 0.35); border-left: 14px solid #7c3aed; opacity: 0; }
          .lt-n { font-family: var(--font-display, system-ui, sans-serif); font-size: 58px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.05; }
          .lt-r { font-size: 36px; font-weight: 500; color: #4b4560; margin-top: 6px; }
          .conf { position: absolute; width: 22px; height: 22px; border-radius: 50%; opacity: 0; }
          .end { position: absolute; inset: 0; background: radial-gradient(circle at 20% 15%, #7c3aed 0%, transparent 52%), radial-gradient(circle at 85% 90%, #d74ac5 0%, transparent 50%), linear-gradient(160deg, #1d0a45 0%, #3b1285 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 30px; color: #ffffff; opacity: 0; }
          .end .wl-badge { width: 96px; height: 96px; }
          .end .wl-name { font-size: 64px; color: #ffffff; }
          .end-logo { display: flex; align-items: center; gap: 22px; }
          .end-t { font-family: var(--font-display, system-ui, sans-serif); font-size: 120px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.02; text-align: center; white-space: nowrap; }
          .end-t i { font-style: normal; color: #ffa8ec; }
          .end-s { font-size: 40px; font-weight: 500; color: #ece2ff; text-align: center; line-height: 1.35; }
          .end-b { height: 104px; padding: 0 56px; display: flex; align-items: center; border-radius: 999px; background: linear-gradient(90deg, #5421a6, #c42fa8); border: 3px solid rgba(255, 255, 255, 0.4); font-size: 44px; font-weight: 700; box-shadow: 0 26px 60px rgba(215, 74, 197, 0.45); white-space: nowrap; }
        </style>

        <div id="tour-clip">
          <div class="cam">
            <div class="win">
              <div class="stage">
                <video id="recorrido-video" class="clip" src="assets/video/recorrido.mp4" data-start="0" data-duration="40" data-track-index="0" muted playsinline></video>
                <div class="rolefix">Director de Scaly AI · Ingeniero por la UNI</div>
                SPOTS
              </div>
            </div>
          </div>
          <div class="brand"><svg class="wl-badge" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="TG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5421a6"/><stop offset="1" stop-color="#d74ac5"/></linearGradient></defs><circle cx="24" cy="24" r="24" fill="url(#TG)"/><path d="M24 11l2.6 8.4L35 22l-8.4 2.6L24 33l-2.6-8.4L13 22l8.4-2.6z" fill="#fff"/><path d="M35 29l1.1 3.4 3.4 1.1-3.4 1.1L35 38l-1.1-3.4-3.4-1.1 3.4-1.1z" fill="#fff"/></svg><span class="wl-name">Warmi Academy</span></div>
          <div class="tag2">2.ª edición</div>
          <div class="lt"><div class="lt-n">Jaime Fernández Chávez</div><div class="lt-r">Director de Scaly AI</div></div>
          <div class="caps">CAPS</div>
          <div class="end">
            <div class="end-logo"><svg class="wl-badge" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="TG2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5421a6"/><stop offset="1" stop-color="#d74ac5"/></linearGradient></defs><circle cx="24" cy="24" r="24" fill="url(#TG2)"/><path d="M24 11l2.6 8.4L35 22l-8.4 2.6L24 33l-2.6-8.4L13 22l8.4-2.6z" fill="#fff"/><path d="M35 29l1.1 3.4 3.4 1.1-3.4 1.1L35 38l-1.1-3.4-3.4-1.1 3.4-1.1z" fill="#fff"/></svg><span class="wl-name">Warmi Academy</span></div>
            <div class="end-t">Empieza el <i>7 de octubre</i></div>
            <div class="end-s">6:30 p. m. Perú, Colombia, Ecuador<br />warmi.ventures@gmail.com</div>
            <div class="end-b">Ver opciones e inscribirme →</div>
          </div>
        </div>

        <script>
          (function () {
            var D = DATA;
            var root = document.getElementById("root");
            var q = function (s) { return root.querySelectorAll(s); };
            var el = function (s) { return root.querySelector(s); };
            var tl = gsap.timeline({ paused: true });
            var K = D.K, WL = D.WL, WT = D.WT;
            // focus the camera on a source-pixel rectangle: scale to fit, centre it a little above the middle
            var focus = function (r, maxS) {
              var w = (r[2] - r[0]) * K, h = (r[3] - r[1]) * K;
              var cx = WL + ((r[0] + r[2]) / 2) * K, cy = WT + ((r[1] + r[3]) / 2) * K;
              var S = Math.min(1920 * 0.78 / w, 760 / h, maxS || 1.9);
              S = Math.max(1.12, S);
              return { scale: S, x: 960 - cx * S, y: 480 - cy * S };
            };
            var cam = el(".cam");
            tl.set(cam, { x: 0, y: 0, scale: 1 }, 0);

            // entrance of the whole window
            tl.fromTo(el(".win"), { autoAlpha: 0, y: 90, rotationX: 14, scale: 0.9, transformPerspective: 1600 }, { autoAlpha: 1, y: 0, rotationX: 0, scale: 1, duration: 0.9, ease: "power3.out" }, 0);
            tl.fromTo(el(".brand"), { autoAlpha: 0, x: -40 }, { autoAlpha: 1, x: 0, duration: 0.7, ease: "power3.out" }, 0.3);
            tl.fromTo(el(".tag2"), { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.7, ease: "power3.out" }, 0.4);

            // captions: one per stop, slide up / out
            Object.keys(D.stops).forEach(function (k) {
              var c = el(".cp" + k);
              var t0 = D.stops[k] + (k === "A" ? 0.5 : 0.3), t1 = D.holdEnd[k] - 0.2;
              tl.fromTo(c, { autoAlpha: 0, y: 40, xPercent: -50, scale: 0.9 }, { autoAlpha: 1, y: 0, xPercent: -50, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, t0);
              tl.to(c, { autoAlpha: 0, y: -24, xPercent: -50, duration: 0.3, ease: "power2.in" }, t1);
            });

            // spotlights + badges + camera moves
            var lastCamEnd = {};
            D.spots.forEach(function (s, i) {
              var t = D.stops[s.stop] + s.off, sp = el(".sp" + i), bd = el(".bd" + i);
              tl.fromTo(sp, { autoAlpha: 0, scale: 1.06, transformOrigin: "50% 50%" }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "power3.out" }, t);
              tl.to(sp, { autoAlpha: 0, duration: 0.3 }, t + s.dur - 0.05);
              if (bd) {
                tl.fromTo(bd, { autoAlpha: 0, scale: 0.2 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(2.6)" }, t + 0.1);
                tl.to(bd, { autoAlpha: 0, duration: 0.3 }, t + s.dur - 0.05);
              }
              var f = focus(s.r, s.stop === "D" ? 1.45 : 1.7);
              tl.to(cam, { x: f.x, y: f.y, scale: f.scale, duration: 0.7, ease: "power3.inOut" }, t);
            });
            // camera returns to the full window before every scroll
            Object.keys(D.stops).forEach(function (k) {
              if (k === "G") return;
              tl.to(cam, { x: 0, y: 0, scale: 1, duration: 0.4, ease: "power2.inOut" }, D.holdEnd[k] - 0.4);
            });

            // the recording still shows the old role: cover that line while the card is frozen
            var rf = el(".rolefix");
            tl.fromTo(rf, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2 }, D.stops.D + 0.05);
            tl.to(rf, { autoAlpha: 0, duration: 0.15 }, D.holdEnd.D - 0.1);
            // lower third while the facilitator is on screen
            var lt = el(".lt");
            tl.fromTo(lt, { autoAlpha: 0, x: -120 }, { autoAlpha: 1, x: 0, duration: 0.7, ease: "power3.out" }, D.stops.D + 1.2);
            tl.to(lt, { autoAlpha: 0, x: 60, duration: 0.4, ease: "power2.in" }, D.holdEnd.D - 0.7);

            // price burst: confetti dots fly out of the price
            var seed = 11; var rnd = function () { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
            var stage = el(".stage");
            for (var c = 0; c < 26; c++) {
              var d = document.createElement("div");
              d.className = "conf";
              d.style.left = "874px"; d.style.top = "300px";
              d.style.background = ["#7c3aed", "#d74ac5", "#7ff0d3", "#ffffff"][c % 4];
              stage.appendChild(d);
              var a = (c / 26) * Math.PI * 2 + rnd() * 0.3, dist = 220 + rnd() * 260;
              tl.set(d, { autoAlpha: 0 }, 0);
              tl.fromTo(d, { x: 0, y: 0, autoAlpha: 1, scale: 1 }, { x: Math.cos(a) * dist, y: Math.sin(a) * dist * 0.7, autoAlpha: 0, scale: 0.3, duration: 1.0, ease: "power3.out", immediateRender: false }, D.stops.F + 0.9);
            }

            // closing card: circle reveal from the centre over the dimmed window
            var end = el(".end");
            tl.set(end, { autoAlpha: 1, clipPath: "circle(0% at 50% 50%)" }, 0);
            tl.to(end, { clipPath: "circle(150% at 50% 50%)", duration: 0.7, ease: "power2.inOut" }, 36.9);
            tl.fromTo(el(".end-logo"), { y: -50 }, { y: 0, duration: 0.6, ease: "power3.out" }, 37.2);
            tl.fromTo(el(".end-t"), { y: 70, scale: 0.92 }, { y: 0, scale: 1, duration: 0.7, ease: "power3.out" }, 37.4);
            tl.fromTo(el(".end-s"), { y: 30 }, { y: 0, duration: 0.6, ease: "power2.out" }, 38.0);
            tl.fromTo(el(".end-b"), { y: 60, scale: 0.7 }, { y: 0, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.55)" }, 38.3);
            tl.to(el(".end-b"), { scale: 1.04, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, 39.0);

            tl.seek(0);
            window.__timelines["tour"] = tl;
          })();
        </script>
      </div>
    </template>
  </body>
</html>
'''
html = html.replace('SPOTS', spots).replace('CAPS', caps).replace('DATA', json.dumps(data))
open(OUT, 'w').write(html)
print('ok')
