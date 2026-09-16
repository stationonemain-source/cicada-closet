const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const fs = require('fs');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://localhost:4780/planB2/', { waitUntil: 'networkidle0' });
  await p.waitForFunction('window.__ready === true', { timeout: 45000 });
  await p.evaluate(() => { scrollTo(0, 5950); }); await new Promise(r => setTimeout(r, 800));
  await p.tracing.start({ path: 'planB2/work/trace.json', categories: ['devtools.timeline', 'disabled-by-default-devtools.timeline', 'blink', 'cc', 'gpu', 'v8'] });
  await p.evaluate(() => new Promise(res => { let y = 5950; const t = () => { y += 13; scrollTo(0, y); if (y < 6300) requestAnimationFrame(t); else res(); }; requestAnimationFrame(t); }));
  await p.tracing.stop(); await b.close();
  const ev = JSON.parse(fs.readFileSync('planB2/work/trace.json', 'utf8')).traceEvents.filter(e => e.dur && e.dur > 20000);
  const agg = {};
  ev.forEach(e => { const k = e.name + (e.args && e.args.data && e.args.data.url ? ' ' + e.args.data.url.split('/').pop() : ''); agg[k] = Math.max(agg[k] || 0, Math.round(e.dur / 1000)); });
  console.log(Object.entries(agg).sort((a, b) => b[1] - a[1]).slice(0, 18).map(([k, v]) => v + 'ms ' + k).join('\n'));
})();
