const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const [,, url, mode] = process.argv;   // mode: loaded | early
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  await p.waitForFunction('window.__ready === true', { timeout: 60000 });
  if (mode === 'loaded') await p.waitForFunction('window.__framesLoaded === true', { timeout: 120000 });
  const r = await p.evaluate(() => new Promise(res => {
    const film = document.getElementById('film'); const end = film.offsetTop + film.offsetHeight - innerHeight;
    const hits = []; const d = []; let last = performance.now(), y = 0;
    const tick = () => { const now = performance.now(), dt = now - last; last = now; d.push(dt); if (dt > 50) hits.push([Math.round(dt), y]); y += 13; scrollTo(0, Math.min(y, end)); if (y < end) requestAnimationFrame(tick); else { d.sort((a, b) => a - b); res({ p95: +d[Math.floor(d.length * .95)].toFixed(1), max: +d[d.length - 1].toFixed(1), over50: hits.length, hits: hits.slice(0, 8), loaded: !!window.__framesLoaded }); } };
    requestAnimationFrame(tick);
  }));
  console.log(mode, JSON.stringify(r)); await b.close();
})();
