from pathlib import Path
from typing import Generator
import pytest
import allure
from playwright.sync_api import Playwright, APIRequestContext, Browser, BrowserContext, Page
from config.settings import settings
from api.endpoints.project_api import ProjectAPI
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Session-scoped API context for fast data setup/teardown and API contract tests."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
    }
    request_context = playwright.request.new_context(
        base_url=settings.API_BASE_URL,
        extra_http_headers=headers,
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="function")
def project_api(api_request_context: APIRequestContext) -> ProjectAPI:
    return ProjectAPI(api_request_context)


@pytest.fixture(scope="session")
def worker_id(request) -> str:
    """Safely returns xdist worker ID (gw0, gw1) or 'master' when running without -n."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"


@pytest.fixture(scope="session")
def auth_storage_state(browser: Browser, worker_id: str) -> str:
    """Logs in ONCE per worker and caches cookies/localStorage to .auth/."""
    auth_dir = Path(".auth")
    auth_dir.mkdir(exist_ok=True)
    state_file = auth_dir / f"storage_state_{worker_id}.json"

    logger.info(f"Generating authenticated storage state for worker: {worker_id}")
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)
    page.wait_for_url("**/inventory.html**")

    context.storage_state(path=str(state_file))
    context.close()
    return str(state_file)


@pytest.fixture(scope="function")
def auth_context(browser: Browser, auth_storage_state: str) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(
        storage_state=auth_storage_state,
        viewport={"width": 1920, "height": 1080},
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def auth_page(auth_context: BrowserContext) -> Generator[Page, None, None]:
    page = auth_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(auth_page: Page) -> DashboardPage:
    return DashboardPage(auth_page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("auth_page") or item.funcargs.get("page")
        if page and not page.is_closed():
            logger.error(f"Test '{item.name}' failed. Capturing failure screenshot.")
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"Failure_Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )