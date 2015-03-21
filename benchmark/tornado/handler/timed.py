from tornado import web, gen
from tapes.registry import Registry

registry = Registry()
timer = registry.timer('my.timer')


class TimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        with timer.time():
            self.write('finished')
