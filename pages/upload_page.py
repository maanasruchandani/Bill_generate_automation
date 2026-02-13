from pages.base_page import BasePage
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class UploadPage(BasePage):

    SIDEBAR_IFRAME = "//iframe[@id='sidebar']"

    FILE_INPUT = "//input[@id='file' and @type='file']"
    UPLOAD_BUTTON = "//a[@id='upload_button']"
    COMMAND_DROPDOWN = "//select[@name='command']"
    RUN_BUTTON = "//a[@id='run_button']"

    def navigate_to_upload_via_menu(self, mrg_locator, upload_locator):
        self.switch_to_default_content()
        # Switch back to main tab (first window)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        self.switch_to_iframe(self.SIDEBAR_IFRAME)
        self.click(mrg_locator)
        time.sleep(1)

        upload_element = self.find(upload_locator)
        upload_href = upload_element.get_attribute("href")
        self.driver.execute_script("window.open(arguments[0], '_blank');", upload_href)
        logger.info("Opened Upload page in new tab via JS")
        time.sleep(2)

        self.switch_to_default_content()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Switched to upload tab")
        time.sleep(2)

    def upload_file(self, file_path):
        file_input = self.find(self.FILE_INPUT)
        file_input.send_keys(file_path)
        logger.info(f"File selected: {file_path}")
        time.sleep(1)
        self.click(self.UPLOAD_BUTTON)
        logger.info("Clicked Upload button")
        time.sleep(3)

    def select_command(self, command="uu"):
        self.click(self.COMMAND_DROPDOWN)
        self.find(f"//select[@name='command']/option[text()='{command}']")
        self.driver.find_element(
            "xpath", f"//select[@name='command']/option[text()='{command}']"
        ).click()
        logger.info(f"Selected command: {command}")

    def click_run(self):
        self.click(self.RUN_BUTTON)
        logger.info("Clicked Run button")
        time.sleep(5)

    def process_upload(self, file_path, command="uu"):
        self.upload_file(file_path)
        self.select_command(command)
        self.click_run()