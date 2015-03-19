from __future__ import print_function

import requests

from tornado.testing import bind_unused_port

from tapes.reporting.http import HTTPReporter
from tests.local.base import StatsTest


class HTTPReportingTestCase(StatsTest):
    def test_threaded_stream_reporter_prints_stats_with_intervals(self):
        counter = self.registry.counter('some.path')

        counter.increment(42)

        sock, http_port = bind_unused_port()
        sock.close()

        reporter = HTTPReporter(http_port, self.registry)
        reporter.start()

        response = requests.get('http://localhost:%d/' % http_port)
        assert response.status_code == 200
        stats = response.json()

        reporter.stop()

        assert stats['some']['path']['value'] == 42
