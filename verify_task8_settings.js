/**
 * Task 8 Verification: Settings Panel
 * Verifies Requirements 10.1-10.7
 */

const fs = require('fs');
const { JSDOM } = require('jsdom');

// Read the HTML file
const html = fs.readFileSync('phishing_detection_dashboard.html', 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;

let passed = 0;
let failed = 0;
const results = [];

function test(name, condition, requirement) {
  if (condition) {
    passed++;
    results.push(`✓ ${name} (${requirement})`);
  } else {
    failed++;
    results.push(`✗ ${name} (${requirement})`);
  }
}

console.log('='.repeat(70));
console.log('TASK 8 VERIFICATION: Settings Panel');
console.log('='.repeat(70));
console.log();

// Requirement 10.1: Display API integration status for all 4 APIs
console.log('Requirement 10.1: API Integration Status Display');
console.log('-'.repeat(70));

const apiStatuses = document.querySelectorAll('.api-status');
test(
  'Settings panel has 4 API status displays',
  apiStatuses.length === 4,
  'Req 10.1'
);

const apiNames = Array.from(apiStatuses).map(status => 
  status.querySelector('.api-name')?.textContent.trim()
);

test(
  'Google Safe Browsing API is displayed',
  apiNames.includes('Google Safe Browsing API'),
  'Req 10.1'
);

test(
  'VirusTotal API is displayed',
  apiNames.includes('VirusTotal API'),
  'Req 10.1'
);

test(
  'ML Heuristic Engine is displayed',
  apiNames.includes('ML Heuristic Engine'),
  'Req 10.1'
);

test(
  'WHOIS Domain Age Checker is displayed',
  apiNames.includes('WHOIS Domain Age Checker'),
  'Req 10.1'
);

console.log();

// Requirement 10.2: Indicate Demo mode or Active status
console.log('Requirement 10.2: API Status Indicators');
console.log('-'.repeat(70));

const statusIndicators = Array.from(apiStatuses).map(status => ({
  name: status.querySelector('.api-name')?.textContent.trim(),
  statusText: status.querySelector('.api-status-text')?.textContent.trim(),
  hasDot: status.querySelector('.api-dot') !== null,
  dotClass: status.querySelector('.api-dot')?.className || ''
}));

test(
  'All APIs have status indicators (dots)',
  statusIndicators.every(s => s.hasDot),
  'Req 10.2'
);

test(
  'All APIs have status text (Demo mode or Active)',
  statusIndicators.every(s => s.statusText === 'Demo mode' || s.statusText === 'Active'),
  'Req 10.2'
);

test(
  'Google Safe Browsing shows Demo mode',
  statusIndicators.find(s => s.name === 'Google Safe Browsing API')?.statusText === 'Demo mode',
  'Req 10.2'
);

test(
  'VirusTotal shows Demo mode',
  statusIndicators.find(s => s.name === 'VirusTotal API')?.statusText === 'Demo mode',
  'Req 10.2'
);

test(
  'ML Heuristic Engine shows Active',
  statusIndicators.find(s => s.name === 'ML Heuristic Engine')?.statusText === 'Active',
  'Req 10.2'
);

test(
  'WHOIS Domain Age Checker shows Active',
  statusIndicators.find(s => s.name === 'WHOIS Domain Age Checker')?.statusText === 'Active',
  'Req 10.2'
);

console.log();

// Requirement 10.3, 10.4, 10.5: Toggle switches for 6 detection signals
console.log('Requirements 10.3, 10.4, 10.5: Detection Signal Toggles');
console.log('-'.repeat(70));

const settingsSections = document.querySelectorAll('.settings-section');
const detectionSignalsSection = Array.from(settingsSections).find(section => 
  section.querySelector('h3')?.textContent.trim() === 'Detection Signals'
);

test(
  'Detection Signals section exists',
  detectionSignalsSection !== undefined,
  'Req 10.3'
);

const detectionToggles = detectionSignalsSection?.querySelectorAll('.toggle-row') || [];

test(
  'Settings panel has 6 detection signal toggles',
  detectionToggles.length === 6,
  'Req 10.3'
);

const expectedSignals = [
  'URL structure analysis',
  'Domain age check',
  'HTTPS / SSL verification',
  'Redirect chain analysis',
  'Brand similarity detection',
  'Page content heuristics'
];

const actualSignals = Array.from(detectionToggles).map(toggle => 
  toggle.querySelector('.toggle-label')?.textContent.trim()
);

expectedSignals.forEach(signal => {
  test(
    `Toggle for "${signal}" exists`,
    actualSignals.includes(signal),
    'Req 10.3'
  );
});

// Requirement 10.4: Each toggle has label and description
test(
  'All detection signal toggles have labels',
  Array.from(detectionToggles).every(toggle => 
    toggle.querySelector('.toggle-label')?.textContent.trim().length > 0
  ),
  'Req 10.4'
);

test(
  'All detection signal toggles have descriptions',
  Array.from(detectionToggles).every(toggle => 
    toggle.querySelector('.toggle-desc')?.textContent.trim().length > 0
  ),
  'Req 10.4'
);

// Requirement 10.5: Toggles show enabled state
test(
  'All detection signal toggles have checkbox inputs',
  Array.from(detectionToggles).every(toggle => 
    toggle.querySelector('input[type="checkbox"]') !== null
  ),
  'Req 10.5'
);

test(
  'All detection signal toggles are enabled by default',
  Array.from(detectionToggles).every(toggle => 
    toggle.querySelector('input[type="checkbox"]')?.hasAttribute('checked')
  ),
  'Req 10.5'
);

console.log();

// Requirement 10.6: Toggle switches for 2 alert preferences
console.log('Requirement 10.6: Alert Preference Toggles');
console.log('-'.repeat(70));

const alertsSection = Array.from(settingsSections).find(section => 
  section.querySelector('h3')?.textContent.trim() === 'Alerts & Notifications'
);

test(
  'Alerts & Notifications section exists',
  alertsSection !== undefined,
  'Req 10.6'
);

const alertToggles = alertsSection?.querySelectorAll('.toggle-row') || [];

test(
  'Settings panel has 2 alert preference toggles',
  alertToggles.length === 2,
  'Req 10.6'
);

const alertToggleLabels = Array.from(alertToggles).map(toggle => 
  toggle.querySelector('.toggle-label')?.textContent.trim()
);

test(
  'Toggle for "Phishing alerts" exists',
  alertToggleLabels.includes('Phishing alerts'),
  'Req 10.6'
);

test(
  'Toggle for "Suspicious URL alerts" exists',
  alertToggleLabels.includes('Suspicious URL alerts'),
  'Req 10.6'
);

test(
  'All alert toggles have labels',
  Array.from(alertToggles).every(toggle => 
    toggle.querySelector('.toggle-label')?.textContent.trim().length > 0
  ),
  'Req 10.6'
);

test(
  'All alert toggles have descriptions',
  Array.from(alertToggles).every(toggle => 
    toggle.querySelector('.toggle-desc')?.textContent.trim().length > 0
  ),
  'Req 10.6'
);

console.log();

// Requirement 10.7: Browser extension installation banner
console.log('Requirement 10.7: Browser Extension Installation Banner');
console.log('-'.repeat(70));

const extBanner = document.querySelector('.ext-banner');

test(
  'Browser extension banner exists',
  extBanner !== null,
  'Req 10.7'
);

test(
  'Extension banner has icon',
  extBanner?.querySelector('.ext-icon') !== null,
  'Req 10.7'
);

test(
  'Extension banner has info section',
  extBanner?.querySelector('.ext-info') !== null,
  'Req 10.7'
);

test(
  'Extension banner has title',
  extBanner?.querySelector('.ext-info strong')?.textContent.trim().length > 0,
  'Req 10.7'
);

test(
  'Extension banner has description',
  extBanner?.querySelector('.ext-info span')?.textContent.trim().length > 0,
  'Req 10.7'
);

test(
  'Extension banner has Install button',
  extBanner?.querySelector('.btn-install') !== null,
  'Req 10.7'
);

test(
  'Install button has text',
  extBanner?.querySelector('.btn-install')?.textContent.trim().includes('Install'),
  'Req 10.7'
);

console.log();
console.log('='.repeat(70));
console.log('VERIFICATION SUMMARY');
console.log('='.repeat(70));
console.log();

results.forEach(result => console.log(result));

console.log();
console.log('-'.repeat(70));
console.log(`Total Tests: ${passed + failed}`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
console.log('-'.repeat(70));

if (failed === 0) {
  console.log();
  console.log('✓ ALL REQUIREMENTS VERIFIED SUCCESSFULLY');
  console.log();
  process.exit(0);
} else {
  console.log();
  console.log('✗ SOME REQUIREMENTS FAILED VERIFICATION');
  console.log();
  process.exit(1);
}
