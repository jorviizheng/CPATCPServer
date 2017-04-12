__author__ = 'Xsank'
from thinkutils.eventbus.event import *

class GreetEvent(Event):
    def __init__(self,name):
        self.name=name


class ByeEvent(Event):
    def __init__(self,name):
        self.name=name