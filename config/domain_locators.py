DOMAIN_LOCATORS = {
    "OTM/A032.CIT": {
        "locators": {
            "freight_pay_quick_links": "//a[contains(text(), 'Freight Pay Quick Links')]",
            "bill_link": "//a[contains(@href, 'OTM.Z1_BILL_INVOICE') and @target='mainBody']"
        },
        "paths": {
            "freight_pay_bill": ["freight_pay_quick_links", "bill_link"]
        }
    }
}

def get_locator(domain, locator_name):
    return DOMAIN_LOCATORS[domain]["locators"][locator_name]

def get_path(domain, path_name):
    return DOMAIN_LOCATORS[domain]["paths"][path_name]