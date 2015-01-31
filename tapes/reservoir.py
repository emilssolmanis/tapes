from bisect import bisect
from operator import attrgetter
from random import random
from six.moves import map
from time import time
from collections import namedtuple
from math import exp, sqrt
from sortedcontainers import SortedDict


_DEFAULT_SIZE = 1028
_DEFAULT_ALPHA = 0.015
_RESCALE_THRESHOLD = 60 * 60.0

_WeightedSample = namedtuple('WeightedSample', ['value', 'weight'])


class _WeightedSnapshot(object):
    def __init__(self, samples):
        sorted_samples = sorted(samples, key=attrgetter('value'))
        self.values = list(map(attrgetter('value'), sorted_samples))

        weight_sum = sum(sample.weight for sample in sorted_samples)
        self.normalized_weights = [sample.weight / weight_sum for sample in sorted_samples]
        self.quantiles = [0.0]
        for i in range(len(sorted_samples) - 1):
            self.quantiles.append(self.quantiles[i] + self.normalized_weights[i])

    def get_min(self):
        return self.values[0]

    def get_max(self):
        return self.values[-1]

    def get_mean(self):
        return sum(value * weight for value, weight in zip(self.values, self.normalized_weights))

    def get_sd(self):
        mean = self.get_mean()
        return sqrt(sum(weight * (value - mean)**2 for value, weight in zip(self.values, self.normalized_weights)))

    def get_quantile(self, q):
        idx = bisect(self.quantiles, q)
        try:
            return self.values[idx]
        except IndexError:
            return self.values[-1]


class ExponentiallyDecayingReservoir(object):
    def __init__(self, size=_DEFAULT_SIZE, alpha=_DEFAULT_ALPHA):
        self.size = size
        self.alpha = alpha
        self.start_time = time()
        self.next_scale_time = self.start_time + _RESCALE_THRESHOLD
        self.values = SortedDict()

    def _rescale_if_needed(self):
        now = time()
        if now > self.next_scale_time:
            self.next_scale_time = now + _RESCALE_THRESHOLD
            old_start_time = self.start_time
            self.start_time = time()
            scaling_factor = exp(-self.alpha * (self.start_time - old_start_time))

            self.values = SortedDict(
                (priority * scaling_factor, _WeightedSample(sample.value, sample.weight * scaling_factor))
                for priority, sample in self.values.items()
            )

    def update(self, value):
        timestamp = time()
        item_weight = exp(self.alpha * (timestamp - self.start_time))
        sample = _WeightedSample(value, item_weight)
        priority = item_weight / random()

        if len(self.values) < self.size:
            self.values[priority] = sample
        elif self.values.keys()[0] < priority:
            self.values.setdefault(priority, value)
            self.values.popitem()

    def get_snapshot(self):
        return _WeightedSnapshot(self.values.values())
