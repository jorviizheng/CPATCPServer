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
from codes import *
from thinkutils.redis.think_redis import *
from tornado import gen
import base64

g_connections = set()
EOF = '\0'

class TCPConnection(object):
    def __init__(self, stream, address):
        g_connections.add(self)
        self.__stream = stream
        self.__address = address
        self.__connect_time = get_timestamp()
        self.__update_time = get_timestamp()
        self.__EOF = EOF
        self.__stream.set_close_callback(self.on_close)
        self.on_message()
        self.__on_message_callback = set()
        self.__client = None
        g_logger.info("A new user connected %s" % (address, ))

    def on_message(self):
        self.__stream.read_until(self.__EOF, self.read_messages)

    def add_on_message_callback(self, callback=None):
        if None != callback:
            self.__on_message_callback.add(callback)

    def get_stream(self):
        return self.__stream

    @gen.coroutine
    def read_messages(self, data):
        try:
            package = json.loads(data[:-1])
            # g_logger.info("Receive message code : %d data: %s" % (int(package["code"]), package[data]))
            # if self._on_message_callback != None:
            #     for callback in self._on_message_callback:
            #         callback(data[:-1])

            if 0 == package["code"]: #heartbeat
                self.send_message(obj2json(package))

            if g_code_do_http_ret == package["code"]:
                yield self.save_to_redis(package)

            if g_code_do_https_ret == package["code"]:
                g_logger.info("Write to client %s" % (package["data"], ))
                try:
                    self.write_https_stream_to_client(base64.b64decode(package["data"]))
                except socket.error, msg:
                    g_logger.error("Exception: %s" % (msg, ))

            if g_code_do_https_close == package["code"]:
                g_logger.info("Remote Server closed")

        except ValueError, e:
            g_logger.info("%s Not a valid package, pass!" % (data[:-1], ))

        # self.send_message("hehe".encode("utf-8") + self._EOF)
        self.on_message()

    def send_message(self, data):
        try:
            self.__stream.write(data + self.__EOF)
        except:
            pass
        finally:
            pass

    def on_close(self):
        g_connections.remove(self)

    @gen.coroutine
    def save_to_redis(self, package):
        r = redis.StrictRedis(connection_pool=g_redis_pool)
        szKey = "actions_" + today()
        g_logger.info("redis key %s", (szKey, ))
        dicRedis = {}
        dicRedis[package["actionID"]] = obj2json(package)
        r.hmset(szKey, dicRedis)
        # szVal = r.hmget(szKey, )
        # pass

    def do_https(self, client, host, port, actionID):
        g_logger.info("Start https proxy")
        def client_close(data=None):
            g_logger.info("FXXK")

        def read_from_client(data):
            g_logger.info("%s" % (base64.b64encode(data)))
            package = {}
            package["code"] = g_code_do_https
            package["host"] = host
            package["port"] = port
            package["data"] = base64.b64encode(data)
            package["actionID"] = actionID

            self.send_message(obj2json(package))
            # client.read_until_close(client_close, read_from_client)

        def start_tunnel():
            self.__client.read_until_close(client_close, read_from_client)
            self.__client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        self.__client = client
        start_tunnel()

    def write_https_stream_to_client(self, data):
        if self.__client is not None:
            try:
                self.__client.write(data)
            except socket.error, msg:
                g_logger.error("Exception: %s" % (msg,))
                self.__client = None

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        g_logger.info("New connection %s %s" % (address, stream))
        TCPConnection(stream, address)

# def broadcast_checker():
