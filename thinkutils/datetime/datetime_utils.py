import time
from datetime import date, timedelta
from thinkutils.log import *

# logger = setup_custom_logger()

def get_timestamp():
    return int(time.time())

def get_current_time_str():
    temp = time.localtime(time.time())
    szTime = time.strftime("%Y-%m-%d %H:%M:%S", temp)
    return szTime

def timestamp2str(tt):
    t1 = time.localtime(float(tt))
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
    return t2

def today():
    today = date.today()
    return today.strftime('%Y-%m-%d')

def yesterday():
    yesterday = date.today() + timedelta(-1)
    return yesterday.strftime('%Y-%m-%d')

def diff_day(nDiff):
    day = date.today() + timedelta(nDiff)
    return day.strftime('%Y-%m-%d')