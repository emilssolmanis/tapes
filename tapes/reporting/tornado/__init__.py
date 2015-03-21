from tornado import ioloop

from .. import ScheduledReporter


class TornadoScheduledReporter(ScheduledReporter):
    """Scheduled reporter that uses a tornado IOLoop for scheduling"""
    def __init__(self, interval, registry=None, io_loop=None):
        """
        :param interval: a timedelta
        :param registry: the registry to report from, defaults to the global one
        :param io_loop: the io_loop to use, defaults to ``IOLoop.current()``
        """
        super(TornadoScheduledReporter, self).__init__(interval, registry)
        self.io_loop = io_loop if io_loop is not None else ioloop.IOLoop.current()
        self.timeout = None

    def start(self):
        def _report():
            self.report()
            self.timeout = self.io_loop.add_timeout(self.interval, _report)
        self.io_loop.add_callback(_report)

    def stop(self):
        if self.timeout:
            self.io_loop.remove_timeout(self.timeout)
            self.timeout = None
