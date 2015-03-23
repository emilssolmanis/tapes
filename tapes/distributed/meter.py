from __future__ import division
from .message import Message


class MeterProxy(object):
    def __init__(self, socket, name):
        self.name = name
        self.socket = socket

    def mark(self, n=1):
        self.socket.send_pyobj(Message('meter', self.name, n))
