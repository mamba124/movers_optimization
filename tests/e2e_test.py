from datetime import datetime
from unittest.mock import patch
from src.source_work import login, get_opportunity
import time
import random
from tests.mocked_selenium import MockedDriver

general_page = open("tests/test_files/general_message_page.html").read()

driver = MockedDriver(general_page)

@patch("src.source_work.login", side_effect=time.sleep(random.randint(10, 15)))
def test_multiple_requests(mocked_login, capsys):
    scraped_links = ['link1', 'link2']
    for link in scraped_links:
        print(f"process link {link} at time {datetime.now().time()}")
        login(driver, link)
        now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        success, _, _ = get_opportunity(driver)
        print(f"Successful? {success}")


