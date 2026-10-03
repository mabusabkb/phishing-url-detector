#!/usr/bin/env python3
"""
Task 4 Verification: Scan History Functionality
Tests Requirements 6.1-6.8
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Test results tracking
results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'tests': []
}

def log_test(requirement, name, passed, details):
    """Log test result"""
    results['total'] += 1
    if passed:
        results['passed'] += 1
        print(f"✓ PASS - {requirement}: {name}")
    else:
        results['failed'] += 1
        print(f"✗ FAIL - {requirement}: {name}")
    print(f"  {details}\n")
    results['tests'].append({
        'requirement': requirement,
        'name': name,
        'passed': passed,
        'details': details
    })

def wait_for_scan(driver, timeout=3):
    """Wait for scan to complete"""
    time.sleep(timeout)

def main():
    print("=" * 70)
    print("TASK 4: SCAN HISTORY FUNCTIONALITY VERIFICATION")
    print("Testing Requirements 6.1-6.8")
    print("=" * 70)
    print()

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8084/phishing_detection_dashboard.html')
        time.sleep(1)  # Wait for page load

        # ===== TEST 1: Req 6.1, 6.2 - Scan results added to history =====
        print("TEST 1: Verifying scan results are added to history...")
        
        initial_history_length = driver.execute_script("return window.history.length;")
        
        # Perform a scan
        url_input = driver.find_element(By.ID, 'url-input')
        url_input.send_keys('https://github.com/test-repo')
        
        scan_btn = driver.find_element(By.ID, 'scan-btn')
        scan_btn.click()
        
        wait_for_scan(driver)
        
        history_data = driver.execute_script("""
            return {
                length: window.history.length,
                latest: window.history[0]
            };
        """)
        
        if history_data['length'] > initial_history_length and history_data['latest']:
            entry = history_data['latest']
            has_required_fields = (
                'url' in entry and 
                'verdict' in entry and 
                'score' in entry and 
                'time' in entry
            )
            
            if has_required_fields:
                log_test('Req 6.1, 6.2', 'Scan results added to history with correct data', True,
                    f"History entry added: URL=\"{entry['url']}\", Verdict=\"{entry['verdict']}\", Score={entry['score']}, Time=\"{entry['time']}\"")
            else:
                log_test('Req 6.1, 6.2', 'Scan results added to history with correct data', False,
                    "Missing required fields in history entry")
        else:
            log_test('Req 6.1, 6.2', 'Scan results added to history with correct data', False,
                f"History not updated after scan. Initial: {initial_history_length}, After: {history_data['length']}")

        # ===== TEST 2: Req 6.3 - Reverse chronological order =====
        print("TEST 2: Verifying history displays in reverse chronological order...")
        
        test_urls = [
            'https://test-url-1.com',
            'https://test-url-2.com',
            'https://test-url-3.com'
        ]
        
        for url in test_urls:
            driver.execute_script("document.getElementById('url-input').value = '';")
            url_input = driver.find_element(By.ID, 'url-input')
            url_input.send_keys(url)
            scan_btn = driver.find_element(By.ID, 'scan-btn')
            scan_btn.click()
            wait_for_scan(driver)
        
        history_order = driver.execute_script("""
            return window.history.slice(0, 3).map(h => h.url);
        """)
        
        is_newest_first = history_order[0] == 'https://test-url-3.com'
        
        if is_newest_first:
            log_test('Req 6.3', 'History displays in reverse chronological order', True,
                f"Newest entry first. Order: {' → '.join(history_order)}")
        else:
            log_test('Req 6.3', 'History displays in reverse chronological order', False,
                f"Incorrect order. Expected newest first, got: {' → '.join(history_order)}")

        # ===== TEST 3: Req 6.4, 6.5 - Filter buttons work correctly =====
        print("TEST 3: Verifying filter buttons work correctly...")
        
        # Switch to History tab
        driver.execute_script("""
            const historyBtn = Array.from(document.querySelectorAll('.nav-btn'))
                .find(btn => btn.textContent.includes('History'));
            historyBtn.click();
        """)
        time.sleep(0.3)
        
        # Test Safe filter
        driver.execute_script("""
            const safeBtn = Array.from(document.querySelectorAll('.filter-btn'))
                .find(btn => btn.textContent === 'Safe');
            safeBtn.click();
        """)
        time.sleep(0.3)
        
        safe_filter_results = driver.execute_script("""
            const items = Array.from(document.querySelectorAll('.hist-item'));
            return items.map(item => {
                const verdict = item.querySelector('.hist-verdict');
                return verdict ? verdict.textContent : '';
            });
        """)
        
        all_safe = len(safe_filter_results) == 0 or all(v == 'safe' for v in safe_filter_results)
        
        # Test Suspicious filter
        driver.execute_script("""
            const suspBtn = Array.from(document.querySelectorAll('.filter-btn'))
                .find(btn => btn.textContent === 'Suspicious');
            suspBtn.click();
        """)
        time.sleep(0.3)
        
        susp_filter_results = driver.execute_script("""
            const items = Array.from(document.querySelectorAll('.hist-item'));
            return items.map(item => {
                const verdict = item.querySelector('.hist-verdict');
                return verdict ? verdict.textContent : '';
            });
        """)
        
        all_susp = len(susp_filter_results) == 0 or all(v == 'suspicious' for v in susp_filter_results)
        
        # Test Phishing filter
        driver.execute_script("""
            const phishBtn = Array.from(document.querySelectorAll('.filter-btn'))
                .find(btn => btn.textContent === 'Phishing');
            phishBtn.click();
        """)
        time.sleep(0.3)
        
        phish_filter_results = driver.execute_script("""
            const items = Array.from(document.querySelectorAll('.hist-item'));
            return items.map(item => {
                const verdict = item.querySelector('.hist-verdict');
                return verdict ? verdict.textContent : '';
            });
        """)
        
        all_phish = len(phish_filter_results) == 0 or all(v == 'phishing' for v in phish_filter_results)
        
        if all_safe and all_susp and all_phish:
            log_test('Req 6.4, 6.5', 'Filter buttons correctly filter history', True,
                f"All filters working correctly. Safe: {len(safe_filter_results)} items, Suspicious: {len(susp_filter_results)} items, Phishing: {len(phish_filter_results)} items")
        else:
            log_test('Req 6.4, 6.5', 'Filter buttons correctly filter history', False,
                f"Filters not working correctly. Safe OK: {all_safe}, Suspicious OK: {all_susp}, Phishing OK: {all_phish}")

        # ===== TEST 4: Req 6.6 - Clicking history item loads URL and switches tabs =====
        print("TEST 4: Verifying clicking history item loads URL and switches tabs...")
        
        # Make sure we're on History tab with All filter
        driver.execute_script("""
            const allBtn = Array.from(document.querySelectorAll('.filter-btn'))
                .find(btn => btn.textContent === 'All');
            allBtn.click();
        """)
        time.sleep(0.3)
        
        history_item_test = driver.execute_script("""
            const firstItem = document.querySelector('.hist-item');
            if (!firstItem) return { found: false };
            
            const urlEl = firstItem.querySelector('.hist-url');
            const expectedUrl = urlEl ? urlEl.textContent : '';
            
            // Click the item
            firstItem.click();
            
            // Check if Scanner tab is active
            const scannerPanel = document.getElementById('panel-scanner');
            const isScannerActive = scannerPanel && scannerPanel.classList.contains('active');
            
            // Check if URL was loaded
            const urlInput = document.getElementById('url-input');
            const loadedUrl = urlInput ? urlInput.value : '';
            
            return {
                found: true,
                expectedUrl: expectedUrl,
                loadedUrl: loadedUrl,
                isScannerActive: isScannerActive
            };
        """)
        
        if (history_item_test['found'] and history_item_test['isScannerActive'] and 
            history_item_test['loadedUrl'] == history_item_test['expectedUrl']):
            log_test('Req 6.6', 'Clicking history item loads URL and switches tabs', True,
                f"Successfully loaded \"{history_item_test['loadedUrl']}\" and switched to Scanner tab")
        elif not history_item_test['found']:
            log_test('Req 6.6', 'Clicking history item loads URL and switches tabs', False,
                'No history items found to test')
        else:
            log_test('Req 6.6', 'Clicking history item loads URL and switches tabs', False,
                f"Scanner active: {history_item_test['isScannerActive']}, URL match: {history_item_test['loadedUrl'] == history_item_test['expectedUrl']}")

        # ===== TEST 5: Req 6.7 - Clear All button removes all entries =====
        print("TEST 5: Verifying Clear All button removes all entries...")
        
        # Switch back to History tab
        driver.execute_script("""
            const historyBtn = Array.from(document.querySelectorAll('.nav-btn'))
                .find(btn => btn.textContent.includes('History'));
            historyBtn.click();
        """)
        time.sleep(0.3)
        
        before_clear = driver.execute_script("return window.history.length;")
        
        if before_clear == 0:
            log_test('Req 6.7', 'Clear All button removes all entries', False,
                'No history entries to clear')
        else:
            # Click Clear All
            driver.execute_script("""
                const clearBtn = Array.from(document.querySelectorAll('.btn-sm'))
                    .find(btn => btn.textContent.toLowerCase().includes('clear'));
                if (clearBtn) clearBtn.click();
            """)
            time.sleep(0.3)
            
            after_clear = driver.execute_script("""
                return {
                    length: window.history.length,
                    hasEmptyState: !!document.querySelector('.empty-state')
                };
            """)
            
            if after_clear['length'] == 0 and after_clear['hasEmptyState']:
                log_test('Req 6.7', 'Clear All button removes all entries', True,
                    f"Successfully cleared {before_clear} entries and displayed empty state")
            else:
                log_test('Req 6.7', 'Clear All button removes all entries', False,
                    f"Before: {before_clear}, After: {after_clear['length']}, Empty state: {after_clear['hasEmptyState']}")

        # ===== TEST 6: Req 6.8 - Empty state displays when no matches =====
        print("TEST 6: Verifying empty state displays when no matches...")
        
        # Test with empty history
        empty_history_test = driver.execute_script("""
            window.history = [];
            window.renderHistory();
            return !!document.querySelector('.empty-state');
        """)
        
        # Add only safe entries
        driver.execute_script("""
            window.history = [
                { url: 'https://safe1.com', verdict: 'safe', score: 10, time: 'Now' },
                { url: 'https://safe2.com', verdict: 'safe', score: 15, time: 'Now' }
            ];
        """)
        
        # Filter by phishing (should show empty state)
        driver.execute_script("""
            const phishBtn = Array.from(document.querySelectorAll('.filter-btn'))
                .find(btn => btn.textContent === 'Phishing');
            if (phishBtn) phishBtn.click();
        """)
        time.sleep(0.3)
        
        empty_filter_test = driver.execute_script("""
            return !!document.querySelector('.empty-state');
        """)
        
        if empty_history_test and empty_filter_test:
            log_test('Req 6.8', 'Empty state displays when no matches', True,
                'Empty state correctly displayed for empty history and filtered results with no matches')
        else:
            log_test('Req 6.8', 'Empty state displays when no matches', False,
                f"Empty history: {empty_history_test}, Empty filter: {empty_filter_test}")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    if results['total'] > 0:
        print(f"Success Rate: {(results['passed'] / results['total'] * 100):.1f}%")
    print("=" * 70)

    if results['failed'] > 0:
        print("\nFailed Tests:")
        for test in results['tests']:
            if not test['passed']:
                print(f"  - {test['requirement']}: {test['name']}")
                print(f"    {test['details']}")

    return 0 if results['failed'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
