from pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from utils.logger import get_logger
import time

logger = get_logger(__name__)


class BillPage(BasePage):
    SIDEBAR_IFRAME = "//iframe[@id='sidebar']"
    MAIN_BODY_IFRAME = "//iframe[@id='mainBody']"

    BILL_ID_INPUT = "//input[@name='invoice/invoice_xid']"
    OPERATOR_DROPDOWN = "//select[@name='invoice/invoice_xid_operator']"
    SAME_AS_OPTION = "//option[@value='same']"
    SEARCH_BUTTON = "//a[@id='search_button']"

    BILL_CHECKBOX_TEMPLATE = "//input[@type='checkbox' and @name='Selected' and @value='{}']"
    ACTIONS_BUTTON = "//a[contains(@onclick, 'loadFinderActionFrame')]"

    FINANCIALS_NODE = "//span[contains(text(), 'Financials')]/..//img[@src='/images/themes/themesswanblue/tplus.gif']"
    BILL_NODE = "//span[contains(text(), 'Bill')]/..//img[@src='/images/themes/themesswanblue/tplus.gif']"
    CREATE_CREDIT_NOTE = "//a[contains(@href, 'CreateCredit_note') or contains(text(), 'Create Credit Note')]"

    NEW_QUERY_BUTTON = "//a[@class='enButton' and contains(@href, 'newSearch()')]"

    RESULTS_CONTAINER = "//div[@id='rgSGContainer']"
    ACTIONS_IFRAME = "//iframe[@id='actionFrame']"

    def navigate_to_bill_via_menu(self, domain, freight_pay_locator, bill_locator):
        self.switch_to_iframe(self.SIDEBAR_IFRAME)
        self.click(freight_pay_locator)
        time.sleep(1)

        bill_element = self.find(bill_locator)
        bill_href = bill_element.get_attribute("href")
        logger.info(f"Bill link href: {bill_href}")

        self.driver.execute_script("window.open(arguments[0], '_blank');", bill_href)
        logger.info("Opened Bill in new tab via JS")
        time.sleep(2)

        self.switch_to_default_content()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Switched to new Bill tab")
        time.sleep(2)

    def enter_bill_id(self, bill_id):
        self.switch_to_default_content()
        self.type_text(self.BILL_ID_INPUT, bill_id)
        logger.info(f"Entered Bill ID: {bill_id}")

    def select_same_as_operator(self):
        self.click(self.OPERATOR_DROPDOWN)
        self.click(self.SAME_AS_OPTION)
        logger.info("Selected 'Same As' operator")

    def click_search(self):
        self.click(self.SEARCH_BUTTON)
        logger.info("Clicked Search button")
        time.sleep(3)

    def click_new_query(self):
        self.click(self.NEW_QUERY_BUTTON)
        logger.info("Clicked New Query")
        time.sleep(2)

    def select_bill_checkbox(self, domain, bill_id):
        # Wait for results container to be visible
        self.find(self.RESULTS_CONTAINER)
        time.sleep(2)
        domain_prefix = domain.replace(".CIT", "")
        full_value = f"{domain_prefix}.{bill_id}"
        checkbox_xpath = self.BILL_CHECKBOX_TEMPLATE.format(full_value)
        self.click(checkbox_xpath)
        logger.info(f"Selected bill checkbox: {full_value}")

    def click_actions(self):
        self.click(self.ACTIONS_BUTTON)
        logger.info("Clicked Actions button")
        time.sleep(3)
        logger.info("Switched to actions iframe")

    def expand_financials(self):
        self.switch_to_iframe_when_loaded(self.ACTIONS_IFRAME)
        self.click(self.FINANCIALS_NODE)
        logger.info("Expanded Financials")
        time.sleep(1)

    def expand_bill_node(self):
        self.click(self.BILL_NODE)
        logger.info("Expanded Bill node")
        time.sleep(1)

    def click_create_credit_note(self):
        self.click(self.CREATE_CREDIT_NOTE)
        logger.info("Clicked Create Credit Note")
        time.sleep(3)
        self.switch_to_default_content()
        self.switch_to_popup()
        time.sleep(2)
        self.driver.close()
        logger.info("Closed credit note popup")
        self.driver.switch_to.window(self.driver.window_handles[-1])


    def process_bill(self, domain, bill_id):
        self.enter_bill_id(bill_id)
        self.select_same_as_operator()
        self.click_search()
        self.select_bill_checkbox(domain, bill_id)
        self.click_actions()
        self.expand_financials()
        self.expand_bill_node()
        self.click_create_credit_note()
        self.click_new_query()