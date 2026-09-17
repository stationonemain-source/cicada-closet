const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.goto('https://stationonemain-source.github.io/cicada-closet/film/?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
  await p.waitForFunction('window.__ready === true', { timeout: 90000 });
  await p.evaluate(() => document.getElementById('studio').scrollIntoView());
  await p.waitForFunction(() => [...document.querySelectorAll('.studio .photos img')].every(i => i.complete && i.naturalWidth > 0), { timeout: 30000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 800));
  console.log(JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.studio .photos img')].map(i => ({ src: i.currentSrc.split('/').slice(-2).join('/'), loaded: i.complete && i.naturalWidth > 0, w: i.naturalWidth })))));
  await p.screenshot({ path: 'film/shots/live_studio_wait.png' });
  await b.close();
})();
