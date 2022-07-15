import time
import json
from datetime import datetime 
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.inbox_selectors import NEXT_BUTTON, RADIO_BUTTON, NAME_SELECTOR, \
                                NEED_MORE_INFO, ANSWER_BUTTON, \
                                SEE_FIRST, EXPIRED_TIME_QUOTE, \
                                YELP_WELCOME, LOGO, MSG_AREA, NEARBY_DETAILS

from src.inbox_selectors import NEXT_ACTIVE #todo add logic that checks if possibility to get fresh quote


def check_if_expired_from_page(driver):
    return "This job has expired" in driver.find_element("css selector", "html").get_attribute("innerHTML")


with open("secret_files/user_info.json", "r") as f:
    credentials = json.load(f)


def wait(driver, time, element):
    WebDriverWait(driver, time).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, element)))

#1 first time. logged is true, but captcha
#2 captcha, logged is false, captcha still
#3 captcha, logged is false, captcha is off, logged becomes true
def login(driver, link, logged=True):
    wait(driver, 3, YELP_WELCOME)
    dog_check(driver)
    if logged:
        email_element = driver.find_elements("name", "email")
        pass_element = driver.find_elements("name", "password")
        if email_element and pass_element:
            email_element[0].send_keys(credentials["username"])
            pass_element[0].send_keys(credentials["password"])
            driver.find_elements("class name", "css-cednmx")[0].click()
    try:
        wait(driver, 15, YELP_WELCOME)
        if driver.find_elements("name", "password"):
            print("Alarm! Captha")
            logged = False
        else:
            logged = True
            print(f"Authenticated at time {datetime.now().time()}")
    except:
        logged = True        
    return logged

def get_opportunity(driver): 
    dog_check(driver) 
    success = False
    t1 = datetime.now().time()
    print(f"Accessed at {datetime.now().time()}")

    print("Nearby jobs details fork")
    check_fork(driver)

    try:
        print("Look for Next active page or Need more info buttons")
        process_main_buttons(driver)
        
        name = driver.find_elements("css selector", NAME_SELECTOR)
        navigate_through_button_menu(driver)            

        t2, success = send_message(driver, name)  

    except Exception as ex:
        print(ex)
        quote_time = driver.find_elements("css selector", EXPIRED_TIME_QUOTE)        
        t2 = build_bad_message(quote_time)
    return success, t1, t2


def navigate_through_button_menu(driver):
    time.sleep(5)
    radio = driver.find_elements("css selector", RADIO_BUTTON)
 
    radio[0].click()
    time.sleep(1)
    is_next = driver.find_elements("css selector", NEXT_BUTTON)
    if is_next:
        is_next[0].click()


def build_message(name):
    if name:
        message_text = f"Hi, {name[0].text}! Thank you for contacting California Express Movers."
    else:
        message_text = "Hi! Thank you for contacting California Express Movers."
    return message_text


def dog_check(driver):
    print("dog check start")
    try:
        print("try find logo in dogcheck")
        wait(driver, 8, element=LOGO)
    finally:
        print("go gateway")
        html = driver.find_elements("css selector", "html")[0].get_attribute("outerHTML")
        if "HTTP 504 - GATEWAY TIMEOUT" in html or "This page is having" in html:
            driver.refresh()
            print("HTTP 504 - GATEWAY TIMEOUT, refreshing..")
            logging.info("HTTP 504 - GATEWAY TIMEOUT, refreshing..")
    print("dog check finish")


def check_fork(driver):
    html = driver.find_element("css selector", "html").get_attribute("innerHTML")
    if "Nearby Jobs Details" not in html:
        elements = driver.find_elements("css selector", SEE_FIRST)
        if elements:
            elements[0].click()
            dog_check(driver)


#TODO Debug logic for Next active quote
def process_main_buttons(driver):
   # next_active = driver.find_elements("css selector", NEXT_ACTIVE)
    more_info = driver.find_elements("css selector", NEED_MORE_INFO)
  #  if next_active:
  #      time.sleep(5)
  #      next_active[0].click()
    if more_info:
        time.sleep(5)
        more_info[0].click()


def send_message(driver, name):
    message_text = build_message(name)
    message = driver.find_element("css selector", MSG_AREA)
    message.send_keys(message_text)
    driver.find_element("css selector", ANSWER_BUTTON).click()
    t2 = datetime.now().time()
    success = True    
    return t2, success


def build_bad_message(quote_time):
    if quote_time:
        t2 = quote_time[0].text.split(": ")[-1]
        quote_time_string = f"Quote appeared at the time {t2}"
    else:
        quote_time_string = ""
        t2 = None
    print(f"Opportunity has expired, no dialogue window found.{quote_time_string}")
    return t2