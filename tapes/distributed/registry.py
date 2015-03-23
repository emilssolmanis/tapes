from multiprocessing import Process
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
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(socket_addr)
    socket.set_hwm(0)
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')
    registry = Registry()

    reporter.registry = registry
    reporter.start()

    while True:
        type_, name, value = socket.recv_pyobj()

        if type_ == 'meter':
            registry.meter(name).mark(value)
        elif type_ == 'timer':
            registry.timer(name).update(value)
        elif type_ == 'counter':
            registry.counter(name).increment(value)
        elif type_ == 'histogram':
            registry.histogram(name).update(value)
        elif type_ == 'shutdown':
            reporter.stop()
            socket.unbind(socket_addr)
            socket.close()
            context.destroy()


class RegistryAggregator(object):
    """Aggregates multiple registry proxies and reports on the unified metrics."""
    def __init__(self, reporter, socket_addr=_DEFAULT_IPC):
        """Constructs a metrics registry aggregator.

        The ``registry`` field on the ``reporter`` argument will be reset to an implementation instance prior to
        calling ``start()``. Any previously set registry is not guaranteed to be used.

        :param reporter: the reporter to use
        :param socket_addr: the 0MQ socket address; has to be the same as corresponding proxies'
        """
        super(RegistryAggregator, self).__init__()
        self.socket_addr = socket_addr
        self.reporter = reporter
        self.process = None

    def start(self, fork=True):
        """Starts the registry aggregator.

        :param fork: whether to fork a process; if ``False``, blocks and stays in the existing process
        """
        if not fork:
            _registry_aggregator(self.reporter, self.socket_addr)
        else:
            p = Process(target=_registry_aggregator, args=(self.reporter, self.socket_addr, ))
            p.start()
            self.process = p

    def stop(self):
        """Terminates the forked process.

        Only valid if started as a fork, because... well you wouldn't get here otherwise.
        :return:
        """
        self.process.terminate()
        self.process.join()


class DistributedRegistry(BaseRegistry):
    """A registry proxy that pushes metrics data to a ``RegistryAggregator``."""
    def __init__(self, socket_addr=_DEFAULT_IPC):
        """
        :param socket_addr: the 0MQ IPC socket address; has to be the same as corresponding aggregator's
        """
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
        """Connects to the 0MQ socket and starts publishing."""
        self.zmq_context = zmq.Context()
        sock = self.zmq_context.socket(zmq.PUB)
        sock.set_hwm(0)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(self.socket_addr)

        def _reset_socket(values):
            for value in values:
                try:
                    _reset_socket(value.values())
                except AttributeError:
                    value.socket = sock

        _reset_socket(self.stats.values())
        self.socket = sock

    def close(self):
        self.socket.send_pyobj(Message('shutdown', 'noname', -1))
        self.socket.disconnect(self.socket_addr)
        self.socket.close()
        self.zmq_context.destroy()
