from __future__ import print_function
import json
import os
import sys

from tornado import ioloop

from tapes.reporting.stream import Reporter


class TornadoStreamReporter(Reporter):
    def __init__(self, registry, interval, stream=sys.stdout, io_loop=None):
        super(TornadoStreamReporter, self).__init__(registry, interval)
        self.io_loop = io_loop if io_loop is not None else ioloop.IOLoop.current()
        self.timeout = None
        self.stream = stream

    def start(self):
        def _print_stats():
            json.dump(self.registry.get_stats(), self.stream)
            self.stream.write(os.linesep)
            self.timeout = self.io_loop.add_timeout(self.interval, _print_stats)
        self.io_loop.add_callback(_print_stats)

    def stop(self):
        if self.timeout:
            self.io_loop.remove_timeout(self.timeout)
