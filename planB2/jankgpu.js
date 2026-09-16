const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars','--enable-gpu','--ignore-gpu-blocklist','--use-angle=d3d11','--enable-gpu-rasterization','--enable-zero-copy'] });
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.goto(process.argv[2] || 'http://localhost:4780/planB2/', { waitUntil: 'networkidle0' });
  await p.waitForFunction('window.__ready === true', { timeout: 45000 });
  const r = await p.evaluate(() => new Promise(res => {
    const end = document.documentElement.scrollHeight - innerHeight; const hits = []; let last = performance.now(), y = 0;
    const desk = ScrollTrigger.getAll().find(s => s.pin && s.trigger.id === 'desk'), run = ScrollTrigger.getAll().find(s => s.pin && s.trigger.id === 'work');
    const tick = () => { const now = performance.now(), d = now - last; last = now; if (d > 40) hits.push([Math.round(d), y]); y += 13; scrollTo(0, Math.min(y, end)); if (y < end) requestAnimationFrame(tick); else res({ hits, desk: desk && [desk.start, desk.end], run: run && [run.start, run.end] }); };
    requestAnimationFrame(tick);
  }));
  console.log(JSON.stringify(r));
  await b.close();
})();
