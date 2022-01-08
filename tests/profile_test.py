import unittest
import pytest
import logging
from tests.mocked_selenium import MockedDriver
from selenium_utils import dog_check, get_opportunity


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
        get_opportunity(driver)
    assert "Answered" in caplog.record_tuples[0][2]