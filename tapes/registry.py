import functools
from addict import Dict

from .meter import Meter
from .counter import Counter
from .gauge import Gauge
from .histogram import Histogram
from .timer import Timer


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
                return Dict({k: _get_value(v) for k, v in stats.items()})
            except AttributeError:
                return Dict(stats.get_values())

        return _get_value(self.stats)
