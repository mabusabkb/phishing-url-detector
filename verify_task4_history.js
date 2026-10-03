/**
 * Task 4 Verification: Scan History Functionality
 * Tests Requirements 6.1-6.8
 */

const puppeteer = require('puppeteer');

// Test results tracking
const results = {
  total: 0,
  passed: 0,
  failed: 0,
  tests: []
};

function logTest(requirement, name, passed, details) {
  results.total++;
  if (passed) {
    results.passed++;
    console.log(`✓ PASS - ${requirement}: ${name}`);
  } else {
    results.failed++;
    console.log(`✗ FAIL - ${requirement}: ${name}`);
  }
  console.log(`  ${details}\n`);
  results.tests.push({ requirement, name, passed, details });
}

async function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runTests() {
  console.log('='.repeat(70));
  console.log('TASK 4: SCAN HISTORY FUNCTIONALITY VERIFICATION');
  console.log('Testing Requirements 6.1-6.8');
  console.log('='.repeat(70));
  console.log('');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.goto('http://localhost:8084/phishing_detection_dashboard.html', {
      waitUntil: 'networkidle0'
    });

    // Wait for page to be fully loaded
    await wait(500);

    // ===== TEST 1: Req 6.1, 6.2 - Scan results added to history =====
    console.log('TEST 1: Verifying scan results are added to history...');
    
    const initialHistoryLength = await page.evaluate(() => window.history.length);
    
    // Perform a scan
    await page.type('#url-input', 'https://github.com/test-repo');
    await page.click('#scan-btn');
    
    // Wait for scan to complete
    await wait(2500);
    
    const historyAfterScan = await page.evaluate(() => {
      return {
        length: window.history.length,
        latest: window.history[0]
      };
    });
    
    if (historyAfterScan.length > initialHistoryLength && historyAfterScan.latest) {
      const entry = historyAfterScan.latest;
      const hasRequiredFields = 
        entry.url && 
        entry.verdict && 
        typeof entry.score === 'number' && 
        entry.time;
      
      if (hasRequiredFields) {
        logTest('Req 6.1, 6.2', 'Scan results added to history with correct data', true,
          `History entry added: URL="${entry.url}", Verdict="${entry.verdict}", Score=${entry.score}, Time="${entry.time}"`);
      } else {
        logTest('Req 6.1, 6.2', 'Scan results added to history with correct data', false,
          `Missing required fields in history entry`);
      }
    } else {
      logTest('Req 6.1, 6.2', 'Scan results added to history with correct data', false,
        `History not updated after scan. Initial: ${initialHistoryLength}, After: ${historyAfterScan.length}`);
    }

    // ===== TEST 2: Req 6.3 - Reverse chronological order =====
    console.log('TEST 2: Verifying history displays in reverse chronological order...');
    
    // Perform multiple scans
    const testUrls = [
      'https://test-url-1.com',
      'https://test-url-2.com',
      'https://test-url-3.com'
    ];
    
    for (const url of testUrls) {
      await page.evaluate(() => {
        document.getElementById('url-input').value = '';
      });
      await page.type('#url-input', url);
      await page.click('#scan-btn');
      await wait(2500);
    }
    
    const historyOrder = await page.evaluate(() => {
      return window.history.slice(0, 3).map(h => h.url);
    });
    
    const isNewestFirst = historyOrder[0] === 'https://test-url-3.com';
    
    if (isNewestFirst) {
      logTest('Req 6.3', 'History displays in reverse chronological order', true,
        `Newest entry first. Order: ${historyOrder.join(' → ')}`);
    } else {
      logTest('Req 6.3', 'History displays in reverse chronological order', false,
        `Incorrect order. Expected newest first, got: ${historyOrder.join(' → ')}`);
    }

    // ===== TEST 3: Req 6.4, 6.5 - Filter buttons work correctly =====
    console.log('TEST 3: Verifying filter buttons work correctly...');
    
    // Switch to History tab
    await page.evaluate(() => {
      const historyBtn = Array.from(document.querySelectorAll('.nav-btn'))
        .find(btn => btn.textContent.includes('History'));
      historyBtn.click();
    });
    await wait(200);
    
    // Test Safe filter
    await page.evaluate(() => {
      const safeBtn = Array.from(document.querySelectorAll('.filter-btn'))
        .find(btn => btn.textContent === 'Safe');
      safeBtn.click();
    });
    await wait(200);
    
    const safeFilterResults = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('.hist-item'));
      return items.map(item => {
        const verdict = item.querySelector('.hist-verdict');
        return verdict ? verdict.textContent : '';
      });
    });
    
    const allSafe = safeFilterResults.length === 0 || safeFilterResults.every(v => v === 'safe');
    
    // Test Suspicious filter
    await page.evaluate(() => {
      const suspBtn = Array.from(document.querySelectorAll('.filter-btn'))
        .find(btn => btn.textContent === 'Suspicious');
      suspBtn.click();
    });
    await wait(200);
    
    const suspFilterResults = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('.hist-item'));
      return items.map(item => {
        const verdict = item.querySelector('.hist-verdict');
        return verdict ? verdict.textContent : '';
      });
    });
    
    const allSusp = suspFilterResults.length === 0 || suspFilterResults.every(v => v === 'suspicious');
    
    // Test Phishing filter
    await page.evaluate(() => {
      const phishBtn = Array.from(document.querySelectorAll('.filter-btn'))
        .find(btn => btn.textContent === 'Phishing');
      phishBtn.click();
    });
    await wait(200);
    
    const phishFilterResults = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('.hist-item'));
      return items.map(item => {
        const verdict = item.querySelector('.hist-verdict');
        return verdict ? verdict.textContent : '';
      });
    });
    
    const allPhish = phishFilterResults.length === 0 || phishFilterResults.every(v => v === 'phishing');
    
    if (allSafe && allSusp && allPhish) {
      logTest('Req 6.4, 6.5', 'Filter buttons correctly filter history', true,
        `All filters working correctly. Safe: ${safeFilterResults.length} items, Suspicious: ${suspFilterResults.length} items, Phishing: ${phishFilterResults.length} items`);
    } else {
      logTest('Req 6.4, 6.5', 'Filter buttons correctly filter history', false,
        `Filters not working correctly. Safe OK: ${allSafe}, Suspicious OK: ${allSusp}, Phishing OK: ${allPhish}`);
    }

    // ===== TEST 4: Req 6.6 - Clicking history item loads URL and switches tabs =====
    console.log('TEST 4: Verifying clicking history item loads URL and switches tabs...');
    
    // Make sure we're on History tab and have items
    await page.evaluate(() => {
      const allBtn = Array.from(document.querySelectorAll('.filter-btn'))
        .find(btn => btn.textContent === 'All');
      allBtn.click();
    });
    await wait(200);
    
    const historyItemTest = await page.evaluate(() => {
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
        expectedUrl,
        loadedUrl,
        isScannerActive
      };
    });
    
    if (historyItemTest.found && historyItemTest.isScannerActive && 
        historyItemTest.loadedUrl === historyItemTest.expectedUrl) {
      logTest('Req 6.6', 'Clicking history item loads URL and switches tabs', true,
        `Successfully loaded "${historyItemTest.loadedUrl}" and switched to Scanner tab`);
    } else if (!historyItemTest.found) {
      logTest('Req 6.6', 'Clicking history item loads URL and switches tabs', false,
        'No history items found to test');
    } else {
      logTest('Req 6.6', 'Clicking history item loads URL and switches tabs', false,
        `Scanner active: ${historyItemTest.isScannerActive}, URL match: ${historyItemTest.loadedUrl === historyItemTest.expectedUrl}`);
    }

    // ===== TEST 5: Req 6.7 - Clear All button removes all entries =====
    console.log('TEST 5: Verifying Clear All button removes all entries...');
    
    // Switch back to History tab
    await page.evaluate(() => {
      const historyBtn = Array.from(document.querySelectorAll('.nav-btn'))
        .find(btn => btn.textContent.includes('History'));
      historyBtn.click();
    });
    await wait(200);
    
    const beforeClear = await page.evaluate(() => window.history.length);
    
    if (beforeClear === 0) {
      logTest('Req 6.7', 'Clear All button removes all entries', false,
        'No history entries to clear');
    } else {
      // Click Clear All
      await page.evaluate(() => {
        const clearBtn = Array.from(document.querySelectorAll('.btn-sm'))
          .find(btn => btn.textContent.toLowerCase().includes('clear'));
        if (clearBtn) clearBtn.click();
      });
      await wait(200);
      
      const afterClear = await page.evaluate(() => {
        return {
          length: window.history.length,
          hasEmptyState: !!document.querySelector('.empty-state')
        };
      });
      
      if (afterClear.length === 0 && afterClear.hasEmptyState) {
        logTest('Req 6.7', 'Clear All button removes all entries', true,
          `Successfully cleared ${beforeClear} entries and displayed empty state`);
      } else {
        logTest('Req 6.7', 'Clear All button removes all entries', false,
          `Before: ${beforeClear}, After: ${afterClear.length}, Empty state: ${afterClear.hasEmptyState}`);
      }
    }

    // ===== TEST 6: Req 6.8 - Empty state displays when no matches =====
    console.log('TEST 6: Verifying empty state displays when no matches...');
    
    // Test with empty history
    const emptyHistoryTest = await page.evaluate(() => {
      window.history = [];
      window.renderHistory();
      return !!document.querySelector('.empty-state');
    });
    
    // Add only safe entries
    await page.evaluate(() => {
      window.history = [
        { url: 'https://safe1.com', verdict: 'safe', score: 10, time: 'Now' },
        { url: 'https://safe2.com', verdict: 'safe', score: 15, time: 'Now' }
      ];
    });
    
    // Filter by phishing (should show empty state)
    await page.evaluate(() => {
      const phishBtn = Array.from(document.querySelectorAll('.filter-btn'))
        .find(btn => btn.textContent === 'Phishing');
      if (phishBtn) phishBtn.click();
    });
    await wait(200);
    
    const emptyFilterTest = await page.evaluate(() => {
      return !!document.querySelector('.empty-state');
    });
    
    if (emptyHistoryTest && emptyFilterTest) {
      logTest('Req 6.8', 'Empty state displays when no matches', true,
        'Empty state correctly displayed for empty history and filtered results with no matches');
    } else {
      logTest('Req 6.8', 'Empty state displays when no matches', false,
        `Empty history: ${emptyHistoryTest}, Empty filter: ${emptyFilterTest}`);
    }

  } catch (error) {
    console.error('Error during testing:', error);
  } finally {
    await browser.close();
  }

  // Print summary
  console.log('='.repeat(70));
  console.log('TEST SUMMARY');
  console.log('='.repeat(70));
  console.log(`Total Tests: ${results.total}`);
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Success Rate: ${((results.passed / results.total) * 100).toFixed(1)}%`);
  console.log('='.repeat(70));

  if (results.failed > 0) {
    console.log('\nFailed Tests:');
    results.tests.filter(t => !t.passed).forEach(t => {
      console.log(`  - ${t.requirement}: ${t.name}`);
      console.log(`    ${t.details}`);
    });
  }

  process.exit(results.failed > 0 ? 1 : 0);
}

runTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
