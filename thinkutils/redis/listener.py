# coding=utf-8
from abc import *

from thinkutils.redis.think_redis import *
from thinkutils.thread.ThreadPool import *


class Listener(object):

    __metaclass__ = ABCMeta

    def __init__(self, redis_conn, channels):
        self.redis_conn = redis_conn
        self.pubsub = self.redis_conn.pubsub()
        self.pubsub.subscribe(channels)
        self.thread_pool = ThreadPool(size=len(channels))

    @abstractmethod
    def on_message(self, item):
        # 修改成你的代码逻辑
        # print item["channel"], item["data"]
        pass
    
    def run(self):
        self.thread_pool.start()
        for item in self.pubsub.listen():
            self.thread_pool.append_job(self.on_message, item)

# class MyListener(Listener):
#     def __init__(self, redis_conn, channels):
#         Listener.__init__(self, redis_conn, channels)
#
#     def on_message(self, item):
#         # 修改成你的代码逻辑
#         print item["channel"], item["data"]
#
# if __name__ == "__main__":
#     r = redis.StrictRedis(connection_pool=g_redis_pool)
#     client = MyListener(r, ['channel1', 'fxxk'])
#     # for i in range(10):
#     #     r.publish("channel1", i)
#     client.run()