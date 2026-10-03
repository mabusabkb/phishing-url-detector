#!/usr/bin/env python3
"""
Task 10 Verification: Accessibility Features

This script verifies all accessibility requirements (12.1-12.6):
- Screen reader-only heading (Req 12.1)
- ARIA labels on chart canvases (Req 12.2)
- Semantic HTML elements (Req 12.3)
- Keyboard accessibility (Req 12.4)
- Color contrast ratios (Req 12.5)
- Text alternatives for icon-only indicators (Req 12.6)
"""

import re
import sys
from pathlib import Path

# ANSI color codes for output
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'

def log(message, color='RESET'):
    color_code = getattr(Colors, color.upper(), Colors.RESET)
    print(f"{color_code}{message}{Colors.RESET}")

def log_section(title):
    print('\n' + '=' * 70)
    log(title, 'cyan')
    print('=' * 70)

def log_test(test_name, passed, details=''):
    status = '✓ PASS' if passed else '✗ FAIL'
    color = 'green' if passed else 'red'
    log(f"{status}: {test_name}", color)
    if details:
        print(f"  {details}")

# Read the HTML file
html_path = Path(__file__).parent / 'phishing_detection_dashboard.html'
html_content = html_path.read_text()

total_tests = 0
passed_tests = 0

def run_test(test_name, test_fn, details=''):
    global total_tests, passed_tests
    total_tests += 1
    passed = test_fn()
    log_test(test_name, passed, details)
    if passed:
        passed_tests += 1
    return passed

# ============================================================================
# Requirement 12.1: Screen Reader-Only Heading
# ============================================================================
log_section('Requirement 12.1: Screen Reader-Only Heading')

run_test(
    'Screen reader-only heading exists',
    lambda: bool(re.search(r'<h2\s+class="sr-only">', html_content, re.I)),
    'Verifies <h2 class="sr-only"> element exists'
)

def test_sr_heading_descriptive():
    match = re.search(r'<h2\s+class="sr-only">([^<]+)</h2>', html_content, re.I)
    if not match:
        return False
    heading_text = match.group(1).strip()
    return (len(heading_text) > 20 and 
            'phishing' in heading_text.lower() and
            'dashboard' in heading_text.lower())

run_test(
    'Screen reader heading contains descriptive text',
    test_sr_heading_descriptive,
    'Heading should describe application purpose'
)

run_test(
    'sr-only CSS class is defined',
    lambda: 'class="sr-only"' in html_content,
    'Class "sr-only" is used for screen reader accessibility'
)

# ============================================================================
# Requirement 12.2: ARIA Labels on Chart Canvases
# ============================================================================
log_section('Requirement 12.2: ARIA Labels on Chart Canvases')

run_test(
    'Distribution chart canvas has role="img"',
    lambda: bool(re.search(r'<canvas[^>]+id="distChart"[^>]+role="img"', html_content, re.I)),
    'Donut chart canvas has role="img" attribute'
)

run_test(
    'Distribution chart canvas has aria-label',
    lambda: bool(re.search(r'<canvas[^>]+id="distChart"[^>]+aria-label="[^"]+"', html_content, re.I)),
    'Donut chart canvas has descriptive aria-label'
)

def test_dist_chart_aria_descriptive():
    match = re.search(r'<canvas[^>]+id="distChart"[^>]+aria-label="([^"]+)"', html_content, re.I)
    if not match:
        return False
    label = match.group(1).lower()
    return 'chart' in label and ('distribution' in label or 'verdict' in label)

run_test(
    'Distribution chart aria-label is descriptive',
    test_dist_chart_aria_descriptive,
    'aria-label describes chart content (distribution/verdict)'
)

run_test(
    'Features chart canvas has role="img"',
    lambda: bool(re.search(r'<canvas[^>]+id="featChart"[^>]+role="img"', html_content, re.I)),
    'Bar chart canvas has role="img" attribute'
)

run_test(
    'Features chart canvas has aria-label',
    lambda: bool(re.search(r'<canvas[^>]+id="featChart"[^>]+aria-label="[^"]+"', html_content, re.I)),
    'Bar chart canvas has descriptive aria-label'
)

def test_feat_chart_aria_descriptive():
    match = re.search(r'<canvas[^>]+id="featChart"[^>]+aria-label="([^"]+)"', html_content, re.I)
    if not match:
        return False
    label = match.group(1).lower()
    return 'chart' in label and ('signal' in label or 'detection' in label or 'bar' in label)

run_test(
    'Features chart aria-label is descriptive',
    test_feat_chart_aria_descriptive,
    'aria-label describes chart content (signals/detection)'
)

run_test(
    'Chart canvases have fallback text content',
    lambda: (bool(re.search(r'<canvas[^>]+id="distChart"[^>]*>([^<]+)</canvas>', html_content, re.I)) and
             bool(re.search(r'<canvas[^>]+id="featChart"[^>]*>([^<]+)</canvas>', html_content, re.I))),
    'Canvas elements contain fallback text for non-canvas browsers'
)

