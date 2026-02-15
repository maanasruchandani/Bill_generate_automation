# OTM Automation

Selenium + Python automation for Oracle Transportation Management (OTM) using Page Object Model (POM).

---

## Project Structure

```
otm-automation/
├── config/
│   ├── config.ini               # URL, credentials, browser settings (gitignored)
│   ├── config.ini.example       # Template for config.ini
│   ├── domains.py               # Domain dictionary (OTM, MENLO + subdomains)
│   └── domain_locators.py       # Per-domain XPath locators and navigation paths
├── data/
│   ├── records.csv                      # Input: Bill and Sell IDs (manually updated)
│   └── Sell_status_update_auto.csv      # Auto-generated: Sell status upload file
├── drivers/
│   └── driver_factory.py        # WebDriver setup (Chrome/Firefox)
├── pages/
│   ├── base_page.py             # Common Selenium actions (click, type, iframe, window)
│   ├── login_page.py            # Login page object
│   ├── role_switch_page.py      # Domain/role switching
│   ├── bill_page.py             # Bill search + Create Credit Note
│   ├── sell_shipment_page.py    # Sell Shipment search + Generate Bill
│   └── upload_page.py           # XML/CSV upload via MRG Quick Links
├── tests/
│   ├── conftest.py              # Pytest fixtures + CLI options
│   └── test_bill_processing.py  # Main test: full end-to-end flow
├── utils/
│   ├── logger.py                # File + console logging
│   └── csv_handler.py           # CSV read + sell status CSV generation
├── requirements.txt
└── .gitignore
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/<your-username>/otm-automation.git
cd otm-automation
pip install -r requirements.txt
```

### 2. Create config.ini from template

```bash
cp config/config.ini.example config/config.ini
```

Edit `config/config.ini` with real credentials:

```ini
[OTM]
url = https://<otm-host>/GC3/glog.webserver.servlet.umt.Login
username = YOUR_USERNAME
password = YOUR_PASSWORD

[BROWSER]
browser = chrome
headless = false
implicit_wait = 10
explicit_wait = 20

[DOMAIN]
parent = OTM
subdomain_code = A032
```

### 3. Prepare records.csv

Edit `data/records.csv` with bill and/or sell IDs:

```csv
Bill,Sell
A032260125-0045,3208566130
A032260125-0095,3208566141
```

- Leave `Bill` column empty if only processing sells.
- Leave `Sell` column empty if only processing bills.

---

## Running Tests

### Full flow (bills + sells + upload)

```bash
pytest tests/test_bill_processing.py -v -s
```

### Skip sell status CSV upload

```bash
pytest tests/test_bill_processing.py -v -s --skip-upload
```

---

## What the Test Does

The test automatically detects what is present in `records.csv` and runs only the relevant steps:

### If Bill IDs present
1. Login to OTM
2. Switch domain (e.g. OTM.CIT -> OTM/A032.CIT)
3. Open Bill screen via Freight Pay Quick Links
4. For each Bill ID:
   - Enter Bill ID with "Same As" operator
   - Search and select bill checkbox
   - Actions -> Financials -> Bill -> Create Credit Note
   - Close popup, click New Query, repeat

### If Sell IDs present
1. Generate `Sell_status_update_auto.csv` with SHIPMENT_STATUS format
2. Open Upload screen via MRG Quick Links (skippable with `--skip-upload`)
3. Upload CSV, select command `uu`, click Run
4. Open Sell Shipments screen via Shipment Management
5. For each Sell ID:
   - Enter Sell ID with "Same As" operator
   - Search and select sell checkbox
   - Actions -> Financials -> Bill -> Generate Bill
   - Click Generate Bill(s) in popup, close popup
   - Click New Query, repeat

---

## Adding a New Domain

### 1. Add to `config/domains.py`

```python
DOMAINS = {
    "OTM": {
        "parent": "OTM.CIT",
        "subdomains": {
            "A032": "OTM/A032.CIT",
            "A052": "OTM/A052.CIT"   # add new subdomain here
        }
    },
    "MENLO": {
        "parent": "MENLO.CIT",
        "subdomains": {
            "A200": "MENLO/A200.CIT"
        }
    }
}
```

### 2. Add locators to `config/domain_locators.py`

```python
"MENLO/A200.CIT": {
    "locators": {
        "freight_pay_quick_links": "//a[...]",
        "bill_link": "//a[...]",
        ...
    },
    "paths": {
        "freight_pay_bill": ["freight_pay_quick_links", "bill_link"],
        ...
    }
}
```

### 3. Update `config/config.ini`

```ini
[DOMAIN]
parent = MENLO
subdomain_code = A200
```

---

## Key Design Decisions

| Decision | Reason |
|----------|--------|
| POM pattern | Reusable page objects across multiple tasks |
| Domain dictionary | Easy to add new domains/subdomains without changing test logic |
| Domain locator dictionary | Different domains can have different XPaths for same actions |
| CSV-driven | Test data managed externally, no code changes needed per run |
| iframe/window handling in BasePage | Centralised so all page objects inherit it |
| `--skip-upload` CLI flag | Flexibility to skip steps without changing code |

---

## Page Objects Reference

### BasePage
Common actions available to all page objects:
- `click(xpath)` - wait for clickable and click
- `type_text(xpath, text)` - clear and type
- `find(xpath)` - wait for presence
- `is_visible(xpath)` - returns True/False
- `switch_to_iframe(xpath)` - switch into iframe
- `switch_to_iframe_when_loaded(xpath)` - wait for `pageloaded` attribute before switching
- `switch_to_default_content()` - exit all iframes
- `switch_to_popup()` - switch to last opened window
- `switch_to_parent_window()` - switch to first/main window
- `switch_to_frame_by_name(name)` - switch by frame name attribute

### Key iframes in OTM
| iframe id | Purpose |
|-----------|---------|
| `topbar` | Contains role switch link |
| `sidebar` | Contains navigation menu (Freight Pay, MRG, Shipment Mgmt) |
| `actionFrame` | Actions overlay (Financials/Bill tree) |
| `mainBody` (frame) | Generate Bill popup content |

---

## Logs

Logs are saved to `logs/YYYYMMDD.log` and also printed to console during test run.

---

## Requirements

```
selenium==4.18.1
pytest==8.1.0
pytest-html==4.1.1
configparser==7.0.0
```

Chrome browser required. Selenium 4.6+ manages ChromeDriver automatically.