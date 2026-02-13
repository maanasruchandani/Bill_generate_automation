import pytest
import configparser
from drivers.driver_factory import get_driver

@pytest.fixture(scope="session")
def config():
    cfg = configparser.ConfigParser()
    cfg.read("config/config.ini")
    return cfg

@pytest.fixture(scope="function")
def driver(config):
    browser = config["BROWSER"]["browser"]
    headless = config["BROWSER"].getboolean("headless")
    implicit_wait = int(config["BROWSER"]["implicit_wait"])

    d = get_driver(browser=browser, headless=headless)
    d.implicitly_wait(implicit_wait)
    yield d
    d.quit()

def pytest_addoption(parser):
    parser.addoption("--skip-upload", action="store_true", default=False,
                     help="Skip sell status CSV upload step")

@pytest.fixture(scope="session")
def run_options(request):
    return {
        "skip_upload": request.config.getoption("--skip-upload")
    }