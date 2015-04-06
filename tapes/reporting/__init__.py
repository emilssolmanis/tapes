from __future__ import print_function
import logging
from threading import Event, Thread

import abc
import six
import tapes


reporting_logger = logging.getLogger('tapes.reporting')


@six.add_metaclass(abc.ABCMeta)
class Reporter(object):
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


@six.add_metaclass(abc.ABCMeta)
class ScheduledReporter(Reporter):
    """Super class for scheduled reporters. Handles scheduling via a ``Thread``."""
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
        reporting_logger.debug('Starting reporter %s', self.__class__.__name__)

        def _report():
            while True:
                self.report()
                terminated = self.termination_event.wait(self.interval.total_seconds())
                if terminated:
                    return
        self.thread = Thread(target=_report)
        self.thread.start()
        reporting_logger.debug('Started reporter %s', self.__class__.__name__)

    def stop(self):
        reporting_logger.debug('Stopping reporter %s', self.__class__.__name__)

        self.termination_event.set()
        self.thread.join()

        reporting_logger.debug('Stopped reporter %s', self.__class__.__name__)
