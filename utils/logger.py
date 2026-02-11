import logging
import os
from datetime import datetime

def get_logger(name):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(
            f"{log_dir}/{datetime.now().strftime('%Y%m%d')}.log"
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ))
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
        logger.addHandler(console)

    return logger