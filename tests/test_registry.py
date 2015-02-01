from tests.base import StatsTest


class RegistryTestCase(StatsTest):
    def test_multiple_meter_calls_with_same_name_return_same_instance(self):
        meter1 = self.registry.meter('lol.hurr.durr.Meter')
        meter2 = self.registry.meter('lol.hurr.durr.Meter')
        assert id(meter1) == id(meter2)

    def test_multiple_timer_calls_with_same_name_return_same_instance(self):
        timer1 = self.registry.timer('lol.hurr.durr.Timer')
        timer2 = self.registry.timer('lol.hurr.durr.Timer')
        assert id(timer1) == id(timer2)

    def test_multiple_gauge_calls_with_same_name_return_same_instance(self):
        gauge1 = self.registry.gauge('lol.hurr.durr.Gauge', lambda: 0)
        gauge2 = self.registry.gauge('lol.hurr.durr.Gauge', lambda: 0)
        assert id(gauge1) == id(gauge2)

    def test_multiple_counter_calls_with_same_name_return_same_instance(self):
        counter1 = self.registry.counter('lol.hurr.durr.Counter')
        counter2 = self.registry.counter('lol.hurr.durr.Counter')
        assert id(counter1) == id(counter2)

    def test_multiple_histogram_calls_with_same_name_return_same_instance(self):
        histogram1 = self.registry.histogram('lol.hurr.durr.Histogram')
        histogram2 = self.registry.histogram('lol.hurr.durr.Histogram')
        assert id(histogram1) == id(histogram2)
