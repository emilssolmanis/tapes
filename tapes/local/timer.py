import contextlib
from time import time

from .meter import Meter
from .stats import Stat
from .histogram import Histogram


class Timer(Stat):
    def __init__(self):
        self.count = 0
        self.meter = Meter()
        self.histogram = Histogram()
        super(Timer, self).__init__()

    @contextlib.contextmanager
    def time(self):
        start_time = time()
        try:
            yield
        finally:
            self.update(time() - start_time)

    def update(self, value):
        self.meter.mark()
        self.histogram.update(value)

    def get_values(self):
        values = self.meter.get_values()
        values.update(self.histogram.get_values())
        return values
