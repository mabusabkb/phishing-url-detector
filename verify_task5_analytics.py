#!/usr/bin/env python3
"""
Task 5 Verification: Analytics Dashboard
Verifies Requirements 7.1-7.9
"""

import re
import sys

def read_file(filename):
    """Read the HTML file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)

def verify_analytics_dashboard(html_content):
    """Verify all analytics dashboard requirements"""
    results = []
    
    # Requirement 7.1: Total scanned URLs count
    has_stat_total = 'id="stat-total"' in html_content or "id='stat-total'" in html_content
    results.append({
        'req': '7.1',
        'description': 'Display total scanned URLs count',
        'passed': has_stat_total,
        'details': 'Found #stat-total element' if has_stat_total else 'Missing #stat-total element'
    })
    
    # Requirement 7.2: Phishing URLs blocked count
    has_stat_phish = 'id="stat-phish"' in html_content or "id='stat-phish'" in html_content
    results.append({
        'req': '7.2',
        'description': 'Display phishing URLs blocked count',
        'passed': has_stat_phish,
        'details': 'Found #stat-phish element' if has_stat_phish else 'Missing #stat-phish element'
    })
    
    # Requirement 7.3: Suspicious URLs flagged count
    has_stat_susp = 'id="stat-susp"' in html_content or "id='stat-susp'" in html_content
    results.append({
        'req': '7.3',
        'description': 'Display suspicious URLs flagged count',
        'passed': has_stat_susp,
        'details': 'Found #stat-susp element' if has_stat_susp else 'Missing #stat-susp element'
    })
    
    # Requirement 7.4: Detection rate display
    has_stat_rate = 'id="stat-rate"' in html_content or "id='stat-rate'" in html_content
    results.append({
        'req': '7.4',
        'description': 'Display detection rate',
        'passed': has_stat_rate,
        'details': 'Found #stat-rate element' if has_stat_rate else 'Missing #stat-rate element'
    })
    
    # Requirement 7.5: Detection rate calculation formula
    # Check if the formula (phish + susp) / total * 100 is implemented
    formula_pattern = r'\(phish\+susp\)/total\*100|\(phishing\+suspicious\)/total\*100'
    has_formula = bool(re.search(formula_pattern, html_content, re.IGNORECASE))
    
    # Also check for the actual implementation
    calc_pattern = r'Math\.round\(\(phish\+susp\)/total\*100\)'
    has_calc = bool(re.search(calc_pattern, html_content))
    
    results.append({
        'req': '7.5',
        'description': 'Detection rate formula: (phishing + suspicious) / total × 100',
        'passed': has_calc,
        'details': 'Found correct formula implementation' if has_calc else 'Formula implementation not found or incorrect'
    })
    
    # Requirement 7.6: Donut chart for verdict distribution
    has_dist_chart = 'id="distChart"' in html_content or "id='distChart'" in html_content
    has_doughnut_type = "'doughnut'" in html_content or '"doughnut"' in html_content
    has_cutout = "'65%'" in html_content or '"65%"' in html_content or "cutout:'65%'" in html_content
    
    results.append({
        'req': '7.6',
        'description': 'Display donut chart showing verdict distribution',
        'passed': has_dist_chart and has_doughnut_type,
        'details': f'Chart canvas: {has_dist_chart}, Doughnut type: {has_doughnut_type}, 65% cutout: {has_cutout}'
    })
    
    # Requirement 7.7: Bar chart for top triggered signals
    has_feat_chart = 'id="featChart"' in html_content or "id='featChart'" in html_content
    has_bar_type = "'bar'" in html_content or '"bar"' in html_content
    
    results.append({
        'req': '7.7',
        'description': 'Display bar chart showing top triggered detection signals',
        'passed': has_feat_chart and has_bar_type,
        'details': f'Chart canvas: {has_feat_chart}, Bar type: {has_bar_type}'
    })
    
    # Requirement 7.8: Charts update when switching to Analytics tab
    # Check if renderAnalytics function exists and is called on tab switch
    has_render_analytics = 'function renderAnalytics' in html_content or 'renderAnalytics()' in html_content
    tab_switch_pattern = r"if\(tab===?['\"]analytics['\"].*renderAnalytics"
    has_tab_switch = bool(re.search(tab_switch_pattern, html_content, re.IGNORECASE))
    
    results.append({
        'req': '7.8',
        'description': 'Charts update when switching to Analytics tab',
        'passed': has_render_analytics and has_tab_switch,
        'details': f'renderAnalytics function: {has_render_analytics}, Tab switch handler: {has_tab_switch}'
    })
    
    # Requirement 7.9: Color coding verification
    # Check for the three color codes
    has_green_safe = '#1D9E75' in html_content  # Safe color
    has_orange_susp = '#EF9F27' in html_content  # Suspicious color
    has_red_phish = '#E24B4A' in html_content  # Phishing color
    
    # Check if colors are used in chart configuration
    chart_colors_pattern = r"backgroundColor:\s*\[[^\]]*#1D9E75[^\]]*#EF9F27[^\]]*#E24B4A[^\]]*\]"
    has_chart_colors = bool(re.search(chart_colors_pattern, html_content))
    
    results.append({
        'req': '7.9',
        'description': 'Color coding: green=Safe, orange=Suspicious, red=Phishing',
        'passed': has_green_safe and has_orange_susp and has_red_phish,
        'details': f'Green (#1D9E75): {has_green_safe}, Orange (#EF9F27): {has_orange_susp}, Red (#E24B4A): {has_red_phish}, Chart colors: {has_chart_colors}'
    })
    
    # Additional checks for stat card styling
    stat_phish_color = 'style="color:var(--phish)"' in html_content or 'style="color:#A32D2D"' in html_content
    stat_susp_color = 'style="color:var(--susp)"' in html_content or 'style="color:#BA7517"' in html_content
    stat_rate_color = 'style="color:var(--safe)"' in html_content or 'style="color:#1D9E75"' in html_content
    
    results.append({
        'req': '7.9',
        'description': 'Stat cards use correct color coding',
        'passed': stat_phish_color and stat_susp_color and stat_rate_color,
        'details': f'Phishing stat color: {stat_phish_color}, Suspicious stat color: {stat_susp_color}, Detection rate color: {stat_rate_color}'
    })
    
    return results

def print_results(results):
    """Print verification results"""
    print("\n" + "="*80)
    print("TASK 5: ANALYTICS DASHBOARD VERIFICATION")
    print("Requirements 7.1-7.9")
    print("="*80 + "\n")
    
    passed_count = sum(1 for r in results if r['passed'])
    total_count = len(results)
    
    for result in results:
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"[{status}] Requirement {result['req']}: {result['description']}")
        print(f"        {result['details']}")
        print()
    
    print("="*80)
    print(f"SUMMARY: {passed_count}/{total_count} tests passed")
    print("="*80 + "\n")
    
    return passed_count == total_count

def main():
    """Main verification function"""
    print("Reading phishing_detection_dashboard.html...")
    html_content = read_file('phishing_detection_dashboard.html')
    
    print("Running verification tests...")
    results = verify_analytics_dashboard(html_content)
    
    all_passed = print_results(results)
    
    if all_passed:
        print("✓ All analytics dashboard requirements verified successfully!")
        sys.exit(0)
    else:
        print("✗ Some requirements failed verification")
        sys.exit(1)

if __name__ == '__main__':
    main()
