"""
Centralized Logging Utility for Energy Prediction & Optimization System.
Configures console output and rotating file log handlers.
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from src.config.config import LOGS_DIR

LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "campus_energy.log"

def setup_logger(name: str = "campus_energy") -> logging.Logger:
    """
    Initializes and returns a configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Rotating File Handler (10MB per file, max 5 backup files)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger("campus_energy")
