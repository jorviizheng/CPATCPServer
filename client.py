#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from tornado import ioloop, httpclient, gen
from tornado.gen import Task
import pdb, time
import tornado.ioloop
import tornado.iostream
import socket
from thinkutils.log.log import *
import threading
import time
import json
from thinkutils.common_utils.object2json import *
from CPATCPServer.models.TCPPackage import *

g_tcp_conns = set()
g_conn_num = 200

class TCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop
        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self._EOF = '\0'

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.on_connect)

    def on_receive(self, data):
        if len(data.decode("utf-8").strip()) > 0:
            g_logger.info("Received: %s", data.decode("utf-8"))
        self.stream.read_until(self._EOF, self.on_receive)

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()

    def on_connect(self):
        g_logger.info("Connected")
        g_tcp_conns.add(self)
        self.stream.read_until(self._EOF, self.on_receive)

    def send_message(self, szMsg):
        g_logger.info("Send message: %s" % (szMsg, ))
        self.stream.write(szMsg + self._EOF)

    def set_shutdown(self):
        self.shutdown = True


def heartbeat_worker():
    while True:
        # g_logger.info("Send heartbeat")
        for conn in g_tcp_conns:
            heartbeat = TCPPackage()
            # heartbeat.data = "你好"
            conn.send_message(obj2json(heartbeat))

        time.sleep(60)

def main():
    io_loop = tornado.ioloop.IOLoop.instance()

    for i in range(g_tcp_conns):
        c = TCPClient("50.116.10.36", 9001, io_loop)
        c.connect()

    t = threading.Thread(target=heartbeat_worker)
    t.start()

    g_logger.info("**********************start ioloop******************")
    io_loop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()