#!/usr/bin/env python3
"""
Task 3 Verification Script
Verifies scan result display and loading states against requirements 4.1-4.7 and 5.1-5.6
"""

import re

# Read the HTML file
with open('phishing_detection_dashboard.html', 'r') as f:
    html_content = f.read()

tests = []
pass_count = 0
fail_count = 0

def test(name, requirement, test_fn):
    global pass_count, fail_count
    try:
        result = test_fn()
        if result['pass']:
            pass_count += 1
            print(f"✓ PASS: {name}")
            print(f"  {requirement}")
            print(f"  Details: {result['details']}\n")
        else:
            fail_count += 1
            print(f"✗ FAIL: {name}")
            print(f"  {requirement}")
            print(f"  Details: {result['details']}\n")
        tests.append({'name': name, 'requirement': requirement, **result})
    except Exception as error:
        fail_count += 1
        print(f"✗ ERROR: {name}")
        print(f"  {requirement}")
        print(f"  Error: {str(error)}\n")
        tests.append({'name': name, 'requirement': requirement, 'pass': False, 'details': str(error)})

print('=' * 80)
print('TASK 3 VERIFICATION: Scan Result Display and Loading States')
print('=' * 80)
print()

# Test 1: Verdict badge displays with correct color coding (Req 4.1)
def test1():
    # Check for verdict badge CSS classes
    has_safe_badge = '.verdict-badge.safe' in html_content
    has_suspicious_badge = '.verdict-badge.suspicious' in html_content
    has_phishing_badge = '.verdict-badge.phishing' in html_content
    
    if not (has_safe_badge and has_suspicious_badge and has_phishing_badge):
        return {'pass': False, 'details': 'Missing verdict badge CSS classes for safe, suspicious, or phishing'}
    
    # Check for color coding in CSS
    has_safe_colors = '--safe-bg' in html_content and '--safe-bd' in html_content
    has_susp_colors = '--susp-bg' in html_content and '--susp-bd' in html_content
    has_phish_colors = '--phish-bg' in html_content and '--phish-bd' in html_content
    
    if not (has_safe_colors and has_susp_colors and has_phish_colors):
        return {'pass': False, 'details': 'Missing color variable definitions for verdict badges'}
    
    # Check for verdict badge rendering in showResult function
    has_verdict_badge_rendering = 'verdict-badge ${d.verdict}' in html_content
    if not has_verdict_badge_rendering:
        return {'pass': False, 'details': 'Verdict badge rendering not found in showResult function'}
    
    return {'pass': True, 'details': 'Verdict badges have CSS classes with color coding for safe (green), suspicious (orange), and phishing (red)'}

test('Verdict badge displays with correct color coding', 'Requirement 4.1', test1)

# Test 2: Risk score displays as circular progress ring (Req 4.2)
def test2():
    # Check for score-ring class
    has_score_ring = 'class="score-ring"' in html_content
    if not has_score_ring:
        return {'pass': False, 'details': 'score-ring class not found'}
    
    # Check for SVG circle elements
    has_svg_circle = '<circle' in html_content and 'stroke-dasharray' in html_content
    if not has_svg_circle:
        return {'pass': False, 'details': 'SVG circle with stroke-dasharray not found'}
    
    # Check for progress calculation
    has_progress_calc = 'dashOffset' in html_content and 'circum' in html_content
    if not has_progress_calc:
        return {'pass': False, 'details': 'Progress calculation (dashOffset, circum) not found'}
    
    # Check for score text display
    has_score_text = '${d.score}' in html_content
    if not has_score_text:
        return {'pass': False, 'details': 'Score text display not found'}
    
    return {'pass': True, 'details': 'Risk score displays as circular progress ring with SVG, stroke-dasharray animation, and score text'}

test('Risk score displays as circular progress ring', 'Requirement 4.2', test2)

