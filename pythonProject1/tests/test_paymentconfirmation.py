import pytest
from playwright.sync_api import sync_playwright

from src.pages.AddtoCart import AddtoCart
from src.pages.Checkout import Checkoutpage
from src.pages.LoginPage import LoginPage
from src.pages.Payment_page import Paymentpage
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
    add_to_cart_functionality(page, test_data)  # Capture the returned inventory_page

    cart_page = AddtoCart(page)
    cart_page.click_cart()
    cart_page.click_checkout()

    checkout_page = Checkoutpage(page)
    checkout_page.fill_first_name(test_data["checkout_page"]["firstname"])
    checkout_page.fill_last_name(test_data["checkout_page"]["lastname"])
    checkout_page.fill_postal_code(test_data["checkout_page"]["postalcode"])

    checkout_page.click_continue()

    return checkout_page

@pytest.mark.skip
def test_print_item_name(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    item_names = payment_page.item_name_input.all_inner_texts()
    print(item_names)

@pytest.mark.skip
def test_print_item_price(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    item_price = payment_page.item_price.all_inner_texts()
    print(item_price)

@pytest.mark.skip
def test_itemtotal(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    item_price = payment_page.item_price.all_inner_texts()

    # Extract numeric values by stripping '$' and converting to float
    numeric_prices = [float(price.replace('$', '')) for price in item_price]

    # Sum up the prices
    total_price = sum(numeric_prices)

    # Get total summary text
    total_sum_text = payment_page.get_itemtotal_total

    # Extract the numeric value (remove text & '$', then convert to float)
    total_sum_numeric = float(total_sum_text.replace('Item total: $', ''))

    # Debugging print statements (optional)
    print(f"Extracted total: {total_sum_numeric}, Calculated total: {total_price}")

    # Perform assertion
    assert total_price == total_sum_numeric, f"Expected {total_price}, but got {total_sum_numeric}"

@pytest.mark.skip
def test_sum_total(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    item_price = payment_page.item_price.all_inner_texts()

    # Extract numeric values by stripping '$' and converting to float
    numeric_prices = [float(price.replace('$', '')) for price in item_price]

    # Sum up the prices
    total_price = sum(numeric_prices)

    # Get total summary text
    total_sum_text = payment_page.get_itemtotal_total

    # Extract the numeric value (remove text & '$', then convert to float)
    total_sum_numeric = float(total_sum_text.replace('Item total: $', ''))

    # Debugging print statements (optional)
    print(f"Extracted total: {total_sum_numeric}, Calculated total: {total_price}")

    tax_text = payment_page.item_tax
    # Extract the numeric value (remove text & '$', then convert to float)
    total_tax_numeric = float(tax_text.replace('Tax: $', ''))

    sum_total = total_sum_numeric + total_tax_numeric

    total_text = payment_page.summary_total_label
    total_text_numeric = float(total_text.replace('Total: $', ''))


    assert total_text_numeric == sum_total


def test_Finish(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(3000)

    payment_page.click_finish()

    assert page.locator("//h2[class='complete-header']")

@pytest.mark.skip
def test_cancel(page, test_data):
    checkout_functionality(page, test_data)

    payment_page = Paymentpage(page)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    payment_page.click_cancel()

    page.wait_for_timeout(3000)

    assert page.locator("//div[class='product_label']").page.url == page.url












