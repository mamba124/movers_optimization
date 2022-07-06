import os
import random
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

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
    RUNTIME = os.environ.get('RUNTIME', 'firefox')
    drivers_dict = {"remote_firefox": {"driver": webdriver.Firefox,
                                    "options": get_mozilla_options()
                                    },
                    "local_firefox": {"driver": webdriver.Firefox,
                                    "options": get_mozilla_options()
                                    },
                    "chrome": {"driver": webdriver.Chrome,
                               "options": get_chrome_options(),
                               },
                    "docker": {"driver": webdriver.Remote,
                               "options": get_chrome_options()}
                    }
    working_runtime = drivers_dict[RUNTIME]["driver"]
    if RUNTIME == 'docker':
        driver = working_runtime['driver']("http://selenium:4444", options=working_runtime['options'])
    elif RUNTIME == 'local_firefox':
        for attempt in range(5):
            sleep_time = 1.8 ** attempt
            my_proxy = generate_proxy()
            if my_proxy:
                break
            else:
                time.sleep(sleep_time)
        if attempt == 4:
            raise Exception("all attempts exceeded, couldn't get proxy")

        proxy = Proxy({
             'proxyType': ProxyType.MANUAL,
             'httpProxy': my_proxy,
             'ftpProxy': my_proxy,
             'sslProxy': my_proxy,
             'noProxy': '' # set this value as desired
        })        
        driver = working_runtime['driver'](options=working_runtime['options'], proxy=proxy)
    else:
        driver = working_runtime['driver'](options=working_runtime['options'])
    driver.maximize_window()
    return driver


#class LocalWebDriver:
#    _subdriver = webdriver.Firefox

#    def __init__(self, **kwargs):
#        self.headless = kwargs.get("headless", False)
#        self.options = kwargs.get("options")
    
#    def __new__(cls):
#        instance = super().__new__(cls)  # don't pass extra *args and **kwargs to obj.__new__
#        cls._subdriver = instance
#        return instance
        

def get_mozilla_options(headless=False):
    options = Options()
    options.headless = headless # in case YELP interface v4 headless mode for local webdriver generally doesn't work

    return options


def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return chrome_options    
    