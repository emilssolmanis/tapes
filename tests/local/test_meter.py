import unittest

import fudge

from tapes.registry import Registry


class MeterTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    @fudge.patch('tapes.local.meter.time')
    def test_meter_count_works(self, time):
        (time
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

        meter = self.registry.meter('MeterTestCase.test_meter_count_works')

        meter.mark()
        meter.mark()
        meter.mark()

        stats = self.registry.get_stats()

        meter_stats = stats.MeterTestCase.test_meter_count_works
        assert meter_stats.count == 3
        assert float(meter_stats.m1) > 0
        assert float(meter_stats.m5) > 0
        assert float(meter_stats.m15) > 0
