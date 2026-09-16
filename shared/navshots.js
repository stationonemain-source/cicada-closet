// node navshots.js <url> <outprefix>  — desktop at top / mid / dark band, phone at top and with menu open
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const [url, out] = process.argv.slice(2);
const wait = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage();
  const errors = []; p.on('pageerror', e => errors.push(e.message)); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const go = async (w, h, y) => {
    await p.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
    await p.goto(url + (url.includes('?') ? '&' : '?') + 'jump=' + y, { waitUntil: 'networkidle0', timeout: 60000 });
    await p.waitForFunction('window.__ready === true', { timeout: 45000 }).catch(() => {});
    await wait(900); await p.evaluate(() => window.__nav && window.__nav.update()); await wait(500);
  };
  const state = () => p.evaluate(() => { const n = document.getElementById('nav'); return { mode: n.dataset.mode, current: [...document.querySelectorAll('.nav-links a[aria-current]')].map(a => a.textContent).join(','), color: getComputedStyle(n).color, bg: getComputedStyle(n).backgroundColor }; });
  await go(1440, 900, 0); console.log('desk top', JSON.stringify(await state())); await p.screenshot({ path: out + '_d0.png', clip: { x: 0, y: await p.evaluate(() => scrollY), width: 1440, height: 160 } });
  const ids = await p.evaluate(() => { const r = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null; }; return { work: r('#work'), artist: r('#artist') }; });
  await go(1440, 900, ids.work + 200); console.log('desk work', JSON.stringify(await state())); await p.screenshot({ path: out + '_d1.png', clip: { x: 0, y: await p.evaluate(() => scrollY), width: 1440, height: 160 } });
  await go(1440, 900, ids.artist + 100); console.log('desk artist', JSON.stringify(await state())); await p.screenshot({ path: out + '_d2.png', clip: { x: 0, y: await p.evaluate(() => scrollY), width: 1440, height: 160 } });
  await go(390, 844, 0); console.log('phone top', JSON.stringify(await state())); await p.screenshot({ path: out + '_m0.png' });
  await p.click('.nav-toggle'); await wait(400);
  console.log('phone menu', await p.evaluate(() => ({ hidden: document.getElementById('nav-sheet').hidden, expanded: document.querySelector('.nav-toggle').getAttribute('aria-expanded'), focus: document.activeElement.textContent.trim().slice(0, 20) })));
  await p.screenshot({ path: out + '_m1.png' });
  await p.evaluate(() => { const a = [...document.querySelectorAll('.nav-sheet nav a')].find(x => x.getAttribute('href') === '#book'); a.click(); });
  await wait(1800);
  console.log('phone after tap Booking', await p.evaluate(() => ({ hidden: document.getElementById('nav-sheet').hidden, bookTop: Math.round(document.querySelector('#book').getBoundingClientRect().top), mode: document.getElementById('nav').dataset.mode })));
  await p.screenshot({ path: out + '_m2.png' });
  console.log('errors', JSON.stringify(errors));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
