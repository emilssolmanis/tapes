from __future__ import division
from math import exp

_INTERVAL = 5.0
_SECONDS_PER_MINUTE = 60.0

_M1_ALPHA = 1 - exp(-_INTERVAL / _SECONDS_PER_MINUTE / 1)
_M5_ALPHA = 1 - exp(-_INTERVAL / _SECONDS_PER_MINUTE / 5)
_M15_ALPHA = 1 - exp(-_INTERVAL / _SECONDS_PER_MINUTE / 15)


class EWMA(object):
    @classmethod
    def one(cls):
        return EWMA(_M1_ALPHA, _INTERVAL)

    @classmethod
    def five(cls):
        return EWMA(_M5_ALPHA, _INTERVAL)

    @classmethod
    def fifteen(cls):
        return EWMA(_M15_ALPHA, _INTERVAL)

    def __init__(self, alpha, interval):
        self.alpha = alpha
        self.interval = interval
        self.rate = 0.0
        self.uncounted = 0

    def get_rate(self):
        return self.rate

    def update(self, n):
        self.uncounted += n

    def _tick_uninitialized(self):
        count = self.uncounted
        self.uncounted = 0
        instant_rate = count / self.interval
        self.rate = instant_rate
        self.tick = self._tick_initialized

    def _tick_initialized(self):
        count = self.uncounted
        self.uncounted = 0
        instant_rate = count / self.interval
        self.rate += (self.alpha * (instant_rate - self.rate))

    tick = _tick_uninitialized
