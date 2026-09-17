const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage();
  for (const [w, h, name] of [[1440, 900, 'card_desk'], [390, 844, 'card_phone']]) {
    await p.setViewport({ width: w, height: h });
    await p.goto('http://localhost:4780/tier1/?jump=0', { waitUntil: 'networkidle0' });
    await p.waitForFunction('window.__ready === true', { timeout: 45000 }).catch(() => {});
    const el = await p.$('.info'); await el.scrollIntoView(); await new Promise(r => setTimeout(r, 1200));
    await el.screenshot({ path: 'film/shots/' + name + '.png' });
  }
  await b.close();
})();
