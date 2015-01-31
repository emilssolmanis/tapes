import unittest

from tapes.registry import Registry


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_multiple_meter_calls_with_same_name_return_same_instance(self):
        meter1 = self.registry.meter('lol.hurr.durr.Meter')
        meter2 = self.registry.meter('lol.hurr.durr.Meter')
        assert id(meter1) == id(meter2)

    def test_multiple_timer_calls_with_same_name_return_same_instance(self):
        timer1 = self.registry.timer('lol.hurr.durr.Timer')
        timer2 = self.registry.timer('lol.hurr.durr.Timer')
        assert id(timer1) == id(timer2)
