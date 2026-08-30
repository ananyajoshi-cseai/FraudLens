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
  tbody.innerHTML = ''; 

  // Loop through each transaction
  for (var i = 0; i < transactions.length; i++) {
    var tx = transactions[i];

    // Create a new table row
    var row = document.createElement('tr');

    // Build row content using plain HTML strings
    row.innerHTML = 
      '<td>' + tx.transaction_id + '</td>' +
      '<td>' + tx.beneficiary_id + '</td>' +
      '<td>₹' + tx.amount + '</td>' +
      '<td><span class="status ' + tx.risk_level.toLowerCase() + '">' + tx.risk_level + '</span></td>';

    // Add row to the table body
    tbody.appendChild(row);
  }
}
const scanData = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  transactions: [3200, 4100, 3800, 5200, 4600, 6100, 5800],
  threats: [42, 55, 38, 71, 49, 83, 64]
};

new Chart(document.getElementById('scanChart'), {
  type: 'line',
  data: {
    labels: scanData.labels,
    datasets: [
      {
        label: 'Transactions',
        data: scanData.transactions,
        borderColor: '#1a2b4c',
        tension: 0.3
      },
      {
        label: 'Threats',
        data: scanData.threats,
        borderColor: '#c5221f',
        tension: 0.3
      }
    ]
  }
});