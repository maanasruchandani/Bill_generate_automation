from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    def __init__(self, driver, explicit_wait=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, explicit_wait)

    def find(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def click(self, xpath):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        logger.info(f"Clicked: {xpath}")

    def type_text(self, xpath, text):
        element = self.find(xpath)
        element.clear()
        element.send_keys(text)
        logger.info(f"Typed into: {xpath}")

    def get_text(self, xpath):
        return self.find(xpath).text

    def is_visible(self, xpath):
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False

    def navigate_to(self, url):
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")

    def switch_to_iframe(self, xpath):
        iframe = self.find(xpath)
        self.driver.switch_to.frame(iframe)
        logger.info(f"Switched to iframe: {xpath}")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        logger.info("Switched back to main content")

    def switch_to_popup(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Switched to popup window")

    def switch_to_parent_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        logger.info("Switched to parent window")

    def switch_to_iframe_when_loaded(self, xpath):
        iframe = self.find(xpath)
        self.wait.until(lambda d: iframe.get_attribute("pageloaded") != "false")
        self.driver.switch_to.frame(iframe)
        logger.info(f"Switched to loaded iframe: {xpath}")

    def switch_to_frame_by_name(self, name):
        self.driver.switch_to.frame(name)
        logger.info(f"Switched to frame by name: {name}")