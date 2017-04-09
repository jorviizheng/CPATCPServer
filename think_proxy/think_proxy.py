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
import settings
from thinkutils.log.log import *

__all__ = ['ProxyHandler', 'run_proxy']


class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']

    @tornado.web.asynchronous
    def get(self):

        def handle_response(response):
            # resp解密
            if response.error and not isinstance(response.error,
                    tornado.httpclient.HTTPError):
                self.set_status(500)
                self.write('Internal server error:\n' + str(response.error))
            else:
                self.set_status(response.code)
                for header in ('Date', 'Cache-Control', 'Server',
                        'Content-Type', 'Location'):
                    v = response.headers.get(header)
                    if v:
                        v = decrypt(v)
                        self.set_header(header, v)
                if response.body:
                    body = decrypt(response.body)
                    self.write(body)
            self.finish()
            
        # req加密
        print "url:", self.request.uri
        url = settings.REMOTE_HOST + encrypt(self.request.uri)
        body = encrypt(self.request.body)
        headers = deepcopy(self.request.headers)
        for k, v in headers.iteritems():
            headers[k] = encrypt(v)
            
        req = tornado.httpclient.HTTPRequest(url=url,
            method=self.request.method, body=body,
            headers=headers, follow_redirects=False,
            allow_nonstandard_methods=True)

        client = tornado.httpclient.AsyncHTTPClient()
        try:
            client.fetch(req, handle_response)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                handle_response(e.response)
            else:
                self.set_status(500)
                self.write('Internal server error:\n' + str(e))
                self.finish()

    @tornado.web.asynchronous
    def post(self):
        return self.get()

    @tornado.web.asynchronous
    def connect(self):
        # 当时ssl时会调用connect
        host, port = self.request.uri.split(':')
        g_logger.info("Connect to %s:%s" % (host, port))
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


def run_proxy(port, start_ioloop=False):
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
