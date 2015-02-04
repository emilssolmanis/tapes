import contextlib
import os
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
            print('timing from PID %s' % os.getpid())
            end_time = time()
            self.socket.send_json(Message('timer', self.name, end_time - start_time))
