import unittest
import logging
from tests.mocked_selenium import MockedDriver, MockedDriverInstance
from unittest.mock import patch
from src import source_work

class MockedObject:
    def __init__(self, text="Karl"):
        self.text = text

dog_page = open("tests/test_files/dog.html").read()
general_page = open("tests/test_files/general_message_page.html").read()
main_page = open("tests/test_files/main_page.html").read()


@patch('src.source_work.wait')
def test_dog_check(mocked_wait, caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(dog_page)
        source_work.dog_check(driver) 
        assert caplog.record_tuples[0][2] == "HTTP 504 - GATEWAY TIMEOUT, refreshing.."

#TODO Debug new dogcheck

@patch("src.source_work.send_message", return_value=("9", True))
@patch("src.source_work.navigate_through_button_menu")
@patch("src.source_work.process_main_buttons")
@patch('src.source_work.wait')
def test_get_opportunity(mocked_wait, mocked_process, mocked_navigate, mocked_send, caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(general_page)
        success, _, _ = source_work.get_opportunity(driver)
    assert success == True


@patch("src.source_work.process_main_buttons", side_effect=Exception)
@patch('src.source_work.wait')
def test_get_opportunity_fail(mocked_wait, mocked_process):
    try:
        driver = MockedDriver(general_page)
        success, _, _ = source_work.get_opportunity(driver)
    except AttributeError:
        assert success == False


def test_build_message():
    name = []
    assert source_work.build_message(name) == "Hi! Thank you for contacting California Express Movers."
    name = [MockedObject()]
    assert source_work.build_message(name) == "Hi, Karl! Thank you for contacting California Express Movers."


def test_build_bad_message(capsys):
    quote_time = [MockedObject(" : 12/05/2022")]
    source_work.build_bad_message(quote_time)
    captured = capsys.readouterr()
    
    assert captured.out == "Opportunity has expired, no dialogue window found.Quote appeared at the time 12/05/2022\n"


@patch('src.source_work.dog_check')
@patch('src.source_work.wait')
def test_login_captcha(mocked_wait, mocked_dog):
    driver = MockedDriver(main_page)
    logged = source_work.login(driver, 'bla.com')
    
    assert logged == False