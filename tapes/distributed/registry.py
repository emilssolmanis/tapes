from multiprocessing import Process
from threading import Thread
import functools

import zmq

from ..registry import Registry, BaseRegistry
from .meter import MeterProxy
from .counter import CounterProxy
from .message import Message
from .timer import TimerProxy
from .histogram import HistogramProxy


_DEFAULT_IPC = 'ipc://tapes_metrics.ipc'


def _registry_aggregator(reporter, socket_addr):
    context = zmq.Context().instance()
    socket = context.socket(zmq.SUB)
    socket.bind(socket_addr)
    socket.set_hwm(0)
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')
    registry = Registry()

    reporter_thread = Thread(target=reporter, args=(registry, ))
    reporter_thread.start()

    while True:
        type_, name, value = socket.recv_json()

        if type_ == 'meter':
            registry.meter(name).mark(value)
        elif type_ == 'timer':
            registry.timer(name).update(value)
        elif type_ == 'counter':
            registry.counter(name).increment(value)
        elif type_ == 'histogram':
            registry.histogram(name).update(value)
        elif type_ == 'shutdown':
            socket.unbind(socket_addr)
            socket.close()
            context.destroy()


class RegistryAggregator(object):
    def __init__(self, reporter, socket_addr=_DEFAULT_IPC):
        super(RegistryAggregator, self).__init__()
        self.socket_addr = socket_addr
        self.reporter = reporter
        self.process = None

    def start(self, fork=True):
        if not fork:
            _registry_aggregator(self.reporter, self.socket_addr)
        else:
            p = Process(target=_registry_aggregator, args=(self.reporter, self.socket_addr, ))
            p.start()
            self.process = p

    def stop(self):
        self.process.terminate()
        self.process.join()


class DistributedRegistry(BaseRegistry):
    def __init__(self, socket_addr=_DEFAULT_IPC):
        super(DistributedRegistry, self).__init__()
        self.stats = dict()
        self.socket_addr = socket_addr
        self.zmq_context = None
        self.socket = None

    def meter(self, name):
        return self._get_or_add_stat(name, functools.partial(MeterProxy, self.socket, name))

    def timer(self, name):
        return self._get_or_add_stat(name, functools.partial(TimerProxy, self.socket, name))

    def gauge(self, name, producer):
        raise NotImplementedError('Gauge is unavailable in distributed mode')

    def counter(self, name):
        return self._get_or_add_stat(name, functools.partial(CounterProxy, self.socket, name))

    def histogram(self, name):
        return self._get_or_add_stat(name, functools.partial(HistogramProxy, self.socket, name))

    def connect(self):
        self.zmq_context = zmq.Context().instance()
        socket = self.zmq_context.socket(zmq.PUB)
        socket.set_hwm(0)
        socket.connect(self.socket_addr)

        def _reset_socket(values):
            for value in values:
                try:
                    _reset_socket(value.values())
                except AttributeError:
                    value.socket = socket

        _reset_socket(self.stats.values())
        self.socket = socket

    def close(self):
        self.socket.send_json(Message('shutdown', 'noname', -1))
        self.socket.disconnect(self.socket_addr)
        self.zmq_context.destroy()
