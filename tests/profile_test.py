import unittest
import pytest
import logging
from tests.mocked_selenium import MockedDriver
from selenium_utils import dog_check, get_opportunity, build_message, login


class MockedObject:
    def __init__(self):
        self.text = "Karl"

dog_page = open("source_pages/dog.html").read()
general_page = open("source_pages/general_message_page.html").read()


def test_dog_check(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(dog_page)
        dog_check(driver)
        assert caplog.record_tuples[0][2] == "HTTP 504 - GATEWAY TIMEOUT, refreshing.."


def test_dog_check_invalid(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(general_page)
        dog_check(driver)
        assert caplog.record_tuples == []


def test_get_opportunity(caplog):
    with caplog.at_level(logging.INFO):
        driver = MockedDriver(general_page)
        success = get_opportunity(driver)
    assert "Answered" in caplog.record_tuples[0][2]
    assert success == True


@unittest.mock.patch("selenium_utils.navigate_through_button_menu", side_effect=AttributeError)
def test_get_opportunity_fail(failing_func):
    try:
        driver = MockedDriver(general_page)
        success = get_opportunity(driver)
    except AttributeError:
        assert success == False


def test_build_message():
    name = []
    assert build_message(name) == "Hi! Thank you for contacting California Express Movers."
    name = [MockedObject()]
    assert build_message(name) == "Hi, Karl! Thank you for contacting California Express Movers."


def test_login(capsys):
    driver = MockedDriver(general_page)
    login(driver, 'blabla.com')
    captured = capsys.readouterr()
    assert captured.out == 'sent keys\nsent keys\nclicked\n'
    