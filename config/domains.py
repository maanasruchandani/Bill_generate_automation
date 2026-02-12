DOMAINS = {
    "OTM": {
        "parent": "OTM.CIT",
        "subdomains": {
            "A032": "OTM/A032.CIT",
            "A052": "OTM/A052.CIT"
        }
    },
    "MENLO": {
        "parent": "MENLO.CIT",
        "subdomains": {
            "A200": "MENLO/A200.CIT"
        }
    }
}

def get_domain(parent, subdomain_code):
    return DOMAINS[parent]["subdomains"][subdomain_code]