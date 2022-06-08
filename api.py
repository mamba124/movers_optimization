import time
import logging
import os
from datetime import datetime
from src.source_work import login, get_opportunity, wait
from src.preprocess_driver import initialize_driver
from src.gmail_processor import get_unread_mails, create_message, send_message, build_service
from src.common import validate_launch_time, make_a_record, RecordClass
import traceback
import json

start_time, end_time = validate_launch_time()
current_date = str(datetime.now().date())
records = RecordClass()
records.date = current_date
#logs = {current_date: {}}

if __name__ == '__main__':
    auth = False
    logged = True
    driver = initialize_driver()
    old_counter = -1
    print("start bot")
    while True:
        if datetime.now().hour >= start_time or datetime.now().hour <= end_time:
            try:
                scraped_links = get_unread_mails()
                if scraped_links:
                    for link in scraped_links:
                        fresh_date = str(datetime.now().date())
                        if current_date != fresh_date:
                            current_date = fresh_date
                            records.date = current_date
                        if not auth:
                            driver.get(link)
                            counter = 0
                        else:
                            driver.execute_script(f'''window.open("{link}","_blank");''')
                            counter += 1
                        records.processed = str(datetime.now().time())
                        records.link = link
                        print(f"process link {link} at time {datetime.now().time()}")
                        while not auth:
                            auth = login(driver, link, logged)
                            logged = auth
                            if auth == False:
                                user="californiaexperessmail@gmail.com"
                                mail = create_message(to=user, message_text="Attention, DEAL WITH CAPTCHA")
                                service = build_service()
                                send_message(service, mail, user=user)                                       
                                time.sleep(5)
                    for index, handler in enumerate(driver.window_handles):
                        if index > old_counter:
                            driver.switch_to.window(handler)
                            try:
                                NAME_SELECTOR = "body > yelp-react-root > div:nth-child(1) > div.responsive.responsive-biz.border-color--default__09f24__NPAKY > div > div.biz-container-full-screen__09f24__fhNa6.border-color--default__09f24__NPAKY > div > div.responsive-biz.css-b95f0i.margin-b4__09f24__jfnOz.margin-sm-r0__09f24__WfNsG.margin-sm-b1__09f24__gvqD8.margin-md-r2__09f24__r7Qz5.border-color--default__09f24__NPAKY > div.css-s7x2v8.border-color--default__09f24__NPAKY > div.css-5739yy.border-color--default__09f24__NPAKY > div > div.css-0.padding-t3__09f24__TMrIW.padding-r3__09f24__eaF7p.padding-b3__09f24__S8R2d.padding-l3__09f24__IOjKY.border--top__09f24__exYYb.border--right__09f24__X7Tln.border--left__09f24__DMOkM.border-color--default__09f24__NPAKY > div > div > div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.border-color--default__09f24__NPAKY > div.user-passport-info.border-color--default__09f24__NPAKY > span > a"
                                print("wait name selector")
                                wait(driver, 15, NAME_SELECTOR)
                            except Exception as ex:
                                print(f"something happened")
                                print(str(ex))
                                continue
                            success, t1, t2 = get_opportunity(driver)
                            print(f"Successful? {success}") # TODO when I open a tab I must distinguish tabs and their success
                            driver.save_screenshot(f"screens/{t1}.png")
                            records.success = success
                            records.accessed = str(t1)
                            records.answered = str(t2)
                            make_a_record(index, records)
                            print(f"Accessed at {t1}")
                            print(f"Answered at {t2}")
                            now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")                      
                            if index >= 17:
                                raise Exception("Too many tabs")
                    old_counter = index
                        
            except Exception as e:
                print(e)
                if "Message: Failed to decode response from marionette" in str(e):
                    user="californiaexperessmail@gmail.com"
                    mail = create_message(to=user, message_text="Attention, something terrible happened with WebDriver! Please, restart bot manually")
                    service = build_service()
                    send_message(service, mail, user="californiaexperessmail@gmail.com")
                    raise Exception("No marionette for some reasons")
                if "Too many tabs" in str(e):
                    user="californiaexperessmail@gmail.com"
                    mail = create_message(to=user, message_text="Attention, Too many tabs on WebDriver. Bot restarts automatically..")
                    service = build_service()
                    send_message(service, mail, user="californiaexperessmail@gmail.com")
                    raise Exception("Too many tabs")                    
                traceback.print_exc()
                if "cookies.pickle" in os.listdir():
                    os.remove("cookies.pickle")
                pass
            
        time.sleep(10)
