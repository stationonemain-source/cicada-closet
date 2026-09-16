(function(){
  var nav = document.getElementById('nav'), sheet = document.getElementById('nav-sheet');
  if (!nav || !sheet) return;
  var btn = nav.querySelector('.nav-toggle'), label = btn.querySelector('span');
  var over = document.querySelector('[data-nav-over]');
  var darks = Array.prototype.slice.call(document.querySelectorAll('[data-nav-dark]'));
  var allLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"], .nav-sheet nav a[href^="#"]'));
  var ids = []; allLinks.forEach(function(a){ var h = a.getAttribute('href'); if (ids.indexOf(h) < 0) ids.push(h); });
  var targets = ids.map(function(h){ return document.querySelector(h); });
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches, ticking = false;

  function update(){
    ticking = false;
    var h = nav.offsetHeight, mode = 'solid';
    if (over && over.hasAttribute('data-nav-over') && over.getBoundingClientRect().bottom > h) mode = 'over';
    else if (darks.some(function(d){ var r = d.getBoundingClientRect(); return r.top <= h - 2 && r.bottom > h + 2; })) mode = 'dark';
    if (nav.dataset.mode !== mode) nav.dataset.mode = mode;
    var line = innerHeight * 0.35, cur = null;
    targets.forEach(function(t, i){ if (t && t.getBoundingClientRect().top <= line) cur = ids[i]; });
    if (over && over.hasAttribute('data-nav-over') && over.getBoundingClientRect().bottom > line) cur = null;
    if (ids.length && innerHeight + scrollY >= document.documentElement.scrollHeight - 4) cur = ids[ids.length - 1];
    allLinks.forEach(function(a){
      if (a.getAttribute('href') === cur) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  function req(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);

  function go(hash){
    var t = document.querySelector(hash); if (!t) return;
    var off = -nav.offsetHeight;
    if (window.__lenis) window.__lenis.scrollTo(t, { offset: off, duration: 1.2 });
    else scrollTo({ top: t.getBoundingClientRect().top + scrollY + off, behavior: reduced ? 'auto' : 'smooth' });
  }
  function open(){
    sheet.hidden = false; nav.classList.add('is-open');
    btn.setAttribute('aria-expanded', 'true'); label.textContent = 'Close';
    document.documentElement.style.overflow = 'hidden'; if (window.__lenis) window.__lenis.stop();
    var first = sheet.querySelector('a'); if (first) first.focus();
  }
  function close(){
    if (sheet.hidden) return;
    sheet.hidden = true; nav.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false'); label.textContent = 'Menu';
    document.documentElement.style.overflow = ''; if (window.__lenis) window.__lenis.start();
  }
  btn.addEventListener('click', function(){ if (sheet.hidden) open(); else close(); });
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href^="#"]'); if (!a) return;
    var h = a.getAttribute('href'); if (h.length < 2 || !document.querySelector(h)) return;
    e.preventDefault(); close(); go(h);
    if (history.replaceState) history.replaceState(null, '', h);
  });
  addEventListener('keydown', function(e){ if (e.key === 'Escape' && !sheet.hidden){ close(); btn.focus(); } });
  matchMedia('(min-width: 901px)').addEventListener('change', function(m){ if (m.matches) close(); });

  window.__nav = { update: update };
  update();
})();
