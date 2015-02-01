import unittest
from tapes.registry import Registry


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
