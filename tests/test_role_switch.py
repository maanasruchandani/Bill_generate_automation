from pages.login_page import LoginPage
from pages.role_switch_page import RoleSwitchPage
from config.domains import get_domain
from utils.logger import get_logger
import time

logger = get_logger(__name__)


class TestRoleSwitch:

    def test_domain_switch(self, driver, config):
        url = config["OTM"]["url"]
        username = config["OTM"]["username"]
        password = config["OTM"]["password"]

        parent = config["DOMAIN"]["parent"]
        subdomain_code = config["DOMAIN"]["subdomain_code"]
        target_domain = get_domain(parent, subdomain_code)

        login_page = LoginPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        login_page.open(url)
        login_page.login(username, password)
        time.sleep(5)
        logger.info("Login completed")

        role_switch = RoleSwitchPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        role_switch.switch_to_domain(target_domain)
        role_switch.verify_domain_switched(target_domain)