from datetime import datetime
__version__ = '0.3.dev{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'))

try:
    # we need __version__ for setup.py, sphinx stuff, just to generally be nice, etc.,
    # but at the point of invocation in setup.py the dependencies imported in .registry are not installed
    # yet, so we do this
    from .registry import Registry
    _global_registry = Registry()

    meter = _global_registry.meter
    timer = _global_registry.timer
    gauge = _global_registry.gauge
    counter = _global_registry.counter
    histogram = _global_registry.histogram
    get_stats = _global_registry.get_stats
except ImportError:
    pass
