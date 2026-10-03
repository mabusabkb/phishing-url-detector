# Task 7: URL Reporting Functionality - Manual Verification Checklist

## Overview
This checklist verifies that the URL reporting modal meets all requirements from Requirement 9 (9.1-9.8).

## Test Environment
- **File**: `phishing_detection_dashboard.html`
- **Browser**: Open the file directly in a web browser
- **Test Date**: _____________

---

## Verification Steps

### ✓ Req 9.1: Report button opens modal dialog

**Steps:**
1. Open `phishing_detection_dashboard.html` in a browser
2. Click one of the quick test buttons (e.g., "paypa1-verify.net (suspicious)")
3. Wait for the scan to complete
4. Locate the "Report" button in the result card header

**Expected Result:**
- [ ] Report button is visible for Suspicious verdict
- [ ] Clicking the Report button opens a modal dialog overlay
- [ ] Modal appears centered on the screen with a semi-transparent background

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.2: Modal displays URL being reported

**Steps:**
1. With the modal open from the previous test
2. Look at the text below the "Report URL" heading

**Expected Result:**
- [ ] The URL being reported is displayed in the modal
- [ ] The URL matches the one that was scanned
- [ ] Long URLs are truncated appropriately (with "..." if > 60 chars)

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.3: Dropdown menu has all report categories

**Steps:**
1. With the modal open, locate the dropdown menu (select element)
2. Click on the dropdown to expand it
3. Review all available options

**Expected Result:**
- [ ] Dropdown contains exactly 5 categories:
  - [ ] "Phishing / Credential harvesting"
  - [ ] "Malware distribution"
  - [ ] "Brand impersonation"
  - [ ] "Spam / unwanted content"
  - [ ] "Other threat"

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.4: Text area for additional details

**Steps:**
1. With the modal open, locate the text area below the dropdown
2. Check the placeholder text
3. Try typing in the text area

**Expected Result:**
- [ ] Text area is present and functional
- [ ] Placeholder text indicates the field is optional (e.g., "Additional details (optional)...")
- [ ] Text area accepts user input
- [ ] Text area is resizable (vertically)

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.5: Cancel button exists and functions

**Steps:**
1. With the modal open, locate the "Cancel" button in the modal actions area
2. Click the Cancel button

**Expected Result:**
- [ ] Cancel button is visible in the modal actions area (bottom right)
- [ ] Cancel button has appropriate styling (btn-sm class)
- [ ] Clicking Cancel closes the modal without submitting
- [ ] No confirmation message appears after clicking Cancel

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.6: Submit Report button exists

**Steps:**
1. Open the modal again (click Report button on a scan result)
2. Locate the "Submit Report" button in the modal actions area

**Expected Result:**
- [ ] Submit Report button is visible in the modal actions area
- [ ] Button has danger styling (red color, btn-sm danger classes)
- [ ] Button text reads "Submit Report"

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.7: Submit Report closes modal and shows confirmation

**Steps:**
1. With the modal open, optionally select a category and add notes
2. Click the "Submit Report" button
3. Observe the modal and the scanner result area

**Expected Result:**
- [ ] Modal closes immediately after clicking Submit Report
- [ ] A success confirmation message appears in the scanner result area
- [ ] Message includes text like "Report submitted successfully" or "thank you"
- [ ] Message has green styling (safe-bg, safe-bd colors)
- [ ] Original scan result remains visible below the confirmation message

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### ✓ Req 9.8: Clicking overlay closes modal

**Steps:**
1. Open the modal again (click Report button)
2. Click on the dark semi-transparent area OUTSIDE the white modal box (the overlay)
3. Observe the modal behavior

**Expected Result:**
- [ ] Clicking the overlay (background) closes the modal
- [ ] Modal does NOT close when clicking inside the white modal box
- [ ] No report is submitted when closing via overlay click

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

## Additional Verification Tests

### Additional Test 1: Modal structure and styling

**Steps:**
1. Open the modal and inspect its visual appearance

