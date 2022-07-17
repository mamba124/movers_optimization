from src.preprocess_driver import get_chrome_options, get_mozilla_options, get_runtime
from selenium import webdriver


def test_get_working_runtime():
    firefox = webdriver.Firefox
    chrome = webdriver.Chrome
    docker = webdriver.Remote

    assert get_runtime("chrome")["driver"] == chrome

    assert get_runtime("docker")["driver"] == docker

    assert get_runtime("local_firefox")["driver"] == firefox
    
    assert get_runtime("remote_firefox")["driver"] == firefox


def test_get_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    assert get_chrome_options().__class__ == chrome_options.__class__


def test_get_mozille_options():
    assert get_mozilla_options().headless == False
    
    assert get_mozilla_options(True).headless == True
