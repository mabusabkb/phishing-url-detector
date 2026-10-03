/**
 * Task 6: Alerts System Verification
 * 
 * This test file verifies that the alerts system meets all requirements:
 * - Req 8.1: Alerts created for Phishing verdicts
 * - Req 8.2: Alerts created for Suspicious verdicts
 * - Req 8.3: Alerts display in reverse chronological order
 * - Req 8.4: Alert badge shows count
 * - Req 8.5: Alert badge hides when zero
 * - Req 8.6: Alert display includes all required fields
 * - Req 8.7: Dismiss button removes individual alerts
 * - Req 8.8: Badge updates after dismissal
 * - Req 8.9: Dismiss All button clears all alerts
 * - Req 8.10: Empty state displays when no alerts
 */

// Test results tracking
const testResults = {
  passed: 0,
  failed: 0,
  tests: []
};

function logTest(name, passed, details = '') {
  testResults.tests.push({ name, passed, details });
  if (passed) {
    testResults.passed++;
    console.log(`✓ ${name}`);
  } else {
    testResults.failed++;
    console.error(`✗ ${name}${details ? ': ' + details : ''}`);
  }
}

// Helper function to wait for DOM updates
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Helper to get alert badge element
function getAlertBadge() {
  return document.getElementById('alert-badge');
}

// Helper to get alerts list element
function getAlertsList() {
  return document.getElementById('alerts-list');
}

// Helper to count visible alerts in DOM
function countVisibleAlerts() {
  const alertsList = getAlertsList();
  return alertsList.querySelectorAll('.alert-item').length;
}

// Helper to get alert by ID from DOM
function getAlertElementById(id) {
  return document.getElementById(`alert-${id}`);
}

// Test 1: Verify alerts created for Phishing verdicts (Req 8.1)
async function testPhishingAlertCreation() {
  console.log('\n--- Test 1: Phishing Alert Creation (Req 8.1) ---');
  
  // Clear existing alerts and history
  alerts = [];
  history = [];
  updateAlertBadge();
  
  // Simulate scanning a phishing URL
  const initialAlertCount = alerts.length;
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  
  // Wait for scan to complete (6 steps * 350ms + buffer)
  await wait(2500);
  
  // Verify alert was created
  const alertCreated = alerts.length === initialAlertCount + 1;
  const isPhishingType = alerts[0]?.type === 'phishing';
  
  logTest(
    'Phishing verdict creates alert',
    alertCreated && isPhishingType,
    alertCreated ? '' : 'Alert was not created for phishing verdict'
  );
}

// Test 2: Verify alerts created for Suspicious verdicts (Req 8.2)
async function testSuspiciousAlertCreation() {
  console.log('\n--- Test 2: Suspicious Alert Creation (Req 8.2) ---');
  
  // Clear existing alerts and history
  alerts = [];
  history = [];
  updateAlertBadge();
  
  // Simulate scanning a suspicious URL
  const initialAlertCount = alerts.length;
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  
  // Wait for scan to complete
  await wait(2500);
  
  // Verify alert was created
  const alertCreated = alerts.length === initialAlertCount + 1;
  const isSuspiciousType = alerts[0]?.type === 'suspicious';
  
  logTest(
    'Suspicious verdict creates alert',
    alertCreated && isSuspiciousType,
    alertCreated ? '' : 'Alert was not created for suspicious verdict'
  );
}

// Test 3: Verify alerts display in reverse chronological order (Req 8.3)
async function testAlertChronologicalOrder() {
  console.log('\n--- Test 3: Alert Chronological Order (Req 8.3) ---');
  
  // Clear and create multiple alerts
  alerts = [];
  history = [];
  updateAlertBadge();
  
  // Scan phishing URL
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  const firstAlertId = alerts[0].id;
  
  // Scan suspicious URL
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  await wait(2500);
  
  const secondAlertId = alerts[0].id;
  
  // Verify most recent alert is first
  const correctOrder = secondAlertId > firstAlertId && alerts[0].id === secondAlertId;
  
  logTest(
    'Alerts display in reverse chronological order (newest first)',
    correctOrder,
    correctOrder ? '' : `Expected newest alert first, got IDs: ${alerts.map(a => a.id).join(', ')}`
  );
}

