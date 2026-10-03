/**
 * Task 6 Verification Runner
 * 
 * This script performs static analysis and code inspection of the 
 * phishing_detection_dashboard.html file to verify that the alerts 
 * system implementation meets all requirements.
 */

const fs = require('fs');

// Read the dashboard HTML file
const dashboardContent = fs.readFileSync('phishing_detection_dashboard.html', 'utf8');

// Test results
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

function test(name, condition, details = '') {
  results.tests.push({ name, passed: condition, details });
  if (condition) {
    results.passed++;
    console.log(`✓ ${name}`);
  } else {
    results.failed++;
    console.error(`✗ ${name}${details ? ': ' + details : ''}`);
  }
}

console.log('='.repeat(70));
console.log('TASK 6: ALERTS SYSTEM VERIFICATION (Static Code Analysis)');
console.log('='.repeat(70));
console.log();

// Req 8.1 & 8.2: Verify alerts created for Phishing and Suspicious verdicts
console.log('--- Requirement 8.1 & 8.2: Alert Creation Logic ---');
const hasPhishingAlertCreation = dashboardContent.includes("d.verdict==='phishing'||d.verdict==='suspicious'");
const hasAlertPush = dashboardContent.includes('alerts.unshift({');
const hasAlertIdGeneration = dashboardContent.includes('id:Date.now()');
test(
  'Code creates alerts for phishing and suspicious verdicts',
  hasPhishingAlertCreation && hasAlertPush && hasAlertIdGeneration,
  'Should have conditional check and alert creation logic'
);

// Req 8.3: Verify alerts display in reverse chronological order
console.log('\n--- Requirement 8.3: Reverse Chronological Order ---');
const usesUnshift = dashboardContent.includes('alerts.unshift(');
test(
  'Alerts use unshift() to prepend new alerts (newest first)',
  usesUnshift,
  'Should use unshift() to add alerts to beginning of array'
);

// Req 8.4 & 8.5: Verify alert badge shows count and hides when zero
console.log('\n--- Requirement 8.4 & 8.5: Alert Badge Behavior ---');
const hasUpdateAlertBadge = dashboardContent.includes('function updateAlertBadge()');
const badgeShowsCount = dashboardContent.includes('b.textContent = alerts.length');
const badgeHidesWhenZero = dashboardContent.includes("b.style.display = alerts.length ? 'inline-block' : 'none'");
test(
  'Alert badge updates with count and hides when zero',
  hasUpdateAlertBadge && badgeShowsCount && badgeHidesWhenZero,
  'Should have updateAlertBadge function with conditional display logic'
);

// Req 8.6: Verify alert display includes all required fields
console.log('\n--- Requirement 8.6: Alert Display Fields ---');
const hasAlertIcon = dashboardContent.includes('alert-icon');
const hasAlertTitle = dashboardContent.includes('alert-title');
const hasAlertMsg = dashboardContent.includes('alert-msg');
const hasAlertUrl = dashboardContent.includes('alert-url');
const hasAlertTime = dashboardContent.includes('alert-time');
const hasAlertActions = dashboardContent.includes('alert-actions');
test(
  'Alert HTML includes all required fields (icon, title, msg, url, time, actions)',
  hasAlertIcon && hasAlertTitle && hasAlertMsg && hasAlertUrl && hasAlertTime && hasAlertActions,
  'Should have CSS classes for all required alert fields'
);

// Req 8.7 & 8.8: Verify Dismiss button removes individual alerts
console.log('\n--- Requirement 8.7 & 8.8: Dismiss Individual Alert ---');
const hasDismissAlert = dashboardContent.includes('function dismissAlert(id)');
const dismissFiltersById = dashboardContent.includes('alerts = alerts.filter(a=>a.id!==id)');
const dismissUpdatesUI = dashboardContent.match(/dismissAlert.*updateAlertBadge.*renderAlerts/s);
test(
  'Dismiss button removes alert by ID and updates UI',
  hasDismissAlert && dismissFiltersById,
  'Should have dismissAlert function that filters by ID'
);

