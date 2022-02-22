import time
import logging
import os
from datetime import datetime
from src.source_work import login, get_opportunity
from src.preprocess_driver import initialize_driver
from src.gmail_processor import get_unread_mails, create_message, send_message, build_service
from src.common import validate_launch_time
import traceback
import json

start_time, end_time = validate_launch_time()
current_date = str(datetime.now().date())
logs = {current_date: {}}

if __name__ == '__main__':
    auth = False
    driver = initialize_driver()
    old_counter = -1
    while True:
        if datetime.now().hour >= start_time or datetime.now().hour <= end_time:
            try:
                scraped_links = get_unread_mails()
                if scraped_links:
                    for link in scraped_links:
                        fresh_date = str(datetime.now().date())
                        if current_date != fresh_date:
                            current_date = fresh_date
                            logs[current_date] = {}
                        if not auth:
                            driver.get(link)
                            counter = 0
                            logs[current_date][counter] = None
                        else:
                            driver.execute_script(f'''window.open("{link}","_blank");''')
                            counter += 1
                        logs[current_date][counter] = {}
                        logs[current_date][counter]["processed"] = str(datetime.now().time())
                        print(f"process link {link} at time {datetime.now().time()}")
                        while not auth:
                            auth = login(driver, link)
                    for index, handler in enumerate(driver.window_handles):
                        if index > old_counter:
                            driver.switch_to.window(handler)
                            time.sleep(6)
                            success, t1, t2 = get_opportunity(driver)
                            print(f"Successful? {success}") # TODO when I open a tab I must distinguish tabs and their success
                            logging.info(f"Successful? {success}")
                            logs[current_date][counter]['success'] = success
                            logs[current_date][counter]['accessed'] = str(t1)
                            logs[current_date][counter]['processed/quote qublished'] = str(t2)
                            with open("stats.json", 'w') as f:
                                json.dump(logs, f)
                            
                            #if success:
                            now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")                      
                            driver.save_screenshot(f"screens/{now}.png")
                    old_counter = index                                

                            #    if len(driver.window_handles) > 1:
                            #        driver.close()
                        
            except Exception as e:
                print(e)
                if "Message: Failed to decode response from marionette" in str(e):
                    user="californiaexperessmail@gmail.com"
                    mail = create_message(to=user, message_text="Attention, something terrible happened with WebDriver! Please, restart bot manually")
                    service = build_service()
                    send_message(service, mail, user="californiaexperessmail@gmail.com")
                traceback.print_exc()
                if "cookies.pickle" in os.listdir():
                    os.remove("cookies.pickle")
                pass
            
        time.sleep(10)  
