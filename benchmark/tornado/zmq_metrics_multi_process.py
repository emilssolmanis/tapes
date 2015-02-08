from time import sleep
from tornado import ioloop, web, httpserver, gen

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

    def _report(_registry):
        while True:
            sleep(100)

    RegistryAggregator(_report).start()

    server = httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)

    registry.connect()

    ioloop.IOLoop.current().start()
