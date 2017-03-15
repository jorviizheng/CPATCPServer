#!/usr/bin/python
#coding=utf-8

import os
import sys
import requests

from thinkutils.common_utils.think_hashlib import *
from thinkutils.datetime.datetime import *
from thinkutils.log.log import *

logger = setup_custom_logger()

def do_post_test():
    payload = {'mobile': '13558575725'
        , 'imsi': '460009049043370'
        , "imei": "862162020352832"
        , "productCode": "P00500"
        , "apiKey": "3031"
        , "pipleId": "14833377425364214195175"
        , "extData": "P074565887"}

    r = requests.post("http://huina365.com/spfee/channel/getSms", data=payload)
    logger.info(r.text)

if __name__ == '__main__':
    # date time test
    logger.info("Test")
    logger.info("date: %d" % (get_timestamp()))
    logger.info(get_current_time_str())
    logger.info(timestamp2str(get_timestamp()))

    #
    logger.info(md5_str("123456"))
    logger.info(md5_file("main.py"))

    #do http post test
    do_post_test()