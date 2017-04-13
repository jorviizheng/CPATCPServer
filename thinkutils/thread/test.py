from ThreadPool import *

def tester(num):
    print("FXXXXXK %d" % (num, ))

def tester1():
    print("FXXXXXK")

if __name__ == '__main__':
    thread_pool = ThreadPool(10)
    for i in range(1000):
        thread_pool.append_job(tester, i)

    for i in range(1000):
        thread_pool.append_job(tester1)

    thread_pool.start()
    thread_pool.join()