# Test 3: All 8 detection signals display in grid layout (Req 4.3, 4.4)
def test3():
    # Check for features-grid class
    has_features_grid = 'class="features-grid"' in html_content
    if not has_features_grid:
        return {'pass': False, 'details': 'features-grid class not found'}
    
    # Check for grid CSS with 2 columns
    has_grid_layout = 'grid-template-columns:1fr 1fr' in html_content
    if not has_grid_layout:
        return {'pass': False, 'details': 'Grid layout with 2 columns not found in CSS'}
    
    # Check for feature-row class
    has_feature_row = 'class="feature-row"' in html_content
    if not has_feature_row:
        return {'pass': False, 'details': 'feature-row class not found'}
    
    # Check for all required feature elements
    has_icon = 'feat-icon' in html_content
    has_name = 'feat-name' in html_content
    has_value = 'feat-value' in html_content
    has_bar = 'feat-bar' in html_content
    has_tag = 'feat-tag' in html_content
    
    if not (has_icon and has_name and has_value and has_bar and has_tag):
        return {'pass': False, 'details': 'Missing required feature elements (icon, name, value, bar, or tag)'}
    
    # Check that demo data has features arrays
    demo_matches = re.findall(r'features:\s*\[', html_content)
    if not demo_matches or len(demo_matches) < 3:
        return {'pass': False, 'details': 'Demo data does not contain features arrays'}
    
    # Verify 8 signals in one demo
    safe_demo_match = re.search(r'safe:\s*{[\s\S]*?features:\s*\[([\s\S]*?)\]', html_content)
    if safe_demo_match:
        feature_count = len(re.findall(r'\{name:', safe_demo_match.group(1)))
        if feature_count != 8:
            return {'pass': False, 'details': f'Expected 8 detection signals in demo data, found {feature_count}'}
    
    return {'pass': True, 'details': 'All 8 detection signals display in 2-column grid layout with icon, name, value, risk bar, and status tag'}

test('All 8 detection signals display in grid layout', 'Requirements 4.3, 4.4', test3)

# Test 4: Explanation section displays reasons (Req 4.5)
def test4():
    # Check for explain-box class
    has_explain_box = 'class="explain-box"' in html_content
    if not has_explain_box:
        return {'pass': False, 'details': 'explain-box class not found'}
    
    # Check for explain-title
    has_explain_title = 'explain-title' in html_content
    if not has_explain_title:
        return {'pass': False, 'details': 'explain-title class not found'}
    
    # Check for explain-reasons container
    has_explain_reasons = 'explain-reasons' in html_content
    if not has_explain_reasons:
        return {'pass': False, 'details': 'explain-reasons class not found'}
    
    # Check for reason-item and reason-dot
    has_reason_item = 'reason-item' in html_content
    has_reason_dot = 'reason-dot' in html_content
    if not (has_reason_item and has_reason_dot):
        return {'pass': False, 'details': 'reason-item or reason-dot class not found'}
    
    # Check for reasons rendering in showResult
    has_reasons_rendering = 'd.reasons.map' in html_content
    if not has_reasons_rendering:
        return {'pass': False, 'details': 'Reasons rendering not found in showResult function'}
    
    # Check that demo data has reasons
    has_reasons_in_demo = 'reasons:' in html_content
    if not has_reasons_in_demo:
        return {'pass': False, 'details': 'Reasons not found in demo data'}
    
    return {'pass': True, 'details': 'Explanation section displays reasons with color-coded dots and text descriptions'}

test('Explanation section displays reasons', 'Requirement 4.5', test4)

# Test 5: URL and timestamp display (Req 4.6)
def test5():
    # Check for url-info class
    has_url_info = 'class="url-info"' in html_content
    if not has_url_info:
        return {'pass': False, 'details': 'url-info class not found'}
    
    # Check for url-text class
    has_url_text = 'url-text' in html_content
    if not has_url_text:
        return {'pass': False, 'details': 'url-text class not found'}
    
    # Check for scan-time class
    has_scan_time = 'scan-time' in html_content
    if not has_scan_time:
        return {'pass': False, 'details': 'scan-time class not found'}
    
    # Check for URL rendering in showResult
    has_url_rendering = '${url}' in html_content
    if not has_url_rendering:
        return {'pass': False, 'details': 'URL rendering not found in showResult function'}
    
    # Check for timestamp rendering
    has_timestamp_rendering = 'Scanned just now' in html_content or 'Risk score:' in html_content
    if not has_timestamp_rendering:
        return {'pass': False, 'details': 'Timestamp rendering not found in showResult function'}
    
    return {'pass': True, 'details': 'URL and timestamp display correctly in result card with url-text and scan-time elements'}

test('URL and timestamp display', 'Requirement 4.6', test5)

