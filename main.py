from thinkutils.common_utils.think_hashlib import *
from thinkutils.datetime.datetime import *
from thinkutils.log.log import *

logger = setup_custom_logger()

if __name__ == '__main__':
    # date time test
    logger.info("Test")
    logger.info("date: %d" % (get_timestamp()))
    logger.info(get_current_time_str())
    logger.info(timestamp2str(get_timestamp()))

    #
    logger.info(md5_str("123456"))
    logger.info(md5_file("main.py"))