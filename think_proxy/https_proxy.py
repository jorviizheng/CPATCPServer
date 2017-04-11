#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
https tunnel for cpa
when receive a connect from client
start a tunnel from client to remote device
"""

import sys
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
from thinkutils.log.log import *
from utils import decrypt, encrypt
from copy import deepcopy
import base64
from CPATCPServer.CPATCPServer import *


# __all__ = ['ProxyHandler', 'run_proxy']

USE_REMOTE_CLIENT = True

class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']

    @tornado.web.asynchronous
    def get(self):
        pass

    @tornado.web.asynchronous
    def post(self):
        pass

    @tornado.web.asynchronous
    def connect(self):
        # 当时ssl时会调用connect

        def read_from_client(data):
            g_logger.info("%s" % (base64.b64encode(data)))
            if USE_REMOTE_CLIENT:
                package = {}
                package["code"] = g_code_do_https
                package["host"] = host
                package["port"] = port
                package["data"] = base64.b64encode(data)
                package["actionID"] = actionID

                upstream1.write(obj2json(package) + EOF)
            else:
                upstream.write(data)

        def read_from_upstream(data):
            g_logger.info("%s" % (base64.b64encode(data)))
            client.write(data)

        def client_close(data=None):
            g_logger.info("FXXK")
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            g_logger.info("FXXK")
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        for conn in g_connections:
            upConn = conn
            upstream1 = conn.get_stream()
            break

        actionID = get_timestamp()
        if USE_REMOTE_CLIENT:
            g_logger.info("FXXK")
            upConn.do_https(client, host, port, actionID)
            pass
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            upstream = tornado.iostream.IOStream(s)
            upstream.connect((host, int(port)), start_tunnel)


def run_https_proxy(port, start_ioloop=False):
    """
    Run proxy on the specified port. If start_ioloop is True (default),
    the tornado IOLoop will be started immediately.
    """
    app = tornado.web.Application([
        (r'.*', ProxyHandler),
    ])
    app.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    if start_ioloop:
        ioloop.start()

# if __name__ == '__main__':
#     port = settings.LOCAL_PORT
#     if len(sys.argv) > 1:
#         port = int(sys.argv[1])
#
#     print ("Starting HTTP proxy on port %d" % port)
#     run_proxy(port)
