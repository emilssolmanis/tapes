import contextlib
from time import time

from .meter import Meter
from .stats import Stat
from .reservoir import ExponentiallyDecayingReservoir


class Timer(Stat):
    def __init__(self):
        self.count = 0
        self.meter = Meter()
        self.reservoir = ExponentiallyDecayingReservoir()
        super(Timer, self).__init__()

    @contextlib.contextmanager
    def time(self):
        start_time = time()
        self.meter.mark()

        try:
            yield
        finally:
            end_time = time()
            self.reservoir.update(end_time - start_time)

    def get_values(self):
        values = self.meter.get_values()
        snapshot = self.reservoir.get_snapshot()
        values.update({
            'min': snapshot.get_min(),
            'max': snapshot.get_max(),
            'mean': snapshot.get_mean(),
            'median': snapshot.get_quantile(0.5),
            'stddev': snapshot.get_sd(),
            'q75': snapshot.get_quantile(0.75),
            'q95': snapshot.get_quantile(0.95),
            'q98': snapshot.get_quantile(0.98),
            'q99': snapshot.get_quantile(0.99),
            'q999': snapshot.get_quantile(0.999),
        })
        return values
