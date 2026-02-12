from pages.base_page import BasePage
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class RoleSwitchPage(BasePage):

    ROLE_SWITCH_LINK = "//a[@id='user_role_link']"
    LIST_BUTTON = "//a[@name='user_role/user_role_xid_clear']//img[@alt='List' and @title='List']"
    DOMAIN_RADIO_TEMPLATE = "//input[@type='radio' and @name='Selected' and @value='{}']"
    FINISH_BUTTON = "//a[@id='finished_button']"
    CHANGE_USER_ROLE_BUTTON = "//a[@class='enButton' and contains(@href, 'submitUserRole')]"
    MAIN_IFRAME = "//iframe[@id='topbar']"

    def click_role_switch_link(self):
        time.sleep(3)
        self.switch_to_iframe(self.MAIN_IFRAME)
        self.click(self.ROLE_SWITCH_LINK)
        logger.info("Clicked role switch link")
        self.switch_to_default_content()
        time.sleep(2)
        self.switch_to_popup()

    def click_list_button(self):
        self.click(self.LIST_BUTTON)
        logger.info("Clicked list button")
        time.sleep(2)
        self.switch_to_popup()

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        logger.info("Clicked Finish button")
        time.sleep(1)
        # Second popup closed, switch to first popup (window_handles[1])
        self.driver.switch_to.window(self.driver.window_handles[1])
        logger.info("Switched back to first popup")
        time.sleep(1)

    def click_change_user_role(self):
        self.click(self.CHANGE_USER_ROLE_BUTTON)
        logger.info("Clicked Change User Role button")
        self.switch_to_parent_window()
        time.sleep(3)

    def select_domain(self, domain_name):
        radio_xpath = self.DOMAIN_RADIO_TEMPLATE.format(domain_name)
        self.click(radio_xpath)
        logger.info(f"Selected domain: {domain_name}")

    def switch_to_domain(self, domain_name):
        self.click_role_switch_link()
        self.click_list_button()
        self.select_domain(domain_name)
        self.click_finish()
        self.click_change_user_role()
        logger.info(f"Role switched to: {domain_name}")

    def verify_domain_switched(self, expected_domain):
        time.sleep(3)
        self.switch_to_iframe(self.MAIN_IFRAME)
        actual_domain = self.get_text(self.ROLE_SWITCH_LINK)
        assert actual_domain == expected_domain, f"Expected {expected_domain}, got {actual_domain}"
        logger.info(f"Domain switch verified: {expected_domain}")
        self.switch_to_default_content()