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
from thinkutils.datetime.datetime_utils import *

g_connections = set()

class TCPConnection(object):
    def __init__(self, stream, address):
        g_connections.add(self)
        self._stream = stream
        self._address = address
        self._connect_time = get_timestamp()
        self._update_time = get_timestamp()
        self._EOF = '\n'
        self._stream.set_close_callback(self.on_close)
        self.on_message()
        g_logger.info("A new user connected %s" % (address, ))

    def on_message(self):
        self._stream.read_until(self._EOF, self.read_messages)

    def read_messages(self, data):
        try:
            package = TCPPackage.from_json(data[:-1])
            g_logger.info("Receive message code : %d data: %s" % (package.code,package.data))
        except ValueError, e:
            g_logger.info("Not a valid package, pass!")

        self.on_message()

    def send_message(self, data):
        self._stream.write(data + self._EOF)

    def on_close(self):
        g_connections.remove(self)

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        g_logger.info("New connection %s %s" % (address, stream))
        TCPConnection(stream, address)

# def broadcast_checker():
