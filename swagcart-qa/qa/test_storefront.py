from decimal import Decimal, ROUND_HALF_UP

import pytest
from selenium.webdriver.common.by import By


def test_login_and_inventory(store):
    store.login()
    assert len(store.products()) == 6
    assert store.element('.app_logo').text == 'SwagCart QA'


@pytest.mark.parametrize('username,password,message',[
    ('','secret_sauce','Username is required'),
    ('standard_user','','Password is required'),
    ('unknown','wrong','do not match'),
    ('locked_out_user','secret_sauce','locked out'),
])
def test_login_errors(store,username,password,message):
    store.login(username,password)
    assert message in store.element('[data-test="error"]').text
    assert not store.driver.current_url.endswith('/inventory.html')


@pytest.mark.parametrize('sort,descending,price',[
    ('az',False,False),('za',True,False),('lohi',False,True),('hilo',True,True)
])
def test_sorting(store,sort,descending,price):
    store.login()
    store.sort(sort)
    selector='.inventory_item_price' if price else '.inventory_item_name'
    values=[row.find_element(By.CSS_SELECTOR,selector).text for row in store.products()]
    if price:
        values=[Decimal(value.replace('$','')) for value in values]
    assert values == sorted(values,reverse=descending)


def test_add_remove_and_reload_cart(store):
    store.login()
    store.add('Sauce Labs Backpack')
    store.add('Sauce Labs Bike Light')
    assert store.cart_count() == 2
    store.driver.refresh()
    assert store.cart_count() == 2
    store.product('Sauce Labs Backpack').find_element(By.CSS_SELECTOR,'button').click()
    assert store.cart_count() == 1
    store.open_cart()
    assert [item.text for item in store.driver.find_elements(By.CSS_SELECTOR,'.inventory_item_name')] == ['Sauce Labs Bike Light']


@pytest.mark.parametrize('first,last,postal,message',[
    ('','Student','100000','First Name'),
    ('Test','','100000','Last Name'),
    ('Test','Student','','Postal Code'),
])
def test_checkout_required_fields(store,first,last,postal,message):
    store.login()
    store.add('Sauce Labs Backpack')
    store.open_cart()
    store.checkout_info(first,last,postal)
    assert message in store.element('[data-test="error"]').text
    assert '/checkout-step-one.html' in store.driver.current_url


@pytest.mark.parametrize('first,last', [('Test','Student'),('测试','同学')])
def test_checkout_totals_and_cart_cleared(store,first,last):
    store.login()
    store.add('Sauce Labs Backpack')
    store.add('Sauce Labs Bike Light')
    store.open_cart()
    store.checkout_info(first,last)
    subtotal=Decimal('29.99')+Decimal('9.99')
    tax=(subtotal*Decimal('0.08')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    assert store.element('[data-test="subtotal-label"]').text.endswith(str(subtotal))
    assert store.element('[data-test="tax-label"]').text.endswith(str(tax))
    assert store.element('[data-test="total-label"]').text.endswith(str(subtotal+tax))
    store.click('[data-test="finish"]')
    assert 'Thank you' in store.element('[data-test="complete-header"]').text
    assert store.cart_count() == 0


def test_anonymous_inventory_redirects_to_login(store):
    store.driver.get(store.base+'/inventory.html')
    store.element('#login_button_container')
    assert not store.driver.find_elements(By.CSS_SELECTOR,'.inventory_list')
