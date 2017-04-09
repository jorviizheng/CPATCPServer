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

g_connections = set()
g_EOF = '\0'

class TCPConnection(object):
    def __init__(self, stream, address):
        g_connections.add(self)
        self._stream = stream
        self._address = address
        self._connect_time = get_timestamp()
        self._update_time = get_timestamp()
        self._EOF = g_EOF
        self._tunnel_client = None
        self._stream.set_close_callback(self.on_close)
        self.on_message()
        self._on_message_callback = set()
        g_logger.info("A new user connected %s" % (address, ))

    def get_stream(self):
        return self._stream

    def get_address(self):
        return self._address

    def on_message(self):
        self._stream.read_until(self._EOF, self.read_messages)

    def add_on_message_callback(self, callback=None):
        if None is not callback:
            self._on_message_callback.add(callback)

    def client_close(self, data=None):
        if self.closed():
            return
        if data:
            self._tunnel_client.write(data)
        # upstream.close()

    def read_from_client(self, data):
        g_logger.info("Send Message")
        self.send_message(data)

    def start_tunnel(self, client):
        self._tunnel_client = client
        client.read_until_close(self.client_close, self.read_from_client)
        # self.read_until_close(upstream_close, read_from_upstream)
        self._tunnel_client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')
        self._tunnel_client = None

    def is_tunneling(self):
        if self._tunnel_client is None:
            return False
        else:
            return True

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

            if g_code_do_budiness_ret == package["code"]:
                yield self.save_to_redis(package)

        except ValueError, e:
            g_logger.info("%s Not a valid package, pass!" % (data[:-1], ))

        # self.send_message("hehe".encode("utf-8") + self._EOF)
        self.on_message()

    def send_message(self, data):
        try:
            self._stream.write(data + self._EOF)
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

class CPATCPServer(TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        g_logger.info("New connection %s %s" % (address, stream))
        TCPConnection(stream, address)

# def broadcast_checker():
