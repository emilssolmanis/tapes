from tests.local.base import StatsTest


class HistogramTestCase(StatsTest):
    def test_histogram_works(self):
        histogram = self.registry.histogram('HistogramTestCase.test_histogram_works')
        histogram.update(1)
        histogram.update(2)
        histogram.update(2)
        histogram.update(1)

        stats = self.registry.get_stats()
        assert stats.HistogramTestCase.test_histogram_works.min == 1
        assert stats.HistogramTestCase.test_histogram_works.max == 2
        assert abs(stats.HistogramTestCase.test_histogram_works.mean - 1.5) < 0.01
