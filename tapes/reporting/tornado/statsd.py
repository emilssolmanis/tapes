from tornado import gen

from . import TornadoScheduledReporter
from ..statsd import StatsdReporter


class TornadoStatsdReporter(StatsdReporter, TornadoScheduledReporter):
    """Reports to StatsD using an IOLoop for scheduling"""
    @gen.coroutine
    def report(self):
        super(TornadoStatsdReporter, self).report()
