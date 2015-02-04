from .message import Message


class HistogramProxy(object):
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def update(self, value):
        self.socket.send_json(Message('histogram', self.name, value))
