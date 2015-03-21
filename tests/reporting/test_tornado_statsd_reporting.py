from datetime import timedelta

import fudge
from tornado import gen, testing

from tapes.registry import Registry
from tapes.reporting.tornado.statsd import TornadoStatsdReporter


class TornadoStatsdReportingTestCase(testing.AsyncTestCase):
    @testing.gen_test
    @fudge.patch('statsd.StatsClient')
    def test_tornado_statsd_reporter_works(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('incr').with_args('some.path.value', 22))

        registry = Registry()

        counter = registry.counter('some.path')
        counter.increment(5)
        counter.increment(20)
        counter.decrement(3)

        reporter = TornadoStatsdReporter(timedelta(milliseconds=500), registry=registry)
        reporter.start()
        yield gen.sleep(0.2)
        reporter.stop()
