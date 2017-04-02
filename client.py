#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from tornado import ioloop, httpclient, gen
from tornado.gen import Task
import pdb, time
import tornado.ioloop
import tornado.iostream
import socket
from thinkutils.log.log import *

class TCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop
        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self.EOF = b'\n'

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.send_message)

    def on_receive(self, data):
        g_logger.info("Received: %s", data)
        self.stream.close()

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()

    def send_message(self):
        g_logger.info("Send message....")
        self.stream.write(b"Hello Server!" + self.EOF)
        self.stream.read_until(self.EOF, self.on_receive)
        g_logger.info("After send....")

    def set_shutdown(self):
        self.shutdown = True

def main():
    io_loop = tornado.ioloop.IOLoop.instance()
    c1 = TCPClient("127.0.0.1", 9001, io_loop)
    c2 = TCPClient("127.0.0.1", 9001, io_loop)
    c1.connect()
    c2.connect()
    # c2.set_shutdown()
    g_logger.info("**********************start ioloop******************")
    io_loop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()