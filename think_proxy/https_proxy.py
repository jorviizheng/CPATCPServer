#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""部署在本地"""

import sys
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient

from utils import decrypt, encrypt
from copy import deepcopy

# __all__ = ['ProxyHandler', 'run_proxy']


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
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

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
