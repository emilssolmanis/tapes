from __future__ import print_function
import json

import sys

import os

from . import TornadoScheduledReporter


class TornadoStreamReporter(TornadoScheduledReporter):
    """Writes JSON serialized metrics to a stream using an ``IOLoop`` for scheduling"""
    def __init__(self, interval, stream=sys.stdout, registry=None, io_loop=None):
        """
        :param interval: a timedelta
        :param stream: the stream to write to, defaults to stdout
        :param registry: the registry to report from, defaults to stdout
        :param io_loop: the IOLoop to use, defaults to ``IOLoop.current()``
        """
        super(TornadoStreamReporter, self).__init__(interval, registry, io_loop)
        self.stream = stream

    def report(self):
        json.dump(self.registry.get_stats(), self.stream)
        self.stream.write(os.linesep)
