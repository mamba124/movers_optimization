import time
import json
from datetime import datetime 
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.inbox_selectors import NEXT_BUTTON, RADIO_BUTTON, NAME_SELECTOR, \
                                NEED_MORE_INFO, ANSWER_BUTTON, \
                                READ_MORE_INBOX, EXPIRED_TIME_QUOTE, \
                                YELP_WELCOME, LOGO, MSG_AREA

from src.inbox_selectors import FIRST_EXPIRED, NEXT_ACTIVE #todo add logic that checks if possibility to get fresh quote


def check_if_expired_from_page(driver):
    return "This job has expired" in driver.find_element("css selector", "html").get_attribute("innerHTML")


with open("secret_files/user_info.json", "r") as f:
    credentials = json.load(f)


def wait(driver, time, element):
    WebDriverWait(driver, time).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, element)))


def login(driver, link):
    wait(driver, 3, YELP_WELCOME)
    dog_check(driver)
    email_element = driver.find_elements("name", "email")
    pass_element = driver.find_elements("name", "password")
    if email_element and pass_element:
        email_element[0].send_keys(credentials["username"])
        pass_element[0].send_keys(credentials["password"])
        driver.find_elements("tag name", "button")[0].click()
        print(f"Authenticated at time {datetime.now().time()}")
        wait(driver, 5, LOGO)
       # time.sleep(2)
        return True


def get_opportunity(driver):
    dog_check(driver)
    time.sleep(0.1)
    success = False
    t1 = datetime.now().time()
    t2 = None
    print(f"Accessed at {datetime.now().time()}")
    html = driver.find_element("css selector", "html").get_attribute("innerHTML")
    if "Nearby Jobs Details" not in html:
        elements = driver.find_elements("css selector", READ_MORE_INBOX)
        if elements:
            elements[0].click()
            dog_check(driver)
    try:
        driver.find_element("css selector", NEED_MORE_INFO).click()
        name = driver.find_elements("css selector", NAME_SELECTOR)
        navigate_through_button_menu(driver)            

        message_text = build_message(name)
        message = driver.find_element("css selector", MSG_AREA)
        message.send_keys(message_text)       
        
        driver.find_element("css selector", ANSWER_BUTTON).click()
        t2 = datetime.now().time()
        logging.info(f"Answered at {datetime.now().time()}")
        print(f"Answered at {datetime.now().time()}")
        success = True
    except Exception as ex:
        print(ex)
        quote_time = driver.find_elements("css selector", EXPIRED_TIME_QUOTE)
        if quote_time:
            t2 = quote_time[0].text.split(": ")[-1]
            quote_time_string = f"Quote appeared at the time {t2}"
        else:
            quote_time_string = ""
        logging.info(f"Opportunity has expired, no dialogue window found.{quote_time_string}")
        print(f"Opportunity has expired, no dialogue window found.{quote_time_string}")
    return success, t1, t2


def navigate_through_button_menu(driver):
    driver.find_element("css selector", RADIO_BUTTON).click()
    time.sleep(0.2)
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
    try:
        wait(driver, 8, element=LOGO)
    finally:    
        html = driver.find_elements("css selector", "html")[0].get_attribute("outerHTML")
        if "HTTP 504 - GATEWAY TIMEOUT" in html:
            driver.refresh()
            print("HTTP 504 - GATEWAY TIMEOUT, refreshing..")
            logging.info("HTTP 504 - GATEWAY TIMEOUT, refreshing..")