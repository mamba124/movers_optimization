from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pickle 
import os
import random
import time
from datetime import datetime 


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


def login(driver, link):
   # login_link = "https://biz.yelp.com"
   # link = "https://biz.yelp.com/messaging/gGbHoiu9Q9WUQcNbWf1qUg/opportunity?ytl_=23242dbf2558902f1e665b272034dbfc&utm_medium=email&utm_source=nearby_jobs_new_job_email&utm_campaign=Dec-03-2021"
  #  driver.get(link)
    first_time = not os.path.exists("cookies.pkl")
    if first_time:
        driver.get(link)
        email_element = driver.find_elements("name", "email")
        pass_element = driver.find_elements("name", "password")
        if email_element and pass_element:
            email_element[0].send_keys("contact@expressmovingvanlines.com")
            pass_element[0].send_keys("ExpressMoving@the2021")
            driver.find_elements("tag name", "button")[0].click()
            time.sleep(3)
         #   pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
   # else:
   #     cookies = pickle.load(open("cookies.pkl", "rb"))
    #    for cookie in cookies:
    #        driver.add_cookie(cookie)
    #    driver.get(link)

def get_opportunity(driver):
    cross_selector = ".dismiss-link__09f24__Q1RVn"
    notification_selector = ".close-button__09f24__qgCyrs"
 #   message = driver.find_elements("name", "message")
    time.sleep(3)
    try:
        name = driver.find_elements("css selector", "body > yelp-react-root > div:nth-child(1) > div.messenger-container__09f24__qt8O4 > div > div.messenger_right__09f24__fndbc.border--left__09f24__Lt8WF.border-color--default__09f24__JbNoB > div > div > div.u-flex__09f24__rt07y.u-flex-column__09f24__m6LIn.u-flex-item__09f24__YuSEF.border-color--default__09f24__JbNoB > div.messenger_right_top__09f24__ZxW58.u-padding-t3.u-padding-b3.border--bottom__09f24__Yl28T.border-color--default__09f24__JbNoB > div > div > div > div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.border-color--default__09f24__NPAKY > div.user-passport-info.border-color--default__09f24__NPAKY > span > a")
        time.sleep(1)
        click = ""
        option = driver.find_element("css selector", "div.margin-r3__09f24__ppHm0:nth-child(2) > button").click()
      #  if not option:
      #      option = driver.find_elements("css selector", "body > yelp-react-root > div:nth-child(1) > div.messenger-container__09f24__qt8O4 > div.messenger__09f24__VxY3p > div.u-flex__09f24__rt07y.u-flex-item__09f24__YuSEF > div > div:nth-child(6) > div > div.border-color--default__09f24__JbNoB.nowrap__09f24__VI7tZ.text-align--center__09f24__kjgPr > div:nth-child(2) > button > div").click()
            
        time.sleep(1)
     #   button = driver.find_element("css selector", "#modal-portal-container > div:nth-child(2) > div > div > div").click()
        next_button = "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(2) > div > button" 
        radio_button = "#how_do_you_want_to_get_more_information--3"
        driver.find_element("css selector", radio_button).click()
        is_next = driver.find_elements("css selector", next_button)
        if is_next:
            is_next[0].click()
        #  if button:
      #      button = driver.find_elements("css selector", "#modal-portal-container > div:nth-child(4) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div:nth-child(1) > div.question-section__09f24__iG3Xq.border-color--default__09f24__JbNoB.overflow--scrolly__09f24__Lssc1 > div:nth-child(2) > div > fieldset > ul > li:nth-child(4) > label > div > div.arrange-unit__09f24__Y0G49.arrange-unit-fill__09f24__wqOS8.border-color--default__09f24__JbNoB > div > span")
        
        time.sleep(1)
        message = driver.find_element("name", "introduce_yourself_send_message")
        time.sleep(0.5)
        if name:
            message.send_keys(f"Hi, {name[0].text}!")
            print("answered", datetime.now().time())
        else:
            message.send_keys("Hi!")
            print("answered", datetime.now().time())
        driver.find_element("css selector", "#modal-portal-container > div:nth-child(2) > div > div > div > div > div.border-color--default__09f24__JbNoB > div > div > div.padding-t4__09f24__Y6aGL.padding-r4__09f24__PQlH_.padding-b4__09f24__q6U6q.padding-l4__09f24__XrHdl.border-color--default__09f24__NPAKY.text-align--left__09f24__ju_Ri > div > div:nth-child(3) > button").click()
    except Exception as e:
        time.sleep(10)
        print(e)
      #  driver.get("https://business.yelp.com/")
    return "I'm back"