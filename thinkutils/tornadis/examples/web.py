from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import tornado.gen
import logging
from thinkutils.tornadis.pool import *
from thinkutils.tornadis.exceptions import *

logging.basicConfig(level=logging.WARNING)
POOL = ClientPool(max_size=15)


class HelloHandler(RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        with (yield POOL.connected_client()) as client:
            reply = yield client.call("PING")
            if not isinstance(reply, TornadisException):
                self.write("Hello, %s" % reply)
        self.finish()


def make_app():
    return Application([
        url(r"/", HelloHandler),
        ])


def main():
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

main()
