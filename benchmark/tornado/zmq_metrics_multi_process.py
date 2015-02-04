from multiprocessing import Process

import os
from tornado import ioloop, web, httpserver, gen

from tapes.registry import DistributedRegistry, registry_aggregator


class TimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        with timer.time():
            if self.get_argument('dump', default=False):
                self.finish(registry.get_stats())
            else:
                self.write('finished')


if __name__ == "__main__":
    print('main PID %s' % os.getpid())

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
