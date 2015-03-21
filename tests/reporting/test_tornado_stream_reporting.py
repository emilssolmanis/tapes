from datetime import timedelta
import json
import os
from six import StringIO
from tornado import gen, testing
from tapes.registry import Registry
from tapes.reporting.tornado.stream import TornadoStreamReporter


class TornadoConsoleReportingTestCase(testing.AsyncTestCase):
    @testing.gen_test
    def test_tornado_stream_reporting_writes_to_stream(self):
        registry = Registry()
        counter = registry.counter('some.tornado.path')
        counter.increment(66)

        s = StringIO()
        reporter = TornadoStreamReporter(timedelta(milliseconds=100), stream=s, registry=registry)
        reporter.start()
        yield gen.sleep(0.2)
        reporter.stop()

        reports = map(json.loads, s.getvalue().strip().split(os.linesep))
        assert all(r['some']['tornado']['path']['value'] == 66 for r in reports)
