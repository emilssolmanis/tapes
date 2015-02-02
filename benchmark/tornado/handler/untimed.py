from tornado import web, gen


class UntimedHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write('finished')
