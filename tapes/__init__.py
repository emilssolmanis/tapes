from .registry import Registry

_registry = Registry()


meter = _registry.meter
timer = _registry.timer
gauge = _registry.gauge
counter = _registry.counter
histogram = _registry.histogram
get_stats = _registry.get_stats
