from . import distributed_logger
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class MetricsProxy(object):
    def __init__(self, socket):
        self.socket = socket

    def send(self, message):
        distributed_logger.debug('Sending message %s', message)
        self.socket.send_pyobj(message)
