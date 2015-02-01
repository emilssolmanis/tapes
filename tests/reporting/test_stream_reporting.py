from __future__ import print_function
from datetime import timedelta
import json
from time import sleep

import os
from six import StringIO
from six.moves import map

from tapes.reporting.stream import ThreadedStreamReporter
from tests.base import StatsTest


class StreamReportingTestCase(StatsTest):
    def test_threaded_stream_reporter_prints_stats_with_intervals(self):
        counter = self.registry.counter(
            'some.path'
        )

        counter.increment(42)

        s = StringIO()
        reporter = ThreadedStreamReporter(self.registry, timedelta(milliseconds=100), stream=s)
        reporter.start()
        sleep(0.2)
        reporter.stop()

        reports = map(json.loads, s.getvalue().strip().split(os.linesep))
        assert all(r['some']['path']['value'] == 42 for r in reports)
