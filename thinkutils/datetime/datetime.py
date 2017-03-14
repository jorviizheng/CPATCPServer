import time

def get_timestamp():
    return int(time.time())

def get_current_time_str():
    temp = time.localtime(time.time())
    szTime = time.strftime("%Y-%m-%d %H:%M:%S", temp)
    return szTime

def timestamp2str(tt):
    t1 = time.localtime(float(tt))
    t2 = time.strftime("%Y-%m-%d %H:%M:%S",t1)
    return t2;