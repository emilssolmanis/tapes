from __future__ import print_function
from datetime import timedelta
from time import sleep
import fudge
from fudge.inspector import arg

from tapes.reporting.statsd import StatsdReporter
from tests.local.base import StatsTest


class StatsdReportingTestCase(StatsTest):
    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_meter_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 2)
                    .expects('timing').with_args('some.path.m1_rate', arg.passes_test(lambda x: isinstance(x, float)))
                    .expects('timing').with_args('some.path.m5_rate', arg.passes_test(lambda x: isinstance(x, float)))
                    .expects('timing').with_args('some.path.m15_rate', arg.passes_test(lambda x: isinstance(x, float))))

        meter = self.registry.meter('some.path')
        meter.mark()
        meter.mark()

        reporter = StatsdReporter(self.registry, timedelta(milliseconds=500))
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_timer_stats_to_statsd(self, StatsClient):
        is_float = arg.passes_test(lambda x: isinstance(x, float))
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 3)
                    .expects('timing').with_args('some.path.m1_rate', is_float)
                    .expects('timing').with_args('some.path.m5_rate', is_float)
                    .expects('timing').with_args('some.path.m15_rate', is_float)
                    .expects('timing').with_args('some.path.min', is_float)
                    .expects('timing').with_args('some.path.max', is_float)
                    .expects('timing').with_args('some.path.mean', is_float)
                    .expects('timing').with_args('some.path.stddev', is_float)
                    .expects('timing').with_args('some.path.q50', is_float)
                    .expects('timing').with_args('some.path.q75', is_float)
                    .expects('timing').with_args('some.path.q98', is_float)
                    .expects('timing').with_args('some.path.q99', is_float)
                    .expects('timing').with_args('some.path.q999', is_float))

        timer = self.registry.timer('some.path')
        timer.update(5.0)
        timer.update(20.0)
        timer.update(3.0)

        reporter = StatsdReporter(self.registry, timedelta(milliseconds=500))
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_gauge_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.value', 42))

        self.registry.gauge('some.path', lambda: 42)

        reporter = StatsdReporter(self.registry, timedelta(milliseconds=500))
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_counter_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('incr').with_args('some.path.value', 22))

        counter = self.registry.counter('some.path')
        counter.increment(5)
        counter.increment(20)
        counter.decrement(3)

        reporter = StatsdReporter(self.registry, timedelta(milliseconds=500))
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_histogram_stats_to_statsd(self, StatsClient):
        is_float = arg.passes_test(lambda x: isinstance(x, float))
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 3)
                    .expects('timing').with_args('some.path.min', is_float)
                    .expects('timing').with_args('some.path.max', is_float)
                    .expects('timing').with_args('some.path.mean', is_float)
                    .expects('timing').with_args('some.path.stddev', is_float)
                    .expects('timing').with_args('some.path.q50', is_float)
                    .expects('timing').with_args('some.path.q75', is_float)
                    .expects('timing').with_args('some.path.q98', is_float)
                    .expects('timing').with_args('some.path.q99', is_float)
                    .expects('timing').with_args('some.path.q999', is_float))

        histogram = self.registry.histogram('some.path')
        histogram.update(3.0)
        histogram.update(4.0)
        histogram.update(5.0)

        reporter = StatsdReporter(self.registry, timedelta(milliseconds=500))
        reporter.start()
        sleep(0.2)
        reporter.stop()
