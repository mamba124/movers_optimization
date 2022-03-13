from selenium import webdriver

#CROSS_SELECTOR = ".dismiss-link__09f24__Q1RVn"
#NOTIFICATION_SELECTOR = ".close-button__09f24__qgCyrs"



def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    return driver
