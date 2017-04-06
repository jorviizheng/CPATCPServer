import os
import sys

import logging
import logging.handlers
from rainbow_logging_handler import RainbowLoggingHandler
from logging.handlers import TimedRotatingFileHandler


def setup_custom_logger():
    LOG_FILE = 'log/app.log'

    formatter = logging.Formatter("[%(asctime)s] %(pathname)s %(funcName)s():%(lineno)d  %(levelname)s \t%(message)s")  # same as default
    # formatter = logging.Formatter('%(asctime)s [%(pathname)s: %(lineno)d] %(levelname)s %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.formatter = formatter
    # logger.addHandler(console_handler)

    # setup `RainbowLoggingHandler`
    handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #Add file handler
    handler = TimedRotatingFileHandler(LOG_FILE,
                                       when="h",
                                       interval=1,
                                       backupCount=48)

    # try:
    #     raise RuntimeError("Opa!")
    # except Exception as e:
    #     logger.exception(e)

    return logger

g_logger = setup_custom_logger()
