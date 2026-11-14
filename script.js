(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // ---------- Header: shadow once the page scrolls ----------
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (header) { header.classList.toggle('is-scrolled', window.scrollY > 8); }
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------- Mobile navigation ----------
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  function setMenu(open) {
    if (!toggle || !nav) { return; }
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setMenu(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (!header.contains(e.target)) { setMenu(false); }
    });
    window.matchMedia('(min-width: 56.01rem)').addEventListener('change', function (m) {
      if (m.matches) { setMenu(false); }
    });
  }

  // ---------- Scroll spy: mark the nav link for the section in view ----------
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-list a[href^="#"]'));
  if (hasIO && navLinks.length) {
    var byId = {};
    navLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        navLinks.forEach(function (a) { a.removeAttribute('aria-current'); });
        var link = byId[entry.target.id];
        if (link) { link.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) { spy.observe(section); }
    });
  }

  // ---------- Reveal on scroll ----------
  var revealables = document.querySelectorAll('[data-reveal]');
  if (reduce || !hasIO) {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { revealer.observe(el); });
    // Safety net: never leave content hidden.
    setTimeout(function () { revealables.forEach(function (el) { el.classList.add('is-visible'); }); }, 6000);
  }

  // ---------- Count-up for the verified figures in the stats strip ----------
  var counters = document.querySelectorAll('[data-count]');
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target) || reduce) { return; }
    var start = null;
    var duration = 1100;
    function frame(ts) {
      if (start === null) { start = ts; }
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = String(Math.round(target * eased));
      if (p < 1) { requestAnimationFrame(frame); }
    }
    el.textContent = '0';
    requestAnimationFrame(frame);
  }
  if (counters.length && hasIO && !reduce) {
    var counterIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { countUp(entry.target); counterIO.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { counterIO.observe(el); });
  }

  // ---------- Reconciliation ledger: checks tick off in turn ----------
  var ledger = document.querySelector('.ledger');
  var rows = document.querySelectorAll('.ledger-table tbody tr');
  var ticked = false;
  function tick() {
    if (ticked) { return; }
    ticked = true;
    rows.forEach(function (row, i) {
      if (reduce) { row.classList.add('is-checked'); return; }
      setTimeout(function () { row.classList.add('is-checked'); }, 200 + i * 260);
    });
  }
  if (ledger) {
    if (reduce || !hasIO) {
      tick();
    } else {
      var ledgerIO = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { tick(); ledgerIO.disconnect(); }
      }, { threshold: 0.4 });
      ledgerIO.observe(ledger);
      setTimeout(tick, 8000);
    }
  }

  // ---------- Case study filters ----------
  var buttons = document.querySelectorAll('.filter');
  var cards = document.querySelectorAll('.card');
  var status = document.getElementById('filter-status');
  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      var filter = button.getAttribute('data-filter');
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
      var shown = 0;
      cards.forEach(function (card) {
        var tags = (card.getAttribute('data-tags') || '').split(' ');
        var match = filter === 'all' || tags.indexOf(filter) !== -1;
        var wasHidden = card.hidden;
        card.hidden = !match;
        card.classList.add('is-visible');
        if (match) {
          shown += 1;
          if (wasHidden && !reduce) {
            card.classList.remove('is-entering');
            void card.offsetWidth; // restart the entrance animation
            card.classList.add('is-entering');
          }
        }
      });
      if (status) {
        status.textContent = 'Showing ' + shown + ' case ' + (shown === 1 ? 'study' : 'studies') + '.';
      }
      // Hide a tier heading when the filter leaves its grid empty.
      document.querySelectorAll('.cards-subhead').forEach(function (head) {
        var grid = head.nextElementSibling;
        var any = grid && Array.prototype.some.call(grid.querySelectorAll('.card'), function (c) { return !c.hidden; });
        head.hidden = !any;
        if (any) { head.classList.add('is-visible'); }
      });
    });
  });

  // ---------- Case study pages: highlight the current step in the contents ----------
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.cs-toc a'));
  if (hasIO && tocLinks.length) {
    var tocIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        tocLinks.forEach(function (a) {
          a.toggleAttribute('aria-current', a.getAttribute('href') === '#' + entry.target.id);
          if (a.hasAttribute('aria-current')) { a.setAttribute('aria-current', 'true'); }
        });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    tocLinks.forEach(function (a) {
      var target = document.getElementById(a.getAttribute('href').slice(1));
      if (target) { tocIO.observe(target); }
    });
  }
})();
