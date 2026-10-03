# Task 4: Manual Verification Checklist

## Scan History Functionality Testing

Use this checklist to manually verify all scan history requirements in the Phishing Detection Dashboard.

---

## Setup

1. Open `phishing_detection_dashboard.html` in a web browser
2. Ensure you're on the Scanner tab
3. Have the browser console open (F12) to inspect state if needed

---

## Test 1: Scan Results Added to History (Req 6.1, 6.2)

**Objective:** Verify that completed scans are added to history with all required data

### Steps:
1. ☐ Enter a URL in the scanner input: `https://github.com/test-repo`
2. ☐ Click "Analyze URL" button
3. ☐ Wait for scan to complete (~2 seconds)
4. ☐ Click on the "History" tab

### Expected Results:
- ☐ A new history entry appears in the list
- ☐ Entry shows the URL: `https://github.com/test-repo`
- ☐ Entry shows a verdict badge (Safe/Suspicious/Phishing)
- ☐ Entry shows a risk score (0-100)
- ☐ Entry shows a timestamp ("Just now")

### Verification in Console:
```javascript
// Check history array
console.log(window.history[0]);
// Should show: {url: "...", verdict: "...", score: ..., time: "..."}
```

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Test 2: Reverse Chronological Order (Req 6.3)

**Objective:** Verify that newest scans appear first in the history list

### Steps:
1. ☐ Go to Scanner tab
2. ☐ Scan URL 1: `https://test-1.com`
3. ☐ Wait for completion
4. ☐ Scan URL 2: `https://test-2.com`
5. ☐ Wait for completion
6. ☐ Scan URL 3: `https://test-3.com`
7. ☐ Wait for completion
8. ☐ Go to History tab

### Expected Results:
- ☐ First item in list is `https://test-3.com` (most recent)
- ☐ Second item is `https://test-2.com`
- ☐ Third item is `https://test-1.com`
- ☐ Order is newest → oldest (top to bottom)

### Verification in Console:
```javascript
// Check order
window.history.slice(0, 3).map(h => h.url);
// Should show: ["https://test-3.com", "https://test-2.com", "https://test-1.com"]
```

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Test 3: Filter Buttons (Req 6.4, 6.5)

**Objective:** Verify that filter buttons correctly filter history by verdict

### Setup:
Ensure you have a mix of verdicts in history:
- ☐ Scan `https://github.com` (should be Safe)
- ☐ Scan `http://paypa1-verify.net/account/confirm` (should be Suspicious)
- ☐ Scan `http://secure-bank-login.xyz/wellsfargo/signin/verify` (should be Phishing)

### Test 3a: All Filter
1. ☐ Go to History tab
2. ☐ Click "All" filter button

**Expected:**
- ☐ All history entries are visible
- ☐ "All" button is highlighted/active

### Test 3b: Safe Filter
1. ☐ Click "Safe" filter button

**Expected:**
- ☐ Only entries with "safe" verdict badge are shown
- ☐ No suspicious or phishing entries visible
- ☐ "Safe" button is highlighted/active

### Test 3c: Suspicious Filter
1. ☐ Click "Suspicious" filter button

**Expected:**
- ☐ Only entries with "suspicious" verdict badge are shown
- ☐ No safe or phishing entries visible
- ☐ "Suspicious" button is highlighted/active

### Test 3d: Phishing Filter
1. ☐ Click "Phishing" filter button

**Expected:**
- ☐ Only entries with "phishing" verdict badge are shown
- ☐ No safe or suspicious entries visible
- ☐ "Phishing" button is highlighted/active

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Test 4: Click History Item (Req 6.6)

**Objective:** Verify that clicking a history item loads the URL and switches to Scanner tab

### Steps:
1. ☐ Go to History tab
2. ☐ Note the URL of the first history item (e.g., `https://example.com`)
3. ☐ Click on that history item

### Expected Results:
- ☐ Automatically switches to Scanner tab
- ☐ Scanner tab is now active/highlighted
- ☐ URL input field contains the clicked URL
- ☐ URL matches exactly what was in the history item

