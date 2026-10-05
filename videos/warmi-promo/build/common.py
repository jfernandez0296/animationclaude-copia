# Shared helpers to emit HyperFrames sub-composition files for the Warmi promo.
HELPERS = r'''
            var root = document.getElementById("root");
            var q = function (s) { return root.querySelectorAll(s); };
            var el = function (s) { return root.querySelector(s); };
            var tl = gsap.timeline({ paused: true });
            var rng = function (seed) {
              return function () {
                seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
                var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
                t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
                return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
              };
            };
            var splitLetters = function (host, cls) {
              var out = [];
              var walk = function (node) {
                Array.prototype.slice.call(node.childNodes).forEach(function (n) {
                  if (n.nodeType === 3) {
                    var frag = document.createDocumentFragment();
                    n.textContent.split(/(\s+)/).forEach(function (part) {
                      if (!part) return;
                      if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
                      var w = document.createElement("span");
                      w.style.display = "inline-block";
                      w.style.whiteSpace = "nowrap";
                      Array.prototype.slice.call(part).forEach(function (ch) {
                        var s = document.createElement("span");
                        s.className = cls;
                        s.style.display = "inline-block";
                        s.textContent = ch;
                        w.appendChild(s);
                        out.push(s);
                      });
                      frag.appendChild(w);
                    });
                    n.parentNode.replaceChild(frag, n);
                  } else if (n.nodeType === 1) { walk(n); }
                });
              };
              walk(host);
              Array.prototype.slice.call(host.querySelectorAll(".grad")).forEach(function (g) {
                var ls = g.querySelectorAll("." + cls);
                var n = ls.length;
                Array.prototype.forEach.call(ls, function (s, i) {
                  var t = n > 1 ? i / (n - 1) : 0;
                  var c = "rgb(" + Math.round(84 + 97 * t) + "," + Math.round(33 + 3 * t) + "," + Math.round(166 - 7 * t) + ")";
                  s.style.color = c;
                  s.style.webkitTextFillColor = c;
                  s.style.background = "none";
                });
                g.style.background = "none";
              });
              return out;
            };
'''

BASE_CSS = '''
          #root { position: absolute; inset: 0; overflow: hidden; color: var(--ink, #170b2e); font-family: var(--font-body, system-ui, sans-serif); }
          .scene { position: absolute; inset: 0; }
          .content { position: absolute; inset: 0; }
          h1, h2, h3, p { margin: 0; }
          .disp { font-family: var(--font-display, system-ui, sans-serif); font-weight: 700; letter-spacing: -0.03em; line-height: 1.04; }
          .grad { background: linear-gradient(90deg, #5421a6 0%, #7c3aed 45%, #b5249f 100%); -webkit-background-clip: text; background-clip: text; color: transparent; -webkit-text-fill-color: transparent; }
          .card { background: #ffffff; border-radius: 40px; box-shadow: 0 40px 80px rgba(60, 20, 120, 0.16), 0 10px 22px rgba(60, 20, 120, 0.08); }
          .eyebrow { display: inline-flex; align-items: center; gap: 14px; padding: 12px 28px; border-radius: 999px; background: #efe3ff; color: #5421a6; font-size: 32px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
'''

def build(sid, title, dur, css, body, js, bg_css=""):
    return f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>{title}</title>
  </head>
  <body>
    <template>
      <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{dur}" data-fps="30">
        <style>{BASE_CSS}{css}
        </style>

        <div id="{sid}-clip" class="clip scene" data-start="0" data-duration="{dur}" data-track-index="0">
{body}
        </div>

        <script>
          (function () {{{HELPERS}
{js}
            tl.seek(0);
            window.__timelines["{sid}"] = tl;
          }})();
        </script>
      </div>
    </template>
  </body>
</html>
'''

LOGO_SVG = '''<svg class="wl-badge" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="WG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5421a6"/><stop offset="1" stop-color="#d74ac5"/></linearGradient></defs><circle cx="24" cy="24" r="24" fill="url(#WG)"/><path d="M24 11l2.6 8.4L35 22l-8.4 2.6L24 33l-2.6-8.4L13 22l8.4-2.6z" fill="#fff"/><path d="M35 29l1.1 3.4 3.4 1.1-3.4 1.1L35 38l-1.1-3.4-3.4-1.1 3.4-1.1z" fill="#fff"/></svg>'''
