from __future__ import division

from .proxy import MetricsProxy
from .message import Message


class MeterProxy(MetricsProxy):
    def __init__(self, socket, name):
        super(MeterProxy, self).__init__(socket)
        self.name = name

    def mark(self, n=1):
        self.send(Message('meter', self.name, n))
