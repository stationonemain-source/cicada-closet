// node film/shoot_space.js <base>  — captures the nav at the top of the page and The Space section.
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const path = require('path');
const base = process.argv[2];
const out = path.join(__dirname);
const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  for (const d of [{ n: 'desktop', w: 1440, h: 900 }, { n: 'phone', w: 390, h: 844 }]) {
    await p.setViewport({ width: d.w, height: d.h });
    await p.goto(base + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await wait(2500);
    await p.screenshot({ path: path.join(out, `nav_${d.n}.png`), clip: { x: 0, y: 0, width: d.w, height: 220 } });
    const y = await p.evaluate(() => {
      const e = document.getElementById('studio');
      return Math.round(e.getBoundingClientRect().top + scrollY - 40);
    });
    await p.evaluate(v => scrollTo(0, v), y);
    await wait(1400);
    await p.screenshot({ path: path.join(out, `space_${d.n}.png`) });
  }
  console.log(errs.length ? 'ERRORS: ' + errs.slice(0, 2).join(' | ') : 'no page errors');
  await b.close();
})();