// Test 4: Verify alert badge shows count (Req 8.4)
async function testAlertBadgeCount() {
  console.log('\n--- Test 4: Alert Badge Count (Req 8.4) ---');
  
  // Clear alerts
  alerts = [];
  updateAlertBadge();
  
  // Create alerts
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  await wait(2500);
  
  const badge = getAlertBadge();
  const badgeCount = parseInt(badge.textContent);
  const actualCount = alerts.length;
  
  logTest(
    'Alert badge shows correct count',
    badgeCount === actualCount,
    `Expected ${actualCount}, got ${badgeCount}`
  );
}

// Test 5: Verify alert badge hides when zero (Req 8.5)
function testAlertBadgeHidesWhenZero() {
  console.log('\n--- Test 5: Alert Badge Hides When Zero (Req 8.5) ---');
  
  // Clear all alerts
  alerts = [];
  updateAlertBadge();
  
  const badge = getAlertBadge();
  const isHidden = badge.style.display === 'none';
  
  logTest(
    'Alert badge hides when count is zero',
    isHidden,
    isHidden ? '' : `Badge display is "${badge.style.display}", expected "none"`
  );
}

// Test 6: Verify alert display includes all required fields (Req 8.6)
async function testAlertRequiredFields() {
  console.log('\n--- Test 6: Alert Required Fields (Req 8.6) ---');
  
  // Clear and create an alert
  alerts = [];
  history = [];
  updateAlertBadge();
  
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  // Switch to alerts tab and render
  switchTab('alerts');
  await wait(100);
  
  const alertsList = getAlertsList();
  const alertElement = alertsList.querySelector('.alert-item');
  
  if (!alertElement) {
    logTest('Alert displays all required fields', false, 'No alert element found in DOM');
    return;
  }
  
  // Check for required elements
  const hasIcon = alertElement.querySelector('.alert-icon') !== null;
  const hasTitle = alertElement.querySelector('.alert-title') !== null;
  const hasMessage = alertElement.querySelector('.alert-msg') !== null;
  const hasUrl = alertElement.querySelector('.alert-url') !== null;
  const hasTime = alertElement.querySelector('.alert-time') !== null;
  const hasActions = alertElement.querySelector('.alert-actions') !== null;
  
  const allFieldsPresent = hasIcon && hasTitle && hasMessage && hasUrl && hasTime && hasActions;
  
  logTest(
    'Alert displays all required fields (icon, title, message, URL, time, actions)',
    allFieldsPresent,
    allFieldsPresent ? '' : `Missing fields: ${[
      !hasIcon && 'icon',
      !hasTitle && 'title',
      !hasMessage && 'message',
      !hasUrl && 'URL',
      !hasTime && 'time',
      !hasActions && 'actions'
    ].filter(Boolean).join(', ')}`
  );
}

// Test 7: Verify Dismiss button removes individual alerts (Req 8.7, 8.8)
async function testDismissIndividualAlert() {
  console.log('\n--- Test 7: Dismiss Individual Alert (Req 8.7, 8.8) ---');
  
  // Create multiple alerts
  alerts = [];
  history = [];
  updateAlertBadge();
  
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  await wait(2500);
  
  const initialCount = alerts.length;
  const alertToRemove = alerts[1]; // Remove second alert
  const alertId = alertToRemove.id;
  
  // Dismiss the alert
  dismissAlert(alertId);
  
  const afterCount = alerts.length;
  const alertRemoved = afterCount === initialCount - 1;
  const specificAlertRemoved = !alerts.find(a => a.id === alertId);
  
  // Check badge updated
  const badge = getAlertBadge();
  const badgeCount = parseInt(badge.textContent);
  const badgeUpdated = badgeCount === afterCount;
  
  logTest(
    'Dismiss button removes individual alert and updates badge',
    alertRemoved && specificAlertRemoved && badgeUpdated,
    `Alert removed: ${alertRemoved}, Specific alert gone: ${specificAlertRemoved}, Badge updated: ${badgeUpdated}`
  );
}

// Test 8: Verify Dismiss All button clears all alerts (Req 8.9)
async function testDismissAllAlerts() {
  console.log('\n--- Test 8: Dismiss All Alerts (Req 8.9) ---');
  
  // Create multiple alerts
  alerts = [];
  history = [];
  updateAlertBadge();
  
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  await wait(2500);
  
  const initialCount = alerts.length;
  
  // Dismiss all alerts
  dismissAllAlerts();
  
  const allCleared = alerts.length === 0;
  const badge = getAlertBadge();
  const badgeHidden = badge.style.display === 'none';
  
  logTest(
    'Dismiss All button clears all alerts and hides badge',
    allCleared && badgeHidden && initialCount > 0,
    `Alerts cleared: ${allCleared}, Badge hidden: ${badgeHidden}, Had alerts: ${initialCount > 0}`
  );
}

