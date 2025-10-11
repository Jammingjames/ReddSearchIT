import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        "bot.log", maxBytes=2_000_000, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        encoding='utf-8'
    )

    logging.info("Logging initialized successfully")
