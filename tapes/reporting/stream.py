from __future__ import print_function
import json
import sys

import os

from . import ScheduledReporter


class ThreadedStreamReporter(ScheduledReporter):
    """Dumps JSON serialized metrics to a stream with an interval"""
    def __init__(self, interval, stream=sys.stdout, registry=None):
        """
        :param interval: a timedelta
        :param stream: the stream to write to, defaults to stdout
        :param registry: the registry to report from, defaults to the global one
        """
        super(ThreadedStreamReporter, self).__init__(interval, registry)
        self.stream = stream

    def report(self):
        stats = self.registry.get_stats()
        json.dump(stats, self.stream)
        self.stream.write(os.linesep)
