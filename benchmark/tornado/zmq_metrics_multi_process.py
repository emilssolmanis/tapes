from tornado import ioloop, web, httpserver, gen

from tapes.reporting.http import HTTPReporter
from tapes.distributed.registry import DistributedRegistry, RegistryAggregator

registry = DistributedRegistry()


class TimedHandler(web.RequestHandler):
    timer = registry.timer('my.timer')

    @gen.coroutine
    def get(self):
        with TimedHandler.timer.time():
            self.write('finished')


if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    RegistryAggregator(HTTPReporter(8889)).start()

    server = httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)

    registry.connect()

    ioloop.IOLoop.current().start()
