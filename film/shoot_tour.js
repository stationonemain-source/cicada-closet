// node film/shoot_tour.js <base>  — proves the walkthrough plays itself on scroll, and captures it.
// Checks the video is actually advancing, not merely present: a poster that never plays looks
// identical in a screenshot.
const puppeteer = require('C:/Users/Circl/.claude/skills/scroll-film-studio/node_modules/puppeteer-core');
const path = require('path');
const base = process.argv[2];
const out = __dirname;
const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--hide-scrollbars', '--use-gl=angle', '--use-angle=swiftshader',
           '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required']
  });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));

  for (const d of [{ n: 'desktop', w: 1440, h: 900 }, { n: 'phone', w: 390, h: 844 }]) {
    await p.setViewport({ width: d.w, height: d.h });
    await p.goto(base + '?jump=0', { waitUntil: 'networkidle0', timeout: 90000 });
    await wait(1500);

    const before = await p.evaluate(() => {
      const v = document.querySelector('.studio .tour');
      return v ? { paused: v.paused, t: v.currentTime } : null;
    });

    await p.evaluate(() => {
      const e = document.getElementById('studio');
      scrollTo(0, Math.round(e.getBoundingClientRect().top + scrollY - 40));
    });
    await wait(9000);                                   // let it load and run

    const after = await p.evaluate(() => {
      const v = document.querySelector('.studio .tour');
      return { paused: v.paused, t: v.currentTime, w: v.videoWidth, h: v.videoHeight,
               box: Math.round(v.getBoundingClientRect().width) + 'x' + Math.round(v.getBoundingClientRect().height) };
    });
    await p.screenshot({ path: path.join(out, `tour_${d.n}.png`) });

    // and that it stops once the visitor leaves it
    await p.evaluate(() => scrollTo(0, 0));
    await wait(1500);
    const away = await p.evaluate(() => document.querySelector('.studio .tour').paused);

    console.log(`${d.n}: before scroll paused=${before && before.paused} | after scroll paused=${after.paused} ` +
                `t=${after.t.toFixed(2)}s video=${after.w}x${after.h} box=${after.box} | paused when away=${away}`);
  }
  console.log(errs.length ? 'ERRORS: ' + errs.slice(0, 3).join(' | ') : 'no page errors');
  await b.close();
})();
