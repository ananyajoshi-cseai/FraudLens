document.addEventListener('DOMContentLoaded', function () {
  // Read saved data from browser storage
  var savedData = sessionStorage.getItem('analysisResult');

  if (!savedData) {
    console.log('No result data found!');
    return;
  }

  // Convert JSON text string back into a JavaScript Object
  var result = JSON.parse(savedData);

  // 1. Update Score and Verdict
  document.querySelector('.score-num').textContent = result.risk_score;
  document.querySelector('.action-badge').textContent = 'ACTION: ' + result.risk_level;
  document.querySelector('.verdict-info h2').textContent = result.risk_level + ' Risk Detected';

  // 2. Build Triggered Risk Rules List
  var ruleList = document.querySelector('.rule-list');
  ruleList.innerHTML = ''; // Clear default HTML placeholders

  for (var i = 0; i < result.reasons.length; i++) {
    var reason = result.reasons[i];

    var li = document.createElement('li');
    li.className = 'rule-item high';

    li.innerHTML = 
      '<div class="rule-details">' +
        '<strong>' + reason.signal + '</strong>' +
        '<p>' + reason.message + '</p>' +
      '</div>' +
      '<div class="rule-score">+' + reason.impact + ' pts</div>';

    ruleList.appendChild(li);
  }

  // 3. Update Raw API JSON Box
  var codeBox = document.querySelector('pre code');
  if (codeBox) {
    codeBox.textContent = JSON.stringify(result, null, 2);
  }
});