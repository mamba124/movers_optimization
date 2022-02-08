import time
import logging
import os
from datetime import datetime
from src.source_work import login, get_opportunity
from src.preprocess_driver import initialize_driver
from src.gmail_processor import get_unread_mails
from src.common import validate_launch_time
import traceback
import pandas as pd


start_time, end_time = validate_launch_time()


if __name__ == '__main__':
    auth = False
    driver = initialize_driver()
    while True:
        if datetime.now().hour >= start_time or datetime.now().hour <= end_time:
            try:
                scraped_links = get_unread_mails()
                if scraped_links:
                    for link in scraped_links:
                        if not auth:
                            driver.get(link)
                        else:
                            driver.execute_script(f'''window.open("{link}","_blank");''')
                        print(f"process link {link} at time {datetime.now().time()}")
                        while not auth:
                            auth = login(driver, link)
                    for handler in driver.window_handles:
                        driver.switch_to.window(handler)
                        success = get_opportunity(driver)
                        print(f"Successful? {success}") # TODO when I open a tab I must distinguish tabs and their success
                        logging.info(f"Successful? {success}")
                        if success:
                            now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")                      
                            driver.save_screenshot(f"screens/{now}.png")
                            if len(driver.window_handles) > 1:
                                driver.close()
                        
            except Exception as e:
                print(e)
                traceback.print_exc()
                if "cookies.pickle" in os.listdir():
                    os.remove("cookies.pickle")
                pass
            
        time.sleep(10)  
