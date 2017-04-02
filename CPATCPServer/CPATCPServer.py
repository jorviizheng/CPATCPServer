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


class Connection(object):
    clients = set()

    def __init__(self, stream, address):
        Connection.clients.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.read_message()
        print "A new user has entered the chat room.", address

    def read_message(self):
        self._stream.read_until('\n', self.broadcast_messages)

    def broadcast_messages(self, data):
        print "broadcast message:", data[:-1], self._address
        for conn in Connection.clients:
            conn.send_message(data)
        self.read_message()

    def send_message(self, data):
        self._stream.write(data)

    def on_close(self):
        print "A user has left the chat room.", self._address
        Connection.clients.remove(self)

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print("New connection" , address, stream)
        Connection(stream, address)