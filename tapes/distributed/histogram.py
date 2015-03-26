from .proxy import MetricsProxy
from .message import Message


class HistogramProxy(MetricsProxy):
    def __init__(self, socket, name):
        super(HistogramProxy, self).__init__(socket)
        self.name = name

    def update(self, value):
        self.send(Message('histogram', self.name, value))
