#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import tornado.web
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from CPATCPServer.CPATCPServer import *

class Broadcast(tornado.web.RequestHandler):
    def get(self):
        print("Request from %s" % (self.request.remote_ip, ))

        szMsg = self.get_argument("msg")
        # Connection.broadcast_messages(szMsg)
        for conn in g_connections:
            conn.send_message(szMsg.encode("utf-8"))

        self.write("Success")