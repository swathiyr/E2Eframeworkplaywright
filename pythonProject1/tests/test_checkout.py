import pytest
from playwright.sync_api import sync_playwright

from src.pages.AddtoCart import AddtoCart
from src.pages.Checkout import Checkoutpage
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


def checkout_functionality(page, test_data):
    inventory_page = add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    cart_page.click_checkout()

    return inventory_page

@pytest.mark.skip
def test_fill_details(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])

    page.wait_for_timeout(3000)
    checkout_page.click_continue()
    page.wait_for_timeout(3000)

@pytest.mark.skip
def test_click_cancel(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])

    checkout_page.click_cancel()
    page.wait_for_timeout(1000)
    assert page.url == "https://www.saucedemo.com/cart.html"


@pytest.mark.skip
def test_input_acceptance(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])
    assert checkout_page.first_name_input.input_value() == "John"
    assert checkout_page.last_name_input.input_value() == "Doe"
    assert checkout_page.postal_code_input.input_value() == "94555"



def test_empty_first_name(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])
    checkout_page.click_continue()

    if checkout_page.errorhandling.is_visible():
        print("Error message is visible!")
        print(page.locator("h3[data-test='error']").text_content())
    else:
        print("Error message is NOT visible!")



    #assert checkout_page.errorhandling.is_visible()
    #print(checkout_page.errorhandling.text_content())


@pytest.mark.skip
def test_empty_last_name(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])
    checkout_page.click_continue()
    assert checkout_page.errorhandling.is_visible()
    print(checkout_page.errorhandling.text_content())


@pytest.mark.skip
def test_empty_postalcode_name(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.click_continue()
    assert checkout_page.errorhandling.is_visible()
    print(checkout_page.errorhandling.text_content())


@pytest.mark.skip
def test_long_input(page, test_data):
    checkout_functionality(page, test_data)

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name("A" * 256)
    checkout_page.fill_last_name("B" * 256)
    checkout_page.fill_postal_code("C" * 256)
    assert len(checkout_page.first_name_input.input_value()) <= 256
    assert len(checkout_page.last_name_input.input_value()) <= 256
    assert len(checkout_page.postal_code_input.input_value()) <= 256