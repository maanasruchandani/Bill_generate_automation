from pages.base_page import BasePage
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class SellShipmentPage(BasePage):

    SIDEBAR_IFRAME = "//iframe[@id='sidebar']"

    SELL_ID_INPUT = "//input[@name='shipment/xid']"
    OPERATOR_DROPDOWN = "//select[@name='shipment/xid_operator']"
    SAME_AS_OPTION = "//option[@value='same']"
    SEARCH_BUTTON = "//a[@id='search_button']"

    SELL_CHECKBOX_TEMPLATE = "//input[@type='checkbox' and @name='Selected' and @value='{}']"
    RESULTS_CONTAINER = "//div[@id='rgSGContainer']"

    ACTIONS_BUTTON = "//a[contains(@onclick, 'loadFinderActionFrame')]"
    ACTIONS_IFRAME = "//iframe[@id='actionFrame']"

    FINANCIALS_NODE = "//span[contains(text(), 'Financials')]/..//img[@src='/images/themes/themesswanblue/tplus.gif']"
    BILL_NODE = "//span[contains(text(), 'Bill')]/..//img[@src='/images/themes/themesswanblue/tplus.gif']"
    GENERATE_BILL_ACTION = "//a[contains(@href, 'generate_customer_bill')]"

    POPUP_FRAME = "//frame[@name='mainBody']"
    GENERATE_BILL_BUTTON = "//a[@id='submit']"

    NEW_QUERY_BUTTON = "//a[contains(@href, 'newSearch()')]"

    def navigate_to_sell_shipments(self, root_locator, child_locator, sell_link_locator):
        self.switch_to_default_content()
        # Switch back to main tab (first window)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        self.switch_to_iframe(self.SIDEBAR_IFRAME)
        self.click(root_locator)
        time.sleep(1)
        self.click(child_locator)
        time.sleep(1)

        sell_element = self.find(sell_link_locator)
        sell_href = sell_element.get_attribute("href")
        self.driver.execute_script("window.open(arguments[0], '_blank');", sell_href)
        logger.info("Opened Sell Shipments in new tab via JS")
        time.sleep(2)

        self.switch_to_default_content()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info("Switched to Sell Shipments tab")
        time.sleep(2)

    def enter_sell_id(self, sell_id):
        self.switch_to_default_content()
        self.type_text(self.SELL_ID_INPUT, sell_id)
        logger.info(f"Entered Sell ID: {sell_id}")

    def select_same_as_operator(self):
        self.click(self.OPERATOR_DROPDOWN)
        self.click(self.SAME_AS_OPTION)
        logger.info("Selected 'Same As' operator")

    def click_search(self):
        self.click(self.SEARCH_BUTTON)
        logger.info("Clicked Search button")
        time.sleep(3)

    def select_sell_checkbox(self, domain, sell_id):
        self.find(self.RESULTS_CONTAINER)
        time.sleep(2)
        domain_prefix = domain.replace(".CIT", "")
        full_value = f"{domain_prefix}.{sell_id}"
        checkbox_xpath = self.SELL_CHECKBOX_TEMPLATE.format(full_value)
        self.click(checkbox_xpath)
        logger.info(f"Selected sell checkbox: {full_value}")

    def click_actions(self):
        self.click(self.ACTIONS_BUTTON)
        logger.info("Clicked Actions button")
        time.sleep(2)
        self.switch_to_iframe_when_loaded(self.ACTIONS_IFRAME)
        time.sleep(2)
        logger.info("Switched to actions iframe")

    def expand_financials(self):
        self.click(self.FINANCIALS_NODE)
        logger.info("Expanded Financials")
        time.sleep(1)

    def expand_bill_node(self):
        self.click(self.BILL_NODE)
        logger.info("Expanded Bill node")
        time.sleep(1)

    def click_generate_bill_action(self):
        self.click(self.GENERATE_BILL_ACTION)
        logger.info("Clicked Generate Bill action")
        time.sleep(3)
        self.switch_to_default_content()
        self.switch_to_popup()
        time.sleep(2)
        logger.info("Switched to Generate Bill popup")

    def click_generate_bill_button(self):
        self.switch_to_frame_by_name("mainBody")
        self.click(self.GENERATE_BILL_BUTTON)
        logger.info("Clicked Generate Bill(s) button")
        time.sleep(3)
        self.driver.close()
        logger.info("Closed Generate Bill popup")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def click_new_query(self):
        self.switch_to_default_content()
        self.click(self.NEW_QUERY_BUTTON)
        logger.info("Clicked New Query")
        time.sleep(2)

    def process_sell(self, domain, sell_id):
        self.enter_sell_id(sell_id)
        self.select_same_as_operator()
        self.click_search()
        self.select_sell_checkbox(domain, sell_id)
        self.click_actions()
        self.expand_financials()
        self.expand_bill_node()
        self.click_generate_bill_action()
        self.click_generate_bill_button()
        self.click_new_query()