const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new' });
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.goto('http://localhost:4780/planC/', { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.querySelector('.dial').scrollIntoView({ block: 'center' }));
  await p.evaluate(() => { const i = document.getElementById('day'); i.value = 250; i.dispatchEvent(new Event('input')); });
  await new Promise(r => setTimeout(r, 700));
  const el = await p.$('.dial'); await el.screenshot({ path: 'film/shots/c_dial10.png' });
  await p.evaluate(() => [...document.querySelectorAll('#stages button')][5].click());
  console.log(await p.evaluate(() => ({ out: document.getElementById('dayOut').textContent, stage: document.getElementById('stageName').textContent, v: document.getElementById('day').value })));
  await p.setViewport({ width: 390, height: 844 }); await p.evaluate(() => document.querySelector('.dial').scrollIntoView({ block: 'start' })); await new Promise(r => setTimeout(r, 500));
  await p.screenshot({ path: 'film/shots/c_dial_phone.png' });
  await b.close();
})();
