from time import sleep

import requests
from tornado.testing import bind_unused_port

from tapes.reporting.http import HTTPReporter
from tapes.distributed.registry import DistributedRegistry, RegistryAggregator


def test_distributed_registry_logs_stuff():
    sock, http_port = bind_unused_port()
    sock.close()

    aggregator = RegistryAggregator(HTTPReporter(http_port))
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
                # more than 200 messages behind...
                assert abs(stats['my']['counter']['value'] - num_messages) < 200
                assert abs(stats['my']['meter']['count'] - num_messages) < 200
                eventually_consistent = True
            except AssertionError:
                sleep(1)

        if not eventually_consistent:
            raise AssertionError('Counts are inconsistent: {} sent, {} received; dropping messages?'.format(
                num_messages,
                stats['my']['counter']['value']
            ))
    finally:
        aggregator.stop()
        registry.close()
