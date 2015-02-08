from time import sleep
import requests
from tapes.distributed.registry import DistributedRegistry, RegistryAggregator
from tapes.distributed.reporting import http_reporter


def _pick_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_distributed_registry_logs_stuff():
    http_port = _pick_port()
    aggregator = RegistryAggregator(http_reporter(http_port))
    aggregator.start()

    # allow the aggregator to start up to get all the messages
    sleep(1)

    registry = DistributedRegistry()
    registry.connect()
    counter = registry.counter('my.counter')
    meter = registry.meter('my.meter')

    try:
        for _ in range(1000):
            meter.mark()
            counter.increment()

        sleep(1)

        response = requests.get('http://localhost:%d/' % http_port)
        assert response.status_code == 200
        print(response)
        stats = response.json()
        assert stats['my']['counter']['value'] == 1000
        assert stats['my']['meter']['count'] == 1000
    finally:
        aggregator.stop()
        registry.close()
