#!/usr/bin/python
#coding=utf-8

import os
import sys
import requests
import redis

from thinkutils.common_utils.think_hashlib import *
from thinkutils.datetime.datetime_utils import *
from thinkutils.log.log import *
from thinkutils.ffan.ffan import *
from thinkutils.redis.think_redis import *


def do_post_test():
    payload = {'mobile': '13558575725'
        , 'imsi': '460009049043370'
        , "imei": "862162020352832"
        , "productCode": "P00500"
        , "apiKey": "3031"
        , "pipleId": "14833377425364214195175"
        , "extData": "P074565887"}

    r = requests.post("http://huina365.com/spfee/channel/getSms", data=payload)
    g_logger.info(r.text)


def redis_demo():
    r = redis.StrictRedis(connection_pool=g_redis_pool)
    r.set("FXXK", get_current_time_str(), ex=30)

if __name__ == '__main__':
    # date time test
    g_logger.info("Test")
    g_logger.info("date: %d" % (get_timestamp()))
    g_logger.info(get_current_time_str())
    g_logger.info(timestamp2str(get_timestamp()))

    #
    g_logger.info(md5_str("123456"))
    g_logger.info(md5_file("main.py"))

    #do http post test
    # do_post_test()

    # load_page()

    #redis test
    redis_demo()