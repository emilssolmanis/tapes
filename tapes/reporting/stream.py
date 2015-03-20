from __future__ import print_function
import json
import sys

import os

from . import ScheduledReporter


class ThreadedStreamReporter(ScheduledReporter):
    def __init__(self, interval, stream=sys.stdout, registry=None):
        super(ThreadedStreamReporter, self).__init__(interval, registry)
        self.stream = stream

    def report(self):
        stats = self.registry.get_stats()
        json.dump(stats, self.stream)
        self.stream.write(os.linesep)
