/* BindRaft prototype — nav, reveal, work hover preview, contact stubs. No frameworks. */
(function () {
  document.documentElement.classList.remove('no-js');

  // Mobile menu
  var nav = document.querySelector('.nav');
  var btn = document.querySelector('.menu-btn');
  if (nav && btn) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Reveal on scroll
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }


  // Scroll-spy for sticky chapter index (Services) and legal contents (desktop)
  document.querySelectorAll('[data-spy]').forEach(function (ol) {
    // Skip if the TOC/index is hidden (e.g. legal Contents on mobile)
    function visible() {
      var host = ol.closest('.legal-toc, .svc-index') || ol;
      return window.getComputedStyle(host).display !== 'none';
    }
    var links = Array.prototype.slice.call(ol.querySelectorAll('a[href^="#"]'));
    var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
    var countEl = ol.parentElement && ol.parentElement.querySelector('[data-spy-count]');
    if (!secs.length) return;
    var active = -1;
    function set(i) {
      if (i < 0 || i >= links.length) return;
      if (i === active) return;
      active = i;
      links.forEach(function (a, k) {
        var on = k === i;
        a.classList.toggle('on', on);
        if (on) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
      if (countEl) countEl.textContent = ('0' + (i + 1)).slice(-2);
      var a = links[i];
      if (a && ol.scrollWidth > ol.clientWidth + 2) {
        ol.scrollTo({ left: Math.max(0, a.offsetLeft - 24), behavior: 'smooth' });
      }
    }
    var ticking = false;
    function check() {
      ticking = false;
      if (!visible()) return;
      var line = Math.min(140, window.innerHeight * 0.28);
      var idx = 0;
      for (var k = 0; k < secs.length; k++) {
        if (secs[k].getBoundingClientRect().top - line <= 0) idx = k;
      }
      var nearBottom = (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 8);
      if (nearBottom) idx = secs.length - 1;
      set(idx);
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function () {
        // Immediate copper active on click; scroll handler confirms after layout
        set(i);
        requestAnimationFrame(function () { setTimeout(check, 60); });
      });
    });
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(check); }
    }, { passive: true });
    window.addEventListener('resize', check);
    check();
  });

  // Work index hover preview
  var list = document.querySelector('.wlist');
  var pv = document.querySelector('.hover-preview');
  if (list && pv) {
    var t = pv.querySelector('.t'), b = pv.querySelector('.b');
    list.querySelectorAll('a[data-bg]').forEach(function (a) {
      a.addEventListener('mouseenter', function () {
        pv.style.background = a.dataset.bg; pv.style.color = a.dataset.fg;
        t.textContent = a.dataset.sector; b.textContent = a.dataset.name;
        pv.classList.add('on'); list.classList.add('dim');
      });
      a.addEventListener('mouseleave', function () { pv.classList.remove('on'); list.classList.remove('dim'); });
    });
    window.addEventListener('mousemove', function (e) {
      pv.style.left = (e.clientX + 180) + 'px'; pv.style.top = e.clientY + 'px';
    });
  }

  // Calendar stub
  var cal = document.getElementById('cal');
  if (cal) {
    var grid = cal.querySelector('.cal-grid');
    var label = cal.querySelector('[data-week]');
    var prev = cal.querySelector('[data-prev]'), next = cal.querySelector('[data-next]');
    var modal = document.getElementById('modal');
    var when = modal.querySelector('.when');
    var lastFocus = null;
    var offset = 0;
    var AM = ['10:00', '11:00', '11:30'], PM = ['14:00', '15:30', '16:30'];
    var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
    var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

    function monday(o) {
      var d = new Date(); d.setHours(0, 0, 0, 0);
      var day = d.getDay(); var diff = ((8 - day) % 7) || 7; // next Monday, always in the future
      d.setDate(d.getDate() + diff + o * 7); return d;
    }
    // deterministic "taken" slots so the grid looks real but is stable
    function taken(i, j, o) { return ((i * 7 + j * 3 + o * 5) % 5) === 0; }

    function render() {
      var m = monday(offset);
      var end = new Date(m); end.setDate(m.getDate() + 4);
      label.textContent = m.getDate() + ' ' + MONTHS[m.getMonth()] + ' – ' + end.getDate() + ' ' + MONTHS[end.getMonth()] + ' ' + end.getFullYear();
      prev.disabled = offset === 0; next.disabled = offset === 2;
      grid.innerHTML = '';
      DAYS.forEach(function (dn, i) {
        var d = new Date(m); d.setDate(m.getDate() + i);
        var col = document.createElement('div'); col.className = 'cal-day';
        col.innerHTML = '<div class="d">' + dn + '</div><div class="dt">' + d.getDate() + '</div>';
        var slots = document.createElement('div'); slots.className = 'slots';
        [['Morning', AM], ['Afternoon', PM]].forEach(function (g, gi) {
          var h = document.createElement('div'); h.className = 'grp'; h.textContent = g[0]; slots.appendChild(h);
          g[1].forEach(function (time, j) {
            var s = document.createElement('button'); s.type = 'button'; s.className = 'slot'; s.textContent = time;
            s.setAttribute('aria-pressed', 'false');
            var full = dn + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' · ' + time + ' (Dhaka, UTC+6) · 30 min';
            if (taken(i, j + gi * 3, offset)) { s.disabled = true; s.setAttribute('aria-label', time + ' unavailable'); }
            else {
              s.setAttribute('aria-label', 'Book ' + full);
              s.addEventListener('click', function () {
                grid.querySelectorAll('.slot[aria-pressed="true"]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
                s.setAttribute('aria-pressed', 'true');
                when.textContent = full; lastFocus = s; openModal();
              });
            }
            slots.appendChild(s);
          });
        });
        col.appendChild(slots); grid.appendChild(col);
      });
    }
    prev.addEventListener('click', function () { if (offset > 0) { offset--; render(); } });
    next.addEventListener('click', function () { if (offset < 2) { offset++; render(); } });

    function openModal() { modal.classList.add('on'); modal.querySelector('.x').focus(); }
    function closeModal() { modal.classList.remove('on'); if (lastFocus) lastFocus.focus(); }
    modal.querySelectorAll('[data-close]').forEach(function (x) { x.addEventListener('click', closeModal); });
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('on')) closeModal(); });
    render();
  }

  // Short form stub
  var form = document.getElementById('short-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var msg = document.getElementById('form-msg');
      msg.classList.add('on'); msg.focus();
      form.reset();
    });
  }
})();
