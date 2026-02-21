import pytest
from playwright.sync_api import expect

BASE_URL = "https://practicetestautomation.com/practice-test-login/"

class TestDashboard:

    def login(self, page):
        page.goto(BASE_URL)
        page.fill("#username", "student")
        page.fill("#password", "Password123")
        page.click("#submit")
        page.wait_for_url("**/logged-in-successfully/")

    def test_dashboard_loads_after_login(self, page):
        self.login(page)
        expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")
        expect(page.locator("h1")).to_be_visible()

    def test_dashboard_heading_visible(self, page):
        self.login(page)
        expect(page.locator("h1")).to_contain_text("Logged In Successfully")

    def test_logout_button_visible(self, page):
        self.login(page)
        expect(page.get_by_role("link", name="Log out")).to_be_visible()

    def test_dashboard_congratulations_text(self, page):
        self.login(page)
        expect(page.get_by_role("paragraph").filter(has_text="Congratulations")).to_be_visible()

    def test_logout_functionality(self, page):
        self.login(page)
        page.get_by_role("link", name="Log out").click()
        expect(page).to_have_url(BASE_URL)