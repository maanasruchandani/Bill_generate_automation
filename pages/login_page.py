from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):

    # Locators
    USERNAME_INPUT = "//input[@name='username']"
    PASSWORD_INPUT = "//input[@name='userpassword']"
    LOGIN_BUTTON   = "//input[@name='submitbutton' and @type='submit']"

    def open(self, url):
        self.navigate_to(url)
        logger.info("Login page opened")

    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        logger.info("Login button clicked")

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()