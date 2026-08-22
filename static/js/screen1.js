document.addEventListener('DOMContentLoaded', function () {
  loadDashboardData();
});


function loadDashboardData() {
  fetch('/api/transactions')
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      updateDashboardTable(data);
    })
    .catch(function (error) {
      console.error('Error loading dashboard:', error);
    });
}

// Function to put data into the HTML table
function updateDashboardTable(transactions) {
  var tbody = document.querySelector('tbody');
  tbody.innerHTML = ''; // Clear out the hardcoded demo rows

  // Loop through each transaction
  for (var i = 0; i < transactions.length; i++) {
    var tx = transactions[i];

    // Create a new table row
    var row = document.createElement('tr');

    // Build row content using plain HTML strings
    row.innerHTML = 
      '<td>' + tx.transaction_id + '</td>' +
      '<td>' + tx.beneficiary_id + '</td>' +
      '<td>$' + tx.amount + '</td>' +
      '<td><span class="status ' + tx.risk_level.toLowerCase() + '">' + tx.risk_level + '</span></td>';

    // Add row to the table body
    tbody.appendChild(row);
  }
}