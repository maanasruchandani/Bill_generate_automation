DOMAIN_LOCATORS = {
    "OTM/A032.CIT": {
        "locators": {
            "freight_pay_quick_links": "//a[contains(text(), 'Freight Pay Quick Links')]",
            "bill_link": "//a[contains(@href, 'OTM.Z1_BILL_INVOICE') and @target='mainBody']",
            "mrg_quick_links": "//a[@id='Link5' and contains(text(), 'MRG Quick Links')]",
            "upload_csv_link": "//a[@id='Link5_5' and contains(text(), 'Upload an XML/CSV Transmission')]",
            "shipment_mgmt_root": "//a[@id='Link14' and contains(text(), 'Shipment Management')]",
            "shipment_mgmt_child": "//a[@id='Link14_0' and contains(text(), 'Shipment Management')]",
            "sell_shipments_link": "//a[@id='Link14_0_1' and contains(text(), 'Sell Shipments')]"
        },
        "paths": {
            "freight_pay_bill": ["freight_pay_quick_links", "bill_link"],
            "mrg_upload": ["mrg_quick_links", "upload_csv_link"],
            "sell_shipments": ["shipment_mgmt_root", "shipment_mgmt_child", "sell_shipments_link"]
        }
    }
}

def get_locator(domain, locator_name):
    return DOMAIN_LOCATORS[domain]["locators"][locator_name]

def get_path(domain, path_name):
    return DOMAIN_LOCATORS[domain]["paths"][path_name]