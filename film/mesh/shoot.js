// node film/mesh/shoot.js <base url of film/mesh/>  — renders the GLB from four angles + reports geometry
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const path = require('path');
const base = process.argv[2];
const VIEWS = [['front', 0, 0], ['three_quarter', 40, 20], ['profile', 88, 8], ['top', 0, 70]];
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage(); await p.setViewport({ width: 900, height: 700 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  for (const [name, yaw, pitch] of VIEWS) {
    await p.goto(`${base}view.html?yaw=${yaw}&pitch=${pitch}`, { waitUntil: 'networkidle0', timeout: 90000 });
    await p.waitForFunction('window.__ready === true', { timeout: 60000 }).catch(() => {});
    await new Promise(r => setTimeout(r, 400));
    await p.screenshot({ path: path.join(__dirname, `shot_${name}.png`) });
  }
  console.log(JSON.stringify(await p.evaluate(() => ({ info: window.__meshInfo, err: window.__err || null }))));
  if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 3).join(' | '));
  await b.close();
})();
