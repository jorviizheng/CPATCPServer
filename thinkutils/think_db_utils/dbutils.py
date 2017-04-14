import MySQLdb
from DBUtils.PooledDB import PooledDB

from thinkutils.config.Config import *

g_dbPool = PooledDB(MySQLdb
                    , 5
                    , host=g_config.get("mysql", "host")
                    , user=g_config.get("mysql", "user")
                    , passwd=g_config.get("mysql", "password")
                    , db=g_config.get("mysql", "db")
                    , port=g_config.get("mysql", "port")
                    , maxconnections=g_config.get("mysql", "maxconnections")
                    , charset = "utf8"
                    , use_unicode = True)
