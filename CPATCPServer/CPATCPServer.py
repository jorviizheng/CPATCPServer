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

g_connections = set()

class TCPConnection(object):

    def __init__(self, stream, address):
        g_connections.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.on_message()
        print "A new user has entered the chat room.", address

    def on_message(self):
        self._stream.read_until('\n', self.read_messages)

    def read_messages(self, data):
        print "Receive message:", data[:-1]
        # for conn in g_connections:
        #     conn.send_message(data)
        self.on_message()

    def send_message(self, data):
        self._stream.write(data)

    def on_close(self):
        print "A user has left the chat room.", self._address
        g_connections.remove(self)

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print("New connection" , address, stream)
        TCPConnection(stream, address)