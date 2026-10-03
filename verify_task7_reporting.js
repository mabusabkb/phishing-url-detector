/**
 * Task 7 Verification: URL Reporting Functionality
 * 
 * This script verifies that the URL reporting modal meets all requirements:
 * - Req 9.1: Report button opens modal dialog
 * - Req 9.2: Modal displays URL being reported
 * - Req 9.3: Dropdown menu has all report categories
 * - Req 9.4: Text area for additional details
 * - Req 9.5, 9.6, 9.7: Cancel and Submit Report buttons
 * - Req 9.8: Clicking overlay closes modal
 */

const fs = require('fs');
const { JSDOM } = require('jsdom');

// Load the HTML file
const html = fs.readFileSync('phishing_detection_dashboard.html', 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', resources: 'usable' });
const { document, window } = dom.window;

// Wait for scripts to load
setTimeout(() => {
  console.log('=== Task 7: URL Reporting Functionality Verification ===\n');

  let passCount = 0;
  let failCount = 0;

  function test(description, fn) {
    try {
      fn();
      console.log(`✓ ${description}`);
      passCount++;
    } catch (error) {
      console.log(`✗ ${description}`);
      console.log(`  Error: ${error.message}`);
      failCount++;
    }
  }

  // Test 9.1: Report button opens modal dialog
  test('Req 9.1: Report button opens modal dialog', () => {
    const modal = document.getElementById('report-modal');
    if (!modal) throw new Error('Modal element not found');
    
    // Initially modal should not have 'open' class
    if (modal.classList.contains('open')) {
      throw new Error('Modal should not be open initially');
    }
    
    // Call openReport function
    window.openReport('http://test-phishing.xyz');
    
    // Modal should now have 'open' class
    if (!modal.classList.contains('open')) {
      throw new Error('Modal should have "open" class after openReport() is called');
    }
    
    // Clean up
    window.closeReport();
  });

  // Test 9.2: Modal displays URL being reported
  test('Req 9.2: Modal displays URL being reported', () => {
    const testUrl = 'http://test-phishing-site.xyz/login';
    window.openReport(testUrl);
    
    const urlDisplay = document.getElementById('report-modal-url');
    if (!urlDisplay) throw new Error('URL display element not found');
    
    const displayedText = urlDisplay.textContent;
    
    // Check if URL is displayed (may be truncated if long)
    if (!displayedText.includes(testUrl) && !displayedText.includes(testUrl.substring(0, 60))) {
      throw new Error(`URL not displayed correctly. Expected: ${testUrl}, Got: ${displayedText}`);
    }
    
    window.closeReport();
  });

  // Test 9.3: Dropdown menu has all report categories
  test('Req 9.3: Dropdown menu has all report categories', () => {
    const dropdown = document.getElementById('report-type');
    if (!dropdown) throw new Error('Report type dropdown not found');
    
    const expectedCategories = [
      'Phishing / Credential harvesting',
      'Malware distribution',
      'Brand impersonation',
      'Spam / unwanted content',
      'Other threat'
    ];
    
    const options = Array.from(dropdown.options).map(opt => opt.textContent);
    
    expectedCategories.forEach(category => {
      if (!options.includes(category)) {
        throw new Error(`Missing category: ${category}`);
      }
    });
    
    if (options.length !== expectedCategories.length) {
      throw new Error(`Expected ${expectedCategories.length} categories, found ${options.length}`);
    }
  });

  // Test 9.4: Text area for additional details
  test('Req 9.4: Text area for additional details', () => {
    const textarea = document.getElementById('report-notes');
    if (!textarea) throw new Error('Report notes textarea not found');
    
    if (textarea.tagName.toLowerCase() !== 'textarea') {
      throw new Error('report-notes should be a textarea element');
    }
    
    const placeholder = textarea.getAttribute('placeholder');
    if (!placeholder || !placeholder.includes('optional')) {
      throw new Error('Textarea should have placeholder indicating optional details');
    }
  });

  // Test 9.5: Cancel button exists and is functional
  test('Req 9.5: Cancel button exists', () => {
    const modalActions = document.querySelector('.modal-actions');
    if (!modalActions) throw new Error('Modal actions container not found');
    
    const buttons = modalActions.querySelectorAll('button');
    const cancelButton = Array.from(buttons).find(btn => 
      btn.textContent.includes('Cancel')
    );
    
    if (!cancelButton) throw new Error('Cancel button not found');
    
    // Check if it has onclick handler
    const onclick = cancelButton.getAttribute('onclick');
    if (!onclick || !onclick.includes('closeReport')) {
      throw new Error('Cancel button should call closeReport()');
    }
  });

  // Test 9.6: Submit Report button exists
  test('Req 9.6: Submit Report button exists', () => {
    const modalActions = document.querySelector('.modal-actions');
    if (!modalActions) throw new Error('Modal actions container not found');
    
    const buttons = modalActions.querySelectorAll('button');
    const submitButton = Array.from(buttons).find(btn => 
      btn.textContent.includes('Submit Report')
    );
    
    if (!submitButton) throw new Error('Submit Report button not found');
    
    // Check if it has onclick handler
    const onclick = submitButton.getAttribute('onclick');
    if (!onclick || !onclick.includes('submitReport')) {
      throw new Error('Submit Report button should call submitReport()');
    }
  });

  // Test 9.7: Submit Report button closes modal and shows confirmation
  test('Req 9.7: Submit Report button closes modal and shows confirmation', () => {
    // First, run a scan to have a result
    const urlInput = document.getElementById('url-input');
    urlInput.value = 'http://test-phishing.xyz';
    window.startScan();
    
    // Wait for scan to complete (simulated)
    setTimeout(() => {
      window.openReport('http://test-phishing.xyz');
      
      const modal = document.getElementById('report-modal');
      if (!modal.classList.contains('open')) {
        throw new Error('Modal should be open before submit');
      }
      
      // Submit report
      window.submitReport();
      
      // Modal should be closed
      if (modal.classList.contains('open')) {
        throw new Error('Modal should be closed after submit');
      }
      
      // Check for success message in scanner result
      const scannerResult = document.getElementById('scanner-result');
      const resultHtml = scannerResult.innerHTML;
      
      if (!resultHtml.includes('Report submitted successfully') && 
          !resultHtml.includes('thank you')) {
        throw new Error('Success confirmation message not displayed');
      }
    }, 100);
  });

  // Test 9.8: Clicking overlay closes modal
  test('Req 9.8: Clicking overlay closes modal', () => {
    window.openReport('http://test.xyz');
    
    const modal = document.getElementById('report-modal');
    if (!modal.classList.contains('open')) {
      throw new Error('Modal should be open');
    }
    
    // Simulate click on overlay (the modal element itself, not its children)
    const clickEvent = new window.MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window
    });
    
    // Set target to the overlay itself
    Object.defineProperty(clickEvent, 'target', {
      value: modal,
      enumerable: true
    });
    
    modal.dispatchEvent(clickEvent);
    
    // Modal should be closed
    if (modal.classList.contains('open')) {
      throw new Error('Modal should close when overlay is clicked');
    }
  });

  // Additional test: Verify modal structure
  test('Additional: Modal has correct structure', () => {
    const modal = document.querySelector('.modal');
    if (!modal) throw new Error('Modal content container not found');
    
    const heading = modal.querySelector('h3');
    if (!heading || !heading.textContent.includes('Report')) {
      throw new Error('Modal should have heading with "Report"');
    }
    
    const subtitle = modal.querySelector('.modal-sub');
    if (!subtitle) throw new Error('Modal should have subtitle');
  });

  // Additional test: Verify Report button only shows for Suspicious/Phishing
  test('Additional: Report button only shows for Suspicious/Phishing verdicts', () => {
    // Test with safe URL
    const urlInput = document.getElementById('url-input');
    urlInput.value = 'https://github.com/anthropics/anthropic-sdk';
    window.startScan();
    
    setTimeout(() => {
      const scannerResult = document.getElementById('scanner-result');
      const reportButtons = scannerResult.querySelectorAll('.btn-report');
      
      if (reportButtons.length > 0) {
        throw new Error('Report button should not appear for Safe verdict');
      }
    }, 100);
  });

  // Summary
  setTimeout(() => {
    console.log('\n=== Verification Summary ===');
    console.log(`Total tests: ${passCount + failCount}`);
    console.log(`Passed: ${passCount}`);
    console.log(`Failed: ${failCount}`);
    
    if (failCount === 0) {
      console.log('\n✓ All URL reporting functionality requirements verified successfully!');
      process.exit(0);
    } else {
      console.log('\n✗ Some requirements failed verification.');
      process.exit(1);
    }
  }, 2000);

}, 1000);
