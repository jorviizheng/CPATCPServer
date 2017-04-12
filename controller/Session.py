#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import tornado.web
import uuid
from RetModel import *
from thinkutils.common_utils.object2json import *

class Session(tornado.web.RequestHandler):
    def get(self):
        self.write(self.make_sessionid().encode("utf-8"))

    def post(self):
        self.write(self.make_sessionid().encode("utf-8"))

    def make_sessionid(self):
        szUuid = uuid.uuid4();
        # szUuid = szUuid.replace("-", "")
        ret = RetModel(code=0, data=str(szUuid).replace("-", ""))
        return obj2json(ret)