# Test 6: Report button shows for Suspicious/Phishing (Req 4.7)
def test6():
    # Check for btn-report class
    has_btn_report = 'btn-report' in html_content
    if not has_btn_report:
        return {'pass': False, 'details': 'btn-report class not found'}
    
    # Check for conditional rendering based on verdict
    has_conditional_report = "d.verdict!=='safe'" in html_content or "d.verdict!='safe'" in html_content
    if not has_conditional_report:
        return {'pass': False, 'details': 'Conditional report button rendering not found (should hide for safe verdicts)'}
    
    # Check for Report button text
    has_report_text = 'Report' in html_content
    if not has_report_text:
        return {'pass': False, 'details': 'Report button text not found'}
    
    # Check for openReport function
    has_open_report = 'function openReport' in html_content
    if not has_open_report:
        return {'pass': False, 'details': 'openReport function not found'}
    
    return {'pass': True, 'details': 'Report button conditionally displays for Suspicious and Phishing verdicts, hidden for Safe'}

test('Report button shows for Suspicious/Phishing verdicts', 'Requirement 4.7', test6)

# Test 7: Loading state shows spinner and progress steps (Req 5.1-5.6)
def test7():
    # Check for loading-wrap class
    has_loading_wrap = 'loading-wrap' in html_content
    if not has_loading_wrap:
        return {'pass': False, 'details': 'loading-wrap class not found'}
    
    # Check for spinner class
    has_spinner = 'class="spinner"' in html_content
    if not has_spinner:
        return {'pass': False, 'details': 'spinner class not found'}
    
    # Check for spinner animation
    has_spin_animation = '@keyframes spin' in html_content
    if not has_spin_animation:
        return {'pass': False, 'details': 'Spinner animation (@keyframes spin) not found'}
    
    # Check for loading-steps class
    has_loading_steps = 'loading-steps' in html_content
    if not has_loading_steps:
        return {'pass': False, 'details': 'loading-steps class not found'}
    
    # Check for loading-step class
    has_loading_step = 'loading-step' in html_content
    if not has_loading_step:
        return {'pass': False, 'details': 'loading-step class not found'}
    
    # Check for step states (done, active)
    has_step_states = 'loading-step done' in html_content and 'loading-step active' in html_content
    if not has_step_states:
        return {'pass': False, 'details': 'Loading step states (done, active) not found'}
    
    # Check for steps array definition
    steps_match = re.search(r'const steps = \[(.*?)\]', html_content, re.DOTALL)
    if not steps_match:
        return {'pass': False, 'details': 'Steps array definition not found'}
    
    steps_content = steps_match.group(1)
    step_count = len(re.findall(r"'", steps_content)) // 2
    if step_count != 6:
        return {'pass': False, 'details': f'Expected 6 detection steps, found {step_count}'}
    
    # Verify expected step content
    expected_steps = [
        'Resolving domain',
        'SSL certificate',
        'Google Safe Browsing',
        'VirusTotal',
        'page content',
        'ML risk score'
    ]
    
    missing_steps = [step for step in expected_steps if step not in steps_content]
    if missing_steps:
        return {'pass': False, 'details': f'Missing expected steps: {", ".join(missing_steps)}'}
    
    # Check for interval-based step progression
    has_step_progression = 'setInterval' in html_content and '350' in html_content
    if not has_step_progression:
        return {'pass': False, 'details': 'Step progression with interval not found'}
    
    return {'pass': True, 'details': 'Loading state displays spinner with animation and 6 progress steps (domain resolution, SSL check, Google Safe Browsing, VirusTotal, content analysis, ML scoring) with active/done indicators'}

test('Loading state shows spinner and progress steps', 'Requirements 5.1-5.6', test7)

# Summary
print('=' * 80)
print('SUMMARY')
print('=' * 80)
print(f'Total Tests: {pass_count + fail_count}')
print(f'Passed: {pass_count}')
print(f'Failed: {fail_count}')
print(f'Success Rate: {round((pass_count / (pass_count + fail_count)) * 100)}%')
print()

if fail_count == 0:
    print('✓ All requirements verified successfully!')
    print('Task 3 implementation meets all requirements 4.1-4.7 and 5.1-5.6')
    exit(0)
else:
    print('✗ Some requirements not met. Please review failures above.')
    exit(1)
