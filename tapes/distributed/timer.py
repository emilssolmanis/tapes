import contextlib
from time import time

from .message import Message


class TimerProxy(object):
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    @contextlib.contextmanager
    def time(self):
        start_time = time()
        try:
            yield
        finally:
            end_time = time()
            self.socket.send_pyobj(Message('timer', self.name, end_time - start_time))
