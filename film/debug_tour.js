// node film/debug_tour.js <url> — logs every play/pause/stall of the walkthrough with where it sat on screen.
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const url = process.argv[2];
const wait = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage();
  p.on('console', m => console.log('  console:', m.text()));
  p.on('pageerror', e => console.log('  pageerror:', e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(url + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
  await wait(1500);
  await p.evaluate(() => {
    const v = document.querySelector('.studio .tour'); const t0 = performance.now();
    for (const ev of ['play', 'playing', 'pause', 'waiting', 'stalled', 'ended', 'error'])
      v.addEventListener(ev, () => console.log(((performance.now() - t0) / 1000).toFixed(2) + 's ' + ev +
        ' t=' + v.currentTime.toFixed(2) + ' top=' + Math.round(v.getBoundingClientRect().top) + ' scrollY=' + Math.round(scrollY)));
    const e = document.getElementById('studio'); scrollTo(0, Math.round(e.getBoundingClientRect().top + scrollY - 40));
  });
  await wait(9000);
  console.log('end: scrollY=' + await p.evaluate(() => Math.round(scrollY)) + ' paused=' + await p.evaluate(() => document.querySelector('.studio .tour').paused));
  await b.close();
})();
