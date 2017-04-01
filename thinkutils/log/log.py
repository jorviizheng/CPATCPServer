import os
import sys

import logging
import logging.handlers
from rainbow_logging_handler import RainbowLoggingHandler

def setup_custom_logger():
    LOG_FILE = 'app.log'

    formatter = logging.Formatter("[%(asctime)s] %(name)s %(funcName)s():%(lineno)d  %(levelname)s \t%(message)s")  # same as default
    # formatter = logging.Formatter('%(asctime)s [%(pathname)s: %(lineno)d] %(levelname)s %(message)s')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)
    return logger

g_logger = setup_custom_logger()
