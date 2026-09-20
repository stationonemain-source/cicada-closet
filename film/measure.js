// node film/measure.js <url>  — transfer weight and frame cost for the hero, phone + desktop.
// Headless GL is software (swiftshader), so frame times are a RELATIVE signal only; the byte
// counts are exact.
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const url = process.argv[2];
const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
  });
  for (const dev of [{ n: 'phone', w: 390, h: 844, dpr: 2 }, { n: 'desktop', w: 1440, h: 900, dpr: 1 }]) {
    const p = await b.newPage();
    await p.setCacheEnabled(false);
    await p.setViewport({ width: dev.w, height: dev.h, deviceScaleFactor: dev.dpr });
    const seen = new Map();
    p.on('response', async (r) => {
      try {
        const len = (await r.buffer()).length;
        const u = r.url().split('/').pop().split('?')[0] || r.url();
        seen.set(u, (seen.get(u) || 0) + len);
      } catch (e) { /* redirects etc. */ }
    });
    const t0 = Date.now();
    await p.goto(url + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await p.waitForFunction('window.__hero3d && window.__hero3d.isReady()', { timeout: 60000 }).catch(() => {});
    const loadMs = Date.now() - t0;
    await wait(900);
    // what the visitor actually pays before anything moves
    const firstPaint = [...seen.values()].reduce((a, b) => a + b, 0);

    // frame cost across the push
    const fps = await p.evaluate(async () => {
      const film = document.getElementById('film');
      const max = film.offsetHeight - innerHeight;
      const d = [];
      let last = performance.now();
      for (let i = 0; i <= 40; i++) {
        scrollTo(0, Math.round(max * (i / 40)));
        await new Promise(r => requestAnimationFrame(r));
        const now = performance.now();
        if (i) d.push(now - last);
        last = now;
      }
      d.sort((a, b) => a - b);
      return { median: +d[Math.floor(d.length / 2)].toFixed(1), p95: +d[Math.floor(d.length * 0.95)].toFixed(1) };
    });

    const rows = [...seen.entries()].sort((a, b) => b[1] - a[1]);
    const total = rows.reduce((s, r) => s + r[1], 0);
    console.log(`
${dev.n}  FIRST PAINT ${(firstPaint / 1024).toFixed(0)} KB   after full push ${(total / 1024).toFixed(0)} KB   load ${loadMs} ms   frame median ${fps.median}ms p95 ${fps.p95}ms (software GL, relative only)`);
    for (const [u, n] of rows.slice(0, 6)) console.log(`   ${(n / 1024).toFixed(0).padStart(6)} KB  ${u}`);
    await p.close();
  }
  await b.close();
})();
