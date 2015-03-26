import contextlib
from time import time

from .proxy import MetricsProxy
from .message import Message


class TimerProxy(MetricsProxy):
    def __init__(self, socket, name):
        super(TimerProxy, self).__init__(socket)
        self.name = name

    @contextlib.contextmanager
    def time(self):
        start_time = time()
        try:
            yield
        finally:
            end_time = time()
            self.send(Message('timer', self.name, end_time - start_time))
