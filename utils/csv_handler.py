import csv
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