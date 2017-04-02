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
        self.stream.connect((self.host, self.port), self.on_connect)

    def on_receive(self, data):
        g_logger.info("Received: %s", data)
        self.stream.close()

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()

    def on_connect(self):
        g_logger.info("Connected")
        self.stream.read_until(self.EOF, self.on_receive)

    def send_message(self, szMsg):
        g_logger.info("Send message....")
        self.stream.write(szMsg + self.EOF)
        g_logger.info("After send....")

    def set_shutdown(self):
        self.shutdown = True

io_loop = tornado.ioloop.IOLoop.instance()
c1 = TCPClient("127.0.0.1", 9001, io_loop)

def heartbeat_worker(conn):
    while True:
        g_logger.info("Send heartbeat")
        heartbeat = TCPPackage()
        conn.send_message(obj2json(heartbeat))
        conn.send_message("hearbbeat")
        time.sleep(5)

def main():
    c1.connect()
    t = threading.Thread(target=heartbeat_worker, args=(c1,))
    t.start()

    g_logger.info("**********************start ioloop******************")
    io_loop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()