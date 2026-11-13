(function () {
  document.documentElement.classList.add('js');

  // The reconciliation checks tick off one after another when the panel scrolls into view.
  var ledger = document.querySelector('.ledger');
  var rows = document.querySelectorAll('.ledger-table tbody tr');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function tick() {
    rows.forEach(function (row, i) {
      if (reduce) { row.classList.add('is-checked'); return; }
      setTimeout(function () { row.classList.add('is-checked'); }, 150 + i * 260);
    });
  }

  if (!ledger || reduce || !('IntersectionObserver' in window)) {
    tick();
  } else {
    var observer = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { tick(); observer.disconnect(); }
    }, { threshold: 0.4 });
    observer.observe(ledger);
    // Safety net: never leave the checks dimmed if the panel is not scrolled to.
    setTimeout(tick, 8000);
  }

  // Case study filters.
  var buttons = document.querySelectorAll('.filter');
  var cards = document.querySelectorAll('.card');
  var status = document.getElementById('filter-status');

  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      var filter = button.getAttribute('data-filter');
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
      var shown = 0;
      cards.forEach(function (card) {
        var tags = card.getAttribute('data-tags').split(' ');
        var match = filter === 'all' || tags.indexOf(filter) !== -1;
        card.hidden = !match;
        if (match) { shown += 1; }
      });
      status.textContent = 'Showing ' + shown + ' case ' + (shown === 1 ? 'study' : 'studies') + '.';
    });
  });
})();
