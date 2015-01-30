import unittest
from tapes.registry import Registry


class MeterTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_meter_count_works(self):
        meter = self.registry.meter('MeterTestCase.test_meter_count_works')

        meter.mark()
        meter.mark()
        meter.mark()

        stats = self.registry.get_stats()
        assert stats.MeterTestCase.test_meter_count_works.count == 3
