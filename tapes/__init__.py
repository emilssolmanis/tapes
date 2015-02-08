from .registry import Registry

_global_registry = Registry()

meter = _global_registry.meter
timer = _global_registry.timer
gauge = _global_registry.gauge
counter = _global_registry.counter
histogram = _global_registry.counter
get_stats = _global_registry.get_stats
