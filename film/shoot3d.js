// node film/shoot3d.js <url> <outdir>
// Captures the 3D hero at several points of the push, on phone and desktop, and stitches
// each into a contact sheet. Drives the scene by calling __hero3d.frame(p) directly, which
// renders synchronously -- so it does not depend on scroll easing settling.
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');

const [url, outDir] = process.argv.slice(2);
const STEPS = [0, 0.22, 0.42, 0.60, 0.76, 0.92];
const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
  });
  const p = await b.newPage();
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

  for (const dev of [{ n: 'phone', w: 390, h: 844 }, { n: 'desktop', w: 1440, h: 900 }]) {
    await p.setViewport({ width: dev.w, height: dev.h, deviceScaleFactor: 1 });
    await p.goto(url + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await p.waitForFunction('window.__hero3d && window.__hero3d.isReady()', { timeout: 60000 }).catch(() => {});
    await wait(1500);
    for (let i = 0; i < STEPS.length; i++) {
      // Scroll to the real position and let the page's own loop render it. Calling
      // __hero3d.frame() directly is pointless here: the page's rAF redraws at the actual
      // scroll position on the very next tick, so every capture came back identical.
      await p.evaluate((v) => {
        const film = document.getElementById('film');
        scrollTo(0, Math.round((film.offsetHeight - innerHeight) * v));
      }, STEPS[i]);
      await wait(420);
      await p.screenshot({ path: path.join(outDir, `${dev.n}_${i}.png`) });
    }
    console.log(dev.n, 'captured', STEPS.length, 'frames');
  }
  console.log(errors.length ? 'PAGE ERRORS: ' + errors.slice(0, 4).join(' | ') : 'no page errors');
  await b.close();
})();
