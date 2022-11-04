import logging
import os
from pathlib import Path

import coloredlogs

LOGS_DIR = f"{os.getcwd()}/logs"

logger = logging.getLogger("main")
logger_stream_handler = logging.StreamHandler()
main_logs_dir = Path(LOGS_DIR)
main_logs_dir.mkdir(exist_ok=True)
logger_file_handler = logging.FileHandler(main_logs_dir / "main.log")
LOGGING_FORMAT = "%(asctime)s - %(levelname)s: %(message)s [%(filename)s:%(lineno)d]"
logging_formatter = logging.Formatter(LOGGING_FORMAT)
logger_file_handler.setFormatter(logging_formatter)
logger.addHandler(logger_file_handler)
logger.addHandler(logger_stream_handler)
logger.setLevel(logging.DEBUG)

coloredlogs.install(level="DEBUG", logger=logger, fmt=LOGGING_FORMAT, milliseconds=False)
