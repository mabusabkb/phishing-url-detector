#!/usr/bin/env python3
"""
Task 6 Verification Runner

This script performs static analysis and code inspection of the 
phishing_detection_dashboard.html file to verify that the alerts 
system implementation meets all requirements.
"""

import re
import sys

# Read the dashboard HTML file
with open('phishing_detection_dashboard.html', 'r') as f:
    dashboard_content = f.read()

# Test results
results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}

def test(name, condition, details=''):
    """Record and display test result"""
    results['tests'].append({'name': name, 'passed': condition, 'details': details})
    if condition:
        results['passed'] += 1
        print(f'✓ {name}')
    else:
        results['failed'] += 1
        error_msg = f'✗ {name}'
        if details:
            error_msg += f': {details}'
        print(error_msg, file=sys.stderr)

print('=' * 70)
print('TASK 6: ALERTS SYSTEM VERIFICATION (Static Code Analysis)')
print('=' * 70)
print()

# Req 8.1 & 8.2: Verify alerts created for Phishing and Suspicious verdicts
print('--- Requirement 8.1 & 8.2: Alert Creation Logic ---')
has_phishing_alert_creation = "d.verdict==='phishing'||d.verdict==='suspicious'" in dashboard_content
has_alert_push = 'alerts.unshift({' in dashboard_content
has_alert_id_generation = 'id:Date.now()' in dashboard_content
test(
    'Code creates alerts for phishing and suspicious verdicts',
    has_phishing_alert_creation and has_alert_push and has_alert_id_generation,
    'Should have conditional check and alert creation logic'
)

# Req 8.3: Verify alerts display in reverse chronological order
print('\n--- Requirement 8.3: Reverse Chronological Order ---')
uses_unshift = 'alerts.unshift(' in dashboard_content
test(
    'Alerts use unshift() to prepend new alerts (newest first)',
    uses_unshift,
    'Should use unshift() to add alerts to beginning of array'
)

# Req 8.4 & 8.5: Verify alert badge shows count and hides when zero
print('\n--- Requirement 8.4 & 8.5: Alert Badge Behavior ---')
has_update_alert_badge = 'function updateAlertBadge()' in dashboard_content
badge_shows_count = 'b.textContent = alerts.length' in dashboard_content
badge_hides_when_zero = "b.style.display = alerts.length ? 'inline-block' : 'none'" in dashboard_content
test(
    'Alert badge updates with count and hides when zero',
    has_update_alert_badge and badge_shows_count and badge_hides_when_zero,
    'Should have updateAlertBadge function with conditional display logic'
)

# Req 8.6: Verify alert display includes all required fields
print('\n--- Requirement 8.6: Alert Display Fields ---')
has_alert_icon = 'alert-icon' in dashboard_content
has_alert_title = 'alert-title' in dashboard_content
has_alert_msg = 'alert-msg' in dashboard_content
has_alert_url = 'alert-url' in dashboard_content
has_alert_time = 'alert-time' in dashboard_content
has_alert_actions = 'alert-actions' in dashboard_content
test(
    'Alert HTML includes all required fields (icon, title, msg, url, time, actions)',
    has_alert_icon and has_alert_title and has_alert_msg and has_alert_url and has_alert_time and has_alert_actions,
    'Should have CSS classes for all required alert fields'
)

# Req 8.7 & 8.8: Verify Dismiss button removes individual alerts
print('\n--- Requirement 8.7 & 8.8: Dismiss Individual Alert ---')
has_dismiss_alert = 'function dismissAlert(id)' in dashboard_content
dismiss_filters_by_id = 'alerts = alerts.filter(a=>a.id!==id)' in dashboard_content
dismiss_updates_ui = re.search(r'dismissAlert.*updateAlertBadge.*renderAlerts', dashboard_content, re.DOTALL)
test(
    'Dismiss button removes alert by ID and updates UI',
    has_dismiss_alert and dismiss_filters_by_id,
    'Should have dismissAlert function that filters by ID'
)

test(
    'Dismiss function updates badge and re-renders alerts',
    dismiss_updates_ui is not None,
    'Should call updateAlertBadge() and renderAlerts() after dismissal'
)

