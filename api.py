import time
import logging
from datetime import datetime
from src.source_work import login, get_opportunity
from src.preprocess_driver import initialize_driver
from src.gmail_processor import get_unread_mails
from src.common import validate_launch_time


start_time, end_time = validate_launch_time()

if __name__ == '__main__':
    driver = initialize_driver()
    while True:
        if datetime.now().hour >= start_time or datetime.now().hour <= end_time:
            try:
                scraped_links = get_unread_mails()
                if scraped_links:
                    for link in scraped_links:
                        print(f"process link {link} at time {datetime.now().time()}")
                        login(driver, link)
                        now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                        success = get_opportunity(driver)
                        print(f"Successful? {success}")
                        logging.info(f"Successful? {success}")
                        driver.save_screenshot(f"screens/{now}.png")
            except Exception as e:
                print(e)
                pass
        time.sleep(10)  
