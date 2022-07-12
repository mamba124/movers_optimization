import unittest
import logging
from tests.mocked_selenium import MockedDriver
from src import source_work

class MockedObject:
    def __init__(self, text="Karl"):
        self.text = text

dog_page = open("tests/test_files/dog.html").read()
general_page = open("tests/test_files/general_message_page.html").read()


def test_dog_check(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(dog_page)
        source_work.dog_check(driver) 
        assert caplog.record_tuples[0][2] == "HTTP 504 - GATEWAY TIMEOUT, refreshing.."


def test_dog_check_invalid(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(general_page)
        source_work.dog_check(driver)
        assert caplog.record_tuples == []


def test_get_opportunity(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(general_page)
        success, _, _ = source_work.get_opportunity(driver)
    assert "Answered" in caplog.record_tuples[0][2]
    assert success == True


@unittest.mock.patch("src.source_work.navigate_through_button_menu", side_effect=AttributeError)
def test_get_opportunity_fail(failing_func):
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


def test_login(capsys):
    driver = MockedDriver(general_page)
    source_work.login(driver, 'blabla.com')
    captured = capsys.readouterr()
    assert captured.out == 'sent keys\nsent keys\nclicked\n'


def test_build_bad_message(capsys):
    quote_time = [MockedObject(" : 12/05/2022")]
    source_work.build_bad_message(quote_time)
    captured = capsys.readouterr()
    
    assert captured.out == "Opportunity has expired, no dialogue window found.Quote appeared at the time 12/05/2022\n"