# Req 8.9: Verify Dismiss All button clears all alerts
print('\n--- Requirement 8.9: Dismiss All Alerts ---')
has_dismiss_all_alerts = 'function dismissAllAlerts()' in dashboard_content
dismiss_all_clears_array = 'alerts=[]' in dashboard_content or 'alerts = []' in dashboard_content
dismiss_all_in_html = 'dismissAllAlerts()' in dashboard_content
test(
    'Dismiss All button clears all alerts',
    has_dismiss_all_alerts and dismiss_all_clears_array and dismiss_all_in_html,
    'Should have dismissAllAlerts function that empties alerts array'
)

# Req 8.10: Verify empty state displays when no alerts
print('\n--- Requirement 8.10: Empty State Display ---')
has_empty_state_check = 'if(!alerts.length)' in dashboard_content
has_empty_state_html = 'empty-state' in dashboard_content
empty_state_in_render_alerts = re.search(r'renderAlerts.*empty-state', dashboard_content, re.DOTALL)
test(
    'Empty state displays when no alerts exist',
    has_empty_state_check and has_empty_state_html and empty_state_in_render_alerts,
    'Should check alerts.length and display empty state'
)

# Additional verification: Alert type styling
print('\n--- Additional: Alert Type Styling ---')
has_phishing_class = 'class="alert-item ${a.type}"' in dashboard_content or "class=\"alert-item ${a.type}\"" in dashboard_content
has_phishing_icon = "a.type==='phishing'?'🚨':'⚠'" in dashboard_content
test(
    'Alerts have type-specific CSS classes and icons',
    has_phishing_class and has_phishing_icon,
    'Should apply type class and conditional icon'
)

# Verify alert badge in navigation
print('\n--- Additional: Alert Badge in Navigation ---')
has_badge_in_nav = 'id="alert-badge"' in dashboard_content
badge_in_alerts_tab = re.search(r'Alerts.*alert-badge', dashboard_content)
test(
    'Alert badge is present in Alerts navigation tab',
    has_badge_in_nav and badge_in_alerts_tab,
    'Should have alert-badge element in navigation'
)

# Verify initial alerts data
print('\n--- Additional: Initial Demo Alerts ---')
has_initial_alerts = 'let alerts = [' in dashboard_content
has_phishing_alert = "type:'phishing'" in dashboard_content
has_suspicious_alert = "type:'suspicious'" in dashboard_content
test(
    'Initial demo alerts include phishing and suspicious types',
    has_initial_alerts and has_phishing_alert and has_suspicious_alert,
    'Should have sample alerts for demonstration'
)

# Verify renderAlerts function
print('\n--- Additional: Render Alerts Function ---')
has_render_alerts = 'function renderAlerts()' in dashboard_content
render_alerts_uses_map = re.search(r'renderAlerts.*alerts\.map', dashboard_content, re.DOTALL)
test(
    'renderAlerts function exists and uses map to render alerts',
    has_render_alerts and render_alerts_uses_map,
    'Should have renderAlerts function that maps over alerts array'
)

# Verify alert styling CSS
print('\n--- Additional: Alert Styling CSS ---')
has_alert_item_css = '.alert-item{' in dashboard_content or '.alert-item {' in dashboard_content
has_phishing_bg = 'alert-item.phishing' in dashboard_content
has_suspicious_bg = 'alert-item.suspicious' in dashboard_content
test(
    'Alert CSS includes styling for phishing and suspicious types',
    has_alert_item_css and has_phishing_bg and has_suspicious_bg,
    'Should have CSS rules for alert type styling'
)

# Verify Dismiss button in alert HTML
print('\n--- Additional: Dismiss Button Implementation ---')
has_dismiss_button = 'onclick="dismissAlert(' in dashboard_content
has_dismiss_all_button = 'onclick="dismissAllAlerts()"' in dashboard_content
test(
    'Dismiss buttons are properly wired to functions',
    has_dismiss_button and has_dismiss_all_button,
    'Should have onclick handlers for dismiss actions'
)

# Print summary
print('\n' + '=' * 70)
print('VERIFICATION SUMMARY')
print('=' * 70)
print(f"Total checks: {len(results['tests'])}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
success_rate = (results['passed'] / len(results['tests'])) * 100
print(f"Success rate: {success_rate:.1f}%")

if results['failed'] > 0:
    print('\nFailed checks:')
    for t in results['tests']:
        if not t['passed']:
            msg = f"  - {t['name']}"
            if t['details']:
                msg += f": {t['details']}"
            print(msg)

print('=' * 70)

# Exit with appropriate code
sys.exit(1 if results['failed'] > 0 else 0)
