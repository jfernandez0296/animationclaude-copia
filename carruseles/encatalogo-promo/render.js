// Exporta cada slide del carrusel a PNG 1080×1350.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 2800 } });
  await p.goto('file://' + path.join(__dirname, 'carrusel.html'));
  await p.evaluate(() => document.fonts.ready);
  for (const id of ['slide-1', 'slide-2']) await p.locator('#' + id).screenshot({ path: path.join(__dirname, id + '.png') });
  await b.close();
})();
