import logging
import os
import sys
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
        
        formatter = logging.Formatter(
            f"%(asctime)s | [{worker_id}] | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_dir = Path("reports/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / f"test_run_{worker_id}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger