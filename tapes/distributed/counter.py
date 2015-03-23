from .message import Message


class CounterProxy(object):
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def increment(self, n=1):
        self.socket.send_pyobj(Message('counter', self.name, n))

    def decrement(self, n=1):
        self.socket.send_pyobj(Message('counter', self.name, -n))
