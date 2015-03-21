from tornado import gen

from . import TornadoScheduledReporter
from ..statsd import StatsdReporter


class TornadoStatsdReporter(StatsdReporter, TornadoScheduledReporter):
    @gen.coroutine
    def report(self):
        super(TornadoStatsdReporter, self).report()