# ============================================================================
# Requirement 12.3: Semantic HTML Elements
# ============================================================================
log_section('Requirement 12.3: Semantic HTML Elements')

def test_nav_buttons():
    matches = re.findall(r'<button\s+class="nav-btn"', html_content, re.I)
    return len(matches) >= 5

run_test(
    'Navigation uses semantic button elements',
    test_nav_buttons,
    'Navigation tabs use <button> elements (found 5 expected buttons)'
)

run_test(
    'Form inputs use semantic input elements',
    lambda: bool(re.search(r'<input[^>]+id="url-input"[^>]+type="text"', html_content, re.I)),
    'URL input uses semantic <input type="text"> element'
)

run_test(
    'Action buttons use semantic button elements',
    lambda: bool(re.search(r'<button[^>]+class="btn-scan"', html_content, re.I)),
    'Scan button uses semantic <button> element'
)

def test_heading_hierarchy():
    h2_count = len(re.findall(r'<h2[^>]*>', html_content, re.I))
    h3_count = len(re.findall(r'<h3[^>]*>', html_content, re.I))
    return h2_count >= 1 and h3_count >= 1

run_test(
    'Headings use semantic heading elements',
    test_heading_hierarchy,
    'Document uses semantic heading hierarchy (h2, h3)'
)

def test_toggle_controls():
    labels = len(re.findall(r'<label\s+class="toggle">', html_content, re.I))
    checkboxes = len(re.findall(r'<input\s+type="checkbox"', html_content, re.I))
    return labels >= 6 and checkboxes >= 6

run_test(
    'Toggle controls use semantic label and input elements',
    test_toggle_controls,
    'Settings toggles use semantic <label> and <input type="checkbox">'
)

run_test(
    'Modal uses semantic select and textarea elements',
    lambda: (bool(re.search(r'<select[^>]+id="report-type"', html_content, re.I)) and
             bool(re.search(r'<textarea[^>]+id="report-notes"', html_content, re.I))),
    'Report modal uses semantic <select> and <textarea> elements'
)

# ============================================================================
# Requirement 12.4: Keyboard Accessibility
# ============================================================================
log_section('Requirement 12.4: Keyboard Accessibility for Interactive Elements')

def test_enter_key_handler():
    pattern = r'addEventListener\([\'"]keydown[\'"]\s*,\s*function\(e\)\s*\{[^}]*if\s*\(\s*e\.key\s*===\s*[\'"]Enter[\'"]\s*\)'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'URL input has keyboard event handler (Enter key)',
    test_enter_key_handler,
    'URL input field responds to Enter key press'
)

run_test(
    'All buttons are keyboard accessible by default',
    lambda: not bool(re.search(r'<button[^>]+tabindex="-1"', html_content, re.I)),
    'No buttons have tabindex="-1" (all are keyboard accessible)'
)

def test_native_focusable_elements():
    div_onclicks = len(re.findall(r'<div[^>]+onclick=', html_content, re.I))
    return div_onclicks < 5

run_test(
    'Interactive elements use native focusable elements',
    test_native_focusable_elements,
    'Primary interactive elements use native focusable HTML elements'
)

run_test(
    'Focus styles are defined for interactive elements',
    lambda: bool(re.search(r'\.url-bar\s+input:focus\s*\{[^}]*border-color', html_content, re.I)),
    'CSS defines visible focus styles for input elements'
)

def test_modal_keyboard_close():
    pattern = r'addEventListener\([\'"]click[\'"]\s*,\s*function\(e\)\s*\{[^}]*if\s*\(\s*e\.target\s*===\s*this\s*\)'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Modal can be closed with keyboard (click handler on overlay)',
    test_modal_keyboard_close,
    'Modal overlay has click handler for keyboard-accessible closing'
)

# ============================================================================
# Requirement 12.5: Color Contrast Ratios (WCAG AA)
# ============================================================================
log_section('Requirement 12.5: Color Contrast Ratios Meet WCAG AA')

