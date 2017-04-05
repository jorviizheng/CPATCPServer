#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import tornado.web
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from CPATCPServer.CPATCPServer import *
import random

class PostToRemote(tornado.web.RequestHandler):
    def get(self):
        print("Request from %s" % (self.request.remote_ip, ))

        szMsg = self.get_argument("msg")
        # Connection.broadcast_messages(szMsg)
        for conn in g_connections:
            conn.send_message(szMsg.encode("utf-8"))

        self.write("Success")

    def post(self):
        szBody = self.request.body
        dicJson = json.loads(szBody)
        g_logger.info("Receive post request, body: %s" % (szBody, ))
        g_logger.info("needResp: %d" % (dicJson["httpInfo"]["needResp"],))

        for conn in g_connections:
            conn.send_message(szBody.encode("utf-8"))
            # conn.add_on_message_callback(self.on_message())
            break
        # conn.add_on_message_callback(self.on_message())

        # if 1 == dicJson["httpInfo"]["needResp"]:
        #     conn = random.sample(g_connections, 1)

        self.write("success")

    def on_message(self, szMsg):
        g_logger.info(szMsg)
        return "success"

