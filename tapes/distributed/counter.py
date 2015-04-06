from .proxy import MetricsProxy
from .message import Message


class CounterProxy(MetricsProxy):
    def __init__(self, socket, name):
        super(CounterProxy, self).__init__(socket)
        self.name = name

    def increment(self, n=1):
        self.send(Message('counter', self.name, n))

    def decrement(self, n=1):
        self.send(Message('counter', self.name, -n))
