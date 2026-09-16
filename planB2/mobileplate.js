const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); await p.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true });
  await p.goto('http://localhost:4780/planB2/?jump=0', { waitUntil: 'networkidle0' });
  await p.waitForFunction('window.__ready === true', { timeout: 45000 });
  const y = await p.evaluate(() => { const e = document.getElementById('plate-1'); return Math.round(e.getBoundingClientRect().top + scrollY); });
  for (const [n, off] of [['m2_plate1_mid', y - 250], ['m2_plate1_open', y + 330]]) {
    await p.goto('http://localhost:4780/planB2/?jump=' + off, { waitUntil: 'networkidle0' }); await p.waitForFunction('window.__ready === true'); await new Promise(r => setTimeout(r, 700));
    await p.screenshot({ path: 'film/shots/' + n + '.png' });
  }
  console.log('overflow-x', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth));
  await b.close();
})();
