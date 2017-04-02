#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import socket

import tornado.gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
from thinkutils.log.log import *
from thinkutils.common_utils.object2json import *
import json
from models.TCPPackage import *

g_connections = set()

class TCPConnection(object):

    def __init__(self, stream, address):
        g_connections.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.on_message()
        g_logger.info("A new user connected %s" % (address, ))

    def on_message(self):
        self._stream.read_until('\n', self.read_messages)

    def read_messages(self, data):
        g_logger.info("Receive message: %s" % (data[:-1], ))
        package = TCPPackage.from_json(data[:-1])
        g_logger.info("Receive message: %d" % (package.code,))
        self.on_message()

    def send_message(self, data):
        self._stream.write(data)

    def on_close(self):
        g_connections.remove(self)

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        g_logger.info("New connection %s %s" % (address, stream))
        TCPConnection(stream, address)