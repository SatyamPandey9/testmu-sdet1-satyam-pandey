import os
import requests
import json

# Option A choose kiya kyunki yeh directly test failures ko explain karta hai
# aur developer ko turant actionable feedback deta hai bina logs manually padhne ke.
# Option B (Flaky Classifier) ke liye bahut saare test runs ka data chahiye hota.

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def explain_failure(test_name: str, error_message: str, page_content: str = "") -> str:
    """
    Test failure ko LLM ko bhejo aur plain English explanation lo.
    Real API call hai — agar credits nahi hain toh mock response return karta hai.
    """
    prompt = f"""You are a senior QA engineer. A Playwright test has failed.
Analyze and provide:
1. What went wrong (simple terms)
2. Most likely root cause
3. Suggested fix

Test Name: {test_name}
Error: {error_message[:1000]}
Page Content: {page_content[:500] if page_content else 'Not available'}"""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["content"][0]["text"]
    except Exception as e:
        # Agar API credits nahi hain toh mock response return karo
        return _mock_explanation(test_name, error_message)


def _mock_explanation(test_name: str, error_message: str) -> str:
    """
    Mock AI explanation — real API ka sample output dikhata hai.
    Actual production mein yeh Claude API se aata hai.
    """
    if "to_have_url" in error_message:
        return """**AI Failure Analysis (Sample Output)**
        
1. **What went wrong:** Test expected page to navigate to success URL after login, but page stayed on login page.

2. **Root Cause:** Invalid credentials were used — password 'WrongPass999' is incorrect. The login form rejected the credentials and did not redirect.

3. **Suggested Fix:** 
   - Verify the correct password is being used: 'Password123'
   - Check if the login endpoint has changed
   - Ensure no typos in credentials
   
*Note: This is a simulated failure for demonstration purposes.*"""
    
    elif "to_be_visible" in error_message:
        return """**AI Failure Analysis (Sample Output)**

1. **What went wrong:** Expected element was not found on the page within timeout period.

2. **Root Cause:** CSS selector may be incorrect or element takes longer to load than expected timeout (5000ms).

3. **Suggested Fix:**
   - Update the selector to match current DOM structure
   - Add explicit wait before assertion
   - Increase timeout if element loads slowly"""
    
    else:
        return """**AI Failure Analysis (Sample Output)**

1. **What went wrong:** Test assertion failed — actual page state did not match expected state.

2. **Root Cause:** Either test data changed, UI was updated, or timing issue caused premature assertion.

3. **Suggested Fix:**
   - Review recent UI changes
   - Add wait_for_load_state() before assertions
   - Update test data if application data has changed"""


def save_failure_report(failures: list, output_path: str = "reports/ai_failure_report.json"):
    """
    Saare failures ka AI report save karo.
    """
    report = {
        "total_failures": len(failures),
        "failures": failures
    }
    os.makedirs("reports", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n✅ AI Failure Report saved to: {output_path}")