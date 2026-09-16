const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const URL = process.argv[2] || 'http://localhost:4780/planB2/';
const W = +(process.argv[3] || 1440), H = +(process.argv[4] || 900), PRE = process.argv[5] || 'b2';
const OUT = 'C:/Users/Circl/.station/sites/cicada-closet/film/shots/';
const wait = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.setViewport({ width: W, height: H });
  await p.goto(URL + '?jump=0', { waitUntil: 'networkidle0', timeout: 60000 });
  await p.waitForFunction('window.__ready === true', { timeout: 45000 });
  const g = await p.evaluate(() => {
    const sts = ScrollTrigger.getAll().filter(s => s.pin);
    const run = document.getElementById('work'); const plates = [...document.querySelectorAll('.plate')];
    const desk = sts.find(s => s.trigger.id === 'desk'), r = sts.find(s => s.trigger.id === 'work');
    return { desk: desk && [desk.start, desk.end], run: r && [r.start, r.end], trackW: document.getElementById('track').scrollWidth, plates: plates.map(x => x.offsetLeft), doc: document.documentElement.scrollHeight };
  });
  console.log(JSON.stringify(g));
  const shots = [];
  if (g.desk) { const [s, e] = g.desk; shots.push(['desk0', 0], ['cover', s + (e - s) * 0.2], ['title', s + (e - s) * 0.5], ['zoom', s + (e - s) * 0.78]); }
  if (g.run) {
    const [s, e] = g.run, span = g.trackW - W;
    const at = (plateLeft, frac) => s + ((plateLeft - W * frac) / span) * (e - s);   // plate left edge at frac of viewport
    shots.push(['plate1-draw', at(g.plates[0], 0.55)], ['plate1-open', at(g.plates[0], 0.08)], ['plate3-open', at(g.plates[2], 0.0)], ['plate7', at(g.plates[6], 0.0)]);
  }
  for (const [name, y] of shots) {
    await p.goto(URL + '?jump=' + Math.round(y), { waitUntil: 'networkidle0' });
    await p.waitForFunction('window.__ready === true', { timeout: 45000 }); await wait(700);
    await p.screenshot({ path: OUT + PRE + '_' + name + '.png' });
    console.log('shot', name, Math.round(y), await p.evaluate(() => document.getElementById('nav').dataset.mode));
  }
  console.log('errors', JSON.stringify(errs));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
