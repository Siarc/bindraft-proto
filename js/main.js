/* BindRaft — nav, reveal, legal scroll-spy, work hover preview, intro-call picker, contact form. No frameworks. Loaded with defer. */
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


  // Scroll-spy for legal contents (desktop)
  document.querySelectorAll('[data-spy]').forEach(function (ol) {
    // Skip if the TOC/index is hidden (e.g. legal Contents on mobile)
    function visible() {
      var host = ol.closest('.legal-toc') || ol;
      return window.getComputedStyle(host).display !== 'none';
    }
    var links = Array.prototype.slice.call(ol.querySelectorAll('a[href^="#"]'));
    var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
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

  var EMAIL = 'contact@bindraft.com';
  function mailto(subject, body) {
    return 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  // Intro-call picker: studio week is Sat–Thu, 9:00–18:00 Dhaka. Requests go out by email; we confirm with an invite.
  var cal = document.getElementById('cal');
  if (cal) {
    var grid = cal.querySelector('.cal-grid');
    var label = cal.querySelector('[data-week]');
    var prev = cal.querySelector('[data-prev]'), next = cal.querySelector('[data-next]');
    var modal = document.getElementById('modal');
    var when = modal.querySelector('.when');
    var send = document.getElementById('m-send');
    var note = document.getElementById('m-note');
    var lastFocus = null, chosen = '';
    var offset = 0, WEEKS = 3;
    var AM = ['10:00', '11:00', '11:30'], PM = ['14:00', '15:30', '16:30'];
    var DAYS = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu'];
    var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

    function saturday(o) { // next Saturday, always in the future
      var d = new Date(); d.setHours(0, 0, 0, 0);
      var diff = ((6 - d.getDay() + 7) % 7) || 7;
      d.setDate(d.getDate() + diff + o * 7); return d;
    }
    function render() {
      var m = saturday(offset);
      var end = new Date(m); end.setDate(m.getDate() + 5);
      label.textContent = m.getDate() + ' ' + MONTHS[m.getMonth()] + ' – ' + end.getDate() + ' ' + MONTHS[end.getMonth()] + ' ' + end.getFullYear();
      prev.disabled = offset === 0; next.disabled = offset === WEEKS - 1;
      grid.innerHTML = '';
      DAYS.forEach(function (dn, i) {
        var d = new Date(m); d.setDate(m.getDate() + i);
        var col = document.createElement('div'); col.className = 'cal-day';
        col.innerHTML = '<div class="d">' + dn + '</div><div class="dt">' + d.getDate() + '</div>';
        var slots = document.createElement('div'); slots.className = 'slots';
        [['Morning', AM], ['Afternoon', PM]].forEach(function (g) {
          var h = document.createElement('div'); h.className = 'grp'; h.textContent = g[0]; slots.appendChild(h);
          g[1].forEach(function (time) {
            var s = document.createElement('button'); s.type = 'button'; s.className = 'slot'; s.textContent = time;
            s.setAttribute('aria-pressed', 'false');
            var full = dn + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() + ' · ' + time + ' Dhaka (UTC+6) · 30 min';
            s.setAttribute('aria-label', 'Request ' + full);
            s.addEventListener('click', function () {
              grid.querySelectorAll('.slot[aria-pressed="true"]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
              s.setAttribute('aria-pressed', 'true');
              chosen = full; when.textContent = full; lastFocus = s; update(); openModal();
            });
            slots.appendChild(s);
          });
        });
        col.appendChild(slots); grid.appendChild(col);
      });
    }
    function update() {
      send.href = mailto('Intro call request: ' + chosen,
        'Hi BindRaft,\n\nI\'d like a 30-minute intro call at: ' + chosen + '.\n' +
        (note.value ? '\n' + note.value + '\n' : '') + '\nThanks,\n');
    }
    note.addEventListener('input', update);
    prev.addEventListener('click', function () { if (offset > 0) { offset--; render(); } });
    next.addEventListener('click', function () { if (offset < WEEKS - 1) { offset++; render(); } });

    function openModal() { modal.classList.add('on'); send.focus(); }
    function closeModal() { modal.classList.remove('on'); if (lastFocus) lastFocus.focus(); }
    send.addEventListener('click', function () { setTimeout(closeModal, 300); });
    modal.querySelectorAll('[data-close]').forEach(function (x) { x.addEventListener('click', closeModal); });
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) {
      if (!modal.classList.contains('on')) return;
      if (e.key === 'Escape') closeModal();
      if (e.key === 'Tab') { // keep focus inside the dialog
        var f = modal.querySelectorAll('button, a[href], input');
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    render();
  }

  // Short message: composes an email in the visitor's mail app (no server round-trip).
  var form = document.getElementById('short-form');
  if (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var v = function (n) { return (form.elements[n].value || '').trim(); };
      var body = v('message') + '\n\n— ' + v('name') + (v('company') ? ', ' + v('company') : '') + '\n' + v('email');
      window.location.href = mailto('Project enquiry' + (v('company') ? ': ' + v('company') : ' from ' + v('name')), body);
      var msg = document.getElementById('form-msg');
      msg.innerHTML = 'Your email app should open with the message ready to send. Nothing opened? Email <a class="link-u" href="mailto:' + EMAIL + '">' + EMAIL + '</a> or call +880 1558 934599.';
      msg.classList.add('on'); msg.focus();
    });
  }
})();
