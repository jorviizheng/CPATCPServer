# Let's import tornado and tornadis
import tornado
from thinkutils.tornadis.pipeline import *
from thinkutils.tornadis.client import *
from thinkutils.tornadis.exceptions import *
from thinkutils.config.Config import *

@tornado.gen.coroutine
def pipeline_coroutine():
    # Let's make a pipeline object to stack commands inside
    pipeline = Pipeline()
    pipeline.stack_call("SET", "foo", "bar")
    pipeline.stack_call("GET", "foo")

    # At this point, nothing is sent to redis

    # let's (re)connect (autoconnect mode), send the pipeline of requests
    # (atomic mode) and wait all replies without blocking the tornado ioloop.
    results = yield client.call(pipeline)
    yield client.call("SET", "2017-04-15", "Hello World")

    if isinstance(results, TornadisException):
        # For specific reasons, tornadis nearly never raises any exception
        # they are returned as results
        print "got exception: %s" % results
    else:
        # The two replies are in the results array
        print results
        # >>> ['OK', 'bar']

# Build a tornadis.Client object with some options as kwargs
# host: redis host to connect
# port: redis port to connect
# autoconnect=True: put the Client object in auto(re)connect mode
client = Client(host=g_config.get("redis", "host"), port=int(g_config.get("redis", "port")), password=g_config.get("redis", "password"), autoconnect=True)

# Start a tornado IOLoop, execute the coroutine and end the program
loop = tornado.ioloop.IOLoop.instance()
loop.run_sync(pipeline_coroutine)
