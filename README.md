# Explainable Real-Time Phishing Detection Dashboard

A single-page dashboard that scans URLs and explains *why* a URL is flagged safe, suspicious, or phishing — showing a risk score, the individual signals that contributed to it (domain/WHOIS checks, SSL, Safe Browsing, VirusTotal, brand-similarity, content analysis), scan history, analytics, and alerting.

## Running it

No build step — it's a static HTML file.

```bash
# from the project folder
python3 -m http.server 8080
# then open http://localhost:8080/phishing_detection_dashboard.html
```

Or just open `phishing_detection_dashboard.html` directly in a browser.

It loads [Chart.js](https://www.chartjs.org/) from a CDN for the analytics charts, so an internet connection is needed for that section; the rest of the app works fully offline.

## What's in here

- `phishing_detection_dashboard.html` — the app itself (scanner, history, analytics, alerts, settings).
- `test_*.html`, `*verify*.js`, `*verify*.py` — manual/automated verification harnesses used while building out each feature.
- `TASK_*`, `VERIFICATION_REPORT_*` — development notes and verification write-ups from building the project task by task.

## Notes

This is a demo/learning project: scan results are generated from built-in sample data and simple heuristics in the browser, not a live threat-intelligence backend. It's meant to illustrate *how* a phishing-detection UI can explain its verdicts, not to serve as a production security tool.
