const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage();
  for (const [w, h, tag] of [[1440, 900, 'desktop'], [390, 844, 'phone']]) {
    await p.setViewport({ width: w, height: h });
    await p.goto('http://localhost:4780/tier2/?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await p.waitForFunction('window.__ready === true', { timeout: 90000 });
    const start = await p.evaluate(() => Math.round(document.getElementById('about').getBoundingClientRect().top + scrollY) - 120);
    const end = await p.evaluate(() => document.documentElement.scrollHeight);
    const shots = [];
    for (let y = start; y < end; y += h - 60) {
      await p.evaluate(yy => scrollTo(0, yy), y); await new Promise(r => setTimeout(r, 700));
      const f = `film/shots/full_${tag}_${shots.length}.png`; await p.screenshot({ path: f }); shots.push(f);
      if (y + h >= end) break;
    }
    console.log(tag, shots.length);
  }
  await b.close();
})();
