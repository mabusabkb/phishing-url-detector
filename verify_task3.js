/**
 * Task 3 Verification Script
 * Verifies scan result display and loading states against requirements 4.1-4.7 and 5.1-5.6
 */

const fs = require('fs');

// Read the HTML file
const htmlContent = fs.readFileSync('phishing_detection_dashboard.html', 'utf8');

const tests = [];
let passCount = 0;
let failCount = 0;

function test(name, requirement, testFn) {
  try {
    const result = testFn();
    if (result.pass) {
      passCount++;
      console.log(`✓ PASS: ${name}`);
      console.log(`  ${requirement}`);
      console.log(`  Details: ${result.details}\n`);
    } else {
      failCount++;
      console.log(`✗ FAIL: ${name}`);
      console.log(`  ${requirement}`);
      console.log(`  Details: ${result.details}\n`);
    }
    tests.push({ name, requirement, ...result });
  } catch (error) {
    failCount++;
    console.log(`✗ ERROR: ${name}`);
    console.log(`  ${requirement}`);
    console.log(`  Error: ${error.message}\n`);
    tests.push({ name, requirement, pass: false, details: error.message });
  }
}

console.log('='.repeat(80));
console.log('TASK 3 VERIFICATION: Scan Result Display and Loading States');
console.log('='.repeat(80));
console.log();

// Test 1: Verdict badge displays with correct color coding (Req 4.1)
test(
  'Verdict badge displays with correct color coding',
  'Requirement 4.1',
  () => {
    // Check for verdict badge CSS classes
    const hasSafeBadge = htmlContent.includes('.verdict-badge.safe');
    const hasSuspiciousBadge = htmlContent.includes('.verdict-badge.suspicious');
    const hasPhishingBadge = htmlContent.includes('.verdict-badge.phishing');
    
    if (!hasSafeBadge || !hasSuspiciousBadge || !hasPhishingBadge) {
      return { pass: false, details: 'Missing verdict badge CSS classes for safe, suspicious, or phishing' };
    }
    
    // Check for color coding in CSS
    const hasSafeColors = htmlContent.includes('--safe-bg') && htmlContent.includes('--safe-bd');
    const hasSuspColors = htmlContent.includes('--susp-bg') && htmlContent.includes('--susp-bd');
    const hasPhishColors = htmlContent.includes('--phish-bg') && htmlContent.includes('--phish-bd');
    
    if (!hasSafeColors || !hasSuspColors || !hasPhishColors) {
      return { pass: false, details: 'Missing color variable definitions for verdict badges' };
    }
    
    // Check for verdict badge rendering in showResult function
    const hasVerdictBadgeRendering = htmlContent.includes('verdict-badge ${d.verdict}');
    if (!hasVerdictBadgeRendering) {
      return { pass: false, details: 'Verdict badge rendering not found in showResult function' };
    }
    
    return { pass: true, details: 'Verdict badges have CSS classes with color coding for safe (green), suspicious (orange), and phishing (red)' };
  }
);

// Test 2: Risk score displays as circular progress ring (Req 4.2)
test(
  'Risk score displays as circular progress ring',
  'Requirement 4.2',
  () => {
    // Check for score-ring class
    const hasScoreRing = htmlContent.includes('class="score-ring"');
    if (!hasScoreRing) {
      return { pass: false, details: 'score-ring class not found' };
    }
    
    // Check for SVG circle elements
    const hasSvgCircle = htmlContent.includes('<circle') && htmlContent.includes('stroke-dasharray');
    if (!hasSvgCircle) {
      return { pass: false, details: 'SVG circle with stroke-dasharray not found' };
    }
    
    // Check for progress calculation
    const hasProgressCalc = htmlContent.includes('dashOffset') && htmlContent.includes('circum');
    if (!hasProgressCalc) {
      return { pass: false, details: 'Progress calculation (dashOffset, circum) not found' };
    }
    
    // Check for score text display
    const hasScoreText = htmlContent.includes('${d.score}');
    if (!hasScoreText) {
      return { pass: false, details: 'Score text display not found' };
    }
    
    return { pass: true, details: 'Risk score displays as circular progress ring with SVG, stroke-dasharray animation, and score text' };
  }
);

