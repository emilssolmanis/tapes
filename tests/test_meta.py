import unittest
import abc
import pytest
import six
from tapes import Registry
from tapes.meta import metered_meta


registry = Registry()


class ClassWithMeta(six.with_metaclass(
    metered_meta([('latency', 'some.path.{}.latency', registry.timer)])
)):
    def foo(self):
        with self.latency.time():
            pass


class AbstractClass(six.with_metaclass(
    metered_meta([('rate', 'some.path.{}.rate', registry.meter)], base=abc.ABCMeta)
)):
    @abc.abstractmethod
    def foo(self):
        pass


class ImplSubClass(AbstractClass):
    def foo(self):
        self.rate.mark()


class MetricsMetaTestCase(unittest.TestCase):
    def test_meta_adds_right_metrics_to_class_and_subclass(self):
        assert ClassWithMeta.latency is not None

        instance = ClassWithMeta()
        instance.foo()
        instance.foo()

        stats = registry.get_stats()
        timer_stats = stats.some.path.ClassWithMeta.latency

        assert timer_stats.count == 2

        assert timer_stats.mean is not None
        assert timer_stats.stddev is not None
        assert timer_stats.min is not None
        assert timer_stats.max is not None

        assert timer_stats.q50 is not None
        assert timer_stats.q75 is not None
        assert timer_stats.q95 is not None
        assert timer_stats.q98 is not None
        assert timer_stats.q99 is not None
        assert timer_stats.q999 is not None

    def test_meta_with_non_default_base_calls_super(self):
        with pytest.raises(TypeError):
            AbstractClass()

        t = ImplSubClass()
        t.foo()
        t.foo()

        stats = registry.get_stats()
        meter_stats = stats.some.path.ImplSubClass.rate

        assert meter_stats.count == 2

        assert meter_stats.m1 is not None
        assert meter_stats.m5 is not None
        assert meter_stats.m15 is not None
