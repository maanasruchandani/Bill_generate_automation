import pytest
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

class TestLogin:

    def test_login_success(self, driver, config):
        url      = config["OTM"]["url"]
        username = config["OTM"]["username"]
        password = config["OTM"]["password"]

        login_page = LoginPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        login_page.open(url)
        login_page.login(username, password)

        logger.info("Login submitted, awaiting post-login verification")
        # Post-login assertion will be added once you share the HTML after login