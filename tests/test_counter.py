from tests.base import StatsTest


class CounterTestCase(StatsTest):
    def test_counter_works(self):
        counter = self.registry.counter('CounterTestCase.test_counter_works')

        counter.increment()
        counter.increment(2)
        stats = self.registry.get_stats()
        assert stats.CounterTestCase.test_counter_works.value == 3

        counter.decrement(2)
        counter.decrement()
        stats = self.registry.get_stats()
        assert stats.CounterTestCase.test_counter_works.value == 0
