from pages.login_page import LoginPage
from pages.role_switch_page import RoleSwitchPage
from pages.bill_page import BillPage
from pages.sell_shipment_page import SellShipmentPage
from pages.upload_page import UploadPage
from config.domains import get_domain
from config.domain_locators import get_locator
from utils.csv_handler import CSVHandler
from utils.logger import get_logger
import time

logger = get_logger(__name__)

class TestBillProcessing:

    def test_process_records_from_csv(self, driver, config, run_options):
        url = config["OTM"]["url"]
        username = config["OTM"]["username"]
        password = config["OTM"]["password"]

        parent = config["DOMAIN"]["parent"]
        subdomain_code = config["DOMAIN"]["subdomain_code"]
        target_domain = get_domain(parent, subdomain_code)
        domain_prefix = target_domain.replace(".CIT", "")

        # Login
        login_page = LoginPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        login_page.open(url)
        login_page.login(username, password)
        time.sleep(5)

        # Switch domain
        role_switch = RoleSwitchPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
        role_switch.switch_to_domain(target_domain)
        role_switch.verify_domain_switched(target_domain)

        # Load CSV
        csv_handler = CSVHandler("data/records.csv")
        all_records = csv_handler.get_all_records()

        bill_ids = [r['Bill'] for r in all_records if r.get('Bill', '').strip()]
        sell_ids = [r['Sell'] for r in all_records if r.get('Sell', '').strip()]

        has_bills = len(bill_ids) > 0
        has_sells = len(sell_ids) > 0

        logger.info(f"Bills to process: {bill_ids}")
        logger.info(f"Sells to process: {sell_ids}")

        # CREDIT NOTE - only if bill ids present
        if has_bills:
            bill_page = BillPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
            freight_pay_locator = get_locator(target_domain, "freight_pay_quick_links")
            bill_locator = get_locator(target_domain, "bill_link")
            bill_page.navigate_to_bill_via_menu(target_domain, freight_pay_locator, bill_locator)

            for bill_id in bill_ids:
                logger.info(f"Processing Bill ID: {bill_id}")
                bill_page.process_bill(target_domain, bill_id)
                logger.info(f"Completed Bill ID: {bill_id}")

        # SELL STATUS CSV + UPLOAD - only if sell ids present
        if has_sells and not run_options["skip_upload"]:
            csv_path = csv_handler.generate_sell_status_csv(domain=domain_prefix)
            upload_page = UploadPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
            mrg_locator = get_locator(target_domain, "mrg_quick_links")
            upload_locator = get_locator(target_domain, "upload_csv_link")
            upload_page.navigate_to_upload_via_menu(mrg_locator, upload_locator)
            upload_page.process_upload(csv_path, command="uu")

        # GENERATE BILL FOR SELLS - only if sell ids present
        if has_sells:
            sell_page = SellShipmentPage(driver, explicit_wait=int(config["BROWSER"]["explicit_wait"]))
            root_locator = get_locator(target_domain, "shipment_mgmt_root")
            child_locator = get_locator(target_domain, "shipment_mgmt_child")
            sell_link_locator = get_locator(target_domain, "sell_shipments_link")
            sell_page.navigate_to_sell_shipments(root_locator, child_locator, sell_link_locator)

            for sell_id in sell_ids:
                logger.info(f"Processing Sell ID: {sell_id}")
                sell_page.process_sell(target_domain, sell_id)
                logger.info(f"Completed Sell ID: {sell_id}")

        logger.info("All records processed successfully")