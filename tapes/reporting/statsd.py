from __future__ import absolute_import
import logging

import statsd

from . import ScheduledReporter, reporting_logger
from ..local.meter import Meter
from ..local.timer import Timer
from ..local.gauge import Gauge
from ..local.counter import Counter
from ..local.histogram import Histogram


class StatsdReporter(ScheduledReporter):
    """Reporter for StatsD."""
    def __init__(self, interval, host='localhost', port=8125, prefix=None, registry=None):
        """
        :param interval: a timedelta, how often metrics are reported
        :param host: the statsd host
        :param port: the statsd port
        :param prefix: the statsd prefix to use
        :param registry: the registry to report on, defaults to the global one
        """
        super(StatsdReporter, self).__init__(interval, registry)
        self.statsd_client = statsd.StatsClient(host, port, prefix)

    def _report_meter(self, name, meter):
        stats = meter.get_values()
        self.statsd_client.gauge('{}.total'.format(name), stats['count'])
        self.statsd_client.timing('{}.m1_rate'.format(name), stats['m1'])
        self.statsd_client.timing('{}.m5_rate'.format(name), stats['m5'])
        self.statsd_client.timing('{}.m15_rate'.format(name), stats['m15'])

    def _report_timer(self, name, timer):
        stats = timer.get_values()
        self.statsd_client.gauge('{}.total'.format(name), stats['count'])
        self.statsd_client.timing('{}.m1_rate'.format(name), stats['m1'])
        self.statsd_client.timing('{}.m5_rate'.format(name), stats['m5'])
        self.statsd_client.timing('{}.m15_rate'.format(name), stats['m15'])
        # statsd wants millis, this is in seconds internally
        self.statsd_client.timing('{}.min'.format(name), stats['min'] * 1000)
        self.statsd_client.timing('{}.max'.format(name), stats['max'] * 1000)
        self.statsd_client.timing('{}.mean'.format(name), stats['mean'] * 1000)
        self.statsd_client.timing('{}.stddev'.format(name), stats['stddev'] * 1000)
        self.statsd_client.timing('{}.q50'.format(name), stats['q50'] * 1000)
        self.statsd_client.timing('{}.q75'.format(name), stats['q75'] * 1000)
        self.statsd_client.timing('{}.q98'.format(name), stats['q98'] * 1000)
        self.statsd_client.timing('{}.q99'.format(name), stats['q99'] * 1000)
        self.statsd_client.timing('{}.q999'.format(name), stats['q999'] * 1000)

    def _report_gauge(self, name, gauge):
        stats = gauge.get_values()
        self.statsd_client.gauge('{}.value'.format(name), stats['value'])

    def _report_counter(self, name, counter):
        stats = counter.get_values()
        self.statsd_client.incr('{}.value'.format(name), stats['value'])

    def _report_histogram(self, name, histogram):
        stats = histogram.get_values()
        self.statsd_client.gauge('{}.total'.format(name), stats['count'])
        self.statsd_client.timing('{}.min'.format(name), stats['min'])
        self.statsd_client.timing('{}.max'.format(name), stats['max'])
        self.statsd_client.timing('{}.mean'.format(name), stats['mean'])
        self.statsd_client.timing('{}.stddev'.format(name), stats['stddev'])
        self.statsd_client.timing('{}.q50'.format(name), stats['q50'])
        self.statsd_client.timing('{}.q75'.format(name), stats['q75'])
        self.statsd_client.timing('{}.q98'.format(name), stats['q98'])
        self.statsd_client.timing('{}.q99'.format(name), stats['q99'])
        self.statsd_client.timing('{}.q999'.format(name), stats['q999'])

    def _talk_this_way(self, name, thing):
        if isinstance(thing, Meter):
            self._report_meter(name, thing)
        elif isinstance(thing, Timer):
            self._report_timer(name, thing)
        elif isinstance(thing, Gauge):
            self._report_gauge(name, thing)
        elif isinstance(thing, Counter):
            self._report_counter(name, thing)
        elif isinstance(thing, Histogram):
            self._report_histogram(name, thing)
        else:
            raise ValueError('No clue what a {} is'.format(type(thing)))

    def _walk_this_way(self, stats, curr_name=''):
        try:
            for k, v in stats.items():
                self._walk_this_way(v, '{}.{}'.format(curr_name, k) if curr_name else k)
        except AttributeError:
            self._talk_this_way(curr_name, stats)

    def report(self):
        if reporting_logger.isEnabledFor(logging.DEBUG):
            reporting_logger.debug('Reporting to StatsD %s', self.registry.get_stats())
        self._walk_this_way(self.registry.stats, '')
