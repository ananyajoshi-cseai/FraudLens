document.addEventListener('DOMContentLoaded', function () {
  fetchAuditLogs();
});

function fetchAuditLogs() {
  fetch('/api/transactions')
    .then(function (response) {
      return response.json();
    })
    .then(function (logs) {
      renderAuditTable(logs);
    })
    .catch(function (error) {
      console.error('Failed to load audit logs:', error);
    });
}

function renderAuditTable(logs) {
  var tbody = document.querySelector('tbody');
  tbody.innerHTML = '';

  for (var i = 0; i < logs.length; i++) {
    var log = logs[i];

    // Main Row
    var mainRow = document.createElement('tr');
    mainRow.className = 'table-row';
    
    // Toggle details row when clicked
    mainRow.onclick = function () {
      this.classList.toggle('expanded');
    };

    mainRow.innerHTML = 
      '<td>' + log.timestamp + '</td>' +
      '<td><code>' + log.transaction_id + '</code></td>' +
      '<td><strong>$' + log.amount + '</strong></td>' +
      '<td>' + log.beneficiary_id + '</td>' +
      '<td><span class="status ' + log.risk_level.toLowerCase() + '">' + log.risk_level + ' Risk</span></td>' +
      '<td><strong>' + log.risk_score + '</strong></td>' +
      '<td class="chevron-cell">▼</td>';

    // Details Row
    var detailsRow = document.createElement('tr');
    detailsRow.className = 'details-row';
    detailsRow.innerHTML = 
      '<td colspan="7">' +
        '<div class="details-content">' +
          '<strong>Evaluation Complete</strong>' +
        '</div>' +
      '</td>';

    tbody.appendChild(mainRow);
    tbody.appendChild(detailsRow);
  }
}