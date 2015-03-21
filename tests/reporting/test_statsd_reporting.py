from __future__ import print_function
from datetime import timedelta
from time import sleep
import fudge
from fudge.inspector import arg

from tapes.reporting.statsd import StatsdReporter
from tests.local.base import StatsTest


def is_within(delta):
    class _(object):
        def of(self, expected_value):
            def _check(value):
                return abs(value - expected_value) < delta
            return arg.passes_test(_check)

    return _()


is_float = arg.passes_test(lambda x: isinstance(x, float))


class StatsdReportingTestCase(StatsTest):
    @fudge.patch('statsd.StatsClient', 'tapes.local.meter.time')
    def test_statsd_reporter_periodically_sends_meter_stats_to_statsd(self, StatsClient, time):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 5)
                    .expects('timing').with_args('some.path.m1_rate', is_within(0.5).of(1.0))
                    .expects('timing').with_args('some.path.m5_rate', is_within(0.5).of(1.0))
                    .expects('timing').with_args('some.path.m15_rate', is_within(0.5).of(1.0)))
        (time.expects_call().returns(1.0)  # initialize Meter
             .next_call().returns(2.0)  # mark()
             .next_call().returns(3.0)  # mark()
             .next_call().returns(3.0)  # mark()
             .next_call().returns(3.0)  # mark()
             .next_call().returns(4.0)  # mark()
             .next_call().returns(21.0)  # get_stats()
             .next_call().returns(21.0)  # get_stats()
             .next_call().returns(21.0))  # get_stats()

        meter = self.registry.meter('some.path')
        meter.mark()
        meter.mark()
        meter.mark()
        meter.mark()
        meter.mark()

        reporter = StatsdReporter(timedelta(milliseconds=500), registry=self.registry)
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_timer_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 4)
                    .expects('timing').with_args('some.path.m1_rate', is_float)
                    .expects('timing').with_args('some.path.m5_rate', is_float)
                    .expects('timing').with_args('some.path.m15_rate', is_float)
                    .expects('timing').with_args('some.path.min', is_within(0.1).of(19e3))
                    .expects('timing').with_args('some.path.max', is_within(0.1).of(21e3))
                    .expects('timing').with_args('some.path.mean', is_within(0.1).of(20e3))
                    .expects('timing').with_args('some.path.stddev', is_within(300).of(1e3))
                    .expects('timing').with_args('some.path.q50', is_within(2000).of(20e3))
                    .expects('timing').with_args('some.path.q75', is_within(2000).of(20e3))
                    .expects('timing').with_args('some.path.q98', is_within(2000).of(20e3))
                    .expects('timing').with_args('some.path.q99', is_within(2000).of(20e3))
                    .expects('timing').with_args('some.path.q999', is_within(2000).of(20e3)))

        timer = self.registry.timer('some.path')
        timer.update(19.0)
        timer.update(20.0)
        timer.update(20.0)
        timer.update(21.0)

        reporter = StatsdReporter(timedelta(milliseconds=500), registry=self.registry)
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_gauge_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.value', 42))

        self.registry.gauge('some.path', lambda: 42)

        reporter = StatsdReporter(timedelta(milliseconds=500), registry=self.registry)
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

        reporter = StatsdReporter(timedelta(milliseconds=500), registry=self.registry)
        reporter.start()
        sleep(0.2)
        reporter.stop()

    @fudge.patch('statsd.StatsClient')
    def test_statsd_reporter_periodically_sends_histogram_stats_to_statsd(self, StatsClient):
        (StatsClient.expects_call().with_args('localhost', 8125, None)
                    .returns_fake()
                    .expects('gauge').with_args('some.path.count', 3)
                    .expects('timing').with_args('some.path.min', is_within(0.1).of(3))
                    .expects('timing').with_args('some.path.max', is_within(0.1).of(5))
                    .expects('timing').with_args('some.path.mean', is_within(0.1).of(4))
                    .expects('timing').with_args('some.path.stddev', is_within(0.3).of(1))
                    .expects('timing').with_args('some.path.q50', is_within(1.01).of(4))
                    .expects('timing').with_args('some.path.q75', is_within(1.01).of(4))
                    .expects('timing').with_args('some.path.q98', is_within(1.01).of(4))
                    .expects('timing').with_args('some.path.q99', is_within(1.01).of(4))
                    .expects('timing').with_args('some.path.q999', is_within(1.01).of(4)))

        histogram = self.registry.histogram('some.path')
        histogram.update(3.0)
        histogram.update(4.0)
        histogram.update(5.0)

        reporter = StatsdReporter(timedelta(milliseconds=500), registry=self.registry)
        reporter.start()
        sleep(0.2)
        reporter.stop()
