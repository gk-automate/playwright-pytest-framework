import pytest
from api.endpoints.project_api import ProjectAPI
from api.models import ProjectCreatePayload
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_authenticated_dashboard_and_add_to_cart(
    project_api: ProjectAPI,
    dashboard_page: DashboardPage
):
    """
    Hybrid E2E Test:
    1. Seeds a test record via API
    2. Opens UI Dashboard directly (already logged in via cached storage_state!)
    3. Adds an item to cart and verifies the badge count
    """
    # Step 1: Fast API setup
    seeded = project_api.create_project(ProjectCreatePayload(title="Sauce Labs Backpack"))
    assert seeded.id is not None

    # Step 2: UI validation using pre-authenticated session
    dashboard_page.open_dashboard()
    dashboard_page.assert_item_visible(seeded.title)
    dashboard_page.add_item_to_cart(seeded.title)
    dashboard_page.assert_cart_count(1)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("username,password,expected_error", [
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("standard_user", "wrong_password", "Username and password do not match"),
])
def test_invalid_login_shows_error_banner(
    login_page: LoginPage,
    username: str,
    password: str,
    expected_error: str
):
    """Negative UI login test using unauthenticated page fixture."""
    login_page.login(username, password)
    login_page.assert_login_error(expected_error)

@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_low_to_high(dashboard_page: DashboardPage):
    """Verifies sorting products from low to high puts the $7.99 Onesie first."""
    dashboard_page.open_dashboard()
    dashboard_page.sort_by_price_low_to_high()
    dashboard_page.assert_first_item_price("$7.99")