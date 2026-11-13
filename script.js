(function () {
  document.documentElement.classList.add('js');

  // Load sequence: the reconciliation checks tick off one after another.
  var rows = document.querySelectorAll('.ledger-table tbody tr');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  rows.forEach(function (row, i) {
    if (reduce) { row.classList.add('is-checked'); return; }
    setTimeout(function () { row.classList.add('is-checked'); }, 400 + i * 260);
  });

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
