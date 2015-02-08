from .stats import Stat


class Counter(Stat):
    def __init__(self):
        self.count = 0

    def get_values(self):
        return {
            'value': self.count
        }

    def increment(self, n=1):
        self.count += n

    def decrement(self, n=1):
        self.count -= n
