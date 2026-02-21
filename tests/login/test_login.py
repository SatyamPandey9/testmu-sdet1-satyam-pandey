import pytest
from playwright.sync_api import expect

BASE_URL = "https://practicetestautomation.com/practice-test-login/"

class TestLogin:
    
    def test_valid_login(self, page):
        """Valid credentials se login hona chahiye"""
        page.goto(BASE_URL)
        page.fill("#username", "student")
        page.fill("#password", "Password123")
        page.click("#submit")
        expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")
        expect(page.locator("h1")).to_contain_text("Logged In Successfully")

    def test_invalid_username(self, page):
        """Invalid username se login fail hona chahiye"""
        page.goto(BASE_URL)
        page.fill("#username", "wronguser")
        page.fill("#password", "Password123")
        page.click("#submit")
        expect(page.locator("#error")).to_be_visible()
        expect(page.locator("#error")).to_contain_text("Your username is invalid!")

    def test_invalid_password(self, page):
        """Invalid password se login fail hona chahiye"""
        page.goto(BASE_URL)
        page.fill("#username", "student")
        page.fill("#password", "wrongpassword")
        page.click("#submit")
        expect(page.locator("#error")).to_be_visible()
        expect(page.locator("#error")).to_contain_text("Your password is invalid!")

    def test_empty_credentials(self, page):
        """Empty fields se login fail hona chahiye"""
        page.goto(BASE_URL)
        page.click("#submit")
        expect(page.locator("#error")).to_be_visible()

    def test_brute_force_lockout(self, page):
        """Multiple failed attempts ke baad error aana chahiye"""
        page.goto(BASE_URL)
        for i in range(5):
            page.fill("#username", "wronguser")
            page.fill("#password", "wrongpass")
            page.click("#submit")
            page.wait_for_timeout(500)
        expect(page.locator("#error")).to_be_visible()