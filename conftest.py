import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск Firefox в headless-режиме",
    )


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("-headless")

    browser = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options,
    )
    browser.set_window_size(1920, 1080)

    yield browser
    browser.quit()
