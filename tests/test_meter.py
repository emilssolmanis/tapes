import unittest
import fudge
from tapes.registry import Registry


class MeterTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    @fudge.patch('tapes.meter.time')
    def test_meter_count_works(self, time):
        (time
         # initialize Meter
         .expects_call().returns(1.0)
         # mark()
         .next_call().returns(6.0)
         # mark()
         .next_call().returns(12.0)
         # mark()
         .next_call().returns(20.0)
         # get_stats()
         .next_call().returns(20.0)
         .next_call().returns(20.0)
         .next_call().returns(20.0))

        meter = self.registry.meter('MeterTestCase.test_meter_count_works')

        meter.mark()
        meter.mark()
        meter.mark()

        stats = self.registry.get_stats()

        assert stats.MeterTestCase.test_meter_count_works.count == 3
        assert stats.MeterTestCase.test_meter_count_works.m1 > 0
        assert stats.MeterTestCase.test_meter_count_works.m5 > 0
        assert stats.MeterTestCase.test_meter_count_works.m15 > 0
