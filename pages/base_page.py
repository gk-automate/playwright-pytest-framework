import re
import allure
from playwright.sync_api import Page, Locator, expect
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(settings.DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)

    @allure.step("Navigate to path: {path}")
    def navigate(self, path: str = "") -> None:
        url = f"{settings.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Click element: {description}")
    def click(self, locator: Locator, description: str = "element") -> None:
        logger.info(f"Clicking on {description}")
        locator.click()

    @allure.step("Fill '{value}' into {description}")
    def fill(self, locator: Locator, value: str, description: str = "input") -> None:
        logger.info(f"Filling {description} with value '{value}'")
        locator.fill(value)

    def assert_url_contains(self, substring: str) -> None:
        expect(self.page).to_have_url(re.compile(f".*{substring}.*"))