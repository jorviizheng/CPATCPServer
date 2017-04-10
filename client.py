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
from threading import Timer
import requests
import base64
from CPATCPServer.codes import *
import sys
import traceback
from tornado import gen
from CPATCPServer.CPATCPServer import *

g_tcp_conns = set()
g_conn_num = 2

class TCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop
        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self._connHttps = {}
        self._EOF = EOF

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)

    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.on_connect)

    @gen.coroutine
    def on_receive(self, data):
        if len(data.decode("utf-8").strip()) > 0:
            g_logger.info("Received: %s", data[:-1].decode("utf-8"))
            try:
                json_dict = json.loads(data[:-1].decode("utf-8"))
                if g_code_do_http == json_dict["code"]:
                    package = TCPPackage(code = json_dict["code"], sessionID = json_dict["sessionID"], actionID = json_dict["actionID"], data = json_dict["data"])
                    g_logger.info("Receive message code : %d data: %s" % (package.code, package.data))
                    szJson = base64.decodestring(package.data)
                    g_logger.info(package.data)
                    dicJson = json.loads(szJson)
                    g_logger.info(szJson)
                    szRet = yield self.do_http(dicJson)
                    self.send_message(szRet)

                if g_code_do_https == json_dict["code"]:
                    self.do_https(json_dict);
            except Exception,e:
                g_logger.error(e)
                traceback.print_exc()
                pass
            finally:
                pass
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

    @gen.coroutine
    def do_http(self, dicJson):
        dicHeader = dicJson["httpInfo"]["header"]
        szUrl = dicJson["httpInfo"]["requrl"]
        szMethod = dicJson["httpInfo"]["method"]

        if "GET" == szMethod.upper():
            r = requests.get(szUrl, headers=dicHeader)
            szRet = r.text
            g_logger.info(szRet)
        else:
            r = requests.post(szUrl, headers=dicHeader)
            szRet = r.text
            g_logger.info(szRet)

        package = TCPPackage()
        package.code = g_code_do_http_ret
        package.actionID = dicJson["actionID"]
        package.sessionID = dicJson["sessionID"]
        package.data = base64.encodestring(szRet.encode("utf-8"))

        raise gen.Return(obj2json(package))
        # g_logger.info("Return value to Server: %s" % (obj2json(package)))
        # self.send_message(obj2json(package))

    def do_https(self, dicJson):
        g_logger.info("FXXK")

        def read_from_upstream(data):
            g_logger.info("%s" % (base64.b64encode(data)))
            package = {}
            package["code"] = g_code_do_https_ret
            package["actionID"] = dicJson["actionID"]
            package["data"] = base64.b64encode(data)
            self.send_message(obj2json(package))

        def upstream_close(data=None):
            g_logger.info("Remote Server Closed")
            if data is not None:
                package = {}
                package["code"] = g_code_do_https_ret
                package["actionID"] = dicJson["actionID"]
                package["data"] = base64.b64encode(data)
                self.send_message(obj2json(package))

            packageClose = {}
            packageClose["code"] = g_code_do_https_close
            packageClose["actionID"] = dicJson["actionID"]
            self.send_message(obj2json(packageClose))

        def start_tunnel():
            # client.read_until_close(client_close, read_from_client)
            # upstream.read_until_close(upstream_close, read_from_upstream)
            # client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')
            g_logger.info("Write to remote server %s" % (dicJson["data"],))

            upstream.write(base64.b64decode(dicJson["data"]))
            upstream.read_until_close(upstream_close, read_from_upstream)


        if dicJson["actionID"] in self._connHttps.keys():
            # send data to real server
            g_logger.info("FXXK")
            upstream = self._connHttps[dicJson["actionID"]]
            g_logger.info("Write to remote server %s" % (dicJson["data"],))
            upstream.write(base64.b64decode(dicJson["data"]))
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            upstream = tornado.iostream.IOStream(s)
            self._connHttps[dicJson["actionID"]] = upstream

            g_logger.info("%s ==> %s" % (dicJson["host"], dicJson["port"]))
            upstream.connect((dicJson["host"], int(dicJson["port"])), start_tunnel)


def heartbeat_worker():
    # g_logger.info("Send heartbeat")
    while True:
        time.sleep(5 * 60) #5 min for heartbeat
        for conn in g_tcp_conns:
            try:
                heartbeat = TCPPackage()
                # heartbeat.data = "你好"
                conn.send_message(obj2json(heartbeat))
            except Exception:
                pass
            finally:
                pass

def main():
    io_loop = tornado.ioloop.IOLoop.instance()

    for i in range(g_conn_num):
        c = TCPClient("127.0.0.1", 9001, io_loop)
        c.connect()

    t = threading.Thread(target=heartbeat_worker)
    t.daemon = True
    t.start()

    g_logger.info("**********************start ioloop******************")
    io_loop.start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()
