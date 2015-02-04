from multiprocessing import Process
from tornado import ioloop, web, gen
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

    application.listen(8888)

    registry = DistributedRegistry()
    timer = registry.timer('my.timer')

    ioloop.IOLoop.instance().start()
