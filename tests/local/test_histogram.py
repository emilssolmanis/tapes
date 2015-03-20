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

    def test_empty_histogram_returns_sane_defaults(self):
        self.registry.histogram('HistogramTestCase.test_empty_histogram_returns_sane_defaults')
        stats = self.registry.get_stats()
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.min == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.max == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.stddev == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.mean == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.q50 == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.q75 == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.q98 == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.q99 == 0
        assert stats.HistogramTestCase.test_empty_histogram_returns_sane_defaults.q999 == 0
