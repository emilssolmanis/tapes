from .stats import Stat


class Gauge(Stat):
    def __init__(self, producer):
        self.producer = producer

    def get_values(self):
        return {
            'value': self.producer()
        }
