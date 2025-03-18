import pytest
from playwright.sync_api import sync_playwright
from src.pages.LoginPage import LoginPage
from src.pages.ProductsPage import ProductsPage

def login_with_valid_credentials(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["valid_user"]["username"])
    login_page.enter_password(test_data["valid_user"]["password"])
    login_page.click_login()


def test_click_item_name(page,test_data):
    login_with_valid_credentials(page, test_data)
    inventory_page = ProductsPage(page)
    item_names = inventory_page.item_names.all_inner_texts()
    #print(item_names)

    for index in range(inventory_page.inventory_items.count()):
        page.wait_for_timeout(2000)
        inventory_page.click_item_name(index)
        page.wait_for_timeout(3000)
        assert item_names[index] == page.locator('.inventory_details_name').text_content()
        assert page.locator('.inventory_details_name').text_content() in item_names
        page.go_back()


def test_click_item_image(page,test_data):
    login_with_valid_credentials(page, test_data)
    inventory_page = ProductsPage(page)
    item_names = inventory_page.item_names.all_inner_texts()

    for index in range(inventory_page.inventory_items.count()):
        #page.wait_for_timeout(2000)
        inventory_page.click_item_image(index)
        #print(page.locator('.inventory_details_name').text_content())
        #assert item_names[index] == page.locator('.inventory_details_name').text_content()
        assert page.url == f"https://www.saucedemo.com/inventory-item.html?id={str(index)}"
        assert page.locator('.inventory_details_name').text_content() in item_names
        page.go_back()


def test_add_to_cart_functionality(page,test_data):
    login_with_valid_credentials(page, test_data)
    inventory_page = ProductsPage(page)

    for index in range(inventory_page.inventory_items.count()):
        inventory_page.click_add_to_cart(index)
        # Add assertion to check if the item is added to the cart (this may require checking a cart counter or similar)
        assert page.locator('.shopping_cart_badge').inner_text() == str(index + 1)

        page.wait_for_timeout(3000)


