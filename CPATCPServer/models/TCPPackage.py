#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
from thinkutils.datetime.datetime_utils import *

class TCPPackage(object):
    code = 0; #0 for heartbeat
    sessionID = ""
    actionID = ""
    data = ""

    def __init__(self, j):
        self.__dict__ = json.loads(j)
    
    def __init__(self, code=0, data=None, sessionID = None, actionID = None):
        self.code = code
        self.data = data
        self.actionID = sessionID
        self.actionID = actionID

    # @classmethod
    # def from_json(cls, json_str):
    #     json_dict = json.loads(json_str)
    #     return cls(**json_dict)