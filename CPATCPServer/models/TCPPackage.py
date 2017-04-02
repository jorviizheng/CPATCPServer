
class TCPPackage(object):
    code = 0; #0 for heartbeat
    date = ""
    
    def __init__(self, code=0, data=None):
        self.code = code
        self.data = data