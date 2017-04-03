#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from tornado import ioloop, httpclient, gen
from tornado.gen import Task
import pdb, time, logging
import tornado.ioloop
import tornado.iostream
import socket

from tornado import stack_context
from thinkutils.log.log import *
from thinkutils.common_utils.object2json import *
from CPATCPServer.models.TCPPackage import *

class TCPClient(object):
    test_start = False
    max_connected = 20
    test_num = 20
    test_remain = test_num
    test_count = 0
    total_count = 0
    shutdown = False

    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop

        self.shutdown = False
        self.stream = None
        self.sock_fd = None

        self.EOF = '\0'

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.send_message)

    def on_receive(self, data):
        logging.info("Received: %s", data)
        self.stream.close()
        self.stream = None
        self.sock_fd = None

        TCPClient.test_count += 1
        try_testing(self.io_loop)

    def on_close(self):
        TCPClient.total_count += 1
        if TCPClient.total_count % 2000 == 0:
            g_logger.info("Has treat: %s", TCPClient.total_count)
            # logging.info("----count: %s %s  %s", TCPClient.total_count, TCPClient.shutdown, TCPClient.test_num)
        if TCPClient.shutdown and TCPClient.total_count == TCPClient.test_num:
            logging.info("shutdown")
            self.io_loop.stop()

    def send_message(self):
        g_logger.info("Send message....")
        # self.stream.write("Hello Server!" + self.EOF)
        heartbeat = TCPPackage()
        self.stream.write(obj2json(heartbeat) + self.EOF)
        self.stream.read_until(self.EOF, self.on_receive)
        # logging.info("After send....")

    def set_shutdown(self):
        TCPClient.shutdown = True


def _handle_exception(typ, value, tb):
    g_logger.info("%s  %s  %s", typ, value, tb)
    return True


def try_testing(io_loop):
    # logging.info("test_count: %s, test_remain: %s", TCPClient.test_count, TCPClient.test_remain)
    if TCPClient.test_start and TCPClient.test_count >= TCPClient.max_connected and TCPClient.test_remain > 0:
        TCPClient.test_start = False

    if not TCPClient.test_start:
        TCPClient.test_count = 0
        TCPClient.test_start = True

        gen = None
        if TCPClient.test_remain >= TCPClient.max_connected:
            gen = start_test(io_loop, TCPClient.max_connected)
        elif TCPClient.test_remain > 0:
            gen = start_test(io_loop, TCPClient.test_remain)

        if gen:
            with stack_context.ExceptionStackContext(_handle_exception):
                c = gen.next()
                while True:
                    c = gen.send(c)


def start_test(io_loop, count):
    TCPClient.test_remain = TCPClient.test_remain - count
    g_logger.info("Will start %s testing! Remain: %s", count, TCPClient.test_remain)
    for i in range(count):
        c = yield TCPClient("thinkman-wang.com", 9001, io_loop)
        if i == (count - 1) and TCPClient.test_remain <= 0:
            c.set_shutdown()
        c.connect()


def main():
    io_loop = tornado.ioloop.IOLoop.instance()
    try_testing(io_loop)

    g_logger.info("**********************start ioloop******************")
    io_loop.start()


if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()