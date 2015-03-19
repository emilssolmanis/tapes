from __future__ import print_function
import json
import os
from threading import Thread, Event
import sys

from . import Reporter


class ThreadedStreamReporter(Reporter):
    def __init__(self, interval, stream=sys.stdout, registry=None):
        super(ThreadedStreamReporter, self).__init__(registry)
        self.interval = interval
        self.thread = None
        self.termination_event = Event()
        self.stream = stream

    def start(self):
        def _print_stats(registry, terminated_flag):
            while True:
                stats = registry.get_stats()
                json.dump(stats, self.stream)
                self.stream.write(os.linesep)
                terminated = terminated_flag.wait(self.interval.total_seconds())
                if terminated:
                    return
        self.thread = Thread(target=_print_stats, args=(self.registry, self.termination_event))
        self.thread.start()

    def stop(self):
        self.termination_event.set()
        self.thread.join(0.0)
