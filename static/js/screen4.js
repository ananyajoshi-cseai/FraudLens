document.addEventListener('DOMContentLoaded', function () {
  setupFilters();
  fetchAuditLogs();
});

var allLogs = [];

function fetchAuditLogs() {
  fetch('/api/transactions')
    .then(function (response) {
      if (!response.ok) {
        throw new Error('Failed to fetch transactions');
      }

      return response.json();
    })
    .then(function (logs) {
      allLogs = Array.isArray(logs) ? logs : [];
      renderAuditTable(allLogs);
    })
    .catch(function (error) {
      console.error('Failed to load audit logs:', error);
    });
}

function setupFilters() {
  var riskFilter = document.getElementById('risk-filter');
  var dateFilter = document.getElementById('date-filter');
  var searchInput = document.querySelector(
    'input[placeholder*="ACC-89210-X"]'
  );

  if (riskFilter) {
    riskFilter.addEventListener('change', applyFilters);
  }

  if (dateFilter) {
    dateFilter.addEventListener('change', applyFilters);
  }

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }
}

function applyFilters() {
  var riskFilter = document.getElementById('risk-filter');
  var dateFilter = document.getElementById('date-filter');
  var searchInput = document.querySelector(
    'input[placeholder*="ACC-89210-X"]'
  );

  var selectedRisk = riskFilter ? riskFilter.value : 'all';
  var selectedDate = dateFilter ? dateFilter.value : '';
  var searchTerm = searchInput
    ? searchInput.value.trim().toLowerCase()
    : '';

  var filteredLogs = allLogs.filter(function (log) {

    // -------------------------
    // Risk filter
    // -------------------------
    if (selectedRisk !== 'all') {
      var score = Number(log.risk_score);

      if (selectedRisk === 'high' && score < 71) {
        return false;
      }

      if (
        selectedRisk === 'medium' &&
        (score < 31 || score > 70)
      ) {
        return false;
      }

      if (selectedRisk === 'low' && score > 30) {
        return false;
      }
    }

    // -------------------------
    // Date filter
    // -------------------------
    if (selectedDate) {
      var logDate = new Date(log.timestamp);

      if (isNaN(logDate.getTime())) {
        return false;
      }

      var year = logDate.getFullYear();
      var month = String(logDate.getMonth() + 1).padStart(2, '0');
      var day = String(logDate.getDate()).padStart(2, '0');

      var formattedDate =
        year + '-' + month + '-' + day;

      if (formattedDate !== selectedDate) {
        return false;
      }
    }

    // -------------------------
    // Search ID / Beneficiary
    // -------------------------
    if (searchTerm) {
      var transactionId = String(
        log.transaction_id || ''
      ).toLowerCase();

      var beneficiaryId = String(
        log.beneficiary_id || ''
      ).toLowerCase();

      if (
        !transactionId.includes(searchTerm) &&
        !beneficiaryId.includes(searchTerm)
      ) {
        return false;
      }
    }

    return true;
  });

  renderAuditTable(filteredLogs);
}

function renderAuditTable(logs) {
  var tbody = document.querySelector('tbody');

  if (!tbody) {
    return;
  }

  tbody.innerHTML = '';

  // -------------------------
  // Empty state
  // -------------------------
  if (logs.length === 0) {
    var emptyRow = document.createElement('tr');

    emptyRow.innerHTML =
      '<td colspan="7" style="text-align:center; padding:30px; color:#666;">' +
      'No transactions match the selected filters.' +
      '</td>';

    tbody.appendChild(emptyRow);
    return;
  }

  // -------------------------
  // Render transactions
  // -------------------------
  for (var i = 0; i < logs.length; i++) {
    var log = logs[i];

    // Main transaction row
    var mainRow = document.createElement('tr');
    mainRow.className = 'table-row';

    mainRow.onclick = function () {
      this.classList.toggle('expanded');
    };

    var riskLevel = String(
      log.risk_level || 'unknown'
    ).toLowerCase();

    mainRow.innerHTML =
      '<td>' +
      (log.timestamp || '-') +
      '</td>' +

      '<td><code>' +
      (log.transaction_id || '-') +
      '</code></td>' +

      '<td><strong>₹' +
      (log.amount ?? 0) +
      '</strong></td>' +

      '<td>' +
      (log.beneficiary_id || '-') +
      '</td>' +

      '<td><span class="status ' +
      riskLevel +
      '">' +
      (log.risk_level || 'Unknown') +
      ' Risk</span></td>' +

      '<td><strong>' +
      (log.risk_score ?? '-') +
      '</strong></td>' +

      '<td class="chevron-cell">▼</td>';

    // Details row
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