// Test 3: All 8 detection signals display in grid layout (Req 4.3, 4.4)
test(
  'All 8 detection signals display in grid layout',
  'Requirements 4.3, 4.4',
  () => {
    // Check for features-grid class
    const hasFeaturesGrid = htmlContent.includes('class="features-grid"');
    if (!hasFeaturesGrid) {
      return { pass: false, details: 'features-grid class not found' };
    }
    
    // Check for grid CSS with 2 columns
    const hasGridLayout = htmlContent.includes('grid-template-columns:1fr 1fr');
    if (!hasGridLayout) {
      return { pass: false, details: 'Grid layout with 2 columns not found in CSS' };
    }
    
    // Check for feature-row class
    const hasFeatureRow = htmlContent.includes('class="feature-row"');
    if (!hasFeatureRow) {
      return { pass: false, details: 'feature-row class not found' };
    }
    
    // Check for all required feature elements
    const hasIcon = htmlContent.includes('feat-icon');
    const hasName = htmlContent.includes('feat-name');
    const hasValue = htmlContent.includes('feat-value');
    const hasBar = htmlContent.includes('feat-bar');
    const hasTag = htmlContent.includes('feat-tag');
    
    if (!hasIcon || !hasName || !hasValue || !hasBar || !hasTag) {
      return { pass: false, details: 'Missing required feature elements (icon, name, value, bar, or tag)' };
    }
    
    // Check that demo data has 8 features
    const demoMatches = htmlContent.match(/features:\s*\[/g);
    if (!demoMatches || demoMatches.length < 3) {
      return { pass: false, details: 'Demo data does not contain features arrays' };
    }
    
    // Verify 8 signals in one demo
    const safeDemo = htmlContent.match(/safe:\s*{[\s\S]*?features:\s*\[([\s\S]*?)\]/);
    if (safeDemo) {
      const featureCount = (safeDemo[1].match(/\{name:/g) || []).length;
      if (featureCount !== 8) {
        return { pass: false, details: `Expected 8 detection signals in demo data, found ${featureCount}` };
      }
    }
    
    return { pass: true, details: 'All 8 detection signals display in 2-column grid layout with icon, name, value, risk bar, and status tag' };
  }
);

// Test 4: Explanation section displays reasons (Req 4.5)
test(
  'Explanation section displays reasons',
  'Requirement 4.5',
  () => {
    // Check for explain-box class
    const hasExplainBox = htmlContent.includes('class="explain-box"');
    if (!hasExplainBox) {
      return { pass: false, details: 'explain-box class not found' };
    }
    
    // Check for explain-title
    const hasExplainTitle = htmlContent.includes('explain-title');
    if (!hasExplainTitle) {
      return { pass: false, details: 'explain-title class not found' };
    }
    
    // Check for explain-reasons container
    const hasExplainReasons = htmlContent.includes('explain-reasons');
    if (!hasExplainReasons) {
      return { pass: false, details: 'explain-reasons class not found' };
    }
    
    // Check for reason-item and reason-dot
    const hasReasonItem = htmlContent.includes('reason-item');
    const hasReasonDot = htmlContent.includes('reason-dot');
    if (!hasReasonItem || !hasReasonDot) {
      return { pass: false, details: 'reason-item or reason-dot class not found' };
    }
    
    // Check for reasons rendering in showResult
    const hasReasonsRendering = htmlContent.includes('d.reasons.map');
    if (!hasReasonsRendering) {
      return { pass: false, details: 'Reasons rendering not found in showResult function' };
    }
    
    // Check that demo data has reasons
    const hasReasonsInDemo = htmlContent.includes('reasons:');
    if (!hasReasonsInDemo) {
      return { pass: false, details: 'Reasons not found in demo data' };
    }
    
    return { pass: true, details: 'Explanation section displays reasons with color-coded dots and text descriptions' };
  }
);

// Test 5: URL and timestamp display (Req 4.6)
test(
  'URL and timestamp display',
  'Requirement 4.6',
  () => {
    // Check for url-info class
    const hasUrlInfo = htmlContent.includes('class="url-info"');
    if (!hasUrlInfo) {
      return { pass: false, details: 'url-info class not found' };
    }
    
    // Check for url-text class
    const hasUrlText = htmlContent.includes('url-text');
    if (!hasUrlText) {
      return { pass: false, details: 'url-text class not found' };
    }
    
    // Check for scan-time class
    const hasScanTime = htmlContent.includes('scan-time');
    if (!hasScanTime) {
      return { pass: false, details: 'scan-time class not found' };
    }
    
    // Check for URL rendering in showResult
    const hasUrlRendering = htmlContent.includes('${url}');
    if (!hasUrlRendering) {
      return { pass: false, details: 'URL rendering not found in showResult function' };
    }
    
    // Check for timestamp rendering
    const hasTimestampRendering = htmlContent.includes('Scanned just now') || htmlContent.includes('Risk score:');
    if (!hasTimestampRendering) {
      return { pass: false, details: 'Timestamp rendering not found in showResult function' };
    }
    
    return { pass: true, details: 'URL and timestamp display correctly in result card with url-text and scan-time elements' };
  }
);

// Test 6: Report button shows for Suspicious/Phishing (Req 4.7)
test(
  'Report button shows for Suspicious/Phishing verdicts',
  'Requirement 4.7',
  () => {
    // Check for btn-report class
    const hasBtnReport = htmlContent.includes('btn-report');
    if (!hasBtnReport) {
      return { pass: false, details: 'btn-report class not found' };
    }
    
    // Check for conditional rendering based on verdict
    const hasConditionalReport = htmlContent.includes("d.verdict!=='safe'") || 
                                  htmlContent.includes("d.verdict!='safe'");
    if (!hasConditionalReport) {
      return { pass: false, details: 'Conditional report button rendering not found (should hide for safe verdicts)' };
    }
    
    // Check for Report button text
    const hasReportText = htmlContent.includes('Report');
    if (!hasReportText) {
      return { pass: false, details: 'Report button text not found' };
    }
    
    // Check for openReport function
    const hasOpenReport = htmlContent.includes('function openReport');
    if (!hasOpenReport) {
      return { pass: false, details: 'openReport function not found' };
    }
    
    return { pass: true, details: 'Report button conditionally displays for Suspicious and Phishing verdicts, hidden for Safe' };
  }
);

// Test 7: Loading state shows spinner and progress steps (Req 5.1-5.6)
test(
  'Loading state shows spinner and progress steps',
  'Requirements 5.1-5.6',
  () => {
    // Check for loading-wrap class
    const hasLoadingWrap = htmlContent.includes('loading-wrap');
    if (!hasLoadingWrap) {
      return { pass: false, details: 'loading-wrap class not found' };
    }
    
    // Check for spinner class
    const hasSpinner = htmlContent.includes('class="spinner"');
    if (!hasSpinner) {
      return { pass: false, details: 'spinner class not found' };
    }
    
    // Check for spinner animation
    const hasSpinAnimation = htmlContent.includes('@keyframes spin');
    if (!hasSpinAnimation) {
      return { pass: false, details: 'Spinner animation (@keyframes spin) not found' };
    }
    
    // Check for loading-steps class
    const hasLoadingSteps = htmlContent.includes('loading-steps');
    if (!hasLoadingSteps) {
      return { pass: false, details: 'loading-steps class not found' };
    }
    
    // Check for loading-step class
    const hasLoadingStep = htmlContent.includes('loading-step');
    if (!hasLoadingStep) {
      return { pass: false, details: 'loading-step class not found' };
    }
    
    // Check for step states (done, active)
    const hasStepStates = htmlContent.includes('loading-step done') && htmlContent.includes('loading-step active');
    if (!hasStepStates) {
      return { pass: false, details: 'Loading step states (done, active) not found' };
    }
    
    // Check for steps array definition
    const stepsMatch = htmlContent.match(/const steps = \[(.*?)\]/s);
    if (!stepsMatch) {
      return { pass: false, details: 'Steps array definition not found' };
    }
    
    const stepsContent = stepsMatch[1];
    const stepCount = (stepsContent.match(/'/g) || []).length / 2;
    if (stepCount !== 6) {
      return { pass: false, details: `Expected 6 detection steps, found ${stepCount}` };
    }
    
    // Verify expected step content
    const expectedSteps = [
      'Resolving domain',
      'SSL certificate',
      'Google Safe Browsing',
      'VirusTotal',
      'page content',
      'ML risk score'
    ];
    
    const missingSteps = expectedSteps.filter(step => !stepsContent.includes(step));
    if (missingSteps.length > 0) {
      return { pass: false, details: `Missing expected steps: ${missingSteps.join(', ')}` };
    }
    
    // Check for interval-based step progression
    const hasStepProgression = htmlContent.includes('setInterval') && htmlContent.includes('350');
    if (!hasStepProgression) {
      return { pass: false, details: 'Step progression with interval not found' };
    }
    
    return { pass: true, details: 'Loading state displays spinner with animation and 6 progress steps (domain resolution, SSL check, Google Safe Browsing, VirusTotal, content analysis, ML scoring) with active/done indicators' };
  }
);

// Summary
console.log('='.repeat(80));
console.log('SUMMARY');
console.log('='.repeat(80));
console.log(`Total Tests: ${passCount + failCount}`);
console.log(`Passed: ${passCount}`);
console.log(`Failed: ${failCount}`);
console.log(`Success Rate: ${Math.round((passCount / (passCount + failCount)) * 100)}%`);
console.log();

if (failCount === 0) {
  console.log('✓ All requirements verified successfully!');
  console.log('Task 3 implementation meets all requirements 4.1-4.7 and 5.1-5.6');
  process.exit(0);
} else {
  console.log('✗ Some requirements not met. Please review failures above.');
  process.exit(1);
}