// Test 9: Verify empty state displays when no alerts (Req 8.10)
function testEmptyState() {
  console.log('\n--- Test 9: Empty State Display (Req 8.10) ---');
  
  // Clear all alerts
  alerts = [];
  updateAlertBadge();
  
  // Render alerts panel
  renderAlerts();
  
  const alertsList = getAlertsList();
  const emptyState = alertsList.querySelector('.empty-state');
  const hasEmptyState = emptyState !== null;
  const emptyStateText = emptyState?.textContent || '';
  const hasAppropriateMessage = emptyStateText.toLowerCase().includes('no') || 
                                 emptyStateText.toLowerCase().includes('clear');
  
  logTest(
    'Empty state displays when no alerts exist',
    hasEmptyState && hasAppropriateMessage,
    hasEmptyState ? '' : 'No empty state element found'
  );
}

// Test 10: Verify Safe verdicts do NOT create alerts
async function testSafeNoAlert() {
  console.log('\n--- Test 10: Safe Verdict Does Not Create Alert ---');
  
  // Clear alerts
  alerts = [];
  history = [];
  updateAlertBadge();
  
  const initialCount = alerts.length;
  
  // Scan safe URL
  document.getElementById('url-input').value = DEMOS.safe.url;
  startScan();
  await wait(2500);
  
  const noAlertCreated = alerts.length === initialCount;
  
  logTest(
    'Safe verdict does not create alert',
    noAlertCreated,
    noAlertCreated ? '' : 'Alert was incorrectly created for safe verdict'
  );
}

// Test 11: Verify alert type styling
async function testAlertTypeStyling() {
  console.log('\n--- Test 11: Alert Type Styling ---');
  
  // Create phishing alert
  alerts = [];
  history = [];
  document.getElementById('url-input').value = DEMOS.phishing.url;
  startScan();
  await wait(2500);
  
  // Create suspicious alert
  document.getElementById('url-input').value = DEMOS.suspicious.url;
  startScan();
  await wait(2500);
  
  // Render alerts
  switchTab('alerts');
  await wait(100);
  
  const alertsList = getAlertsList();
  const alertElements = alertsList.querySelectorAll('.alert-item');
  
  // Check first alert (suspicious - most recent)
  const suspiciousAlert = alertElements[0];
  const hasSuspiciousClass = suspiciousAlert?.classList.contains('suspicious');
  
  // Check second alert (phishing)
  const phishingAlert = alertElements[1];
  const hasPhishingClass = phishingAlert?.classList.contains('phishing');
  
  logTest(
    'Alerts have correct type-specific CSS classes',
    hasSuspiciousClass && hasPhishingClass,
    `Suspicious class: ${hasSuspiciousClass}, Phishing class: ${hasPhishingClass}`
  );
}

// Main test runner
async function runAllTests() {
  console.log('='.repeat(60));
  console.log('TASK 6: ALERTS SYSTEM VERIFICATION');
  console.log('='.repeat(60));
  
  try {
    await testPhishingAlertCreation();
    await testSuspiciousAlertCreation();
    await testAlertChronologicalOrder();
    await testAlertBadgeCount();
    testAlertBadgeHidesWhenZero();
    await testAlertRequiredFields();
    await testDismissIndividualAlert();
    await testDismissAllAlerts();
    testEmptyState();
    await testSafeNoAlert();
    await testAlertTypeStyling();
    
    // Print summary
    console.log('\n' + '='.repeat(60));
    console.log('TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`Total tests: ${testResults.tests.length}`);
    console.log(`Passed: ${testResults.passed}`);
    console.log(`Failed: ${testResults.failed}`);
    console.log(`Success rate: ${((testResults.passed / testResults.tests.length) * 100).toFixed(1)}%`);
    
    if (testResults.failed > 0) {
      console.log('\nFailed tests:');
      testResults.tests
        .filter(t => !t.passed)
        .forEach(t => console.log(`  - ${t.name}${t.details ? ': ' + t.details : ''}`));
    }
    
    console.log('='.repeat(60));
    
    // Return results for programmatic access
    return testResults;
    
  } catch (error) {
    console.error('Test execution error:', error);
    return { error: error.message, ...testResults };
  }
}

// Auto-run if in browser context
if (typeof window !== 'undefined') {
  console.log('Verification script loaded. Run runAllTests() to execute all tests.');
}

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runAllTests, testResults };
}