### Verification:
```javascript
// Check URL input value
document.getElementById('url-input').value;
// Should match the clicked history item URL
```

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Test 5: Clear All Button (Req 6.7)

**Objective:** Verify that Clear All button removes all history entries

### Steps:
1. ☐ Go to History tab
2. ☐ Note the number of history entries currently visible
3. ☐ Click the "Clear all" button (top right of History panel)

### Expected Results:
- ☐ All history entries are removed
- ☐ Empty state message appears: "🔍 No scans found"
- ☐ No history items visible

### Verification in Console:
```javascript
// Check history array
window.history.length;
// Should be: 0
```

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Test 6: Empty State Display (Req 6.8)

**Objective:** Verify that empty state displays when no history matches the filter

### Test 6a: Empty History
1. ☐ Clear all history (if not already empty)
2. ☐ Go to History tab

**Expected:**
- ☐ Empty state message displayed: "🔍 No scans found"
- ☐ No history items visible

### Test 6b: Filter with No Matches
1. ☐ Scan only safe URLs (e.g., `https://github.com`, `https://google.com`)
2. ☐ Go to History tab
3. ☐ Click "Phishing" filter button

**Expected:**
- ☐ Empty state message displayed: "🔍 No scans found"
- ☐ No history items visible (because no phishing entries exist)

4. ☐ Click "All" filter button

**Expected:**
- ☐ Safe entries reappear
- ☐ Empty state is hidden

**Status:** ☐ PASS ☐ FAIL

**Notes:**

---

## Integration Tests

### Integration Test 1: History Persists Across Tab Switches

1. ☐ Perform a scan on Scanner tab
2. ☐ Switch to Analytics tab
3. ☐ Switch to Alerts tab
4. ☐ Switch back to History tab

**Expected:**
- ☐ History entries are still present
- ☐ No data loss occurred

**Status:** ☐ PASS ☐ FAIL

---

### Integration Test 2: Multiple Scans Build History

1. ☐ Perform 5 different scans
2. ☐ Go to History tab

**Expected:**
- ☐ All 5 scans appear in history
- ☐ Newest scan is at the top
- ☐ All entries have complete data

**Status:** ☐ PASS ☐ FAIL

---

### Integration Test 3: Filter State Persists

1. ☐ Go to History tab
2. ☐ Select "Safe" filter
3. ☐ Switch to Scanner tab
4. ☐ Switch back to History tab

**Expected:**
- ☐ "Safe" filter is still active
- ☐ Only safe entries are shown

**Status:** ☐ PASS ☐ FAIL

---

## Summary

### Test Results

| Test | Requirement | Status |
|------|-------------|--------|
| Test 1 | Req 6.1, 6.2 | ☐ PASS ☐ FAIL |
| Test 2 | Req 6.3 | ☐ PASS ☐ FAIL |
| Test 3 | Req 6.4, 6.5 | ☐ PASS ☐ FAIL |
| Test 4 | Req 6.6 | ☐ PASS ☐ FAIL |
| Test 5 | Req 6.7 | ☐ PASS ☐ FAIL |
| Test 6 | Req 6.8 | ☐ PASS ☐ FAIL |

### Overall Status

- **Total Tests:** 6
- **Passed:** ___
- **Failed:** ___
- **Success Rate:** ___%

### Issues Found

(List any issues or unexpected behavior discovered during testing)

---

### Tester Information

- **Tester Name:** _______________
- **Date:** _______________
- **Browser:** _______________
- **Browser Version:** _______________

---

## Quick Reference: Console Commands

```javascript
// View entire history array
window.history

// View most recent entry
window.history[0]

// Count history entries
window.history.length

// View current filter state
window.filterState

// Manually trigger history render
window.renderHistory()

// Clear history programmatically
window.clearHistory()

// Add test entry
window.history.unshift({
  url: 'https://test.com',
  verdict: 'safe',
  score: 10,
  time: 'Test'
})
window.renderHistory()
```

---

## Notes

- All tests should be performed in a fresh browser session for consistency
- If a test fails, note the specific behavior observed
- Check browser console for any JavaScript errors
- Take screenshots of failures for documentation

````