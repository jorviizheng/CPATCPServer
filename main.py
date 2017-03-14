import os
import sys

from thinkutils.log.log import *
from thinkutils.datetime.datetime import *

logger = setup_custom_logger()

if __name__ == '__main__':
    # date time test
    logger.info("Test")
    logger.info("date: %d" % (get_timestamp()))
    logger.info(get_current_time_str())
    logger.info(timestamp2str(get_timestamp()))