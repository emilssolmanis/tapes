from greplin import scales
from tornado import ioloop, web, gen


STATS = scales.collection('/web',
                          scales.PmfStat('latency'))


class TimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        with STATS.latency.time():
            self.write('finished')


if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    application.listen(8888)
    ioloop.IOLoop.instance().start()
