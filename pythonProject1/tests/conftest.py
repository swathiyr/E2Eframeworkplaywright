import os
import pytest
from playwright.sync_api import Playwright, sync_playwright, Browser, Page
import yaml

from src.pages.LoginPage import LoginPage
from src.pages.ProductsPage import ProductsPage

BASE_URL = "https://www.saucedemo.com"  # Define the URL here
yaml_path = os.path.join('tests/test_data.yaml', "test_data.yaml")



@pytest.fixture(scope="session")
def test_data():
    """Load test data from YAML file using an absolute path."""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of conftest.py
    yaml_path = os.path.join(base_dir, "test_data.yaml")  # Full path

    print(f"🔥 Debug: Expected YAML path: {yaml_path}")  # Debugging path output

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"❌ test_data.yaml NOT FOUND at: {yaml_path}")

    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)

    return data


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Initialize Playwright instance once per test session."""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """Launch a browser instance (Chromium) once per test session."""
    browser = playwright_instance.chromium.launch(headless=False,args=['--start-maximized'])  # Change to True for headless mode

    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """Create a new browser context and page for each test function."""
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto(BASE_URL)  # Automatically navigate to the defined URL
    yield page
    page.close()
    context.close()

