
from thinkutils.eventbus.event import *

class HeartBeatEvent(Event):
    '''
    0 for offline
    1 for online
    '''
    # def __init__(self, code = 0, sessionID = None):
    #     self.code = code
    #     self.sessionID = sessionID

    def __init__(self, code = 0, data = None):
        self.code = code
        self.data = data