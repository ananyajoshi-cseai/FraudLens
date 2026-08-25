document.addEventListener('DOMContentLoaded', function () {
  var savedData = sessionStorage.getItem('analysisResult');

  if (!savedData) {
    console.log('No result data found!');
    return;
  }

  var result = JSON.parse(savedData);

  // =========================
  // 1. UPDATE SCORE & VERDICT
  // =========================

  document.querySelector('.score-num').textContent = result.risk_score;

  document.querySelector('.action-badge').textContent =
    'ACTION: ' + result.recommended_action.toUpperCase();

  document.querySelector('.verdict-info h2').textContent =
    result.risk_level + ' Risk Detected';


  // =========================
  // 2. UPDATE RULE COUNT
  // =========================

  var ruleCount = document.querySelector('.rule-count');

  if (ruleCount) {
    ruleCount.textContent =
      result.reasons.length + ' rules contributed to the total risk score';
  }


  // =========================
  // 3. BUILD RISK RULE LIST
  // =========================

  var ruleList = document.querySelector('.rule-list');

  if (ruleList) {
    ruleList.innerHTML = '';

    for (var i = 0; i < result.reasons.length; i++) {

      var reason = result.reasons[i];

      var li = document.createElement('li');
      li.className = 'rule-item ' + result.risk_level.toLowerCase();

      li.innerHTML =
        '<div class="rule-details">' +
          '<strong>' + reason.signal + '</strong>' +
          '<p>' + reason.message + '</p>' +
        '</div>' +
        '<div class="rule-score">+' + reason.impact + ' pts</div>';

      ruleList.appendChild(li);
    }
  }


  // =========================
  // 4. UPDATE TRANSACTION DATA
  // =========================

  var transaction = result.transaction;

  if (transaction) {

    // Amount
    var amountElement = document.querySelector('.transaction-amount');

    if (amountElement) {
      amountElement.textContent =
        '₹' + Number(transaction.amount).toLocaleString('en-IN');
    }


    // Beneficiary
    var beneficiaryElement =
      document.querySelector('.transaction-beneficiary');

    if (beneficiaryElement) {
      beneficiaryElement.textContent =
        transaction.beneficiary_id;
    }


    // Transaction time
    var timeElement =
      document.querySelector('.transaction-time');

    if (timeElement) {
      timeElement.textContent =
        transaction.transaction_hour + ':00';
    }


    // Device
    var deviceElement =
      document.querySelector('.transaction-device');

    if (deviceElement) {
      deviceElement.textContent =
        transaction.device_id;
    }


    // Failed attempts
    var failedAttemptsElement =
      document.querySelector('.transaction-failed');

    if (failedAttemptsElement) {
      failedAttemptsElement.textContent =
        transaction.failed_attempts;
    }
  }


  // =========================
  // 5. UPDATE RAW API RESPONSE
  // =========================

  var codeBox = document.querySelector('pre code');

  if (codeBox) {
    codeBox.textContent =
      JSON.stringify(result, null, 2);
  }
});