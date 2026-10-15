from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.components.navbar import Navbar


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = Navbar(page)
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge_count = page.locator(".shopping_cart_badge")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.item_prices = page.locator(".inventory_item_price")

    def open_dashboard(self) -> None:
        self.navigate("/inventory.html")
        self.navbar.verify_logged_in()

    def get_item_by_name(self, name: str):
        return self.inventory_items.filter(has_text=name)

    def add_item_to_cart(self, name: str) -> None:
        item = self.get_item_by_name(name)
        add_btn = item.get_by_role("button", name="Add to cart")
        self.click(add_btn, f"Add to cart button for {name}")

    def sort_by_price_low_to_high(self) -> None:
        self.sort_dropdown.select_option("lohi")

    def assert_first_item_price(self, expected_price: str) -> None:
        expect(self.item_prices.first).to_have_text(expected_price)

    def assert_item_visible(self, name: str) -> None:
        item = self.get_item_by_name(name)
        expect(item).to_be_visible()

    def assert_cart_count(self, expected_count: int) -> None:
        expect(self.cart_badge_count).to_have_text(str(expected_count))