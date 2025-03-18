# test_login.py
import pytest
from playwright.sync_api import Page, sync_playwright

from src.pages.LoginPage import LoginPage


def test_login_with_valid_credentials(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["valid_user"]["username"])
    login_page.enter_password(test_data["valid_user"]["password"])
    page.screenshot(path="screenshots/login_page.png")

    login_page.click_login()
    page.screenshot(path="screenshots/login_successfully.png")
    # print(page.url)

    assert page.url == "https://www.saucedemo.com/inventory.html"


def test_login_with_locked_out_user(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["locked_out_user"]["username"])
    login_page.enter_password(test_data["locked_out_user"]["password"])
    login_page.click_login()
    assert login_page.error_message.is_visible()
    assert login_page.error_message.inner_text() == "Epic sadface: Sorry, this user has been locked out."

def test_login_with_problem_user(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["problem_user"]["username"])
    login_page.enter_password(test_data["problem_user"]["password"])
    login_page.click_login()
    assert page.url == "https://www.saucedemo.com/inventory.html"


def test_login_with_performance_glitch_user(page,test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["performance_glitch_user"]["username"])
    login_page.enter_password(test_data["performance_glitch_user"]["password"])
    login_page.click_login()
    assert page.url == "https://www.saucedemo.com/inventory.html"

def test_login_with_invalid_username(page,test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["invalid_username"]["username"])
    login_page.enter_password(test_data["invalid_username"]["password"])
    login_page.click_login()
    assert login_page.error_message.is_visible()
    assert login_page.error_message.inner_text() == "Epic sadface: Username and password do not match any user in this service"

def test_login_with_invalid_password(page,test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["invalid_username"]["username"])
    login_page.enter_password(test_data["invalid_password"]["password"])
    login_page.click_login()
    assert login_page.error_message.is_visible()
    assert login_page.error_message.text_content() == "Epic sadface: Username and password do not match any user in this service"

