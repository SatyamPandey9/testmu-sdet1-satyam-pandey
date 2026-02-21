# Prompts Used for Test Generation

## Login Module

**Prompt:**
You are a senior QA engineer. Generate Playwright Python test cases for a Login module.
Cover: valid login, invalid credentials (wrong username, wrong password),
empty credentials, and brute-force lockout after 5 attempts.
Use pytest fixtures for page. Be specific about selectors and error messages.

**What didn't work first time:**
First prompt was too vague — didn't specify framework or selectors.
Added "Playwright Python" and "pytest fixtures" to get framework-specific code.
Also added specific scenarios like brute-force to get better coverage.

---

## Dashboard Module

**Prompt:**
You are a senior QA engineer. Generate Playwright Python test cases for a Dashboard module.
The dashboard loads after successful login at practicetestautomation.com.
Cover: page load verification, heading visibility, logout button presence,
congratulations text, and logout functionality.
Use get_by_role() selectors instead of CSS classes for reliability.

**What didn't work first time:**
CSS selector "a.button" failed — element not found.
Changed to get_by_role("link", name="Log out") which is more reliable.
Also fixed strict mode violation on "p" locator by using filter(has_text=).

---

## REST API Module

**Prompt:**
You are a senior QA engineer. Generate Python pytest test cases for REST API testing
using the requests library. Use JSONPlaceholder (jsonplaceholder.typicode.com) as test API.
Cover: GET single/multiple resources, POST create, PUT update, DELETE,
404 error handling, and schema validation.
Assert status codes and response body fields explicitly.

**What didn't work first time:**
First prompt didn't specify which API to use — got generic code.
Added JSONPlaceholder URL explicitly. Also added schema validation test
which wasn't in original output.