#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json

class TCPPackage(object):
    code = 0; #0 for heartbeat
    date = ""
    
    def __init__(self, code=0, data=None):
        self.code = code
        self.data = data

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)