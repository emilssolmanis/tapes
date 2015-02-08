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
    http_up = False
    for _ in range(10):
        try:
            requests.get('http://localhost:%d/' % http_port)
            http_up = True
            break
        except requests.ConnectionError:
            sleep(0.5)

    if http_up:
        # http is up, wait a bit for the actual socket
        sleep(1)
    else:
        raise AssertionError('Failed to start registry aggregator')

    registry = DistributedRegistry()
    registry.connect()
    counter = registry.counter('my.counter')
    meter = registry.meter('my.meter')

    try:
        num_messages = 1000
        for _ in range(num_messages):
            meter.mark()
            counter.increment()

        eventually_consistent = False
        for _ in range(10):
            try:
                response = requests.get('http://localhost:%d/' % http_port)
                assert response.status_code == 200
                stats = response.json()
                # TODO: 0MQ batches the sends, and there's no reliable way to test this afaik. Just make sure it's no
                # more than 100 messages behind...
                assert abs(stats['my']['counter']['value'] - num_messages) < 100
                assert abs(stats['my']['meter']['count'] - num_messages) < 100
                eventually_consistent = True
            except AssertionError:
                sleep(0.5)

        if not eventually_consistent:
            raise AssertionError('Counts are inconsistent; dropping messages?')
    finally:
        aggregator.stop()
        registry.close()
