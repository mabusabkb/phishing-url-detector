#!/usr/bin/env python3
"""
Task 8 Verification: Settings Panel
Verifies Requirements 10.1-10.7
"""

import re

def test(name, condition, requirement):
    """Test helper function"""
    if condition:
        print(f"✓ {name} ({requirement})")
        return True
    else:
        print(f"✗ {name} ({requirement})")
        return False

def main():
    # Read HTML file
    with open('phishing_detection_dashboard.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print('=' * 70)
    print('TASK 8 VERIFICATION: Settings Panel')
    print('=' * 70)
    print()
    
    passed = 0
    failed = 0
    
    # Extract settings panel content
    settings_match = re.search(r'<div id="panel-settings"[^>]*>(.*?)</div>\s*</div>\s*<!-- REPORT MODAL', html_content, re.DOTALL)
    if not settings_match:
        print("ERROR: Could not find settings panel")
        return 1
    
    settings_html = settings_match.group(1)
    
    # Requirement 10.1: Display API integration status for all 4 APIs
    print('Requirement 10.1: API Integration Status Display')
    print('-' * 70)
    
    api_status_blocks = re.findall(r'<div class="api-status">(.*?)</div>', settings_html, re.DOTALL)
    
    if test('Settings panel has 4 API status displays', 
            len(api_status_blocks) == 4, 'Req 10.1'):
        passed += 1
    else:
        failed += 1
    
    # Extract API names
    api_names = re.findall(r'<div class="api-name">([^<]+)</div>', settings_html)
    
    if test('Google Safe Browsing API is displayed',
            'Google Safe Browsing API' in api_names, 'Req 10.1'):
        passed += 1
    else:
        failed += 1
    
    if test('VirusTotal API is displayed',
            'VirusTotal API' in api_names, 'Req 10.1'):
        passed += 1
    else:
        failed += 1
    
    if test('ML Heuristic Engine is displayed',
            'ML Heuristic Engine' in api_names, 'Req 10.1'):
        passed += 1
    else:
        failed += 1
    
    if test('WHOIS Domain Age Checker is displayed',
            'WHOIS Domain Age Checker' in api_names, 'Req 10.1'):
        passed += 1
    else:
        failed += 1
    
    print()
    
    # Requirement 10.2: Indicate Demo mode or Active status
    print('Requirement 10.2: API Status Indicators')
    print('-' * 70)
    
    # Check for status indicators (dots)
    api_dots = re.findall(r'<div class="api-dot[^"]*">', settings_html)
    
    if test('All APIs have status indicators (dots)',
            len(api_dots) == 4, 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    # Extract status texts
    api_status_texts = re.findall(r'<div class="api-status-text">([^<]+)</div>', settings_html)
    
    if test('All APIs have status text (Demo mode or Active)',
            all(status in ['Demo mode', 'Active'] for status in api_status_texts), 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    # Check specific API statuses
    gsb_match = re.search(r'<div class="api-name">Google Safe Browsing API</div>\s*<div class="api-status-text">([^<]+)</div>', settings_html)
    if test('Google Safe Browsing shows Demo mode',
            gsb_match and gsb_match.group(1) == 'Demo mode', 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    vt_match = re.search(r'<div class="api-name">VirusTotal API</div>\s*<div class="api-status-text">([^<]+)</div>', settings_html)
    if test('VirusTotal shows Demo mode',
            vt_match and vt_match.group(1) == 'Demo mode', 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    ml_match = re.search(r'<div class="api-name">ML Heuristic Engine</div>\s*<div class="api-status-text">([^<]+)</div>', settings_html)
    if test('ML Heuristic Engine shows Active',
            ml_match and ml_match.group(1) == 'Active', 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    whois_match = re.search(r'<div class="api-name">WHOIS Domain Age Checker</div>\s*<div class="api-status-text">([^<]+)</div>', settings_html)
    if test('WHOIS Domain Age Checker shows Active',
            whois_match and whois_match.group(1) == 'Active', 'Req 10.2'):
        passed += 1
    else:
        failed += 1
    
    print()
    
    # Requirements 10.3, 10.4, 10.5: Toggle switches for 6 detection signals
    print('Requirements 10.3, 10.4, 10.5: Detection Signal Toggles')
    print('-' * 70)
    
    # Find Detection Signals section
    detection_section_match = re.search(r'<h3>Detection Signals</h3>(.*?)(?=<div class="settings-section">|</div>\s*</div>\s*<!-- REPORT MODAL)', settings_html, re.DOTALL)
    
    if not detection_section_match:
        print("ERROR: Could not find Detection Signals section")
        detection_section = ""
    else:
        detection_section = detection_section_match.group(1)
    
    # Count toggle rows in detection section
    detection_toggles = re.findall(r'<div class="toggle-row">(.*?)</div>\s*(?=<div class="toggle-row">|</div>)', detection_section, re.DOTALL)
    
    if test('Settings panel has 6 detection signal toggles',
            len(detection_toggles) >= 6, 'Req 10.3'):
        passed += 1
    else:
        failed += 1
    
    # Check for specific detection signals
    expected_signals = [
        'URL structure analysis',
        'Domain age check',
        'HTTPS / SSL verification',
        'Redirect chain analysis',
        'Brand similarity detection',
        'Page content heuristics'
    ]
    
    for signal in expected_signals:
        if test(f'Toggle for "{signal}" exists',
                signal in detection_section, 'Req 10.3'):
            passed += 1
        else:
            failed += 1
    
    # Requirement 10.4: Each toggle has label and description
    toggle_labels = re.findall(r'<div class="toggle-label">([^<]+)</div>', detection_section)
    toggle_descs = re.findall(r'<div class="toggle-desc">([^<]+)</div>', detection_section)
    
    if test('All detection signal toggles have labels',
            len(toggle_labels) >= 6 and all(len(label.strip()) > 0 for label in toggle_labels), 'Req 10.4'):
        passed += 1
    else:
        failed += 1
    
    if test('All detection signal toggles have descriptions',
            len(toggle_descs) >= 6 and all(len(desc.strip()) > 0 for desc in toggle_descs), 'Req 10.4'):
        passed += 1
    else:
        failed += 1
    
    # Requirement 10.5: Toggles show enabled state
    checkboxes_in_detection = re.findall(r'<input type="checkbox"([^>]*)>', detection_section)
    checked_count = sum(1 for cb in checkboxes_in_detection if 'checked' in cb)
    
    if test('All detection signal toggles are enabled by default',
            checked_count >= 6, 'Req 10.5'):
        passed += 1
    else:
        failed += 1
    
    print()
    
    # Requirement 10.6: Toggle switches for 2 alert preferences
    print('Requirement 10.6: Alert Preference Toggles')
    print('-' * 70)
    
    # Find Alerts & Notifications section
    alerts_section_match = re.search(r'<h3>Alerts & Notifications</h3>(.*?)(?=</div>\s*</div>\s*<!-- REPORT MODAL|$)', settings_html, re.DOTALL)
    
    if not alerts_section_match:
        print("ERROR: Could not find Alerts & Notifications section")
        alerts_section = ""
    else:
        alerts_section = alerts_section_match.group(1)
    
    # Count toggle rows in alerts section
    alert_toggles = re.findall(r'<div class="toggle-row">', alerts_section)
    
    if test('Settings panel has 2 alert preference toggles',
            len(alert_toggles) == 2, 'Req 10.6'):
        passed += 1
    else:
        failed += 1
    
    if test('Toggle for "Phishing alerts" exists',
            'Phishing alerts' in alerts_section, 'Req 10.6'):
        passed += 1
    else:
        failed += 1
    
    if test('Toggle for "Suspicious URL alerts" exists',
            'Suspicious URL alerts' in alerts_section, 'Req 10.6'):
        passed += 1
    else:
        failed += 1
    
    alert_labels = re.findall(r'<div class="toggle-label">([^<]+)</div>', alerts_section)
    alert_descs = re.findall(r'<div class="toggle-desc">([^<]+)</div>', alerts_section)
    
    if test('All alert toggles have labels',
            len(alert_labels) >= 2 and all(len(label.strip()) > 0 for label in alert_labels), 'Req 10.6'):
        passed += 1
    else:
        failed += 1
    
    if test('All alert toggles have descriptions',
            len(alert_descs) >= 2 and all(len(desc.strip()) > 0 for desc in alert_descs), 'Req 10.6'):
        passed += 1
    else:
        failed += 1
    
    print()
    
    # Requirement 10.7: Browser extension installation banner
    print('Requirement 10.7: Browser Extension Installation Banner')
    print('-' * 70)
    
    ext_banner_match = re.search(r'<div class="ext-banner">(.*?)</div>\s*<div class="settings-section">', settings_html, re.DOTALL)
    
    if test('Browser extension banner exists',
            ext_banner_match is not None, 'Req 10.7'):
        passed += 1
    else:
        failed += 1
    
    if ext_banner_match:
        ext_banner = ext_banner_match.group(1)
        
        if test('Extension banner has icon',
                '<div class="ext-icon">' in ext_banner, 'Req 10.7'):
            passed += 1
        else:
            failed += 1
        
        if test('Extension banner has info section',
                '<div class="ext-info">' in ext_banner, 'Req 10.7'):
            passed += 1
        else:
            failed += 1
        
        ext_title_match = re.search(r'<strong>([^<]+)</strong>', ext_banner)
        if test('Extension banner has title',
                ext_title_match and len(ext_title_match.group(1).strip()) > 0, 'Req 10.7'):
            passed += 1
        else:
            failed += 1
        
        ext_desc_match = re.search(r'<span>([^<]+)</span>', ext_banner)
        if test('Extension banner has description',
                ext_desc_match and len(ext_desc_match.group(1).strip()) > 0, 'Req 10.7'):
            passed += 1
        else:
            failed += 1
        
        if test('Extension banner has Install button',
                '<button class="btn-install"' in ext_banner, 'Req 10.7'):
            passed += 1
        else:
            failed += 1
    else:
        # If banner doesn't exist, fail all sub-tests
        failed += 5
        print(f"✗ Extension banner has icon (Req 10.7)")
        print(f"✗ Extension banner has info section (Req 10.7)")
        print(f"✗ Extension banner has title (Req 10.7)")
        print(f"✗ Extension banner has description (Req 10.7)")
        print(f"✗ Extension banner has Install button (Req 10.7)")
    
    print()
    print('=' * 70)
    print('VERIFICATION SUMMARY')
    print('=' * 70)
    print()
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    print('-' * 70)
    
    if failed == 0:
        print()
        print('✓ ALL REQUIREMENTS VERIFIED SUCCESSFULLY')
        print()
        return 0
    else:
        print()
        print('✗ SOME REQUIREMENTS FAILED VERIFICATION')
        print()
        return 1

if __name__ == '__main__':
    exit(main())
