from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import time
from datetime import datetime 
import logging



NEXT_BUTTON = "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(2) > div > button" 
RADIO_BUTTON = "#how_do_you_want_to_get_more_information--3"
NAME_SELECTOR = "body > yelp-react-root > div:nth-child(1) > div.messenger-container__09f24__qt8O4 > div > div.messenger_right__09f24__fndbc.border--left__09f24__Lt8WF.border-color--default__09f24__JbNoB > div > div > div.u-flex__09f24__rt07y.u-flex-column__09f24__m6LIn.u-flex-item__09f24__YuSEF.border-color--default__09f24__JbNoB > div.messenger_right_top__09f24__ZxW58.u-padding-t3.u-padding-b3.border--bottom__09f24__Yl28T.border-color--default__09f24__JbNoB > div > div > div > div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.border-color--default__09f24__NPAKY > div.user-passport-info.border-color--default__09f24__NPAKY > span > a"
OPTION_BUTTON = "div.margin-r3__09f24__ppHm0:nth-child(2) > button"
SEND_BUTTON = "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(3) > button"
#CROSS_SELECTOR = ".dismiss-link__09f24__Q1RVn"
#NOTIFICATION_SELECTOR = ".close-button__09f24__qgCyrs"

def generate_proxy():
    profile = webdriver.FirefoxProfile()
    options = Options()
    options.headless = True
    options.add_argument("start-maximized")

    driver = webdriver.Firefox(profile, options=options)
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered']//th[contains(., 'IP Address')]"))))

    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 2]")))]
    
    driver.quit()
    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])
    pos = random.randint(0, len(proxies))
    try:
        print("Proxy selected: {}".format(proxies[pos]))
        my_proxy = proxies[pos]
    except Exception as e:
        print(e)
        driver.quit()
        my_proxy = None
    return my_proxy


def initialize_driver():
    for attempt in range(5):
        sleep_time = 1.8 ** attempt
        my_proxy = generate_proxy()
        if my_proxy:
            break
        else:
            time.sleep(sleep_time)
    if attempt == 4:
        raise Exception("all attempts exceeded, couldn't get proxy")
    options = Options()
    options.headless = True
    proxy = Proxy({
         'proxyType': ProxyType.MANUAL,
         'httpProxy': my_proxy,
         'ftpProxy': my_proxy,
         'sslProxy': my_proxy,
         'noProxy': '' # set this value as desired
    })

    driver = webdriver.Firefox(proxy=proxy, options=options)    
    driver.maximize_window()
    return driver


def login(driver, link):
    driver.get(link)
    time.sleep(0.5)
    dog_check(driver)
    email_element = driver.find_elements("name", "email")
    pass_element = driver.find_elements("name", "password")
    if email_element and pass_element:
        email_element[0].send_keys("contact@expressmovingvanlines.com")
        pass_element[0].send_keys("ExpressMoving@the2021")
        driver.find_elements("tag name", "button")[0].click()
        time.sleep(2)


def get_opportunity(driver):
    time.sleep(3)
    success = False
    try:
        name = driver.find_elements("css selector", NAME_SELECTOR)
        navigate_through_button_menu(driver)            

        message_text = build_message(name)
        message = driver.find_element("name", "introduce_yourself_send_message")
        message.send_keys(message_text)       

        driver.find_element("css selector", SEND_BUTTON).click()
        logging.info(f"Answered at {datetime.now().time()}")
        success = True
    except Exception as e:
        quote_time = driver.find_elements("css selector", "body > yelp-react-root > div > div.messenger-container__09f24__qt8O4 > div > div.messenger_right__09f24__fndbc.border--left__09f24__Lt8WF.border-color--default__09f24__JbNoB > div > div > div.u-flex__09f24__rt07y.u-flex-column__09f24__m6LIn.u-flex-item__09f24__YuSEF.border-color--default__09f24__JbNoB > div.project-description-container__09f24__zySxi.u-flex-item__09f24__YuSEF.messenger-right.border-color--default__09f24__JbNoB > div > div > div.messages-grouped-by-time-view_group_time-sent__09f24__lCCiu.border-color--default__09f24__NPAKY > p")
        if quote_time:
            quote_time_string = f"Quote appeared at the time {quote_time[0]}"
        else:
            quote_time_string = ""
        logging.info(f"Opportunity has expired, no dialogue window found.{quote_time_string}")
    return success


def navigate_through_button_menu(driver):
    driver.find_element("css selector", OPTION_BUTTON).click()
    time.sleep(0.2)
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
    html = driver.find_elements("css selector", "html")[0].get_attribute("outerHTML")
    if "HTTP 504 - GATEWAY TIMEOUT" in html:
        driver.refresh()
        logging.info("HTTP 504 - GATEWAY TIMEOUT, refreshing..")

"""


def initialize_driver():
    profile = webdriver.FirefoxProfile()
    options = Options()
  #  options.headless = True
    options.add_argument("start-maximized")
#    options.add_experimental_option("excludeSwitches", ["enable-automation"])
  #  options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Firefox(profile, options=options)
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered']//th[contains(., 'IP Address')]"))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 2]")))]
    driver.quit()
    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])
   # print(proxies)
    pos = random.randint(0, len(proxies))
 #   for i in range(0, len(proxies)):
    try:
        print("Proxy selected: {}".format(proxies[pos]))
        my_proxy = proxies[pos]
      
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': my_proxy,
            'ftpProxy': my_proxy,
            'sslProxy': my_proxy,
            'noProxy': '' # set this value as desired
            })            
#      options = Options()
#      options.add_argument('--proxy-server={}'.format(proxies[i]))
        driver = webdriver.Firefox(proxy=proxy)
     #   break
 #     driver.get("https://www.whatismyip.com/proxy-check/?iref=home")
 #     if "Proxy Type" in WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))):
 #         break
    except Exception as e:
        print(e)
        driver.quit()
    print("Proxy Invoked")
  #  options.headless = True
   # ua = UserAgent()
 #   user_agent = ua.random
   # profile.set_preference("general.useragent.override", ua.random)    
   # profile.set_preference('permissions.default.stylesheet', 2)
   # profile.set_preference('permissions.default.image', 2)
  #  profile.set_preference('network.proxy.type', 1)
   # profile.set_preference('network.proxy.socks', '127.0.0.1')
   # profile.set_preference('network.proxy.socks_port', 9150)
 #   driver = webdriver.Firefox(profile, options=options)
    
    driver.maximize_window()
    return driver
"""