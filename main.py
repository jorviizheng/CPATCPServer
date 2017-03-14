import os
import sys

from thinkutils.log.log import *
from thinkutils.datetime.datetime import *

logger = setup_custom_logger()

if __name__ == '__main__':
    logger.info("Test")
    logger.info("date: %d" % (get_timestamp()))