from tapes.reservoir import ExponentiallyDecayingReservoir
from .stats import Stat


class Histogram(Stat):
    def __init__(self):
        self.count = 0
        self.reservoir = ExponentiallyDecayingReservoir()

    def update(self, value):
        self.count += 1
        self.reservoir.update(value)

    def get_values(self):
        snapshot = self.reservoir.get_snapshot()
        return {
            'count': self.count,
            'min': snapshot.get_min(),
            'max': snapshot.get_max(),
            'mean': snapshot.get_mean(),
            'stddev': snapshot.get_sd(),
            'q50': snapshot.get_quantile(0.5),
            'q75': snapshot.get_quantile(0.75),
            'q95': snapshot.get_quantile(0.95),
            'q98': snapshot.get_quantile(0.98),
            'q99': snapshot.get_quantile(0.99),
            'q999': snapshot.get_quantile(0.999),
        }
