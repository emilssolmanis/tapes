import functools
from multiprocessing import Process
import os

from addict import Dict

from .local.meter import Meter
from .local.counter import Counter
from .local.gauge import Gauge
from .local.histogram import Histogram
from .local.timer import Timer
from .proxy.meter import MeterProxy
from .proxy.counter import CounterProxy
from .proxy.gauge import GaugeProxy
from .proxy.timer import TimerProxy
from .proxy.histogram import HistogramProxy
from tapes.proxy.message import Message


class Registry(object):
    def __init__(self):
        self.stats = dict()

    def _get_or_add_stat(self, name, stat_factory):
        path_parts = name.split('.')
        path, stat_name = path_parts[:-1], path_parts[-1]

        stats = self.stats
        for p in path:
            try:
                stats = stats[p]
            except KeyError:
                new_dict = dict()
                stats[p] = new_dict
                stats = new_dict

        try:
            return stats[stat_name]
        except KeyError:
            stat = stat_factory()
            stats[stat_name] = stat
            return stat

    def meter(self, name):
        return self._get_or_add_stat(name, Meter)

    def timer(self, name):
        return self._get_or_add_stat(name, Timer)

    def gauge(self, name, producer):
        return self._get_or_add_stat(name, functools.partial(Gauge, producer))

    def counter(self, name):
        return self._get_or_add_stat(name, Counter)

    def histogram(self, name):
        return self._get_or_add_stat(name, Histogram)

    def get_stats(self):
        def _get_value(stats):
            try:
                return Dict((k, _get_value(v)) for k, v in stats.items())
            except AttributeError:
                return Dict(stats.get_values())

        return _get_value(self.stats)


def registry_aggregator():
    print('subbing PID %s' % os.getpid())
    import zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("ipc://somestuff.ipc")
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')
    registry = Registry()
    print('subbed PID %s' % os.getpid())

    while True:
        type_, name, value = socket.recv_json()
        print('handling in PID %s' % os.getpid(), type_, name, value)

        if type_ == 'meter':
            registry.meter(name).mark(value)
        elif type_ == 'timer':
            registry.timer(name).update(value)
        elif type_ == 'counter':
            registry.counter(name).increment(value)
        elif type_ == 'histogram':
            registry.histogram(name).update(value)
        elif type_ == 'dump':
            # socket.send_json(registry.get_stats())
            print(registry.get_stats())


class DistributedRegistry(object):
    def __init__(self):
        self.stats = dict()
        print('constructing registry in %s' % os.getpid())
        import zmq
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("ipc://somestuff.ipc")
        self.socket = socket
        print('constructed registry in %s' % os.getpid())

    def _get_or_add_stat(self, name, stat_factory):
        path_parts = name.split('.')
        path, stat_name = path_parts[:-1], path_parts[-1]

        stats = self.stats
        for p in path:
            try:
                stats = stats[p]
            except KeyError:
                new_dict = dict()
                stats[p] = new_dict
                stats = new_dict

        try:
            return stats[stat_name]
        except KeyError:
            stat = stat_factory()
            stats[stat_name] = stat
            return stat

    def meter(self, name):
        return self._get_or_add_stat(name, functools.partial(MeterProxy, self.socket, name))

    def timer(self, name):
        return self._get_or_add_stat(name, functools.partial(TimerProxy, self.socket, name))

    def gauge(self, name, producer):
        return self._get_or_add_stat(name, functools.partial(GaugeProxy, producer, self.socket, name))

    def counter(self, name):
        return self._get_or_add_stat(name, functools.partial(CounterProxy, self.socket, name))

    def histogram(self, name):
        return self._get_or_add_stat(name, functools.partial(HistogramProxy, self.socket, name))

    def get_stats(self):
        self.socket.send_json(Message('dump', 'no_name', 0))
        return self.socket.recv_json()
