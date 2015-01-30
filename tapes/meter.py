class Meter(object):
    def __init__(self):
        self.count = 0

    def mark(self):
        self.count += 1

    def get_values(self):
        return {
            'count': self.count,
            'm1': 0.0,
            'm5': 0.0,
            'm15': 0.0,
        }