test(
  'Dismiss function updates badge and re-renders alerts',
  dismissUpdatesUI !== null,
  'Should call updateAlertBadge() and renderAlerts() after dismissal'
);

// Req 8.9: Verify Dismiss All button clears all alerts
console.log('\n--- Requirement 8.9: Dismiss All Alerts ---');
const hasDismissAllAlerts = dashboardContent.includes('function dismissAllAlerts()');
const dismissAllClearsArray = dashboardContent.includes('alerts=[]');
const dismissAllInHTML = dashboardContent.includes('dismissAllAlerts()');
test(
  'Dismiss All button clears all alerts',
  hasDismissAllAlerts && dismissAllClearsArray && dismissAllInHTML,
  'Should have dismissAllAlerts function that empties alerts array'
);

// Req 8.10: Verify empty state displays when no alerts
console.log('\n--- Requirement 8.10: Empty State Display ---');
const hasEmptyStateCheck = dashboardContent.includes('if(!alerts.length)');
const hasEmptyStateHTML = dashboardContent.includes('empty-state');
const emptyStateInRenderAlerts = dashboardContent.match(/renderAlerts.*empty-state/s);
test(
  'Empty state displays when no alerts exist',
  hasEmptyStateCheck && hasEmptyStateHTML && emptyStateInRenderAlerts,
  'Should check alerts.length and display empty state'
);

// Additional verification: Alert type styling
console.log('\n--- Additional: Alert Type Styling ---');
const hasPhishingClass = dashboardContent.includes("class=\"alert-item ${a.type}\"");
const hasPhishingIcon = dashboardContent.includes("a.type==='phishing'?'🚨':'⚠'");
test(
  'Alerts have type-specific CSS classes and icons',
  hasPhishingClass && hasPhishingIcon,
  'Should apply type class and conditional icon'
);

// Verify alert badge in navigation
console.log('\n--- Additional: Alert Badge in Navigation ---');
const hasBadgeInNav = dashboardContent.includes('id="alert-badge"');
const badgeInAlertsTab = dashboardContent.match(/Alerts.*alert-badge/);
test(
  'Alert badge is present in Alerts navigation tab',
  hasBadgeInNav && badgeInAlertsTab,
  'Should have alert-badge element in navigation'
);

// Verify initial alerts data
console.log('\n--- Additional: Initial Demo Alerts ---');
const hasInitialAlerts = dashboardContent.includes('let alerts = [');
const hasPhishingAlert = dashboardContent.includes("type:'phishing'");
const hasSuspiciousAlert = dashboardContent.includes("type:'suspicious'");
test(
  'Initial demo alerts include phishing and suspicious types',
  hasInitialAlerts && hasPhishingAlert && hasSuspiciousAlert,
  'Should have sample alerts for demonstration'
);

// Verify renderAlerts function
console.log('\n--- Additional: Render Alerts Function ---');
const hasRenderAlerts = dashboardContent.includes('function renderAlerts()');
const renderAlertsUsesMap = dashboardContent.match(/renderAlerts.*alerts\.map/s);
test(
  'renderAlerts function exists and uses map to render alerts',
  hasRenderAlerts && renderAlertsUsesMap,
  'Should have renderAlerts function that maps over alerts array'
);

// Print summary
console.log('\n' + '='.repeat(70));
console.log('VERIFICATION SUMMARY');
console.log('='.repeat(70));
console.log(`Total checks: ${results.tests.length}`);
console.log(`Passed: ${results.passed}`);
console.log(`Failed: ${results.failed}`);
console.log(`Success rate: ${((results.passed / results.tests.length) * 100).toFixed(1)}%`);

if (results.failed > 0) {
  console.log('\nFailed checks:');
  results.tests
    .filter(t => !t.passed)
    .forEach(t => console.log(`  - ${t.name}${t.details ? ': ' + t.details : ''}`));
}

console.log('='.repeat(70));

// Exit with appropriate code
process.exit(results.failed > 0 ? 1 : 0);
