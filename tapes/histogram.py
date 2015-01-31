from .reservoir import ExponentiallyDecayingReservoir


class Histogram(object):
    def __init__(self):
        self.count = 0
        self.reservoir = ExponentiallyDecayingReservoir()

    def update(self, value):
        self.count += 1
        self.reservoir.update(value)

    def get_snapshot(self):
        return self.reservoir.get_snapshot()
