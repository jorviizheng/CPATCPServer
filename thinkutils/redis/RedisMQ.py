# coding=utf-8
from abc import *

from thinkutils.redis.think_redis import *
from thinkutils.thread.ThreadPool import *
from threading import Thread


class PubSubListener(Thread):

    __metaclass__ = ABCMeta

    def __init__(self, redis_conn, channels):
        super(PubSubListener, self).__init__()
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

class RedisMQListener(Thread):
    __metaclass__ = ABCMeta

    def __init__(self, redis_conn, queueName):
        super(RedisMQListener, self).__init__()
        self.__running = True
        self.__redis_conn = redis_conn
        self.__queue_name = queueName
        pass

    @abstractmethod
    def on_message(self, item):
        pass

    def is_finished(self):
        return self.__running__

    def finish(self):
        self.__running = False

    def run(self):
        while self.__running:
            item = self.__redis_conn.lpop(self.__queue_name)
            if item is not None:
                self.on_message(item)
            else:
                time.sleep(2)
                continue

class MyListener(PubSubListener):
    def __init__(self, redis_conn, channels):
        PubSubListener.__init__(self, redis_conn, channels)

    def on_message(self, item):
        # 修改成你的代码逻辑
        print item["channel"], item["data"]

class MyMQ(RedisMQListener):
    def __init__(self, redis_conn, queueName):
        RedisMQListener.__init__(self, redis_conn, queueName)

    def on_message(self, item):
        print (item)

'''
For test redis MQ
'''
# if __name__ == "__main__":
#     r = redis.StrictRedis(connection_pool=g_redis_pool)
#     queue = MyMQ(r, "test_queue")
#     queue.start()
#     queue.join()

'''
For test redis Pub/Sub
'''
if __name__ == "__main__":
    r = redis.StrictRedis(connection_pool=g_redis_pool)
    client = MyListener(r, ['channel1', 'fxxk'])
    # for i in range(10):
    #     r.publish("channel1", i)
    client.run()