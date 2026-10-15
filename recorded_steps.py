import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    page.get_by_text("Sauce Labs Backpackcarry.").click()
    page.locator("[data-test=\"item-1-title-link\"]").click()
    page.locator("[data-test=\"add-to-cart\"]").click()
    page.locator("[data-test=\"back-to-products\"]").click()
    page.get_by_text("Rib snap infant onesie for").click()
    page.locator("[data-test=\"item-2-img-link\"]").click()
    page.locator("[data-test=\"add-to-cart\"]").click()
    page.locator("[data-test=\"back-to-products\"]").click()
    page.locator("[data-test=\"add-to-cart-test.allthethings()-t-shirt-(red)\"]").click()
    page.locator("[data-test=\"product-sort-container\"]").select_option("lohi")
