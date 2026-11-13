(function () {
  document.documentElement.classList.add('js');

  // Load sequence: the reconciliation checks tick off one after another.
  var rows = document.querySelectorAll('.ledger-table tbody tr');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  rows.forEach(function (row, i) {
    if (reduce) { row.classList.add('is-checked'); return; }
    setTimeout(function () { row.classList.add('is-checked'); }, 350 + i * 260);
  });

  // Case study filters.
  var buttons = document.querySelectorAll('.filter');
  var items = document.querySelectorAll('.work-item');
  var status = document.getElementById('filter-status');

  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      var filter = button.getAttribute('data-filter');
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
      var shown = 0;
      items.forEach(function (item) {
        var tags = item.getAttribute('data-tags').split(' ');
        var match = filter === 'all' || tags.indexOf(filter) !== -1;
        item.hidden = !match;
        if (match) { shown += 1; }
      });
      status.textContent = 'Showing ' + shown + ' case ' + (shown === 1 ? 'study' : 'studies') + '.';
    });
  });
})();
