from __future__ import print_function
import json

import sys

import os

from . import TornadoScheduledReporter


class TornadoStreamReporter(TornadoScheduledReporter):
    def __init__(self, interval, stream=sys.stdout, registry=None, io_loop=None):
        super(TornadoStreamReporter, self).__init__(registry, interval, io_loop)
        self.stream = stream

    def report(self):
        json.dump(self.registry.get_stats(), self.stream)
        self.stream.write(os.linesep)
