import os
import sys

import logging
import logging.handlers

def setup_custom_logger():
    LOG_FILE = 'app.log'

    formatter = logging.Formatter('%(asctime)s [%(pathname)s: %(lineno)d] %(levelname)s %(message)s')

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
