import pytest
from playwright.sync_api import sync_playwright
from src.pages.LoginPage import LoginPage
from src.pages.MenuBar import MenuBar
from src.pages.ProductsPage import ProductsPage

def login_with_valid_credentials(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["valid_user"]["username"])
    login_page.enter_password(test_data["valid_user"]["password"])
    login_page.click_login()


def test_click_all_items(page, test_data):
    login_with_valid_credentials(page, test_data)
    menu_page = MenuBar(page)

    menu_page.click_burger_button()
    menu_page.click_all_items()
    assert page.title() == "Swag Labs"


def test_click_about(page, test_data):
    login_with_valid_credentials(page, test_data)
    menu_page = MenuBar(page)

    menu_page.click_burger_button()
    menu_page.click_about()

    assert page.title() == "Sauce Labs: Cross Browser Testing, Selenium Testing & Mobile Testing"

def test_click_logout(page, test_data):
    login_with_valid_credentials(page, test_data)
    menu_page = MenuBar(page)

    menu_page.click_burger_button()
    menu_page.click_logout()

    assert page.title() == "Swag Labs"


