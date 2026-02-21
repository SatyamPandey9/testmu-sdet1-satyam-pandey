# TestMu SDET-1 Assessment — Satyam Pandey

## Stack
- Python 3.14
- Playwright (pytest-playwright)
- pytest + pytest-html
- Anthropic Claude API (AI Failure Explainer)

## Project Structure
```
testmu-sdet1-satyam-pandey/
├── tests/
│   ├── login/test_login.py
│   ├── dashboard/test_dashboard.py
│   └── api/test_api.py
├── ai_integration/
│   └── failure_explainer.py
├── reports/
├── prompts.md
├── ai-usage-log.md
└── README.md
```

## Setup & Run

### 1. Install dependencies
```bash
pip install playwright pytest pytest-playwright pytest-html requests
playwright install
```

### 2. Set API Key (optional)
```bash
$env:ANTHROPIC_API_KEY="your-key-here"
```

### 3. Run all tests
```bash
pytest -v
```

## Test Coverage
| Module    | Tests | Status |
|-----------|-------|--------|
| Login     | 5     | ✅ Pass |
| Dashboard | 5     | ✅ Pass |
| API       | 7     | ✅ Pass |
| **Total** | **17**| **✅** |

## AI Integration — Task 3 (Option A: Failure Explainer)
When a test fails, the framework automatically:
1. Captures error message and page content
2. Sends it to Claude API
3. Gets plain English explanation with root cause and fix
4. Saves full report to reports/ai_failure_report.json

## What I'd Build Next
- CI/CD pipeline with GitHub Actions
- Screenshot capture on failure
- Slack notification with AI explanation
- More edge case coverage