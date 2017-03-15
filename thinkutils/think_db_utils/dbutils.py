import sys
import os

import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time

g_dbPool = PooledDB(MySQLdb, 5, host='localhost', user='notes', passwd='welc0me', db='db_notes', port=3306, charset = "utf8", use_unicode = True)
