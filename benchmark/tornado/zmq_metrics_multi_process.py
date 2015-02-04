from multiprocessing import Process

from tornado import ioloop, web, httpserver, gen

from tapes.registry import DistributedRegistry, registry_aggregator


class TimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        with timer.time():
            self.write('finished')


if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    p = Process(target=registry_aggregator)
    p.start()

    server = httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)

    registry = DistributedRegistry()
    timer = registry.timer('my.timer')

    ioloop.IOLoop.current().start()
