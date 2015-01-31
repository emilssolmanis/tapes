from addict import Dict

from .meter import Meter
from .timer import Timer


class Registry(object):
    def __init__(self):
        self.stats = dict()

    def _add_stat(self, name, stat_factory):
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
        return self._add_stat(name, Meter)

    def timer(self, name):
        return self._add_stat(name, Timer)

    def get_stats(self):
        def _get_value(stats):
            try:
                return Dict({k: _get_value(v) for k, v in stats.items()})
            except AttributeError:
                return Dict(stats.get_values())

        return _get_value(self.stats)
