from __future__ import print_function
from threading import Event, Thread

import abc
import tapes


class Reporter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry=None):
        self.registry = registry if registry is not None else tapes._global_registry

    @abc.abstractmethod
    def start(self):
        """Starts reporting."""
        pass

    @abc.abstractmethod
    def stop(self):
        """Stops reporting."""
        pass


class ScheduledReporter(Reporter):
    """Super class for scheduled reporters. Handles scheduling via a ``Thread``."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, interval, registry=None):
        """Creates a reporter that reports with the given interval.

        Suitable for push style reporting. Uses a Python ``Thread`` for implementation, so reporting will block your
        application from doing anything else.

        :param interval: A ``timedelta`` instance
        :param registry: The registry to report from, defaults to the global one
        """
        super(ScheduledReporter, self).__init__(registry)
        self.interval = interval
        self.thread = None
        self.termination_event = Event()

    @abc.abstractmethod
    def report(self):
        """Override in subclasses.

        A Python ``Thread`` is used for scheduling, so whatever this ends up doing, it should be pretty fast.
        """
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
