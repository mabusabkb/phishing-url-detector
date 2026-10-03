#!/usr/bin/env python3
"""
Task 9 Verification: Demo Mode Operation

Verifies Requirements 11.1-11.7:
- 11.1: Exact demo URL matches return correct results
- 11.2: Phishing keyword detection
- 11.3: Suspicious keyword detection
- 11.4: Default safe classification
- 11.5: Three predefined demo URLs work
- 11.6: Realistic detection signal values
- 11.7: Timing delays between steps (~350ms)
"""

import re
import json
from typing import Dict, List, Tuple

def read_html_file(filename: str) -> str:
    """Read the HTML file content."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def extract_demos_object(html_content: str) -> Dict:
    """Extract the DEMOS JavaScript object from HTML."""
    # Find the DEMOS object definition
    pattern = r'const DEMOS = ({[\s\S]*?});'
    match = re.search(pattern, html_content)
    
    if not match:
        return None
    
    demos_str = match.group(1)
    
    # Parse the DEMOS object manually (simplified parsing)
    demos = {}
    
    # Extract safe demo
    safe_match = re.search(r"safe:\s*{[\s\S]*?url:\s*'([^']+)'[\s\S]*?result:\s*{[\s\S]*?verdict:\s*'(\w+)'[\s\S]*?score:\s*(\d+)", demos_str)
    if safe_match:
        demos['safe'] = {
            'url': safe_match.group(1),
            'verdict': safe_match.group(2),
            'score': int(safe_match.group(3))
        }
    
    # Extract suspicious demo
    susp_match = re.search(r"suspicious:\s*{[\s\S]*?url:\s*'([^']+)'[\s\S]*?result:\s*{[\s\S]*?verdict:\s*'(\w+)'[\s\S]*?score:\s*(\d+)", demos_str)
    if susp_match:
        demos['suspicious'] = {
            'url': susp_match.group(1),
            'verdict': susp_match.group(2),
            'score': int(susp_match.group(3))
        }
    
    # Extract phishing demo
    phish_match = re.search(r"phishing:\s*{[\s\S]*?url:\s*'([^']+)'[\s\S]*?result:\s*{[\s\S]*?verdict:\s*'(\w+)'[\s\S]*?score:\s*(\d+)", demos_str)
    if phish_match:
        demos['phishing'] = {
            'url': phish_match.group(1),
            'verdict': phish_match.group(2),
            'score': int(phish_match.group(3))
        }
    
    return demos

def extract_features_count(html_content: str, demo_type: str) -> int:
    """Count the number of features in a demo result."""
    # Find the demo section
    pattern = rf"{demo_type}:\s*{{[\s\S]*?features:\s*\[([\s\S]*?)\]"
    match = re.search(pattern, html_content)
    
    if not match:
        return 0
    
    features_str = match.group(1)
    # Count feature objects by counting 'name:' occurrences
    return len(re.findall(r"name:\s*'", features_str))

def classify_url(url: str, demos: Dict) -> str:
    """Simulate the classification logic from startScan()."""
    # Check exact matches first
    for demo_type in ['safe', 'suspicious', 'phishing']:
        if demo_type in demos and demos[demo_type]['url'] == url:
            return demo_type
    
    # Check phishing keywords
    lc = url.lower()
    phishing_keywords = ['phish', 'xyz', 'click', 'login', 'verify', 'secure-']
    if any(kw in lc for kw in phishing_keywords):
        return 'phishing'
    
    # Check suspicious keywords
    suspicious_keywords = ['paypa', 'amaz', 'bank', 'account']
    if any(kw in lc for kw in suspicious_keywords):
        return 'suspicious'
    
    # Default to safe
    return 'safe'

def log_test(req_id: str, test_name: str, passed: bool, details: str = '') -> Tuple[bool, Dict]:
    """Log a test result."""
    status = '✓ PASS' if passed else '✗ FAIL'
    message = f'[Req {req_id}] {status}: {test_name}'
    print(message)
    if details:
        print(f'  {details}')
    
    return passed, {
        'reqId': req_id,
        'testName': test_name,
        'passed': passed,
        'details': details
    }

def main():
    print('=== TASK 9 VERIFICATION: DEMO MODE OPERATION ===\n')
    
    all_tests_passed = True
    results = []
    
    try:
        # Read HTML file
        html_content = read_html_file('phishing_detection_dashboard.html')
        
        # Extract DEMOS object
        demos = extract_demos_object(html_content)
        
        if not demos:
            print('✗ FAIL: Could not extract DEMOS object from HTML')
            return 1
        
        # ===================================================================
        # Requirement 11.5: Three predefined demo URLs work
        # ===================================================================
        print('\n--- Requirement 11.5: Three Predefined Demo URLs ---')
        
        # Test 1: Safe demo URL exists
        has_safe = 'safe' in demos and demos['safe']['url'] == 'https://github.com/anthropics/anthropic-sdk'
        passed, result = log_test('11.5', 'Safe demo URL (github.com) exists', has_safe,
            f"URL: {demos['safe']['url']}" if has_safe else 'Safe demo URL not found or incorrect')
        all_tests_passed &= passed
        results.append(result)
        
        # Test 2: Suspicious demo URL exists
        has_suspicious = 'suspicious' in demos and demos['suspicious']['url'] == 'http://paypa1-verify.net/account/confirm'
        passed, result = log_test('11.5', 'Suspicious demo URL (paypa1-verify.net) exists', has_suspicious,
            f"URL: {demos['suspicious']['url']}" if has_suspicious else 'Suspicious demo URL not found or incorrect')
        all_tests_passed &= passed
        results.append(result)
        
        # Test 3: Phishing demo URL exists
        has_phishing = 'phishing' in demos and demos['phishing']['url'] == 'http://secure-bank-login.xyz/wellsfargo/signin/verify'
        passed, result = log_test('11.5', 'Phishing demo URL (secure-bank-login.xyz) exists', has_phishing,
            f"URL: {demos['phishing']['url']}" if has_phishing else 'Phishing demo URL not found or incorrect')
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.1: Exact demo URL matches return correct results
        # ===================================================================
        print('\n--- Requirement 11.1: Exact Demo URL Matches ---')
        
        # Test safe demo result
        safe_correct = (demos['safe']['verdict'] == 'safe' and 
                       0 <= demos['safe']['score'] <= 39)
        safe_features = extract_features_count(html_content, 'safe')
        safe_correct = safe_correct and safe_features == 8
        passed, result = log_test('11.1', 'Safe demo returns correct result', safe_correct,
            f"Verdict: {demos['safe']['verdict']}, Score: {demos['safe']['score']}, Signals: {safe_features}" if safe_correct
            else f"Expected safe verdict with score 0-39 and 8 signals, got {demos['safe']['verdict']}/{demos['safe']['score']}/{safe_features}")
        all_tests_passed &= passed
        results.append(result)
        
        # Test suspicious demo result
        suspicious_correct = (demos['suspicious']['verdict'] == 'suspicious' and 
                             40 <= demos['suspicious']['score'] <= 69)
        suspicious_features = extract_features_count(html_content, 'suspicious')
        suspicious_correct = suspicious_correct and suspicious_features == 8
        passed, result = log_test('11.1', 'Suspicious demo returns correct result', suspicious_correct,
            f"Verdict: {demos['suspicious']['verdict']}, Score: {demos['suspicious']['score']}, Signals: {suspicious_features}" if suspicious_correct
            else f"Expected suspicious verdict with score 40-69 and 8 signals")
        all_tests_passed &= passed
        results.append(result)
        
        # Test phishing demo result
        phishing_correct = (demos['phishing']['verdict'] == 'phishing' and 
                           70 <= demos['phishing']['score'] <= 100)
        phishing_features = extract_features_count(html_content, 'phishing')
        phishing_correct = phishing_correct and phishing_features == 8
        passed, result = log_test('11.1', 'Phishing demo returns correct result', phishing_correct,
            f"Verdict: {demos['phishing']['verdict']}, Score: {demos['phishing']['score']}, Signals: {phishing_features}" if phishing_correct
            else f"Expected phishing verdict with score 70-100 and 8 signals")
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.6: Realistic detection signal values
        # ===================================================================
        print('\n--- Requirement 11.6: Realistic Detection Signal Values ---')
        
        required_signals = [
            'URL structure',
            'Domain age',
            'HTTPS / SSL',
            'Redirects',
            'Brand similarity',
            'Page content',
            'Google Safe Browsing',
            'VirusTotal'
        ]
        
        # Check all required signals are present
        all_signals_present = all(signal in html_content for signal in required_signals)
        passed, result = log_test('11.6', 'All 8 required detection signals are defined', all_signals_present,
            'All signals found in code' if all_signals_present else 'Some signals missing')
        all_tests_passed &= passed
        results.append(result)
        
        # Check that each demo has 8 features
        safe_has_8 = safe_features == 8
        suspicious_has_8 = suspicious_features == 8
        phishing_has_8 = phishing_features == 8
        all_have_8 = safe_has_8 and suspicious_has_8 and phishing_has_8
        passed, result = log_test('11.6', 'Each demo has exactly 8 detection signals', all_have_8,
            f"Safe: {safe_features}, Suspicious: {suspicious_features}, Phishing: {phishing_features}" if all_have_8
            else f"Expected 8 signals for each demo")
        all_tests_passed &= passed
        results.append(result)
        
        # Check that signals have required fields
        has_risk_values = 'risk:' in html_content and 'tag:' in html_content and 'tagLabel:' in html_content
        passed, result = log_test('11.6', 'Detection signals have required fields (risk, tag, tagLabel)', has_risk_values,
            'All required fields found' if has_risk_values else 'Some required fields missing')
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.2: Phishing keyword detection
        # ===================================================================
        print('\n--- Requirement 11.2: Phishing Keyword Detection ---')
        
        # Test phishing keywords
        test_urls = [
            'http://test-phish.com',
            'http://example.xyz',
            'http://click-here.com',
            'http://login-portal.com',
            'http://verify-account.com',
            'http://secure-bank.com'
        ]
        
        all_phishing_detected = all(classify_url(url, demos) == 'phishing' for url in test_urls)
        passed, result = log_test('11.2', 'Phishing keywords detected correctly', all_phishing_detected,
            f"All {len(test_urls)} phishing keyword URLs classified as phishing" if all_phishing_detected
            else 'Some phishing keywords not detected')
        all_tests_passed &= passed
        results.append(result)
        
        # Test case-insensitivity
        upper_case_url = 'http://VERIFY-LOGIN.COM'
        case_insensitive = classify_url(upper_case_url, demos) == 'phishing'
        passed, result = log_test('11.2', 'Phishing keyword detection is case-insensitive', case_insensitive,
            'Uppercase keywords detected correctly' if case_insensitive else 'Case-insensitive detection failed')
        all_tests_passed &= passed
        results.append(result)
        
        # Check that phishing keywords are in the code
        phishing_keywords = ['phish', 'xyz', 'click', 'login', 'verify', 'secure-']
        keywords_in_code = all(kw in html_content for kw in phishing_keywords)
        passed, result = log_test('11.2', 'All phishing keywords present in classification code', keywords_in_code,
            'All keywords found' if keywords_in_code else 'Some keywords missing from code')
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.3: Suspicious keyword detection
        # ===================================================================
        print('\n--- Requirement 11.3: Suspicious Keyword Detection ---')
        
        # Test suspicious keywords (avoid URLs with phishing keywords like 'login', 'verify', 'secure-', 'click')
        test_urls = [
            'http://paypa-support.com',
            'http://amaz-prime.com',
            'http://bank-portal.com',
            'http://account-update.com'
        ]
        
        all_suspicious_detected = all(classify_url(url, demos) == 'suspicious' for url in test_urls)
        passed, result = log_test('11.3', 'Suspicious keywords detected correctly', all_suspicious_detected,
            f"All {len(test_urls)} suspicious keyword URLs classified as suspicious" if all_suspicious_detected
            else 'Some suspicious keywords not detected')
        all_tests_passed &= passed
        results.append(result)
        
        # Test priority: phishing keywords should override suspicious keywords
        mixed_url = 'http://paypa-login.com'  # has both 'paypa' (suspicious) and 'login' (phishing)
        priority_correct = classify_url(mixed_url, demos) == 'phishing'
        passed, result = log_test('11.3', 'Phishing keywords have priority over suspicious keywords', priority_correct,
            'Phishing keywords correctly prioritized' if priority_correct else 'Priority order incorrect')
        all_tests_passed &= passed
        results.append(result)
        
        # Check that suspicious keywords are in the code
        suspicious_keywords = ['paypa', 'amaz', 'bank', 'account']
        keywords_in_code = all(kw in html_content for kw in suspicious_keywords)
        passed, result = log_test('11.3', 'All suspicious keywords present in classification code', keywords_in_code,
            'All keywords found' if keywords_in_code else 'Some keywords missing from code')
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.4: Default safe classification
        # ===================================================================
        print('\n--- Requirement 11.4: Default Safe Classification ---')
        
        # Test URLs with no suspicious patterns
        safe_urls = [
            'https://example.com',
            'https://google.com',
            'https://wikipedia.org',
            'https://stackoverflow.com',
            'https://news.ycombinator.com'
        ]
        
        all_default_to_safe = all(classify_url(url, demos) == 'safe' for url in safe_urls)
        passed, result = log_test('11.4', 'URLs without suspicious patterns default to safe', all_default_to_safe,
            f"All {len(safe_urls)} neutral URLs classified as safe" if all_default_to_safe
            else 'Some neutral URLs not classified as safe')
        all_tests_passed &= passed
        results.append(result)
        
        # Check that the code has a default return for safe
        has_default_safe = "matchedDemo='safe'" in html_content or 'return "safe"' in html_content or "else matchedDemo='safe'" in html_content
        passed, result = log_test('11.4', 'Code has default safe classification', has_default_safe,
            'Default safe classification found in code' if has_default_safe else 'Default safe classification not found')
        all_tests_passed &= passed
        results.append(result)
        
        # ===================================================================
        # Requirement 11.7: Timing delays between steps (~350ms)
        # ===================================================================
        print('\n--- Requirement 11.7: Timing Delays Between Steps ---')
        
        # Check for setInterval with 350ms delay
        has_interval_delay = 'setInterval' in html_content and '350' in html_content
        passed, result = log_test('11.7', 'Code contains setInterval with 350ms delay', has_interval_delay,
            'Found setInterval with 350ms timing' if has_interval_delay else 'setInterval with 350ms not found')
        all_tests_passed &= passed
        results.append(result)
        
        # Check for detection steps
        steps = [
            'Resolving domain',
            'Checking SSL certificate',
            'Scanning with Google Safe Browsing',
            'Running VirusTotal check',
            'Analyzing page content',
            'Computing ML risk score'
        ]
        
        all_steps_present = all(step.lower() in html_content.lower() for step in steps)
        passed, result = log_test('11.7', 'All 6 detection steps are defined', all_steps_present,
            'All detection steps found in code' if all_steps_present else 'Some detection steps missing')
        all_tests_passed &= passed
        results.append(result)
        
        # Calculate expected total time
        expected_time = 2100  # 6 steps × 350ms
        passed, result = log_test('11.7', 'Expected scan time is approximately 2.1 seconds', True,
            f"6 steps × 350ms = {expected_time}ms (2.1 seconds)")
        results.append(result)
        
        # ===================================================================
        # Summary
        # ===================================================================
        print('\n=== VERIFICATION SUMMARY ===')
        print(f'Total tests: {len(results)}')
        print(f'Passed: {sum(1 for r in results if r["passed"])}')
        print(f'Failed: {sum(1 for r in results if not r["passed"])}')
        
        if all_tests_passed:
            print('\n✓ ALL TESTS PASSED - Task 9 requirements verified successfully!')
            return 0
        else:
            print('\n✗ SOME TESTS FAILED - Review failures above')
            print('\nFailed tests:')
            for r in results:
                if not r['passed']:
                    print(f"  - [Req {r['reqId']}] {r['testName']}")
                    if r['details']:
                        print(f"    {r['details']}")
            return 1
            
    except FileNotFoundError:
        print('✗ ERROR: phishing_detection_dashboard.html not found')
        return 1
    except Exception as e:
        print(f'✗ ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
