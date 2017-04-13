# coding=utf-8
import redis
from thinkutils.common_utils.ThreadPool import *
from thinkutils.redis.think_redis import *

class Listener():
    def __init__(self, redis_conn, channels):
        self.redis_conn = redis_conn
        self.pubsub = self.redis_conn.pubsub()
        self.pubsub.subscribe(channels)
        self.thread_pool = ThreadPool(size=len(channels))
    
    def on_message(self, item):
        # 修改成你的代码逻辑
        print item["channel"], item["data"]
    
    def run(self):
        self.thread_pool.start()
        for item in self.pubsub.listen():
            self.thread_pool.append_job(self.on_message, item)

if __name__ == "__main__":
    r = redis.StrictRedis(connection_pool=g_redis_pool)
    client = Listener(r, ['channel1'])
    # for i in range(10):
    #     r.publish("channel1", i)
    client.run()