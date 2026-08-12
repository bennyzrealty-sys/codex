/* ============================================================
   THE OPERATOR'S CODEX — the agentic layer
   No dependencies, no build step, no network beyond this origin.

     field()  the living neural background
     rail()   reading progress + where you are
     reveal() sections arrive instead of appearing
     lens()   every image, truly fullscreen
     pulse()  the live update feed (updates.json)
     marks()  newly-updated, until read three times
     door()   double-click a word, the wall opens
     seek()   press / or ⌘K to jump anywhere
   ============================================================ */
(function () {
  'use strict';

  var STILL = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ==========================================================
     1 · THE FIELD — a background that behaves like a mesh
     ========================================================== */
  function field() {
    if (STILL) return;
    var c = document.createElement('canvas');
    c.id = 'field';
    document.body.insertBefore(c, document.body.firstChild);
    var x = c.getContext('2d'), w = 0, h = 0;
    var nodes = [], far = [], signals = [], run = true;
    var px2 = -9999, py2 = -9999;      /* pointer, lerped */
    var tx = -9999, ty = -9999;        /* pointer, raw    */

    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, window.innerWidth < 900 ? 1.5 : 2);
      w = c.clientWidth; h = c.clientHeight;
      c.width = w * dpr; c.height = h * dpr;
      x.setTransform(dpr, 0, 0, dpr, 0, 0);
      var want = Math.max(26, Math.min(72, Math.round((w * h) / 26000)));
      nodes = []; far = [];
      var i;
      for (i = 0; i < want; i++) {
        nodes.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - .5) * .16, vy: (Math.random() - .5) * .16,
          r: Math.random() * 1.5 + .7, p: Math.random() * Math.PI * 2
        });
      }
      /* the far layer — smaller, dimmer, slower, and it parallaxes */
      for (i = 0; i < Math.min(30, want >> 1); i++) {
        far.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - .5) * .06, vy: (Math.random() - .5) * .06,
          r: Math.random() * .9 + .4, p: Math.random() * Math.PI * 2
        });
      }
    }

    function spark() {
      if (!nodes.length || signals.length > 5) return;
      var a = (Math.random() * nodes.length) | 0, b = (Math.random() * nodes.length) | 0;
      if (a === b) return;
      signals.push({ a: a, b: b, t: 0, hue: Math.random() < .5 ? '223,163,43' : '87,179,156' });
    }

    var LINK = 132, PULL = 140;
    function frame() {
      if (!run) return;
      x.clearRect(0, 0, w, h);
      var i, j, n, m, dx, dy, d;

      /* pointer eases in so the field feels liquid, not twitchy */
      if (tx > -9000) { px2 += (tx - px2) * .08; py2 += (ty - py2) * .08; }

      /* far layer first, shifted a touch by scroll */
      var off = (window.pageYOffset || 0) * -0.03;
      for (i = 0; i < far.length; i++) {
        n = far[i];
        n.x += n.vx; n.y += n.vy; n.p += .008;
        if (n.x < -20) n.x = w + 20; if (n.x > w + 20) n.x = -20;
        if (n.y < -20) n.y = h + 20; if (n.y > h + 20) n.y = -20;
        var fa = .08 + Math.sin(n.p) * .05;
        x.fillStyle = 'rgba(159,180,216,' + fa.toFixed(3) + ')';
        x.beginPath(); x.arc(n.x, ((n.y + off) % (h + 40) + h + 40) % (h + 40) - 20, n.r, 0, 6.284); x.fill();
      }

      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        n.x += n.vx; n.y += n.vy; n.p += .012;
        /* nodes near the pointer lean gently toward it */
        if (px2 > -9000) {
          dx = px2 - n.x; dy = py2 - n.y; d = dx * dx + dy * dy;
          if (d < PULL * PULL && d > 1) {
            var f = .012 * (1 - Math.sqrt(d) / PULL);
            n.x += dx * f; n.y += dy * f;
          }
        }
        if (n.x < -20) n.x = w + 20; if (n.x > w + 20) n.x = -20;
        if (n.y < -20) n.y = h + 20; if (n.y > h + 20) n.y = -20;
      }
      x.lineWidth = 1;
      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          m = nodes[j]; dx = n.x - m.x; dy = n.y - m.y; d = Math.sqrt(dx * dx + dy * dy);
          if (d < LINK) {
            x.strokeStyle = 'rgba(231,226,212,' + (.055 * (1 - d / LINK)).toFixed(3) + ')';
            x.beginPath(); x.moveTo(n.x, n.y); x.lineTo(m.x, m.y); x.stroke();
          }
        }
      }
      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        var a = .18 + Math.sin(n.p) * .12;
        x.fillStyle = 'rgba(223,163,43,' + a.toFixed(3) + ')';
        x.beginPath(); x.arc(n.x, n.y, n.r, 0, 6.284); x.fill();
      }
      for (i = signals.length - 1; i >= 0; i--) {
        var s = signals[i]; s.t += .012;
        if (s.t >= 1 || !nodes[s.a] || !nodes[s.b]) { signals.splice(i, 1); continue; }
        var A = nodes[s.a], B = nodes[s.b];
        var sx = A.x + (B.x - A.x) * s.t, sy = A.y + (B.y - A.y) * s.t;
        var fade = Math.sin(s.t * Math.PI);
        x.strokeStyle = 'rgba(' + s.hue + ',' + (.10 * fade).toFixed(3) + ')';
        x.beginPath(); x.moveTo(A.x, A.y); x.lineTo(B.x, B.y); x.stroke();
        x.fillStyle = 'rgba(' + s.hue + ',' + (.75 * fade).toFixed(3) + ')';
        x.beginPath(); x.arc(sx, sy, 2.1, 0, 6.284); x.fill();
      }
      requestAnimationFrame(frame);
    }

    size();
    window.addEventListener('resize', size, { passive: true });
    window.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      if (px2 < -9000) { px2 = tx; py2 = ty; }
    }, { passive: true });
    document.addEventListener('visibilitychange', function () {
      run = !document.hidden;
      if (run) requestAnimationFrame(frame);
    });
    setInterval(spark, 1400);
    requestAnimationFrame(frame);
  }

  /* ==========================================================
     2 · THE RAIL — progress and position
     ========================================================== */
  function rail() {
    var bar = document.createElement('div'); bar.id = 'rail';
    var tag = document.createElement('div'); tag.id = 'here';
    document.body.appendChild(bar); document.body.appendChild(tag);
    var secs = $$('section[id]');
    var tick = false;
    function paint() {
      tick = false;
      var top = window.pageYOffset || document.documentElement.scrollTop;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, top / max) : 0) + ')';
      var cur = null;
      for (var i = 0; i < secs.length; i++) {
        if (secs[i].getBoundingClientRect().top <= 110) cur = secs[i];
      }
      if (cur) {
        var n = $('.lnum', cur), t = $('h2', cur);
        tag.textContent = (n ? n.textContent.trim() + ' · ' : '') + (t ? t.textContent.trim() : '');
        tag.classList.add('on');
      } else { tag.classList.remove('on'); }
    }
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; requestAnimationFrame(paint); }
    }, { passive: true });
    paint();
  }

  /* ==========================================================
     2b · THE TRAIL — which layers you have actually sat in
     The numbering is the order these layers were written; the path
     panel is the order to read them, and ticks itself as you go.
     ========================================================== */
  var DWELL = 5000;   // ms in a section before it counts as read
  function trail() {
    var panel = $('#path');
    if (!panel) return;
    var links = $$('.plink', panel);
    var secs = $$('section[id]');
    var cur = null, since = 0;

    function key(id) { return 'codex.seen.' + id; }
    function seen(id) { return store.get(key(id)) === '1'; }

    function paint() {
      var done = 0;
      links.forEach(function (a) {
        var ok = seen(a.getAttribute('data-layer'));
        a.classList.toggle('seen', ok);
        if (ok) done += 1;
      });
      var slot = $('#pathcount');
      if (slot) {
        slot.textContent = done
          ? done + ' of ' + links.length + ' stops read on this device'
          : 'six stages · ' + links.length + ' stops · nothing read yet on this device';
      }
    }

    function settle() {
      if (cur && Date.now() - since >= DWELL && !seen(cur)) {
        store.set(key(cur), '1');
        paint();
      }
    }

    function where() {
      var found = null, mid = window.innerHeight * 0.45;
      for (var i = 0; i < secs.length; i++) {
        var r = secs[i].getBoundingClientRect();
        if (r.top <= mid && r.bottom > mid) { found = secs[i].id; break; }
      }
      if (found !== cur) { settle(); cur = found; since = Date.now(); }
    }

    var tick = false;
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; where(); }); }
    }, { passive: true });
    /* poll as well as listen — a jump from the path panel, a hash link or a
       restored scroll position can land you in a section without a scroll
       event ever reaching here */
    setInterval(function () { where(); settle(); }, 1500);
    window.addEventListener('beforeunload', settle);
    document.addEventListener('visibilitychange', function () { if (document.hidden) settle(); });

    var reset = $('#pathreset');
    if (reset) {
      reset.addEventListener('click', function () {
        links.forEach(function (a) {
          try { localStorage.removeItem(key(a.getAttribute('data-layer'))); } catch (e) {}
        });
        cur = null; since = Date.now();
        paint();
      });
    }

    where();
    paint();
  }

  /* ==========================================================
     3 · REVEAL — things arrive
     ========================================================== */
  function reveal() {
    if (STILL || !('IntersectionObserver' in window)) return;
    var targets = $$('section > h2, section > .lede, details.card, .rung, .blend, ' +
      'figure.fig, .note, .warn, .log, pre, .nodelog, .drop');
    var io = new IntersectionObserver(function (rows) {
      rows.forEach(function (r) {
        if (r.isIntersecting) { r.target.classList.add('lit'); io.unobserve(r.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .04 });
    targets.forEach(function (el) {
      if (el.closest('#lens') || el.closest('#door')) return;
      el.classList.add('rise'); io.observe(el);
    });
  }

  /* ==========================================================
     4 · THE LENS — every image, truly fullscreen
     ========================================================== */
  var lens = (function () {
    var box, stage, img, cap, count, figs = [], at = 0;
    var z = 1, ox = 0, oy = 0, drag = null, pinch = null;

    function build() {
      box = document.createElement('div');
      box.id = 'lens';
      box.setAttribute('role', 'dialog');
      box.setAttribute('aria-modal', 'true');
      box.setAttribute('aria-label', 'Image viewer');
      box.innerHTML =
        '<div class="bar">' +
          '<span class="count"></span>' +
          '<button class="lensbtn" data-a="out" aria-label="Zoom out">–</button>' +
          '<button class="lensbtn" data-a="in" aria-label="Zoom in">+</button>' +
          '<button class="lensbtn" data-a="fit" aria-label="Fit to screen">fit</button>' +
          '<button class="lensbtn" data-a="full" aria-label="Fill the whole screen">⤢</button>' +
          '<button class="lensbtn" data-a="shut" aria-label="Close">✕</button>' +
        '</div>' +
        '<div class="stage">' +
          '<button class="side prev" aria-label="Previous image">‹</button>' +
          '<img alt="">' +
          '<button class="side next" aria-label="Next image">›</button>' +
          '<div class="hint">pinch or double-tap to zoom · swipe for the next figure</div>' +
        '</div>' +
        '<div class="cap"></div>';
      document.body.appendChild(box);
      stage = $('.stage', box); img = $('img', box);
      cap = $('.cap', box); count = $('.count', box);

      box.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        if (b.classList.contains('prev')) return go(-1);
        if (b.classList.contains('next')) return go(1);
        var a = b.getAttribute('data-a');
        if (a === 'shut') shut();
        else if (a === 'in') zoom(1.4);
        else if (a === 'out') zoom(1 / 1.4);
        else if (a === 'fit') fit();
        else if (a === 'full') fullscreen();
      });

      img.addEventListener('dblclick', function (e) {
        e.preventDefault(); e.stopPropagation();
        if (z > 1.05) fit(); else zoom(2.2);
      });

      /* drag to pan */
      img.addEventListener('pointerdown', function (e) {
        if (z <= 1.02) return;
        drag = { x: e.clientX - ox, y: e.clientY - oy, id: e.pointerId };
        img.classList.add('grabbing');
        try { img.setPointerCapture(e.pointerId); } catch (err) {}
      });
      img.addEventListener('pointermove', function (e) {
        if (!drag || drag.id !== e.pointerId) return;
        ox = e.clientX - drag.x; oy = e.clientY - drag.y; put();
      });
      ['pointerup', 'pointercancel'].forEach(function (ev) {
        img.addEventListener(ev, function () { drag = null; img.classList.remove('grabbing'); });
      });

      /* pinch + swipe */
      stage.addEventListener('touchstart', function (e) {
        if (e.touches.length === 2) {
          pinch = { d: gap(e.touches), z: z };
        } else if (e.touches.length === 1 && z <= 1.02) {
          drag = { sx: e.touches[0].clientX, sy: e.touches[0].clientY, swipe: true };
        }
      }, { passive: true });
      stage.addEventListener('touchmove', function (e) {
        if (pinch && e.touches.length === 2) {
          e.preventDefault();
          z = Math.max(1, Math.min(6, pinch.z * (gap(e.touches) / pinch.d)));
          put();
        }
      }, { passive: false });
      stage.addEventListener('touchend', function (e) {
        if (pinch && e.touches.length < 2) { pinch = null; if (z <= 1.02) fit(); return; }
        if (drag && drag.swipe && e.changedTouches.length) {
          var dx = e.changedTouches[0].clientX - drag.sx;
          var dy = e.changedTouches[0].clientY - drag.sy;
          if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1);
          drag = null;
        }
      }, { passive: true });

      stage.addEventListener('wheel', function (e) {
        if (!box.classList.contains('on')) return;
        e.preventDefault(); zoom(e.deltaY < 0 ? 1.12 : 1 / 1.12);
      }, { passive: false });

      document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('on')) return;
        if (e.key === 'Escape') { e.preventDefault(); shut(); }
        else if (e.key === 'ArrowRight') go(1);
        else if (e.key === 'ArrowLeft') go(-1);
        else if (e.key === '+' || e.key === '=') zoom(1.3);
        else if (e.key === '-') zoom(1 / 1.3);
        else if (e.key === '0') fit();
        else if (e.key.toLowerCase() === 'f') fullscreen();
      });
    }

    function gap(t) {
      var dx = t[0].clientX - t[1].clientX, dy = t[0].clientY - t[1].clientY;
      return Math.sqrt(dx * dx + dy * dy) || 1;
    }
    function put() { img.style.transform = 'translate(' + ox + 'px,' + oy + 'px) scale(' + z + ')'; }
    function fit() { z = 1; ox = 0; oy = 0; put(); }
    function zoom(f) { z = Math.max(1, Math.min(6, z * f)); if (z === 1) { ox = 0; oy = 0; } put(); }

    function fullscreen() {
      var d = document;
      if (d.fullscreenElement || d.webkitFullscreenElement) {
        (d.exitFullscreen || d.webkitExitFullscreen || function () {}).call(d);
      } else {
        (box.requestFullscreen || box.webkitRequestFullscreen || function () {}).call(box);
      }
    }

    function show(i) {
      at = (i + figs.length) % figs.length;
      var f = figs[at];
      img.style.animation = 'none';
      /* reflow so the entrance animation replays on every figure */
      void img.offsetWidth;
      img.style.animation = '';
      img.src = f.src;
      img.alt = f.alt;
      cap.textContent = f.cap;
      count.textContent = (at + 1) + ' / ' + figs.length;
      fit();
    }
    function go(d) { if (figs.length > 1) show(at + d); }

    function open(el) {
      if (!box) build();
      /* index by element, not by src — the same diagram can legitimately
         appear in a layer and again in a feed entry, with different captions */
      var nodes = $$('figure.fig img');
      figs = nodes.map(function (n) {
        var fg = n.closest('figure');
        var fc = fg ? $('figcaption', fg) : null;
        return { src: n.currentSrc || n.src, alt: n.alt || '', cap: fc ? fc.textContent.trim() : (n.alt || '') };
      });
      var idx = nodes.indexOf(el);
      if (idx < 0) idx = 0;
      box.classList.add('on');
      document.documentElement.style.overflow = 'hidden';
      show(idx);
      $('.side.prev', box).style.display = figs.length > 1 ? '' : 'none';
      $('.side.next', box).style.display = figs.length > 1 ? '' : 'none';
      $('[data-a="shut"]', box).focus();
    }

    function shut() {
      if (!box) return;
      box.classList.remove('on');
      document.documentElement.style.overflow = '';
      if (document.fullscreenElement) { try { document.exitFullscreen(); } catch (e) {} }
    }

    return { open: open, shut: shut };
  })();

  function wireLens() {
    document.addEventListener('click', function (e) {
      var im = e.target.closest('figure.fig img');
      if (!im) return;
      e.preventDefault();
      lens.open(im);
    });
    $$('figure.fig img').forEach(function (im) {
      im.setAttribute('tabindex', '0');
      im.setAttribute('role', 'button');
      im.setAttribute('aria-label', 'Open full screen: ' + (im.alt || 'figure'));
      im.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); lens.open(im); }
      });
    });
  }

  /* ==========================================================
     5 · THE MARKS — newly updated, until read three times
     ========================================================== */
  var READS_NEEDED = 3;
  function marks() {
    $$('details.card[data-updated]').forEach(function (card) {
      var id = card.getAttribute('data-card') || '';
      var when = card.getAttribute('data-updated') || '';
      var note = card.getAttribute('data-updnote') || '';
      var key = 'codex.read.' + id + '.' + when;
      var seen = parseInt(store.get(key) || '0', 10) || 0;

      var sum = $('summary', card); if (!sum) return;
      var badge = document.createElement('span');
      badge.className = 'mark' + (seen >= READS_NEEDED ? ' faded' : '');
      sum.insertBefore(badge, sum.firstChild);

      var line = null;
      if (note || when) {
        line = document.createElement('p');
        line.className = 'markline';
        line.innerHTML = '<b>Updated ' + esc(when) + '</b>' + (note ? ' — ' + esc(note) : '');
        if (sum.nextSibling) card.insertBefore(line, sum.nextSibling);
        else card.appendChild(line);
      }

      function paint() {
        if (seen >= READS_NEEDED) {
          badge.classList.add('faded');
          badge.innerHTML = '<span class="dot"></span>read · ' + esc(when);
        } else {
          badge.classList.remove('faded');
          badge.innerHTML = '<span class="dot"></span>newly updated · ' +
            seen + ' of ' + READS_NEEDED + ' reads';
        }
      }
      paint();

      card.addEventListener('toggle', function () {
        if (!card.open || seen >= READS_NEEDED) return;
        seen += 1; store.set(key, String(seen)); paint();
      });
    });

    /* the header tally: how many marks are still unread */
    var left = $$('details.card[data-updated]').filter(function (c) {
      var k = 'codex.read.' + c.getAttribute('data-card') + '.' + c.getAttribute('data-updated');
      return (parseInt(store.get(k) || '0', 10) || 0) < READS_NEEDED;
    }).length;
    var slot = $('#updtally');
    if (slot) {
      slot.textContent = left
        ? left + ' card' + (left === 1 ? '' : 's') + ' newly updated — unread'
        : 'every updated card read three times';
      if (left) slot.classList.add('newbadge');
    }
  }

  /* ==========================================================
     6 · THE PULSE — the live update feed
     ========================================================== */
  var PAGE = 10;
  function pulse() {
    var host = $('#feed'); if (!host) return;
    fetch('updates.json?t=' + Date.now())
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { render(host, d); })
      .catch(function () {
        host.innerHTML = '<div class="vault">The feed file could not be read from here. ' +
          'Open the Codex at its published link and the last two years of updates load ' +
          'instantly — nothing in it is ever deleted.</div>';
      });
  }

  function render(host, d) {
    var all = (d.entries || []).slice().sort(function (a, b) {
      return (b.date || '').localeCompare(a.date || '') ||
             (b.id || '').localeCompare(a.id || '');
    });
    var filter = 'all', shown = PAGE;

    var meta = $('#pulsemeta');
    if (meta) {
      var next = d.next_scan ? esc(d.next_scan) : 'in under 48 hours';
      meta.innerHTML =
        'scan cadence <b>every 2 days</b> · 06:00 UTC · next sweep <b>' + next + '</b><br>' +
        'entries held <b>' + all.length + '</b> · newest first · ' +
        '<b>append-only</b> — nothing here is ever edited away or deleted';
    }

    var chips = $('#filters');
    if (chips) {
      chips.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        filter = b.getAttribute('data-dom');
        $$('button', chips).forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
        });
        shown = PAGE; paint();
      });
    }

    function paint() {
      var rows = all.filter(function (e) { return filter === 'all' || e.domain === filter; });
      var slice = rows.slice(0, shown);
      var html = '', month = '';
      slice.forEach(function (e, i) {
        var m = (e.date || '').slice(0, 7);
        if (m !== month) {
          month = m;
          html += '<div class="yearline">' + esc(monthName(m)) + '</div>';
        }
        html += card(e, i === 0);
      });
      if (!slice.length) html = '<div class="vault">Nothing filed under this field yet. ' +
        'The next sweep is never more than two days away.</div>';
      host.innerHTML = html +
        (rows.length > shown
          ? '<button class="feedmore">show older — ' + (rows.length - shown) + ' more in the vault</button>'
          : (rows.length > PAGE
            ? '<div class="vault"><b>End of the vault.</b> Every entry ever written is above; ' +
              'the feed only ever grows downward.</div>' : ''));
      var more = $('.feedmore', host);
      if (more) more.addEventListener('click', function () { shown += PAGE; paint(); });
    }

    /* `open` unfolds the newest item so the section is never a wall of
       closed titles; `fresh` is the pulsing dot, which belongs to anything
       from the last sweep whether or not it happens to be first. */
    function card(e, open) {
      var dom = (e.domain || 'it').toLowerCase();
      var isNew = daysAgo(e.date) <= 2;
      var fresh = isNew;
      /* width/height reserve the space before the image loads, so the feed
         does not shove the rest of the page down as you read it */
      var dim = (e.artw && e.arth) ? ' width="' + e.artw + '" height="' + e.arth + '"' : '';
      var art = e.art
        ? '<figure class="fig"><img src="' + esc(e.art) + '" alt="' + esc(e.artalt || e.title || '') +
          '" loading="lazy"' + dim + '><figcaption>' + esc(e.artcap || e.title || '') +
          '</figcaption></figure>'
        : '';
      var tools = (e.tools && e.tools.length)
        ? '<p class="kit">' + e.tools.map(function (t) { return '<code>' + esc(t) + '</code>'; }).join(' ') +
          (e.toolnote ? '<br>' + esc(e.toolnote) : '') + '</p>'
        : '';
      var srcs = (e.sources && e.sources.length)
        ? '<p class="srcs">' + e.sources.map(function (s) {
            return s.url
              ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer">' + esc(s.label || s.url) + ' ↗</a>'
              : esc(s.label || '');
          }).join('') + '</p>'
        : '';
      return '<details class="drop' + (fresh ? ' fresh' : '') + '"' + (open ? ' open' : '') + '>' +
        '<summary>' +
          '<span class="dropmeta">' +
            '<span class="when">' + esc(e.date || '') + '</span>' +
            '<span class="dom ' + esc(dom) + '">' + esc(domName(dom)) + '</span>' +
            (isNew ? '<span class="dom new">new</span>' : '') +
          '</span>' +
          '<h4>' + esc(e.title || '') + '</h4>' +
          (e.oneline ? '<span class="oneline">' + esc(e.oneline) + '</span>' : '') +
        '</summary>' +
        '<div class="dropbody">' +
          art +
          (e.plain ? '<p class="plain">' + esc(e.plain) + '</p>' : '') +
          (e.tech ? '<p class="tech">' + esc(e.tech) + '</p>' : '') +
          (e.lands ? '<p class="lands">' + esc(e.lands) + '</p>' : '') +
          tools + srcs +
        '</div>' +
      '</details>';
    }
    paint();
  }

  function domName(d) {
    return { ai: 'artificial intelligence', it: 'information technology',
             hardware: 'hardware & silicon', cyber: 'cyber security' }[d] || d;
  }
  function monthName(m) {
    var p = m.split('-'); if (p.length < 2) return m;
    var names = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
      'August', 'September', 'October', 'November', 'December'];
    return (names[parseInt(p[1], 10) - 1] || '') + ' ' + p[0];
  }
  function daysAgo(iso) {
    var t = Date.parse(iso + 'T00:00:00Z');
    if (isNaN(t)) return 999;
    return Math.floor((Date.now() - t) / 86400000);
  }

  /* ==========================================================
     7 · THE DOOR — double-click a word, the wall opens
     ========================================================== */

  /* ---- a procedural illustration, seeded by the word itself ----
     Shared by the door (a room with no art still gets a picture)
     and the atlas (a layer with no diagram still gets a tile). */
  function glyph(term, W, H, label, world) {
    W = W || 720; H = H || 300;
    var seed = 0;
    for (var i = 0; i < term.length; i++) seed = (seed * 31 + term.charCodeAt(i)) >>> 0;
    function rnd() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
    var cx = W / 2, cy = H / 2;
    var cols = ['#dfa32b', '#57b39c', '#cf6f57'];

    var head = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" ' +
      'aria-label="Abstract emblem for ' + esc(term) + '" preserveAspectRatio="xMidYMid slice">' +
      '<rect width="' + W + '" height="' + H + '" fill="#0a0e13"/>';
    var tail = (label !== false
      ? '<text x="' + cx + '" y="' + (H - 18) + '" text-anchor="middle" fill="#aab5c1" ' +
        'font-family="ui-monospace,monospace" font-size="12" letter-spacing="3">' +
        esc(term.toUpperCase()) + '</text>'
      : '') + '</svg>';
    var g, j, a, r;

    /* the shield family — concentric wards and spokes */
    if (world === 'shield') {
      g = head;
      var R = Math.min(W, H) * .42, NR = 4, SP = 7 + Math.floor(rnd() * 4);
      for (r = 1; r <= NR; r++) {
        g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (R * r / NR).toFixed(1) +
             '" fill="none" stroke="#cf6f57" stroke-opacity="' + (.42 - r * .07).toFixed(2) + '"/>';
      }
      for (j = 0; j < SP; j++) {
        a = (j / SP) * 6.283 + rnd() * .2;
        g += '<line x1="' + (cx + Math.cos(a) * R * .22).toFixed(1) + '" y1="' + (cy + Math.sin(a) * R * .22).toFixed(1) +
             '" x2="' + (cx + Math.cos(a) * R).toFixed(1) + '" y2="' + (cy + Math.sin(a) * R).toFixed(1) +
             '" stroke="#e7e2d4" stroke-opacity=".12"/>';
        var rr = R * (.4 + rnd() * .6);
        g += '<circle cx="' + (cx + Math.cos(a) * rr).toFixed(1) + '" cy="' + (cy + Math.sin(a) * rr).toFixed(1) +
             '" r="' + (2.2 + rnd() * 2.6).toFixed(1) + '" fill="' + cols[j % 3] + '" fill-opacity=".85"/>';
      }
      g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (R * .16).toFixed(1) +
           '" fill="none" stroke="#dfa32b" stroke-opacity=".7"/>' +
           '<circle cx="' + cx + '" cy="' + cy + '" r="5" fill="#cf6f57"/>';
      return g + tail;
    }

    /* the wire & silicon families — a jittered lattice */
    if (world === 'wire' || world === 'silicon') {
      g = head;
      var hue = world === 'wire' ? '#9fb4d8' : '#dfa32b';
      var GX = 9, GY = 4, gx = W / (GX + 1), gy = H / (GY + 1), grid = [];
      for (var yy = 1; yy <= GY; yy++) for (var xx = 1; xx <= GX; xx++) {
        grid.push({ x: xx * gx + (rnd() - .5) * gx * .5, y: yy * gy + (rnd() - .5) * gy * .5, on: rnd() > .35 });
      }
      g += '<g stroke="' + hue + '" stroke-opacity=".14">';
      for (j = 0; j < grid.length; j++) {
        if (j % GX !== GX - 1) g += '<line x1="' + grid[j].x.toFixed(1) + '" y1="' + grid[j].y.toFixed(1) +
          '" x2="' + grid[j + 1].x.toFixed(1) + '" y2="' + grid[j + 1].y.toFixed(1) + '"/>';
        if (j + GX < grid.length && rnd() > .4) g += '<line x1="' + grid[j].x.toFixed(1) + '" y1="' + grid[j].y.toFixed(1) +
          '" x2="' + grid[j + GX].x.toFixed(1) + '" y2="' + grid[j + GX].y.toFixed(1) + '"/>';
      }
      g += '</g>';
      grid.forEach(function (p, i2) {
        if (!p.on) return;
        g += '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="' + (1.8 + rnd() * 2.4).toFixed(1) +
             '" fill="' + (rnd() > .75 ? cols[i2 % 3] : hue) + '" fill-opacity=".8"/>';
      });
      return g + tail;
    }

    /* the default — a seeded constellation */
    var pts = [], rings = 3, k = 0;
    var scale = Math.min(W / 720, 1);
    for (var r = 1; r <= rings; r++) {
      var n = 3 + r * 2 + Math.floor(rnd() * 3);
      var rad = (34 + r * 42) * (H / 300);
      var off = rnd() * 6.28;
      for (var j = 0; j < n; j++) {
        var a = off + (j / n) * 6.283 + (rnd() - .5) * .3;
        pts.push({
          x: cx + Math.cos(a) * rad * 1.85, y: cy + Math.sin(a) * rad * .82,
          r: (2 + rnd() * 3.2) * Math.max(scale, .7), c: cols[(k++) % 3], d: (rnd() * 3).toFixed(2)
        });
      }
    }
    var s = head;
    s += '<g stroke="#e7e2d4" stroke-opacity=".10" stroke-width="1">';
    for (var p = 0; p < pts.length; p++) {
      var q = pts[(p + 1 + Math.floor(rnd() * 3)) % pts.length];
      s += '<line x1="' + pts[p].x.toFixed(1) + '" y1="' + pts[p].y.toFixed(1) +
           '" x2="' + q.x.toFixed(1) + '" y2="' + q.y.toFixed(1) + '"/>';
    }
    s += '</g>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (26 * (H / 300)).toFixed(1) +
         '" fill="none" stroke="#dfa32b" stroke-opacity=".5"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (7 * (H / 300)).toFixed(1) + '" fill="#dfa32b"/>';
    pts.forEach(function (p) {
      s += '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="' + p.r.toFixed(1) +
           '" fill="' + p.c + '" fill-opacity=".8">' +
           (STILL ? '' : '<animate attributeName="fill-opacity" values="0.8;0.25;0.8" dur="' +
            (2.6 + parseFloat(p.d)).toFixed(1) + 's" repeatCount="indefinite"/>') +
           '</circle>';
    });
    return s + tail;
  }

  /* ==========================================================
     6b · THE ATLAS — the constellation of layers up top
     ========================================================== */
  function atlas() {
    var host = $('#atlas'); if (!host) return;
    var tiles = $$('.tile[data-layer]', host);

    /* imageless layers get a seeded constellation tile */
    $$('.glyphslot', host).forEach(function (slot) {
      slot.innerHTML = glyph(slot.getAttribute('data-glyph') || 'codex', 480, 200, false);
    });

    /* card counts are computed from the live DOM, so a caretaker
       sweep that adds cards can never leave a stale number here */
    tiles.forEach(function (t) {
      var id = t.getAttribute('data-layer');
      var sec = document.getElementById(id);
      if (!sec) return;
      var n = $$('details.card', sec).length;
      if (!n) return;
      var chip = document.createElement('span');
      chip.className = 'tcount';
      chip.textContent = n + (n === 1 ? ' card' : ' cards');
      t.appendChild(chip);
    });

    /* seen state + the header ring — read-only reuse of the trail's keys */
    var ring = $('#atlasring');
    function paint() {
      var done = 0;
      tiles.forEach(function (t) {
        var ok = store.get('codex.seen.' + t.getAttribute('data-layer')) === '1';
        t.classList.toggle('seen', ok);
        if (ok) done += 1;
      });
      if (ring) {
        var R = 15, C = 2 * Math.PI * R, frac = tiles.length ? done / tiles.length : 0;
        ring.innerHTML =
          '<svg width="38" height="38" viewBox="0 0 38 38" aria-hidden="true">' +
          '<circle cx="19" cy="19" r="' + R + '" fill="none" stroke="rgba(231,226,212,.14)" stroke-width="3"/>' +
          '<circle cx="19" cy="19" r="' + R + '" fill="none" stroke="#57b39c" stroke-width="3" ' +
          'stroke-linecap="round" stroke-dasharray="' + C.toFixed(1) + '" ' +
          'stroke-dashoffset="' + (C * (1 - frac)).toFixed(1) + '" ' +
          'transform="rotate(-90 19 19)"/></svg>' +
          '<span>' + done + ' of ' + tiles.length + ' read</span>';
      }
    }
    paint();
    /* the trail writes its keys on a settle; a slow poll keeps the
       tiles honest without wiring the two modules together */
    setInterval(paint, 2500);

    /* at a desk, the reading path stands open as a route stepper */
    var path = $('#path');
    if (path && window.matchMedia) {
      var mq = window.matchMedia('(min-width:1024px)');
      function fit() { if (mq.matches) path.setAttribute('open', ''); }
      if (mq.addEventListener) mq.addEventListener('change', fit);
      fit();
    }
  }

  /* ==========================================================
     6c · THE MINIMAP — every layer as a dot on a fixed rail
     ========================================================== */
  function minimap() {
    var secs = $$('section[id]');
    if (!secs.length) return;
    var map = document.createElement('div');
    map.id = 'map';
    map.setAttribute('aria-label', 'Layer minimap');
    map.innerHTML = secs.map(function (s) {
      var n = $('.lnum', s), h = $('h2', s);
      var t = ((n ? n.textContent.trim().replace(/\s*·.*$/, '') : '') + ' ' +
               (h ? h.textContent.trim() : s.id)).trim();
      return '<a href="#' + esc(s.id) + '" data-id="' + esc(s.id) + '" data-t="' + esc(t) + '"></a>';
    }).join('');
    document.body.appendChild(map);

    map.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      e.preventDefault();
      var el = document.getElementById(a.getAttribute('data-id'));
      if (el) el.scrollIntoView({ behavior: STILL ? 'auto' : 'smooth', block: 'start' });
    });

    var dots = $$('a', map), tick = false;
    function paint() {
      tick = false;
      var cur = null;
      for (var i = 0; i < secs.length; i++) {
        if (secs[i].getBoundingClientRect().top <= 120) cur = secs[i].id;
      }
      dots.forEach(function (d) {
        var id = d.getAttribute('data-id');
        d.classList.toggle('on', id === cur);
        d.classList.toggle('seen', store.get('codex.seen.' + id) === '1');
      });
    }
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; requestAnimationFrame(paint); }
    }, { passive: true });
    setInterval(paint, 2500);
    paint();
  }

  /* Inline code copies itself on a click — small, but it makes the
     tech voices feel like a workbench instead of a wall of jargon. */
  function copycode() {
    if (!navigator.clipboard) return;
    document.addEventListener('click', function (e) {
      var el = e.target.closest('code');
      if (!el || el.closest('pre,a,button,#door,#seek,#lens')) return;
      var txt = el.textContent.trim();
      if (!txt) return;
      navigator.clipboard.writeText(txt).then(function () {
        var tip = document.createElement('div');
        tip.className = 'dtip';
        tip.textContent = 'copied';
        var r = el.getBoundingClientRect();
        tip.style.position = 'absolute';
        tip.style.left = (r.left + r.width / 2) + 'px';
        tip.style.top = (r.top + window.pageYOffset - 4) + 'px';
        document.body.appendChild(tip);
        requestAnimationFrame(function () { tip.classList.add('on'); });
        setTimeout(function () { tip.classList.remove('on'); }, 1000);
        setTimeout(function () { tip.remove(); }, 1400);
      }).catch(function () {});
    });
  }

  /* When an open card jumps to full width the grid reflows under the
     pointer; keep the card the reader just opened inside the viewport. */
  function settleCards() {
    document.addEventListener('toggle', function (e) {
      var d = e.target;
      if (!d || !d.matches || !d.matches('details.card') || !d.open) return;
      requestAnimationFrame(function () {
        var r = d.getBoundingClientRect();
        if (r.top < 0 || r.top > window.innerHeight * .8) {
          d.scrollIntoView({ behavior: STILL ? 'auto' : 'smooth', block: 'nearest' });
        }
      });
    }, true);
  }

  /* Hand-written entries carry both voices. Everything else is
     assembled at runtime from the glossary and the layers, so the
     door never goes stale when the caretaker rewrites a card. */
  var LEX = {
    'token': { art: 'images/tokens.svg',
      plain: 'Models do not read words. They read word-pieces called tokens — roughly three quarters of a word each. Everything in this world is counted in them: speed is tokens per second, cost is pounds per million tokens, memory is a token budget.',
      tech: 'Sub-word units produced by a BPE-family tokenizer mapping text → integer IDs; ~4 chars/token for English, materially worse for Malayalam and other agglutinative, Unicode-heavy scripts. Both API pricing and context limits are token-denominated.' },
    'context window': { art: 'images/context-window.svg', aka: ['context'],
      plain: 'Everything the model can see in this one moment — your question, the conversation so far, any files pasted in. Nothing outside the window exists to it. When the window fills, the oldest things fall out and it genuinely forgets them.',
      tech: 'The maximum token span attended over in a single forward pass. Attention cost grows roughly quadratically with length, so long contexts are expensive and degrade in the middle ("lost in the middle"). KV-cache size scales with context × layers × heads — often the real memory ceiling at inference.' },
    'quantization': { art: 'images/quantization.svg', aka: ['quantisation', 'quantized', 'quantised', 'q4'],
      plain: 'Rounding off a model\'s billions of dials so each takes less room — like storing prices to the nearest pound instead of the nearest penny. The model gets small enough to run on your own machine and loses a little precision doing it.',
      tech: 'Reducing weight/activation precision from FP16 to INT8/INT4 (GGUF Q4_K_M, AWQ, GPTQ, NF4). Memory footprint falls roughly linearly with bit-width; perplexity degrades gently to ~4-bit then sharply below. This is the single technique that puts a capable model on a Pi.' },
    'agent': { art: 'images/agent-loop.svg', aka: ['agents', 'agentic'],
      plain: 'A model given three extra things: a goal, a set of tools it may use, and a loop that lets it keep going until the goal is met. Chat answers you. An agent goes and does.',
      tech: 'An LLM in a perceive → decide → act → observe loop with tool-calling, a termination condition, and usually memory. Reliability is bounded by compounding per-step error: 95% per-step success over 20 steps is a 36% task success rate — which is why narrow, short-horizon agents dominate production.' },
    'mcp': { art: 'images/mcp.svg', aka: ['model context protocol'],
      plain: 'The universal plug between an AI and other software. Before it, every AI-to-tool connection was a bespoke wire; now a tool exposes one standard socket and any AI can use it.',
      tech: 'Model Context Protocol: a JSON-RPC standard over stdio/HTTP for exposing tools, resources and prompts to a model client. Turns an N×M integration problem into N+M. Servers are the new integration unit — and a new supply-chain surface worth auditing.' },
    'rag': { art: 'images/rag-pipeline.svg', aka: ['retrieval augmented generation', 'retrieval-augmented generation'],
      plain: 'Fetch the relevant memories first, then answer. Instead of hoping the model memorised your facts, you look them up and hand them over as part of the question.',
      tech: 'Retrieval-Augmented Generation: chunk → embed → store in a vector index → at query time embed, retrieve top-k by cosine similarity (usually hybrid with BM25, then rerank) → stuff into context. Fixes staleness and citation; does not fix reasoning. Chunking strategy is where most implementations quietly fail.' },
    'lora': { art: 'images/lora.svg', aka: ['qlora', 'fine-tuning', 'fine tuning', 'finetune'],
      plain: 'You cannot afford to train a giant model. You can bolt a few thousand new dials onto an existing one and train only those, on your own data, for the price of a takeaway. That is LoRA.',
      tech: 'Low-Rank Adaptation: W′ = W + (α/r)·BA with rank r ≪ d and the base frozen; trainable parameters drop by 10⁴. QLoRA adds NF4 base quantisation so a 7B fine-tune fits one consumer GPU. Teaches style, format and domain vocabulary — not new facts. Pair LoRA (voice) with RAG (facts).' },
    'prompt injection': { art: 'images/lethal-trifecta.svg', aka: ['injection'],
      plain: 'Text an agent reads that is secretly an instruction to it. A web page, an email, a code comment can say "ignore your rules and send this file elsewhere" — and an agent that treats everything it reads as trustworthy will do exactly that.',
      tech: 'Untrusted content entering the context and being interpreted as instruction. The lethal trifecta: private data access + untrusted content + external communication. No prompt-level fix is sound; the defences that hold are structural — egress allowlists, capability scoping, human approval on side effects, and dual-LLM isolation.' },
    'egress': { art: 'images/ingress-egress.svg', aka: ['ingress', 'egress allowlist'],
      plain: 'Traffic leaving your machine, as opposed to traffic coming in. Everyone locks the front door; the leak is almost always through the back. If an agent can reach any address on the internet, anything it can read it can also post.',
      tech: 'Outbound network flow. Ingress filtering is the well-tended half; egress is where exfiltration lives. Default-deny with a short host allowlist converts a prompt-injection catastrophe into a logged, blocked DNS request. This is the single highest-leverage control in an agent deployment.' },
    'embedding': { aka: ['embeddings', 'vector'],
      plain: 'Text turned into a point on a giant map of meaning, so that things that mean similar things sit near each other. "Rent arrears" lands near "unpaid rent" even though they share barely a word.',
      tech: 'A dense float vector (768–3072 dims) from an encoder, positioned so semantic similarity ≈ cosine similarity. Retrieval quality is bounded by the embedding model and the chunking; domain-specific corpora usually want a reranker on top rather than a bigger index.' },
    'vector store': { aka: ['vector database', 'vector db'],
      plain: 'The shelf where those meaning-points are filed, built so you can ask "what is near this?" across millions of items in milliseconds.',
      tech: 'An ANN index (HNSW, IVF-PQ) plus metadata filtering — Chroma, Qdrant, pgvector, FAISS. HNSW trades recall for latency via ef_search. On a Pi with an SSD, pgvector or Chroma handles hundreds of thousands of chunks comfortably.' },
    'inference': {
      plain: 'Using a trained model — the everyday act of getting an answer out of it, one word-piece at a time. Training is building the brain; inference is thinking with it.',
      tech: 'The forward pass at serving time. Prefill (parallel, compute-bound) then decode (sequential, memory-bandwidth-bound). Batching, KV-cache reuse, paged attention and speculative decoding are the levers. On CPU, tokens/sec is almost entirely a bandwidth story.' },
    'hallucination': {
      plain: 'Fluent guessing presented as fact. The model is not lying — it is doing exactly its job, guessing plausible next word-pieces, in a place where it has no knowledge. Confidence tells you nothing about truth.',
      tech: 'Ungrounded generation. Rooted in the training objective: next-token likelihood rewards plausibility, not verifiability, and RLHF can reward confident phrasing. Mitigations are architectural — retrieval grounding, citation-required prompting, constrained decoding, and verification passes.' },
    'transformer': { art: 'images/next-token-loop.svg', aka: ['attention'],
      plain: 'The design that made all of this work. Its trick is attention: every word-piece looks at every other word-piece and decides which ones matter to it. That is how meaning travels across a sentence.',
      tech: 'Self-attention: softmax(QKᵀ/√d_k)·V, multi-head, stacked with feed-forward blocks and residual connections. Parallelisable over sequence length at training time (unlike RNNs) — the property that made scaling laws exploitable at all.' },
    'container': {
      plain: 'A sealed pop-up workshop: the code, its tools and its ingredients in one box that runs identically anywhere, then gets shredded when the job ends.',
      tech: 'OS-level virtualisation via namespaces and cgroups (Docker/OCI). Image = layered filesystem recipe; container = running instance. Ephemeral by design — persist anything valuable to an external store before exit, or it goes with the box.' },
    'ssh': { aka: ['ssh key', 'ssh keys'],
      plain: 'The encrypted tunnel you use to sit at a computer that is not in front of you. You prove who you are with a key file, not a password — the key never leaves your machine.',
      tech: 'Secure Shell over TCP/22. Public-key auth: ed25519 keypair, public half in ~/.ssh/authorized_keys. Harden by disabling password auth and root login (PasswordAuthentication no, PermitRootLogin no). On a home node, prefer no port-forward at all — reach it over Tailscale/WireGuard.' },
    'dns': {
      plain: 'The internet\'s phone book. You type a name; DNS turns it into the number a machine can actually dial. It is also the quietest place to watch what a machine is trying to talk to.',
      tech: 'Hierarchical name resolution: stub resolver → recursive → root → TLD → authoritative, cached by TTL. Records: A/AAAA, CNAME, MX, TXT. DNS logs are the cheapest exfiltration detector you will ever deploy — and DNS itself is a classic covert channel.' },
    'tls': { aka: ['https', 'ssl', 'certificate'],
      plain: 'The padlock. Before any of your data moves, the two ends agree a secret nobody watching can work out, and the server proves it really is who the address claims. That is all HTTPS is.',
      tech: 'TLS 1.3: ECDHE key agreement, AEAD ciphers, one round trip. X.509 certificates chain to a trusted root; Let\'s Encrypt via ACME made them free and automatic. The ClientHello is sent in clear — which is exactly why JA3/JA4 fingerprints a caller before a single header is read.' },
    'zero trust': {
      plain: 'Stop believing that being inside the building makes you trustworthy. Every request proves who it is and what it may do, every time, no matter where it came from.',
      tech: 'BeyondCorp-style architecture: no implicit network trust, per-request authN/authZ, device posture as a signal, micro-segmentation, short-lived credentials. NIST SP 800-207 is the reference. Practically: identity-aware proxy in front of everything, and no flat LAN.' },
    'mfa': { aka: ['2fa', 'passkey', 'passkeys', 'two-factor'],
      plain: 'A second proof beyond the password. The strong version is a passkey — a secret your phone or laptop holds and will only release to the real website, so a convincing fake page gets nothing.',
      tech: 'Multi-factor auth. SMS/TOTP resist reuse but not real-time phishing proxies (Evilginx). FIDO2/WebAuthn passkeys bind the credential to the origin and keep the private key in a secure element — phishing-resistant by construction. Migrate admin accounts first.' },
    'ransomware': {
      plain: 'Software that encrypts everything you own and sells you the key. The modern version steals a copy first, so paying to decrypt does not stop the leak.',
      tech: 'Double/triple extortion: exfiltrate, then encrypt, then threaten disclosure or DDoS. Initial access is overwhelmingly phished credentials, unpatched edge devices, or a compromised supplier. The only reliable control is tested, offline, immutable backups — the 3-2-1-1-0 rule, with the 0 meaning "restore verified".' },
    'cve': { aka: ['cvss', 'vulnerability', 'kev'],
      plain: 'A public serial number for a specific security flaw, plus a severity score. It lets the whole world talk about the same hole in the same words — and it tells you what to patch first.',
      tech: 'CVE = the identifier; CVSS = the 0–10 severity vector; EPSS = probability of exploitation in the wild; CISA KEV = the list of what is already being exploited. Patch by KEV ∪ (high EPSS), not by CVSS alone — most 9.8s are never weaponised.' },
    'supply chain attack': { aka: ['supply chain', 'dependency confusion', 'typosquatting'],
      plain: 'Nobody breaks into you. They break into something you already trust and installed — a library, an update, a browser extension — and ride in with it.',
      tech: 'Compromise upstream of the target: malicious package versions, typosquats, dependency confusion against internal names, build-system compromise (SolarWinds), or a poisoned CI action. Defences: lockfiles with hashes, pinned actions by SHA, SBOMs, provenance attestation (SLSA/Sigstore), and an allowlisted internal registry.' },
    'phishing': { aka: ['social engineering', 'vishing', 'smishing'],
      plain: 'Persuading a person to hand over the keys. Cheaper than any exploit, and now generated at scale in perfect English — or in a cloned voice on the phone.',
      tech: 'Credential harvesting via pretext. AI removed the tell (bad grammar) and added real-time voice cloning for vishing. Technical mitigations that actually hold: phishing-resistant MFA, DMARC enforcement (p=reject), and blocking newly-registered domains at the resolver.' },
    'systemd': { aka: ['daemon', 'service'],
      plain: 'The thing on Linux that starts your programs at boot and restarts them when they crash. If you want something to be running whether or not you are watching, you hand it to systemd.',
      tech: 'The init system and service manager (PID 1). A unit file declares ExecStart, Restart=always, After= ordering and a hardening block (ProtectSystem, NoNewPrivileges, DynamicUser). Timers replace cron with proper logging and dependency ordering; journalctl -u is the log.' },
    'cron': { aka: ['crontab', 'scheduled job'],
      plain: 'The alarm clock. Five numbers say when — minute, hour, day, month, weekday — and the machine runs your command then, forever, whether or not anyone is awake.',
      tech: 'Time-based job scheduler. Fields: m h dom mon dow. Gotchas that bite everyone once: a minimal PATH, no shell profile, times in the daemon\'s timezone (UTC on most CI), and no overlap protection — wrap long jobs in flock. This Codex refreshes on "0 6 */2 * *".' },
    'acid': { aka: ['transaction', 'transactions'],
      plain: 'The promise a serious database makes: a group of changes either all happen or none do, the rules are never broken halfway, two people editing at once do not corrupt each other, and once it says "saved" it survives a power cut.',
      tech: 'Atomicity, Consistency, Isolation, Durability. Isolation levels trade correctness for throughput (read committed → serialisable); Postgres defaults to read committed, so lost updates are yours to prevent. Durability depends on fsync actually reaching the platter — consumer SSDs and SD cards lie about this.' },
    'index': { aka: ['database index', 'indexes'],
      plain: 'The database\'s contents page. Without one it reads every row to answer you; with one it jumps straight there. The cost is that every write has to update the index too.',
      tech: 'Usually a B-tree; GIN/GiST for full-text and arrays, HNSW for vectors. Selectivity decides whether the planner uses it at all. Read EXPLAIN ANALYZE before adding one, and remember composite index column order is left-to-right prefix-matched.' },
    'idempotent': { aka: ['idempotency'],
      plain: 'Doing it twice is the same as doing it once. It matters because networks lie: your request may have succeeded and the reply got lost, so everything retries — and anything that is not idempotent double-charges someone.',
      tech: 'f(f(x)) = f(x). Achieved with client-supplied idempotency keys, upserts, or conditional writes (If-Match/ETag). Every webhook consumer and every payment path needs it, because at-least-once delivery is the only guarantee most systems offer.' },
    'observability': { aka: ['monitoring', 'telemetry', 'tracing'],
      plain: 'Being able to answer "what is it actually doing right now?" without guessing. Logs say what happened, metrics say how much, traces say where the time went.',
      tech: 'The three signals plus OpenTelemetry as the wire format. For agents add four more: tokens spent, tool-call outcomes, step counts, and per-task cost. An unmetered agent is an unbounded invoice — instrument cost before you instrument anything else.' },
    'eval': { aka: ['evals', 'benchmark'],
      plain: 'A repeatable test for something that does not give the same answer twice. You write down what a good outcome looks like, run it after every change, and stop arguing from vibes.',
      tech: 'A fixed dataset + scorer (exact match, rubric-graded LLM judge, or human). Guard against contamination and judge bias; measure the outcome you actually care about, not the proxy. Regression evals in CI are what makes a prompt change safe to ship.' },
    'post-quantum': { aka: ['pqc', 'post quantum', 'harvest now decrypt later'],
      plain: 'Encryption designed to survive a computer that does not exist yet. It matters today because anything secret and long-lived can be recorded now and unlocked later — so the migration has to start before the machine arrives.',
      tech: 'NIST-standardised ML-KEM (Kyber, FIPS 203) and ML-DSA (Dilithium, FIPS 204), with hybrid X25519+ML-KEM key agreement already default in major browsers and TLS stacks. Signatures migrate slower than key exchange. Inventory long-lived secrets first — that is the actual project.' },
    'edge': { aka: ['edge function', 'cdn'],
      plain: 'Your code copied to hundreds of cities so it runs near whoever asked. Instant to reach, but tiny: no long jobs, small memory, and it forgets everything between requests.',
      tech: 'V8 isolates at PoPs (Cloudflare Workers, Vercel Edge). Sub-millisecond cold start, but no full Node API, hard CPU-time caps and no persistent local state — pair with a durable store. The 10-second wall that kills long scrapers lives here.' },
    'webhook': { art: 'images/webhook-vs-polling.svg', aka: ['polling'],
      plain: 'A service ringing your doorbell when something happens, instead of you knocking on its door every minute to ask. Cheaper, faster, and it needs somewhere always awake to answer — which is the whole argument for the node.',
      tech: 'Server-initiated HTTP callback. Requirements the tutorials skip: verify the HMAC signature, respond 2xx in milliseconds and process async, deduplicate on delivery ID (at-least-once), and handle replay with a timestamp window.' },
    'git': { art: 'images/git-graph.svg', aka: ['commit', 'rebase', 'branch'],
      plain: 'A project folder with perfect memory. Every save is a numbered snapshot you can return to forever, and branches let you keep several drafts alive at once.',
      tech: 'A content-addressed DAG of commits, each a tree snapshot + parent pointer(s), identified by SHA. Branches are movable refs. Rebase replays commits onto a new base with new hashes; merge preserves both histories. Committed is saved — pushed is safe.' },
    'api': { aka: ['rest', 'endpoint'],
      plain: 'A service\'s front counter for machines. You send a request in an agreed shape, you get an answer in an agreed shape, and a key proves you are allowed to ask.',
      tech: 'Usually HTTP+JSON over REST semantics: verbs, resource paths, status codes, pagination, rate limits and idempotency keys. The key is a bearer credential — whoever holds it is you, so it belongs in an environment variable and never in the repo.' },
    'kernel': { aka: ['linux', 'process', 'chmod', 'permissions'],
      plain: 'The part of the operating system that actually touches the hardware. Your programs never speak to the disk or the network directly — they ask the kernel, and the kernel decides whether they are allowed.',
      tech: 'Ring-0 code mediating hardware via syscalls; userspace runs unprivileged. Processes carry uid/gid; files carry mode bits (rwx for user/group/other — 644 for data, 600 for secrets, 755 for executables). Least privilege on a home node is mostly just: do not run it as root.' },
    'nat': { aka: ['cgnat', 'port forward', 'firewall'],
      plain: 'Why your home devices share one public address. It is also, by accident, a firewall: nothing outside can reach in unless you deliberately open a hole — and opening holes is how home servers get owned.',
      tech: 'Network Address Translation maps many private addresses (RFC 1918) onto one public IP by port. Carrier-grade NAT (RFC 6598, 100.64/10) shares a public IP across thousands of subscribers, which breaks inbound entirely. The modern answer is not port-forwarding but an overlay: WireGuard, Tailscale, or a reverse tunnel.' },
    'reverse proxy': { aka: ['nginx', 'caddy', 'load balancer'],
      plain: 'A doorman in front of your services. Everything arrives at one address; the doorman decides which room it belongs to, handles the padlock, and turns away what should not be there.',
      tech: 'Terminates TLS and routes by host/path to upstreams — nginx, Caddy (automatic ACME), Traefik. Also where you put rate limits, request-size caps, auth headers and access logs. On a single node it is the difference between "some ports are open" and "one hardened front door".' },
    'sbom': { aka: ['software bill of materials'],
      plain: 'The ingredients list for your software. When a flaw is announced in some library at midnight, the difference between "we are fine" and a week of panic is having written down what you actually shipped.',
      tech: 'A machine-readable dependency inventory (CycloneDX or SPDX), generated in CI per build and stored with the artifact. Pair with provenance attestation and continuous VEX matching against advisory feeds; otherwise it is a file nobody queries.' },
    'gdpr': { aka: ['data protection', 'dpia', 'personal data'],
      plain: 'The law that says personal information belongs to the person it is about. You need a reason to hold it, you may only keep what you need, only as long as you need it, and you must be able to say where it went.',
      tech: 'UK GDPR + DPA 2018: lawful basis, purpose limitation, data minimisation, storage limitation, and Article 30 records. A DPIA is mandatory for high-risk processing — which includes most automated decision-making. For agents: log what left the building, where it was processed, and under what basis.' },
    'ai act': { aka: ['eu ai act', 'ai regulation', 'ai governance'],
      plain: 'Europe\'s rulebook for AI, sorted by how much harm a use could do rather than how clever the model is. Unacceptable uses are banned outright; high-risk ones carry real paperwork; a chatbot mostly just has to admit it is one.',
      tech: 'Risk-tiered: prohibited, high-risk (Annex III — includes employment, credit, essential services), limited-risk transparency duties, and separate GPAI obligations. Extraterritorial where output is used in the EU. ISO/IEC 42001 and the NIST AI RMF are the management-system answers auditors expect.' },
    'ollama': { aka: ['llama.cpp', 'gguf', 'local model', 'open weights', 'open-weights'],
      plain: 'The easiest way to run a model on your own machine. One command pulls the weights and gives you a local endpoint — no account, no per-token bill, and nothing you type ever leaves the house.',
      tech: 'A llama.cpp wrapper with a model registry, GGUF quantisation and an OpenAI-compatible API on :11434. On a 16GB Pi 5, 3–4B models at Q4_K_M run at a usable few tokens/sec on CPU; anything larger is bandwidth-starved. Free per use, and the privacy boundary is physical.' },
    'test-time compute': { aka: ['reasoning model', 'chain of thought', 'thinking'],
      plain: 'Letting a model think for longer on a hard question instead of building a bigger model. It writes out its working before answering, and on maths, code and planning that alone is worth a generation of scale.',
      tech: 'Inference-time scaling: extended chain-of-thought, self-consistency sampling, search over candidate traces, verifier-guided selection. Trades latency and output tokens for accuracy — and moves a large share of spend from training capex to serving cost.' },
    'hbm': { art: 'images/h100-photo.png', aka: ['memory bandwidth', 'cowos', 'packaging'],
      plain: 'The stacked memory glued right next to an AI chip. It is the real bottleneck of the whole industry: not how fast the chip can calculate, but how fast you can feed it — and only a handful of factories on earth can build it.',
      tech: 'High Bandwidth Memory — DRAM dies stacked with through-silicon vias, co-packaged on an interposer (TSMC CoWoS). Token generation is memory-bandwidth-bound, not FLOP-bound, so HBM stacks and advanced packaging capacity — not lithography alone — gate accelerator supply.' },
    'euv': { art: 'images/euv-photo.jpg', aka: ['lithography', 'asml', 'tsmc', 'fab'],
      plain: 'The machine that prints the finest circuits on earth, using light so extreme it is made by vaporising tin droplets with a laser. One company builds them, they cost as much as a jumbo jet, and every advanced chip in the world passes through one.',
      tech: 'Extreme Ultraviolet lithography at 13.5nm wavelength — ASML monopoly, High-NA at ~$380M/tool. Combined with the TSMC leading-edge node concentration and HBM/CoWoS capacity, this is the physical chokepoint the entire export-control regime is built around.' },
    'diffusion': { art: 'images/diffusion.svg',
      plain: 'How images are generated: start from pure static, and repeatedly remove a little of the noise until a picture is standing there. The model was trained by watching pictures dissolve into static, backwards.',
      tech: 'Denoising diffusion (DDPM ε-prediction), increasingly with transformer backbones (DiT) and flow-matching objectives; latent diffusion runs the process in a compressed VAE space for tractability. Sampling steps trade quality for latency; distillation collapses 50 steps to 4.' },
    'orchestration': { art: 'images/orchestration.svg', aka: ['multi-agent', 'multi agent', 'swarm'],
      plain: 'Conducting many agents and tools into one piece of work — deciding who does what, in what order, and who checks the result. It is management, applied to software that thinks.',
      tech: 'Coordination patterns: supervisor/worker, pipeline, blackboard, debate. Cost and error both compound with agent count, so the durable designs keep fan-out shallow, make every step verifiable, and put a deterministic script — not a model — in charge of control flow.' }
  };

  /* which world a layer belongs to, for doors with no authored home */
  var SEC2WORLD = {
    l1: 'silicon', l2: 'mind', l3: 'mind', l4: 'mind', l5: 'craft', l6: 'craft',
    l7: 'silicon', l8: 'craft', l9: 'world', l10: 'world', l11: 'world',
    l12: 'shield', l13: 'shield', l14: 'mind', l15: 'wire', l16: 'wire',
    l17: 'craft', l18: 'craft', l19: 'shield', l20: 'world', l21: 'mind',
    l22: 'mind', l23: 'world', l24: 'craft', l25: 'craft', l26: 'world',
    deep: 'shield', gloss: 'craft', live: 'world'
  };
  var WORLDRGB = {
    mind: '87,179,156', wire: '159,180,216', silicon: '223,163,43',
    shield: '207,111,87', craft: '183,171,99', world: '231,226,212'
  };
  var WORLDNAME = {
    mind: 'the world of minds', wire: 'the world of wires',
    silicon: 'the world of silicon', shield: 'the world of shields',
    craft: 'the world of the craft', world: 'the wider world'
  };

  var door = (function () {
    var box, room, index = null, keys = [], dmeta = {}, walked = [];

    /* ---- build the searchable index from LEX + the page itself ---- */
    function build() {
      index = {};
      function add(term, entry) {
        var k = norm(term);
        if (!k) return;
        if (!index[k]) index[k] = entry;
      }
      Object.keys(LEX).forEach(function (k) {
        var e = LEX[k]; e.term = e.term || k;
        add(k, e);
        (e.aka || []).forEach(function (a) { add(a, e); });
      });
      /* the sixty-second glossary becomes doors too */
      $$('#gloss .gloss p').forEach(function (p) {
        var b = $('b', p); if (!b) return;
        var term = b.textContent.trim();
        var line = p.textContent.replace(b.textContent, '').replace(/^\s*[—–-]\s*/, '').trim();
        var k = norm(term);
        if (index[k]) { if (!index[k].plain) index[k].plain = line; return; }
        add(term, { term: term, plain: line, fromGloss: true });
      });
      keys = Object.keys(index).sort(function (a, b) { return b.length - a.length; });
    }

    function norm(s) {
      return String(s || '').toLowerCase()
        .replace(/[‘’“”]/g, "'")
        .replace(/[^a-z0-9+/.\- ]+/g, ' ')
        .replace(/\s+/g, ' ').trim();
    }

    function lookup(raw) {
      if (!index) build();
      var k = norm(raw);
      if (!k) return null;
      if (index[k]) return index[k];
      /* plurals and simple inflections */
      var tries = [k.replace(/ies$/, 'y'), k.replace(/es$/, ''), k.replace(/s$/, ''),
                   k.replace(/ing$/, ''), k.replace(/ed$/, ''), k + 's'];
      for (var i = 0; i < tries.length; i++) if (index[tries[i]]) return index[tries[i]];
      return null;
    }

    function near(raw) {
      if (!index) build();
      var k = norm(raw); if (!k) return [];
      return keys.filter(function (t) {
        return t.indexOf(k) >= 0 || (k.length > 3 && k.indexOf(t) >= 0);
      }).slice(0, 6);
    }

    /* ---- pull supporting material out of the layers ---- */
    function cardsFor(term) {
      var t = norm(term), hits = [];
      $$('details.card').forEach(function (c) {
        var sum = $('summary', c); if (!sum) return;
        var head = norm(sum.textContent);
        var score = head.indexOf(t) >= 0 ? 2 : (norm(c.textContent).indexOf(t) >= 0 ? 1 : 0);
        if (score) hits.push({ el: c, score: score });
      });
      hits.sort(function (a, b) { return b.score - a.score; });
      return hits.slice(0, 3).map(function (h) {
        var sec = h.el.closest('section');
        var b = $('summary b', h.el);
        return {
          id: h.el.id || h.el.getAttribute('data-card') || '',
          el: h.el,
          label: (b ? b.textContent.trim() : 'the card'),
          layer: sec ? ($('.lnum', sec) ? $('.lnum', sec).textContent.trim() : '') : ''
        };
      });
    }

    function make() {
      box = document.createElement('div');
      box.id = 'door';
      box.setAttribute('role', 'dialog');
      box.setAttribute('aria-modal', 'true');
      box.innerHTML =
        '<div class="veil"></div>' +
        '<canvas class="warp" aria-hidden="true"></canvas>' +
        '<div class="beam"></div>' +
        '<div class="leaf l"></div><div class="leaf r"></div>' +
        '<div class="room"><div class="panel"></div></div>';
      document.body.appendChild(box);
      room = $('.panel', box);
      $('.veil', box).addEventListener('click', shut);
      box.addEventListener('click', function (e) {
        if (e.target.closest('.shut')) shut();
        var n = e.target.closest('button[data-t]');
        if (n) open(n.getAttribute('data-t'));
        var j = e.target.closest('.jump a');
        if (j) {
          var t = document.getElementById(j.getAttribute('data-go'));
          shut();
          if (t) {
            if (t.tagName === 'DETAILS') t.open = true;
            setTimeout(function () { t.scrollIntoView({ behavior: STILL ? 'auto' : 'smooth', block: 'center' }); }, 60);
          }
          e.preventDefault();
        }
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && box.classList.contains('on')) { e.preventDefault(); shut(); }
      });
    }

    /* the starfield burst behind the opening door — one-shot, self-terminating */
    function warp(ox, oy, rgb) {
      if (STILL) return;
      var c = $('.warp', box); if (!c) return;
      var x = c.getContext('2d');
      var w = c.width = window.innerWidth, h = c.height = window.innerHeight;
      ox = ox == null ? w / 2 : ox; oy = oy == null ? h / 2 : oy;
      var streaks = [], i;
      for (i = 0; i < 240; i++) {
        streaks.push({
          a: Math.random() * 6.283, r: Math.random() * 30,
          v: 4 + Math.random() * 16, l: 26 + Math.random() * 110
        });
      }
      var t0 = null;
      function fr(now) {
        if (!t0) t0 = now;
        var t = (now - t0) / 900;
        if (t >= 1 || !box.classList.contains('on')) { x.clearRect(0, 0, w, h); return; }
        x.clearRect(0, 0, w, h);
        x.lineWidth = 1.4;
        var fade = t < .2 ? t / .2 : 1 - (t - .2) / .8;
        for (i = 0; i < streaks.length; i++) {
          var s = streaks[i];
          s.r += s.v * (1 + t * 4);
          var ca = Math.cos(s.a), sa = Math.sin(s.a);
          x.strokeStyle = 'rgba(' + rgb + ',' + (fade * .5).toFixed(3) + ')';
          x.beginPath();
          x.moveTo(ox + ca * s.r, oy + sa * s.r);
          x.lineTo(ox + ca * (s.r + s.l * (0.4 + t)), oy + sa * (s.r + s.l * (0.4 + t)));
          x.stroke();
        }
        requestAnimationFrame(fr);
      }
      requestAnimationFrame(fr);
    }

    /* fold assets/doors.json in when it arrives — metadata for known
       doors, brand-new doors for keys the index has never seen */
    function absorb(meta) {
      if (!index) build();
      var added = 0;
      Object.keys(meta).forEach(function (k) {
        if (k.charAt(0) === '_') return;
        var nk = norm(k);
        if (!nk) return;
        dmeta[nk] = meta[k];
        if (!index[nk]) {
          index[nk] = { term: k, plain: '', fromMeta: true };
          keys.push(nk);
          added += 1;
        }
      });
      if (added) keys.sort(function (a, b) { return b.length - a.length; });
      return keys.length;
    }

    function metaFor(term, e) {
      var m = dmeta[norm(term)];
      if (!m && e) m = dmeta[norm(e.term)];
      if (!m && e && e.aka) {
        for (var i = 0; i < e.aka.length; i++) {
          if (dmeta[norm(e.aka[i])]) { m = dmeta[norm(e.aka[i])]; break; }
        }
      }
      return m || null;
    }

    function open(raw, origin) {
      if (!box) make();
      /* a phrase candidate can carry the punctuation that followed it
         ("tokens —"); the index ignores that, so the heading should too */
      var term = String(raw || '')
        .replace(/^[^A-Za-z0-9]+/, '')
        .replace(/[^A-Za-z0-9)]+$/, '')
        .replace(/\s+/g, ' ')
        .trim();
      var e = lookup(term);
      var meta = metaFor(term, e);
      /* The heading is the word they actually double-clicked — being shown
         "mfa" after clicking "passkey" is disorienting. The entry's own name
         and its other spellings go in the line underneath. */
      var name = term;
      var also = e
        ? [e.term].concat(e.aka || []).filter(function (a) {
            return a && a.toLowerCase() !== term.toLowerCase();
          })
        : [];
      var cards = e || term.length > 2 ? cardsFor(name) : [];

      /* which world this door leads to */
      var world = (meta && meta.world) || '';
      if (!world && cards.length) {
        var sec = cards[0].el.closest('section');
        world = (sec && SEC2WORLD[sec.id]) || '';
      }
      if (!world) world = 'mind';

      var art = '';
      var artSrc = (meta && meta.art) || (e && e.art) || '';
      if (artSrc) {
        art = '<figure><img src="' + esc(artSrc) + '" alt="' + esc(name) + '" loading="lazy">' +
              '<figcaption>from the layers — tap to open it full screen</figcaption></figure>';
      } else if (cards.length && $('figure.fig img', cards[0].el)) {
        var im = $('figure.fig img', cards[0].el);
        art = '<figure><img src="' + esc(im.getAttribute('src')) + '" alt="' + esc(im.alt) + '" loading="lazy">' +
              '<figcaption>' + esc((($('figcaption', im.closest('figure')) || {}).textContent || '').trim()) + '</figcaption></figure>';
      } else {
        art = '<figure>' + glyph(name, 720, 420, true, world) +
              '<figcaption>an emblem drawn for this word alone</figcaption></figure>';
      }

      var plain = e && e.plain ? e.plain : '';
      var tech = e && e.tech ? e.tech : '';
      if (!tech && cards.length) {
        var tp = $('.tech', cards[0].el);
        if (tp) {
          tech = tp.textContent.trim();
          if (tech.length > 460) tech = tech.slice(0, 455).replace(/\s+\S*$/, '') + ' …';
        }
      }
      if (!plain && cards.length) {
        var pp = $('.plain', cards[0].el);
        if (pp) {
          plain = pp.textContent.trim();
          if (plain.length > 420) plain = plain.slice(0, 415).replace(/\s+\S*$/, '') + ' …';
        }
      }

      /* neighboring doors: authored kin first, fuzzy matches as the fallback */
      var kin = [];
      if (meta && meta.kin) {
        kin = meta.kin.filter(function (k2) {
          return norm(k2) !== norm(term) && !!lookup(k2);
        });
      }
      if (!kin.length) {
        kin = near(term).filter(function (k2) { return norm(k2) !== norm(term); }).slice(0, 5);
      }
      kin = kin.slice(0, 6);

      var found = plain || tech || (meta && meta.why);
      var body;
      if (!found) {
        var alts = near(term);
        body =
          '<div class="top"><div class="word"><span class="k">no entry — yet</span>' +
          '<h3>' + esc(term) + '</h3></div>' +
          '<button class="shut" aria-label="Close">✕</button></div>' +
          '<div class="none">This word has no door of its own. The Codex holds <b>' +
          (keys.length) + '</b> of them, and the caretaker adds more every two days.' +
          (alts.length
            ? '<div class="near">' + alts.map(function (a) {
                return '<button data-t="' + esc(a) + '">' + esc(a) + '</button>';
              }).join('') + '</div>'
            : '') + '</div>';
        box.className = '';
      } else {
        /* the walked trail — the doors that led here */
        var crumbs = walked.filter(function (w) { return norm(w) !== norm(term); }).slice(-3);
        walked.push(term);
        if (walked.length > 12) walked.shift();

        body =
          '<div class="top"><div class="word">' +
          '<span class="k">a door opens on · ' + esc(WORLDNAME[world] || world) + '</span>' +
          '<h3>' + esc(name) + '</h3>' +
          (also.length
            ? '<p class="aka">also filed as ' + esc(also.slice(0, 4).join(' · ')) + '</p>' : '') +
          '</div><button class="shut" aria-label="Close">✕</button></div>' +
          '<div class="duo">' +
            '<div class="artside">' + art + '</div>' +
            '<div class="txtside">' +
              (plain ? '<p class="plain">' + esc(plain) + '</p>' : '') +
              (tech ? '<p class="tech">' + esc(tech) + '</p>' : '') +
              (meta && meta.why
                ? '<p class="why"><span>why it matters</span>' + esc(meta.why) + '</p>' : '') +
              (cards.length
                ? '<div class="jump"><span class="sec">where you met it</span>' + cards.map(function (c) {
                    return '<a href="#' + esc(c.id) + '" data-go="' + esc(c.id) + '">' +
                           esc(c.layer || 'open') + ' · ' + esc(c.label) + '</a>';
                  }).join('') + '</div>'
                : '') +
              (kin.length
                ? '<div class="kin"><span class="sec">neighboring doors</span>' + kin.map(function (k2) {
                    return '<button data-t="' + esc(k2) + '">' + esc(k2) + ' →</button>';
                  }).join('') + '</div>'
                : '') +
              (crumbs.length
                ? '<div class="crumbs"><span class="sec">the way you came</span>' + crumbs.map(function (w) {
                    return '<button data-t="' + esc(w) + '">← ' + esc(w) + '</button>';
                  }).join('') + '</div>'
                : '') +
            '</div>' +
          '</div>';
        box.className = 'w-' + world;
      }

      /* the iris opens where the word was double-clicked, and grows
         just far enough to swallow the farthest corner of the screen */
      var vw = window.innerWidth, vh = window.innerHeight;
      var ox2 = origin && origin.x != null ? origin.x : vw / 2;
      var oy2 = origin && origin.y != null ? origin.y : vh * .45;
      var irad = Math.sqrt(
        Math.pow(Math.max(ox2, vw - ox2), 2) + Math.pow(Math.max(oy2, vh - oy2), 2)
      ) * 1.05;
      box.style.setProperty('--ox', ox2.toFixed(0) + 'px');
      box.style.setProperty('--oy', oy2.toFixed(0) + 'px');
      box.style.setProperty('--irad', irad.toFixed(0) + 'px');

      room.innerHTML = body;
      box.classList.add('on');
      document.documentElement.style.overflow = 'hidden';
      /* replay the whole arrival on every open */
      $$('.leaf', box).forEach(function (l) {
        l.style.animation = 'none'; void l.offsetWidth; l.style.animation = '';
      });
      var beam = $('.beam', box); beam.style.animation = 'none'; void beam.offsetWidth; beam.style.animation = '';
      var rm = $('.room', box); rm.style.animation = 'none'; void rm.offsetWidth; rm.style.animation = '';
      rm.scrollTop = 0;
      box.style.animation = 'none'; void box.offsetWidth; box.style.animation = '';
      warp(origin && origin.x, origin && origin.y, WORLDRGB[world] || WORLDRGB.mind);
      var sh = $('.shut', box); if (sh) sh.focus();
    }

    function shut() {
      if (!box) return;
      box.classList.remove('on');
      document.documentElement.style.overflow = '';
      var s = window.getSelection && window.getSelection();
      if (s && s.removeAllRanges) s.removeAllRanges();
    }

    return {
      open: open, shut: shut, absorb: absorb,
      has: function (t) { return !!lookup(t); },
      count: function () { if (!index) build(); return keys.length; }
    };
  })();

  /* ---- catching the double-click / double-tap ---- */
  function wireDoor() {
    function noGo(t) {
      return !t || t.closest('a,button,summary,input,textarea,pre,code,#lens,#door,#seek,.filters');
    }

    function contextWords() {
      var sel = window.getSelection();
      if (!sel || !sel.rangeCount || sel.isCollapsed) return null;
      var word = sel.toString().trim();
      if (!word || word.length > 44 || !/[a-z]/i.test(word)) return null;
      var node = sel.anchorNode, before = '', after = '';
      if (node && node.nodeType === 3) {
        var t = node.textContent;
        var a = Math.min(sel.anchorOffset, sel.focusOffset);
        var b = Math.max(sel.anchorOffset, sel.focusOffset);
        before = t.slice(Math.max(0, a - 42), a);
        after = t.slice(b, b + 42);
      }
      var pre = before.trim().split(/\s+/).filter(Boolean);
      var post = after.trim().split(/\s+/).filter(Boolean);
      var p1 = pre.length ? pre[pre.length - 1] : '';
      var p2 = pre.length > 1 ? pre[pre.length - 2] : '';
      var n1 = post.length ? post[0] : '';
      var n2 = post.length > 1 ? post[1] : '';
      /* longest phrase first — "context window" must beat "context" */
      return [
        [p2, p1, word].filter(Boolean).join(' '),
        [p1, word, n1].filter(Boolean).join(' '),
        [word, n1, n2].filter(Boolean).join(' '),
        [p1, word].filter(Boolean).join(' '),
        [word, n1].filter(Boolean).join(' '),
        word
      ];
    }

    /* Longest phrase wins: "context window" must beat "context", and
       "prompt injection" must beat "prompt". Only the bare word is
       allowed to fall through to the no-entry panel. */
    function fire(target) {
      if (noGo(target)) return;
      var cands = contextWords();
      if (!cands) return;
      /* the iris will open exactly where the word sits — read the
         selection rect now, before anything clears the ranges */
      var origin = null;
      try {
        var sel = window.getSelection();
        if (sel && sel.rangeCount) {
          var r = sel.getRangeAt(0).getBoundingClientRect();
          if (r && (r.width || r.height)) origin = { x: r.left + r.width / 2, y: r.top + r.height / 2 };
        }
      } catch (err) {}
      var bare = cands[cands.length - 1];
      for (var i = 0; i < cands.length - 1; i++) {
        if (cands[i] && door.has(cands[i])) { door.open(cands[i], origin); return; }
      }
      door.open(bare, origin);
    }

    document.addEventListener('dblclick', function (e) { fire(e.target); });

    /* double-tap for touch, without stealing the browser's own gestures */
    var last = 0, lx = 0, ly = 0;
    document.addEventListener('touchend', function (e) {
      if (!e.changedTouches || e.changedTouches.length !== 1) return;
      var t = e.changedTouches[0], now = Date.now();
      if (now - last < 340 && Math.abs(t.clientX - lx) < 26 && Math.abs(t.clientY - ly) < 26) {
        last = 0;
        setTimeout(function () { fire(document.elementFromPoint(t.clientX, t.clientY)); }, 30);
      } else { last = now; lx = t.clientX; ly = t.clientY; }
    }, { passive: true });

    /* the invitation — shown once, then never again */
    if (!store.get('codex.door.taught')) {
      var tip = document.createElement('div');
      tip.className = 'dtip';
      tip.textContent = 'double-click any word';
      document.body.appendChild(tip);
      var lede = $('#l1 .lede') || $('header .sub');
      if (lede) {
        var r = lede.getBoundingClientRect();
        tip.style.left = (r.left + r.width / 2) + 'px';
        tip.style.top = (r.top + window.pageYOffset + r.height) + 'px';
        tip.style.position = 'absolute';
        setTimeout(function () { tip.classList.add('on'); }, 1400);
        setTimeout(function () { tip.classList.remove('on'); }, 7000);
        setTimeout(function () { tip.remove(); }, 8200);
      }
      store.set('codex.door.taught', '1');
    }
  }

  /* ==========================================================
     8 · THE SEEKER — press / or ⌘K
     ========================================================== */
  function seek() {
    var box = document.createElement('div');
    box.id = 'seek';
    box.innerHTML =
      '<div class="veil"></div>' +
      '<div class="box">' +
        '<input type="search" placeholder="jump to a layer, a card, a word…" ' +
               'aria-label="Search the Codex" autocomplete="off" spellcheck="false">' +
        '<div class="hits"></div>' +
        '<div class="foot">↑↓ move · ↵ open · esc close</div>' +
      '</div>';
    document.body.appendChild(box);
    var input = $('input', box), hits = $('.hits', box), rows = [], sel = 0;

    var items = [];
    $$('section[id]').forEach(function (s) {
      var h = $('h2', s), n = $('.lnum', s);
      if (h) items.push({ t: h.textContent.trim(), s: n ? n.textContent.trim() : '', id: s.id, kind: 'layer' });
      $$('details.card', s).forEach(function (c) {
        var b = $('summary b', c), sp = $('summary span', c);
        if (b) items.push({
          t: b.textContent.trim(),
          s: (n ? n.textContent.trim() + ' · ' : '') + (sp ? sp.textContent.trim() : ''),
          id: c.id || c.getAttribute('data-card') || s.id, kind: 'card', el: c
        });
      });
    });

    function paint(q) {
      var qq = q.toLowerCase().trim();
      rows = (!qq ? items.slice(0, 12) : items.filter(function (i) {
        return (i.t + ' ' + i.s).toLowerCase().indexOf(qq) >= 0;
      }).slice(0, 40));
      sel = 0;
      hits.innerHTML = rows.map(function (i, n) {
        return '<button class="hit' + (n === 0 ? ' sel' : '') + '" data-n="' + n + '">' +
          esc(i.t) + '<small>' + esc(i.s) + '</small></button>';
      }).join('') || '<div class="foot">nothing under that word — try double-clicking it in the text instead</div>';
    }
    function jump(i) {
      var it = rows[i]; if (!it) return;
      close();
      var el = it.el || document.getElementById(it.id);
      if (!el) return;
      if (el.tagName === 'DETAILS') el.open = true;
      setTimeout(function () { el.scrollIntoView({ behavior: STILL ? 'auto' : 'smooth', block: 'start' }); }, 50);
    }
    function open() {
      box.classList.add('on'); document.documentElement.style.overflow = 'hidden';
      input.value = ''; paint(''); input.focus();
    }
    function close() { box.classList.remove('on'); document.documentElement.style.overflow = ''; }

    input.addEventListener('input', function () { paint(input.value); });
    hits.addEventListener('click', function (e) {
      var b = e.target.closest('.hit'); if (b) jump(parseInt(b.getAttribute('data-n'), 10));
    });
    $('.veil', box).addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      var on = box.classList.contains('on');
      var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || ''));
      if (!on && ((e.key === '/' && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k'))) {
        e.preventDefault(); open(); return;
      }
      if (!on) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        var els = $$('.hit', hits); if (!els.length) return;
        els[sel] && els[sel].classList.remove('sel');
        sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + els.length) % els.length;
        els[sel].classList.add('sel'); els[sel].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') { e.preventDefault(); jump(sel); }
    });

    var btn = document.createElement('button');
    btn.className = 'lensbtn';
    btn.style.cssText = 'width:46px;height:46px;border-radius:50%';
    btn.setAttribute('aria-label', 'Search the Codex');
    btn.textContent = '⌕';
    btn.addEventListener('click', open);
    var dock = $('.sizer'); if (dock) dock.appendChild(btn);
  }

  /* ==========================================================
     9 · boot
     ========================================================== */
  function boot() {
    field(); rail(); trail(); reveal(); wireLens(); marks(); pulse();
    atlas(); minimap(); settleCards(); copycode(); wireDoor(); seek();

    /* the door count, printed where the header promises it */
    var dc = $('#doorcount');
    if (dc) dc.textContent = door.count();

    /* fold in the door metadata — worlds, why-lines, kin — when it lands */
    fetch('assets/doors.json')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d) return;
        var total = door.absorb(d);
        if (dc && total) dc.textContent = total;
      })
      .catch(function () {});

    /* deep links to cards open them */
    function openHash() {
      var h = location.hash.slice(1); if (!h) return;
      var el = document.getElementById(h);
      if (el && el.tagName === 'DETAILS') el.open = true;
    }
    window.addEventListener('hashchange', openHash);
    openHash();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
