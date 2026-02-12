from pages.login_page import LoginPage
from pages.role_switch_page import RoleSwitchPage
from pages.bill_page import BillPage
from config.domains import get_domain
from config.domain_locators import get_locator
from utils.csv_handler import CSVHandler
from utils.logger import get_logger
import time

logger = get_logger(__name__)


class TestBillProcessing:

    def test_process_bills_from_csv(self, driver, config):
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

        role_switch = RoleSwitchPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        role_switch.switch_to_domain(target_domain)
        role_switch.verify_domain_switched(target_domain)

        bill_page = BillPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))

        freight_pay_locator = get_locator(target_domain, "freight_pay_quick_links")
        bill_locator = get_locator(target_domain, "bill_link")

        bill_page.navigate_to_bill_via_menu(target_domain, freight_pay_locator, bill_locator)

        csv_handler = CSVHandler("data/records.csv")
        bill_ids = csv_handler.get_bill_ids()

        for bill_id in bill_ids:
            logger.info(f"Processing Bill ID: {bill_id}")
            bill_page.process_bill(target_domain, bill_id)
            logger.info(f"Completed Bill ID: {bill_id}")

        logger.info("All bills processed successfully")