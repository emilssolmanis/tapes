from __future__ import print_function
from threading import Event, Thread

import abc
import tapes


class Reporter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry):
        self.registry = registry if registry is not None else tapes._global_registry

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ScheduledReporter(Reporter):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, interval):
        super(ScheduledReporter, self).__init__(registry)
        self.interval = interval
        self.thread = None
        self.termination_event = Event()

    @abc.abstractmethod
    def report(self):
        pass

    def start(self):
        def _report():
            while True:
                self.report()
                terminated = self.termination_event.wait(self.interval.total_seconds())
                if terminated:
                    return
        self.thread = Thread(target=_report)
        self.thread.start()

    def stop(self):
        self.termination_event.set()
        self.thread.join()
