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

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_web_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    app = make_web_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()