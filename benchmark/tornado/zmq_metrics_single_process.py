from tornado import ioloop, web, gen

from tapes.reporting.http import HTTPReporter
from tapes.distributed.registry import DistributedRegistry, RegistryAggregator

registry = DistributedRegistry()
registry.connect()
timer = registry.timer('my.timer')


class TimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        with timer.time():
            self.write('finished')

if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    RegistryAggregator(HTTPReporter(8889)).start()

    application.listen(8888)

    ioloop.IOLoop.instance().start()
