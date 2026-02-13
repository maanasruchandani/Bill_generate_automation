import csv
import os
from utils.logger import get_logger

logger = get_logger(__name__)

class CSVHandler:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.records = []
        self.load_records()

    def load_records(self):
        with open(self.csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            self.records = [{k.strip(): v.strip() for k, v in row.items()} for row in reader]
            logger.info(f"CSV Headers found: {list(self.records[0].keys()) if self.records else 'No records'}")
        logger.info(f"Loaded {len(self.records)} records from {self.csv_path}")

    def get_bill_ids(self):
        return [record['Bill'] for record in self.records]

    def get_all_records(self):
        return self.records

    def generate_sell_status_csv(self, domain, output_path="data/Sell_status_update_auto.csv"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sell_ids = [record['Sell'] for record in self.records if record.get('Sell', '').strip()]

        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['SHIPMENT_STATUS'])
            writer.writerow(['SHIPMENT_GID', 'STATUS_TYPE_GID', 'STATUS_VALUE_GID', 'DOMAIN_NAME'])
            for sell_id in sell_ids:
                writer.writerow([
                    f"{domain}.{sell_id}",
                    f"{domain}.REVIEWED_SELL",
                    f"{domain}.REVIEWED_SELL_REVIEWED",
                    domain
                ])

        logger.info(f"Generated sell status CSV at: {output_path}")
        return os.path.abspath(output_path)