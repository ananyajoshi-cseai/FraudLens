document.addEventListener('DOMContentLoaded', function () {
  setupScenarioButtons();
  setupFormSubmit();
});

// 1. Setup Demo Scenario Buttons to auto-fill input fields
function setupScenarioButtons() {
  var scenarioButtons = document.querySelectorAll('.scenario-btn');

  // Loop over scenario buttons and assign preset data
  scenarioButtons[0].addEventListener('click', function () {
    // Normal Purchase (Safe)
    document.getElementById('amount').value = '50.00';
    document.getElementById('beneficiary').value = 'B101';
    document.getElementById('failed-attempts').value = '0';
  });

  scenarioButtons[2].addEventListener('click', function () {
    // High Risk Scenario
    document.getElementById('amount').value = '18500.00';
    document.getElementById('beneficiary').value = 'B999';
    document.getElementById('failed-attempts').value = '2';
  });
}

// 2. Setup Form Submission to POST data to backend
function setupFormSubmit() {
  var form = document.getElementById('payment-form');

  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Stop page from refreshing

    // Collect data from HTML input fields
    var selectedDevice = document.querySelector('input[name="device"]:checked').value;
    
    var payload = {
      user_id: "test_user_01", // Updated to match MongoDB!
      amount: parseFloat(document.getElementById('amount').value),
      beneficiary_id: document.getElementById('beneficiary').value,
      beneficiary_name: "Test Beneficiary",
      transaction_hour: parseInt(document.getElementById('transaction-time').value),
      device_id: selectedDevice === "known" ? "DEV-OLD-01" : selectedDevice,
      failed_attempts: parseInt(document.getElementById('failed-attempts').value)
    };

    // Send payload to Ananya's API
    fetch('/api/transactions/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(function (response) {
      return response.json();
    })
    .then(function (resultData) {
      // Save result in browser storage so Screen 3 can read it
      sessionStorage.setItem('analysisResult', JSON.stringify(resultData));

      // Navigate to Screen 3 (Results)
      window.location.href = '/screen3';
    })
    .catch(function (error) {
      alert('Error analyzing transaction!');
      console.error(error);
    });
  });
}

// Counter button handler (+ / - buttons)
function adjustCount(amount) {
  var input = document.getElementById('failed-attempts');
  var currentVal = parseInt(input.value) || 0;
  var newVal = currentVal + amount;
  if (newVal >= 0 && newVal <= 10) {
    input.value = newVal;
  }
}
