from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_btn = page.locator("[data-test='login-button']")
        self.error_alert = page.locator("[data-test='error']")

    def login(self, username: str, password: str) -> None:
        self.navigate("/")
        self.fill(self.username_input, username, "Username Input")
        self.fill(self.password_input, password, "Password Input")
        self.click(self.login_btn, "Login Button")

    def assert_login_error(self, expected_text: str) -> None:
        expect(self.error_alert).to_be_visible()
        expect(self.error_alert).to_contain_text(expected_text)