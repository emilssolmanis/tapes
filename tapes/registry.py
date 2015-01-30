from addict import Dict
from tapes.meter import Meter


class Registry(object):
    def __init__(self):
        super(Registry, self).__init__()
        self.stats = dict()

    def meter(self, name):
        stat = Meter()

        path_parts = name.split('.')
        path, meter_name = path_parts[:-1], path_parts[-1]

        stats = self.stats
        for p in path:
            try:
                stats = stats[p]
            except KeyError:
                new_dict = dict()
                stats[p] = new_dict
                stats = new_dict

        stats[meter_name] = stat

        return stat

    def get_stats(self):
        def _get_value(stats):
            try:
                return Dict({k: _get_value(v) for k, v in stats.items()})
            except AttributeError:
                return Dict(stats.get_values())

        return _get_value(self.stats)
