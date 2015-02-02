from time import sleep
import fudge

from tests.base import StatsTest


class TimerTestCase(StatsTest):
    @fudge.patch('tapes.meter.time')
    def test_timer_has_meter(self, meter_time):
        (meter_time
         # initialize Meter
         .expects_call().returns(1.0)
         # mark()
         .next_call().returns(60.0)
         # mark()
         .next_call().returns(5 * 60.0)
         # mark()
         .next_call().returns(15 * 60.0)
         # get_stats()
         .next_call().returns(15 * 60.0)
         .next_call().returns(15 * 60.0)
         .next_call().returns(15 * 60.0))

        timer = self.registry.timer('TimerTestCase.test_timer_has_meter')

        with timer.time():
            pass

        with timer.time():
            pass

        with timer.time():
            pass

        stats = self.registry.get_stats()

        meter_stats = stats.TimerTestCase.test_timer_has_meter
        assert meter_stats.count == 3
        assert float(meter_stats.m1) > 0
        assert float(meter_stats.m5) > 0
        assert float(meter_stats.m15) > 0

    def test_timer_times_execution_histogram(self):
        timer = self.registry.timer('TimerTestCase.test_timer_times_execution_histogram')

        sleep_time = 0.005

        def _run_for_fun():
            with timer.time():
                sleep(sleep_time)

        for _ in range(100):
            _run_for_fun()

        stats = self.registry.get_stats()
        timer_stats = stats.TimerTestCase.test_timer_times_execution_histogram

        assert abs(float(timer_stats.mean) - sleep_time) < 0.0005
        assert float(timer_stats.stddev) > 0
        assert float(timer_stats.min) > 0
        assert float(timer_stats.max) > 0

        assert float(timer_stats.q50) > 0
        assert float(timer_stats.q75) > 0
        assert float(timer_stats.q95) > 0
        assert float(timer_stats.q98) > 0
        assert float(timer_stats.q99) > 0
        assert float(timer_stats.q999) > 0
