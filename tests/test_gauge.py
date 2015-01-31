import unittest

from tapes.registry import Registry


class GaugeTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_gauge_works(self):
        fugly_hack = {'i': 0}

        def _gauge_value():
            fugly_hack['i'] += 1
            return fugly_hack['i']

        self.registry.gauge('GaugeTestCase.test_gauge_works', _gauge_value)

        stats = self.registry.get_stats()
        assert stats.GaugeTestCase.test_gauge_works.value == 1

        stats = self.registry.get_stats()
        assert stats.GaugeTestCase.test_gauge_works.value == 2
