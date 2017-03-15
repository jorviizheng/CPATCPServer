import os
import sys
import hashlib
import requests

def md5_str(szText):
    return str(hashlib.md5(szText).hexdigest())

def md5_file(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()