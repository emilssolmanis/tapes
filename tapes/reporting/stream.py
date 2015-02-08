from __future__ import print_function
import json
import os
from threading import Thread, Event

import abc
import sys
import tapes


class Reporter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, interval):
        self.registry = registry if registry is not None else tapes._global_registry
        self.interval = interval

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ThreadedStreamReporter(Reporter):
    def __init__(self, interval, stream=sys.stdout, registry=None):
        super(ThreadedStreamReporter, self).__init__(registry, interval)
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
