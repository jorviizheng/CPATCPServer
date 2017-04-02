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
import tornado.gen
import tornado.ioloop
import tornado.web
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
from CPATCPServer.CPATCPServer import *
from controller.broadcast import *

define('tcp_port', default=9001)
define('http_port', default=9000)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = Application([
    (r'/', MainHandler),
    (r'/broadcast', Broadcast),
])

def main():
    # http server
    http_server = HTTPServer(application)
    http_server.listen(options.http_port)

    # tcp server
    server = CPATCPServer()
    server.listen(options.tcp_port)
    g_logger.info('Server started...')

    # tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()