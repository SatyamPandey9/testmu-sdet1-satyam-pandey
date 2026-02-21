import pytest
import json
import os
from playwright.sync_api import sync_playwright
from ai_integration.failure_explainer import explain_failure, save_failure_report

# Store all failures for AI report
failure_list = []

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        test_name = item.name
        error_message = str(report.longrepr)

        print(f"\n🤖 AI is analyzing failure: {test_name}...")
        
        # Get page content if available
        page_content = ""
        if "page" in item.funcargs:
            try:
                page_content = item.funcargs["page"].content()[:2000]
            except:
                page_content = "Page content unavailable"

        # Call AI for explanation
        ai_explanation = explain_failure(test_name, error_message, page_content)
        
        print(f"\n🔍 AI Explanation:\n{ai_explanation}\n")

        # Store failure
        failure_list.append({
            "test_name": test_name,
            "error": error_message[:500],
            "ai_explanation": ai_explanation
        })

def pytest_sessionfinish(session, exitstatus):
    """Test session khatam hone pe AI report save karo"""
    if failure_list:
        save_failure_report(failure_list)
    else:
        print("\n✅ No failures detected — No AI report needed!")