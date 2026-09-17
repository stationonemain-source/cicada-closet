const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const URL = process.argv[2] || 'https://stationonemain-source.github.io/cicada-closet/film/'; const PRE = process.argv[3] || 'audit';
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage();
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await p.setViewport({ width: w, height: h });
    await p.goto(URL + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await p.waitForFunction('window.__ready === true', { timeout: 90000 });
    const ids = await p.evaluate(() => ['about','work','studio','artist','book','care'].map(id => { const e = document.getElementById(id) || document.querySelector('.intro'); return [id, Math.round(e.getBoundingClientRect().top + scrollY)]; }).concat([['footer', Math.round(document.querySelector('footer').getBoundingClientRect().top + scrollY)]]));
    console.log(tag, JSON.stringify(ids));
    for (const [id, y] of ids) {
      await p.evaluate(yy => { scrollTo(0, yy - 70); }, y); await new Promise(r => setTimeout(r, 900));
      await p.screenshot({ path: `film/shots/${PRE}_${tag}_${id}.png` });
    }
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
