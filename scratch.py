from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.firefox.options import Options as FirefoxOptions

options = FirefoxOptions()
options.add_argument("--headless")
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import json

url = "https://secure.3gdirectpay.com/API/v7/index.php"


def get_transaction_token(payment_url):
    """
    get transaction token from given payment url
    :param payment_url:
    :return:
    """
    if payment_url is not None:
        parsed_url = urlparse(payment_url)
        transaction_token = parse_qs(parsed_url.query)['ID'][0]
        return transaction_token


lte_number = None
package = None
driver = webdriver.Firefox(options=options)
print('Selenium is opening the url opening https://zm.liquidhome.tech/myliquid/')
driver.get('https://zm.liquidhome.tech/myliquid/')
print('finding email field...')
email_field = driver.find_element(by.CSS_SELECTOR, '.form-control__icon-email')
print('finding password field...')
password_field = driver.find_element(by.CSS_SELECTOR, '.form-control__icon-lock')
print('finding login button...')
log_in_button = driver.find_element(by.CSS_SELECTOR, '.btn-block')
print('filling in email field..')
email_field.send_keys('jack@jacktembo.com')
print('filling in password field')
password_field.send_keys('30970084')
print('loging in: please wait...')
log_in_button.click()
print('clicking on topup friend..')
topup_friend = driver.find_element(by.CSS_SELECTOR, 'a[href="#modalTopupFriends"]')
topup_friend.click()
sleep(3)
modal = driver.find_element(by.CSS_SELECTOR, '.modal-content')
name_field = driver.find_element(by.CSS_SELECTOR, 'input[name="name"]')
phone_field = driver.find_element(by.CSS_SELECTOR, 'input[name="phone"]')
name_field.send_keys(random.random())
phone_field.send_keys(lte_number)
phone_field.send_keys(Keys.ENTER)
sleep(4)
topup_action = driver.find_elements(by.CSS_SELECTOR, '.action-topup-friend')
topup_action[-1].click()
sleep(3)
packages = driver.find_elements(by.CSS_SELECTOR, '.package-item--button')
packages[int(package.identifier)].submit()
payment_title = 'Online Payments - Direct Pay Online'
driver.implicitly_wait(10)
WebDriverWait(driver, 10).until(
    EC.title_is(payment_title)
)
payment_url = driver.current_url
print(f"Your payment url is {payment_url}")
payment_amount = 1
transaction_token = get_transaction_token(payment_url)
company_token = "EB310B77-FE73-427B-B3BB-97F19A0D70EA"
data = {"Request": "UpdateToken", "CompanyToken": company_token, "TransactionToken": transaction_token,
        "PaymentAmount": payment_amount}

r = requests.post(url, data=json.dumps(data))
print('Updating the amount to K1 Please wait...')
print('Amount successfully updated...')
if r.json().get('Code', 1) == '000':
    print('success')
    driver.refresh()
else:
    print('failed')
print('Stopping selenium because the job is complete..')
driver.quit()
