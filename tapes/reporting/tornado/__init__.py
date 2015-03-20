from tornado import ioloop

from .. import ScheduledReporter


class TornadoScheduledReporter(ScheduledReporter):
    def __init__(self, interval, registry=None, io_loop=None):
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
