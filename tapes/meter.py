from __future__ import division
from time import time

from .average import EWMA
from .stats import Stat


_INTERVAL = 5.0


class Meter(Stat):
    def __init__(self):
        self.last_tick = time()
        self.count = 0
        self.m1 = EWMA.one()
        self.m5 = EWMA.five()
        self.m15 = EWMA.fifteen()

    def mark(self, n=1):
        self._tick_if_needed()
        self.count += n
        self.m1.update(n)
        self.m5.update(n)
        self.m15.update(n)

    def _get_one_minute(self):
        self._tick_if_needed()
        return self.m1.get_rate()

    def _get_five_minute(self):
        self._tick_if_needed()
        return self.m5.get_rate()

    def _get_fifteen_minute(self):
        self._tick_if_needed()
        return self.m15.get_rate()

    def _tick_if_needed(self):
        old_tick = self.last_tick
        new_tick = time()
        age = new_tick - old_tick
        if age > _INTERVAL:
            new_interval_start_tick = new_tick - age % _INTERVAL
            self.last_tick = new_interval_start_tick
            required_ticks = int(age // _INTERVAL)
            for _ in range(required_ticks):
                self.m1.tick()
                self.m5.tick()
                self.m15.tick()

    def get_values(self):
        return {
            'count': self.count,
            'm1': self._get_one_minute(),
            'm5': self._get_five_minute(),
            'm15': self._get_fifteen_minute(),
        }
