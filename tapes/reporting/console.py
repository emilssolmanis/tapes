from __future__ import print_function
import json
from threading import Thread, Event

import abc


class ConsoleReporter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, interval):
        self.registry = registry
        self.interval = interval

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ThreadedConsoleReporter(ConsoleReporter):
    def __init__(self, registry, interval):
        super(ThreadedConsoleReporter, self).__init__(registry, interval)
        self.thread = None
        self.termination_event = Event()

    def start(self):
        def _print_stats(registry, terminated_flag):
            while True:
                stats = registry.get_stats()
                print(json.dumps(stats))
                terminated = terminated_flag.wait(self.interval.total_seconds())
                if terminated:
                    return
        self.thread = Thread(target=_print_stats, args=(self.registry, self.termination_event))
        self.thread.start()

    def stop(self):
        self.termination_event.set()
        self.thread.join(0.0)
