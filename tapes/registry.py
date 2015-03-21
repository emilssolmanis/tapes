import functools
import abc

from addict import Dict

from .local.meter import Meter
from .local.counter import Counter
from .local.gauge import Gauge
from .local.histogram import Histogram
from .local.timer import Timer


class BaseRegistry(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(BaseRegistry, self).__init__()
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

    @abc.abstractmethod
    def meter(self, name):
        raise NotImplementedError()

    @abc.abstractmethod
    def timer(self, name):
        raise NotImplementedError()

    @abc.abstractmethod
    def gauge(self, name, producer):
        raise NotImplementedError()

    @abc.abstractmethod
    def counter(self, name):
        raise NotImplementedError()

    @abc.abstractmethod
    def histogram(self, name):
        raise NotImplementedError()


class Registry(BaseRegistry):
    """Factory and storage location for all metrics stuff.

    Use producer methods to create metrics. Metrics are hierarchical, the names are split on '.'.
    """

    def meter(self, name):
        """Creates or gets an existing meter.

        :param name: The name
        :return: The created or existing meter for the given name
        """
        return self._get_or_add_stat(name, Meter)

    def timer(self, name):
        """Creates or gets an existing timer.

        :param name: The name
        :return: The created or existing timer for the given name
        """
        return self._get_or_add_stat(name, Timer)

    def gauge(self, name, producer):
        """Creates or gets an existing gauge.

        :param name: The name
        :return: The created or existing gauge for the given name
        """
        return self._get_or_add_stat(name, functools.partial(Gauge, producer))

    def counter(self, name):
        """Creates or gets an existing counter.

        :param name: The name
        :return: The created or existing counter for the given name
        """
        return self._get_or_add_stat(name, Counter)

    def histogram(self, name):
        """Creates or gets an existing histogram.

        :param name: The name
        :return: The created or existing histogram for the given name
        """
        return self._get_or_add_stat(name, Histogram)

    def get_stats(self):
        """Retrieves the current values of the metrics associated with this registry, formatted as a dict.

        The metrics form a hierarchy, their names are split on '.'. The returned dict is an `addict`, so you can
        use it as either a regular dict or via attributes, e.g.,

        >>> import tapes
        >>> registry = tapes.Registry()
        >>> timer = registry.timer('my.timer')
        >>> stats = registry.get_stats()
        >>> print(stats['my']['timer']['count'])
        0
        >>> print(stats.my.timer.count)
        0

        :return: The values of the metrics associated with this registry
        """
        def _get_value(stats):
            try:
                return Dict((k, _get_value(v)) for k, v in stats.items())
            except AttributeError:
                return Dict(stats.get_values())

        return _get_value(self.stats)
