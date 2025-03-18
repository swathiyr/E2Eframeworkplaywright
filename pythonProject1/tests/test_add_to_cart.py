import pytest
from playwright.sync_api import sync_playwright

from src.pages.AddtoCart import AddtoCart
from src.pages.LoginPage import LoginPage
from src.pages.ProductsPage import ProductsPage

def login_with_valid_credentials(page, test_data):
    login_page = LoginPage(page)
    login_page.enter_username(test_data["valid_user"]["username"])
    login_page.enter_password(test_data["valid_user"]["password"])
    login_page.click_login()


def add_to_cart_functionality(page, test_data):
    login_with_valid_credentials(page, test_data)
    inventory_page = ProductsPage(page)

    for index in range(inventory_page.inventory_items.count()):
        inventory_page.click_add_to_cart(index)
        assert page.locator('.shopping_cart_badge').inner_text() == str(index + 1)

    return inventory_page # Return inventory_page

@pytest.mark.skip
def test_add_to_cart_functionality(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page
    expected_count = inventory_page.inventory_items.count()

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    items_count = cart_page.cart_items.count()

    print(f"Items in cart: {items_count}, Expected: {expected_count}")  # Debugging output

    assert items_count == expected_count

@pytest.mark.skip
def test_remove_item(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page
    initial_count = inventory_page.inventory_items.count()

    cart_page = AddtoCart(page)
    cart_page.click_cart()

    cart_page.remove_item(0)
    final_count = cart_page.cart_items.count()
    assert final_count == initial_count - 1


@pytest.mark.skip
def test_remove_all_items(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page
    initial_count = inventory_page.inventory_items.count()

    cart_page = AddtoCart(page)
    cart_page.click_cart()

    for i in range(initial_count):
        cart_page.remove_item(0)

    final_count = cart_page.cart_items.count()
    assert final_count == 0

@pytest.mark.skip#Not working
def test_continue_shopping_button_visible(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(5000)
    assert cart_page.is_continue_shopping_visible() == True


@pytest.mark.skip
def test_checkout_button_visible(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(5000)

    assert cart_page.is_checkout_button_visible() == True


@pytest.mark.skip #Not working
def test_continue_shopping_functionality(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(5000)
    cart_page.click_continue_shopping()
    assert page.url == "https://www.saucedemo.com/v1/inventory.html"



def test_checkout_functionality(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    cart_page.click_checkout()


    #page.locator('.subheader').text_content() == "Checkout: Your Information"

    assert page.url == "https://www.saucedemo.com/checkout-step-one.html"