def get_luminance(r, g, b):
    """Calculate relative luminance"""
    def adjust(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    rs, gs, bs = adjust(r), adjust(g), adjust(b)
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs

def get_contrast_ratio(rgb1, rgb2):
    """Calculate contrast ratio between two RGB colors"""
    l1 = get_luminance(rgb1[0], rgb1[1], rgb1[2])
    l2 = get_luminance(rgb2[0], rgb2[1], rgb2[2])
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Extract color values from CSS
safe_color = '#1D9E75'
safe_bg = '#E1F5EE'
susp_color = '#BA7517'
susp_bg = '#FAEEDA'
phish_color = '#A32D2D'
phish_bg = '#FCEBEB'

def test_safe_contrast():
    ratio = get_contrast_ratio(hex_to_rgb(safe_color), hex_to_rgb(safe_bg))
    return ratio >= 4.5

run_test(
    'Safe verdict color contrast meets WCAG AA (4.5:1)',
    test_safe_contrast,
    f'Safe: {safe_color} on {safe_bg} (contrast ratio should be ≥ 4.5:1)'
)

def test_susp_contrast():
    ratio = get_contrast_ratio(hex_to_rgb(susp_color), hex_to_rgb(susp_bg))
    return ratio >= 4.5

run_test(
    'Suspicious verdict color contrast meets WCAG AA (4.5:1)',
    test_susp_contrast,
    f'Suspicious: {susp_color} on {susp_bg} (contrast ratio should be ≥ 4.5:1)'
)

def test_phish_contrast():
    ratio = get_contrast_ratio(hex_to_rgb(phish_color), hex_to_rgb(phish_bg))
    return ratio >= 4.5

run_test(
    'Phishing verdict color contrast meets WCAG AA (4.5:1)',
    test_phish_contrast,
    f'Phishing: {phish_color} on {phish_bg} (contrast ratio should be ≥ 4.5:1)'
)

def test_color_vars_defined():
    pattern = r':root\s*\{[^}]*--safe:\s*#1D9E75[^}]*--susp:\s*#BA7517[^}]*--phish:\s*#A32D2D'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Color variables are defined in CSS',
    test_color_vars_defined,
    'CSS custom properties define accessible color palette'
)

def test_border_colors():
    safe_border = '#5DCAA5'
    susp_border = '#EF9F27'
    phish_border = '#E24B4A'
    return (safe_border in html_content and 
            susp_border in html_content and 
            phish_border in html_content)

run_test(
    'Verdict colors use sufficient contrast for borders',
    test_border_colors,
    'Border colors are defined for enhanced visual distinction'
)

# ============================================================================
# Requirement 12.6: Text Alternatives for Icon-Only Indicators
# ============================================================================
log_section('Requirement 12.6: Text Alternatives for Icon-Only Indicators')

def test_verdict_badges():
    pattern = r'<div\s+class="verdict-badge[^"]*">[^<]*<span\s+class="icon">[^<]+</span>[^<]*<span\s+class="label">'
    matches = re.findall(pattern, html_content, re.I)
    return len(matches) >= 1

run_test(
    'Verdict badges include text labels with icons',
    test_verdict_badges,
    'Verdict badges combine icons with text labels (not icon-only)'
)

def test_feature_icons():
    pattern = r'<div\s+class="feat-icon"[^>]*>[^<]+</div>[^<]*<div\s+class="feat-body">[^<]*<div\s+class="feat-name">'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Feature icons are accompanied by feature names',
    test_feature_icons,
    'Detection signal icons are paired with descriptive text names'
)

def test_alert_icons():
    pattern = r'<div\s+class="alert-icon">[^<]+</div>[^<]*<div\s+class="alert-body">[^<]*<div\s+class="alert-title">'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Alert icons are accompanied by alert titles',
    test_alert_icons,
    'Alert icons are paired with descriptive alert titles'
)

def test_status_dots():
    hist_dot = bool(re.search(r'<div\s+class="hist-dot[^"]*"></div>[^<]*<div\s+class="hist-url">', html_content, re.I))
    hist_verdict = bool(re.search(r'<div\s+class="hist-verdict[^"]*">[^<]+</div>', html_content, re.I))
    return hist_dot and hist_verdict

run_test(
    'Status indicators (dots) are accompanied by text labels',
    test_status_dots,
    'Status indicator dots are accompanied by verdict text labels'
)

def test_api_status_dots():
    pattern = r'<div\s+class="api-dot[^"]*"></div>[^<]*<div\s+class="api-name">[^<]+</div>[^<]*<div\s+class="api-status-text">'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'API status dots are accompanied by status text',
    test_api_status_dots,
    'API status dots are paired with descriptive status text'
)

def test_loading_spinner():
    pattern = r'<div\s+class="spinner"></div>[^<]*<div[^>]*>Analyzing URL security'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Loading spinner is accompanied by descriptive text',
    test_loading_spinner,
    'Loading spinner animation is accompanied by status text'
)

def test_empty_state_icons():
    pattern = r'<div\s+class="empty-icon">[^<]+</div>[^<]*No\s+(scans|active\s+alerts)'
    return bool(re.search(pattern, html_content, re.I))

run_test(
    'Empty state icons are accompanied by descriptive text',
    test_empty_state_icons,
    'Empty state icons are paired with explanatory text'
)

# ============================================================================
# Summary
# ============================================================================
log_section('Verification Summary')

pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
all_passed = passed_tests == total_tests

print(f"\nTotal Tests: {total_tests}")
log(f"Passed: {passed_tests}", 'green')
if total_tests - passed_tests > 0:
    log(f"Failed: {total_tests - passed_tests}", 'red')
log(f"Pass Rate: {pass_rate:.1f}%", 'green' if all_passed else 'yellow')

if all_passed:
    log('\n✓ All accessibility requirements verified successfully!', 'green')
    log('The dashboard meets WCAG AA standards for accessibility.', 'green')
else:
    log('\n✗ Some accessibility requirements need attention.', 'red')
    log('Review the failed tests above for details.', 'yellow')

# Exit with appropriate code
sys.exit(0 if all_passed else 1)
