#!/usr/bin/python
#coding=utf-8

import tornado.gen
import tornado.ioloop
import tornado.web

from CPATCPServer.CPATCPServer import *
from controller.PostToRemote import *
from controller.Session import *
from controller.broadcast import *
from think_proxy.https_proxy import *

define('tcp_port', default=9001)
define('http_port', default=9002)
define('https_port', default=9003)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = Application([
    (r'/', MainHandler),
    (r'/broadcast', Broadcast),
    (r'/post_to_remote', PostToRemote),
    (r'/get_session', Session),
])

def main():
    # http server
    http_server = HTTPServer(application)
    http_server.listen(options.http_port)

    #for https proxy
    run_https_proxy(options.https_port)

    # tcp server
    server = CPATCPServer()
    server.listen(options.tcp_port)
    g_logger.info('Server started...')

    # tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
