from reader import get_unread_mails
from selenium_utils import initialize_driver, login, get_opportunity
import time
import os
from datetime import datetime


if __name__ == '__main__':
    driver = initialize_driver()
   # time.sleep(60*30)
    while True:
        if datetime.now().hour >= 15 or datetime.now().hour <= 10:
            try:
                scraped_links = get_unread_mails()
                if scraped_links:
                    for link in scraped_links:
                        print(f"process link {link} at time {datetime.now().time()}")
                        login(driver, link)
                        time.sleep(3)
                        now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                        get_opportunity(driver)
                        driver.save_screenshot(f"screens/{now}.png")
            except Exception as e:
                print(e)
                pass
        time.sleep(10)  
        #     os.remove('cookies.pkl')