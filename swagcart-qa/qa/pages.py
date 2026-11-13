"""Page object keeps browser operations separate from business assertions."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class Storefront:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base = base_url
        self.wait = WebDriverWait(driver, 12)

    def element(self, selector):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def click(self, selector):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

    def login(self, username="standard_user", password="secret_sauce"):
        self.driver.get(self.base)
        self.driver.execute_async_script("const done=arguments[0]; document.fonts.ready.then(() => done());")
        self.element('#user-name').send_keys(username)
        self.element('#password').send_keys(password)
        self.click('[data-test="login-button"]')

    def products(self):
        self.element('.inventory_list')
        return self.driver.find_elements(By.CSS_SELECTOR, '.inventory_item')

    def product(self, name):
        return next(item for item in self.products() if item.find_element(By.CSS_SELECTOR,'.inventory_item_name').text == name)

    def add(self, name):
        self.product(name).find_element(By.CSS_SELECTOR,'button').click()

    def open_cart(self):
        self.click('.shopping_cart_link')
        self.wait.until(EC.url_contains('/cart.html'))
        self.element('#cart_contents_container')

    def checkout_info(self, first="Test", last="Student", postal="100000"):
        self.click('[data-test="checkout"]')
        self.wait.until(EC.url_contains('/checkout-step-one.html'))
        for field,value in [('first-name',first),('last-name',last),('postal-code',postal)]:
            self.element('#'+field).send_keys(value)
        self.click('[data-test="continue"]')

    def sort(self, value):
        Select(self.element('[data-test="product-sort-container"]')).select_by_value(value)

    def cart_count(self):
        badges = self.driver.find_elements(By.CSS_SELECTOR,'.shopping_cart_badge')
        return int(badges[0].text) if badges else 0
