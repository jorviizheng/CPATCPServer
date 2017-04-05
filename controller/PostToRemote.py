#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import tornado.web
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from CPATCPServer.CPATCPServer import *
import random
from CPATCPServer.codes import *
import base64

g_reqursts = {}

class PostToRemote(tornado.web.RequestHandler):
    def get(self):
        print("Request from %s" % (self.request.remote_ip, ))

        szMsg = self.get_argument("msg")
        # Connection.broadcast_messages(szMsg)
        for conn in g_connections:
            conn.send_message(szMsg.encode("utf-8"))

        self.write("Success")

    @tornado.gen.coroutine
    def post(self):
        szBody = self.request.body
        dicJson = json.loads(szBody)
        g_logger.info("Receive post request, body: %s" % (szBody, ))
        g_logger.info("needResp: %d" % (dicJson["httpInfo"]["needResp"],))
        g_reqursts[dicJson["actionID"]] = dicJson

        for conn in g_connections:
            package = TCPPackage()
            package.code = g_code_do_budiness
            package.actionID = dicJson["actionID"]
            package.sessionID = dicJson["sessionID"]
            package.data = base64.b64encode(szBody.encode("utf-8"))
            g_logger.info(package.data)
            conn.send_message(obj2json(package))
            # conn.add_on_message_callback(self.on_message())
            break

        r = redis.StrictRedis(connection_pool=g_redis_pool)
        szKey = "actions_" + today()
        for i in range(60):
            if r.exists(szKey):
                szVal = r.hmget(szKey, package.actionID)
                g_logger.info(szVal[0].encode("utf-8"))
                dictRet = json.loads(szVal[0].encode("utf-8"))
                if szVal != None:
                    g_logger.info(szVal)
                    self.write(dictRet["data"])
                    return

            yield tornado.gen.sleep(0.5)

        self.finish(json.dumps(szVal))
        # self.write("success".encode("utf-8"))

    def on_message(self, szMsg):
        g_logger.info(szMsg)
        return "success"

