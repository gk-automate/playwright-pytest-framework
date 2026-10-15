from playwright.sync_api import Page, expect


class Navbar:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_link")
        self.burger_menu_btn = page.get_by_role("button", name="Open Menu")
        self.app_logo = page.locator(".app_logo")

    def verify_logged_in(self) -> None:
        expect(self.app_logo).to_have_text("Swag Labs")
        expect(self.cart_badge).to_be_visible()