**Expected Result:**
- [ ] Modal has a heading "Report URL"
- [ ] Modal has a subtitle mentioning "Google Safe Browsing & VirusTotal"
- [ ] Modal has rounded corners and proper spacing
- [ ] Modal is properly centered on the screen
- [ ] Overlay has semi-transparent dark background (rgba(0,0,0,.45))

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### Additional Test 2: Report button visibility based on verdict

**Steps:**
1. Test with a Safe URL (e.g., "github.com (safe)" quick test)
2. Wait for scan to complete
3. Look for the Report button in the result card

**Expected Result:**
- [ ] Report button does NOT appear for Safe verdict
- [ ] Report button DOES appear for Suspicious verdict
- [ ] Report button DOES appear for Phishing verdict

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

### Additional Test 3: Multiple report submissions

**Steps:**
1. Submit a report for one URL
2. Scan a different suspicious/phishing URL
3. Open the report modal for the new URL
4. Verify the URL displayed is the new one, not the previous one

**Expected Result:**
- [ ] Modal displays the correct URL for each report
- [ ] Previous report submissions don't interfere with new ones
- [ ] Each submission shows a new confirmation message

**Status:** ☐ Pass ☐ Fail

**Notes:** _________________________________________________________________

---

## Summary

**Total Requirements Tested:** 8 (Req 9.1 - 9.8)
**Additional Tests:** 3

**Passed:** _____ / 11
**Failed:** _____ / 11

**Overall Status:** ☐ All Pass ☐ Some Failures

---

## Issues Found

List any issues, bugs, or discrepancies discovered during testing:

1. _________________________________________________________________

2. _________________________________________________________________

3. _________________________________________________________________

---

## Recommendations

List any recommendations for improvements or fixes:

1. _________________________________________________________________

2. _________________________________________________________________

3. _________________________________________________________________

---

## Tester Information

**Tester Name:** _____________________________________________

**Date:** _____________________________________________

**Browser/Version:** _____________________________________________

**Screen Resolution:** _____________________________________________

---

## Code Verification

### Modal HTML Structure (from phishing_detection_dashboard.html)

```html
<!-- REPORT MODAL -->
<div class="modal-overlay" id="report-modal">
  <div class="modal">
    <h3>Report URL</h3>
    <div class="modal-sub" id="report-modal-url">Submitting to Google Safe Browsing & VirusTotal threat databases</div>
    <select id="report-type">
      <option>Phishing / Credential harvesting</option>
      <option>Malware distribution</option>
      <option>Brand impersonation</option>
      <option>Spam / unwanted content</option>
      <option>Other threat</option>
    </select>
    <textarea id="report-notes" placeholder="Additional details (optional)..."></textarea>
    <div class="modal-actions">
      <button class="btn-sm" onclick="closeReport()">Cancel</button>
      <button class="btn-sm danger" onclick="submitReport()">Submit Report</button>
    </div>
  </div>
</div>
```

### JavaScript Functions

```javascript
function openReport(url) {
  document.getElementById('report-modal-url').textContent = url.length>60?url.substring(0,60)+'...':url;
  document.getElementById('report-modal').classList.add('open');
}

function closeReport() { 
  document.getElementById('report-modal').classList.remove('open'); 
}

function submitReport() {
  closeReport();
  const old = document.getElementById('scanner-result').innerHTML;
  const notice = '<div style="padding:10px 14px;border-radius:var(--border-radius-md);background:var(--safe-bg);border:0.5px solid var(--safe-bd);color:var(--safe);font-size:13px;margin-bottom:12px">Report submitted successfully — thank you for helping protect the community.</div>';
  document.getElementById('scanner-result').innerHTML = notice + old;
}

// Event listener for clicking overlay
document.getElementById('report-modal').addEventListener('click', function(e){
  if(e.target===this) closeReport();
});
```

**Code Review Status:** ☐ Verified ☐ Issues Found

**Notes:** _________________________________________________________________


````